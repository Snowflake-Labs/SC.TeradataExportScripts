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
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. .LOGTABLE DB_TEST.DWEXAMPLE002 **
    
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. .RUN FILE DWLOGPRD **
    
   #** MSC-WARNING - MSCEWI1002 - REMOVED NEXT STATEMENT, NOT APPLICABLE IN SNOWFLAKE. 
   #.BEGIN IMPORT MLOAD
   #       TABLES REFERENCE.T84008_TABLE
   #       WORKTABLES  DB_TEST.WT_EXAMPLE_TABLE
   #       ERRORTABLES DB_TEST.ET_EXAMPLE_TABLE
   #                   DB_TEST.UV_EXAMPLE_TABLE **
    
   EXAMPLE_LAYOUT_TableName = "EXAMPLE_LAYOUT_TEMP_TABLE"
   EXAMPLE_LAYOUT_Columns = """
RECTYPE CHAR(001),
TABLE_NUMBER CHAR(004)"""
   EXAMPLE_LAYOUT_Query = "*"
   exec("""
      UPDATE REFERENCE.EXAMPLE_TABLE
      SET
           TABLE_NAME     =:TABLE_NAME
          ,TABLE_CATEGORY =:TABLE_CATEGORY
     WHERE TABLE_NUMBER   =:TABLE_NUMBER
      """)
   exec("""
      INSERT INTO REFERENCE.EXAMPLE_TABLE (
      TABLE_NUMBER, TABLE_NAME) VALUES (:TABLE_NUMBER, :TABLE_NAME)
      """)
   snowconvert.helpers.import_file_to_temptable("DATAIN", EXAMPLE_LAYOUT_TableName, EXAMPLE_LAYOUT_Columns)
   U_EXAMPLE(EXAMPLE_LAYOUT_TableName)
   snowconvert.helpers.drop_transient_table(EXAMPLE_LAYOUT_TableName)
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
   #             TO DB_TEST.ET_EXAMPLE_&SYSDAY&SYSETCNT;
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
   #             TO DB_TEST.UV_EXAMPLE_&SYSDAY&SYSUVCNT;
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