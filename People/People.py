# -*- coding: utf-8 -*-
##############################################################################
## 人物
##############################################################################
import os
import sys
import time
import datetime
import threading
import json
import codecs
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
##############################################################################
from   AITK  . Essentials . Relation       import Relation       as Relation
##############################################################################
from   AITK  . Networking . WebPage        import WebPage        as WebPage
from   AITK  . Pictures   . Picture        import Picture        as Picture
##############################################################################
class People          (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    ##########################################################################
    self . Uuid     = 0
    self . Settings = {                                                      }
    self . Tables   = {                                                      }
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    return
  ############################################################################
  ## 新增人物
  ############################################################################
  def NewPeople              ( self , DB                                   ) :
    ##########################################################################
    HEAD   = self . Settings [ "Head"                                        ]
    PEOTAB = self . Tables   [ "People"                                      ]
    ##########################################################################
    UUID   = DB . LastUuid   ( PEOTAB , "uuid" , HEAD                        )
    ############################################################################
    QQ     = f"""insert into {PEOTAB}
                 ( `uuid`,`used`,`state` )
                 values
                 ( {UUID} , 1 , 0 ) ;"""
    QQ     = " " . join      ( QQ . split ( )                                )
    DB     . Query           ( QQ                                            )
    ##########################################################################
    return UUID
  ############################################################################
  ## 搜尋人物名稱
  ############################################################################
  def PeopleByName         ( self , DB , Name , Locality                   ) :
    ##########################################################################
    PEOTAB = self . Tables [ "People"                                        ]
    NAMTAB = self . Tables [ "Names"                                         ]
    ##########################################################################
    PQ     = f"select `uuid` from {PEOTAB} where ( `used` = 1 )"
    QQ     = f"""select `uuid` from {NAMTAB}
                    where ( `locality` = {Locality} )
                      and ( `name` = %s )
                      and ( `uuid` in ( {PQ} ) )
                      group by `uuid` ;"""
    ##########################################################################
    QQ     = " " . join    ( QQ . split ( )                                  )
    DB     . QueryValues   ( QQ , ( Name , )                                 )
    ALL    = DB . FetchAll (                                                 )
    ##########################################################################
    if                     ( ALL in [ False , None ]                       ) :
      return               [                                                 ]
    ##########################################################################
    if                     ( len ( ALL ) <= 0                              ) :
      return               [                                                 ]
    ##########################################################################
    R      =               [                                                 ]
    for A in ALL                                                             :
      U    = int           ( A [ 0 ]                                         )
      if                   ( U not in R                                    ) :
        R  . append        ( U                                               )
    ##########################################################################
    return R
  ############################################################################
  def ConnectToPeople ( self , DB , TABLE , UUID , T1 , UUIDs              ) :
    ##########################################################################
    REL = Relation    (                                                      )
    REL . set         ( "first" , UUID                                       )
    REL . setT1       ( T1                                                   )
    REL . setT2       ( "People"                                             )
    REL . setRelation ( "Subordination"                                      )
    REL . Joins       ( DB , TABLE , UUIDs                                   )
    ##########################################################################
    return
  ############################################################################
  def CountBelongs           ( self , DB , TABLE , UUID , T1               ) :
    ##########################################################################
    REL = Relation           (                                               )
    REL . set                ( "first" , UUID                                )
    REL . setT1              ( T1                                            )
    REL . setT2              ( "People"                                      )
    REL . setRelation        ( "Subordination"                               )
    ##########################################################################
    return REL . CountSecond ( DB , TABLE                                    )
  ############################################################################
  def RelateWithPeople  ( self , DB , TABLE , RELATED , UUID , T2 , UUIDs  ) :
    ##########################################################################
    REL   = Relation    (                                                    )
    REL   . set         ( "second" , UUID                                    )
    REL   . setT1       ( "People"                                           )
    REL   . setRelation ( RELATED                                            )
    ##########################################################################
    for PUID in UUIDs                                                        :
      REL . setT2       ( T2                                                 )
      REL . set         ( "first" , PUID                                     )
      REL . Join        ( DB , TABLE                                         )
    ##########################################################################
    return
  ############################################################################
  def CountOwners           ( self , DB , TABLE , RELATED , UUID , T2      ) :
    ##########################################################################
    REL = Relation          (                                                )
    REL . set               ( "second" , UUID                                )
    REL . setT1             ( "People"                                       )
    REL . setT2             ( T2                                             )
    REL . setRelation       ( RELATED                                        )
    ##########################################################################
    return REL . CountFirst ( DB , TABLE                                     )
  ############################################################################
  def Subordination            ( self , DB , TABLE , PUID , T2 , RELATED   ) :
    ##########################################################################
    REL        = Relation      (                                             )
    ##########################################################################
    REL        . set           ( "first" , f"{PUID}"                         )
    REL        . setT1         ( "People"                                    )
    REL        . setT2         ( T2                                          )
    REL        . setRelation   ( RELATED                                     )
    ##########################################################################
    return REL . Subordination (        DB , TABLE                           )
  ############################################################################
  def GetOwners              ( self , DB , TABLE , UUID , T2 , RELATED     ) :
    ##########################################################################
    REL        = Relation    (                                               )
    ##########################################################################
    REL        . set         ( "second" , f"{UUID}"                          )
    REL        . setT1       ( "People"                                      )
    REL        . setT2       ( T2                                            )
    REL        . setRelation ( RELATED                                       )
    ##########################################################################
    return REL . GetOwners   (        DB , TABLE                             )
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
