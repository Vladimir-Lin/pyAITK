# -*- coding: utf-8 -*-
##############################################################################
## SplitterHandle
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
##############################################################################
import PySide6
from   PySide6               import QtCore
from   PySide6               import QtGui
from   PySide6               import QtWidgets
##############################################################################
from   PySide6 . QtCore      import *
from   PySide6 . QtGui       import *
from   PySide6 . QtWidgets   import *
##############################################################################
from           . MenuManager import MenuManager as MenuManager
from           . VirtualGui  import VirtualGui  as VirtualGui
##############################################################################
class SplitterHandle         ( QSplitterHandle , VirtualGui                ) :
  ############################################################################
  assignOrientation = Signal ( int                                           )
  ############################################################################
  def __init__               ( self                                        , \
                               orientation                                 , \
                               parent = None                               , \
                               plan   = None                               ) :
    ##########################################################################
    super (                   ) . __init__ ( orientation , parent            )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    self . Menus =                         {                                 }
    ##########################################################################
    return
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    ##########################################################################
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . contextMenuEvent ( event                                     )
    ##########################################################################
    return
  ############################################################################
  def Menu                            ( self , pos                         ) :
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ORI    = self . orientation       (                                      )
    ##########################################################################
    if                                ( ORI == Qt . Horizontal             ) :
      ########################################################################
      msg  = self . getMenuItem       ( "Vertical"                           )
      mm   . addAction                ( 301 , msg                            )
    elif                              ( ORI  == Qt . Vertical              ) :
      ########################################################################
      msg  = self . getMenuItem       ( "Horizontal"                         )
      mm   . addAction                ( 302 , msg                            )
    ##########################################################################
    mm     . setFont                  ( self    . menuFont ( )               )
    aa     = mm . exec_               ( QCursor . pos      ( )               )
    at     = mm . at                  ( aa                                   )
    ##########################################################################
    if                                ( at == 301                          ) :
      self . assignOrientation . emit ( Qt . Vertical                        )
      return True
    ##########################################################################
    if                                ( at == 302                          ) :
      self . assignOrientation . emit ( Qt . Horizontal                      )
      return True
    ##########################################################################
    return True
##############################################################################
