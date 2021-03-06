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
from   pathlib import Path
from   io import BytesIO
import pycurl
##############################################################################
class Download    (                                                        ) :
  ############################################################################
  def __init__    ( self                                                   ) :
    self . Clear  (                                                          )
  ############################################################################
  def __del__     ( self                                                   ) :
    pass
  ############################################################################
  def Clear       ( self                                                   ) :
    self . Headers   = [ 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:8.0) Gecko/20100101 Firefox/8.0' ]
    self . Filename  = ""
    self . URL       = ""
    self . Responses = { }
    self . isHTTPS   = False
    self . Success   = False
    self . Data      = BytesIO ( )
    self . download  = pycurl . Curl ( )
    return
  ############################################################################
  def setFilename ( self , filename                                        ) :
    self . Filename  = filename
    return
  ############################################################################
  def setURL      ( self , url                                             ) :
    self   . URL  = url
    self   . isHTTPS   = False
    if ( "https://" in url . lower ( ) ) :
      self . isHTTPS   = True
    return
  ############################################################################
  def Execute                   ( self                                      ) :
    try                                                                       :
      self . download . perform (                                             )
    except pycurl . error                                                     :
      return False
    return True
  ############################################################################
  def CheckHttps             (     self                                    ) :
    if                       ( not self . isHTTPS                          ) :
      return False
    self . download . setopt ( pycurl . SSL_VERIFYPEER , 0                   )
    self . download . setopt ( pycurl . SSL_VERIFYHOST , 0                   )
    return True
  ############################################################################
  def GetHeader        ( self , headerLine                                 ) :
    self . Responses = {                                                     }
    headerLine       = headerLine . decode ( 'iso-8859-1' )
    if ":" not in headerLine                                                 :
      return
    h_name, h_value  = headerLine . split  ( ':' , 1 )
    h_name  = h_name  . strip ( )
    h_value = h_value . strip ( )
    h_name  = h_name  . lower ( )
    self . Responses [ h_name ] = h_value
    return
  ############################################################################
  def Write                  (     self                                    ) :
    if                       ( not self . Success                          ) :
      return False
    with open                ( self . Filename , "wb" ) as f                 :
        f . write            ( self . Data . getbuffer ( )                   )
    return True
  ############################################################################
  def Download               ( self                                        ) :
    self . download . setopt ( pycurl . URL            , self . URL          )
    self . download . setopt ( pycurl . HEADERFUNCTION , self . GetHeader    )
    self . download . setopt ( pycurl . WRITEDATA      , self . Data         )
    self . download . setopt ( pycurl . HTTPHEADER     , self . Headers      )
    self . CheckHttps        (                                               )
    self . Success  = self . Execute (                                       )
    self . download . close          (                                       )
    return self . Success
  ############################################################################
