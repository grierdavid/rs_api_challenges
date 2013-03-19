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
import sys
import pyrax
import pyrax.exceptions as exc
import argparse
from IPy import IP

parser = argparse.ArgumentParser()

parser.add_argument('-a','--address', help='IP Address', required=True)
parser.add_argument('-d','--domain', help='FQDN', required=True)

args = vars(parser.parse_args())

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(cred_file)

dns = pyrax.cloud_dns
address = args['address']
domain = args['domain']

try:
  IP(address)
except:
  print "Yo, Dog how about a Valid IP"

if len(domain.split('.',)) > 3:
  print "this program only supports third level domains"
  sys.exit(0)

dom = domain.partition('.')[2]
print dom

try:
  dns.find(name=dom)
except:
  print "domain not found %s" % dom  

''
for r in dns.get_record_iterator(name=dom):
      if r.name != domain:
        addrec = 'Yes' 
      else:
        addrec = 'No'
        break
''
a_rec = {"type": "A",
        "name": domain_name,
        "data": "1.2.3.4",
        "ttl": 6000}
