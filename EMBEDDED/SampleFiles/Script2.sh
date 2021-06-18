#/***********************************************************************************/
#!/usr/bin/ksh

echo 'Extracting all tables of the AdventureWorksDW database'

Workfile=$RUN_WORK_DIR/MyExportFile1.txt

bteq << EOF

.logon $TERADATA_DATABASE/$TERADATA_USER,$TERADATA_PASSWORD;

.EXPORT DATA FILE =${Workfile};
.SET WIDTH 300;
.SET RECORDMODE OFF; 
.SET FORMAT OFF; 
.SET TITLEDASHES OFF;
SELECT  DatabaseName,TableName,CreateTimeStamp,LastAlterTimeStamp
FROM    DBC.TablesV
WHERE   DatabaseName = 'AdventureWorksDW'
ORDER BY    TableName;
.EXPORT RESET

.logoff;
.quit;

EOF


