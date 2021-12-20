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
  def AssureIcon         ( self , DB , TABLE , UUID , T1 , PUID            ) :
    ##########################################################################
    REL = Relation       (                                                   )
    REL . set            ( "first"  , UUID                                   )
    REL . set            ( "second" , PUID                                   )
    REL . setT1          ( T1                                                )
    REL . setT2          ( "Picture"                                         )
    REL . setRelation    ( "Using"                                           )
    REL . Assure         ( DB , TABLE                                        )
    ##########################################################################
    return
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
  def PicturesFromWebPage  ( self , DB , TABLE , WPID                      ) :
    ##########################################################################
    REL = Relation         (                                                 )
    REL . set              ( "second" , WPID                                 )
    REL . setT1            ( "Picture"                                       )
    REL . setT2            ( "WebPage"                                       )
    REL . setRelation      ( "Subordination"                                 )
    return REL . GetOwners ( DB , TABLE                                      )
  ############################################################################
  def PictureRelateWebPage ( self , DB , TABLE , PCID , WPID               ) :
    ##########################################################################
    REL = Relation         (                                                 )
    REL . set              ( "first"  , PCID                                 )
    REL . set              ( "second" , WPID                                 )
    REL . setT1            ( "Picture"                                       )
    REL . setT2            ( "WebPage"                                       )
    REL . setRelation      ( "Subordination"                                 )
    REL . Join             ( DB , TABLE                                      )
    ##########################################################################
    return
  ############################################################################
  def GetLastestPosition     ( self , DB , TABLE , REL                     ) :
    ##########################################################################
    ITEM   = "`position`"
    OPTS   = f"order by {ITEM} desc"
    LMTS   = "limit 0 , 1"
    ##########################################################################
    WS     = REL . FirstItem ( OPTS , LMTS                                   )
    QQ     = f"select {ITEM} from {TABLE} {WS} ;"
    DB     . Query           ( QQ                                            )
    RR     = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( RR in [ False , None ]                      ) :
      return 0
    ##########################################################################
    if                       ( len ( RR ) != 1                             ) :
      return 0
    ##########################################################################
    return int               ( RR [ 0 ]                                      )
  ############################################################################
  def CreateRepositionSQL     ( self , SQLs , TABLE , REL , START , UUIDs  ) :
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL   . set             ( "second" , UUID                              )
      WS    = REL . ExactItem (                                              )
      QQ    = f"update {TABLE} set `position` = {START} {WS} ;"
      START = START + 1
      SQLs  . append          ( QQ                                           )
    ##########################################################################
    return SQLs
  ############################################################################
  def RepositionGallery                ( self , DB , TABLE , UUID , UUIDs  ) :
    ##########################################################################
    REL   = Relation                   (                                     )
    REL   . set                        ( "first"  , UUID                     )
    REL   . setT1                      ( "Gallery"                           )
    REL   . setT2                      ( "Picture"                           )
    REL   . setRelation                ( "Subordination"                     )
    ##########################################################################
    LAST  = self . GetLastestPosition  ( DB , TABLE , REL                    )
    L     = LAST + 1000
    SQLs  =                            [                                     ]
    SQLs  = self . CreateRepositionSQL ( SQLs , TABLE , REL , L , UUIDs      )
    SQLs  = self . CreateRepositionSQL ( SQLs , TABLE , REL , 0 , UUIDs      )
    ##########################################################################
    for QQ in SQLs                                                           :
      DB  . Query                      ( QQ                                  )
    ##########################################################################
    return
  ############################################################################
  def GetSubgroupGalleries     ( self , DB , TABLE , SUBGROUP              ) :
    ##########################################################################
    REL = Relation             (                                             )
    REL . set                  ( "first" , SUBGROUP                          )
    REL . setT1                ( "Subgroup"                                  )
    REL . setT2                ( "Gallery"                                   )
    REL . setRelation          ( "Subordination"                             )
    return REL . Subordination ( DB , TABLE                                  )
  ############################################################################
  ############################################################################
##############################################################################
