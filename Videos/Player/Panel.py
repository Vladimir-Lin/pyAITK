# -*- coding: utf-8 -*-
##############################################################################
## Panel
## 影片播放控制板
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
from   PySide6                     import QtCore
from   PySide6                     import QtGui
from   PySide6                     import QtWidgets
from   PySide6 . QtCore            import *
from   PySide6 . QtGui             import *
from   PySide6 . QtWidgets         import *
from   AITK    . Qt6               import *
##############################################################################
from   AITK    . Qt6 . MenuManager import MenuManager as MenuManager
from   AITK    . Qt6 . Widget      import Widget      as Widget
##############################################################################
class Panel                        ( Widget                                ) :
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    self . Configure     (                                                   )
    ##########################################################################
    return
  ############################################################################
  def Configure                   ( self                                   ) :
    ##########################################################################
    PAL  = self     . palette     (                                          )
    BKC  = QColor                 ( 255 , 255 , 255 , 255                    )
    PAL  . setColor               ( QPalette . Window , BKC                  )
    self . setAutoFillBackground  ( True                                     )
    self . setPalette             ( PAL                                      )
    ##########################################################################
    self . Clock    = QSlider     ( Qt . Horizontal , self                   )
    self . Clock    . setMaximum  ( 1000                                     )
    self . Clock    . show        (                                          )
    ##########################################################################
    self . Volume   = QSlider     ( Qt . Horizontal , self                   )
    self . Volume   . setMaximum  ( 100                                      )
    self . Volume   . show        (                                          )
    ##########################################################################
    PICO            = QIcon       ( ":/images/PlayerPlay.png"                )
    self . Play     = QPushButton ( PICO , "" , self                         )
    self . Play     . setIconSize ( QSize ( 48 , 48                        ) )
    self . Play     . setFlat     ( True                                     )
    self . Play     . setEnabled  ( False                                    )
    self . Play     . show        (                                          )
    ##########################################################################
    SICO            = QIcon       ( ":/images/StopPlay.png"                  )
    self . Stop     = QPushButton ( SICO , "" , self                         )
    self . Stop     . setIconSize ( QSize ( 48 , 48                        ) )
    self . Stop     . setFlat     ( True                                     )
    self . Stop     . setEnabled  ( False                                    )
    self . Stop     . show        (                                          )
    ##########################################################################
    EICO            = QIcon       ( ":/images/PlayPause.png"                 )
    self . Pause    = QPushButton ( EICO , "" , self                         )
    self . Pause    . setIconSize ( QSize ( 48 , 48                        ) )
    self . Pause    . setFlat     ( True                                     )
    self . Pause    . setEnabled  ( False                                    )
    self . Pause    . hide        (                                          )
    ##########################################################################
    FICO            = QIcon       ( ":/images/hidewindow.png"                )
    self . BWin     = QPushButton ( FICO , "" , self                         )
    self . BWin     . setIconSize ( QSize ( 48 , 48                        ) )
    self . BWin     . setFlat     ( True                                     )
    self . BWin     . setEnabled  ( True                                     )
    self . BWin     . hide        (                                          )
    ##########################################################################
    CICO            = QIcon       ( ":/images/computer.png"                  )
    self . SWin     = QPushButton ( CICO , "" , self                         )
    self . SWin     . setIconSize ( QSize ( 48 , 48                        ) )
    self . SWin     . setFlat     ( True                                     )
    self . SWin     . setEnabled  ( True                                     )
    self . SWin     . show        (                                          )
    ##########################################################################
    MICO            = QIcon       ( ":/images/hidespeech.png"                )
    self . MWin     = QPushButton ( MICO , "" , self                         )
    self . MWin     . setIconSize ( QSize ( 48 , 48                        ) )
    self . MWin     . setFlat     ( True                                     )
    self . MWin     . setEnabled  ( True                                     )
    self . MWin     . hide        (                                          )
    ##########################################################################
    self . CLabel   = QLabel      ( self                                     )
    self . CLabel   . show        (                                          )
    ##########################################################################
    self . FLabel   = QLabel      ( self                                     )
    self . FLabel   . show        (                                          )
    ##########################################################################
    self . WinSize  = QLabel      ( self                                     )
    self . WinSize  . show        (                                          )
    ##########################################################################
    self . FilmSize = QLabel      ( self                                     )
    self . FilmSize . show        (                                          )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def showEvent            ( self , e                                      ) :
    ##########################################################################
    super ( ) . showEvent  (        e                                        )
    self      . Relocation (                                                 )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , e                                     ) :
    ##########################################################################
    super ( ) . resizeEvent (        e                                       )
    self      . Relocation  (                                                )
    ##########################################################################
    return
  ############################################################################
  def Relocation                  ( self                                   ) :
    ##########################################################################
    W    = self     . width       (                                          )
    ##########################################################################
    self . Clock    . setGeometry (       0 ,  0 ,   W , 16                  )
    ##########################################################################
    self . CLabel   . setGeometry ( W - 120 , 16 , 120 , 16                  )
    self . FLabel   . setGeometry ( W - 120 , 32 , 120 , 16                  )
    self . Volume   . setGeometry ( W - 120 , 48 , 120 , 16                  )
    ##########################################################################
    self . FilmSize . setGeometry ( W - 240 , 16 , 120 , 24                  )
    self . WinSize  . setGeometry ( W - 240 , 40 , 120 , 24                  )
    ##########################################################################
    self . Play     . setGeometry (       0 , 16 ,  48 , 48                  )
    self . Pause    . setGeometry (       0 , 16 ,  48 , 48                  )
    self . Stop     . setGeometry (      48 , 16 ,  48 , 48                  )
    self . BWin     . setGeometry (      96 , 16 ,  48 , 48                  )
    self . SWin     . setGeometry (     144 , 16 ,  48 , 48                  )
    self . MWin     . setGeometry (     144 , 16 ,  48 , 48                  )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Menu ( self , pos                                                    ) :
    ##########################################################################
    if     ( not self . isPrepared ( )                                     ) :
      return False
    ##########################################################################
    ##########################################################################
    return True
##############################################################################
