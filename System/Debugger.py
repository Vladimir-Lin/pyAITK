# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import datetime
import logging
import requests
import threading

def GetDebuggerLevel ( DBG ) :
  LEVEL     = logging . NOTSET
  if   ( "NOTSET"     == DBG ) :
    LEVEL = logging . NOTSET
  elif   ( "DEBUG"    == DBG ) :
    LEVEL = logging . DEBUG
  elif   ( "INFO"     == DBG ) :
    LEVEL = logging . INFO
  elif   ( "WARNING"  == DBG ) :
    LEVEL = logging . WARNING
  elif   ( "ERROR"    == DBG ) :
    LEVEL = logging . ERROR
  elif   ( "CRITICAL" == DBG ) :
    LEVEL = logging . CRITICAL
  return LEVEL

def ChangeDebuggerLevel        ( DBG   ) :
  LEVEL  = GetDebuggerLevel    ( DBG   )
  Logger = logging . getLogger (       )
  Logger . setLevel            ( LEVEL )

def ConfigureDebugger ( settings = { } ) :
  DBG       = "NOTSET"
  LOG       = ""
  isConsole = False
  LEVEL     = logging . NOTSET
  if ( "Debug" in settings ) :
    DBG       = settings [ "Debug"   ]
  if ( "LOG" in settings ) :
    LOG       = settings [ "LOG"     ]
  if ( "Console" in settings ) :
    isConsole = settings [ "Console" ]
  LEVEL = GetDebuggerLevel ( DBG )
  # 規劃除錯訊息
  logging . basicConfig                                 (
    level   = LEVEL                                     ,
    format  = '%(asctime)s %(levelname)-8s %(message)s' ,
    datefmt = '%Y/%m/%d %H:%M:%S'                       ,
  )
  # 設定記錄檔
  if ( len ( LOG ) > 0 ) :
    Logger     = logging . getLogger ( )
    fileh      = logging . FileHandler ( LOG , 'a' )
    if ( not isConsole ) :
      for hdlr in Logger . handlers [ : ] :
        Logger . removeHandler ( hdlr )
    formatter  = logging . Formatter ( '%(asctime)s %(levelname)-8s %(message)s' , '%Y/%m/%d %H:%M:%S' )
    fileh      . setFormatter ( formatter )
    Logger     . addHandler   ( fileh )
