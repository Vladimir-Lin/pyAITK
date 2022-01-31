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
from   PyQt5 . QtWidgets                 import QFileDialog
##############################################################################
from   AITK  . Qt        . MenuManager   import MenuManager   as MenuManager
from   AITK  . Qt        . LineEdit      import LineEdit      as LineEdit
from   AITK  . Qt        . ComboBox      import ComboBox      as ComboBox
from   AITK  . Qt        . SpinBox       import SpinBox       as SpinBox
from   AITK  . Qt        . TextEdit      import TextEdit      as TextEdit
##############################################################################
from   AITK  . Essentials . Relation     import Relation
from   AITK  . Calendars  . StarDate     import StarDate
from   AITK  . Calendars  . Periode      import Periode
from   AITK  . Documents  . Notes        import Notes
##############################################################################
class SmartNote                     ( TextEdit                             ) :
  ############################################################################
  HavingMenu  = 1371434312
  ############################################################################
  emitAddText     = pyqtSignal      ( str                                    )
  emitWindowIcon  = pyqtSignal      ( bool                                   )
  emitInsertText  = pyqtSignal      ( str                                    )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            ( parent , plan                          )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea                   | \
                                Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                                
    ##########################################################################
    self . setFunction              ( self . FunctionDocking , True          )
    self . setFunction              ( self . HavingMenu      , True          )
    ##########################################################################
    self . TZ           = "Asia/Taipei"
    self . VoiceJSON    =           {                                        }
    ##########################################################################
    self . Method       = "None"
    self . Uuid         = 0
    self . Key          = ""
    self . Prefer       = -1
    self . Filename     = ""
    self . Relation     = Relation  (                                        )
    self . defaultLocality  = 1002
    ##########################################################################
    self . emitInsertText . connect ( self . insertPlainText                 )
    ##########################################################################
    self . setPrepared              ( True                                   )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                 ( self                                      ) :
    return QSize               ( 800 , 600                                   )
  ############################################################################
  def WithinCommand     ( self , language , key , message                  ) :
    ##########################################################################
    if                  ( language not in self . VoiceJSON                 ) :
      return False
    ##########################################################################
    if                  ( key      not in self . VoiceJSON [ language ]    ) :
      return False
    ##########################################################################
    if                  ( message in self . VoiceJSON [ language ] [ key ] ) :
      return True
    ##########################################################################
    return   False
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"   , self . windowTitle ( )              )
    ##########################################################################
    self . LinkAction      ( "Load"      , self . Load                       )
    self . LinkAction      ( "Save"      , self . Save                       )
    self . LinkAction      ( "SaveAs"    , self . SaveAs                     )
    self . LinkAction      ( "Undo"      , self . undo                       )
    self . LinkAction      ( "Redo"      , self . redo                       )
    self . LinkAction      ( "Cut"       , self . cut                        )
    self . LinkAction      ( "Copy"      , self . copy                       )
    self . LinkAction      ( "Paste"     , self . paste                      )
    self . LinkAction      ( "SelectAll" , self . selectAll                  )
    self . LinkAction      ( "ZoomIn"    , self . ZoomIn                     )
    self . LinkAction      ( "ZoomOut"   , self . ZoomOut                    )
    ##########################################################################
    self . LinkVoice       ( self . CommandParser                            )
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
    self . LinkAction      ( "ZoomIn"    , self . ZoomIn    , False          )
    self . LinkAction      ( "ZoomOut"   , self . ZoomOut   , False          )
    ##########################################################################
    self . LinkVoice       ( None                                            )
    ##########################################################################
    super ( ) . closeEvent ( event                                           )
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
  def LoadFromNotes                ( self                                  ) :
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    NOXTAB = self . Tables         [ "Notes"                                 ]
    NOX    = Notes                 (                                         )
    NOX    . Uuid = self . Uuid
    NOX    . Name = self . Key
    NOX    . Obtains               ( DB , NOXTAB , self . Prefer             )
    BODY   = NOX . Note
    ##########################################################################
    DB     . Close                 (                                         )
    ##########################################################################
    self   . emitInsertText . emit ( BODY                                    )
    self   . Notify                ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def SaveToNotes                        ( self                            ) :
    ##########################################################################
    DB     = self . ConnectDB            (                                   )
    if                                   ( DB == None                      ) :
      return
    ##########################################################################
    NOXTAB = self . Tables               [ "Notes"                           ]
    NOX    = Notes                       (                                   )
    NOX    . Uuid   = self . Uuid
    NOX    . Name   = self . Key
    NOX    . Prefer = self . Prefer
    NOX    . Note   = self . toPlainText (                                   )
    ##########################################################################
    DB     . LockWrites                  ( [ NOXTAB                        ] )
    NOX    . Editing                     ( DB , NOXTAB                       )
    DB     . UnlockTables                (                                   )
    ##########################################################################
    DB     . Close                       (                                   )
    ##########################################################################
    self   . Notify                      ( 5                                 )
    ##########################################################################
    return
  ############################################################################
  def loading              ( self                                          ) :
    ##########################################################################
    if                     ( self . Method in [ "Note" ]                   ) :
      self . LoadFromNotes (                                                 )
      return
    ##########################################################################
    if                     ( self . Method in [ "File" ]                   ) :
      self . LoadFromFile  (                                                 )
      return
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    if                           ( self . Method not in [ "None" ]         ) :
      self . Go                  ( self . loading                            )
    ##########################################################################
    self   . setFocus            (                                           )
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
    if                            ( self . Method in [ "None" , "File" ]   ) :
      self   . Filename = Name
      self   . startup            (                                          )
      return
    ##########################################################################
    self     . Go                 ( self . LoadFromFilename ,  ( Name , )    )
    ##########################################################################
    return
  ############################################################################
  def Save          ( self                                                 ) :
    ##########################################################################
    if              ( self . Method in [ "None" ]                          ) :
      self . SaveAs (                                                        )
      return
    ##########################################################################
    if              ( self . Method in [ "File" ]                          ) :
      self . Go     ( self . SaveToFile                                      )
      return
    ##########################################################################
    if              ( self . Method in [ "Note" ]                          ) :
      self . Go     ( self . SaveToNotes                                     )
      return
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
    if                            ( self . Method in [ "None" ]            ) :
      ########################################################################
      self   . Filename = Name
      self   . Method   = "File"
      self   . Go                 ( self . SaveToFile                        )
      ########################################################################
      return
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
  def CommandParser           ( self , language , message , timestamp      ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      self . selectAll        (                                              )
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    if                        ( len ( message ) > 0                        ) :
      self . emitInsertText . emit ( message                                 )
    ##########################################################################
    return          { "Match" : True                                         }
  ############################################################################
  def TranslationsMenu             ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations   [ "Translations"                          ]
    msg    = self . Translations   [ "UI::Translations"                      ]
    KEYs   = TRX  . keys           (                                         )
    ##########################################################################
    LOT    = mm . addMenu          ( msg                                     )
    ##########################################################################
    for K in KEYs                                                            :
       msg = TRX                   [ K                                       ]
       V   = int                   ( K                                       )
       mm  . addActionFromMenu     ( LOT , V , msg                           )
    ##########################################################################
    return mm
  ############################################################################
  def LocalityMenu                 ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    LOC    = TRX                   [ "SmartNote" ] [ "Languages"             ]
    ##########################################################################
    msg    = TRX                   [ "SmartNote" ] [ "Menus" ] [ "Language"  ]
    LOM    = mm . addMenu          ( msg                                     )
    ##########################################################################
    KEYs   = LOC . keys            (                                         )
    ##########################################################################
    for K in KEYs                                                            :
       msg = LOC                   [ K                                       ]
       V   = int                   ( K                                       )
       hid =                       ( V == self . defaultLocality             )
       mm  . addActionFromMenu     ( LOM , 10000000 + V , msg , True , hid   )
    ##########################################################################
    return mm
  ############################################################################
  def RunLocalityMenu           ( self , at                                ) :
    ##########################################################################
    if                          ( ( at >= 10000000 ) and ( at < 11000000 ) ) :
      ########################################################################
      self . defaultLocality  = at - 10000000
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def TranslateMenu                ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    LOC    = self . Translations   [ "SmartNote" ] [ "Languages"             ]
    ##########################################################################
    msg    = TRX                   [ "UI::Translate"                         ]
    LOM    = mm . addMenu          ( msg                                     )
    ##########################################################################
    KEYs   = LOC . keys            (                                         )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      V    = int                   ( K                                       )
      if                           ( V in [ 0 , 1004 , 1005 ]              ) :
        continue
      msg  = LOC                   [ K                                       ]
      mm   . addActionFromMenu     ( LOM , 11000000 + V , msg                )
    ##########################################################################
    return mm
  ############################################################################
  def RunTranslate                     ( self , menu , action              ) :
    ##########################################################################
    stext  = self . textCursor ( ) . selectedText (                          )
    ##########################################################################
    if                                 ( len ( stext ) <= 0                ) :
      return False
    ##########################################################################
    at     = menu . at                 (               action                )
    ##########################################################################
    if                                 ( at < 11000000                     ) :
      return False
    ##########################################################################
    if                                 ( at > 11100000                     ) :
      return False
    ##########################################################################
    LID    = at   - 11000000
    DID    = self . defaultLocality
    SRC    = self . LocalityToGoogleLC ( DID                                 )
    DEST   = self . LocalityToGoogleLC ( LID                                 )
    ##########################################################################
    if                                 ( len ( SRC ) <= 0                  ) :
      return True
    ##########################################################################
    if                                 ( len ( DEST ) <= 0                 ) :
      return True
    ##########################################################################
    gt     = Translator     ( service_urls = [ "translate.googleapis.com" ]  )
    ##########################################################################
    try                                                                      :
      target = gt . translate ( stext , src = SRC , dest = DEST ) . text
    except                                                                   :
      return True
    ##########################################################################
    self   . ReplaceSelection          ( target                              )
    ##########################################################################
    return False
  ############################################################################
  def HandleTranslations      ( self , stext , ID                          ) :
    ##########################################################################
    if                        ( ( ID < 7001 ) or ( ID > 7008 )             ) :
      return False
    ##########################################################################
    CODE   = ""
    if                        ( ID == 7001                                 ) :
      CODE = "t2s"
    elif                      ( ID == 7002                                 ) :
      CODE = "s2t"
    elif                      ( ID == 7003                                 ) :
      CODE = "tw2s"
    elif                      ( ID == 7004                                 ) :
      CODE = "s2tw"
    elif                      ( ID == 7005                                 ) :
      CODE = "tw2sp"
    elif                      ( ID == 7006                                 ) :
      CODE = "s2twp"
    elif                      ( ID == 7007                                 ) :
      CODE = "hk2s"
    elif                      ( ID == 7008                                 ) :
      CODE = "s2hk"
    ##########################################################################
    cc     = OpenCC           ( CODE                                         )
    target = cc . convert     ( stext                                        )
    ##########################################################################
    self   . ReplaceSelection ( target                                       )
    ##########################################################################
    return True
  ############################################################################
  def TextingMenu               ( self , mm                                ) :
    ##########################################################################
    TRX = self . Translations
    LOM = mm   . addMenu        (              TRX [ "UI::Texting"         ] )
    ##########################################################################
    mm  . addActionFromMenu     ( LOM , 1001 , TRX [ "UI::Cut"             ] )
    mm  . addActionFromMenu     ( LOM , 1002 , TRX [ "UI::CopyToClipboard" ] )
    mm  . addActionFromMenu     ( LOM , 1003 , TRX [ "UI::Paste"           ] )
    mm  . addSeparatorFromMenu  ( LOM                                        )
    mm  . addActionFromMenu     ( LOM , 1011 , TRX [ "UI::Undo"            ] )
    mm  . addActionFromMenu     ( LOM , 1012 , TRX [ "UI::Redo"            ] )
    mm  . addSeparatorFromMenu  ( LOM                                        )
    mm  . addActionFromMenu     ( LOM , 1021 , TRX [ "UI::ClearAll"        ] )
    mm  . addActionFromMenu     ( LOM , 1022 , TRX [ "UI::SelectAll"       ] )
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
  def DisplayMenu               ( self , mm                                ) :
    ##########################################################################
    TRX = self . Translations
    LOM = mm   . addMenu        (              TRX [ "UI::Display"         ] )
    ##########################################################################
    mm  . addActionFromMenu     ( LOM , 1104 , TRX [ "UI::ZoomIn"          ] )
    mm  . addActionFromMenu     ( LOM , 1105 , TRX [ "UI::ZoomOut"         ] )
    ##########################################################################
    return mm
  ############################################################################
  def RunDisplayMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at == 1104                            ) :
      self . ZoomIn                (                                         )
      return True
    ##########################################################################
    if                             ( at == 1105                            ) :
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
    stext  = self . textCursor ( ) . selectedText (                          )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . TextingMenu    ( mm                                      )
    mm     = self . DisplayMenu    ( mm                                      )
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( len ( stext ) > 0                     ) :
      ########################################################################
      if                           ( self . canSpeak ( )                   ) :
        mm . addAction             ( 1501 ,  TRX [ "UI::Talk"  ]             )
        mm . addSeparator          (                                         )
      ########################################################################
      mm   = self . TranslateMenu    ( mm                                    )
      mm   = self . TranslationsMenu ( mm                                    )
    ##########################################################################
    mm     = self . LocalityMenu   ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    self   . Notify                ( 0                                       )
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking      ( mm , aa )    ) :
      return True
    ##########################################################################
    if                             ( self . RunLocalityMenu ( at      )    ) :
      return True
    ##########################################################################
    if                             ( self . RunTextingMenu  ( at      )    ) :
      return True
    ##########################################################################
    if                             ( self . RunDisplayMenu  ( at      )    ) :
      return True
    ##########################################################################
    if                             ( self . RunTranslate ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( len ( stext ) > 0                     ) :
      if ( self . HandleTranslations ( stext , at )                        ) :
        return True
    ##########################################################################
    if                             ( at == 1501                            ) :
      ########################################################################
      self . Talk                  ( stext , self . defaultLocality          )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
