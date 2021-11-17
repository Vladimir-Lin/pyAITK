# -*- coding: utf-8 -*-
##############################################################################
## ClipboardView
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import random
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
from   PyQt5 . QtCore                    import QUrl
##############################################################################
from   PyQt5 . QtGui                     import QIcon
from   PyQt5 . QtGui                     import QPixmap
from   PyQt5 . QtGui                     import QImage
from   PyQt5 . QtGui                     import QCursor
from   PyQt5 . QtGui                     import QKeySequence
from   PyQt5 . QtGui                     import QTextDocument
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
from   AITK  . Qt        . SpinBox       import SpinBox       as SpinBox
from   AITK  . Qt        . TextEdit      import TextEdit      as TextEdit
##############################################################################
class ClipboardView            ( TextEdit                                  ) :
  ############################################################################
  HavingMenu  = 1371434312
  ############################################################################
  emitAddText     = pyqtSignal ( str                                         )
  emitWindowIcon  = pyqtSignal ( bool                                        )
  ############################################################################
  def __init__                 ( self , parent = None , plan = None        ) :
    ##########################################################################
    super ( ) . __init__       ( parent , plan                               )
    ##########################################################################
    self . dockingOrientation = Qt . Horizontal
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea                   | \
                                Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                                
    ##########################################################################
    self . setFunction         ( self . FunctionDocking , True               )
    self . setFunction         ( self . HavingMenu      , True               )
    ##########################################################################
    self     . setPrepared     ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                 ( self                                      ) :
    return QSize               ( 800 , 600                                   )
  ############################################################################
  def FocusIn                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return False
    ##########################################################################
    self . setActionLabel        ( "Label"   , self . windowTitle ( )        )
    ##########################################################################
    self . LinkAction            ( "Refresh"   , self . startup              )
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
  def ZoomIn                       ( self                                  ) :
    self . zoomIn                  ( 1                                       )
    return
  ############################################################################
  def ZoomOut                      ( self                                  ) :
    self . zoomOut                 ( 1                                       )
    return
  ############################################################################
  def startup                     ( self                                   ) :
    ##########################################################################
    clip     = qApp . clipboard   (                                          )
    ##########################################################################
    self     . clear              (                                          )
    ##########################################################################
    if                            ( clip in [ False , None ]               ) :
      return False
    ##########################################################################
    lmsg     = "-------------------------------------------------------------"
    pix      = clip . pixmap      (                                          )
    txt      = clip . text        (                                          )
    mime     = clip . mimeData    (                                          )
    ##########################################################################
    if                            ( clip . ownsClipboard ( )               ) :
      ########################################################################
      msg    = "Application owns clipboard."
      self   . append             ( msg                                      )
    ##########################################################################
    if                            ( clip . ownsFindBuffer ( )              ) :
      ########################################################################
      msg    = "Application has 'find buffer' functionality."
      self   . append             ( msg                                      )
    ##########################################################################
    if                            ( clip . ownsSelection ( )              ) :
      ########################################################################
      msg    = "Application has selections."
      self   . append             ( msg                                      )
    ##########################################################################
    if                            ( len ( txt ) > 0                        ) :
      ########################################################################
      msg    = "Clipboard text : "
      self   . append             ( lmsg                                     )
      self   . append             ( msg                                      )
      self   . append             ( txt                                      )
      self   . append             ( lmsg                                     )
    ##########################################################################
    if                            ( not pix . isNull ( )                   ) :
      ########################################################################
      imgid  = random . randint   ( 1000000 , 9999999                        )
      img    = pix    . toImage   (                                          )
      path   = "file://{0}.png" . format ( imgid                             )
      uri    = QUrl               ( path                                     )
      self   . document ( ) . addResource                                  ( \
                                    QTextDocument . ImageResource          , \
                                    uri                                    , \
                                    img                                      )
      msg    = "Pixmap : "
      self   . append             ( msg                                      )
      self   . append             ( lmsg                                     )
      msg    = "<img src='{0}'>" . format ( uri . toString ( )               )
      self   . append             ( msg                                      )
      self   . append             ( lmsg                                     )
    ##########################################################################
    if                            ( mime in [ False , None ]               ) :
      return True
    ##########################################################################
    msg      = "Application has mime data."
    self     . append             ( msg                                      )
    ##########################################################################
    if                            ( mime . hasText ( )                     ) :
      ########################################################################
      msg    = "Mime text : "
      self   . append             ( msg                                      )
      self   . append             ( lmsg                                     )
      self   . append             ( mime . text ( )                          )
      self   . append             ( lmsg                                     )
    ##########################################################################
    if                            ( mime . hasHtml ( )                     ) :
      ########################################################################
      msg    = "Mime HTML : "
      self   . append             ( msg                                      )
      self   . append             ( lmsg                                     )
      self   . append             ( mime . html ( )                          )
      self   . append             ( lmsg                                     )
    ##########################################################################
    if                            ( mime . hasUrls ( )                     ) :
      ########################################################################
      urls   = mime . urls        (                                          )
      ########################################################################
      msg    = "Mime URLs : "
      self   . append             ( msg                                      )
      self   . append             ( "<hr>"                                   )
      self   . append             ( lmsg                                     )
      for u in urls                                                          :
        self . append             ( u . toString ( )                         )
      self   . append             ( lmsg                                     )
    ##########################################################################
    if                            ( mime . hasColor ( )                    ) :
      ########################################################################
      color   = mime . colorData  (                                          )
      msg     = "Mime Color : "
      self    . append            ( msg                                      )
      self    . append            ( lmsg                                     )
      ########################################################################
      msg     = "[ R , G , B , A ] = [ {0} , {1} , {2} , {3} ]" . format   ( \
                  color . red   ( )                                        , \
                  color . green ( )                                        , \
                  color . blue  ( )                                        , \
                  color . alpha ( )                                          )
      self    . append            ( msg                                      )
      ########################################################################
      self    . append            ( lmsg                                     )
    ##########################################################################
    if                            ( mime . hasImage ( )                    ) :
      ########################################################################
      imgid  = random . randint   ( 1000000 , 9999999                        )
      img    = mime . imageData   (                                          )
      path   = "file://{0}.png" . format ( imgid                             )
      uri    = QUrl               ( path                                     )
      self   . document ( ) . addResource                                  ( \
                                    QTextDocument . ImageResource          , \
                                    uri                                    , \
                                    img                                      )
      msg    = "Mime Image : "
      self   . append             ( msg                                      )
      self   . append             ( lmsg                                     )
      msg    = "<img src='{0}'>" . format ( uri . toString ( )               )
      self   . append             ( msg                                      )
      self   . append             ( lmsg                                     )
    ##########################################################################
    Formats  = mime . formats     (                                          )
    for f in Formats                                                         :
      if                          ( mime . hasFormat ( f )                 ) :
        ######################################################################
        D    = mime . data        ( f                                        )
        ######################################################################
        if                        ( D . size ( ) > 0                       ) :
          ####################################################################
          self . append           ( "Data : {0}" . format ( f              ) )
          self . append           ( "Size : {0}" . format ( D . size ( )   ) )
          ####################################################################
          self . append           ( lmsg                                     )
          ####################################################################
          HBD  = D . toHex        (                                          )
          BB   = ""
          SS   = ""
          ####################################################################
          try                                                                :
            BB = HBD . data       (                                          )
          except                                                             :
            pass
          ####################################################################
          try                                                                :
            SS = BB . decode      ( "utf-8"                                  )
          except                                                             :
            pass
          ####################################################################
          self . append           ( SS . upper ( )                           )
          self . append           ( lmsg                                     )
    ##########################################################################
    return
  ############################################################################
  def TextingMenu               ( self , mm                                ) :
    ##########################################################################
    TRX = self . Translations
    LOM = mm   . addMenu        (              TRX [ "UI::Texting"         ] )
    ##########################################################################
    mm  . addActionFromMenu     ( LOM , 1001 , TRX [ "UI::ClearAll"        ] )
    mm  . addActionFromMenu     ( LOM , 1002 , TRX [ "UI::CopyToClipboard" ] )
    mm  . addActionFromMenu     ( LOM , 1003 , TRX [ "UI::SelectAll"       ] )
    ##########################################################################
    return mm
  ############################################################################
  def RunTextingMenu               ( self , at                             ) :
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
    return False
  ############################################################################
  def DisplayMenu               ( self , mm                                ) :
    ##########################################################################
    TRX = self . Translations
    LOM = mm   . addMenu        (              TRX [ "UI::Display"         ] )
    ##########################################################################
    mm  . addActionFromMenu     ( LOM , 1004 , TRX [ "UI::ZoomIn"          ] )
    mm  . addActionFromMenu     ( LOM , 1005 , TRX [ "UI::ZoomOut"         ] )
    ##########################################################################
    return mm
  ############################################################################
  def RunDisplayMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at == 1004                            ) :
      self . ZoomIn                (                                         )
      return True
    ##########################################################################
    if                             ( at == 1005                            ) :
      self . ZoomOut               (                                         )
      return True
    ##########################################################################
    return False
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
    mm     . addAction             ( 1001 , TRX [ "UI::Refresh"            ] )
    mm     . addAction             ( 1002 , TRX [ "UI::ClearClipboard"     ] )
    ##########################################################################
    mm     = self . TextingMenu    ( mm                                      )
    mm     = self . DisplayMenu    ( mm                                      )
    ##########################################################################
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    self   . Notify                ( 0                                       )
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunTextingMenu ( at      )     ) :
      return True
    ##########################################################################
    if                             ( self . RunDisplayMenu ( at      )     ) :
      return True
    ##########################################################################
    if                             ( self . RunDocking     ( mm , aa )     ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1002                            ) :
      qApp . clipboard ( ) . clear (                                         )
      return True
    ##########################################################################
    return True
##############################################################################
