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
import sys
import logging
import traceback

from optparse import OptionParser

from clusterchaos.tester import config
from clusterchaos.tester import runner


def initCmdLineParser():
    """
    Initiate the optparse object, add all the groups and general command line
    flags and returns the optparse object
    """

    # Init parser and all general flags
    usage = "usage: %prog --config-file=CONFIGFILE [options] [--help]"
    parser = OptionParser(usage=usage, version="%prog 0.1")
    parser.add_option("--config-file", dest="configfile",
                      help="Use the specified configuration file (required)")
    parser.add_option("--log-file", dest="logfile",
                      help="Use the specified log file. If ommited, output is"
                           " logged to standard error")
    parser.add_option("--debug", action="store_true", default=False,
                      help="Enable debug logging")
    parser.add_option("--verbose", action="store_true", default=False,
                      help="Enable verbose logging")
    return parser


def initLogging(debug, verbose, logfile):
    if(logfile):
        try:
            # Create the log file with specific permissions,
            # puppet has a habbit of putting passwords in logs
            os.close(os.open(logfile, os.O_CREAT | os.O_TRUNC, 0o600))
            hdlr = logging.FileHandler(filename=logfile, mode='w')

            fmts = ('%(asctime)s::%(levelname)s::%(module)s::%(lineno)d'
                    '::%(name)s:: %(message)s')
            dfmt = '%Y-%m-%d %H:%M:%S'
            fmt = logging.Formatter(fmts, dfmt)
            hdlr.setFormatter(fmt)

            logging.root.handlers = []
            logging.root.addHandler(hdlr)
        except:
            logging.error(traceback.format_exc())
            raise Exception("Failed to initialize log file: " + logfile)

    if (debug):
        level = logging.DEBUG
    elif(verbose):
        level = logging.INFO
    else:
        level = logging.ERROR
    logging.root.setLevel(level)


def main():
    try:
        optParser = initCmdLineParser()
        (options, args) = optParser.parse_args()

        initLogging(options.debug, options.verbose, options.logfile)
        logging.debug(options)
        logging.debug(args)

        if options.configfile:
            confighash = config.read_config(options.configfile)
            logging.debug(str(confighash))
        else:
            optParser.error("Config file required")
        runner.run_tests(confighash)

    except Exception as e:
        print("Error " + str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
