# -*- coding: utf-8 -*-
##############################################################################
## PeopleView
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
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import pyqtSlot
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QMimeData
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QMouseEvent
from   PyQt5 . QtGui                  import QDrag
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QListWidget
from   PyQt5 . QtWidgets              import QListWidgetItem
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QFileDialog
##############################################################################
from   AITK  . Qt . IconDock          import IconDock    as IconDock
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation    as Relation
from   AITK  . Calendars  . StarDate  import StarDate    as StarDate
from   AITK  . Calendars  . Periode   import Periode     as Periode
from   AITK  . Pictures   . Gallery   import Gallery     as GalleryItem
from   AITK  . People     . People    import People      as PeopleItem
##############################################################################
class PeopleView                     ( IconDock                            ) :
  ############################################################################
  HavingMenu            = 1371434312
  ############################################################################
  ShowPersonalGallery   = pyqtSignal ( str , int , str  ,       QIcon        )
  ShowPersonalIcons     = pyqtSignal ( str , int , str  , str , QIcon        )
  ShowPersonalFaces     = pyqtSignal ( str , str                             )
  ShowGalleries         = pyqtSignal ( str , int , str  ,       QIcon        )
  ShowGalleriesRelation = pyqtSignal ( str , int , str  , str , QIcon        )
  ShowVideoAlbums       = pyqtSignal ( str , int , str  ,       QIcon        )
  ShowWebPages          = pyqtSignal ( str , int , str  , str , QIcon        )
  OwnedOccupation       = pyqtSignal ( str , int , str  , str , QIcon        )
  OpenVariantTables     = pyqtSignal ( str , str , int  , str , dict         )
  ShowLodListings       = pyqtSignal ( str , str              , QIcon        )
  OpenLogHistory        = pyqtSignal ( str , str , str  , str , str          )
  OpenBodyShape         = pyqtSignal ( str , str , dict                      )
  emitOpenSmartNote     = pyqtSignal ( str                                   )
  ############################################################################
  def __init__                       ( self , parent = None , plan = None  ) :
    ##########################################################################
    super ( ) . __init__             (        parent        , plan           )
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 60
    self . SortOrder          = "asc"
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . dockingPlace       = Qt . BottomDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT1        ( "People"                                )
    self . Relation . setT2        ( "People"                                )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def GetUuidIcon                    ( self , DB , UUID                    ) :
    ##########################################################################
    RELTAB = self . Tables           [ "Relation"                            ]
    ##########################################################################
    return self . defaultGetUuidIcon ( DB , RELTAB , "People" , UUID         )
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "People"                                    ]
    QQ     = f"select count(*) from {TABLE} where ( `used` = 1 ) ;"
    DB     . Query             ( QQ                                          )
    ONE    = DB . FetchOne     (                                             )
    ##########################################################################
    if                         ( ONE == None                               ) :
      return 0
    ##########################################################################
    if                         ( len ( ONE ) <= 0                          ) :
      return 0
    ##########################################################################
    return ONE                 [ 0                                           ]
  ############################################################################
  def FetchGroupMembersCount             ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountSecond ( DB , RELTAB                       )
  ############################################################################
  def FetchGroupOwnersCount              ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountFirst  ( DB , RELTAB                       )
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    TABLE  = self . Tables          [ "People"                               ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
                 where ( `used` = 1 )
                 order by `id` {ORDER}
                 limit {SID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables     [ "Relation"                                  ]
    ##########################################################################
    if                         ( self . isSubordination ( )                ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                         ( self . isReverse       ( )                ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                     [                                             ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isSearching (       ) ) :
      return self . UUIDs
    ##########################################################################
    if                                      ( self . isOriginal  (       ) ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def FetchSessionInformation             ( self , DB                      ) :
    ##########################################################################
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    self . AppendToolNamingAction (                                          )
    ##########################################################################
    msg  = self . getMenuItem     ( "Search"                                 )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/search.png" )          )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . Search                            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    self . AppendWindowToolSeparatorAction (                                 )
    ##########################################################################
    msg  = self . getMenuItem     ( "Galleries"                              )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/galleries.png" )       )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenPersonalGalleries             )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "PersonalGallery"                        )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/gallery.png" )         )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenPersonalGallery               )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "Videos"                                 )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/video.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenPeopleVideos                  )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    A    = QAction                (                                          )
    A    . setSeparator           ( True                                     )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "BodyShapes"                             )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/android.png" )         )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . DoOpenBodyShape                   )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    A    = QAction                (                                          )
    A    . setSeparator           ( True                                     )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "IdentWebPage"                           )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/webfind.png" )         )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenIdentifierWebPages            )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Load"       , self . AppendingPeople , Enabled      )
    self . LinkAction ( "Import"     , self . ImportPeople    , Enabled      )
    self . LinkAction ( "Export"     , self . ExportSameNames , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenamePeople    , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Cut"        , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyItems       , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    self . LinkAction ( "Search"     , self . Search          , Enabled      )
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
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
    self . LinkVoice         ( self . CommandParser                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . LinkVoice         ( None                                          )
    self . defaultCloseEvent ( event                                         )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "people/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
    ##########################################################################
    return self . CreateDragMime ( self , mtype , message                    )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes     ( self , mime                                   ) :
    ##########################################################################
    formats = "people/uuids;picture/uuids;face/uuids"
    ##########################################################################
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                       ( self                                 , \
                                      sourceWidget                         , \
                                      mimeData                             , \
                                      mousePos                             ) :
    ##########################################################################
    RDN     = self . RegularDropNew ( mimeData                               )
    if                              ( not RDN                              ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON     [ "Mime"                                 ]
    UUIDs   = self . DropInJSON     [ "UUIDs"                                ]
    ##########################################################################
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        FMT = self . getMenuItem    ( "Moving"                               )
        MSG = FMT  . format         ( CNT                                    )
      else                                                                   :
        FMT = self . getMenuItem    ( "Copying"                              )
        MSG = FMT  . format         ( title , CNT                            )
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        return False
      ########################################################################
      FMT   = self . getMenuItem    ( "GetPictures"                          )
      MSG   = FMT  . format         ( title , CNT                            )
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "face/uuids" ]            ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        return False
      ########################################################################
      FMT   = self . getMenuItem    ( "GetFaces"                             )
      MSG   = FMT  . format         ( title , CNT                            )
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople                   ( self , source , pos , JSOX            ) :
    ##########################################################################
    ATID , NAME = self . itemAtPos ( pos                                     )
    ##########################################################################
    ## 在內部移動
    ##########################################################################
    if                             ( self == source                        ) :
      ########################################################################
      self . Go ( self . PeopleMoving    , ( ATID , NAME , JSOX , )          )
      ########################################################################
      return True
    ##########################################################################
    ## 從外部加入
    ##########################################################################
    self   . Go ( self . PeopleAppending , ( ATID , NAME , JSOX , )          )
    ##########################################################################
    return True
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures                 ( self , source , pos , JSON            ) :
    ##########################################################################
    PUID , NAME = self . itemAtPos ( pos                                     )
    if                             ( int ( PUID ) <= 0                     ) :
      return True
    ##########################################################################
    self . Go ( self . PicturesAppending , ( PUID , NAME , JSON , )          )
    ##########################################################################
    return True
  ############################################################################
  def acceptFacesDrop          ( self                                      ) :
    return True
  ############################################################################
  def dropFaces                    ( self , source , pos , JSON            ) :
    ##########################################################################
    PUID , NAME = self . itemAtPos ( pos                                     )
    if                             ( int ( PUID ) <= 0                     ) :
      return True
    ##########################################################################
    self . Go ( self . FacesAppending , ( PUID , NAME , JSON , )             )
    ##########################################################################
    return True
  ############################################################################
  def GetLastestPosition                  ( self , DB , LUID               ) :
    return self . GetGroupLastestPosition ( DB , "RelationPeople" , LUID     )
  ############################################################################
  def GenerateMovingSQL                  ( self , LAST , UUIDs             ) :
    return self . GenerateGroupMovingSQL ( "RelationPeople" , LAST , UUIDs   )
  ############################################################################
  def PeopleMoving            ( self , atUuid , NAME , JSON                ) :
    ##########################################################################
    UUIDs  = JSON             [ "UUIDs"                                      ]
    if                        ( len ( UUIDs ) <= 0                         ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    RELTAB = self . Tables    [ "RelationPeople"                             ]
    DB     . LockWrites       ( [ RELTAB                                   ] )
    ##########################################################################
    OPTS   = f"order by `position` asc"
    PUIDs  = self . Relation . Subordination ( DB , RELTAB , OPTS            )
    ##########################################################################
    LUID   = PUIDs            [ -1                                           ]
    LAST   = self . GetLastestPosition ( DB     , LUID                       )
    PUIDs  = self . OrderingPUIDs      ( atUuid , UUIDs , PUIDs              )
    SQLs   = self . GenerateMovingSQL  ( LAST   , PUIDs                      )
    self   . ExecuteSqlCommands ( "OrganizePeople" , DB , SQLs , 100         )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def PeopleAppending          ( self , atUuid , NAME , JSON               ) :
    ##########################################################################
    UUIDs  = JSON              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ "RelationPeople"                            ]
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    self   . Relation  . Joins ( DB , RELTAB , UUIDs                         )
    OPTS   = f"order by `position` asc"
    PUIDs  = self . Relation . Subordination ( DB , RELTAB , OPTS            )
    ##########################################################################
    LUID   = PUIDs             [ -1                                          ]
    LAST   = self . GetLastestPosition ( DB     , LUID                       )
    PUIDs  = self . OrderingPUIDs      ( atUuid , UUIDs , PUIDs              )
    SQLs   = self . GenerateMovingSQL  ( LAST   , PUIDs                      )
    self   . ExecuteSqlCommands ( "OrganizePeople" , DB , SQLs , 100         )
    ##########################################################################
    DB     . UnlockTables      (                                             )
    self   . setVacancy        (                                             )
    self   . GoRelax . emit    (                                             )
    DB     . Close             (                                             )
    ##########################################################################
    self   . loading           (                                             )
    ##########################################################################
    return
  ############################################################################
  def PicturesAppending            ( self , atUuid , NAME , JSON           ) :
    ##########################################################################
    T1  = "People"
    TAB = "RelationPeople"
    ##########################################################################
    OK  = self . AppendingPictures (        atUuid , NAME , JSON , TAB , T1  )
    if                             ( not OK                                ) :
      return
    ##########################################################################
    self   . loading               (                                         )
    ##########################################################################
    return
  ############################################################################
  def FacesAppending           ( self , atUuid , NAME , JSON               ) :
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
    FRNTAB = self . Tables     [ "FaceRegions"                               ]
    FRXTAB = self . Tables     [ "FaceRecognitions"                          ]
    ##########################################################################
    DB     . LockWrites        ( [ FRNTAB , FRXTAB                         ] )
    ##########################################################################
    UXIDs  =                   [                                             ]
    for UUID in UUIDs                                                        :
      UXIDs . append           ( f"{UUID}"                                   )
    UXIDX  = " , " . join      ( UXIDs                                       )
    ##########################################################################
    QQ     = f"""update {FRNTAB}
                 set `owner` = {atUuid}
                 where ( `uuid` in ( {UXIDX} ) ) ;"""
    ##########################################################################
    QQ     = " " . join        ( QQ . split ( )                              )
    DB     . Query             ( QQ                                          )
    ##########################################################################
    QQ     = f"""update {FRXTAB}
                 set `owner` = {atUuid}
                 where ( `face` in ( {UXIDX} ) ) ;"""
    ##########################################################################
    QQ     = " " . join        ( QQ . split ( )                              )
    DB     . Query             ( QQ                                          )
    ##########################################################################
    DB     . UnlockTables      (                                             )
    self   . setVacancy        (                                             )
    self   . GoRelax . emit    (                                             )
    DB     . Close             (                                             )
    ##########################################################################
    self   . Notify            ( 5                                           )
    ##########################################################################
    return
  ############################################################################
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( "ContiguousSelection"                       )
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def looking             ( self , name                                    ) :
    ##########################################################################
    self . SearchingForT2 ( name , "People" , "Names"                        )
    ##########################################################################
    return
  ############################################################################
  def CopyItems                    ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PasteItems                   ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def RenamePeople    ( self                                               ) :
    ##########################################################################
    self . RenameItem (                                                      )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                     ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    SQLs   =                          [                                      ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . Relation . set           ( "second" , UUID                      )
      QQ   = self . Relation . Delete ( RELTAB                               )
      SQLs . append                   ( QQ                                   )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    self   . setBustle                (                                      )
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    TITLE  = "RemovePeopleItems"
    self   . ExecuteSqlCommands       ( TITLE , DB , SQLs , 100              )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    self   . setVacancy               (                                      )
    self   . GoRelax . emit           (                                      )
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    self   . loading                  (                                      )
    ##########################################################################
    return
  ############################################################################
  def AppendItemName                     ( self , item , name              ) :
    ##########################################################################
    DB       = self . ConnectDB          ( UsePure = True                    )
    if                                   ( self . NotOkay ( DB )           ) :
      return
    ##########################################################################
    uuid     = item . data               ( Qt . UserRole                     )
    uuid     = int                       ( uuid                              )
    ##########################################################################
    PHID     = 1400000000000000000
    if                                   ( "Heading" in self . Tables      ) :
      ########################################################################
      PHID   = self . Tables             [ "Heading"                         ]
      PHID   = int                       ( PHID                              )
    ##########################################################################
    PEOTAB   = self . Tables             [ "People"                          ]
    NAMTAB   = self . Tables             [ "NamesEditing"                    ]
    RELTAB   = self . Tables             [ "RelationPeople"                  ]
    TABLES   =                           [ PEOTAB , NAMTAB                   ]
    ##########################################################################
    if                                   (  self . isGrouping ( )          ) :
      TABLES . append                    ( RELTAB                            )
      T1     = self . Relation . get     ( "t1"                              )
      T2     = self . Relation . get     ( "t2"                              )
      RR     = self . Relation . get     ( "relation"                        )
    ##########################################################################
    DB       . LockWrites                ( TABLES                            )
    ##########################################################################
    if                                   ( uuid <= 0                       ) :
      ########################################################################
      PI     = PeopleItem                (                                   )
      PI     . Settings [ "Head"   ] = PHID
      PI     . Tables   [ "People" ] = PEOTAB
      ########################################################################
      uuid   = PI . NewPeople            ( DB                                )
    ##########################################################################
    REL      = Relation                  (                                   )
    REL      . set                       ( "relation" , RR                   )
    ##########################################################################
    if                                   ( self . isSubordination ( )      ) :
      ########################################################################
      PUID   = self . Relation . get     ( "first"                           )
      REL    . set                       ( "first"    , PUID                 )
      REL    . set                       ( "second"   , uuid                 )
      REL    . set                       ( "t1"       , T1                   )
      REL    . setT2                     ( "People"                          )
      REL    . Join                      ( DB , RELTAB                       )
      ########################################################################
    elif                                 ( self . isReverse       ( )      ) :
      ########################################################################
      PUID   = self . Relation . get     ( "second"                          )
      REL    . set                       ( "first"    , uuid                 )
      REL    . set                       ( "second"   , PUID                 )
      REL    . setT1                     ( "People"                          )
      REL    . set                       ( "t2"       , T2                   )
      REL    . Join                      ( DB , RELTAB                       )
    ##########################################################################
    self     . AssureUuidNameByLocality  ( DB                              , \
                                           NAMTAB                          , \
                                           uuid                            , \
                                           name                            , \
                                           self . getLocality ( )            )
    ##########################################################################
    DB       . UnlockTables              (                                   )
    DB       . Close                     (                                   )
    ##########################################################################
    self     . PrepareItemContent        ( item , uuid , name                )
    self     . assignToolTip             ( item , str ( uuid )               )
    ##########################################################################
    return
  ############################################################################
  def ListAllNames                  ( self                                 ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def JoiningPeople            ( self , UUIDs                              ) :
    ##########################################################################
    if                         ( len ( UUIDs ) <= 0                        ) :
      return
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ "RelationPeople"                            ]
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    self   . Relation  . Joins ( DB , RELTAB , UUIDs                         )
    ##########################################################################
    DB     . UnlockTables      (                                             )
    self   . setVacancy        (                                             )
    self   . GoRelax . emit    (                                             )
    DB     . Close             (                                             )
    ##########################################################################
    self   . loading           (                                             )
    ##########################################################################
    return
  ############################################################################
  def JoinPeopleFromFile             ( self , Filename                     ) :
    ##########################################################################
    UUIDs = self . LoadUuidsFromFile (        Filename                       )
    ##########################################################################
    if                               ( len ( UUIDs ) <= 0                  ) :
      return
    ##########################################################################
    self  . JoiningPeople            ( UUIDs                                 )
    ##########################################################################
    return
  ############################################################################
  def AppendingPeople             ( self                                   ) :
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
    VAL      =                    ( Name ,                                   )
    self     . Go                 ( self . JoinPeopleFromFile , VAL          )
    ##########################################################################
    return
  ############################################################################
  def ImportPeople                  ( self                                 ) :
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
    VAL      =                    ( Name ,                                   )
    self     . Go                 ( self . ImportPeopleFromFile , VAL        )
    ##########################################################################
    return
  ############################################################################
  def ImportPeopleFromFile           ( self , Filename                     ) :
    ##########################################################################
    UUIDs = self . LoadUuidsFromFile (        Filename                       )
    ##########################################################################
    if                               ( len ( UUIDs ) <= 0                  ) :
      return False
    ##########################################################################
    self  . SearchKey = ""
    self  . UUIDs     = UUIDs
    self  . Grouping  = "Searching"
    ##########################################################################
    self  . loading                  (                                       )
    ##########################################################################
    return True
  ############################################################################
  def ImportPeopleFromClipboard         ( self                             ) :
    ##########################################################################
    BODY  = qApp . clipboard ( ) . text (                                    )
    UUIDs = self . GetUuidsFromText     ( BODY                               )
    ##########################################################################
    if                                  ( len ( UUIDs ) <= 0               ) :
      return False
    ##########################################################################
    self  . SearchKey = ""
    self  . UUIDs     = UUIDs
    self  . Grouping  = "Searching"
    ##########################################################################
    self  . loading                     (                                    )
    ##########################################################################
    return True
  ############################################################################
  def ExportSameNames              ( self                                  ) :
    ##########################################################################
    self . Go                      ( self . ExportSameNamesListings          )
    ##########################################################################
    return
  ############################################################################
  def ExportSameNamesListings      ( self                                  ) :
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    NAMTAB = self . Tables         [ "Names"                                 ]
    RELTAB = self . Tables         [ "Relation"                              ]
    ##########################################################################
    UUID   = self . Relation . get ( "first"                                 )
    T1     = self . Relation . get ( "t1"                                    )
    T2     = self . Relation . get ( "t2"                                    )
    REL    = self . Relation . get ( "relation"                              )
    ##########################################################################
    LISTS  =                       [                                         ]
    FF     = f"""select `second` from {RELTAB}
                 where ( `first` = {UUID} )
                 and ( `t1` = {T1} )
                 and ( `t2` = {T2} )
                 and ( `relation` = {REL} )"""
    QQ     = f"""select `uuid`,`name` from {NAMTAB}
                 where ( `uuid` in ( {FF} ) )
                 and ( `relevance` = 0 )
                 order by `name` asc , `uuid` asc ;"""
    QQ     = " " . join            ( QQ . split ( )                          )
    DB     . Query                 ( QQ                                      )
    ALL    = DB . FetchAll         (                                         )
    TOTAL  = len                   ( ALL                                     )
    PREV   = 0
    AT     = 1
    CC     = False
    ##########################################################################
    PVID   = ALL                   [ PREV ] [ 0                              ]
    NAME   = ALL                   [ PREV ] [ 1                              ]
    ##########################################################################
    while                          ( AT < TOTAL                            ) :
      ########################################################################
      U    = ALL                   [ AT ] [ 0                                ]
      N    = ALL                   [ AT ] [ 1                                ]
      ########################################################################
      if                           ( ( N == NAME ) and ( PVID != U )       ) :
        ######################################################################
        if                         ( not CC                                ) :
          ####################################################################
          CC = True
          L  = f"{PVID}"
          LISTS . append ( L )
        ######################################################################
        L  = f"{U}"
        LISTS . append ( L )
        ######################################################################
      else                                                                   :
        ######################################################################
        CC   = False
        NAME = N
      ########################################################################
      PVID = U
      AT   = AT + 1
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    if                                ( len ( LISTS ) > 0                  ) :
      ########################################################################
      NOTE = "\n" . join              ( LISTS                                )
      self . emitOpenSmartNote . emit ( NOTE                                 )
    ##########################################################################
    return
  ############################################################################
  def SearchForSameNames           ( self                                  ) :
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    NAMTAB = self . Tables         [ "Names"                                 ]
    RELTAB = self . Tables         [ "Relation"                              ]
    ##########################################################################
    UUID   = self . Relation . get ( "first"                                 )
    T1     = self . Relation . get ( "t1"                                    )
    T2     = self . Relation . get ( "t2"                                    )
    REL    = self . Relation . get ( "relation"                              )
    ##########################################################################
    LISTS  =                       [                                         ]
    FF     = f"""select `second` from {RELTAB}
                 where ( `first` = {UUID} )
                 and ( `t1` = {T1} )
                 and ( `t2` = {T2} )
                 and ( `relation` = {REL} )"""
    QQ     = f"""select `uuid`,`name` from {NAMTAB}
                 where ( `uuid` in ( {FF} ) )
                 and ( `relevance` = 0 )
                 order by `name` asc , `uuid` asc ;"""
    QQ     = " " . join            ( QQ . split ( )                          )
    DB     . Query                 ( QQ                                      )
    ALL    = DB . FetchAll         (                                         )
    TOTAL  = len                   ( ALL                                     )
    PREV   = 0
    AT     = 1
    CC     = False
    ##########################################################################
    PVID   = ALL                   [ PREV ] [ 0                              ]
    NAME   = ALL                   [ PREV ] [ 1                              ]
    ##########################################################################
    while                          ( AT < TOTAL                            ) :
      ########################################################################
      U    = ALL                   [ AT ] [ 0                                ]
      N    = ALL                   [ AT ] [ 1                                ]
      ########################################################################
      if                           ( ( N == NAME ) and ( PVID != U )       ) :
        ######################################################################
        if                         ( not CC                                ) :
          ####################################################################
          CC = True
          L  = f"{PVID} {NAME}"
          LISTS . append ( L )
        ######################################################################
        L  = f"{U} {NAME}"
        LISTS . append ( L )
        ######################################################################
      else                                                                   :
        ######################################################################
        CC   = False
        NAME = N
      ########################################################################
      PVID = U
      AT   = AT + 1
    ##########################################################################
    DB     . Close                    (                                      )
    ##########################################################################
    if                                ( len ( LISTS ) > 0                  ) :
      ########################################################################
      NOTE = "\n" . join              ( LISTS                                )
      self . emitOpenSmartNote . emit ( NOTE                                 )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage          ( self                                  ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
      self . emitRestart . emit    (                                         )
      return False
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( self . NotOkay ( DB )                 ) :
      return False
    ##########################################################################
    PAMTAB = self . Tables         [ "Parameters"                            ]
    DB     . LockWrites            ( [ PAMTAB ]                              )
    ##########################################################################
    if                             ( self . isSubordination ( )            ) :
      ########################################################################
      TYPE = self . Relation . get ( "t1"                                    )
      UUID = self . Relation . get ( "first"                                 )
      ########################################################################
    elif                           ( self . isReverse       ( )            ) :
      ########################################################################
      TYPE = self . Relation . get ( "t2"                                    )
      UUID = self . Relation . get ( "second"                                )
    ##########################################################################
    SCOPE  = self . Grouping
    SCOPE  = f"PeopleView-{SCOPE}"
    self   . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
    DB     . UnlockTables          (                                         )
    DB     . Close                 (                                         )
    self   . emitRestart . emit    (                                         )
    ##########################################################################
    return True
  ############################################################################
  def ReloadLocality               ( self , DB                             ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
      return
    ##########################################################################
    PAMTAB = self . Tables         [ "Parameters"                            ]
    ##########################################################################
    if                             ( self . isSubordination ( )            ) :
      ########################################################################
      TYPE = self . Relation . get ( "t1"                                    )
      UUID = self . Relation . get ( "first"                                 )
      ########################################################################
    elif                            ( self . isReverse       ( )           ) :
      ########################################################################
      TYPE = self . Relation . get ( "t2"                                    )
      UUID = self . Relation . get ( "second"                                )
    ##########################################################################
    SCOPE  = self . Grouping
    SCOPE  = f"PeopleView-{SCOPE}"
    self   . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
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
    return          { "Match" : False                                        }
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def OpenIdentifierWebPages        ( self                                 ) :
    ##########################################################################
    atItem = self . currentItem     (                                        )
    if                              ( self . NotOkay ( atItem )            ) :
      return
    ##########################################################################
    uuid   = atItem . data          ( Qt . UserRole                          )
    uuid   = int                    ( uuid                                   )
    self   . OpenWebPageBelongings  ( uuid , atItem , "Equivalent"           )
    ##########################################################################
    return
  ############################################################################
  def OpenPeopleVideos              ( self                                 ) :
    ##########################################################################
    atItem = self . currentItem     (                                        )
    if                              ( self . NotOkay ( atItem )            ) :
      return
    ##########################################################################
    uuid   = atItem . data          ( Qt . UserRole                          )
    uuid   = int                    ( uuid                                   )
    text   = atItem . text          (                                        )
    icon   = atItem . icon          (                                        )
    xsid   = str                    ( uuid                                   )
    ##########################################################################
    self   . ShowVideoAlbums . emit ( text , 7 , xsid , icon                 )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , "People" , "NamesEditing"     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemGalleries         ( self , item                              ) :
    ##########################################################################
    uuid = item . data          ( Qt . UserRole                              )
    uuid = int                  ( uuid                                       )
    text = item . text          (                                            )
    icon = item . icon          (                                            )
    xsid = str                  ( uuid                                       )
    ##########################################################################
    self . ShowGalleries . emit ( text , 7 , xsid , icon                     )
    ##########################################################################
    return
  ############################################################################
  def OpenPersonalGalleries     ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self . OpenItemGalleries    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenGalleryItem                 ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( Qt . UserRole                        )
    uuid = int                        ( uuid                                 )
    text = item . text                (                                      )
    icon = item . icon                (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    self . ShowPersonalGallery . emit ( text , 7 , xsid , icon               )
    ##########################################################################
    return
  ############################################################################
  def OpenPersonalGallery       ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenGalleryItem    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def DoOpenBodyShape             ( self                                   ) :
    ##########################################################################
    atItem = self . currentItem   (                                          )
    ##########################################################################
    if                            ( self . NotOkay ( atItem )              ) :
      return
    ##########################################################################
    uuid   = atItem . data        ( Qt . UserRole                            )
    uuid   = int                  ( uuid                                     )
    text   = atItem . text        (                                          )
    xsid   = str                  ( uuid                                     )
    ##########################################################################
    self   . OpenBodyShape . emit ( text , xsid , { }                        )
    ##########################################################################
    return
  ############################################################################
  def OpenWebPageListings          ( self , Related                        ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
      return
    ##########################################################################
    text   = self . windowTitle    (                                         )
    icon   = self . windowIcon     (                                         )
    ##########################################################################
    if                             ( self . isSubordination ( )            ) :
      Typi = self . Relation . get ( "t1"                                    )
      uuid = self . Relation . get ( "first"                                 )
    elif                           ( self . isReverse       ( )            ) :
      Typi = self . Relation . get ( "t2"                                    )
      uuid = self . Relation . get ( "second"                                )
    ##########################################################################
    Typi   = int                   ( Typi                                    )
    uuid   = int                   ( uuid                                    )
    xsid   = str                   ( uuid                                    )
    ##########################################################################
    self   . ShowWebPages . emit   ( text , Typi , xsid , Related , icon     )
    ##########################################################################
    return
  ############################################################################
  def OpenWebPageBelongings    ( self , uuid , item , Related              ) :
    ##########################################################################
    text = item . text         (                                             )
    icon = item . icon         (                                             )
    ##########################################################################
    uuid = int                 ( uuid                                        )
    xsid = str                 ( uuid                                        )
    ##########################################################################
    self . ShowWebPages . emit ( text , 7 , xsid , Related , icon            )
    ##########################################################################
    return
  ############################################################################
  def IndexingMenu               ( self , mm , menu , uuid , item          ) :
    ##########################################################################
    MSG = self . getMenuItem     ( "Indexing"                                )
    LOM = mm   . addMenuFromMenu ( menu , MSG                                )
    ##########################################################################
    msg = self . getMenuItem     ( "AppendLists"                             )
    mm  . addActionFromMenu      ( LOM , 25355001 , msg                      )
    ##########################################################################
    mm  . addSeparatorFromMenu   ( LOM                                       )
    ##########################################################################
    msg = self . getMenuItem     ( "ImportLists"                             )
    mm  . addActionFromMenu      ( LOM , 25355002 , msg                      )
    ##########################################################################
    msg = self . getMenuItem     ( "ImportListsFromClipboard"                )
    mm  . addActionFromMenu      ( LOM , 25355003 , msg                      )
    ##########################################################################
    mm  . addSeparatorFromMenu   ( LOM                                       )
    ##########################################################################
    msg = self . getMenuItem     ( "ExportSameNames"                         )
    mm  . addActionFromMenu      ( LOM , 25355004 , msg                      )
    ##########################################################################
    msg = self . getMenuItem     ( "AllNames"                                )
    mm  . addActionFromMenu      ( LOM , 25355005 , msg                      )
    ##########################################################################
    mm  . addSeparatorFromMenu   ( LOM                                       )
    ##########################################################################
    msg = self . getMenuItem     ( "LocateSameNames"                         )
    mm  . addActionFromMenu      ( LOM , 25355006 , msg                      )
    ##########################################################################
    return mm
  ############################################################################
  def FunctionsMenu               ( self , mm , uuid , item                ) :
    ##########################################################################
    MSG   = self . getMenuItem    ( "Functions"                              )
    LOM   = mm   . addMenu        ( MSG                                      )
    ##########################################################################
    msg   = self . accessibleName (                                          )
    if                            ( len ( msg ) > 0                        ) :
      mm  . addActionFromMenu     ( LOM , 25351201 , msg                     )
    ##########################################################################
    msg   = self . getMenuItem    ( "AssignAccessibleName"                   )
    mm    . addActionFromMenu     ( LOM , 25351202 , msg                     )
    ##########################################################################
    msg   = self . getMenuItem    ( "Panel"                                  )
    mm    . addActionFromMenu     ( LOM , 25351203 , msg                     )
    ##########################################################################
    if                            ( self . isSubordination ( )             ) :
      ########################################################################
      msg = self . getMenuItem    ( "AssignTables"                           )
      mm  . addActionFromMenu     ( LOM , 25351301 , msg                     )
    ##########################################################################
    mm    = self . IndexingMenu   ( mm , LOM , uuid , item                   )
    ##########################################################################
    mm    . addSeparatorFromMenu  ( LOM                                      )
    ##########################################################################
    MSG   = self . getMenuItem    ( "WebPages"                               )
    mm    . addActionFromMenu     ( LOM , 25351221 , MSG                     )
    ##########################################################################
    MSG   = self . getMenuItem    ( "IdentWebPage"                           )
    mm    . addActionFromMenu     ( LOM , 25351222 , MSG                     )
    ##########################################################################
    return mm
  ############################################################################
  def RunFunctionsMenu                 ( self , at , uuid , item           ) :
    ##########################################################################
    if                                 ( at == 25351202                    ) :
      ########################################################################
      self . ConfigureAccessibleName   (                                     )
      ########################################################################
      return
    ##########################################################################
    if                                 ( at == 25351203                    ) :
      ########################################################################
      ########################################################################
      return
    ##########################################################################
    if                                 ( at == 25351301                    ) :
      ########################################################################
      TITLE = self . windowTitle       (                                     )
      UUID  = self . Relation  . get   ( "first"                             )
      TYPE  = self . Relation  . get   ( "t1"                                )
      TYPE  = int                      ( TYPE                                )
      self  . OpenVariantTables . emit ( str ( TITLE )                     , \
                                         str ( UUID  )                     , \
                                         TYPE                              , \
                                         self . FetchTableKey              , \
                                         self . Tables                       )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355001                    ) :
      ########################################################################
      self . AppendingPeople           (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355002                    ) :
      ########################################################################
      self . ImportPeople              (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355003                    ) :
      ########################################################################
      self . ImportPeopleFromClipboard (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355004                    ) :
      ########################################################################
      self . ExportSameNames           (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355005                    ) :
      ########################################################################
      self . ListAllNames              (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25355006                    ) :
      ########################################################################
      self . Go                        ( self . SearchForSameNames           )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351221                    ) :
      ########################################################################
      self . OpenWebPageListings       ( "Subordination"                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 25351222                    ) :
      ########################################################################
      self . OpenWebPageListings       ( "Equivalent"                        )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def RelatedGalleriesMenu           ( self , mm , Menu                    ) :
    ##########################################################################
    MSG  = self . getMenuItem        ( "RelatedGalleries"                    )
    LOM  = mm   . addMenuFromMenu    ( Menu , MSG                            )
    ##########################################################################
    MSG  = self . getMenuItem        ( "PersonalGallery"                     )
    icon = QIcon                     ( ":/images/gallery.png"                )
    mm   . addActionFromMenuWithIcon ( LOM , 24231311 , icon , MSG           )
    ##########################################################################
    msg  = self . getMenuItem        ( "LOD"                                 )
    mm   . addActionFromMenu         ( LOM , 24231312 , msg                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Icons"                               )
    mm   . addActionFromMenu         ( LOM , 24231313 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Faces"                               )
    mm   . addActionFromMenu         ( LOM , 24231314 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Mouth"                               )
    mm   . addActionFromMenu         ( LOM , 24231315 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Eyes"                                )
    mm   . addActionFromMenu         ( LOM , 24231316 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Iris"                                )
    mm   . addActionFromMenu         ( LOM , 24231317 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Nose"                                )
    mm   . addActionFromMenu         ( LOM , 24231318 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Tits"                                )
    mm   . addActionFromMenu         ( LOM , 24231319 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Umbilicus"                           )
    mm   . addActionFromMenu         ( LOM , 24231320 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Pussy"                               )
    mm   . addActionFromMenu         ( LOM , 24231321 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Asshole"                             )
    mm   . addActionFromMenu         ( LOM , 24231322 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Tattoo"                              )
    mm   . addActionFromMenu         ( LOM , 24231323 , MSG                  )
    ##########################################################################
    MSG  = self . getMenuItem        ( "Texture"                             )
    mm   . addActionFromMenu         ( LOM , 24231324 , MSG                  )
    ##########################################################################
    return mm
  ############################################################################
  def GroupsMenu               ( self , mm , uuid , item                   ) :
    ##########################################################################
    if                         ( uuid <= 0                                 ) :
      return mm
    ##########################################################################
    TRX = self . Translations
    FMT = self . getMenuItem   ( "Belongs"                                   )
    MSG = FMT  . format        ( item . text ( )                             )
    LOM = mm   . addMenu       ( MSG                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "CopyPeopleUuid"                            )
    mm  . addActionFromMenu    ( LOM , 24231101 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "LogHistory"                                )
    mm  . addActionFromMenu    ( LOM , 24231102 , msg                        )
    ##########################################################################
    MSG = self . getMenuItem   ( "Occupations"                               )
    mm  . addActionFromMenu    ( LOM , 24231201 , MSG                        )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    MSG = self . getMenuItem   ( "Galleries"                                 )
    ICO = QIcon                ( ":/images/galleries.png"                    )
    mm  . addActionFromMenuWithIcon   ( LOM , 24231211 , ICO , MSG           )
    ##########################################################################
    mm  = self . RelatedGalleriesMenu ( mm , LOM                             )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    MSG = self . getMenuItem   ( "BodyShapes"                                )
    mm  . addActionFromMenu    ( LOM , 24231351 , MSG                        )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    MSG = self . getMenuItem   ( "Videos"                                    )
    ICO = QIcon                ( ":/images/video.png"                        )
    mm  . addActionFromMenuWithIcon   ( LOM , 24231411 , ICO , MSG           )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    MSG = self . getMenuItem   ( "WebPages"                                  )
    mm  . addActionFromMenu    ( LOM , 24231511 , MSG                        )
    ##########################################################################
    MSG = self . getMenuItem   ( "IdentWebPage"                              )
    mm  . addActionFromMenu    ( LOM , 24231512 , MSG                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                     ( self , at , uuid , item          ) :
    ##########################################################################
    if                                  ( at == 24231101                   ) :
      ########################################################################
      qApp . clipboard ( ). setText     ( f"{uuid}"                          )
      ########################################################################
      return
    ##########################################################################
    if                                  ( at == 24231102                   ) :
      ########################################################################
      t    = item . text                (                                    )
      nx   = ""
      ########################################################################
      if                                ( "Notes" in self . Tables         ) :
        nx = self . Tables              [ "Notes"                            ]
      ########################################################################
      self . OpenLogHistory . emit      ( t                                  ,
                                          str ( uuid )                       ,
                                          "Description"                      ,
                                          nx                                 ,
                                          ""                                 )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231201                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      rela = "Subordination"
      ########################################################################
      self . OwnedOccupation     . emit ( text , 7 , xsid , rela , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231211                   ) :
      ########################################################################
      self . OpenItemGalleries          ( item                               )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231311                   ) :
      ########################################################################
      self . OpenGalleryItem            ( item                               )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231312                   ) :
      ########################################################################
      icon = item . icon                (                                    )
      head = item . text                (                                    )
      xsid = str                        ( uuid                               )
      ########################################################################
      self . ShowLodListings . emit     ( head , str ( uuid ) , icon         )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231313                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Using"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231314                   ) :
      ########################################################################
      text = item . text                (                                    )
      ## icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      ## relz = "Face"
      ########################################################################
      self . ShowPersonalFaces . emit   ( text , xsid                        )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231315                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Mouth"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231316                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Eye"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231317                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Iris"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231318                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Nose"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231319                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Tit"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231320                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Umbilicus"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231321                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Pussy"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231322                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Asshole"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231323                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Tattoo"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231324                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      relz = "Texture"
      ########################################################################
      self . ShowPersonalIcons . emit   ( text , 7 , relz , xsid , icon      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231351                   ) :
      ########################################################################
      text = item . text                (                                    )
      xsid = str                        ( uuid                               )
      ########################################################################
      self . OpenBodyShape . emit       ( text , xsid , { }                  )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231411                   ) :
      ########################################################################
      text = item . text                (                                    )
      icon = item . icon                (                                    )
      xsid = str                        ( uuid                               )
      ########################################################################
      self . ShowVideoAlbums . emit     ( text , 7 , xsid , icon             )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231511                   ) :
      ########################################################################
      self . OpenWebPageBelongings      ( uuid , item , "Subordination"      )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231512                   ) :
      ########################################################################
      self . OpenWebPageBelongings      ( uuid , item , "Equivalent"         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager               ( self                                )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                                 ( self . isSearching ( )            ) :
      ########################################################################
      msg  = self . getMenuItem        ( "NotSearch"                         )
      mm   . addAction                 ( 7401 , msg                          )
    ##########################################################################
    self   . StopIconMenu              ( mm                                  )
    self   . AmountIndexMenu           ( mm                                  )
    self   . AppendRefreshAction       ( mm , 1001                           )
    self   . AppendInsertAction        ( mm , 1101                           )
    self   . AppendSearchAction        ( mm , 1102                           )
    ##########################################################################
    if                                 ( len ( items ) > 0                 ) :
      self . AppendDeleteAction        ( mm , 1103                           )
    ##########################################################################
    if                                 ( uuid > 0                          ) :
      self . AppendRenameAction        ( mm , 1104                           )
      self . AssureEditNamesAction     ( mm , 1601 , atItem                  )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . FunctionsMenu             ( mm , uuid , atItem                  )
    self   . GroupsMenu                ( mm , uuid , atItem                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu (                                     )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu   ( at , uuid , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu      ( at , uuid , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunStopIconMenu    ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1101                        ) :
      ########################################################################
      self . InsertItem                (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1102                        ) :
      self . Search                    (                                     )
      return True
    ##########################################################################
    if                                 ( at == 1103                        ) :
      ########################################################################
      self . DeleteItems               (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1104                        ) :
      ########################################################################
      self . RenamePeople              (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 7401                        ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
