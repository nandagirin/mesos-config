from subprocess import *
import json, sys, os, argparse, subprocess

print ("**************************************************")
print ("**          Tested on Ubuntu 16.04 LTS          **")
print ("**             Mesos version 1.6.0              **")
print ("**************************************************")

parser = argparse.ArgumentParser()
parser.add_argument('--config', '-c',
    dest = 'config', help = 'Config written in JSON', required = True)
args = parser.parse_args()

cfgfile = open(str(os.getcwd()) + "/" + str(args.config))
conf = json.load(cfgfile)

print("Config file:\n" + json.dumps(conf, indent=2))
mastercount = len(conf['MASTERS'])
slavecount = len(conf['SLAVES'])
quorum = (2 * mastercount) - 1

