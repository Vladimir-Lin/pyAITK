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
from   AITK . Database   . Connection     import Connection     as Connection
##############################################################################
from   AITK . Documents  . Name           import Name           as NameItem
from   AITK . Documents  . Name           import Naming         as Naming
from   AITK . Documents  . Notes          import Notes          as NoteItem
from   AITK . Documents  . Variables      import Variables      as VariableItem
from   AITK . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK . Calendars  . StarDate       import StarDate       as StarDate
from   AITK . Calendars  . Periode        import Periode        as Periode
from   AITK . Essentials . Relation       import Relation       as Relation
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
  def PlaceUuidToFirst ( self , UUID , UUIDs                               ) :
    ##########################################################################
    ICONs     =        [ UUID                                                ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if               ( U not in ICONs                                    ) :
        ######################################################################
        ICONs . append ( U                                                   )
    ##########################################################################
    return ICONs
  ############################################################################
  def TableListings       ( self , TABLEs , PREFIX , Amount                ) :
    ##########################################################################
    for i in range        ( 0 , Amount                                     ) :
      ########################################################################
      ID    = int         ( i + 1                                            )
      ########################################################################
      MSG   = f"{ID}"
      MSG   = MSG . zfill ( 4                                                )
      ########################################################################
      Table = f"{PREFIX}_{MSG}`"
      ########################################################################
      if                  ( Table not in TABLEs                            ) :
        TABLEs . append   ( Table                                            )
    ##########################################################################
    return TABLEs
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
  def JoinIcon        ( self , DB , TABLE , UUID , T1 , PUID               ) :
    ##########################################################################
    REL = Relation    (                                                      )
    REL . set         ( "first"  , UUID                                      )
    REL . set         ( "second" , PUID                                      )
    REL . setT1       ( T1                                                   )
    REL . setT2       ( "Picture"                                            )
    REL . setRelation ( "Using"                                              )
    REL . Join        ( DB , TABLE                                           )
    ##########################################################################
    return
  ############################################################################
  def JoinIconByT1    ( self , DB , TABLE , UUID , T1 , PUID               ) :
    ##########################################################################
    REL = Relation    (                                                      )
    REL . set         ( "first"  , UUID                                      )
    REL . set         ( "second" , PUID                                      )
    REL . set         ( "t1"     , T1                                        )
    REL . setT2       ( "Picture"                                            )
    REL . setRelation ( "Using"                                              )
    REL . Join        ( DB , TABLE                                           )
    ##########################################################################
    return
  ############################################################################
  def GetIcons                 ( self , DB , TABLE , UUID , T1             ) :
    ##########################################################################
    REL = Relation             (                                             )
    REL . set                  ( "first" , UUID                              )
    REL . setT1                ( T1                                          )
    REL . setT2                ( "Picture"                                   )
    REL . setRelation          ( "Using"                                     )
    ##########################################################################
    return REL . Subordination ( DB      , TABLE                        )
  ############################################################################
  def GetPictures              ( self , DB , TABLE , UUID , T1 , RELATED   ) :
    ##########################################################################
    REL = Relation             (                                             )
    REL . set                  ( "first"    , UUID                           )
    REL . set                  ( "t1"       , T1                             )
    REL . setT2                ( "Picture"                                   )
    REL . set                  ( "relation" , RELATED                        )
    ##########################################################################
    return REL . Subordination ( DB , TABLE                                  )
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
  def GetOwnerGalleries        ( self , DB , TABLE , T1 , GUID             ) :
    ##########################################################################
    REL = Relation             (                                             )
    REL . set                  ( "first" , GUID                              )
    REL . setT1                ( T1                                          )
    REL . setT2                ( "Gallery"                                   )
    REL . setRelation          ( "Subordination"                             )
    return REL . Subordination ( DB , TABLE                                  )
  ############################################################################
  def RepositionIcons       ( self , DB , TABLE , FIRST , T1 , UUIDs       ) :
    ##########################################################################
    REL = Relation          (                                                )
    REL . set               ( "first" , FIRST                                )
    REL . set               ( "t1"    , T1                                   )
    REL . setT2             ( "Picture"                                      )
    REL . setRelation       ( "Using"                                        )
    REL . RepositionByFirst ( DB , TABLE , UUIDs                             )
    ##########################################################################
    return
  ############################################################################
  def LookingForContains               ( self                              , \
                                         DB                                , \
                                         TABLE                             , \
                                         UUIDs                             , \
                                         T1                                , \
                                         RELATED                           ) :
    ##########################################################################
    CUIDs         =                    [                                     ]
    MUIDs         =                    {                                     }
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 1                ) :
      return CUIDs
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      PCIDs       = self . GetPictures ( DB , TABLE , UUID , T1 , RELATED    )
      MUIDs [ UUID ] = PCIDs
    ##########################################################################
    BCNT          = len                ( UUIDs                               )
    ACNT          = int                ( BCNT - 1                            )
    ASTART        = 0
    ##########################################################################
    while                              ( ASTART < ACNT                     ) :
      ########################################################################
      BSTART      = int                ( ASTART + 1                          )
      AUID        = UUIDs              [ ASTART                              ]
      AUIDs       = MUIDs              [ AUID                                ]
      TOTAL       = len                ( AUIDs                               )
      ########################################################################
      while                            ( BSTART < BCNT                     ) :
        ######################################################################
        BUID      = UUIDs              [ BSTART                              ]
        BUIDs     = MUIDs              [ BUID                                ]
        ######################################################################
        MATCH     = False
        CNT       = 0
        ######################################################################
        while                          ( ( not MATCH ) and ( CNT < TOTAL ) ) :
          ####################################################################
          PUID    = AUIDs              [ CNT                                 ]
          ####################################################################
          if                           ( PUID in BUIDs                     ) :
            ##################################################################
            MATCH = True
          ####################################################################
          CNT     = int                ( CNT + 1                             )
        ######################################################################
        if                             ( MATCH                             ) :
          ####################################################################
          if                           ( AUID not in CUIDs                 ) :
            CUIDs . append             ( AUID                                )
          ####################################################################
          if                           ( BUID not in CUIDs                 ) :
            CUIDs . append             ( BUID                                )
        ######################################################################
        BSTART    = int                ( BSTART + 1                          )
      ########################################################################
      ASTART      = int                ( ASTART + 1                          )
    ##########################################################################
    return CUIDs
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
