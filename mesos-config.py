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
    dest = 'config', help = 'Config written in JSON', required = True)
args = parser.parse_args()

# Set config file and bash file
cfgfile = open(str(os.getcwd()) + "/" + str(args.config))
install_master = str(os.getcwd()) + "/" + 'install_master.sh'
install_slave = str(os.getcwd()) + "/" + 'install_slave.sh'
conf = json.load(cfgfile)

# Parse JSON
print("Config file:\n" + json.dumps(conf, indent=2))
mastercount = len(conf['MASTERS'])
slavecount = len(conf['SLAVES'])
quorum = int(math.ceil(mastercount / 2))

# Declare variables needed
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
for i in mastercount:
    list_ip.append(conf['MASTERS'][i]['ipaddr'])
for i in slavecount:
    list_ip.append(conf['SLAVES'][i]['ipaddr'])
ip_dupes = [x for n, x in enumerate(list_ip) if x in list_ip[:n]]

# Install and configure master server
for i in range(mastercount):
    hostname = conf['MASTERS'][i]['name']
    ip = conf['MASTERS'][i]['ipaddr']
    id = conf['MASTERS'][i]['id']
    print("Accessing " + hostname + " over ssh...")

    # Check if the server must be configured as master only or master and slave
    check = 0
    for i in ip_dupes:
        if ip == ip_dupes[i]:
            check = 1
            break

    print("Start Mesos-Master service on " + hostname + "...")
    subprocess.call(['ssh', 'root@' + hostname, 'HOSTNAME=' + hostname])
    subprocess.call(['ssh', 'root@' + hostname, 'IP=' + ip])
    subprocess.call(['ssh', 'root@' + hostname, 'QUORUM=' + quorum])
    subprocess.call(['ssh', 'root@' + hostname, 'ID=' + id])
    subprocess.call(['ssh', 'root@' + hostname, 'ZKADDRESS=' + zkaddress])
    subprocess.call(['ssh', 'root@' + hostname, 'ZKMARATHON=' + zkmarathon])
    subprocess.call(['ssh', 'root@' + hostname, 'ZOOCFG=' + zoocfg])
    subprocess.call(['ssh', 'root@' + hostname, 'CHECK=' + check])
    subprocess.call(['scp', install_master,'root@' + hostname, '/tmp'])
    subprocess.call(['ssh', 'root@' + hostname, 'bash', '/tmp/' + install_master])