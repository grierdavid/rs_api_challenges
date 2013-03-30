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
'''
Write a script that creates a Cloud Database instance. This instance should contain at least one database, 
and the database should have at least one user that can connect to it. Worth 1 Point
'''

import os
import sys
import pyrax
import time



cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(cred_file)

inst_name = "challenge2"
flavor = int(512)
db_name = "mydb"
user_name = "dgrier"
db_pass = "notagoodpass"

cdb = pyrax.cloud_databases

for flv in cdb.list_flavors():
     if flv.ram == flavor:
       flavor = flv.name 

inst = cdb.create(inst_name, flavor=flavor, volume=2)
print inst

while not "ACTIVE" in cdb.find(name=inst_name).status:
  time.sleep(1)
  
db = inst.create_database(db_name)
print "DB:", db.name

user = inst.create_user(name=user_name, password=db_pass, database_names=[db])
print "User:", user


