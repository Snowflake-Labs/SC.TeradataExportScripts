import sys
import re
import os
import json

input_directory = sys.argv[1]
base_output_dir = sys.argv[2]

def get_proper_target_directory(kind, schema):
    #if (kind == "table"):
    #    return os.path.join(base_output_dir, kind)
    if (kind=="table" or kind == "view" or kind == "procedure" or kind == "macro" or kind == "function" or kind == "joinindex"):
        if (schema is not None):
            return os.path.join(base_output_dir, kind, schema)
    if (kind == "schema"):
        return os.path.join(base_output_dir, kind)
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
    if (kind == "joinindex"):
        return ".sql"
    return ".unknown"


def process_file(input_directory, input_file):
    pathFile = input_directory + os.path.sep + input_file
    f = open(pathFile, "r")
    s = f.read()
    f.close()
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
                f = open(target_filename,"w+")
                f.write(sp)
                f.close()
            i += 1
        


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
