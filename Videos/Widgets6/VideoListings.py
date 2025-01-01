# -*- coding: utf-8 -*-
##############################################################################
## VideoListings
## 影片列表
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
from   PySide6                         import QtCore
from   PySide6                         import QtGui
from   PySide6                         import QtWidgets
from   PySide6 . QtCore                import *
from   PySide6 . QtGui                 import *
from   PySide6 . QtWidgets             import *
from   AITK    . Qt6                   import *
##############################################################################
from   AITK    . Qt6 . MenuManager     import MenuManager as MenuManager
from   AITK    . Qt6 . TreeDock        import TreeDock    as TreeDock
from   AITK    . Qt6 . LineEdit        import LineEdit    as LineEdit
from   AITK    . Qt6 . ComboBox        import ComboBox    as ComboBox
from   AITK    . Qt6 . SpinBox         import SpinBox     as SpinBox
##############################################################################
from   AITK    . Essentials . Relation import Relation
from   AITK    . Calendars  . StarDate import StarDate
from   AITK    . Calendars  . Periode  import Periode
from   AITK    . People     . People   import People
##############################################################################
class VideoListings          ( TreeDock                                    ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = Signal (                                               )
  emitAllNames      = Signal ( list                                          )
  AddToPlayList     = Signal ( str                                           )
  CreateAnalysis    = Signal ( str                                           )
  PlayAnalysis      = Signal ( str                                           )
  JoinCurrentEditor = Signal ( str                                           )
  OpenLogHistory    = Signal ( str , str , str , str , str                   )
  ############################################################################
  def __init__               ( self , parent = None , plan = None          ) :
    ##########################################################################
    super ( ) . __init__     (        parent        , plan                   )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . GType              = 11
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "asc"
    self . SearchLine         = None
    self . SearchKey          = ""
    self . Method             = ""
    self . ClipJson           = {                                            }
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . FetchTableKey      = "VideoListings"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "Video"                                 )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 14                                      )
    self . setColumnHidden         (  8 , True                               )
    self . setColumnHidden         (  9 , True                               )
    self . setColumnHidden         ( 10 , True                               )
    self . setColumnHidden         ( 11 , True                               )
    self . setColumnHidden         ( 12 , True                               )
    self . setColumnHidden         ( 13 , True                               )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ## self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 1024 , 480 )                      )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenVideoNames                    )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    ##########################################################################
    self . LinkAction ( "Search"     , self . Search          , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    ##########################################################################
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    ##########################################################################
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
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked            ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0 ]                        ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "VideoListings" , 13                             )
    ##########################################################################
    return
  ############################################################################
  def toHMS    ( self , DURATION                                           ) :
    ##########################################################################
    TT   = int ( DURATION / 1000000                                          )
    MM   = int ( TT       / 60                                               )
    SS   = int ( TT       % 60                                               )
    HH   = int ( MM       / 60                                               )
    MM   = int ( MM       % 60                                               )
    ##########################################################################
    SS   = f"{SS}"
    MM   = f"{MM}"
    ##########################################################################
    if         ( len ( SS ) < 2                                            ) :
      SS = f"0{SS}"
    ##########################################################################
    if         ( ( HH > 0 ) and ( len ( MM ) < 2 )                         ) :
      MM = f"0{MM}"
    ##########################################################################
    return f"{HH}:{MM}:{SS}"
  ############################################################################
  def PrepareItem               ( self , JSOX                              ) :
    ##########################################################################
    UUID       = JSOX           [ "Uuid"                                     ]
    NAME       = JSOX           [ "Name"                                     ]
    FILESIZE   = JSOX           [ "FileSize"                                 ]
    DURATION   = JSOX           [ "Duration"                                 ]
    WIDTH      = JSOX           [ "Width"                                    ]
    HEIGHT     = JSOX           [ "Height"                                   ]
    FRAMES     = JSOX           [ "Frames"                                   ]
    FORMAT     = JSOX           [ "Format"                                   ]
    FPS        = JSOX           [ "FPS"                                      ]
    VCODEC     = JSOX           [ "vCodec"                                   ]
    VBITRATE   = JSOX           [ "vBitRate"                                 ]
    ACODEC     = JSOX           [ "aCodec"                                   ]
    SAMPLERATE = JSOX           [ "SampleRate"                               ]
    ABITRATE   = JSOX           [ "aBitRate"                                 ]
    ##########################################################################
    IT = self . PrepareUuidItem (  0 , UUID , NAME                           )
    ##########################################################################
    IT . setText                (  1 , str ( FORMAT                        ) )
    IT . setText                (  2 , self . toHMS ( DURATION             ) )
    IT . setText                (  3 , str ( FILESIZE                      ) )
    IT . setText                (  4 , str ( WIDTH                         ) )
    IT . setText                (  5 , str ( HEIGHT                        ) )
    IT . setText                (  6 , str ( FPS                           ) )
    IT . setText                (  7 , str ( FRAMES                        ) )
    IT . setText                (  8 , str ( VCODEC                        ) )
    IT . setText                (  9 , str ( VBITRATE                      ) )
    IT . setText                ( 10 , str ( ACODEC                        ) )
    IT . setText                ( 11 , str ( SAMPLERATE                    ) )
    IT . setText                ( 12 , str ( ABITRATE                      ) )
    ##########################################################################
    IT . setTextAlignment       ( 13 , Qt . AlignRight                       )
    ##########################################################################
    return IT
  ############################################################################
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveItems                       )
    ##########################################################################
    return
  ############################################################################
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
    ##########################################################################
    return
  ############################################################################
  def nameChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item , 0                                   )
    ##########################################################################
    if                          ( len ( msg ) <= 0                         ) :
      self . removeTopLevelItem ( item                                       )
      return
    ##########################################################################
    item   . setText            ( column , msg                               )
    ##########################################################################
    self   . removeParked       (                                            )
    VAL    =                    ( item , uuid , msg ,                        )
    self   . Go                 ( self . AssureUuidItem , VAL                )
    ##########################################################################
    return
  ############################################################################
  def refresh                     ( self , JSONs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    for J in JSONs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( J                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( JSONs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
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
    if                                      ( self . isOriginal ( )        ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    ITEMs   =                         [                                      ]
    ##########################################################################
    VIDTAB  = self . Tables           [ "Videos"                             ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME  = self . GetName          ( DB , NAMTAB , UUID , "Default"       )
      ########################################################################
      QQ    = f"""select `filesize` , `duration` , `width` , `height` ,
                         `frames` , `format` , `fps` , `vcodec` ,
                         `vbitrate` , `acodec` , `samplerate` , `abitrate`
                  from {VIDTAB}
                  where ( `uuid` = {UUID} ) ;"""
      ########################################################################
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      if                              ( RR in [ False , None ]             ) :
        continue
      ########################################################################
      if                              ( len ( RR ) <= 0                    ) :
        continue
      ########################################################################
      FILESIZE   = int                ( RR [  0                            ] )
      DURATION   = int                ( RR [  1                            ] )
      WIDTH      = int                ( RR [  2                            ] )
      HEIGHT     = int                ( RR [  3                            ] )
      FRAMES     = int                ( RR [  4                            ] )
      FORMAT     = self.assureString  ( RR [  5                            ] )
      FPS        = self.assureString  ( RR [  6                            ] )
      VCODEC     = self.assureString  ( RR [  7                            ] )
      VBITRATE   = int                ( RR [  8                            ] )
      ACODEC     = self.assureString  ( RR [  9                            ] )
      SAMPLERATE = int                ( RR [ 10                            ] )
      ABITRATE   = int                ( RR [ 11                            ] )
      ########################################################################
      J          =                    { "Uuid"       : UUID                  ,
                                        "Name"       : NAME                  ,
                                        "FileSize"   : FILESIZE              ,
                                        "Duration"   : DURATION              ,
                                        "Width"      : WIDTH                 ,
                                        "Height"     : HEIGHT                ,
                                        "Frames"     : FRAMES                ,
                                        "Format"     : FORMAT                ,
                                        "FPS"        : FPS                   ,
                                        "vCodec"     : VCODEC                ,
                                        "vBitRate"   : VBITRATE              ,
                                        "aCodec"     : ACODEC                ,
                                        "SampleRate" : SAMPLERATE            ,
                                        "aBitRate"   : ABITRATE              }
      ########################################################################
      ITEMs . append                  ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( ITEMs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( ITEMs                                )
    ##########################################################################
    self   . Notify                   ( 5                                    )
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
  def ObtainAllUuids                ( self , DB                            ) :
    ##########################################################################
    TABLE  = self . Tables          [ "Videos"                               ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    QQ     = " " . join             ( QQ . split ( )                         )
    ##########################################################################
    return DB . ObtainUuids         ( QQ , 0                                 )
  ############################################################################
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    VIDTAB = self . Tables   [ "Videos"                                      ]
    QQ     = f"select count(*) from {VIDTAB} where ( `used` > 0 ) ;"
    DB     . Query           ( QQ                                            )
    ONE    = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( ONE == None                                 ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
      return 0
    ##########################################################################
    return ONE               [ 0                                             ]
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
    VIDTAB = self . Tables          [ "Videos"                               ]
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {VIDTAB}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    if                                ( self . isOriginal      ( )         ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isSubordination ( )         ) :
      ########################################################################
      UUID = self . Relation . get    ( "first"                              )
      TYPE = self . Relation . get    ( "t1"                                 )
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . isReverse       ( )         ) :
      ########################################################################
      UUID = self . Relation . get    ( "second"                             )
      TYPE = self . Relation . get    ( "t2"                                 )
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "video/uuids"
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
    formats = "video/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                        ( self                                , \
                                       source                              , \
                                       mimeData                            , \
                                       mousePos                            ) :
    ##########################################################################
    if                               ( self == source                      ) :
      return False
    ##########################################################################
    RDN    = self . RegularDropNew   ( mimeData                              )
    if                               ( not RDN                             ) :
      return False
    ##########################################################################
    mtype  = self   . DropInJSON     [ "Mime"                                ]
    UUIDs  = self   . DropInJSON     [ "UUIDs"                               ]
    atItem = self   . itemAt         ( mousePos                              )
    title  = source . windowTitle    (                                       )
    CNT    = len                     ( UUIDs                                 )
    ##########################################################################
    if                               ( mtype in [ "video/uuids"          ] ) :
      self . ShowMenuItemTitleStatus ( "VideosFrom" , title , CNT            )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving ( self , source , mimeData , mousePos                     ) :
    ##########################################################################
    if           ( self . droppingAction                                   ) :
      return False
    ##########################################################################
    if           ( source == self                                          ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def acceptVideoDrop ( self                                               ) :
    return True
  ############################################################################
  def dropVideos  ( self , source , pos , JSOX                             ) :
    ##########################################################################
    if            ( "UUIDs" not in JSOX                                    ) :
      return True
    ##########################################################################
    UUIDs = JSOX  [ "UUIDs"                                                  ]
    if            ( len ( UUIDs ) <= 0                                     ) :
      return True
    ##########################################################################
    self . Go     ( self . AppendingVideos , ( UUIDs , )                     )
    ##########################################################################
    return True
  ############################################################################
  def AppendingVideos           ( self , UUIDs                             ) :
    ##########################################################################
    COUNT  = len                ( UUIDs                                      )
    if                          ( COUNT <= 0                               ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    FMT    = self . getMenuItem ( "JoinVideos"                               )
    MSG    = FMT  . format      ( COUNT                                      )
    self   . ShowStatus         ( MSG                                        )
    self   . TtsTalk            ( MSG , 1002                                 )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationVideos"                           ]
    DB     . LockWrites         ( [ RELTAB                                 ] )
    ##########################################################################
    if                          ( self . isSubordination ( )               ) :
      ########################################################################
      self . Relation . Joins   ( DB , RELTAB , UUIDs                        )
      ########################################################################
    elif                        ( self . isReverse       ( )               ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        self . Relation . set   ( "first" , UUID                             )
        self . Relation . Join  ( DB      , RELTAB                           )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    ##########################################################################
    self   . setVacancy         (                                            )
    self   . GoRelax . emit     (                                            )
    DB     . Close              (                                            )
    self   . loading            (                                            )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                     ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    RELTAB = self . Tables            [ "RelationEditing"                    ]
    SQLs   =                          [                                      ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . Relation . set           ( "second" , UUID                      )
      QQ   = self . Relation . Delete ( RELTAB                               )
      SQLs . append                   ( QQ                                   )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    self   . setBustle                (                                      )
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    TITLE  = "RemoveOrganizationItems"
    self   . ExecuteSqlCommands       ( TITLE , DB , SQLs , 100              )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    self   . setVacancy               (                                      )
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    self   . loading                  (                                      )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    VIDTAB = self . Tables    [ "Videos"                                     ]
    RELTAB = self . Tables    [ "RelationEditing"                            ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ VIDTAB , RELTAB , NAMTAB                 ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( VIDTAB , "uuid" , 4500000000000000000        )
      DB   . AppendUuid       ( VIDTAB , uuid                                )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    if                        ( self . isSubordination ( )                 ) :
      ########################################################################
      self . Relation . set   ( "second" , uuid                              )
      self . Relation . Join  ( DB       , RELTAB                            )
      ########################################################################
    elif                      ( self . isReverse       ( )                 ) :
      ########################################################################
      self . Relation . set   ( "first"  , uuid                              )
      self . Relation . Join  ( DB       , RELTAB                            )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
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
  def OpenVideoNames            ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    uuid   = atItem . data      ( 0 , Qt . UserRole                          )
    uuid   = int                ( uuid                                       )
    head   = atItem . text      ( 0                                          )
    NAM    = self . Tables      [ "NamesEditing"                             ]
    self   . EditAllNames       ( self , "Video" , uuid , NAM                )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9013 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                ( self , mm , item                         ) :
    ##########################################################################
    if                          ( self . NotOkay ( item )                  ) :
      return mm
    ##########################################################################
    msg  = self . getMenuItem   ( "GroupFunctions"                           )
    COL  = mm . addMenu         ( msg                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "CopyVideoUuid"                            )
    mm   . addActionFromMenu    ( COL , 38521001 , msg                       )
    ##########################################################################
    mm   . addSeparatorFromMenu ( COL                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "Description"                              )
    mm   . addActionFromMenu    ( COL , 38522001 , msg                       )
    ##########################################################################
    if                          ( "Embedded" != self . Method              ) :
      return mm
    ##########################################################################
    mm   . addSeparatorFromMenu ( COL                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "AddToPlayList"                            )
    mm   . addActionFromMenu    ( COL , 38523001 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "CreateAnalysis"                           )
    mm   . addActionFromMenu    ( COL , 38523003 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "PlayAnalysis"                             )
    mm   . addActionFromMenu    ( COL , 38523003 , msg                       )
    ##########################################################################
    msg  = self . getMenuItem   ( "JoinCurrentEditor"                        )
    mm   . addActionFromMenu    ( COL , 38523004 , msg                       )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , item                     ) :
    ##########################################################################
    if                              ( at == 38521001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38522001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      head = item . text            ( 0                                      )
      nx   = ""
      ########################################################################
      if                            ( "Notes" in self . Tables             ) :
        nx = self . Tables          [ "Notes"                                ]
      ########################################################################
      self . OpenLogHistory . emit  ( head                                   ,
                                      str ( uuid )                           ,
                                      "Description"                          ,
                                      nx                                     ,
                                      ""                                     )
      ########################################################################
      return True
    ##########################################################################
    if                              ( "Embedded" != self . Method          ) :
      return False
    ##########################################################################
    if                              ( at == 38523001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      ########################################################################
      self . AddToPlayList . emit   ( str ( uuid                           ) )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38523002                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      ########################################################################
      self . CreateAnalysis . emit  ( str ( uuid                           ) )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38523003                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      ########################################################################
      self . PlayAnalysis . emit    ( str ( uuid                           ) )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38523004                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      ########################################################################
      self . JoinCurrentEditor . emit ( str ( uuid                         ) )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendRenameAction    ( mm , 1102                               )
    self   . AppendDeleteAction    ( mm , 1103                               )
    self   . TryAppendEditNamesAction ( atItem , mm , 1601                   )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . GroupsMenu            ( mm ,        atItem                      )
    self   . ColumnsMenu           ( mm                                      )
    self   . SortingMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu (                                     )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return
    ##########################################################################
    OKAY   = self . RunDocking     ( mm , aa                                 )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu ( at                                      )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu ( at                                      )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu  ( at , atItem                             )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1002                            ) :
      ########################################################################
      self . Grouping = self . OldGrouping
      self . restart               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      self . DeleteItems           (                                         )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      ########################################################################
      uuid = self . itemUuid       ( atItem , 0                              )
      NAM  = self . Tables         [ "NamesEditing"                          ]
      self . EditAllNames          ( self , "Video" , uuid , NAM             )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
