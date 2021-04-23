from common.db_tools import *
from logger import *

from xml_generator.main import *

def generateBoxShipmentNotification(tasks_ids):
	header = {
		'lifecycle_id': '1000230022021021800000002',
		'addressing_to': [
			'100000003',
			'100000004',
			'100000005'
		],
		'from_address': 'http://www.any.com/circum/regemque',
		'reply_to_address': 'http://www.test.com/foedere/ferant',
		'service_name': 'qname',
		'message_id': '1000000032021021800005059',
		'Security': {
			'created': '2016-10-07T18:24:19+03:00',
			'expires': '2002-11-05T11:30:58',
			'CanonicalizationMethod': {
				'ignore_comments': 'false',
				'trim_text_nodes': 'true',
				'prefix_rewrite': 'sequential',
				'qname_aware_element': 'http://www.sample.edu/soror/abdidit',
				# 'qname_aware_qualified_attr': 'some attr'
			},
			'Reference': [{
					'ignore_comments': 'false',
					'trim_text_nodes': 'true',
					'prefix_rewrite': 'sequential',
					'qname_aware_element': 'http://www.sample.edu/soror/abdidit',
					# 'qname_aware_qualified_attr': 'some attr',
					'digest_method': 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411',
					'digest_value': 'YXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXQ='
				},{
					'ignore_comments': 'true',
					'trim_text_nodes': 'false',
					'prefix_rewrite': 'sequential',
					'qname_aware_element': 'http://www.sample.edu/soror/abdidit',
					# 'qname_aware_qualified_attr': 'some attr',
					'digest_method': 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411',
					'digest_value': 'YXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXQ='
				},{
					'ignore_comments': 'true',
					'trim_text_nodes': 'true',
					'prefix_rewrite': 'sequential',
					'qname_aware_element': 'http://www.sample.edu/soror/abdidit',
					# 'qname_aware_qualified_attr': 'some attr',
					'digest_method': 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:gostr3411',
					'digest_value': 'YXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXQ='
				}
			],
			'signature_value': 'aW1wb3N1aXRpbXBvc3VpdGltcG9zdWl0aW1wb3N1aXRpbXBvc3VpdGltcG9zdWl0aW1wb3N1aXRpbXBvc3VpdA==',
			'certificate': 'YXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpc2F0cmlzYXRyaXNhdHJpcw==',
			'EncryptedKey': [{
					'encryption_method': 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:transport-gost2012-512',
					'IssuerSerial': {
						'name': 'string',
						'serial': '100'
					},
					'cipher_value': 'c29ub3Jhcw==',
					'DataReference': [
						{'uri': 'string1'},
						{'uri': 'string1'},
						{'uri': 'string1'}
					]
				},{
					'encryption_method': 'urn:ietf:params:xml:ns:cpxmlsec:algorithms:transport-gost2012-512',
					'IssuerSerial': {
						'name': 'string',
						'serial': '100'
					},
					'cipher_value': 'c29ub3Jhcw==',
					'DataReference': [
						{'uri': 'string1'},
						{'uri': 'string1'},
						{'uri': 'string1'}
					]
				}
			],
		}
	}
	return [fillTemplate('BoxShipmentNotification', {
		'Header': header,
		'box_id': '100',
		'DocumentEntry': {
			'document_type': 'PR',
			'document_number': 'stringstr',
			'task_id': t_id,
			'blank_id': 'string'
		}
	}) for t_id in tasks_ids]

initial_messages_ids = getAllMessagesIds()
def takeMessagesIds(n):
	return initial_messages_ids[:n]

def getRequestKwargs(n):
	messages_ids = takeMessagesIds(1)
	return {
		'data': generateBoxShipmentNotification(messages_ids)
	}
	# return {
	# 	'json': str(result)
	# }