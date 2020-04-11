# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime
import getopt
import json
import logging
import threading

class CommandsMapper ( ) :

  def __init__ ( self , settings = {} ) :
    self . Initialize ( settings )

  def __del__ ( self ) :
    pass

  def Initialize ( self , settings ) :
    self . Settings = settings
    self . Commands = { }
    KEYs = settings . keys ( )
    for k in KEYs :
      L = settings [ k ]
      for w in L :
        self . Commands [ w ] = k
    return True

  def Id ( self , key ) :
    if ( key in self . Commands ) :
      return int ( self . Commands [ key ] )
    return -1
