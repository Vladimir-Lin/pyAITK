# -*- coding: utf-8 -*-
##############################################################################
## 種族
##############################################################################
import os
import sys
import getopt
import time
import datetime
import requests
import threading
##############################################################################
import mysql . connector
from   mysql . connector                   import Error
##############################################################################
import AITK
from   AITK  . Database   . Query          import Query
from   AITK  . Database   . Connection     import Connection
from   AITK  . Database   . Pair           import Pair
from   AITK  . Database   . Columns        import Columns
##############################################################################
from   AITK  . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
from   AITK  . Essentials . Relation       import Relation       as Relation
##############################################################################
RACEREL       = "`affiliations`.`relations_people`"
RACENAM       = "`appellations`.`names_commons_0019`"
RACEPARAM     = "`cios`.`parameters`"
RaceShortType = 34
RaceLongType  = 1100000000000000034
RaceTypeName  = "Race"
##############################################################################
class Races              ( Columns                                         ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    self      . Clear    (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Clear             ( self                                             ) :
    ##########################################################################
    self . Columns    = [                                                    ]
    self . Id         = -1
    self . Uuid       =  0
    self . Used       =  0
    self . Name       =  ""
    self . Comment    =  ""
    self . ltime      =  0
    ##########################################################################
    self . PeopleUuid =  0
    ##########################################################################
    return
  ############################################################################
  def assign ( self , item                                                 ) :
    ##########################################################################
    self . Columns = item . Columns
    self . Id      = item . Id
    self . Uuid    = item . Uuid
    self . Used    = item . Used
    self . Name    = item . Name
    self . Comment = item . Comment
    self . ltime   = item . ltime
    ##########################################################################
    return
  ############################################################################
  def set            ( self , item , value                                 ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"      == a                                      ) :
      self . Id      = value
    ##########################################################################
    elif             ( "uuid"    == a                                      ) :
      self . Uuid    = value
    ##########################################################################
    elif             ( "used"    == a                                      ) :
      self . Used    = value
    ##########################################################################
    elif             ( "name"    == a                                      ) :
      self . Name    = value
    ##########################################################################
    elif             ( "comment" == a                                      ) :
      self . Comment = value
    ##########################################################################
    elif             ( "ltime"   == a                                      ) :
      self . ltime   = value
    ##########################################################################
    return
  ############################################################################
  def get            ( self , item                                         ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"      == a                                      ) :
      return self . Id
    ##########################################################################
    if               ( "uuid"    == a                                      ) :
      return self . Uuid
    ##########################################################################
    if               ( "used"    == a                                      ) :
      return self . Used
    ##########################################################################
    if               ( "name"    == a                                      ) :
      return self . Name
    ##########################################################################
    if               ( "comment" == a                                      ) :
      return self . Comment
    ##########################################################################
    if               ( "ltime"   == a                                      ) :
      return self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems        ( self                                             ) :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "used"                                                          ,
             "name"                                                          ,
             "comment"                                                       ,
             "ltime"                                                         ]
  ############################################################################
  def pair              ( self , item                                      ) :
    v = self . get      (        item                                        )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems        ( self                                             ) :
    return [ "used"                                                          ,
             "name"                                                          ,
             "comment"                                                       ]
  ############################################################################
  def toJson ( self                                                        ) :
    return   { "Id"      : self . Id                                       , \
               "Uuid"    : self . Uuid                                     , \
               "Used"    : self . Used                                     , \
               "Name"    : self . Name                                     , \
               "Comment" : self . Comment                                    }
  ############################################################################
  def assureString     ( self , pb                                         ) :
    ##########################################################################
    BB   = pb
    ##########################################################################
    try                                                                      :
      BB = BB . decode ( "utf-8"                                             )
    except                                                                   :
      pass
    ##########################################################################
    return BB
  ############################################################################
  def setPeople ( self , uuid                                              ) :
    ##########################################################################
    self . PeopleUuid = uuid
    ##########################################################################
    return
  ############################################################################
  ## 查詢語法
  ############################################################################
  def QuerySyntax     ( self                                               , \
                        TABLE                                              , \
                        UsedOptions                                        , \
                        ORDER                                              , \
                        START                                              , \
                        AMOUNT                                             ) :
    ##########################################################################
    UQ = " , " . join ( str(x) for x in UsedOptions                          )
    QQ = f"""select `uuid` from {TABLE}
             where ( `used` in ( {UQ} ) )
             order by `id` {ORDER}
             limit {START} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join ( QQ . split (                                       ) )
  ############################################################################
  def QuerySyntaxAll  ( self                                               , \
                        TABLE                                              , \
                        UsedOptions                                        , \
                        ORDER                                              ) :
    ##########################################################################
    UQ = " , " . join ( str(x) for x in UsedOptions                          )
    QQ = f"""select `uuid` from {TABLE}
             where ( `used` in ( {UQ} ) )
             order by `id` {ORDER} ;"""
    ##########################################################################
    return " " . join ( QQ . split (                                       ) )
  ############################################################################
  def CountOptions     ( self , DB , TABLE , UsedOptions                   ) :
    ##########################################################################
    UQ = " , " . join  ( str(x) for x in UsedOptions                         )
    QQ = f"""select count(*) from {TABLE} where ( `used` in ( {UQ} ) ) ;"""
    ##########################################################################
    DB . Query         ( QQ                                                  )
    RR = DB . FetchOne (                                                     )
    ##########################################################################
    if                 ( RR in [ False , None                            ] ) :
      return 0
    ##########################################################################
    if                 ( len ( RR ) <= 0                                   ) :
      return 0
    ##########################################################################
    return int         ( RR [ 0                                            ] )
  ############################################################################
  def FetchUuids            ( self , DB , TABLE , UsedOptions              ) :
    ##########################################################################
    UQ = " , " . join       ( str(x) for x in UsedOptions                    )
    QQ = f"""select `uuid` from {TABLE}
             where ( `used` in ( {UQ} ) )
             order by `id` asc ;"""
    ##########################################################################
    return DB . ObtainUuids ( " " . join ( QQ . split ( ) ) , 0              )
  ############################################################################
  ## 取得種族辨識字
  ############################################################################
  def GetIdentifiers           ( self , DB , TABLE , UUIDs                 ) :
    ##########################################################################
    IDFs =                     {                                             }
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ = f"select `name` from {TABLE} where ( `uuid` = {UUID} ) ;"
      NN = DB   . GetOne       ( QQ , ""                                     )
      NA = self . assureString ( NN                                          )
      ########################################################################
      IDFs [ UUID ] = NA
    ##########################################################################
    return IDFs
  ############################################################################
  ## 更新種族辨識字
  ############################################################################
  def UpdateIdentifier ( self , DB , TABLE , UUID , NAME                   ) :
    ##########################################################################
    QQ = f"""update {TABLE}
             set `name` = '{NAME}'
             where ( `uuid` = {UUID} ) ;"""
    ##########################################################################
    DB . Query         ( " " . join ( QQ . split (                       ) ) )
    ##########################################################################
    return
  ############################################################################
  ## 種族所擁有的人物族群
  ############################################################################
  def CountCrowds            ( self , DB , TABLE , RELATE , UUID           ) :
    ##########################################################################
    global RaceTypeName
    ##########################################################################
    REL        = Relation    (                                               )
    REL        . set         ( "first" , UUID                                )
    REL        . setT1       ( RaceTypeName                                  )
    REL        . setT2       ( "People"                                      )
    REL        . setRelation ( RELATE                                        )
    ##########################################################################
    return REL . CountSecond ( DB , TABLE                                    )
  ############################################################################
  def CountDefaultCrowds      ( self , DB ,           RELATE , UUID        ) :
    ##########################################################################
    global RACEREL
    ##########################################################################
    return self . CountCrowds (        DB , RACEREL , RELATE , UUID          )
  ############################################################################
  ## 人物加入種族
  ############################################################################
  def PeopleJoinRace  ( self , DB , TABLE , RELATE , UUID , UUIDs          ) :
    ##########################################################################
    global RaceTypeName
    ##########################################################################
    REL = Relation    (                                                      )
    REL . set         ( "first" , UUID                                       )
    REL . setT1       ( RaceTypeName                                         )
    REL . setT2       ( "People"                                             )
    REL . setRelation ( RELATE                                               )
    REL . Joins       ( DB , TABLE , UUIDs                                   )
    ##########################################################################
    return
  ############################################################################
  def PeopleJoinDefaultRace ( self , DB , RELATE , UUID , UUIDs            ) :
    ##########################################################################
    global RACEREL
    ##########################################################################
    self . PeopleJoinRace   ( DB , RACEREL , RELATE , UUID , UUIDs           )
    ##########################################################################
    return
  ############################################################################
  def FetchPeopleRaces       ( self , DB , RELATED                         ) :
    ##########################################################################
    global RaceTypeName
    global RACEREL
    ##########################################################################
    REL        = Relation    (                                               )
    REL        . set         ( "second" , self . PeopleUuid                  )
    REL        . setT1       ( RaceTypeName                                  )
    REL        . setT2       ( "People"                                      )
    REL        . setRelation ( RELATED                                       )
    ##########################################################################
    return REL . GetOwners   ( DB       , RACEREL                            )
  ############################################################################
  def LockRelationTable ( self , DB                                        ) :
    ##########################################################################
    global RACEREL
    ##########################################################################
    DB . LockWrites     ( [ RACEREL                                        ] )
    ##########################################################################
    return
  ############################################################################
  def AssignPeopleRace  ( self , DB , SEID , State , RELATED               ) :
    ##########################################################################
    global RaceTypeName
    global RACEREL
    ##########################################################################
    REL   = Relation    (                                                    )
    REL   . set         ( "first"  , SEID                                    )
    REL   . set         ( "second" , self . PeopleUuid                       )
    REL   . setT1       ( RaceTypeName                                       )
    REL   . setT2       ( "People"                                           )
    REL   . setRelation ( RELATED                                            )
    ##########################################################################
    if                  ( State                                            ) :
      ########################################################################
      REL . Join        ( DB ,           RACEREL                             )
      ########################################################################
    else                                                                     :
      ########################################################################
      DB  . Query       ( REL . Delete ( RACEREL                           ) )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
