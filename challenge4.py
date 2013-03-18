#!/usr/bin/env python
# -*- coding: utf-8 -*-

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys

import pyrax
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f','--folder', help='Folder to be uploaded', required=True)
parser.add_argument('-c','--container', help='Container to be recieve upload', required=True)

args = vars(parser.parse_args())

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(cred_file)
