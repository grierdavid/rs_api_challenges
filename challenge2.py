#!/usr/bin/env python

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

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")

pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
imgs = cs.images.list()

servername = 'mysavvy'
nextServer = 'mysavvy1'
imgname = 'mysavvy-img8'
size = 512

def get_flavor(self, size=512):
  flavId = [flavor for flavor in cs.flavors.list()
                  if flavor.ram == 512][0]
  return flavId 

def get_server_id(name):
  sid = [s.id for s in cs.servers.list()
         if name == s.name]
  return sid[0]

sid = get_server_id(servername)

imgId = cs.servers.create_image(sid, imgname)

while "ACTIVE" not in cs.images.get(imgId).status:
  time.sleep(1)

print cs.images.get(imgId).status

flav = get_flavor(size)

server = cs.servers.create(nextServer, imgId, flav.id)

print "Name:", server.name
print "ID:", server.id
print "Status:", server.status
print "Admin Password:", server.adminPass
print "Waiting for Network config.."
while not cs.servers.get(server.id).networks:
  time.sleep(1)
print "Networks:", cs.servers.get(server.id).networks['public']








