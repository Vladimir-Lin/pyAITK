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
    self . DebugLogger     = None
    self . Talk            = None
    self . Beau            = "Scheduler"
    self . JSON            = { }
    self . Calendar        = None
    self . Running         = False
    self . Working         = 0
    self . Locality        = 1002
    self . CalendarLocker  = threading . Lock ( )
    ##########################################################################
    self . Configure   (        jsonFile                                     )
    ##########################################################################
    self . AITKDB          = self . JSON [ "Database" ]
    self . CurrentCalendar = self . JSON [ "Google" ] [ "Options" ] [ "Pick" ]
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
  def ReportCurrentCalendar   ( self                                       ) :
    ##########################################################################
    if                        ( len ( self . CurrentCalendar ) <= 0        ) :
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
  def ReportCurrentEvents            ( self                                ) :
    ##########################################################################
    if                               ( len ( self . CurrentCalendar ) <= 0 ) :
      return False
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
    VAX     = VariableItem      (                                            )
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
      NIT   . Uuid      = PUID
      NIT   . Locality  = self . Locality
      NIT   . Priority  = 0
      NIT   . Relevance = 0
      NIT   . Flags     = 1
      NIT   . Name      = TITLE
      NIT   . Editing           ( DB , NAMTAB                                )
    ##########################################################################
    if                          ( len ( DESCR ) > 0                        ) :
      ########################################################################
      NOX   . Uuid      = PUID
      NOX   . Name      = "Description"
      NOX   . Prefer    = -1
      NOX   . Note      = DESCR
      NOX   . Editing           ( DB , NOXTAB                                )
    ##########################################################################
    VAX     . Uuid      = PUID
    VAX     . Type      = 196833
    VAX     . Name      = "GoogleCalendar"
    VAX     . Value     = ID
    VAX     . AssureValue       ( DB , VARTAB                                )
    ##########################################################################
    REL     . set               ( "first"  , TUID                            )
    REL     . set               ( "second" , PUID                            )
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
  def SyncEvents                     ( self                                ) :
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
      self . AppendEventEntry      ( DB , G , TUID , e                       )
    ##########################################################################
    DB . UnlockTables              (                                         )
    DB . Close                     (                                         )
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
