from tqdm import tqdm
from multiprocessing.pool import ThreadPool
import requests
import argparse
import sys
import random
from import_tools import importModuleItself

parser = argparse.ArgumentParser(description='do stress test')
parser.add_argument('-r', type=str,
                    help='total number of requests to make', default=1000)
parser.add_argument('-p', type=str,
                    help='number of parallel requests', default=100)
parser.add_argument('-u', type=str,
                    help='URL', default='http://10.1.13.136:8002/test/')
parser.add_argument('--request_kwargs', type=str,
					help='get request kwargs function file', default='tester_configs.request_kwargs_files.step_1_request_kwargs')
args = parser.parse_args()

def importModuleItself(addr):
	module = __import__(addr)
	temp_result = module
	addr_as_list = addr.split('.')
	for submodule in addr_as_list[1:]:
		temp_result = getattr(temp_result, submodule)
	return temp_result

requests_number = int(args.r)
parallel_requests_number = int(args.p)
url = args.u
get_request_kwargs_function = importModuleItself(args.request_kwargs).getRequestKwargs

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def requests_retry_session(
	retries=3,
	backoff_factor=0.3,
	status_forcelist=(500, 502, 504),
	session=None,
):
	session = session or requests.Session()
	retry = Retry(
		total=retries,
		read=retries,
		connect=retries,
		backoff_factor=backoff_factor,
		status_forcelist=status_forcelist,
	)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	return session

def makeRequest(n, url, attempts, timeout):
	request_kwargs = get_request_kwargs_function(n)
	return requests_retry_session(retries=attempts).get(url, timeout=timeout, **request_kwargs)

def simpleStressTest(url, requests_number, threads):
	print('simpleStressTest', url, requests_number, threads)
	requests_urls = [url] * requests_number
	for result in tqdm(ThreadPool(threads).imap_unordered(lambda n_url: makeRequest(n_url[0], n_url[1], 100500, 100500), enumerate(requests_urls)), 
			desc='sending requests', total=len(requests_urls)):
		# print(result)
		pass

simpleStressTest(url, requests_number, parallel_requests_number)