#!/usr/bin/env python

# Deployment script for all nodeflux microservices hosted as marathon app
# 
from subprocess import call
import sys, os, argparse
import subprocess, requests, json

parser = argparse.ArgumentParser(prog="deployment script")
parser.add_argument('--prefix', '-p', 
	dest= 'prefix' , help='Build number or any other prefix', required=True)
parser.add_argument('--marathon-host', '-m', 
	dest= 'marathon' , help='Host of marathon app', required=True)
parser.add_argument('--deploy-file', '-d', 
	dest= 'deploy_file' , help='deployment file', required=True)

if __name__ == '__main__':
	args = parser.parse_args()
	data = None
	# Reformat deploy.json using the current build number
	print "INFO > Configuring deployment configuration ..."
	try:
		with open(args.deploy_file, 'rb') as f:
			data = f.read()
			data = data.format(
				build_number=args.prefix
			)
			f.close()
	except:
		print("ERROR > Error when parsing deploy.json file")
		sys.exit()

	print "INFO > ", "marathon config : ", data

	data = json.loads(data)
	# Deploying app to marathon
	print "Deploying apps to marathon ..."
	if data:
		path = "/v2/apps"
		headers = {'Content-type': 'application/json'}
		try:
			res = requests.put(args.marathon + path + "/" + \
				data['id'], data = json.dumps(data), headers=headers)
			
			print "INFO > Respon from marathon : ", res.json()
		except:
			print "ERROR > Error when performing request "
	else:
		print("File empty. Closing script")
		sys.exit()
		