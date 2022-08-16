import os
from io import StringIO
import ast_node
import py_flowchart
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/llc')
def dis_python_code():
	py_code = request.args.get('code')
	print(py_code)
	py_code = py_code.replace("(enter)","\r\n")
	py_code = py_code.replace("(tab)","\t")
	py_code = py_code.replace("(add)","+")

	file = open("source_code.txt",'w')
	file.write(py_code)
	file.close()

	file_name = "source_code.txt"
	base = os.path.splitext(file_name)[0]
	os.rename(file_name, base + '.py')

	source_py = "source_code.py"
	py_2_llc_map = []
	dis_code = ""
	try:
		py_2_llc_map = ast_node.parse_pseudo_code(source_py)
		file = open('pseudo_code.txt','r')
		dis_code = file.read()
		file.close()
		print(dis_code)	
	except:
		print(sys.exc_info()[0])
		print("The ast tree generated error.")

	return jsonify(code=str(dis_code),map=py_2_llc_map)

@app.route('/fc')
def fc_sample():

	py_code = request.args.get('code')
	# print(py_code)

	py_code = "def Module():\n\t"+ py_code
	py_code = py_code.replace("(enter)","\r\n\t")
	py_code = py_code.replace("(tab)","\t\t")
	py_code = py_code.replace("(add)","+")

	file = open("source_code.txt",'w')
	file.write(py_code)
	file.close()

	file_name = "source_code.txt"
	base = os.path.splitext(file_name)[0]
	os.rename(file_name, base + '.py')

	source_py = "source_code.py"

	os.system("python3 py_flowchart/main.py {0} > flowchart.txt".format(source_py))

	with open('flowchart.txt') as file:
		fc_code = file.read()

	return jsonify(code=str(fc_code))
	
if __name__ == "__main__":
	app.run()