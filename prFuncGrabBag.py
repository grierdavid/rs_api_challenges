#!/usr/bin/env python
'''
Some misc functions that might make it into a module


'''

def get_flavor_id(self, size=512):
  flavId = [flavor for flavor in cs.flavors.list()
                  if flavor.ram == size][0]
  return flavId 

'''
better: cs.server.find(name=servername).id
'''
def get_server_id(name):
  sId = [s.id for s in cs.servers.list()
         if name == s.name]
  return sId[0]

def get_img_id(self):
  imgId = [i.id for i in cs.images.list()
         if imgname == i.name] 
  return imgId[0]

def container_exist(name):
     if name in cf.list_containers():
       return True
     else:
       return False

'''
protip: pyrax already does this down to 
try: dns.list_records(dns.get(dns.find(name=domain)))

===

for d in dns.get_domain_iterator():
    for r in dns.get_record_iterator(d):
      if r.name != domain:
        addrec = 'Yes'
      else:
        addrec = 'No'
        break
===
'''

