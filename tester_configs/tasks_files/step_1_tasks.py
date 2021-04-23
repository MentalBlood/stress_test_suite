input_variables = [
	"requests_number",
	"parallel_requests_number"
]

tasks = lambda: [
	{
		"commands_to_execute": [
			"python simpleStressTest.py -r %s -p %s" % (requests_number, parallel_requests_number)
		],
		"init_file": "tester_configs.init_files.step_1_init_file",
		"watch_functions_file": "tester_configs.watch_functions_files.step_1_watch_functions",
		"delay": 1,
		"stop_when_values": [requests_number] * 3,
		"windows_to_close_names": [
			"cod - start_cod.cmd",
			"mrcod - start_mrcod.cmd"
		]
	}
]