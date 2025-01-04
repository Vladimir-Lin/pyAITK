# -*- coding: utf-8 -*-
##############################################################################
## SexualityListings
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
from   AITK    . Qt6        . MenuManager   import MenuManager   as MenuManager
from   AITK    . Qt6        . MajorListings import MajorListings as MajorListings
##############################################################################
from   AITK    . Essentials . Relation      import Relation
from   AITK    . Calendars  . StarDate      import StarDate
from   AITK    . Calendars  . Periode       import Periode
##############################################################################
class SexualityListings        ( MajorListings                             ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitAssignAmounts   = Signal ( str , int , int                             )
  PeopleGroup         = Signal ( str , int , str                             )
  ShowPersonalGallery = Signal ( str , int , str , QIcon                     )
  OpenLogHistory      = Signal ( str , str , str , str , str                 )
  emitLog             = Signal ( str                                         )
  ############################################################################
  def __init__                 ( self , parent = None , plan = None        ) :
    ##########################################################################
    super ( ) . __init__       (        parent        , plan                 )
    ##########################################################################
    self . ClassTag         = "SexualityListings"
    self . FetchTableKey    = "SexualityListings"
    ##########################################################################
    self . IncludeUndecided = True
    self . GType            = 77
    self . CreatureUuid     = 5431231000000000001
    self . UsedOptions      = [ 1 , 2 , 3 , 4 , 5                            ]
    self . PeopleBtn        = None
    self . NameBtn          = None
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setFunction     ( self . FunctionDocking , True                   )
    self . setFunction     ( self . HavingMenu      , True                   )
    ##########################################################################
    self . setColumnCount  ( 3                                               )
    self . setColumnHidden ( 1 , True                                        )
    self . setColumnHidden ( 2 , True                                        )
    ##########################################################################
    self . setDragEnabled  ( False                                           )
    self . setDragDropMode ( QAbstractItemView . DropOnly                    )
    ##########################################################################
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 240 , 440 )                       )
  ############################################################################
  def PrepareForActions                   ( self                           ) :
    ##########################################################################
    msg  = self . getMenuItem             ( "Crowds"                         )
    A    = QAction                        (                                  )
    IC   = QIcon                          ( ":/images/peoplegroups.png"      )
    A    . setIcon                        ( IC                               )
    A    . setToolTip                     ( msg                              )
    A    . triggered . connect            ( self . GotoItemCrowd             )
    A    . setEnabled                     ( False                            )
    ##########################################################################
    self . PeopleBtn = A
    ##########################################################################
    self . WindowActions . append         ( A                                )
    ##########################################################################
    self . AppendToolNamingAction         (                                  )
    self . NameBtn = self . WindowActions [ -1                               ]
    self . NameBtn . setEnabled           ( False                            )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                       Enabled       ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup      , Enabled         )
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
    self . setActionLabel    ( "Label" , self . windowTitle ( )              )
    self . AttachActions     ( True                                          )
    self . attachActionsTool (                                               )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                 ( self                                      ) :
    ##########################################################################
    if                         ( not self . isPrepared ( )                 ) :
      return True
    ##########################################################################
    if                         ( not self . AtMenu                         ) :
      ########################################################################
      self . AttachActions     ( False                                       )
      self . detachActionsTool (                                             )
    ##########################################################################
    return False
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . defaultCloseEvent ( event                                         )
    ##########################################################################
    return
  ############################################################################
  def SwitchSideTools ( self , Enabled                                     ) :
    ##########################################################################
    if                ( self . PeopleBtn not in self . EmptySet            ) :
      ########################################################################
      self . PeopleBtn . setEnabled ( Enabled                                )
    ##########################################################################
    if                ( self . NameBtn   not in self . EmptySet            ) :
      ########################################################################
      self . NameBtn   . setEnabled ( Enabled                                )
    ##########################################################################
    return
  ############################################################################
  def singleClicked        ( self , item , column                          ) :
    ##########################################################################
    self . Notify          ( 0                                               )
    self . SwitchSideTools ( True                                            )
    ##########################################################################
    return True
  ############################################################################
  def selectionsChanged            ( self                                  ) :
    ##########################################################################
    OKAY = self . isEmptySelection (                                         )
    self . SwitchSideTools         ( OKAY                                    )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery                ( self                               ) :
    ##########################################################################
    TABLE   = self . Tables           [ "Sexuality"                          ]
    LISTs   =                         [ self . CreatureUuid                  ]
    ##########################################################################
    if                                ( self . IncludeUndecided            ) :
      LISTs . append                  ( 0                                    )
    ##########################################################################
    LQ      = " , " . join            ( str(x) for x in LISTs                )
    UQ      = " , " . join            ( str(x) for x in self . UsedOptions   )
    ##########################################################################
    QQ      = f"""select `uuid` from {TABLE}
                  where ( `used` in ( {UQ} ) )
                  and ( `creature` in ( {LQ} ) )
                  order by `id` asc ;"""
    ##########################################################################
    return " " . join                 ( QQ . split ( )                       )
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
    REL    . setT1                    ( "Sexuality"                          )
    REL    . setT2                    ( "People"                             )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    ##########################################################################
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
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
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    NAMEs   = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    JSON    =                         {  "UUIDs" : UUIDs , "NAMEs" : NAMEs   }
    ##########################################################################
    self    . emitAllNames . emit     ( JSON                                 )
    ##########################################################################
    OKAY    = self . isColumnHidden   ( 1                                    )
    if                                ( not OKAY                           ) :
      VAL   =                         ( UUIDs ,                              )
      self  . Go                      ( self . ReportBelongings , VAL        )
    ##########################################################################
    self    . Notify                  ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    ##########################################################################
    formats = "people/uuids"
    ##########################################################################
    return self . MimeType    ( mime , formats                               )
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
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      FMT   = self . getMenuItem    ( "CopyingCrowd"                         )
      MSG   = FMT  . format         ( title , CNT                            )
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
    if                         ( atItem in self . EmptySet                 ) :
      return False
    if                         ( atItem . isSelected ( )                   ) :
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
    if                         ( atItem in [ False , None ]                ) :
      return True
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    self . Go                  ( self . PeopleJoinSexuality                , \
                                 ( UUID , UUIDs , )                          )
    ##########################################################################
    return True
  ############################################################################
  def PeopleJoinSexuality       ( self , atUuid , UUIDs                    ) :
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
    REL    . setT1              ( "Sexuality"                                )
    REL    . setT2              ( "People"                                   )
    REL    . setRelation        ( "Subordination"                            )
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
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "SexualityListings" , 2                          )
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
                                        "Sexuality"                        , \
                                        "NamesEditing"                       )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9002 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      if                           ( ( at in [ 9001 ] ) and ( hid )        ) :
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
    msg  = self . getMenuItem        ( "CopySexualityUuid"                   )
    mm   . addActionFromMenu         ( COL , 38521001 , msg                  )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "Crowds"                              )
    ICON = QIcon                     ( ":/images/viewpeople.png"             )
    mm   . addActionFromMenuWithIcon ( COL , 38521002 , ICON , msg           )
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
  def Menu                         ( self , pos                            ) :
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
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    mm     . addSeparator          (                                         )
    self   . TryAppendEditNamesAction ( atItem , mm , 1601                   )
    ##########################################################################
    self   . GroupsMenu            ( mm ,        atItem                      )
    self   . ColumnsMenu           ( mm                                      )
    self   . SortingMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
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
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor ( at , 1601 , atItem                   )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    return True
##############################################################################
