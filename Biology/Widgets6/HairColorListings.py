# -*- coding: utf-8 -*-
##############################################################################
## HairColorListings
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
from   AITK    . Essentials . Relation      import Relation
from   AITK    . Calendars  . StarDate      import StarDate
from   AITK    . Calendars  . Periode       import Periode
from   AITK    . People     . People        import People
from   AITK    . People     . Hairs . Hairs import Hairs
##############################################################################
class HairColorListings        ( TreeDock                                  ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow       = Signal (                                             )
  emitAllNames        = Signal ( list                                        )
  emitAssignAmounts   = Signal ( str , int , int                             )
  emitDyeAmounts      = Signal ( str , int , int                             )
  PeopleGroup         = Signal ( str , int , str                             )
  ShowPersonalGallery = Signal ( str , int , str , QIcon                     )
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
    self . ClassTag           = "HairColorListings"
    self . FetchTableKey      = "HairColorListings"
    self . GType              = 20
    self . SortOrder          = "asc"
    self . JoinRelate         = "Subordination"
    ##########################################################################
    self . HAIRS              = Hairs  (                                     )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount              ( 5                                   )
    self . setColumnHidden             ( 1 , True                            )
    self . setColumnHidden             ( 2 , True                            )
    self . setColumnHidden             ( 3 , True                            )
    self . setColumnHidden             ( 4 , True                            )
    ##########################################################################
    self . setRootIsDecorated          ( False                               )
    self . setAlternatingRowColors     ( True                                )
    ##########################################################################
    self . MountClicked                ( 1                                   )
    self . MountClicked                ( 2                                   )
    ##########################################################################
    self . assignSelectionMode         ( "ExtendedSelection"                 )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
    self . emitDyeAmounts    . connect ( self . DyeAmounts                   )
    ##########################################################################
    self . setFunction                 ( self . FunctionDocking , True       )
    self . setFunction                 ( self . HavingMenu      , True       )
    ##########################################################################
    self . setAcceptDrops              ( True                                )
    self . setDragEnabled              ( True                                )
    self . setDragDropMode             ( QAbstractItemView . DragDrop        )
    ##########################################################################
    self . setMinimumSize              ( 80 , 80                             )
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
    self . AppendSideActionWithIcon        ( "HairGallery"                 , \
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
  def ObtainUuidsQuery      ( self                                         ) :
    ##########################################################################
    HAIRTAB = self . Tables [ "Hairs"                                        ]
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"select `uuid` from {HAIRTAB} order by `id` {ORDER} ;"
    ##########################################################################
    return QQ
  ############################################################################
  def ObtainsInformation  ( self , DB                                      ) :
    ##########################################################################
    self . ReloadLocality (        DB                                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                 ( self , JSON , BRUSH                    ) :
    ##########################################################################
    UUID = JSON                   [ "Uuid"                                   ]
    NAME = JSON                   [ "Name"                                   ]
    IDF  = JSON                   [ "Identifier"                             ]
    R    = JSON                   [ "R"                                      ]
    G    = JSON                   [ "G"                                      ]
    B    = JSON                   [ "B"                                      ]
    ICON = self . CreateColorIcon ( R , G , B , 24 , 24                      )
    ##########################################################################
    IT   = self . PrepareUuidItem ( 0 , UUID , NAME                          )
    IT   . setIcon                ( 0 , ICON                                 )
    ##########################################################################
    IT   . setText                ( 1 , IDF                                  )
    IT   . setTextAlignment       ( 2 , Qt . AlignRight                      )
    IT   . setTextAlignment       ( 3 , Qt . AlignRight                      )
    ##########################################################################
    IT   . setData                ( 4 , Qt . UserRole , JSON                 )
    ##########################################################################
    for COL in                    [ 0 , 1 , 2 , 3                          ] :
      ########################################################################
      IT . setBackground          ( COL , BRUSH                              )
    ##########################################################################
    return IT
  ############################################################################
  def DyeAmounts           ( self , UUID , Amounts , Column                ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT in [ False , None ]                        ) :
      return
    ##########################################################################
    IT . setText           ( Column , str ( Amounts )                        )
    ##########################################################################
    return
  ############################################################################
  def ReportDyeHairs               ( self , UUIDs                          ) :
    ##########################################################################
    time   . sleep                 ( 1.0                                     )
    ##########################################################################
    RELTAB = self . Tables         [ "RelationPeople"                        ]
    REL    = Relation              (                                         )
    REL    . setT1                 ( "Hairs"                                 )
    REL    . setT2                 ( "People"                                )
    REL    . setRelation           ( "Contains"                              )
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    ##########################################################################
    if                             ( self . NotOkay ( DB )                 ) :
      return
    ##########################################################################
    self   . OnBusy  . emit        (                                         )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                           ( not self . StayAlive                  ) :
        continue
      ########################################################################
      REL  . set                   ( "first" , UUID                          )
      CNT  = REL . CountSecond     ( DB , RELTAB                             )
      ########################################################################
      self . emitDyeAmounts . emit ( str ( UUID ) , CNT , 3                  )
    ##########################################################################
    self   . GoRelax . emit        (                                         )
    DB     . Close                 (                                         )
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
    REL    . setT1                    ( "Hairs"                              )
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
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT , 2               )
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
  def refresh                     ( self , LISTs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    CNT    = 0
    MOD    = len                  ( self . TreeBrushes                       )
    ##########################################################################
    for JSON in LISTs                                                        :
      ########################################################################
      IT   = self . PrepareItem   ( JSON , self . TreeBrushes [ CNT ]        )
      self . addTopLevelItem      ( IT                                       )
      ########################################################################
      CNT  = int                  ( int ( CNT + 1 ) % MOD                    )
    ##########################################################################
    self   . RefreshToolTip       ( len ( LISTs )                            )
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def LoadHairListings                ( self , DB                          ) :
    ##########################################################################
    LISTs   =                         [                                      ]
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return LISTs
    ##########################################################################
    HAIRTAB = self . Tables           [ "Hairs"                              ]
    NAMEs   = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select `id`,`name`,`formula`,`parameter`,`R`,`G`,`B` from {HAIRTAB}
                 where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      if                              ( self . NotOkay ( RR )              ) :
        continue
      ########################################################################
      if                              ( len ( RR ) != 7                    ) :
        continue
      ########################################################################
      ID    = int                     ( RR [ 0                             ] )
      NA    = self . assureString     ( RR [ 1                             ] )
      FM    = int                     ( RR [ 2                             ] )
      PA    = float                   ( RR [ 3                             ] )
      R     = int                     ( RR [ 4                             ] )
      G     = int                     ( RR [ 5                             ] )
      B     = int                     ( RR [ 6                             ] )
      ########################################################################
      J     =                         { "Id"         : ID                  , \
                                        "Uuid"       : UUID                , \
                                        "Name"       : NAMEs [ UUID ]      , \
                                        "Identifier" : NA                  , \
                                        "Formula"    : FM                  , \
                                        "Parameter"  : PA                  , \
                                        "R"          : R                   , \
                                        "G"          : G                   , \
                                        "B"          : B                     }
      LISTs . append                  ( J                                    )
    ##########################################################################
    return UUIDs , LISTs
  ############################################################################
  def loading                               ( self                         ) :
    ##########################################################################
    DB            = self . ConnectDB        (                                )
    if                                      ( self . NotOkay ( DB )        ) :
      self        . emitNamesShow . emit    (                                )
      return
    ##########################################################################
    self          . Notify                  ( 3                              )
    self          . OnBusy  . emit          (                                )
    self          . setBustle               (                                )
    ##########################################################################
    FMT           = self . Translations     [ "UI::StartLoading"             ]
    MSG           = FMT . format            ( self . windowTitle ( )         )
    self          . ShowStatus              ( MSG                            )
    ##########################################################################
    self          . ObtainsInformation      ( DB                             )
    UUIDs , LISTs = self . LoadHairListings ( DB                             )
    ##########################################################################
    self          . setVacancy              (                                )
    self          . GoRelax . emit          (                                )
    self          . ShowStatus              ( ""                             )
    DB            . Close                   (                                )
    ##########################################################################
    if                                      ( len ( LISTs ) <= 0           ) :
      self        . emitNamesShow . emit    (                                )
      return
    ##########################################################################
    self          . emitAllNames  . emit    ( LISTs                          )
    ##########################################################################
    OKAY          = self . isColumnHidden   ( 1                              )
    if                                      ( not OKAY                     ) :
      VAL         =                         ( UUIDs ,                        )
      self        . Go                      ( self . ReportBelongings , VAL  )
    ##########################################################################
    OKAY          = self . isColumnHidden   ( 2                              )
    if                                      ( not OKAY                     ) :
      VAL         =                         ( UUIDs ,                        )
      self        . Go                      ( self . ReportDyeHairs , VAL    )
    ##########################################################################
    self          . Notify                  ( 5                              )
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
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "hairs/uuids"
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
  def DecideDropItems                    ( self                            , \
                                           sourceWidget                    , \
                                           mtype                           , \
                                           UUIDs                           , \
                                           HUID                            , \
                                           NAME                            ) :
    ##########################################################################
    if                                   ( mtype in [ "people/uuids" ]     ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "Copying"                         )
      MSG   = FMT  . format              ( title , CNT , NAME                )
      ########################################################################
      self  . ShowStatus                 ( MSG                               )
    ##########################################################################
    elif                                 ( mtype in [ "picture/uuids" ]    ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "GetPictures"                     )
      MSG   = FMT  . format              ( title , CNT , NAME                )
      ########################################################################
      self  . ShowStatus                 ( MSG                               )
    ##########################################################################
    return
  ############################################################################
  def HandleDropIn                      ( self                             , \
                                          sourceWidget                     , \
                                          mimeData                         , \
                                          mousePos                         , \
                                          Newbie                           ) :
    ##########################################################################
    if                                  ( self == sourceWidget             ) :
      return False
    ##########################################################################
    GDN         = False
    RDN         = False
    if                                  ( Newbie                           ) :
      GDN       = True
    elif                                ( "Mime" not in self . DropInJSON  ) :
      GDN       = True
    else                                                                     :
      RDN       = True
    ##########################################################################
    if                                  ( GDN                              ) :
      ########################################################################
      RDN       = self . RegularDropNew ( mimeData                           )
      if                                ( not RDN                          ) :
        return False
    ##########################################################################
    HUID , NAME = self . itemAtPos      ( mousePos , 0 , 0                   )
    if                                  ( HUID <= 0                        ) :
      return False
    ##########################################################################
    mtype       = self . DropInJSON     [ "Mime"                             ]
    UUIDs       = self . DropInJSON     [ "UUIDs"                            ]
    ##########################################################################
    self        . DecideDropItems       ( sourceWidget                     , \
                                          mtype                            , \
                                          UUIDs                            , \
                                          HUID                             , \
                                          NAME                               )
    ##########################################################################
    return RDN
  ############################################################################
  def dropNew                  ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    return self . HandleDropIn ( sourceWidget , mimeData , mousePos , True   )
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    return self . HandleDropIn ( sourceWidget , mimeData , mousePos , False  )
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople                   ( self , source , pos , JSOX            ) :
    ##########################################################################
    HUID , NAME = self . itemAtPos ( pos , 0 , 0                             )
    if                             ( HUID <= 0                             ) :
      return True
    ##########################################################################
    ## 從外部加入
    ##########################################################################
    VAL         =                  ( HUID , NAME , JSOX ,                    )
    self        . Go               ( self . PeopleAppending , VAL            )
    ##########################################################################
    return True
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
  def PeopleAppending           ( self , atUuid , NAME , JSON              ) :
    ##########################################################################
    UUIDs  = JSON               [ "UUIDs"                                    ]
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
    REL    . setT1              ( "Hairs"                                    )
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
    RR     =                    ( not self . isColumnHidden ( 1 )            )
    ##########################################################################
    if                          ( not self . isColumnHidden ( 2 )          ) :
      RR   = True
    ##########################################################################
    if                          ( RR                                       ) :
      ########################################################################
      self . emitRestart . emit (                                            )
    ##########################################################################
    return
  ############################################################################
  def PicturesAppending      ( self , atUuid , NAME , JSON                 ) :
    ##########################################################################
    T1   = "Hairs"
    TAB  = "RelationPictures"
    ##########################################################################
    self . AppendingPictures (        atUuid , NAME , JSON , TAB , T1        )
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
    self . defaultOpenItemNamesEditor ( item , 0 , "Hairs" , "NamesEditing"  )
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
    self . defaultPrepare ( self . ClassTag , 4                              )
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
    if                             ( at >= 9001 ) and ( at <= 9004 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      if                           ( ( at in [ 9002 , 9003 ] ) and ( hid ) ) :
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
    msg  = self . getMenuItem        ( "CopyHairUuid"                        )
    mm   . addActionFromMenu         ( COL , 38521001 , msg                  )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "HairGallery"                         )
    ICON = QIcon                     ( ":/images/gallery.png"                )
    mm   . addActionFromMenuWithIcon ( COL , 38521002 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "Crowds"                              )
    ICON = QIcon                     ( ":/images/viewpeople.png"             )
    mm   . addActionFromMenuWithIcon ( COL , 38521003 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "ColorGroup"                          )
    mm   . addActionFromMenu         ( COL , 38521004        , msg           )
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
      self . OpenItemGallery        ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38521003                       ) :
      ########################################################################
      self . OpenItemCrowd          ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38521004                       ) :
      ########################################################################
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
    msg = self . getMenuItem ( "OriginalHairColor"                           )
    mm  . addActionFromMenu  ( LOM , 66471301 , msg , True , CK              )
    ##########################################################################
    CK  =                    ( "Contains"      == self . JoinRelate          )
    msg = self . getMenuItem ( "DyeHairColor"                                )
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
      self . JoinRelate = "Contains"
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    if                                 ( not self . isPrepared ( )         ) :
      return False
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager               ( self                                )
    ##########################################################################
    self   . AppendRefreshAction       (          mm , 1001                  )
    self   . TryAppendEditNamesAction  ( atItem , mm , 1601                  )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . FunctionsMenu             ( mm , uuid , atItem                  )
    self   . GroupsMenu                ( mm ,        atItem                  )
    self   . JoinsMenu                 ( mm                                  )
    self   . ColumnsMenu               ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu   ( at , uuid , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu     ( at                                  )
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
    OKAY   = self . RunGroupsMenu      ( at , atItem                         )
    if                                 ( OKAY                              ) :
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
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    return True
##############################################################################
