# Clusterchaos

This is a utility to test the resiliency of the components of a highly
available environment. It works by killing nodes in a defined environment, and
then executing a testing command or script. The testing command must be
provided by the user, so it should be able to accomodate to different types
of environments.

To kill systems, it makes use of the **fence agents**, provided by
<https://git.fedorahosted.org/git/fence-agents.git>.

## Installation of clusterchaos

   $ sudo yum -y install git fence-agents
   $ git clone git://github.com/javierpena/clusterchaos
   $ cd clusterchaos && sudo python setup.py install

## Executing

The basic command line is:

   $ clusterchaos --config-file=/tmp/config.yml

The configuration file will use a YAML format, with the following fields:

   # Generic config values
   config:
           # test_command supports the following substitutions
           # - $name
           test_command: "ping -c 1 $name"
           # test_type must be one of single-node, all-down-simultaneous, all-down"
           test_type: "single-node"
           post_poweroff_delay: 1 
           post_poweron_delay:  1
   # Environment description
   nodes:
           - name: machine1
             fence:
                   driver: virsh
                   IP : 127.0.0.1
                   user: root
                   password: password
                   additional_options: "-n machine1"
           - name: machine2
             fence:
                   driver: virsh
                   IP : 127.0.0.1
                   user: root
                   password: password
                   additional_options: "-n machine2"
           - name: machine3
             fence:
                   driver: virsh
                   IP : 127.0.0.1
                   user: root
                   password: password
                   additional_options: "-n machine3"

## Debugging

You can use the `--verbose` and `--debug` options to make **Clusterchaos**
provide detailed information.

## Logging

By default, logging will be directed to the standard error. Use
`--log-file=log.txt` to specify a log file.

## TO-DO

Lots of stuff. Mainly better error handling, better output, complete the
testing scenarios... This is still an experiment.
