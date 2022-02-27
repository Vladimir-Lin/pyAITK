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
    self . Groups   = [                                                      ]
    self . Details  = {                                                      }
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    return
  ############################################################################
  def Join                   ( self , PUID                                 ) :
    ##########################################################################
    if                       ( PUID not in self . Groups                   ) :
      self . Groups . append ( PUID                                          )
    ##########################################################################
    return
  ############################################################################
  def setDetail ( self , PUID , detail                                     ) :
    ##########################################################################
    self . Details [ PUID ] = detail
    ##########################################################################
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
    ##########################################################################
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
  def UpdatePeopleUsed ( self , DB , TABLE , UUID , USED                   ) :
    ##########################################################################
    QQ = f"""update {TABLE}
             set `used` = {USED}
             where ( `uuid` = {UUID} ) ;"""
    QQ = " " . join    ( QQ . split ( )                                      )
    DB . Query         ( QQ                                                  )
    ##########################################################################
    return
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
  def ConnectWithPeople ( self , DB , TABLE , UUID , T2 , RELATED , UUIDs  ) :
    ##########################################################################
    REL = Relation      (                                                    )
    REL . set           ( "first" , UUID                                     )
    REL . setT1         ( "People"                                           )
    REL . setT2         ( T2                                                 )
    REL . setRelation   ( RELATED                                            )
    REL . Joins         ( DB , TABLE , UUIDs                                 )
    ##########################################################################
    return
  ############################################################################
  def ConnectWithWebPages    ( self , DB , TABLE , PUID , WPID             ) :
    ##########################################################################
    self . ConnectWithPeople ( DB                                          , \
                               TABLE                                       , \
                               PUID                                        , \
                               "WebPage"                                   , \
                               "Equivalent"                                , \
                               [ WPID ]                                      )
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
    REL   . setT2       ( T2                                                 )
    REL   . setRelation ( RELATED                                            )
    ##########################################################################
    for PUID in UUIDs                                                        :
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
  def GetIcons                  ( self , DB , TABLE , PUID                 ) :
    return self . Subordination ( DB , TABLE , PUID , "Picture" , "Using"    )
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
  def RepositionIcons       ( self , DB , TABLE , PUID , UUIDs             ) :
    ##########################################################################
    REL = Relation          (                                                )
    ##########################################################################
    REL . set               ( "first" , f"{PUID}"                            )
    REL . setT1             ( "People"                                       )
    REL . setT2             ( "Picture"                                      )
    REL . setRelation       ( "Using"                                        )
    REL . RepositionByFirst ( DB , TABLE , UUIDs                             )
    ##########################################################################
    return
  ############################################################################
  def MergeVariables          ( self , DB , PUID , MERGER                  ) :
    ##########################################################################
    VARTAB = self . Tables    [ "Variables"                                  ]
    ##########################################################################
    QQ     = f"lock tables {VARTAB} write , {VARTAB} as TT read ;"
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""select `type`,`name` from {VARTAB} as TT
                 where ( `uuid` = {PUID} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ALL    = DB . FetchAll    (                                              )
    ##########################################################################
    for RR in ALL                                                            :
      ########################################################################
      TT   = RR               [ 0                                            ]
      NA   = RR               [ 1                                            ]
      ########################################################################
      try                                                                    :
        NA = NA . decode      ( "utf-8"                                      )
      except                                                                 :
        pass
      ########################################################################
      QQ   = f"""delete from {VARTAB}
                 where ( `uuid` = {MERGER} )
                 and ( `type` = {TT} )
                 and ( `name` = '{NA}' ) ;"""
      QQ   = " " . join       ( QQ . split ( )                               )
      DB   . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""update {VARTAB}
                 set `uuid` = {PUID}
                 where ( `uuid` = {MERGER} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    return
  ############################################################################
  def MergeParameters                ( self , DB , PUID , MERGER           ) :
    ##########################################################################
    PAMTAB = self . Tables           [ "Parameters"                          ]
    ##########################################################################
    DB     . LockWrites              ( [ PAMTAB                            ] )
    ##########################################################################
    QQ     = f"""update {PAMTAB}
                 set `uuid` = {PUID}
                 where ( `uuid` = {MERGER} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    return
  ############################################################################
  def MergeNotes                     ( self , DB , PUID , MERGER           ) :
    ##########################################################################
    NOXTAB = self . Tables           [ "Notes"                               ]
    ##########################################################################
    DB     . LockWrites              ( [ NOXTAB                            ] )
    ##########################################################################
    QQ     = f"""update {NOXTAB}
                 set `uuid` = {PUID}
                 where ( `uuid` = {MERGER} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    return
  ############################################################################
  def PurgeNamesByCatalog            ( self                                , \
                                       DB                                  , \
                                       PUID                                , \
                                       LOCALITY                            , \
                                       RELEVANCE                           ) :
    ##########################################################################
    NAMTAB = self . Tables           [ "Names"                               ]
    NI     = NameItem                (                                       )
    ##########################################################################
    NI     . Uuid      = PUID
    NI     . Locality  = LOCALITY
    NI     . Relevance = RELEVANCE
    ##########################################################################
    IDs    = NI . ObtainsForPriority ( DB , NAMTAB                           )
    MAPs   =                         {                                       }
    TOTAL  = len                     ( IDs                                   )
    ##########################################################################
    if                               ( TOTAL <= 0                          ) :
      return
    ##########################################################################
    for ID in IDs                                                            :
      ########################################################################
      NX   = NameItem                (                                       )
      NX   . Id        = ID
      NX   . ObtainsById             ( DB , NAMTAB                           )
      MAPs [ ID ] = NX
    ##########################################################################
    PURGEs =                         [                                       ]
    AT     = 0
    ##########################################################################
    while                            ( AT < TOTAL                          ) :
      ########################################################################
      ID   = IDs                     [ AT                                    ]
      NAME = MAPs [ ID ] . Name
      NEXT = AT + 1
      ########################################################################
      while                          ( NEXT < TOTAL                        ) :
        ######################################################################
        IX = IDs                     [ NEXT                                  ]
        ######################################################################
        if                           ( IX not in PURGEs                    ) :
          ####################################################################
          NX = MAPs [ IX ] . Name
          if                         ( NAME == NX                          ) :
            ##################################################################
            PURGEs . append          ( IX                                    )
        ######################################################################
        NEXT = NEXT + 1
      ########################################################################
      AT   = AT + 1
    ##########################################################################
    if                               ( len ( PURGEs ) <= 0                 ) :
      return
    ##########################################################################
    DB     . LockWrites              ( [ NAMTAB                            ] )
    ##########################################################################
    for ID in PURGEs                                                         :
      ########################################################################
      QQ   = f"delete from {NAMTAB} where ( `id` = {ID} ) ;"
      DB   . Query                   ( QQ                                    )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    return
  ############################################################################
  def MergeNamesByCatalog            ( self                                , \
                                       DB                                  , \
                                       PUID                                , \
                                       MERGER                              , \
                                       LOCALITY                            , \
                                       RELEVANCE                           ) :
    ##########################################################################
    NAMTAB = self . Tables           [ "Names"                               ]
    NI     = NameItem                (                                       )
    ##########################################################################
    NI     . Uuid      = MERGER
    NI     . Locality  = LOCALITY
    NI     . Relevance = RELEVANCE
    ##########################################################################
    IDs    = NI . ObtainsForPriority ( DB , NAMTAB                           )
    ##########################################################################
    NI     . Uuid      = PUID
    POS    = NI . LastPosition       ( DB , NAMTAB                           )
    ##########################################################################
    DB     . LockWrites              ( [ NAMTAB                            ] )
    for ID in IDs                                                            :
      ########################################################################
      NI   . Id        = ID
      NI   . Priority  = POS
      NI   . UpdateUuidPriorityById  ( DB , NAMTAB                           )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    return
  ############################################################################
  def MergeNames                     ( self , DB , PUID , MERGER           ) :
    ##########################################################################
    NAMTAB   = self . Tables         [ "Names"                               ]
    NI       = NameItem              (                                       )
    ##########################################################################
    NI       . Uuid = MERGER
    CATALOGs = NI . SelectCatalogues ( DB , NAMTAB                           )
    ##########################################################################
    for C in CATALOGs                                                        :
      ########################################################################
      LC     = C                     [ "Locality"                            ]
      RX     = C                     [ "Relevance"                           ]
      self   . MergeNamesByCatalog   ( DB , PUID , MERGER , LC , RX          )
      self   . PurgeNamesByCatalog   ( DB , PUID          , LC , RX          )
    ##########################################################################
    return
  ############################################################################
  def GetFirstRelationCatalogues  ( self , DB , MERGER                     ) :
    ##########################################################################
    RELTAB = self . Tables        [ "Relation"                               ]
    ##########################################################################
    QQ     = f"""select `t2`,`relation` from {RELTAB}
                 where ( `first` = {MERGER} )
                 and ( `t1` = 7 )
                 group by `t2` asc ,`relation` asc ;"""
    QQ     = " " . join           ( QQ . split ( )                           )
    DB     . Query                ( QQ                                       )
    ALL    = DB . FetchAll        (                                          )
    ##########################################################################
    if                            ( ALL in [ False , None ]                ) :
      return                      [                                          ]
    ##########################################################################
    if                            ( len ( ALL ) <= 0                       ) :
      return                      [                                          ]
    ##########################################################################
    RELs   =                      [                                          ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      T2   = R                    [ 0                                        ]
      REL  = R                    [ 1                                        ]
      J    =                      { "T2" : T2 , "Relation" : REL             }
      RELs . append               ( J                                        )
    ##########################################################################
    return RELs
  ############################################################################
  def MergeFirstPosition      ( self , DB , PUID , MERGER , T2 , REL       ) :
    ##########################################################################
    RELTAB = self . Tables    [ "Relation"                                   ]
    ##########################################################################
    QQ     = f"lock tables {RELTAB} write , {RELTAB} as TT read ;"
    DB     . Query            ( QQ                                           )
    ##########################################################################
    FF     = f"""select `second` from {RELTAB} as TT
                   where ( `first` = {PUID} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )"""
    QQ     = f"""delete from {RELTAB}
                   where ( `first` = {MERGER} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )
                   and ( `second` in ( {FF} ) ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    POS    = -1
    QQ     = f"""select `position` from {RELTAB} as TT
                 where ( `first` = {PUID} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )
                   order by `position` desc
                   limit 0 , 1 ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    RR     = DB . FetchOne    (                                              )
    if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )            :
      POS  = RR               [ 0                                            ]
    POS    = POS + 1
    ##########################################################################
    QQ     = f"""select `second` from {RELTAB} as TT
                   where ( `first` = {MERGER} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )
                   order by `position` asc ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    UUIDs  = DB . ObtainUuids ( QQ                                           )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ   = f"""update {RELTAB}
                   set `first` = {PUID} , `position` = {POS}
                   where ( `first` = {MERGER} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )
                   and ( `second` = {UUID} ) ;"""
      QQ   = " " . join       ( QQ . split ( )                               )
      DB   . Query            ( QQ                                           )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    return
  ############################################################################
  def MergeFirstRelations         ( self , DB , PUID , MERGER              ) :
    ##########################################################################
    RELTAB   = self . Tables      [ "Relation"                               ]
    CATALOGs = self . GetFirstRelationCatalogues  ( DB , MERGER              )
    ##########################################################################
    for CATALOG in CATALOGs                                                  :
      ########################################################################
      T2     = CATALOG            [ "T2"                                     ]
      REL    = CATALOG            [ "Relation"                               ]
      self   . MergeFirstPosition ( DB , PUID , MERGER , T2 , REL            )
    ##########################################################################
    return
  ############################################################################
  def GetSecondRelationCatalogues ( self , DB , MERGER                     ) :
    ##########################################################################
    RELTAB = self . Tables        [ "Relation"                               ]
    ##########################################################################
    QQ     = f"""select `t1`,`relation` from {RELTAB}
                 where ( `second` = {MERGER} )
                 and ( `t2` = 7 )
                 group by `t1` asc ,`relation` asc ;"""
    QQ     = " " . join           ( QQ . split ( )                           )
    DB     . Query                ( QQ                                       )
    ALL    = DB . FetchAll        (                                          )
    ##########################################################################
    if                            ( ALL in [ False , None ]                ) :
      return                      [                                          ]
    ##########################################################################
    if                            ( len ( ALL ) <= 0                       ) :
      return                      [                                          ]
    ##########################################################################
    RELs   =                      [                                          ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      T1   = R                    [ 0                                        ]
      REL  = R                    [ 1                                        ]
      J    =                      { "T1" : T1 , "Relation" : REL             }
      RELs . append               ( J                                        )
    ##########################################################################
    return RELs
  ############################################################################
  def MergeSecondPosition      ( self , DB , PUID , MERGER , T1 , REL      ) :
    ##########################################################################
    RELTAB  = self . Tables    [ "Relation"                                  ]
    ##########################################################################
    QQ     = f"lock tables {RELTAB} write , {RELTAB} as TT read ;"
    DB     . Query            ( QQ                                           )
    ##########################################################################
    FF      = f"""select `first` from {RELTAB} as TT
                   where ( `second` = {PUID} )
                   and ( `t1` = {T1} )
                   and ( `t2` = 7 )
                   and ( `relation` = {REL} )"""
    QQ      = f"""delete from {RELTAB}
                   where ( `second` = {MERGER} )
                   and ( `t1` = {T1} )
                   and ( `t2` = 7 )
                   and ( `relation` = {REL} )
                   and ( `first` in ( {FF} ) ) ;"""
    QQ      = " " . join       ( QQ . split ( )                              )
    DB      . Query            ( QQ                                          )
    ##########################################################################
    QQ      = f"""select `first` from {RELTAB} as TT
                   where ( `second` = {MERGER} )
                   and ( `t1` = {T1} )
                   and ( `t2` = 7 )
                   and ( `relation` = {REL} )
                   order by `position` asc ;"""
    QQ      = " " . join       ( QQ . split ( )                              )
    UUIDs   = DB . ObtainUuids ( QQ                                          )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      POS   = -1
      QQ    = f"""select `position` from {RELTAB} as TT
                   where ( `first` = {UUID} )
                     and ( `t1` = {T1} )
                     and ( `t2` = 7 )
                     and ( `relation` = {REL} )
                     order by `position` desc
                     limit 0 , 1 ;"""
      QQ    = " " . join       ( QQ . split ( )                              )
      DB    . Query            ( QQ                                          )
      RR    = DB . FetchOne    (                                             )
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )          :
        POS = RR               [ 0                                           ]
      POS   = POS + 1
      ########################################################################
      QQ    = f"""update {RELTAB}
                   set `second` = {PUID} , `position` = {POS}
                   where ( `second` = {MERGER} )
                   and ( `t1` = {T1} )
                   and ( `t2` = 7 )
                   and ( `relation` = {REL} )
                   and ( `first` = {UUID} ) ;"""
      QQ    = " " . join       ( QQ . split ( )                              )
      DB    . Query            ( QQ                                          )
      ########################################################################
      POS   = POS + 1
    ##########################################################################
    DB      . UnlockTables     (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeSecondRelations         ( self , DB , PUID , MERGER             ) :
    ##########################################################################
    RELTAB   = self . Tables       [ "Relation"                              ]
    CATALOGs = self . GetSecondRelationCatalogues ( DB , MERGER              )
    ##########################################################################
    for CATALOG in CATALOGs                                                  :
      ########################################################################
      T1     = CATALOG             [ "T1"                                    ]
      REL    = CATALOG             [ "Relation"                              ]
      self   . MergeSecondPosition ( DB , PUID , MERGER , T1 , REL           )
    ##########################################################################
    return
  ############################################################################
  def MergeRelations            ( self , DB , PUID , MERGER                ) :
    ##########################################################################
    self . MergeFirstRelations  (        DB , PUID , MERGER                  )
    self . MergeSecondRelations (        DB , PUID , MERGER                  )
    ##########################################################################
    return
  ############################################################################
  def Merge                   ( self , DB , PUID , MERGER                  ) :
    ##########################################################################
    self   . MergeVariables   (        DB , PUID , MERGER                    )
    self   . MergeParameters  (        DB , PUID , MERGER                    )
    self   . MergeNotes       (        DB , PUID , MERGER                    )
    self   . MergeNames       (        DB , PUID , MERGER                    )
    self   . MergeRelations   (        DB , PUID , MERGER                    )
    ##########################################################################
    PEOTAB = self . Tables    [ "People"                                     ]
    DB     . LockWrites       ( [ PEOTAB                                   ] )
    self   . UpdatePeopleUsed ( DB , PEOTAB , MERGER , 3                     )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    return
  ############################################################################
  def MergeAll                 ( self , DB , PUID , MERGERs , ICON = 0     ) :
    ##########################################################################
    PXID     = 0
    ##########################################################################
    ## 取得指派的代表圖示
    ##########################################################################
    if                         ( ICON > 0                                  ) :
      ########################################################################
      RELTAB = self . Tables   [ "Relation"                                  ]
      PXIDs  = self . GetIcons ( DB , RELTAB , ICON                          )
      ########################################################################
      if                       ( len ( PXIDs ) > 0                         ) :
        ######################################################################
        PXID = PXIDs           [ 0                                           ]
    ##########################################################################
    ## 合併人物資訊
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . Merge             (        DB , PUID , MERGER                   )
    ##########################################################################
    ## 重新排序代表圖示
    ##########################################################################
    if                         ( ( ICON > 0 ) and ( PXID > 0 )             ) :
      ########################################################################
      RELTAB = self . Tables   [ "Relation"                                  ]
      PXIDs  = self . GetIcons ( DB , RELTAB , PUID                          )
      CXIDs  =                 [ PXID                                        ]
      ########################################################################
      for CUID in PXIDs                                                      :
        ######################################################################
        if                     ( CUID not in CXIDs                         ) :
          CXIDs . append       ( CUID                                        )
      ########################################################################
      if                       ( len ( CXIDs ) > 0                         ) :
        DB   . LockWrites      ( [ RELTAB                                  ] )
        self . RepositionIcons ( DB , RELTAB , PUID , CXIDs                  )
        DB   . UnlockTables    (                                             )
    ##########################################################################
    return
##############################################################################
