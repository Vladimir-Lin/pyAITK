# -*- coding: utf-8 -*-
##############################################################################
## 影集
##############################################################################
import os
import sys
import time
import datetime
import logging
import requests
import threading
import gettext
import binascii
import hashlib
import base64
##############################################################################
from   AITK  . Database   . Connection     import Connection     as Connection
##############################################################################
from   AITK  . Documents  . Name           import Name           as NameItem
from   AITK  . Documents  . Name           import Naming         as Naming
from   AITK  . Documents  . Notes          import Notes          as NoteItem
from   AITK  . Documents  . Variables      import Variables      as VariableItem
from   AITK  . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK  . Calendars  . StarDate       import StarDate       as StarDate
from   AITK  . Calendars  . Periode        import Periode        as Periode
from   AITK  . Essentials . Relation       import Relation       as Relation
##############################################################################
class Album           (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    ##########################################################################
    self . Uuid     = 0
    self . Settings = {                                                      }
    self . Tables   = {                                                      }
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  ## 新增影片
  ############################################################################
  def NewAlbum               ( self , DB                                   ) :
    ##########################################################################
    HEAD   = self . Settings [ "Head"                                        ]
    ALMTAB = self . Tables   [ "Albums"                                      ]
    ##########################################################################
    UUID   = DB . LastUuid   ( ALMTAB , "uuid" , HEAD                        )
    ##########################################################################
    QQ     = f"""insert into {ALMTAB}
                 ( `uuid`,`used`,`states` )
                 values
                 ( {UUID} , 1 , 0 ) ;"""
    QQ     = " " . join      ( QQ . split ( )                                )
    DB     . Query           ( QQ                                            )
    ##########################################################################
    return UUID
  ############################################################################
  def ConnectToAlbums ( self , DB , TABLE , UUID , T1 , UUIDs              ) :
    ##########################################################################
    REL = Relation    (                                                      )
    REL . set         ( "first" , UUID                                       )
    REL . setT1       ( T1                                                   )
    REL . setT2       ( "Album"                                              )
    REL . setRelation ( "Subordination"                                      )
    REL . Joins       ( DB , TABLE , UUIDs                                   )
    ##########################################################################
    return
  ############################################################################
  def GetSubgroupAlbums        ( self , DB , TABLE , SUBGROUP              ) :
    ##########################################################################
    REL        = Relation      (                                             )
    REL        . set           ( "first" , SUBGROUP                          )
    REL        . setT1         ( "Subgroup"                                  )
    REL        . setT2         ( "Album"                                     )
    REL        . setRelation   ( "Subordination"                             )
    return REL . Subordination ( DB , TABLE                                  )
  ############################################################################
  def GetIdentifiers        ( self , DB                                    ) :
    ##########################################################################
    IDFTAB  = self . Tables [ "Identifiers"                                  ]
    IDs     =               [                                                ]
    UUID    = self . Uuid
    ##########################################################################
    QQ      = f"""select `name` from {IDFTAB}
                   where ( `type` = 76 )
                     and ( `uuid` = {UUID} )
                     order by `name` asc ;"""
    QQ      = " " . join    ( QQ . split ( )                                 )
    DB      . Query         ( QQ                                             )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return IDs
    ##########################################################################
    if                      ( len ( ALL ) <= 0                             ) :
      return IDs
    ##########################################################################
    for ID in ALL                                                            :
      ########################################################################
      N     = ID            [ 0                                              ]
      ########################################################################
      try                                                                    :
        N   = N . decode    ( "utf-8"                                        )
      except                                                                 :
        pass
      ########################################################################
      if                    ( N not in IDs                                 ) :
        IDs . append        ( N                                              )
    ##########################################################################
    return IDs
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
