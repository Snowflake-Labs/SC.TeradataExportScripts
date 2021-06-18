STAGE_DB_NAME=${ENVDB}_STG
mload <<!
$LOGON;
INSERT INTO ${STAGE_DB_NAME}."DimCurrency"  
	("CurrencyKey", "CurrencyAlternateKey", "CurrencyName")  
VALUES
	($CURRENCY_KEY, $CURRENCY_ALTERNATE_KEY, $CURRENCY_NAME);

.END MLOAD;
.LOGOFF;

QUIT;
!
