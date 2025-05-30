# -*- coding: utf-8 -*-
##############################################################################
## 頭髮
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
HAIRSREL        = "`affiliations`.`relations_people_0009`"
HPICREL         = "`affiliations`.`relations_pictures_0009`"
HAIRSNAM        = "`appellations`.`names_commons_0014`"
HAIRSNOTE       = "`notez`.`notes_commons_0027`"
HAIRSPARAM      = "`cios`.`parameters`"
HairsShortType  = 20
HairsLongType   = 1100000000000000020
HairsTypeName   = "Hairs"
##############################################################################
HairColorRanges =                                                          { \
  "Brown"       : ( [  10 ,  50 ,  50 ] , [  30 , 255 , 150 ]            ) , \
  "Blue"        : ( [  90 ,  50 ,  50 ] , [ 130 , 255 , 255 ]            ) , \
  "Green"       : ( [  40 ,  50 ,  50 ] , [  80 , 255 , 255 ]            ) , \
  "Gray"        : ( [   0 ,   0 ,  50 ] , [ 179 ,  50 , 150 ]            )   }
##############################################################################
class Hairs              ( Columns                                         ) :
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
    self . Id         =  -1
    self . Uuid       =   0
    self . HType      =   1
    self . Name       =  ""
    self . Formula    =   0
    self . Parameter  = 1.0
    self . R          =   0
    self . G          =   0
    self . B          =   0
    self . ltime      =   0
    ##########################################################################
    self . PeopleUuid =   0
    ##########################################################################
    return
  ############################################################################
  def assign ( self , item                                                 ) :
    ##########################################################################
    self . Columns   = item . Columns
    self . Id        = item . Id
    self . Uuid      = item . Uuid
    self . HType     = item . Type
    self . Name      = item . Name
    self . Formula   = item . Formula
    self . Parameter = item . Parameter
    self . R         = item . R
    self . G         = item . G
    self . B         = item . B
    self . ltime     = item . ltime
    ##########################################################################
    return
  ############################################################################
  def set            ( self , item , value                                 ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"        == a                                    ) :
      self . Id        = value
    ##########################################################################
    elif             ( "uuid"      == a                                    ) :
      self . Uuid      = value
    ##########################################################################
    elif             ( "type"      == a                                    ) :
      self . HType     = value
    ##########################################################################
    elif             ( "name"      == a                                    ) :
      self . Name      = value
    ##########################################################################
    elif             ( "formula"   == a                                    ) :
      self . Formula   = value
    ##########################################################################
    elif             ( "parameter" == a                                    ) :
      self . Parameter = value
    ##########################################################################
    elif             ( "r"         == a                                    ) :
      self . R         = value
    ##########################################################################
    elif             ( "g"         == a                                    ) :
      self . G         = value
    ##########################################################################
    elif             ( "b"         == a                                    ) :
      self . B         = value
    ##########################################################################
    elif             ( "ltime"     == a                                    ) :
      self . ltime     = value
    ##########################################################################
    return
  ############################################################################
  def get            ( self , item                                         ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"        == a                                    ) :
      return self . Id
    ##########################################################################
    if               ( "uuid"      == a                                    ) :
      return self . Uuid
    ##########################################################################
    if               ( "type"      == a                                    ) :
      return self . HType
    ##########################################################################
    if               ( "name"      == a                                    ) :
      return self . Name
    ##########################################################################
    if               ( "formula"   == a                                    ) :
      return self . Formula
    ##########################################################################
    if               ( "parameter" == a                                    ) :
      return self . Parameter
    ##########################################################################
    if               ( "r"         == a                                    ) :
      return self . R
    ##########################################################################
    if               ( "g"         == a                                    ) :
      return self . G
    ##########################################################################
    if               ( "b"         == a                                    ) :
      return self . B
    ##########################################################################
    if               ( "ltime"     == a                                    ) :
      return self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems        ( self                                             ) :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "type"                                                          ,
             "name"                                                          ,
             "formula"                                                       ,
             "parameter"                                                     ,
             "r"                                                             ,
             "g"                                                             ,
             "b"                                                             ,
             "ltime"                                                         ]
  ############################################################################
  def pair              ( self , item                                      ) :
    v = self . get      (        item                                        )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems        ( self                                             ) :
    return [ "type"                                                          ,
             "name"                                                          ,
             "formula"                                                       ,
             "parameter"                                                     ,
             "r"                                                             ,
             "g"                                                             ,
             "b"                                                             ]
  ############################################################################
  def toJson ( self                                                        ) :
    return   { "Id"        : self . Id                                     , \
               "Uuid"      : self . Uuid                                   , \
               "Type"      : self . HType                                  , \
               "Name"      : self . Name                                   , \
               "Formula"   : self . Formula                                , \
               "Parameter" : self . Parameter                              , \
               "R"         : self . R                                      , \
               "G"         : self . G                                      , \
               "B"         : self . B                                        }
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
  def QuerySyntax ( self , TABLE , ORDER                                   ) :
    return f"select `uuid` from {TABLE} order by `id` {ORDER} ;"
  ############################################################################
  ## 取得所有頭髮顏色細節
  ############################################################################
  def GetHairListings             ( self , DB , TABLE , UUIDs , NAMEs      ) :
    ##########################################################################
    LISTs   =                     [                                          ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select `id`,`name`,`formula`,`parameter`,`R`,`G`,`B` from {TABLE}
                 where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join          ( QQ . split (                           ) )
      DB    . Query               ( QQ                                       )
      RR    = DB . FetchOne       (                                          )
      ########################################################################
      if                          ( RR in [ False , None ]                 ) :
        continue
      ########################################################################
      if                          ( len ( RR ) != 7                        ) :
        continue
      ########################################################################
      ID    = int                 ( RR [ 0                                 ] )
      NA    = self . assureString ( RR [ 1                                 ] )
      FM    = int                 ( RR [ 2                                 ] )
      PA    = float               ( RR [ 3                                 ] )
      R     = int                 ( RR [ 4                                 ] )
      G     = int                 ( RR [ 5                                 ] )
      B     = int                 ( RR [ 6                                 ] )
      ########################################################################
      J     =                     { "Id"         : ID                      , \
                                    "Uuid"       : UUID                    , \
                                    "Name"       : NAMEs [ UUID ]          , \
                                    "Identifier" : NA                      , \
                                    "Formula"    : FM                      , \
                                    "Parameter"  : PA                      , \
                                    "R"          : R                       , \
                                    "G"          : G                       , \
                                    "B"          : B                         }
      LISTs . append              ( J                                        )
    ##########################################################################
    return LISTs
  ############################################################################
  ## 計算頭髮顏色所擁有的人物族群
  ############################################################################
  def CountCrowds            ( self , DB , TABLE , RELATE , UUID           ) :
    ##########################################################################
    global HairsTypeName
    ##########################################################################
    REL        = Relation    (                                               )
    REL        . set         ( "first" , UUID                                )
    REL        . setT1       ( HairsTypeName                                 )
    REL        . setT2       ( "People"                                      )
    REL        . setRelation ( RELATE                                        )
    ##########################################################################
    return REL . CountSecond ( DB , TABLE                                    )
  ############################################################################
  def CountDefaultCrowds      ( self , DB ,            RELATE , UUID       ) :
    ##########################################################################
    global HAIRSREL
    ##########################################################################
    return self . CountCrowds (        DB , HAIRSREL , RELATE , UUID         )
  ############################################################################
  ## 人物加入頭髮顏色族群
  ############################################################################
  def PeopleJoinHair  ( self , DB , TABLE , RELATE , UUID , UUIDs          ) :
    ##########################################################################
    global HairsTypeName
    ##########################################################################
    REL = Relation    (                                                      )
    REL . set         ( "first" , UUID                                       )
    REL . setT1       ( HairsTypeName                                        )
    REL . setT2       ( "People"                                             )
    REL . setRelation ( RELATE                                               )
    REL . Joins       ( DB , TABLE , UUIDs                                   )
    ##########################################################################
    return
  ############################################################################
  def PeopleJoinDefaultHair ( self , DB , RELATE , UUID , UUIDs            ) :
    ##########################################################################
    global HAIRSREL
    ##########################################################################
    self . PeopleJoinHair   ( DB , HAIRSREL , RELATE , UUID , UUIDs          )
    ##########################################################################
    return
  ############################################################################
  def FetchPeopleHairColors  ( self , DB , RELATED                         ) :
    ##########################################################################
    global HairsTypeName
    global HAIRSREL
    ##########################################################################
    REL        = Relation    (                                               )
    REL        . set         ( "second" , self . PeopleUuid                  )
    REL        . setT1       ( HairsTypeName                                 )
    REL        . setT2       ( "People"                                      )
    REL        . setRelation ( RELATED                                       )
    ##########################################################################
    return REL . GetOwners   ( DB       , HAIRSREL                           )
  ############################################################################
  def LockRelationTable ( self , DB                                        ) :
    ##########################################################################
    global HAIRSREL
    ##########################################################################
    DB . LockWrites     ( [ HAIRSREL                                       ] )
    ##########################################################################
    return
  ############################################################################
  def AssignPeopleHairColor ( self , DB , SEID , State , RELATED           ) :
    ##########################################################################
    global HairsTypeName
    global HAIRSREL
    ##########################################################################
    REL   = Relation        (                                                )
    REL   . set             ( "first"  , SEID                                )
    REL   . set             ( "second" , self . PeopleUuid                   )
    REL   . setT1           ( HairsTypeName                                  )
    REL   . setT2           ( "People"                                       )
    REL   . setRelation     ( RELATED                                        )
    ##########################################################################
    if                      ( State                                        ) :
      ########################################################################
      REL . Join            ( DB ,           HAIRSREL                        )
      ########################################################################
    else                                                                     :
      ########################################################################
      DB  . Query           ( REL . Delete ( HAIRSREL                      ) )
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
