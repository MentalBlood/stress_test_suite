input_variables = [
	"requests_number",
	"parallel_requests_number"
]

tasks = lambda: [
	{
		"commands_to_execute": [
			"rmdir /S /Q compiled_templates",
			"mkdir compiled_templates",
			"compileTemplates.exe",
			"psql --host=10.1.13.130 --username=testuser < clearTables_postgresql.sql",
			"rd /s /q cod\\fs",
			"del mrcod\\log.txt",
			"del cod\\log.txt",
			{
				"command": "start_cod.cmd",
				"window_name": "cod"
			},
			{
				"command": "start_mrcod.cmd",
				"window_name": "mrcod"
			},
			{
				"command": "start_vizualization_server.cmd",
				"window_name": "vizualization_server"
			},
			{
				"command": "start_vizualization_client.cmd",
				"window_name": "vizualization_client"
			},
			"timeout 1"
		],
		"subtasks": [
			{
				"commands_to_execute": [
					{
						"command": "python simpleStressTest.py -r %s -p %s" % (requests_number, parallel_requests_number),
						"window_name": "stress_test"
					}
				],
				"init_file": "tester_configs.init_files.step_1_init_file",
				"watch_functions_file": "tester_configs.watch_functions_files.step_1_watch_functions",
				"delay": 1,
				"stop_when_values": [requests_number] * 3 + [int(requests_number) * 3] + [requests_number] * 2
			},
			{
				"commands_to_execute": [
					{
						"command": "python simpleStressTest.py -u http://10.1.13.136:8001/test/ --request_kwargs tester_configs.request_kwargs_files.step_2_request_kwargs -r %s -p %s" % (requests_number, parallel_requests_number),
						"window_name": "stress_test"
					}
				],
				"init_file": "tester_configs.init_files.step_2_init_file",
				"watch_functions_file": "tester_configs.watch_functions_files.step_2_watch_functions",
				"delay": 1,
				"stop_when_values": [requests_number] * 5 + [int(requests_number) * 3],
				"windows_to_close_names": [
					"cod",
					"mrcod",
					{
						"name": "vizualization_server",
						"delay": 2
					}
				]
			}
		]
	}
]