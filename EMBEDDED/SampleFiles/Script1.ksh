#/***********************************************************************************/
#!/usr/bin/ksh

echo 'Inserting rows on a table'

$BTEQ_COMMAND << EOB

.LOGON $TERADATA_ID/$TERADATA_USER,$TERADATA_PASSWORD
BEGIN TRANSACTION ;
INSERT INTO "AdventureWorksDW"."DimCurrency"  ("CurrencyKey", "CurrencyAlternateKey", "CurrencyName")  VALUES($CURRENCY_KEY, $CURRENCY_ALTERNATE_KEY, $CURRENCY_NAME);
END TRANSACTION ;
.LOGOFF
.EXIT

EOB

ReturnCode=$?
 
if [ ${ReturnCode} -eq 0 ] 
then
echo "BTEQ script completed successfully"
exit 0
else
echo "BTEQ script failled"
exit 1
fi
