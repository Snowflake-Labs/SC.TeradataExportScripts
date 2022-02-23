#*** Generated code is based on the SnowConvert Python Helpers version 2.0.6 ***
 
import os

import sys

import snowconvert.helpers

from snowconvert.helpers import Export
from snowconvert.helpers import exec
con = None

def main():
   snowconvert.helpers.configure_log()
   con = snowconvert.helpers.log_on()
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. .LOGTABLE DB_TEST.DWCCR138_TABLE **
    
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. .RUN FILE DWLOGPRD **
    
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. .RUN FILE DECCR138 **
    
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. .BEGIN IMPORT MLOAD
   #       TABLES  REFERENCE.TABLE_TAX_SRCHRG_EXMPTN_RULE
   #   WORKTABLES  DB_TEST.WT_EXAMPLE_TABLE
   #  ERRORTABLES  DB_TEST.ET_EXAMPLE_TABLE
   #               DB_TEST.UV_EXAMPLE_TABLE **
    
   TABLE_LAYOUT_TableName = "TABLE_LAYOUT_TEMP_TABLE"
   TABLE_LAYOUT_Columns = """
COLUMN1_TYPE CHAR(00001),
LD_COLUMN2_RECTYPE CHAR(00003)"""
   TABLE_LAYOUT_Query = "*"

   def INSERT_TABLE(tempTableName, queryFields, queryConditions = ""):
      exec(f"""INSERT INTO REFERENCE.TABLE_TAX_EXAMPLE SELECT {queryFields} FROM {tempTableName} {queryConditions}""")
   snowconvert.helpers.import_file_to_temptable("DATAIN", TABLE_LAYOUT_TableName, TABLE_LAYOUT_Columns)
   INSERT_TABLE(TABLE_LAYOUT_TableName, TABLE_LAYOUT_Query, "WHERE COLUMN1_TYPE = 1")
   snowconvert.helpers.drop_transient_table(TABLE_LAYOUT_TableName)
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. 
   #/*********************************************************************/
   #
   #.IF &SYSRC > 0 THEN;
   #   .LOGOFF &SYSRC;
   #.ENDIF; **
    
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. 
   #.IF &SYSETCNT > 0  THEN;
   #--   .SET RETURNCD TO 01
   #                      ;
   #
   #   RENAME TABLE DB_TEST.ET_EXAMPLE_TABLE
   #             TO DB_TEST.ET_EXAMPLE_TABLE_&SYSDAY&SYSUVCNT;
   #      .IF &SYSRC <> 0;DISPLAY 'ET RENAME UNSUCCESSFUL' TO FILE SYSPRINT;
   #      .LOGOFF &SYSRC;
   #      .ENDIF;
   #.ENDIF; **
    
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. 
   #.IF &SYSUVCNT > 0  THEN;
   #--   .SET RETURNCD TO 02
   #                      ;
   #
   #   RENAME TABLE DB_TEST.UV_EXAMPLE_TABLE
   #             TO DB_TEST.UV_EXAMPLE_TABLE_&SYSDAY&SYSUVCNT;
   #      .IF &SYSRC <> 0;DISPLAY 'UV RENAME UNSUCCESSFUL' TO FILE SYSPRINT;
   #      .LOGOFF &SYSRC;
   #      .ENDIF;
   #.ENDIF; **
    
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. 
   #.IF &SYSETCNT > 0  AND &SYSUVCNT > 0 THEN;
   #--   .SET RETURNCD TO 03
   #                      ;
   #.ENDIF; **
    

   if con is not None:
      con.close()
      con = None
   snowconvert.helpers.quit_application()

if __name__ == "__main__":
   main()