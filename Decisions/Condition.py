# -*- coding: utf-8 -*-
#
# 條件元件
#

import os
import sys
import time
import datetime

class Condition ( ) :

  def __init__ ( self , uuid ) :
    self . Uuid = uuid

  def __del__ ( self ) :
    pass

  def name ( self ) :
    raise NotImplementedError ( )

  def value ( self ) :
    raise NotImplementedError ( )
