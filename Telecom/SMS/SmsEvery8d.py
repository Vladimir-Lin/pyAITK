# -*- coding: utf-8 -*-
##############################################################################
## 互動資通簡訊發送平台
## 網址：http://www.every8d.com
##############################################################################
import os
import sys
import requests
import urllib
##############################################################################
from . SMS import SMS
##############################################################################
class SmsEvery8d                 ( SMS                                     ) :
  ############################################################################
  def __init__                   ( self , Options = { }                    ) :
    self . setOptions            (        Options                            )
    return
  ############################################################################
  def __del__                    ( self                                    ) :
    return
  ############################################################################
  def setOptions                 ( self , Options                          ) :
    ##########################################################################
    self . URL        = Options  [ "Hostname"                                ]
    self . Username   = Options  [ "Username"                                ]
    self . Password   = Options  [ "Password"                                ]
    self . Credits    = 0
    self . Error      = ""
    self . JSON       =          {                                           }
    ##########################################################################
    return
  ############################################################################
  def login                      ( self                                    ) :
    return True
  ############################################################################
  def error                      ( self                                    ) :
    return self . Error
  ############################################################################
  def credits                    ( self                                    ) :
    ##########################################################################
    self . Credits = 0
    self . Error   = ""
    ##########################################################################
    CMD            = self . URL + "/API21/HTTP/getCredit.ashx"
    Parameters     = { "UID" : self . Username                               ,
                       "PWD" : self . Password                               }
    try                                                                      :
      answer       = requests . post ( CMD , params = Parameters             )
    except                                                                   :
      self . Error = "Failure to Query Mitake account Credits"
      return False
    ##########################################################################
    if                               ( answer . status_code != 200         ) :
      CODE         = answer . status_code
      self . Error = f"HTTP return code is {CODE}"
      return False
    ##########################################################################
    try                                                                      :
      Creditz      = int             ( answer . text                         )
    except                                                                   :
      T            = answer . text
      self . Error = f"Every8d did not answer current credits : {T}"
      return False
    ##########################################################################
    self . Credits = Creditz
    ##########################################################################
    return self . Credits
  ############################################################################
  def send                       ( self , phone , content , title = ""     ) :
    ##########################################################################
    self . Error   = ""
    ##########################################################################
    if                           ( len ( phone ) <= 0                      ) :
      self . Error = "SMS requires a valid phone number"
      return False
    ##########################################################################
    if                           ( len ( content ) <= 0                    ) :
      self . Error = "SMS requires content"
      return False
    ##########################################################################
    CMD            = self . URL + "/API21/HTTP/sendSMS.ashx"
    Parameters     = { "UID"   : self . Username                             ,
                       "PWD"   : self . Password                             ,
                       "DEST"  : phone                                       ,
                       "MSG"   : content                                     }
    try                                                                      :
      answer       = requests . post ( CMD , params = Parameters             )
    except                                                                   :
      self . Error = "Failure to send SMS Content via Mitake"
      return False
    ##########################################################################
    if                               ( answer . status_code != 200         ) :
      CODE         = answer . status_code
      self . Error = f"HTTP return code is {CODE} when sending SMS Content"
      return False
    ##########################################################################
    if                               ( len ( answer . text ) <= 0          ) :
      self . Error = f"HTTP return text is empty"
      return False
    ##########################################################################
    LISTS          = answer . text
    ANSZ           = LISTS . split   ( ","                                   )
    if                               ( len ( ANSZ ) < 5                    ) :
      self . Error = f"HTTP Response format did not match API document - {LISTS}"
      return False
    ##########################################################################
    CREDITZ        = int             ( float ( ANSZ [ 0 ] )                  )
    self . JSON    =                                                         {
      "CREDIT"     : CREDITZ                                                 ,
      "SENDED"     : ANSZ            [ 1                                   ] ,
      "COST"       : ANSZ            [ 2                                   ] ,
      "UNSEND"     : ANSZ            [ 3                                   ] ,
      "BATCH_ID"   : ANSZ            [ 4                                   ] }
    ##########################################################################
    if                               ( CREDITZ < 0                         ) :
      self . Error = f"Unknown mistake : " + answer . text
      return False
    ##########################################################################
    self . Credits = CREDITZ
    ##########################################################################
    return True
##############################################################################
