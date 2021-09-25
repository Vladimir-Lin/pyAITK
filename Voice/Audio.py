# -*- coding: utf-8 -*-
import os
import os . path
import sys
import time
import datetime
import getopt
import logging
import threading
from   playsound import playsound

class AudioPlayer ( ) :

  def __init__ ( self , mappings = { } ) :
    self . Initialize ( mappings )

  def Initialize ( self , mappings ) :
    self . Mappings = mappings
    return True

  def PlayFile ( self , Filename ) :
    if ( not os . path . isfile ( Filename ) ) :
      return False
    playsound  ( Filename )
    return True

  def Play ( self , Filename ) :
    threading . Thread ( target = self . PlayFile , args = ( Filename , ) ) . start ( )
    return

  def Notice ( self , key ) :
    if ( key in self . Mappings ) :
      self . Play ( self . Mappings [ key ] )
    return
