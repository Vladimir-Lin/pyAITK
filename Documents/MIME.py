# -*- coding: utf-8 -*-
##############################################################################
## MIME
##############################################################################
import os
import sys
import time
import datetime
##############################################################################
import mysql . connector
from   mysql . connector              import Error
##############################################################################
import AITK
from   AITK . Database  . Query       import Query
from   AITK . Database  . Connection  import Connection
from   AITK . Database  . Columns     import Columns
##############################################################################
## 附記元件
##############################################################################
class MIME ( Columns )                                                     :
  ############################################################################
  def __init__ ( self )                                                      :
    super ( Columns , self ) . __init__ ( )
    self                     . Clear    ( )
  ############################################################################
  def __del__  ( self )                                                      :
    pass
  ############################################################################
  def Clear    ( self )                                                      :
    self . Columns = [ ]
    self . Id      = -1
    self . Uuid    =  0
    self . Name    =  ""
    self . Prefer  =  0
    self . Note    =  ""
    self . Title   =  ""
    self . Comment =  ""
    self . Extra   =  ""
    self . ltime   =  0
  ############################################################################
  def assign ( self , item )                                                 :
    self . Columns = item . Columns
    self . Id      = item . Id
    self . Uuid    = item . Uuid
    self . Name    = item . Name
    self . Prefer  = item . Prefer
    self . Note    = item . Note
    self . Title   = item . Title
    self . Comment = item . Comment
    self . Extra   = item . Extra
    self . ltime   = item . ltime
  ############################################################################
  def set ( self , item , value )                                            :
    a = item . lower ( )
    if ( "id"     == a ) :
      self . Id      = value
    if ( "uuid"   == a ) :
      self . Uuid    = value
    if ( "name"   == a ) :
      self . Name    = str ( value )
    if ( "prefer"   == a ) :
      self . Prefer  = value
    if ( "note"  == a ) :
      self . Note    = str ( value )
    if ( "title"    == a ) :
      self . Title   = str ( value )
    if ( "comment" == a ) :
      self . Comment = str ( value )
    if ( "extra" == a ) :
      self . Extra   = str ( value )
    if ( "ltime"  == a ) :
      self . ltime   = value
  ############################################################################
  def get ( self , item )                                                    :
    a = item.lower()
    if ( "id"     == a ) :
      return self . Id
    if ( "uuid"   == a ) :
      return self . Uuid
    if ( "name"   == a ) :
      return self . Name
    if ( "prefer"   == a ) :
      return self . Prefer
    if ( "note"  == a ) :
      return self . Note
    if ( "title"    == a ) :
      return self . Title
    if ( "comment" == a ) :
      return self . Comment
    if ( "extra" == a ) :
      return self . Extra
    if ( "ltime"  == a ) :
      return self . ltime
    return ""
  ############################################################################
  def tableItems ( self )                                                    :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "name"                                                          ,
             "prefer"                                                        ,
             "note"                                                          ,
             "title"                                                         ,
             "comment"                                                       ,
             "extra"                                                         ,
             "ltime"                                                         ]
  ############################################################################
  def pair ( self , item )                                                   :
    v = self . get ( item )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems ( self                                                    ) :
    return [ "uuid"                                                          ,
             "name"                                                          ,
             "prefer"                                                        ,
             "note"                                                          ,
             "title"                                                         ,
             "comment"                                                       ,
             "extra"                                                         ]
##############################################################################
