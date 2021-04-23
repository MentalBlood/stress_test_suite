from flask import Flask, request, render_template, Response, jsonify
from flask_restful import Resource, Api
from logging.config import dictConfig
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

elements_data = {'template': {}}

@app.route('/get', methods=['POST'])
def get_element():
	element_name = request.get_json()['name']
	element_path = element_name + '.html'
	
	global elements_data
	data = elements_data[element_name]

	return Response(json.dumps(data), status=200)

def setData(element_name, new_data):
	global elements_data
	for key, value in new_data.items():
		elements_data[element_name][key] = value

@app.route('/set', methods=['POST'])
def set_data():
	request_json = request.get_json()
	element_name = request_json['name']
	data = request_json['data']
	print('set_data', data)
	setData(element_name, data)
	
	return Response(status=200)

if __name__ == '__main__':
	app.run('10.1.13.136', port=8003)