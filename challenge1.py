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

Cent = [img for img in cs.images.list()
                if "CentOS 6.3" in img.name][0]
flavor_512 = [flavor for flavor in cs.flavors.list()
                if flavor.ram == 512][0]

for i in range(1, 2):
    server_name='web' + str(i)
    server = cs.servers.create(server_name, Cent.id, flavor_512.id)
    print "Name:", server.name
    print "ID:", server.id
    print "Status:", server.status
    print "Admin Password:", server.adminPass
    print "Waiting for Network config.."
    while not cs.servers.get(server.id).networks:
      time.sleep(1)
    print "Networks:", cs.servers.get(server.id).networks['public']

