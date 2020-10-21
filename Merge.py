import sys
import re
import json
import os

jsonFile = sys.argv[1]
inputFolder = sys.argv[2]
outputFolder = sys.argv[3]

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

if (not os.path.exists(outputFolder)):
    os.makedirs(outputFolder)

with open(jsonFile) as json_file:
    data = json.load(json_file)
    fileSource = "";
    sqlMergedFile = None
    for p in data:
        if fileSource != p["source"]:
            if sqlMergedFile != None:
                sqlMergedFile.close()
                sqlMergedFile = None
            filePath = os.path.join(outputFolder,p["source"])
            sqlMergedFile = open(filePath,"w+")
            fileSource = p["source"]
        folderSchema = "" if p["schema"] is None else p["schema"] + "\\"
        object_name = p["type"] + "\\" + folderSchema + p["object_name"]
        sqlSpPath = os.path.join(inputFolder,object_name + get_proper_extension(p["type"]))
        if os.path.exists(sqlSpPath):
            sqlFile = open(sqlSpPath,"r")
            sqlFileContent = sqlFile.read()
            sqlFile.close()
            sqlMergedFile.write(sqlFileContent + "\n")
    
