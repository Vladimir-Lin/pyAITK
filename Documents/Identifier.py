# -*- coding: utf-8 -*-
##############################################################################
## 辨識字物件
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
from   AITK . Database  . Query       import Query
from   AITK . Database  . Connection  import Connection
from   AITK . Database  . Columns     import Columns
##############################################################################
## 辨識字物件
##############################################################################
class Identifier         ( Columns                                         ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    self      . Clear    (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def Clear          ( self                                                ) :
    ##########################################################################
    self . Columns = [                                                       ]
    self . Id      = -1
    self . Uuid    =  0
    self . Type    =  1
    self . Name    =  ""
    self . ltime   =  0
    ##########################################################################
    return
  ############################################################################
  def assign ( self , item                                                 ) :
    ##########################################################################
    self . Columns = item . Columns
    self . Id      = item . Id
    self . Uuid    = item . Uuid
    self . Type    = item . Type
    self . Name    = item . Name
    self . ltime   = item . ltime
    ##########################################################################
    return
  ############################################################################
  def set                 ( self , item , value                            ) :
    ##########################################################################
    a      = item . lower (                                                  )
    ##########################################################################
    if                    ( "id"    == a                                   ) :
      self . Id    = int  ( value                                            )
    if                    ( "uuid"  == a                                   ) :
      self . Uuid  = int  ( value                                            )
    if                    ( "type"  == a                                   ) :
      self . Type  = int  ( value                                            )
    if                    ( "name"  == a                                   ) :
      self . Name  = value
    if                    ( "ltime" == a                                   ) :
      self . ltime = value
    ##########################################################################
    return
  ############################################################################
  def get            ( self , item                                         ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"    == a                                        ) :
      return self . Id
    if               ( "uuid"  == a                                        ) :
      return self . Uuid
    if               ( "type"  == a                                        ) :
      return self . Type
    if               ( "name"  == a                                        ) :
      return self . Name
    if               ( "ltime" == a                                        ) :
      return self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems ( self                                                    ) :
    return       [ "id"                                                    , \
                   "uuid"                                                  , \
                   "type"                                                  , \
                   "name"                                                  , \
                   "ltime"                                                   ]
  ############################################################################
  def pair ( self , item )                                                   :
    v = self . get ( item )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems ( self                                                    ) :
    return       [ "type" , "name"                                           ]
  ############################################################################
  def setType           ( self , TYPE                                      ) :
    ##########################################################################
    try                                                                      :
      self . Type = int (        TYPE                                        )
    except                                                                   :
      pass
    ##########################################################################
    return self . Type
  ############################################################################
  def setIdentifier                    ( self , Identifier                 ) :
    ##########################################################################
    self . Name = Identifier
    ##########################################################################
    self . Name = self . Name .  strip (                                     )
    self . Name = self . Name . rstrip (                                     )
    ##########################################################################
    return self . Name
  ############################################################################
  def ObtainsById                        ( self , DB , TABLE               ) :
    ##########################################################################
    ID     = int                         ( self . Id                         )
    ##########################################################################
    if                                   ( ID < 0                          ) :
      return False
    ##########################################################################
    QQ     = f"""select `uuid`,`type`,`name` from {TABLE}
               where ( `id` = {ID} ) ;"""
    QQ     = " " . join                  ( QQ . split ( )                    )
    DB     . Query                       ( QQ                                )
    RR     = DB  . FetchOne              (                                   )
    ##########################################################################
    if                                   ( RR in [ False , None ]          ) :
      return False
    ##########################################################################
    if                                   ( len ( RR ) <= 0                 ) :
      return False
    ##########################################################################
    self   . Uuid = int                  ( RR [ 0 ]                          )
    self   . Type = int                  ( RR [ 1 ]                          )
    self   . Name = RR                   [ 2                                 ]
    ##########################################################################
    try                                                                      :
      self . Name = self . Name . decode ( "utf-8"                           )
    except                                                                   :
      pass
    ##########################################################################
    return True
  ############################################################################
  def DeleteId ( self , DB , TABLE                                         ) :
    ##########################################################################
    ID = int   ( self . Id                                                   )
    ##########################################################################
    if         ( ID < 0                                                    ) :
      return False
    ##########################################################################
    QQ = f"delete from {TABLE} where ( `id` = {ID} ) ;"
    DB . Query ( QQ                                                          )
    ##########################################################################
    return
  ############################################################################
  def WipeOut       ( self , DB , TABLE                                    ) :
    ##########################################################################
    U  = self . Uuid
    T  = self . Type
    ##########################################################################
    QQ = f"""delete from {TABLE}
             where ( `uuid` = {U} )
               and ( `type` = {T} ) ;"""
    QQ = " " . join ( QQ . split ( )                                         )
    DB . Query      ( QQ                                                     )
    ##########################################################################
    return
  ############################################################################
  def Owners                  ( self , DB , TABLE                          ) :
    ##########################################################################
    T         = self . Type
    VAL       =               ( self . Name ,                                )
    ##########################################################################
    QQ        = f"""select `uuid` from {TABLE}
                    where ( `type` = {T} )
                      and ( `name` = %s )
                    group by `uuid` ;"""
    QQ        = " " . join    ( QQ . split ( )                               )
    DB        . QueryValues   ( QQ , VAL                                     )
    ##########################################################################
    RR        = DB . FetchAll (                                              )
    if                        ( RR in [ False , None ]                     ) :
      return                  [                                              ]
    ##########################################################################
    if                        ( len ( RR ) <= 0                            ) :
      return                  [                                              ]
    ##########################################################################
    UUIDs     =               [                                              ]
    ##########################################################################
    for R in RR                                                              :
      ########################################################################
      U       = R             [ 0                                            ]
      U       = int           ( U                                            )
      if                      ( U not in UUIDs                             ) :
        UUIDs . append        ( U                                            )
    ##########################################################################
    return UUIDs
  ############################################################################
  def Identifiers         ( self , DB , TABLE , ORDER = "asc"              ) :
    ##########################################################################
    U     = self . Uuid
    T     = self . Type
    ##########################################################################
    QQ    = f"""select convert ( `name` using utf8 ) from {TABLE}
                where ( `uuid` = {U} )
                  and ( `type` = {T} )
                order by `id` {ORDER} ;"""
    QQ    = " " . join    ( QQ . split ( )                                   )
    DB    . Query         ( QQ                                               )
    ##########################################################################
    RR    = DB . FetchAll (                                                  )
    if                    ( RR in [ False , None ]                         ) :
      return              [                                                  ]
    ##########################################################################
    if                    ( len ( RR ) <= 0                                ) :
      return              [                                                  ]
    ##########################################################################
    ALL   =               [                                                  ]
    ##########################################################################
    for R in RR                                                              :
      ########################################################################
      N   = R             [ 0                                                ]
      ALL . append        ( f"{N}"                                           )
    ##########################################################################
    return ALL
  ############################################################################
  def Append                 ( self , DB , TABLE                           ) :
    ##########################################################################
    N   = self . Name
    try                                                                      :
      B = N . encode         ( "utf-8"                                       )
    except                                                                   :
      pass
    ##########################################################################
    U   = self . Uuid
    T   = self . Type
    VAL =                    ( B ,                                           )
    ##########################################################################
    QQ  = f"""insert into {TABLE}
              ( `uuid` , `type` , `name` )
              values
              ( {U} , {T} , %s ) ;"""
    QQ  = " "  . join        ( QQ . split ( )                                )
    return DB  . QueryValues ( QQ , VAL                                      )
  ############################################################################
  def Assure                  ( self , DB , TABLE                          ) :
    ##########################################################################
    IDs = self  . Identifiers (        DB , TABLE                            )
    ##########################################################################
    if                        ( len ( IDs ) > 0                            ) :
      if                      ( self . Name in IDs                         ) :
        return True
    ##########################################################################
    return self . Append      (        DB , TABLE                            )
##############################################################################
