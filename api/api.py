import dis
import os
from io import StringIO
import ast_node
import sys
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/dis')
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
	target_py = "pseudo_code.txt"

	try:
		dis_code = ""
		ast_node.parse_pseudo_code(source_py)
		file = open('pseudo_code.txt','r')
		dis_code = file.read()
		file.close()
		
		print(dis_code)	
	except:
		print(sys.exc_info()[0])
		print("The ast tree generated error.")

	
	# byte_code = compile(source_code, source_py, "exec")
	# dis_code = dis.Bytecode(byte_code).dis()
	# print("Dissembly Code:\n",dis_code)

	# for x in byte_code.co_consts:
	# 	if isinstance(x, types.CodeType):
	# 		sub_byte_code = x
	# 		func_name = sub_byte_code.co_name
	# 		print('\nDisassembly of %s:' % func_name)
	# 		dis.dis(sub_byte_code)

	return jsonify(code=str(dis_code))
 
