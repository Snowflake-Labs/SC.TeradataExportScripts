import argparse
import os
import re
from shutil import copyfile

arguments_parser = argparse.ArgumentParser(description="MLOAD/BTEQ embedded shell script extractor for SnowConvert")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your *.sh or *.ksh files are')
arguments_parser.add_argument('--outdir', required=True, help='This is the directory where the splitted files will be put')
arguments = arguments_parser.parse_args()

supported_extensions = { "bteq":"_BTEQ.py", "mload": "_MultiLoad.py" }
pattern_extensions = "|".join(supported_extensions.keys())
pattern_extensions_upper = pattern_extensions.upper()
input_directory = arguments.inputdir
output_directory = arguments.outdir
snippetbyext = {}
unmodifiedfiles = 0
totalfiles = 0
PRE_SH_TYPE = "pre.sh"
supported_extension_keys = supported_extensions.keys()
supported_extension_tags = []

for ext in supported_extension_tags:
    supported_extension_tags.append("$" + ext.upper() + "_COMMAND")

def find_extensions_in_text(line, extensions, extension_tags):
    for ext in extensions:
        if ext in line:
            return True

    for tag in extension_tags:
        if tag in line:
            return True

    return False

def findnext(lines, pos, terminator, block):
    pos = pos + 1
    while (pos < len(lines)):
        line = lines[pos]
        if re.search(f".*{terminator}.*", line):
            return pos + 1
        replaced_text = re.sub(r'^([ \t]*)(\$[A-Za-z][A-Za-z0-9]*;[ \t]*)$', r'\1;/*Not supported command from variable \2*/', line)
        block.append(replaced_text + "\n")
        pos = pos + 1
    return pos

if (len(input_directory) > 0 and input_directory[-1] != os.path.sep):
    input_directory = input_directory + os.path.sep

rootlen = len(input_directory)
for dirpath, dirnames, files in os.walk(input_directory):
    for file_name in files:
        inputfile = os.path.join(dirpath, file_name)
        inputsubdir = os.path.dirname(inputfile)
        subdir = inputsubdir[rootlen:]
        all_text = open(inputfile, encoding="ISO-8859-1").read()

        snippets = []

        if find_extensions_in_text(all_text, supported_extension_keys, supported_extension_tags):
            lines = all_text.splitlines()
            file_without_snippets = []

            pos = 0
            lenLines = len(lines)
            while pos < lenLines:
                current_line = lines[pos]
                matches = re.match(f".*({pattern_extensions})\s*<<[-]*\s*(.+?)\s.*", current_line) or re.match(f".*({pattern_extensions})\s*<<[-]*\s*(.*)$", current_line) or re.match(f".*\$({pattern_extensions_upper})_\w+\s*<<[-]*\s*(.*)$", current_line)
                if matches:
                    terminator = matches.group(2)
                    filetype = matches.group(1).lower()
                    newblock = []
                    pos = findnext(lines, pos, terminator, newblock)
                    snippets.append(newblock)
                    file_without_snippets.append(f"@@SNIPPET{len(snippets)}{supported_extensions[filetype]}\n")
                    continue
                file_without_snippets.append(current_line + "\n")
                pos = pos + 1

        outputfile = os.path.join(output_directory, subdir, file_name)
        outputsubdir = os.path.dirname(outputfile)
        if not os.path.exists(outputsubdir):
            os.makedirs(outputsubdir)

        if len(snippets) == 0:
            unmodifiedfiles = unmodifiedfiles + 1
            totalfiles = totalfiles + 1
            try:
                copyfile(inputfile, outputfile)
            except IOError as e:
                print(f"Error: Unable to copy file. {e}")
            continue

        with open(outputfile + ".pre.sh", "w", encoding="ISO-8859-1") as newscript:
            newscript.writelines(file_without_snippets)
        print(f"Wrote to file {subdir}{os.path.sep}{file_name}.pre.sh without snippets")

        currentpresh = 0
        currentsumsnippets = 0

        if filetype in snippetbyext:
            currentsumsnippets = snippetbyext[filetype]
        snippetbyext[filetype] = currentsumsnippets + len(snippets)
        totalfiles = totalfiles + len(snippets)

        if PRE_SH_TYPE in snippetbyext:
            currentpresh = snippetbyext[PRE_SH_TYPE]
        snippetbyext[PRE_SH_TYPE] = currentpresh + 1
        totalfiles = totalfiles + 1
        
        pos = 1
        for s in snippets:
            outputsuffix = f".snippet.{pos}.{filetype}"
            with open(f"{outputfile}{outputsuffix}", "w", encoding="ISO-8859-1") as newsnippet:
                newsnippet.writelines(s)
            pos = pos + 1
            print(f"Wrote to file {subdir}{os.path.sep}{file_name}{outputsuffix}")

print()
print("The total of created files")
print(snippetbyext)
print(f"The total of copied unmodified files {unmodifiedfiles}")
print(f"Total output files {totalfiles}")