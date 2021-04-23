from common.db_tools import *
from logger import *

print('reseting log')
resetLog()
print('log reseted')

def init():
	result = {}
	result['conn'] = connect()
	return result

def after(init_result):
	init_result['conn'].close()