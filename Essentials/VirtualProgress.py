# -*- coding: utf-8 -*-
##############################################################################
## 虛擬進度物件
##############################################################################
import os
import sys
import getopt
import time
import datetime
import requests
import threading
##############################################################################
class VirtualProgress         (                                            ) :
  ############################################################################
  def __init__                ( self                                       ) :
    return
  ############################################################################
  def __del__                 ( self                                       ) :
    return
  ############################################################################
  def Progress                ( self , name , Format                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def ProgressName            ( self , Id , name                           ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def ProgressText            ( self , Id , message                        ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def setProgress             ( self , Id , Format                         ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def setRange                ( self , Id , Min , Max                      ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def setFrequency            ( self , Id , cFmt , rFmt                    ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def Start                   ( self , Id , ValueFunc , RunningFunc        ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def Finish                  ( self , Id                                  ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def ProgressReady           ( self , Id , msecs = 1000                   ) :
    raise NotImplementedError (                                              )
##############################################################################
