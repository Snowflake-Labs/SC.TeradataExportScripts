# Documentation for extract_snippets.py

This script requires python 3.7 to correct properly.

The supported parameters of the script are:

```shell
python extract_snippets.py -h
usage: extract_snippets.py [-h] --inputdir INPUTDIR --outdir OUTDIR --verbose

BTEQ/MLOAD/FLOAD embeded shell script extractor for SnowConvert

optional arguments:
  -h, --help           show this help message and exit
  --inputdir INPUTDIR  This is the directory where your *.sh or *.ksh files
                       are
  --outdir OUTDIR      This is the directory where the splitted files will be
                       put
  --verbose            If this is specified all the files that are being copied 
                       and processed will be displayed
  --no-verbose         If this is specified none of the copied and processed will 
                       be displayed, this is the default behaviour                       

```

After running this script there will .pre.sh files, .snippet1.bteq, snippets.mload files depending on the tags found in the input files.
And there will be two summary files generated at the root of the output directory with information on the generated files:
* summary_input.csv
* summary_output.csv

Each input file will be tried to be read in several encodings configured internally:
* UTF-8
* ISO-8859-1

The first encoding that works will be used and their generated files will also use that encoding.  In the summary files there will be the information of the encoding the script found for each input and output file.

The summary of the output is a csv containing the followin columns:
* ENCODING: the encoding that the file was read
* FILE: the full file path name of the file
* HAS_EMBEDDED: True if the file has embedded blocks of bteq, fload or mload, False otherwise
* NUM_SNIPPETS: The number of snippets extracted
* SNIPPETS_TYPES: The list of snippets generated like bteq, fload, mload or both

The summary of the input is a csv containing the following columns:
* ENCODING: the encoding that the file was written
* FILE: the relative file path name of the file
* REMOVED_EMBEDDED: True if the file removed the embedded script files, False otherwise
* IS_GENERATED_SNIPPET: True if the file was a generated snippet

