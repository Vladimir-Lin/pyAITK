# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime

def isFTP ( parameters ) :
  if ( len ( parameters ) < 2 ) :
    return False
  hostname = parameters [ "hostname" ]
  port     = parameters [ "port" ]
  if ( len ( hostname ) <= 0 ) :
    return False
  if ( port             <= 0 ) :
    return False
  return True

def Download ( Host , output , remote ) :
  if ( len ( output ) <= 0 ) :
    return False
  if ( len ( remote ) <= 0 ) :
    return False
  if ( not isFTP ( Host ) ) :
    return False
  hostname = Host [ "hostname" ]
  username = Host [ "username" ]
  password = Host [ "password" ]
  port     = Host [ "port"     ]
  if ( len ( username ) > 0 ) and ( len ( password ) > 0 ) :
    cmd = f"curl -o {output} ftp://{username}:{password}@{hostname}:{port}{remote}"
  else :
    cmd = f"curl -o {output} ftp://{hostname}:{port}{remote}"
  dels = f"del /s {output}"
  os.system ( dels )
  r = os.system ( cmd  )
  if ( r == 0 ) :
    if os.path.isfile ( output ) :
      return True
  return False

def Upload ( Host , file , remote ) :
  if ( len ( file ) <= 0 ) :
    return False
  if ( len ( remote ) <= 0 ) :
    return False
  if ( not isFTP ( Host ) ) :
    return False
  hostname = Host [ "hostname" ]
  username = Host [ "username" ]
  password = Host [ "password" ]
  port     = Host [ "port"     ]
  if ( len ( username ) > 0 ) and ( len ( password ) > 0 ) :
    cmd = f"curl -T {file} ftp://{username}:{password}@{hostname}:{port}{remote}"
  else :
    cmd = f"curl -T {file} ftp://{hostname}:{port}{remote}"
  r = os.system ( cmd  )
  if ( r == 0 ) :
    return True
  return False
