# -*- coding: utf-8 -*-
##############################################################################
## 變數物件
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
## 變數元件
##############################################################################
class Variables ( Columns )                                                  :
  ############################################################################
  def __init__ ( self )                                                      :
    super ( Columns , self ) . __init__ ( )
    self                     . Clear    ( )
    return
  ############################################################################
  def __del__ ( self )                                                       :
    return
  ############################################################################
  def Clear ( self )                                                         :
    self . Columns   = [ ]
    self . Id        = -1
    self . Uuid      =  0
    self . Type      =  1
    self . Name      =  ""
    self . Value     =  ""
    self . ltime     =  0
    return
  ############################################################################
  def assign ( self , item )                                                 :
    self . Columns = item . Columns
    self . Id      = item . Id
    self . Uuid    = item . Uuid
    self . Type    = item . Type
    self . Name    = item . Name
    self . Value   = item . Value
    self . ltime   = item . ltime
    return
  ############################################################################
  def set ( self , item , value )                                            :
    a = item . lower ( )
    if ( "id"     == a ) :
      self . Id     = value
    if ( "uuid"   == a ) :
      self . Uuid   = value
    if ( "type"   == a ) :
      self . Type   = value
    if ( "name"   == a ) :
      self . Name   = value
    if ( "value"  == a ) :
      self . Value  = value
    if ( "ltime"  == a ) :
      self . ltime  = value
    return
  ############################################################################
  def get ( self , item )                                                    :
    a = item.lower()
    if ( "id"     == a ) :
      return self . Id
    if ( "uuid"   == a ) :
      return self . Uuid
    if ( "type"   == a ) :
      return self . Type
    if ( "name"   == a ) :
      return self . Name
    if ( "value"  == a ) :
      return self . Value
    if ( "ltime"  == a ) :
      return self . ltime
    return ""
  ############################################################################
  def tableItems ( self )                                                    :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "type"                                                          ,
             "name"                                                          ,
             "value"                                                         ,
             "ltime"                                                         ]
  ############################################################################
  def pair ( self , item )                                                   :
    v = self . get ( item )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems ( self )                                                    :
    return [ "type"                                                          ,
             "name"                                                          ,
             "value"                                                         ]
  ############################################################################
  def GetValue         ( self , DB , TABLE                                 ) :
    ##########################################################################
    U  = self . Uuid
    T  = self . Type
    N  = self . Name
    ##########################################################################
    QQ = f"""select `value` from {TABLE}
             where ( `uuid` = {U} )
             and ( `type` = {T} )
             and ( `name` = '{N}' )
             order by `id` desc
             limit 0,1 ;"""
    DB . Query         ( QQ                                                  )
    ##########################################################################
    RR = DB . FetchOne (                                                     )
    if                 ( RR in [ False , None ]                            ) :
      return None
    if                 ( len ( RR ) <= 0                                   ) :
      return None
    ##########################################################################
    return RR          [ 0                                                   ]
  ############################################################################
  def AssureValue            ( self , DB , TABLE                           ) :
    ##########################################################################
    UU  = self . Uuid
    TT  = self . Type
    NN  = self . Name
    VAL =                    ( self . Uuid                                 , \
                               self . Type                                 , \
                               self . Name                                 , \
                               self . Value                                , )
    QQ  = f"""delete from {TABLE}
              where ( `uuid` = {UU} )
                and ( `type` = {TT} )
                and ( `name` = '{NN}' ) ;"""
    QQ  = " " . join         ( QQ . split ( )                                )
    DB  . Query              ( QQ                                            )
    QQ  = f"""insert into {TABLE}
              ( `uuid`,`type`,`name`,`value` )
              values
              ( %s,%s,%s,%s ) ;"""
    QQ  = " " . join         ( QQ . split ( )                                )
    return DB  . QueryValues ( QQ , VAL                                      )
##############################################################################
