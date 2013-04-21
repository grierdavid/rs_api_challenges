#!/usr/bin/env python

import os
import sys
import pyrax
import time

'''
Write an application that nukes everything in your Cloud Account. It should:
Delete all Cloud Servers
Delete all Custom Images
Delete all Cloud Files Containers and Objects
Delete all Databases
Delete all Networks
Delete all CBS Volumes
Worth 3 points
'''

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')
pyrax.set_credential_file(cred_file)

clb = pyrax.cloud_loadbalancers
cs = pyrax.cloudservers
cbs = pyrax.cloud_blockstorage
dns = pyrax.cloud_dns
cnw = pyrax.cloud_networks

print "Delete cloud servers"
for server in cs.servers.list():
    cs.servers.delete(server.id)

print "Delete Load Balancers"
for lb in clb.list():
    clb.delete(lb)

print "Delete Block Storage"
for bs in cbs.list():
    if bs.status == "attached":
        cbs.detach(bs)
        wait_until(bs, "status", "available")
        cbs.delete(bs)
    else:
        cbs.delete(bs)

print "Delete cbs snapshots"
for cbs_sh in cbs.list_snapshots():
    cbs.delete_snapshot(cbs_sh)

print "Delete Cloud Network"
for nw in cnw.list():
    cnw.delete(nw)


