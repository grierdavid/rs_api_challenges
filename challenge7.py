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
Challenge 7: Write a script that will create 2 Cloud Servers and add them as nodes to a new Cloud Load Balancer.
'''

import os
import sys
import pyrax
import time
import pdb

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')
pyrax.set_credential_file(cred_file)

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

lb_name = 'challb'

Cent = [img for img in cs.images.list()
                if "CentOS 6.3" in img.name][0]
flavor_512 = [flavor for flavor in cs.flavors.list()
                if flavor.ram == 512][0]

pvt_nets = []

for i in range(3, 6):
    server_name='web' + str(i)
    server = cs.servers.create(server_name, Cent.id, flavor_512.id)
    print "Name:", server.name
    print "ID:", server.id
    print "Status:", server.status
    print "Admin Password:", server.adminPass
    print "Waiting for Network config.."
    while not cs.servers.get(server.id).networks:
      time.sleep(1)
    pvt_net = cs.servers.get(cs.servers.find(name=server_name).id).networks['private'][0]
    pub_net = cs.servers.get(cs.servers.find(name=server_name).id).networks['public'][0]
#    pvt_net = server.networks['private'][0]
#    pvt_nets.append(str(pvt_net))
    pvt_nets.append(pvt_net) 
    print "Public Networks: %s" % pub_net 
    print "Private Networks: %s" % pvt_net

print pvt_nets
node = clb.Node(address=pvt_nets[0], port=80, condition="ENABLED")
nnode = clb.Node(address=pvt_nets[1], port=80, condition="ENABLED")

vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(lb_name, port=80, protocol="HTTP", nodes=[node], virtual_ips=[vip])
while not "ACTIVE" in lb.status:
  time.sleep(1)

lb.add_nodes(nnode)

