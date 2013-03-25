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
parser.add_argument('-c','--create', help="shall I create this if it doesn't exist [-c ya]", required=False)

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
  sys.exit(0)

if len(fqdn.split('.')) > 3:
  print "this program only supports second level domains"
  sys.exit(0)

a_rec = {"type": "A",
        "name": fqdn,
        "data": address,
        "ttl": 6000}



domains = [ domain.name for domain in dns.list() ]
records = []

base_domain = ".".join(fqdn.split('.')[-2:])

print base_domain

if base_domain in domains and base_domain == fqdn:
   recs = dns.add_record(dns.find(name=base_domain).id, a_rec)
   print "added records"
   sys.exit(0)

elif base_domain == fqdn and base_domain not in domains:
   if args[create] == "ya":
     domain = dns.create(name=fqdn)
     recs = domain.add_records(a_rec)
     print "created:"
     print domain
     print recs 
     sys.exit(0)
   else:
     print "domain doesn't exist on account, create?\n add -c ya to the command line"
     sys.exit(0)
else:
  for d in domains:
    for r in dns.list_records(dns.find(name=d).id):
     records.append(r.name)
if fqdn not in records:
   print "creating subdomain and add record"
   domain = dns.create(name=fqdn, a_rec)
   #recs = domain.add_records(a_rec)
else:
   print "adding records"
     
   

print records


