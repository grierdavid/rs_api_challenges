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
Challenge 10: Write an application that will:
- Create 2 servers, supplying a ssh key to be installed at /root/.ssh/authorized_keys.
- Create a load balancer
- Add the 2 new servers to the LB
- Set up LB monitor and custom error page. 
- Create a DNS record based on a FQDN for the LB VIP. 
- Write the error page html to a file in cloud files for backup.
Whew! That one is worth 8 points!

'''

import os
import sys
import pyrax
import time

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')
pyrax.set_credential_file(cred_file)

cs = pyrax.cloudservers
clb = pyrax.cloud_loadbalancers

lb_name = 'challb'
imgname = 'CentOS 6.3'
size = 512

myimage = [img for img in cs.images.list()
                if imgname in img.name][0]
myflavor = [flavor for flavor in cs.flavors.list()
                if flavor.ram == size][0]

pvt_nets = []

keyfile = os.path.expanduser('~/pubkey')

files = {'/root/.ssh/authorized_keys': keyfile}

for i in range(1, 3):
    server_name='web' + str(i)
    server = cs.servers.create(server_name, myimage.id, myimage.id, files=files)
    print "Name:", server.name
    print "ID:", server.id
    print "Admin Password:", server.adminPass
    print "Waiting for Network config.."
    while not cs.servers.get(server.id).networks:
      time.sleep(1)
    pvt_net = str(cs.servers.get(server.id).networks['private'][0])
    pub_net = str(cs.servers.get(server.id).networks['private'][0])
    pvt_nets.append(pvt_net) 
    print "Public Networks: %s" % pub_net 
    print "Private Networks: %s" % pvt_net

print pvt_nets
node = clb.Node(address=pvt_nets[0], port=80, condition="ENABLED")
nnode = clb.Node(address=pvt_nets[1], port=80, condition="ENABLED")

vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(lb_name, port=80, protocol="HTTP", nodes=[node], virtual_ips=[vip])

while not "ACTIVE" in clb.get(lb).status: 
  time.sleep(1)

lb.add_nodes(nnode)

