from common.db_tools import *

def countRowsFunction(table_name):
	def f():
		new_cursor = conn.cursor()
		return getRowsNumber(new_cursor, table_name)
	return f

def countDeletedDbRowsFunction(table_name):
	def f():
		new_cursor = conn.cursor()
		return initial_rows_number[table_name] - getRowsNumber(new_cursor, table_name)
	return f

def countMarkedAsDeletedDbRowsFunction(table_name):
	def f():
		new_cursor = conn.cursor()
		return getMarkedRowsNumber(new_cursor, table_name, 'deleted=true')
	return f

countDeletedXmlFiles = lambda: initial_files_number - countFiles('cod/fs', lambda f: f.split('.')[-1] == 'gz')

def countInFileFunction(file_path, substring):
	def f():
		result = None
		with open(file_path) as file:
			result = file.read().count(substring)
		return result
	return f

watch_functions = [
	('accept requests', countInFileFunction('mrcod/log.txt', '/test/accept HTTP/1.1[0m" 201')),
	('ticket_accept requests', countInFileFunction('cod/log.txt', '/test/ticket_accept HTTP/1.1[0m" 201')),
	('messages files deleted', countDeletedXmlFiles),
	('messages_metadata rows marked as deleted', countMarkedAsDeletedDbRowsFunction('messages_metadata')),
	('messages_metadata rows left', countRowsFunction('messages_metadata')),
	('messages_and_addresses rows deleted', countDeletedDbRowsFunction('messages_and_addresses'))
]