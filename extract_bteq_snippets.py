import os
import sys
import re

input = sys.argv[1]

lines = open(input).readlines()

file_without_snippets = []
snippets = []

index = 0
while index < len(lines):
    l = lines[index]
    matches = re.search("bteq\s+<<",l)
    if (not matches is None):
        terminator = re.sub(".*bteq\s+<<\s*","",l)
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


with open(input + ".pre.sh","w") as newscript:
    newscript.writelines(file_without_snippets)

index = 1
for s in snippets:
    with open(f"{input}.snippet.{index}.bteq","w") as newsnippet:
        newsnippet.writelines(s)
    index = index + 1
print("done")