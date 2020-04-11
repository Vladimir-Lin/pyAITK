# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import datetime
import requests
import threading
import mysql.connector
from   mysql.connector import Error
from   .SQL            import isSQL
from   .SqlQuery       import SqlQuery       as SqlQuery
from   .SqlConnection  import SqlConnection  as SqlConnection
from   .SqlConnection  import ConnectionPair as ConnectionPair

def Dump ( Host , db , table , file ) :
  if ( not isSQL ( Host ) ) :
    return False
  hostname = Host [ "hostname" ]
  username = Host [ "username" ]
  password = Host [ "password" ]
  if ( len ( db    ) <= 0 ) :
    return False
  if ( len ( file  ) <= 0 ) :
    return False
  cmd = ""
  if ( len ( table ) >  0 ) :
    cmd = f"mysqldump --hex-blob -h {hostname} -u {username} --password={password} {db} {table} > {file}"
  else :
    cmd = f"mysqldump --hex-blob -h {hostname} -u {username} --password={password} {db} > {file}"
  r = os.system ( cmd  )
  if ( r == 0 ) :
    return True
  return False

def Import ( Host , db , file ) :
  if ( not isSQL ( Host ) ) :
    return False
  hostname = Host [ "hostname" ]
  username = Host [ "username" ]
  password = Host [ "password" ]
  if ( len ( db   ) <= 0 ) :
    return False
  if ( len ( file ) <= 0 ) :
    return False
  cmd = f"mysql --max_allowed_packet=64M -h {hostname} -u {username} --password={password} {db} < {file}"
  r = os.system ( cmd  )
  if ( r == 0 ) :
    return True
  return False

def OptimizeAll ( CP , SHOW = False ) :
  SysDBs = [ "information_schema" , "mysql" , "performance_schema" , "test" ]
  SQ  = CP . Querier ( )
  DBs = CP . Write . ObtainUuids ( "show databases ;" )
  for db in DBs :
    if ( db not in SysDBs ) :
      CP . Write . Query ( f"use {db};" )
      TABLEs = CP . Write . ObtainUuids ( "show tables ;" )
      for t in TABLEs :
        X = SQ . MakeTable ( db , t )
        Q = f"optimize table {X} ;"
        if ( SHOW ) :
          print ( Q )
        CP . Write . Run ( Q )
  return True
