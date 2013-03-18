#!/usr/bin/env python
''
Some misc functions that might make it into a module


''

def get_flavor_id(self, size=512):
  flavId = [flavor for flavor in cs.flavors.list()
                  if flavor.ram == 512][0]
  return flavId 

def get_server_id(name):
  sId = [s.id for s in cs.servers.list()
         if name == s.name]
  return sId[0]

def get_img_id(self):
  imgId = [i.id for i in cs.images.list()
         if imgname == i.name] 
  return imgId[0]

def get_container(name):
  conId = [c.id for c in cf.get_all_containers()
         if name == c.name] 
  return conId[0]

