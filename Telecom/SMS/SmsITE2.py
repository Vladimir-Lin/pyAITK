# -*- coding: utf-8 -*-
##############################################################################
## 詮力簡訊發送平台
## 網址：https://www.ite2.com
##############################################################################
import os
import sys
import base64
import json
import requests
##############################################################################
from . SMS import SMS
##############################################################################
class SmsITE2                   ( SMS                                      ) :
  ############################################################################
  def __init__                  ( self , Options = { }                     ) :
    self . setOptions           (        Options                             )
    return
  ############################################################################
  def __del__                   ( self                                     ) :
    return
  ############################################################################
  def setOptions                ( self , Options                           ) :
    ##########################################################################
    self . URL      = Options   [ "Hostname"                                 ]
    self . Username = Options   [ "Username"                                 ]
    self . Password = Options   [ "Password"                                 ]
    self . Credits  = 0
    self . Error    = ""
    ##########################################################################
    BSTR            = self   . Password . encode ( "utf-8"                   )
    self . B64PWD   = base64 . b64encode         ( BSTR                      )
    self . B64PWD   = self   . B64PWD   . decode ( "utf-8"                   )
    ##########################################################################
    return
  ############################################################################
  def login                     ( self                                     ) :
    return True
  ############################################################################
  def error                     ( self                                     ) :
    return self . Error
  ############################################################################
  def credits                   ( self                                     ) :
    ##########################################################################
    self . Credits = 0
    self . Error   = ""
    ##########################################################################
    CMD            = self . URL + "/QueryPoint"
    Parameters     = { "UID" : self . Username                               ,
                       "Pwd" : self . B64PWD                                 }
    try                                                                      :
      answer       = requests . post ( CMD , params = Parameters             )
    except                                                                   :
      self . Error = "Failure to Query ITE2 account Credits"
      return False
    ##########################################################################
    if                               ( answer . status_code != 200         ) :
      CODE         = answer . status_code
      self . Error = f"HTTP return code is {CODE}"
      return False
    ##########################################################################
    print(answer.text)
    try                                                                      :
      JSON         = json . loads    ( answer . text                         )
    except                                                                   :
      self . Error = f"ITE2 did not answer current credits"
      return False
    ##########################################################################
    if ( ( "SmsPoint" not in JSON ) or ( "ErrorCode" not in JSON ) )         :
      self . Error = f"ITE2 answer incorrect credit format"
      return False
    ##########################################################################
    ECODE          = JSON            [ "ErrorCode"                           ]
    if                               ( ECODE != 0                          ) :
      self . Error = f"ITE2 error code : {ECODE}"
      return False
    ##########################################################################
    self . Credits = int             ( JSON [ "SmsPoint" ]                   )
    ##########################################################################
    return self . Credits
  ############################################################################
  def send                      ( self , phone , content , title = ""      ) :
    self . Error = "SMS sending function is not implemented"
    return False
##############################################################################
