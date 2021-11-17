import sys
import re
import os
import json
import argparse


arguments_parser = argparse.ArgumentParser(description="DDLs file splitter for SnowConvert")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your DDL_xxx.sql files are')
arguments_parser.add_argument('--outdir', required=True, help='This is the directory where the splitted files will be put')
arguments_parser.add_argument('--duplicates', help='If given duplicate files will be stored on this directory. NOTE: do not put this directory in the the same output directory, this way when running SnowConvert you can just point it to the directory where the splitted files are')
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir
base_output_dir = arguments.outdir


extracted_counts = {}


def element_already_extracted(full_object_name):
    if full_object_name in extracted_counts.keys():
        return True
    else:
        return False

def update_extraction_count(full_object_name): 
    previous_count = 0
    if full_object_name in extracted_counts.keys():
        previous_count = extracted_counts[full_object_name]
    extracted_counts[full_object_name] = previous_count + 1

def get_proper_target_directory(kind, schema, duplicates = False):
    #if (kind == "table"):
    #    return os.path.join(base_output_dir, kind)
    if (kind=="table" or kind == "view" or kind == "procedure" or kind == "macro" or kind == "function" or kind == "index" or kind == "materialized_view" or kind == "sequence" or kind == "dblink" or kind == "synonym" or kind == "trigger" or kind == "type" or kind == "package"):
        if (schema is not None):
            if duplicates:
                return os.path.join(arguments.duplicates, kind, schema)
            else:
                return os.path.join(base_output_dir, kind, schema)
    if (kind == "schema"):
        if duplicates:
            return os.path.join(arguments.duplicates, kind)
        else:
            return os.path.join(base_output_dir, kind)
    if duplicates:
        return arguments.duplicates
    else:
        return base_output_dir

def get_proper_extension(kind):
    if (kind == "view"):
        return ".sql"
    if (kind == "table"):
        return ".sql"
    if (kind == "macro"):
        return ".sql"
    if (kind == "procedure"):
        return ".sql"
    if (kind == "function"):
        return ".sql"
    if (kind == "schema"):
        return ".sql"
    if (kind == "index"):
        return ".sql"
    if (kind == "materialized_view"):
        return ".sql"
    if (kind == "sequence"):
        return ".sql"
    if (kind == "dblink"):
        return ".sql"
    if (kind == "synonym"):
        return ".sql"
    if (kind == "trigger"):
        return ".sql"
    if (kind == "type"):
        return ".sql"
    if (kind == "package"):
        return ".sql"      
    return "."+kind


def process_file(input_directory, input_file):
    pathFile = input_directory + os.path.sep + input_file
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
            print(f"Error opening file {[pathFile]} please review encoding and file permissions")
            s = ""
    p = s.replace("/* <sc-","/* <cconv> *//* <sc-")
    delimiter = "/* <cconv> */"
    stmnts = p.split(delimiter)

    if len(stmnts) > 0:
        i = 1
        while i < len(stmnts):
            sp = stmnts[i]
            matches = re.search("<sc-(.*)>(.*)\<.sc-(.*)\>",sp)
            if (matches is not None):
                groups = matches.groups()
                kind = groups[0].lower()
                full_object_name = groups[1].lower().strip()
                object_name = full_object_name
                schema = None
                if ("." in full_object_name):
                    parts = full_object_name.split(".")
                    schema = parts[0]
                    object_name = parts[1]
                element_info = {"full_object_name": full_object_name, "object_name":object_name, "schema":schema, "type": kind, "source": input_file, "position": i}
                elements.append(element_info)
                print("Extracting " +  full_object_name)
                # We need to make sure the target dir exists
                target_dir = get_proper_target_directory(kind, schema)
                if (not os.path.exists(target_dir)):
                    os.makedirs(target_dir)
                target_filename = os.path.join(target_dir,object_name + get_proper_extension(kind))
                is_duplicate = False
                if element_already_extracted(full_object_name):
                    is_duplicate = True
                    print(f"    >>  Duplicate found for {full_object_name}")
                    target_dir = get_proper_target_directory(kind, schema, True)
                    target_filename = os.path.join(target_dir,object_name + "_" + str(extracted_counts[full_object_name]) + get_proper_extension(kind))
                    duplicate_dir = os.path.dirname(target_filename)
                    # check if duplicates dir was given
                    if arguments.duplicates:
                        if (not os.path.exists(duplicate_dir)):
                            os.makedirs(duplicate_dir)
                update_extraction_count(full_object_name)
                if is_duplicate and not arguments.duplicates:
                    pass
                else:
                    f = open(target_filename,"w+")
                    f.write(sp)
                    f.close()
            i += 1
        

print("DDLs files splitter")
print(f"Processing input dir: {input_directory}")
# Walking a directory tree and printing the names of the directories and files
for dirpath, dirnames, files in os.walk(input_directory):
    print(f'Found directory: {dirpath}')
    elements = []
    for file_name in files:
        fname, fextension = os.path.splitext(file_name)
        fextension = fextension.lower()
        if (fextension == ".sql"):
            print("Processing file " +  file_name)
            process_file(input_directory, file_name)
    jsonFilePath = os.path.join(base_output_dir, "Names.json")
    with open(jsonFilePath, 'w+') as outfile:
            json.dump(elements, outfile)


print("Done")
