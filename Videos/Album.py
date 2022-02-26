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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
