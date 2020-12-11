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
logFileName = os.path.join(splunkHomeDir, "var", "log", "wls_jmx_minute.log")

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

		cd ('/ServerRuntimes/' + server.getName() + '/JVMRuntime/'  + server.getName())
		jvmDataStr = "domain=%s|server=%s|heap_size_current=%s" % ( domainRuntime.getName(), server.getName(), str(cmo.getHeapSizeCurrent()) )
		jvmDataStr = jvmDataStr + "|heap_free_current=%s" % ( str(cmo.getHeapFreeCurrent()) )
		jvmDataStr = jvmDataStr + "|heap_free_percent=%s" % ( str(cmo.getHeapFreePercent()) )
		writeServerData(jvmDataStr)

		cd ('/ServerRuntimes/' + server.getName() + '/ThreadPoolRuntime/ThreadPoolRuntime')
		threadPoolDataStr = "domain=%s|server=%s|throughput=%s" % ( domainRuntime.getName(), server.getName(), str(cmo.getThroughput()) )
		threadPoolDataStr = threadPoolDataStr + "|total_threads=%s" % ( str(cmo.getExecuteThreadTotalCount()) )
		threadPoolDataStr = threadPoolDataStr + "|completed_reqs=%s" % ( str(cmo.getCompletedRequestCount()) )
        	threadPoolDataStr = threadPoolDataStr + "|hogging_threads=%s" % ( str(cmo.getHoggingThreadCount()) )
        	threadPoolDataStr = threadPoolDataStr + "|pending_reqs=%s" % ( str(cmo.getQueueLength()) )
		writeServerData(threadPoolDataStr)
		
		jmsRuntime = server.getJMSRuntime();
		jmsServers = jmsRuntime.getJMSServers();

		for jmsServer in jmsServers:
			jmsServerDataStr = "domain=%s|server=%s|jms_server=%s" % ( domainRuntime.getName(), server.getName(), jmsServer.getName() )
			jmsServerDataStr = jmsServerDataStr + "|jms_current_messages_count=%s|jms_pending_messages_count=%s" % ( str(jmsServer.getMessagesCurrentCount()), str(jmsServer.getMessagesPendingCount()) )
			jmsServerDataStr = jmsServerDataStr + "|jms_current_connection_count=%s" % ( str(jmsRuntime.getConnectionsCurrentCount()) )
			writeServerData(jmsServerDataStr)
			
		jdbcRuntime = server.getJDBCServiceRuntime();
		datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans();
		for datasource in datasources:
			jdbcDataStr = "domain=%s|server=%s" % ( domainRuntime.getName(), server.getName() )
			jdbcDataStr = jdbcDataStr + "|jdbc_datasource_name=%s|jdbc_active_connection_count=%s" % ( datasource.getName(), repr(datasource.getActiveConnectionsCurrentCount()) )
			jdbcDataStr = jdbcDataStr + "|jdbc_connection_waiting_count=%s" % ( repr(datasource.getWaitingForConnectionCurrentCount()) )
			jdbcDataStr = jdbcDataStr + "|jdbc_available_connections=%s" % ( repr(datasource.getNumAvailable()) )
			writeServerData(jdbcDataStr)

		userLockRuntime = server.getServerSecurityRuntime().getDefaultRealmRuntime().getUserLockoutManagerRuntime();
		userLockStr = "domain=%s|server=%s" % ( domainRuntime.getName(), server.getName() )
		userLockStr = userLockStr + "|locked_users_count=%s|invalid_logins_total=%s" % ( repr(userLockRuntime.getLockedUsersCurrentCount()) , repr(userLockRuntime.getInvalidLoginAttemptsTotalCount()) )
		writeServerData(userLockStr)

#Commented out to add code below, which includes domain and server calls.
#cd('/AppRuntimeStateRuntime/AppRuntimeStateRuntime')
#appList = cmo.getApplicationIds()
#for app in appList:
#	appStateStr = "app=%s|app_state=%s" % ( app , cmo.getIntendedState(app) )
#	writeServerData( appStateStr );

cd('/AppRuntimeStateRuntime/AppRuntimeStateRuntime')
appList = cmo.getApplicationIds()
for app in appList:
	appStateStr = "domain=%s|server=%s|app=%s|app_state=%s" % ( domainRuntime.getName(), server.getName(), app , cmo.getIntendedState(app) )
	writeServerData( appStateStr );
