# -*- coding: utf-8 -*-
##############################################################################
## 時間區段物件
##############################################################################
import os
import sys
import getopt
import time
import datetime
import requests
import threading
##############################################################################
import mysql . connector
from   mysql . connector              import Error
##############################################################################
import AITK
from   AITK . Database  . Query       import Query
from   AITK . Database  . Connection  import Connection
from   AITK . Database  . Pair        import Pair
from   AITK . Database  . Columns     import Columns
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
##############################################################################
## from   . Relation                        import Types
##############################################################################
"""
create table `periods` (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `type` integer default 0,
  `used` integer default 1,
  `start` bigint default 0,
  `end` bigint default 0,
  `realm` bigint default 0,
  `role` integer default 0,
  `item` integer default 0,
  `states` bigint default 0,
  `creation` bigint default (unix_timestamp() + 1420092377704080000),
  `modified` bigint default (unix_timestamp() + 1420092377704080000),
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uuid` (`uuid`),
  key `type` (`type`),
  key `used` (`used`),
  key `start` (`start`),
  key `end` (`end`),
  key `realm` (`realm`),
  key `role` (`role`),
  key `item` (`item`),
  key `states` (`states`),
  key `creation` (`creation`),
  key `modified` (`modified`),
  key `ltime` (`ltime`)
) Engine = Aria default charset = utf8mb4 ;
"""
##############################################################################
## 時間區段元件
##############################################################################
class Periode  ( Columns )                                                   :
  ############################################################################
  def __init__ ( self ) :
    super ( Columns , self ) . __init__ ( )
    self                     . Clear    ( )
  ############################################################################
  def __del__ ( self ) :
    pass
  ############################################################################
  def Clear ( self ) :
    self . Columns   = [ ]
    self . Id        = -1
    self . Uuid      =  0
    self . Type      =  1
    self . Used      =  1
    self . Start     =  0
    self . End       =  0
    self . States    =  1
    self . ltime     =  0
    self . TermCount =  0
  ############################################################################
  def assign ( self , item ) :
    self . Columns   = item . Columns
    self . Id        = item . Id
    self . Uuid      = item . Uuid
    self . Type      = item . Type
    self . Used      = item . Used
    self . Start     = item . Start
    self . End       = item . End
    self . States    = item . States
    self . ltime     = item . ltime
    self . TermCount = item . TermCount
  ############################################################################
  def set ( self , item , value ) :
    a = item.lower()
    if ( "id"     == a ) :
      self . Id     = value
    if ( "uuid"   == a ) :
      self . Uuid   = value
    if ( "type"   == a ) :
      self . Type   = value
    if ( "used"   == a ) :
      self . Used   = value
    if ( "start"  == a ) :
      self . Start  = value
    if ( "end"    == a ) :
      self . End    = value
    if ( "states" == a ) :
      self . States = value
    if ( "ltime"  == a ) :
      self . ltime  = value
  ############################################################################
  def get ( self , item ) :
    a = item.lower()
    if ( "id"     == a ) :
      return self . Id
    if ( "uuid"   == a ) :
      return self . Uuid
    if ( "type"   == a ) :
      return self . Type
    if ( "used"   == a ) :
      return self . Used
    if ( "start"  == a ) :
      return self . Start
    if ( "end"    == a ) :
      return self . End
    if ( "states" == a ) :
      return self . States
    if ( "ltime"  == a ) :
      return self . ltime
    return ""
  ############################################################################
  def tableItems ( self ) :
    S = [ ]
    S . append ( "id"     )
    S . append ( "uuid"   )
    S . append ( "type"   )
    S . append ( "used"   )
    S . append ( "start"  )
    S . append ( "end"    )
    S . append ( "states" )
    S . append ( "ltime"  )
    return S
  ############################################################################
  def pair ( self , item ) :
    v = self . get ( item )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems ( self ) :
    S = [ ]
    S . append ( "type"   )
    S . append ( "used"   )
    S . append ( "start"  )
    S . append ( "end"    )
    S . append ( "states" )
    return S
  ############################################################################
  def toString ( self ) :
    return "prd9%08d" % ( self . Uuid % 100000000 )
  ############################################################################
  def setType ( self , type ) :
    self . Type = type
  ############################################################################
  def setStates ( self , states ) :
    self . States = states
  ############################################################################
  def setInterval ( self , seconds ) :
    self . End += seconds
  ############################################################################
  def setNow ( self , shrink = False ) :
    SD = StarDate ( )
    SD . Now      ( )
    if ( shrink ) :
      SD . ShrinkMinute ( )
    self . Start = SD . Stardate
    self . setInterval ( 86400 )
  ############################################################################
  def setStart ( self , DATETIME , TZ = "" ) :
    SD = StarDate  ( )
    SD . fromInput ( DATETIME , TZ )
    self . Start = SD . Stardate
    return self . Start
  ############################################################################
  def setEnd ( self , DATETIME , TZ = "" ) :
    SD = StarDate  ( )
    SD . fromInput ( DATETIME , TZ )
    self . End = SD . Stardate
    return self . End
  ############################################################################
  def setPeriod ( self , STARTTIME , ENDTIME , TZ = "" ) :
    self . setStart ( STARTTIME , TZ )
    self . setEnd   ( ENDTIME   , TZ )
  ############################################################################
  def isCorrect ( self ) :
    return ( self . End > self . Start )
  ############################################################################
  def Between ( self , T ) :
    if ( self . Start > T ) :
      return 1
    if ( self . End > T ) :
      return 0
    return -1
  ############################################################################
  def Within ( self , T , PERIODs ) :
    for p in PERIODs :
      if ( p . Between ( T ) == 0 ) :
        return True
    return False
  ############################################################################
  def GetUuid ( self , DB , Table , Main ) :
    global Types
    BASE = 3500000000000000000
    TYPE = Types [ "Period" ]
    self . Uuid = DB . LastUuid ( Table , "uuid" , BASE )
    if ( self . Uuid <= 0 ) :
      return False
    DB . AddUuid ( Table , self . Uuid , self . Type )
    DB . AddUuid ( Main  , self . Uuid , TYPE )
    return self . Uuid
##############################################################################
