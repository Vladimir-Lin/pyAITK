# -*- coding: utf-8 -*-
##############################################################################
## PicturesView
##############################################################################
import os
import sys
import time
import requests
import threading
import json
##############################################################################
from   PySide6                              import QtCore
from   PySide6                              import QtGui
from   PySide6                              import QtWidgets
from   PySide6 . QtCore                     import *
from   PySide6 . QtGui                      import *
from   PySide6 . QtWidgets                  import *
from   AITK    . Qt6                        import *
##############################################################################
from   AITK    . Essentials . Relation      import Relation    as Relation
from   AITK    . Calendars  . StarDate      import StarDate    as StarDate
from   AITK    . Calendars  . Periode       import Periode     as Periode
from   AITK    . Documents  . Variables     import Variables   as VariableItem
from   AITK    . Pictures   . Picture6      import Picture     as PictureItem
from   AITK    . Pictures   . Gallery       import Gallery     as GalleryItem
##############################################################################
from   AITK    . UUIDs      . UuidListings6 import appendUuid
from   AITK    . UUIDs      . UuidListings6 import appendUuids
from   AITK    . UUIDs      . UuidListings6 import getUuids
from   AITK    . UUIDs      . UuidListings6 import assignUuids
##############################################################################
class PicturesView              ( IconDock                                 ) :
  ############################################################################
  HavingMenu           = 1371434312
  ############################################################################
  ShowPicture          = Signal ( str                                        )
  OpenPictureEditor    = Signal ( str , dict                                 )
  OpenVariantTables    = Signal ( str , str , int , str , dict               )
  OpenLogHistory       = Signal ( str , str , str , str , str                )
  emitLog              = Signal ( str                                        )
  ############################################################################
  def __init__                  ( self , parent = None , plan = None       ) :
    ##########################################################################
    super ( ) . __init__        (        parent        , plan                )
    ##########################################################################
    self . GetImportDIR   = self . defaultGetBrowseDirectory
    self . StoreImportDIR = self . defaultUpdateBrowseDirectory
    ##########################################################################
    self . ClassTag       = "PicturesView"
    self . FetchTableKey  = self . ClassTag
    ##########################################################################
    self . Total          = 0
    self . StartId        = 0
    self . Amount         = 60
    self . SortOrder      = "asc"
    self . UsingName      = False
    self . ExtraINFOs     = True
    self . RefreshOpts    = True
    self . Watermarking   = False
    self . ShowRecognize  = False
    self . PictureOPTs    =         {                                         }
    ##########################################################################
    self . defaultSelectionMode = "ExtendedSelection"
    ##########################################################################
    self . Grouping       = "Original"
    self . OldGrouping    = "Original"
    ## self . Grouping       = "Subordination"
    ## self . Grouping       = "Reverse"
    ##########################################################################
    self . Naming         = ""
    ## self . Naming         = "Size"
    ## self . Naming         = "Name"
    ## self . Naming         = "Uuid"
    ##########################################################################
    self . Relation  = Relation    (                                         )
    self . Relation  . setT2       ( "Picture"                               )
    self . Relation  . setRelation ( "Subordination"                         )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . setFunction             ( self . HavingMenu , True                )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    self . setMinimumSize          ( 144 , 200                               )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 660 , 800 )                       )
  ############################################################################
  def PrepareRelateType ( self , RelateId                                  ) :
    ##########################################################################
    PVCT  = self . ClassTag
    MEETs =             [ "Mouth"                                          , \
                          "Eye"                                            , \
                          "Iris"                                           , \
                          "Nose"                                           , \
                          "Tit"                                            , \
                          "Umbilicus"                                      , \
                          "Pussy"                                          , \
                          "Asshole"                                        , \
                          "Tattoo"                                         , \
                          "Piercings"                                      , \
                          "Texture"                                          ]
    ##########################################################################
    if                  ( RelateId in MEETs                                ) :
      ########################################################################
      self . FetchTableKey = f"{PVCT}-{RelateId}"
    ##########################################################################
    return
  ############################################################################
  def PrepareFetchTableKey ( self                                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . PrepareFetchTableKey     (                                        )
    self . AppendToolNamingAction   (                                        )
    ##########################################################################
    self . AppendWindowToolSeparatorAction (                                 )
    ##########################################################################
    self . AppendSideActionWithIcon ( "EditPicture"                        , \
                                      ":/images/epicture.png"              , \
                                      self . EditCurrentPicture              )
    self . AppendSideActionWithIcon ( "ViewPicture"                        , \
                                      ":/images/searchimages.png"          , \
                                      self . OpenPictureViewer               )
    self . AppendSideActionWithIcon ( "AssignIcon"                         , \
                                      ":/images/avataricon.png"            , \
                                      self . DoAssignAsIcon                  )
    ##########################################################################
    self . AppendWindowToolSeparatorAction (                                 )
    ##########################################################################
    self . AppendSideActionWithIcon ( "AssignTables"                       , \
                                      ":/images/vtables.png"               , \
                                      self . EditVariantTables             , \
                                      True                                 , \
                                      False                                  )
    ##########################################################################
    self . AppendWindowToolSeparatorAction (                                 )
    ##########################################################################
    self . AppendSideActionWithIcon ( "ImportPictures"                     , \
                                      ":/images/importpictures.png"        , \
                                      self . ImportPictures                , \
                                      True                                 , \
                                      False                                  )
    ##########################################################################
    self . AppendWindowToolSeparatorAction (                                 )
    ##########################################################################
    self . AppendSideActionWithIcon ( "SavePicture"                        , \
                                      ":/images/savepicture.png"           , \
                                      self . SaveCurrentPicture              )
    self . AppendSideActionWithIcon ( "SaveAllPictures"                    , \
                                      ":/images/savepictures.png"          , \
                                      self . SaveAllPictures               , \
                                      True                                 , \
                                      False                                  )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                         Enabled     ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup        , Enabled       )
    self . LinkAction ( "Import"     , self . ImportPictures , Enabled       )
    self . LinkAction ( "Delete"     , self . DeleteItems    , Enabled       )
    self . LinkAction ( "Cut"        , self . DeleteItems    , Enabled       )
    self . LinkAction ( "Home"       , self . PageHome       , Enabled       )
    self . LinkAction ( "End"        , self . PageEnd        , Enabled       )
    self . LinkAction ( "PageUp"     , self . PageUp         , Enabled       )
    self . LinkAction ( "PageDown"   , self . PageDown       , Enabled       )
    ## self . LinkAction ( "Select"     , self . SelectOne      , Enabled       )
    self . LinkAction ( "Reversal"   , self . ReversalSelect , Enabled       )
    self . LinkAction ( "SelectAll"  , self . SelectAll      , Enabled       )
    self . LinkAction ( "SelectNone" , self . SelectNone     , Enabled       )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                     ( self                                   ) :
    return self . defaultFocusIn  (                                          )
  ############################################################################
  def FocusOut                    ( self                                   ) :
    return self . defaultFocusOut (                                          )
  ############################################################################
  def Shutdown               ( self                                        ) :
    ##########################################################################
    self . StayAlive   = False
    self . LoopRunning = False
    ##########################################################################
    if                       ( self . isThreadRunning (                  ) ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label" , ""                                  )
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    ##########################################################################
    self . Leave . emit      ( self                                          )
    ##########################################################################
    return True
  ############################################################################
  def GetUuidIcon ( self , DB , Uuid                                       ) :
    return Uuid
  ############################################################################
  def FetchBaseINFO                  ( self , DB , UUID , PUID             ) :
    ##########################################################################
    ICZ    = self . FetchEntityImage (        DB , PUID                      )
    ##########################################################################
    if                               ( ICZ in self . EmptySet              ) :
      return
    ##########################################################################
    if                               ( UUID in self . PictureOPTs          ) :
      ########################################################################
      self . PictureOPTs [ UUID ] [ "Image" ] = ICZ
      ########################################################################
    else                                                                     :
      ########################################################################
      self . PictureOPTs [ UUID ] =  { "Image" : ICZ                         }
    ##########################################################################
    self   . EmitInfoIcon            ( UUID                                  )
    ##########################################################################
    return
  ############################################################################
  def DrawRecognition ( self , p , IW , IH , WW , HH , RCOG                ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def EmitInfoIcon                    ( self , UUID                        ) :
    ##########################################################################
    if                                ( UUID not in self . UuidItemMaps    ) :
      return
    ##########################################################################
    if                                ( UUID not in self . PictureOPTs     ) :
      return
    ##########################################################################
    GOPTs     = self . PictureOPTs    [ UUID                                 ]
    item      = self . UuidItemMaps   [ UUID                                 ]
    ##########################################################################
    RECG      = self . GetRecognizer  (                                      )
    ##########################################################################
    if                                ( "Image" in GOPTs                   ) :
      ########################################################################
      IMG     = GOPTs                 [ "Image"                              ]
      ########################################################################
    else                                                                     :
      ########################################################################
      ICON    = self . windowIcon     (                                      )
      PIX     = ICON . pixmap         ( 128 , 128                            )
      IMG     = PIX  . toImage        (                                      )
    ##########################################################################
    TIW       = 16
    TIH       = 16
    DINFO     = False
    ##########################################################################
    if                                ( not self . Watermarking            ) :
      ########################################################################
      DINFO   = False
    ##########################################################################
    if                                ( DINFO                              ) :
      ########################################################################
      ISIZE   = IMG . size            (                                      )
      ICZ     = QImage                ( ISIZE , QImage . Format_ARGB32       )
      ICZ     . fill                  ( QColor ( 255 , 255 , 255 )           )
      ########################################################################
      PTS     = QPoint                ( 0 , 0                                )
      ########################################################################
      p       = QPainter              (                                      )
      p       . begin                 ( ICZ                                  )
      ########################################################################
      p       . drawImage             ( PTS , IMG                            )
      ########################################################################
      if                              ( self . ShowRecognize               ) :
        ######################################################################
        if                            ( RECG not in self . EmptySet        ) :
          if                          ( "Recognition" in GOPTs             ) :
            ##################################################################
            RCOG = GOPTs              [ "Recognition"                        ]
            WW   = GOPTs              [ "Width"                              ]
            HH   = GOPTs              [ "Height"                             ]
            self . DrawRecognition    ( p , 128 , 128 , WW , HH , RCOG       )
      ########################################################################
      p       . end                   (                                      )
      ########################################################################
    else                                                                     :
      ########################################################################
      ICZ     = IMG
    ##########################################################################
    icon      = self . ImageToIcon    ( ICZ                                  )
    ##########################################################################
    self      . emitAssignIcon . emit ( item , icon                          )
    ##########################################################################
    return
  ############################################################################
  def ParallelFetchIcons      ( self , ID , UUIDs                          ) :
    ##########################################################################
    self . ParallelFetchINFOs (        ID , UUIDs                            )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item                              ) :
    ##########################################################################
    self . defaultSingleClicked (        item                                )
    ##########################################################################
    return True
  ############################################################################
  def doubleClicked        ( self , item                                   ) :
    ##########################################################################
    self . EditPictureItem (        item                                     )
    ##########################################################################
    return True
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
    self . PictureOPTs =                  {                                  }
    ##########################################################################
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def GenerateItemToolTip             ( self , UUID                        ) :
    ##########################################################################
    if                                ( UUID not in self . UuidItemMaps    ) :
      return
    ##########################################################################
    if                                ( UUID not in self . PictureOPTs     ) :
      return
    ##########################################################################
    FMT    = self . getMenuItem       ( "PictureToolTip"                     )
    ##########################################################################
    WIDTH  = self . PictureOPTs       [ UUID ] [ "Width"                     ]
    HEIGHT = self . PictureOPTs       [ UUID ] [ "Height"                    ]
    FORMAT = self . PictureOPTs       [ UUID ] [ "Format"                    ]
    FSIZE  = self . PictureOPTs       [ UUID ] [ "FileSize"                  ]
    ##########################################################################
    text   = FMT . format             ( UUID                               , \
                                        WIDTH                              , \
                                        HEIGHT                             , \
                                        FORMAT                             , \
                                        FSIZE                                )
    ##########################################################################
    item   = self . UuidItemMaps      [ UUID                                 ]
    self   . emitAssignToolTip . emit ( item , text                          )
    self   . EmitInfoIcon             ( UUID                                 )
    ##########################################################################
    return
  ############################################################################
  def FetchExtraInformations           ( self , UUIDs                      ) :
    ##########################################################################
    DB           = self . ConnectDB    (                                     )
    if                                 ( self . NotOkay ( DB )             ) :
      return
    ##########################################################################
    PICTAB       = self . Tables       [ "Information"                       ]
    ##########################################################################
    DSKEY        = "DescribeVariables"
    VARTAB       = ""
    ##########################################################################
    if                                 ( DSKEY in self . Tables            ) :
      VARTAB     = self . Tables       [ DSKEY                               ]
    ##########################################################################
    PV           = VariableItem        (                                     )
    ##########################################################################
    PV . Type    = 9
    PV . Name    = "Description"
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if                               ( not self . StayAlive              ) :
        continue
      ########################################################################
      GJSON      =                     { "Width"    : 0                    , \
                                         "Height"   : 0                    , \
                                         "Format"   : ""                   , \
                                         "FileSize" : 0                      }
      ########################################################################
      if                               ( U in self . PictureOPTs           ) :
        ######################################################################
        GOPTs    = self . PictureOPTs  [ U                                   ]
        ######################################################################
        if                             ( "Image" in GOPTs                  ) :
          ####################################################################
          GJSON [ "Image" ] = GOPTs    [ "Image"                             ]
      ########################################################################
      self       . PictureOPTs [ U ] = GJSON
      ########################################################################
      QQ         = f"""select `width` , `height` , `filesize` , `suffix` from {PICTAB}
                       where ( `uuid` = {U} ) ;"""
      DB         . Query               ( " " . join ( QQ . split (       ) ) )
      RR         = DB . FetchOne       (                                     )
      ########################################################################
      if                               ( RR not in self . EmptySet         ) :
        ######################################################################
        if                             ( 4 == len ( RR )                   ) :
          ####################################################################
          WW     = int                 ( RR [ 0                            ] )
          HH     = int                 ( RR [ 1                            ] )
          SS     = int                 ( RR [ 2                            ] )
          FF     = self . BlobToString ( RR [ 3                            ] )
          ####################################################################
          self   . PictureOPTs [ U ] [ "Width"    ] = WW
          self   . PictureOPTs [ U ] [ "Height"   ] = HH
          self   . PictureOPTs [ U ] [ "Format"   ] = FF
          self   . PictureOPTs [ U ] [ "FileSize" ] = SS
          ####################################################################
          if                           ( len ( VARTAB ) > 0                ) :
            ##################################################################
            PV   . Uuid = U
            ##################################################################
            RCOG = PV . GetValue       ( DB , VARTAB                         )
            ##################################################################
            if                         ( RCOG not in self . EmptySet       ) :
              ################################################################
              if                       ( len ( RCOG ) > 0                  ) :
                ##############################################################
                RS = self . assureString ( RCOG                              )
                ##############################################################
                try                                                          :
                  ############################################################
                  JS = json . loads      ( RS                                )
                  self   . PictureOPTs [ U ] [ "Recognition" ] = JS
                  ############################################################
                except                                                       :
                  pass
      ########################################################################
      self       . GenerateItemToolTip ( U                                   )
    ##########################################################################
    DB           . Close               (                                     )
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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def AnalyzePictureDescription          ( self , DB , UUIDs               ) :
    ##########################################################################
    RECG     = self . GetRecognizer      (                                   )
    ##########################################################################
    if                                   ( RECG in self . EmptySet         ) :
      return
    ##########################################################################
    OPTs     =                           {                                   }
    PV       = VariableItem              (                                   )
    PICTAB   = self . Tables             [ "Information"                     ]
    DOPTAB   = self . Tables             [ "Depot"                           ]
    VARTAB   = self . Tables             [ "DescribeVariables"               ]
    ##########################################################################
    PV       . Type = 9
    PV       . Name = "Description"
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      PIC    = PictureItem               (                                   )
      INFO   = PIC . GetInformation      ( DB , PICTAB , UUID                )
      ########################################################################
      if                                 ( INFO not in self . EmptySet     ) :
        ######################################################################
        QQ   = f"select `file` from {DOPTAB} where ( `uuid` = {UUID} ) ;"
        OKAY = PIC . FromDB              ( DB , QQ                           )
        ######################################################################
        if                               ( OKAY                            ) :
          ####################################################################
          J  = RECG . DoBasicDescription ( PIC , INFO , OPTs                 )
          ####################################################################
          PV . Uuid  = UUID
          PV . Value = json . dumps      ( J                                 )
          PV . AssureValue               ( DB , VARTAB                       )
    ##########################################################################
    return
  ############################################################################
  def DescribeAllPictures             ( self                               ) :
    ##########################################################################
    DB    = self . ConnectDB          ( UsePure = True                       )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self  . OnBusy  . emit            (                                      )
    self  . setBustle                 (                                      )
    ##########################################################################
    UUIDs = self . ObtainsItemUuids   ( DB                                   )
    self  . AnalyzePictureDescription ( DB , UUIDs                           )
    ##########################################################################
    self  . setVacancy                (                                      )
    self  . GoRelax . emit            (                                      )
    DB    . Close                     (                                      )
    ##########################################################################
    self  . Notify                    ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def DoDescribePictures             ( self , UUIDs                        ) :
    ##########################################################################
    DB   = self . ConnectDB          ( UsePure = True                        )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    self . OnBusy  . emit            (                                       )
    self . setBustle                 (                                       )
    ##########################################################################
    self . AnalyzePictureDescription ( DB , UUIDs                            )
    ##########################################################################
    self . setVacancy                (                                       )
    self . GoRelax . emit            (                                       )
    DB   . Close                     (                                       )
    ##########################################################################
    self . Notify                    ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def DescribePictures              ( self                                 ) :
    ##########################################################################
    UUIDs = self . getSelectedUuids (                                        )
    ##########################################################################
    if                              ( len ( UUIDs ) <= 0                   ) :
      return
    ##########################################################################
    VAL   =                         ( UUIDs ,                                )
    self  . Go                      ( self . DoDescribePictures , VAL        )
    ##########################################################################
    return
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
    UUIDs = self . getSelectedUuids (                                        )
    ##########################################################################
    if                              ( len ( UUIDs ) <= 0                   ) :
      return
    ##########################################################################
    ROOT  = self . GetImportDIR     (                                        )
    TITLE = self . getMenuItem      ( "SaveSelections"                       )
    ##########################################################################
    DIR   = QFileDialog . getExistingDirectory                               (
                                      self                                   ,
                                      TITLE                                  ,
                                      ROOT                                   ,
                                      QFileDialog . ShowDirsOnly             )
    ##########################################################################
    if                              ( len ( DIR ) <= 0                     ) :
      return
    ##########################################################################
    self  . StoreImportDIR          ( DIR                                    )
    ##########################################################################
    VALs  =                         ( DIR , UUIDs ,                          )
    self  . Go                      ( self . ExportPictureUUIDs , VALs       )
    ##########################################################################
    return
  ############################################################################
  def SaveAllPictures           ( self                                     ) :
    ##########################################################################
    ROOT  = self . GetImportDIR (                                            )
    TITLE = self . getMenuItem  ( "SaveAllPictures"                          )
    ##########################################################################
    DIR   = QFileDialog . getExistingDirectory                               (
                        self                                                 ,
                        TITLE                                                ,
                        ROOT                                                 ,
                        QFileDialog . ShowDirsOnly                           )
    ##########################################################################
    if                          ( len ( DIR ) <= 0                         ) :
      return
    ##########################################################################
    self  . StoreImportDIR      ( DIR                                        )
    ##########################################################################
    self  . Go                  ( self . ExportAllPictures , ( DIR ,       ) )
    ##########################################################################
    return
  ############################################################################
  def SavePicture                  ( self , UUID                           ) :
    ##########################################################################
    ROOT     = self . GetImportDIR (                                         )
    Filename = f"{ROOT}/{UUID}.jpg"
    TITLE    = self . getMenuItem  ( "StorePictureAs"                        )
    FILTERS  = self . getMenuItem  ( "SaveImageFilters"                      )
    ##########################################################################
    F , _    = QFileDialog . getSaveFileName ( self                          ,
                                               TITLE                         ,
                                               Filename                      ,
                                               FILTERS                       )
    ##########################################################################
    if                             ( len ( F ) <= 0                        ) :
      return
    ##########################################################################
    self     . StoreImportDIR      ( F                                       )
    ##########################################################################
    VAL      =                     ( F , UUID ,                              )
    self     . Go                  ( self . SavePictureAs , VAL              )
    ##########################################################################
    return
  ############################################################################
  def SaveCurrentPicture          ( self                                   ) :
    ##########################################################################
    atItem = self   . currentItem (                                          )
    ##########################################################################
    if                            ( self . NotOkay ( atItem )              ) :
      return
    ##########################################################################
    uuid   = atItem . data        ( Qt . UserRole                            )
    uuid   = int                  ( uuid                                     )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      return
    ##########################################################################
    self   . SavePicture          ( uuid                                     )
    ##########################################################################
    return
  ############################################################################
  def ImportPictures                ( self                                 ) :
    ##########################################################################
    ROOT      = self . GetImportDIR (                                        )
    TITLE     = self . getMenuItem  ( "ImportPictures"                       )
    FILTERS   = self . getMenuItem  ( "OpenImageFilters"                     )
    ##########################################################################
    LISTS , _ = QFileDialog . getOpenFileNames ( self                        ,
                                                 TITLE                       ,
                                                 ROOT                        ,
                                                 FILTERS                     )
    ##########################################################################
    if                              ( len ( LISTS ) <= 0                   ) :
      return
    ##########################################################################
    self      . StoreImportDIR      ( LISTS [ 0                            ] )
    self      . Go                  ( self . ImportPicturesToDB , ( LISTS, ) )
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
    RELTAB = self . Tables           [ "RelationPictures"                    ]
    ##########################################################################
    FIRST  = self . Relation . get   ( "first"                               )
    T1     = self . Relation . get   ( "t1"                                  )
    ##########################################################################
    GALM   = GalleryItem             (                                       )
    ICONs  = GALM . GetPictures      ( DB , RELTAB , FIRST , T1 , 12         )
    INSIDE =                         ( UUID in ICONs                         )
    UUIDs  = GALM . PlaceUuidToFirst ( UUID , ICONs                          )
    ##########################################################################
    DB     . LockWrites              ( [ RELTAB                            ] )
    ##########################################################################
    if                               ( not INSIDE                          ) :
      ########################################################################
      GALM . JoinIconByT1            ( DB , RELTAB , FIRST , T1 , UUID       )
    ##########################################################################
    GALM   . RepositionIcons         ( DB , RELTAB , FIRST , T1 , UUIDs      )
    DB     . UnlockTables            (                                       )
    ##########################################################################
    DB     . Close                   (                                       )
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def DoAssignAsIcon              ( self                                   ) :
    ##########################################################################
    atItem = self   . currentItem (                                          )
    ##########################################################################
    if                            ( self . NotOkay ( atItem )              ) :
      return
    ##########################################################################
    uuid   = atItem . data        ( Qt . UserRole                            )
    uuid   = int                  ( uuid                                     )
    ##########################################################################
    if                            ( uuid <= 0                              ) :
      return
    ##########################################################################
    self . Go                     ( self . AssignAsIcon , ( uuid , )         )
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
  def EditPictureItem                 ( self , item                        ) :
    ##########################################################################
    uuid   = item . data              ( Qt . UserRole                        )
    uuid   = int                      ( uuid                                 )
    ##########################################################################
    self   . OpenPictureEditor . emit ( str ( uuid ) , self . Tables         )
    ##########################################################################
    return
  ############################################################################
  def EditCurrentPicture        ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( atItem == None                           ) :
      return
    ##########################################################################
    self   . EditPictureItem    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def ViewPictureItem         ( self , item                                ) :
    ##########################################################################
    uuid = item . data        ( Qt . UserRole                                )
    uuid = int                ( uuid                                         )
    ##########################################################################
    self . ShowPicture . emit ( str ( uuid )                                 )
    ##########################################################################
    return
  ############################################################################
  def OpenPictureViewer         ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    ##########################################################################
    if                          ( atItem == None                           ) :
      return
    ##########################################################################
    self   . ViewPictureItem    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def EditVariantTables              ( self                                ) :
    ##########################################################################
    TITLE = self . windowTitle       (                                       )
    UUID  = self . Relation  . get   ( "first"                               )
    TYPE  = self . Relation  . get   ( "t1"                                  )
    TYPE  = int                      ( TYPE                                  )
    self  . OpenVariantTables . emit ( str ( TITLE )                       , \
                                       str ( UUID  )                       , \
                                       TYPE                                , \
                                       self . FetchTableKey                , \
                                       self . Tables                         )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , "Picture" , "NamesEditing"    )
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
  def PropertiesMenu             ( self , mm                               ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "Properties"                              )
    COL   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    if                           ( self . isSubordination ( )              ) :
      ########################################################################
      msg = self . getMenuItem   ( "AssignTables"                            )
      ICN = QIcon                ( ":/images/vtables.png"                    )
      mm  . addActionFromMenuWithIcon ( COL , 34471101 , ICN , msg           )
    ##########################################################################
    msg   = self . getMenuItem   ( "DoReposition"                            )
    mm    . addActionFromMenu    ( COL                                     , \
                                   34471102                                , \
                                   msg                                     , \
                                   True                                    , \
                                   self . DoReposition                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "Watermarking"                            )
    mm    . addActionFromMenu    ( COL                                     , \
                                   34471103                                , \
                                   msg                                     , \
                                   True                                    , \
                                   self . Watermarking                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "ShowRecognize"                           )
    mm    . addActionFromMenu    ( COL                                     , \
                                   34471104                                , \
                                   msg                                     , \
                                   True                                    , \
                                   self . Watermarking                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "ReportTables"                            )
    mm    . addActionFromMenu    ( COL , 34471105 , msg                      )
    ##########################################################################
    msg   = self . getMenuItem   ( "SaveAllPictures"                         )
    ICON  = QIcon                ( ":/images/savepictures.png"               )
    mm    . addActionFromMenuWithIcon ( COL , 34471201 , ICON , msg          )
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
      self . EditVariantTables (                                             )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 34471102                                   ) :
      ########################################################################
      self . DoReposition = not self . DoReposition
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 34471103                                   ) :
      ########################################################################
      self . Watermarking = not self . Watermarking
      ########################################################################
      self . restart    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 34471104                                   ) :
      ########################################################################
      self . ShowRecognize = not self . ShowRecognize
      ########################################################################
      self . restart    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 34471105                                   ) :
      ########################################################################
      self . emitLog . emit ( json . dumps ( self . Tables                 ) )
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
    ICN = QIcon                ( ":/images/savepicture.png"                  )
    mm  . addActionFromMenuWithIcon ( LOM , 24231101 , ICN , msg             )
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
  def AnalyzeMenu              ( self , mm , uuid , item                   ) :
    ##########################################################################
    MSG   = self . getMenuItem ( "AnalyzePictures"                           )
    LOM   = mm   . addMenu     ( MSG                                         )
    ##########################################################################
    if                         ( uuid > 0                                  ) :
      ########################################################################
      msg = self . getMenuItem ( "DescribePictures"                          )
      mm  . addActionFromMenu  ( LOM , 27931001 , msg                        )
    ##########################################################################
    msg   = self . getMenuItem ( "DescribeAllPictures"                       )
    mm    . addActionFromMenu  ( LOM , 27931002 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunAnalyzeMenu          ( self , at , uuid , item                    ) :
    ##########################################################################
    if                        ( 27931001 == at                             ) :
      ########################################################################
      self . DescribePictures (                                              )
      ########################################################################
      return True
    ##########################################################################
    if                        ( 27931002 == at                             ) :
      ########################################################################
      self . Go               ( self . DescribeAllPictures                   )
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
    self   . AmountIndexMenu            ( mm , True                          )
    self   . AppendRefreshAction        ( mm , 1001                          )
    ##########################################################################
    if                                  ( uuid > 0                         ) :
      ########################################################################
      mm   . addSeparator               (                                    )
      ########################################################################
      msg  = self . getMenuItem         ( "EditPicture"                      )
      icon = QIcon                      ( ":/images/epicture.png"            )
      mm   . addActionWithIcon          ( 1101 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "ViewPicture"                      )
      icon = QIcon                      ( ":/images/searchimages.png"        )
      mm   . addActionWithIcon          ( 1102 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "AssignIcon"                       )
      icon = QIcon                      ( ":/images/avataricon.png"          )
      mm   . addActionWithIcon          ( 1103 , icon , msg                  )
    ##########################################################################
    msg    = self . getMenuItem         ( "ImportPictures"                   )
    icon   = QIcon                      ( ":/images/importpictures.png"      )
    mm     . addActionWithIcon          ( 2001 , icon , msg                  )
    ##########################################################################
    mm     . addSeparator               (                                    )
    self   . PropertiesMenu             ( mm                                 )
    self   . PictureMenu                ( mm , uuid , atItem                 )
    self   . AnalyzeMenu                ( mm , uuid , atItem                 )
    self   . SortingMenu                ( mm                                 )
    self   . LocalityMenu               ( mm                                 )
    self   . ScrollBarMenu              ( mm                                 )
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                    ( self    . menuFont ( )             )
    aa     = mm . exec_                 ( QCursor . pos      ( )             )
    at     = mm . at                    ( aa                                 )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu  ( at                                 )
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
    OKAY   = self . RunAnalyzeMenu      ( at , uuid , atItem                 )
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
    OKAY   = self . RunScrollBarMenu    ( at                                 )
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
      self . ViewPictureItem            ( atItem                             )
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
