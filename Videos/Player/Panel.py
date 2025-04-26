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
from                 . FilmBar     import FilmBar     as FilmBar
##############################################################################
class Panel              ( Widget                                          ) :
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    self . Configure     (                                                   )
    ##########################################################################
    return
  ############################################################################
  def Configure                     ( self                                 ) :
    ##########################################################################
    PAL  = self     . palette       (                                        )
    BKC  = QColor                   ( 255 , 255 , 255 , 255                  )
    PAL  . setColor                 ( QPalette . Window , BKC                )
    self . setAutoFillBackground    ( True                                   )
    self . setPalette               ( PAL                                    )
    ##########################################################################
    self . Bar      = FilmBar       ( self , self . PlanFunc                 )
    self . Bar      . show          (                                        )
    ##########################################################################
    self . Clock    = QSlider       ( Qt . Horizontal , self                 )
    self . Clock    . setMaximum    ( 1000                                   )
    self . Clock    . setSingleStep ( 1                                      )
    self . Clock    . show          (                                        )
    ##########################################################################
    self . Volume   = QSlider       ( Qt . Horizontal , self                 )
    self . Volume   . setMaximum    ( 100                                    )
    self . Volume   . setSingleStep ( 1                                      )
    self . Volume   . show          (                                        )
    ##########################################################################
    PICO            = QIcon         ( ":/images/PlayerPlay.png"              )
    self . Play     = QPushButton   ( PICO , "" , self                       )
    self . Play     . setIconSize   ( QSize ( 40 , 40                      ) )
    self . Play     . setFlat       ( True                                   )
    self . Play     . setEnabled    ( False                                  )
    self . Play     . show          (                                        )
    ##########################################################################
    SICO            = QIcon         ( ":/images/StopPlay.png"                )
    self . Stop     = QPushButton   ( SICO , "" , self                       )
    self . Stop     . setIconSize   ( QSize ( 40 , 40                      ) )
    self . Stop     . setFlat       ( True                                   )
    self . Stop     . setEnabled    ( False                                  )
    self . Stop     . show          (                                        )
    ##########################################################################
    EICO            = QIcon         ( ":/images/PlayPause.png"               )
    self . Pause    = QPushButton   ( EICO , "" , self                       )
    self . Pause    . setIconSize   ( QSize ( 40 , 40                      ) )
    self . Pause    . setFlat       ( True                                   )
    self . Pause    . setEnabled    ( False                                  )
    self . Pause    . hide          (                                        )
    ##########################################################################
    FICO            = QIcon         ( ":/images/hidewindow.png"              )
    self . BWin     = QPushButton   ( FICO , "" , self                       )
    self . BWin     . setIconSize   ( QSize ( 40 , 40                      ) )
    self . BWin     . setFlat       ( True                                   )
    self . BWin     . setEnabled    ( True                                   )
    self . BWin     . hide          (                                        )
    ##########################################################################
    CICO            = QIcon         ( ":/images/computer.png"                )
    self . SWin     = QPushButton   ( CICO , "" , self                       )
    self . SWin     . setIconSize   ( QSize ( 40 , 40                      ) )
    self . SWin     . setFlat       ( True                                   )
    self . SWin     . setEnabled    ( True                                   )
    self . SWin     . show          (                                        )
    ##########################################################################
    MICO            = QIcon         ( ":/images/hidespeech.png"              )
    self . MWin     = QPushButton   ( MICO , "" , self                       )
    self . MWin     . setIconSize   ( QSize ( 40 , 40                      ) )
    self . MWin     . setFlat       ( True                                   )
    self . MWin     . setEnabled    ( True                                   )
    self . MWin     . hide          (                                        )
    ##########################################################################
    AICO            = QIcon         ( ":/images/galleries.png"               )
    self . Analysis = QPushButton   ( AICO , "" , self                       )
    self . Analysis . setIconSize   ( QSize ( 40 , 40                      ) )
    self . Analysis . setFlat       ( True                                   )
    self . Analysis . setEnabled    ( True                                   )
    self . Analysis . hide          (                                        )
    ##########################################################################
    DICO            = QIcon         ( ":/images/drawing.png"                 )
    self . Drawing  = QPushButton   ( DICO , "" , self                       )
    self . Drawing  . setIconSize   ( QSize ( 40 , 40                      ) )
    self . Drawing  . setFlat       ( True                                   )
    self . Drawing  . setEnabled    ( True                                   )
    self . Drawing  . setCheckable  ( True                                   )
    self . Drawing  . hide          (                                        )
    ##########################################################################
    DICO            = QIcon         ( ":/images/Menu.png"                    )
    self . VMenu    = QPushButton   ( DICO , "" , self                       )
    self . VMenu    . setIconSize   ( QSize ( 40 , 40                      ) )
    self . VMenu    . setFlat       ( True                                   )
    self . VMenu    . setEnabled    ( True                                   )
    self . VMenu    . setCheckable  ( True                                   )
    self . VMenu    . hide          (                                        )
    ##########################################################################
    self . FineTune = QSlider       ( Qt . Horizontal , self                 )
    self . FineTune . setMaximum    ( 3000                                   )
    self . FineTune . setSingleStep ( 1                                      )
    self . FineTune . hide          (                                        )
    self . FineTune . setEnabled    ( False                                  )
    ##########################################################################
    FNT  = self     . font          (                                        )
    FNT  . setPixelSize             ( 12                                     )
    ##########################################################################
    self . CLabel   = QLabel        ( self                                   )
    self . CLabel   . setFont       ( FNT                                    )
    self . CLabel   . show          (                                        )
    ##########################################################################
    self . FLabel   = QLabel        ( self                                   )
    self . FLabel   . setFont       ( FNT                                    )
    self . FLabel   . show          (                                        )
    ##########################################################################
    FNT  = self     . font          (                                        )
    FNT  . setPixelSize             ( 20                                     )
    ##########################################################################
    self . WinSize  = QLabel        ( self                                   )
    self . WinSize  . setFont       ( FNT                                    )
    self . WinSize  . show          (                                        )
    ##########################################################################
    self . FilmSize = QLabel        ( self                                   )
    self . FilmSize . setFont       ( FNT                                    )
    self . FilmSize . show          (                                        )
    ##########################################################################
    self . DeltaEditor = None
    ##########################################################################
    return
  ############################################################################
  def UpdatePanel                  ( self                                  ) :
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "Play"                     ]
    self . Play     . setToolTip   ( MSG                                     )
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "Stop"                     ]
    self . Stop     . setToolTip   ( MSG                                     )
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "Pause"                    ]
    self . Pause    . setToolTip   ( MSG                                     )
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "NormalWindow"             ]
    self . BWin     . setToolTip   ( MSG                                     )
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "Stacked"                  ]
    self . SWin     . setToolTip   ( MSG                                     )
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "MDI"                      ]
    self . MWin     . setToolTip   ( MSG                                     )
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "Analysis"                 ]
    self . Analysis . setToolTip   ( MSG                                     )
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "Drawing"                  ]
    self . Drawing  . setToolTip   ( MSG                                     )
    ##########################################################################
    MSG  = self     . Translations [ "Player" ] [ "VMenu"                    ]
    self . VMenu    . setToolTip   ( MSG                                     )
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
    self . Bar      . setGeometry (       0 ,  0 ,   W ,  8                  )
    self . Clock    . setGeometry (       0 ,  8 ,   W , 16                  )
    ##########################################################################
    self . CLabel   . setGeometry ( W -  80 , 24 ,  80 , 12                  )
    self . FLabel   . setGeometry ( W -  80 , 36 ,  80 , 12                  )
    self . Volume   . setGeometry ( W -  80 , 48 ,  80 , 16                  )
    ##########################################################################
    self . FilmSize . setGeometry ( W - 200 , 24 , 120 , 20                  )
    self . WinSize  . setGeometry ( W - 200 , 44 , 120 , 20                  )
    ##########################################################################
    self . Play     . setGeometry (       0 , 24 ,  40 , 40                  )
    self . Pause    . setGeometry (       0 , 24 ,  40 , 40                  )
    self . Stop     . setGeometry (      40 , 24 ,  40 , 40                  )
    self . BWin     . setGeometry (      80 , 24 ,  40 , 40                  )
    self . SWin     . setGeometry (     120 , 24 ,  40 , 40                  )
    self . MWin     . setGeometry (     120 , 24 ,  40 , 40                  )
    self . Analysis . setGeometry (     160 , 24 ,  40 , 40                  )
    self . Drawing  . setGeometry (     200 , 24 ,  40 , 40                  )
    self . VMenu    . setGeometry (     240 , 24 ,  40 , 40                  )
    ##########################################################################
    self . FineTune . setGeometry (       0 , 64 ,   W , 16                  )
    ##########################################################################
    if ( self . DeltaEditor not in [ False , None ]                        ) :
      ########################################################################
      self . DeltaEditor . setGeometry ( 300 , 24 ,  120 , 24                )
    ##########################################################################
    return
  ############################################################################
  def addDelta                       ( self , widget , V                   ) :
    ##########################################################################
    if ( self . DeltaEditor not in [ False , None ]                        ) :
      return
    ##########################################################################
    DSP  = QSpinBox                  ( self                                  )
    DSP  . setMinimum                ( 1                                     )
    DSP  . setMaximum                ( 600 * 1000                            )
    DSP  . setSingleStep             ( 10                                    )
    DSP  . setValue                  ( V                                     )
    ##########################################################################
    DSP  . valueChanged    . connect ( widget . StepChanged                  )
    DSP  . editingFinished . connect ( self   . removeDelta                  )
    ##########################################################################
    self . DeltaEditor = DSP
    DSP  . show                      (                                       )
    self . Relocation                (                                       )
    ##########################################################################
    return
  ############################################################################
  def removeDelta ( self                                                   ) :
    ##########################################################################
    if            ( self . DeltaEditor in [ False , None ]                 ) :
      return
    ##########################################################################
    DELX               = self . DeltaEditor
    self . DeltaEditor = None
    DELX               . deleteLater (                                       )
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
