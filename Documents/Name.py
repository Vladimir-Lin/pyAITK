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
## 元件名稱
##############################################################################
Usages            =                                                        { \
  "Default"       :   0                                                    , \
  "Typo"          :   1                                                    , \
  "Pen"           :   2                                                    , \
  "Stage"         :   3                                                    , \
  "Abbreviation"  :   4                                                    , \
  "Identifier"    :   5                                                    , \
  "Entry"         :   6                                                    , \
  "Pronunciation" :   7                                                    , \
  "Unit"          :   8                                                    , \
  "Symbol"        :   9                                                    , \
  "Other"         :  99                                                    , \
  "EndName"       :  10                                                      }
##############################################################################
class Name               ( Columns                                         ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    self      . Clear    (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__  ( self )                                                      :
    return
  ############################################################################
  def Clear            ( self                                              ) :
    ##########################################################################
    self . Columns   = [                                                     ]
    self . Id        = -1
    self . Uuid      =  0
    self . Locality  =  0
    self . Priority  =  0
    self . Relevance =  0
    self . Flags     =  0
    self . Utf8      =  0
    self . Length    =  0
    self . Name      =  ""
    self . ltime     =  0
    ##########################################################################
    return
  ############################################################################
  def assign ( self , item )                                                 :
    ##########################################################################
    self . Columns   = item . Columns
    self . Id        = item . Id
    self . Uuid      = item . Uuid
    self . Locality  = item . Locality
    self . Priority  = item . Priority
    self . Relevance = item . Relevance
    self . Flags     = item . Flags
    self . Utf8      = item . Utf8
    self . Length    = item . Length
    self . Name      = item . Name
    self . ltime     = item . ltime
    ##########################################################################
    return
  ############################################################################
  def set                    ( self , item , value                         ) :
    ##########################################################################
    a      = item . lower    (                                               )
    ##########################################################################
    if                       ( "id"        == a                            ) :
      self . Id        = int ( value                                         )
    if                       ( "uuid"      == a                            ) :
      self . Uuid      = int ( value                                         )
    if                       ( "locality"  == a                            ) :
      self . Locality  = int ( value                                         )
    if                       ( "priority"  == a                            ) :
      self . Priority  = int ( value                                         )
    if                       ( "relevance" == a                            ) :
      self . Relevance = int ( value                                         )
    if                       ( "flags"     == a                            ) :
      self . Flags     = int ( value                                         )
    if                       ( "utf8"      == a                            ) :
      self . Utf8      = int ( value                                         )
    if                       ( "length"    == a                            ) :
      self . Length    = int ( value                                         )
    if                       ( "name"      == a                            ) :
      self . Name      = value
    if                       ( "ltime"     == a                            ) :
      self . ltime     = value
    ##########################################################################
    return
  ############################################################################
  def get                        ( self , item                             ) :
    ##########################################################################
    a             = item . lower (                                           )
    ##########################################################################
    if                           ( "id"        == a                        ) :
      return int                 ( self . Id                                 )
    if                           ( "uuid"      == a                        ) :
      return int                 ( self . Uuid                               )
    if                           ( "locality"  == a                        ) :
      return int                 ( self . Locality                           )
    if                           ( "priority"  == a                        ) :
      return int                 ( self . Priority                           )
    if                           ( "relevance" == a                        ) :
      return int                 ( self . Relevance                          )
    if                           ( "flags"     == a                        ) :
      return int                 ( self . Flags                              )
    if                           ( "utf8"      == a                        ) :
      return int                 ( self . Utf8                               )
    if                           ( "length"    == a                        ) :
      return int                 ( self . Length                             )
    if                           ( "name"      == a                        ) :
      return                       self . Name
    if                           ( "ltime"     == a                        ) :
      return                       self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems ( self                                                    ) :
    return       [ "id"                                                    , \
                   "uuid"                                                  , \
                   "locality"                                              , \
                   "priority"                                              , \
                   "relevance"                                             , \
                   "flags"                                                 , \
                   "utf8"                                                  , \
                   "length"                                                , \
                   "name"                                                  , \
                   "ltime"                                                   ]
  ############################################################################
  def pair         ( self , item                                           ) :
    v = self . get (        item                                             )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems ( self                                                    ) :
    return       [ "id"                                                    , \
                   "uuid"                                                  , \
                   "locality"                                              , \
                   "priority"                                              , \
                   "relevance"                                             , \
                   "flags"                                                 , \
                   "utf8"                                                  , \
                   "length"                                                , \
                   "name"                                                  , \
                   "ltime"                                                   ]
  ############################################################################
  def isFlag ( self , Mask                                                 ) :
    return   ( ( self . Flags & Mask ) == Mask                               )
  ############################################################################
  def isUuid ( self , U                                                    ) :
    return   ( U == self . Uuid                                              )
  ############################################################################
  def isLocality ( self , L                                                ) :
    return       ( L == self . Locality                                      )
  ############################################################################
  def isRelevance ( self , R                                               ) :
    return        ( R == self . Relevance                                    )
  ############################################################################
  def hasName ( self                                                       ) :
    return    ( len ( self . Name ) > 0                                      )
  ############################################################################
  def setRelevance            ( self , N                                   ) :
    ##########################################################################
    global Usages
    ##########################################################################
    if                        ( N not in Usages                            ) :
      return
    ##########################################################################
    self . Relevance = Usages [ N                                            ]
    ##########################################################################
    return
  ############################################################################
  def toJson ( self                                                        ) :
    return   { "id"        : self . Id                                     , \
               "uuid"      : self . Uuid                                   , \
               "locality"  : self . Locality                               , \
               "priority"  : self . Priority                               , \
               "relevance" : self . Relevance                              , \
               "flags"     : self . Flags                                  , \
               "utf8"      : self . Utf8                                   , \
               "length"    : self . Length                                 , \
               "name"      : self . Name                                   , \
               "ltime"     : self . ltime                                    }
  ############################################################################
  def toList          ( self                                               ) :
    ##########################################################################
    Listings =        [                                                      ]
    Listings . append ( self . Id                                            )
    Listings . append ( self . Uuid                                          )
    Listings . append ( self . Locality                                      )
    Listings . append ( self . Priority                                      )
    Listings . append ( self . Relevance                                     )
    Listings . append ( self . Flags                                         )
    Listings . append ( self . Utf8                                          )
    Listings . append ( self . Length                                        )
    Listings . append ( self . Name                                          )
    Listings . append ( self . ltime                                         )
    ##########################################################################
    return Listings
  ############################################################################
  def Select                  ( self                                         ,
                                TABLE                                        ,
                                Options = "order by `priority` asc"          ,
                                Limits  = "limit 0,1"                      ) :
    ##########################################################################
    L    =                    [ "uuid" , "locality" , "relevance"            ]
    return self . SelectItems ( TABLE , L , Options , Limits                 )
  ############################################################################
  def SelectPosition          ( self , TABLE                               ) :
    L  =                      [ "uuid"                                       ,
                                "locality"                                   ,
                                "priority"                                   ,
                                "relevance"                                  ]
    QI = self . QueryItems    ( L                                            )
    return f"select `id` from {TABLE}{QI} ;"
  ############################################################################
  def LastPriority            ( self , TABLE                               ) :
    L  =                      [ "uuid" , "locality" , "relevance"            ]
    QI = self . QueryItems    ( L , "order by `priority` desc" , "limit 0,1" )
    return f"select `priority` from {TABLE}{QI} ;"
  ############################################################################
  def Fetch                   ( self , DB , TABLE                          ) :
    ##########################################################################
    L     =                   [ "uuid" , "locality" , "relevance"            ]
    QI    = self . QueryItems ( L , "order by `priority` asc" , "limit 0,1"  )
    ##########################################################################
    DB    . Query             ( f"select `name` from {TABLE}{QI} ;"          )
    RR    = DB . FetchOne     (                                              )
    ##########################################################################
    if                        ( RR == None                                 ) :
      return ""
    ##########################################################################
    if                        ( len ( RR ) <= 0                            ) :
      return ""
    ##########################################################################
    return RR                 [ 0                                            ]
  ############################################################################
  def FetchUuids                 ( self , DB , TABLE , UUIDs               ) :
    ##########################################################################
    NAMEs         =              {                                           }
    for u in UUIDs                                                           :
      ########################################################################
      self . Uuid = u
      NAMEs [ u ] = self . Fetch ( DB , TABLE                                )
    ##########################################################################
    return NAMEs
  ############################################################################
  def FetchEverything          ( self , DB , TABLE                         ) :
    ##########################################################################
    U     = self . Uuid
    L     = self . tableItems  (                                             )
    IS    = self . join        ( L , " , "                                   )
    WH    = f"where ( `uuid` = {U} )"
    SORT  = f"order by `locality` asc, `relevance` asc, `priority` asc"
    QQ    = f"select {IS} from {TABLE} {WH} {SORT} ;"
    ##########################################################################
    QQ    = " " . join         ( QQ . split ( )                              )
    DB    . Query              ( QQ                                          )
    RR    = DB . FetchAll      (                                             )
    ##########################################################################
    if                         ( RR == None                                ) :
      return                   [                                             ]
    ##########################################################################
    if                         ( len ( RR ) <= 0                           ) :
      return                   [                                             ]
    ##########################################################################
    return RR
  ############################################################################
  def InsertSyntax    ( self , TABLE                                       ) :
    ##########################################################################
    try                                                                      :
      ########################################################################
      BN = self . Name . encode ( "utf-8"                                    )
      ########################################################################
    except                                                                   :
      ########################################################################
      BN = self . Name
    ##########################################################################
    PU   = self . Uuid
    PL   = self . Locality
    PP   = self . Priority
    PR   = self . Relevance
    PF   = self . Flags
    PT   = len        ( self . Name                                          )
    PX   = len        ( BN                                                   )
    self . Length = PX
    self . Utf8   = PT
    ##########################################################################
    QQ   = f"""insert into {TABLE}
               ( `uuid`,`locality`,`priority`,`relevance`,
                 `flags`,`utf8`,`length`,`name` )
               values ( {PU},{PL},{PP},{PR},{PF},{PT},{PX},%s ) ;"""
    ##########################################################################
    return " " . join ( QQ . split ( )                                       )
  ############################################################################
  def Insert                     ( self , TABLE                            ) :
    return self . InsertSyntax   (        TABLE                              )
  ############################################################################
  def Delete               ( self , TABLE                                  ) :
    ##########################################################################
    L  =                   [ "uuid"                                          ,
                             "locality"                                      ,
                             "priority"                                      ,
                             "relevance"                                     ]
    QI = self . QueryItems ( L                                               )
    ##########################################################################
    return f"delete from {TABLE}{QI} ;"
  ############################################################################
  def DeleteID ( self , TABLE                                              ) :
    ID = self . Id
    return f"delete from {TABLE} where ( `id` = {ID} ) ;"
  ############################################################################
  def DeleteIDs      ( self , TABLE , Listings                             ) :
    UID = self . Uuid
    DD  = "," . join ( [ str(x) for x in Listings ]                          )
    return f"delete from {TABLE} where ( `uuid` = {UID} ) and ( `id` in ( {DD} ) ) ;"
  ############################################################################
  def UpdateSyntax           ( self , TABLE                                ) :
    ##########################################################################
    L    =                   [ "uuid"                                        ,
                               "locality"                                    ,
                               "priority"                                    ,
                               "relevance"                                   ]
    QI   = self . QueryItems ( L                                             )
    PF   = self . Flags
    PT   = len               ( self . Name                                   )
    PX   = len               ( self . Name . encode ( "utf-8" )              )
    ##########################################################################
    self . Length = PX
    self . Utf8   = PT
    ##########################################################################
    QQ   = f"""update {TABLE}
               set `name` = %s ,
                   `flags` = {PF} ,
                   `utf8` = {PT} ,
                   `length` = {PX} {QI} ;"""
    ##########################################################################
    return " " . join        ( QQ . split ( )                                )
  ############################################################################
  def Update                   ( self , TABLE                              ) :
    return self . UpdateSyntax (        TABLE                                )
  ############################################################################
  def UpdateId        ( self , TABLE                                       ) :
    ##########################################################################
    ID   = self . Id
    PU   = self . Uuid
    PL   = self . Locality
    PP   = self . Priority
    PR   = self . Relevance
    PF   = self . Flags
    PT   = len        ( self . Name                                          )
    PX   = len        ( self . Name . encode ( "utf-8" )                     )
    ##########################################################################
    self . Length = PX
    self . Utf8   = PT
    ##########################################################################
    QQ   = f"""update {TABLE}
               set `name` = %s ,
                   `uuid` = {PU} ,
                   `locality` = {PL} ,
                   `priority` = {PP} ,
                   `relevance` = {PR} ,
                   `flags` = {PF} ,
                   `utf8` = {PT} ,
                   `length` = {PX}
               where ( `id` = {ID} ) ;"""
    ##########################################################################
    return " " . join ( QQ . split ( )                                       )
  ############################################################################
  def LastPosition              ( self , DB , TABLE                        ) :
    ##########################################################################
    QQ    = self . LastPriority (             TABLE                          )
    ID    = -1
    DB    . Query               ( QQ                                         )
    RR    = DB . FetchOne       (                                            )
    if                          ( ( RR != None ) and ( len ( RR ) > 0 )    ) :
      ID  = RR                  [ 0                                          ]
    ##########################################################################
    return ID + 1
  ############################################################################
  def GetPosition              ( self , DB , TABLE                         ) :
    ##########################################################################
    QQ = self . SelectPosition ( TABLE                                       )
    DB . Query                 ( QQ                                          )
    RR = DB . FetchOne         (                                             )
    ##########################################################################
    if                         ( ( RR != None ) and ( len ( RR ) > 0 )     ) :
      return RR                [ 0                                           ]
    ##########################################################################
    return -1
  ############################################################################
  def UpdateNameById        ( self , DB , TABLE                            ) :
    ##########################################################################
    ID   = self . Id
    PT   = len              ( self . Name                                    )
    PX   = len              ( self . Name . encode ( "utf-8" )               )
    self . Length = PX
    self . Utf8   = PT
    QQ   = f"update {TABLE} set `name` = %s , `utf8` = {PT} , `length` = {PX} where ( `id` = {ID} ) ;"
    ##########################################################################
    return DB . QueryValues ( QQ , ( self . Name , )                         )
  ############################################################################
  def UpdateParametersById ( self , DB , TABLE                        ) :
    ##########################################################################
    ID = self . Id
    PL = self . Locality
    PP = self . Priority
    PR = self . Relevance
    QQ = f"""update {TABLE}
             set `locality` = {PL} ,
                 `priority` = {PP} ,
                 `relevance` = {PR}
             where ( `id` = {ID} ) ;"""
    QQ = " " . join        ( QQ . split ( )                                  )
    ##########################################################################
    R  = DB . Query        ( QQ                                              )
    ##########################################################################
    return R
  ############################################################################
  def Append                              ( self , DB , TABLE              ) :
    ##########################################################################
    if                                    ( self . Uuid <= 0               ) :
      return False
    ##########################################################################
    self . Length   = len                 ( self . Name                      )
    self . Utf8     = len                 ( self . Name . encode ( "utf-8" ) )
    self . Priority = self . LastPosition ( DB , TABLE                       )
    QQ   = self . InsertSyntax            ( TABLE                            )
    ##########################################################################
    return DB   . QueryValues             ( QQ , ( self . Name , )           )
  ############################################################################
  def Sync                   ( self , DB , TABLE                           ) :
    ##########################################################################
    if                       ( self . Uuid <= 0                            ) :
      return False
    ##########################################################################
    QQ = self . UpdateSyntax ( TABLE                                         )
    ##########################################################################
    return DB . QueryValues  ( QQ , ( self . Name , )                        )
  ############################################################################
  def SyncId                ( self , DB , TABLE                            ) :
    ##########################################################################
    if                      ( self . Id < 0                                ) :
      return False
    QQ = self . UpdateId    ( TABLE                                          )
    ##########################################################################
    return DB . QueryValues ( QQ , ( self . Name , )                         )
  ############################################################################
  def Assure                    ( self , DB , TABLE                        ) :
    ##########################################################################
    if                          ( self . Id <= 0                           ) :
      IDX  = self . GetPosition (        DB , TABLE                          )
      if                        ( IDX >= 0                                 ) :
        self . Id = IDX
    ##########################################################################
    if                          ( self . Id >  0                           ) :
      return self . SyncId      ( DB , TABLE                                 )
    ##########################################################################
    return   self . Append      ( DB , TABLE                                 )
  ############################################################################
  def ObtainsById          ( self , DB , TABLE                             ) :
    ##########################################################################
    ID     = self . Id
    IT     = self . items  (                                                 )
    QQ     = f"select {IT} from {TABLE} where `id` = {ID} ;"
    DB     . Query         ( QQ                                              )
    IT     = DB . FetchOne (                                                 )
    ##########################################################################
    if                     ( ( None != IT ) and ( len ( IT ) > 0 )         ) :
      self . obtain        ( IT                                              )
      return True
    ##########################################################################
    return False
  ############################################################################
  def ObtainsForPriority    ( self , DB , TABLE                            ) :
    ##########################################################################
    PU = self . Uuid
    PL = self . Locality
    PR = self . Relevance
    L  =                    [ "uuid" , "locality" , "relevance"              ]
    QI = self . QueryItems  ( L , "order by `priority` asc"                  )
    ##########################################################################
    return DB . ObtainUuids ( f"select `id` from {TABLE} {QI} ;"             )
  ############################################################################
  def FindByName          ( self , DB , TABLE , Name                       ) :
    ##########################################################################
    SPT   = "%" + Name + "%"
    QQ    = f"""select `uuid` from {TABLE} where `name` like %s order by `ltime` desc ;"""
    QQ    = QQ  . replace ( "\n" , ""                                        )
    QQ    = " " . join    ( QQ . split ( )                                   )
    DB    . QueryValues   ( QQ , ( SPT , )                                   )
    Lists = DB . FetchAll (                                                  )
    ##########################################################################
    if                    ( not Lists                                      ) :
      return UU
    ##########################################################################
    for x in Lists                                                           :
      UU  . append        ( x [ index ]                                      )
    ##########################################################################
    return UU
  ############################################################################
  def ObtainsIDs            ( self , DB , Table                            ) :
    ##########################################################################
    UX = self . Uuid
    RX = self . Relevance
    QQ = f"""select `id` from {Table}
             where `uuid` = {UX} and `relevance` = {RX}
             order by `priority` asc,`locality` asc ;"""
    QQ = QQ   . replace     ( "\n" , ""                                      )
    QQ = " "  . join        ( QQ . split ( )                                 )
    ##########################################################################
    return DB . ObtainUuids ( QQ                                             )
  ############################################################################
  def UpdateName             ( self , DB , Table                           ) :
    ##########################################################################
    ID   = self . Id
    LX   = self . Locality
    PT   = len               ( self . Name                                   )
    PX   = len               ( self . Name . encode ( "utf-8" )              )
    self . Length = PX
    self . Utf8   = PT
    QQ   = f"""update {Table}
               set `name` = %s ,
               `locality` = {LX} ,
               `utf8` = {PT} ,
               `length` = {PX}
               where `id` = {ID} ;"""
    QQ   = QQ  . replace     ( "\n" , ""                                     )
    QQ   = " " . join        ( QQ . split ( )                                )
    ##########################################################################
    return DB  . QueryValues ( QQ , ( self . Name , )                        )
  ############################################################################
  def Editing                      ( self , DB , Table                     ) :
    ##########################################################################
    if                             ( self . Id < 0                         ) :
      if                           ( len ( self . Name ) > 0               ) :
        self . Assure              ( DB , Table                              )
    else                                                                     :
      if                           ( len ( self . Name ) > 0               ) :
        self . UpdateName          ( DB , Table                              )
      else                                                                   :
        DB . Query                 ( self . DeleteId ( Table )               )
    ##########################################################################
    return True
  ############################################################################
  ## This will have a Table Locked
  ############################################################################
  def UpdatePriority    ( self , DB , Table , IDs                          ) :
    ##########################################################################
    if                  ( len ( IDs ) <= 0                                 ) :
      return False
    ##########################################################################
    CC   = 0
    DB   . LockWrites   ( [ Table ]                                          )
    ##########################################################################
    for id in IDs                                                            :
      ########################################################################
      QQ = f"update {Table} set `priority` = {CC} where `id` = {id} ;"
      DB . Query        ( QQ                                                 )
      CC = CC + 1
    ##########################################################################
    DB   . UnlockTables (                                                    )
    ##########################################################################
    return True
  ############################################################################
  def UpdateFlagsById ( self , DB , Table                                  ) :
    ##########################################################################
    ID = self . Id
    F  = self . Flags
    QQ = f"update {Table} set `flags` = {F} where ( `id` = {ID} ) ;"
    DB . Query        ( QQ                                                   )
    ##########################################################################
    return True
  ############################################################################
  def UpdateSmartly                    ( self , DB , Table                 ) :
    ##########################################################################
    if                                 ( self . Id < 0                     ) :
      ########################################################################
      if                               ( len ( self . Name ) > 0           ) :
        ######################################################################
        ## Append a new name
        ######################################################################
        Priority = self . LastPosition ( DB , Table                          )
        self     . set                 ( "Priority" , Priority               )
        DB       . LockWrite           ( Table                               )
        self     . Assure              ( DB         , Table                  )
        DB       . UnlockTables        (                                     )
        ######################################################################
    else                                                                     :
      ########################################################################
      if                               ( len ( self . Name ) > 0           ) :
        ######################################################################
        ## Update name content by Id
        ######################################################################
        ID       = self . Id
        LX       = self . Locality
        QQ       = f"""update {Table}
                       set `name` = %s ,
                           `locality` = {LX} ,
                           `length` = length(`name`)
                       where `id` = {ID} ;"""
        QQ       = QQ  . replace       ( "\n" , ""                           )
        QQ       = " " . join          ( QQ . split ( )                      )
        DB       . LockWrite           ( [ Table ]                           )
        DB       . QueryValues         ( QQ , ( self . Name , )              )
        DB       . UnlockTables        (                                     )
        ######################################################################
      else                                                                   :
        ######################################################################
        ## Name is empty, delete it
        ######################################################################
        QQ       = self . DeleteId     ( Table                               )
        DB       . LockWrite           ( Table                               )
        DB       . Query               ( QQ                                  )
        DB       . UnlockTables        (                                     )
    ##########################################################################
    return True
  ############################################################################
  def SelectCatalogues    ( self , DB , Table                              ) :
    ##########################################################################
    UUID  = self . Uuid
    QQ    = f"""select `locality` , `relevance` from {Table}
                where ( `uuid` = {UUID} )
                group by `locality` asc , `relevance` asc ;"""
    QQ    = " " . join    ( QQ . split ( )                                   )
    DB    . Query         ( QQ                                               )
    ALL   = DB . FetchAll (                                                  )
    ##########################################################################
    if                    ( ALL in [ False , None ]                        ) :
      return              [                                                  ]
    ##########################################################################
    if                    ( len ( ALL ) <= 0                               ) :
      return              [                                                  ]
    ##########################################################################
    LISTS =               [                                                  ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      LOCALITY  = R       [ 0                                                ]
      RELEVANCE = R       [ 1                                                ]
      ########################################################################
      J   =               { "Locality" : LOCALITY , "Relevance" : RELEVANCE  }
      ########################################################################
      LISTS     . append  ( J                                                )
    ##########################################################################
    return LISTS
  ############################################################################
  def UpdateUuidPriorityById ( self , DB , Table                           ) :
    ##########################################################################
    ID = self . Id
    UX = self . Uuid
    PY = self . Priority
    ##########################################################################
    QQ = f"""update {Table}
             set `uuid` = {UX} , `priority` = {PY}
             where ( `id` = {ID} ) ;"""
    QQ = " " . join          ( QQ . split ( )                                )
    DB . Query               ( QQ                                            )
    ##########################################################################
    return True
  ############################################################################
  def ListsToStrings ( self , LISTS                                        ) :
    ##########################################################################
    KK   =           [                                                       ]
    ##########################################################################
    for K in LISTS                                                           :
      ########################################################################
      KK . append    ( f"{K}"                                                )
    ##########################################################################
    return KK
  ############################################################################
  def LocateByName       ( self                                            , \
                           DB                                              , \
                           TABLE                                           , \
                           NAME                                            , \
                           LOCALITIES = [ ]                                , \
                           RELEVANCES = [ ]                                , \
                           PRIORITIES = [ ]                                ) :
    ##########################################################################
    LSQL   = ""
    RSQL   = ""
    PSQL   = ""
    ##########################################################################
    if                   ( len ( LOCALITIES ) > 0                          ) :
      ########################################################################
      KS   = self . ListsToStrings ( LOCALITIES                              )
      VS   = " , " . join          ( KS                                      )
      LSQL = f"and ( `locality` in ( {VS} ) )"
    ##########################################################################
    if                   ( len ( RELEVANCES ) > 0                          ) :
      ########################################################################
      KS   = self . ListsToStrings ( RELEVANCES                              )
      VS   = " , " . join          ( KS                                      )
      RSQL = f"and ( `relevance` in ( {VS} ) )"
    ##########################################################################
    if                   ( len ( PRIORITIES ) > 0                          ) :
      ########################################################################
      KS   = self . ListsToStrings ( PRIORITIES                              )
      VS   = " , " . join          ( KS                                      )
      PSQL = f"and ( `priority` in ( {VS} ) )"
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
               where ( `name` = %s ) {LSQL} {RSQL} {PSQL}
               group by `uuid` asc ;"""
    QQ     = " " . join    ( QQ . split ( )                                  )
    VAL    =               ( NAME ,                                          )
    ##########################################################################
    DB     . QueryValues   ( QQ , VAL                                        )
    RR     = DB . FetchAll (                                                 )
    ##########################################################################
    if                     ( RR in [ False , None ]                        ) :
      return               [                                                 ]
    ##########################################################################
    UU     =               [                                                 ]
    ##########################################################################
    for V in RR                                                              :
      ########################################################################
      XX   = V             [ 0                                               ]
      ########################################################################
      try                                                                    :
        VV = int           ( XX                                              )
      except                                                                 :
        VV = 0
      ########################################################################
      if                   ( VV not in UU                                  ) :
        UU . append        ( VV                                              )
    ##########################################################################
    return UU
##############################################################################
def Naming                 ( DB , Table , U , Locality , Usage = "Default" ) :
  NN        = Name         (                                                 )
  NN        . set          ( "Uuid"     , U                                  )
  NN        . set          ( "Locality" , Locality                           )
  NN        . setRelevance ( Usage                                           )
  return NN . Fetch        ( DB         , Table                              )
##############################################################################
def Locate                 ( DB                                            , \
                             TABLE                                         , \
                             NAME                                          , \
                             LOCALITIES = [ ]                              , \
                             RELEVANCES = [ ]                              , \
                             PRIORITIES = [ ]                              ) :
  ############################################################################
  NN        = Name         (                                                 )
  return NN . LocateByName ( DB                                            , \
                             TABLE                                         , \
                             NAME                                          , \
                             LOCALITIES                                    , \
                             RELEVANCES                                    , \
                             PRIORITIES                                      )
##############################################################################
