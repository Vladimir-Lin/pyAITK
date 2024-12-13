# -*- coding: utf-8 -*-
##############################################################################
## PicturesView
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
from   PySide6                             import QtCore
from   PySide6                             import QtGui
from   PySide6                             import QtWidgets
from   PySide6 . QtCore                    import *
from   PySide6 . QtGui                     import *
from   PySide6 . QtWidgets                 import *
from   AITK    . Qt6                       import *
##############################################################################
from   AITK    . Qt6        . IconDock     import IconDock    as IconDock
##############################################################################
from   AITK    . Qt6        . MenuManager  import MenuManager as MenuManager
from   AITK    . Qt6        . LineEdit     import LineEdit    as LineEdit
from   AITK    . Qt6        . ComboBox     import ComboBox    as ComboBox
from   AITK    . Qt6        . SpinBox      import SpinBox     as SpinBox
##############################################################################
from   AITK    . Essentials . Relation     import Relation    as Relation
from   AITK    . Calendars  . StarDate     import StarDate    as StarDate
from   AITK    . Calendars  . Periode      import Periode     as Periode
from   AITK    . Pictures   . Picture      import Picture     as PictureItem
from   AITK    . Pictures   . Gallery      import Gallery     as GalleryItem
##############################################################################
from   AITK    . UUIDs      . UuidListings import appendUuid
from   AITK    . UUIDs      . UuidListings import appendUuids
from   AITK    . UUIDs      . UuidListings import getUuids
##############################################################################
class PicturesView           ( IconDock                                    ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  ShowPicture       = Signal ( str                                           )
  OpenPictureEditor = Signal ( str , dict                                    )
  OpenVariantTables = Signal ( str , str , int , str , dict                  )
  OpenLogHistory    = Signal ( str , str , str , str , str                   )
  ############################################################################
  def __init__               ( self , parent = None , plan = None          ) :
    ##########################################################################
    super ( ) . __init__     (        parent        , plan                   )
    ##########################################################################
    self . Total         = 0
    self . StartId       = 0
    self . Amount        = 60
    self . SortOrder     = "asc"
    self . UsingName     = False
    self . FetchTableKey = "PicturesView"
    ##########################################################################
    self . Grouping      = "Original"
    self . OldGrouping   = "Original"
    ## self . Grouping   = "Subordination"
    ## self . Grouping   = "Reverse"
    ##########################################################################
    self . Property   =             {                                        }
    self . Naming     = ""
    ## self . Naming     = "Size"
    ## self . Naming     = "Name"
    ## self . Naming     = "Uuid"
    ##########################################################################
    self . Relation  = Relation    (                                         )
    self . Relation  . setT2       ( "Picture"                               )
    self . Relation  . setRelation ( "Subordination"                         )
    ##########################################################################
    self . setFunction             ( self . HavingMenu , True                )
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
  def PrepareRelateType ( self , RelateId                                  ) :
    ##########################################################################
    if                  ( "Mouth"     == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Mouth"
    elif                ( "Eye"       == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Eye"
    elif                ( "Iris"      == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Iris"
    elif                ( "Nose"      == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Nose"
    elif                ( "Tit"       == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Tit"
    elif                ( "Umbilicus" == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Umbilicus"
    elif                ( "Pussy"     == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Pussy"
    elif                ( "Asshole"   == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Asshole"
    elif                ( "Tattoo"    == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Tattoo"
    elif                ( "Texture"   == RelateId                          ) :
      self . FetchTableKey = "PicturesView-Texture"
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    msg  = self . getMenuItem     ( "EditPicture"                            )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/interfaces.png" )      )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . EditCurrentPicture                )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    msg  = self . getMenuItem     ( "ImportPictures"                         )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/imagecollection.png" ) )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . ImportPictures                    )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Import"     , self . ImportPictures  , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Cut"        , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
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
    ## self . LinkVoice         ( self . CommandParser                          )
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
  def GetUuidIcon                ( self , DB , Uuid                        ) :
    ##########################################################################
    return Uuid
  ############################################################################
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    TABLE  = self . Tables   [ "Pictures"                                    ]
    QQ     = f"select count(*) from {TABLE} ;"
    DB     . Query           ( QQ                                            )
    ONE    = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( ONE in [ False , None ]                     ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
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
    TABLE  = self . Tables          [ "Pictures"                             ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    QQ     = f"select `uuid` from {TABLE} order by `id` {ORDER} limit {SID} , {AMOUNT} ;"
    ##########################################################################
    return QQ
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables     [ "Relation"                                  ]
    ##########################################################################
    if                                       ( self . isSubordination ( )  ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                                       ( self . isReverse       ( )  ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                     [                                             ]
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( self . isOriginal ( )        ) :
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
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "picture/uuids"
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
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "picture/uuids"
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
    if                              ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        FMT   = self . getMenuItem  ( "MoveTo"                               )
        MSG   = FMT . format        ( CNT                                    )
      else                                                                   :
        title = sourceWidget . windowTitle (                                 )
        FMT   = self . getMenuItem  ( "CopyFrom"                             )
        MSG   = FMT . format        ( title , CNT                            )
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
    return True
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures             ( self , sourceWidget , pos , JSOX          ) :
    ##########################################################################
    atItem = self . itemAt     ( pos                                         )
    ##########################################################################
    ## 在內部移動
    ##########################################################################
    if                         ( self == sourceWidget                      ) :
      ########################################################################
      uuid   = -1
      if                       ( atItem not in [ False , None ]            ) :
        ######################################################################
        uuid = atItem . data   ( Qt . UserRole                               )
        uuid = int             ( uuid                                        )
      ########################################################################
      self   . Go              ( self . PicturesMoving                     , \
                                 ( uuid , JSOX , )                           )
      ########################################################################
      return True
    ##########################################################################
    ## 從外部加入
    ##########################################################################
    uuid     = -1
    if                         ( atItem not in [ False , None ]            ) :
      uuid   = atItem . data   ( Qt . UserRole                               )
      uuid   = int             ( uuid                                        )
    ##########################################################################
    self     . Go              ( self . PicturesAppending                  , \
                                 ( uuid , JSOX , )                           )
    ##########################################################################
    return True
  ############################################################################
  def GetLastestPosition                   ( self , DB         , LUID      ) :
    return self . GetNormalLastestPosition ( DB   , "Relation" , LUID        )
  ############################################################################
  def GenerateMovingSQL                    ( self , LAST , UUIDs           ) :
    return self . GenerateNormalMovingSQL  ( "Relation"                    , \
                                             LAST                          , \
                                             UUIDs                         , \
                                             False                           )
  ############################################################################
  def PicturesMoving          ( self , atUuid , JSON                       ) :
    ##########################################################################
    UUIDs  = JSON             [ "UUIDs"                                      ]
    if                        ( len ( UUIDs ) <= 0                         ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    RELTAB = self . Tables    [ "Relation"                                   ]
    DB     . LockWrites       ( [ RELTAB                                   ] )
    ##########################################################################
    OPTS   = f"order by `position` asc"
    PUIDs  = self . Relation . Subordination ( DB , RELTAB , OPTS            )
    ##########################################################################
    LUID   = PUIDs            [ -1                                           ]
    LAST   = self . GetLastestPosition ( DB     , LUID                       )
    PUIDs  = self . OrderingPUIDs      ( atUuid , UUIDs , PUIDs              )
    SQLs   = self . GenerateMovingSQL  ( LAST   , PUIDs                      )
    self   . ExecuteSqlCommands ( "OrganizePositions" , DB , SQLs , 100      )
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
  def PicturesAppending        ( self , atUuid , JSON                      ) :
    ##########################################################################
    UUIDs  = JSON              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( DB == None                                ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ "Relation"                                  ]
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
    self   . ExecuteSqlCommands ( "OrganizePositions" , DB , SQLs , 100      )
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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def ImportPictureToDB              ( self , DB , Filename                ) :
    ##########################################################################
    PIC            = PictureItem     (                                       )
    OKAY           = PIC . Load      (             Filename                  )
    ##########################################################################
    if                               ( not OKAY                            ) :
      return False
    ##########################################################################
    BaseUuid       = int             ( self . Tables [ "BaseUuid" ]          )
    PICTAB         = self . Tables   [ "Information"                         ]
    DOPTAB         = self . Tables   [ "Depot"                               ]
    THUTAB         = self . Tables   [ "ThumbsInformation"                   ]
    THUDOP         = self . Tables   [ "Thumb"                               ]
    HASH           = self . Tables   [ "PictureHash"                         ]
    STAT           = self . Tables   [ "PictureStatistics"                   ]
    RELTAB         = self . Tables   [ "Relation"                            ]
    ##########################################################################
    OPTS           =                                                         {
      "Base"       : BaseUuid                                                ,
      "Prefer"     : 0                                                       ,
      "Master"     : PICTAB                                                  ,
      "Depot"      : DOPTAB                                                  ,
      "Thumb"      : THUTAB                                                  ,
      "ThumbDepot" : THUDOP                                                  ,
      "Hash"       : HASH                                                    ,
      "Histogram"  : STAT                                                    ,
    }
    ##########################################################################
    PIC            . PrepareForDB    (                                       )
    PIC            . ImportDB        ( DB , OPTS                             )
    PUID           = int             ( PIC . UUID                            )
    ##########################################################################
    if                               ( PUID <= 0                           ) :
      return False
    ##########################################################################
    if                               ( self . isSubordination ( )          ) :
      ########################################################################
      self         . Relation . set  ( "second" , PUID                       )
      DB           . LockWrites      ( [ RELTAB                            ] )
      self         . Relation . Join ( DB , RELTAB                           )
      DB           . UnlockTables    (                                       )
      ########################################################################
    elif                             ( self . isReverse       ( )          ) :
      ########################################################################
      self         . Relation . set  ( "first"  , PUID                       )
      DB           . LockWrites      ( [ RELTAB                            ] )
      self         . Relation . Join ( DB , RELTAB                           )
      DB           . UnlockTables    (                                       )
    ##########################################################################
    return True
  ############################################################################
  def ImportPicturesToDB       ( self , FILEs                              ) :
    ##########################################################################
    DB     = self . ConnectDB  ( UsePure = True                              )
    if                         ( DB == None                                ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    for Filename in FILEs                                                    :
      ########################################################################
      self . ImportPictureToDB ( DB , Filename                               )
    ##########################################################################
    self   . setVacancy        (                                             )
    self   . GoRelax . emit    (                                             )
    DB     . Close             (                                             )
    ##########################################################################
    self   . Notify            ( 5                                           )
    self   . startup           (                                             )
    ##########################################################################
    return
  ############################################################################
  def SavePictureAs                ( self , Filename , UUID                ) :
    ##########################################################################
    DB      = self . ConnectDB     ( UsePure = True                          )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    self    . OnBusy  . emit       (                                         )
    self    . setBustle            (                                         )
    ##########################################################################
    PICTAB  = self . Tables        [ "Information"                           ]
    DOPTAB  = self . Tables        [ "Depot"                                 ]
    ##########################################################################
    PIC     = PictureItem          (                                         )
    DOE     = False
    ##########################################################################
    INFO    = PIC . GetInformation ( DB , PICTAB , UUID                      )
    if                             ( INFO not in [ False , None ]          ) :
      ########################################################################
      QQ    = f"select `file` from {DOPTAB} where ( `uuid` = {UUID} ) ;"
      OKAY  = PIC . FromDB         ( DB , QQ                                 )
      ########################################################################
      if                           ( OKAY                                  ) :
        ######################################################################
        PIC . Image . save         ( filename = Filename                     )
        DOE = True
    ##########################################################################
    self    . setVacancy           (                                         )
    self    . GoRelax . emit       (                                         )
    DB      . Close                (                                         )
    ##########################################################################
    if                             ( DOE                                   ) :
      self    . Notify             ( 5                                       )
    else                                                                     :
      self    . Notify             ( 1                                       )
    ##########################################################################
    return
  ############################################################################
  def ExportPicturesToDIR       ( self , DB , DIR , UUIDs                  ) :
    ##########################################################################
    PICTAB  = self . Tables     [ "Information"                              ]
    DOPTAB  = self . Tables     [ "Depot"                                    ]
    ##########################################################################
    PIC     = PictureItem       (                                            )
    ##########################################################################
    for PCID in UUIDs                                                        :
      ########################################################################
      PIC      . UUID = PCID
      SUFFIX   = ""
      ########################################################################
      INFO     = PIC . GetInformation ( DB , PICTAB , PCID                   )
      if                              ( INFO not in [ False , None ]       ) :
        ######################################################################
        SUFFIX = INFO                 [ "Suffix"                             ]
      ########################################################################
      if                              ( len ( SUFFIX ) > 0                 ) :
        ######################################################################
        FNAM   = f"{DIR}/{PCID}.{SUFFIX}"
        PIC    . Export               ( DB , DOPTAB , FNAM                   )
    ##########################################################################
    return
  ############################################################################
  def ExportAllPictures         ( self , DIR                               ) :
    ##########################################################################
    DB      = self . ConnectDB  ( UsePure = True                             )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    self    . OnBusy  . emit    (                                            )
    self    . setBustle         (                                            )
    ##########################################################################
    RELTAB  = self . Tables     [ "Relation"                                 ]
    TABLE   = self . Tables     [ "Pictures"                                 ]
    UUIDs   =                   [                                            ]
    ##########################################################################
    if                          ( self . isSubordination ( )               ) :
      ########################################################################
      UUIDs = self . Relation . Subordination ( DB , RELTAB                  )
      ########################################################################
    elif                        ( self . isReverse       ( )               ) :
      ########################################################################
      UUIDs = self . Relation . GetOwners     ( DB , RELTAB                  )
    ##########################################################################
    if                          ( len ( UUIDs ) > 0                        ) :
      ########################################################################
      self  . ExportPicturesToDIR ( DB , DIR , UUIDs                         )
    ##########################################################################
    self    . setVacancy        (                                            )
    self    . GoRelax . emit    (                                            )
    DB      . Close             (                                            )
    ##########################################################################
    self    . Notify            ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def ExportPictureUUIDs       ( self , DIR , UUIDs                        ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB == None                                ) :
      return
    ##########################################################################
    self . OnBusy  . emit      (                                             )
    self . setBustle           (                                             )
    ##########################################################################
    self . ExportPicturesToDIR ( DB , DIR , UUIDs                            )
    ##########################################################################
    self . setVacancy          (                                             )
    self . GoRelax . emit      (                                             )
    DB   . Close               (                                             )
    ##########################################################################
    self    . Notify            ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def SaveSelectedPictures          ( self                                 ) :
    ##########################################################################
    DIR   = QFileDialog . getExistingDirectory                               (
                                      self                                   ,
                                      "儲存選取圖片" ,
                                      ""                                     ,
                                      QFileDialog . ShowDirsOnly             )
    ##########################################################################
    UUIDs = self . getSelectedUuids (                                        )
    VALs  =                         ( DIR , UUIDs ,                          )
    self  . Go                      ( self . ExportPictureUUIDs , VALs       )
    ##########################################################################
    return
  ############################################################################
  def SaveAllPictures ( self                                               ) :
    ##########################################################################
    DIR  = QFileDialog . getExistingDirectory                                (
                        self                                                 ,
                        "儲存全部圖片" ,
                        ""                                                   ,
                        QFileDialog . ShowDirsOnly                           )
    ##########################################################################
    self . Go         ( self . ExportAllPictures , ( DIR , )                 )
    ##########################################################################
    return
  ############################################################################
  def SavePicture                 ( self , UUID                            ) :
    ##########################################################################
    Filename = f"{UUID}.jpg"
    FILTERS  = self . getMenuItem ( "SaveImageFilters"                       )
    ##########################################################################
    F , _    = QFileDialog . getSaveFileName ( self                          ,
                                               "儲存圖片成指定格式" ,
                                               Filename                      ,
                                               FILTERS                       )
    ##########################################################################
    if                            ( len ( F ) <= 0                         ) :
      return
    ##########################################################################
    VAL      =                    ( F , UUID ,                               )
    self     . Go                 ( self . SavePictureAs , VAL               )
    ##########################################################################
    return
  ############################################################################
  def ImportPictures               ( self                                  ) :
    ##########################################################################
    FILTERS   = self . getMenuItem ( "OpenImageFilters"                      )
    ##########################################################################
    LISTS , _ = QFileDialog . getOpenFileNames ( self                        ,
                                                 "匯入圖片" ,
                                                 ""                          ,
                                                 FILTERS                     )
    ##########################################################################
    if                             ( len ( LISTS ) <= 0                    ) :
      return
    ##########################################################################
    self      . Go                 ( self . ImportPicturesToDB , ( LISTS , ) )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                      ( self , UUIDs                      ) :
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 0                ) :
      return
    ##########################################################################
    TITLE  = "RemovePictureItems"
    RELTAB = self . Tables             [ "Relation"                          ]
    SQLs   = self . GenerateRemoveSQLs ( UUIDs , self . Relation , RELTAB    )
    self   . QuickExecuteSQLs          ( TITLE , 100 , RELTAB , SQLs         )
    self   . loading                   (                                     )
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
  def ObtainPictureSizes       ( self , DB , UUIDs                         ) :
    ##########################################################################
    PICTAB = self . Tables     [ "Information"                               ]
    NAMEs  =                   {                                             }
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ   = f"""select `width`,`height` from {PICTAB}
                where ( `uuid` = {UUID} ) ;"""
      QQ   = " " . join        ( QQ . split ( )                              )
      DB   . Query             ( QQ                                          )
      RR   = DB . FetchOne     (                                             )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) > 0 ) )           :
        WW             = RR    [ 0                                           ]
        HH             = RR    [ 1                                           ]
        NAMEs [ UUID ] = f"{WW} x {HH}"
      else                                                                   :
        NAMEs [ UUID ] = ""
    ##########################################################################
    return NAMEs
  ############################################################################
  def ObtainsUuidNames                 ( self , DB , UUIDs                 ) :
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 0                ) :
      return                           {                                     }
    ##########################################################################
    if                                 ( self . Naming == "Uuid"           ) :
      NAMEs =                          {                                     }
      for UUID in UUIDs                                                      :
        NAMEs [ UUID ] = str           ( UUID                                )
      return NAMEs
    ##########################################################################
    if                                 ( self . Naming == "Name"           ) :
      TABLE = self . Tables            [ "Names"                             ]
      NAMEs = self . GetNames          ( DB , TABLE , UUIDs                  )
      return NAMEs
    ##########################################################################
    if                                 ( self . Naming == "Size"           ) :
      return self . ObtainPictureSizes ( DB , UUIDs                          )
    ##########################################################################
    return                            {                                      }
  ############################################################################
  def AssignAsIcon                   ( self , UUID                         ) :
    ##########################################################################
    DB     = self . ConnectDB        ( UsePure = True                        )
    if                               ( DB in [ False , None ]              ) :
      return
    ##########################################################################
    RELTAB = self . Tables           [ "Relation"                            ]
    ##########################################################################
    FIRST  = self . Relation . get   ( "first"                               )
    T1     = self . Relation . get   ( "t1"                                  )
    ##########################################################################
    GALM   = GalleryItem             (                                       )
    ICONs  = GALM . GetPictures      ( DB , RELTAB , FIRST , T1 , 12         )
    UUIDs  = GALM . PlaceUuidToFirst ( UUID , ICONs                          )
    ##########################################################################
    DB     . LockWrites              ( [ RELTAB                            ] )
    GALM   . RepositionIcons         ( DB , RELTAB , FIRST , T1 , UUIDs      )
    DB     . UnlockTables            (                                       )
    ##########################################################################
    DB     . Close                   (                                       )
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage          ( self                                  ) :
    ##########################################################################
    if                             ( not self . isGrouping ( )             ) :
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
    SCOPE  = f"PicturesView-{SCOPE}"
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
    elif                           ( self . isReverse       ( )            ) :
      ########################################################################
      TYPE = self . Relation . get ( "t2"                                    )
      UUID = self . Relation . get ( "second"                                )
    ##########################################################################
    SCOPE  = self . Grouping
    SCOPE  = f"PicturesView-{SCOPE}"
    self   . GetLocalityByUuid     ( DB , PAMTAB , UUID , TYPE , SCOPE       )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems                   ( self                                 ) :
    ##########################################################################
    UUIDs = self . getSelectedUuids (                                        )
    if                              ( len ( UUIDs ) <= 0                   ) :
      return
    ##########################################################################
    self  . Go                      ( self . RemoveItems , ( UUIDs , )       )
    ##########################################################################
    return
  ############################################################################
  def EditCurrentPicture              ( self                               ) :
    ##########################################################################
    atItem = self . currentItem       (                                      )
    ##########################################################################
    if                                ( atItem == None                     ) :
      return False
    ##########################################################################
    uuid   = atItem . data            ( Qt . UserRole                        )
    uuid   = int                      ( uuid                                 )
    ##########################################################################
    self   . OpenPictureEditor . emit ( str ( uuid ) , self . Tables         )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , "Picture" , "NamesEditing"    )
    ##########################################################################
    return
  ############################################################################
  def PropertiesMenu             ( self , mm                               ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "Properties"                              )
    COL   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    if                           ( self . isSubordination ( )              ) :
      ########################################################################
      msg = self . getMenuItem   ( "AssignTables"                            )
      mm  . addActionFromMenu    ( COL , 34471101 , msg                      )
    ##########################################################################
    msg   = self . getMenuItem   ( "SaveAllPictures"                         )
    mm    . addActionFromMenu    ( COL , 34471201 , msg                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( COL                                       )
    ##########################################################################
    CHECKED =                    ( not self . UsingName                      )
    msg   = self . getMenuItem   ( "DisplayNone"                             )
    mm    . addActionFromMenu    ( COL , 34471301 , msg , True , CHECKED     )
    ##########################################################################
    CHECKED   = False
    if ( self . UsingName ) and ( self . Naming == "Size" )                  :
      CHECKED = True
    ##########################################################################
    msg   = self . getMenuItem   ( "DisplaySize"                             )
    mm    . addActionFromMenu    ( COL , 34471302 , msg , True , CHECKED     )
    ##########################################################################
    CHECKED   = False
    if ( self . UsingName ) and ( self . Naming == "Name" )                  :
      CHECKED = True
    ##########################################################################
    msg   = self . getMenuItem   ( "DisplayName"                             )
    mm    . addActionFromMenu    ( COL , 34471303 , msg , True , CHECKED     )
    ##########################################################################
    CHECKED   = False
    if ( self . UsingName ) and ( self . Naming == "Uuid" )                  :
      CHECKED = True
    ##########################################################################
    msg   = self . getMenuItem   ( "DisplayUuid"                             )
    mm    . addActionFromMenu    ( COL , 34471304 , msg , True , CHECKED     )
    ##########################################################################
    return mm
  ############################################################################
  def RunPropertiesMenu ( self , at                                        ) :
    ##########################################################################
    if                  ( at == 34471101                                   ) :
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
    if                  ( at == 34471201                                   ) :
      ########################################################################
      self . SaveAllPictures (                                               )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 34471301                                   ) :
      ########################################################################
      self . UsingName = False
      self . Naming    = ""
      ########################################################################
      self . clear      (                                                    )
      self . startup    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 34471302                                   ) :
      ########################################################################
      self . UsingName = True
      self . Naming    = "Size"
      ########################################################################
      self . clear      (                                                    )
      self . startup    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 34471303                                   ) :
      ########################################################################
      self . UsingName = True
      self . Naming    = "Name"
      ########################################################################
      self . clear      (                                                    )
      self . startup    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 34471304                                   ) :
      ########################################################################
      self . UsingName = True
      self . Naming    = "Uuid"
      ########################################################################
      self . clear      (                                                    )
      self . startup    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def PictureMenu              ( self , mm , uuid , item                   ) :
    ##########################################################################
    if                         ( uuid <= 0                                 ) :
      return mm
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    FMT = self . getMenuItem   ( "Belongs"                                   )
    MSG = FMT  . format        ( item . text ( )                             )
    LOM = mm   . addMenu       ( MSG                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "SavePicture"                               )
    mm  . addActionFromMenu    ( LOM , 24231101 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "SaveSelections"                            )
    mm  . addActionFromMenu    ( LOM , 24231102 , msg                        )
    ##########################################################################
    msg = TRX                  [ "UI::EditNames"                             ]
    mm  . addActionFromMenu    ( LOM , 24231201 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "Description"                               )
    mm  . addActionFromMenu    ( LOM , 24231202 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunPictureMenu                    ( self , at , uuid , item          ) :
    ##########################################################################
    if                                  ( at == 24231101                   ) :
      ########################################################################
      self . SavePicture                ( uuid                               )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 24231102                   ) :
      ########################################################################
      self . SaveSelectedPictures       (                                    )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor   ( at , 24231201 , item               )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    if                                  ( at == 24231202                   ) :
      ########################################################################
      name = item . text                (                                    )
      LOC  = self . getLocality         (                                    )
      nx   = ""
      ########################################################################
      if                                ( "Notes" in self . Tables         ) :
        nx = self . Tables              [ "Notes"                            ]
      ########################################################################
      self . OpenLogHistory . emit      ( name                               ,
                                          str ( uuid )                       ,
                                          "Description"                      ,
                                          nx                                 ,
                                          str ( LOC  )                       )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                              ( self , pos                       ) :
    ##########################################################################
    if                                  ( not self . isPrepared ( )        ) :
      return False
    ##########################################################################
    doMenu = self . isFunction          ( self . HavingMenu                  )
    if                                  ( not doMenu                       ) :
      return False
    ##########################################################################
    self   . Notify                     ( 0                                  )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager                ( self                               )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . StopIconMenu               ( mm                                 )
    self   . AmountIndexMenu            ( mm                                 )
    self   . AppendRefreshAction        ( mm , 1001                          )
    ##########################################################################
    if                                  ( uuid > 0                         ) :
      ########################################################################
      mm   . addSeparator               (                                    )
      ########################################################################
      msg  = self . getMenuItem         ( "EditPicture"                      )
      icon = QIcon                      ( ":/images/interfaces.png"          )
      mm   . addActionWithIcon          ( 1101 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "ViewPicture"                      )
      mm   . addAction                  ( 1102 , msg                         )
      ########################################################################
      msg  = self . getMenuItem         ( "AssignIcon"                       )
      mm   . addAction                  ( 1103 , msg                         )
    ##########################################################################
    msg    = self . getMenuItem         ( "ImportPictures"                   )
    icon   = QIcon                      ( ":/images/imagecollection.png"     )
    mm     . addActionWithIcon          ( 2001 , icon , msg                  )
    ##########################################################################
    mm     . addSeparator               (                                    )
    self   . PropertiesMenu             ( mm                                 )
    self   . PictureMenu                ( mm , uuid , atItem                 )
    self   . SortingMenu                ( mm                                 )
    self   . LocalityMenu               ( mm                                 )
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    mm     . setFont                    ( self    . menuFont ( )             )
    aa     = mm . exec_                 ( QCursor . pos      ( )             )
    at     = mm . at                    ( aa                                 )
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu  (                                    )
    if                                  ( OKAY                             ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunPropertiesMenu   ( at                                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . RunPictureMenu      ( at , uuid , atItem                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu      ( at                                 )
    if                                  ( OKAY                             ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunDocking          ( mm , aa                            )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu  ( at                                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . RunStopIconMenu     ( at                                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    if                                  ( at == 1001                       ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 1101                       ) :
      self . OpenPictureEditor . emit   ( str ( uuid ) , self . Tables       )
      return True
    ##########################################################################
    if                                  ( at == 1102                       ) :
      self . ShowPicture       . emit   ( str ( uuid )                       )
      return True
    ##########################################################################
    if                                  ( at == 1103                       ) :
      self . Go                         ( self . AssignAsIcon , ( uuid , )   )
      return True
    ##########################################################################
    if                                  ( at == 2001                       ) :
      self . ImportPictures             (                                    )
      return True
    ##########################################################################
    return True
##############################################################################
