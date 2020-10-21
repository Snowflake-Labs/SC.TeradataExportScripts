import os
import sys
import re

input = sys.argv[1]
original_file = re.sub("(.*).pre.sh",r"\1",input)
target_script = original_file + ".sh"
lines = open(input).readlines()


with open(target_script,"w") as f:
    for l in lines:
        matches = re.search("@@SNIPPET(\d+)",l)
        if not matches is None:
            snippet_number = matches.groups()[0]
            with open(original_file + ".snippet." + snippet_number + "_BTEQ.py") as snippet_file:
                contents = snippet_file.read()
                f.write(f'result=$(python <<END_SNOWSCRIPT\n{contents}\nEND_SNOWSCRIPT\n)\n')
        else:
            f.write(l)