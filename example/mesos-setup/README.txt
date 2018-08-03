alfin@nodeflux.io
Last Updated: 30 December 2016

Two method for installing and configuring mesos masters and slaves
  1)  Manual Installation: manually typing the IP addresses
      (this mode is only working for a single master)
  2)  Automatic Installation
      (this mode requires config (.json) file as its reference)

1)  Manual Installation
    a)  To run installation and configuration for master, execute this command
        on your terminal. (e.g. mesos-master1 to mesos-master3)
        $ python install-shell.py --domain=smdonkey.com --hostname=mesos-master --start=1 --finish=3

    b)  To run installation and configuration for slave, execute this command
        on your terminal. (e.g. mesos-slave1 to mesos-slave3)
        $ python install-shell.py --domain=smdonkey.com --hostname=mesos-slave --start=1 --finish=3

2)  Automatic Installation
    To run installation and configuration for both masters and slaves, execute
    this command on yout terminal. The configuration will be set based on the
    configuration file (*.json)
    $ python install.py --domain=smdonkey.com --config=conf.json

conf.json guide:
  Name and ip address fields are required for each machines
  Master's id will decide the order of master in the zookeeper configuration

LIST OF NODEFLUX SERVERS
M4 10.116.139.17
S14 10.116.139.7
S15 10.116.139.53
S16 10.116.139.9
