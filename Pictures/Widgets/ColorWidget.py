# -*- coding: utf-8 -*-
##############################################################################
## ColorWidget
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
from   PyQt5 . QtCore                 import pyqtSlot
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
from   PyQt5 . QtCore                 import QRect
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QPainter
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QPainter
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QColorDialog
##############################################################################
from   AITK . Qt       . AttachDock   import AttachDock        as AttachDock
from   AITK . Qt       . MenuManager  import MenuManager       as MenuManager
from   AITK . Qt       . Widget       import Widget            as Widget
from   AITK . Qt       . SpinBox      import SpinBox           as SpinBox
from   AITK . Pictures . Colors       import WaveLengthToRGB   as waveToRGB
from   AITK . Pictures . Colors       import RatioToWaveLength as RatioToWave
##############################################################################
class ColorWidget                 ( Widget                                 ) :
  ############################################################################
  HavingMenu   = 1371434312
  ############################################################################
  emitSetColor = pyqtSignal       ( QColor                                   )
  Leave        = pyqtSignal       ( QWidget                                  )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          (        parent        , plan              )
    ##########################################################################
    self . setFunction            ( self . HavingMenu    , True              )
    ##########################################################################
    self . Color = QColor         ( 255 , 255 , 255 , 255                    )
    self . Image = None
    self . setColorToolTip        (                                          )
    ##########################################################################
    self . emitSetColor . connect ( self . setColor                          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint   ( self                                                    ) :
    return QSize ( 32 , 24                                                   )
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
  def mousePressEvent             ( self  , event                          ) :
    ##########################################################################
    if                            ( event . button ( ) == Qt . LeftButton  ) :
      ## self . WaveLengthPressed    ( event . pos ( )                          )
      pass
    super ( ) . mousePressEvent   ( event                                    )
    ##########################################################################
    return
  ############################################################################
  def paintEvent           ( self , event                                  ) :
    ##########################################################################
    if                     ( self . Image == None                          ) :
      self . PrepareImage  (                                                 )
    ##########################################################################
    p = QPainter           ( self                                            )
    p . drawImage          ( 0 , 0 , self . Image                            )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    self . PrepareImage     (                                                )
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def PrepareImage        ( self                                           ) :
    ##########################################################################
    w    = self . width   (                                                  )
    h    = self . height  (                                                  )
    p    = QPainter       (                                                  )
    self . Image = QImage ( w , h , QImage . Format_ARGB32                   )
    p    . begin          ( self . Image                                     )
    p    . setPen         ( QPen   ( self . Color  )                         )
    p    . setBrush       ( QBrush ( self . Color  )                         )
    p    . drawRect       ( QRect  ( 0 , 0 , w , h )                         )
    p    . end            (                                                  )
    ##########################################################################
    return
  ############################################################################
  def setColorToolTip           ( self                                     ) :
    ##########################################################################
    R    = self . Color . red   (                                            )
    G    = self . Color . green (                                            )
    B    = self . Color . blue  (                                            )
    A    = self . Color . alpha (                                            )
    M    = f"{R} , {G} , {B} , {A}"
    self . setToolTip           ( M                                          )
    ##########################################################################
    return
  ############################################################################
  def setColor             ( self , color                                  ) :
    ##########################################################################
    self . Color = color
    self . PrepareImage    (                                                 )
    self . setColorToolTip (                                                 )
    ##########################################################################
    return
  ############################################################################
  def UpdateColor              ( self , color                              ) :
    ##########################################################################
    self . emitSetColor . emit (        color                                )
    ##########################################################################
    return
  ############################################################################
  def SystemPickColor              ( self                                  ) :
    ##########################################################################
    C    = self . Color
    R    = QColorDialog . getColor ( C , self                                )
    if                             ( not R . isValid ( )                   ) :
      return
    ##########################################################################
    self . setColor                ( R                                       )
    self . update                  (                                         )
    ##########################################################################
    return
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    MSG    = self . getMenuItem     ( "DefaultSelectColor"                   )
    mm     . addAction              ( 1001 , MSG                             )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . SystemPickColor        (                                        )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
