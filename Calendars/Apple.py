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
    return
  ############################################################################
  def __del__           ( self                                             ) :
    return
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
    if                  ( self . Principal in [ False , None ]             ) :
      return False
    ##########################################################################
    CAL              = self . Principal . calendars (                        )
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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################