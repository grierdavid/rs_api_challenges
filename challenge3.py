#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013 David Grier

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

cf = pyrax.cloudfiles

folder = args['folder']
container = args['container']

if not os.path.isdir(folder):
  print "Invalid Directory or Path\n"
  sys.exit(0)


def container_exist(name):
     if name in cf.list_containers():
       return True 
     else:
       return False

if container_exist(container):
  print "Container pics exists"  
else:
    print "Creating container: %s" % container
    cf.create_container(container)

print "Uploading files from: %s to: %s\n" % (folder, container)  
cf.sync_folder_to_container(folder, container)
print "Upload complete"

for obj in cf.get_container_objects(container):
  print obj



