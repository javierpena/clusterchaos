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

import yaml
import sys
import logging


# Read config file, return hash with configuration
def read_config(filename):
    try:
        config = open(filename).read()
        confighash = yaml.load(config)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)
    # TODO perform basic configuration validation here
    return confighash
