# -*- coding: utf-8 -*-
##############################################################################
## FileExtension
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
## 副檔名元件
##############################################################################
class FileExtension      ( Columns                                         ) :
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
  def Clear            ( self                                              ) :
    ##########################################################################
    self . Columns   = [                                                     ]
    self . Id        = -1
    self . Uuid      =  0
    self . Extension =  ""
    self . Creator   =  ""
    self . Comment   =  ""
    self . Wiki      =  ""
    self . ltime     =  0
    ##########################################################################
    return
  ############################################################################
  def assign ( self , item                                                 ) :
    ##########################################################################
    self . Columns   = item . Columns
    self . Id        = item . Id
    self . Uuid      = item . Uuid
    self . Extension = item . Extension
    self . Creator   = item . Creator
    self . Comment   = item . Comment
    self . Wiki      = item . Wiki
    self . ltime     = item . ltime
    ##########################################################################
    return
  ############################################################################
  def set                    ( self , item , value                         ) :
    ##########################################################################
    a = item . lower         (                                               )
    ##########################################################################
    if                       ( "id"        == a                            ) :
      self . Id        = int ( value                                         )
    if                       ( "uuid"      == a                            ) :
      self . Uuid      = int ( value                                         )
    if                       ( "extension" == a                            ) :
      self . Extension = str ( value                                         )
    if                       ( "creator"   == a                            ) :
      self . Creator   = str ( value                                         )
    if                       ( "comment"   == a                            ) :
      self . Comment   = str ( value                                         )
    if                       ( "wiki"      == a                            ) :
      self . Wiki      = str ( value                                         )
    if                       ( "ltime"     == a                            ) :
      self . ltime     = value
    ##########################################################################
    return
  ############################################################################
  def get            ( self , item                                         ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"        == a                                    ) :
      return int     ( self . Id                                             )
    if               ( "uuid"      == a                                    ) :
      return int     ( self . Uuid                                           )
    if               ( "extension" == a                                    ) :
      return str     ( self . Extension                                      )
    if               ( "creator"   == a                                    ) :
      return str     ( self . Creator                                        )
    if               ( "comment"   == a                                    ) :
      return str     ( self . Comment                                        )
    if               ( "wiki"      == a                                    ) :
      return str     ( self . Wiki                                           )
    if               ( "ltime"     == a                                    ) :
      return self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems ( self                                                    ) :
    return       [ "id"                                                    , \
                   "uuid"                                                  , \
                   "extension"                                             , \
                   "creator"                                               , \
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
                   "extension"                                             , \
                   "creator"                                               , \
                   "comment"                                               , \
                   "wiki"                                                    ]
  ############################################################################
  def ObtainsAll               ( self , DB , TABLE                         ) :
    ##########################################################################
    QQ      = f"select `uuid` from {TABLE} order by `id` asc ;"
    UUIDs   = DB . ObtainUuids ( QQ                                          )
    ##########################################################################
    LISTS   =                  [                                             ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      FE    = FileExtension    (                                             )
      FE    . Uuid = UUID
      FE    . ObtainsByUuid    ( DB , TABLE                                  )
      LISTS . append           ( FE                                          )
    ##########################################################################
    return LISTS
##############################################################################
