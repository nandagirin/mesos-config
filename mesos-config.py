#!/usr/bin/python3

from subprocess import call
import json, sys, os, argparse, subprocess, math

print ("**************************************************")
print ("**          Tested on Ubuntu 16.04 LTS          **")
print ("**             Mesos version 1.6.0              **")
print ("**************************************************")

# Set up option configuration with Parser
parser = argparse.ArgumentParser()
parser.add_argument('--config', '-c',
    dest = 'config', help = 'Config written in JSON', required = True, default = 'conf.json')
parser.add_argument('--username', '-u',
    dest = 'user', help = 'Username used in the server host', required = False, default = 'root')
args = parser.parse_args()

# Set config file and bash file
cfgfile = open(str(os.getcwd()) + "/" + str(args.config))
user = str(args.user)
conf = json.load(cfgfile)

# Parse JSON
print("Config file:\n" + json.dumps(conf, indent=2))
mastercount = len(conf['MASTERS'])
slavecount = len(conf['SLAVES'])
quorum = int(math.ceil(mastercount / 2))

# Declare variables needed (zookeeper related)
zkaddr = conf['MASTERS'][0]['ipaddr'] + ':2181'
if mastercount > 1:
    for i in range(mastercount - 1):
        zkaddr = zkaddr + ',' + conf['MASTERS'][i + 1]['ipaddr'] + ':2181'
zkaddress = 'zk://' + zkaddr + '/mesos'
zkmarathon = 'zk://' + zkaddr + '/marathon'

# Make zoo.cfg file to be sent to each host
f = open("/tmp/zoo.cfg", "w+")
f.write("tickTime=2000\n")
f.write("initLimit=10\n")
f.write("syncLimit=5\n")
f.write("dataDir=/var/lib/zookeeper\n")
f.write("clientPort=2181\n")
for i in range(mastercount):
    f.write("server." + str(i+1) + "=" + conf['MASTERS'][i]['ipaddr'] + ":2888:3888\n")
f.close()

# Search for entries containing similar IP between master and slave
list_ip = []
for i in range(mastercount):
    list_ip.append(conf['MASTERS'][i]['ipaddr'])
for i in range(slavecount):
    list_ip.append(conf['SLAVES'][i]['ipaddr'])
ip_dupes = [x for n, x in enumerate(list_ip) if x in list_ip[:n]]

# Install and configure master servers
master_cmd = 'bash /tmp/install-master.sh'
for i in range(mastercount):

    hostname = conf['MASTERS'][i]['name']
    ip = conf['MASTERS'][i]['ipaddr']
    identity = conf['MASTERS'][i]['id']
    print("Accessing " + hostname + " over ssh...")

    # Check if the server must be configured as master only or master and slave
    check = 0
    if ip in ip_dupes:
        check = 1

    print("Start Mesos-Master service on " + hostname + "...")
    subprocess.call(['scp', 'install-master.sh', '/tmp/zoo.cfg', user + '@' + ip + ':/tmp;'])
    subprocess.call(['ssh', user + '@' + ip, master_cmd, 
        hostname, zkaddress, identity, str(quorum), ip, zkmarathon, str(check)])
    
# Install and configure agent servers
slave_cmd = 'bash /tmp/install-slave.sh'
for i in range(slavecount):
    hostname = conf['SLAVES'][i]['name']
    ip = conf['SLAVES'][i]['ipaddr']
    attributes = conf['SLAVES'][i]['attr']
    print("Accessing " + hostname + " over ssh...")

    # Check if the server must be configured as master only or master and slave
    check = 0
    if ip in ip_dupes:
        check = 1

    print("Start Mesos-Slave service on " + hostname + "...")
    subprocess.call(['scp', 'install-slave.sh', user + '@' + ip + ':/tmp'])
    subprocess.call(['ssh', user + '@' + ip, slave_cmd, 
        str(check), zkaddress, ip, hostname, attributes])

subprocess.call(['sudo', 'rm', '-rf', '/tmp/zoo.cfg'])