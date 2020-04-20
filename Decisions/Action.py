# -*- coding: utf-8 -*-
#
# 決策基礎元件
#

import os
import sys
import time
import datetime
from   threading import Thread
from   threading import Lock

class Action ( ) :

  def __init__ ( self , uuid ) :
    self . Uuid       = uuid
    self . arguments  = { }
    self . conditions = { }
    self . locker     = Lock ( )
    pass

  def __del__ ( self ) :
    pass


