##########################################################################################################
#
#  This is a helper utility to process some input files for the conversion tool named SnowConvert
#  of Mobilize.Net
#
#  More info: https://www.mobilize.net/products/database-migrations/snowconvert
#
#  This script needs the required parameters --inoutdir INOUTDIR
#    INOUTDIR where are located the supported files with sql, bteq, fload or mload scripts 
#
#  The files of the supported extensions will be modified the content for the 4 following problemtic patterns:
#  *1)  The character # at the beginning of the line will be commented
#       Input:
#         # Original Comment
#       Output:
#         --# Original Comment
#
#  *2)  Multiple block markers of comments will be corrected 
#       Input:
#         /*COMMENT /*INNER COMMENT */ OUT COMMENT */ 
#       Output:
#         /*COMMENT /-*INNER COMMENT *-/ OUT COMMENT */
#
#  *3)  Definition of a variable with a content in multiple line (or singular line) 
#       Input:
#         VAR_NAME = "content of the whole file"
#       Output:
#         --VAR_NAME = "
#         content of the whole file
#         --"
#       Input:
#         VAR_NAME = "
#         content of the
#         whole file
#         "
#       Output:
#         --VAR_NAME = "
#         content of the
#         whole file
#         --"
#
#   *4) End double quote at the end of last line of the file
#       Input:
#         LOGOFF"
#       Output:
#         LOGOFF
#         --"
#
# Changes Log
# 
# 2021-11-05
# - Creation of the script to support the 4 different scenarios
# - Displaying information of total of modified files by extension
#
##########################################################################################################

import argparse
import os
import re

arguments_parser = argparse.ArgumentParser(description="MLOAD/BTEQ/SQL/FLOAD files corrector to help the tool SnowConvert")
arguments_parser.add_argument('--inoutdir',required=True, help='This is the directory where your bteq/fload/mload/sql files are')
arguments_parser.add_argument('--verbose', required=False, dest='verbose', action='store_true', help='If this is specified all the files that are being copied and processed will be displayed')
arguments_parser.add_argument('--no-verbose', required=False, dest='verbose', action='store_false', help='If this is specified none of the copied and processed will be displayed, this is the default behaviour')
arguments_parser.set_defaults(verbose=False)
arguments = arguments_parser.parse_args()
verbose = arguments.verbose

def increment_table(table, key):
    """Increments the value in the table for 1 in its value, or 1 if it did not exist
    if table key is not present
    table[key] = 1
    if table key is present
    table[key] = table[key] + 1
    """
    currentvalue = 0
    if key in table:
        currentvalue = table[key]
    table[key] = currentvalue + 1

def correct_multiblock_line(line, index, close_index, inside_block_comments):
    newline = ""
    restOfLine = line
    corrected = False
    openedPending = 1 if inside_block_comments else 0
    while index > 0  or close_index > 0:
        if inside_block_comments:
            if index >= 0:
                restOfLine = restOfLine[index:]
            if close_index >= 0:
                inside_block_comments = False
                restOfLine = restOfLine[close_index:]
                break

        else:
            if index >= 0 and close_index >= 0: # /* and */ are present
                newline = restOfLine[0: index + 2]
                sub = restOfLine[index + 2: close_index]
                newPending = sub.count("/*")
                if newPending > 0:
                    openedPending += newPending
                    restOfLine = restOfLine[close_index:]
                    newline += sub.replace("/*", "/-*")
                    last_index = restOfLine.rfind("*/", 0) # at least one terminator
                    sub = restOfLine[0: last_index]
                    newline += sub.replace("*/", "*-/")
                    restOfLine = restOfLine[last_index:]
                    newline += restOfLine

                    inside_block_comments = False
                    corrected = True
                    break
                else:
                    newline = restOfLine[0: close_index + 2]
                    restOfLine = restOfLine[close_index + 2:]
            elif index >= 0:
                inside_block_comments = True
                break
            elif close_index >= 0:
                inside_block_comments = False
                break

        index = restOfLine.find("/*")
        close_index = restOfLine.find("*/")

    if corrected:
        return (corrected, newline, inside_block_comments)
    else:
        return (corrected, line, inside_block_comments)

def repair_assign_vars(file):
    if not file:
        print("Please supply a value for the file parameter")
        return 0

    newlines = []
    repaired = False
    double_comment_fixed = False
    search_close = False
    fixed_comments = False
    fixed_lastline = False
    inside_block_comments = False

    varname=""
    lines = open(file, "r")
    size = os.path.getsize(file)
    position = 0
    for line in lines:
        newline = line
        position += len(line) + 1
        if (matches:= re.search("^([A-Z_0-9]+)(=\")(.*)", line)):
            varname = matches.group(1)
            asg = matches.group(2)
            value = matches.group(3)
            newlines.append(f"--{varname}{asg}\n")
            repaired = True
            matches = re.search("(.*)(\")$", value)
            if matches:
                newlines.append(f"{matches.group(1)}\n")
                newline = f"--{matches.group(2)}\n"
                search_close = False
            else:
                newline = f"{value}\n"
                search_close = True
        elif search_close and re.search("^\"", line):
            newline=f"--{line}"
            search_close = False
        elif (index := line.find("/*")) > 0 or (close_index := line.find("*/")) >= 0: 
            (corrected, newline, inside_block_comments) = correct_multiblock_line(line, index, close_index, inside_block_comments)
            if corrected:
                double_comment_fixed = True
        elif not inside_block_comments and re.search("^#", line):
            newline=f"--{line}"
            fixed_comments = True
        elif position == size and (matches := re.search("^([^\"]{3}[^\"]*)(\")$", line)):
            fixed_lastline = True
            newlines.append(f"{matches.group(1)}\n")
            newline=f"--{matches.group(2)}\n"

        newlines.append(newline)

    if verbose:
        if repaired:
            not_tag = "" if not search_close else "NOT "
            print(f"The file {file} HAD the variable mark. The varname was $varname. The closing quote was {not_tag}found")
        if double_comment_fixed:
            print(f"The file {file} HAD double comment mark, and it is now fixed")
        if fixed_comments:
            print(f"The file {file} HAD # comment mark, and it is now fixed as --#")
        if fixed_lastline:
            print(f"The file {file} needed to correct the last line with an ending double quote")

    if repaired or double_comment_fixed or fixed_comments or fixed_lastline:
        with open(f"{file}", "w") as f:
            f.writelines(newlines)
        return 1

    return 0

input_directory=arguments.inoutdir
supported_extentions={ ".bteq", ".mload", ".fload", ".sql" }
supported = 0
changed = 0
total = 0
modifiedbyext = {}
for dirpath, dirnames, files in os.walk(input_directory):
    total += len(files)
    for file_name in files:
        inoutfile = os.path.join(dirpath, file_name)
        ext = os.path.splitext(file_name)[1]
        if ext in supported_extentions:
            supported += 1
            current_changed = repair_assign_vars(inoutfile)
            if current_changed > 0:
                changed += current_changed
                increment_table(modifiedbyext, ext)

if len(modifiedbyext) > 0:
    print("The total of modified files by extension")
    print(modifiedbyext)

print(f"Changed {changed} files from total of {supported} supported files and a total {total} files from inout directory specified")
