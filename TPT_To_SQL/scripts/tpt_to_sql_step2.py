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
#  TPT to SQL Scripts:
#  This is a helper utility consisting of two steps to convert TPT files to SQL.
#  
#  This is the step 2. This step takes the converted SQL snippets and embeds the code into the preliminary 
#  file generating the final SQL file.
#
#  Parameters:
#  -- inputdir: This is the directory where your preprocessed SQL files and snippets are
#  -- outdir: This is the directory where the final SQL files will be put
#
# Changes History
#    20220209-TGM: 
#      - Initial Version
# 
##########################################################################################################

import argparse
import os
import glob
from shutil import copyfile
import sys

arguments_parser = argparse.ArgumentParser(description="TPT to SQL Tool: Step 2")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your preprocessed SQL files and snippets are')
arguments_parser.add_argument('--outdir', required=True, help='This is the directory where the final SQL files will be put')
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir
output_directory = arguments.outdir

# Description: 
#   This method finds the SQL fragments of the file to be processed and replaces the @@ placeholders with the corresponding code.
#   Finally, it generates the complete SQL file in the output directory
# Parameters:
#  - filename: name of the file being processed
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


print("TPT to SQL Tool: Step 2")
print(f'Processing folder {input_directory}')

# Get the list of the files in the input directory to be process
# Only get the *.sql files in the root directory
os.chdir(input_directory)
for file in glob.glob("*.sql"):
    try:
        print(f"\t\tProcessing file: {file}")
        os.chdir(input_directory)
        process_file(file)
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")

print("Done!") 