import ast
from dataclasses import astuple
from pprint import pprint
from tokenize import Name
from xml.dom.minidom import Attr

import astunparse

def incremental_pseudo():
    global PSEUDO_INDEX
    PSEUDO_INDEX = PSEUDO_INDEX + 1

def incremental_py():
    global PY_INDEX
    PY_INDEX = PY_INDEX + 1

def incremental_index():
    global LABEL_INDEX
    LABEL_INDEX = LABEL_INDEX + 1

def generate_tab(number):
    tab_list = []
    for i in range(number):
        tab_list.append("   ")
    return "".join(tab_list)

def loop_cond_expr(node):
    source = astunparse.unparse(node)
    statement = source.strip()
    lines = statement.splitlines()
    if len(lines) >= 1:
        return lines[0].rstrip(":")
    else:
        return True

def while_cond_args(node,label):
    cond = loop_cond_expr(node)
    cond = cond.split("while")[1]
    row = "if "+ cond + " is satisfied, run the code below. Otherwise, go to "+ label 
    return row

def for_cond_args(node,label):
    cond = loop_cond_expr(node)
    cond = cond.split("for")[1]
    row = "if" + cond + " is satisfied, run the code below. Otherwise, go to "+ label 
    return row

#parse the operation
def operation_label(node):
    if isinstance(node,ast.Add):
        return "+"
    elif isinstance(node,ast.Mult):
        return "*"
    elif isinstance(node,ast.Div):
        return "/"
    elif isinstance(node,ast.Sub):
        return "-"

#for whileLoop
def cmp_label(node):
    if isinstance(node,ast.LtE):
        return "is greater than"
    elif isinstance(node,ast.GtE):
        return "is lower than"
    elif isinstance(node,ast.Lt):
        return "is greater than or equal to"
    elif isinstance(node,ast.Gt):
        return "is lower than or equal to"
    elif isinstance(node,ast.Eq):
        return "is not equal to"

def assign_id_or_value(node):
    if isinstance(node,ast.Constant):
        return node.value
    elif isinstance(node,ast.Name):
        return node.id

def cond_expr(node):    
        source = astunparse.unparse(node)
        loop_statement = source.strip()
        lines = loop_statement.splitlines()
        if len(lines) >= 1:
            return lines[0].rstrip(':')
        else:
            return 'True'

def parseIfCondition(tab,node,label):
    row = generate_tab(tab) + cond_expr(node) + " run the code below. If not satified, then go to " + label + "\n"
    return row

def parseAssign(tab,node):
    if isinstance(node,ast.BinOp) :
        #If left_node is not null, left_node will be _ast.BinOp
        left_node_is_null = isinstance(node.left,ast.Name) or isinstance(node.left,ast.Constant) or isinstance(node.left,ast.Num)
        right_node_is_null = isinstance(node.right,ast.Name) or isinstance(node.right,ast.Constant) or isinstance(node.right,ast.Num)
        if left_node_is_null and right_node_is_null:   
            result = astunparse.unparse(node).strip().splitlines()[0]
            row = generate_tab(tab) + result + "\n"
            print(row)
            file.write(row)
            incremental_pseudo()
            return result

        elif left_node_is_null == False and right_node_is_null == False:

            left_node =str(parseAssign(tab,node.left))
            right_node = str(parseAssign(tab,node.right))
            result = left_node + " "+ operation_label(node.op) + " "+ right_node 
            row = generate_tab(tab)+ result + "\n"
            file.write(row)
            incremental_pseudo()
            return result

        elif left_node_is_null == True :
            left_node = str(assign_id_or_value(node.left))
            right_node = str(parseAssign(tab,node.right))
            result = left_node + " "+ operation_label(node.op) + " "+ right_node
            row = generate_tab(tab)+result + "\n"
            file.write(row) 
            incremental_pseudo()
            return result

        elif right_node_is_null == True :
            left_node =str(parseAssign(tab,node.left))
            right_node = str(assign_id_or_value(node.right))
            result = left_node + " "+ operation_label(node.op) + " "+ right_node
            row = generate_tab(tab)+ result + "\n"
            file.write(row)
            incremental_pseudo()
            return result

    elif isinstance(node,ast.Name):
        return node.id
    elif isinstance(node,ast.Constant):
        return node.value
    elif isinstance(node,ast.Num):
        return node.n

#_ast.Assign 
#Consider the value is _ast.Call or _ast.BinOp
def parseAssignWrapper(tab,node):
    el_pseudo_index = []
    start_point = PSEUDO_INDEX
    if isinstance(node.value,ast.Call):
        print(node)
        el_pseudo_index = parseExpr(tab,node)
        incremental_pseudo()
        row = "The result above will be assigned to " + node.targets[0].id
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()
        return el_pseudo_index
    
    result = str(parseAssign(tab,node.value))
    row = generate_tab(tab) + node.targets[0].id + " " + "=" + " "+result + "\n"
    file.write(row)
    incremental_pseudo()

    for i in range(start_point,PSEUDO_INDEX):
        el_pseudo_index.append(i)
    
    return el_pseudo_index

#_ast.For   
def parseForLoop(tab,node):
    el_pseudo_index = []
    label_index = LABEL_INDEX
    for_label = "LABEL{0}".format(label_index)
    row = for_label + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    
    incremental_pseudo()
    

    #The args
    if node.iter:
        cond = for_cond_args(node,"LABEL{0}".format(label_index + 1))
        row = generate_tab(tab) + cond + "\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()

    #A loop structure will have two labels, index should be increased twice.
    incremental_index()
    incremental_index()
    parse_body(tab + 1,node.body)

    #modify the iter number
    #
    #
    #

    row = generate_tab(tab + 1) + "Iterate the next element"+"\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    row = generate_tab(tab + 1) + "goto " + for_label + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    row = "LABEL{0}".format(label_index+1) + "\n"
    file.write(row)
    # el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()
    incremental_index()

    return el_pseudo_index

#_ast.While
def parseWhileLoop(tab,node):
    el_pseudo_index = []
    label_index = LABEL_INDEX
    while_label = "LABEL{0}".format(label_index)

    row = while_label + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    #The args
    if isinstance(node.test,ast.Compare):
        cond = while_cond_args(node,"LABEL{0}".format(label_index + 1))
        row = generate_tab(tab)+ cond + "\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()
    
    #A loop structure contains two labels
    incremental_index()
    incremental_index()
    parse_body(tab + 1,node.body)

    row = generate_tab(tab + 1) +"goto " + while_label + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    row ="LABEL{0}".format(label_index+1) + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()
    incremental_index()

    return el_pseudo_index

#_ast.Expr
def parseExpr(tab,node):
    el_pseudo_index = []
    if node.value and isinstance(node.value,ast.Call):
        row = generate_tab(tab)+"call function "+ node.value.func.id + "\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()

        if node.value.args == []:
            return el_pseudo_index

        plural = True if len(node.value.args) >= 2 else False
        if plural:
            args = []
            for arg in node.value.args:
                if isinstance(arg,ast.Constant):
                    args.append(arg.value)
                elif isinstance(arg,ast.Name):
                    args.append(arg.id)
                elif isinstance(arg,ast.Str):
                    args.append(args.s)

            args = " ".join([arg for arg in args])
            row = generate_tab(tab)+ "input args: " + args + "\n"
            file.write(row)
            el_pseudo_index.append(PSEUDO_INDEX)
            incremental_pseudo()
        else:
            if(hasattr(node.value.args[0],"id")): #_ast.Name
                row = generate_tab(tab)+ "input arg:" + str(node.value.args[0].id) + "\n"
            elif(hasattr(node.value.args[0],"value")): #_ast.Constant
                row = generate_tab(tab)+ "input arg:" + str(node.value.args[0].value) + "\n"
            elif(hasattr(node.value.args[0],"s")): #_ast.String
                row = generate_tab(tab)+ "input arg:" + str(node.value.args[0].s) + "\n"
            file.write(row)
            el_pseudo_index.append(PSEUDO_INDEX)
            incremental_pseudo()
    return el_pseudo_index

#_ast.If
def parseIfElse(tab,node):
    el_pseudo_index = []
    label_index = LABEL_INDEX
    if_else_label = "LABEL{0}".format(label_index)
    if isinstance(node.test, ast.Compare):
        row = parseIfCondition(tab,node,if_else_label)
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    #Enter a new body, to avoid it will lead to another cond 
    incremental_index()
    parse_body(tab + 1, node.body)

    row = generate_tab(tab + 1)+ "goto LABEL{0}".format(label_index+1)+ "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    #if has else 
    if hasattr(node,"orelse"):
        row = if_else_label + "\n"
        file.write(row)
        incremental_pseudo()
        
        if node.orelse != []:
            #If else body contain IF node, skip the incremental_py()
            if isinstance(node.orelse[0],ast.If) == False:
                incremental_py()
            #There is a else body in if-else
            parse_body(tab + 1, node.orelse)

        row = generate_tab(tab + 1)+ "goto LABEL{0}".format(label_index+1) +"\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()

    row = "LABEL{0}".format(label_index + 1) + "\n"
    file.write(row)
    incremental_pseudo()
    
    #Skip the label that used before
    incremental_index()
    return el_pseudo_index

#_ast.FunctionDef
def parseFunctionDef(tab,node):
    el_pseudo_index = []

    row = generate_tab(tab)+"Define a function called " + node.name+ "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    if node.args.args != []:   
        plural = True if len(node.args.args) >= 2 else False
        if plural:
            args = " ".join([str(arg.arg) for arg in node.args.args])
            row = generate_tab(tab) + "input args:" + args + "\n"
            file.write(row)
            el_pseudo_index.append(PSEUDO_INDEX)
            incremental_pseudo()
        else:
            row = generate_tab(tab) + "input arg:" + str(node.args.args[0].arg) + "\n"
            file.write(row)
            el_pseudo_index.append(PSEUDO_INDEX)
            incremental_pseudo()

    parse_body(tab+1,node.body)


    return el_pseudo_index

def parseCallFunc(tab,node):
    el_pseudo_index = []

    if node.args:
        #The node.args is not null
        args = []
        for arg in node.args:
            if isinstance(arg,ast.Name):
                args.append(str(arg.id))
            elif isinstance(arg,ast.Constant):
                args.append(str(node.value))
            elif isinstance(arg,ast.BinOp):
                args.append("EXPR")
        
        args = " ".join([str(arg) for arg in args])

    return el_pseudo_index

#_ast.Return
def parseReturn(tab,node):
    el_pseudo_index = []
    if isinstance(node.value,ast.Name):
        row = generate_tab(tab) + "Return variable " + str(node.value.id) + "\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()
    elif isinstance(node.value,ast.BinOp):
        start_point = PSEUDO_INDEX
        result = str(parseAssign(tab,node.value))
        row = generate_tab(tab) + "Return " + result + "\n"
        file.write(row)
        incremental_pseudo()

        for i in range(start_point,PSEUDO_INDEX):
            el_pseudo_index.append(i)

    return el_pseudo_index


#Parse the node.body
def parse_body(tab,body):
    for node in body :

        incremental_py()
        el = {"py_index":PY_INDEX,"pseudo_index":[]}

        if isinstance(node,ast.Assign):
            el["pseudo_index"]=parseAssignWrapper(tab,node)

        elif isinstance(node,ast.For):
            el["pseudo_index"] = parseForLoop(tab,node)

        elif isinstance(node,ast.While):
            el["pseudo_index"] = parseWhileLoop(tab,node)

        elif isinstance(node,ast.FunctionDef):
            el["pseudo_index"] = parseFunctionDef(tab,node)

        elif isinstance(node,ast.Expr):
        #check value whether it is call function
            el["pseudo_index"] = parseExpr(tab,node)

        elif isinstance(node,ast.If):
            incremental_index()
            el["pseudo_index"] = parseIfElse(tab,node)

        elif isinstance(node,ast.Return):
            el["pseudo_index"] = parseReturn(tab,node)

        elif isinstance(node,ast.Call):
            el["pseudo_index"] = parseCallFunc(tab,node)

        map_2_low_level_code.append(el)
        
        #elif isinstance(node,ast.Switch):
        #Python not like to provide switch function
 
def parse_ast_tree(tab,tree):
    if isinstance(tree,ast.Module):
        row = "Module Start"
        file.write(row)
        file.write('\n')

    parse_body(tab,tree.body)
        
    if isinstance (tree,ast.Module):
        row = "Module Done"
        file.write(row)

#Main function
def parse_pseudo_code(filename):
    ##To record all relationships
    global map_2_low_level_code;
    map_2_low_level_code = []

    #Add a function to run the code to check whether there are any problems

    #Open the file
    global file
    file = open("pseudo_code.txt", 'w')

    #Record the index for mapping
    global PSEUDO_INDEX,PY_INDEX,LABEL_INDEX
    PSEUDO_INDEX = 1
    PY_INDEX = -1
    LABEL_INDEX = 0
    

    code = ""
    with open(filename) as f:
        code = code + f.read()
    print("[ast_node.py]Origin code is:",code)
    tree = ast.parse(code)

    astTree = ast.dump(tree)
    pprint(astTree) #Print tree
    # pprint(tree.body) #Print all child nodes

    try:
        parse_ast_tree(1,tree)
        file.close()
    except NameError or AttributeError:
        file.close()
        return "404"

    
    return map_2_low_level_code
    
