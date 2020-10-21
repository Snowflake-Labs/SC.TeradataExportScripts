
# Teradata DDL Export Sample Script

Sometimes you need to generate DDL scripts for all the objects in your
teradata databases.

These scripts are provided as a reference to perform that task.

# How to use these scripts

Download or clone the repository into your server. Lets say under a folder called `extract`

Once you are in that folder:

- Create an output folder
`mkdir out`

- add your settings in the `create_ddl_config.sh` in that file you can specify which database(s) to export and which elements to include

- run the `create_ddls.sh` script
For example for host: `localhost` user: `dbc` and password: `dbc` and output folder: `out` use this:

```
./create_ddls.sh localhost dbc dbc ./out
```

After execution go to the output folder. All your scripted objects will be in DDL_xxx.sql files

You can look at a sample extraction in the **SampleOutput** folder in this repo.
