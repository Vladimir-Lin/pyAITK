# -*- coding: utf-8 -*-
##############################################################################
## Pen
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
from   PySide6             import QtCore
from   PySide6             import QtGui
from   PySide6             import QtWidgets
##############################################################################
from   PySide6 . QtCore    import *
from   PySide6 . QtGui     import *
from   PySide6 . QtWidgets import *
##############################################################################
class Pen                  ( QPen                                          ) :
  ############################################################################
  def __init__             ( self                                          ) :
    ##########################################################################
    super ( ) . __init__   (                                                 )
    self      . Initialize (                                                 )
    ##########################################################################
    return
  ############################################################################
  def __del__              ( self                                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Initialize           ( self                                          ) :
    ##########################################################################
    self . Uuid     = 0
    self . Name     = ""
    self . Editable = True
    ##########################################################################
    return
  ############################################################################
  def Configuration                           ( self                       ) :
    ##########################################################################
    c                     = self . color      (                              )
    JSON                  =                   {                              }
    UUID                  = self . Uuid
    ##########################################################################
    JSON [ "Type"       ] = "Pen"
    JSON [ "Uuid"       ] = f"{UUID}"
    JSON [ "Name"       ] = self . Name
    JSON [ "Editable"   ] = self . Editable
    JSON [ "MiterLimit" ] = self . miterLimit (                              )
    JSON [ "WidthF"     ] = self . widthF     (                              )
    JSON [ "CapStyle"   ] = self . capStyle   (                              )
    JSON [ "PenStyle"   ] = self . style      (                              )
    JSON [ "JoinStyle"  ] = self . joinStyle  (                              )
    JSON [ "Cosmetic"   ] = self . isCosmetic (                              )
    JSON [ "R"          ] = c    . red        (                              )
    JSON [ "G"          ] = c    . green      (                              )
    JSON [ "B"          ] = c    . blue       (                              )
    JSON [ "A"          ] = c    . alpha      (                              )
    ##########################################################################
    return JSON
  ############################################################################
  def setConfigure         ( self , JSON                                   ) :
    ##########################################################################
    self . Uuid     = int  ( JSON [ "Uuid" ]                                 )
    self . Name     = JSON [ "Name"                                          ]
    self . Editable = JSON [ "Editable"                                      ]
    ##########################################################################
    self . setMiterLimit   ( JSON [ "MiterLimit"                           ] )
    self . setWidthF       ( JSON [ "WidthF"                               ] )
    self . setCapStyle     ( JSON [ "CapStyle"                             ] )
    self . setStyle        ( JSON [ "PenStyle"                             ] )
    self . setJoinStyle    ( JSON [ "JoinStyle"                            ] )
    self . setCosmetic     ( JSON [ "Cosmetic"                             ] )
    ##########################################################################
    R    = int             ( JSON [ "R"                                    ] )
    G    = int             ( JSON [ "G"                                    ] )
    B    = int             ( JSON [ "B"                                    ] )
    A    = int             ( JSON [ "A"                                    ] )
    self . setColor        ( QColor ( R , G , B , A )                        )
    ##########################################################################
    return
##############################################################################