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
Challenge 8: Write a script that will create a static webpage served out of Cloud Files. The script must create a new container, cdn enable it, enable it to serve an index file, create an index file object, upload the object to the container, and create a CNAME record pointing to the CDN URL of the container. Worth 3 Points

'''

import os
import sys
import pyrax

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')
pyrax.set_credential_file(cred_file)

cf = pyrax.cloudfiles
dns = pyrax.cloud_dns

cname = 'static.mymuseisnan.com'
base_domain = 'mymuseisnan.com'
index_file = 'index.html'
upload_dir = os.path.expanduser('~/upload/')
cont_name = 'staticsite'

container = cf.create_container(cont_name)
container.make_public()
cf.set_container_web_index_page(cont_name, index_file)
cf.upload_file(cont_name, upload_dir + index_file)
uri = container.cdn_uri.split('//')

cname_rec = {"type": "CNAME",
        "name": cname,
        "data": uri[1],
        "ttl": 6000}

recs = dns.add_record(dns.find(name=base_domain), cname_rec)
