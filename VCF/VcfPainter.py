# -*- coding: utf-8 -*-
##############################################################################
## VcfPainter
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
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QPolygonF
##############################################################################
class VcfPainter                 (                                         ) :
  ############################################################################
  def __init__                   ( self                                    ) :
    ##########################################################################
    self . setVcfPainterDefaults (                                           )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def setVcfPainterDefaults ( self                                         ) :
    ##########################################################################
    self . Names     =      {                                                }
    self . pens      =      {                                                }
    self . brushes   =      {                                                }
    self . gradients =      {                                                }
    self . fonts     =      {                                                }
    self . pathes    =      {                                                }
    self . switches  =      {                                                }
    ##########################################################################
    return
  ############################################################################
  def addMap ( self , Name , Id                                            ) :
    self . Names [ Name ] = Id
    return
  ############################################################################
  def addPen                       ( self , Id , color                     ) :
    self . pens    [ Id ] = QPen   ( color                                   )
    return len                     ( self . pens                             )
  ############################################################################
  def addBrush                     ( self , Id , color                     ) :
    self . brushes [ Id ] = QBrush ( color                                   )
    return len                     ( self . brushes                          )
  ############################################################################
  def setPainter       ( self , p , name                                   ) :
    ##########################################################################
    if                 ( name not in self . Names                          ) :
      return
    ##########################################################################
    Id  = self . Names [ name                                                ]
    ##########################################################################
    if                 ( Id in self . pens                                 ) :
      p . setPen       ( self . pens    [ Id ]                               )
    ##########################################################################
    if                 ( Id in self . brushes                              ) :
      p . setBrush     ( self . brushes [ Id ]                               )
    ##########################################################################
    return
  ############################################################################
  def drawRect         ( self , p , name , rect                            ) :
    ##########################################################################
    if                 ( name not in self . Names                          ) :
      return
    ##########################################################################
    Id  = self . Names [ name                                                ]
    ##########################################################################
    if                 ( Id in self . pens                                 ) :
      p . setPen       ( self . pens    [ Id ]                               )
    ##########################################################################
    if                 ( Id in self . brushes                              ) :
      p . setBrush     ( self . brushes [ Id ]                               )
    ##########################################################################
    p   . drawRect     ( rect                                                )
    ##########################################################################
    return
  ############################################################################
  def drawBorder       ( self , p , name ,rect                             ) :
    ##########################################################################
    if                 ( name not in self . Names                          ) :
      return
    ##########################################################################
    Id  = self . Names [ name                                                ]
    ##########################################################################
    if                 ( Id in self . pens                                 ) :
      p . setPen       ( self . pens    [ Id ]                               )
    ##########################################################################
    X   = QPolygonF    (                                                     )
    ##########################################################################
    X   . append       ( rect . topLeft     ( )                              )
    X   . append       ( rect . topRight    ( )                              )
    X   . append       ( rect . bottomRight ( )                              )
    X   . append       ( rect . bottomLeft  ( )                              )
    X   . append       ( rect . topLeft     ( )                              )
    ##########################################################################
    p   . drawPolyline ( X                                                   )
    ##########################################################################
    return
  ############################################################################
  def FontMetrics        ( self , Id                                       ) :
    return QFontMetricsF ( self . fonts [ Id ]                               )
  ############################################################################
  def boundingRect ( self , Id , text                                      ) :
    return self . FontMetrics ( Id ) . boundingRect ( text                   )
##############################################################################
