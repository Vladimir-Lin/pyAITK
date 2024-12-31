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
from   pathlib                                              import Path
##############################################################################
import AITK
##############################################################################
from   AITK    . Calendars . StarDate                       import StarDate            as StarDate
from   AITK    . Documents . JSON                           import Load                as LoadJson
from   AITK    . Documents . JSON                           import Save                as SaveJson
##############################################################################
from   PySide6                                              import QtCore
from   PySide6                                              import QtGui
from   PySide6                                              import QtWidgets
from   PySide6 . QtCore                                     import *
from   PySide6 . QtGui                                      import *
from   PySide6 . QtWidgets                                  import *
from   AITK    . Qt6                                        import *
##############################################################################
from   AITK    . Qt6      . MenuManager                     import MenuManager         as MenuManager
from   AITK    . Qt6      . AttachDock                      import AttachDock          as AttachDock
from   AITK    . Qt6      . Widget                          import Widget              as Widget
##############################################################################
from   AITK    . Widgets  . Commons6 . NamesEditor          import NamesEditor
from   AITK    . People   . Widgets6 . PeopleView           import PeopleView
from   AITK    . Finance  . Widgets6 . IdentifierListings   import IdentifierListings
from   AITK    . Society  . Widgets6 . OrganizationListings import OrganizationListings
from   AITK    . Pictures . Widgets6 . GalleriesView        import GalleriesView
from   AITK    . Pictures . Widgets6 . PicturesView         import PicturesView
##############################################################################
from   AITK    . Videos   . Album                           import Album               as AlbumItem
from   AITK    . Videos   . Film                            import Film                as FilmItem
##############################################################################
from   AITK    . Videos   . Utilities                       import SilentRun           as SilentRun
##############################################################################
from                      . Episode                         import Episode             as Episode
##############################################################################
from                      . UiEpisodeEstablish              import Ui_EpisodeEstablish as Ui_EpisodeEstablish
##############################################################################
##############################################################################
##############################################################################
##############################################################################
##############################################################################
class EpisodeEditor          ( ScrollArea                                  ) :
  ############################################################################
  emitEstablish     = Signal (                                               )
  emitEditing       = Signal (                                               )
  emitCoversChanged = Signal (                                               )
  emitInformation   = Signal ( str , str                                     )
  emitLog           = Signal ( str                                           )
  emitPlay          = Signal ( QWidget                                       )
  Leave             = Signal ( QWidget                                       )
  ############################################################################
  def           __init__     ( self , parent = None , plan = None          ) :
    ##########################################################################
    super ( ) . __init__     (        parent        , plan                   )
    self      . Configure    (                                               )
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
    self . LoopRunning      = True
    self . ALBUM            = Episode (                                      )
    self . PLAYER           =         {                                      }
    self . ALBUM  . LogFunc = self . addLog
    self . Method = "Nothing"
    ##########################################################################
    self . CLI              = None
    self . EstablishWidget  = None
    self . EditingWidget    = None
    ##########################################################################
    self . emitEstablish     . connect ( self . DoEstablish                  )
    self . emitEditing       . connect ( self . DoEditing                    )
    self . emitCoversChanged . connect ( self . DoCoversChanged              )
    self . emitInformation   . connect ( self . OpenInformation              )
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
  def OpenInformation         ( self , title , msg                         ) :
    ##########################################################################
    QMessageBox . information ( self , title , msg                           )
    ##########################################################################
    return
  ############################################################################
  def PrepareForDB              ( self                                     ) :
    ##########################################################################
    if                          ( not self . LoopRunning                   ) :
      return None
    ##########################################################################
    HNAME  = self . DB          [ "hostname"                                 ]
    CDMSG  = self . getMenuItem ( "ConnectDB"                                )
    MSG    = f"{CDMSG}{HNAME}"
    self   . addLog             ( MSG                                        )
    ##########################################################################
    self   . ALBUM . Settings         = self . Settings
    self   . ALBUM . Translations     = self . Translations
    self   . ALBUM . Messages         = self . Translations [ "Episode"      ]
    self   . ALBUM . Tables           = self . Tables
    self   . ALBUM . CoverOpts        = self . CLI . CLI [ "Tables" ] [ "CoverOptions" ]
    self   . ALBUM . AlbumCoverTables = self . CLI . CLI [ "Tables" ] [ "AlbumCovers"  ]
    self   . ALBUM . PeopleViewTables = self . CLI . CLI [ "Tables" ] [ "PeopleView"   ]
    ##########################################################################
    self   . LoopRunning = False
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      self . LoopRunning = True
      return None
    ##########################################################################
    return DB
  ############################################################################
  def DoEstablish               ( self                                     ) :
    ##########################################################################
    self   . EstablishWidget      = QWidget (                                )
    self   . EstablishWidget . ui = Ui_EpisodeEstablish (                    )
    self   . EstablishWidget . ui . setupUi ( self . EstablishWidget         )
    self   . EstablishWidget . ui . Scanning . hide (                        )
    self   . EstablishWidget . ui . Start . clicked . connect ( self . DoEstablishAlbum )
    self   . EstablishWidget . ui . Close . clicked . connect ( self . CloseThis        )
    ##########################################################################
    if                          ( "Font" in self . Settings                ) :
      ########################################################################
      fnt  = QFont              (                                            )
      fnt  . fromString         ( self . Settings [ "Font" ]                 )
      ########################################################################
      self . setAllFont         ( self . EstablishWidget , fnt               )
    ##########################################################################
    self   . setWidget          ( self . EstablishWidget                     )
    self   . setWidgetResizable ( True                                       )
    ##########################################################################
    self   . Method = "Establish"
    ##########################################################################
    return
  ############################################################################
  def EstablishAlbum           ( self                                      ) :
    ##########################################################################
    DB   = self . PrepareForDB (                                             )
    if                         ( DB in [ False , None ]                    ) :
      return
    ##########################################################################
    self . ALBUM . Establish   ( DB                                          )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    self . LoopRunning = True
    ##########################################################################
    self . Notify              ( 5                                           )
    self . emitEditing . emit  (                                             )
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
    MACT . triggered . connect ( self . DoMainMenu                           )
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
  def AlbumLanguageChanged ( self , IDX                                    ) :
    ##########################################################################
    LCID = int ( self . EditingWidget . LanguageEditor . itemData ( IDX )    )
    ##########################################################################
    self . ALBUM . Album [ "Language" ] = LCID
    ##########################################################################
    if ( self . EditingWidget . PeopleView not in [ False , None ] )         :
      ########################################################################
      self . EditingWidget . PeopleView . setLocality ( LCID                 )
      self . EditingWidget . PeopleView . startup     (                      )
    ##########################################################################
    return
  ############################################################################
  def addAlbumTitle         ( self                                         ) :
    ##########################################################################
    self  . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 32
    ##########################################################################
    TITLE  = self . ALBUM . Album [ "Names" ] [ "Default"                    ]
    UUID   = self . ALBUM . Uuid
    UXID   = ""
    ##########################################################################
    if                      ( UUID > 0                                     ) :
      UXID = f"{UUID}"
    ##########################################################################
    SPLT   = QSplitter      ( Qt . Horizontal                                )
    LEDIT  = QComboBox      (                                                )
    TEDIT  = QLineEdit      (                                                )
    UEDIT  = QLineEdit      (                                                )
    ##########################################################################
    LOCs   = self . Translations  [ "EpisodeEditor" ] [ "Languages"          ]
    LANG   = self . ALBUM . Album [ "Language"                               ]
    KEYs   = LOCs . keys    (                                                )
    LCAT   = -1
    LCNT   = 0
    LEDIT  . setGeometry    ( 0 , 0 , 120 , 28                               )
    LEDIT  . setMinimumSize ( 120 , 28                                       )
    LEDIT  . setMaximumSize ( 120 , 28                                       )
    ##########################################################################
    for ID in KEYs                                                           :
      ########################################################################
      LEDIT . addItem       ( LOCs [ ID ] , ID                               )
      ########################################################################
      if                    ( LANG == int ( ID )                           ) :
        ######################################################################
        LCAT = LCNT
      ########################################################################
      LCNT  = LCNT + 1
    ##########################################################################
    if                      ( LCAT >= 0                                    ) :
      ########################################################################
      LEDIT . setCurrentIndex ( LCAT)
    ##########################################################################
    LEDIT  . currentIndexChanged . connect ( self . AlbumLanguageChanged     )
    ##########################################################################
    TEDIT  . setGeometry    ( 0 , 0 , 400 , 28                               )
    TEDIT  . setMinimumSize ( 240 , 28                                       )
    TEDIT  . setText        ( TITLE                                          )
    TEDIT  . editingFinished . connect ( self . AlbumTitleChanged            )
    ##########################################################################
    UEDIT  . setGeometry    ( 0 , 0 , 240 , 28                               )
    UEDIT  . setMinimumSize ( 120 , 28                                       )
    UEDIT  . setText        ( UXID                                           )
    UEDIT  . setReadOnly    ( True                                           )
    ##########################################################################
    SPLT   . addWidget      ( LEDIT                                          )
    SPLT   . addWidget      ( TEDIT                                          )
    SPLT   . addWidget      ( UEDIT                                          )
    ##########################################################################
    self   . EditingWidget . TitleSplit     = SPLT
    self   . EditingWidget . LanguageEditor = LEDIT
    self   . EditingWidget . TitleEditor    = TEDIT
    self   . EditingWidget . UuidEditor     = UEDIT
    ##########################################################################
    self   . EditingWidget . addWidget ( self . EditingWidget . TitleSplit   )
    ##########################################################################
    return
  ############################################################################
  def AssignCoverImageToToolButton   ( self                                ) :
    ##########################################################################
    TCW   = 640
    TCH   = 360
    CF    = self . ALBUM . CoverFile (                                       )
    CIM   = QImage                   ( CF                                    )
    ##########################################################################
    if                               ( CIM . width  ( ) > TCW              ) :
      ########################################################################
      TTH = int ( int ( TCW * CIM . height ( ) ) / CIM . width (           ) )
      CIM = CIM . scaled             ( TCW , TTH , Qt . KeepAspectRatio      )
    ##########################################################################
    if                               ( CIM . height ( ) > TCH              ) :
      ########################################################################
      TTW = int ( int ( TCH * CIM . width ( ) ) / CIM . height (           ) )
      CIM = CIM . scaled             ( TTW , TCH , Qt . KeepAspectRatio      )
    ##########################################################################
    if                               ( CIM . width  ( ) > TCW              ) :
      ########################################################################
      TTH = int ( int ( TCW * CIM . height ( ) ) / CIM . width (           ) )
      CIM = CIM . scaled             ( TCW , TTH , Qt . KeepAspectRatio      )
    ##########################################################################
    PIX   = QPixmap                  (                                       )
    ##########################################################################
    if                               ( PIX . convertFromImage( CIM       ) ) :
      ########################################################################
      ICN = QIcon                    ( PIX                                   )
      self  . EditingWidget . Cover . setIconSize ( CIM . size (           ) )
      self  . EditingWidget . Cover . setIcon     ( ICN                      )
    ##########################################################################
    return
  ############################################################################
  def ChangeCoverImage           ( self                                    ) :
    ##########################################################################
    Title   = self . getMenuItem ( "AssignCoverImage"                        )
    Filters = self . getMenuItem ( "CoverImageFilters"                       )
    ROOT    = self . ALBUM . DIR
    ROOT    = f"{ROOT}/images"
    ##########################################################################
    ( PFILE , filter ) = QFileDialog . getOpenFileName                       (
                           self                                            , \
                           Title                                           , \
                           ROOT                                            , \
                           Filters                                           )
    ##########################################################################
    if                           ( len ( PFILE ) <= 0                      ) :
      return
    ##########################################################################
    PROOT   = f"{ROOT}/"
    ##########################################################################
    if                           ( PROOT not in PFILE                      ) :
      ########################################################################
      MSG   = self . getMenuItem ( "CoverImageNotInPlace"                    )
      self  . OpenInformation    ( Title , MSG                               )
      ########################################################################
      return
    ##########################################################################
    CFILE   = PFILE . replace    ( PROOT , ""                                )
    self    . ALBUM . Album [ "Images" ] [ "Cover" ] = CFILE
    ##########################################################################
    self    . AssignCoverImageToToolButton (                                 )
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
    self . EditingWidget . Cover . clicked . connect ( self . ChangeCoverImage )
    ##########################################################################
    self . EditingWidget . addWidget    ( self . EditingWidget . Cover       )
    ##########################################################################
    if                                  ( not self . ALBUM . isCover (   ) ) :
      return
    ##########################################################################
    self . AssignCoverImageToToolButton (                                    )
    ##########################################################################
    return
  ############################################################################
  def addCompanyAndNames            ( self                                 ) :
    ##########################################################################
    self  . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 240
    ##########################################################################
    SPLT  = QSplitter               ( Qt . Horizontal                        )
    SPLT  . setMinimumHeight        ( 120                                    )
    SPLT  . setMaximumHeight        ( 400                                    )
    ##########################################################################
    TNE   = NamesEditor             ( None , self . PlanFunc                 )
    TNE   . setMinimumWidth         ( 240                                    )
    TNE   . setMinimumHeight        ( 120                                    )
    TNE   . setMaximumHeight        ( 400                                    )
    TNE   . resize                  ( 400 , 240                              )
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
    DKEY   = "OrganizationListings"
    ORGS   = OrganizationListings   ( None , self . PlanFunc                 )
    ORGS   . setMinimumWidth        ( 160                                    )
    ORGS   . setMinimumHeight       ( 120                                    )
    ORGS   . setMaximumHeight       ( 400                                    )
    ORGS   . resize                 ( 400 , 240                              )
    ##########################################################################
    ORGS   . Hosts        = { "Database" : self . Settings [ "Database" ]  , \
                              "Oriphase" : self . Settings [ "Oriphase" ]    }
    ORGS   . DB           = self . DB
    ORGS   . Settings     = self . Settings
    ORGS   . Translations = self . Translations
    ORGS   . Tables       = self . Tables [ DKEY                             ]
    ##########################################################################
    ORGS   . Relation . set         ( "second" , self . ALBUM . Uuid         )
    ORGS   . Relation . set         ( "t2"     , 76                          )
    ORGS   . Relation . setT1       ( "Organization"                         )
    ORGS   . Relation . setRelation ( "Subordination"                        )
    ORGS   . setGrouping            ( "Reverse"                              )
    ##########################################################################
    LANGZ  = self . Translations    [ DKEY ] [ "Languages"                   ]
    MENUZ  = self . Translations    [ DKEY ] [ "Menus"                       ]
    ##########################################################################
    ORGS   . PrepareMessages        (                                        )
    ##########################################################################
    ORGS   . setLocality            ( self . getLocality ( )                 )
    ORGS   . setLanguages           ( LANGZ                                  )
    ORGS   . setMenus               ( MENUZ                                  )
    ##########################################################################
    if                              ( "Font" in self . Settings            ) :
      fnt  = QFont                  (                                        )
      fnt  . fromString             ( self . Settings [ "Font" ]             )
      ORGS . setFont                ( fnt                                    )
    ##########################################################################
    ORGS   . PrepareForActions      (                                        )
    ##########################################################################
    ORGS   . PeopleGroup         . connect ( self . MAIN . ShowPeopleGroup       )
    ORGS   . AlbumGroup          . connect ( self . MAIN . OpenAlbumGroup        )
    ORGS   . OpenVariantTables   . connect ( self . MAIN . OpenVariantTables     )
    ORGS   . ShowWebPages        . connect ( self . MAIN . ShowWebPages          )
    ORGS   . OpenLogHistory      . connect ( self . MAIN . OpenLogHistory        )
    ORGS   . OpenIdentifiers     . connect ( self . MAIN . OpenIdentifiers       )
    ORGS   . emitVendorDirectory . connect ( self . MAIN . CreateVendorDirectory )
    ORGS   . emitLog             . connect ( self . MAIN . appendLog             )
    ##########################################################################
    SPLT   .                 addWidget ( TNE                                 )
    SPLT   .                 addWidget ( ORGS                                )
    ##########################################################################
    self   . EditingWidget . CompanyAndNames = SPLT
    self   . EditingWidget . NamesEditor     = TNE
    self   . EditingWidget . Organizations   = ORGS
    ##########################################################################
    self   . EditingWidget . addWidget ( SPLT                                )
    ##########################################################################
    TNE    . startup                   (                                     )
    ORGS   . startup                   (                                     )
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
    dIcon = QIcon             ( ":/images/buddy.png"                         )
    PEOW  . setDefaultIcon    ( dIcon                                        )
    PEOW  . setMinimumHeight  ( 160                                          )
    PEOW  . resize            ( 400 , 320                                    )
    ##########################################################################
    KEY   = "PeopleView"
    PEOW  . DB           = self . DB
    PEOW  . Hosts        = { "Database" : self . Settings [ "Database" ]   , \
                             "Oriphase" : self . Settings [ "Oriphase" ]     }
    PEOW  . Settings     = self . Settings
    PEOW  . Translations = self . Translations
    PEOW  . Tables       = self . CLI . CLI [ "Tables" ] [ "PeopleView"      ]
    PEOW  . Relation . set    ( "second" , int ( self . ALBUM . Uuid )       )
    PEOW  . Relation . set    ( "t2"     , 76                                )
    PEOW  . setGrouping       ( "Reverse"                                    )
    ##########################################################################
    LANGZ = self . Translations [ KEY ] [ "Languages"                        ]
    MENUZ = self . Translations [ KEY ] [ "Menus"                            ]
    ##########################################################################
    PEOW  . PrepareMessages   (                                              )
    PEOW  . setLocality       ( int ( self . ALBUM . Album [ "Language" ] )  )
    PEOW  . setLanguages      ( LANGZ                                        )
    PEOW  . setMenus          ( MENUZ                                        )
    ##########################################################################
    PEOW  . ShowGalleries         . connect ( self . MAIN . ShowGalleries            )
    PEOW  . ShowGalleriesRelation . connect ( self . MAIN . ShowGalleriesRelation    )
    PEOW  . ShowPersonalGallery   . connect ( self . MAIN . ShowPersonalGallery      )
    PEOW  . ShowPersonalIcons     . connect ( self . MAIN . ShowPersonalIcons        )
    ## PEOW  . ShowPersonalFaces     . connect ( self . MAIN . ShowFaceViewByPeople     )
    PEOW  . ShowVideoAlbums       . connect ( self . MAIN . ShowVideoAlbums          )
    PEOW  . ShowWebPages          . connect ( self . MAIN . ShowWebPages             )
    PEOW  . OwnedOccupation       . connect ( self . MAIN . OwnedOccupationSubgroups )
    PEOW  . OpenVariantTables     . connect ( self . MAIN . OpenVariantTables        )
    ## PEOW  . ShowLodListings       . connect ( self . MAIN . ShowLodListings          )
    PEOW  . OpenLogHistory        . connect ( self . MAIN . OpenLogHistory           )
    ## PEOW  . OpenBodyShape         . connect ( self . MAIN . OpenBodyShape            )
    PEOW  . emitOpenSmartNote     . connect ( self . MAIN . assignSmartNote          )
    PEOW  . emitLog              . connect ( self . MAIN . appendLog         )
    ##########################################################################
    self  . setAllFont        ( PEOW , self . font (                       ) )
    PEOW  . PrepareForActions (                                              )
    ##########################################################################
    self . EditingWidget . PeopleView = PEOW
    ##########################################################################
    self . EditingWidget . addWidget ( self . EditingWidget . PeopleView     )
    ##########################################################################
    PEOW . startup            (                                              )
    ##########################################################################
    return
  ############################################################################
  def addAlbumGallery         ( self                                       ) :
    ##########################################################################
    self . EditingWidget . BaseHeight = self . EditingWidget . BaseHeight + 320
    ##########################################################################
    PSVW  = PicturesView      ( None , self . PlanFunc                       )
    ##########################################################################
    dIcon = QIcon             ( ":/images/pictures.png"                      )
    PSVW  . setDefaultIcon    ( dIcon                                        )
    PSVW  . setMinimumHeight  ( 160                                          )
    PSVW  . resize            ( 400 , 320                                    )
    ##########################################################################
    KEY   = "PicturesView"
    PSVW  . DB           = self . DB
    PSVW  . Hosts        = { "Database" : self . Settings [ "Database" ]   , \
                             "Oriphase" : self . Settings [ "Oriphase" ]     }
    PSVW  . Settings     = self . Settings
    PSVW  . Translations = self . Translations
    PSVW  . Tables       = self . CLI . CLI [ "Tables" ] [ "AlbumCovers"     ]
    PSVW  . EditAllNames = None
    PSVW  . Relation . set    ( "first" , int ( self . ALBUM . Uuid )        )
    PSVW  . Relation . set    ( "t1"     , 76                                )
    PSVW  . Relation . setRelation ( "Subordination"                         )
    PSVW  . setGrouping       ( "Subordination"                              )
    ##########################################################################
    LANGZ = self . Translations [ KEY ] [ "Languages"                        ]
    MENUZ = self . Translations [ KEY ] [ "Menus"                            ]
    ##########################################################################
    PSVW  . PrepareMessages   (                                              )
    PSVW  . setLocality       ( self . getLocality ( )                       )
    PSVW  . setLanguages      ( LANGZ                                        )
    PSVW  . setMenus          ( MENUZ                                        )
    ##########################################################################
    PSVW  . ShowPicture       . connect ( self . MAIN . ShowPicture          )
    ## PSVW  . OpenPictureEditor . connect ( self . MAIN . OpenPictureEditor    )
    PSVW  . OpenVariantTables . connect ( self . MAIN . OpenVariantTables    )
    PSVW  . OpenLogHistory    . connect ( self . MAIN . OpenLogHistory       )
    ##########################################################################
    self  . setAllFont        ( PSVW , self . font (                       ) )
    PSVW  . PrepareForActions (                                              )
    ##########################################################################
    self  . EditingWidget . GalleryViewer = PSVW
    ##########################################################################
    self  . EditingWidget . addWidget ( self . EditingWidget . GalleryViewer )
    ##########################################################################
    PSVW  . PrepareRelateType      ( "Subordination"                         )
    PSVW  . startup                (                                         )
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
    self . EditingWidget . NamesEditor   = None
    self . EditingWidget . Organizations = None
    self . EditingWidget . Identifiers   = None
    self . EditingWidget . PeopleView    = None
    ##########################################################################
    if                             ( self . ALBUM . Uuid > 0               ) :
      ########################################################################
      self . addCompanyAndNames    (                                         )
      self . addAlbumIdentifiers   (                                         )
      self . addPeopleView         (                                         )
      self . addAlbumGallery       (                                         )
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
    if ( self . EditingWidget . CompanyAndNames not in [ False , None ]    ) :
      ########################################################################
      TH   = self . EditingWidget . CompanyAndNames . height (               )
      self .        EditingWidget . CompanyAndNames . resize ( WW , TH       )
    ##########################################################################
    if ( self . EditingWidget . Identifiers   not in [ False , None ]      ) :
      ########################################################################
      TH   = self . EditingWidget . Identifiers     . height (               )
      self .        EditingWidget . Identifiers     . resize ( WW , TH       )
    ##########################################################################
    if ( self . EditingWidget . PeopleView    not in [ False , None ]      ) :
      ########################################################################
      TH   = self . EditingWidget . PeopleView      . height (               )
      self .        EditingWidget . PeopleView      . resize ( WW , TH       )
    ##########################################################################
    if ( self . EditingWidget . GalleryViewer not in [ False , None ]      ) :
      ########################################################################
      TH   = self . EditingWidget . GalleryViewer   . height (               )
      self .        EditingWidget . GalleryViewer   . resize ( WW , TH       )
    ##########################################################################
    TH     = self . EditingWidget . TitleSplit      . height (               )
    self   .        EditingWidget . TitleSplit      . resize ( WW , TH       )
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
  def ScanCoversWithinDirectories  ( self                                  ) :
    ##########################################################################
    self . ALBUM . ScanAlbumImages (                                         )
    self . logMessage              ( "ExecuteCompleted"                      )
    ##########################################################################
    return
  ############################################################################
  def DoCoversChanged ( self                                               ) :
    ##########################################################################
    if ( self . EditingWidget . GalleryViewer in [ False , None ]          ) :
      return
    ##########################################################################
    self . EditingWidget . GalleryViewer . startup (                         )
    ##########################################################################
    return
  ############################################################################
  def SyncCoversToDatabase                ( self                           ) :
    ##########################################################################
    DB   = self . PrepareForDB            (                                  )
    if                                    ( DB in [ False , None ]         ) :
      return
    ##########################################################################
    self . ALBUM . SyncCoversToDatabase   ( DB                               )
    self . ALBUM . SyncCoversFromDatabase ( DB                               )
    ##########################################################################
    DB   . Close                          (                                  )
    ##########################################################################
    self . LoopRunning = True
    ##########################################################################
    self . Notify                         ( 5                                )
    self . logMessage                     ( "ExecuteCompleted"               )
    self . emitCoversChanged . emit       (                                  )
    ##########################################################################
    return
  ############################################################################
  def SyncActorsFromDatabase              ( self                           ) :
    ##########################################################################
    DB   = self . PrepareForDB            (                                  )
    if                                    ( DB in [ False , None ]         ) :
      return
    ##########################################################################
    self . ALBUM . SyncActorsFromDatabase ( DB                               )
    ##########################################################################
    DB   . Close                          (                                  )
    ##########################################################################
    self . LoopRunning = True
    ##########################################################################
    self . Notify                         ( 5                                )
    self . logMessage                     ( "ExecuteCompleted"               )
    ##########################################################################
    return
  ############################################################################
  def SyncClipsFromDatabase              ( self                            ) :
    ##########################################################################
    DB   = self . PrepareForDB           (                                   )
    if                                   ( DB in [ False , None ]          ) :
      return
    ##########################################################################
    self . ALBUM . SyncClipsFromDatabase ( DB                                )
    ##########################################################################
    DB   . Close                         (                                   )
    ##########################################################################
    self . LoopRunning = True
    ##########################################################################
    self . Notify                        ( 5                                 )
    self . logMessage                    ( "ExecuteCompleted"                )
    ##########################################################################
    return
  ############################################################################
  def AppendClipsToDatabase              ( self                            ) :
    ##########################################################################
    DB   = self . PrepareForDB           (                                   )
    if                                   ( DB in [ False , None ]          ) :
      return
    ##########################################################################
    self . ALBUM . AppendClipsToDatabase ( DB                                )
    ##########################################################################
    DB   . Close                         (                                   )
    ##########################################################################
    self . LoopRunning = True
    ##########################################################################
    self . Notify                        ( 5                                 )
    self . logMessage                    ( "ExecuteCompleted"                )
    ##########################################################################
    return
  ############################################################################
  def UpdateClipsToDatabase              ( self                            ) :
    ##########################################################################
    DB   = self . PrepareForDB           (                                   )
    if                                   ( DB in [ False , None ]          ) :
      return
    ##########################################################################
    self . ALBUM . UpdateClipsToDatabase ( DB                                )
    ##########################################################################
    DB   . Close                         (                                   )
    ##########################################################################
    self . LoopRunning = True
    ##########################################################################
    self . Notify                        ( 5                                 )
    self . logMessage                    ( "ExecuteCompleted"                )
    ##########################################################################
    return
  ############################################################################
  def UpdateClipsToGroups                ( self                            ) :
    ##########################################################################
    DB   = self . PrepareForDB           (                                   )
    if                                   ( DB in [ False , None ]          ) :
      return
    ##########################################################################
    self . ALBUM . UpdateClipsToGroups ( DB                                )
    ##########################################################################
    DB   . Close                         (                                   )
    ##########################################################################
    self . LoopRunning = True
    ##########################################################################
    self . Notify                        ( 5                                 )
    self . logMessage                    ( "ExecuteCompleted"                )
    ##########################################################################
    return
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
  def DoMainMenu                ( self                                     ) :
    ##########################################################################
    mm     = MenuManager        ( self                                       )
    ##########################################################################
    MSG    = self . getMenuItem ( "ScanCovers"                               )
    mm     . addAction          ( 1001  , MSG                                )
    ##########################################################################
    MSG    = self . getMenuItem ( "SyncCovers"                               )
    mm     . addAction          ( 1002  , MSG                                )
    ##########################################################################
    MSG    = self . getMenuItem ( "SyncActors"                               )
    mm     . addAction          ( 1003  , MSG                                )
    ##########################################################################
    MSG    = self . getMenuItem ( "SyncClips"                                )
    mm     . addAction          ( 1004  , MSG                                )
    ##########################################################################
    MSG    = self . getMenuItem ( "AppendClips"                              )
    mm     . addAction          ( 1005  , MSG                                )
    ##########################################################################
    MSG    = self . getMenuItem ( "UpdateClips"                              )
    mm     . addAction          ( 1006  , MSG                                )
    ##########################################################################
    MSG    = self . getMenuItem ( "ClipsJoinGroups"                          )
    mm     . addAction          ( 1007  , MSG                                )
    ##########################################################################
    mm     . setFont            ( self    . menuFont ( )                     )
    aa     = mm . exec_         ( QCursor . pos      ( )                     )
    at     = mm . at            ( aa                                         )
    ##########################################################################
    if                          ( at == 1001                               ) :
      ########################################################################
      self . Go                 ( self . ScanCoversWithinDirectories         )
      ########################################################################
      return
    ##########################################################################
    if                          ( at == 1002                               ) :
      ########################################################################
      self . Go                 ( self . SyncCoversToDatabase                )
      ########################################################################
      return
    ##########################################################################
    if                          ( at == 1003                               ) :
      ########################################################################
      self . Go                 ( self . SyncActorsFromDatabase              )
      ########################################################################
      return
    ##########################################################################
    if                          ( at == 1004                               ) :
      ########################################################################
      self . Go                 ( self . SyncClipsFromDatabase               )
      ########################################################################
      return
    ##########################################################################
    if                          ( at == 1005                               ) :
      ########################################################################
      self . Go                 ( self . AppendClipsToDatabase               )
      ########################################################################
      return
    ##########################################################################
    if                          ( at == 1006                               ) :
      ########################################################################
      self . Go                 ( self . UpdateClipsToDatabase               )
      ########################################################################
      return
    ##########################################################################
    if                          ( at == 1007                               ) :
      ########################################################################
      self . Go                 ( self . UpdateClipsToGroups                 )
      ########################################################################
      return
    ##########################################################################
    return
##############################################################################
