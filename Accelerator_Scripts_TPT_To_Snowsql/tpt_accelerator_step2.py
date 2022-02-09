

import argparse
import os
import glob
from shutil import copyfile
from tkinter import E

# import module sys to get the type of exception
import sys

arguments_parser = argparse.ArgumentParser(description="TPT Processing tool")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your preprocessed SQL files and snippets are')
arguments_parser.add_argument('--outdir', required=True, help='This is the directory where the final SQL files will be put')
arguments_parser.set_defaults(verbose=False)
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir
output_directory = arguments.outdir

def process_file(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    target_file = os.path.join(output_directory, name + ".sql")
    content = open(filename).read()
    os.chdir(os.path.join(input_directory, "snippets", name))
    for file in glob.glob("*.sql"):
        id = os.path.splitext(file)[0]
        snippet_content = open(file).read()
        content = content.replace(f"@@{id}", snippet_content)
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(target_file,"w") as f:
        f.write(content)

print("Teradata TPTs Process tool")
print(f'Processing folder {input_directory}')
# get list of files
os.chdir(input_directory)
for file in glob.glob("*.sql"):
    try:
        print(f"\t\tProcessing file: {file}")
        os.chdir(input_directory)
        process_file(file)
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")

print("Done!") 