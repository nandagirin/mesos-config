#!/usr/bin/python3

from subprocess import call
import json, sys, os, argparse, subprocess, math

print ("**************************************************")
print ("**          Tested on Ubuntu 16.04 LTS          **")
print ("**             Mesos version 1.6.1              **")
print ("**************************************************")

# Set up option configuration with Parser
parser = argparse.ArgumentParser()
parser.add_argument('--config', '-c',
    dest = 'config', help = 'Config written in JSON', required = True)
parser.add_argument('--username', '-u',
    dest = 'user', help = 'Username used in the server host', required = False, default = 'root')
args = parser.parse_args()

# Set config file and bash file
cfgfile = open(str(os.getcwd()) + "/" + str(args.config))
user = str(args.user)
install_master = str(os.getcwd()) + "/install-master.sh"
install_slave = str(os.getcwd()) + "/install-slave.sh"
conf = json.load(cfgfile)

# Parse JSON
print("Config file:\n" + json.dumps(conf, indent=2))
mastercount = len(conf['MASTERS'])
slavecount = len(conf['SLAVES'])
quorum = int(math.ceil(mastercount / 2))

# Declare variables needed (zookeeper related)
zkaddr = conf['MASTERS'][0]['ipaddr'] + ':2181'
zoocfg = 'server.1=' + conf['MASTERS'][0]['ipaddr'] + ':2888:3888'
if mastercount > 1:
    for i in range(mastercount - 1):
        zkaddr = zkaddr + ',' + conf['MASTERS'][i + 1]['ipaddr'] + ':2181'
        zoocfg = zoocfg + '\n' + 'server.' + str(i+2) + '=' + conf['MASTERS'][i+1]['ipaddr'] + ':2888:3888'
zkaddress = zkaddr + '/mesos'
zkmarathon = zkaddr + '/marathon'

# Search for entries containing similar IP between master and slave
list_ip = []
for i in range(mastercount):
    list_ip.append(conf['MASTERS'][i]['ipaddr'])
for i in range(slavecount):
    list_ip.append(conf['SLAVES'][i]['ipaddr'])
ip_dupes = [x for n, x in enumerate(list_ip) if x in list_ip[:n]]

# Install and configure master servers
for i in range(mastercount):
    hostname = conf['MASTERS'][i]['name']
    ip = conf['MASTERS'][i]['ipaddr']
    id = conf['MASTERS'][i]['id']
    print("Accessing " + hostname + " over ssh...")

    # Check if the server must be configured as master only or master and slave
    check = 0
    if ip in ip_dupes:
        check = 1

    print("Start Mesos-Master service on " + hostname + "...")
    subprocess.call(['scp', 'install-master.sh', user + '@' + ip + ':/tmp'])
    #subprocess.call(['ssh', '-f', user + '@' + ip, 
    #    'echo "IP=' + ip + '" | tee /tmp/var;' +
    #    'echo "HOSTNAME=' + hostname + '" | tee -a /tmp/var;' +
    #    'echo "QUORUM=' + str(quorum + '" | tee -a /tmp/var;' +
    #    'echo "ID=' + id + '" | tee -a /tmp/var;' +
    #    'echo "ZKADDRESS=' + zkaddress + '" | tee -a /tmp/var;' +
    #    'echo "ZKMARATHON=' + zkmarathon + '" | tee -a /tmp/var;' +
    #    'echo "ZOOCFG=' + zoocfg + '" | tee -a /tmp/var;' +
    #    'echo "CHECK=' + str(check) + '" | tee -a /tmp/var;' + 
    #    'source /tmp/var; bash /tmp/install-master.sh'])
    
    subprocess.call(['ssh', '-f', user + '@' + ip, '"HOSTNAME=' + hostname + ';' +
        'IP=' + ip + ';' + 'QUORUM=' + str(quorum) + ';' + 'ID=' + id + ';' + 'ZKADDRESS=' + zkaddress + ';',
        'ZKMARATHON=' + zkmarathon + ';' + 'ZOOCFG=' + zoocfg + ';' +  'CHECK=' + str(check) + ';' +
        'bash /tmp/install-master.sh"'])
    
# Install and configure agent servers
for i in range(slavecount):
    hostname = conf['SLAVES'][i]['name']
    ip = conf['SLAVES'][i]['ipaddr']
    attributes = conf['SLAVES'][i]['attr']
    print("Accessing " + hostname + " over ssh...")

    # Check if the server must be configured as master only or master and slave
    check = 0
    if ip in ip_dupes:
        check = 1

    print("Start Mesos-Master service on " + hostname + "...")
    subprocess.call(['scp', 'install-slave.sh', user + '@' + ip + ':/tmp'])
    subprocess.call(['ssh', '-f', user + '@' + ip, '"HOSTNAME=' + hostname, ';' +
        'IP=' + ip + ';' + 'ZKADDRESS=' + zkaddress + ';' + 'CHECK=' + str(check) + ';' +
        'bash /tmp/install-slave.sh"'])