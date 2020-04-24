# -*- coding: utf-8 -*-

"""
物件長編號表格

create table `uuids_template_name` (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `type` integer default 0,
  `used` integer default 1,
  `previous` integer default 0,
  `states` bigint default 0,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uuid` (`uuid`),
  key `type` (`type`),
  key `used` (`used`),
  key `previous` (`previous`),
  key `states` (`states`),
  key `ltime` (`ltime`)
) Engine = MyISAM default charset = utf8mb4 ;
"""

import os
import sys
import getopt
import time
import datetime
import logging
import requests
import threading

import mysql . connector
from   mysql . connector             import Error

from   ..      Database . Query      import Query      as Query
from   ..      Database . Connection import Connection as Connection
from   ..      Database . Columns    import Columns    as Columns

class UUID ( Columns ) :

  def __init__ ( self ) :
    super ( Columns , self ) . __init__ ( )
    self . Clear ( )

  def __del__ ( self ) :
    pass

  def Clear ( self ) :
    self . Columns  = [ ]
    self . Id       = -1
    self . Uuid     =  0
    self . Type     =  0
    self . Used     =  1
    self . Previous =  0
    self . States   =  0
    self . Update   =  0

  def assign ( self , item ) :
    self . Columns  = item . Columns
    self . Id       = item . Id
    self . Uuid     = item . Uuid
    self . Type     = item . Type
    self . Used     = item . Used
    self . Previous = item . Previous
    self . States   = item . States
    self . Update   = item . Update

  def set ( self , item , value ) :
    a = item . lower ( )
    if ( "id"       == a ) :
      self . Id       = value
    if ( "uuid"     == a ) :
      self . Uuid     = value
    if ( "type"     == a ) :
      self . Type     = value
    if ( "used"     == a ) :
      self . Used     = value
    if ( "previous" == a ) :
      self . Previous = value
    if ( "states"   == a ) :
      self . States   = value
    if ( "ltime"    == a ) :
      self . Update   = value

  def get ( self , item ) :
    a = item . lower ( )
    if ( "id"           == a ) :
      return self . Id
    if ( "uuid"         == a ) :
      return self . Uuid
    if ( "type"         == a ) :
      return self . Type
    if ( "used"         == a ) :
      return self . Used
    if ( "states"       == a ) :
      return self . States
    if ( "trainee"      == a ) :
      return self . Trainee
    if ( "tutor"        == a ) :
      return self . Tutor
    if ( "manager"      == a ) :
      return self . Manager
    if ( "receptionist" == a ) :
      return self . Receptionist
    if ( "item"         == a ) :
      return self . Item
    if ( "lecture"      == a ) :
      return self . Lecture
    if ( "description"  == a ) :
      return self . Description
    if ( "period"       == a ) :
      return self . Period
    if ( "start"        == a ) :
      return self . Start
    if ( "end"          == a ) :
      return self . End
    if ( "ltime"        == a ) :
      return self . Update
    return ""

  def tableItems ( self ) :
    return [ "id"       ,
             "uuid"     ,
             "type"     ,
             "used"     ,
             "previous" ,
             "states"   ,
             "ltime"    ]

  def pair ( self , item ) :
    v = self . get ( item )
    return f"`{item}` = {v}"

  def valueItems ( self ) :
    return [ "type"     ,
             "used"     ,
             "previous" ,
             "states"   ]

  def obtain ( self , R ) :
    List = self . tableItems ( )
    CNT  = 0
    for x in List :
      self . set ( x , R [ CNT ] )
      CNT += 1
    return True

  def ObtainsByUuid ( self , DB , Table ) :
    ITS = self . items ( )
    WHS = DB . WhereUuid ( self . Uuid , True )
    QQ = f"select {ITS} from {Table} {WHS}"
    DB . Execute ( QQ )
    LL = DB . FetchOne ( )
    if ( not LL ) :
      return False
    return self . obtain ( LL )

  def ObtainsById ( self , DB , Table ) :
    ITS = self . items ( )
    WHS = DB . WhereId ( self . Uuid , True )
    QQ = f"select {ITS} from {Table} {WHS}"
    DB . Execute ( QQ )
    LL = DB . FetchOne ( )
    if ( not LL ) :
      return False
    return self . obtain ( LL )
