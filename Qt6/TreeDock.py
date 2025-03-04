# -*- coding: utf-8 -*-
##############################################################################
## TreeWidget
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
import PySide6
from   PySide6                         import QtCore
from   PySide6                         import QtGui
from   PySide6                         import QtWidgets
##############################################################################
from   PySide6 . QtCore                import *
from   PySide6 . QtGui                 import *
from   PySide6 . QtWidgets             import *
##############################################################################
from           . MenuManager           import MenuManager as MenuManager
from           . TreeWidget            import TreeWidget  as TreeWidget
from           . AttachDock            import AttachDock  as AttachDock
from           . LineEdit              import LineEdit    as LineEdit
from           . ComboBox              import ComboBox    as ComboBox
from           . SpinBox               import SpinBox     as SpinBox
##############################################################################
from   AITK    . Essentials . Relation import Relation    as Relation
from   AITK    . Calendars  . StarDate import StarDate    as StarDate
from   AITK    . Calendars  . Periode  import Periode     as Periode
from   AITK    . Pictures   . Gallery  import Gallery     as GalleryItem
from   AITK    . Videos     . Album    import Album       as AlbumItem
from   AITK    . People     . People   import People      as PeopleItem
##############################################################################
class TreeDock                    ( TreeWidget , AttachDock                ) :
  ############################################################################
  attachNone             = Signal ( QWidget                                  )
  attachStack            = Signal ( QWidget                                  )
  attachDock             = Signal ( QWidget                                , \
                                    str                                    , \
                                    Qt . DockWidgetArea                    , \
                                    Qt . DockWidgetAreas                     )
  attachMdi              = Signal ( QWidget , int                            )
  Clicked                = Signal ( int                                      )
  emitRelationParameters = Signal ( str , int , int                          )
  emitRestart            = Signal (                                          )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super (                   ) . __init__ ( parent , plan                   )
    super ( AttachDock , self ) . __init__ (                                 )
    self . InitializeDock                  (          plan                   )
    ##########################################################################
    ## WidgetClass                                                       ;
    ##########################################################################
    self . ClassTag           = ""
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 60
    self . AssignedAmount     = 0
    self . SortOrder          = "asc"
    self . LoopRunning        = True
    self . AtMenu             = False
    self . SpinStartId        = None
    self . SpinAmount         = None
    self . FetchTableKey      = "Tables"
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . defaultSelectionMode = "ContiguousSelection"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = None
    self . dockingPlaces      = None
    ## dockingPlace       ( Qt::RightDockWidgetArea     )
    ## dockingPlaces      ( Qt::TopDockWidgetArea       |
    ##                      Qt::BottomDockWidgetArea    |
    ##                      Qt::LeftDockWidgetArea      |
    ##                      Qt::RightDockWidgetArea     )
    ##########################################################################
    self . emitRestart . connect   ( self . restart                          )
    ##########################################################################
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ## self . MountClicked            ( 2                                       )
    ##########################################################################
    self . TreeBrushes = [ QBrush ( QColor ( 255 , 255 , 255 ) )           , \
                           QBrush ( QColor ( 255 , 244 , 244 ) )           , \
                           QBrush ( QColor ( 244 , 255 , 244 ) )           , \
                           QBrush ( QColor ( 244 , 244 , 255 ) )             ]
    ##########################################################################
    return
  ############################################################################
  def FocusOut ( self                                                      ) :
    ##########################################################################
    if         ( not self . isPrepared ( )                                 ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def setGrouping ( self , group                                           ) :
    self . Grouping    = group
    self . OldGrouping = group
    return self . Grouping
  ############################################################################
  def getGrouping ( self                                                   ) :
    return self . Grouping
  ############################################################################
  def isGrouping  ( self                                                   ) :
    return        ( self . Grouping in [ "Subordination" , "Reverse" ]       )
  ############################################################################
  def isOriginal       ( self                                              ) :
    return             ( self . Grouping in [ "Original"                   ] )
  ############################################################################
  def isSubordination  ( self                                              ) :
    return             ( self . Grouping in [ "Subordination"              ] )
  ############################################################################
  def isReverse        ( self                                              ) :
    return             ( self . Grouping in [  "Reverse"                   ] )
  ############################################################################
  def isSearching     ( self                                               ) :
    ##########################################################################
    return            ( self . Grouping in [ "Searching"                   ] )
  ############################################################################
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None"                      ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock"                      ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"                       ]
    STKMSG = self . Translations [ "Docking" ] [ "Stack"                     ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone  , IDPMSG             )
    self   . setLocalMessage     ( self . AttachToMdi   , MDIMSG             )
    self   . setLocalMessage     ( self . AttachToDock  , DCKMSG             )
    self   . setLocalMessage     ( self . AttachToStack , STKMSG             )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery                ( self                               ) :
    raise NotImplementedError         (                                      )
  ############################################################################
  def DefaultObtainsItemUuids         ( self , DB                          ) :
    ##########################################################################
    QQ      = self . ObtainUuidsQuery (                                      )
    UUIDs   =                         [                                      ]
    if                                ( len ( QQ ) > 0                     ) :
      UUIDs = DB   . ObtainUuids      ( QQ                                   )
    ##########################################################################
    return UUIDs
  ############################################################################
  def ObtainsItemUuids                    ( self , DB                      ) :
    return self . DefaultObtainsItemUuids ( DB                               )
  ############################################################################
  def ObtainsUuidNames                ( self , DB , UUIDs                  ) :
    ##########################################################################
    NAMEs   =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "Names"                              ]
      NAMEs = self . GetNames         ( DB , TABLE , UUIDs                   )
    ##########################################################################
    return NAMEs
  ############################################################################
  def CreateColorIcon      ( self , R , G , B , W , H                      ) :
    ##########################################################################
    IMG = QImage           ( W , H , QImage . Format_RGB32                   )
    IMG . fill             ( QColor ( R , G , B )                            )
    ##########################################################################
    PIX = QPixmap          (                                                 )
    PIX . convertFromImage ( IMG                                             )
    ##########################################################################
    return QIcon           ( PIX                                             )
  ############################################################################
  def FetchSessionInformation         ( self , DB                          ) :
    return
  ############################################################################
  def PrepareUuidItem    ( self , column , UUID , NAME                     ) :
    ##########################################################################
    IT = QTreeWidgetItem (                                                   )
    IT . setText         ( column , NAME                                     )
    IT . setToolTip      ( column , str ( UUID )                             )
    IT . setData         ( column , Qt . UserRole , str ( UUID )             )
    ##########################################################################
    return IT
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
  def twiceClicked        ( self , item , column                           ) :
    ##########################################################################
    uuid      = int       ( item . data ( column , Qt . UserRole )           )
    self . Clicked . emit ( uuid                                             )
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
  def DockingMenu                     ( self , menu                        ) :
    ##########################################################################
    if                                ( not self . HavingPlacement         ) :
      return
    ##########################################################################
    canDock  = self . isFunction      ( self . FunctionDocking               )
    if                                ( not canDock                        ) :
      return
    ##########################################################################
    p        = self . parentWidget    (                                      )
    S        = False
    D        = False
    M        = False
    ##########################################################################
    if                                ( p == None                          ) :
      S      = True
    else                                                                     :
      ########################################################################
      if                              ( self . isDocking ( )               ) :
        D    = True
      else                                                                   :
        M    = True
    ##########################################################################
    menu     . addSeparator           (                                      )
    ##########################################################################
    if                                ( self . HavingMDI                   ) :
      if                              (     S or D                         ) :
        ######################################################################
        msg  = self . getLocalMessage ( self . AttachToMdi                   )
        ico  = QIcon                  ( ":/images/GUI.png"                   )
        menu . addActionWithIcon      ( self . AttachToMdi  , ico , msg      )
    ##########################################################################
    if                                ( self . HavingDOCK                  ) :
      if                              (     S or M                         ) :
        ######################################################################
        msg  = self . getLocalMessage ( self . AttachToDock                  )
        ico  = QIcon                  ( ":/images/hidespeech.png"            )
        menu . addActionWithIcon      ( self . AttachToDock , ico , msg      )
    ##########################################################################
    ## if                                ( self . HavingSTACK                 ) :
    ##   if                              ( not S                              ) :
    ##     ######################################################################
    ##     msg  = self . getLocalMessage ( self . AttachToStack                 )
    ##     menu . addAction              ( self . AttachToStack , msg           )
    ##########################################################################
    if                                ( self . HavingALONE                 ) :
      if                              ( not S                              ) :
        ######################################################################
        msg  = self . getLocalMessage ( self . AttachToNone                  )
        menu . addAction              ( self . AttachToNone , msg            )
    ##########################################################################
    return
  ############################################################################
  def RunDocking                ( self , menu , action                     ) :
    ##########################################################################
    at = menu . at              ( action                                     )
    ##########################################################################
    if                          ( at == self . AttachToNone                ) :
      self . attachNone  . emit ( self                                       )
      return True
    ##########################################################################
    if                          ( at == self . AttachToMdi                 ) :
      self . attachMdi   . emit ( self , self . dockingOrientation           )
      return True
    ##########################################################################
    if                          ( at == self . AttachToDock                ) :
      self . attachDock  . emit ( self                                     , \
                                  self . windowTitle ( )                   , \
                                  self . dockingPlace                      , \
                                  self . dockingPlaces                       )
      return True
    ##########################################################################
    if                          ( at == self . AttachToStack               ) :
      self . attachStack . emit ( self                                       )
      return True
    ##########################################################################
    return False
  ############################################################################
  def AmountIndexMenu                   ( self , mm , HasFull = False      ) :
    ##########################################################################
    T      = int                        ( self . Total                       )
    AMT    = int                        ( self . Amount                      )
    if                                  ( T <= 0                           ) :
      return mm
    if                                  ( AMT > T                          ) :
      AMT  = T
    if                                  ( self . StartId > T               ) :
      self . StartId = 0
    ##########################################################################
    self   . AssignedAmount = AMT
    ##########################################################################
    MSG    = self . getMenuItem         ( "Total"                            )
    SSI    = self . getMenuItem         ( "SpinStartId"                      )
    SSA    = self . getMenuItem         ( "SpinAmount"                       )
    MSG    = MSG . format               ( T                                  )
    ##########################################################################
    mm     . addAction                  ( 9999991 , MSG                      )
    ##########################################################################
    self   . SpinStartId = SpinBox      ( None , self . PlanFunc             )
    self   . SpinStartId . setPrefix    ( SSI                                )
    self   . SpinStartId . setRange     ( 0 , self . Total                   )
    self   . SpinStartId . setValue     ( self . StartId                     )
    self   . SpinStartId . setAlignment ( Qt . AlignRight                    )
    mm     . addWidget                  ( 9999992 , self . SpinStartId       )
    ##########################################################################
    self   . SpinAmount  = SpinBox      ( None , self . PlanFunc             )
    self   . SpinAmount  . setPrefix    ( SSA                                )
    self   . SpinAmount  . setRange     ( 0 , self . Total                   )
    self   . SpinAmount  . setValue     ( AMT                                )
    self   . SpinAmount  . setAlignment ( Qt . AlignRight                    )
    mm     . addWidget                  ( 9999993 , self . SpinAmount        )
    ##########################################################################
    if                                  ( HasFull                          ) :
      ########################################################################
      MSG  = self . getMenuItem         ( "ShowEverything"                   )
      mm   . addAction                  ( 9999994 , MSG                      )
      ########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    return mm
  ############################################################################
  def RunAmountIndexMenu                ( self , ATID = -1                 ) :
    ##########################################################################
    if                                  ( 9999994 == ATID                  ) :
      ########################################################################
      self . StartId = 0
      self . Amount  = self . Total
      ########################################################################
      return True
    ##########################################################################
    if                                  ( self . SpinStartId == None       ) :
      return False
    ##########################################################################
    if                                  ( self . SpinAmount  == None       ) :
      return False
    ##########################################################################
    SID    = self . SpinStartId . value (                                    )
    AMT    = self . SpinAmount  . value (                                    )
    ##########################################################################
    self . SpinStartId = None
    self . SpinAmount  = None
    ##########################################################################
    if ( ( SID != self . StartId ) or ( AMT != self . AssignedAmount ) )     :
      ########################################################################
      self . StartId = SID
      self . Amount  = AMT
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def setSortingOrder              ( self , order                          ) :
    ##########################################################################
    self . SortOrder = order
    ##########################################################################
    return
  ############################################################################
  def getSortingOrder              ( self                                  ) :
    return self . SortOrder
  ############################################################################
  def SortingMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self  . Translations
    LOM    = mm    . addMenu       ( TRX [ "UI::Sorting" ]                   )
    ##########################################################################
    hid    = self . isSortingEnabled (                                       )
    msg    = TRX                   [ "UI::SortColumns"                       ]
    mm     . addActionFromMenu     ( LOM , 20000001 , msg , True , hid       )
    ##########################################################################
    hid    =                       ( self . SortOrder == "asc"               )
    msg    = TRX                   [ "UI::SortAsc"                           ]
    mm     . addActionFromMenu     ( LOM , 20000002 , msg , True , hid       )
    ##########################################################################
    hid    =                       ( self . SortOrder == "desc"              )
    msg    = TRX                   [ "UI::SortDesc"                          ]
    mm     . addActionFromMenu     ( LOM , 20000003 , msg , True , hid       )
    ##########################################################################
    return mm
  ############################################################################
  def RunSortingMenu               ( self , atId                           ) :
    ##########################################################################
    if                             ( atId == 20000001                      ) :
      ########################################################################
      if                           ( self . isSortingEnabled ( )           ) :
        self . setSortingEnabled   ( False                                   )
      else                                                                   :
        self . setSortingEnabled   ( True                                    )
      ########################################################################
      return False
    ##########################################################################
    if                             ( atId == 20000002                      ) :
      self . SortOrder = "asc"
      return True
    ##########################################################################
    if                             ( atId == 20000003                      ) :
      self . SortOrder = "desc"
      return True
    ##########################################################################
    return   False
  ############################################################################
  def DefaultColumnsMenu            ( self , mm , startId = 1              ) :
    ##########################################################################
    TRX     = self . Translations
    head    = self . headerItem     (                                        )
    COL     = mm   . addMenu        ( TRX [ "UI::Columns" ]                  )
    ##########################################################################
    for i in range                  ( startId , self . columnCount ( )     ) :
      ########################################################################
      msg   = head . text           ( i                                      )
      if                            ( len ( msg ) <= 0                     ) :
        msg = TRX                   [ "UI::Whitespace"                       ]
      ########################################################################
      hid   = self . isColumnHidden ( i                                      )
      mm    . addActionFromMenu     ( COL , 9000 + i , msg , True , not hid  )
    ##########################################################################
    return mm
  ############################################################################
  def AppendRefreshAction    ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Refresh"                                 ]
    icon = QIcon             ( ":/images/reload.png"                         )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendInsertAction     ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Insert"                                  ]
    icon = QIcon             ( ":/images/plus.png"                           )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendDeleteAction     ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Delete"                                  ]
    icon = QIcon             ( ":/images/delete.png"                         )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendRenameAction     ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::Rename"                                  ]
    icon = QIcon             ( ":/images/rename.png"                         )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def AppendClearAllAction   ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::ClearAll"                                ]
    icon = QIcon             ( ":/images/cut.png"                            )
    mm   . addActionWithIcon ( Id , icon , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def TryAppendEditNamesAction ( self , atItem , mm , Id                   ) :
    ##########################################################################
    if                         ( self . NotOkay ( atItem )                 ) :
      return mm
    ##########################################################################
    if                         ( self . NotOkay ( self . EditAllNames )    ) :
      return mm
    ##########################################################################
    return self . AppendEditNamesAction (                 mm , Id            )
  ############################################################################
  def AppendEditNamesAction  ( self , mm , Id                              ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX               [ "UI::EditNames"                               ]
    ICON = QIcon             ( ":/images/names.png"                          )
    mm   . addActionWithIcon ( Id , ICON , msg                               )
    ##########################################################################
    return mm
  ############################################################################
  def doEditAllNames ( self                                                ) :
    return           ( self . EditAllNames not in [ False , None ]           )
  ############################################################################
  def AppendTranslateAllAction ( self , mm , Id                            ) :
    ##########################################################################
    TRX = self . Translations
    msg = TRX                  [ "UI::TranslateAll"                          ]
    mm  . addAction            ( Id , msg                                    )
    ##########################################################################
    return mm
  ############################################################################
  ## 選單當中抓取項目資訊
  ############################################################################
  def GetMenuDetails              ( self , column = 0                      ) :
    ##########################################################################
    items  = self . selectedItems (                                          )
    atItem = self . currentItem   (                                          )
    uuid   = 0
    ##########################################################################
    if                            ( atItem not in [ False , None ]         ) :
      uuid = self . itemUuid      ( atItem , column                          )
    ##########################################################################
    return items , atItem , uuid
  ############################################################################
  def TranslateAll              ( self                                     ) :
    ##########################################################################
    DB    = self . ConnectDB    (                                            )
    if                          ( DB in [ False , None ]                   ) :
      return
    ##########################################################################
    TABLE = self . Tables       [ "Names"                                    ]
    FMT   = self . Translations [ "UI::Translating"                          ]
    self  . DoTranslateAll      ( DB , TABLE , FMT , 15.0                    )
    ##########################################################################
    DB    . Close               (                                            )
    ##########################################################################
    return
  ############################################################################
  def DoCopyToClipboard              ( self , SPEAK = True                 ) :
    ##########################################################################
    item   = self . currentItem      (                                       )
    if                               ( item in [ False , None ]            ) :
      return
    ##########################################################################
    column = self . currentColumn    (                                       )
    if                               ( column < 0                          ) :
      return
    ##########################################################################
    MSG    = item . text             ( column                                )
    LID    = self . getLocality      (                                       )
    qApp   . clipboard ( ) . setText ( MSG                                   )
    ##########################################################################
    if                               ( SPEAK                               ) :
      self . TtsTalk                 ( MSG , LID                             )
    ##########################################################################
    return
  ############################################################################
  def PageHome       ( self                                                ) :
    ##########################################################################
    self . StartId = 0
    self . restart   (                                                       )
    ##########################################################################
    return
  ############################################################################
  def PageEnd        ( self                                                ) :
    ##########################################################################
    self   . StartId = self . Total - self . Amount
    if               ( self . StartId <= 0                                 ) :
      self . StartId = 0
    ##########################################################################
    self   . restart (                                                       )
    ##########################################################################
    return
  ############################################################################
  def PageUp         ( self                                                ) :
    ##########################################################################
    self   . StartId = self . StartId - self . Amount
    if               ( self . StartId <= 0                                 ) :
      self . StartId = 0
    ##########################################################################
    self   . restart (                                                       )
    ##########################################################################
    return
  ############################################################################
  def PageDown       ( self                                                ) :
    ##########################################################################
    self   . StartId = self . StartId + self . Amount
    if               ( self . StartId > self . Total                       ) :
      self . StartId = self . Total
    ##########################################################################
    self   . restart (                                                       )
    ##########################################################################
    return
  ############################################################################
  def Finding          ( self                                              ) :
    ##########################################################################
    L    = self . SearchLine
    ##########################################################################
    if                 ( L in [ False , None ]                             ) :
      return
    ##########################################################################
    self . SearchLine = None
    T    = L . text    (                                                     )
    L    . deleteLater (                                                     )
    ##########################################################################
    if                 ( len ( T ) <= 0                                    ) :
      return
    ##########################################################################
    self . Go          ( self . looking , ( T , )                            )
    ##########################################################################
    return
  ############################################################################
  def Search                           ( self                              ) :
    ##########################################################################
    L      = LineEdit                  ( None , self . PlanFunc              )
    OK     = self . attacheStatusBar   ( L , 1                               )
    ##########################################################################
    if                                 ( not OK                            ) :
      ########################################################################
      L    . deleteLater               (                                     )
      self . Notify                    ( 1                                   )
      ########################################################################
      return
    ##########################################################################
    L      . blockSignals              ( True                                )
    L      . editingFinished . connect ( self . Finding                      )
    L      . blockSignals              ( False                               )
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    MSG    = self . getMenuItem        ( "Search"                            )
    L      . setPlaceholderText        ( MSG                                 )
    L      . setFocus                  ( Qt . TabFocusReason                 )
    ##########################################################################
    self   . SearchLine = L
    ##########################################################################
    return
  ############################################################################
  def SearchingForT1                  ( self , name , Main , NameTable     ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    OCPTAB  = self . Tables           [ Main                                 ]
    NAMTAB  = self . Tables           [ NameTable                            ]
    LIC     = self . getLocality      (                                      )
    LNAME   = name
    LNAME   = LNAME . lower           (                                      )
    LIKE    = f"%{LNAME}%"
    UUIDs   =                         [                                      ]
    ##########################################################################
    RQ      = f"select `uuid` from {OCPTAB} where ( `used` > 0 )"
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` = {LIC} )
                  and ( `uuid` in ( {RQ} ) )
                  and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if ( ( ALL in [ False , None ] ) or ( len ( ALL ) <= 0 ) )               :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    for U in ALL                                                             :
      UUIDs . append                  ( U [ 0 ]                              )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    self . SearchKey = name
    self . UUIDs     = UUIDs
    self . Method    = "Searching"
    ##########################################################################
    self . loading                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def SearchingForT2                  ( self , name , Main , NameTable     ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    OCPTAB  = self . Tables           [ Main                                 ]
    NAMTAB  = self . Tables           [ NameTable                            ]
    LIC     = self . getLocality      (                                      )
    LNAME   = name
    LNAME   = LNAME . lower           (                                      )
    LIKE    = f"%{LNAME}%"
    UUIDs   =                         [                                      ]
    ##########################################################################
    RQ      = f"select `uuid` from {OCPTAB} where ( `used` > 0 )"
    QQ      = f"""select `uuid` from {NAMTAB}
                  where ( `locality` = {LIC} )
                  and ( `uuid` in ( {RQ} ) )
                  and ( lower ( convert ( `name` using utf8 ) ) like %s )
                  group by `uuid` asc ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if ( ( ALL in [ False , None ] ) or ( len ( ALL ) <= 0 ) )               :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    for U in ALL                                                             :
      UUIDs . append                  ( U [ 0 ]                              )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    self . SearchKey = name
    self . UUIDs     = UUIDs
    self . Grouping  = "Searching"
    ##########################################################################
    self . loading                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def defaultPaste                  ( self , func                          ) :
    ##########################################################################
    T = qApp . clipboard ( ) . text (                                        )
    ##########################################################################
    if                              ( len ( T ) <= 0                       ) :
      return
    ##########################################################################
    self . Go                       ( func , ( T , )                         )
    ##########################################################################
    return
  ############################################################################
  def defaultImport                      ( self , func                     ) :
    ##########################################################################
    FILTERS       = self . Translations  [ "UI::PlainTextFiles"              ]
    Filename , Ok = QFileDialog . getOpenFileName                          ( \
                      self                                                 , \
                      self . windowTitle (                               ) , \
                      ""                                                   , \
                      FILTERS                                                )
    ##########################################################################
    if                                   ( len ( Filename ) <= 0           ) :
      return
    ##########################################################################
    BODY          = ""
    with open                            ( Filename , "rb" ) as f            :
      BODY        = f . read             (                                   )
    ##########################################################################
    if                                   ( len ( BODY ) <= 0               ) :
      return
    ##########################################################################
    text          = ""
    try                                                                      :
      text        = BODY . decode        ( "utf-8"                           )
    except                                                                   :
      return
    ##########################################################################
    if                                   ( len ( text ) <= 0               ) :
      return
    ##########################################################################
    self          . Go                   ( func , ( text , )                 )
    ##########################################################################
    return
  ############################################################################
  def ShowMenuItemTitleStatus ( self , menuItem , title , CNT              ) :
    ##########################################################################
    FMT  = self . getMenuItem ( menuItem                                     )
    MSG  = FMT  . format      ( title , CNT                                  )
    self . ShowStatus         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def ShowMenuItemCountStatus ( self , menuItem , CNT                      ) :
    ##########################################################################
    FMT  = self . getMenuItem ( menuItem                                     )
    MSG  = FMT  . format      ( CNT                                          )
    self . ShowStatus         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def ShowMenuItemMessage     ( self , menuItem                            ) :
    ##########################################################################
    MSG  = self . getMenuItem ( menuItem                                     )
    self . ShowStatus         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . Go      ( self . loading                                        )
    ##########################################################################
    return
  ############################################################################
  def restart        ( self                                                ) :
    ##########################################################################
    self . clear     (                                                       )
    self . startup   (                                                       )
    ##########################################################################
    return
  ############################################################################
  def RemoveMembers             ( self , UUIDs                             ) :
    ##########################################################################
    if                          ( not self . isGrouping ( )                ) :
      return False
    ##########################################################################
    DB       = self . ConnectDB (                                            )
    if                          ( DB in [ False , None ]                   ) :
      return False
    ##########################################################################
    RELTAB   = self . Tables    [ "Relation"                                 ]
    ##########################################################################
    DB       . LockWrites       ( [ RELTAB                                 ] )
    ##########################################################################
    if                          ( self . isSubordination ( )               ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set   ( "second" , UUID                            )
        QQ   = self . Relation . Delete ( RELTAB                             )
        DB   . Query            ( QQ                                         )
      ########################################################################
    elif                        ( self . isReverse       ( )               ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set   ( "first" , UUID                             )
        QQ   = self . Relation . Delete ( RELTAB                             )
        DB   . Query            ( QQ                                         )
    ##########################################################################
    DB       . Close            (                                            )
    ##########################################################################
    return True
  ############################################################################
  def UpdateTableItemValue    ( self , TABLE , uuid , item , value         ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB in [ False , None ]                     ) :
      return
    ##########################################################################
    DB     . LockWrites       ( [ TABLE                                    ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    QQ     = f"""update {TABLE}
                 set `{item}` = {value}
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    return
  ############################################################################
  def JoinMembers               ( self , TABLE , UUIDs                     ) :
    ##########################################################################
    if                          ( len ( UUIDs ) <= 0                       ) :
      return False
    ##########################################################################
    if                          ( not self . isGrouping ( )                ) :
      return False
    ##########################################################################
    DB       = self . ConnectDB (                                            )
    if                          ( DB in [ False , None ]                   ) :
      return False
    ##########################################################################
    DB       . LockWrites       ( [ TABLE                                  ] )
    ##########################################################################
    if                          ( self . isSubordination ( )               ) :
      ########################################################################
      self   . Relation . Joins ( DB , TABLE , UUIDs                         )
      ########################################################################
    elif                        ( self . isReverse       ( )               ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set   ( "first" , UUID                             )
        self . Relation . Join  ( DB      , TABLE                            )
    ##########################################################################
    DB       . UnlockTables     (                                            )
    DB       . Close            (                                            )
    ##########################################################################
    return True
  ############################################################################
  def Shutdown          ( self                                             ) :
    ##########################################################################
    self . StayAlive   = False
    self . LoopRunning = False
    ##########################################################################
    if                  ( self . isThreadRunning ( )                       ) :
      return False
    ##########################################################################
    self . Leave . emit ( self                                               )
    ##########################################################################
    return True
  ############################################################################
  def AppendToolNamingAction      ( self                                   ) :
    ##########################################################################
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names-editor.png" )    )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . GotoItemNamesEditor               )
    A    . setEnabled             ( False                                    )
    ##########################################################################
    self . WindowActions . append ( A                                        )
    self . HandleActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def GotoItemNamesEditor        ( self                                    ) :
    ##########################################################################
    atItem = self . currentItem  (                                           )
    if                           ( self . NotOkay ( atItem )               ) :
      return
    ##########################################################################
    self   . OpenItemNamesEditor ( atItem                                    )
    ##########################################################################
    return
  ############################################################################
  def defaultOpenItemNamesEditor ( self , item , column , scope , name     ) :
    ##########################################################################
    uuid   = item . data         ( column , Qt . UserRole                    )
    uuid   = int                 ( uuid                                      )
    NAMTAB = self . Tables       [ name                                      ]
    self   . EditAllNames        ( self , scope , uuid , NAMTAB              )
    ##########################################################################
    return
  ############################################################################
  def AtItemNamesEditor          ( self , at , Id , item                   ) :
    ##########################################################################
    if                           ( at == Id                                ) :
      ########################################################################
      self . OpenItemNamesEditor ( item                                      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def OpenItemNamesEditor ( self , item                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AppendingPictures        ( self , atUuid , NAME , JSON , table , T1  ) :
    ##########################################################################
    UUIDs  = JSON              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return False
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return False
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ table                                       ]
    GALM   = GalleryItem       (                                             )
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    GALM   . ConnectToPictures ( DB , RELTAB , atUuid , T1 , UUIDs           )
    ##########################################################################
    DB     . UnlockTables      (                                             )
    self   . setVacancy        (                                             )
    self   . GoRelax . emit    (                                             )
    DB     . Close             (                                             )
    ##########################################################################
    self   . Notify            ( 5                                           )
    ##########################################################################
    return True
  ############################################################################
  def AssignAccessibleName          ( self                                 ) :
    ##########################################################################
    NAME = self . getSearchLineText (                                        )
    self        . detachSearchTool  (                                        )
    self        . setAccessibleName ( NAME                                   )
    self        . Notify            ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def ConfigureAccessibleName      ( self                                  ) :
    ##########################################################################
    NAME = self . accessibleName   (                                         )
    self . attachSearchToolMessage ( self . AssignAccessibleName           , \
                                     "AccessibleName"                      , \
                                     NAME                                    )
    ##########################################################################
    return
  ############################################################################
  def EmitRelateParameters               ( self                            ) :
    ##########################################################################
    if                                   ( not self . isSubordination (  ) ) :
      return
    ##########################################################################
    UUID = self . Relation  . get        ( "first"                           )
    UUID = str                           ( UUID                              )
    TYPE = self . Relation  . get        ( "t1"                              )
    TYPE = int                           ( TYPE                              )
    RR   = self . Relation  . get        ( "relation"                        )
    RR   = int                           ( RR                                )
    ##########################################################################
    self . emitRelationParameters . emit ( UUID , RR , TYPE                  )
    ##########################################################################
    return
  ############################################################################
  def EmitOpenLogHistory         ( self , item , column = 0                ) :
    ##########################################################################
    uuid = item . data           ( column , Qt . UserRole                    )
    uuid = int                   ( uuid                                      )
    head = item . text           ( column                                    )
    nx   = ""
    ##########################################################################
    if                           ( "Notes" in self . Tables                ) :
      nx = self . Tables         [ "Notes"                                   ]
    ##########################################################################
    self . OpenLogHistory . emit ( head                                    , \
                                   str ( uuid )                            , \
                                   "Description"                           , \
                                   nx                                      , \
                                   str ( self . getLocality (            ) ) )
    ##########################################################################
    return
  ############################################################################
  def GotoItemDescription       ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . EmitOpenLogHistory ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
