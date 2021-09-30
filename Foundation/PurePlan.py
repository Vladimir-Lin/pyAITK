# -*- coding: utf-8 -*-
##############################################################################
import os
import sys
##############################################################################
class PurePlan (                                                           ) :
  ############################################################################
  def __init__ ( self                                                      ) :
    ##########################################################################
    self . Application = ""
    self . Machine     = ""
    self . Hostname    = ""
    self . Root        = ""
    self . Home        = ""
    self . User        = ""
    self . Bin         = ""
    self . Arguments   = [ ]
    self . PluginPaths = [ ]
    self . Locality    = 1002
    self . UserUuid    =    0
    self . uid         =  500
    self . gid         =  500
    self . Verbose     =   20
    self . MaxLogs     =    0
    self . Visible     = True
    self . scene       = False
    self . canContinue = True
    self . Tables      = { }
    self . Values      = { }
    self . Booleans    = { }
    self . Uuids       = [ ]
    self . SQLs        = { }
    self . Dirs        = { }
    self . Variables   = { }
    ##########################################################################
    return
  ############################################################################
  def __del__                  ( self                                      ) :
    return
  ############################################################################
  def type                     ( self                                      ) :
    return 1
  ############################################################################
  def Initialize               ( self                                      ) :
    return True
  ############################################################################
  def arguments                ( self , argv                               ) :
    return
  ############################################################################
  def Path                     ( self , name                               ) :
    return os . path . abspath ( self . Root + "/" + filename                )
  ############################################################################
  def Temporary        ( self , filename                                   ) :
    return self . Path ( "Temp"                                              )
##############################################################################
