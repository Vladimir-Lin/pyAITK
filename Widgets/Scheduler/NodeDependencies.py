# -*- coding: utf-8 -*-
##############################################################################
## NodeDependencies
## 節點相依性
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
from   PyQt5 . QtCore                 import QDateTime
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QDateTimeEdit
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . TreeDock          import TreeDock    as TreeDock
##############################################################################
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
from   AITK  . Scheduler  . Project   import Project     as Project
from   AITK  . Scheduler  . Projects  import Projects    as Projects
from   AITK  . Scheduler  . Task      import Task        as Task
from   AITK  . Scheduler  . Tasks     import Tasks       as Tasks
from   AITK  . Scheduler  . Event     import Event       as Event
from   AITK  . Scheduler  . Events    import Events      as Events
##############################################################################
class NodeDependencies             ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
  updateTitle   = pyqtSignal       (                                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ClassTag           = "NodeDependencies"
    self . SortOrder          = "asc"
    self . AssignedTitle      = ""
    self . DoResizeColumns    = True
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Prerequisite = Relation     (                                     )
    self . Prerequisite . setRelation  ( "Prerequisite"                      )
    ##########################################################################
    self . Successor    = Relation     (                                     )
    self . Successor    . setRelation  ( "Successor"                         )
    ##########################################################################
    self . setColumnCount          ( 8                                       )
    self . setColumnHidden         ( 7 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    self . updateTitle   . connect ( self . changeWindowTitle                )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 800 , 400 )                       )
  ############################################################################
  def asPrerequisite                  ( self                               ) :
    ##########################################################################
    self . Prerequisite . setRelation ( "Prerequisite"                       )
    self . Successor    . setRelation ( "Successor"                          )
    ##########################################################################
    return
  ############################################################################
  def asSuccessor                     ( self                               ) :
    ##########################################################################
    self . Prerequisite . setRelation ( "Successor"                          )
    self . Successor    . setRelation ( "Prerequisite"                       )
    ##########################################################################
    return
  ############################################################################
  def setRequirement        ( self , require                               ) :
    ##########################################################################
    if                      ( require == 31                                ) :
      self . asPrerequisite (                                                )
    elif                    ( require == 32                                ) :
      self . asSuccessor    (                                                )
    ##########################################################################
    return
  ############################################################################
  def setOwner                ( self     , TypeId , Uuid                   ) :
    ##########################################################################
    self . Prerequisite . set ( "t1"     , TypeId                            )
    self . Prerequisite . set ( "first"  , Uuid                              )
    ##########################################################################
    self . Successor    . set ( "t2"     , TypeId                            )
    self . Successor    . set ( "second" , Uuid                              )
    ##########################################################################
    return
  ############################################################################
  def assignWindowTitle      ( self , Title                                ) :
    ##########################################################################
    self . AssignedTitle = Title
    self . changeWindowTitle (                                               )
    ##########################################################################
    return
  ############################################################################
  def changeWindowTitle                 ( self                             ) :
    ##########################################################################
    REL     = self . Prerequisite . get ( "relation"                         )
    REL     = int                       ( REL                                )
    TFMT    = self . getMenuItem        ( "TitleFormat"                      )
    ##########################################################################
    if                                  ( REL == 31                        ) :
      MSG   = self . getMenuItem        ( "Prerequisite"                     )
      title = TFMT . format             ( self . AssignedTitle , MSG         )
    elif                                ( REL == 32                        ) :
      MSG   = self . getMenuItem        ( "Successor"                        )
      title = TFMT . format             ( self . AssignedTitle , MSG         )
    else                                                                     :
      title = self . AssignedTitle
    ##########################################################################
    self    . setWindowTitle            ( title                              )
    ##########################################################################
    return
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup                   )
    self . LinkAction      ( "Delete"     , self . DeleteItems               )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard           )
    self . LinkAction      ( "SelectAll"  , self . SelectAll                 )
    self . LinkAction      ( "SelectNone" , self . SelectNone                )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut ( self                                                      ) :
    ##########################################################################
    if         ( not self . isPrepared ( )                                 ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    self     . Notify         ( 0                                            )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    return
  ############################################################################
  def DurationSTR              ( self , START , FINISH                     ) :
    ##########################################################################
    TRX  = self . Translations [ self . ClassTag ] [ "Units"                 ]
    SFMT = TRX                 [ "Second"                                    ]
    MFMT = TRX                 [ "Minute"                                    ]
    HFMT = TRX                 [ "Hour"                                      ]
    DFMT = TRX                 [ "Day"                                       ]
    ##########################################################################
    DT   = int                 ( FINISH - START                              )
    RR   = int                 ( DT % 60                                     )
    DT   = int                 ( DT / 60                                     )
    SS   = SFMT . format       ( RR                                          )
    ##########################################################################
    if                         ( DT <= 0                                   ) :
      return SS
    ##########################################################################
    RR   = int                 ( DT % 60                                     )
    DT   = int                 ( DT / 60                                     )
    MM   = MFMT . format       ( RR                                          )
    SS   = f"{MM}{SS}"
    ##########################################################################
    if                         ( DT <= 0                                   ) :
      return SS
    ##########################################################################
    RR   = int                 ( DT % 24                                     )
    DT   = int                 ( DT / 24                                     )
    HH   = HFMT . format       ( RR                                          )
    SS   = f"{HH}{SS}"
    ##########################################################################
    if                         ( DT <= 0                                   ) :
      return SS
    ##########################################################################
    DD   = DFMT . format       ( RR                                          )
    SS   = f"{DD}{SS}"
    ##########################################################################
    return SS
  ############################################################################
  def PrepareItemContent           ( self , IT , JSON                      ) :
    ##########################################################################
    TZ       = "Asia/Taipei"
    TRX      = self . Translations [ self . ClassTag                         ]
    NOW      = StarDate            (                                         )
    ##########################################################################
    UUID     = int                 ( JSON [ "Uuid" ]                         )
    Id       = int                 ( UUID % 100000000                        )
    UXID     = str                 ( UUID                                    )
    Name     = JSON                [ "Name"                                  ]
    TYPE     = JSON                [ "Type"                                  ]
    USED     = JSON                [ "Used"                                  ]
    START    = JSON                [ "Start"                                 ]
    ENDT     = JSON                [ "End"                                   ]
    REALM    = JSON                [ "Realm"                                 ]
    RNAME    = JSON                [ "RName"                                 ]
    ROLE     = JSON                [ "Role"                                  ]
    TNAME    = JSON                [ "TName"                                 ]
    ITEM     = JSON                [ "Item"                                  ]
    STATES   = JSON                [ "States"                                ]
    CREATION = JSON                [ "Creation"                              ]
    MODIFIED = JSON                [ "Modified"                              ]
    ##########################################################################
    DURATION = self . DurationSTR  ( START , ENDT                            )
    ##########################################################################
    IT       . setText             ( 0 , str ( Id )                          )
    IT       . setToolTip          ( 0 , UXID                                )
    IT       . setData             ( 0 , Qt . UserRole , UXID                )
    IT       . setTextAlignment    ( 0 , Qt . AlignRight                     )
    ##########################################################################
    IT       . setText             ( 1 , Name                                )
    ##########################################################################
    DTS      = ""
    if                             ( START    > 0                          ) :
      NOW    . Stardate = START
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             ( 2 , DTS                                 )
    ##########################################################################
    DTS      = ""
    if                             ( ENDT     > 0                          ) :
      NOW    . Stardate = ENDT
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             ( 3 , DTS                                 )
    ##########################################################################
    IT       . setText             ( 4 , DURATION                            )
    ##########################################################################
    TRXS     = TRX                 [ "States"                                ]
    IT       . setText             ( 5 , TRXS [ str ( STATES ) ]             )
    ##########################################################################
    DTS      = ""
    if                             ( CREATION > 0                          ) :
      NOW    . Stardate = CREATION
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             ( 6 , DTS                                 )
    ##########################################################################
    DTS      = ""
    if                             ( MODIFIED > 0                          ) :
      NOW    . Stardate = MODIFIED
      DTS    = NOW . toDateTimeString ( TZ , " " , "%Y/%m/%d" , "%H:%M:%S"   )
    IT       . setText             ( 7 , DTS                                )
    ##########################################################################
    IT       . setData             ( 8 , Qt . UserRole , JSON                )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem             ( self , JSON                                ) :
    ##########################################################################
    IT   = QTreeWidgetItem    (                                              )
    self . PrepareItemContent ( IT   , JSON                                  )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                          (        list                           )
  def refresh                        ( self , PERIODs                      ) :
    ##########################################################################
    self   . clear                   (                                       )
    ##########################################################################
    for P in PERIODs                                                         :
      ########################################################################
      IT   = self . PrepareItem      ( P                                     )
      self . addTopLevelItem         ( IT                                    )
    ##########################################################################
    self   . emitNamesShow . emit    (                                       )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids                    ( self , DB                      ) :
    return self . DefaultObtainsItemUuids (        DB                        )
  ############################################################################
  def ObtainsUuidNames        ( self , DB , UUIDs                          ) :
    ##########################################################################
    NAMEs   =                 {                                              }
    ##########################################################################
    if                        ( len ( UUIDs ) > 0                          ) :
      TABLE = self . Tables   [ "NamesLocal"                                 ]
      NAMEs = self . GetNames ( DB , TABLE , UUIDs                           )
    ##########################################################################
    return NAMEs
  ############################################################################
  def ObtainPeriodDetail             ( self , DB , NAMEs , U               ) :
    ##########################################################################
    NAMTAB = self . Tables           [ "NamesLocal"                          ]
    GNATAB = self . Tables           [ "NamesPrivate"                        ]
    PRDTAB = self . Tables           [ "Periods"                             ]
    TYPTAB = self . Tables           [ "Types"                               ]
    ##########################################################################
    J      =                         { "Uuid"     : U                      , \
                                       "Name"     : ""                     , \
                                       "Type"     : 0                      , \
                                       "TName"    : ""                     , \
                                       "Used"     : 0                      , \
                                       "Start"    : 0                      , \
                                       "End"      : 0                      , \
                                       "Realm"    : 0                      , \
                                       "RName"    : ""                     , \
                                       "Role"     : 0                      , \
                                       "Item"     : 0                      , \
                                       "States"   : 0                      , \
                                       "Creation" : 0                      , \
                                       "Modified" : 0                        }
    ##########################################################################
    if                               ( U in NAMEs                          ) :
      J [ "Name" ] = self . assureString ( NAMEs [ U ]                       )
    ##########################################################################
    QQ     = f"""select
                 `type`,`used`,
                 `start`,`end`,
                 `realm`,`role`,
                 `item`,`states`,
                 `creation`,`modified`
                 from {PRDTAB}
                 where ( `uuid` = {U} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    RR     = DB . FetchOne           (                                       )
    ##########################################################################
    if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 10 ) )           :
      ########################################################################
      J [ "Type"     ] = int         ( RR [ 0 ]                              )
      J [ "Used"     ] = int         ( RR [ 1 ]                              )
      J [ "Start"    ] = int         ( RR [ 2 ]                              )
      J [ "End"      ] = int         ( RR [ 3 ]                              )
      J [ "Realm"    ] = int         ( RR [ 4 ]                              )
      J [ "Role"     ] = int         ( RR [ 5 ]                              )
      J [ "Item"     ] = int         ( RR [ 6 ]                              )
      J [ "States"   ] = int         ( RR [ 7 ]                              )
      J [ "Creation" ] = int         ( RR [ 8 ]                              )
      J [ "Modified" ] = int         ( RR [ 9 ]                              )
      ########################################################################
      RU   = J                       [ "Realm"                               ]
      if                             ( RU > 0                              ) :
        N  = self . GetName          ( DB , GNATAB , RU                      )
        J [ "RName" ] = N
      ########################################################################
      TU   = J                       [ "Role"                                ]
      TU   = 1100000000000000000 + TU
      if                             ( TU > 0                              ) :
        ######################################################################
        QQ = f"select `name` from {TYPTAB} where ( `uuid` = {TU} ) ;"
        DB . Query                   ( QQ                                    )
        RR = DB . FetchOne           (                                       )
        N  = str                     ( J [ "Role" ]                          )
        if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )        :
          N   = self . assureString  ( RR [ 0 ]                              )
        ## N = self . GetName          ( DB , GNATAB , TU                     )
        ####################################################################
        J [ "TName" ] = N
    ##########################################################################
    return J
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    ITEMs   =                         [                                      ]
    """
    self    . PrepareTimeRange        (                                      )
    ##########################################################################
    NAMEs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    PERIODS =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      J = self . ObtainPeriodDetail   ( DB , NAMEs , U                       )
      PERIODS . append                ( J                                    )
    """
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
    return
  ############################################################################
  @pyqtSlot          (                                                       )
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . Go      ( self . loading                                        )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . DetachConditions                  )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth (  0 ,  80                                         )
    self . setColumnWidth (  1 , 120                                         )
    self . setColumnWidth (  2 , 280                                         )
    self . defaultPrepare ( self . ClassTag , 7                              )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def GroupsMenu              ( self , mm                                  ) :
    ##########################################################################
    msg  = self . getMenuItem ( "Details"                                    )
    LOM  = mm . addMenu       ( msg                                          )
    ##########################################################################
    msg  = self . getMenuItem ( "Project"                                    )
    mm   . addActionFromMenu  ( LOM , 2001 , msg                             )
    ##########################################################################
    msg  = self . getMenuItem ( "Task"                                       )
    mm   . addActionFromMenu  ( LOM , 2002 , msg                             )
    ##########################################################################
    msg  = self . getMenuItem ( "Event"                                      )
    mm   . addActionFromMenu  ( LOM , 2003 , msg                             )
    ##########################################################################
    msg  = self . getMenuItem ( "Editor"                                     )
    mm   . addActionFromMenu  ( LOM , 2004 , msg                             )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu               ( self , at , item                       ) :
    ##########################################################################
    if                            ( at == 2001                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      self . Go                   ( self . OpenProjects , ( uuid , )         )
      ########################################################################
      return True
    ##########################################################################
    if                            ( at == 2002                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      self . Go                   ( self . OpenTasks , ( uuid , )            )
      ########################################################################
      return True
    ##########################################################################
    if                            ( at == 2003                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      self . Go                   ( self . OpenEvents , ( uuid , )           )
      ########################################################################
      return True
    ##########################################################################
    if                            ( at == 2004                             ) :
      ########################################################################
      uuid = self . itemUuid      ( item , 0                                 )
      name = item . text          ( 1                                        )
      self . PeriodDetails . emit ( name , str ( uuid )                      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    ##########################################################################
    return self . DefaultColumnsMenu (        mm , 0                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9000 ) and ( at <= 9007 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    ## if                              ( atItem not in [ False , None ]       ) :
    ##   mm   = self . GroupsMenu      ( mm                                     )
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunGroupsMenu ( at , atItem ) ) :
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
