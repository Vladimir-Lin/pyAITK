# -*- coding: utf-8 -*-
##############################################################################
## Apple iCloud Calendar
##############################################################################
import os
import sys
import time
import datetime
import pytz
import requests
import threading
import shutil
import json
import icalendar
import caldav
##############################################################################
from . StarDate import StarDate
from . Periode  import Periode
##############################################################################
## 蘋果行事曆物件
##############################################################################
class Apple              (                                                 ) :
  ############################################################################
  def __init__           ( self , URL , DSID , USERNAME , PASSWORD         ) :
    ##########################################################################
    self . MasterURL = URL
    self . DSID      = DSID
    self . Username  = USERNAME
    self . Password  = PASSWORD
    self . Client    = None
    self . Principal = None
    self . Calendars =   [                                                   ]
    ##########################################################################
    self . CURL      = f"{URL}/{DSID}/calendars"
    self . PURL      = f"{URL}/{DSID}/principal"
    ##########################################################################
    ## self . PRODID    = "-//caldav.icloud.com//CALDAVJ 2206B560//EN"
    self . PRODID    = "-//AITK Scheduler//Python 2022-01-21//TW"
    self . TZ        = "Asia/Taipei"
    ##########################################################################
    return
  ############################################################################
  def __del__           ( self                                             ) :
    return
  ############################################################################
  def assureString       ( self , pb                                       ) :
    ##########################################################################
    BB   = pb
    ##########################################################################
    try                                                                      :
      BB = BB . decode   ( "utf-8"                                           )
    except                                                                   :
      pass
    ##########################################################################
    return BB
  ############################################################################
  def GetEventURL       ( self , CalendarId , EventId                      ) :
    URL = self . CURL
    return f"{URL}/{CalendarId}/{EventId}.ics"
  ############################################################################
  def FetchCalendars    ( self                                             ) :
    ##########################################################################
    self . Client    = caldav . DAVClient ( self . CURL                    , \
                                            username = self . Username     , \
                                            password = self . Password       )
    if                  ( self . Client    in [ False , None ]             ) :
      return False
    ##########################################################################
    self . Principal = caldav . Principal ( client = self . Client         , \
                                            url    = self . PURL             )
    ##########################################################################
    if                  ( self . Principal in [ False , None ]             ) :
      return False
    ##########################################################################
    try                                                                      :
      CAL            = self . Principal . calendars (                        )
    except                                                                   :
      return False
    ##########################################################################
    if                  ( CAL              in [ False , None ]             ) :
      return False
    ##########################################################################
    self . Calendars = CAL
    ##########################################################################
    return True
  ############################################################################
  def CalendarId        ( self , calendar                                  ) :
    ##########################################################################
    if                  ( calendar in [ False , None ]                     ) :
      return ""
    ##########################################################################
    URL = str           ( calendar . url                                     )
    if                  ( len ( URL ) <= 0                                 ) :
      return ""
    ##########################################################################
    if                  ( self . CURL not in URL                           ) :
      return ""
    ##########################################################################
    URL = URL . replace ( self . CURL , ""                                   )
    URL = URL . replace ( "/"         , ""                                   )
    ##########################################################################
    return URL
  ############################################################################
  def FindCalendar           ( self , CID                                  ) :
    ##########################################################################
    if                       ( self . Calendars in [ False , None ]        ) :
      return None
    ##########################################################################
    for calendar in self . Calendars                                         :
      ########################################################################
      ID = self . CalendarId ( calendar                                      )
      if                     ( ID == CID                                   ) :
        return calendar
    ##########################################################################
    return None
  ############################################################################
  def EventFromICalData                  ( self , iCalData                 ) :
    return icalendar . Event . from_ical ( iCalData                          )
  ############################################################################
  def GetEventBrief                           ( self , event               ) :
    ##########################################################################
    TITLE     = ""
    UID       = ""
    PUID      = ""
    ##########################################################################
    for key , value in event . property_items (                            ) :
      ########################################################################
      K       = key . lower                   (                              )
      if                                      ( K in [ "summary"         ] ) :
        TITLE = self . assureString           ( str ( value                ) )
      elif                                    ( K in [ "uid"             ] ) :
        UID   = self . assureString           ( str ( value                ) )
      elif                                    ( K in [ "class"           ] ) :
        PUID  = self . assureString           ( str ( value                ) )
    ##########################################################################
    if                                        ( len ( UID ) > 0            ) :
      return                                  { "Id"     : UID             , \
                                                "Name"   : TITLE           , \
                                                "Period" : PUID              }
    ##########################################################################
    return None
  ############################################################################
  def LocateEvent                    ( self , calendar , UID               ) :
    ##########################################################################
    ## CID = self . CalendarId          ( calendar                              )
    ## URL = self . GetEventURL         ( CID , UID                             )
    ## try                                                                      :
    ##   E = calendar . event_by_url    ( URL                                   )
    ##   return E
    ## except                                                                   :
    ##   return None
    for event in calendar . events   (                                     ) :
      ########################################################################
      evt = self . EventFromICalData ( event . data                          )
      J   = self . GetEventBrief     ( evt                                   )
      if                             ( J [ "Id" ] == UID                   ) :
        return event
    ##########################################################################
    return None
  ############################################################################
  def FindEvent                      ( self , calendar , UID               ) :
    ##########################################################################
    ## CID = self . CalendarId          ( calendar                              )
    ## URL = self . GetEventURL         ( CID , UID                             )
    ## try                                                                      :
    ##   E = calendar . event_by_url    ( URL                                   )
    ##   return E
    ## except                                                                   :
    ##   return None
    for event in calendar . events   (                                     ) :
      ########################################################################
      evt = self . EventFromICalData ( event . data                          )
      J   = self . GetEventBrief     ( evt                                   )
      if                             ( J [ "Id" ] == UID                   ) :
        return evt
    ##########################################################################
    return None
  ############################################################################
  def GetEvents                           ( self , calendar                ) :
    ##########################################################################
    EVENTs     =                          [                                  ]
    ##########################################################################
    for event in calendar . events        (                                ) :
      ########################################################################
      evt      = self . EventFromICalData ( event . data                     )
      J        = self . GetEventBrief     ( evt                              )
      ########################################################################
      if                                  ( J not in [ False , None ]      ) :
        EVENTs . append                   ( J                                )
    ##########################################################################
    return EVENTs
  ############################################################################
  def iCalFromPeriod             ( self , PERIOD                           ) :
    ##########################################################################
    tzx   = pytz . timezone      ( self . TZ                                 )
    NOW   = StarDate             (                                           )
    ##########################################################################
    NOW   . Stardate = PERIOD . Start
    DTS   = NOW . toDateTime     ( self . TZ                                 )
    ##########################################################################
    NOW   . Stardate = PERIOD . End
    ETS   = NOW . toDateTime     ( self . TZ                                 )
    ##########################################################################
    NAME  = PERIOD . getProperty ( "Name"                                    )
    DESC  = PERIOD . getProperty ( "Description"                             )
    CID   = PERIOD . getProperty ( "Calendar"                                )
    EID   = PERIOD . getProperty ( "Event"                                   )
    ##########################################################################
    iCal  = icalendar . Calendar (                                           )
    iCal  . add                  ( "PRODID"      , self . PRODID             )
    iCal  . add                  ( "VERSION"     , "1.0"                     )
    iCal  . add                  ( "CALSCALE"    , "GREGORIAN"               )
    ##########################################################################
    evt   = icalendar . Event    (                                           )
    evt   . add                  ( "CLASS"       , PERIOD . Uuid             )
    evt   . add                  ( "SUMMARY"     , NAME                      )
    evt   . add                  ( "DTSTART"     , DTS                       )
    evt   . add                  ( "DTEND"       , ETS                       )
    ##########################################################################
    if                           ( len ( DESC ) > 0                        ) :
      ########################################################################
      evt . add                  ( "DESCRIPTION" , DESC                      )
    ##########################################################################
    if                           ( len ( EID ) > 0                         ) :
      ########################################################################
      evt . add                  ( "UID" , EID                               )
    ##########################################################################
    iCal  . add_component        ( evt                                       )
    ##########################################################################
    return iCal
  ############################################################################
  def iCalUpdateFromPeriod           ( self , iCal , PERIOD                ) :
    ##########################################################################
    NCAL     = self . iCalFromPeriod ( PERIOD                                )
    ##########################################################################
    for c in iCal . subcomponents                                            :
      ########################################################################
      n      = c . name
      n      = n . lower             (                                       )
      ########################################################################
      if                             ( n not in [ "vevent" , "vcalendar" ] ) :
        ######################################################################
        NCAL . add_component         ( c                                     )
    ##########################################################################
    return NCAL
##############################################################################
