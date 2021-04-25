# -*- coding: utf-8 -*-
##############################################################################
## Foxman代理人
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
## Foxman智能回應程式
##############################################################################
class FoxmanRobot (                                                        ) :
  ############################################################################
  def __init__         ( self , jsonFile = ""                              ) :
    ##########################################################################
    self . DebugLogger = None
    self . Talk        = None
    self . Reboot      = None
    self . StopIt      = None
    self . State       = 0
    self . CurrentDir  = ""
    self . Beau        = "Foxman"
    self . PullCommand = ""
    self . PushCommand = ""
    self . tblHost     = "http://insider.actions.com.tw:8364"
    self . sohoHost    = "http://soho.actions.com.tw:8364"
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
  def HttpParser                   ( self , Path , Headers , JSON          ) :
    return                         { "Process" : False                       }
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
  ############################################################################
  def Reply                        ( self , beau , message                 ) :
    ##########################################################################
    if                             ( self . State ==  0                    ) :
      self . IdleState             (        beau , message                   )
    ##########################################################################
    elif                           ( self . State ==  1                    ) :
      self . BasicMode             (        beau , message                   )
    ##########################################################################
    elif                           ( self . State == 11                    ) :
      self . tblMode               (        beau , message                   )
    ##########################################################################
    return True
  ############################################################################
  def IdleState                    ( self , beau , message                 ) :
    ##########################################################################
    s    = message . lower         (                                         )
    s    = s       . rstrip        (                                         )
    beau = "Idle"
    STAS = "Startup"
    TBLS = "Taiwan-Big-Lottery"
    ##########################################################################
    if   ( s in self . JSON [ "Commands" ] [ STAS ] [ "Allows" ] )           :
      self . State = 1
      MSG          = self . JSON [ "Commands" ] [ STAS ] [ "Welcome" ]
      self . TalkTo                ( self . Beau , MSG                       )
    ##########################################################################
    elif ( s in self . JSON [ "Commands" ] [ TBLS ] [ "Allows" ] )           :
      self . State = 11
      MSG          = self . JSON [ "Commands" ] [ TBLS ] [ "Welcome" ]
      self . TalkTo                ( self . Beau , MSG                       )
    ##########################################################################
    return True
  ############################################################################
  def BasicMode                    ( self , beau , message                 ) :
    ##########################################################################
    s    = message . lower         (                                         )
    s    = s       . rstrip        (                                         )
    L    = s       . split         ( ' '                                     )
    CNT  = len                     ( L                                       )
    beau = "Basic"
    ##########################################################################
    if ( s in self . JSON [ "Commands" ] [ "Reboot" ] [ "Allows" ] )         :
      self . Reboot                (                                         )
      return True
    ##########################################################################
    if ( CNT == 1 ) and ( s in self . JSON [ "Commands" ] [ "Stop" ] [ "Allows" ] ) :
      self . StopIt                (                                         )
      return True
    ##########################################################################
    if ( s in self . JSON [ "Commands" ] [ "Finish" ] [ "Allows" ]         ) :
      self . State = 0
      MSG          = self . JSON [ "Commands" ] [ "Finish" ] [ "Welcome" ]
      self . TalkTo                ( beau , MSG                              )
      return True
    ##########################################################################
    if ( s in self . JSON [ "Commands" ] [ "Settings" ] [ "Allows" ]       ) :
      MSG = json . dumps           ( self . JSON , ensure_ascii = False      )
      self . TalkTo                ( "settings" , MSG                        )
      return True
    ##########################################################################
    if                             ( CNT <= 0                              ) :
      return True
    ##########################################################################
    if                             ( L [ 0 ] == "current"                  ) :
      ########################################################################
      if                           ( CNT > 1                               ) :
        ######################################################################
        if                         ( L [ 1 ] == "directory"                ) :
          self . OsGetCWD          (                                         )
    ##########################################################################
    elif ( L [ 0 ] in self . JSON [ "Commands" ] [ "PWD" ] [ "Allows" ]    ) :
      self     . OsGetCWD          (                                         )
    ##########################################################################
    elif                           ( L [ 0 ] == "chdir"                    ) :
      self . OsChdir               ( message [ 6 : ]                         )
    elif                           ( L [ 0 ] == "cd"                       ) :
      self . OsChdir               ( message [ 3 : ]                         )
    ##########################################################################
    elif                           ( L [ 0 ] == "dir"                      ) :
      threading . Thread           ( target = self . ListFiles   ) . start ( )
    elif                           ( L [ 0 ] == "ls"                       ) :
      threading . Thread           ( target = self . ListFiles   ) . start ( )
    elif                           ( L [ 0 ] == "files"                    ) :
      threading . Thread           ( target = self . ListFiles   ) . start ( )
    ##########################################################################
    elif                           ( L [ 0 ] == "push"                     ) :
      threading . Thread           ( target = self . PushSystem  ) . start ( )
    elif                           ( L [ 0 ] == "commit"                   ) :
      threading . Thread           ( target = self . PushSystem  ) . start ( )
    ##########################################################################
    elif                           ( L [ 0 ] == "pull"                     ) :
      threading . Thread           ( target = self . PullSystem  ) . start ( )
    elif                           ( L [ 0 ] == "upgrade"                  ) :
      threading . Thread           ( target = self . PullSystem  ) . start ( )
    ##########################################################################
    elif                           ( L [ 0 ] == "sync"                     ) :
      threading . Thread           ( target = self . SyncSystem  ) . start ( )
    ##########################################################################
    elif                           ( L [ 0 ] == "dos"                      ) :
      cmd       = message          [ 4:                                      ]
      threading . Thread           ( target = self . RunCommand            , \
                                     args = ( cmd , )            ) . start ( )
    elif                           ( L [ 0 ] == "run"                      ) :
      cmd       = message          [ 4:                                      ]
      threading . Thread           ( target = self . RunCommand            , \
                                     args = ( cmd , )            ) . start ( )
    elif                           ( L [ 0 ] == "command"                  ) :
      cmd       = message          [ 8:                                      ]
      threading . Thread           ( target = self . RunCommand            , \
                                     args = ( cmd , )            ) . start ( )
    ##########################################################################
    elif ( L [ 0 ] in self . JSON [ "Commands" ] [ "Load" ] [ "Allows" ]   ) :
      if ( CNT > 1 ) and ( L [ 1 ] in self . JSON [ "Commands" ] [ "Settings" ] [ "Allows" ] ) :
        threading . Thread         ( target = self . LoadJSON    ) . start ( )
    elif ( L [ 0 ] in self . JSON [ "Commands" ] [ "Save" ] [ "Allows" ]   ) :
      if ( CNT > 1 ) and ( L [ 1 ] in self . JSON [ "Commands" ] [ "Settings" ] [ "Allows" ] ) :
        threading . Thread         ( target = self . StoreJSON   ) . start ( )
    ##########################################################################
    return True
  ############################################################################
  def tblMode                      ( self , beau , message                 ) :
    ##########################################################################
    s    = message . lower         (                                         )
    s    = s       . rstrip        (                                         )
    L    = s       . split         ( ' '                                     )
    CNT  = len                     ( L                                       )
    beau = "Lottery"
    ##########################################################################
    if ( s in self . JSON [ "Commands" ] [ "Finish" ] [ "Allows" ]         ) :
      self . State = 0
      MSG          = self . JSON [ "Commands" ] [ "Finish" ] [ "Welcome" ]
      self . TalkTo                ( beau , MSG                              )
      return True
    ##########################################################################
    SERIALID = "Current-Serial"
    if ( s in self . JSON [ "Commands" ] [ SERIALID ] [ "Allows" ]         ) :
      JSON = {}
      JSON [ "Action" ] = "Serial"
      print ( "Lottery Serial" )
      self . SendRPC                ( self . tblHost , "TBL" , JSON          )
      return True
    ##########################################################################
    return True
  ############################################################################
  def OsGetCWD                      ( self                                 ) :
    ##########################################################################
    self . CurrentDir = os . getcwd (                                        )
    self . TalkTo                   ( self . Beau , self . CurrentDir        )
    ##########################################################################
    return
  ############################################################################
  def OsChdir                       ( self , directory                     ) :
    ##########################################################################
    os   . chdir                    (        directory                       )
    self . OsGetCWD                 (                                        )
    ##########################################################################
    return
  ############################################################################
  def ListFiles                     ( self                                 ) :
    ##########################################################################
    L     = "\n" . join ( [ f for f in os . listdir ( ) ] )
    T     = L
    self . TalkTo                   ( "files" , T                            )
    ##########################################################################
    return
  ############################################################################
  def SendRPC                       ( self , HOST , Command , JSON         ) :
    ##########################################################################
    CMD      = f"{HOST}/{Command}"
    Headers  = { "Username" : "foxman"                                       ,
                 "Password" : "actionsfox2019"                               }
    try                                                                      :
      status = requests . post ( CMD                                         ,
                                 data    = json . dumps ( JSON )             ,
                                 headers = Headers                           )
      print ( "Send Requests" )
    except                                                                   :
      print ( "Requests Fail" )
      return False
    ##########################################################################
    return status . status_code
  ############################################################################
  def PullSystem                    ( self                                 ) :
    return self . RunCommand        ( self . PullCommand                     )
  ############################################################################
  def PushSystem                    ( self                                 ) :
    ##########################################################################
    return self . RunCommand        ( self . PushCommand                     )
  ############################################################################
  def SyncSystem                    ( self                                 ) :
    ##########################################################################
    self . RunCommand               ( self . PushCommand                     )
    self . RunCommand               ( self . PullCommand                     )
    ##########################################################################
    return
  ############################################################################
  def RunCommand                       ( self , command                    ) :
    ##########################################################################
    if                                 ( len ( command ) <= 0              ) :
      return
    ##########################################################################
    r = subprocess . Popen             ( command                           , \
                                        shell  = True                      , \
                                        stdout = subprocess . PIPE         , \
                                        stderr = subprocess . STDOUT         )
    L = r . stdout . readlines         (                                     )
    r . stdout . close                 (                                     )
    ##########################################################################
    X     = [ ]
    for S in L                                                               :
      X   . append                     ( S . decode ( "utf-8" )              )
    T     = "" . join                  ( X                                   )
    ##########################################################################
    self  . TalkTo                     ( "command" , T                       )
    ##########################################################################
    return
##############################################################################
