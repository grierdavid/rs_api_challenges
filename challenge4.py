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
fqdn = args['domain']

try:
  IP(address)
except:
  print "Yo, Dog how about a Valid IP"

if len(fqdn.split('.')) > 2:
  print "this program only supports second level domains"
  sys.exit(0)

a_rec = {"type": "A",
        "name": fqdn,
        "data": address,
        "ttl": 6000}

domains = [ domain.name for domain in dns.zones() ]
domain = "."
for d in domains:
  if address.endswith(d) and len(domain) < len(d):
    domain = d

if domain != ".":
  domain = dns.find(name=domain)
else:
  base_domain = ".".join(address.split('.')[:-2])
  domain = dns.create(name=base_domain)

domain.add_record(a_rec)

if len(fqdn.split('.',)) >= 3:
  maindom = fqdn.partition('.')[2]
  sub = fqdn.partition('.')[1]
  
  print maindom
  try:
    domid = dns.find(name=maindom).id
  except:
    print "domain not found %s" % maindom  
  for r in  dns.list_records(domid):
    if r.name == fqdn:
      exists = 'Yes' 
      break
    else:
      exists = 'No'
  if exists == 'Yes':
    print "%s already exists" % fqdn   
  else:
    print "adding subdomain with record"
    subdom = dns.create(name=maindom, subdomains=sub, records=a_rec)
    #recs = subdom.add_record(a_rec)
    print subdom

else:
  print "is second level domain adding record"
  try:
    dom = dns.find(name=fqdn)
    recs = dom.add_record(a_rec)
    print "adding record for %s" % fqdn
    print recs
  except:
    print "domain not found %s" % fqdn  

