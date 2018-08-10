*********************************************************************
*                                                                   *
*               READ FIRST BEFORE INSTALLING MESOS                  *
*                                                                   *
*********************************************************************

1. This script is tested in Ubuntu 16.04 environment with Apache Mesos version 1.6.0.
2. Follow the steps below to execute the script:
    1. Make sure your local machine and all hosts that will be installed with Mesos are connected to the internet.
    2. Make sure you can do SSH to each host you want to configure. Use same username for each host.
    3. Open 'conf.json' file. Modify it as you need. Make sure the data format is same.
    4. This script was tested with python3. Execute below command within the script directory: 
            python3 mesos-config.py -c conf.json -u <username for ssh to your hosts (default is root)>
    5. You can use other json file as long as the format is same as the one provided here.
    6. Wait until the installation finish.
3. Hope it is useful :) 