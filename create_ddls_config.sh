
#list of databases
DBS="'tutorial_db'"
DBS_EXCLUDE="'SYS_CALENDAR','ALL','CONSOLE','CRASHDUMPS','DBC','DBCMANAGER','DBCMNGR','DEFAULT','EXTERNAL_AP','EXTUSER','LOCKLOGSHREDDER','PDCRADM','PDCRDATA','PDCRINFO','PDCRSTG','PDCRTPCD','PUBLIC','SQLJ','SYSDBA','SYSADMIN','SYSBAR','SYSJDBC','SYS_MGMT','SYSLIB','SYSSPATIAL','SYSTEMFE','SYSUDTLIB','SYSUIF','TD_SERVER_DB','TD_SYSFNLIB','TD_SYSFNLIB','TD_SYSGPL','TD_SYSXML','TDMAPS','TDPUSER','TDQCD','TDSTATS','TDWM','VIEWPOINT'"

# list of databases from which to export tables
DBS_TABLES=$DBS
DBS_TABLES_EXCLUDE=$DBS_EXCLUDE
TABLES_INCLUDE="'%'"

# list of databases from which to export join indexes
DBS_JOININDEX=$DBS
JOININDEX_INCLUDE="'%'"

# list of databases from which to export views
DBS_VIEWS="$DBS"
VIEWS_INCLUDE="'%'"
# list of databases from which to export functions
DBS_FUNCTIONS="$DBS"
FUNCTIONS_INCLUDE="'%'"

# list of databases from which to export macros
DBS_MACROS="$DBS"
MACROS_INCLUDE="'%'"

# list of database form which to export procedures
DBS_PROCEDURES="$DBS"
PROCEDURES_INCLUDE="'%'"
    