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
    self . DebugLogger = None
    self . Talk        = None
    self . Beau        = "Scheduler"
    self . JSON        = { }
    ##########################################################################
    self . Configure   (        jsonFile                                     )
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
##############################################################################
