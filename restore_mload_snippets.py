import os
import sys
import re

input_directory = sys.argv[1]


for dirpath, dirnames, files in os.walk(input_directory):
    for file_name in files:
        if "pre.sh" in file_name:
            file_path = os.path.join(dirpath,file_name)
            original_file = re.sub("(.*).pre.sh",r"\1",file_path)
            target_script = original_file + ".sh"
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