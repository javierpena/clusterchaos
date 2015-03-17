# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import logging
import random
import subprocess
import time

from string import Template
from clusterchaos.tester import utils


def execute(cmd, workdir=None, can_fail=True, use_shell=False, log=True):
    """
    Runs shell command cmd. If can_fail is set to False
    ExecuteRuntimeError is raised if command returned non-zero return
    code. Otherwise
    """
    environ = os.environ
    environ['LANG'] = 'en_US.UTF8'

    logging.debug("Running %s" % cmd)

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=workdir,
                            shell=use_shell, close_fds=True,
                            env=environ)
    out, err = proc.communicate()

    if proc.returncode:
        if log:
            logging.error(err)
        if can_fail:
            msg = ('Failed to execute command, '
                   'stdout: %s\nstderr: %s' %
                   (out, err))
            logging.warning(msg)
    return proc.returncode, out


def fence_node(node, operation):
    fence_driver = node['fence']['driver']
    fence_ip = node['fence']['IP']
    fence_user = node['fence']['user']
    fence_pass = node['fence']['password']
    fence_options = node['fence']['additional_options']

    cmdline = "/usr/sbin/fence_%s -a %s -l %s -p %s -o %s %s" % (fence_driver,
                                                                 fence_ip,
                                                                 fence_user,
                                                                 fence_pass,
                                                                 operation,
                                                                 fence_options)
    retcode, out = execute(cmdline, use_shell=True)


def run_failover_test(config, node):
    cmdline_template = Template(config['config']['test_command'])
    cmdline = cmdline_template.substitute(name=node['name'])

    retcode, out = execute(cmdline, use_shell=True)
    if retcode != 0:
        result = utils.color_text('[FAILED]', 'red')
    else:
        result = utils.color_text('[OK]', 'green')
    print ("Test for node " + node['name'] + " " + result)


def wait(wait_period):
    time.sleep(wait_period)


def shuffle_node_list(nodearray):
    random.shuffle(nodearray)
    return nodearray


def run_tests(config):
    # Shuffle array, so we will kill nodes in random order
    nodelist = shuffle_node_list(config['nodes'])
    test_type = config['config']['test_type']

    if test_type == 'single-node':
        for node in nodelist:
            logging.info("Now killing node " + node['name'])
            fence_node(node, 'off')
            logging.info("Waiting for post_poweroff_delay seconds")
            wait(config['config']['post_poweroff_delay'])
            logging.info("Now testing after killing node" + node['name'])
            run_failover_test(config, node)
            logging.info("Now starting node " + node['name'])
            fence_node(node, 'on')
            wait(config['config']['post_poweron_delay'])
            logging.info("Waiting for post_poweron_delay seconds")
    elif test_type == 'all-down-simultaneous':
        logging.warning("Warning, test type all-down-simultaneous"
                        "not implemented yet")
    elif test_type == 'all-down':
        logging.warning("Warning, test type all-down not implemented yet")
