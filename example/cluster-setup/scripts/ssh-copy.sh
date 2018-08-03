#!/bin/bash

for i in {2..8}
do
	echo "Copying ssh id to mesos-slave$i.smdonkey.com"
	ssh-copy-id farisais@mesos-slave$i.smdonkey.com
done
