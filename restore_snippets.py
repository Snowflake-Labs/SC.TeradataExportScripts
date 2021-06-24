import argparse
import os
import re
from os.path import exists

arguments_parser = argparse.ArgumentParser(description="MLOAD/BTEQ embedded shell script restorer for SnowConvert. This script will take the migrated snippets and recreated shell scripts using those files")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your *.sh or *.ksh files are')
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir
totalfiles = 0

for dirpath, dirnames, files in os.walk(input_directory):
    for file_name in files:
        if "pre.sh" in file_name:
            totalfiles = totalfiles + 1
            file_path = os.path.join(dirpath, file_name)
            if "pre.sh" in file_name:
                original_file = re.sub("(.*).pre.sh", r"\1", file_path)
                target_script = original_file + ".sh"
            lines = open(file_path, encoding="ISO-8859-1").readlines()
            print(f"Restoring {target_script}")
            with open(target_script, "w", encoding="ISO-8859-1") as file:
                for current_line in lines:
                    matches = re.search("@@SNIPPET(\d+)(.*)$", current_line)
                    if matches is not None:
                        snippet_number = matches.group(1)
                        suffix_file = matches.group(2)
                        snippet_filepath = original_file + ".snippet." + snippet_number + suffix_file
                        if exists(snippet_filepath):
                            with open(snippet_filepath, encoding="ISO-8859-1") as snippet_file:
                                contents = snippet_file.read()
                                file.write(f'result=$(python <<END_SNOWSCRIPT\n{contents}\nEND_SNOWSCRIPT\n)\n')
                        else:
                            print(f"The expected snippet file {snippet_filepath} does not exist")
                    else:
                        file.write(current_line)

print()
print(f"The total of sh restored files are {totalfiles}")

