"""Initial settings for centos 6.5 to install coloudera distribution of hadoop"""
import sys
import os

#PROPERTIES
IPADDR = sys.argv[1]
HOSTNAME="twi.datalab."+sys.argv[2]
NETMASK="255.255.252.0"
GATEWAY="10.132.2.254"
DNS1="10.10.1.1"
DNS2="8.8.8.8"

#STEP-1:
def set_static_IP():
	path_to_eth0 = "/etc/sysconfig/network-scripts/ifcfg-eth0"
	templete = """TYPE=Ethernet
ONBOOT=yes
BOOTPROTO=STATIC
IPV6INIT=no
USERCTL=no
NM_CONTROLLED=yes
PEERDNS=yes
IPADDR={IPADD}
NETMASK={NM}
GATEWAY={GW}
DNS1={DN1}
DNS2={DN2}
"""
	eth0 = open(path_to_eth0,"w")
	eth0.write(templete.format(IPADD = IPADDR, 
								NM = NETMASK, 
								GW = GATEWAY, 
								DN1 = DNS1, 
								DN2 = DNS2))
	eth0.close()

#STEP-2:
def configure_network():
	path_to_network = "/etc/sysconfig/network"
	templete = """NETWORKING=yes
NETWORKING_IPV6=no
HOSTNAME={HN}
GATEWAY={GW}
"""
	network = open(path_to_network,"w")
	network.write(templete.format(HN = HOSTNAME, GW = GATEWAY))
	network.close()

#STEP-3:
def configure_hosts():
	path_to_hosts = "/etc/hosts"
	templete = """127.0.0.1	localhost.localdomain localhost
::1	localhost6.localdomain6 localhost6
10.132.3.125    twi.datalab.node1    node1
10.132.3.126    twi.datalab.node2    node2
10.132.3.127    twi.datalab.node3    node3
10.132.3.128    twi.datalab.node4    node4
"""
	hosts = open(path_to_hosts,"w")
	hosts.write(templete)
	hosts.close()

#STEP-4:
def check_internet_connection():
	import socket
	try:
		remote_server = "www.google.com"
		host = socket.gethostbyname(remote_server)
		s = socket.create_connection((host,80),2)
		print("Internet and DNS both are working")
		return True
	except Exception as e:
		print >> sys.stderr, "Problem in either Internet or DNS Settings!!!"
		exit(1)
		
#STEP-5:
def disable_se_linux():
	path_to_selinux_conf = "/etc/selinux/config"
	data = open(path_to_selinux_conf,'r').read()
	data_m = data.replace("SELINUX=enforcing","SELINUX=disabled")
	ref_data = open(path_to_selinux_conf,'w')
	ref_data.write(data_m)
	ref_data.close()

#STEP-6:
def start_ssh_service():
	
	os.system("service sshd start")
	os.system("chkconfig sshd on")

#STEP-7:
def change_ntp_conf():
	path_to_ntp_conf = "/etc/ntp.conf"
	ntp_conf = open(path_to_ntp_conf,'r').read()
	ntp_modified_conf = open(path_to_ntp_conf,'w')
	replace_tags = {"server 0.centos.pool.ntp.org iburst":"server 0.pool.ntp.org",
					"server 1.centos.pool.ntp.org iburst":"server 1.pool.ntp.org",
					"server 2.centos.pool.ntp.org iburst":"server 2.pool.ntp.org",
					"server 3.centos.pool.ntp.org iburst":"server 3.pool.ntp.org"}

	for i in replace_tags:
		ntp_conf = ntp_conf.replace(i,replace_tags[i])
	ntp_modified_conf.write(ntp_conf)

#STEP-8:
def start_nsc_service():
	os.system("service nscd start")
	os.system("chkconfig nscd on")

#STEP-9:
def start_ntp_server():
	os.system("service ntpd start")
	os.system("chkconfig ntpd on")	

#STEP-10:
def stop_iptables():
	os.system("iptables -F")
	os.system("chkconfig iptables off")
	os.system("service network resart")

#STEP-11:
def swappiness():
	path_to_sysctl_conf = "/etc/sysctl.conf"
	sysctl_conf = open(path_to_sysctl_conf,'a')
	sysctl_conf.write("\nvm.swappiness=10\n")
	sysctl_conf.close()

set_static_IP()
configure_network()
configure_hosts()
check_internet_connection()
disable_se_linux()
start_ssh_service()
change_ntp_conf()
start_nsc_service()
start_ntp_server()
stop_iptables()
swappiness()
