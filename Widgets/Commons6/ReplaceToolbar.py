# -*- coding: utf-8 -*-
##############################################################################
## ReplaceToolbar
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
from   PySide6             import QtCore
from   PySide6             import QtGui
from   PySide6             import QtWidgets
from   PySide6 . QtCore    import *
from   PySide6 . QtGui     import *
from   PySide6 . QtWidgets import *
##############################################################################
class ReplaceToolbar                ( QToolBar                             ) :
  ############################################################################
  def __init__                      ( self , parent = None                 ) :
    ##########################################################################
    super ( ) . __init__            (        parent                          )
    ##########################################################################
    self . setAllowedAreas          ( Qt . TopToolBarArea                    |
                                      Qt . BottomToolBarArea                 )
    ##########################################################################
    self . ActionWidget = QWidget   (                                        )
    self . addWidget                ( self . ActionWidget                    )
    self . SourceEdit   = QLineEdit ( self . ActionWidget                    )
    self . TargetEdit   = QLineEdit ( self . ActionWidget                    )
    self . FontSize     = int       ( 14                                     )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def PrepareWidgets                       ( self                          ) :
    ##########################################################################
    FH   = int                             ( self . FontSize                 )
    HF   = int                             ( FH + 2                          )
    HH   = int                             ( HF * 2                          )
    ##########################################################################
    self . HalfHeight   = HF
    ##########################################################################
    FNT  = self         . font             (                                 )
    FNT  . setPixelSize                    ( FH                              )
    ##########################################################################
    self .                setMinimumHeight ( HH + 1                          )
    self .                setMaximumHeight ( HH + 1                          )
    self . ActionWidget . setMinimumHeight ( HH                              )
    self . ActionWidget . setMaximumHeight ( HH                              )
    ##########################################################################
    self . SourceEdit   . setFont          ( FNT                             )
    self . TargetEdit   . setFont          ( FNT                             )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
    self      . Relocation  (                                                )
    ##########################################################################
    return
  ############################################################################
  def showEvent           ( self , event                                   ) :
    ##########################################################################
    super ( ) . showEvent ( event                                            )
    self . Relocation     (                                                  )
    ##########################################################################
    return
  ############################################################################
  def Relocation                 ( self                                    ) :
    ##########################################################################
    WW = self . width            (                                           )
    HH = self . height           (                                           )
    HF = self . HalfHeight
    ##########################################################################
    self . ActionWidget . resize ( WW - 1 , HH - 1                           )
    self . SourceEdit   . move   (  0     ,  0                               )
    self . SourceEdit   . resize ( WW - 1 , HF - 1                           )
    self . TargetEdit   . move   (  0     , HF                               )
    self . TargetEdit   . resize ( WW - 1 , HF - 1                           )
    ##########################################################################
    return
##############################################################################
