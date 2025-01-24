# -*- coding: utf-8 -*-
##############################################################################
## FaceShapeListings
##############################################################################
import os
import sys
import time
import requests
import threading
import json
##############################################################################
from   PySide6                                   import QtCore
from   PySide6                                   import QtGui
from   PySide6                                   import QtWidgets
from   PySide6 . QtCore                          import *
from   PySide6 . QtGui                           import *
from   PySide6 . QtWidgets                       import *
from   AITK    . Qt6                             import *
##############################################################################
from   AITK    . Essentials . Relation           import Relation
from   AITK    . Calendars  . StarDate           import StarDate
from   AITK    . Calendars  . Periode            import Periode
from   AITK    . People     . People             import People
from   AITK    . People     . Faces . FaceShapes import FaceShapes
##############################################################################
class FaceShapeListings        ( TreeDock                                  ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow       = Signal (                                             )
  emitAllNames        = Signal ( dict                                        )
  emitAssignAmounts   = Signal ( str , int , int                             )
  emitPossibleAmounts = Signal ( str , int , int                             )
  PeopleGroup         = Signal ( str , int , str                             )
  ShowPersonalGallery = Signal ( str , int , str ,       QIcon               )
  ShowPersonalIcons   = Signal ( str , int , str , str , QIcon               )
  OpenVariantTables   = Signal ( str , str , int , str , dict                )
  OpenLogHistory      = Signal ( str , str , str , str , str                 )
  emitLog             = Signal ( str                                         )
  ############################################################################
  def __init__                 ( self , parent = None , plan = None        ) :
    ##########################################################################
    super ( ) . __init__       (        parent        , plan                 )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "FaceShapeListings"
    self . FetchTableKey      = "FaceShapeListings"
    self . GType              = 159
    self . SortOrder          = "asc"
    self . JoinRelate         = "Subordination"
    ##########################################################################
    self . SHAPES             = FaceShapes (                                 )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount                  ( 4                               )
    self . setColumnHidden                 ( 1 , True                        )
    self . setColumnHidden                 ( 2 , True                        )
    self . setColumnHidden                 ( 3 , True                        )
    ##########################################################################
    self . setRootIsDecorated              ( False                           )
    self . setAlternatingRowColors         ( True                            )
    ##########################################################################
    self . MountClicked                    ( 1                               )
    self . MountClicked                    ( 2                               )
    ##########################################################################
    self . assignSelectionMode             ( "ExtendedSelection"             )
    ##########################################################################
    self . emitNamesShow       . connect   ( self . show                     )
    self . emitAllNames        . connect   ( self . refresh                  )
    self . emitAssignAmounts   . connect   ( self . AssignAmounts            )
    self . emitPossibleAmounts . connect   ( self . PossibleAmounts          )
    ##########################################################################
    self . setFunction                     ( self . FunctionDocking , True   )
    self . setFunction                     ( self . HavingMenu      , True   )
    ##########################################################################
    self . setAcceptDrops                  ( True                            )
    self . setDragEnabled                  ( True                            )
    self . setDragDropMode                 ( QAbstractItemView . DragDrop    )
    ##########################################################################
    self . setMinimumSize                  ( 80 , 80                         )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 240 , 280 )                       )
  ############################################################################
  def PrepareForActions                    ( self                          ) :
    ##########################################################################
    self . AppendSideActionWithIcon        ( "Crowds"                      , \
                                             ":/images/viewpeople.png"     , \
                                             self . GotoItemCrowd            )
    self . AppendSideActionWithIcon        ( "FaceShapeGallery"            , \
                                             ":/images/gallery.png"        , \
                                             self . GotoItemGallery          )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendToolNamingAction          (                                 )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
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
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    ##########################################################################
    self . Leave . emit      ( self                                          )
    ##########################################################################
    return True
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked              ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery    ( self                                           ) :
    ##########################################################################
    TABLE = self . Tables [ "FaceShapes"                                     ]
    ##########################################################################
    QQ    = f"""select `uuid` from {TABLE}
                where ( `used` >0 )
                order by `id` asc ;"""
    ##########################################################################
    return " " . join     ( QQ . split (                                   ) )
  ############################################################################
  def ObtainsInformation  ( self , DB                                      ) :
    ##########################################################################
    self . ReloadLocality (        DB                                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem           ( self , UUID , NAME , BRUSH                   ) :
    ##########################################################################
    IT   = QTreeWidgetItem  (                                                )
    IT   . setText          ( 0 , NAME                                       )
    IT   . setToolTip       ( 0 , str ( UUID )                               )
    IT   . setData          ( 0 , Qt . UserRole , str ( UUID )               )
    IT   . setTextAlignment ( 1 , Qt . AlignRight                            )
    IT   . setTextAlignment ( 2 , Qt . AlignRight                            )
    ##########################################################################
    for COL in              [ 0 , 1 , 2 , 3                                ] :
      ########################################################################
      IT . setBackground    ( COL , BRUSH                                    )
    ##########################################################################
    return IT
  ############################################################################
  def PossibleAmounts      ( self , UUID , Amounts , Column                ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT in [ False , None ]                        ) :
      return
    ##########################################################################
    IT . setText           ( Column , str ( Amounts )                        )
    ##########################################################################
    return
  ############################################################################
  def ReportPossible                    ( self , UUIDs                     ) :
    ##########################################################################
    time   . sleep                      ( 1.0                                )
    ##########################################################################
    RELTAB = self . Tables              [ "RelationPeople"                   ]
    REL    = Relation                   (                                    )
    REL    . setT1                      ( "FaceShape"                        )
    REL    . setT2                      ( "People"                           )
    REL    . setRelation                ( "Contains"                         )
    ##########################################################################
    DB     = self . ConnectDB           (                                    )
    ##########################################################################
    if                                  ( self . NotOkay ( DB )            ) :
      return
    ##########################################################################
    self   . OnBusy  . emit             (                                    )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                                ( not self . StayAlive             ) :
        continue
      ########################################################################
      REL  . set                        ( "first" , UUID                     )
      CNT  = REL . CountSecond          ( DB , RELTAB                        )
      ########################################################################
      self . emitPossibleAmounts . emit ( str ( UUID ) , CNT , 2             )
    ##########################################################################
    self   . GoRelax . emit             (                                    )
    DB     . Close                      (                                    )
    ##########################################################################
    return
  ############################################################################
  def AssignAmounts        ( self , UUID , Amounts , Column                ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT in [ False , None ]                        ) :
      return
    ##########################################################################
    IT . setText           ( Column , str ( Amounts )                        )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                ( self , UUIDs                       ) :
    ##########################################################################
    time   . sleep                    ( 1.0                                  )
    ##########################################################################
    RELTAB = self . Tables            [ "RelationPeople"                     ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "FaceShape"                          )
    REL    . setT2                    ( "People"                             )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    ##########################################################################
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                              ( not self . StayAlive               ) :
        continue
      ########################################################################
      REL  . set                      ( "first" , UUID                       )
      CNT  = REL . CountSecond        ( DB , RELTAB                          )
      ########################################################################
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT , 1               )
    ##########################################################################
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def RefreshToolTip              ( self , Total                           ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    CNT    = 0
    MOD    = len                  ( self . TreeBrushes                       )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    NAMEs  = JSON                 [ "NAMEs"                                  ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U                                      , \
                                    NAMEs [ U ]                            , \
                                    self . TreeBrushes [ CNT ]               )
      self . addTopLevelItem      ( IT                                       )
      ########################################################################
      CNT  = int                  ( int ( CNT + 1 ) % MOD                    )
    ##########################################################################
    self   . RefreshToolTip       ( len ( UUIDs )                            )
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def loading                        ( self                                ) :
    ##########################################################################
    DB     = self . ConnectDB        (                                       )
    if                               ( DB == None                          ) :
      self . emitNamesShow . emit    (                                       )
      return
    ##########################################################################
    self   . Notify                  ( 3                                     )
    self   . OnBusy  . emit          (                                       )
    self   . setBustle               (                                       )
    ##########################################################################
    FMT    = self . Translations     [ "UI::StartLoading"                    ]
    MSG    = FMT . format            ( self . windowTitle ( )                )
    self   . ShowStatus              ( MSG                                   )
    ##########################################################################
    UUIDs  = self . ObtainsItemUuids ( DB                                    )
    NAMEs  = self . ObtainsUuidNames ( DB , UUIDs                            )
    ##########################################################################
    self   . setVacancy              (                                       )
    self   . GoRelax . emit          (                                       )
    self   . ShowStatus              ( ""                                    )
    DB     . Close                   (                                       )
    ##########################################################################
    if                               ( len ( UUIDs ) <= 0                  ) :
      self . emitNamesShow . emit    (                                       )
      return
    ##########################################################################
    JSON   =                         {  "UUIDs" : UUIDs , "NAMEs" : NAMEs    }
    ##########################################################################
    self   . emitAllNames . emit     ( JSON                                  )
    ##########################################################################
    OKAY   = self . isColumnHidden   ( 1                                     )
    if                               ( not OKAY                            ) :
      VAL  =                         ( UUIDs ,                               )
      self . Go                      ( self . ReportBelongings , VAL         )
    ##########################################################################
    OKAY   = self . isColumnHidden   ( 2                                     )
    if                               ( not OKAY                            ) :
      VAL  =                         ( UUIDs ,                               )
      self . Go                      ( self . ReportPossible   , VAL         )
    ##########################################################################
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "faceshape/uuids"
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
  def allowedMimeTypes     ( self , mime                                   ) :
    ##########################################################################
    formats = "people/uuids;picture/uuids"
    ##########################################################################
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                       ( self                                 , \
                                      sourceWidget                         , \
                                      mimeData                             , \
                                      mousePos                             ) :
    ##########################################################################
    if                              ( self == sourceWidget                 ) :
      return False
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
      item  = self . itemAt         ( mousePos                               )
      if                            ( item in self . EmptySet              ) :
        return False
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      TN    = item . text           (                                        )
      FMT   = self . getMenuItem    ( "CopyingCrowd"                         )
      MSG   = FMT  . format         ( title , CNT , TN                       )
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      item  = self . itemAt         ( mousePos                               )
      if                            ( item in self . EmptySet              ) :
        return False
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      TN    = item . text           (                                        )
      FMT   = self . getMenuItem    ( "GetPictures"                          )
      MSG   = FMT  . format         ( title , CNT , TN                       )
      ########################################################################
      self  . ShowStatus                 ( MSG                               )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving           ( self , sourceWidget , mimeData , mousePos     ) :
    ##########################################################################
    if                     ( self . droppingAction                         ) :
      return False
    ##########################################################################
    if                     ( sourceWidget != self                          ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( mousePos                                        )
    ##########################################################################
    if                     ( atItem in self . EmptySet                     ) :
      return False
    if                     ( atItem . isSelected ( )                       ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop ( self                                              ) :
    return True
  ############################################################################
  def dropPeople               ( self , source , pos , JSOX                ) :
    ##########################################################################
    if                         ( "UUIDs" not in JSOX                       ) :
      return True
    ##########################################################################
    UUIDs  = JSOX              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( pos                                         )
    if                         ( atItem in self . EmptySet                 ) :
      return True
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    self . Go                  ( self . PeopleJoinFaceShape                , \
                                 ( UUID , UUIDs , )                          )
    ##########################################################################
    return True
  ############################################################################
  def PeopleJoinFaceShape       ( self , atUuid , UUIDs                    ) :
    ##########################################################################
    if                          ( len ( UUIDs ) <= 0                       ) :
      return
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return
    ##########################################################################
    self   . OnBusy  . emit     (                                            )
    self   . setBustle          (                                            )
    ##########################################################################
    RELTAB = self . Tables      [ "RelationPeople"                           ]
    ##########################################################################
    REL    = Relation           (                                            )
    REL    . set                ( "first" , atUuid                           )
    REL    . setT1              ( "FaceShape"                                )
    REL    . setT2              ( "People"                                   )
    REL    . setRelation        ( self . JoinRelate                          )
    ##########################################################################
    DB     . LockWrites         ( [ RELTAB                                 ] )
    REL    . Joins              ( DB , RELTAB , UUIDs                        )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    self   . setVacancy         (                                            )
    self   . GoRelax . emit     (                                            )
    DB     . Close              (                                            )
    ##########################################################################
    if                          ( not self . isColumnHidden ( 1 )          ) :
      ########################################################################
      self . emitRestart . emit (                                            )
    ##########################################################################
    return
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures                 ( self , source , pos , JSON            ) :
    ##########################################################################
    HUID , NAME = self . itemAtPos ( pos , 0 , 0                             )
    if                             ( HUID <= 0                             ) :
      return True
    ##########################################################################
    self . Go ( self . PicturesAppending , ( HUID , NAME , JSON , )          )
    ##########################################################################
    return True
  ############################################################################
  def PicturesAppending      ( self , atUuid , NAME , JSON                 ) :
    ##########################################################################
    T1   = "FaceShape"
    TAB  = "RelationPictures"
    ##########################################################################
    self . AppendingPictures (        atUuid , NAME , JSON , TAB , T1        )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard ( False                                         )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 3                              )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage       ( self                                     ) :
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return False
    ##########################################################################
    PAMTAB = self . Tables      [ "Parameters"                               ]
    DB     . LockWrites         ( [ PAMTAB                                 ] )
    ##########################################################################
    self   . SetLocalityByUuid  ( DB                                       , \
                                  PAMTAB                                   , \
                                  0                                        , \
                                  self . GType                             , \
                                  self . ClassTag                            )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    DB     . Close              (                                            )
    self   . emitRestart . emit (                                            )
    ##########################################################################
    return True
  ############################################################################
  def ReloadLocality           ( self , DB                                 ) :
    ##########################################################################
    PAMTAB = self . Tables     [ "Parameters"                                ]
    self   . GetLocalityByUuid ( DB                                        , \
                                 PAMTAB                                    , \
                                 0                                         , \
                                 self . GType                              , \
                                 self . ClassTag                             )
    ##########################################################################
    return
  ############################################################################
  def OpenItemGallery                 ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( 0 , Qt . UserRole                    )
    uuid = int                        ( uuid                                 )
    text = item . text                ( 0                                    )
    icon = self . windowIcon          (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    self . ShowPersonalGallery . emit ( text , self . GType , xsid , icon    )
    ##########################################################################
    return
  ############################################################################
  def GotoItemGallery           ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemGallery    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemCrowd           ( self , item                                ) :
    ##########################################################################
    uuid = item . data        ( 0 , Qt . UserRole                            )
    uuid = int                ( uuid                                         )
    xsid = str                ( uuid                                         )
    text = item . text        ( 0                                            )
    ##########################################################################
    self . PeopleGroup . emit ( text , self . GType , str ( uuid )           )
    ##########################################################################
    return
  ############################################################################
  def GotoItemCrowd             ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemCrowd      ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item                               , \
                                        0                                  , \
                                        "FaceShape"                        , \
                                        "NamesEditing"                       )
    ##########################################################################
    return
  ############################################################################
  def FunctionsMenu                  ( self , mm , uuid , item             ) :
    ##########################################################################
    msg  = self . getMenuItem        ( "Functions"                           )
    LOM  = mm   . addMenu            ( msg                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "AssignTables"                        )
    mm   . addActionFromMenu         ( LOM , 25351301 , msg                  )
    ##########################################################################
    return mm
  ############################################################################
  def RunFunctionsMenu                 ( self , at , uuid , item           ) :
    ##########################################################################
    if                                 ( at == 25351301                    ) :
      ########################################################################
      TITLE = self . windowTitle       (                                     )
      ########################################################################
      self  . OpenVariantTables . emit ( str ( TITLE )                     , \
                                         "0"                               , \
                                         self . GType                      , \
                                         self . FetchTableKey              , \
                                         self . Tables                       )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9003 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      if                           ( ( at in [ 9001 , 9002 ] ) and ( hid ) ) :
        ######################################################################
        self . restart             (                                         )
        ######################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                     ( self , mm , item                    ) :
    ##########################################################################
    if                               ( self . NotOkay ( item )             ) :
      return mm
    ##########################################################################
    TRX  = self . Translations
    NAME = item . text               ( 0                                     )
    FMT  = TRX                       [ "UI::Belongs"                         ]
    MSG  = FMT . format              ( NAME                                  )
    COL  = mm . addMenu              ( MSG                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "CopyFaceShapeUuid"                   )
    mm   . addActionFromMenu         ( COL , 38521001 , msg                  )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "Crowds"                              )
    ICON = QIcon                     ( ":/images/viewpeople.png"             )
    mm   . addActionFromMenuWithIcon ( COL , 38521002 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "FaceIcon"                            )
    ICON = QIcon                     ( ":/images/oneself.png"                )
    mm   . addActionFromMenuWithIcon ( COL , 38521003 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "FaceShapeGallery"                    )
    ICON = QIcon                     ( ":/images/gallery.png"                )
    mm   . addActionFromMenuWithIcon ( COL , 38521004 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "Description"                         )
    mm   . addActionFromMenu         ( COL , 38522001        , msg           )
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
      self . Notify                 ( 5                                      )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38521002                       ) :
      ########################################################################
      self . OpenItemCrowd          ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38521003                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      head = item . text            ( 0                                      )
      icon = self . windowIcon      (                                        )
      xsid = str                    ( uuid                                   )
      relz = "Using"
      ########################################################################
      self . ShowPersonalIcons . emit                                      ( \
                                      head                                 , \
                                      self . GType                         , \
                                      relz                                 , \
                                      xsid                                 , \
                                      icon                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38521004                       ) :
      ########################################################################
      self . OpenItemGallery        ( item                                   )
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
                                      str ( self . getLocality ( ) )         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def JoinsMenu              ( self , mm                                   ) :
    ##########################################################################
    msg = self . getMenuItem ( "JoinMethod"                                  )
    LOM = mm   . addMenu     ( msg                                           )
    ##########################################################################
    CK  =                    ( "Subordination" == self . JoinRelate          )
    msg = self . getMenuItem ( "ConfirmFaceShape"                            )
    mm  . addActionFromMenu  ( LOM , 66471301 , msg , True , CK              )
    ##########################################################################
    CK  =                    ( "Possible"      == self . JoinRelate          )
    msg = self . getMenuItem ( "PossibleFaceShape"                           )
    mm  . addActionFromMenu  ( LOM , 66471302 , msg , True , CK              )
    ##########################################################################
    return mm
  ############################################################################
  def RunJoinsMenu ( self , at                                             ) :
    ##########################################################################
    if             ( at == 66471301                                        ) :
      ########################################################################
      self . JoinRelate = "Subordination"
      ########################################################################
      return True
    ##########################################################################
    if             ( at == 66471302                                        ) :
      ########################################################################
      self . JoinRelate = "Possible"
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def Menu                            ( self , pos                         ) :
    ##########################################################################
    if                                ( not self . isPrepared ( )          ) :
      return False
    ##########################################################################
    doMenu = self . isFunction        ( self . HavingMenu                    )
    if                                ( not doMenu                         ) :
      return False
    ##########################################################################
    self   . Notify                   ( 0                                    )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction      ( mm , 1001                            )
    ## self   . AppendInsertAction       ( mm , 1101                            )
    self   . TryAppendEditNamesAction ( atItem , mm , 1601                   )
    mm     . addSeparator             (                                      )
    ##########################################################################
    self   . FunctionsMenu            ( mm , uuid , atItem                   )
    self   . GroupsMenu               ( mm ,        atItem                   )
    self   . JoinsMenu                ( mm                                   )
    self   . ColumnsMenu              ( mm                                   )
    self   . SortingMenu              ( mm                                   )
    self   . LocalityMenu             ( mm                                   )
    self   . DockingMenu              ( mm                                   )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                  ( self    . menuFont ( )               )
    aa     = mm . exec_               ( QCursor . pos      ( )               )
    at     = mm . at                  ( aa                                   )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    if                                ( self . RunDocking   ( mm , aa )    ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu  ( at , uuid , atItem                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    if                                ( self . HandleLocalityMenu ( at )   ) :
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu    ( at                                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu    ( at                                   )
    if                                ( OKAY                               ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu     ( at , atItem                          )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    OKAY   = self . RunJoinsMenu       ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    ## if                                ( at == 1101                         ) :
    ##   self . InsertItem               (                                      )
    ##   return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor ( at , 1601 , atItem                   )
    if                                ( OKAY                               ) :
      return True
    ##########################################################################
    return True
##############################################################################
