##Set your WebLogic home path here
export BEA_HOME=/opt/weblogic

##Set your Splunk home path here
export SPLUNK_HOME=/opt/splunkforwarder

##Set your total number of domains here
export DOMAIN_COUNT=1

## For each domain on this server, add the domain path, adminServerName and admin port
## Please make sure that the entries are in the respective order
export DOMAIN_PATH_1=/opt/weblogic/user_projects/domains/wcsDomain/
export ADMIN_SERVER_1=AdminServer
export ADMIN_PORT_1=7001

#export DOMAIN_PATH_2=/path/to/your/weblogic/domain/
#export ADMIN_SERVER_2=enterAdminServerNamehere
#export ADMIN_PORT_2=enterAdminPortHere

#export DOMAIN_PATH_3=/path/to/your/weblogic/domain/
#export ADMIN_SERVER_3=enterAdminServerNamehere
#export ADMIN_PORT_3=enterAdminPortHere

#export DOMAIN_PATH_4=/path/to/your/weblogic/domain/
#export ADMIN_SERVER_4=enterAdminServerNamehere
#export ADMIN_PORT_4=enterAdminPortHere

export JMX_LOGFILE_MAX_SIZE=100000
