from common.db_tools import *
from countFiles import countFiles

def init():
	result = {}
	result['conn'] = connect()
	cursor = result['conn'].cursor()
	result['initial_rows_number'] = {
		name: getRowsNumber(cursor, name)
		for name in [
			'messages_metadata',
			'messages_and_addresses'
		]
	}
	result['initial_files_number'] = countFiles('cod/fs', lambda f: f.split('.')[-1] == 'gz')
	return result

def after(init_result):
	init_result['conn'].close()