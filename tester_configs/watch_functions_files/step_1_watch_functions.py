from countFiles import countFiles
import re
from common.db_tools import *

from logger import *

filter_function = lambda f: f.split('.')[-1] == 'gz'
countXmlFiles = lambda: countFiles('cod/fs', filter_function)

def countDbRowsFunction(table_name):
	def countDbRows():
		new_cursor = conn.cursor()
		result = getRowsNumber(new_cursor, table_name)
		new_cursor.close()
		return result
	return countDbRows

def countInFileFunction(file_path, substring):
	def f():
		result = -1
		try:
			with open(file_path) as file:
				result = file.read().count(substring)
		except:
			pass
		return result
	return f

def countUniqueInFileFunction(file_path, substring):
	def f():
		file_text = ''
		with open(file_path) as file:
			file_text = file.read()
		values_starts = [m.end() for m in re.finditer(var_name + ' ', file.read())]
		values_ends = [s.find('\n', start) for start in values_starts]
		values = [s[s_e[0]:s_e[1]] for s_e in zip(values_starts, values_ends)]
		return len(set(values))
	return f

watch_functions = [
	('valid xml requests', countLogsFunction('message is ok')),
	('valid xml responses', countLogsFunction('response is ok')),
	('messages_metadata rows', countDbRowsFunction('messages_metadata')),
	('messages_and_addresses rows', countDbRowsFunction('messages_and_addresses')),
	('xml files', countXmlFiles),
	('ticket_message requests', countInFileFunction('mrcod/log.txt', '/test/ticket_message HTTP/1.1[0m" 201')),
]