# -*- coding: utf-8 -*-
##############################################################################
## CLI Parser
## 命令列解譯器
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import vlc
import math
import cv2
##############################################################################
import pathlib
from   pathlib                           import Path
##############################################################################
import AITK
##############################################################################
from   AITK . Database  . Query          import Query
from   AITK . Database  . Connection     import Connection
from   AITK . Database  . Pair           import Pair
from   AITK . Database  . Columns        import Columns
##############################################################################
from   AITK . Calendars . StarDate       import StarDate       as StarDate
##############################################################################
from   AITK . Documents . JSON           import Load           as LoadJson
from   AITK . Documents . JSON           import Save           as SaveJson
from   AITK . Documents . Name           import Name           as NameItem
from   AITK . Documents . Name           import Naming         as Naming
from   AITK . Documents . ParameterQuery import ParameterQuery as ParameterQuery
from   AITK . Documents . Variables      import Variables      as VariableItem
##############################################################################
from   AITK . UUIDs     . UuidListings6  import appendUuid
from   AITK . UUIDs     . UuidListings6  import appendUuids
from   AITK . UUIDs     . UuidListings6  import assignUuids
from   AITK . UUIDs     . UuidListings6  import getUuids
##############################################################################
class CliParser  (                                                         ) :
  ############################################################################
  def __init__   ( self                                                    ) :
    ##########################################################################
    self . Clear (                                                           )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def Clear               ( self                                           ) :
    ##########################################################################
    self . CLI          = {                                                  }
    self . Settings     = {                                                  }
    self . Translations = {                                                  }
    self . Tables       = {                                                  }
    self . DbConf       = {                                                  }
    self . Logger       = None
    self . Execution    = None
    self . GetClipboard = None
    ##########################################################################
    return
  ############################################################################
  def LOG         ( self , message                                         ) :
    ##########################################################################
    if            ( self . Logger in [ False , None ]                      ) :
      return
    ##########################################################################
    self . Logger (        message                                           )
    ##########################################################################
    return
  ############################################################################
  def Load                  ( self , Filename                              ) :
    ##########################################################################
    self   . CLI = LoadJson (        Filename                                )
    ##########################################################################
    if ( "Tables"      not in self . CLI                                   ) :
      ########################################################################
      self . CLI [ "Tables" ] = {                                            }
    ##########################################################################
    if ( "CoverOptions" not in self . CLI [ "Tables" ]                     ) :
      ########################################################################
      CVOPTs = { "Base"       : 3800700000000000001                        , \
                 "Prefer"     : 0                                          , \
                 "Master"     : "`cios`.`pictures_covers`"                 , \
                 "Depot"      : "`cios`.`pictures_depot_covers`"           , \
                 "Thumb"      : "`cios`.`thumbs_covers`"                   , \
                 "ThumbDepot" : "`cios`.`thumbs_depot_covers`"             , \
                 "Hash"       : "`cios`.`pictureproperties_hash`"          , \
                 "Histogram"  : "`cios`.`pictureproperties_statistics`"      }
      ########################################################################
      self . CLI [ "Tables" ] [ "CoverOptions" ] = CVOPTs
    ##########################################################################
    if ( "AlbumCovers" not in self . CLI [ "Tables" ]                      ) :
      ########################################################################
      ACTABs = { "Pictures"          : "`cios`.`pictureorders`"            , \
                 "Information"       : "`cios`.`pictures_covers`"          , \
                 "Depot"             : "`cios`.`pictures_depot_covers`"    , \
                 "Galleries"         : "`cios`.`galleries`"                , \
                 "Contours"          : "`cios`.`contours`"                 , \
                 "Parameters"        : "`cios`.`parameters`"               , \
                 "Variables"         : "`cios`.`variables`"                , \
                 "Names"             : "`cios`.`names_others`"             , \
                 "NamesEditing"      : "`appellations`.`names_others_0013`" , \
                 "Notes"             : "`cios`.`notes_materials`"          , \
                 "ThumbsInformation" : "`cios`.`thumbs_covers`"            , \
                 "Thumb"             : "`cios`.`thumbs_depot_covers`"      , \
                 "Relation"          : "`cios`.`relations`"                , \
                 "RelationPeople"    : "`cios`.`relations_people`"         , \
                 "RelationPictures"  : "`cios`.`relations_pictures`"       , \
                 "RelationVideos"    : "`affiliations`.`relations_videos_0003`" , \
                 "RelationCovers"    : "`affiliations`.`relations_videos_0007`" , \
                 "PictureHash"       : "`cios`.`pictureproperties_hash`"   , \
                 "PictureStatistics" : "`cios`.`pictureproperties_statistics`" , \
                 "BaseUuid"          : "3800700000000000001"                 }
      ########################################################################
      self . CLI [ "Tables" ] [ "AlbumCovers" ] = ACTABs
    ##########################################################################
    if ( "PeopleView"    not in self . CLI [ "Tables" ]                    ) :
      ########################################################################
      PETABs = { "People"            : "`leagues`.`people_av`"             , \
                 "Parameters"        : "`cios`.`parameters`"               , \
                 "Variables"         : "`cios`.`variables`"                , \
                 "Names"             : "`cios`.`names`"                    , \
                 "NamesEditing"      : "`appellations`.`names_people`"     , \
                 "Notes"             : "`cios`.`notes_descriptions`"       , \
                 "Information"       : "`cios`.`pictures`"                 , \
                 "Depot"             : "`cios`.`picturedepot`"             , \
                 "ThumbsInformation" : "`cios`.`thumbs`"                   , \
                 "Thumb"             : "`cios`.`thumbdepot`"               , \
                 "FaceRegions"       : "`cios`.`faceregions`"              , \
                 "FaceRecognitions"  : "`cios`.`facerecognitions`"         , \
                 "Relation"          : "`cios`.`relations`"                , \
                 "RelationPeople"    : "`affiliations`.`relations_videos`" , \
                 "RelationPictures"  : "`cios`.`relations_pictures`"         }
      ########################################################################
      self . CLI [ "Tables" ] [ "PeopleView" ] = PETABs
    ##########################################################################
    if ( "GalleriesView" not in self . CLI [ "Tables" ]                    ) :
      ########################################################################
      GATABs = { "Galleries"          : "`cios`.`galleries`"                 ,
                 "Contours"           : "`cios`.`contours`"                  ,
                 "Names"              : "`appellations`.`names_others`"      ,
                 "NamesEditing"       : "`appellations`.`names_others`"      ,
                 "Notes"              : "`cios`.`notes_materials`"           ,
                 "ThumbsInformation"  : "`cios`.`thumbs`"                    ,
                 "Thumb"              : "`cios`.`thumbdepot`"                ,
                 "Parameters"         : "`cios`.`parameters`"                ,
                 "Variables"          : "`cios`.`variables`"                 ,
                 "Relation"           : "`cios`.`relations`"                 ,
                 "RelationPeople"     : "`cios`.`relations_people`"          ,
                 "RelationPictures"   : "`affiliations`.`relations_pictures_0017`" ,
                 "RelationIcons"      : "`affiliations`.`relations_pictures`"      ,
                 "RelationVideos"     : "`cios`.`relations_videos`"          }
      ########################################################################
      self . CLI [ "Tables" ] [ "GalleriesView" ] = GATABs
    ##########################################################################
    return
  ############################################################################
  def Save   ( self , Filename                                             ) :
    ##########################################################################
    CLIF = self . CLI
    ##########################################################################
    GRPs =   [ "Film"                                                      , \
               "Episode"                                                   , \
               "People"                                                    , \
               "Crowd"                                                     , \
               "Galleries"                                                 , \
               "Organization"                                                ]
    ##########################################################################
    for G in GRPs                                                            :
      ########################################################################
      if                         ( G in CLIF                               ) :
        ######################################################################
        CLIF [ G ] [ "Found" ] = [                                           ]
    ##########################################################################
    CLIF [ "Action" ] = ""
    ##########################################################################
    SaveJson (        Filename , CLIF                                        )
    ##########################################################################
    return
  ############################################################################
  def Run            ( self                                                ) :
    ##########################################################################
    if               ( self . Execution in [ False , None ]                ) :
      return
    ##########################################################################
    self . Execution (                                                       )
    ##########################################################################
    return
  ############################################################################
  def PurgeCommand  ( self , cmd                                           ) :
    ##########################################################################
    C = cmd
    C = C . replace ( "\r" , ""                                              )
    C = C . replace ( "\n" , ""                                              )
    ##########################################################################
    return C
  ############################################################################
  def StripCommand    ( self , cmd , prefix                                ) :
    ##########################################################################
    PLEN = len        ( prefix                                               )
    AT   = cmd . find ( prefix                                               )
    ##########################################################################
    if                ( AT < 0                                             ) :
      return ""
    ##########################################################################
    S    = cmd        [ AT + PLEN :                                          ]
    S    = S . lstrip (                                                      )
    S    = S . rstrip (                                                      )
    ##########################################################################
    return S
  ############################################################################
  def GetLineNames            ( self , TEXT                                ) :
    ##########################################################################
    if                        ( len ( TEXT ) <= 0                          ) :
      return                  [                                              ]
    ##########################################################################
    LINEz = TEXT . splitlines (                                              )
    ##########################################################################
    if                        ( len ( LINEz ) <= 0                         ) :
      return                  [                                              ]
    ##########################################################################
    LINEs =                   [                                              ]
    ##########################################################################
    for L in LINEz                                                           :
      ########################################################################
      if                      ( len ( L ) <= 0                             ) :
        continue
      ########################################################################
      X   = L . replace       ( "\t" , ""                                    )
      X   = X . replace       ( "\r" , ""                                    )
      X   = X . replace       ( "\n" , ""                                    )
      X   = " " . join        ( X . split (                                ) )
      ########################################################################
      if                      ( len ( X ) <= 0                             ) :
        continue
      ########################################################################
      LINEs . append          ( X                                            )
    ##########################################################################
    return LINEs
  ############################################################################
  def ExtractLineNames        ( self , TEXT                                ) :
    ##########################################################################
    if                        ( len ( TEXT ) <= 0                          ) :
      return                  [                                              ]
    ##########################################################################
    ZTEXT = TEXT  . replace   ( "Starring: " , ""                            )
    LINEz = ZTEXT . split     ( ", "                                         )
    ##########################################################################
    if                        ( len ( LINEz ) <= 0                         ) :
      return                  [                                              ]
    ##########################################################################
    LINEs =                   [                                              ]
    ##########################################################################
    for Z in LINEz                                                           :
      ########################################################################
      L   = Z .  strip        (                                              )
      L   = L . lstrip        (                                              )
      L   = L . lstrip        (                                              )
      ########################################################################
      if                      ( len ( L ) <= 0                             ) :
        continue
      ########################################################################
      X   = L . replace       ( "\t" , ""                                    )
      X   = X . replace       ( "\r" , ""                                    )
      X   = X . replace       ( "\n" , ""                                    )
      X   = " " . join        ( X . split (                                ) )
      ########################################################################
      if                      ( len ( X ) <= 0                             ) :
        continue
      ########################################################################
      LINEs . append          ( X                                            )
    ##########################################################################
    return LINEs
  ############################################################################
  def ObtainsVariantTables   ( self                                        , \
                               DB                                          , \
                               VARTAB                                      , \
                               UUID                                        , \
                               TYPE                                        , \
                               NAME                                        , \
                               JSON                                        ) :
    ##########################################################################
    VARI   = VariableItem    (                                               )
    VARI   . Uuid = UUID
    VARI   . Type = TYPE
    VARI   . Name = NAME
    ##########################################################################
    BODY   = VARI . GetValue ( DB , VARTAB                                   )
    if                       ( BODY in [ False , None ]                    ) :
      return JSON
    ##########################################################################
    try                                                                      :
      BODY = BODY . decode   ( "utf-8"                                       )
    except                                                                   :
      pass
    ##########################################################################
    if                       ( len ( BODY ) <= 0                           ) :
      return JSON
    ##########################################################################
    try                                                                      :
      J    = json . loads    ( BODY                                          )
    except                                                                   :
      return JSON
    ##########################################################################
    JKS    = JSON . keys     (                                               )
    ##########################################################################
    for T in JKS                                                             :
      ########################################################################
      if                     ( T not in J                                  ) :
        J [ T ] = JSON       [ T                                             ]
    ##########################################################################
    return J
  ############################################################################
  def OrganizeNamesByWestern  ( self                                       ) :
    ##########################################################################
    DB     = Connection       (                                              )
    ##########################################################################
    if                        ( not DB . ConnectTo ( self . DbConf )       ) :
      ########################################################################
      self . LOG              ( json . dumps  ( TABLEs )                     )
      ########################################################################
      return
    ##########################################################################
    DB     . Prepare          (                                              )
    ##########################################################################
    PEOTAB = "`leagues`.`people_av_0002`"
    WESNAM = "`appellations`.`names_people_0004`"
    JPNNAM = "`appellations`.`names_people_0005`"
    PEONAM = "`appellations`.`names_people_0010`"
    OTHNAM = "`appellations`.`names_others_0020`"
    COLS   = "`uuid`,`locality`,`priority`,`relevance`,`flags`,`utf8`,`length`,`name`,`ltime`"
    ##########################################################################
    QQ     = f"""insert into {WESNAM} ( {COLS} )
                 select {COLS} from {OTHNAM}
                 where ( `uuid` in ( select `uuid` from {PEOTAB} ) ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""delete  from {OTHNAM}
                 where ( `uuid` in ( select `uuid` from {PEOTAB} ) ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""select `uuid` from {JPNNAM}
                 where ( `uuid` in ( select `uuid` from {PEOTAB} ) )
                 group by `uuid` asc ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    self   . LOG              ( QQ                                           )
    UUIDs  = DB . ObtainUuids ( QQ                                           )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ   = f"""select `relevance` from {JPNNAM}
                 where ( `uuid` in ( {UUID} ) )
                 group by `relevance` asc ;"""
      QQ   = " " . join       ( QQ . split (                               ) )
      self . LOG              ( QQ                                           )
      REVs = DB . ObtainUuids ( QQ                                           )
      ########################################################################
      for R in REVs                                                          :
        ######################################################################
        QQ = f"""select `priority` from {WESNAM}
                 where ( `uuid` in ( {UUID} ) )
                   and ( `relevance` = {R} )
                   order by `priority` desc
                   limit 0 , 1 ;"""
        QQ = " " . join       ( QQ . split (                               ) )
        self . LOG            ( QQ                                           )
        PP = DB . GetOne      ( QQ , -1                                      )
        PP = int              ( int ( PP ) + 1                               )
        ######################################################################
        QQ = f"""update {JPNNAM}
                 set `priority` = `priority` + {PP}
                 where ( `uuid` in ( {UUID} ) )
                   and ( `relevance` = {R} )
                 order by `priority` desc ;"""
        QQ = " " . join       ( QQ . split (                               ) )
        self . LOG            ( QQ                                           )
        DB . Query            ( QQ                                           )
        ######################################################################
        QQ = f"""insert into {WESNAM} ( {COLS} )
                 select {COLS} from {JPNNAM}
                 where ( `uuid` in ( {UUID} ) )
                   and ( `relevance` = {R} ) ;"""
        QQ = " " . join       ( QQ . split (                               ) )
        self . LOG            ( QQ                                           )
        DB . Query            ( QQ                                           )
        ######################################################################
        QQ = f"""delete  from {JPNNAM}
                 where ( `uuid` in ( {UUID} ) )
                   and ( `relevance` = {R} ) ;"""
        QQ = " " . join       ( QQ . split (                               ) )
        self . LOG            ( QQ                                           )
        DB . Query            ( QQ                                           )
    ##########################################################################
    DB     . Close            (                                              )
    self   . LOG              ( "OrganizeNamesByWestern Completed"           )
    ##########################################################################
    return
  ############################################################################
  def ParkPeopleVideos        ( self                                       ) :
    ##########################################################################
    DB     = Connection       (                                              )
    ##########################################################################
    if                        ( not DB . ConnectTo ( self . DbConf )       ) :
      ########################################################################
      self . LOG              ( json . dumps  ( TABLEs )                     )
      ########################################################################
      return
    ##########################################################################
    DB     . Prepare          (                                              )
    ##########################################################################
    VIDREL =   "`affiliations`.`relations_videos_0005`"
    LTRELs = [ "`affiliations`.`relations_videos_0010`"                    , \
               "`affiliations`.`relations_people_0020`"                      ]
    COLS   = "`first`,`t1`,`second`,`t2`,`relation`,`position`,`reverse`,`prefer`,`membership`,`description`,`ltime`"
    ##########################################################################
    for TAGREL in LTRELs                                                     :
      ########################################################################
      QQ   = f"""insert into {VIDREL} ( {COLS} )
                 select {COLS} from {TAGREL}
                 where ( `t1` = 7 )
                   and ( `t2` = 76 )
                   and ( `relation` = 1 )
                 order by `id` asc ;"""
      QQ   = " " . join       ( QQ . split (                               ) )
      self . LOG              ( QQ                                           )
      DB   . Query            ( QQ                                           )
      ##########################################################################
      QQ   = f"""delete  from {TAGREL}
                 where ( `t1` = 7 )
                   and ( `t2` = 76 )
                   and ( `relation` = 1 ) ;"""
      QQ   = " " . join       ( QQ . split (                               ) )
      self . LOG              ( QQ                                           )
      DB   . Query            ( QQ                                           )
    ##########################################################################
    DB     . Close            (                                              )
    self   . LOG              ( "ParkPeopleVideos Completed"                 )
    ##########################################################################
    return
  ############################################################################
  def ParkPictureDescriptions ( self                                       ) :
    ##########################################################################
    DB     = Connection       (                                              )
    ##########################################################################
    if                        ( not DB . ConnectTo ( self . DbConf )       ) :
      ########################################################################
      self . LOG              ( json . dumps  ( TABLEs )                     )
      ########################################################################
      return
    ##########################################################################
    DB     . Prepare          (                                              )
    ##########################################################################
    FPD1   = "`factors`.`variables_pictures_0030`"
    FPD2   = "`factors`.`variables_pictures_0031`"
    COLS   = "`uuid`,`type`,`name`,`value`,`ltime`"
    ##########################################################################
    QQ     = f"""insert into {FPD1} ( {COLS} )
                 select {COLS} from {FPD2}
                 where ( `type` = 9 )
                   and ( `name` = 'Description' )
                 order by `id` asc ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""delete  from {FPD2}
                 where ( `type` = 9 )
                   and ( `name` = 'Description' ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"optimize table {FPD1} ;"
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    RR     = DB . FetchAll    (                                              )
    ##########################################################################
    QQ     = f"optimize table {FPD2} ;"
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    RR     = DB . FetchAll    (                                              )
    ##########################################################################
    DB     . Close            (                                              )
    self   . LOG              ( "ParkPictureDescriptions Completed"          )
    ##########################################################################
    return
  ############################################################################
  def MovePictureDescriptions ( self                                       ) :
    ##########################################################################
    DB     = Connection       (                                              )
    ##########################################################################
    if                        ( not DB . ConnectTo ( self . DbConf )       ) :
      ########################################################################
      self . LOG              ( json . dumps  ( TABLEs )                     )
      ########################################################################
      return
    ##########################################################################
    DB     . Prepare          (                                              )
    ##########################################################################
    FPD1   = "`factors`.`variables_pictures_0031`"
    FPD2   = "`factors`.`variables_pictures_0080`"
    COLS   = "`uuid`,`type`,`name`,`value`,`ltime`"
    ##########################################################################
    QQ     = f"""insert into {FPD1} ( {COLS} )
                 select {COLS} from {FPD2}
                 where ( `type` = 9 )
                   and ( `name` = 'Description' )
                 order by `id` asc ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""delete  from {FPD2}
                 where ( `type` = 9 )
                   and ( `name` = 'Description' ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"optimize table {FPD1} ;"
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    RR     = DB . FetchAll    (                                              )
    ##########################################################################
    QQ     = f"optimize table {FPD2} ;"
    self   . LOG              ( QQ                                           )
    DB     . Query            ( QQ                                           )
    RR     = DB . FetchAll    (                                              )
    ##########################################################################
    DB     . Close            (                                              )
    self   . LOG              ( "MovePictureDescriptions Completed"          )
    ##########################################################################
    return
  ############################################################################
  def hasScope                   ( self                                    ) :
    ##########################################################################
    if                           ( "Scope" not in self . CLI               ) :
      ########################################################################
      M    = self . Translations [ "CMD::NoScope"                            ]
      self . LOG                 ( M                                         )
      ########################################################################
      return False
    ##########################################################################
    return   True
  ############################################################################
  def decodeScopeForWhat ( self , cmd , sequences                          ) :
    ##########################################################################
    SCOPE  = self . CLI  [ "Scope"                                           ]
    ##########################################################################
    if                   ( len ( SCOPE ) <= 0                              ) :
      return             ( True   , False ,                                  )
    ##########################################################################
    T      = len         ( sequences                                         )
    ##########################################################################
    if                   ( T < 3                                           ) :
      return             ( True   , False ,                                  )
    ##########################################################################
    S      = sequences   [ 2                                                 ]
    S      = S . lower   (                                                   )
    ##########################################################################
    if                   ( "exact" == S                                    ) :
      ########################################################################
      self . CLI [ SCOPE ] [ "Lower" ] = False
      ########################################################################
      return             ( True   , False ,                                  )
    ##########################################################################
    if                   ( "lower" == S                                    ) :
      ########################################################################
      self . CLI [ SCOPE ] [ "Lower" ] = True
      ########################################################################
      return             ( True   , False ,                                  )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    return               ( True   , False ,                                  )
  ############################################################################
  def decodeScope                ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Scope"                         ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    if                           ( T < 2                                   ) :
      ########################################################################
      if                         ( "Scope" in self . CLI                   ) :
        ######################################################################
        S  = self . CLI          [ "Scope"                                   ]
        M  = self . Translations [ "CMD::CurrentScope:"                      ]
        R  = f"{M}{S}"
        ######################################################################
        self . LOG               ( R                                         )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    S      = sequences           [ 1                                         ]
    S      = S . lower           (                                           )
    ##########################################################################
    if                           ( "for" == S                              ) :
      ########################################################################
      self . decodeScopeForWhat  (        cmd , sequences                    )
    ##########################################################################
    KEY    = "Film"
    TM     = self . Translations [ f"CMD::Scope::Key::{KEY}"                 ]
    ##########################################################################
    if                           ( S in TM                                 ) :
      ########################################################################
      self   . CLI [ "Scope" ] = KEY
      ########################################################################
      if                         ( KEY not in self . CLI                   ) :
        ######################################################################
        self . CLI [ KEY     ] = { "First"     : 0                         , \
                                   "T1"        : 76                        , \
                                   "Second"    : 0                         , \
                                   "T2"        : 11                        , \
                                   "Relation"  : 1                         , \
                                   "Name"      : ""                        , \
                                   "Names"     : [ ]                       , \
                                   "Locality"  : 1002                      , \
                                   "Lower"     : True                      , \
                                   "Languages" : [ 1001 , 1002 , 1006 ]      }
      ########################################################################
      M    = self . Translations [ f"CMD::Scope::{KEY}"                      ]
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    KEY    = "Episode"
    TM     = self . Translations [ f"CMD::Scope::Key::{KEY}"                 ]
    ##########################################################################
    if                           ( S in TM                                 ) :
      ########################################################################
      self   . CLI [ "Scope" ] = KEY
      ########################################################################
      if                         ( KEY not in self . CLI                   ) :
        ######################################################################
        self . CLI [ KEY     ] = { "First"     : 0                         , \
                                   "T1"        : 158                       , \
                                   "Second"    : 0                         , \
                                   "T2"        : 76                        , \
                                   "Relation"  : 1                         , \
                                   "Name"      : ""                        , \
                                   "Names"     : [ ]                       , \
                                   "Locality"  : 1002                      , \
                                   "Lower"     : True                      , \
                                   "Languages" : [ 1001 , 1002 , 1006 ]      }
      ########################################################################
      M    = self . Translations [ f"CMD::Scope::{KEY}"                      ]
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    KEY    = "People"
    TM     = self . Translations [ f"CMD::Scope::Key::{KEY}"                 ]
    ##########################################################################
    if                           ( S in TM                                 ) :
      ########################################################################
      self   . CLI [ "Scope" ] = KEY
      ########################################################################
      if                         ( KEY not in self . CLI                   ) :
        ######################################################################
        self . CLI [ KEY     ] = { "Uuid"      : 0                         , \
                                   "Names"     : { }                       , \
                                   "Languages" : [ 1001 , 1002 , 1006 ]      }
      ########################################################################
      M    = self . Translations [ f"CMD::Scope::{KEY}"                      ]
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    KEY    = "Crowd"
    TM     = self . Translations [ f"CMD::Scope::Key::{KEY}"                 ]
    ##########################################################################
    if                           ( S in TM                                 ) :
      ########################################################################
      self   . CLI [ "Scope" ] = KEY
      ########################################################################
      if                         ( KEY not in self . CLI                   ) :
        ######################################################################
        self . CLI [ KEY     ] = { "First"     : 0                         , \
                                   "T1"        : 158                       , \
                                   "Second"    : 0                         , \
                                   "T2"        : 7                         , \
                                   "Relation"  : 1                         , \
                                   "Name"      : ""                        , \
                                   "Names"     : [ ]                       , \
                                   "Locality"  : 1002                      , \
                                   "Lower"     : True                      , \
                                   "Languages" : [ 1001 , 1002 , 1006 ]      }
      ########################################################################
      M    = self . Translations [ f"CMD::Scope::{KEY}"                      ]
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    KEY    = "Galleries"
    TM     = self . Translations [ f"CMD::Scope::Key::{KEY}"                 ]
    ##########################################################################
    if                           ( S in TM                                 ) :
      ########################################################################
      self   . CLI [ "Scope" ] = KEY
      ########################################################################
      if                         ( KEY not in self . CLI                   ) :
        ######################################################################
        self . CLI [ KEY     ] = { "First"     : 0                         , \
                                   "T1"        : 158                       , \
                                   "Second"    : 0                         , \
                                   "T2"        : 64                        , \
                                   "Relation"  : 1                         , \
                                   "Name"      : ""                        , \
                                   "Names"     : [ ]                       , \
                                   "Locality"  : 1002                      , \
                                   "Lower"     : True                      , \
                                   "Languages" : [ 1001 , 1002 , 1006 ]      }
      ########################################################################
      M    = self . Translations [ f"CMD::Scope::{KEY}"                      ]
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    KEY    = "Organization"
    TM     = self . Translations [ f"CMD::Scope::Key::{KEY}"                 ]
    ##########################################################################
    if                           ( S in TM                                 ) :
      ########################################################################
      self   . CLI [ "Scope" ] = KEY
      ########################################################################
      if                         ( KEY not in self . CLI                   ) :
        ######################################################################
        self . CLI [ KEY     ] = { "First"     : 0                         , \
                                   "T1"        : 158                       , \
                                   "Second"    : 0                         , \
                                   "T2"        : 38                        , \
                                   "Relation"  : 1                         , \
                                   "Name"      : ""                        , \
                                   "Names"     : [ ]                       , \
                                   "Locality"  : 1002                      , \
                                   "Lower"     : True                      , \
                                   "Languages" : [ 1001 , 1002 , 1006 ]      }
      ########################################################################
      M    = self . Translations [ f"CMD::Scope::{KEY}"                      ]
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    return                       ( False , False ,                           )
  ############################################################################
  def decodeName                 ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Name"                          ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    Scope  = self . CLI          [ "Scope"                                   ]
    ##########################################################################
    if                           ( T < 2                                   ) :
      ########################################################################
      if                         ( "Name" not in self . CLI [ Scope ]      ) :
        return                   ( False , False ,                           )
      ########################################################################
      MSG  = self . Translations [ "CMD::Name::Current"                      ]
      NAME = self . CLI [ Scope ] [ "Name"                                   ]
      M    = f"{MSG}{NAME}"
      ########################################################################
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( False , False ,                           )
    ##########################################################################
    NAME   = self . StripCommand (        cmd , sequences [ 0 ]              )
    ##########################################################################
    if                           ( len ( NAME ) <= 0                       ) :
      return
    ##########################################################################
    self   . CLI [ Scope ] [ "Name" ] = NAME
    ##########################################################################
    MSG    = self . Translations [ "CMD::Name::Assign"                       ]
    M      = f"{MSG}{NAME}"
    self   . LOG                 ( M                                         )
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def decodeNames                ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Names"                         ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    Scope  = self . CLI          [ "Scope"                                   ]
    ##########################################################################
    if                           ( T < 2                                   ) :
      ########################################################################
      if                         ( "Names" not in self . CLI [ Scope ]     ) :
        return                   ( False , False ,                           )
      ########################################################################
      MSG  = self . Translations [ "CMD::Names::Current"                     ]
      NS   = self . CLI [ Scope ] [ "Names"                                  ]
      ########################################################################
      if                         ( len ( NS ) <= 0                         ) :
        return                   ( False , False ,                           )
      ########################################################################
      M    = "\n" . join         ( NS                                        )
      ########################################################################
      self . LOG                 ( f"{MSG}\n{M}"                             )
      ########################################################################
      return                     ( False , False ,                           )
    ##########################################################################
    NAME   = self . StripCommand (        cmd , sequences [ 0 ]              )
    ##########################################################################
    if                           ( len ( NAME ) <= 0                       ) :
      return
    ##########################################################################
    if                           ( "Names" not in self . CLI [ Scope ]     ) :
      ########################################################################
      self . CLI [ Scope ] [ "Names" ] = [                                   ]
    ##########################################################################
    self   . CLI [ Scope ] [ "Names" ] . append ( NAME                       )
    ##########################################################################
    MSG    = self . Translations [ "CMD::Names::Append"                      ]
    M      = f"{MSG}{NAME}"
    self   . LOG                 ( NAME                                      )
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def decodeLanguages            ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Languages"                     ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    Scope  = self . CLI          [ "Scope"                                   ]
    ##########################################################################
    if                           ( T < 2                                   ) :
      ########################################################################
      if                         ( "Languages" not in self . CLI [ Scope ] ) :
        return                   ( False , False ,                           )
      ########################################################################
      MSG  = self . Translations [ "CMD::Languages::Current"                 ]
      LS   = self . CLI [ Scope ] [ "Languages"                              ]
      ########################################################################
      if                         ( len ( LS ) <= 0                         ) :
        return                   ( False , False ,                           )
      ########################################################################
      NS   =                     [ MSG                                       ]
      for LID in LS                                                          :
        ######################################################################
        NS . append              ( f"{LID}"                                  )
      ########################################################################
      M    = " " . join          ( NS                                        )
      ########################################################################
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( False , False ,                           )
    ##########################################################################
    self . CLI [ Scope ] [ "Languages" ] = [                                 ]
    ##########################################################################
    ENID   = self . Translations [ "CMD::Languages::English"                 ]
    TWID   = self . Translations [ "CMD::Languages::Chinese"                 ]
    JPID   = self . Translations [ "CMD::Languages::Japanese"                ]
    ##########################################################################
    for L in sequences                                                       :
      ########################################################################
      S    = L . lower           (                                           )
      ########################################################################
      if                         ( S in ENID                               ) :
        self . CLI [ Scope ] [ "Languages" ] . append ( 1001                 )
      ########################################################################
      if                         ( S in TWID                               ) :
        self . CLI [ Scope ] [ "Languages" ] . append ( 1002                 )
      ########################################################################
      if                         ( S in JPID                               ) :
        self . CLI [ Scope ] [ "Languages" ] . append ( 1006                 )
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def decodeLocality             ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Locality"                      ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    Scope  = self . CLI          [ "Scope"                                   ]
    ##########################################################################
    if                           ( T < 2                                   ) :
      ########################################################################
      if                         ( "Locality" not in self . CLI [ Scope ]  ) :
        return                   ( False , False ,                           )
      ########################################################################
      MSG  = self . Translations [ "CMD::Locality::Current"                  ]
      LCN  = self . CLI [ Scope ] [ "Locality"                               ]
      NS   =                     [ MSG , f"{LCN}"                            ]
      ########################################################################
      M    = " " . join          ( NS                                        )
      ########################################################################
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( False , False ,                           )
    ##########################################################################
    ENID   = self . Translations [ "CMD::Languages::English"                 ]
    TWID   = self . Translations [ "CMD::Languages::Chinese"                 ]
    JPID   = self . Translations [ "CMD::Languages::Japanese"                ]
    ##########################################################################
    for L in sequences                                                       :
      ########################################################################
      S    = L . lower           (                                           )
      ########################################################################
      if                         ( S in ENID                               ) :
        self . CLI [ Scope ] [ "Locality" ] = 1001
      ########################################################################
      if                         ( S in TWID                               ) :
        self . CLI [ Scope ] [ "Locality" ] = 1002
      ########################################################################
      if                         ( S in JPID                               ) :
        self . CLI [ Scope ] [ "Locality" ] = 1006
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def LookForEpisodeTables ( self                                          ) :
    ##########################################################################
    KEY    = "Episode"
    TABLEs = self . Tables [ "VideoAlbums" ] [ "Subordination"               ]
    ##########################################################################
    self   . CLI [ KEY ] [ "Tables" ] = TABLEs
    ##########################################################################
    DB     = Connection    (                                                 )
    ##########################################################################
    if                     ( not DB . ConnectTo ( self . DbConf )          ) :
      ########################################################################
      self . LOG           ( json . dumps  ( TABLEs )                        )
      ########################################################################
      return
    ##########################################################################
    DB     . Prepare       (                                                 )
    ##########################################################################
    VARTAB = self . Tables [ "VariantTables" ] [ "Variables"                 ]
    ##########################################################################
    SCOPE  = "ViewAlbums"
    F      = self . CLI    [ KEY ] [ "First"                                 ]
    T1     = self . CLI    [ KEY ] [ "T1"                                    ]
    R      = self . CLI    [ KEY ] [ "Relation"                              ]
    ##########################################################################
    TABLEs = self . ObtainsVariantTables ( DB                              , \
                                           VARTAB                          , \
                                           str ( F )                       , \
                                           T1                              , \
                                           SCOPE                           , \
                                           TABLEs                            )
    ##########################################################################
    self   . CLI [ KEY ] [ "Tables" ] = TABLEs
    ##########################################################################
    DB     . Close         (                                                 )
    ##########################################################################
    self   . LOG           ( json . dumps  ( TABLEs )                        )
    ##########################################################################
    return
  ############################################################################
  def FindEpisodeByName     ( self                                         ) :
    ##########################################################################
    KEY     = "Episode"
    TABLEs  = self . CLI    [ KEY ] [ "Tables"                               ]
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    ## NAMTAB  = TABLEs        [ "NamesVideo"                                   ]
    NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    RELTAB  = TABLEs        [ "RelationVideos"                               ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    NAME    = self . CLI    [ KEY ] [ "Name"                                 ]
    UUID    = self . CLI    [ KEY ] [ "First"                                ]
    T1      = self . CLI    [ KEY ] [ "T1"                                   ]
    R       = self . CLI    [ KEY ] [ "Relation"                             ]
    ##########################################################################
    HMSG    = self . Translations [ f"CMD::{KEY}::Search:"                   ]
    MLOG    = f"{HMSG}{NAME}"
    self    . LOG           ( MLOG                                           )
    ##########################################################################
    LNAME   = NAME . lower  (                                                )
    ZNAME   = f"%{LNAME}%"
    ##########################################################################
    VQ      = f"""select `second` from {RELTAB}
                 where ( `t1` = {T1} )
                   and ( `relation` = {R} )
                   and ( `first` = {UUID} )"""
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
    ##########################################################################
    QQ      = " " . join    ( QQ . split ( )                                 )
    ##########################################################################
    self    . LOG           ( QQ                                             )
    ##########################################################################
    DB      . QueryValues   ( QQ , ( ZNAME , )                               )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindEpisodeByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def FindAllEpisodeByName  ( self                                         ) :
    ##########################################################################
    KEY     = "Episode"
    TABLEs  = self . CLI    [ KEY ] [ "Tables"                               ]
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    NAMTAB  = TABLEs        [ "Names"                                        ]
    ## NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    ALMTAB  = TABLEs        [ "Albums"                                       ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    NAME    = self . CLI    [ KEY ] [ "Name"                                 ]
    ##########################################################################
    TOLWR   = True
    ##########################################################################
    if                      ( "Lower" in self . CLI [ KEY ]                ) :
      TOLWR = self . CLI    [ KEY ] [ "Lower"                                ]
    ##########################################################################
    HMSG    = self . Translations   [ f"CMD::{KEY}::Search:"                 ]
    MLOG    = f"{HMSG}{NAME}"
    self    . LOG           ( MLOG                                           )
    ##########################################################################
    LNAME   = NAME
    ##########################################################################
    if                      ( TOLWR                                        ) :
      LNAME = NAME . lower  (                                                )
    ##########################################################################
    ZNAME   = f"%{LNAME}%"
    ##########################################################################
    VQ      = f"select `uuid` from {ALMTAB} where ( `used` > 0 )"
    ##########################################################################
    if                      ( TOLWR                                        ) :
      ########################################################################
      QQ    = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
      ########################################################################
    else                                                                     :
      ########################################################################
      QQ    = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( convert ( `name` using utf8 ) like %s )
                  group by `uuid` asc ;"""
    ##########################################################################
    QQ      = " " . join    ( QQ . split ( )                                 )
    ##########################################################################
    self    . LOG           ( QQ                                             )
    ##########################################################################
    DB      . QueryValues   ( QQ , ( ZNAME , )                               )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindEpisodeByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def FindAllEpisodeByNames ( self                                         ) :
    ##########################################################################
    KEY     = "Episode"
    TABLEs  = self . CLI    [ KEY ] [ "Tables"                               ]
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    NAMEs   = self . CLI    [ KEY ] [ "Names"                                ]
    ##########################################################################
    if                      ( len ( NAMEs ) <= 0                           ) :
      return
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    NAMTAB  = TABLEs        [ "Names"                                        ]
    ## NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    ALMTAB  = TABLEs        [ "Albums"                                       ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    TOLWR   = True
    ##########################################################################
    if                      ( "Lower" in self . CLI [ KEY ]                ) :
      TOLWR = self . CLI    [ KEY ] [ "Lower"                                ]
    ##########################################################################
    ALL     =               [                                                ]
    HMSG    = self . Translations   [ f"CMD::{KEY}::Search:"                 ]
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      MLOG  = f"{HMSG}{NAME}"
      self  . LOG           ( MLOG                                           )
      ########################################################################
      LNAME = NAME
      ########################################################################
      if                    ( TOLWR                                        ) :
        LNAME = NAME . lower (                                               )
      ########################################################################
      ZNAME = f"%{LNAME}%"
      ########################################################################
      VQ    = f"select `uuid` from {ALMTAB} where ( `used` > 0 )"
      ########################################################################
      if                    ( TOLWR                                        ) :
        ######################################################################
        QQ  = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
      ########################################################################
      else                                                                   :
        ######################################################################
        QQ  = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( convert ( `name` using utf8 ) like %s )
                  group by `uuid` asc ;"""
      ########################################################################
      QQ    = " " . join    ( QQ . split ( )                                 )
      ########################################################################
      self  . LOG           ( QQ                                             )
      ########################################################################
      DB    . QueryValues   ( QQ , ( ZNAME , )                               )
      ALLz  = DB . FetchAll (                                                )
      ########################################################################
      if                    ( ALLz in [ False , None ]                     ) :
        continue
      ########################################################################
      for UAID in ALLz                                                       :
        ######################################################################
        if                  ( UAID not in ALL                              ) :
          ####################################################################
          ALL . append      ( UAID                                           )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindEpisodeByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def FindEpisodeNoName     ( self                                         ) :
    ##########################################################################
    KEY     = "Episode"
    TABLEs  = self . CLI    [ KEY ] [ "Tables"                               ]
    MAXE    = 30
    ##########################################################################
    if                      ( "MaxEmpty" in self . CLI [ KEY ]             ) :
      MAXE  = int           ( self . CLI [ KEY ] [ "MaxEmpty"              ] )
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    NAMTAB  = TABLEs        [ "Names"                                        ]
    ## NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    ALMTAB  = TABLEs        [ "Albums"                                       ]
    RELTAB  = TABLEs        [ "Relation"                                     ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    NAME    = self . CLI    [ KEY ] [ "Name"                                 ]
    UUID    = self . CLI    [ KEY ] [ "First"                                ]
    T1      = self . CLI    [ KEY ] [ "T1"                                   ]
    R       = self . CLI    [ KEY ] [ "Relation"                             ]
    ##########################################################################
    HMSG    = self . Translations   [ f"CMD::{KEY}::FindNoname"              ]
    self    . LOG           ( HMSG                                           )
    ##########################################################################
    VQ      = f"""select `second` from {RELTAB}
                  where ( `t1` = {T1} )
                    and ( `relation` = {R} )
                    and ( `first` = {UUID} )"""
    ##########################################################################
    EQ      = f"""select `uuid` from {NAMTAB}
                  where ( `uuid` in ( {VQ} ) )
                    and ( length ( `name` ) > 0 )
                  group by `uuid`"""
    ##########################################################################
    XQ      = f"""select `first` from {RELTAB}
                  where ( `t1` = 76 )
                    and ( `t2` = 9 )
                    and ( `relation` in ( 1 , 12 ) )
                    and ( `first` in ( {VQ} ) )
                  group by `first`"""
    ##########################################################################
    WQ      = f"""select `first` from {RELTAB}
                  where ( `t1` = 76 )
                    and ( `t2` = 208 )
                    and ( `relation` in ( 10 ) )
                    and ( `first` in ( {VQ} ) )
                  group by `first`"""
    ##########################################################################
    QQ      = f"""select `second` from {RELTAB}
                  where ( `t1` = {T1} )
                    and ( `relation` = {R} )
                    and ( `first` = {UUID} )
                    and ( `second` not in ( {EQ} ) )
                    and ( `second` not in ( {XQ} ) )
                    and ( `second` not in ( {WQ} ) )
                  order by `second` asc
                  limit 0 , {MAXE} ;"""
    ##########################################################################
    QQ      = " " . join    ( QQ . split ( )                                 )
    ##########################################################################
    self    . LOG           ( QQ                                             )
    ##########################################################################
    DB      . Query         ( QQ                                             )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindEpisodeByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def LookForPeopleTables       ( self                                     ) :
    ##########################################################################
    KEY    = "Crowd"
    TABLEs = self . Tables      [ "PeopleView"                               ]
    ##########################################################################
    self   . CLI [ KEY ] [ "Tables" ] = TABLEs
    ##########################################################################
    self   . LOG                ( json . dumps  ( TABLEs )                   )
    ##########################################################################
    return
  ############################################################################
  def FindPeopleByName      ( self                                         ) :
    ##########################################################################
    KEY     = "Crowd"
    TABLEs  = self . CLI    [ KEY ] [ "Tables"                               ]
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    RELTAB  = TABLEs        [ "RelationPeople"                               ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    NAME    = self . CLI    [ KEY ] [ "Name"                                 ]
    UUID    = self . CLI    [ KEY ] [ "First"                                ]
    T1      = self . CLI    [ KEY ] [ "T1"                                   ]
    R       = self . CLI    [ KEY ] [ "Relation"                             ]
    ##########################################################################
    TOLWR   = True
    ##########################################################################
    if                      ( "Lower" in self . CLI [ KEY ]                ) :
      TOLWR = self . CLI    [ KEY ] [ "Lower"                                ]
    ##########################################################################
    HMSG    = self . Translations   [ f"CMD::{KEY}::Search:"                 ]
    MLOG    = f"{HMSG}{NAME}"
    self    . LOG           ( MLOG                                           )
    ##########################################################################
    LNAME   = NAME
    ##########################################################################
    if                      ( TOLWR                                        ) :
      LNAME = NAME . lower  (                                                )
    ##########################################################################
    ZNAME   = f"%{LNAME}%"
    ##########################################################################
    VQ      = f"""select `second` from {RELTAB}
                 where ( `t1` = {T1} )
                   and ( `relation` = {R} )
                   and ( `first` = {UUID} )"""
    ##########################################################################
    if                      ( TOLWR                                        ) :
      ########################################################################
      QQ    = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
      ########################################################################
    else                                                                     :
      ########################################################################
      QQ    = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( convert ( `name` using utf8 ) like %s )
                  group by `uuid` asc ;"""
    ##########################################################################
    QQ      = " " . join    ( QQ . split ( )                                 )
    ##########################################################################
    self    . LOG           ( QQ                                             )
    ##########################################################################
    DB      . QueryValues   ( QQ , ( ZNAME , )                               )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindPeopleByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def FindAllPeopleByName   ( self                                         ) :
    ##########################################################################
    KEY     = "Crowd"
    TABLEs  = self . CLI    [ KEY ] [ "Tables"                               ]
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    PEOTAB  = TABLEs        [ "People"                                       ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    NAME    = self . CLI    [ KEY ] [ "Name"                                 ]
    ##########################################################################
    TOLWR   = True
    ##########################################################################
    if                      ( "Lower" in self . CLI [ KEY ]                ) :
      TOLWR = self . CLI    [ KEY ] [ "Lower"                                ]
    ##########################################################################
    HMSG    = self . Translations   [ f"CMD::{KEY}::Search:"                 ]
    MLOG    = f"{HMSG}{NAME}"
    self    . LOG           ( MLOG                                           )
    ##########################################################################
    LNAME   = NAME
    ##########################################################################
    if                      ( TOLWR                                        ) :
      LNAME = NAME . lower  (                                                )
    ##########################################################################
    ZNAME   = f"%{LNAME}%"
    ##########################################################################
    VQ      = f"select `uuid` from {PEOTAB} where ( `used` > 0 )"
    ##########################################################################
    if                      ( TOLWR                                        ) :
      ########################################################################
      QQ    = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
      ########################################################################
    else                                                                     :
      ########################################################################
      QQ    = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( convert ( `name` using utf8 ) like %s )
                  group by `uuid` asc ;"""
    ##########################################################################
    QQ      = " " . join    ( QQ . split ( )                                 )
    ##########################################################################
    self    . LOG           ( QQ                                             )
    ##########################################################################
    DB      . QueryValues   ( QQ , ( ZNAME , )                               )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindPeopleByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def FindAllPeopleByNames  ( self                                         ) :
    ##########################################################################
    KEY     = "Crowd"
    TABLEs  = self . CLI    [ KEY ] [ "Tables"                               ]
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    NAMEs   = self . CLI    [ KEY ] [ "Names"                                ]
    ##########################################################################
    if                      ( len ( NAMEs ) <= 0                           ) :
      return
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    PEOTAB  = TABLEs        [ "People"                                       ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    TOLWR   = True
    ##########################################################################
    if                      ( "Lower" in self . CLI [ KEY ]                ) :
      TOLWR = self . CLI    [ KEY ] [ "Lower"                                ]
    ##########################################################################
    ALL     =               [                                                ]
    HMSG    = self . Translations   [ f"CMD::{KEY}::Search:"                 ]
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      MLOG  = f"{HMSG}{NAME}"
      self  . LOG           ( MLOG                                           )
      ########################################################################
      LNAME = NAME
      ########################################################################
      if                    ( TOLWR                                        ) :
        LNAME = NAME . lower (                                               )
      ########################################################################
      ZNAME = f"%{LNAME}%"
      ########################################################################
      VQ    = f"select `uuid` from {PEOTAB} where ( `used` > 0 )"
      ########################################################################
      if                    ( TOLWR                                        ) :
        ######################################################################
        QQ  = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
      ########################################################################
      else                                                                   :
        ######################################################################
        QQ  = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( convert ( `name` using utf8 ) like %s )
                  group by `uuid` asc ;"""
      ########################################################################
      QQ    = " " . join    ( QQ . split ( )                                 )
      ########################################################################
      self  . LOG           ( QQ                                             )
      ########################################################################
      DB    . QueryValues   ( QQ , ( ZNAME , )                               )
      ALLz  = DB . FetchAll (                                                )
      ########################################################################
      if                    ( ALLz in [ False , None ]                     ) :
        continue
      ########################################################################
      for UAID in ALLz                                                       :
        ######################################################################
        if                  ( UAID not in ALL                              ) :
          ####################################################################
          ALL . append      ( UAID                                           )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindPeopleByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def FindPeopleNoName      ( self                                         ) :
    ##########################################################################
    KEY     = "Crowd"
    TABLEs  = self . CLI    [ "Tables" ] [ "PeopleView"                      ]
    MAXE    = 30
    ##########################################################################
    if                      ( "MaxEmpty" in self . CLI [ KEY ]             ) :
      MAXE  = int           ( self . CLI [ KEY ] [ "MaxEmpty"              ] )
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    RELTAB  = TABLEs        [ "Relation"                                     ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    NAME    = self . CLI    [ KEY ] [ "Name"                                 ]
    UUID    = self . CLI    [ KEY ] [ "First"                                ]
    T1      = self . CLI    [ KEY ] [ "T1"                                   ]
    R       = self . CLI    [ KEY ] [ "Relation"                             ]
    ##########################################################################
    TOLWR   = True
    ##########################################################################
    if                      ( "Lower" in self . CLI [ KEY ]                ) :
      TOLWR = self . CLI    [ KEY ] [ "Lower"                                ]
    ##########################################################################
    HMSG    = self . Translations   [ f"CMD::{KEY}::FindNoname"              ]
    self    . LOG           ( HMSG                                           )
    ##########################################################################
    VQ      = f"""select `second` from {RELTAB}
                  where ( `t1` = {T1} )
                    and ( `relation` = {R} )
                    and ( `first` = {UUID} )"""
    ##########################################################################
    EQ      = f"""select `uuid` from {NAMTAB}
                  where ( `uuid` in ( {VQ} ) )
                    and ( length ( `name` ) > 0 )
                  group by `uuid`"""
    ##########################################################################
    QQ      = f"""select `second` from {RELTAB}
                  where ( `t1` = {T1} )
                    and ( `relation` = {R} )
                    and ( `first` = {UUID} )
                    and ( `second` not in ( {EQ} ) )
                  order by `second` asc
                  limit 0 , {MAXE} ;"""
    ##########################################################################
    QQ      = " " . join    ( QQ . split ( )                                 )
    ##########################################################################
    self    . LOG           ( QQ                                             )
    ##########################################################################
    DB      . Query         ( QQ                                             )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindPeopleByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def LookForGalleriesTables ( self                                        ) :
    ##########################################################################
    KEY    = "Galleries"
    TABLEs = self . Tables   [ "GalleriesView" ] [ "Subordination"           ]
    ##########################################################################
    self   . CLI [ KEY ] [ "Tables" ] = TABLEs
    ##########################################################################
    DB     = Connection      (                                               )
    ##########################################################################
    if                       ( not DB . ConnectTo ( self . DbConf )        ) :
      ########################################################################
      self . LOG             ( json . dumps  ( TABLEs )                      )
      ########################################################################
      return
    ##########################################################################
    DB     . Prepare         (                                               )
    ##########################################################################
    VARTAB = self . Tables   [ "VariantTables" ] [ "Variables"               ]
    ##########################################################################
    F      = self . CLI      [ KEY ] [ "First"                               ]
    T1     = self . CLI      [ KEY ] [ "T1"                                  ]
    R      = self . CLI      [ KEY ] [ "Relation"                            ]
    SCOPE  = f"GalleriesView-Subordination-{T1}-{R}"
    ##########################################################################
    TABLEs = self . ObtainsVariantTables ( DB                              , \
                                           VARTAB                          , \
                                           str ( F )                       , \
                                           T1                              , \
                                           SCOPE                           , \
                                           TABLEs                            )
    ##########################################################################
    self   . CLI [ KEY ] [ "Tables" ] = TABLEs
    ##########################################################################
    DB     . Close           (                                               )
    ##########################################################################
    self   . LOG             ( json . dumps  ( TABLEs )                      )
    ##########################################################################
    return
  ############################################################################
  def FindGalleriesByNameSqlSyntax ( self , QQ                             ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def FindGalleriesByName   ( self                                         ) :
    ##########################################################################
    KEY     = "Galleries"
    TABLEs  = self . CLI    [ "Tables" ] [ "GalleriesView"                   ]
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    ## NAMTAB  = TABLEs        [ "NamesVideo"                                   ]
    NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    RELTAB  = TABLEs        [ "Relation"                                     ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    NAME    = self . CLI    [ KEY ] [ "Name"                                 ]
    UUID    = self . CLI    [ KEY ] [ "First"                                ]
    T1      = self . CLI    [ KEY ] [ "T1"                                   ]
    R       = self . CLI    [ KEY ] [ "Relation"                             ]
    ##########################################################################
    HMSG    = self . Translations   [ f"CMD::{KEY}::Search:"                 ]
    MLOG    = f"{HMSG}{NAME}"
    self    . LOG           ( MLOG                                           )
    ##########################################################################
    LNAME   = NAME . lower  (                                                )
    ZNAME   = f"%{LNAME}%"
    ##########################################################################
    VQ      = f"""select `second` from {RELTAB}
                 where ( `t1` = {T1} )
                   and ( `relation` = {R} )
                   and ( `first` = {UUID} )"""
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
    ##########################################################################
    QQ      = " " . join    ( QQ . split ( )                                 )
    ##########################################################################
    self    . LOG           ( QQ                                             )
    ##########################################################################
    DB      . QueryValues   ( QQ , ( ZNAME , )                               )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    CNT     = len           ( UUIDs                                          )
    FMT     = self . Translations [ f"CMD::{KEY}::FoundTotal"                ]
    TMSG    = FMT  . format ( CNT                                            )
    MSG     = "\n" . join   ( UUIDz                                          )
    MSG     = f"{MSG}\n{TMSG}"
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindGalleriesByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def FindAllGalleriesByName ( self                                        ) :
    ##########################################################################
    KEY     = "Galleries"
    TABLEs  = self . CLI     [ "Tables" ] [ "GalleriesView"                  ]
    ##########################################################################
    self    . CLI            [ "Action" ] = ""
    self    . CLI            [ KEY ] [ "Found" ] = [                         ]
    ##########################################################################
    DB      = Connection     (                                               )
    ##########################################################################
    if                       ( not DB . ConnectTo ( self . DbConf )        ) :
      return
    ##########################################################################
    DB      . Prepare        (                                               )
    ##########################################################################
    GALTAB  = TABLEs         [ "Galleries"                                   ]
    NAMTAB  = TABLEs         [ "Names"                                       ]
    ##########################################################################
    LANGz   =                [                                               ]
    LANGs   = self . CLI     [ KEY ] [ "Languages"                           ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append         ( f"{L}"                                        )
    ##########################################################################
    LANGx   = " , " . join   ( LANGz                                         )
    ##########################################################################
    NAME    = self . CLI     [ KEY ] [ "Name"                                ]
    ##########################################################################
    HMSG    = self . Translations   [ f"CMD::{KEY}::Search:"                 ]
    MLOG    = f"{HMSG}{NAME}"
    self    . LOG            ( MLOG                                          )
    ##########################################################################
    LNAME   = NAME . lower   (                                               )
    ZNAME   = f"%{LNAME}%"
    ##########################################################################
    VQ      = f"""select `uuid` from {GALTAB}
                  where ( `used` > 0 )"""
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
    ##########################################################################
    QQ      = " " . join     ( QQ . split ( )                                )
    ##########################################################################
    self    . LOG            ( QQ                                            )
    ##########################################################################
    DB      . QueryValues    ( QQ , ( ZNAME , )                              )
    ALL     = DB . FetchAll  (                                               )
    ##########################################################################
    DB      . Close          (                                               )
    ##########################################################################
    if                       ( ALL in [ False , None ]                     ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =                [                                               ]
    UUIDz   =                [ MSG                                           ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int            ( R [ 0                                       ] )
      UUIDs . append         ( U                                             )
      UUIDz . append         ( f"{U}"                                        )
    ##########################################################################
    if                       ( len ( UUIDs ) <= 0                          ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG            ( MSG                                           )
      ########################################################################
      return
    ##########################################################################
    CNT     = len            ( UUIDs                                         )
    FMT     = self . Translations [ f"CMD::{KEY}::FoundTotal"                ]
    TMSG    = FMT  . format  ( CNT                                           )
    MSG     = "\n" . join    ( UUIDz                                         )
    MSG     = f"{MSG}\n{TMSG}"
    self    . LOG            ( MSG                                           )
    ##########################################################################
    self    . CLI            [ "Action" ] = "FindGalleriesByName"
    self    . CLI            [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run            (                                               )
    ##########################################################################
    return
  ############################################################################
  def FindAllGalleriesByNames ( self                                       ) :
    ##########################################################################
    KEY     = "Galleries"
    TABLEs  = self . CLI      [ "Tables" ] [ "GalleriesView"                 ]
    ##########################################################################
    self    . CLI             [ "Action" ] = ""
    self    . CLI             [ KEY ] [ "Found" ] = [                        ]
    ##########################################################################
    NAMEs   = self . CLI      [ KEY ] [ "Names"                              ]
    ##########################################################################
    if                        ( len ( NAMEs ) <= 0                         ) :
      return
    ##########################################################################
    DB      = Connection      (                                              )
    ##########################################################################
    if                        ( not DB . ConnectTo ( self . DbConf )       ) :
      return
    ##########################################################################
    DB      . Prepare         (                                              )
    ##########################################################################
    GALTAB  = TABLEs          [ "Galleries"                                  ]
    NAMTAB  = TABLEs          [ "Names"                                      ]
    ##########################################################################
    LANGz   =                 [                                              ]
    LANGs   = self . CLI      [ KEY ] [ "Languages"                          ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append          ( f"{L}"                                       )
    ##########################################################################
    LANGx   = " , " . join    ( LANGz                                        )
    ##########################################################################
    ALL     =                 [                                              ]
    HMSG    = self . Translations [ f"CMD::{KEY}::Search:"                   ]
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      MLOG  = f"{HMSG}{NAME}"
      self  . LOG             ( MLOG                                         )
      ########################################################################
      LNAME = NAME . lower    (                                              )
      ZNAME = f"%{LNAME}%"
      ########################################################################
      VQ    = f"""select `uuid` from {GALTAB}
                  where ( `used` > 0 )"""
      QQ    = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
      ########################################################################
      QQ    = " " . join     ( QQ . split ( )                                )
      ########################################################################
      self  . LOG            ( QQ                                            )
      ########################################################################
      DB    . QueryValues    ( QQ , ( ZNAME , )                              )
      ALLz  = DB . FetchAll  (                                               )
      ########################################################################
      if                     ( ALLz in [ False , None ]                    ) :
        continue
      ########################################################################
      for UAID in ALLz                                                       :
        ######################################################################
        if                   ( UAID not in ALL                             ) :
          ALL . append       ( UAID                                          )
    ##########################################################################
    DB      . Close          (                                               )
    ##########################################################################
    if                       ( ALL in [ False , None ]                     ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =                [                                               ]
    UUIDz   =                [ MSG                                           ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int            ( R [ 0                                       ] )
      UUIDs . append         ( U                                             )
      UUIDz . append         ( f"{U}"                                        )
    ##########################################################################
    if                       ( len ( UUIDs ) <= 0                          ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG            ( MSG                                           )
      ########################################################################
      return
    ##########################################################################
    CNT     = len            ( UUIDs                                         )
    FMT     = self . Translations [ f"CMD::{KEY}::FoundTotal"                ]
    TMSG    = FMT  . format  ( CNT                                           )
    MSG     = "\n" . join    ( UUIDz                                         )
    MSG     = f"{MSG}\n{TMSG}"
    self    . LOG            ( MSG                                           )
    ##########################################################################
    self    . CLI            [ "Action" ] = "FindGalleriesByName"
    self    . CLI            [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run            (                                               )
    ##########################################################################
    return
  ############################################################################
  def LookForOrganizationTables ( self                                     ) :
    ##########################################################################
    KEY    = "Organization"
    TABLEs = self . Tables      [ "OrganizationListings"                     ]
    ##########################################################################
    self   . CLI [ KEY ] [ "Tables" ] = TABLEs
    ##########################################################################
    self   . LOG                ( json . dumps  ( TABLEs )                   )
    ##########################################################################
    return
  ############################################################################
  def FindOrganizationByName ( self                                        ) :
    ##########################################################################
    KEY     = "Organization"
    TABLEs  = self . CLI    [ KEY ] [ "Tables"                               ]
    ##########################################################################
    self    . CLI           [ "Action" ] = ""
    self    . CLI           [ KEY ] [ "Found" ] = [                          ]
    ##########################################################################
    DB      = Connection    (                                                )
    ##########################################################################
    if                      ( not DB . ConnectTo ( self . DbConf )         ) :
      return
    ##########################################################################
    DB      . Prepare       (                                                )
    ##########################################################################
    NAMTAB  = TABLEs        [ "NamesEditing"                                 ]
    RELTAB  = TABLEs        [ "RelationPeople"                               ]
    ##########################################################################
    LANGz   =               [                                                ]
    LANGs   = self . CLI    [ KEY ] [ "Languages"                            ]
    ##########################################################################
    for L in LANGs                                                           :
      LANGz . append        ( f"{L}"                                         )
    ##########################################################################
    LANGx   = " , " . join  ( LANGz                                          )
    ##########################################################################
    NAME    = self . CLI    [ KEY ] [ "Name"                                 ]
    UUID    = self . CLI    [ KEY ] [ "First"                                ]
    T1      = self . CLI    [ KEY ] [ "T1"                                   ]
    R       = self . CLI    [ KEY ] [ "Relation"                             ]
    ##########################################################################
    HMSG    = self . Translations [ "CMD::Organization::Search:"             ]
    MLOG    = f"{HMSG}{NAME}"
    self    . LOG           ( MLOG                                           )
    ##########################################################################
    LNAME   = NAME . lower  (                                                )
    ZNAME   = f"%{LNAME}%"
    ##########################################################################
    VQ      = f"""select `second` from {RELTAB}
                 where ( `t1` = {T1} )
                   and ( `relation` = {R} )
                   and ( `first` = {UUID} )"""
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` in ( {LANGx} ) )
                    and ( `uuid` in ( {VQ} ) )
                    and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
    ##########################################################################
    QQ      = " " . join    ( QQ . split ( )                                 )
    ##########################################################################
    self    . LOG           ( QQ                                             )
    ##########################################################################
    DB      . QueryValues   ( QQ , ( ZNAME , )                               )
    ALL     = DB . FetchAll (                                                )
    ##########################################################################
    DB      . Close         (                                                )
    ##########################################################################
    if                      ( ALL in [ False , None ]                      ) :
      return
    ##########################################################################
    MSG     = self . Translations [ f"CMD::{KEY}::Found"                     ]
    UUIDs   =               [                                                ]
    UUIDz   =               [ MSG                                            ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      U     = int           ( R [ 0                                        ] )
      UUIDs . append        ( U                                              )
      UUIDz . append        ( f"{U}"                                         )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      ########################################################################
      MSG   = self . Translations [ f"CMD::{KEY}::NotFound"                  ]
      self  . LOG           ( MSG                                            )
      ########################################################################
      return
    ##########################################################################
    MSG     = "\n" . join   ( UUIDz                                          )
    self    . LOG           ( MSG                                            )
    ##########################################################################
    self    . CLI           [ "Action" ] = "FindOrganizationByName"
    self    . CLI           [ KEY ] [ "Found" ] = UUIDs
    ##########################################################################
    self    . Run           (                                                )
    ##########################################################################
    return
  ############################################################################
  def decodeCatalogue            ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Catalogue"                     ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    Scope  = self . CLI          [ "Scope"                                   ]
    ERR    = False
    ##########################################################################
    if                           ( T < 4                                   ) :
      ########################################################################
      ERR  = True
    ##########################################################################
    if                           ( not ERR                                 ) :
      ########################################################################
      if                         ( 19 != len ( sequences [ 3 ] )           ) :
        ######################################################################
        ERR = True
    ##########################################################################
    if                           ( ERR                                     ) :
      ########################################################################
      MSG  = self . Translations [ "CMD::Catalogue::Current"                 ]
      F    = self . CLI [ Scope ] [ "First"    ]
      T1   = self . CLI [ Scope ] [ "T1"       ]
      R    = self . CLI [ Scope ] [ "Relation" ]
      ########################################################################
      M    = f"{MSG}{F} ( Subordination : {R} , {T1} )"
      ########################################################################
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( False , False ,                           )
    ##########################################################################
    R      = int                 ( sequences [ 1                           ] )
    T1     = int                 ( sequences [ 2                           ] )
    F      = int                 ( sequences [ 3                           ] )
    ##########################################################################
    self . CLI [ Scope ] [ "First"    ] = F
    self . CLI [ Scope ] [ "T1"       ] = T1
    self . CLI [ Scope ] [ "Relation" ] = R
    ##########################################################################
    if                           ( Scope in [ "Episode" ]                  ) :
      ########################################################################
      threading . Thread         ( target = self . LookForEpisodeTables    ) \
                . start          (                                           )
    ##########################################################################
    if                           ( Scope in [ "Crowd" ]                    ) :
      ########################################################################
      threading . Thread         ( target = self . LookForPeopleTables     ) \
                . start          (                                           )
    ##########################################################################
    if                           ( Scope in [ "Galleries" ]                ) :
      ########################################################################
      threading . Thread         ( target = self . LookForGalleriesTables  ) \
                . start          (                                           )
    ##########################################################################
    if                           ( Scope in [ "Organization" ]             ) :
      ########################################################################
      threading . Thread         ( target = self.LookForOrganizationTables ) \
                . start          (                                           )
    ##########################################################################
    return                       ( True , False ,                            )
  ############################################################################
  def decodeDefault              ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Default"                       ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    Scope  = self . CLI          [ "Scope"                                   ]
    ERR    = False
    ##########################################################################
    if                           ( T < 4                                   ) :
      ########################################################################
      ERR  = True
    ##########################################################################
    if                           ( not ERR                                 ) :
      ########################################################################
      if                         ( 19 != len ( sequences [ 3 ] )           ) :
        ######################################################################
        ERR = True
    ##########################################################################
    if                           ( ERR                                     ) :
      return                     ( False , False ,                           )
    ##########################################################################
    R      = int                 ( sequences [ 1                           ] )
    T1     = int                 ( sequences [ 2                           ] )
    F      = int                 ( sequences [ 3                           ] )
    ##########################################################################
    JPC    =                     { "First"    : F                          , \
                                   "T1"       : T1                         , \
                                   "Relation" : R                            }
    self . CLI [ Scope ] [ "Default" ] = JPC
    ##########################################################################
    return                       ( True , False ,                            )
  ############################################################################
  def decodeSearchEpisode               ( self , cmd , sequences           ) :
    ##########################################################################
    T             = len                 (              sequences             )
    ##########################################################################
    if                                  ( T > 1                            ) :
      ########################################################################
      token       = sequences           [ 1                                  ]
      token       = token . lower       (                                    )
      ########################################################################
      EM          = self . Translations [ "CMD::Key::Empty"                  ]
      ########################################################################
      if                                ( token in EM                      ) :
        ######################################################################
        if                              ( T > 2                            ) :
          ####################################################################
          try                                                                :
            ##################################################################
            SS    = int                 ( sequences [ 2                    ] )
            self . CLI [ "Episode" ] [ "MaxEmpty" ] = SS
            ##################################################################
          except                                                             :
            pass
        ######################################################################
        threading . Thread              ( target = self . FindEpisodeNoName ) \
                  . start               (                                    )
        ######################################################################
        return
      ########################################################################
      EM          = self . Translations [ "CMD::Key::All"                    ]
      ########################################################################
      if                                ( token in EM                      ) :
        ######################################################################
        if                              ( T > 2                            ) :
          ####################################################################
          tkn     = sequences           [ 2                                  ]
          tkn     = tkn  . lower        (                                    )
          BM      = self . Translations [ "CMD::Key::By"                     ]
          ####################################################################
          if                            ( tkn in BM                        ) :
            ##################################################################
            if                          ( T > 3                            ) :
              ################################################################
              NN  = sequences           [ 3                                  ]
              NN  = NN   . lower        (                                    )
              NM  = self . Translations [ "CMD::Key::Names"                  ]
              ################################################################
              if                        ( NN in NM                         ) :
                ##############################################################
                threading . Thread      ( target = self . FindAllEpisodeByNames ) \
                          . start       (                                    )
                ##############################################################
                return
          ####################################################################
        ######################################################################
        ######################################################################
        ######################################################################
        ######################################################################
        threading . Thread              ( target = self . FindAllEpisodeByName ) \
                  . start               (                                    )
        ######################################################################
        return
    ##########################################################################
    threading     . Thread              ( target = self . FindEpisodeByName ) \
                  . start               (                                    )
    ##########################################################################
    return
  ############################################################################
  def decodeSearchCrowd                 ( self , cmd , sequences           ) :
    ##########################################################################
    T             = len                 (              sequences             )
    ##########################################################################
    if                                  ( T > 1                            ) :
      ########################################################################
      token       = sequences           [ 1                                  ]
      token       = token . lower       (                                    )
      ########################################################################
      EM          = self . Translations [ "CMD::Key::Empty"                  ]
      ########################################################################
      if                                ( token in EM                      ) :
        ######################################################################
        if                              ( T > 2                            ) :
          ####################################################################
          try                                                                :
            ##################################################################
            SS    = int                 ( sequences [ 2                    ] )
            self . CLI [ "Crowd" ] [ "MaxEmpty" ] = SS
            ##################################################################
          except                                                             :
            pass
        ######################################################################
        threading . Thread              ( target = self . FindPeopleNoName ) \
                  . start               (                                    )
        ######################################################################
        return
      ########################################################################
      EM          = self . Translations [ "CMD::Key::All"                    ]
      ########################################################################
      if                                ( token in EM                      ) :
        ######################################################################
        if                              ( T > 2                            ) :
          ####################################################################
          tkn     = sequences           [ 2                                  ]
          tkn     = tkn  . lower        (                                    )
          BM      = self . Translations [ "CMD::Key::By"                     ]
          ####################################################################
          if                            ( tkn in BM                        ) :
            ##################################################################
            if                          ( T > 3                            ) :
              ################################################################
              NN  = sequences           [ 3                                  ]
              NN  = NN   . lower        (                                    )
              NM  = self . Translations [ "CMD::Key::Names"                  ]
              ################################################################
              if                        ( NN in NM                         ) :
                ##############################################################
                threading . Thread      ( target = self . FindAllPeopleByNames ) \
                          . start       (                                    )
                ##############################################################
                return
          ####################################################################
        ######################################################################
        ######################################################################
        ######################################################################
        ######################################################################
        threading . Thread              ( target = self . FindAllPeopleByName ) \
                  . start               (                                    )
        ######################################################################
        return
    ##########################################################################
    threading     . Thread              ( target = self . FindPeopleByName ) \
                  . start               (                                    )
    ##########################################################################
    return
  ############################################################################
  def decodeSearchGalleries             ( self , cmd , sequences           ) :
    ##########################################################################
    T             = len                 (              sequences             )
    ##########################################################################
    if                                  ( T > 1                            ) :
      ########################################################################
      token       = sequences           [ 1                                  ]
      token       = token . lower       (                                    )
      ########################################################################
      EM          = self . Translations [ "CMD::Key::Empty"                  ]
      ########################################################################
      if                                ( token in EM                      ) :
        ######################################################################
        if                              ( T > 2                            ) :
          ####################################################################
          try                                                                :
            ##################################################################
            SS    = int                 ( sequences [ 2                    ] )
            self . CLI [ "Galleries" ] [ "MaxEmpty" ] = SS
            ##################################################################
          except                                                             :
            pass
        ######################################################################
        ## threading . Thread              ( target = self . FindGalleriesNoPicture ) \
        ##           . start               (                                    )
        ######################################################################
        return
      ########################################################################
      EM          = self . Translations [ "CMD::Key::All"                    ]
      ########################################################################
      if                                ( token in EM                      ) :
        ######################################################################
        if                              ( T > 2                            ) :
          ####################################################################
          tkn     = sequences           [ 2                                  ]
          tkn     = tkn  . lower        (                                    )
          BM      = self . Translations [ "CMD::Key::By"                     ]
          ####################################################################
          if                            ( tkn in BM                        ) :
            ##################################################################
            if                          ( T > 3                            ) :
              ################################################################
              NN  = sequences           [ 3                                  ]
              NN  = NN   . lower        (                                    )
              NM  = self . Translations [ "CMD::Key::Names"                  ]
              ################################################################
              if                        ( NN in NM                         ) :
                ##############################################################
                threading . Thread      ( target = self . FindAllGalleriesByNames ) \
                          . start       (                                    )
                ##############################################################
                return
          ####################################################################
        ######################################################################
        threading . Thread              ( target = self . FindAllGalleriesByName ) \
                  . start               (                                    )
        ######################################################################
        return
      ########################################################################
      EM          = self . Translations [ "CMD::Key::Groups"                 ]
      ########################################################################
      if                                ( token in EM                      ) :
        ######################################################################
        ######################################################################
        ## threading . Thread              ( target = self . FindGalleriesNoPicture ) \
        ##           . start               (                                    )
        ######################################################################
        return
    ##########################################################################
    threading     . Thread              ( target = self . FindGalleriesByName ) \
                  . start               (                                    )
    ##########################################################################
    return
  ############################################################################
  def decodeSearch                 ( self , cmd , sequences                ) :
    ##########################################################################
    TM     = self . Translations   [ "CMD::Key::Search"                      ]
    T      = len                   ( sequences                               )
    anchor = sequences             [ 0                                       ]
    anchor = anchor . lower        (                                         )
    ##########################################################################
    if                             ( anchor not in TM                      ) :
      return                       ( False , False ,                         )
    ##########################################################################
    Scope  = self . CLI            [ "Scope"                                 ]
    ##########################################################################
    if                             ( Scope in [ "Episode"                ] ) :
      ########################################################################
      self . decodeSearchEpisode   (        cmd , sequences                  )
      ########################################################################
      return                       ( True , False ,                          )
    ##########################################################################
    if                             ( Scope in [ "Crowd"                  ] ) :
      ########################################################################
      self . decodeSearchCrowd     (        cmd , sequences                  )
      ########################################################################
      return                       ( True , False ,                          )
    ##########################################################################
    if                             ( Scope in [ "Galleries"              ] ) :
      ########################################################################
      self . decodeSearchGalleries (      cmd , sequences                    )
      ########################################################################
      return                       ( True , False ,                          )
    ##########################################################################
    if                             ( Scope in [ "Organization"           ] ) :
      ########################################################################
      threading . Thread           ( target = self.FindOrganizationByName  ) \
                . start            (                                         )
      ########################################################################
      return                       ( True , False ,                          )
    ##########################################################################
    return                         ( True , False ,                          )
  ############################################################################
  def decodeUuid                 ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Uuid"                          ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def decodeUuids                ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Uuids"                         ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def decodeClipboard            ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Clipboard"                     ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def decodeRun                  ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Run"                           ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    if                           ( T < 2                                   ) :
      return                     ( False , False ,                           )
    ##########################################################################
    anchor = sequences           [ 1                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( "organizenamesbywestern" == anchor      ) :
      ########################################################################
      threading . Thread         ( target = self . OrganizeNamesByWestern  ) \
                . start          (                                           )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    if                           ( "parkpeoplevideos"       == anchor      ) :
      ########################################################################
      threading . Thread         ( target = self . ParkPeopleVideos        ) \
                . start          (                                           )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    if                           ( "parkpicturedescriptions" == anchor     ) :
      ########################################################################
      threading . Thread         ( target = self . ParkPictureDescriptions ) \
                . start          (                                           )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    if                           ( "movepicturedescriptions" == anchor     ) :
      ########################################################################
      threading . Thread         ( target = self . MovePictureDescriptions ) \
                . start          (                                           )
      ########################################################################
      return                     ( True  , False ,                           )
    ##########################################################################
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def decodeClear                ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Clear"                         ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    if                           ( T < 2                                   ) :
      return                     ( False , False ,                           )
    ##########################################################################
    anchor = sequences           [ 1                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Editor"                        ]
    ##########################################################################
    if                           ( anchor in TM                            ) :
      ########################################################################
      self . CLI                 [ "Action" ] = "ClearCommandEditor"
      ########################################################################
      return                     ( True  , True  ,                           )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    if                           ( self . hasScope (                     ) ) :
      return                     ( False , False ,                           )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  def decodeGrab                 ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Take"                          ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    if                           ( T < 2                                   ) :
      return                     ( False , False ,                           )
    ##########################################################################
    Scope  = self . CLI          [ "Scope"                                   ]
    ##########################################################################
    anchor = sequences           [ 1                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    KM     = self . Translations [ "CMD::Key::Names"                         ]
    ##########################################################################
    if                           ( anchor     in KM                        ) :
      ########################################################################
      if                         ( T < 3                                   ) :
        return                   ( False , False ,                           )
      ########################################################################
      vv   = sequences           [ 2                                         ]
      zz   = vv . lower          (                                           )
      ########################################################################
      BM   = self . Translations [ "CMD::Key::From"                          ]
      EM   = self . Translations [ "CMD::Key::Extract"                       ]
      ########################################################################
      if                         ( ( zz not in BM ) and ( zz not in EM )   ) :
        return                   ( False , False ,                           )
      ########################################################################
      if                         ( T < 4                                   ) :
        return                   ( False , False ,                           )
      ########################################################################
      vv   = sequences           [ 3                                         ]
      vv   = vv . lower          (                                           )
      ########################################################################
      CM   = self . Translations [ "CMD::Key::Clipboard"                     ]
      ########################################################################
      if                         ( vv     in CM                            ) :
        ######################################################################
        T  = self . GetClipboard (                                           )
        ######################################################################
        if                       ( zz in BM                                ) :
          ####################################################################
          LX = self . GetLineNames     ( T                                   )
          ####################################################################
        elif                     ( zz in EM                                ) :
          ####################################################################
          LX = self . ExtractLineNames ( T                                   )
        ######################################################################
        self . CLI [ Scope ] [ "Names" ] = LX
        ######################################################################
        self . LOG               ( "\n" . join ( LX )                        )
        ######################################################################
        return                   ( True  , False ,                           )
      ########################################################################
      return                     ( False , False ,                           )
    ##########################################################################
    return                       ( False , False ,                           )
  ############################################################################
  def decodeFilename             ( self , cmd , sequences                  ) :
    ##########################################################################
    TM     = self . Translations [ "CMD::Key::Filename"                      ]
    T      = len                 ( sequences                                 )
    anchor = sequences           [ 0                                         ]
    anchor = anchor . lower      (                                           )
    ##########################################################################
    if                           ( anchor not in TM                        ) :
      return                     ( False , False ,                           )
    ##########################################################################
    Scope  = self . CLI          [ "Scope"                                   ]
    ##########################################################################
    if                           ( T < 2                                   ) :
      ########################################################################
      if                         ( "Filename" not in self . CLI [ Scope ]  ) :
        return                   ( False , False ,                           )
      ########################################################################
      MSG  = self . Translations [ "CMD::Filename::Current"                  ]
      NAME = self . CLI [ Scope ] [ "Filename"                               ]
      M    = f"{MSG}{NAME}"
      ########################################################################
      self . LOG                 ( M                                         )
      ########################################################################
      return                     ( False , False ,                           )
    ##########################################################################
    FNAME  = self . StripCommand (        cmd , sequences [ 0 ]              )
    ##########################################################################
    if                           ( len ( NAME ) <= 0                       ) :
      return
    ##########################################################################
    self   . CLI [ Scope ] [ "Filename" ] = FNAME
    ##########################################################################
    MSG    = self . Translations [ "CMD::Filename::Assign"                   ]
    M      = f"{MSG}{NAME}"
    self   . LOG                 ( M                                         )
    ##########################################################################
    return                       ( True  , False ,                           )
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def Decode                       ( self , cmd , sequences                ) :
    ##########################################################################
    M , A = self . decodeClear     (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeScope     (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeUuid      (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeUuids     (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeClipboard (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeRun       (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    if                             ( not self . hasScope (               ) ) :
      return
    ##########################################################################
    M , A = self . decodeName      (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeNames     (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeLanguages (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeLocality  (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeCatalogue (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeDefault   (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeSearch    (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeGrab      (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    M , A = self . decodeFilename  (        cmd , sequences                  )
    ##########################################################################
    if                             ( M                                     ) :
      return A
    ##########################################################################
    return False
  ############################################################################
  def PasteIn ( self , cmd , sequences                                     ) :
    ##########################################################################
    ##########################################################################
    return False
  ############################################################################
  def Interpret             ( self , cmd                                   ) :
    ##########################################################################
    C = self . PurgeCommand (        cmd                                     )
    ##########################################################################
    if                      ( len ( C ) <= 0                               ) :
      return False
    ##########################################################################
    L = C . split           ( " "                                            )
    T = len                 ( L                                              )
    ##########################################################################
    if                      ( T <= 0                                       ) :
      return False
    ##########################################################################
    return self . Decode    ( C , L                                          )
  ############################################################################
  def PasteInto             ( self , cmd                                   ) :
    ##########################################################################
    C = self . PurgeCommand (        cmd                                     )
    ##########################################################################
    if                      ( len ( C ) <= 0                               ) :
      return False
    ##########################################################################
    L = C . split           ( " "                                            )
    T = len                 ( L                                              )
    ##########################################################################
    if                      ( T <= 0                                       ) :
      return False
    ##########################################################################
    return self . PasteIn   ( C , L                                          )
##############################################################################
