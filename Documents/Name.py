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
## 元件名稱
##############################################################################
class Name  ( Columns )                                                      :
  ############################################################################
  def __init__ ( self )                                                      :
    self . Clear ( )
    return
  ############################################################################
  def __del__  ( self )                                                      :
    return
  ############################################################################
  def Clear    ( self )                                                      :
    self . Columns   = [ ]
    self . Id        = -1
    self . Uuid      =  0
    self . Locality  =  1001
    self . Priority  =  1
    self . Relevance =  0
    self . Flags     =  0
    self . Utf8      =  0
    self . Length    =  0
    self . Name      =  ""
    self . ltime     =  0
    return
  ############################################################################
  def assign ( self , item ) :
    self . Columns   = item . Columns
    self . Id        = item . Id
    self . Uuid      = item . Uuid
    self . Locality  = item . Locality
    self . Priority  = item . Priority
    self . Relevance = item . Relevance
    self . Flags     = item . Flags
    self . Utf8      = item . Utf8
    self . Length    = item . Length
    self . Name      = item . Name
    self . ltime     = item . ltime
    return
  ############################################################################
  def set ( self , item , value )                                            :
    a = item . lower ( )
    if ( "id"        == a ) :
      self . Id        = value
    if ( "uuid"      == a ) :
      self . Uuid      = value
    if ( "locality"  == a ) :
      self . Locality  = value
    if ( "priority"  == a ) :
      self . Priority  = value
    if ( "relevance" == a ) :
      self . Relevance = value
    if ( "flags"     == a ) :
      self . Flags     = value
    if ( "utf8"      == a ) :
      self . Utf8      = value
    if ( "length"    == a ) :
      self . Length    = value
    if ( "name"      == a ) :
      self . Name      = value
    if ( "ltime"     == a ) :
      self . ltime     = value
  ############################################################################
  def get ( self , item ) :
    a = item . lower ( )
    if ( "id"        == a ) :
      return self . Id
    if ( "uuid"      == a ) :
      return self . Uuid
    if ( "locality"  == a ) :
      return self . Locality
    if ( "priority"  == a ) :
      return self . Priority
    if ( "relevance" == a ) :
      return self . Relevance
    if ( "flags"     == a ) :
      return self . Flags
    if ( "utf8"      == a ) :
      return self . Utf8
    if ( "length"    == a ) :
      return self . Length
    if ( "name"      == a ) :
      return self . Name
    if ( "ltime"     == a ) :
      return self . ltime
    return ""
  ############################################################################
  def tableItems ( self )                                                    :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "locality"                                                      ,
             "priority"                                                      ,
             "relevance"                                                     ,
             "flags"                                                         ,
             "utf8"                                                          ,
             "length"                                                        ,
             "name"                                                          ,
             "ltime"                                                         ]
  ############################################################################
  def pair ( self , item )                                                   :
    v = self . get ( item )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems ( self )                                                    :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "locality"                                                      ,
             "priority"                                                      ,
             "relevance"                                                     ,
             "flags"                                                         ,
             "utf8"                                                          ,
             "length"                                                        ,
             "name"                                                          ,
             "ltime"                                                         ]
##############################################################################
