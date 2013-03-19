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
'''
Write a script that creates a Cloud Database instance. This instance should contain at least one database, 
and the database should have at least one user that can connect to it. Worth 1 Point
'''

import os
import sys
import pyrax


cdb = pyrax.cloud_databases

inst = cdb.create("first_instance", flavor="m1.tiny", volume=2)
print inst

db = inst.create_database("db_name")
print "DB:", db

user = inst.create_user(name="groucho", password="top secret", database_names=[db])
print "User:", user


