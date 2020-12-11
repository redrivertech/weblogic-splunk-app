@ECHO OFF

set BEA_HOME=C:\oracle\Middleware


set SPLUNK_HOME=C:\\Program Files\\SplunkUniversalForwarder
set JMX_LOGFILE_MAX_SIZE=100000

@rem Set the count for each domain set in the next section
set DOMAIN_COUNT=1

@rem ## For each domain on this server, add the domain path, adminServerName and admin port
@rem ## Please make sure that the entries are in the respective order

set DOMAIN_PATH_1=C:\oracle\Middleware\wlserver_10.3\samples\domains\medrec
set ADMIN_SERVER_1=MedRecServer
set ADMIN_PORT_1=7011

@rem #set DOMAIN_PATH_2=C:\oracle\Middleware\wlserver_10.3\samples\domains\medrec
@rem #set ADMIN_SERVER_2=MedRecServer
@rem #set ADMIN_PORT_2=7011

@ECHO ON
