# -*- coding: utf-8 -*-
##############################################################################
## VoiceTracker
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
from   opencc                            import OpenCC
from   googletrans                       import Translator
##############################################################################
from   PyQt5                             import QtCore
from   PyQt5                             import QtGui
from   PyQt5                             import QtWidgets
##############################################################################
from   PyQt5 . QtCore                    import QObject
from   PyQt5 . QtCore                    import pyqtSignal
from   PyQt5 . QtCore                    import pyqtSlot
from   PyQt5 . QtCore                    import Qt
from   PyQt5 . QtCore                    import QPoint
from   PyQt5 . QtCore                    import QPointF
from   PyQt5 . QtCore                    import QSize
##############################################################################
from   PyQt5 . QtGui                     import QIcon
from   PyQt5 . QtGui                     import QCursor
from   PyQt5 . QtGui                     import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets                 import QApplication
from   PyQt5 . QtWidgets                 import QWidget
from   PyQt5 . QtWidgets                 import qApp
from   PyQt5 . QtWidgets                 import QMenu
from   PyQt5 . QtWidgets                 import QAction
from   PyQt5 . QtWidgets                 import QShortcut
from   PyQt5 . QtWidgets                 import QMenu
from   PyQt5 . QtWidgets                 import QAbstractItemView
from   PyQt5 . QtWidgets                 import QTreeWidget
from   PyQt5 . QtWidgets                 import QTreeWidgetItem
from   PyQt5 . QtWidgets                 import QLineEdit
from   PyQt5 . QtWidgets                 import QComboBox
from   PyQt5 . QtWidgets                 import QSpinBox
##############################################################################
from   AITK  . Calendars . StarDate      import StarDate      as StarDate
##############################################################################
from   AITK  . Qt        . MenuManager   import MenuManager   as MenuManager
from   AITK  . Qt        . PlainTextEdit import PlainTextEdit as PlainTextEdit
##############################################################################
class VoiceTracker         ( PlainTextEdit                                 ) :
  ############################################################################
  HavingMenu  = 1371434312
  ############################################################################
  emitAddText    = pyqtSignal ( str                                          )
  emitWindowIcon = pyqtSignal ( bool                                         )
  ############################################################################
  def __init__             ( self , parent = None , plan = None            ) :
    ##########################################################################
    super ( ) . __init__   ( parent , plan                                   )
    ##########################################################################
    self . dockingOrientation = Qt . Horizontal
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea                   | \
                                Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                                
    ##########################################################################
    self . setFunction     ( self . FunctionDocking , True                   )
    self . setFunction     ( self . HavingMenu      , True                   )
    ##########################################################################
    self . emitAddText    . connect ( self . appendPlainText                 )
    self . emitWindowIcon . connect ( self . assignWindowIcon                )
    ##########################################################################
    self . setReadOnly     ( True                                            )
    self . TZ          = "Asia/Taipei"
    self . Recognizer  = None
    self . Execution   = None
    self . DoExecution = True
    self . ShowParser  = True
    self . ShowError   = False
    self . ShowReading = False
    self . DoSplit     = True
    ##########################################################################
    self . LangOn      = { "zh-TW" : False , "en-US" : False , "ja" : False  }
    self . onOff       = False
    self . onIcon      = None
    self . offIcon     = None
    ##########################################################################
    self     . setPrepared         ( True                                    )
    ##########################################################################
    return
  ############################################################################
  def sizeHint            ( self                                           ) :
    return QSize          ( 320 , 240                                        )
  ############################################################################
  def FocusIn                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return False
    ##########################################################################
    self . setActionLabel        ( "Label"   , self . windowTitle ( )        )
    ##########################################################################
    self . LinkAction            ( "Delete"    , self . clear                )
    self . LinkAction            ( "Copy"      , self . copy                 )
    self . LinkAction            ( "SelectAll" , self . selectAll            )
    self . LinkAction            ( "ZoomIn"    , self . ZoomIn               )
    self . LinkAction            ( "ZoomOut"   , self . ZoomOut              )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return False
    ##########################################################################
    return False
  ############################################################################
  def CurrentMoment              ( self , TZ = "Asia/Taipei"               ) :
    ##########################################################################
    NOW = StarDate               (                                           )
    NOW . Now                    (                                           )
    DTS = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"        )
    ##########################################################################
    return DTS
  ############################################################################
  def addText                 ( self , message                             ) :
    ##########################################################################
    self . emitAddText . emit (        message                               )
    ##########################################################################
    return
  ############################################################################
  def assignWindowIcon     ( self , onOff                                  ) :
    ##########################################################################
    if                     ( onOff                                         ) :
      self . setWindowIcon ( self . onIcon                                   )
    else                                                                     :
      self . setWindowIcon ( self . offIcon                                  )
    ##########################################################################
    return
  ############################################################################
  def Parser                   ( self , language , message , timestamp     ) :
    ##########################################################################
    if                         ( len ( message ) <= 0                      ) :
      return
    ##########################################################################
    if                         ( self . ShowParser                         ) :
      ########################################################################
      NOW = StarDate           (                                             )
      NOW . Stardate = timestamp
      CMT = NOW . toDateTimeString ( self.TZ , " " , "%Y/%m/%d" , "%H:%M:%S" )
      ########################################################################
      MSG = f"{CMT} ( {language} ) : {message}"
      self . addText           ( MSG                                         )
    ##########################################################################
    if                         ( self . DoExecution                        ) :
      ########################################################################
      if                       ( self . Execution != None                  ) :
        ######################################################################
        RR = self . Execution  ( language , message , timestamp              )
        if                     ( "Match" in RR                             ) :
          if                   ( RR [ "Match"   ]                          ) :
            self . addText     ( RR [ "Message" ]                            )
    ##########################################################################
    return
  ############################################################################
  def Error               ( self , language , code , message , timestamp   ) :
    ##########################################################################
    if                    ( not self . ShowError                           ) :
      return
    ##########################################################################
    if                    ( code in [ 1002 , 2001 , 3001 ]                 ) :
      return
    ##########################################################################
    NOW = StarDate               (                                           )
    NOW . Stardate = timestamp
    CMT = NOW . toDateTimeString ( self . TZ , " " , "%Y/%m/%d" , "%H:%M:%S" )
    ##########################################################################
    MSG = f"{CMT} ( {language} ) Error - {code} : {message}"
    self . addText             ( MSG                                         )
    ##########################################################################
    return
  ############################################################################
  def Reading                      ( self , language , onOff , timestamp   ) :
    ##########################################################################
    if                             ( not self . ShowReading                ) :
      return
    ##########################################################################
    self    . LangOn [ language ] = onOff
    ##########################################################################
    OFX     = False
    KEYs    = self . LangOn . keys (                                         )
    for K in KEYs                                                            :
      if                           ( self . LangOn [ K ]                   ) :
        OFX = True
    ##########################################################################
    if                             ( OFX == self . onOff                   ) :
      return
    ##########################################################################
    self . onOff = OFX
    ##########################################################################
    self . emitWindowIcon . emit   ( OFX                                     )
    ##########################################################################
    ## print ( "Reading : " , language , " => " , onOff )
    ##########################################################################
    return
  ############################################################################
  def ZoomIn                       ( self                                  ) :
    self . zoomIn                  ( 1                                       )
    return
  ############################################################################
  def ZoomOut                      ( self                                  ) :
    self . zoomOut                 ( 1                                       )
    return
  ############################################################################
  def LocIdToLC                    ( self , Id                             ) :
    ##########################################################################
    if                             ( Id == 1001                            ) :
      return "en-US"
    ##########################################################################
    if                             ( Id == 1002                            ) :
      return "zh-TW"
    ##########################################################################
    if                             ( Id == 1006                            ) :
      return "ja"
    ##########################################################################
    return ""
  ############################################################################
  def LocalityMenu                 ( self , mm                             ) :
    ##########################################################################
    TRX   = self . Translations
    LOC   = self . Translations   [ "NamesEditor" ] [ "Languages"           ]
    ##########################################################################
    msg   = TRX  [ "NamesEditor" ] [ "Menus" ] [ "Language" ]
    LOM   = mm . addMenu           ( msg                                     )
    ##########################################################################
    KEYs  = LOC . keys             (                                         )
    ##########################################################################
    for K in KEYs                                                            :
      msg   = LOC                  [ K                                       ]
      V     = int                  ( K                                       )
      if                           ( V in [ 1001 , 1002 , 1006 ]           ) :
        LC  = self . LocIdToLC     ( V                                       )
        hid =                      ( LC in self . Recognizer . Languages     )
        mm  . addActionFromMenu    ( LOM , 10000000 + V , msg , True , hid   )
    ##########################################################################
    return mm
  ############################################################################
  def RunLocality       ( self , at                                        ) :
    ##########################################################################
    if                  ( not ( ( at >= 10000000 ) and ( at < 11000000 ) ) ) :
      return False
    ##########################################################################
    V  = at   - 10000000
    LC = self . LocIdToLC ( V                                                )
    ##########################################################################
    if                    ( len ( LC ) <= 0                                ) :
      return True
    ##########################################################################
    if                    ( LC in self . Recognizer . Languages            ) :
      self . Recognizer . Languages . remove ( LC                            )
    else                                                                     :
      self . Recognizer . Languages . append ( LC                            )
    ##########################################################################
    return True
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     . addAction             ( 1001 , "清除全部" )
    mm     . addAction             ( 1002 , "複製" )
    mm     . addAction             ( 1003 , "選取全部" )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     . addAction             ( 1004 , "放大" )
    mm     . addAction             ( 1005 , "縮小" )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     . addAction             ( 2001                                  , \
                                     TRX [ "UI::Execution" ]               , \
                                     True                                  , \
                                     self . DoExecution                      )
    mm     . addAction             ( 2002                                  , \
                                     "語音活動偵測" , \
                                     True                                  , \
                                     self . DoSplit                          )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . LocalityMenu   ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    self   . Notify                ( 0                                       )
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . RunLocality  ( at      )       ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . clear                 (                                         )
      return True
    ##########################################################################
    if                             ( at == 1002                            ) :
      self . copy                  (                                         )
      return True
    ##########################################################################
    if                             ( at == 1003                            ) :
      self . selectAll             (                                         )
      return True
    ##########################################################################
    if                             ( at == 1004                            ) :
      self . ZoomIn                (                                         )
      return True
    ##########################################################################
    if                             ( at == 1005                            ) :
      self . ZoomOut               (                                         )
      return True
    ##########################################################################
    if                             ( at == 2001                            ) :
      if                           ( self . DoExecution                    ) :
        self . DoExecution = False
      else                                                                   :
        self . DoExecution = True
    ##
    ##########################################################################
    if                             ( at == 2002                            ) :
      if                           ( self . DoSplit                        ) :
        self . DoSplit  = False
      else                                                                   :
        self . DoSplit  = True
      self . Recognizer . DoSplit = self . DoSplit
    ##########################################################################
    return True
##############################################################################
