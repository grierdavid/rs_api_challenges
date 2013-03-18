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
import time

import pyrax
import pyrax.exceptions as exc
import pyrax.utils as utils

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')
pyrax.set_credential_file(cred_file)

cf = pyrax.cloudfiles


def container_exist(name):
  for c in cf.get_all_containers():
    if name == c.name:    
      return True 
    else:
      return False

if container_exist('pics'):
   print "Container pics exists"  

