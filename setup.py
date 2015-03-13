#!/usr/bin/env python
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

from setuptools import setup
from setuptools import find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="clusterchaos",
    version="0.0",
    author="Javier Peña",
    author_email="jpena@redhat.com",
    description=("A utility to create chaos in a cluster to test HA functionality"),
    license="ASL 2.0",
    keywords="cluster",
    url="https://github.com/javierpena/clusterchaos",
    packages=find_packages('.'),
    include_package_data=True,
    long_description=read('README.md'),
    zip_safe=False,
    install_requires=['PyYAML'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
    scripts=["bin/clusterchaos"],
)
