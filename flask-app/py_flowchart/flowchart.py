"""
This file defines Flowchart.

Copyright 2020 CDFMLR. All rights reserved.
Use of this source code is governed by a MIT
license that can be found in the LICENSE file.
"""

import ast

from py_flowchart.ast_node import parse
from py_flowchart.node import NodesGroup


class Flowchart(NodesGroup):
    #Flowchart extends NodesGroup object.
    #This is the class that contains flowchart's definitions and connections

    def __init__(self, head_node):
        super().__init__(head_node)

    def flowchart(self):
        return self.fc_definition() + '\n' + self.fc_connection()

    @staticmethod
    def from_code(code):
       
        code_ast = ast.parse(code)

        p = parse(code_ast.body, simplify=False, conds_align=True)
        return Flowchart(p.head)

