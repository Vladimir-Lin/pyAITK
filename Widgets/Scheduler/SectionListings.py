# -*- coding: utf-8 -*-
##############################################################################
## SectionListings
## 時段列表
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
class SectionListings              ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
  ProjectTasks  = pyqtSignal       ( str , int , str , QIcon                 )
  TaskEvents    = pyqtSignal       ( str , int , str                         )
  EventPeriods  = pyqtSignal       ( str , int , str                         )
  PeriodDetails = pyqtSignal       ( str , str                               )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    self . StartTimeEditor    = None
    self . FinishTimeEditor   = None
    self . ClassTag           = "SectionListings"
    self . SortOrder          = "asc"
    self . FromTime           =  - ( 8 *  3600                               )
    self . ToTime             =    ( 3 * 86400                               )
    self . FromStarDate       = 0
    self . ToStarDate         = 0
    self . Icon               = QIcon ( ":/images/project.png"               )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 9                                       )
    self . setColumnHidden         ( 6 , True                                )
    self . setColumnHidden         ( 7 , True                                )
    self . setColumnHidden         ( 8 , True                                )
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
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                     ( self                                  ) :
    return self . SizeSuggestion   ( QSize ( 1024 , 480 )                    )
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup                   )
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
    self   . resizeColumnsToContents (                                       )
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
  def PrepareTimeRange        ( self                                       ) :
    ##########################################################################
    NOW  = StarDate           (                                              )
    NOW  . Now                (                                              )
    SDT  = NOW . Stardate
    ##########################################################################
    self . FromStarDate = int ( SDT + self . FromTime                        )
    self . ToStarDate   = int ( SDT + self . ToTime                          )
    ##########################################################################
    return
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
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( PERIODS ) <= 0               ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( PERIODS                              )
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
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    PRDTAB = self . Tables [ "Periods"                                       ]
    ORDER  = self . SortOrder
    FSD    = self . FromStarDate
    TSD    = self . ToStarDate
    ##########################################################################
    QQ     = f"""select `uuid` from {PRDTAB}
                 where ( `used` > 0 )
                 and ( `item` = 196833 )
                 and ( `type` = 4 )
                 and ( ( ( `start` >= {FSD} ) and ( `start` <= {TSD} ) )
                    or ( ( `end` >= {FSD} ) and ( `end` <= {TSD} ) )
                    or ( ( `start` < {FSD} ) and ( `end` > {TSD} ) ) )
                 order by `start` {ORDER} ;"""
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def OpenProjects ( self , UUID ) :
    ##########################################################################
    DB      = self . ConnectDB       (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    GRPREL  = self . Tables          [ "RelationGroups"                      ]
    PRDREL  = self . Tables          [ "RelationPeriods"                     ]
    NAMTAB  = self . Tables          [ "NamesParent"                         ]
    ##########################################################################
    EVTS    = Events                 (                                       )
    EVENTS  = EVTS . GetPeriodEvents ( DB , PRDREL , UUID                    )
    ##########################################################################
    TASKS   =                        [                                       ]
    ##########################################################################
    if                               ( len ( EVENTS ) > 0                  ) :
      ########################################################################
      TSKS  = Tasks                  (                                       )
      ########################################################################
      for EUID in EVENTS                                                     :
        ######################################################################
        T   = TSKS . GetEventTasks   ( DB , GRPREL , EUID                    )
        for TUID in T                                                        :
          if                         ( TUID not in TASKS                   ) :
            TASKS . append           ( TUID                                  )
    ##########################################################################
    PRJS    =                        [                                       ]
    ##########################################################################
    if                               ( len ( TASKS ) > 0                   ) :
      ########################################################################
      PRJX  = Projects               (                                       )
      ########################################################################
      for TUID in TASKS                                                      :
        ######################################################################
        T   = PRJX . GetTaskProjects ( DB , GRPREL , TUID                    )
        for PUID in T                                                        :
          if                         ( PUID not in PRJS                    ) :
            PRJS . append            ( PUID                                  )
    ##########################################################################
    NAMEs   = self . GetNames        ( DB , NAMTAB , PRJS                    )
    ##########################################################################
    DB      . Close                  (                                       )
    ##########################################################################
    for PUID in PRJS                                                         :
      ########################################################################
      NAME = NAMEs                   [ PUID                                  ]
      self . ProjectTasks . emit     ( NAME , 71 , str (PUID) , self . Icon  )
    ##########################################################################
    return
  ############################################################################
  def OpenTasks                      ( self , UUID                         ) :
    ##########################################################################
    DB      = self . ConnectDB       (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    GRPREL  = self . Tables          [ "RelationGroups"                      ]
    PRDREL  = self . Tables          [ "RelationPeriods"                     ]
    NAMTAB  = self . Tables          [ "NamesParent"                         ]
    ##########################################################################
    EVTS    = Events                 (                                       )
    EVENTS  = EVTS . GetPeriodEvents ( DB , PRDREL , UUID                    )
    ##########################################################################
    TASKS   =                        [                                       ]
    ##########################################################################
    if                               ( len ( EVENTS ) > 0                  ) :
      ########################################################################
      TSKS  = Tasks                  (                                       )
      ########################################################################
      for EUID in EVENTS                                                     :
        ######################################################################
        T   = TSKS . GetEventTasks   ( DB , GRPREL , EUID                    )
        for TUID in T                                                        :
          if                         ( TUID not in TASKS                   ) :
            TASKS . append           ( TUID                                  )
    ##########################################################################
    NAMEs   = self . GetNames        ( DB , NAMTAB , TASKS                   )
    ##########################################################################
    DB      . Close                  (                                       )
    ##########################################################################
    for TUID in TASKS                                                        :
      ########################################################################
      NAME = NAMEs                   [ TUID                                  ]
      self . TaskEvents . emit       ( NAME , 16 , str ( TUID )              )
    ##########################################################################
    return
  ############################################################################
  def OpenEvents                     ( self , UUID                         ) :
    ##########################################################################
    DB      = self . ConnectDB       (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    PRDREL  = self . Tables          [ "RelationPeriods"                     ]
    NAMTAB  = self . Tables          [ "NamesParent"                         ]
    ##########################################################################
    EVTS    = Events                 (                                       )
    EVENTS  = EVTS . GetPeriodEvents ( DB , PRDREL , UUID                    )
    ##########################################################################
    NAMEs   = self . GetNames        ( DB , NAMTAB , EVENTS                  )
    ##########################################################################
    DB      . Close                  (                                       )
    ##########################################################################
    for EUID in EVENTS                                                       :
      ########################################################################
      NAME = NAMEs                   [ EUID                                  ]
      self . EventPeriods . emit     ( NAME , 15 , str ( EUID )              )
    ##########################################################################
    return
  ############################################################################
  def dragMime                      ( self                                 ) :
    ##########################################################################
    mtype   = "period/uuids"
    message = self . getMenuItem    ( "PeriodsSelected"                      )
    ##########################################################################
    return self    . CreateDragMime ( self , 0 , mtype , message             )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth (  0 , 120                                         )
    self . setColumnWidth (  1 , 280                                         )
    self . setColumnWidth (  2 , 180                                         )
    self . setColumnWidth (  3 , 180                                         )
    self . defaultPrepare ( self . ClassTag , 8                              )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def RangeMenu                         ( self , mm                        ) :
    ##########################################################################
    NOW    = StarDate                   (                                    )
    NOW    . Stardate = self . FromStarDate
    STS    = NOW . Timestamp            (                                    )
    NOW    . Stardate = self . ToStarDate
    ETS    = NOW . Timestamp            (                                    )
    ##########################################################################
    SDTX   = QDateTime . fromSecsSinceEpoch ( STS                            )
    EDTX   = QDateTime . fromSecsSinceEpoch ( ETS                            )
    ##########################################################################
    DTFMT  = self . getMenuItem         ( "TimeFormat"                       )
    ## SSI    = self . getMenuItem         ( "StartTime:"                       )
    ## SSA    = self . getMenuItem         ( "FinishTime:"                      )
    ##########################################################################
    self   . StartTimeEditor  = QDateTimeEdit    (                           )
    self   . StartTimeEditor  . setDateTime      ( SDTX                      )
    self   . StartTimeEditor  . setDisplayFormat ( DTFMT                     )
    ## self   . StartTimeEditor  . setPrefix        ( SSI                       )
    self   . StartTimeEditor  . setAlignment     ( Qt . AlignRight           )
    mm     . addWidget                  ( 9999992 , self . StartTimeEditor   )
    ##########################################################################
    self   . FinishTimeEditor = QDateTimeEdit    (                           )
    self   . FinishTimeEditor . setDateTime      ( EDTX                      )
    self   . FinishTimeEditor . setDisplayFormat ( DTFMT                     )
    ## self   . FinishTimeEditor . setPrefix        ( SSA                       )
    self   . FinishTimeEditor . setAlignment     ( Qt . AlignRight           )
    mm     . addWidget                  ( 9999993 , self . FinishTimeEditor  )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    return mm
  ############################################################################
  def RunRangeMenu                      ( self                             ) :
    ##########################################################################
    if                                  ( self . StartTimeEditor  == None  ) :
      return False
    ##########################################################################
    if                                  ( self . FinishTimeEditor == None  ) :
      return False
    ##########################################################################
    SDTX   = self . StartTimeEditor  . dateTime (                            )
    EDTX   = self . FinishTimeEditor . dateTime (                            )
    ##########################################################################
    NOW    = StarDate                   (                                    )
    STS    = SDTX . toSecsSinceEpoch    (                                    )
    ETS    = EDTX . toSecsSinceEpoch    (                                    )
    ##########################################################################
    NOW    . setTime                    ( STS                                )
    SDT    = NOW . Stardate
    NOW    . setTime                    ( ETS                                )
    EDT    = NOW . Stardate
    ##########################################################################
    if ( ( SDT == self . FromStarDate ) and ( EDT == self . ToStarDate ) )   :
      return False
    ##########################################################################
    NOW    . Now                        (                                    )
    CDT    = NOW . Stardate
    self   . FromTime     = int         ( SDT - CDT                          )
    self   . ToTime       = int         ( EDT - CDT                          )
    self   . FromStarDate = int         ( SDT                                )
    self   . ToStarDate   = int         ( EDT                                )
    ##########################################################################
    return   True
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
    return self . DefaultColumnsMenu (        mm , 4                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9004 ) and ( at <= 9008 )         :
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
    mm     = self . RangeMenu       ( mm                                     )
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      mm   = self . GroupsMenu      ( mm                                     )
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self   . RunRangeMenu ( )            ) :
      ########################################################################
      self . restart                (                                        )
      ########################################################################
      return
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
