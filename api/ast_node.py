import ast
from pprint import pprint

import astunparse

def incremental_pseudo():
    global PSEUDO_INDEX
    PSEUDO_INDEX = PSEUDO_INDEX + 1

def incremental_py():
    global PY_INDEX
    PY_INDEX = PY_INDEX + 1

def generate_tab(number):
    tab_list = []
    for i in range(number):
        tab_list.append("   ")
    return "".join(tab_list)

def while_cond_args(test,goto):
    if isinstance(test,ast.Compare):
        #The condition has one left node
        if(isinstance(test.left,ast.Name)):
            cond = "if variable "+ test.left.id +" "+ cmp_label(test.ops[0]) + " " + str(test.comparators[0].value) + " then goto " + goto
            return cond
    return True

def loop_cond_expr(node):
    source = astunparse.unparse(node)
    loop_statement = source.strip()
    lines = loop_statement.splitlines()
    if len(lines) >= 1:
        return lines[0]
    else:
        return True

def iter_args(iter,goto):
    if isinstance(iter,ast.Call):
        if(iter.func.id == "range"):
            cond = "if variable is out of range(" + str(iter.args[0].value) + ")"+" then goto " + goto
            return cond
    return True

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

def parseAssign(tab,node):
    if isinstance(node,ast.BinOp) :
        left_node_is_null = isinstance(node.left,ast.Name)or isinstance(node.left,ast.Constant)
        right_node_is_null = isinstance(node.right,ast.Name)or isinstance(node.right,ast.Constant)
        if left_node_is_null and right_node_is_null:     
            row = generate_tab(tab)+ast.unparse(node) + "\n"
            file.write(row)
            incremental_pseudo()
            return "("+ ast.unparse(node)+ ")"

        elif left_node_is_null == False and right_node_is_null == False:
            left_node =str(parseAssign(tab,node.left))
            right_node = str(parseAssign(tab,node.right))
            result = left_node + " "+ operation_label(node.op) + " "+ right_node 
            row = generate_tab(tab)+result + "\n"
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

def parseAssignWrapper(tab,node):
    el_pseudo_index = []
    start_point = PSEUDO_INDEX
    result = str(parseAssign(tab,node.value))
    row = generate_tab(tab) + node.targets[0].id + " " + "=" + " "+result + "\n"
    file.write(row)
    incremental_pseudo()

    for i in range(start_point,PSEUDO_INDEX):
        el_pseudo_index.append(i)
    
    return el_pseudo_index
    
def parseForLoop(tab,node):
    el_pseudo_index = []
    row = generate_tab(tab)+"ForLoop:" + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()
    
    #The args
    if node.iter:
        cond = iter_args(node.iter,"ForLoopDone")
        row = generate_tab(tab+1) + cond + "\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()

    parse_body(tab + 1,node.body)

    #modify the iter number
    #
    #
    #


    row = generate_tab(tab + 1) + "goto ForLoop" + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    row = generate_tab(tab) + "ForLoopDone" + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    return el_pseudo_index

##add try catch
def parseWhileLoop(tab,node):
    el_pseudo_index = []
    row = generate_tab(tab)+"WhileLoop:"+"\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    #The args
    if node.test:
        cond = while_cond_args(node.test,"WhileLoopDone")
        row = generate_tab(tab)+cond + "\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()

    parse_body(tab + 1,node.body)

    row = generate_tab(tab + 1) +"goto WhileLoop" + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    row = generate_tab(tab) + "WhileLoopDone" + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    return el_pseudo_index

def parseExpr(tab,node):
    el_pseudo_index = []
    if node.value and isinstance(node.value,ast.Call):
        row = generate_tab(tab)+"call function "+ node.value.func.id + "\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()
        plural = True if len(node.value.args) >= 2 else False
        if plural:
            args = " ".join([ str(arg.value) for arg in node.value.args ])
            row = generate_tab(tab)+ "input args: " + args + "\n"
            file.write(row)
            el_pseudo_index.append(PSEUDO_INDEX)
            incremental_pseudo()
        else:
            if(hasattr(node.value.args[0],"id")):
                row = generate_tab(tab)+ "input arg:" + node.value.args[0].id + "\n"
            elif(hasattr(node.value.args[0],"value")):
                row = generate_tab(tab)+ "input arg:" + node.value.args[0].value + "\n"
            file.write(row)
            el_pseudo_index.append(PSEUDO_INDEX)
            incremental_pseudo()
    return el_pseudo_index

def parseIfElse(tab,node):
    el_pseudo_index = []
    if isinstance(node.test, ast.Compare):
        row = generate_tab(tab)+"If " + str(node.test.left.id) + " " + str(cmp_label(node.test.ops[0])) + " "+ str(node.test.comparators[0].value) + ", then skip the code" + "\n"
    file.write(row)
    el_pseudo_index.append(PSEUDO_INDEX)
    incremental_pseudo()

    parse_body(tab + 1, node.body)

    if hasattr(node,'orelse'):
        if isinstance(node.test, ast.Compare):
            row = generate_tab(tab)+"If " + str(node.test.left.id) + " " + str(cmp_label(node.test.ops[0])) + " "+ str(node.test.comparators[0].value) + ", then run these code" + "\n"
        file.write(row)
        el_pseudo_index.append(PSEUDO_INDEX)
        incremental_pseudo()

        parse_body(tab + 1, node.orelse)
    
    return el_pseudo_index

def parse_body(tab,body):
    for node in body :

        incremental_py()

        el = {"py_index":PY_INDEX,"pseudo_index":[]}

        if isinstance(node,ast.Assign):
            print("Assign")
            el["pseudo_index"]=parseAssignWrapper(tab,node)

        elif isinstance(node,ast.For):
            el["pseudo_index"] = parseForLoop(tab,node)

        elif isinstance(node,ast.While):
            el["pseudo_index"] = parseWhileLoop(tab,node)

        elif isinstance(node,ast.FunctionDef):
            el["type"] = FUNCTIONDEF
            el["llc"] = ""
            print("ast.FunctionDef")
            print(node)

        elif isinstance(node,ast.Expr):
        #check value whether it is call function
            el["pseudo_index"] = parseExpr(tab,node)

        elif isinstance(node,ast.If):
            el["pseudo_index"] = parseIfElse(tab,node)

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

    #These variables are for the llc_parse_tree
    global ASSIGN,FOR,WHILE,FUNCTIONDEF,EXPR,IFELSE
    ASSIGN = "assign"
    FOR = "for"
    WHILE = "while"
    FUNCTIONDEF = "functiondef"
    EXPR = "expression"
    IFELSE = "ifelse"

    global file
    file = open("pseudo_code.txt", 'w')

    #Record the index for mapping
    global PSEUDO_INDEX,PY_INDEX
    PSEUDO_INDEX = 1
    PY_INDEX = -1
    

    code = ""
    with open(filename) as f:
        code = code + f.read()
    print("[ast_node.py]Origin code is:",code)
    tree = ast.parse(code)

    astTree = ast.dump(tree)
    pprint(astTree) #Print tree
    # pprint(tree.body) #Print all child nodes

    parse_ast_tree(1,tree)

    file.close()
    return map_2_low_level_code
    
