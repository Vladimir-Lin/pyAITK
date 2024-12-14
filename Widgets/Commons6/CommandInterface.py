# -*- coding: utf-8 -*-
##############################################################################
## CommandInterface
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
from   PySide6                            import QtCore
from   PySide6                            import QtGui
from   PySide6                            import QtWidgets
from   PySide6 . QtCore                   import *
from   PySide6 . QtGui                    import *
from   PySide6 . QtWidgets                import *
from   AITK    . Qt6                      import *
##############################################################################
from   AITK    . Qt6        . MenuManager import MenuManager as MenuManager
from   AITK    . Qt6        . LineEdit    import LineEdit    as LineEdit
from   AITK    . Qt6        . ComboBox    import ComboBox    as ComboBox
from   AITK    . Qt6        . SpinBox     import SpinBox     as SpinBox
from   AITK    . Qt6        . TextEdit    import TextEdit    as TextEdit
##############################################################################
from   AITK    . Essentials . Relation    import Relation
from   AITK    . Calendars  . StarDate    import StarDate
from   AITK    . Calendars  . Periode     import Periode
from   AITK    . Documents  . Notes       import Notes
##############################################################################
class CommandInterface    ( TextEdit                                       ) :
  ############################################################################
  HavingMenu     = 1371434312
  ############################################################################
  emitAddText    = Signal ( str                                              )
  emitWindowIcon = Signal ( bool                                             )
  emitInsertText = Signal ( str                                              )
  emitLog        = Signal ( str                                              )
  emitCommand    = Signal ( str                                              )
  ############################################################################
  def __init__            ( self , parent = None , plan = None             ) :
    ##########################################################################
    super ( ) . __init__  ( parent , plan                                    )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea                   | \
                                Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction              ( self . FunctionDocking , True          )
    self . setFunction              ( self . HavingMenu      , True          )
    ##########################################################################
    self . TZ              = "Asia/Taipei"
    ##########################################################################
    self . Filename        = ""
    self . defaultLocality = 1002
    ##########################################################################
    self . emitInsertText . connect ( self . insertPlainText                 )
    ##########################################################################
    self . setPrepared              ( True                                   )
    ##########################################################################
    return
  ############################################################################
  def sizeHint   ( self                                                    ) :
    return QSize ( 800 , 320                                                 )
  ############################################################################
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"     , self . windowTitle ( )             )
    ##########################################################################
    self . LinkAction     ( "Load"      , self . Load                        )
    self . LinkAction     ( "Save"      , self . Save                        )
    self . LinkAction     ( "SaveAs"    , self . SaveAs                      )
    self . LinkAction     ( "Undo"      , self . undo                        )
    self . LinkAction     ( "Redo"      , self . redo                        )
    self . LinkAction     ( "Cut"       , self . cut                         )
    self . LinkAction     ( "Copy"      , self . copy                        )
    self . LinkAction     ( "Paste"     , self . paste                       )
    self . LinkAction     ( "SelectAll" , self . selectAll                   )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut ( self                                                      ) :
    ##########################################################################
    if         ( not self . isPrepared ( )                                 ) :
      return False
    ##########################################################################
    return False
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Load"      , self . Load      , False          )
    self . LinkAction      ( "Save"      , self . Save      , False          )
    self . LinkAction      ( "SaveAs"    , self . SaveAs    , False          )
    self . LinkAction      ( "Undo"      , self . undo      , False          )
    self . LinkAction      ( "Redo"      , self . redo      , False          )
    self . LinkAction      ( "Cut"       , self . cut       , False          )
    self . LinkAction      ( "Copy"      , self . copy      , False          )
    self . LinkAction      ( "Paste"     , self . paste     , False          )
    self . LinkAction      ( "SelectAll" , self . selectAll , False          )
    ##########################################################################
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def doLog               ( self , message                                 ) :
    ##########################################################################
    self . emitLog . emit (        message                                   )
    ##########################################################################
    return
  ############################################################################
  def LoadFileContent        ( self , Filename                             ) :
    ##########################################################################
    TEXT     = ""
    BODY     = ""
    ##########################################################################
    try                                                                      :
      with open              ( Filename , "rb" ) as File                     :
        TEXT = File . read   (                                               )
    except                                                                   :
      return "" , False
    ##########################################################################
    try                                                                      :
      BODY   = TEXT . decode ( "utf-8"                                       )
    except                                                                   :
      return "" , False
    ##########################################################################
    return BODY , True
  ############################################################################
  def SaveFileContent             ( self , Filename                        ) :
    ##########################################################################
    BODY     = self . toPlainText (                                          )
    try                                                                      :
      with open ( Filename , 'w' , encoding = "utf-8" ) as File              :
        File . write              ( BODY                                     )
    except                                                                   :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def LoadFromFilename                   ( self , Filename                 ) :
    ##########################################################################
    if                                   ( len ( Filename ) <= 0           ) :
      self      . Notify                 ( 1                                 )
      return
    ##########################################################################
    BODY , OKAY = self . LoadFileContent ( Filename                          )
    if                                   ( not OKAY                        ) :
      self      . Notify                 ( 1                                 )
      return
    ##########################################################################
    self        . emitInsertText . emit  ( BODY                              )
    self        . Notify                 ( 5                                 )
    ##########################################################################
    return
  ############################################################################
  def LoadFromFile          ( self                                         ) :
    ##########################################################################
    self . LoadFromFilename ( self . Filename                                )
    ##########################################################################
    return
  ############################################################################
  def SaveToFilename                ( self , Filename                      ) :
    ##########################################################################
    if                              ( len ( Filename ) <= 0                ) :
      self . Notify                 ( 1                                      )
      return
    ##########################################################################
    OKAY   = self . SaveFileContent ( Filename                               )
    if                              ( not OKAY                             ) :
      self . Notify                 ( 1                                      )
      return
    ##########################################################################
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def SaveToFile          ( self                                           ) :
    ##########################################################################
    self . SaveToFilename ( self . Filename                                  )
    ##########################################################################
    return
  ############################################################################
  def loading              ( self                                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def startup         ( self                                               ) :
    ##########################################################################
    if                ( not self . isPrepared ( )                          ) :
      self . Prepare  (                                                      )
    ##########################################################################
    self   . Go       ( self . loading                                       )
    self   . setFocus (                                                      )
    ##########################################################################
    return
  ############################################################################
  def Load                        ( self                                   ) :
    ##########################################################################
    Filters  = self . getMenuItem ( "TextFilters"                            )
    Name , t = QFileDialog . getOpenFileName                                 (
                                    self                                   , \
                                    self . windowTitle ( )                 , \
                                    ""                                     , \
                                    Filters                                  )
    ##########################################################################
    if                            ( len ( Name ) <= 0                      ) :
      self   . Notify             ( 1                                        )
      return
    ##########################################################################
    self     . setPlainText       ( ""                                       )
    ##########################################################################
    self     . Filename = Name
    ##########################################################################
    self     . Go                 ( self . LoadFromFilename ,  ( Name , )    )
    ##########################################################################
    return
  ############################################################################
  def Save              ( self                                             ) :
    ##########################################################################
    if                  ( len ( self . Filename ) > 0                      ) :
      self . SaveToFile (                                                    )
    ##########################################################################
    return
  ############################################################################
  def SaveAs                      ( self                                   ) :
    ##########################################################################
    Filters  = self . getMenuItem ( "TextFilters"                            )
    Name , t = QFileDialog . getSaveFileName                                 (
                                    self                                   , \
                                    self . windowTitle ( )                 , \
                                    ""                                     , \
                                    Filters                                  )
    ##########################################################################
    if                            ( len ( Name ) <= 0                      ) :
      self   . Notify             ( 1                                        )
      return
    ##########################################################################
    self     . Filename = Name
    ##########################################################################
    self     . Go                 ( self . SaveToFilename , ( Name , )       )
    ##########################################################################
    return
  ############################################################################
  def ReplaceSelection           ( self , text                             ) :
    ##########################################################################
    cursor   = self . textCursor (                                           )
    if                           ( cursor . hasSelection ( )               ) :
      cursor . insertText        ( text                                      )
    ##########################################################################
    return
  ############################################################################
  def LocalityMenu            ( self , mm                                  ) :
    ##########################################################################
    TRX   = self . Translations
    KIX   = "CommandInterface"
    LOC   = TRX               [ KIX ]             [ "Languages"              ]
    ##########################################################################
    msg   = TRX               [ KIX ] [ "Menus" ] [ "Language"               ]
    LOM   = mm . addMenu      ( msg                                          )
    ##########################################################################
    KEYs  = LOC . keys        (                                              )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      msg = LOC               [ K                                            ]
      V   = int               ( K                                            )
      hid =                   ( V == self . defaultLocality                  )
      mm  . addActionFromMenu ( LOM , 10000000 + V , msg , True , hid        )
    ##########################################################################
    return mm
  ############################################################################
  def RunLocalityMenu ( self , at                                          ) :
    ##########################################################################
    if                ( ( at >= 10000000 ) and ( at < 11000000 )           ) :
      ########################################################################
      self . defaultLocality  = at - 10000000
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def TextingMenu              ( self , mm                                 ) :
    ##########################################################################
    TRX = self . Translations
    LOM = mm   . addMenu       (              TRX [ "UI::Texting"          ] )
    ##########################################################################
    mm  . addActionFromMenu    ( LOM , 1001 , TRX [ "UI::Cut"              ] )
    mm  . addActionFromMenu    ( LOM , 1002 , TRX [ "UI::CopyToClipboard"  ] )
    mm  . addActionFromMenu    ( LOM , 1003 , TRX [ "UI::Paste"            ] )
    mm  . addSeparatorFromMenu ( LOM                                         )
    mm  . addActionFromMenu    ( LOM , 1011 , TRX [ "UI::Undo"             ] )
    mm  . addActionFromMenu    ( LOM , 1012 , TRX [ "UI::Redo"             ] )
    mm  . addSeparatorFromMenu ( LOM                                         )
    mm  . addActionFromMenu    ( LOM , 1021 , TRX [ "UI::ClearAll"         ] )
    mm  . addActionFromMenu    ( LOM , 1022 , TRX [ "UI::SelectAll"        ] )
    ##########################################################################
    return mm
  ############################################################################
  def RunTextingMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . cut                   (                                         )
      return True
    ##########################################################################
    if                             ( at == 1002                            ) :
      self . copy                  (                                         )
      return True
    ##########################################################################
    if                             ( at == 1003                            ) :
      self . paste                 (                                         )
      return True
    ##########################################################################
    if                             ( at == 1011                            ) :
      self . undo                  (                                         )
      return True
    ##########################################################################
    if                             ( at == 1012                            ) :
      self . redo                  (                                         )
      return True
    ##########################################################################
    if                             ( at == 1021                            ) :
      self . clear                 (                                         )
      return True
    ##########################################################################
    if                             ( at == 1022                            ) :
      self . selectAll             (                                         )
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                       ( self , pos                              ) :
    ##########################################################################
    doMenu = self . isFunction   ( self . HavingMenu                         )
    if                           ( not doMenu                              ) :
      return False
    ##########################################################################
    mm     = MenuManager         ( self                                      )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . TextingMenu  ( mm                                        )
    mm     . addSeparator        (                                           )
    ##########################################################################
    mm     = self . LocalityMenu ( mm                                        )
    self   . DockingMenu         ( mm                                        )
    ##########################################################################
    self   . Notify              ( 0                                         )
    mm     . setFont             ( self    . menuFont ( )                    )
    aa     = mm . exec_          ( QCursor . pos      ( )                    )
    at     = mm . at             ( aa                                        )
    ##########################################################################
    if                           ( self . RunDocking      ( mm , aa )      ) :
      return True
    ##########################################################################
    if                           ( self . RunLocalityMenu ( at      )      ) :
      return True
    ##########################################################################
    if                           ( self . RunTextingMenu  ( at      )      ) :
      return True
    ##########################################################################
    return True
##############################################################################
