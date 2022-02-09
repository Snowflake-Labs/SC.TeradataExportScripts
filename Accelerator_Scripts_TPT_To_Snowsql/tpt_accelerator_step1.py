

import argparse
import os
import re
import glob
from shutil import copyfile
from tkinter import E

# import module sys to get the type of exception
import sys

arguments_parser = argparse.ArgumentParser(description="TPT Preprocessing tool")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your *.tpt files are')
arguments_parser.add_argument('--outdir', required=True, help='This is the directory where the SQL preprocessed files will be put')
arguments_parser.set_defaults(verbose=False)
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir
output_directory = arguments.outdir

class Schema:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

class Operator:
    def __init__(self, name, type, schema, attributes):
        self.name = name
        self.type = type,
        self.schema = schema,
        self.attribtutes = attributes

class Apply:
    def __init__(self, id, statement):
        self.id = id
        self.statement = statement

appliesCount = 0
merge_flag = r"INSERT\s+FOR\s+MISSING\s+UPDATE\s+ROWS"

def read_schema(index, lines):
    i = 0
    content = ''
    current_line = lines[index]
    match = re.search(r"DEFINE\s+SCHEMA\s+(\w+)",current_line)
    schema_name = match.group(1)
    while i < len(lines):
        current_line = lines[i]
        if i > index:
            if lines[i].find(");") >= 0:
                break
            else:
                content = content + lines[i]
        i = i + 1
    schema_columns = content
    return Schema(schema_name, schema_columns)

def read_operator(index, lines):
    i = 0
    content = ''
    operator_type = ''
    operator_schema = ''
    current_line = lines[index]
    match = re.search(r"DEFINE\s+OPERATOR\s+(\w+)",current_line)
    operator_name = match.group(1)
    while i < len(lines):
        current_line = lines[i]
        if i > index:
            match = re.search(r"^[\t\s]*TYPE\s+([\w\s]+)$",current_line)
            if match:
                operator_type =  match.group(1)
            else:
                match = re.search(r"^[\t\s]*SCHEMA\s+([\w\s\*]+)$",current_line)
                if match:
                    operator_schema =  match.group(1)
                else:
                    content = content + lines[i]
            if lines[i].find(");") >= 0:
                break
        i = i + 1
    operator_attributes = content
    return Operator(operator_name, operator_type, operator_schema, operator_attributes)

def read_apply(index, lines):
    i = 0
    content = ''
    applies = []
    while i < len(lines):
        if i > index:
            if lines[i].find(");") >= 0:
                break
            else:
                content = content + lines[i]
        i = i + 1
    statements = content.split(';')
    for stmt in statements:
        applies.append(Apply(0, stmt))
    return applies

def extract_sql_from_apply(apply, filename): 
    apply_contents = ''
    name = os.path.splitext(os.path.basename(filename))[0]       
    target_folder = os.path.join(input_directory,"snippets",name)
    target_file = os.path.join(target_folder, apply.id + ".sql")
    temp_table_name = f"TEMP_{name}"

    apply_contents = apply.statement.strip()                    # remove leading and trailing characters
    apply_contents = apply_contents.replace("''","'")           # remove double single quotes
    apply_contents = re.sub(r":(\w{1})","\\1",apply_contents)   # remove colons(:) in columns
    apply_contents = re.sub(r"@(\w+)",":\\1",apply_contents)    # change @variable by :variable

    if re.match(r".*INSERT\s+INTO.*", apply_contents, flags=re.I|re.S):
        apply_contents = re.sub(r"(.*)?(INSERT\s+INTO.*)", "\\2", apply_contents, flags=re.I|re.S)          # remove any content before INSERT statement
        apply_contents = re.sub(r"\)[\n\s]*VALUES[\n\s]*\(", ")\nSELECT ",apply_contents, flags=re.I|re.S)  # transform VALUES to SELECT
        apply_contents = apply_contents + f"\n FROM {temp_table_name}"                                      # add FROM clause

    if re.match(r".*UPDATE\s+.*", apply_contents, flags=re.I|re.S):
        apply_contents = re.sub(r"(.*)?(UPDATE\s+\w+.*)", "\\2", apply_contents, flags=re.I|re.S) # remove any content before UPDATE statement
        apply_contents = re.sub(r"(UPDATE\s+\w+\s+)(.*)", f"\\1 FROM {temp_table_name}\n\\2", apply_contents, flags=re.I|re.S) # add FROM clause

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with open(target_file,"w") as f:
        f.write(apply_contents)

def create_sql_template(filename, schemas, applies, merge_alert): 
    name = os.path.splitext(os.path.basename(filename))[0]
    target_file = os.path.join(output_directory, name + ".sql")

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    format_name = f"FORMAT_{name}"
    stage_name = f"STAGE_{name}"
    temp_table_name = f"TEMP_{name}"
    schema_columns = schemas[0].columns #TODO: Asumming the tpt file only has one schema definition
    contents = f"/*MSC-WARNING: File format definition must be changed according to the input file. More info https://docs.snowflake.com/en/sql-reference/sql/create-file-format.html*/\n"
    contents = contents + f"CREATE OR REPLACE FILE FORMAT {format_name} TYPE = 'CSV' FIELD_DELIMITER = '|' TRIM_SPACE = TRUE SKIP_HEADER = 0; \n--\n"
    contents = contents +  f"CREATE OR REPLACE TEMPORARY STAGE {stage_name};\n--\n"
    contents = contents + f"PUT file://&DirectoryPath/&FileName @{stage_name} OVERWRITE = TRUE AUTO_COMPRESS = FALSE;\n--\n"
    contents = contents + f"CREATE OR REPLACE TEMPORARY TABLE {temp_table_name} {schema_columns};\n--\n"
    contents = contents + f"COPY INTO {temp_table_name} FROM @{stage_name} FILE_FORMAT = (format_name = '{format_name}');\n"
    
    if merge_alert:
        contents = contents + f"\n/*MSC-WARNING: INSERT FOR MISSING UPDATE ROWS was found in TPT source file. It is posible some statements bellow must be converted to a single MERGE statement. More info: https://docs.snowflake.com/en/sql-reference/sql/merge.html*/"
        
    for apply in applies:
        contents = contents + f"--\n@@{apply.id}\n"

    with open(target_file,"w") as f:
        f.write(contents)

def process_file(filename):
    schemas = []
    operators = []
    applies = []
    extra = []
    appliesCount = 0
    merge_alert = False
    name = os.path.splitext(os.path.basename(filename))[0]

    lines = open(filename).readlines()
    index = 1
    while index < len(lines):
        current_line = lines[index].strip()
        if current_line.startswith("DEFINE SCHEMA"):
            schemas.append(read_schema(index, lines))
        else:
            if current_line.startswith("DEFINE OPERATOR"):
                operators.append(read_operator(index, lines))
            else:
                if current_line.startswith("APPLY"):
                    _applies = read_apply(index, lines)
                    for _apply in _applies:
                        appliesCount = appliesCount + 1
                        _apply.id = name + ".snippet." + str(appliesCount)
                        applies.append(_apply)
                else:
                    if re.match(merge_flag, current_line, flags=re.I):
                        merge_alert = True
                    extra.append(current_line)

        index = index + 1

    # After reading the file, extract and transform apply statements
    # Operators information are not needed in Snowflake normally.
    # Schemas information will be used to define temporary tables definition
    for apply in applies:
        extract_sql_from_apply(apply, filename)

    # Create template new SQL file
    create_sql_template(filename, schemas, applies, merge_alert)

print("Teradata TPTs Pre-process tool")
print(f'Processing folder {input_directory}')
# get list of files
os.chdir(input_directory)
for file in glob.glob("*.tpt"):
    try:
        print(f"\t\tProcessing file: {file}")
        process_file(file)
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")

print("Done!") 