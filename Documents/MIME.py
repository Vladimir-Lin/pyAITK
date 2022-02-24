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
## MIME元件
##############################################################################
class MIME               ( Columns                                         ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    self      . Clear    (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def Clear             ( self                                             ) :
    ##########################################################################
    self . Columns    = [                                                    ]
    self . Id         = -1
    self . Uuid       =  0
    self . MIME       =  ""
    self . Type       =  ""
    self . SubType    =  ""
    self . Comment    =  ""
    self . Wiki       =  ""
    self . ltime      =  0
    self . Extensions = [                                                    ]
    ##########################################################################
    return
  ############################################################################
  def assign ( self , item                                                 ) :
    ##########################################################################
    self . Columns    = item . Columns
    self . Id         = item . Id
    self . Uuid       = item . Uuid
    self . MIME       = item . MIME
    self . Type       = item . Type
    self . SubType    = item . SubType
    self . Comment    = item . Comment
    self . Wiki       = item . Wiki
    self . ltime      = item . ltime
    self . Extensions = item . Extensions
    ##########################################################################
    return
  ############################################################################
  def set                  ( self , item , value                           ) :
    ##########################################################################
    a = item . lower       (                                                 )
    ##########################################################################
    if                     ( "id"      == a                                ) :
      self . Id      = int ( value                                           )
    if                     ( "uuid"    == a                                ) :
      self . Uuid    = int ( value                                           )
    if                     ( "mime"    == a                                ) :
      self . MIME    = str ( value                                           )
    if                     ( "type"    == a                                ) :
      self . Type    = str ( value                                           )
    if                     ( "subtype" == a                                ) :
      self . SubType = str ( value                                           )
    if                     ( "comment" == a                                ) :
      self . Comment = str ( value                                           )
    if                     ( "wiki"    == a                                ) :
      self . Wiki    = str ( value                                           )
    if                     ( "ltime"   == a                                ) :
      self . ltime   = value
    ##########################################################################
    return
  ############################################################################
  def get            ( self , item                                         ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"      == a                                      ) :
      return int     ( self . Id                                             )
    if               ( "uuid"    == a                                      ) :
      return int     ( self . Uuid                                           )
    if               ( "mime"    == a                                      ) :
      return str     ( self . MIME                                           )
    if               ( "type"    == a                                      ) :
      return str     ( self . Type                                           )
    if               ( "subtype" == a                                      ) :
      return str     ( self . SubType                                        )
    if               ( "comment" == a                                      ) :
      return str     ( self . Comment                                        )
    if               ( "wiki"    == a                                      ) :
      return str     ( self . Wiki                                           )
    if               ( "ltime"   == a                                      ) :
      return self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems ( self                                                    ) :
    return       [ "id"                                                    , \
                   "uuid"                                                  , \
                   "mime"                                                  , \
                   "type"                                                  , \
                   "subtype"                                               , \
                   "comment"                                               , \
                   "wiki"                                                  , \
                   "ltime"                                                   ]
  ############################################################################
  def pair ( self , item )                                                   :
    v = self . get ( item )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems ( self                                                    ) :
    return       [ "uuid"                                                  , \
                   "mime"                                                  , \
                   "type"                                                  , \
                   "subtype"                                               , \
                   "comment"                                               , \
                   "wiki"                                                    ]
  ############################################################################
  def GetExtensions       ( self , DB , TABLE                              ) :
    ##########################################################################
    MIME  = self . Id
    ##########################################################################
    QQ    = f"""select `extension` from {TABLE}
                where ( `mime` = {MIME} )
                order by `id` asc ;"""
    QQ    = " " . join    ( QQ . split ( )                                   )
    DB    . Query         ( QQ                                               )
    ##########################################################################
    RR    = DB . FetchAll (                                                  )
    if                    ( RR in [ False , None ]                         ) :
      return              [                                                  ]
    ##########################################################################
    if                    ( len ( RR ) <= 0                                ) :
      return              [                                                  ]
    ##########################################################################
    ALL   =               [                                                  ]
    ##########################################################################
    for R in RR                                                              :
      ########################################################################
      E   = int           ( R [ 0 ]                                          )
      ALL . append        ( E                                                )
    ##########################################################################
    self  . Extensions = E
    ##########################################################################
    return E
##############################################################################
