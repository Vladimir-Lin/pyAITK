# -*- coding: utf-8 -*-
##############################################################################
## Skype機器人
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
import urllib
import urllib   . parse
from   urllib                              import parse
from   pathlib                             import Path
from   http  . server                      import HTTPServer
from   http  . server                      import BaseHTTPRequestHandler
from   http  . server                      import ThreadingHTTPServer
from   skpy                                import Skype
##############################################################################
## Skype監控程式
##############################################################################
class SkypeWatcher            ( BaseHTTPRequestHandler                     ) :
  ############################################################################
  ## 檢查帳號密碼
  ############################################################################
  def isAuthorized            ( self                                       ) :
    ##########################################################################
    if                        ( self . Robot == None                       ) :
      return False
    ##########################################################################
    Username = self . Robot . HttpUsername
    Password = self . Robot . HttpPassword
    ##########################################################################
    if                        ( len ( Password ) <= 0                      ) :
      return True
    ##########################################################################
    if                        ( len ( Username ) <= 0                      ) :
      return True
    ##########################################################################
    USER     = self . headers [ "Username"                                   ]
    PASS     = self . headers [ "Password"                                   ]
    ##########################################################################
    if                        ( USER != Username                           ) :
      return False
    ##########################################################################
    if                        ( PASS != Password                           ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  ## 發送回應
  ############################################################################
  def SendResponse       ( self , Answer , Response                        ) :
    ##########################################################################
    ## Send the html header
    ##########################################################################
    self . send_response ( Answer                                            )
    self . send_header   ( 'Content-type' , 'application/json'               )
    self . end_headers   (                                                   )
    ##########################################################################
    ## Send the html message
    ##########################################################################
    self . wfile . write ( bytes ( str ( Response ) , encoding = "utf8" )    )
    ##########################################################################
    return
  ############################################################################
  ## Silence output message
  ############################################################################
  def log_message             ( self , format , *args                      ) :
    return
  ############################################################################
  ## Handler for the GET requests
  ############################################################################
  def do_GET                  ( self                                       ) :
    return self . Handling    ( False                                        )
  ############################################################################
  ## Handler for the GET requests
  ############################################################################
  def do_POST                 ( self                                       ) :
    return self . Handling    ( True                                         )
  ############################################################################
  ## 處理命令輸入
  ############################################################################
  def Handling                  ( self , posting                           ) :
    ##########################################################################
    self . Robot = self . server . Robot
    ##########################################################################
    if                          ( self . Robot == None                     ) :
      self . SendResponse       ( 401 , { }                                  )
      return
    ##########################################################################
    uri      = parse . urlparse ( self . path                                )
    JSON     = { }
    Response = { }
    Answer   = 200
    ##########################################################################
    if                          ( posting                                  ) :
      contentLength = int       ( self . headers [ 'Content-Length' ]        )
      if                        ( contentLength > 0                        ) :
        ######################################################################
        try                                                                  :
          body = self . rfile . read ( contentLength                         )
          body = body . decode  ( "utf-8"                                    )
          JSON = json . loads   ( body                                       )
        except ValueError                                                    :
          Answer = 400
        ######################################################################
    else                                                                     :
      par    = parse . parse_qs ( uri . query                                )
      if                        ( len ( par ) > 0                          ) :
        pKeys = par . keys      (                                            )
        for k in pKeys                                                       :
          JSON [ k ] = par [ k ] [ 0 ]
    ##########################################################################
    ## Check Account
    ##########################################################################
    if                          ( not self . isAuthorized ( )              ) :
      Answer = 401
    ##########################################################################
    if                          ( Answer == 200                            ) :
      ########################################################################
      Dispatched = self . Dispatch ( uri . path , self . headers , JSON      )
      ########################################################################
      Response   = Dispatched [ "Response" ]
      Answer     = Dispatched [ "Answer"   ]
    ##########################################################################
    self . SendResponse       ( Answer , Response                            )
    ##########################################################################
    return
  ############################################################################
  def Dispatch                ( self , Path , Headers , JSON               ) :
    ##########################################################################
    if                        ( "/Message" == Path                         ) :
      return self . DoMessage ( JSON                                         )
    ##########################################################################
    if                        ( "/System" == Path                          ) :
      return self . DoSystem  ( JSON                                         )
    ##########################################################################
    return { "Answer" : 200 , "Response" : { "Answer" : "Yes" }              }
  ############################################################################
  def DoMessage             ( self , JSON                                  ) :
    ##########################################################################
    if                      ( self . Robot != None                         ) :
      self . Robot . append ( JSON                                           )
    ##########################################################################
    return { "Answer" : 200 , "Response" : { "Answer": "Yes" } }
  ############################################################################
  def DoSystem                  ( self , JSON                              ) :
    ##########################################################################
    Action = JSON               [ "Action"                                   ]
    Action = Action . lower     (                                            )
    if                          ( self . Robot != None                     ) :
      if                        ( Action == "stop"                         ) :
        self . Robot . Shutdown (                                            )
    ##########################################################################
    return { "Answer" : 200 , "Response" : { "Answer": "Yes" } }
##############################################################################
class SkypeRobot (                                                         ) :
  ############################################################################
  def __init__   ( self                                                      ,
                   Username = ""                                             ,
                   Password = ""                                             ,
                   Account  = ""                                             ,
                   Options  = { }                                          ) :
    self . SkypeLocker  = threading . Lock (                                 )
    self . IMS          = None
    self . Watcher      = None
    self . Port         = 5531
    self . HttpUsername = ""
    self . HttpPassword = ""
    self . DebugLogger  = None
    self . Running      = False
    self . Queues       = [ ]
    self . Account      = Account
    self . Username     = Username
    self . Password     = Password
    self . Reply        = None
    self . SendTo       = None
    self . SetOptions ( Options )
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    return
  ############################################################################
  def SetOptions ( self , Options                                          ) :
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
  def lock                     ( self                                      ) :
    self . SkypeLocker . acquire (                                             )
    return
  ############################################################################
  def release                  ( self                                      ) :
    self . SkypeLocker . release (                                             )
    return
  ############################################################################
  def count             ( self                                             ) :
    ##########################################################################
    self  . lock        (                                                    )
    COUNT = len         ( self . Queues                                      )
    self  . release     (                                                    )
    ##########################################################################
    return COUNT
  ############################################################################
  def append                  ( self , JSON                                ) :
    ##########################################################################
    self    . lock            (                                              )
    self    . Queues . append ( JSON                                         )
    self    . release         (                                              )
    ##########################################################################
    ACCOUNT = JSON            [ "Account"                                    ]
    BEAU    = JSON            [ "Beau"                                       ]
    ##########################################################################
    MSG     = f"Queue {ACCOUNT} Message for {BEAU}"
    self    . debug           ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def first                ( self                                          ) :
    ##########################################################################
    BODY   = None
    self   . lock          (                                                 )
    if                     ( len ( self . Queues ) > 0                     ) :
      BODY = self . Queues [ 0                                               ]
      del    self . Queues [ 0                                               ]
    self   . release       (                                                 )
    ##########################################################################
    return BODY
  ############################################################################
  def send            ( self , BODY                                        ) :
    ##########################################################################
    ACCOUNT = BODY    [ "Account"                                            ]
    BEAU    = BODY    [ "Beau"                                               ]
    MESSAGE = BODY    [ "Message"                                            ]
    ##########################################################################
    if                ( len ( ACCOUNT ) <= 0                               ) :
      return False
    ##########################################################################
    if                ( len ( MESSAGE ) <= 0                               ) :
      return False
    ##########################################################################
    try                                                                      :
      CH    = self . IMS . contacts [ ACCOUNT ] . chat
      CH    . sendMsg ( MESSAGE                                              )
      MSG   = f"Send Message to {ACCOUNT} for {BEAU}"
      self  . debug   ( MSG                                                  )
      if              ( self . SendTo != None                              ) :
        self . SendTo ( ACCOUNT , BEAU , MESSAGE                             )
    except                                                                   :
      MSG   = f"Failure to Send Message to {ACCOUNT} for {BEAU}"
      self  . debug   ( MSG                                                  )
    ##########################################################################
    return True
  ############################################################################
  def Incoming                    ( self , account , content               ) :
    ##########################################################################
    MSG  = f"Reply Message from {account}"
    self . debug                  ( MSG                                      )
    ##########################################################################
    if                            ( self . Reply == None                   ) :
      return
    ##########################################################################
    self . Reply                  (        account , "Reply" , content       )
    ##########################################################################
    return
  ############################################################################
  def EventHandler                ( self                                   ) :
    ##########################################################################
    while                         ( self . Running                         ) :
      ########################################################################
      time . sleep                ( 1.0                                      )
      ########################################################################
      if                          ( self . IMS == None                     ) :
        continue
      if                          ( not self . IMS . conn . connected      ) :
        continue
      ########################################################################
      Events   = [ ]
      try                                                                    :
        Events = self . IMS . getEvents (                                    )
      except                                                                 :
        continue
      ########################################################################
      if                          ( len ( Events ) <= 0                    ) :
        continue
      ########################################################################
      self . lock                 (                                          )
      ########################################################################
      try                                                                    :
        for E in Events                                                      :
          if   ( type ( E ) . __name__ == "SkypeNewMessageEvent"           ) :
            ID        = E . msg . user . id
            if ( ID != self . Account                                      ) :
              CONTENT = E . msg . content
              self    . Incoming    ( ID , CONTENT                           )
      except                                                                 :
        pass
      finally                                                                :
        self . release            (                                          )
    ##########################################################################
    return True
  ############################################################################
  def Monitor                     ( self                                   ) :
    ##########################################################################
    self           . Running = True
    ##########################################################################
    threading . Thread            ( target = self . EventHandler ) . start ( )
    ##########################################################################
    while                         ( self . Running                         ) :
      ########################################################################
      time         . sleep        ( 1.0                                      )
      ########################################################################
      if                          ( self . IMS == None                     ) :
        ######################################################################
        self       . lock         (                                          )
        try                                                                  :
          Username = self . Username
          Password = self . Password
          MSG      = f"Trying to login Skype Service Account : {Username}"
          self     . debug        ( MSG                                      )
          self     . IMS = Skype  ( Username , Password                      )
          self     . IMS . setPresence  (                                    )
          MSG      = f"Login Skype Service Account {Username} Successfully"
          self     . debug        ( MSG                                      )
        except                                                               :
          self     . IMS       = None
          Username = self . Username
          MSG      = f"Failure to login Skype Service Account {Username}"
          self     . debug        ( MSG                                      )
          time     . sleep        ( 30                                       )
        finally                                                              :
          self     . release      (                                          )
        ######################################################################
        continue
      ########################################################################
      if                          ( not self . IMS . conn . connected      ) :
        Username   = self . Username
        self . IMS = None
        self . debug              ( f"Skype for {Username} disconnected"     )
        continue
      ########################################################################
      CNT          = self . count (                                          )
      if                          ( CNT <= 0                               ) :
        continue
      ########################################################################
      BODY         = self . first (                                          )
      if                          ( BODY == None                           ) :
        continue
      ########################################################################
      self         . send         ( BODY                                     )
    ##########################################################################
    return True
  ############################################################################
  def StartHttpd                         ( self                            ) :
    ##########################################################################
    MSG            = "Skype Robot is binded to 0.0.0.0:" + str ( self . Port )
    IP             =                     ( "0.0.0.0" , self . Port           )
    ##########################################################################
    self . Watcher = ThreadingHTTPServer ( IP , SkypeWatcher                 )
    self . Watcher . Robot = self
    self . debug                         ( MSG                               )
    self . Watcher . serve_forever       (                                   )
    ##########################################################################
    return
  ############################################################################
  def StopHttpd               ( self                                       ) :
    ##########################################################################
    if                        ( self . Watcher == None                     ) :
      return False
    ##########################################################################
    self . Watcher . shutdown (                                              )
    ##########################################################################
    return True
  ############################################################################
  def Shutdown       ( self                                                ) :
    ##########################################################################
    self . Running = False
    self . StopHttpd (                                                       )
    self . debug     ( "Skype Robot is Stopping, please wait for a moment"   )
    ##########################################################################
    return True
  ############################################################################
  def Start               ( self                                           ) :
    ##########################################################################
    threading . Thread    ( target = self . StartHttpd           ) . start ( )
    ##########################################################################
    return self . Monitor (                                                  )
  ############################################################################
  def StartThreads        ( self                                           ) :
    ##########################################################################
    threading . Thread    ( target = self . StartHttpd           ) . start ( )
    threading . Thread    ( target = self . Monitor              ) . start ( )
    ##########################################################################
    return True
  ############################################################################
  def SendMessage     ( self , Host , JSON                                 ) :
    ##########################################################################
    CMD        = f"{Host}/Message"
    Headers    = { "Username" : self . HttpUsername                          ,
                   "Password" : self . HttpPassword                          }
    try                                                                      :
      requests . post ( CMD                                                  ,
                        data    = json . dumps ( JSON )                      ,
                        headers = Headers                                    )
    except                                                                   :
      return False
    ##########################################################################
    return True
  ############################################################################
  def StopRobot       ( self , Host                                        ) :
    ##########################################################################
    CMD        = f"{Host}/System"
    Headers    = { "Username" : self . HttpUsername                          ,
                   "Password" : self . HttpPassword                          }
    JSON       = { "Action" : "Stop"                                         }
    try                                                                      :
      requests . post ( CMD                                                  ,
                        data    = json . dumps ( JSON )                      ,
                        headers = Headers                                    )
    except                                                                   :
      return False
    ##########################################################################
    return True
##############################################################################
