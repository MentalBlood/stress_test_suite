import argparse
import time
import json
import os
import requests
from tqdm.auto import tqdm
from multiprocessing.pool import ThreadPool
from types import FunctionType
from import_tools import importModuleItself

parser = argparse.ArgumentParser(description='do stress test')
parser.add_argument('input_variables_values', metavar='INPUT', type=str, nargs='*',
					help='task input variables values')
parser.add_argument('--tasks', type=str,
					help='tasks file path', default='tester_configs.tasks_files.steps_1_2_tasks')
args = parser.parse_args()

input_variables_values = args.input_variables_values
tasks_file_path = args.tasks


def appendSpaces(s, max_length):
	return s + ' ' * (max_length - len(s))

vizualization_server_address = 'http://10.1.13.136:8003'

def updateBarsOnVizualizationServer(bars):
	bars_info = {b.desc.strip(): {
		'current': b.n,
		'total': b.total,
		'elapsed': b.format_dict['elapsed'],
		'average_speed': b.n / (b.format_dict['elapsed'] + 0.001),
		'chart_data': b.chart_data
	} for b in bars}
	json_to_send = {
		'name': 'template',
		'data': bars_info
	}
	requests.post(
		vizualization_server_address + '/set',
		headers={
			'content-type': 'application/json; charset=utf-8',
			'Access-Control-Allow-Origin': '*'
		},
		json=json_to_send
	)

def getDelta(chart_data, field_name, current):
	last = 0 if len(chart_data) == 0 else chart_data[-1][field_name]
	return current - last

def watch(watch_functions, stop_when_values, delay, additional_variables):
	global_variables = {**globals(), **additional_variables}
	watch_functions = list(map(lambda name_and_function:
		(name_and_function[0], FunctionType(name_and_function[1].__code__, global_variables, closure=name_and_function[1].__closure__)), watch_functions))

	max_function_description_length = max(map(lambda w_f: len(w_f[0]), watch_functions))
	bars = [tqdm(
		total=int(stop_when_values[i]),
		desc=appendSpaces(watch_functions[i][0], max_function_description_length),
	) for i in range(len(watch_functions))]
	threads_number = len(watch_functions)
	for b in bars:
		b.chart_data = []
	while True:
		# conn.commit()
		results = list(ThreadPool(threads_number).map(lambda w_f: w_f[1](), watch_functions))
		for i in range(len(results)):
			bars[i].update(results[i] - bars[i].n)
			current_elapsed = bars[i].format_dict['elapsed']
			current_current = bars[i].n

			bars[i].chart_data.append({
				'elapsed': current_elapsed,
				'current': current_current,
				'average_speed': getDelta(bars[i].chart_data, 'current', current_current) / (getDelta(bars[i].chart_data, 'elapsed', current_elapsed) + 0.0001)
			})
		updateBarsOnVizualizationServer(bars)
		if all(map(lambda b: b.n == b.total, bars)):
			break
		time.sleep(delay - time.time() % delay)
	for b in bars:
		b.close()

def closeWindows(names):
	for n in names:
		if type(n) == dict:
			os.system('timeout %s & taskkill /F /FI "WindowTitle eq %s" /T > nul' % (n['delay'], n['name']))
		elif type(n) == str:
			os.system('taskkill /F /FI "WindowTitle eq %s" /T > nul' % n)


def processTask(task, input_variables):
	additional_variables = input_variables

	if 'init_file' in task:
		init_module = importModuleItself(task['init_file'])
		init_result = init_module.init()
		additional_variables = {**additional_variables, **init_module.__dict__, **init_result}

	if 'commands_to_execute' in task:
		commands_to_execute = task['commands_to_execute']
		for c in commands_to_execute:
			print('executing command "%s"' % c)
			if type(c) == str:
				os.system(c)
			elif type(c) == dict:
				command = c['command']
				window_name = c['window_name']
				os.system('start "%s" cmd /c "%s & %s"' % (
					window_name, 
					command,
					"timeout -1" if ('dont close' in c) else "exit"
				))

	if 'watch_functions_file' in task:
		watch_functions_module = importModuleItself(task['watch_functions_file'])
		watch_functions = watch_functions_module.watch_functions
		additional_variables = {**additional_variables, **watch_functions_module.__dict__}
		watch(watch_functions, task['stop_when_values'], task['delay'], additional_variables)
		# time.sleep(1)

	if 'init_file' in task:
		init_module.after(init_result)

	if 'windows_to_close_names' in task:
		closeWindows(task['windows_to_close_names'])

	if 'subtasks' in task:
		for st in subtasks:
			processTask(st)


def flattenRecursiveTasks(tasks):
	result = []
	for t in tasks:
		result.append({k: t[k] for k in t if k != 'subtasks'})
		if 'subtasks' in t:
			result += flattenRecursiveTasks(t['subtasks'])
	return result

def processTasks(file_path, input_variables_values):
	tasks_module = importModuleItself(tasks_file_path)
	input_variables = { **dict(zip(tasks_module.input_variables, input_variables_values)), **globals() }
	tasks = FunctionType(tasks_module.tasks.__code__, input_variables)()
	flatten_tasks = flattenRecursiveTasks(tasks)
	for t in flatten_tasks:
		processTask(t, input_variables)


processTasks(tasks_file_path, input_variables_values)