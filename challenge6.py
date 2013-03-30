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
Challenge 6: Write a script that creates a CDN-enabled container in Cloud Files
'''

import os
import sys
import pyrax

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(cred_file)

contName = 'yac'
cf = pyrax.cloudfiles

try:
  cont = cf.create_container(contName)
  cont.make_public
except:
  print "Something went horribly wrong"

print "Container name:%s" % cont.name
print "Container uri:%s" % cont.cdn_uri
print "Container ssl uri:%s" % cont.cdn_ssl_uri
print "Container streaming uri:%s" % cont.cdn_streaming_uri
