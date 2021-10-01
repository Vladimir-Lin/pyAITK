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
## 時間區段元件
##############################################################################
class Periode            ( Columns                                         ) :
  ############################################################################
  def __init__           ( self                                            ) :
    super ( ) . __init__ (                                                   )
    self      . Clear    (                                                   )
    return
  ############################################################################
  def __del__           ( self                                             ) :
    return
  ############################################################################
  def Clear             ( self                                             ) :
    self . Columns   = [ ]
    self . Id        = -1
    self . Uuid      =  0
    self . Type      =  0
    self . Used      =  0
    self . Start     =  0
    self . End       =  0
    self . Realm     =  0
    self . Role      =  0
    self . Item      =  0
    self . States    =  0
    self . Creation  =  0
    self . Modified  =  0
    self . ltime     =  0
    return
  ############################################################################
  def assign            ( self , item                                      ) :
    self . Columns   = item . Columns
    self . Id        = item . Id
    self . Uuid      = item . Uuid
    self . Type      = item . Type
    self . Used      = item . Used
    self . Start     = item . Start
    self . End       = item . End
    self . Realm     = item . Realm
    self . Role      = item . Role
    self . Item      = item . Item
    self . States    = item . States
    self . Creation  = item . Creation
    self . Modified  = item . Modified
    self . ltime     = item . ltime
    return
  ############################################################################
  def set               ( self , item , value                              ) :
    a = item . lower ( )
    if ( "id"       == a ) :
      self . Id     = value
    if ( "uuid"     == a ) :
      self . Uuid   = value
    if ( "type"     == a ) :
      self . Type   = value
    if ( "used"     == a ) :
      self . Used   = value
    if ( "start"    == a ) :
      self . Start  = value
    if ( "end"      == a ) :
      self . End    = value
    if ( "realm"    == a ) :
      self . Realm = value
    if ( "role"     == a ) :
      self . Role = value
    if ( "item"     == a ) :
      self . Item = value
    if ( "states"   == a ) :
      self . States = value
    if ( "creation" == a ) :
      self . Creation = value
    if ( "modified" == a ) :
      self . Modified = value
    if ( "ltime"    == a ) :
      self . ltime  = value
    return
  ############################################################################
  def get               ( self , item                                      ) :
    a = item . lower ( )
    if ( "id"       == a ) :
      return self . Id
    if ( "uuid"     == a ) :
      return self . Uuid
    if ( "type"     == a ) :
      return self . Type
    if ( "used"     == a ) :
      return self . Used
    if ( "start"    == a ) :
      return self . Start
    if ( "end"      == a ) :
      return self . End
    if ( "realm"    == a ) :
      return self . Realm
    if ( "role"     == a ) :
      return self . Role
    if ( "item"     == a ) :
      return self . Item
    if ( "states"   == a ) :
      return self . States
    if ( "creation" == a ) :
      return self . Creation
    if ( "modified" == a ) :
      return self . Modified
    if ( "ltime"    == a ) :
      return self . ltime
    return ""
  ############################################################################
  def tableItems        ( self                                             ) :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "type"                                                          ,
             "used"                                                          ,
             "start"                                                         ,
             "end"                                                           ,
             "realm"                                                         ,
             "role"                                                          ,
             "item"                                                          ,
             "states"                                                        ,
             "creation"                                                      ,
             "modified"                                                      ,
             "ltime"                                                         ]
  ############################################################################
  def pair              ( self , item                                      ) :
    v = self . get      (        item                                        )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems        ( self                                             ) :
    return [ "type"                                                          ,
             "used"                                                          ,
             "start"                                                         ,
             "end"                                                           ,
             "realm"                                                         ,
             "role"                                                          ,
             "item"                                                          ,
             "states"                                                        ,
             "creation"                                                      ,
             "modified"                                                      ]
  ############################################################################
  def toString          ( self                                             ) :
    return "prd9%08d" % ( self . Uuid % 100000000                            )
  ############################################################################
  def fromString                   ( self , PRID                           ) :
    ##########################################################################
    PXID          = f"{PRID}"
    if                             ( len ( PXID ) != 12                    ) :
      self . Uuid = 0
      return 0
    ##########################################################################
    if                             ( "prd9" not in PXID                    ) :
      self . Uuid = 0
      return 0
    ##########################################################################
    UXID          = PXID . replace ( "prd9" , "35000000000"                  )
    self . Uuid   = int            ( UXID                                    )
    ##########################################################################
    return self . Uuid
  ############################################################################
  def setType           ( self , type                                      ) :
    self . Type = type
    return
  ############################################################################
  def setStates         ( self , states                                    ) :
    self . States = states
    return
  ############################################################################
  def setInterval       ( self , seconds                                    ) :
    self . End += seconds
    return
  ############################################################################
  def setNow            ( self , shrink = False                            ) :
    SD = StarDate       (                                                    )
    SD . Now            (                                                    )
    if                  ( shrink                                           ) :
      SD . ShrinkMinute (                                                    )
    self . Start = SD . Stardate
    self . setInterval  ( 86400                                              )
    return
  ############################################################################
  def setStart          ( self , DATETIME , TZ = ""                        ) :
    SD = StarDate       (                                                    )
    SD . fromInput      ( DATETIME , TZ                                      )
    self . Start = SD . Stardate
    return self . Start
  ############################################################################
  def setEnd            ( self , DATETIME , TZ = ""                        ) :
    SD = StarDate       (                                                    )
    SD . fromInput      ( DATETIME , TZ                                      )
    self . End = SD . Stardate
    return self . End
  ############################################################################
  def setPeriod         ( self , STARTTIME , ENDTIME , TZ = ""             ) :
    self . setStart     ( STARTTIME , TZ                                     )
    self . setEnd       ( ENDTIME   , TZ                                     )
    return
  ############################################################################
  def isCorrect         ( self                                             ) :
    return              ( self . End > self . Start                          )
  ############################################################################
  def Between           ( self , T                                         ) :
    if                  ( self . Start > T                                 ) :
      return 1
    if                  ( self . End   > T                                 ) :
      return 0
    return -1
  ############################################################################
  def Within            ( self , T , PERIODs                               ) :
    for p in PERIODs                                                         :
      if                ( p . Between ( T ) == 0                           ) :
        return True
    return False
  ############################################################################
  def GetUuid           ( self , DB , Table                                ) :
    BASE = 3500000000000000000
    self . Uuid = DB . LastUuid ( Table , "uuid" , BASE )
    if                  ( self . Uuid <= 0                                 ) :
      return False
    DB . AddUuid        ( Table , self . Uuid , self . Type                  )
    return self . Uuid
##############################################################################
