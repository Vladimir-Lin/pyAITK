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
## 變數元件
##############################################################################
class Variables ( Columns )                                                  :
  ############################################################################
  def __init__ ( self ) :
    self . Clear ( )
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
##############################################################################
