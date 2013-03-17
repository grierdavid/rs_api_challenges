#!/usr/bin/env python
''
Some misc functions that might make it into a module

''

def get_flavor(self, size=512):
  flavId = [flavor for flavor in cs.flavors.list()
                  if flavor.ram == 512][0]
  return flavId 

def get_server_id(name):
  sid = [s.id for s in cs.servers.list()
         if name == s.name]
  return sid[0]

def get_img_id(self):
  imgid = [i.id for i in cs.images.list()
         if imgname == i.name] 
  return imgid[0]

