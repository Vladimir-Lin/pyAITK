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
  emitSelection  = Signal ( str                                              )
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
    self . defaultFont     = self . font (                                   )
    self . Filename        = ""
    self . defaultLocality = 1002
    self . AtMenu          = False
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
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendSideActionWithIcon ( "ClearAll"                           , \
                                      ":/images/undecided.png"             , \
                                      self . clear                         , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "NamesFromClipboard"                 , \
                                      ":/images/copy.png"                  , \
                                      self . TakeNamesFromClipboard        , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "NamesExtractClipboard"              , \
                                      ":/images/standalone.png"            , \
                                      self . TakeNamesExtractClipboard     , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "FindAll"                            , \
                                      ":/images/zoom.png"                  , \
                                      self . FindAllByName                 , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "FindEmpty"                          , \
                                      ":/images/list.png"                  , \
                                      self . FindAllEmpty                  , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "FindAllByNames"                     , \
                                      ":/images/documentsearch.png"        , \
                                      self . FindAllByNames                , \
                                      True                                 , \
                                      False                                  )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                   Enabled           ) :
    ##########################################################################
    self . LinkAction ( "Load"      , self . Load      , Enabled             )
    self . LinkAction ( "Save"      , self . Save      , Enabled             )
    self . LinkAction ( "SaveAs"    , self . SaveAs    , Enabled             )
    self . LinkAction ( "Undo"      , self . undo      , Enabled             )
    self . LinkAction ( "Redo"      , self . redo      , Enabled             )
    self . LinkAction ( "Cut"       , self . cut       , Enabled             )
    self . LinkAction ( "Copy"      , self . copy      , Enabled             )
    self . LinkAction ( "Paste"     , self . paste     , Enabled             )
    self . LinkAction ( "SelectAll" , self . selectAll , Enabled             )
    self . LinkAction ( "ZoomIn"    , self . ZoomIn    , Enabled             )
    self . LinkAction ( "ZoomOut"   , self . ZoomOut   , Enabled             )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label" , self . windowTitle ( )              )
    self . AttachActions     ( True                                          )
    self . attachActionsTool (                                               )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                 ( self                                      ) :
    ##########################################################################
    if                         ( not self . isPrepared ( )                 ) :
      return True
    ##########################################################################
    if                         ( not self . AtMenu                         ) :
      ########################################################################
      self . AttachActions     ( False                                       )
      self . detachActionsTool (                                             )
    ##########################################################################
    return False
  ############################################################################
  def Shutdown               ( self                                        ) :
    ##########################################################################
    self . StayAlive   = False
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent     ( self , event                                        ) :
    ##########################################################################
    if               ( self . Shutdown (                                 ) ) :
      event . accept (                                                       )
    else                                                                     :
      event . ignore (                                                       )
    ##########################################################################
    return
  ############################################################################
  def keyPressEvent           ( self , e                                   ) :
    ##########################################################################
    if                        ( e . key ( ) == Qt . Key_Return             ) :
      ########################################################################
      self . CommandEnter     (                                              )
    ##########################################################################
    super ( ) . keyPressEvent (        e                                     )
    ##########################################################################
    return
  ############################################################################
  def doLog               ( self , message                                 ) :
    ##########################################################################
    self . emitLog . emit (        message                                   )
    ##########################################################################
    return
  ############################################################################
  def ZoomIn       ( self                                                  ) :
    ##########################################################################
    self . zoomIn  ( 1                                                       )
    ##########################################################################
    return
  ############################################################################
  def ZoomOut      ( self                                                  ) :
    ##########################################################################
    self . zoomOut ( 1                                                       )
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
    self   . defaultFont = self . font (                                     )
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
  def AssignFileName              ( self                                   ) :
    ##########################################################################
    TITLE    = self . getMenuItem ( "AssignTextFile"                         )
    FILTERs  = self . getMenuItem ( "TextFilters"                            )
    NAME , t = QFileDialog . getOpenFileName                                 (
                                    self                                   , \
                                    TITLE                                  , \
                                    ""                                     , \
                                    FILTERs                                  )
    ##########################################################################
    if                            ( len ( NAME ) <= 0                      ) :
      self   . Notify             ( 1                                        )
      return
    ##########################################################################
    CMD  = f"filename {NAME}"
    self . insertPlainText        ( CMD                                      )
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
  def CommandEnter                              ( self                     ) :
    ##########################################################################
    T = self . document   ( ) . blockCount      (                            )
    Y = self . textCursor ( ) . blockNumber     (                            )
    ##########################################################################
    D = int                                     ( T - Y                      )
    ##########################################################################
    if                                          ( 1 != D                   ) :
      return
    ##########################################################################
    ## X = self . textCursor ( ) . positionInBlock (                            )
    C = self . document   ( ) . findBlockByNumber ( Y ) . text (             )
    ##########################################################################
    if                                          ( len ( C ) <= 0           ) :
      return
    ##########################################################################
    M    = f":-> {C}"
    ##########################################################################
    self . emitLog     . emit                   ( M                          )
    self . emitCommand . emit                   ( C                          )
    ##########################################################################
    return
  ############################################################################
  def addCommand  ( self , cmd                                             ) :
    ##########################################################################
    self . append (        cmd                                               )
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
  def TakeNamesFromClipboard ( self                                        ) :
    ##########################################################################
    self . insertPlainText   ( "take names from clipboard"                   )
    ##########################################################################
    return
  ############################################################################
  def TakeNamesExtractClipboard ( self                                     ) :
    ##########################################################################
    self . insertPlainText      ( "take names extract clipboard"             )
    ##########################################################################
    return
  ############################################################################
  def FindAllByName        ( self                                          ) :
    ##########################################################################
    self . insertPlainText ( "find all"                                      )
    ##########################################################################
    return
  ############################################################################
  def FindAllEmpty         ( self                                          ) :
    ##########################################################################
    self . insertPlainText ( "find empty"                                    )
    ##########################################################################
    return
  ############################################################################
  def FindAllByNames       ( self                                          ) :
    ##########################################################################
    self . insertPlainText ( "find all by names"                             )
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
  def TextingMenu                   ( self , mm                            ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    LOM = mm   . addMenu            ( TRX [ "UI::Texting"                  ] )
    ##########################################################################
    mm  . addActionFromMenuWithIcon ( LOM                                  , \
                                      1001                                 , \
                                      QIcon ( ":/images/cut.png"         ) , \
                                      TRX   [ "UI::Cut"                  ]   )
    mm  . addActionFromMenuWithIcon ( LOM                                  , \
                                      1002                                 , \
                                      QIcon ( ":/images/copy.png"        ) , \
                                      TRX   [ "UI::CopyToClipboard"      ]   )
    mm  . addActionFromMenuWithIcon ( LOM                                  , \
                                      1003                                 , \
                                      QIcon ( ":/images/paste.png"       ) , \
                                      TRX   [ "UI::Paste"                ]   )
    ##########################################################################
    mm  . addSeparatorFromMenu      ( LOM                                    )
    ##########################################################################
    mm  . addActionFromMenu         ( LOM , 1011 , TRX [ "UI::Undo"        ] )
    mm  . addActionFromMenu         ( LOM , 1012 , TRX [ "UI::Redo"        ] )
    ##########################################################################
    mm  . addSeparatorFromMenu      ( LOM                                    )
    ##########################################################################
    ## mm  . addActionFromMenu         ( LOM , 1021 , TRX [ "UI::ClearAll"    ] )
    mm  . addActionFromMenu         ( LOM , 1022 , TRX [ "UI::SelectAll"   ] )
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
  def DisplayMenu                   ( self , mm                            ) :
    ##########################################################################
    TRX = self . Translations
    LOM = mm   . addMenu            (              TRX [ "UI::Display"     ] )
    ##########################################################################
    mm  . addActionFromMenuWithIcon ( LOM                                  , \
                                      1104                                 , \
                                      QIcon ( ":/images/zoomin.png"      ) , \
                                      TRX   [ "UI::ZoomIn"               ]   )
    mm  . addActionFromMenuWithIcon ( LOM                                  , \
                                      1105                                 , \
                                      QIcon ( ":/images/zoomout.png"     ) , \
                                      TRX   [ "UI::ZoomOut"              ]   )
    ##########################################################################
    return mm
  ############################################################################
  def RunDisplayMenu ( self , at                                           ) :
    ##########################################################################
    if               ( at == 1104                                          ) :
      self . ZoomIn  (                                                       )
      return True
    ##########################################################################
    if               ( at == 1105                                          ) :
      self . ZoomOut (                                                       )
      return True
    ##########################################################################
    return   False
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    mm     = MenuManager               ( self                                )
    ##########################################################################
    TRX    = self . Translations
    TEXT   = qApp . clipboard          ( ) . text (                          )
    ##########################################################################
    if                                 ( len ( TEXT ) > 0                  ) :
      ########################################################################
      MSG  = TRX                       [ "CMD::SelectionToCommand"           ]
      mm   . addAction                 ( 4001 , MSG                          )
    ##########################################################################
    MSG    = self . getMenuItem        ( "DefaultFont"                       )
    mm     . addAction                 ( 4002 , MSG                          )
    ##########################################################################
    MSG    = self . getMenuItem        ( "ClearAll"                          )
    ICN    = QIcon                     ( ":/images/undecided.png"            )
    mm     . addActionWithIcon         ( 4003 , ICN , MSG                    )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    MSG    = self . getMenuItem        ( "NamesFromClipboard"                )
    ICN    = QIcon                     ( ":/images/copy.png"                 )
    mm     . addActionWithIcon         ( 4101 , ICN , MSG                    )
    ##########################################################################
    MSG    = self . getMenuItem        ( "NamesExtractClipboard"             )
    ICN    = QIcon                     ( ":/images/standalone.png"           )
    mm     . addActionWithIcon         ( 4102 , ICN , MSG                    )
    ##########################################################################
    MSG    = self . getMenuItem        ( "FindAll"                           )
    ICN    = QIcon                     ( ":/images/zoom.png"                 )
    mm     . addActionWithIcon         ( 4103 , ICN , MSG                    )
    ##########################################################################
    MSG    = self . getMenuItem        ( "FindEmpty"                         )
    ICN    = QIcon                     ( ":/images/list.png"                 )
    mm     . addActionWithIcon         ( 4104 , ICN , MSG                    )
    ##########################################################################
    MSG    = self . getMenuItem        ( "FindAllByNames"                    )
    ICN    = QIcon                     ( ":/images/documentsearch.png"       )
    mm     . addActionWithIcon         ( 4105 , ICN , MSG                    )
    ##########################################################################
    MSG    = self . getMenuItem        ( "AssignTextFile"                    )
    mm     . addAction                 ( 4106 , MSG                          )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    mm     = self . TextingMenu        ( mm                                  )
    mm     = self . DisplayMenu        ( mm                                  )
    mm     . addSeparator              (                                     )
    ##########################################################################
    mm     = self . LocalityMenu       ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    if                                 ( self . RunDocking ( mm , aa )     ) :
      return True
    ##########################################################################
    if                                 ( self . RunLocalityMenu ( at     ) ) :
      return True
    ##########################################################################
    if                                 ( self . RunTextingMenu  ( at     ) ) :
      return True
    ##########################################################################
    if                                 ( self . RunDisplayMenu  ( at     ) ) :
      return True
    ##########################################################################
    if                                 ( 4001 == at                        ) :
      ########################################################################
      self . emitSelection . emit      ( TEXT                                )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 4002 == at                        ) :
      ########################################################################
      self . setFont                   ( self . defaultFont                  )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 4003 == at                        ) :
      ########################################################################
      self . clear                     (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 4101 == at                        ) :
      ########################################################################
      self . TakeNamesFromClipboard    (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 4102 == at                        ) :
      ########################################################################
      self . TakeNamesExtractClipboard (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 4103 == at                        ) :
      ########################################################################
      self . FindAllByName             (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 4104 == at                        ) :
      ########################################################################
      self . FindAllEmpty              (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 4105 == at                        ) :
      ########################################################################
      self . FindAllByNames            (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 4106 == at                        ) :
      self . AssignFileName            (                                     )
      return True
    ##########################################################################
    return True
##############################################################################
