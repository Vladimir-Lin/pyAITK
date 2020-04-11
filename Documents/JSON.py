# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import getopt
import json
import logging
import threading

def Load ( Filename ) :
  if ( not os . path . isfile ( Filename ) ) :
    return { }
  TEXT     = ""
  with open ( Filename , "rb" ) as jsonFile :
    TEXT   = jsonFile . read ( )
  if ( len ( TEXT ) <= 0 ) :
    return { }
  BODY = TEXT . decode ( "utf-8" )
  if ( len ( BODY ) <= 0 ) :
    return { }
  return json . loads  ( BODY    )

def Merge ( Main , After , Ignore = [ ] ) :
  if ( len ( After ) <= 0 ) :
    return Main
  KEYs = After . keys ( )
  if ( len ( KEYs ) <= 0 ) :
    return Main
  for k in KEYs :
    if ( k not in Ignore ) :
      Main [ k ] = After [ k ]
  return Main

def Save ( Filename , Main ) :
  with     open ( Filename , 'w' , encoding = 'utf-8' ) as f   :
    json . dump ( Main , f , ensure_ascii = False , indent = 4 )
  return True
