# -*- coding: utf-8 -*-
##############################################################################
## LINE機器人
##############################################################################
import os
import sys
import getopt
import time
import datetime
import logging
import requests
import threading
import gettext
import shutil
import json
import ssl
import asyncio
##############################################################################
import urllib
import urllib   . parse
from   urllib                              import parse
##############################################################################
from   pathlib                             import Path
##############################################################################
from   http  . server                      import HTTPServer
from   http  . server                      import BaseHTTPRequestHandler
from   http  . server                      import ThreadingHTTPServer
##############################################################################
from   flask                               import Flask                 as Flask
from   flask                               import request               as request
from   flask                               import abort                 as abort
from   linebot                             import LineBotApi            as LineBotApi
from   linebot                             import WebhookHandler        as WebhookHandler
from   linebot . exceptions                import InvalidSignatureError as InvalidSignatureError
from   linebot . models                    import MessageEvent          as MessageEvent
from   linebot . models                    import TextMessage           as TextMessage
from   linebot . models                    import TextSendMessage       as TextSendMessage
##############################################################################
from   . HttpRPC                           import HttpRPC as HttpRPC
##############################################################################
class LineWatcher               ( HttpRPC                                  ) :
  ############################################################################
  ## 檢查帳號密碼
  ############################################################################
  def isAuthorized              ( self                                     ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  ## 掛入額外資訊
  ############################################################################
  def Attache                   ( self                                     ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def Dispatch                  ( self , Path , Headers , JSON             ) :
    ##########################################################################
    ##########################################################################
    return                      { "Answer"     : 202                         ,
                                    "Response" :                             {
                                    "Answer"   : "Yes"                     } }
##############################################################################
class LineRobot  (                                                         ) :
  ############################################################################
  def __init__   ( self                                                      ,
                   Username = ""                                             ,
                   Password = ""                                             ,
                   Account  = ""                                             ,
                   Options  = { }                                          ) :
    ##########################################################################
    self . LineLocker = threading . Lock (                                   )
    self . Watcher        = None
    self . DebugLogger    = None
    self . Running        = False
    self . Account        = Account
    self . Username       = Username
    self . Password       = Password
    self . HttpPlugin     = None
    self . SetOptions ( Options )
    ##########################################################################
    return
  ############################################################################
  def __del__       ( self                                                 ) :
    return
  ############################################################################
  def SetOptions ( self , Options                                          ) :
    self . Options = Options
    return
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
  def lock                      ( self                                     ) :
    self . LineLocker . acquire (                                            )
    return
  ############################################################################
  def release                   ( self                                     ) :
    self . LineLocker . release (                                            )
    return
  ############################################################################
  def isWorking         ( self                                             ) :
    return self . Working
##############################################################################
