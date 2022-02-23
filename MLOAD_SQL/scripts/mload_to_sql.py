##########################################################################################################
#
#  Copyright (C) Mobilize.Net info@mobilize.net - All Rights Reserved
#  This file is part of the Mobilize Frameworks, which is proprietary and confidential.
#  NOTICE: All information contained herein is, and remains the property of Mobilize.Net Corporation.
#  The intellectual and technical concepts contained herein are proprietary to Mobilize.Net Corporation 
#  and may be covered by U.S. Patents, and are protected by trade secret or copyright law.
#  Dissemination of this information or reproduction of this material is strictly forbidden unless 
#  prior written permission is obtained from Mobilize.Net Corporation.
#
#---------------------------------------------------------------------------------------------------------
#  MLOAD (Python) to SQL Tool:
#  This is a helper utility to convert MLOAD converted files (Python scripts) to SQL.
#
# NOTES:
#  - This script assumes that a temporary table is defined in the source file; otherwise, 
#    an error message is generated and the file is not processed.
#  - This script creates a temp folder under the target folder. It can be manually deleted after script execution.
#
#  Parameters:
#  -- inputdir: This is the directory where your *.py files are
#  -- outdir: This is the directory where the SQL files will be put
#
# Changes History
#    20220216-TGM: 
#      - Initial Version
# 
##########################################################################################################


import re
import os
import argparse
import sys

arguments_parser = argparse.ArgumentParser(description="MLOAD (Python) to SQL Tool")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your *.py files are')
arguments_parser.add_argument('--outdir', required=True, help='This is the directory where the SQL files will be put')
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir
base_output_dir = arguments.outdir

# Definition:
#   Method to read the files. 
# Parameters:
#   - pathFile: name of the file being readed.
def read_file(pathFile):
    try:
        f = open(pathFile, "r")
        s = f.read()
        f.close()
    except UnicodeDecodeError:
        try:
            f = open(pathFile, "r", encoding="ISO-8859-1")
            s = f.read()
            f.close()
        except Exception:
            print("Error opening file [" + pathFile + "] please review encoding and file permissions")
            s = ""
    return s

# Definition:
#   This method creates the new sql file using the extracted sql statements 
# Parameters:
#   - filename: name of the file being processed
#   - snnipetPath: name of the snippet file being processed
#   - table_name: name of the temporary table
#   - table_columns: list of the table columns
def create_sql(file_name, snnipetPath, table_name, table_columns): 
    name = os.path.splitext(os.path.basename(file_name))[0]
    target_file = os.path.join(base_output_dir, name + ".sql")

    format_name = f"FORMAT_{name}"
    stage_name = f"STAGE_{name}"
    contents = f"/*MSC-WARNING: File format definition must be changed according to the input file. More info https://docs.snowflake.com/en/sql-reference/sql/create-file-format.html*/\n"
    contents = contents + f"CREATE OR REPLACE FILE FORMAT {format_name} TYPE = 'CSV' FIELD_DELIMITER = '|' TRIM_SPACE = TRUE SKIP_HEADER = 0; \n--\n"
    contents = contents +  f"CREATE OR REPLACE TEMPORARY STAGE {stage_name};\n--\n"
    contents = contents + f"PUT file://&DirectoryPath/&FileName @{stage_name} OVERWRITE = TRUE AUTO_COMPRESS = FALSE;\n--\n"
    contents = contents + f"CREATE OR REPLACE TEMPORARY TABLE {table_name} ({table_columns.replace(';','')});\n--\n"
    contents = contents + f"COPY INTO {table_name} FROM @{stage_name} FILE_FORMAT = (format_name = '{format_name}');\n--\n"
    
    s = read_file(snnipetPath)

    contents = contents + "\n" + s;

    with open(target_file,"w") as f:
        f.write(contents)

# Definition:
#   This method extracts the sql statements located in the python file and create a new sql file with the converted MLOAD functionality. 
# Parameters:
#   - filename: name of the file being processed
def process_file(file_name):
    pathFile = os.path.join(input_directory, file_name)
    targetFolder = os.path.join(base_output_dir, "temp")
    targetPath = os.path.join(targetFolder, file_name)
    snnipetPath = targetPath + ".sql"
    table_name = ""
    table_columns = ""
    
    if not os.path.exists(targetFolder):
        os.makedirs(targetFolder)

    print('Processing file: ' + file_name)

    s = read_file(pathFile)

    # Add a custom print function to add final semi-colon in each statement
    s = f"def myPrint(str):\tprint(str.strip() + ';')\n\n" + s
    
    # Comment all the not required lines of code
    s = s.replace("import snowconvert.helpers", "#import snowconvert.helpers")
    s = s.replace("from snowconvert.helpers import Export", "#from snowconvert.helpers import Export")
    s = s.replace("from snowconvert.helpers import exec", "#from snowconvert.helpers import exec")
    s = s.replace("snowconvert.helpers.configure_log()", "#snowconvert.helpers.configure_log()")
    s = s.replace("con = snowconvert.helpers.log_on()", "#con = snowconvert.helpers.log_on()")
    s = s.replace("snowconvert.helpers.quit_application()", "#snowconvert.helpers.quit_application()")
    s = s.replace("snowconvert.helpers.import_file_to_temptable", "#snowconvert.helpers.import_file_to_temptable")
    s = s.replace("snowconvert.helpers.drop_transient_table", "#snowconvert.helpers.drop_transient_table")
    s = s.replace("con = None", "#con = None")
    s = s.replace("if con is not None:", "#if con is not None:")
    s = s.replace("con.close()", "#con.close()")

    # Replace the execution by a print function
    s = s.replace("exec(", "myPrint(")

    # Write the modified file in the temp folder
    f = open(targetPath,"a")
    f.write(s)
    f.close()
 
    # Execute python scripts and write the prints in the temp folder
    os.system(f"python {targetPath} > {snnipetPath}")

    # Get table info
    match = re.search(r'\w+_LAYOUT_TableName\s*=\s*"(\w+)"', s, flags=re.I)
    if match:
        table_name = match.group(1)

    # Get columns info
    match = re.search(r'\w+_LAYOUT_Columns\s*=\s*"""([\w/(\),\s]+)"""', s, flags=re.I | re.S)
    if match:
        table_columns = match.group(1)

    if table_name != "" and table_columns != "":
        # Create the sql file
        create_sql(file_name, snnipetPath, table_name, table_columns)
    else:
        print("ERROR: The source file has no information about the temporary table and its columns. This information is required to load the data.")

print("Teradata MLOAD (python) to SQL Tool")
print("Processing input dir: " + input_directory)

if not os.path.exists(base_output_dir):
    print(f"Creating output dir {base_output_dir}")
    os.makedirs(base_output_dir)

for dirpath, dirnames, files in os.walk(input_directory):
    print('Found directory: ' + dirpath)
    try:
        for file_name in files:
            process_file(file_name)
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")

print("Done!") 
