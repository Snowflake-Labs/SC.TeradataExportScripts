import os
import sys
import re

import argparse


arguments_parser = argparse.ArgumentParser(description="BTEQ embeded shell script extractor for SnowConvert")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your *.sh or *.ksh files are')
arguments_parser.add_argument('--outdir', required=True, help='This is the directory where the splitted files will be put')
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir
output_directory = arguments.outdir

def findnext(lines,pos,terminator,block):
    pos = pos + 1
    while (pos < len(lines)):
        line = lines[pos]
        if re.search(f".*{terminator}.*",line):
            return pos + 1
        block.append(line + "\n")
        pos = pos + 1
    return pos


for dirpath, dirnames, files in os.walk(input_directory):
    for file_name in files:
        print(file_name)
        all_text = open(os.path.join(dirpath, file_name), encoding="ISO-8859-1").read()
        if not "bteq" in all_text:
            continue
        lines = all_text.splitlines()
        snippets = []
        file_without_snippets = []
        pos = 0
        while pos < len(lines):
            current_line = lines[pos]
            matches = re.match(".*bteq\s*<<[-]*\s*(.+?)\s.*",current_line) or re.match(".*bteq\s*<<[-]*\s*(.*)$",current_line) or re.match(".*\$BTEQ_\w+\s*<<[-]*\s*(.*)$",current_line)
            if matches:
                terminator = matches.group(1)
                newblock = []
                pos = findnext(lines,pos,terminator,newblock)
                snippets.append(newblock)
                file_without_snippets.append(f"@@SNIPPET{len(snippets)}\n")
                continue
            file_without_snippets.append(current_line + "\n")
            pos = pos + 1

        snippetName = os.path.join(output_directory, file_name)
        with open(snippetName + ".pre.sh","w", encoding="ISO-8859-1") as newscript:
            newscript.writelines(file_without_snippets)

        index = 1
        for s in snippets:
            with open(f"{snippetName}.snippet.{index}.bteq","w",  encoding="ISO-8859-1") as newsnippet:
                newsnippet.writelines(s)
            index = index + 1
        print("done")
