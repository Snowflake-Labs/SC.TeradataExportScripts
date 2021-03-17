import os
import sys
import re

input_directory = sys.argv[1]
output_directory = sys.argv[2]

for dirpath, dirnames, files in os.walk(input_directory):
    for file_name in files:
        print(file_name)
        lines = open(os.path.join(dirpath, file_name)).readlines()

        file_without_snippets = []
        snippets = []

        index = 0
        while index < len(lines):
            l = lines[index]
            matches = re.search("mload\s+<<",l)
            if (not matches is None):
                terminator = re.sub(".*mload\s+<<\s*","",l)
                index = index + 1
                l=lines[index]
                snippet = []
                while not terminator in l:
                    snippet.append(l)
                    index = index + 1
                    l=lines[index]
                index = index + 1
                snippets.append(snippet)
                file_without_snippets.append(f"@@SNIPPET{len(snippets)}\n")
                continue
            else:
                file_without_snippets.append(l)
            index =index + 1


        snippetName = os.path.join(output_directory, file_name)
        with open(snippetName + ".pre.sh","w") as newscript:
            newscript.writelines(file_without_snippets)

        index = 1
        for s in snippets:
            with open(f"{snippetName}.snippet.{index}.mload","w") as newsnippet:
                newsnippet.writelines(s)
            index = index + 1
        print("done")