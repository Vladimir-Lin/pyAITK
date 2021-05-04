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
from   AITK  . Documents  . Name       import Name       as NameItem
from   AITK  . Documents  . Name       import Naming     as Naming
from   AITK  . Documents  . Notes      import Notes      as NoteItem
from   AITK  . Documents  . Variables  import Variables  as VariableItem
##############################################################################
from   AITK  . Database   . Connection import Connection as Connection
##############################################################################
from   AITK  . Calendars  . StarDate   import StarDate   as StarDate
from   AITK  . Calendars  . Periode    import Periode    as Periode
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
  def ReportCurrentCalendar   ( self                                       ) :
    ##########################################################################
    if                        ( len ( self . CurrentCalendar ) <= 0        ) :
      return
    ##########################################################################
    G      = self . CurrentCalendar
    ##########################################################################
    if                        ( G in self . JSON [ "Google" ] [ "Groups" ] ) :
      ########################################################################
      NAME = self . JSON [ "Google" ] [ "Groups" ] [ G ] [ "summary" ]
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
        NAME = Groups [ G ] [ "summary" ]
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
      NAME  = Groups [ K ] [ "summary" ]
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
  def SyncCalendars               ( self , Calendars                       ) :
    ##########################################################################
    if                            ( len ( Calendars ) <= 0                 ) :
      return False
    ##########################################################################
    CHANGED       = False
    Groups        = self . JSON [ "Google" ] [ "Groups" ]
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
        self      . JSON [ "Google" ] [ "Groups" ] [ ID ] = calendar
        CHANGED   = True
        ######################################################################
      else                                                                   :
        ######################################################################
        J         = self . JSON [ "Google" ] [ "Groups" ] [ ID ]
        A         = json . dumps  ( calendar , sort_keys = True              )
        B         = json . dumps  ( J        , sort_keys = True              )
        ######################################################################
        if                        ( A != B                                 ) :
          ####################################################################
          self    . JSON [ "Google" ] [ "Groups" ] [ ID ] = calendar
          CHANGED = True
    ##########################################################################
    if                            ( CHANGED                                ) :
      ########################################################################
      self . ReportCalendars      (                                          )
      self . StoreJSON            (                                          )
    ##########################################################################
    ## REPLACEMENTS = [ ]
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
    ##########################################################################
    while                               ( self . Running                   ) :
      ########################################################################
      NOW    . Now                      (                                    )
      if                                ( int ( NOW . Stardate ) < SDT     ) :
        time . sleep                    ( 0.1                                )
        continue
      ########################################################################
      if                                ( not CONNECTED                    ) :
        ######################################################################
        self . CalendarLocker . acquire (                                    )
        if                              ( self . Calendar . Connect ( )    ) :
          CONNECTED = True
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
