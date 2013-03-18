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
import argparse
from IPy import IP

parser = argparse.ArgumentParser()

#parser.add_argument('-a','--address', help='IP Address', required=True)
#parser.add_argument('-d','--domain', help='FQDN', required=True)

args = vars(parser.parse_args())

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')

pyrax.set_credential_file(cred_file)

dns = pyrax.cloud_dns
address = '198.61.200.31'
#address = '555.555.555.555'
domain = 'another.mymuseisnan.com'

def domain_exist(domain):
  for d in dns.get_domain_iterator():
    for r in dns.get_record_iterator(d):
      if  r.name == domain:
        return True
      else:
        return False

try:
  IP(address)
except:
  print "Yo, Dog how about a Valid IP"
