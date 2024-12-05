# -*- coding: utf-8 -*-
##############################################################################
## ProgressIndicator
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
from   opencc                          import OpenCC
from   googletrans                     import Translator
##############################################################################
from   PyQt5                           import QtCore
from   PyQt5                           import QtGui
from   PyQt5                           import QtWidgets
##############################################################################
from   PyQt5 . QtCore                  import QObject
from   PyQt5 . QtCore                  import pyqtSignal
from   PyQt5 . QtCore                  import pyqtSlot
from   PyQt5 . QtCore                  import Qt
from   PyQt5 . QtCore                  import QPoint
from   PyQt5 . QtCore                  import QPointF
from   PyQt5 . QtCore                  import QSize
from   PyQt5 . QtCore                  import QTimer
from   PyQt5 . QtCore                  import QMutex
from   PyQt5 . QtCore                  import QMutexLocker
from   PyQt5 . QtCore                  import QDateTime
##############################################################################
from   PyQt5 . QtGui                   import QIcon
from   PyQt5 . QtGui                   import QCursor
from   PyQt5 . QtGui                   import QKeySequence
from   PyQt5 . QtGui                   import QPen
from   PyQt5 . QtGui                   import QBrush
from   PyQt5 . QtGui                   import QPainter
##############################################################################
from   PyQt5 . QtWidgets               import QApplication
from   PyQt5 . QtWidgets               import QWidget
from   PyQt5 . QtWidgets               import qApp
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAction
from   PyQt5 . QtWidgets               import QShortcut
from   PyQt5 . QtWidgets               import QSizePolicy
from   PyQt5 . QtWidgets               import QAbstractItemView
from   PyQt5 . QtWidgets               import QTreeWidget
from   PyQt5 . QtWidgets               import QTreeWidgetItem
from   PyQt5 . QtWidgets               import QLineEdit
from   PyQt5 . QtWidgets               import QComboBox
from   PyQt5 . QtWidgets               import QSpinBox
from   PyQt5 . QtWidgets               import QProgressBar
from   PyQt5 . QtWidgets               import QToolButton
##############################################################################
class ProgressIndicator   ( QWidget                                        ) :
  ############################################################################
  def __init__            ( self , parent = None                           ) :
    ##########################################################################
    super ( ) . __init__  (        parent                                    )
    ##########################################################################
    self . m_angle                = 0
    self . m_timerId              = -1
    self . m_delay                = 40
    self . m_entry                = 0
    self . m_count                = 15
    self . m_factor               = 0.50
    self . m_displayedWhenStopped = False
    self . m_color                = Qt . black
    self . hint                   = QSize ( 20 , 20                          )
    ##########################################################################
    self . setSizePolicy  ( QSizePolicy . Fixed , QSizePolicy . Fixed        )
    self . setFocusPolicy ( Qt . NoFocus                                     )
    ##########################################################################
    return
  ############################################################################
  def __del__             ( self                                           ) :
    return
  ############################################################################
  def sizeHint            ( self                                           ) :
    return self . hint
  ############################################################################
  def animationDelay      ( self                                           ) :
    return self . m_delay
  ############################################################################
  def color               ( self                                           ) :
    return self . m_color
  ############################################################################
  def TickCount           ( self                                           ) :
    return self . m_count
  ############################################################################
  def RadiusFactor        ( self                                           ) :
    return self . m_factor
  ############################################################################
  def isAnimated          ( self                                           ) :
    return                ( self . m_timerId != -1                           )
  ############################################################################
  def heightForWidth      ( self , w                                       ) :
    return w
  ############################################################################
  def setColor            ( self , color                                   ) :
    ##########################################################################
    self . m_color = color
    self . update         (                                                  )
    ##########################################################################
    return
  ############################################################################
  def setTicks            ( self , count                                   ) :
    ##########################################################################
    self . m_count = count
    ##########################################################################
    return
  ############################################################################
  def setRadiusFactor     ( self , factor                                  ) :
    ##########################################################################
    self . m_factor = factor
    ##########################################################################
    return
  ############################################################################
  def setDisplayedWhenStopped ( self , state                               ) :
    ##########################################################################
    self . m_displayedWhenStopped = state
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def isDisplayedWhenStopped  ( self                                       ) :
    return self . m_displayedWhenStopped
  ############################################################################
  def startAnimation                       ( self                          ) :
    ##########################################################################
    self   . m_entry = self . m_entry + 1
    ##########################################################################
    if                                     ( self . m_entry > 1            ) :
      return
    ##########################################################################
    self   . m_angle = 0
    ##########################################################################
    if                                     ( self . m_timerId == -1        ) :
      self . m_timerId = self . startTimer ( self . m_delay                  )
    ##########################################################################
    return self . m_entry
  ############################################################################
  def stopAnimation    ( self                                              ) :
    ##########################################################################
    self . m_entry = self . m_entry - 1
    ##########################################################################
    if                 ( self . m_entry > 0                                ) :
      return self . m_entry
    ##########################################################################
    self . m_entry = 0
    ##########################################################################
    if                 ( self . m_timerId != -1                            ) :
      self . killTimer ( self . m_timerId                                    )
    ##########################################################################
    self . m_timerId = -1
    self . update      (                                                     )
    ##########################################################################
    return 0
  ############################################################################
  def setAnimationDelay                    ( self , delay                  ) :
    ##########################################################################
    if                                     ( self . m_timerId != -1        ) :
      self . killTimer                     ( self . m_timerId                )
    ##########################################################################
    self . m_delay = delay
    ##########################################################################
    if                                     ( self . m_timerId != -1        ) :
      self . m_timerId = self . startTimer ( self . m_delay                  )
    ##########################################################################
    return
  ############################################################################
  def timerEvent         ( self , timeEvent                                ) :
    ##########################################################################
    degree         = int ( 360 / self . m_count                              )
    self . m_angle = int ( self . m_angle + degree                           )
    self . m_angle = int ( self . m_angle % 360                              )
    ##########################################################################
    self . update        (                                                   )
    ##########################################################################
    return
  ############################################################################
  def paintEvent               ( self , paintEvent                         ) :
    ##########################################################################
    if                         ( not self . m_displayedWhenStopped         ) :
      if                       ( not self . isAnimated ( )                 ) :
        return
    ##########################################################################
    w       = self . width     (                                             )
    if                         ( self . height ( ) < w                     ) :
      w     = self . height    (                                             )
    ##########################################################################
    p       = QPainter         ( self                                        )
    p       . setRenderHint    ( QPainter . Antialiasing                     )
    ##########################################################################
    outerRadius    = float     ( ( w - 1 )   * 0.50                          )
    innerRadius    = float     ( outerRadius * self . m_factor               )
    ##########################################################################
    capsuleHeight  = float     ( outerRadius - innerRadius                   )
    capsuleWidth   = float     ( capsuleHeight * 0.35                        )
    if                         ( w > 32                                    ) :
      capsuleWidth = float     ( capsuleHeight * 0.23                        )
    ##########################################################################
    capsuleRadius  = float     ( capsuleWidth / 2                            )
    cornerHeight   = - float   ( innerRadius + capsuleHeight                 )
    ##########################################################################
    gap            = self . m_count
    angle          = float     ( 360.0        / gap                          )
    ##########################################################################
    for i in range             ( 0 , gap                                   ) :
      ########################################################################
      color = self . m_color
      alpha = float            ( 1.0 - float ( float ( i ) / float ( gap ) ) )
      color . setAlphaF        ( alpha                                       )
      ########################################################################
      p     . setPen           ( Qt . NoPen                                  )
      p     . setBrush         ( QBrush ( color )                            )
      p     . save             (                                             )
      p     . translate        ( self . rect ( ) . center ( )                )
      p     . rotate           ( self . m_angle - ( float ( i ) * angle )    )
      p     . drawRoundedRect  ( - int   ( capsuleRadius )                 , \
                                   int   ( cornerHeight  )                 , \
                                   int   ( capsuleWidth  )                 , \
                                   int   ( capsuleHeight )                 , \
                                   float ( capsuleRadius )                 , \
                                   float ( capsuleRadius )                   )
      p     . restore          (                                             )
    ##########################################################################
    return
##############################################################################
