"""
pyflowchart CLI

Copyright 2020 CDFMLR. All rights reserved.
Use of this source code is governed by a MIT
license that can be found in the LICENSE file.
"""

import argparse

from flowchart import Flowchart

def main(code_file):
    # read file content: binary
    file_content: bytes = code_file.read()

    flowchart = Flowchart.from_code(file_content)
    print(flowchart.flowchart())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python code to flowchart.')

    # code_file: open as binary, detect encoding and decode in main later
    parser.add_argument('code_file', type=argparse.FileType('rb'))
    
    args = parser.parse_args()

    
    main(args.code_file)
