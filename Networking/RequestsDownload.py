# -*- coding: utf-8 -*-
##############################################################################
## 下載檔案
##############################################################################
import os
import sys
import time
import datetime
import logging
import requests
import threading
import gettext
import json
import codecs
import urllib
import urllib . parse
##############################################################################
from   pathlib import Path
from   io      import BytesIO
##############################################################################
class RequestsDownload (                                                   ) :
  ############################################################################
  def __init__         ( self                                              ) :
    self . Clear       (                                                     )
    return
  ############################################################################
  def __del__          ( self                                              ) :
    return
  ############################################################################
  def Clear       ( self                                                   ) :
    self . Headers   = [ 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0' ]
    self . Filename  = ""
    self . URL       = ""
    self . Responses = { }
    self . isHTTPS   = False
    self . Success   = False
    self . Data      = BytesIO ( )
    self . Code      = 0
    return
  ############################################################################
  def setFilename ( self , filename                                        ) :
    self . Filename  = filename
    return
  ############################################################################
  def setURL      ( self , url                                             ) :
    ##########################################################################
    self   . URL  = url
    self   . isHTTPS   = False
    ##########################################################################
    if            ( "https://" in url . lower ( )                          ) :
      self . isHTTPS   = True
    return
  ############################################################################
  def toUtf8                          ( self                               ) :
    ##########################################################################
    JDATA  = self   . Data . getvalue (                                      )
    ##########################################################################
    if                                ( len ( JDATA ) <= 0                 ) :
      return ""
    ##########################################################################
    try                                                                      :
      JST   = JDATA . decode          ( "utf-8"                              )
    except                                                                   :
      try                                                                    :
        JST = JDATA . decode          ( "utf-8" , "ignore"                   )
      except                                                                :
        return ""
    ##########################################################################
    return JST
  ############################################################################
  def Download                 ( self                                      ) :
    ##########################################################################
    if                         ( len ( self . URL ) <= 0                   ) :
      return False
    ##########################################################################
    try                                                                      :
      r  = requests . get      ( self . URL                                  )
    except                                                                   :
      return False
    ##########################################################################
    self . Data      = BytesIO ( r.content                                   )
    self . Responses = r . headers
    self . Code      = r . status_code
    self . Success   =         ( self . Code == 200                          )
    ##########################################################################
    return self . Success
##############################################################################