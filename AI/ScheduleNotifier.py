# -*- coding: utf-8 -*-
##############################################################################
## 行事曆管理介面
##############################################################################
import os
import sys
import subprocess
import getopt
import time
import datetime
import logging
import requests
import threading
import gettext
import shutil
import json
##############################################################################
import AITK
##############################################################################
from   AITK  . Database   . Connection import Connection as Connection
##############################################################################
from   AITK  . Documents  . Name       import Name       as NameItem
from   AITK  . Documents  . Name       import Naming     as Naming
from   AITK  . Documents  . Notes      import Notes      as NoteItem
from   AITK  . Documents  . Variables  import Variables  as VariableItem
##############################################################################
from   AITK  . Calendars  . StarDate   import StarDate   as StarDate
from   AITK  . Calendars  . Periode    import Periode    as Periode
##############################################################################
from   AITK  . Essentials . Relation   import Relation   as Relation
##############################################################################
from   AITK  . Google     . Calendar   import Calendar   as GCalendar
##############################################################################
class ScheduleNotifier (                                                   ) :
  ############################################################################
  def __init__         ( self , jsonFile = ""                              ) :
    ##########################################################################
    self . DebugLogger        = None
    self . Talk               = None
    self . Beau               = "Scheduler"
    self . JSON               = { }
    self . Calendar           = None
    self . Running            = False
    self . Working            = 0
    self . Locality           = 1002
    self . CalendarLocker     = threading . Lock ( )
    ##########################################################################
    self . Configure   (        jsonFile                                     )
    ##########################################################################
    self . AITKDB             = self . JSON [ "Database" ]
    self . CurrentCalendar    = self . JSON [ "Google" ] [ "Options" ] [ "Pick"   ]
    self . CurrentTask        = self . JSON [ "Google" ] [ "Options" ] [ "Task"   ]
    self . CurrentEvent       = self . JSON [ "Google" ] [ "Options" ] [ "Event"  ]
    self . CurrentPeriod      = self . JSON [ "Google" ] [ "Options" ] [ "Period" ]
    ##########################################################################
    self . CurrentTitle       = ""
    self . CurrentDescription = ""
    self . CurrentStart       = 0
    self . CurrentEnd         = 0
    ##########################################################################
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    return
  ############################################################################
  def Configure            ( self , jsonFile = ""                          ) :
    ##########################################################################
    self . JsonFile = f"{jsonFile}"
    ##########################################################################
    return self . LoadJSON (                                                 )
  ############################################################################
  def LoadJSON   ( self                                                    ) :
    ##########################################################################
    self  . JSON = { }
    J            = self  . JsonFile
    ##########################################################################
    if                          ( len ( J ) <= 0                           ) :
      return False
    ##########################################################################
    if                          ( not os . path . isfile ( J )             ) :
      return False
    ##########################################################################
    T     = ""
    try                                                                      :
      with open                 ( J , "rb" ) as F                            :
        T = F . read            (                                            )
    except                                                                   :
      return False
    ##########################################################################
    if                          ( len ( T ) <= 0                           ) :
      return False
    ##########################################################################
    BODY     = T . decode       ( "utf-8"                                    )
    if                          ( len ( BODY ) <= 0                        ) :
      return False
    ##########################################################################
    self  . JSON = json . loads ( BODY                                       )
    ##########################################################################
    return True
  ############################################################################
  def StoreJSON  ( self                                                    ) :
    ##########################################################################
    if           ( len ( self . JsonFile ) <= 0                            ) :
      return False
    ##########################################################################
    try                                                                      :
      with     open ( self . JsonFile , 'w' , encoding = 'utf-8' ) as f      :
        json . dump ( self  . JSON , f , ensure_ascii = False , indent = 2   )
    except                                                                   :
      return False
    ##########################################################################
    return True
  ############################################################################
  def debug                        ( self , message , way = "info"         ) :
    ##########################################################################
    Logger   = self . DebugLogger
    ##########################################################################
    if                             ( Logger == None                        ) :
      return
    ##########################################################################
    if                             ( way == "debug"                        ) :
      Logger . debug               ( message                                 )
    elif                           ( way == "info"                         ) :
      Logger . info                ( message                                 )
    ##########################################################################
    return
  ############################################################################
  def ActualTalkTo                 ( self , beau , message                 ) :
    ##########################################################################
    if                             ( self . Talk == None                   ) :
      return False
    ##########################################################################
    time . sleep                   ( 1.0                                     )
    self . Talk                    ( beau , message                          )
    ##########################################################################
    return True
  ############################################################################
  def TalkTo                       ( self , beau , message                 ) :
    threading . Thread             ( target = self . ActualTalkTo          , \
                                     args = ( beau , message , ) ) . start ( )
    return True
  ############################################################################
  def addWorking                   ( self                                  ) :
    ##########################################################################
    self . Working = int           ( self . Working + 1                      )
    ##########################################################################
    return
  ############################################################################
  def removeWorking                ( self                                  ) :
    ##########################################################################
    self . Working = int           ( self . Working - 1                      )
    ##########################################################################
    return
  ############################################################################
  def assureName             ( self                                        , \
                               DB                                          , \
                               UUID                                        , \
                               NAME                                        , \
                               TABLE = "`names_others`"                    , \
                               Flags = 1                                   ) :
    ##########################################################################
    N = NameItem             (                                               )
    N . Uuid      = UUID
    N . Locality  = self . Locality
    N . Priority  = 0
    N . Relevance = 0
    N . Flags     = Flags
    N . Name      = NAME
    N . Editing              ( DB , TABLE                                    )
    ##########################################################################
    return True
  ############################################################################
  def ObtainTaskUuid         ( self , DB , TABLE = "`tags`"                ) :
    ##########################################################################
    UUID = DB . LastUuid     ( TABLE , "uuid" , 2800000000000000000          )
    DB   . AddUuid           ( TABLE , UUID   , 92                           )
    ##########################################################################
    return UUID
  ############################################################################
  def AssureVariables        ( self                                        , \
                               DB                                          , \
                               UUID                                        , \
                               TYPE                                        , \
                               NAME                                        , \
                               VALUE                                       , \
                               TABLE = "`variables`"                       ) :
    ##########################################################################
    V         = VariableItem (                                               )
    V . Uuid  = UUID
    V . Type  = TYPE
    V . Name  = NAME
    V . Value = VALUE
    ##########################################################################
    V . AssureValue          ( DB , TABLE                                    )
    ##########################################################################
    return
  ############################################################################
  def GetVariable            ( self                                        , \
                               DB                                          , \
                               UUID                                        , \
                               TYPE                                        , \
                               NAME                                        , \
                               TABLE = "`variables`"                       ) :
    ##########################################################################
    V         = VariableItem (                                               )
    V . Uuid  = UUID
    V . Type  = TYPE
    V . Name  = NAME
    ##########################################################################
    return V . GetValue      ( DB , TABLE                                    )
  ############################################################################
  def EventToSkypeRTF         ( self , event                               ) :
    ##########################################################################
    if                        ( event [ "kind" ] != "calendar#event"       ) :
      return ""
    ##########################################################################
    TZ      = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    NOW     = StarDate          (                                            )
    PRD     = Periode           (                                            )
    ##########################################################################
    TITLE   = ""
    DESCR   = ""
    ##########################################################################
    if                          ( "summary"     in event                   ) :
      TITLE = event             [ "summary"                                  ]
    if                          ( "description" in event                   ) :
      DESCR = event             [ "description"                              ]
    ##########################################################################
    UUID = 0
    if     ( "extendedProperties" in event                                 ) :
      if   ( "private" in event [ "extendedProperties" ]                   ) :
        if ( "Uuid"    in event [ "extendedProperties" ] [ "private" ]     ) :
          UUID   = event [ "extendedProperties" ] [ "private" ] [ "Uuid" ]
          UUID   = int          ( UUID                                       )
    ##########################################################################
    SDATE   = event [ "start" ] [ "dateTime" ]
    EDATE   = event [ "end"   ] [ "dateTime" ]
    ##########################################################################
    SDATE   = SDATE             [ : 19                                       ]
    NOW     . fromInput         ( SDATE , TZ                                 )
    START   = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"    )
    ##########################################################################
    EDATE   = EDATE             [ : 19                                       ]
    NOW     . fromInput         ( EDATE , TZ                                 )
    ENDST   = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"    )
    ##########################################################################
    MSG     = f"<u>{TITLE}</u>\n開始時間:<b>{START}</b>\n結束時間:<b>{ENDST}</b>"
    ##########################################################################
    if                          ( len ( DESCR ) > 0                        ) :
      MSG   = f"{MSG}\n{DESCR}"
    ##########################################################################
    if                          ( UUID > 0                                 ) :
      PRD   . Uuid = UUID
      PXID  = PRD   . toString  (                                            )
      MSG   = f"{MSG}\n系統編號:{PXID}"
    ##########################################################################
    return MSG
  ############################################################################
  def ClearCurrentSettings    ( self                                       ) :
    ##########################################################################
    self . CurrentTitle       = ""
    self . CurrentDescription = ""
    self . CurrentStart       = 0
    self . CurrentEnd         = 0
    self . CurrentTask        = 0
    self . CurrentEvent       = 0
    self . CurrentPeriod      = 0
    self . JSON [ "Google" ] [ "Options" ] [ "Task"   ] = 0
    self . JSON [ "Google" ] [ "Options" ] [ "Event"  ] = 0
    self . JSON [ "Google" ] [ "Options" ] [ "Period" ] = 0
    self . StoreJSON ( )
    ##########################################################################
    return True
  ############################################################################
  def hasCurrentCalendarId    ( self                                       ) :
    ##########################################################################
    if                        ( len ( self . CurrentCalendar ) <= 0        ) :
      FAIL = "請先指定行事曆"
      self . TalkTo           ( "Calendars" , FAIL                           )
      return False
    ##########################################################################
    return True
  ############################################################################
  def hasCurrentPeriod          ( self                                     ) :
    ##########################################################################
    if                          ( self . CurrentPeriod <= 0                ) :
      FAIL = "請先指定時段編號"
      self . TalkTo             ( "Calendars" , FAIL                         )
      return False
    ##########################################################################
    return True
  ############################################################################
  def hasCompletePeriodDetails  ( self                                     ) :
    ##########################################################################
    FAIL   = "資訊不足以新增時段"
    ##########################################################################
    if                           ( len ( self . CurrentTitle ) <= 0        ) :
      self . TalkTo              ( "Calendars" , FAIL                        )
      return False
    ##########################################################################
    if                           ( self . CurrentStart <= 0                ) :
      self . TalkTo              ( "Calendars" , FAIL                        )
      return False
    ##########################################################################
    if                           ( self . CurrentEnd   <= 0                ) :
      self . TalkTo              ( "Calendars" , FAIL                        )
      return False
    ##########################################################################
    return True
  ############################################################################
  def ReportCurrentCalendar   ( self                                       ) :
    ##########################################################################
    if                        ( not self . hasCurrentCalendarId ( )        ) :
      return
    ##########################################################################
    G      = self . CurrentCalendar
    ##########################################################################
    if                        ( G in self . JSON [ "Google" ] [ "Groups" ] ) :
      ########################################################################
      NAME = self . JSON [ "Google" ] [ "Groups" ] [ G ] [ "Entry" ] [ "summary" ]
      TT   = self . JSON [ "Google" ] [ "Messages" ] [ "Picking" ]
      ########################################################################
      MSG  = f"{TT} : {NAME}"
      self . TalkTo           ( "Calendars" , MSG                            )
    ##########################################################################
    return
  ############################################################################
  def PickCalendar                  ( self , ID                            ) :
    ##########################################################################
    CNT    = 0
    ID     = int                    ( ID                                     )
    Groups = self . JSON [ "Google" ] [ "Groups" ]
    ##########################################################################
    for G in Groups                                                          :
      ########################################################################
      CNT  = CNT + 1
      ########################################################################
      if                            ( CNT == ID                            ) :
        ######################################################################
        self . CurrentCalendar = G
        NAME = Groups [ G ] [ "Entry" ] [ "summary" ]
        TT   = self . JSON [ "Google" ] [ "Messages" ] [ "Picking" ]
        ######################################################################
        MSG  = f"{TT} : {NAME}"
        self . TalkTo               ( "Calendars" , MSG                      )
        ######################################################################
        self . JSON [ "Google" ] [ "Options" ] [ "Pick" ] = self . CurrentCalendar
        self . StoreJSON            (                                        )
    ##########################################################################
    return
  ############################################################################
  def ReportCalendars             ( self                                   ) :
    ##########################################################################
    Groups  = self . JSON [ "Google" ] [ "Groups" ]
    KEYs    = Groups . keys       (                                          )
    CNT     = 0
    NAMES   =                     [                                          ]
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      CNT   = CNT + 1
      NAME  = Groups [ K ] [ "Entry" ] [ "summary" ]
      N     = f"{CNT}. {NAME}"
      NAMES . append              ( N                                        )
    ##########################################################################
    if                            ( len ( NAMES ) > 0                      ) :
      KK    = "\n" . join         ( NAMES                                    )
      TT    = self . JSON [ "Google" ] [ "Messages" ] [ "Groups" ]
      MSG   = f"{TT}\n\n{KK}"
      self  . TalkTo              ( "Calendars" , MSG                        )
    ##########################################################################
    return
  ############################################################################
  def ReportCurrentPeriods           ( self                                ) :
    ##########################################################################
    if                               ( not self . hasCurrentCalendarId ( ) ) :
      return
    ##########################################################################
    G      = self . CurrentCalendar
    ##########################################################################
    if ( G not in self . JSON [ "Google" ] [ "Groups" ] )                    :
      return False
    ##########################################################################
    TZ   = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    self . CalendarLocker . acquire  (                                       )
    ##########################################################################
    events       = self . Calendar . GetEvents                               (
      calendarId = G                                                         ,
      options    = { "timeZone" : TZ }                                       )
    ##########################################################################
    self . CalendarLocker . release  (                                       )
    ##########################################################################
    ITEMs = [ ]
    CNT   = 0
    ##########################################################################
    for e in events                                                          :
      CNT   = CNT + 1
      ITEM  = self . EventToSkypeRTF ( e                                     )
      if                             ( len ( ITEM ) > 0                    ) :
        ITEM  = f"{CNT}. {ITEM}"
        ITEMs . append               ( ITEM                                  )
    ##########################################################################
    MSG     = "\n\n" . join          ( ITEMs                                 )
    MSG     = f"總計有{CNT}個行事曆事件\n\n{MSG}"
    self    . TalkTo                 ( "Calendars" , MSG                     )
    ##########################################################################
    return True
  ############################################################################
  def AppendCalendarEntry         ( self , DB , ID , ENTRY                 ) :
    ##########################################################################
    UUID = self . ObtainTaskUuid  ( DB                                       )
    self . AssureVariables        ( DB , UUID , 75 , "Calendar" , ID         )
    self . assureName             ( DB , UUID , ENTRY [ "summary" ]          )
    ##########################################################################
    self . JSON [ "Google" ] [ "Groups" ] [ ID ] [ "Uuid"  ] = UUID
    ##########################################################################
    return True
  ############################################################################
  def UpdateCalendarEntry         ( self , DB , ID , UUID , ENTRY          ) :
    ##########################################################################
    self . assureName             ( DB , UUID , ENTRY [ "summary" ]          )
    ##########################################################################
    return True
  ############################################################################
  def AppendEventEntry          ( self , DB , CalendarId , TUID , EVENT    ) :
    ##########################################################################
    if                          ( EVENT [ "kind" ] != "calendar#event"     ) :
      return False
    ##########################################################################
    PRDTAB  = "`periods`"
    NOXTAB  = "`notes`"
    VARTAB  = "`variables`"
    RELTAB  = "`relations_others`"
    NAMTAB  = "`names_others`"
    ##########################################################################
    TZ      = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    NOW     = StarDate          (                                            )
    PRD     = Periode           (                                            )
    REL     = Relation          (                                            )
    NOX     = NoteItem          (                                            )
    NIT     = NameItem          (                                            )
    ##########################################################################
    PUID    = PRD . GetUuid     ( DB , PRDTAB                                )
    ID      = EVENT             [ "id"                                       ]
    TITLE   = ""
    DESCR   = ""
    ##########################################################################
    if                          ( "summary"     in EVENT                   ) :
      TITLE = EVENT             [ "summary"                                  ]
    if                          ( "description" in EVENT                   ) :
      DESCR = EVENT             [ "description"                              ]
    ##########################################################################
    SDATE   = EVENT [ "start" ] [ "dateTime" ]
    EDATE   = EVENT [ "end"   ] [ "dateTime" ]
    ##########################################################################
    SDATE   = SDATE             [ : 19                                       ]
    NOW     . fromInput         ( SDATE , TZ                                 )
    PRD     . Start = NOW . Stardate
    ##########################################################################
    EDATE   = EDATE             [ : 19                                       ]
    NOW     . fromInput         ( EDATE , TZ                                 )
    PRD     . End   = NOW . Stardate
    ##########################################################################
    PRD     . Type   = 4
    PRD     . Used   = 1
    PRD     . Realm  = 0
    PRD     . Role   = 0
    PRD     . Item   = 196833
    PRD     . States = 3
    ##########################################################################
    PRD     . UpdateColumns     ( DB , PRDTAB                                )
    ##########################################################################
    if                          ( len ( TITLE ) > 0                        ) :
      ########################################################################
      self . assureName         ( DB , PUID , TITLE , NAMTAB , 1             )
    ##########################################################################
    if                          ( len ( DESCR ) > 0                        ) :
      ########################################################################
      NOX   . Uuid      = PUID
      NOX   . Name      = "Description"
      NOX   . Prefer    = -1
      NOX   . Note      = DESCR
      NOX   . Editing           ( DB , NOXTAB                                )
    ##########################################################################
    self    . AssureVariables   ( DB                                       , \
                                  PUID                                     , \
                                  196833                                   , \
                                  "GoogleCalendar"                         , \
                                  ID                                       , \
                                  VARTAB                                     )
    ##########################################################################
    REL     . set               ( "first"  , f"{TUID}"                       )
    REL     . set               ( "second" , f"{PUID}"                       )
    REL     . setT1             ( "Tag"                                      )
    REL     . setT2             ( "Period"                                   )
    REL     . setRelation       ( "Contains"                                 )
    REL     . Append            ( DB , RELTAB                                )
    ##########################################################################
    EVENT [ "extendedProperties" ] =                                         {
      "private"                    :                                         {
        "Uuid"                     : PUID                                    ,
        "Tag"                      : TUID                                    ,
    }                                                                        }
    ##########################################################################
    self    . Calendar . Update ( calendarId = CalendarId                    ,
                                  eventId    = ID                            ,
                                  Body       = EVENT                         )
    ##########################################################################
    return True
  ############################################################################
  def AppendPeriodItem          ( self                                     , \
                                  DB                                       , \
                                  CalendarId                               , \
                                  TITLE                                    , \
                                  START                                    , \
                                  END                                      , \
                                  DESCRIPTION                              ) :
    ##########################################################################
    PRDTAB  = "`periods`"
    NOXTAB  = "`notes`"
    VARTAB  = "`variables`"
    RELTAB  = "`relations_others`"
    NAMTAB  = "`names_others`"
    ##########################################################################
    TZ      = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    TZE     = self . JSON [ "Google" ] [ "Options" ] [ "TZextend" ]
    TUID    = self . JSON [ "Google" ] [ "Groups"  ] [ CalendarId ] [ "Uuid" ]
    ##########################################################################
    NOW     = StarDate          (                                            )
    PRD     = Periode           (                                            )
    REL     = Relation          (                                            )
    NOX     = NoteItem          (                                            )
    ##########################################################################
    PUID    = PRD . GetUuid     ( DB , PRDTAB                                )
    ##########################################################################
    PRD     . Start = START
    PRD     . End   = END
    ##########################################################################
    PRD     . Type   = 4
    PRD     . Used   = 1
    PRD     . Realm  = 0
    PRD     . Role   = 0
    PRD     . Item   = 196833
    PRD     . States = 3
    ##########################################################################
    PRD     . UpdateColumns     ( DB , PRDTAB                                )
    ##########################################################################
    if                          ( len ( TITLE ) > 0                        ) :
      ########################################################################
      self . assureName         ( DB , PUID , TITLE , NAMTAB , 1             )
    ##########################################################################
    if                          ( len ( DESCRIPTION ) > 0                  ) :
      ########################################################################
      NOX   . Uuid      = PUID
      NOX   . Name      = "Description"
      NOX   . Prefer    = -1
      NOX   . Note      = DESCRIPTION
      NOX   . Editing           ( DB , NOXTAB                                )
    ##########################################################################
    REL     . set               ( "first"  , f"{TUID}"                       )
    REL     . set               ( "second" , f"{PUID}"                       )
    REL     . setT1             ( "Tag"                                      )
    REL     . setT2             ( "Period"                                   )
    REL     . setRelation       ( "Contains"                                 )
    REL     . Append            ( DB , RELTAB                                )
    ##########################################################################
    NOW     . Stardate = START
    SDTX    = NOW . toDateTimeString ( TZ )
    SDTX    = SDTX + TZE
    ##########################################################################
    NOW     . Stardate = END
    EDTX    = NOW . toDateTimeString ( TZ )
    EDTX    = EDTX + TZE
    ##########################################################################
    E       = { "kind"              : "calendar#event"                       ,
                "summary"            : TITLE                                 ,
                "description"        : DESCRIPTION                           ,
                "start"              :                                       {
                  "timeZone"         : TZ                                    ,
                  "dateTime"         : SDTX                                  ,
                }                                                            ,
                "end"                :                                       {
                  "timeZone"         : TZ                                    ,
                  "dateTime"         : EDTX                                } ,
                "extendedProperties" :                                       {
                  "private"          :                                       {
                    "Uuid"           : PUID                                  ,
                    "Tag"            : TUID                                  ,
                  }                                                          ,
                }                                                            }
    z  = self . Calendar . Append ( calendarId = CalendarId , Body = E       )
    ##########################################################################
    if                            ( not z                                  ) :
      return False
    ##########################################################################
    if                            ( "id" in z                              ) :
      ########################################################################
      ID    = z [ "id" ]
      ########################################################################
      self  . AssureVariables     ( DB                                     , \
                                    PUID                                   , \
                                    196833                                 , \
                                    "GoogleCalendar"                       , \
                                    ID                                     , \
                                    VARTAB                                   )
      ########################################################################
    return True
  ############################################################################
  def SyncEntries                  ( self , Entries                        ) :
    ##########################################################################
    if                             ( len ( Entries ) <= 0                  ) :
      return False
    ##########################################################################
    DB = Connection                (                                         )
    ##########################################################################
    if                             ( not DB . ConnectTo ( self . AITKDB )  ) :
      return
    DB . Prepare                   (                                         )
    DB . LockWrites                ( [ "`tags`"                            , \
                                      "`variables`"                        , \
                                      "`names_others`"                     ] )
    ##########################################################################
    for ID in Entries                                                        :
      ########################################################################
      UUID     = self . JSON [ "Google" ] [ "Groups" ] [ ID ] [ "Uuid"  ]
      ENTRY    = self . JSON [ "Google" ] [ "Groups" ] [ ID ] [ "Entry" ]
      ########################################################################
      UUID     = int               ( UUID                                    )
      if                           ( UUID > 0                              ) :
        ######################################################################
        self . UpdateCalendarEntry ( DB , ID , UUID , ENTRY                  )
        ######################################################################
      else                                                                   :
        ######################################################################
        self . AppendCalendarEntry ( DB , ID ,        ENTRY                  )
        ######################################################################
        NAME = ENTRY               [ "summary"                               ]
        KK   = self . JSON [ "Google" ] [ "Messages" ] [ "Appending" ]
        MSG  = f"{KK} : {NAME}"
        self . TalkTo              ( "Calendars" , MSG                       )
    ##########################################################################
    """
    NOW    . Now                       (                                     )
    BASE   = NOW    . Stardate
    for c in OriphaseSettings [ "Channels" ]                                 :
      CID   = OriphaseSettings [ "Channels" ] [ c ] [ "CalendarId" ]
      if   ( CID in OriphaseSettings [ "Watch" ]                           ) :
        p   = OriphaseSettings [ "Watch" ] [ CID ]
        if ( c == p [ "id" ]                                               ) :
          e  = OriphaseSettings [ "Watch" ] [ CID ] [ "expiration" ]
          NOW . setTime ( int ( int ( e ) / 1000 ) )
          DT = int ( NOW . Stardate ) - BASE
          if ( DT < 43200 ) :
            if ( c not in REPLACEMENTS ) :
              REPLACEMENTS . append ( c )
    if                                 ( len ( REPLACEMENTS ) > 0          ) :
      for r in REPLACEMENTS                                                  :
        CID   = OriphaseSettings [ "Channels" ] [ r ] [ "CalendarId" ]
        JSOX  = { "CalendarId" : CID }
        RemoveWatchChannel             ( JSOX                                )
        WatchChannel                   ( JSOX                                )
    """
    ##########################################################################
    DB . UnlockTables              (                                         )
    DB . Close                     (                                         )
    ##########################################################################
    return True
  ############################################################################
  def SyncCalendars               ( self , Calendars                       ) :
    ##########################################################################
    if                            ( len ( Calendars ) <= 0                 ) :
      return False
    ##########################################################################
    CHANGED       = False
    Groups        = self . JSON [ "Google" ] [ "Groups" ]
    REPLACEMENTS  = [ ]
    ##########################################################################
    for calendar in Calendars                                                :
      ########################################################################
      KIND        = calendar      [ "kind"                                   ]
      ID          = calendar      [ "id"                                     ]
      ########################################################################
      if                          ( KIND != "calendar#calendarListEntry"   ) :
        continue
      ########################################################################
      if                          ( ID not in Groups                       ) :
        ######################################################################
        ENTRY     = { "Uuid" : 0 , "Options" : {} , "Entry" : calendar }
        self      . JSON [ "Google" ] [ "Groups" ] [ ID ] = ENTRY
        CHANGED   = True
        REPLACEMENTS . append     ( ID                                       )
        ######################################################################
      else                                                                   :
        ######################################################################
        J         = self . JSON [ "Google" ] [ "Groups" ] [ ID ] [ "Entry" ]
        A         = json . dumps  ( calendar , sort_keys = True              )
        B         = json . dumps  ( J        , sort_keys = True              )
        ######################################################################
        if                        ( A != B                                 ) :
          ####################################################################
          self    . JSON [ "Google" ] [ "Groups" ] [ ID ] [ "Entry" ] = calendar
          CHANGED = True
          REPLACEMENTS . append   ( ID                                       )
    ##########################################################################
    if                            ( not CHANGED                            ) :
      return False
    ##########################################################################
    self . SyncEntries            ( REPLACEMENTS                             )
    self . ReportCalendars        (                                          )
    self . StoreJSON              (                                          )
    ##########################################################################
    return True
  ############################################################################
  def SyncPeriods                    ( self                                ) :
    ##########################################################################
    if                               ( len ( self . CurrentCalendar ) <= 0 ) :
      return False
    ##########################################################################
    G      = self . CurrentCalendar
    ##########################################################################
    if ( G not in self . JSON [ "Google" ] [ "Groups" ] )                    :
      return False
    ##########################################################################
    TUID   = self . JSON [ "Google" ] [ "Groups" ] [ G ] [ "Uuid" ]
    if                                ( TUID <= 0                          ) :
      return False
    ##########################################################################
    TZ     = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    ##########################################################################
    self   . CalendarLocker . acquire (                                      )
    ##########################################################################
    events       = self . Calendar . GetEvents                               (
      calendarId = G                                                         ,
      options    = { "timeZone" : TZ }                                       )
    ##########################################################################
    self   . CalendarLocker . release (                                      )
    ##########################################################################
    if                                ( len ( events ) <= 0                ) :
      return False
    ##########################################################################
    DB = Connection                (                                         )
    ##########################################################################
    if                             ( not DB . ConnectTo ( self . AITKDB )  ) :
      return
    DB . Prepare                   (                                         )
    DB . LockWrites                ( [ "`periods`"                         , \
                                       "`notes`"                           , \
                                       "`variables`"                       , \
                                       "`relations_others`"                , \
                                       "`names_others`"                    ] )
    ##########################################################################
    for e in events                                                          :
      ########################################################################
      APPENDING = True
      ########################################################################
      if                           ( "extendedProperties" in e             ) :
        P     = e                  [ "extendedProperties"                    ]
        if                         ( "private" in P                        ) :
          R   = P                  [ "private"                               ]
          if                       ( ( "Uuid" in R ) and ( "Tag" in R )    ) :
            APPENDING = False
      ########################################################################
      if                           ( APPENDING                             ) :
        self . AppendEventEntry    ( DB , G , TUID , e                       )
    ##########################################################################
    DB . UnlockTables              (                                         )
    DB . Close                     (                                         )
    ##########################################################################
    return True
  ############################################################################
  def ReportPeriodBrief          ( self , DB , PUID                        ) :
    ##########################################################################
    PRDTAB   = "`periods`"
    NAMTAB   = "`names_others`"
    TZ       = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    MSG      = ""
    WRONG    = f"時段編號'{PUID}'錯誤"
    NOTFOUND = "找不到時段資訊"
    ##########################################################################
    PRD      = Periode           (                                           )
    NOW      = StarDate          (                                           )
    ##########################################################################
    PRD      . Uuid = PUID
    if                           ( not PRD . ObtainsByUuid ( DB , PRDTAB ) ) :
      self   . TalkTo            ( "Calendars" , NOTFOUND                    )
      return False
    ##########################################################################
    NX       = Naming            ( DB , NAMTAB , PUID , self . Locality      )
    ##########################################################################
    NOW      . Stardate = PRD . Start
    SDT      = NOW . toLongDateTimeString ( TZ , "%Y/%m/%d" , "%H:%M:%S"     )
    ##########################################################################
    NOW      . Stardate = PRD . End
    EDT      = NOW . toLongDateTimeString ( TZ , "%Y/%m/%d" , "%H:%M:%S"     )
    ##########################################################################
    PXID     = PRD . toString    (                                           )
    MSG      = f"時段 : {NX}\n編號 : {PXID}\n開始時間 : {SDT}\n結束時間 : {EDT}"
    ##########################################################################
    self   . TalkTo              ( "Calendars" , MSG                         )
    ##########################################################################
    return True
  ############################################################################
  def AssignCurrentPeriod         ( self , PERIOD                          ) :
    ##########################################################################
    PERIOD   = f"{PERIOD}"
    WRONG    = f"時段編號'{PERIOD}'錯誤"
    PUID     = 0
    ##########################################################################
    PRD      = Periode            (                                          )
    ##########################################################################
    if                            ( len ( PERIOD ) == 12                   ) :
      ########################################################################
      PUID   = PRD . fromString   ( PERIOD                                   )
      if                          ( PUID <= 0                              ) :
        self . TalkTo             ( "Calendars" , WRONG                      )
        return False
      ########################################################################
    elif                          ( len ( PERIOD ) == 19                   ) :
      ########################################################################
      try                                                                    :
        PUID = int                ( PERIOD                                   )
        PRD  . Uuid = PUID
      except                                                                 :
        ######################################################################
        self . TalkTo             ( "Calendars" , WRONG                      )
        return False
      ########################################################################
    else                                                                     :
      try                                                                    :
        PUID = int                ( PERIOD                                   )
        PUID = int                ( PUID + 3500000000000000000               )
        PRD  . Uuid = PUID
      except                                                                 :
        ######################################################################
        self . TalkTo             ( "Calendars" , WRONG                      )
        return False
    ##########################################################################
    DB       = Connection         (                                          )
    ##########################################################################
    if                            ( not DB . ConnectTo ( self . AITKDB )   ) :
      return False
    DB       . Prepare            (                                          )
    ##########################################################################
    if                            ( self . ReportPeriodBrief ( DB , PUID ) ) :
      self . CurrentPeriod = PUID
      self . JSON [ "Google" ] [ "Options" ] [ "Period" ] = PUID
      self . StoreJSON            (                                          )
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    return True
  ############################################################################
  def ModifyCurrentPeriod        ( self                                    ) :
    ##########################################################################
    if                           ( not self . hasCurrentCalendarId     ( ) ) :
      return False
    ##########################################################################
    if                           ( not self . hasCurrentPeriod         ( ) ) :
      return False
    ##########################################################################
    if                           ( not self . hasCompletePeriodDetails ( ) ) :
      return False
    ##########################################################################
    PRDTAB  = "`periods`"
    VARTAB  = "`variables`"
    NOXTAB  = "`notes`"
    NAMTAB  = "`names_others`"
    ##########################################################################
    PUID    = self . CurrentPeriod
    GID     = ""
    ##########################################################################
    TZ      = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    TZE     = self . JSON [ "Google" ] [ "Options" ] [ "TZextend" ]
    ##########################################################################
    NOW     = StarDate          (                                            )
    PRD     = Periode           (                                            )
    NOX     = NoteItem          (                                            )
    ##########################################################################
    DB      = Connection         (                                           )
    ##########################################################################
    if                           ( not DB . ConnectTo ( self . AITKDB )    ) :
      return False
    DB      . Prepare            (                                           )
    ##########################################################################
    DB      . LockWrites         ( [ PRDTAB , VARTAB , NOXTAB , NAMTAB     ] )
    ##########################################################################
    PRD     . Uuid = PUID
    ##########################################################################
    if                           ( PRD . ObtainsByUuid ( DB , PRDTAB )     ) :
      ########################################################################
      PRD   . Start = self . CurrentStart
      PRD   . End   = self . CurrentEnd
      ########################################################################
      self  . assureName         ( DB                                      , \
                                   PUID                                    , \
                                   self . CurrentTitle                     , \
                                   NAMTAB                                  , \
                                   1                                         )
      ########################################################################
      if                         ( len ( self . CurrentDescription ) > 0   ) :
        ######################################################################
        NOX . Uuid      = PUID
        NOX . Name      = "Description"
        NOX . Prefer    = -1
        NOX . Note      = self . CurrentDescription
        NOX . Editing            ( DB , NOXTAB                               )
      ########################################################################
      GID   = self . GetVariable ( DB                                      , \
                                   PUID                                    , \
                                   196833                                  , \
                                   "GoogleCalendar"                        , \
                                   VARTAB                                    )
      ########################################################################
      if                         ( ( GID != None ) and ( len ( GID ) > 0 ) ) :
        ######################################################################
        self . CalendarLocker . acquire (                                    )
        ######################################################################
        Z    = False
        E    = self . Calendar . Get    ( self . CurrentCalendar , GID       )
        if                       ( E != False                              ) :
          ####################################################################
          NOW  . Stardate = PRD . Start
          SDTX            = NOW . toDateTimeString ( TZ )
          SDTX            = SDTX + TZE
          ####################################################################
          NOW  . Stardate = PRD . End
          EDTX            = NOW . toDateTimeString ( TZ )
          EDTX            = EDTX + TZE
          ####################################################################
          E [ "summary"                    ] = self . CurrentTitle
          E [ "description"                ] = self . CurrentDescription
          E [ "start"       ] [ "timeZone" ] = TZ
          E [ "start"       ] [ "dateTime" ] = SDTX
          E [ "end"         ] [ "timeZone" ] = TZ
          E [ "end"         ] [ "dateTime" ] = EDTX
          ####################################################################
          Z = self . Calendar . Update ( self . CurrentCalendar , GID , Body = E )
        ######################################################################
        self  . CalendarLocker . release (                                   )
        ######################################################################
        if                       ( Z != False                              ) :
          ####################################################################
          CDATE = Z [ "created" ]
          MDATE = Z [ "updated" ]
          ####################################################################
          CDATE = CDATE          [ : 19                                      ]
          NOW   . fromInput      ( CDATE , TZ                                )
          PRD   . Creation = NOW . Stardate
          ####################################################################
          MDATE = MDATE          [ : 19                                      ]
          NOW   . fromInput      ( MDATE , TZ                                )
          PRD   . Modified = NOW . Stardate
      ########################################################################
      PRD   . UpdateColumns      ( DB , PRDTAB                               )
    ##########################################################################
    DB      . UnlockTables       (                                           )
    DB      . Close              (                                           )
    ##########################################################################
    return True
  ############################################################################
  def InventoryCurrentPeriods    ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def ReportEventBrief           ( self , DB , PUID                        ) :
    ##########################################################################
    EVNTAB   = "`events`"
    NAMTAB   = "`names_others`"
    MSG      = ""
    WRONG    = f"事件編號'{PUID}'錯誤"
    NOTFOUND = "找不到事件資訊"
    ##########################################################################
    NX       = Naming            ( DB , NAMTAB , PUID , self . Locality      )
    if                           ( len ( NX ) <= 0                         ) :
      self   . TalkTo            ( "Calendars" , WRONG                       )
      return False
    ##########################################################################
    MSG      = f"事件 : {NX}\n編號 : {PUID}"
    ##########################################################################
    self   . TalkTo              ( "Calendars" , MSG                         )
    ##########################################################################
    return True
  ############################################################################
  def AssignCurrentEvent          ( self , EVENT                           ) :
    ##########################################################################
    EVENT    = f"{EVENT}"
    WRONG    = f"事件編號'{EVENT}'錯誤"
    PUID     = 0
    if                            ( len ( EVENT ) == 19                    ) :
      ########################################################################
      try                                                                    :
        PUID = int                ( EVENT                                    )
      except                                                                 :
        ######################################################################
        self . TalkTo             ( "Calendars" , WRONG                      )
        return False
      ########################################################################
    else                                                                     :
      try                                                                    :
        PUID = int                ( EVENT                                    )
        PUID = int                ( PUID + 7302000000000000000               )
      except                                                                 :
        ######################################################################
        self . TalkTo             ( "Calendars" , WRONG                      )
        return False
    ##########################################################################
    DB       = Connection         (                                          )
    ##########################################################################
    if                            ( not DB . ConnectTo ( self . AITKDB )   ) :
      return False
    DB       . Prepare            (                                          )
    ##########################################################################
    if                            ( self . ReportEventBrief ( DB , PUID ) ) :
      self . CurrentEvent       = PUID
      self . JSON [ "Google" ] [ "Options" ] [ "Event"  ] = PUID
      self . StoreJSON            (                                          )
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    return True
  ############################################################################
  def ModifyCurrentEvent         ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def InventoryCurrentEvents     ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def ReportTaskBrief            ( self , DB , PUID                        ) :
    ##########################################################################
    TSKTAB   = "`tasks`"
    NAMTAB   = "`names_others`"
    MSG      = ""
    WRONG    = f"任務編號'{PUID}'錯誤"
    NOTFOUND = "找不到任務資訊"
    ##########################################################################
    NX       = Naming            ( DB , NAMTAB , PUID , self . Locality      )
    if                           ( len ( NX ) <= 0                         ) :
      self   . TalkTo            ( "Calendars" , WRONG                       )
      return False
    ##########################################################################
    MSG      = f"任務 : {NX}\n編號 : {PUID}"
    ##########################################################################
    self   . TalkTo              ( "Calendars" , MSG                         )
    ##########################################################################
    return True
  ############################################################################
  def AssignCurrentTask           ( self , TASK                            ) :
    ##########################################################################
    TASK     = f"{TASK}"
    WRONG    = f"任務編號'{TASK}'錯誤"
    PUID     = 0
    if                            ( len ( TASK ) == 19                     ) :
      ########################################################################
      try                                                                    :
        PUID = int                ( TASK                                     )
      except                                                                 :
        ######################################################################
        self . TalkTo             ( "Calendars" , WRONG                      )
        return False
      ########################################################################
    else                                                                     :
      try                                                                    :
        PUID = int                ( TASK                                     )
        PUID = int                ( PUID + 7303000000000000000               )
      except                                                                 :
        ######################################################################
        self . TalkTo             ( "Calendars" , WRONG                      )
        return False
    ##########################################################################
    DB       = Connection         (                                          )
    ##########################################################################
    if                            ( not DB . ConnectTo ( self . AITKDB )   ) :
      return False
    DB       . Prepare            (                                          )
    ##########################################################################
    if                            ( self . ReportTaskBrief ( DB , PUID )   ) :
      self . CurrentTask        = PUID
      self . JSON [ "Google" ] [ "Options" ] [ "Task"   ] = PUID
      self . StoreJSON            (                                          )
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    return True
  ############################################################################
  def ModifyCurrentTask          ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def InventoryCurrentTasks      ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def ReportCurrentPeriod          ( self                                  ) :
    ##########################################################################
    if                             ( not self . hasCurrentPeriod ( )       ) :
      return False
    ##########################################################################
    DB = Connection                (                                         )
    ##########################################################################
    if                             ( not DB . ConnectTo ( self . AITKDB )  ) :
      return
    DB       . Prepare             (                                         )
    ##########################################################################
    self     . ReportPeriodBrief   ( DB , self . CurrentPeriod               )
    ##########################################################################
    DB       . Close               (                                         )
    ##########################################################################
    return True
  ############################################################################
  def AssignStartTime              ( self , DTIME                          ) :
    ##########################################################################
    TZ       = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    NOW      = StarDate            (                                         )
    NOW      . fromInput           ( DTIME , TZ                              )
    ##########################################################################
    self . CurrentStart = NOW . Stardate
    ##########################################################################
    if                             ( NOW . Stardate <= 0                   ) :
      return True
    ##########################################################################
    SDT      = NOW . toLongDateTimeString ( TZ , "%Y/%m/%d" , "%H:%M:%S"     )
    MSG      = f"開始時間 : {SDT}"
    self . TalkTo                  ( "Calendars" , MSG                       )
    ##########################################################################
    return True
  ############################################################################
  def AssignEndTime                ( self , DTIME                          ) :
    ##########################################################################
    TZ       = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    NOW      = StarDate            (                                         )
    NOW      . fromInput           ( DTIME , TZ                              )
    ##########################################################################
    self . CurrentEnd = NOW . Stardate
    ##########################################################################
    if                             ( NOW . Stardate <= 0                   ) :
      return True
    ##########################################################################
    EDT      = NOW . toLongDateTimeString ( TZ , "%Y/%m/%d" , "%H:%M:%S"     )
    MSG      = f"結束時間 : {EDT}"
    self . TalkTo                  ( "Calendars" , MSG                       )
    ##########################################################################
    return True
  ############################################################################
  def ReportCurrentSettings        ( self                                  ) :
    ##########################################################################
    NAMTAB   = "`names_others`"
    TZ       = self . JSON [ "Google" ] [ "Options" ] [ "TimeZone" ]
    TITLE    = self . CurrentTitle
    DESCRIPT = self . CurrentDescription
    MSG      = ""
    ##########################################################################
    NOW      = StarDate            (                                         )
    ##########################################################################
    DB       = Connection          (                                         )
    ##########################################################################
    if                             ( not DB . ConnectTo ( self . AITKDB )  ) :
      return False
    DB       . Prepare             (                                         )
    ##########################################################################
    if                             ( self . CurrentStart > 0               ) :
      NOW    . Stardate = self . CurrentStart
      SDT    = NOW . toLongDateTimeString ( TZ , "%Y/%m/%d" , "%H:%M:%S"     )
      MSG    = f"開始時間 : {SDT}"
    ##########################################################################
    if                             ( self . CurrentEnd   > 0               ) :
      NOW    . Stardate = self . CurrentEnd
      EDT    = NOW . toLongDateTimeString ( TZ , "%Y/%m/%d" , "%H:%M:%S"     )
      MSGK   = f"結束時間 : {EDT}"
      if                           ( len ( MSG ) > 0                       ) :
        MSG  = f"{MSG}\n{MSGK}"
      else                                                                   :
        MSG = MSGK
    ##########################################################################
    if                             ( len ( TITLE ) > 0                     ) :
      TSGK  = f"標題 : \n{TITLE}"
      if                           ( len ( MSG ) > 0                       ) :
        MSG  = f"{MSG}\n{TSGK}"
      else                                                                   :
        MSG = TSGK
    ##
    ##########################################################################
    if                             ( len ( DESCRIPT ) > 0                  ) :
      DSGK  = f"內容 : \n{DESCRIPT}"
      if                           ( len ( MSG ) > 0                       ) :
        MSG = f"{MSG}\n{DSGK}"
      else                                                                   :
        MSG = DSGK
    ##########################################################################
    if                             ( self . CurrentTask > 0                ) :
      TUID  = self . CurrentTask
      NX    = Naming               ( DB  , NAMTAB , TUID , self . Locality   )
      if                           ( len ( NX ) > 0                        ) :
        TSGK  = f"任務標題 : {NX}\n任務編號 : {TUID}"
        if                         ( len ( MSG ) > 0                       ) :
          MSG = f"{MSG}\n{TSGK}"
        else                                                                 :
          MSG = TSGK
    ##########################################################################
    if                             ( self . CurrentEvent > 0               ) :
      TUID  = self . CurrentEvent
      NX    = Naming               ( DB  , NAMTAB , TUID , self . Locality   )
      if                           ( len ( NX ) > 0                        ) :
        TSGK  = f"事件標題 : {NX}\n事件編號 : {TUID}"
        if                         ( len ( MSG ) > 0                       ) :
          MSG = f"{MSG}\n{TSGK}"
        else                                                                 :
          MSG = TSGK
    ##########################################################################
    if                             ( self . CurrentPeriod > 0              ) :
      TUID  = self . CurrentPeriod
      NX    = Naming               ( DB  , NAMTAB , TUID , self . Locality   )
      if                           ( len ( NX ) > 0                        ) :
        TSGK  = f"時段標題 : {NX}\n時段編號 : {TUID}"
        if                         ( len ( MSG ) > 0                       ) :
          MSG = f"{MSG}\n{TSGK}"
        else                                                                 :
          MSG = TSGK
    ##########################################################################
    self . TalkTo                  ( "Calendars" , MSG                       )
    ##########################################################################
    DB   . Close                   (                                         )
    ##########################################################################
    return True
  ############################################################################
  def AppendCurrentPeriod     ( self                                       ) :
    ##########################################################################
    if                           ( not self . hasCompletePeriodDetails ( ) ) :
      return False
    ##########################################################################
    DB     = Connection       (                                              )
    ##########################################################################
    if                        ( not DB . ConnectTo ( self . AITKDB )       ) :
      return
    DB     . Prepare          (                                              )
    ##########################################################################
    self   . AppendPeriodItem ( DB                                         , \
                                self . CurrentCalendar                     , \
                                self . CurrentTitle                        , \
                                self . CurrentStart                        , \
                                self . CurrentEnd                          , \
                                self . CurrentDescription                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    return True
  ############################################################################
  def AppendCurrentEvent      ( self                                       ) :
    ##########################################################################
    FAIL   = "資訊不足以新增事件"
    ##########################################################################
    if                        ( len ( self . CurrentTitle ) <= 0           ) :
      self . TalkTo           ( "Calendars" , FAIL                           )
      return False
    ##########################################################################
    DB     = Connection       (                                              )
    ##########################################################################
    if                        ( not DB . ConnectTo ( self . AITKDB )       ) :
      return
    DB     . Prepare          (                                              )
    ##########################################################################
    EVNTAB = "`events`"
    NAMTAB = "`names_others`"
    ##########################################################################
    PUID   = DB . LastUuid    ( EVNTAB , "uuid" , 7302000000000000000        )
    if                        ( PUID > 0                                   ) :
      DB   . AddUuid          ( EVNTAB , PUID , 196833                       )
      self . assureName       ( DB , PUID , self . CurrentTitle , NAMTAB , 1 )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    return True
  ############################################################################
  def AppendCurrentTask       ( self                                       ) :
    ##########################################################################
    FAIL   = "資訊不足以新增任務"
    ##########################################################################
    if                        ( len ( self . CurrentTitle ) <= 0           ) :
      self . TalkTo           ( "Calendars" , FAIL                           )
      return False
    ##########################################################################
    DB     = Connection       (                                              )
    ##########################################################################
    if                        ( not DB . ConnectTo ( self . AITKDB )       ) :
      return
    DB     . Prepare          (                                              )
    ##########################################################################
    TSKTAB = "`tasks`"
    NAMTAB = "`names_others`"
    ##########################################################################
    PUID   = DB . LastUuid    ( TSKTAB , "uuid" , 7303000000000000000        )
    if                        ( PUID > 0                                   ) :
      DB   . AddUuid          ( TSKTAB , PUID , 196833                       )
      self . assureName       ( DB , PUID , self . CurrentTitle , NAMTAB , 1 )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    return True
  ############################################################################
  def RelateTaskAndPeriod     ( self                                       ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def RelateEventAndPeriod    ( self                                       ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def RelateTaskAndEvent      ( self                                       ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def ReportCurrentGooglePeriod ( self                                     ) :
    ##########################################################################
    if                          ( not self . hasCurrentCalendarId ( )      ) :
      return False
    ##########################################################################
    if                          ( not self . hasCurrentPeriod     ( )      ) :
      return False
    ##########################################################################
    PUID   = self . CurrentPeriod
    ##########################################################################
    DB     = Connection         (                                            )
    ##########################################################################
    if                          ( not DB . ConnectTo ( self . AITKDB )     ) :
      return False
    DB     . Prepare            (                                            )
    ##########################################################################
    VARTAB = "`variables`"
    ##########################################################################
    GID    = self . GetVariable ( DB                                       , \
                                  PUID                                     , \
                                  196833                                   , \
                                  "GoogleCalendar"                         , \
                                  VARTAB                                     )
    ##########################################################################
    DB     . Close              (                                            )
    ##########################################################################
    if                          ( ( GID != None ) and ( len ( GID ) > 0 )  ) :
      ########################################################################
      self . CalendarLocker . acquire (                                      )
      ########################################################################
      E    = self . Calendar . Get    ( self . CurrentCalendar , GID         )
      ########################################################################
      self . CalendarLocker . release (                                      )
      ########################################################################
      if                        ( E != False                               ) :
        T  = json . dumps       ( E                                          )
        self . TalkTo           ( "Calendars" , T                            )
    ##########################################################################
    return True
  ############################################################################
  def GoogleMonitor                     ( self                             ) :
    ##########################################################################
    self . addWorking                   (                                    )
    ##########################################################################
    CONNECTED       = False
    ORIPHASE        = self . JSON [ "Calendars" ] [ "OAuth"  ]
    GTOKENS         = self . JSON [ "Calendars" ] [ "Pickle" ]
    GJSON           = { "Secrets" : ORIPHASE , "Authorized" : GTOKENS        }
    self . Calendar = GCalendar         ( GJSON                              )
    ##########################################################################
    NOW             = StarDate          (                                    )
    NOW             . Now               (                                    )
    SDT             = int ( NOW . Stardate ) - 1
    UDT             = 0
    ##########################################################################
    while                               ( self . Running                   ) :
      ########################################################################
      NOW    . Now                      (                                    )
      if                                ( int ( NOW . Stardate ) < SDT     ) :
        time . sleep                    ( 0.1                                )
        continue
      ########################################################################
      if                                ( NOW . Stardate > UDT             ) :
        CONNECTED = False
      ########################################################################
      if                                ( not CONNECTED                    ) :
        ######################################################################
        self . CalendarLocker . acquire (                                    )
        if                              ( self . Calendar . Connect ( )    ) :
          ####################################################################
          CONNECTED = True
          NOW       . Now               (                                    )
          UDT       = NOW . Stardate
          UDT       = int               ( UDT                                )
          UDT       = UDT +             ( 86400 * 7                          )
        ######################################################################
        self . CalendarLocker . release (                                    )
        ######################################################################
        if                              ( not CONNECTED                    ) :
          continue
        else                                                                 :
          ####################################################################
          self . ReportCurrentCalendar  (                                    )
      ########################################################################
      SDT    = int ( NOW . Stardate ) + 600
      ########################################################################
      self   . CalendarLocker . acquire (                                    )
      Calendars = self . Calendar . GetCalendars (                           )
      ########################################################################
      self   . SyncCalendars            ( Calendars                          )
      ########################################################################
      self   . CalendarLocker . release (                                    )
    ##########################################################################
    self . removeWorking                (                                    )
    ##########################################################################
    return
  ############################################################################
  def Start                      ( self                                    ) :
    ##########################################################################
    self . Running = True
    threading . Thread           ( target = self . GoogleMonitor ) . start ( )
    ##########################################################################
    return True
  ############################################################################
  def Stop                       ( self                                    ) :
    ##########################################################################
    self . Running = False
    while                        ( self . Working > 0                      ) :
      time . sleep               ( 0.1                                       )
    ##########################################################################
    return True
##############################################################################
