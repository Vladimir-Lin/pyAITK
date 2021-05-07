# -*- coding: utf-8 -*-
##############################################################################
##
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
import Actions
from   Actions . Database . SqlQuery       import SqlQuery
from   Actions . Database . SqlConnection  import SqlConnection
from   Actions . Database . SqlConnection  import ConnectionPair
from   Actions . System   . StarDate       import StarDate
##############################################################################
from   . Columns                           import Columns
##############################################################################
Relations         =      { \
  "Ignore"        :  0   , \
  "Subordination" :  1   , \
  "Icon"          :  2   , \
  "Sexuality"     :  3   , \
  "Trigger"       :  4   , \
  "StartTrigger"  :  5   , \
  "FinalTrigger"  :  6   , \
  "Action"        :  7   , \
  "Condition"     :  8   , \
  "Synonymous"    :  9   , \
  "Equivalent"    : 10   , \
  "Contains"      : 11   , \
  "Using"         : 12   , \
  "Possible"      : 13   , \
  "Originate"     : 14   , \
  "Capable"       : 15   , \
  "Estimate"      : 16   , \
  "Alias"         : 17   , \
  "Counterpart"   : 18   , \
  "Explain"       : 19   , \
  "Fuzzy"         : 20   , \
  "Greater"       : 21   , \
  "Less"          : 22   , \
  "Before"        : 23   , \
  "After"         : 24   , \
  "Tendency"      : 25   , \
  "Different"     : 26   , \
  "Acting"        : 27   , \
  "Forgotten"     : 28   , \
  "Google"        : 29   , \
  "Facebook"      : 30   , \
  "End"           : 31   , \
}
##############################################################################
Types                 =      { \
  "None"              :   0  , \
  "Type"              :   1  , \
  "Picture"           :   9  , \
  "Video"             :  11  , \
  "PlainText"         :  12  , \
  "File"              :  14  , \
  "Schedule"          :  15  , \
  "Task"              :  16  , \
  "Subgroup"          :  17  , \
  "Account"           :  18  , \
  "TopLevelDomain"    :  23  , \
  "SecondLevelDomain" :  24  , \
  "DomainName"        :  26  , \
  "Username"          :  27  , \
  "ITU"               :  28  , \
  "Nation"            :  43  , \
  "Currency"          :  45  , \
  "Tag"               :  75  , \
  "SqlConnection"     :  81  , \
  "Division"          :  91  , \
  "Period"            :  92  , \
  "Variable"          :  93  , \
  "CountryCode"       :  97  , \
  "AreaCode"          :  98  , \
  "Language"          : 101  , \
  "Place"             : 102  , \
  "People"            : 103  , \
  "Station"           : 104  , \
  "Organization"      : 105  , \
  "Role"              : 106  , \
  "Relevance"         : 107  , \
  "Locality"          : 108  , \
  "Group"             : 109  , \
  "Course"            : 110  , \
  "Lesson"            : 111  , \
  "IMApp"             : 112  , \
  "InstantMessage"    : 113  , \
  "Phone"             : 114  , \
  "Occupation"        : 115  , \
  "TimeZone"          : 116  , \
  "IPA"               : 117  , \
  "Address"           : 118  , \
  "EMail"             : 119  , \
  "Description"       : 120  , \
  "SqlServer"         : 121  , \
  "Lecture"           : 122  , \
  "Trade"             : 123  , \
  "Token"             : 124  , \
  "BankAccount"       : 125  , \
  "Class"             : 126  , \
  "Fragment"          : 127  , \
  "AgeGroup"          : 128  , \
  "Proficiency"       : 129  , \
}
##############################################################################
##
##############################################################################
class Relation       ( Columns                                             ) :
  ############################################################################
  global Relations
  global Types
  ############################################################################
  def __init__ ( self ) :
    self . Clear ( )
  ############################################################################
  def __del__ ( self ) :
    pass
  ############################################################################
  def Clear ( self ) :
    self . Columns     = [ ]
    self . Id          = 0
    self . First       = 0
    self . T1          = 0
    self . Second      = 0
    self . T2          = 0
    self . Relation    = 0
    self . Position    = 0
    self . Reverse     = 0
    self . Prefer      = 0
    self . Membership  = 0
    self . Description = 0
  ############################################################################
  def assign ( self , item ) :
    self . Columns     = item . Columns
    self . Id          = item . Id
    self . First       = item . First
    self . T1          = item . T1
    self . Second      = item . Second
    self . T2          = item . T2
    self . Relation    = item . Relation
    self . Position    = item . Position
    self . Reverse     = item . Reverse
    self . Prefer      = item . Prefer
    self . Membership  = item . Membership
    self . Description = item . Description
  ############################################################################
  def set ( self , item , value ) :
    a = item . lower ( )
    if ( "id"           == a ) :
      self . Id          = value
    if ( "first"        == a ) :
      self . First       = value
    if ( "t1"           == a ) :
      self . T1          = value
    if ( "second"       == a ) :
      self . Second      = value
    if ( "t2"           == a ) :
      self . T2          = value
    if ( "relation"     == a ) :
      self . Relation    = value
    if ( "position"     == a ) :
      self . Position    = value
    if ( "reverse"      == a ) :
      self . Reverse     = value
    if ( "prefer"       == a ) :
      self . Prefer      = value
    if ( "membership"   == a ) :
      self . Membership  = value
    if ( "description"  == a ) :
      self . Description = value
  ############################################################################
  def get ( self , item ) :
    a = item.lower()
    if ( "id"          == a ) :
      return self . Id
    if ( "first"       == a ) :
      return self . First
    if ( "t1"          == a ) :
      return self . T1
    if ( "second"      == a ) :
      return self . Second
    if ( "t2"          == a ) :
      return self . T2
    if ( "relation"    == a ) :
      return self . Relation
    if ( "position"    == a ) :
      return self . Position
    if ( "reverse"     == a ) :
      return self . Reverse
    if ( "prefer"      == a ) :
      return self . Prefer
    if ( "membership"  == a ) :
      return self . Membership
    if ( "description" == a ) :
      return self . Description
    return ""
  ############################################################################
  def Value ( self , item ) :
    return self . get ( item )
  ############################################################################
  def Values ( self , items ) :
    I = [ ]
    for x in items :
      I . append ( str ( self . Value ( x ) ) )
    return " , " . join ( I )
  ############################################################################
  def tableItems ( self ) :
    S = [ ]
    S . append ( "id"          )
    S . append ( "first"       )
    S . append ( "t1"          )
    S . append ( "second"      )
    S . append ( "t2"          )
    S . append ( "relation"    )
    S . append ( "position"    )
    S . append ( "reverse"     )
    S . append ( "prefer"      )
    S . append ( "membership"  )
    S . append ( "description" )
    return S
  ############################################################################
  def pair ( self , item ) :
    v = self . get ( item )
    return f"`{item}` = {v}"
  ############################################################################
  def FullList ( self ) :
    return [ "t1"       ,
             "t2"       ,
             "relation" ,
             "first"    ,
             "second"   ,
             "position" ]
  ############################################################################
  def ExactList ( self ) :
    return [ "t1"       ,
             "t2"       ,
             "relation" ,
             "first"    ,
             "second"   ]
  ############################################################################
  def FirstList ( self ) :
    return [ "t1"       ,
             "t2"       ,
             "relation" ,
             "first"    ]
  ############################################################################
  def SecondList ( self ) :
    return [ "t1"       ,
             "t2"       ,
             "relation" ,
             "second"   ]
  ############################################################################
  def isFirst ( self , F ) :
    return ( F == self . First )
  ############################################################################
  def isSecond ( self , S ) :
    return ( S == self . Second )
  ############################################################################
  def isType ( self , t1 , t2 ) :
    if ( self . T1 != t1 ) :
      return False
    if ( self . T2 != t2 ) :
      return False
    return True
  ############################################################################
  def isT1 ( self , t1 ) :
    return ( t1 == self . T1 )
  ############################################################################
  def isT2 ( self , t2 ) :
    return ( t2 == self . T2 )
  ############################################################################
  def isRelation ( self , R ) :
    return ( R == self . Relation )
  ############################################################################
  def setT1 ( self , N ) :
    self . T1 = Types [ N ]
  ############################################################################
  def setT2 ( self , N ) :
    self . T2 = Types [ N ]
  ############################################################################
  def setRelation ( self , N ) :
    self . Relation = Relations [ N ]
  ############################################################################
  def ExactItem ( self , Options = "" , Limits = "" ) :
    L = self . ExactList  ( )
    Q = self . QueryItems ( L , Options , Limits )
    return Q
  ############################################################################
  def FirstItem ( self , Options = "" , Limits = "" ) :
    L = self . FirstList  ( )
    Q = self . QueryItems ( L , Options , Limits )
    return Q
  ############################################################################
  def SecondItem ( self , Options = "" , Limits = "" ) :
    L = self . SecondList ( )
    Q = self . QueryItems ( L , Options , Limits )
    return Q
  ############################################################################
  def Last ( self , Table ) :
    WS = self . FirstItem ( "order by `position` desc" , "limit 0,1" )
    return f"select `position` from {Table} {WS} ;"
  ############################################################################
  def ExactColumn ( self , Table , Item , Options = "" , Limits = "" ) :
    WS = self . ExactItem ( Options , Limits )
    return f"select {Item} from {Table} {WS} ;" ;
  ############################################################################
  def InsertItems ( self , Table , items ) :
    JI = self . join   ( items , " , " )
    VL = self . Values ( items )
    return f"insert into {Table} ( {JI} ) values ( {VL} ) ;"
  ############################################################################
  def Insert ( self , Table ) :
    L = self . FullList ( )
    return self . InsertItems ( Table , L )
  ############################################################################
  def DeleteItems ( self , Table , items ) :
    QI = self . QueryItems ( items )
    return f"delete from {Table} {QI} ;"
  ############################################################################
  def Delete ( self , Table ) :
    L = self . ExactList ( )
    return self . DeleteItems ( Table , L )
  ############################################################################
  def WipeOut ( self , Table ) :
    L = self . FirstList ( )
    return self . DeleteItems ( Table , L )
  ############################################################################
  def obtain ( self , R ) :
    List = self . tableItems ( )
    CNT  = 0
    for x in List :
      self . set ( x , R [ CNT ] )
      CNT += 1
    return True
  ############################################################################
  def Subordination ( self , DB , Table , Options = "order by `position` asc" , Limits = "" ) :
    W = self . FirstItem ( Options , Limits )
    Q = f"select `second` from {Table} {W} ;"
    return DB . ObtainUuids ( Q )
  ############################################################################
  def GetOwners ( self , DB , Table , Options = "order by `id` asc" , Limits = "" ) :
    W = self . SecondItem ( Options , Limits )
    Q = f"select `first` from {Table} {W} ;"
    return DB . ObtainUuids ( Q )
  ############################################################################
  def CountFirst ( self , DB , Table ) :
    WW = self . SecondItem ( )
    QQ = f"select count(*) from {Table} {WW} ;"
    DB . Query ( QQ )
    rr = DB . FetchOne ( )
    return rr [ 0 ]
  ############################################################################
  def CountSecond ( self , DB , Table ) :
    WW = self . FirstItem ( )
    QQ = f"select count(*) from {Table} {WW} ;"
    DB . Query ( QQ )
    rr = DB . FetchOne ( )
    return rr [ 0 ]
  ############################################################################
  def Assure ( self , DB , Table ) :
    QQ = self . WipeOut ( Table )
    DB . Query          ( QQ    )
    QQ = self . Insert  ( Table )
    DB . Query          ( QQ    )
  ############################################################################
  def Append ( self , DB , Table ) :
    QQ = self . Insert ( Table )
    return DB . Query  ( QQ    )
  ############################################################################
  def Join ( self , DB , Table ) :
    QQ = self . ExactColumn ( Table , "id" )
    DB . Query ( QQ )
    Lists = DB . FetchAll ( )
    if ( not Lists ) :
      return False
    ID = -1
    QQ = self . Last ( Table )
    DB . Query ( QQ )
    rr = DB . FetchOne ( )
    if ( not rr ) :
      pass
    else :
      ID = rr [ 0 ]
    ID = ID + 1
    self . Position = ID
    return self . Append ( DB , Table )
  ############################################################################
  def Joins ( self , DB , Table , Lists ) :
    for x in Lists :
      self . set  ( "second" , x     )
      self . Join ( DB       , Table )
  ############################################################################
  def PrefectOrder ( self , DB , Table ) :
    IX  = [ ]
    WH  = self . FirstItem ( "order by `position` asc" )
    QQ  = f"select `id` from {Table} {WH} ;"
    IX  = DB . ObtainUuids ( QQ )
    pos = 0
    for xx in IX :
      QQ  = f"update {Table} set `position` = {pos} where `id` = {xx} ;"
      DB  . Query ( QQ )
      pos += 1
  ############################################################################
  def ObtainOwners ( self , DB , Table , Members , TMP ) :
    for nsx in TMP :
      self . set ( "second" , nsx )
      CC   = self . GetOwners ( DB , Table )
      Members . extend ( CC )
    return Members
  ############################################################################
  def Organize ( self , DB , Table ) :
    WH = self . FirstItem ( "order by `position` asc" )
    QQ = f"select `id` from {Table} {WH} ;"
    IX = DB . ObtainUuids ( QQ )
    if ( len ( IX ) <= 0 ) :
      return False
    pos    = 0
    DB     . LockWrites ( [ Table ] )
    for iv in IX :
      QQ   = f"update {Table} set `position` = {pos} where `id` = {iv} ;"
      DB   . Query ( QQ )
      pos += 1
    DB . UnlockTables ( )
    return True
  ############################################################################
  def Ordering ( self , DB , Table , UUIDs ) :
    pos = 0
    DB . LockWrite ( [ Table ] )
    for xu in UUIDs :
      self . set ( "second" , xu )
      WH   = self . ExactItem ( )
      QQ   = f"update {Table} set `position` = {pos} {WH} ;"
      DB   . Query ( QQ )
      pos += 1
    DB . UnlockTables ( )
    return True
##############################################################################
