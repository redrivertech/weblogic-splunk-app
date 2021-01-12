import os
from java.util import Date
from java.text import SimpleDateFormat


print 'Starting JMX Data Extraction'

curr_index = sys.argv[1]
adminsvr = os.environ['ADMIN_SERVER_'+curr_index]
adminsvrport = os.environ['ADMIN_PORT_'+curr_index]

admin_url = "t3://localhost:" + adminsvrport

# below  connect method requires the WLST be invoked from the domain directory and uses encrypted credentials to avoid plantext credentials; userConfigFile and userKeyFile can be created manually using StoreUserConfig using WLST: more in README
connect(userConfigFile='D:\somedirectory\myuserconfigfile.secure', userKeyFile='D:\somedirectory\myuserkeyfile.secure',url=admin_url,adminServerName=adminsvr)

# this connect method requires the WLST be invoked from the domain directory and below connect method uses plain text credentails
#connect(url=admin_url,adminServerName=adminsvr)


splunkHomeDir = ''
try:  
   splunkHomeDir = os.environ['SPLUNK_HOME']
except KeyError: 
   print "Please set the environment variable SPLUNK_HOME"
   sys.exit(1)
	
#logFileName = splunkHomeDir + '\\var\\log\\wls_jmx.log'
#logFileName = os.path.join(os.environ['SPLUNK_HOME'], "var", "log", "wls_jmx.log")
#logFileName = os.path.join(splunkHomeDir, "var", "log", "wls_jmx.log")
logFileName = os.path.join(splunkHomeDir, "var", "log", "wls_jmx_daily.log")

logFile = open(logFileName,'a')

def writeServerData(dataStr):
	currTime=SimpleDateFormat("MMM dd, yyyy hh:mm:ss a zzz").format(Date())
	logStr = "timestamp=%s|%s\n" % ( currTime, dataStr )
	logFile.write(logStr)

	

domainRuntime = domainRuntime()

cd('ServerRuntimes')
servers = domainRuntimeService.getServerRuntimes()
for server in servers:
   # serverNameStr=server.getName()
	cd ('/ServerRuntimes/' + server.getName() )
	serverDataStr = "domain=%s|server=%s|server_version=%s|server_port=%s" % ( domainRuntime.getName(), server.getName(), str(cmo.getWeblogicVersion()), str(cmo.getListenPort()) )
	writeServerData(serverDataStr)
	
	cd ('/ServerRuntimes/' + server.getName() + '/JVMRuntime/'  + server.getName())
	jvmDataStr = "domain=%s|server=%s|jvm_heap_size_max=%s" % ( domainRuntime.getName(), server.getName(), str(cmo.getHeapSizeMax()) )
	jvmDataStr = jvmDataStr + "|jvm_uptime=%s" % ( str(cmo.getUptime()) )
	jvmDataStr = jvmDataStr + "|jvm_vendor=%s" % ( str(cmo.getJavaVMVendor()) )
	jvmDataStr = jvmDataStr + "|java_vendor=%s" % ( str(cmo.getJavaVendor()) )
	jvmDataStr = jvmDataStr + "|java_version=%s" % ( str(cmo.getJavaVersion()) )
	jvmDataStr = jvmDataStr + "|os_name=%s" % ( str(cmo.getOSName()) )
	jvmDataStr = jvmDataStr + "|os_version=%s" % ( str(cmo.getOSVersion()) )
	writeServerData(jvmDataStr)	
