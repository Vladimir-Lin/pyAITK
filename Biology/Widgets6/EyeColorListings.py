# -*- coding: utf-8 -*-
##############################################################################
## EyeColorListings
## 眼睛瞳色列表元件
##############################################################################
import os
import sys
import time
import requests
import threading
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
from   AITK    . Essentials . Relation     import Relation
from   AITK    . Calendars  . StarDate     import StarDate
from   AITK    . Calendars  . Periode      import Periode
from   AITK    . People     . People       import People
from   AITK    . People     . Eyes . Iris  import Iris
##############################################################################
class EyeColorListings           ( TreeDock                                ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow         = Signal (                                           )
  emitAllNames          = Signal ( list                                      )
  emitAssignAmounts     = Signal ( str , int , int                           )
  emitPossibleAmounts   = Signal ( str , int , int                           )
  PeopleGroup           = Signal ( str , int , str                           )
  ShowPeopleGroupRelate = Signal ( str , int , str , str                     )
  ShowPersonalGallery   = Signal ( str , int , str       , QIcon             )
  ShowPersonalIcons     = Signal ( str , int , str , str , QIcon             )
  ShowGalleries         = Signal ( str , int , str ,       QIcon             )
  ShowLodListings       = Signal ( str , str             , QIcon             )
  ShowIrisEditor        = Signal ( str , str             , QIcon             )
  OpenVariantTables     = Signal ( str , str , int , str , dict              )
  OpenLogHistory        = Signal ( str , str , str , str , str               )
  emitLog               = Signal ( str                                       )
  ############################################################################
  def __init__                   ( self , parent = None , plan = None      ) :
    ##########################################################################
    super ( ) . __init__         (        parent        , plan               )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "EyeColorListings"
    self . FetchTableKey      = "EyeColorListings"
    self . GType              = 19
    self . SortOrder          = "asc"
    self . JoinRelate         = "Subordination"
    ##########################################################################
    self . IRIS               = Iris (                                       )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 4                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 3 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ##########################################################################
    self . emitNamesShow       . connect ( self . show                       )
    self . emitAllNames        . connect ( self . refresh                    )
    self . emitAssignAmounts   . connect ( self . AssignAmounts              )
    self . emitPossibleAmounts . connect ( self . PossibleAmounts            )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    self . setMinimumSize          ( 80 , 80                                 )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 160 , 200 )                       )
  ############################################################################
  def PrepareForActions                    ( self                          ) :
    ##########################################################################
    self . AppendSideActionWithIcon        ( "Crowds"                      , \
                                             ":/images/viewpeople.png"     , \
                                             self . GotoItemCrowd            )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendSideActionWithIcon        ( "EyesGallery"                 , \
                                             ":/images/gallery.png"        , \
                                             self . GotoItemGallery          )
    self . AppendSideActionWithIcon        ( "EyesGalleries"               , \
                                             ":/images/galleries.png"      , \
                                             self . GotoItemGalleries        )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendSideActionWithIcon        ( "IrisEditor"                  , \
                                             ":/images/edit.png"           , \
                                             self . GotoItemEditor           )
    self . AppendSideActionWithIcon        ( "AssignIrisColor"             , \
                                             ":/images/colorgroups.png"    , \
                                             self . GotoIrisColor            )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendToolNamingAction          (                                 )
    self . AppendSideActionWithIcon        ( "LogHistory"                  , \
                                             ":/images/notes.png"          , \
                                             self . GotoItemNote             )
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
  def ObtainUuidsQuery                    ( self                           ) :
    return self . IRIS . ObtainUuidsQuery ( self . Tables [ "Eyes" ]       , \
                                            self . SortOrder                 )
  ############################################################################
  def ObtainsInformation  ( self , DB                                      ) :
    ##########################################################################
    self . ReloadLocality (        DB                                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                 ( self , JSON                            ) :
    ##########################################################################
    UUID = JSON                   [ "Uuid"                                   ]
    NAME = JSON                   [ "Name"                                   ]
    R    = JSON                   [ "R"                                      ]
    G    = JSON                   [ "G"                                      ]
    B    = JSON                   [ "B"                                      ]
    ICON = self . CreateColorIcon ( R , G , B , 24 , 24                      )
    ##########################################################################
    IT   = self . PrepareUuidItem ( 0 , UUID , NAME                          )
    IT   . setIcon                ( 0 , ICON                                 )
    ##########################################################################
    IT   . setTextAlignment       ( 1 , Qt . AlignRight                      )
    IT   . setTextAlignment       ( 2 , Qt . AlignRight                      )
    ##########################################################################
    IT   . setData                ( 3 , Qt . UserRole , JSON                 )
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
  def ReportRelateEyes                    ( self , Relate , UUIDs          ) :
    ##########################################################################
    time     . sleep                      ( 1.0                              )
    ##########################################################################
    RELTAB   = self . Tables              [ "RelationPeople"                 ]
    ##########################################################################
    DB       = self . ConnectDB           (                                  )
    ##########################################################################
    if                                    ( self . NotOkay ( DB )          ) :
      return
    ##########################################################################
    self     . OnBusy  . emit             (                                  )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                                  ( not self . StayAlive           ) :
        continue
      ########################################################################
      CNT    = self . IRIS . CountIrisPeopleTotal                            (
                                            DB                             , \
                                            RELTAB                         , \
                                            UUID                           , \
                                            Relate                           )
      ########################################################################
      if                                  ( Relate in [ "Possible"       ] ) :
        self . emitPossibleAmounts . emit ( str ( UUID ) , CNT , 2           )
      else                                                                   :
        self . emitAssignAmounts   . emit ( str ( UUID ) , CNT , 1           )
    ##########################################################################
    self     . GoRelax . emit             (                                  )
    DB       . Close                      (                                  )
    ##########################################################################
    return
  ############################################################################
  def ReportPossibleEyes    ( self       , UUIDs                           ) :
    ##########################################################################
    self . ReportRelateEyes ( "Possible" , UUIDs                             )
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
  def ReportBelongings      ( self , UUIDs                                 ) :
    ##########################################################################
    self . ReportRelateEyes ( "Subordination" , UUIDs                        )
    ##########################################################################
    return
  ############################################################################
  def refresh                     ( self , LISTs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    for JSON in LISTs                                                        :
      ########################################################################
      IT   = self . PrepareItem   ( JSON                                     )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def LoadEyesListings                     ( self , DB                     ) :
    ##########################################################################
    LISTs  =                               [                                 ]
    UUIDs  = self . ObtainsItemUuids       ( DB                              )
    ##########################################################################
    if                                     ( len ( UUIDs ) <= 0            ) :
      return LISTs
    ##########################################################################
    EYETAB = self . Tables                 [ "Eyes"                          ]
    NAMEs  = self . ObtainsUuidNames       ( DB ,          UUIDs             )
    LISTs  = self . IRIS . QueryAllDetails ( DB , EYETAB , UUIDs , NAMEs     )
    ##########################################################################
    self   . IRIS . UUIDs = UUIDs
    self   . IRIS . NAMEs = NAMEs
    self   . IRIS . LISTs = LISTs
    ##########################################################################
    return                                 ( UUIDs , LISTs ,                 )
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
    UUIDs , LISTs = self . LoadEyesListings ( DB                             )
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
      self        . Go                      ( self . ReportPossibleEyes , VAL )
    ##########################################################################
    self          . Notify                  ( 5                              )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "eyes/uuids"
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
  def allowedMimeTypes                ( self , mime                        ) :
    ##########################################################################
    FMTs =                            [ "people/uuids"                     , \
                                        "gallery/uuids"                    , \
                                        "picture/uuids"                      ]
    ##########################################################################
    return self . MimeTypeFromFormats ( mime , FMTs                          )
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
      ########################################################################
      return
    ##########################################################################
    elif                                 ( mtype in [ "gallery/uuids" ]    ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "GetGalleries"                    )
      MSG   = FMT  . format              ( title , CNT , NAME                )
      ########################################################################
      self  . ShowStatus                 ( MSG                               )
      ########################################################################
      return
    ##########################################################################
    elif                                 ( mtype in [ "picture/uuids" ]    ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "GetPictures"                     )
      MSG   = FMT  . format              ( title , CNT , NAME                )
      ########################################################################
      self  . ShowStatus                 ( MSG                               )
      ########################################################################
      return
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
  def PeopleAppending              ( self , atUuid , NAME , JSON           ) :
    ##########################################################################
    UUIDs  = JSON                  [ "UUIDs"                                 ]
    if                             ( len ( UUIDs ) <= 0                    ) :
      return
    ##########################################################################
    DB     = self . ConnectDB      (                                         )
    if                             ( self . NotOkay ( DB )                 ) :
      return
    ##########################################################################
    self   . OnBusy  . emit        (                                         )
    self   . setBustle             (                                         )
    ##########################################################################
    RELTAB = self . Tables         [ "RelationPeople"                        ]
    ##########################################################################
    DB     . LockWrites            ( [ RELTAB                              ] )
    self   . IRIS . CrowdsJoinIris ( DB                                    , \
                                     RELTAB                                , \
                                     atUuid                                , \
                                     UUIDs                                 , \
                                     self . JoinRelate                       )
    DB     . UnlockTables          (                                         )
    ##########################################################################
    self   . setVacancy            (                                         )
    self   . GoRelax . emit        (                                         )
    DB     . Close                 (                                         )
    ##########################################################################
    RR     =                       ( not self . isColumnHidden ( 1 )         )
    ##########################################################################
    if                             ( not self . isColumnHidden ( 2 )       ) :
      RR   = True
    ##########################################################################
    if                             ( RR                                    ) :
      ########################################################################
      self . emitRestart . emit    (                                         )
    ##########################################################################
    REA    = self    . getMenuItem ( "ConfirmEyeColor"                       )
    ##########################################################################
    if                             ( self . JoinRelate in [ "Possible"   ] ) :
       REA = self    . getMenuItem ( "PossibleEyeColor"                      )
    ##########################################################################
    FMT    = self    . getMenuItem ( "JoinCrowdsToIris"                      )
    MSG    = FMT     . format      ( len ( CNT ) , NAME , RENA               )
    self   . emitLog . emit        ( MSG                                     )
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
    T1   = "Eyes"
    TAB  = "RelationPictures"
    ##########################################################################
    self . AppendingPictures (        atUuid , NAME , JSON , TAB , T1        )
    ##########################################################################
    return
  ############################################################################
  def acceptGalleriesDrop ( self                                           ) :
    return True
  ############################################################################
  def dropGalleries                ( self , source , pos , JSON            ) :
    ##########################################################################
    HUID , NAME = self . itemAtPos ( pos , 0 , 0                             )
    if                             ( HUID <= 0                             ) :
      return True
    ##########################################################################
    UUIDs       = JSON             [ "UUIDs"                                 ]
    if                             ( len ( UUIDs ) <= 0                    ) :
      return True
    ##########################################################################
    ## 從外部加入
    ##########################################################################
    VAL         =                  ( HUID , NAME , UUIDs ,                   )
    self        . Go               ( self . GalleriesAppending , VAL         )
    ##########################################################################
    return True
  ############################################################################
  def GalleriesAppending              ( self , atUuid , NAME , UUIDs       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    self   . setBustle                (                                      )
    ##########################################################################
    RELTAB = self . Tables            [ "RelationPeople"                     ]
    ##########################################################################
    DB     . LockWrites               ( [ RELTAB                           ] )
    self   . IRIS . GalleriesJoinIris ( DB , RELTAB , atUuid , UUIDs         )
    DB     . UnlockTables             (                                      )
    ##########################################################################
    self   . setVacancy               (                                      )
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    ##########################################################################
    FMT    = self . getMenuItem       ( "JoinGalleriesToIris"                )
    MSG    = FMT . format             ( len ( CNT ) , NAME                   )
    self   . emitLog . emit           ( MSG                                  )
    ##########################################################################
    return
  ############################################################################
  def UpdateIrisColor           ( self , UUID , R , G , B                  ) :
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return
    ##########################################################################
    EYETAB = self . Tables      [ "Eyes"                                     ]
    ##########################################################################
    DB     . LockWrites         ( [ EYETAB                                 ] )
    self   . IRIS . UpdateColor ( DB , EYETAB , UUID , R , G , B             )
    DB     . UnlockTables       (                                            )
    ##########################################################################
    DB     . Close              (                                            )
    self   . emitRestart . emit (                                            )
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
  def OpenItemGalleries         ( self , item                              ) :
    ##########################################################################
    uuid = item . data          ( 0 , Qt . UserRole                          )
    uuid = int                  ( uuid                                       )
    text = item . text          ( 0                                          )
    icon = self . windowIcon    (                                            )
    xsid = str                  ( uuid                                       )
    ##########################################################################
    self . ShowGalleries . emit ( text , self . GType , xsid , icon          )
    ##########################################################################
    return
  ############################################################################
  def GotoItemGalleries         ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemGalleries  ( atItem                                     )
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
  def OpenItemPossibleCrowd             ( self , item                      ) :
    ##########################################################################
    uuid = item . data                  ( 0 , Qt . UserRole                  )
    uuid = int                          ( uuid                               )
    xsid = str                          ( uuid                               )
    text = item . text                  ( 0                                  )
    relz = "Possible"
    ##########################################################################
    self . ShowPeopleGroupRelate . emit ( text , self . GType , xsid , relz  )
    ##########################################################################
    return
  ############################################################################
  def OpenItemEditor             ( self , item                             ) :
    ##########################################################################
    uuid = item . data           ( 0 , Qt . UserRole                         )
    uuid = int                   ( uuid                                      )
    head = item . text           ( 0                                         )
    icon = self . windowIcon     (                                           )
    xsid = str                   ( uuid                                      )
    ##########################################################################
    self . ShowIrisEditor . emit ( head , xsid , icon                        )
    ##########################################################################
    return
  ############################################################################
  def GotoItemEditor            ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemEditor     ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNote               ( self , item                             ) :
    ##########################################################################
    uuid = item . data           ( 0 , Qt . UserRole                         )
    uuid = int                   ( uuid                                      )
    head = item . text           ( 0                                         )
    nx   = ""
    ##########################################################################
    if                           ( "Notes" in self . Tables                ) :
      nx = self . Tables         [ "Notes"                                   ]
    ##########################################################################
    self . OpenLogHistory . emit ( head                                    , \
                                   str ( uuid )                            , \
                                   "Description"                           , \
                                   nx                                      , \
                                   str ( self . getLocality ( ) )            )
    ##########################################################################
    return
  ############################################################################
  def GotoItemNote              ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemNote       ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item , 0 , "Eyes" , "NamesEditing"   )
    ##########################################################################
    return
  ############################################################################
  def AssignIrisColor              ( self , item                           ) :
    ##########################################################################
    if                             ( self . NotOkay ( item )               ) :
      return
    ##########################################################################
    T    = self . getMenuItem      ( "AssignIrisColor"                       )
    JS   = item . data             ( 3 , Qt . UserRole                       )
    RR   = JS                      [ "R"                                     ]
    GG   = JS                      [ "G"                                     ]
    BB   = JS                      [ "B"                                     ]
    CC   = QColor                  ( RR , GG , BB                            )
    ##########################################################################
    X    = QColorDialog . getColor ( CC , self , T                           )
    ##########################################################################
    uuid = item . data             ( 0 , Qt . UserRole                       )
    uuid = int                     ( uuid                                    )
    ##########################################################################
    XR   = X . red                 (                                         )
    XG   = X . green               (                                         )
    XB   = X . blue                (                                         )
    ##########################################################################
    if ( ( RR == XR ) and ( GG == XG ) and ( BB == XB ) )                    :
      return
    ##########################################################################
    VAL  =                         ( uuid , XR , XG , XB ,                   )
    self . Go                      ( self . UpdateIrisColor , VAL            )
    ##########################################################################
    return
  ############################################################################
  def GotoIrisColor             ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . AssignIrisColor    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard ( False                                         )
    ##########################################################################
    return
  ############################################################################
  def CopyUuidToClipboard         ( self , item                            ) :
    ##########################################################################
    uuid = item . data            ( 0 , Qt . UserRole                        )
    uuid = int                    ( uuid                                     )
    qApp . clipboard ( ). setText ( f"{uuid}"                                )
    self . Notify                 ( 5                                        )
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
    msg  = self . getMenuItem        ( "CopyEyesUuid"                        )
    mm   . addActionFromMenu         ( COL , 38521001 , msg                  )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "EyeModel"                            )
    ICON = QIcon                     ( ":/images/model.png"                  )
    mm   . addActionFromMenuWithIcon ( COL , 38522001 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "IrisEditor"                          )
    ICON = QIcon                     ( ":/images/edit.png"                   )
    mm   . addActionFromMenuWithIcon ( COL , 38522002 , ICON , msg           )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "EyesIcon"                            )
    ICON = QIcon                     ( ":/images/oneself.png"                )
    mm   . addActionFromMenuWithIcon ( COL , 38523001 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "EyesGallery"                         )
    ICON = QIcon                     ( ":/images/gallery.png"                )
    mm   . addActionFromMenuWithIcon ( COL , 38523002 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "EyesGalleries"                       )
    ICON = QIcon                     ( ":/images/galleries.png"              )
    mm   . addActionFromMenuWithIcon ( COL , 38523003 , ICON , msg           )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "Crowds"                              )
    ICON = QIcon                     ( ":/images/viewpeople.png"             )
    mm   . addActionFromMenuWithIcon ( COL , 38523004 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "PossibleCrowds"                      )
    mm   . addActionFromMenu         ( COL , 38523005        , msg           )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "AssignIrisColor"                     )
    ICON = QIcon                     ( ":/images/colorgroups.png"            )
    mm   . addActionFromMenuWithIcon ( COL , 38524001 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "ColorGroup"                          )
    mm   . addActionFromMenu         ( COL , 38524002        , msg           )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "Description"                         )
    ICON = QIcon                     ( ":/images/notes.png"                  )
    mm   . addActionFromMenuWithIcon ( COL , 38525001 , ICON , msg           )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , item                     ) :
    ##########################################################################
    if                              ( at == 38521001                       ) :
      ########################################################################
      self . CopyUuidToClipboard    ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38522001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      head = item . text            ( 0                                      )
      icon = self . windowIcon      (                                        )
      xsid = str                    ( uuid                                   )
      ########################################################################
      self . ShowLodListings . emit ( head , str ( uuid ) , icon             )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38522002                       ) :
      ########################################################################
      self . GotoItemEditor         ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38523001                       ) :
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
    if                              ( at == 38523002                       ) :
      ########################################################################
      self . OpenItemGallery        ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38523003                       ) :
      ########################################################################
      self . OpenItemGalleries      ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38523004                       ) :
      ########################################################################
      self . OpenItemCrowd          ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38523005                       ) :
      ########################################################################
      self . OpenItemPossibleCrowd  ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38524001                       ) :
      ########################################################################
      self . AssignIrisColor        ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38524002                       ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38525001                       ) :
      ########################################################################
      self . GotoItemNote           ( item                                   )
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
    msg = self . getMenuItem ( "ConfirmEyeColor"                             )
    mm  . addActionFromMenu  ( LOM , 66471301 , msg , True , CK              )
    ##########################################################################
    CK  =                    ( "Possible"      == self . JoinRelate          )
    msg = self . getMenuItem ( "PossibleEyeColor"                            )
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
