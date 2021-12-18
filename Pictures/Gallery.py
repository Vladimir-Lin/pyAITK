# -*- coding: utf-8 -*-
##############################################################################
## 圖庫
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
class Gallery     (                                                        ) :
  ############################################################################
  def __init__    ( self                                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__     ( self                                                   ) :
    pass
  ############################################################################
  def NewUuid            ( self , DB , TABLE                               ) :
    ##########################################################################
    GUID = DB . LastUuid ( TABLE , "uuid" , 2800001000000000000              )
    DB   . AppendUuid    ( TABLE , GUID                                      )
    ##########################################################################
    return GUID
  ############################################################################
  def ConnectToPictures  ( self , DB , TABLE , UUID , T1 , UUIDs           ) :
    ##########################################################################
    REL = Relation       (                                                   )
    REL . set            ( "first" , UUID                                    )
    REL . setT1          ( T1                                                )
    REL . setT2          ( "Picture"                                         )
    REL . setRelation    ( "Subordination"                                   )
    REL . Joins          ( DB , TABLE , UUIDs                                )
    ##########################################################################
    return
  ############################################################################
  def ConnectToGalleries ( self , DB , TABLE , UUID , T1 , UUIDs           ) :
    ##########################################################################
    REL = Relation       (                                                   )
    REL . set            ( "first" , UUID                                    )
    REL . setT1          ( T1                                                )
    REL . setT2          ( "Gallery"                                         )
    REL . setRelation    ( "Subordination"                                   )
    REL . Joins          ( DB , TABLE , UUIDs                                )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
