import os
import sys
import re


import argparse


arguments_parser = argparse.ArgumentParser(description="BTEQ embedded shell script restorer for SnowConvert. This script will take the migrated snippets and recreated shell scripts using those files")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your *.sh or *.ksh files are')
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir


for dirpath, dirnames, files in os.walk(input_directory):
    for file_name in files:
        if "pre.sh" in file_name:
            file_path = os.path.join(dirpath,file_name)
            if "pre.sh" in file_name:
                original_file = re.sub("(.*).pre.sh",r"\1",file_path)
                target_script = original_file + ".sh"
            if "pre.ksh" in file_name:
                original_file = re.sub("(.*).pre.sh",r"\1",file_path)
                target_script = original_file + ".ksh"
            lines = open(file_path).readlines()
            print(target_script)
            with open(target_script,"w") as f:
                for l in lines:
                    matches = re.search("@@SNIPPET(\d+)",l)
                    if not matches is None:
                        snippet_number = matches.groups()[0]
                        with open(original_file + ".snippet." + snippet_number + "_MultiLoad.py") as snippet_file:
                            contents = snippet_file.read()
                            f.write(f'result=$(python <<END_SNOWSCRIPT\n{contents}\nEND_SNOWSCRIPT\n)\n')
                    else:
                        f.write(l)
