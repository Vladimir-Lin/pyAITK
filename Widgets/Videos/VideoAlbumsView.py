# -*- coding: utf-8 -*-
##############################################################################
## VideoAlbumsView
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import glob
import shutil
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
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . Pictures   . Picture   import Picture     as PictureItem
from   AITK  . People     . People    import People      as PeopleItem
from   AITK  . Videos     . Album     import Album       as AlbumItem
##############################################################################
class VideoAlbumsView              ( IconDock                              ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  OwnedPeopleGroup    = pyqtSignal ( str , int , str                         )
  ShowPersonalGallery = pyqtSignal ( str , int , str , QIcon                 )
  GalleryGroup        = pyqtSignal ( str , int , str                         )
  ShowWebPages        = pyqtSignal ( str , int , str , str , QIcon           )
  OpenVariantTables   = pyqtSignal ( str , str , int , str , dict            )
  emitOpenSmartNote   = pyqtSignal ( str                                     )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 60
    self . SortOrder          = "asc"
    self . ShowIdentifier     = False
    self . FetchTableKey      = "VideoAlbums"
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
    self . Relation . setT2        ( "Album"                                 )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . setDragEnabled          ( True                                    )
    self . setAcceptDrops          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def AttachActions   ( self         ,                       Enabled       ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup      , Enabled         )
    self . LinkAction ( "Insert"     , self . InsertItem   , Enabled         )
    self . LinkAction ( "Rename"     , self . RenameVideo  , Enabled         )
    self . LinkAction ( "Delete"     , self . DeleteItems  , Enabled         )
    self . LinkAction ( "Cut"        , self . DeleteItems  , Enabled         )
    self . LinkAction ( "Copy"       , self . CopyItems    , Enabled         )
    self . LinkAction ( "Paste"      , self . PasteItems   , Enabled         )
    self . LinkAction ( "Search"     , self . Search       , Enabled         )
    self . LinkAction ( "Home"       , self . PageHome     , Enabled         )
    self . LinkAction ( "End"        , self . PageEnd      , Enabled         )
    self . LinkAction ( "PageUp"     , self . PageUp       , Enabled         )
    self . LinkAction ( "PageDown"   , self . PageDown     , Enabled         )
    self . LinkAction ( "SelectAll"  , self . SelectAll    , Enabled         )
    self . LinkAction ( "SelectNone" , self . SelectNone   , Enabled         )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label"      , self . windowTitle ( )         )
    self . AttachActions     ( True                                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def GetUuidIcon                    ( self , DB , UUID                    ) :
    ##########################################################################
    RELTAB = self . Tables           [ "Relation"                            ]
    ##########################################################################
    return self . defaultGetUuidIcon ( DB , RELTAB , "Album" , UUID          )
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "Albums"                                    ]
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
    TABLE  = self . Tables          [ "Albums"                               ]
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
  def ObtainSubgroupUuids                    ( self , DB                   ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder          (                               )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables                   [ "Relation"                    ]
    ##########################################################################
    if                                       ( self . isSubordination ( )  ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                                       ( self . isReverse       ( )  ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                                   [                               ]
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
  def ObtainsUuidNames                 ( self , DB , UUIDs                 ) :
    ##########################################################################
    NAMEs     =                        {                                     }
    ##########################################################################
    if                                 ( len ( UUIDs ) > 0                 ) :
      ########################################################################
      TABLE   = self . Tables          [ "Names"                             ]
      NAMEs   = self . GetNames        ( DB , TABLE , UUIDs                  )
    ##########################################################################
    if                                 ( self . ShowIdentifier             ) :
      ########################################################################
      NKs     =                        {                                     }
      ALBUM   = AlbumItem              (                                     )
      ALBUM   . Settings = self . Settings
      ALBUM   . Tables   = self . Tables
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        N     = NAMEs                  [ UUID                                ]
        ALBUM . Uuid = UUID
        IDs   = ALBUM . GetIdentifiers ( DB                                  )
        ######################################################################
        if                             ( len ( IDs ) > 0                   ) :
          ####################################################################
          ID  = " , " . join           ( IDs                                 )
          ####################################################################
          if                           ( len ( ID ) > 0                    ) :
            ##################################################################
            if                         ( len ( IDs ) == 1                  ) :
              ################################################################
              N = f"[{ID}] {N}"
              ################################################################
            elif                       ( len ( ID ) > 1                    ) :
              ################################################################
              N = f"[ {ID} ] {N}"
        ######################################################################
        NKs [ UUID ] = N
      ########################################################################
      NAMEs   = NKs
    ##########################################################################
    return NAMEs
  ############################################################################
  def FetchSessionInformation             ( self , DB                      ) :
    ##########################################################################
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "album/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
    ##########################################################################
    return self . CreateDragMime ( self , 0 , mtype , message                )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "album/uuids;people/uuids;picture/uuids"
    return self . MimeType    ( mime , formats                               )
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
        MSG = f"移動{CNT}個人物"
      else                                                                   :
        MSG = f"從「{title}」複製{CNT}個人物"
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        MSG = f"移動{CNT}張圖片"
      else                                                                   :
        MSG = f"從「{title}」複製{CNT}張圖片"
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    if                         ( sourceWidget != self                      ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    if                         ( atItem is None                            ) :
      return False
    if                         ( atItem . isSelected ( )                   ) :
      return False
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople               ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("PeopleView::dropPeople")
    print(JSOX)
    if ( atItem is not None ) :
      print("TO:",atItem.text())
    ##########################################################################
    return True
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures             ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("PeopleView::dropPictures")
    print(JSOX)
    if ( atItem is not None ) :
      print("TO:",atItem.text())
    ##########################################################################
    return True
  ############################################################################
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( "ContiguousSelection"                       )
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def singleClicked                ( self , item                           ) :
    ##########################################################################
    self . Notify                  ( 0                                       )
    ##########################################################################
    return True
  ############################################################################
  def doubleClicked                ( self , item                           ) :
    ##########################################################################
    ##########################################################################
    return True
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
  def RenameVideo     ( self                                               ) :
    ##########################################################################
    self . RenameItem (                                                      )
    ##########################################################################
    return
  ############################################################################
  def BuildAlbum                 ( self , templDIR , path                  ) :
    ##########################################################################
    shutil     . copytree        ( DIR , path                                )
    ##########################################################################
    VIDPATH    = f"{path}/videos"
    TAILs      =                 [ "*.mp4"                                 , \
                                   "*.mkv"                                 , \
                                   "*.avi"                                 , \
                                   "*.wmv"                                 , \
                                   "*.vob"                                 , \
                                   "*.rmvb"                                  ]
    ##########################################################################
    for suffix in TAILs                                                      :
      ########################################################################
      for file in glob . glob    ( f"{path}/{suffix}"                      ) :
        shutil . move            ( file , VIDPATH                            )
    ##########################################################################
    return
  ############################################################################
  def GenerateVideoAlbum         ( self , uuid , path                      ) :
    ##########################################################################
    CONFs     = self . Settings  [ "Albums"                                  ]
    DIR       = CONFs            [ "Template"                                ]
    ##########################################################################
    ALBUM     = AlbumItem        (                                           )
    ALBUM     . Uuid     = uuid
    ALBUM     . Settings = self . Settings
    ALBUM     . Tables   = self . Tables
    ##########################################################################
    self      . BuildAlbum       ( DIR , path                                )
    ##########################################################################
    DB        = self . ConnectDB ( UsePure = True                            )
    if                           ( self . NotOkay ( DB )                   ) :
      return
    ##########################################################################
    print(uuid,path)
    print(json.dumps(CONFs))
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    DB        . Close            (                                           )
    ##########################################################################
    self      . Notify           ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def CreateAlbum               ( self , VIDEO                             ) :
    ##########################################################################
    MSG    = self . getMenuItem ( "CreateAlbum"                              )
    path   = QFileDialog . getExistingDirectory                            ( \
                                  self                                     , \
                                  MSG                                      , \
                                  ""                                       , \
                                  QFileDialog . ShowDirsOnly               | \
                                  QFileDialog . DontResolveSymlinks          )
    if                          ( not path                                 ) :
      return
    ##########################################################################
    PARAMs =                    ( VIDEO , path ,                             )
    self . Go                   ( self . GenerateVideoAlbum , PARAMs         )
    ##########################################################################
    return
  ############################################################################
  def UpdateVideoAlbum          ( self , uuid , path                       ) :
    ##########################################################################
    CONFs     = self . Settings  [ "Albums"                                  ]
    DIR       = CONFs            [ "Template"                                ]
    ##########################################################################
    ALBUM     = AlbumItem        (                                           )
    ALBUM     . Uuid     = uuid
    ALBUM     . Settings = self . Settings
    ALBUM     . Tables   = self . Tables
    ##########################################################################
    DB        = self . ConnectDB ( UsePure = True                            )
    if                           ( self . NotOkay ( DB )                   ) :
      return
    ##########################################################################
    print(uuid,path)
    print(json.dumps(CONFs))
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    DB        . Close            (                                           )
    ##########################################################################
    self      . Notify           ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def UpdateAlbum               ( self , VIDEO                             ) :
    ##########################################################################
    MSG    = self . getMenuItem ( "UpdateAlbum"                              )
    path   = QFileDialog . getExistingDirectory                            ( \
                                  self                                     , \
                                  MSG                                      , \
                                  ""                                       , \
                                  QFileDialog . ShowDirsOnly               | \
                                  QFileDialog . DontResolveSymlinks          )
    if                          ( not path                                 ) :
      return
    ##########################################################################
    PARAMs =                    ( VIDEO , path ,                             )
    self . Go                   ( self . UpdateVideoAlbum , PARAMs           )
    ##########################################################################
    return
  ############################################################################
  def looking             ( self , name                                    ) :
    ##########################################################################
    self . SearchingForT2 ( name , "Albums" , "Names"                        )
    ##########################################################################
    return
  ############################################################################
  def FindProducts                    ( self , name                        ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    FMT     = self . Translations     [ "UI::SearchKey"                      ]
    MSG     = FMT . format            ( name                                 )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    ##########################################################################
    ALMTAB  = self . Tables           [ "Albums"                             ]
    IDFTAB  = self . Tables           [ "Identifiers"                        ]
    RELTAB  = self . Tables           [ "Relation"                           ]
    LIKE    = f"{name}"
    UUIDs   =                         [                                      ]
    ##########################################################################
    if                                ( self . isOriginal      (         ) ) :
      ########################################################################
      PEQ   = f"""select `uuid` from {ALMTAB} where ( `used` > 0 )"""
      ########################################################################
    elif                              ( self . isSubordination (         ) ) :
      ########################################################################
      FIRST = self . Relation . get   ( "first"                              )
      T1    = self . Relation . get   ( "t1"                                 )
      T2    = self . Relation . get   ( "t2"                                 )
      REL   = self . Relation . get   ( "relation"                           )
      ########################################################################
      REQ   = f"""select `second` from {RELTAB}
                  where ( `t1` = {T1} )
                    and ( `t2` = {T2} )
                    and ( `relation` = {REL} )
                    and ( `first` = {FIRST} )"""
      PEQ   = f"""select `uuid` from {ALMTAB}
                  where ( `used` > 0 )
                  and ( `uuid` in ( {REQ} ) )"""
      ########################################################################
    elif                              ( self . isReverse       (         ) ) :
      ########################################################################
      SECID = self . Relation . get   ( "second"                             )
      T1    = self . Relation . get   ( "t1"                                 )
      T2    = self . Relation . get   ( "t2"                                 )
      REL   = self . Relation . get   ( "relation"                           )
      ########################################################################
      REQ   = f"""select `first` from {RELTAB}
                  where ( `t1` = {T1} )
                    and ( `t2` = {T2} )
                    and ( `relation` = {REL} )
                    and ( `second` = {SECID} )"""
      PEQ   = f"""select `uuid` from {ALMTAB}
                  where ( `used` > 0 )
                  and ( `uuid` in ( {REQ} ) )"""
    ##########################################################################
    IDQ     = f"""select `uuid` from {IDFTAB}
                  where ( `type` = 76 )
                    and ( `name` like %s )
                    and ( `uuid` in ( {PEQ} ) )
                  group by `uuid`"""
    QQ      = f"""select `uuid` from {IDFTAB}
                  where ( `uuid` in ( {IDQ} ) )
                  order by `name` asc ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
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
  @pyqtSlot            (                                                     )
  def FindIdentifiers  ( self                                              ) :
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
    self . Go          ( self . FindProducts , ( T , )                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                            (                                     )
  def SearchIdentifier                 ( self                              ) :
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
    L      . editingFinished . connect ( self . FindIdentifiers              )
    L      . blockSignals              ( False                               )
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    MSG    = self . getMenuItem        ( "SearchIdentifier"                  )
    L      . setPlaceholderText        ( MSG                                 )
    L      . setFocus                  ( Qt . TabFocusReason                 )
    ##########################################################################
    self   . SearchLine = L
    ##########################################################################
    return
  ############################################################################
  def ObtainAlbumNames                 ( self , DB , UUIDs                 ) :
    ##########################################################################
    IDFTAB   = self . Tables           [ "Identifiers"                       ]
    NAMTAB   = self . Tables           [ "Names"                             ]
    ##########################################################################
    NAMEs    =                         {                                     }
    if                                 ( len ( UUIDs ) <= 0                ) :
      return NAMEs
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME   = self . GetName          ( DB , NAMTAB , UUID                  )
      ########################################################################
      QQ     = f"""select `name` from {IDFTAB}
                 where ( `type` = 76 )
                 and ( `uuid` = {UUID} ) ;"""
      QQ     = " " . join              ( QQ . split ( )                      )
      DB     . Query                   ( QQ                                  )
      RR     = DB . FetchOne           (                                     )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )          :
        ######################################################################
        IDEF = RR                      [ 0                                   ]
        SS   = ""
        ######################################################################
        try                                                                  :
          SS = IDEF . decode           ( "utf-8"                             )
        except                                                               :
          pass
        ######################################################################
        if                             ( len ( SS ) > 0                    ) :
          NAME = f"{SS} {NAME}"
      ########################################################################
      NAMEs [ UUID ] = NAME
    ##########################################################################
    return NAMEs
  ############################################################################
  def UpdateLocalityUsage          ( self                                  ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
      return False
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( DB == None                            ) :
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
    SCOPE  = f"ViewAlbums-{SCOPE}"
    self   . SetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
    DB     . UnlockTables          (                                         )
    DB     . Close                 (                                         )
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
    SCOPE  = f"ViewAlbums-{SCOPE}"
    self   . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
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
    self . ShowWebPages . emit ( text , 76 , xsid , Related , icon           )
    ##########################################################################
    return
  ############################################################################
  def FunctionsMenu              ( self , mm , uuid , item                 ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "Functions"                               )
    LOM   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    if                           ( self . isSubordination ( )              ) :
      ########################################################################
      msg = self . getMenuItem   ( "AssignTables"                            )
      mm  . addActionFromMenu    ( LOM , 34621301 , msg                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "ShowIdentifier"                          )
    mm    . addActionFromMenu    ( LOM                                     , \
                                   34621101                                , \
                                   MSG                                     , \
                                   True                                    , \
                                   self . ShowIdentifier                     )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "Search"                                  )
    mm    . addActionFromMenu    ( LOM , 34621391 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "SearchIdentifier"                        )
    mm    . addActionFromMenu    ( LOM , 34621392 , MSG                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "WebPages"                                )
    mm    . addActionFromMenu    ( LOM , 34621321 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "IdentWebPage"                            )
    mm    . addActionFromMenu    ( LOM , 34621322 , MSG                      )
    ##########################################################################
    return mm
  ############################################################################
  def RunFunctionsMenu                 ( self , at , uuid , item           ) :
    ##########################################################################
    if                                 ( at == 34621101                    ) :
      ########################################################################
      if                               ( self . ShowIdentifier             ) :
        self . ShowIdentifier = False
      else                                                                   :
        self . ShowIdentifier = True
      ########################################################################
      self   . clear                   (                                     )
      self   . startup                 (                                     )
      ########################################################################
      return
    ##########################################################################
    if                                 ( at == 34621301                    ) :
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
    if                                 ( at == 34621321                    ) :
      ########################################################################
      self . OpenWebPageListings       ( "Subordination"                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621322                    ) :
      ########################################################################
      self . OpenWebPageListings       ( "Equivalent"                        )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621391                    ) :
      ########################################################################
      self . Search                    (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 34621392                    ) :
      ########################################################################
      self . SearchIdentifier          (                                     )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                 ( self , mm , uuid , item                 ) :
    ##########################################################################
    if                           ( uuid <= 0                               ) :
      return mm
    ##########################################################################
    TRX   = self . Translations
    NAME  = item . text          (                                           )
    MSG   = self . getMenuItem   ( "Belongs"                                 )
    LOM   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "CreateAlbum"                             )
    mm    . addActionFromMenu    ( LOM , 34635101 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "UpdateAlbum"                             )
    mm    . addActionFromMenu    ( LOM , 34635102 , MSG                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "Crowds"                                  )
    mm    . addActionFromMenu    ( LOM , 34635201 , MSG                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "IconGroups"                              )
    mm    . addActionFromMenu    ( LOM , 1201 , MSG                          )
    ##########################################################################
    MSG   = TRX                  [ "UI::PersonalGallery"                     ]
    mm    . addActionFromMenu    ( LOM , 1202 , MSG                          )
    ##########################################################################
    MSG   = TRX                  [ "UI::Galleries"                           ]
    mm    . addActionFromMenu    ( LOM , 1203 , MSG                          )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "WebPages"                                )
    mm    . addActionFromMenu    ( LOM , 34631321 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "IdentWebPage"                            )
    mm    . addActionFromMenu    ( LOM , 34631322 , MSG                      )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                ( self , at , uuid , item               ) :
    ##########################################################################
    if                             ( at == 34635101                        ) :
      ########################################################################
      self . CreateAlbum           ( uuid                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635102                        ) :
      ########################################################################
      self . UpdateAlbum           ( uuid                                    )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34635201                        ) :
      ########################################################################
      text = item . text           (                                         )
      xsid = str                   ( uuid                                    )
      ########################################################################
      self . OwnedPeopleGroup . emit ( text , 76 , xsid                      )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1201                            ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1202                            ) :
      ########################################################################
      text = item . text           (                                         )
      icon = item . icon           (                                         )
      xsid = str                   ( uuid                                    )
      ########################################################################
      self . ShowPersonalGallery . emit ( text , 76 , xsid , icon            )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1203                            ) :
      ########################################################################
      text = item . text           (                                         )
      icon = item . icon           (                                         )
      xsid = str                   ( uuid                                    )
      ########################################################################
      self . GalleryGroup . emit   ( text , 76 , xsid                        )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34631321                        ) :
      ########################################################################
      self . OpenWebPageBelongings ( uuid , item , "Subordination"           )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 34631322                        ) :
      ########################################################################
      self . OpenWebPageBelongings ( uuid , item , "Equivalent"              )
      ########################################################################
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
    self . Notify                  ( 0                                       )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                             ( self . isSearching ( )                ) :
      ########################################################################
      msg  = self . getMenuItem    ( "NotSearch"                             )
      mm   . addAction             ( 7401 , msg                              )
    ##########################################################################
    self   . AmountIndexMenu       ( mm                                      )
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    self   . AppendRenameAction    ( mm , 1102                               )
    self   . AssureEditNamesAction ( mm , 1601 , atItem                      )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . FunctionsMenu         ( mm , uuid , atItem                      )
    self   . GroupsMenu            ( mm , uuid , atItem                      )
    self   . SortingMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunAmountIndexMenu ( )         ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if ( self . RunGroupsMenu    ( at , uuid , atItem ) )                    :
      return True
    ##########################################################################
    if ( self . RunFunctionsMenu ( at , uuid , atItem ) )                    :
      return True
    ##########################################################################
    if                             ( self . RunSortingMenu     ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      ########################################################################
      self . RenameVideo           (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      NAM  = self . Tables         [ "NamesEditing"                          ]
      self . EditAllNames          ( self , "Albums" , uuid , NAM            )
      return True
    ##########################################################################
    if                             ( at == 7401                            ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
