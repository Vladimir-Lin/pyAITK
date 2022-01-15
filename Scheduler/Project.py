# -*- coding: utf-8 -*-
##############################################################################
## 計畫物件
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
from   AITK . Database   . Query      import Query
from   AITK . Database   . Connection import Connection
from   AITK . Database   . Columns    import Columns
##############################################################################
from   AITK . Essentials . Relation   import Relation as Relation
from   AITK . Calendars  . StarDate   import StarDate as StarDate
from   AITK . Calendars  . Periode    import Periode  as Periode
##############################################################################
from                     . Event      import Event    as Event
from                     . Events     import Events   as Events
from                     . Task       import Task     as Task
from                     . Tasks      import Tasks    as Tasks
##############################################################################
class Project            ( Columns                                         ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    self      . Clear    (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
  ############################################################################
  def Clear                       ( self                                   ) :
    ##########################################################################
    self . Columns      =         [                                          ]
    self . Id           = -1
    self . Uuid         =  0
    self . Used         =  0
    self . Type         =  0
    self . States       =  0
    self . ltime        =  0
    ##########################################################################
    self . Tables       =         {                                          }
    self . Translations =         {                                          }
    self . Period       = Periode (                                          )
    self . Tasks        =         [                                          ]
    ##########################################################################
    return
  ############################################################################
  def assign            ( self , item                                      ) :
    ##########################################################################
    self . Columns      = item . Columns
    self . Id           = item . Id
    self . Uuid         = item . Uuid
    self . Used         = item . Used
    self . Type         = item . Type
    self . States       = item . States
    self . ltime        = item . ltime
    ##########################################################################
    self . Tables       = item . Tables
    self . Translations = item . Translations
    self . Period       = item . Period
    ##########################################################################
    return
  ############################################################################
  def set                   ( self , item , value                          ) :
    ##########################################################################
    a      = item   . lower (                                                )
    if                      ( "id"       == a                              ) :
      self . Id     = value
    if                      ( "uuid"     == a                              ) :
      self . Uuid   = value
    if                      ( "used"     == a                              ) :
      self . Used   = value
    if                      ( "type"     == a                              ) :
      self . Type   = value
    if                      ( "states"   == a                              ) :
      self . States = value
    if                      ( "ltime"    == a                              ) :
      self . ltime  = value
    ##########################################################################
    return
  ############################################################################
  def get                   ( self , item                                  ) :
    ##########################################################################
    a      = item . lower   (                                                )
    if                      ( "id"       == a                              ) :
      return self . Id
    if                      ( "uuid"     == a                              ) :
      return self . Uuid
    if                      ( "used"     == a                              ) :
      return self . Used
    if                      ( "type"     == a                              ) :
      return self . Type
    if                      ( "states"   == a                              ) :
      return self . States
    if                      ( "ltime"    == a                              ) :
      return self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems        ( self                                             ) :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "used"                                                          ,
             "type"                                                          ,
             "states"                                                        ,
             "ltime"                                                         ]
  ############################################################################
  def pair              ( self , item                                      ) :
    v = self . get      (        item                                        )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems        ( self                                             ) :
    return [ "used"                                                          ,
             "type"                                                          ,
             "states"                                                        ]
  ############################################################################
  def toJson ( self                                                        ) :
    return   { "Id"     : self . Id                                          ,
               "Uuid"   : self . Uuid                                        ,
               "Used"   : self . Used                                        ,
               "Type"   : self . Type                                        ,
               "States" : self . States                                      }
  ############################################################################
  ############################################################################
  ############################################################################
  def JoinTasks       ( self , DB , RELTAB , UUIDs                         ) :
    ##########################################################################
    REL = Relation    (                                                      )
    REL . set         ( "first" , self . Uuid                                )
    REL . setT1       ( "Project"                                            )
    REL . setT2       ( "Task"                                               )
    REL . setRelation ( "Contains"                                           )
    REL . Joins       ( DB , RELTAB , UUIDs                                  )
    ##########################################################################
    return
  ############################################################################
  def GetTasks                 ( self , DB                                 ) :
    ##########################################################################
    RELTAB = self . Tables     [ "Relation"                                  ]
    REL    = Relation          (                                             )
    REL    . set               ( "first" , self . Uuid                       )
    REL    . setT1             ( "Project"                                   )
    REL    . setT2             ( "Task"                                      )
    REL    . setRelation       ( "Contains"                                  )
    ##########################################################################
    return REL . Subordination ( DB , RELTAB                                 )
  ############################################################################
  def FetchPeriod            ( self , DB                                   ) :
    ##########################################################################
    PRDTAB   = self . Tables [ "Periods"                                     ]
    UUID     = self . Uuid
    QQ       = f"""select `uuid` from {PRDTAB}
                   where ( `realm` = {UUID} )
                     and ( `role` = 71 )
                     and ( `item` = 1 )
                     and ( `used` = 1 )
                   order by `id` desc
                   limit 0 , 1 ;"""
    QQ       = " " . join    ( QQ . split ( )                                )
    DB       . Query         ( QQ                                            )
    RR       = DB . FetchOne (                                               )
    ##########################################################################
    if                       ( RR in [ False , None ]                      ) :
      return
    ##########################################################################
    if                       ( len ( RR ) != 1                             ) :
      return
    ##########################################################################
    PUID     = RR            [ 0                                             ]
    ##########################################################################
    self . Period . Uuid = PUID
    self . Period . ObtainsByUuid ( DB , PRDTAB                              )
    ##########################################################################
    return
  ############################################################################
  def reload                 ( self , DB                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def load                           ( self , DB                           ) :
    ##########################################################################
    PRJTAB = self . Tables           [ "Projects"                            ]
    self   . ObtainsByUuid           ( DB , PRJTAB                           )
    self   . FetchPeriod             ( DB                                    )
    self   . Tasks = self . GetTasks ( DB                                    )
    ##########################################################################
    return
##############################################################################
