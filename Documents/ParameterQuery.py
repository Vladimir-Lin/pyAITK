# -*- coding: utf-8 -*-
##############################################################################
## 時間區段物件
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
class ParameterQuery       (                                               ) :
  ############################################################################
  def __init__             ( self                                          , \
                             Type    = 0                                   , \
                             Variety = 0                                   , \
                             Scope   = ""                                  , \
                             Table   = "`parameters`"                      ) :
    ##########################################################################
    self . Type    = Type
    self . Variety = Variety
    self . Scope   = Scope
    self . Table   = Table
    ##########################################################################
    return
  ############################################################################
  def __del__              ( self                                          ) :
    return
  ############################################################################
  def setType              ( self , T                                      ) :
    ##########################################################################
    self . Type = T
    ##########################################################################
    return
  ############################################################################
  def setVariety           ( self , V                                      ) :
    ##########################################################################
    self . Variety = V
    ##########################################################################
    return
  ############################################################################
  def setScope             ( self , S                                      ) :
    ##########################################################################
    self . Scope = S
    ##########################################################################
    return
  ############################################################################
  def setTable             ( self , T                                      ) :
    ##########################################################################
    self . Table = T
    ##########################################################################
    return
  ############################################################################
  def Where                ( self , Uuid , Name                            ) :
    ##########################################################################
    T  = self . Type
    V  = self . Variety
    S  = self . Scope
    ##########################################################################
    N  = Name
    N  = N . replace       ( "'" , ""                                        )
    ##########################################################################
    QQ = f"""where `uuid` = {Uuid} and `type` = {T} and
            `variety` = {V} and `scope` = '{S}' and `name` = '{N}'"""
    QQ = QQ . replace      ( "\n" , ""                                       )
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def SelectItem           ( self , Item , Uuid , Name                     ) :
    ##########################################################################
    T = self . Table
    W = self . Where       (               Uuid , Name                       )
    ##########################################################################
    return f"select `{Item}` from {T} {W} ;"
  ############################################################################
  def UpdateItem           ( self , Item , Uuid , Name                     ) :
    ##########################################################################
    T = self . Table
    W = self . Where       (               Uuid , Name                       )
    ##########################################################################
    return f"update {T} set `{Item}` = ? {W} ;"
  ############################################################################
  def UpdateId             ( self , Id , Item , Value                      ) :
    ##########################################################################
    T = self . Table
    ##########################################################################
    return f"update {T} set `{Item}` = {Value} where `id` = {Id} ;"
  ############################################################################
  def Fetch                ( self , DB , Item , Uuid , Name                ) :
    ##########################################################################
    QQ = self . SelectItem (             Item , Uuid , Name                  )
    DB . Query             ( QQ                                              )
    RR = DB . FetchOne     (                                                 )
    ##########################################################################
    if                     ( RR in [ False , None ]                        ) :
      return ""
    ##########################################################################
    if                     ( len ( RR ) > 0                                ) :
      return RR            [ 0                                               ]
    ##########################################################################
    return ""
  ############################################################################
  def Value             ( self , DB ,              Uuid , Name             ) :
    return self . Fetch (        DB , "value"    , Uuid , Name               )
  ############################################################################
  def Floating          ( self , DB ,              Uuid , Name             ) :
    return self . Fetch (        DB , "floating" , Uuid , Name               )
  ############################################################################
  def Data              ( self , DB ,              Uuid , Name             ) :
    return self . Fetch (        DB , "data"     , Uuid , Name               )
  ############################################################################
  def ObtainsId       ( self , DB , Uuid , Name                            ) :
    ##########################################################################
    Id = self . Fetch ( DB , "id" , Uuid , Name                              )
    if                ( len ( str ( Id ) ) <= 0                            ) :
      return -1
    ##########################################################################
    return int        ( Id                                                   )
  ############################################################################
  def InsertIntoValue      ( self , DB , Uuid , Name , Value ) :
    ##########################################################################
    T  = self . Table
    Y  = self . Type
    V  = self . Variety
    S  = self . Scope
    ##########################################################################
    N  = Name
    N  = N . replace       ( "'" , ""                                        )
    ##########################################################################
    QQ = f"""insert into {T}
             (`uuid`,`type`,`variety`,`scope`,`name`,`value`)
             values
             ( {Uuid} , {Y} , {V} , '{S}' , '{N}' , {Value} ) ;"""
    QQ = QQ . replace      ( "\n" , ""                                       )
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def InsertIntoFloating   ( self , DB , Uuid , Name , Floating            ) :
    ##########################################################################
    T  = self . Table
    Y  = self . Type
    V  = self . Variety
    S  = self . Scope
    ##########################################################################
    N  = Name
    N  = N . replace       ( "'" , ""                                        )
    ##########################################################################
    QQ = f"""insert into {T}
             (`uuid`,`type`,`variety`,`scope`,`name`,`floating`)
             values
             ( {Uuid} , {Y} , {V} , '{S}' , '{N}' , {Floating} ) ;"""
    QQ = QQ . replace      ( "\n" , ""                                       )
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def InsertIntoData       ( self , DB , Uuid , Name                       ) :
    ##########################################################################
    T  = self . Table
    Y  = self . Type
    V  = self . Variety
    S  = self . Scope
    ##########################################################################
    N  = Name
    N  = N . replace       ( "'" , ""                                        )
    ##########################################################################
    QQ = f"""insert into {T}
             (`uuid`,`type`,`variety`,`scope`,`name`,`data`)
             values
             ( {Uuid} , {Y} , {V} , '{S}' , '{N}' , %s ) ;"""
    QQ = QQ . replace      ( "\n" , ""                                       )
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def assureValue                    ( self , DB , Uuid , Name , Value     ) :
    ##########################################################################
    Id   = self . ObtainsId          (        DB , Uuid , Name               )
    QQ   = ""
    if                               ( Id <= 0                             ) :
      QQ = self . InsertIntoValue    (        DB , Uuid , Name , Value       )
    else                                                                     :
      QQ = self . UpdateId           ( Id , "value"     , Value              )
    ##########################################################################
    return DB . Query                ( QQ                                    )
  ############################################################################
  def assureFloating                 ( self , DB , Uuid , Name , FloatV    ) :
    ##########################################################################
    Id   = self . ObtainsId          (        DB , Uuid , Name               )
    QQ   = ""
    if                               ( Id <= 0                             ) :
      QQ = self . InsertIntoFloating (        DB , Uuid , Name , FloatV      )
    else                                                                     :
      QQ = self . UpdateId           ( Id , "floating" , FloatV              )
    ##########################################################################
    return DB . Query                ( QQ                                    )
  ############################################################################
  def assureData                     ( self , DB , Uuid , Name , BLOB      ) :
    ##########################################################################
    Id   = self . ObtainsId          (        DB , Uuid , Name               )
    QQ   = ""
    if                               ( Id <= 0                             ) :
      QQ = self . InsertIntoData     (        DB , Uuid , Name               )
    else                                                                     :
      QQ = self . UpdateId           ( Id , "data" , "%s"                    )
    ##########################################################################
    return DB   . QueryValues        ( QQ , ( BLOB , )                       )
  ############################################################################
  def GetJsonScopeValues   ( self , DB , UUID                              ) :
    ##########################################################################
    T     = self . Table
    Y     = self . Type
    V     = self . Variety
    S     = self . Scope
    ##########################################################################
    J     =                {                                                 }
    ##########################################################################
    QQ    = f"""select `name` , `value` from {T}
                where ( `uuid` = {UUID} )
                  and ( `type` = {Y} )
                  and ( `variety` = {V} )
                  and ( `scope` = '{S}' )
                order by `id` asc ;"""
    QQ    = QQ . replace   ( "\n" , ""                                       )
    QQ    = " " . join     ( QQ . split ( )                                  )
    DB    . Query          ( QQ                                              )
    ALL   = DB . FetchAll  (                                                 )
    ##########################################################################
    if                     ( ALL in [ False , None ]                       ) :
      return J
    ##########################################################################
    if                     ( len ( ALL ) <= 0                              ) :
      return J
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      Z   = R              [ 1                                               ]
      Z   = f"{Z}"
      if                   ( len ( Z ) <= 0                                ) :
        continue
      ########################################################################
      try                                                                    :
        Z = int            ( Z                                               )
      except                                                                 :
        continue
      ########################################################################
      N   = R              [ 0                                               ]
      ########################################################################
      try                                                                    :
        N = N . decode     ( "utf-8"                                         )
      except                                                                 :
        pass
      ########################################################################
      J [ N ] = Z
    ##########################################################################
    return   J
##############################################################################
def GetParameterData     ( DB , PUID , Item , T , V , S                    ) :
  PQ = ParameterQuery    (                    T , V , S                      )
  return PQ . Data       ( DB , PUID , Item                                  )
##############################################################################
def GetParameterFloating ( DB , PUID , Item , T , V , S                    ) :
  PQ = ParameterQuery    (                    T , V , S                      )
  return PQ . Floating   ( DB , PUID , Item                                  )
##############################################################################
def GetParameter         ( DB , PUID , Item , T , V , S                    ) :
  PQ = ParameterQuery    (                    T , V , S                      )
  return PQ . Value      ( DB , PUID , Item                                  )
##############################################################################
