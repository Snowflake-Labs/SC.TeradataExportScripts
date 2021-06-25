
# Teradata DDL Export Sample Script

Sometimes you need to generate DDL scripts for all the objects in your
teradata databases.

These scripts are provided as a reference to perform that task.

# How to use these scripts

## To Extract Teradata DDL Code

Download or clone the repository into your server. Lets say under a folder called `extract`

Once you are in that folder:

- Create an output folder
`mkdir out`

- add your settings in the `create_ddl_config.sh` in that file you can specify which database(s) to export and which elements to include

- run the `create_ddls.sh` script
For example for host: `localhost` user: `dbc` and password: `dbc` and output folder: `out` use this:

```shell
./create_ddls.sh localhost dbc dbc ./out
```

After execution go to the output folder. All your scripted objects will be in DDL_xxx.sql files

You can look at a sample extraction in the **SampleOutput** folder in this repo.

# Handling Shell scripts with BTEQ

## To handle embedded BTEQ Code inside shell scripts like `.ksh` or `.sh` 

It is very common to encounter scenarios where you have embedded BTEQ inside your shell scripts.
For example something like this:

```bash
echo 'unix command'
echo 'unix command'
bteq << EOF
.logon <systemid>/<userid>,<password>;
select current_timestamp;
.logoff;
.quit;
EOF
echo 'unix command 3'
echo 'unix command 4'
echo 'unix command 5'
```

In those scenarios you can use these helpers scripts. You can run them like this:

```bash
python extract_snippets.py -h
usage: extract_snippets.py [-h] --inputdir INPUTDIR --outdir OUTDIR --verbose

BTEQ/MLOAD embeded shell script extractor for SnowConvert

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

```bash
python extract_snippets.py --inputdir source_dir_with_shell_scripts --outdir target_dir_with_extracted_bteq 
```

This script will generate several files like:
* shell_script_with_embedded_bteq.sh.pre.sh
* shell_script_with_embedded_bteq.sh.snippet.1.bteq

You can then feed those bteq files to the migration tool. Just point it to the `target_dir_with_extracted_bteq`

After migration just run

```bash
python restore_snippets.py outputdir
```

And it will rebuild your original file replacing your 

```bash
bteq << EOF
.REMARK bteq code
EOF
```

fragments by 
```bash
python <<END_SNOWSCRIPT
print("bteq code")
END_SNOWSCRIPT
```
## To handle embedded MLOAD Code

It is very common to encounter scenarios where you have embedded MLOAD inside your shell scripts.
For example something like this:

```bash
STAGE_DB_NAME=${ENVDB}_STG
mload <<!
$LOGON;
INSERT INTO ${STAGE_DB_NAME}.INVLIST_MLD
      (INVLIST
      ,INVMAP) 
VALUES 
      (1
      ,'test');

.END MLOAD;
.LOGOFF;

QUIT;
!
```

In those scenarios you can use these helpers scripts. You can run them like this:

```bash
python extract_snippets.py -h
usage: extract_snippets.py [-h] --inputdir INPUTDIR --outdir OUTDIR

BTEQ/MLOAD embeded shell script extractor for SnowConvert

optional arguments:
  -h, --help           show this help message and exit
  --inputdir INPUTDIR  This is the directory where your *.sh or *.ksh files
                       are
  --outdir OUTDIR      This is the directory where the splitted files will be
                       put

```

```bash
python extract_snippets.py --inputdir source_dir_with_shell_scripts --outdir target_dir_with_extracted_mload 
```

This script will generate several files like:
* test.mload.invlist.mload.pre.sh
* test.mload.invlist.mload.snippet.1.mload

You can then feed those mload files to the migration tool.

After migration just run

```bash
python restore_snippets.py --inputdir INPUTDIR
```
>> NOTE: the tool assumes that the given input directory contains the files that were preprocessed. For example the *.pre.sh and the migrated .mload files as well.


And it will rebuild your original files replacing your 
```bash
mload <<!
.REMARK mload code
!
```
fragments by 

```bash
python <<END_SNOWSCRIPT
print("mload code")
END_SNOWSCRIPT
```

# To Split the DDLs files.

Sometimes the DDLs files can be too big or have duplicates.
This script will split then like this:
```
+ output_folder
+ -- table
+ -- schema
+ -- procedure
+ -- macro
+ -- joinindex
```

Inside each folder a subfolder with the database name will be created, and then one file for each element.

```
$ python3 split_ddls.py -h
usage: split_ddls.py [-h] --inputdir INPUTDIR --outdir OUTDIR [--duplicates DUPLICATES]

DDLs file splitter for SnowConvert

optional arguments:
  -h, --help            show this help message and exit
  --inputdir INPUTDIR   This is the directory where your DDL_xxx.sql files are
  --outdir OUTDIR       This is the directory where the splitted files will be put
  --duplicates DUPLICATES
                        If given duplicate files will be stored on this directory. NOTE: do not put this directory in the the same output directory, this way when running SnowConvert you can just point
                        it to the directory where the splitted files are
```
