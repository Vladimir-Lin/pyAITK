# -*- coding: utf-8 -*-
#
# 決策列表
#

import os
import sys
import time
import datetime
from   threading import Thread
from   threading import Lock
from   .         import Table

class Tables ( ) :

  def __init__ ( self ) :
    self . clear ( )
    return

  def __del__ ( self ) :
    pass

  def __getitem__ ( self , uuid ) :
    self . Blank ( uuid )
    return self . Tables [ uuid ]

  def clear ( self ) :
    self . Tables = { }
    return

  def keys ( self ) :
    return self . Tables . keys ( )

  def remove ( self , uuid ) :
    if ( uuid in self . Tables ) :
      del self . Tables [ uuid ]
    return

  def Blank ( self , uuid ) :
    if ( uuid not in self . Tables ) :
      T = Table ( uuid )
      self . Tables [ uuid ] = T
    return
