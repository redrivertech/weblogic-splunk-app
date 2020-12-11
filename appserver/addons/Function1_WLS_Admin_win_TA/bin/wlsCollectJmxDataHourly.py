import os
from java.util import Date
from java.text import SimpleDateFormat


print 'Starting JMX Data Extraction'

curr_index = sys.argv[1]
adminsvr = os.environ['ADMIN_SERVER_'+curr_index]
adminsvrport = os.environ['ADMIN_PORT_'+curr_index]

admin_url = "t3://localhost:" + adminsvrport

# this connect method requires the WLST be invoked from the domain directory
connect(url=admin_url,adminServerName=adminsvr)
	
splunkHomeDir = ''
try:  
   splunkHomeDir = os.environ['SPLUNK_HOME']
except KeyError: 
   print "Please set the environment variable SPLUNK_HOME"
   sys.exit(1)

#logFileName = splunkHomeDir + '\\var\\log\\wls_jmx.log'
#logFileName = os.path.join(os.environ['SPLUNK_HOME'], "var", "log", "wls_jmx.log")
#logFileName = os.path.join(splunkHomeDir, "var", "log", "wls_jmx.log")
logFileName = os.path.join(splunkHomeDir, "var", "log", "wls_jmx_hourly.log")
   
# Check the log file size and roll the file as needed
logfileMaxSize = os.environ['JMX_LOGFILE_MAX_SIZE']
try:  
   os.environ['JMX_LOGFILE_MAX_SIZE']
except KeyError: 
   print "Please set the environment variable JMX_LOGFILE_MAX_SIZE"
   sys.exit(1)

   
#if logPath:
#logFileName = splunkHomeDir + '\\var\\log\\wls_jmx.log'
#else:
#logFileName = "splunk_test_wls_jmx.log"


# roll log file if needed
#fsize = os.path.getsize(logFileName)
#if fsize > int(logfileMaxSize) :
#	os.rename(logFileName, logFileName+".1")

logFile = open(logFileName,'a')

def writeServerData(dataStr):
	currTime=SimpleDateFormat("MMM dd, yyyy hh:mm:ss a zzz").format(Date())
	logStr = "timestamp=%s|%s\n" % ( currTime, dataStr )
	logFile.write(logStr)


domainRuntime = domainRuntime()


cd('ServerRuntimes')
servers = domainRuntimeService.getServerRuntimes()
if (len(servers) > 0):
	for server in servers:
		cd ('/ServerRuntimes/' + server.getName() )
		serverDataStr = "domain=%s|server=%s|server_state=%s|server_health=%s" % ( domainRuntime.getName(), server.getName(), str(cmo.getState()), str(cmo.getHealthState()) )
		writeServerData(serverDataStr)
		cd ('/ServerRuntimes/' + server.getName() + '/ThreadPoolRuntime/ThreadPoolRuntime')
		threadPoolDataStr = "domain=%s|server=%s|throughput=%s" % ( domainRuntime.getName(), server.getName(), str(cmo.getThroughput()) )
		threadPoolDataStr = threadPoolDataStr + "|total_threads=%s" % ( str(cmo.getExecuteThreadTotalCount()) )
		threadPoolDataStr = threadPoolDataStr + "|completed_reqs=%s" % ( str(cmo.getCompletedRequestCount()) )
		writeServerData(threadPoolDataStr)
		
		jmsRuntime = server.getJMSRuntime();
		jmsServers = jmsRuntime.getJMSServers();

		jmsRuntimeStr = "domain=%s|server=%s|jms_health=%s" % ( domainRuntime.getName(), server.getName(), jmsRuntime.getHealthState() )
		jmsRuntimeStr = jmsRuntimeStr + "|jms_server_count=%s|jms_total_connections=%s" % ( str(jmsRuntime.getJMSServersCurrentCount()), str(jmsRuntime.getConnectionsTotalCount()) )
		writeServerData(jmsRuntimeStr)
		
		for jmsServer in jmsServers:
			jmsServerDataStr = "domain=%s|server=%s|jms_server=%s" % ( domainRuntime.getName(), server.getName(), jmsServer.getName() )
			jmsServerDataStr = jmsServerDataStr + "|jms_messages_received_count=%s|jms_destination_count=%s" % ( str(jmsServer.getMessagesReceivedCount()), str(jmsServer.getDestinationsCurrentCount()) )
			writeServerData(jmsServerDataStr)
			
		jdbcRuntime = server.getJDBCServiceRuntime();
		datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans();
		for datasource in datasources:
			jdbcDataStr = "domain=%s|server=%s" % ( domainRuntime.getName(), server.getName() )
			jdbcDataStr = jdbcDataStr + "|jdbc_datasource_name=%s|jdbc_connection_count=%s" % ( datasource.getName(), repr(datasource.getConnectionsTotalCount()) )
			writeServerData(jdbcDataStr)

	

#cd('/AppRuntimeStateRuntime/AppRuntimeStateRuntime')
#appList = cmo.getApplicationIds()
#for app in appList:
#	appStateStr = "domain=%s|app=%s|app_state=%s" % ( domainRuntime.getName(), app , cmo.getIntendedState(app) )
#	writeServerData( appStateStr );
	
