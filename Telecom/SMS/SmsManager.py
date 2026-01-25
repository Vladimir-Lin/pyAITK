# -*- coding: utf-8 -*-
##############################################################################
## 多種簡訊平台管理
##############################################################################
import os
import sys
import time
import datetime
import random
import json
##############################################################################
from . SmsMitake  import SmsMitake  as SmsMitake
from . SmsITE2    import SmsITE2    as SmsITE2
from . SmsEvery8d import SmsEvery8d as SmsEvery8d
##############################################################################
class SmsManager                   (                                       ) :
  ############################################################################
  def __init__                     ( self , Options = { }                  ) :
    self . setOptions              (        Options                          )
    return
  ############################################################################
  def __del__                      ( self                                  ) :
    return
  ############################################################################
  def setOptions                   ( self , Options                        ) :
    ##########################################################################
    self . Options  = Options
    self . Provider = ""
    self . Plugin   = None
    self . Error    = ""
    ##########################################################################
    return
  ############################################################################
  def isPrepared                   ( self                                  ) :
    ##########################################################################
    self   . Error = ""
    if                             ( self . Plugin == None                 ) :
      self . Error = "SMS Provider is not prepared"
      return False
    ##########################################################################
    return True
  ############################################################################
  def prepare                      ( self , phone , provider = ""          ) :
    ##########################################################################
    self . Provider = ""
    self . Plugin   = None
    self . Error    = ""
    PICKED          = False
    CONF            =              {                                         }
    ##########################################################################
    if                             ( len ( provider ) > 0                  ) :
      for PROVIDER in self . Options                                         :
        if                         ( PROVIDER [ "Name" ] == provider       ) :
          CONF      = PROVIDER     [ "Configuration"                         ]
          PICKED    = True
    ##########################################################################
    if                             ( not PICKED                            ) :
      CONFs         =              {                                         }
      PROPORTION    =              [                                         ]
      NAMEs         =              [                                         ]
      TOTAL         = 0
      CNT           = 0
      ########################################################################
      for PROVIDER in self . Options                                         :
        CNT         = CNT + 1
        NAME        = PROVIDER     [ "Name"                                  ]
        P           = PROVIDER     [ "Proportion"                            ]
        P           = int          ( P                                       )
        TOTAL       = TOTAL + P
        PROPORTION  . append       ( TOTAL                                   )
        NAMEs       . append       ( NAME                                    )
        CONFs [ NAME ] = PROVIDER  [ "Configuration"                         ]
      ########################################################################
      if                           ( TOTAL > 0                             ) :
        ######################################################################
        AT          = random . randint ( 0 , TOTAL                           )
        ID          = 0
        while ( AT >= PROPORTION [ ID ] ) and ( ( ID + 1 ) < CNT  )          :
          ID        = ID + 1
        ######################################################################
        provider    = NAMEs        [ ID                                      ]
        CONF        = CONFs        [ provider                                ]
        PICKED      = True
    ##########################################################################
    if                             ( not PICKED                            ) :
      self . Error  = "Provider is indeterminate"
      return False
    ##########################################################################
    self . Provider = provider
    ##########################################################################
    if                             ( provider == "Mitake"                  ) :
      self . Plugin = SmsMitake    ( CONF                                    )
    elif                           ( provider == "ITE2"                    ) :
      self . Plugin = SmsITE2      ( CONF                                    )
    elif                           ( provider == "Every8d"                 ) :
      self . Plugin = SmsEvery8d   ( CONF                                    )
    else                                                                     :
      self . Error  = "Provider is indeterminate"
      return False
    ##########################################################################
    return True
  ############################################################################
  def login                        ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    return self . Plugin . login   (                                           )
  ############################################################################
  def error                        ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return self . Error
    ##########################################################################
    return self . Plugin . error   (                                         )
  ############################################################################
  def credits                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    return self . Plugin . credits (                                         )
  ############################################################################
  def send                         ( self , phone , content , title = ""   ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    return self . Plugin . send    (        phone , content , title          )
##############################################################################
