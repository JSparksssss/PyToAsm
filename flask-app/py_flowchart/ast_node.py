"""
This file manage to translate AST into our Nodes Graph,
By defining AstNodes, and statements to parse AST.

Copyright 2020 CDFMLR. All rights reserved.
Use of this source code is governed by a MIT
license that can be found in the LICENSE file.
"""

import _ast
from typing import List, Tuple

import astunparse

from py_flowchart.node import *


class AstNode(Node):

    #AstNode is the node from AST tree
    def __init__(self, ast_object):
        Node.__init__(self)
        self.ast_object = ast_object

    def ast_to_source(self):

        return astunparse.unparse(self.ast_object).strip()


class AstConditionNode(AstNode, ConditionNode):

    #ASTConditionNode covers For/While/If class in AST

    def __init__(self, ast_cond, **kwargs):
        #Define a ASTNode and ConditionNode for flowchart
        AstNode.__init__(self, ast_cond, **kwargs)
        ConditionNode.__init__(self, cond=self.cond_expr())

    def cond_expr(self):

        source = astunparse.unparse(self.ast_object)
        loop_statement = source.strip()
        lines = loop_statement.splitlines()

        if len(lines) >= 1:
            return lines[0].rstrip(':')
        else:
            return 'True'

    def fc_connection(self):
        return ""

##
# FunctionDef
##
class FunctionDefStart(AstNode, StartNode):

    #Defined the start node of a function
    def __init__(self, ast_function_def: _ast.FunctionDef, **kwargs):
        AstNode.__init__(self, ast_function_def, **kwargs)
        StartNode.__init__(self, ast_function_def.name)

class FunctionDefEnd(AstNode, EndNode):
    #Defined the end node of a function
    def __init__(self, ast_function_def: _ast.FunctionDef, **kwargs):
        AstNode.__init__(self, ast_function_def, **kwargs)
        EndNode.__init__(self, ast_function_def.name)

class FunctionDefArgsInput(AstNode, InputOutputNode):
    #Define the Function Input & Output for the args in FunctionDef
    def __init__(self, ast_function_def: _ast.FunctionDef, **kwargs):
        AstNode.__init__(self, ast_function_def, **kwargs)
        InputOutputNode.__init__(self, InputOutputNode.INPUT, self.func_args_str())

    def func_args_str(self):
        args = []
        for arg in self.ast_object.args.args:
            args.append(str(arg.arg))

        return ', '.join(args)

class FunctionDef(NodesGroup, AstNode):

    #FunctionDef is a AstNode for _ast.FunctionDef
    #It contains FunctionDefStart & FunctionDefArgsInput & function-body & FunctionDefEnd

    def __init__(self, ast_func: _ast.FunctionDef, **kwargs):  # _ast.For | _ast.While

        AstNode.__init__(self, ast_func, **kwargs)

        # get nodes
        self.func_start = FunctionDefStart(ast_func, **kwargs)
        self.func_args_input = FunctionDefArgsInput(ast_func, **kwargs)
        self.body_head, self.body_tails = self.parse_func_body(**kwargs)
        self.func_end = FunctionDefEnd(ast_func, **kwargs)

        # connect
        if self.ast_object.args.args == []:
            self.func_start.connect(self.body_head)
        else:
            self.func_start.connect(self.func_args_input)
            self.func_args_input.connect(self.body_head)
            

        for t in self.body_tails:
            if isinstance(t, Node):
                t.connect(self.func_end)

        NodesGroup.__init__(self, self.func_start, [self.func_end])

    def parse_func_body(self, **kwargs):
        p = parse(self.ast_object.body, **kwargs)
        return p.head, p.tails

##
# For While
##
class LoopCondition(AstConditionNode):
    
    #For the condition in loop
    def connect(self, sub_node, direction=''):
        if direction:
            self.set_connect_direction(direction)
        self.connect_no(sub_node)

    def is_one_line_body(self):
        one_line_body = False
        try:
            loop_body = self.connection_yes
            one_line_body = isinstance(loop_body, CondYN) and \
                            isinstance(loop_body.sub, Node) and \
                            not isinstance(loop_body.sub, NodesGroup) and \
                            not isinstance(loop_body.sub, ConditionNode) and \
                            len(loop_body.sub.connections) == 1 and \
                            loop_body.sub.connections[0] == self
        except Exception as e:
            print(e)
        return False


class Loop(NodesGroup, AstNode):
    #This is the for WhileLoop and ForLoop 
    def __init__(self, ast_loop, **kwargs):
        
        # Construct Loop object will make following Node chain:
        #     Loop -> LoopCondition -> (yes) -> LoopCondition
        #                           -> (no)  -> <next_node>

        AstNode.__init__(self, ast_loop, **kwargs)

        self.cond_node = LoopCondition(ast_loop)

        NodesGroup.__init__(self, self.cond_node)

        self.parse_loop_body(**kwargs)

        self._virtual_no_tail()


    def parse_loop_body(self, **kwargs):
        """
        Parse and Connect loop-body (a node graph) to self.cond_node (LoopCondition), extend self.tails with tails got.
        """
        progress = parse(self.ast_object.body, **kwargs)

        #If loop body has content
        if progress.head is not None:
            process = parse(self.ast_object.body, **kwargs)
            # head
            self.cond_node.connect_yes(process.head)
            # tails connect back to cond
            for tail in process.tails:
                if isinstance(tail, Node):
                    tail.set_connect_direction("left")
                    tail.connect(self.cond_node)
        else:
            noop = SubroutineNode("no-op")
            noop.set_connect_direction("left")
            noop.connect(self.cond_node)
            self.cond_node.connection_yes(noop)

    def _virtual_no_tail(self):

        #Create a tail for this loop
        #Connect the tail with the next node in parse()
        virtual_no = CondYN(self, CondYN.NO)

        self.cond_node.connection_no = virtual_no
        self.cond_node.connections.append(virtual_no)

        self.append_tails(virtual_no)

##
# If
##

class IfCondition(AstConditionNode):
    #For the Condition in If node
    def is_one_line_body(self):
        one_line_body = False
        try:
            yes = self.connection_yes
            one_line_body = isinstance(yes, CondYN) and \
                            isinstance(yes.sub, Node) and \
                            not isinstance(yes.sub, NodesGroup) and \
                            not isinstance(yes.sub, ConditionNode) and \
                            not yes.sub.connections
        except Exception as e:
            print(e)
        return False

    def is_no_else(self):
        #If the orelse attrbute is null in If, return False
        no_else = False
        try:
            no = self.connection_no
            no_else = isinstance(no, CondYN) and \
                      not no.sub
        except Exception as e:
            print(e)
        return no_else


class If(NodesGroup, AstNode):

    # AstNode for If
    # This class is a NodesGroup that connects to IfCondition & if-body & else-body.

    def __init__(self, ast_if: _ast.If, **kwargs):
        AstNode.__init__(self, ast_if, **kwargs)

        self.cond_node = IfCondition(ast_if)

        NodesGroup.__init__(self, self.cond_node)

        self.parse_if_body(**kwargs)
        self.parse_else_body(**kwargs)
        

    def parse_if_body(self, **kwargs):

        nodes = parse(self.ast_object.body, **kwargs)

        if nodes.head is not None:
            self.cond_node.connect_yes(nodes.head)

            #node.tails is a list
            for tail in nodes.tails:
                self.append_tails(tail)
        else: 
            virtual_yes = CondYN(self, CondYN.YES)
            self.cond_node.connection_yes = virtual_yes
            self.cond_node.connections.append(virtual_yes)

            self.append_tails(virtual_yes)

    def parse_else_body(self, **kwargs):

        nodes = parse(self.ast_object.orelse, **kwargs)

        if nodes.head is not None:
            self.cond_node.connect_no(nodes.head)
            for tail in nodes.tails:
                self.append_tails(tail)
        else:
            virtual_no = CondYN(self, CondYN.NO)
            self.cond_node.connection_no = virtual_no
            self.cond_node.connections.append(virtual_no)

            self.append_tails(virtual_no)


    def align(self):
        self.cond_node.no_align_next()


###
# Common, Call
###

class CommonOperation(AstNode, OperationNode):

    #For common arithmetic statements
    def __init__(self, ast_object: _ast.AST, **kwargs):
        AstNode.__init__(self, ast_object, **kwargs)
        OperationNode.__init__(self, operation=self.ast_to_source())


class CallSubroutine(AstNode, SubroutineNode):
    
    #For call statements
    def __init__(self, ast_call: _ast.Call, **kwargs):
        AstNode.__init__(self, ast_call, **kwargs)
        SubroutineNode.__init__(self, self.ast_to_source())


##
# Return
##

class ReturnOutput(AstNode, InputOutputNode):

    def __init__(self, ast_return: _ast.Return, **kwargs):
        AstNode.__init__(self, ast_return, **kwargs)
        InputOutputNode.__init__(self, InputOutputNode.OUTPUT, self.ast_to_source().lstrip("return"))


class ReturnEnd(AstNode, EndNode):
    
    #This is a endnode for a function with return
    def __init__(self, ast_return: _ast.Return, **kwargs):
        AstNode.__init__(self, ast_return, **kwargs)
        EndNode.__init__(self, "function") 


class Return(NodesGroup, AstNode):

    def __init__(self, ast_return: _ast.Return, **kwargs):

        # Construct Return object will make following Node chain:
        #     Return -> ReturnOutput -> ReturnEnd
        # Giving return sentence without return-values, the ReturnOutput will be omitted: (Return -> ReturnEnd)

        AstNode.__init__(self, ast_return, **kwargs)

        self.output_node = None
        self.end_node = None

        self.head = None

        self.end_node = ReturnEnd(ast_return, **kwargs)
        self.head = self.end_node
        if ast_return.value:
            self.output_node = ReturnOutput(ast_return, **kwargs)
            self.output_node.connect(self.end_node)
            self.head = self.output_node

        self.connections.append(self.head)

        NodesGroup.__init__(self, self.head, [self.end_node])

    def connect(self, sub_node, direction=''):
        """
        Return should not be connected with anything
        """
        pass


__special_stmts = {
    _ast.FunctionDef: FunctionDef,
    _ast.If: If,
    _ast.For: Loop,
    _ast.While: Loop,
    _ast.Return: Return,
    _ast.Call: CallSubroutine
}


class ParseProcessGraph(NodesGroup):
    """
    ParseGraph is a NodesGroup for parse process result.
    """
    pass


def parse(ast_list: List[_ast.AST], **kwargs):

    # Keyword Args:
    #     * simplify: for If & Loop: simplify the one line body cases
    #     * conds_align: for If: allow the align-next option set for the condition nodes.
    #         See https://github.com/cdfmlr/pyflowchart/issues/14

    # Returns:
    #     ParseGraph

    head_node = None
    tail_node = None

    process = ParseProcessGraph(head_node, tail_node)

    for ast_object in ast_list:
        # ast_node_class: some special AstNode subclass or CommonOperation by default.
        ast_node_class = __special_stmts.get(type(ast_object), CommonOperation)

        # special case: special stmt as a expr value. e.g. function call
        if type(ast_object) == _ast.Expr:
            try:
                ast_node_class = __special_stmts.get(type(ast_object.value), CommonOperation)
            except AttributeError:
                # ast_object has no value attribute
                ast_node_class = CommonOperation

        assert issubclass(ast_node_class, AstNode)

        node = ast_node_class(ast_object)

        if head_node is None:  # is the first node
            head_node = node
            tail_node = node
        else:
            tail_node.connect(node) 

            if isinstance(tail_node, If) and isinstance(node, If) and \
                    kwargs.get("conds_align", False):
                tail_node.align()

            tail_node = node

    process.set_head(head_node)
    process.append_tails(tail_node)

    return process
