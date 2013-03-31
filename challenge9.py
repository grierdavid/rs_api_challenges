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
Challenge 9: Write an application that when passed the arguments FQDN, image, and flavor it creates a server of the specified
 image and flavor with the same name as the fqdn, and creates a DNS entry for the fqdn pointing to the server's public IP. 
 Worth 2 Points

'''

import os
import sys
import pyrax
import time
import argparse 

parser = argparse.ArgumentParser()

parser.add_argument('-d','--domain', help='FQDN', required=True)
parser.add_argument('-i','--image', help='Image name to build From', required=True)
parser.add_argument('-f','--flavor', help='Size of server', required=True)

args = vars(parser.parse_args())

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')
pyrax.set_credential_file(cred_file)

dns = pyrax.cloud_dns
cs = pyrax.cloudservers

fqdn = args['domain']
image = args['image']
size = args['flavor']

myimage = [img for img in cs.images.list()
                if image in img.name][0]

myflavor = [flavor for flavor in cs.flavors.list()
                if flavor.ram == int(size)][0]

if len(fqdn.split('.')) < 3:
  print "needs to be a FQDN"
  sys.exit(0)
else:
  base_domain = ".".join(fqdn.split('.')[-2:])

server = cs.servers.create(fqdn, myimage.id, myflavor.id)
myserver = { "name": server.name,
             "ID": server.id,
             "adminpass": server.adminPass }

print "Name:", myserver['name']
print "ID:", myserver['ID']
print "Status:", server.status
print "Admin Password:", myserver['adminpass']
print "Waiting for Network config.."
while not cs.servers.get(server).networks:
  time.sleep(1)

mypubipv4 = [ ip for ip in cs.servers.get(server).networks['public']
                if len( ip.split(".") ) == 4 ]

print "IP:", str(mypubipv4[0])

a_rec = {"type": "A",
        "name": fqdn,
        "data": str(mypubipv4[0]),
        "ttl": 6000}
print a_rec 

domains = [ domain.name for domain in dns.list() ]

if base_domain not in domains:
  print "Base domain needs to be associated with your account" 
  print domains
  sys.exit(0)
else:
  recs = dns.add_record(dns.find(name=base_domain), a_rec)
  print "Record added"
  print recs
