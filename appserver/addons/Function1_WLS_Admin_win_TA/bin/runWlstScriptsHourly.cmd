@ECHO OFF

call "%1\etc\apps\function1_weblogicserver_ta_win\bin\setWlstEnv.cmd"

SETLOCAL EnableDelayedExpansion

FOR /L %%i IN (1,1,%DOMAIN_COUNT%) DO (
	IF EXIST !DOMAIN_PATH_%%i! (
		@rem Need to CD to the domain dir so that the user authentication is picked up from the boot.properties file
		cd !DOMAIN_PATH_%%i!
                @rem Invoke WLST
                java -cp "%2\wlserver_10.3\server\lib\weblogic.jar" weblogic.WLST "%1\etc\apps\function1_weblogicserver_ta_win\bin\wlsCollectJmxDataHourly.py" %%i
	)	
)
