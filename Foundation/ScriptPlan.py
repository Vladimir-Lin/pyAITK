# -*- coding: utf-8 -*-

import os
import sys

from . Plan import Plan as Plan

class ScriptPlan ( Plan ) :

  def __init__ ( self ) :
    super ( Plan , self ) . __init__ ( )
    return

  def __del__  ( self ) :
    pass
