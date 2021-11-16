# -*- coding: utf-8 -*-
##############################################################################
## SmartNote
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
from   AITK  . Qt        . SpinBox       import SpinBox       as SpinBox
from   AITK  . Qt        . TextEdit      import TextEdit      as TextEdit
##############################################################################
class SmartNote                ( TextEdit                                  ) :
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
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea                   | \
                                Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                                
    ##########################################################################
    self . setFunction         ( self . FunctionDocking , True               )
    self . setFunction         ( self . HavingMenu      , True               )
    ##########################################################################
    self . TZ           = "Asia/Taipei"
    self . VoiceJSON    =      {                                             }
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
    ## self . LinkAction            ( "Delete"    , self . clear                )
    self . LinkAction            ( "Copy"      , self . copy                 )
    self . LinkAction            ( "SelectAll" , self . selectAll            )
    self . LinkAction            ( "ZoomIn"    , self . ZoomIn               )
    self . LinkAction            ( "ZoomOut"   , self . ZoomOut              )
    ## undo redo paste cut clear delete
    ##########################################################################
    self . LinkVoice             ( self . CommandParser                      )
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
  def CommandParser ( self , language , message , timestamp                ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectNone"   , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::OpenSubgroup" , message )  ) :
      if            ( self . OpenCurrentSubgroup ( )                       ) :
        return      { "Match" : True , "Message" : TRX [ "UI::Processed" ]   }
      else                                                                   :
        return      { "Match" : True                                         }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::OpenAlbums"   , message )  ) :
      if            ( self . OpenCurrentAlbum ( )                          ) :
        return      { "Match" : True , "Message" : TRX [ "UI::Processed" ]   }
      else                                                                   :
        return      { "Match" : True                                         }
    ##########################################################################
    return          { "Match" : False                                        }
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
    return True
##############################################################################
