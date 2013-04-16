#!/usr/bin/env python

import os
import sys
import pyrax
import time

'''
Create an SSL terminated load balancer (Create self-signed certificate.)
Create a DNS record that should be pointed to the load balancer.
Create Three servers as nodes behind the LB.
     Each server should have a CBS volume attached to it. (Size and type are irrelevant.)
     All three servers should have a private Cloud Network shared between them.
     Login information to all three servers returned in a readable format as the result of the script, including connection information.
Worth 6 points
'''

cred_file = os.path.expanduser('~/.rackspace_cloud_credentials')
pyrax.set_credential_file(cred_file)

clb = pyrax.cloud_loadbalancers
cs = pyrax.cloudservers
cbs = pyrax.cloud_blockstorage
dns = pyrax.cloud_dns
cnw = pyrax.cloud_networks



#Needs to be fqdn and based on a domain associated with this account
lb_name = 'challb.mymuseisnan.com'
pvt_nets = []
cbs_ids = []
srv_ids = []
imgname = 'CentOS 6.3'
size = 512
new_network_name = "Chall_Net"
new_network_cidr = "192.168.0.0/24"

if len(lb_name.split('.')) < 3:
  print "needs to be a FQDN"
  sys.exit(0)
else:
  base_domain = ".".join(lb_name.split('.')[-2:])

domains = [ domain.name for domain in dns.list() ]

if base_domain not in domains:
  print "Base domain needs to be associated with your account"
  print domains
  sys.exit(0)

new_net = cnw.create(new_network_name, cidr=new_network_cidr)
print "New network:", new_net
networks = new_net.get_server_networks(public=True, private=True)

for i in range(1, 4):
    cbsname = 'mycbs' + str(i)
    sata_vol = cbs.create(name=cbsname, size=500, volume_type="SATA")
    pyrax.utils.wait_until(sata_vol,"status","available", interval=1)
    cbs_ids.append(sata_vol.id)
    print "vol %s: %s" % (cbsname, sata_vol)

myimage = [img for img in cs.images.list()
                if imgname in img.name][0]
myflavor = [flavor for flavor in cs.flavors.list()
                if flavor.ram == size][0]

for i in range(1, 4):
    server_name='web' + str(i)
    server = cs.servers.create(server_name, myimage.id, myflavor.id, nics=networks)
    print "Name:", server.name
    print "ID:", server.id
    srv_ids.append(server.id)
    adminpass = server.adminPass
    print "Admin Password:", adminpass
    print "Waiting for Network config.."
    while not cs.servers.get(server.id).networks:
      time.sleep(1)
    pvt_net = str(cs.servers.get(server.id).networks['private'][0])
    pub_net = str(cs.servers.get(server.id).networks['public'][0])
    pvt_nets.append(pvt_net)
    print "Public Networks: %s" % pub_net
    print "Private Networks: %s" % pvt_net


print pvt_nets
node = clb.Node(address=pvt_nets[0], port=80, condition="ENABLED")
nnode = clb.Node(address=pvt_nets[1], port=80, condition="ENABLED")
nnnode = clb.Node(address=pvt_nets[2], port=80, condition="ENABLED")

vip = clb.VirtualIP(type="PUBLIC")
lb = clb.create(lb_name, port=80, protocol="HTTP", nodes=[node], virtual_ips=[vip])

while not "ACTIVE" in clb.get(lb).status:
  time.sleep(1)
lb.add_nodes(nnode)
while not "ACTIVE" in clb.get(lb).status:
  time.sleep(1)
lb.add_nodes(nnnode)
while not "ACTIVE" in clb.get(lb).status:
  time.sleep(1)

#get vip from lb
for i in lb.virtual_ips:
    if i.type == 'PUBLIC':
      pub_vip = i.address
    else:
      print "couldn't get IP from vip"
      sys.exit(0)
#- Create a DNS record based on a FQDN for the LB VIP.
a_rec = {"type": "A",
        "name": lb_name,
        "data": pub_vip,
        "ttl": 6000}

recs = dns.add_record(dns.find(name=base_domain), a_rec)
print "Record added"
print recs

for i in srv_ids:
    mysrv = cs.servers.get(i)
    pyrax.utils.wait_until(server, "status", "ACTIVE", attempts=0,
                verbose=True)
    for id in cbs_ids:
      vol = cbs.get(id)
      vol.attach_to_instance(mysrv, mountpoint="/dev/xvdb")
      pyrax.utils.wait_until(vol, "status", "in-use", interval=3, attempts=0,
        verbose=True)
      print "Volume attachments:", vol.attachments
      cbs_ids.pop(0)
