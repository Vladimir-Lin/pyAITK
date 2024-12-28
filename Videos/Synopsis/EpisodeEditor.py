# -*- coding: utf-8 -*-
##############################################################################
## EpisodeEditor
## 影集編輯
##############################################################################
import os
import sys
import time
import datetime
import requests
import threading
import json
import vlc
import math
import cv2
##############################################################################
import pathlib
from   pathlib                                    import Path
##############################################################################
import AITK
##############################################################################
from   AITK    . Calendars . StarDate                    import StarDate            as StarDate
from   AITK    . Documents . JSON                        import Load                as LoadJson
from   AITK    . Documents . JSON                        import Save                as SaveJson
##############################################################################
from   PySide6                                           import QtCore
from   PySide6                                           import QtGui
from   PySide6                                           import QtWidgets
from   PySide6 . QtCore                                  import *
from   PySide6 . QtGui                                   import *
from   PySide6 . QtWidgets                               import *
from   AITK    . Qt6                                     import *
##############################################################################
from   AITK    . Qt6     . MenuManager                   import MenuManager         as MenuManager
from   AITK    . Qt6     . AttachDock                    import AttachDock          as AttachDock
from   AITK    . Qt6     . Widget                        import Widget              as Widget
##############################################################################
from   AITK    . Widgets . Commons6 . NamesEditor        import NamesEditor
from   AITK    . People  . Widgets6 . PeopleView         import PeopleView
from   AITK    . Finance . Widgets6 . IdentifierListings import IdentifierListings
from   AITK    . Videos  . Utilities                     import SilentRun           as SilentRun
##############################################################################
from                     . Episode                       import Episode             as Episode
##############################################################################
from                     . UiEpisodeEstablish            import Ui_EpisodeEstablish as Ui_EpisodeEstablish
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
class EpisodeEditor       ( ScrollArea                                     ) :
  ############################################################################
  emitEstablish = Signal  (                                                  )
  emitEditing   = Signal  (                                                  )
  emitLog       = Signal  ( str                                              )
  Leave         = Signal  ( QWidget                                          )
  ############################################################################
  def           __init__  ( self , parent = None , plan = None             ) :
    ##########################################################################
    super ( ) . __init__  (        parent        , plan                      )
    self      . Configure (                                                  )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 640 , 480 )                       )
  ############################################################################
  def Configure                      ( self                                ) :
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self          . setMinimumHeight ( 60                                    )
    self          . setHorizontalScrollBarPolicy ( Qt . ScrollBarAlwaysOff   )
    ##########################################################################
    self . ALBUM  = Episode          (                                       )
    self . ALBUM  . LogFunc = self . addLog
    self . Method = "Nothing"
    ##########################################################################
    self . CLI             = None
    self . EstablishWidget = None
    self . EditingWidget   = None
    ##########################################################################
    self . emitEstablish   . connect ( self . DoEstablish                    )
    self . emitEditing     . connect ( self . DoEditing                      )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    if                      ( self . Relocation ( )                        ) :
      event . accept        (                                                )
      return
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
    ##########################################################################
    return
  ############################################################################
  def showEvent           ( self , event                                   ) :
    ##########################################################################
    super ( ) . showEvent ( event                                            )
    self . Relocation     (                                                  )
    ##########################################################################
    return
  ############################################################################
  def addLog              ( self , MSG                                     ) :
    ##########################################################################
    self . emitLog . emit (        MSG                                       )
    ##########################################################################
    return
  ############################################################################
  def logMessage             ( self , KEY                                  ) :
    ##########################################################################
    MSG = self . getMenuItem ( KEY                                           )
    ##########################################################################
    if                       ( len ( MSG ) <= 0                            ) :
      return
    ##########################################################################
    return self . addLog     ( MSG                                           )
  ############################################################################
  def AssignCLI ( self , CLI                                               ) :
    ##########################################################################
    self . CLI = CLI
    ##########################################################################
    return
  ############################################################################
  def LoadDocument           ( self , Filename                             ) :
    ##########################################################################
    if                       ( not os . path . isfile ( Filename )         ) :
      return ""
    ##########################################################################
    TEXT   = ""
    with open                ( Filename , "rb" ) as jsonFile                 :
      TEXT = jsonFile . read (                                               )
    ##########################################################################
    if                       ( len ( TEXT ) <= 0                           ) :
      return ""
    ##########################################################################
    return TEXT . decode     ( "utf-8"                                       )
  ############################################################################
  def SaveDocument   ( self , Filename , BODY                              ) :
    ##########################################################################
    try                                                                      :
      with open      ( Filename , 'w' , encoding = "utf-8" ) as File         :
        File . write (                   BODY                                )
    except                                                                   :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def SaveAlbumJson           ( self                                       ) :
    ##########################################################################
    self . ALBUM . SaveToFile (                                              )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  def DoEstablish ( self                                                   ) :
    ##########################################################################
    ## self . EstablishWidget      = QWidget ( self . cwidget                   )
    self . EstablishWidget      = QWidget (                                  )
    self . EstablishWidget . ui = Ui_EpisodeEstablish (                      )
    self . EstablishWidget . ui . setupUi ( self . EstablishWidget           )
    self . EstablishWidget . ui . Scanning . hide (                          )
    self . EstablishWidget . ui . Start . clicked . connect ( self . DoEstablishAlbum )
    self . EstablishWidget . ui . Close . clicked . connect ( self . CloseThis        )
    ##########################################################################
    ## self . vlayout         . addWidget    ( self . EstablishWidget           )
    self . setWidget ( self . EstablishWidget                                )
    self . setWidgetResizable ( True )
    ## self . EstablishWidget . move         ( 0 , 0                            )
    ## self . EstablishWidget . show         (                                  )
    ##########################################################################
    self . Method    = "Establish"
    ##########################################################################
    return
  ############################################################################
  def EstablishAlbum            ( self                                     ) :
    ##########################################################################
    HNAME  = self . DB          [ "hostname"                                 ]
    CDMSG  = self . getMenuItem ( "ConnectDB"                                )
    MSG    = f"{CDMSG}{HNAME}"
    self   . addLog             ( MSG                                        )
    ##########################################################################
    self . ALBUM . Settings     = self . Settings
    self . ALBUM . Translations = self . Translations
    self . ALBUM . Messages     = self . Translations [ "Episode"            ]
    self . ALBUM . Tables       = self . Tables
    ##########################################################################
    self   . LoopRunning = False
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      self . LoopRunning = True
      return
    ##########################################################################
    self   . ALBUM . Establish  ( DB                                         )
    ##########################################################################
    DB     . Close              (                                            )
    ##########################################################################
    self   . LoopRunning = True
    ##########################################################################
    self   . Notify             ( 5                                          )
    self   . emitEditing . emit (                                            )
    ##########################################################################
    return
  ############################################################################
  def DoEstablishAlbum ( self                                              ) :
    ##########################################################################
    self . EstablishWidget . ui . Start    . hide (                          )
    self . EstablishWidget . ui . Close    . hide (                          )
    self . EstablishWidget . ui . NotReady . hide (                          )
    self . EstablishWidget . ui . Scanning . show (                          )
    ##########################################################################
    self . Go          ( self . EstablishAlbum                               )
    ##########################################################################
    return
  ############################################################################
  def addEditingTools                         ( self                       ) :
    ##########################################################################
    self . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 80
    ##########################################################################
    self . EditingWidget . ToolBar = QToolBar (                              )
    ##########################################################################
    self . EditingWidget . ToolBar . setMinimumHeight ( 72                   )
    self . EditingWidget . ToolBar . setMaximumHeight ( 72                   )
    self . EditingWidget . ToolBar . setIconSize      ( QSize ( 48 , 48    ) )
    self . EditingWidget . ToolBar . setFloatable     ( False                )
    self . EditingWidget . ToolBar . setMovable       ( False                )
    self . EditingWidget . ToolBar . setToolButtonStyle ( Qt . ToolButtonTextUnderIcon )
    ##########################################################################
    FNT  = self . font                        (                              )
    FNT  . setPixelSize                       ( 8                            )
    self . EditingWidget . ToolBar . setFont  ( FNT                          )
    ##########################################################################
    MSG  = self . getMenuItem                 ( "MainMenu"                   )
    ICON = QIcon ( QPixmap ( ":/images/Menu.png"                           ) )
    MACT = self . EditingWidget . ToolBar . addAction ( ICON , MSG           )
    ##########################################################################
    MSG  = self . getMenuItem                 ( "SaveJson"                   )
    ICON = QIcon ( QPixmap ( ":/images/save.png"                           ) )
    MACT = self . EditingWidget . ToolBar . addAction ( ICON , MSG           )
    MACT . triggered . connect ( self . SaveAlbumJson                        )
    ##########################################################################
    MSG  = self . getMenuItem                 ( "SyncDatabase"               )
    ICON = QIcon ( QPixmap ( ":/images/importdatabase.png"                 ) )
    MACT = self . EditingWidget . ToolBar . addAction ( ICON , MSG           )
    ## MACT . triggered . connect ( self . SaveAlbumJson                        )
    ##########################################################################
    MSG  = self . getMenuItem                 ( "DockMenu"                   )
    ICON = QIcon ( QPixmap ( ":/images/hidespeech.png"                     ) )
    MACT = self . EditingWidget . ToolBar . addAction ( ICON , MSG           )
    MACT . triggered . connect ( self . DoDockMenu                           )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    self . EditingWidget . addWidget ( self . EditingWidget . ToolBar        )
    ##########################################################################
    return
  ############################################################################
  def AlbumTitleChanged ( self                                             ) :
    ##########################################################################
    TITLE = self . EditingWidget . TitleEditor . text ( )
    self  . ALBUM . Album [ "Names" ] [ "Default" ] = TITLE
    ##########################################################################
    return
  ############################################################################
  def addAlbumTitle ( self                                                 ) :
    ##########################################################################
    self  . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 32
    ##########################################################################
    TITLE = self . ALBUM . Album [ "Names" ] [ "Default"                     ]
    ##########################################################################
    self  . EditingWidget . TitleEditor = QLineEdit      (                   )
    self  . EditingWidget . TitleEditor . setGeometry    ( 0 , 0 , 400 , 28  )
    self  . EditingWidget . TitleEditor . setMinimumSize ( 400 , 28          )
    self  . EditingWidget . TitleEditor . setText        ( TITLE             )
    self  . EditingWidget . TitleEditor . editingFinished . connect ( self . AlbumTitleChanged )
    ##########################################################################
    self  . EditingWidget . addWidget ( self . EditingWidget . TitleEditor   )
    ##########################################################################
    return
  ############################################################################
  def addAlbumCoverSection ( self                                          ) :
    ##########################################################################
    self . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 400
    ##########################################################################
    TCW  = 640
    TCH  = 360
    self . EditingWidget . Cover = QToolButton (                             )
    self . EditingWidget . Cover . setGeometry ( QRect ( 0 , 0 , TCW , TCH ) )
    self . EditingWidget . Cover . setMinimumSize ( 128 , 128                )
    ##########################################################################
    self . EditingWidget . addWidget ( self . EditingWidget . Cover          )
    ##########################################################################
    if                              ( not self . ALBUM . isCover (       ) ) :
      return
    ##########################################################################
    CF  = self . ALBUM . CoverFile (                                         )
    CIM = QImage                  ( CF                                       )
    ##########################################################################
    if                            ( CIM . width  ( ) > TCW                 ) :
      ########################################################################
      TTH = int ( int ( TCW * CIM . height ( ) ) / CIM . width (           ) )
      CIM = CIM . scaled          ( TCW , TTH , Qt . KeepAspectRatio         )
    ##########################################################################
    if                            ( CIM . height ( ) > TCH                 ) :
      ########################################################################
      TTW = int ( int ( TCH * CIM . width ( ) ) / CIM . height (           ) )
      CIM = CIM . scaled          ( TTW , TCH , Qt . KeepAspectRatio         )
    ##########################################################################
    if                            ( CIM . width  ( ) > TCW                 ) :
      ########################################################################
      TTH = int ( int ( TCW * CIM . height ( ) ) / CIM . width (           ) )
      CIM = CIM . scaled          ( TCW , TTH , Qt . KeepAspectRatio         )
    ##########################################################################
    PIX   = QPixmap               (                                          )
    ##########################################################################
    if                            ( PIX . convertFromImage( CIM          ) ) :
      ########################################################################
      ICN = QIcon                 ( PIX                                      )
      self  . EditingWidget . Cover . setIconSize ( CIM . size (           ) )
      self  . EditingWidget . Cover . setIcon     ( ICN                      )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def addNamesEditor ( self                                                ) :
    ##########################################################################
    self . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 360
    ##########################################################################
    TNE   = NamesEditor             ( None , self . PlanFunc                 )
    TNE   . setMinimumHeight        ( 120                                    )
    TNE   . resize                  ( 400 , 320                              )
    ##########################################################################
    TNE   . DB           = self . DB
    TNE   . Settings     = self . Settings
    TNE   . Translations = self . Translations
    TNE   . Tables [ "Names" ] = self . Tables [ "VideoAlbums" ] [ "Subordination" ] [ "NamesEditing" ]
    ##########################################################################
    TNE   . set                     ( "uuid" , self . ALBUM . Uuid           )
    TNE   . PrepareMessages         (                                        )
    ##########################################################################
    if                              ( "Font" in self . Settings            ) :
      fnt = QFont                   (                                        )
      fnt . fromString              ( self . Settings [ "Font" ]             )
      TNE . setFont                 ( fnt                                    )
    ##########################################################################
    self . EditingWidget . NamesEditor = TNE
    ##########################################################################
    self . EditingWidget . addWidget ( self . EditingWidget . NamesEditor    )
    ##########################################################################
    TNE   . startup                 (                                        )
    ##########################################################################
    return
  ############################################################################
  def addAlbumIdentifiers              ( self                              ) :
    ##########################################################################
    self   . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 240
    ##########################################################################
    DKEY   = "IdentifierListings"
    IDFW   = IdentifierListings        ( None , self . PlanFunc              )
    IDFW   . setMinimumHeight          ( 120                                 )
    IDFW   . resize                    ( 400 , 240                           )
    ##########################################################################
    IDFW   . setUuidMethod             ( self . ALBUM . Uuid , 76            )
    IDFW   . Hosts        = { "Database" : self . Settings [ "Database" ]  , \
                              "Oriphase" : self . Settings [ "Oriphase" ]    }
    IDFW   . DB           = self . DB
    IDFW   . Settings     = self . Settings
    IDFW   . Translations = self . Translations
    IDFW   . Tables       = self . Tables [ DKEY                             ]
    ##########################################################################
    LANGZ  = self . Translations       [ DKEY ] [ "Languages"                ]
    MENUZ  = self . Translations       [ DKEY ] [ "Menus"                    ]
    ##########################################################################
    IDFW   . PrepareMessages           (                                     )
    ##########################################################################
    IDFW   . setLocality               ( self . getLocality ( )              )
    IDFW   . setLanguages              ( LANGZ                               )
    IDFW   . setMenus                  ( MENUZ                               )
    ##########################################################################
    if                                 ( "Font" in self . Settings         ) :
      fnt  = QFont                     (                                     )
      fnt  . fromString                ( self . Settings [ "Font" ]          )
      IDFW . setFont                   ( fnt                                 )
    ##########################################################################
    self   . EditingWidget . Identifiers = IDFW
    ##########################################################################
    self   . EditingWidget . addWidget ( self . EditingWidget . Identifiers  )
    ##########################################################################
    IDFW   . startup                   (                                     )
    ##########################################################################
    return
  ############################################################################
  def addPeopleView           ( self                                       ) :
    ##########################################################################
    self . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 320
    ##########################################################################
    PEOW  = PeopleView        ( None , self . PlanFunc                       )
    ##########################################################################
    PEOW  . setMinimumHeight  ( 160                                          )
    PEOW  . resize            ( 400 , 320                                    )
    ##########################################################################
    KEY   = "PeopleView"
    PEOW  . DB           = self . DB
    PEOW  . Hosts        = { "Database" : self . Settings [ "Database" ]   , \
                             "Oriphase" : self . Settings [ "Oriphase" ]     }
    PEOW  . Settings     = self . Settings
    PEOW  . Translations = self . Translations
    PEOW  . Tables       = self . Tables [ KEY                     ]
    PEOW  . Relation . set    ( "second" , int ( self . ALBUM . Uuid )       )
    PEOW  . Relation . set    ( "t2"     , 76                                )
    PEOW  . setGrouping       ( "Reverse"                                    )
    ##########################################################################
    LANGZ = self . Translations [ KEY ] [ "Languages"                        ]
    MENUZ = self . Translations [ KEY ] [ "Menus"                            ]
    ##########################################################################
    PEOW  . PrepareMessages   (                                              )
    PEOW  . setLocality       ( self . getLocality ( )                       )
    PEOW  . setLanguages      ( LANGZ                                        )
    PEOW  . setMenus          ( MENUZ                                        )
    ##########################################################################
    ## PEOW . ShowGalleries         . connect ( self . ShowGalleries            )
    ## PEOW . ShowGalleriesRelation . connect ( self . ShowGalleriesRelation    )
    ## PEOW . ShowPersonalGallery   . connect ( self . ShowPersonalGallery      )
    ## PEOW . ShowPersonalIcons     . connect ( self . ShowPersonalIcons        )
    ## PEOW . ShowPersonalFaces     . connect ( self . ShowFaceViewByPeople     )
    ## PEOW . ShowVideoAlbums       . connect ( self . ShowVideoAlbums          )
    ## PEOW . ShowWebPages          . connect ( self . ShowWebPages             )
    ## PEOW . OwnedOccupation       . connect ( self . OwnedOccupationSubgroups )
    ## PEOW . OpenVariantTables     . connect ( self . OpenVariantTables        )
    ## PEOW . ShowLodListings       . connect ( self . ShowLodListings          )
    ## PEOW . OpenLogHistory        . connect ( self . OpenLogHistory           )
    ## PEOW . OpenBodyShape         . connect ( self . OpenBodyShape            )
    ## PEOW . emitOpenSmartNote     . connect ( self . assignSmartNote          )
    PEOW  . emitLog              . connect ( self . MAIN . appendLog         )
    ##########################################################################
    self  . setAllFont        ( PEOW , self . font (                       ) )
    PEOW  . PrepareForActions (                                              )
    ##########################################################################
    self . EditingWidget . PeopleView = PEOW
    ##########################################################################
    self . EditingWidget . addWidget ( self . EditingWidget . PeopleView     )
    ##########################################################################
    return
  ############################################################################
  def addSketch                      ( self                                ) :
    ##########################################################################
    self . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 660
    ##########################################################################
    MSG  = self . getMenuItem        ( "SketchArena"                         )
    TEXT = QPlainTextEdit            (                                       )
    TEXT . setMinimumHeight          ( 200                                   )
    TEXT . resize                    ( 400 , 640                             )
    TEXT . setToolTip                ( MSG                                   )
    ##########################################################################
    self . EditingWidget . SketchText = TEXT
    ##########################################################################
    self . EditingWidget . addWidget ( self . EditingWidget . SketchText     )
    ##########################################################################
    return
  ############################################################################
  def SaveAlbumChapters ( self                                             ) :
    ##########################################################################
    DKEY = "Chapters"
    DDIR = self . ALBUM . DIR
    DFIL = self . ALBUM . Album [ "Documents" ] [ DKEY                       ]
    DFIL = f"{DDIR}/{DFIL}"
    ##########################################################################
    BODY = self . EditingWidget . ChaptersText . toPlainText (               )
    ##########################################################################
    self . SaveDocument ( DFIL , BODY                                        )
    ##########################################################################
    return
  ############################################################################
  def addAlbumChapters         ( self                                      ) :
    ##########################################################################
    self . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 700
    ##########################################################################
    TOOL = QToolBar            (                                             )
    ##########################################################################
    TOOL . setMinimumHeight    ( 32                                          )
    TOOL . setMaximumHeight    ( 32                                          )
    TOOL . setIconSize         ( QSize ( 32 , 32                           ) )
    TOOL . setFloatable        ( False                                       )
    TOOL . setMovable          ( False                                       )
    TOOL . setToolButtonStyle  ( Qt . ToolButtonIconOnly                     )
    ##########################################################################
    MSG  = self . getMenuItem  ( "SaveChapters"                              )
    ICON = QIcon               ( QPixmap ( ":/images/save.png"             ) )
    MACT = TOOL . addAction    ( ICON , MSG                                  )
    ##########################################################################
    MACT . triggered . connect ( self . SaveAlbumChapters                    )
    ##########################################################################
    TEXT = QPlainTextEdit      (                                             )
    TEXT . setMinimumHeight    ( 200                                         )
    TEXT . resize              ( 400 , 640                                   )
    ##########################################################################
    DKEY = "Chapters"
    DDIR = self . ALBUM . DIR
    DFIL = self . ALBUM . Album [ "Documents" ] [ DKEY                       ]
    DFIL = f"{DDIR}/{DFIL}"
    DOC  = self . LoadDocument ( DFIL                                        )
    ##########################################################################
    TEXT . setPlainText        ( DOC                                         )
    MSG  = self . getMenuItem  ( "ChaptersArena"                             )
    TEXT . setToolTip          ( MSG                                         )
    ##########################################################################
    self . EditingWidget . ChaptersText = TEXT
    self . EditingWidget . ChaptersTool = TOOL
    ##########################################################################
    self . setAllFont ( self . EditingWidget . ChaptersText , self . font ( ) )
    self . EditingWidget . addWidget ( self . EditingWidget . ChaptersTool   )
    self . EditingWidget . addWidget ( self . EditingWidget . ChaptersText   )
    ##########################################################################
    return
  ############################################################################
  def SaveAlbumDescription ( self                                          ) :
    ##########################################################################
    DKEY = "Description"
    DDIR = self . ALBUM . DIR
    DFIL = self . ALBUM . Album [ "Documents" ] [ DKEY                       ]
    DFIL = f"{DDIR}/{DFIL}"
    ##########################################################################
    BODY = self . EditingWidget . DescriptionText . toPlainText (            )
    ##########################################################################
    self . SaveDocument   ( DFIL , BODY                                      )
    ##########################################################################
    return
  ############################################################################
  def addAlbumDescription      ( self                                      ) :
    ##########################################################################
    self . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 700
    ##########################################################################
    TOOL = QToolBar            (                                             )
    ##########################################################################
    TOOL . setMinimumHeight    ( 32                                          )
    TOOL . setMaximumHeight    ( 32                                          )
    TOOL . setIconSize         ( QSize ( 32 , 32                           ) )
    TOOL . setFloatable        ( False                                       )
    TOOL . setMovable          ( False                                       )
    TOOL . setToolButtonStyle  ( Qt . ToolButtonIconOnly                     )
    ##########################################################################
    MSG  = self . getMenuItem  ( "SaveDescription"                           )
    ICON = QIcon               ( QPixmap ( ":/images/save.png"             ) )
    MACT = TOOL . addAction    ( ICON , MSG                                  )
    ##########################################################################
    MACT . triggered . connect ( self . SaveAlbumDescription                 )
    ##########################################################################
    TEXT = QPlainTextEdit      (                                             )
    TEXT . setMinimumHeight    ( 200                                         )
    TEXT . resize              ( 400 , 640                                   )
    ##########################################################################
    DKEY = "Description"
    DDIR = self . ALBUM . DIR
    DFIL = self . ALBUM . Album [ "Documents" ] [ DKEY                       ]
    DFIL = f"{DDIR}/{DFIL}"
    DOC  = self . LoadDocument ( DFIL                                        )
    ##########################################################################
    TEXT . setPlainText        ( DOC                                         )
    MSG  = self . getMenuItem  ( "DescriptionArena"                          )
    TEXT . setToolTip          ( MSG                                         )
    ##########################################################################
    self . EditingWidget . DescriptionText = TEXT
    self . EditingWidget . DescriptionTool = TOOL
    ##########################################################################
    self . setAllFont ( self . EditingWidget . DescriptionText , self . font ( ) )
    self . EditingWidget . addWidget ( self . EditingWidget . DescriptionTool )
    self . EditingWidget . addWidget ( self . EditingWidget . DescriptionText )
    ##########################################################################
    return
  ############################################################################
  def DoEditing                    ( self                                  ) :
    ##########################################################################
    self  . logMessage             ( "OpenEpisodeDetails"                    )
    ##########################################################################
    self  . Method = "Editing"
    TITLE = self . ALBUM . Album [ "Names" ] [ "Default"                     ]
    ##########################################################################
    self  . setWindowTitle         ( TITLE                                   )
    ##########################################################################
    self . EditingWidget = QSplitter ( Qt . Vertical                         )
    self . EditingWidget . BaseHeight = 600
    self . EditingWidget . setChildrenCollapsible ( True                     )
    ## self . EditingWidget . setHandleWidth   ( 5                              )
    self . EditingWidget . Tick = datetime . datetime . now ( ) . timestamp ( ) - 1.0
    ##########################################################################
    self . addEditingTools         (                                         )
    self . addAlbumTitle           (                                         )
    self . addAlbumCoverSection    (                                         )
    ##########################################################################
    self . EditingWidget . NamesEditor = None
    self . EditingWidget . Identifiers = None
    self . EditingWidget . PeopleView  = None
    ##########################################################################
    if                             ( self . ALBUM . Uuid > 0               ) :
      ########################################################################
      self . addNamesEditor        (                                         )
      self . addAlbumIdentifiers   (                                         )
      self . addPeopleView         (                                         )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    self . addSketch               (                                         )
    self . addAlbumChapters        (                                         )
    self . addAlbumDescription     (                                         )
    ##########################################################################
    self . EditingWidget . Tail = QWidget (                                  )
    self . EditingWidget . Tail . resize           ( 100 , 5                 )
    self . EditingWidget . Tail . setMinimumHeight (  5                      )
    self . EditingWidget . Tail . setMaximumHeight ( 40                      )
    self . EditingWidget . addWidget ( self . EditingWidget . Tail           )
    ##########################################################################
    self . EditingWidget . setMinimumHeight ( self . EditingWidget . BaseHeight )
    self . EditingWidget . setFont ( self . font (                         ) )
    self . setWidget               ( self . EditingWidget                    )
    self . setWidgetResizable      ( True                                    )
    self . ResizeEditing           (                                         )
    ##########################################################################
    return
  ############################################################################
  def ResizeEditing                      ( self                            ) :
    ##########################################################################
    CTC  = datetime . datetime . now ( ) . timestamp (                       )
    LTC  = self . EditingWidget . Tick
    if                                   ( ( CTC - LTC ) < 0.1             ) :
      return False
    ##########################################################################
    self . EditingWidget . Tick = CTC
    ##########################################################################
    SW   = self .                 width  (                                   )
    SH   = self .                 height (                                   )
    ##########################################################################
    VSB  = self . verticalScrollBar      (                                   )
    ##########################################################################
    if                                   ( VSB not in [ False , None     ] ) :
      ########################################################################
      if                                 ( VSB . isVisible (             ) ) :
        ######################################################################
        SW = int                         ( SW - VSB . width ( ) - 2          )
        ######################################################################
      else                                                                   :
        ######################################################################
        SW = int                         ( SW - 4                            )
        ######################################################################
    else                                                                     :
      ########################################################################
      SW   = int                         ( SW - 4                            )
    ##########################################################################
    self        . EditingWidget . setMinimumWidth ( SW                       )
    ##########################################################################
    WW   = self . EditingWidget . width  (                                   )
    HH   = self . EditingWidget . height (                                   )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    if ( self . EditingWidget . NamesEditor not in [ False , None ]        ) :
      ########################################################################
      TH   = self . EditingWidget . NamesEditor     . height (               )
      self .        EditingWidget . NamesEditor     . resize ( WW , TH       )
    ##########################################################################
    if ( self . EditingWidget . Identifiers not in [ False , None ]        ) :
      ########################################################################
      TH   = self . EditingWidget . Identifiers     . height (               )
      self .        EditingWidget . Identifiers     . resize ( WW , TH       )
    ##########################################################################
    if ( self . EditingWidget . PeopleView  not in [ False , None ]        ) :
      ########################################################################
      TH   = self . EditingWidget . PeopleView      . height (               )
      self .        EditingWidget . PeopleView      . resize ( WW , TH       )
    ##########################################################################
    TH     = self . EditingWidget . TitleEditor     . height (               )
    self   .        EditingWidget . TitleEditor     . resize ( WW , TH       )
    ##########################################################################
    TH     = self . EditingWidget . SketchText      . height (               )
    self   .        EditingWidget . SketchText      . resize ( WW , TH       )
    ##########################################################################
    TH     = self . EditingWidget . ChaptersTool    . height (               )
    self   .        EditingWidget . ChaptersTool    . resize ( WW , TH       )
    ##########################################################################
    TH     = self . EditingWidget . ChaptersText    . height (               )
    self   .        EditingWidget . ChaptersText    . resize ( WW , TH       )
    ##########################################################################
    TH     = self . EditingWidget . DescriptionTool . height (               )
    self   .        EditingWidget . DescriptionTool . resize ( WW , TH       )
    ##########################################################################
    TH     = self . EditingWidget . DescriptionText . height (               )
    self   .        EditingWidget . DescriptionText . resize ( WW , TH       )
    ##########################################################################
    return False
  ############################################################################
  def Relocation                  ( self                                   ) :
    ##########################################################################
    if                            ( "Editing" == self . Method             ) :
      ########################################################################
      return self . ResizeEditing (                                          )
    ##########################################################################
    return False
  ############################################################################
  def RefreshJson                 ( self                                   ) :
    ##########################################################################
    self . ALBUM . LoadFromFile   (                                          )
    ##########################################################################
    if                            ( not self . ALBUM . Exists ( "Version") ) :
      return
    if                            ( not self . ALBUM . Exists ( "Edited" ) ) :
      return
    ##########################################################################
    EDITED = self . ALBUM . Album [ "Edited"                                 ]
    ##########################################################################
    if                            ( not EDITED                             ) :
      ########################################################################
      self . emitEstablish . emit (                                          )
      ########################################################################
      return
    ##########################################################################
    self   . emitEditing   . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def startup ( self , JsonFile , DIR                                      ) :
    ##########################################################################
    self . ALBUM . Filename = JsonFile
    self . ALBUM . DIR      = DIR
    ##########################################################################
    self . Go ( self . RefreshJson                                           )
    ##########################################################################
    return
  ############################################################################
  def CloseThis         ( self                                             ) :
    ##########################################################################
    self . Leave . emit ( self                                               )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def DockIn        ( self , shown                                         ) :
    ##########################################################################
    self . ShowDock (        shown                                           )
    ##########################################################################
    return
  ############################################################################
  def Visible        ( self , visible                                      ) :
    ##########################################################################
    self . Visiblity (        visible                                        )
    ##########################################################################
    return
  ############################################################################
  def Docking            ( self , Main , title , area , areas              ) :
    ##########################################################################
    super ( )  . Docking (        Main , self ,  title , area , areas        )
    if                   ( self . Dock == None                             ) :
      return
    ##########################################################################
    self . Dock . visibilityChanged . connect ( self . Visible               )
    ##########################################################################
    return
  ############################################################################
  def DoDockMenu                 ( self                                    ) :
    ##########################################################################
    MSGs   = self . Translations [ "EpisodeEditor" ] [ "Docking"             ]
    ##########################################################################
    p      = self . parentWidget (                                           )
    S      = False
    D      = False
    M      = False
    ##########################################################################
    if                           ( p == None                               ) :
      S    = True
    else                                                                     :
      ########################################################################
      if                         ( self . isDocking ( )                    ) :
        D  = True
      else                                                                   :
        M  = True
    ##########################################################################
    mm     = MenuManager         ( self                                      )
    ##########################################################################
    if                           (     S or D                              ) :
      MSG  = MSGs                [ "MDI"                                     ]
      mm   . addAction           ( 1001  , MSG                               )
    ##########################################################################
    if                           (     S or M                              ) :
      MSG  = MSGs                [ "Dock"                                    ]
      mm   . addAction           ( 1002 , MSG                                )
    ##########################################################################
    if                           ( not S                                   ) :
      MSG  = MSGs                [ "None"                                    ]
      mm   . addAction           ( 1003 , MSG                                )
    ##########################################################################
    mm     . setFont             ( self    . menuFont ( )                    )
    aa     = mm . exec_          ( QCursor . pos      ( )                    )
    at     = mm . at             ( aa                                        )
    ##########################################################################
    if                           ( at == 1001                              ) :
      self . attachMdi  . emit   ( self , self . dockingOrientation          )
      return
    ##########################################################################
    if                           ( at == 1002                              ) :
      self . attachDock . emit   ( self                                    , \
                                   self . windowTitle ( )                  , \
                                   self . dockingPlace                     , \
                                   self . dockingPlaces                      )
      return
    ##########################################################################
    if                           ( at == 1003                              ) :
      self . attachNone . emit   ( self                                      )
      return
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
