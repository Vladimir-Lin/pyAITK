# -*- coding: utf-8 -*-
##############################################################################
## AlbumDateEditor
## 影集事件日期
##############################################################################
import os
import sys
import time
import requests
import threading
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
from   AITK    . Essentials . Relation import Relation
from   AITK    . Calendars  . StarDate import StarDate
from   AITK    . Calendars  . Periode  import Periode
from   AITK    . People     . People   import People as PeopleItem
##############################################################################
class AlbumDateEditor    ( TreeDock                                        ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = Signal (                                                   )
  emitAllNames  = Signal ( list                                              )
  emitLog       = Signal ( str                                               )
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    ##########################################################################
    self . ClassTag           = "AlbumDateEditor"
    self . FetchTableKey      = self . ClassTag
    self . AlbumUuid          = 0
    self . GType              = 76
    self . TZ                 = "Asia/Taipei"
    self . TzDiff             = 0
    ##########################################################################
    self . PEOPLE             = PeopleItem (                                 )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 4                                       )
    self . setColumnWidth          ( 0 , 120                                 )
    self . setColumnWidth          ( 1 , 280                                 )
    self . setColumnWidth          ( 2 , 280                                 )
    self . setColumnWidth          ( 3 ,   5                                 )
    ##########################################################################
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    self . setMinimumSize          ( 80 , 80                                 )
    self . DoTzDiff                (                                         )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 720 , 200 )                       )
  ############################################################################
  def PrepareForActions ( self                                             ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . restart         , Enabled      )
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
  def DoTzDiff          ( self                                             ) :
    ##########################################################################
    BTX  = "2000/01/01 00:00:00"
    FMT  = "yyyy/MM/dd hh:mm:ss"
    ##########################################################################
    NOW  = StarDate     (                                                    )
    NOW  . fromInput    ( BTX                                                )
    AAA  = int          ( NOW . Stardate                                     )
    NOW  . fromInput    ( BTX , self . TZ                                    )
    BBB  = int          ( NOW . Stardate                                     )
    self . TzDiff = int ( BBB - AAA                                          )
    ##########################################################################
    return
  ############################################################################
  def setDateTimeEdit         ( self , item , column , signal , method     ) :
    ##########################################################################
    if                        ( not hasattr ( self , 'CurrentItem' )       ) :
      self . CurrentItem =    {                                              }
    ##########################################################################
    le     = QDateTimeEdit    ( self                                         )
    le     . setDisplayFormat ( "yyyy/MM/dd hh:mm:ss"                        )
    dtx    = item . data      ( column , Qt . UserRole                       )
    ##########################################################################
    if                        ( int ( dtx ) > 0                            ) :
      ########################################################################
      NOW  = StarDate         (                                              )
      NOW  . Stardate = int   ( dtx                                          )
      TS   = NOW . Timestamp  (                                              )
      DTZ  = QDateTime . fromSecsSinceEpoch ( TS - self . TzDiff             )
      le   . setDateTime      ( DTZ                                          )
    ##########################################################################
    self   . setItemWidget    ( item , column , le                           )
    ##########################################################################
    self   . CurrentItem [ "Item"   ] = item
    self   . CurrentItem [ "Column" ] = column
    self   . CurrentItem [ "Widget" ] = le
    ##########################################################################
    try                                                                      :
      ########################################################################
      S  = getattr            ( le, signal                                   )
      S  . connect            ( method                                       )
      ########################################################################
    except AttributeError                                                    :
      pass
    ##########################################################################
    return le
  ############################################################################
  def twiceClicked                ( self , item , column                   ) :
    ##########################################################################
    if                            ( column in [ 1 , 2 ]                    ) :
      ########################################################################
      dt = self . setDateTimeEdit ( item                                   , \
                                    column                                 , \
                                   "editingFinished"                       , \
                                   self . datetimeChanged                    )
      dt . setFocus               ( Qt . TabFocusReason                      )
    ##########################################################################
    self . defaultSingleClicked   (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation ( self , DB                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                        ( self , JSON , BRUSH             ) :
    ##########################################################################
    KTZ     = self . TZ
    NOW     = StarDate                   (                                   )
    UUID    = JSON                       [ "Uuid"                            ]
    NAME    = JSON                       [ "Name"                            ]
    PTYPE   = JSON                       [ "Type"                            ]
    PSTART  = JSON                       [ "Start"                           ]
    PFINISH = JSON                       [ "Finish"                          ]
    UXID    = str                        ( UUID                              )
    KSTART  = str                        ( PSTART                            )
    KFINISH = str                        ( PFINISH                           )
    ##########################################################################
    SDATE   = ""
    FDATE   = ""
    ##########################################################################
    if                                   ( PSTART > 0                      ) :
      ########################################################################
      NOW   . Stardate = PSTART
      SDATE = NOW . toLongDateTimeString ( KTZ , "%Y/%m/%d" , "%H:%M:%S"     )
    ##########################################################################
    if                                   ( PFINISH > 0                     ) :
      ########################################################################
      NOW   . Stardate = PFINISH
      FDATE = NOW . toLongDateTimeString ( KTZ , "%Y/%m/%d" , "%H:%M:%S"     )
    ##########################################################################
    IT      = QTreeWidgetItem            (                                   )
    IT      . setText                    ( 0 , NAME                          )
    IT      . setTextAlignment           ( 0 , Qt . AlignCenter              )
    IT      . setToolTip                 ( 0 , UXID                          )
    IT      . setData                    ( 0 , Qt . UserRole , UXID          )
    IT      . setText                    ( 1 , SDATE                         )
    IT      . setData                    ( 1 , Qt . UserRole , KSTART        )
    IT      . setText                    ( 2 , FDATE                         )
    IT      . setData                    ( 2 , Qt . UserRole , KFINISH       )
    ##########################################################################
    for COL in range                     ( 0 , self . columnCount (      ) ) :
      ########################################################################
      IT    . setBackground              ( COL , BRUSH                       )
    ##########################################################################
    return IT
  ############################################################################
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 1                                                  )
    ##########################################################################
    return
  ############################################################################
  def RefreshToolTip          ( self , Total                               ) :
    ##########################################################################
    FMT  = self . getMenuItem ( "DisplayTotal"                               )
    MSG  = FMT  . format      ( Total                                        )
    self . setToolTip         ( MSG                                          )
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
    for J in LISTs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( J , self . TreeBrushes [ CNT ]           )
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
  def LoadPeriods                  ( self , DB                             ) :
    ##########################################################################
    LISTs    =                     [                                         ]
    NOW      = StarDate            (                                         )
    EVENTs   = self . Translations [ self . ClassTag ] [ "Events"            ]
    PRDTAB   = self . Tables       [ "Periods"                               ]
    COLs     = "`uuid`,`type`,`start`,`end`,`states`"
    PUID     = self . AlbumUuid
    GTYPE    = self . GType
    ##########################################################################
    for E in EVENTs                                                          :
      ########################################################################
      ITEM   = E                   [ "Item"                                  ]
      MARK   = E                   [ "Marking"                               ]
      NAME   = E                   [ "Name"                                  ]
      NEWBIE = True
      ########################################################################
      QQ     = f"""select {COLs} from {PRDTAB}
                   where ( `realm` = {PUID} )
                     and ( `role` = {GTYPE} )
                     and ( `item` = {ITEM} )
                   order by `id` desc
                   limit 0 , 1;"""
      QQ     = " " . join          ( QQ . split (                          ) )
      DB     . Query               ( QQ                                      )
      ALL    = DB . FetchAll       (                                         )
      ########################################################################
      if                           ( ALL not in self . EmptySet            ) :
        if                         ( len ( ALL ) > 0                       ) :
          ####################################################################
          RR = ALL                 [ 0                                       ]
          ####################################################################
          if                       ( 5 == len ( RR )                       ) :
            ##################################################################
            NEWBIE  = False
            ##################################################################
            UUID    = int          ( RR [ 0                                ] )
            PTYPE   = int          ( RR [ 1                                ] )
            PSTART  = int          ( RR [ 2                                ] )
            PFINISH = int          ( RR [ 3                                ] )
            PSTATES = int          ( RR [ 4                                ] )
            ##################################################################
            JJ      =              { "Item"    : ITEM                      , \
                                     "Marking" : MARK                      , \
                                     "Name"    : NAME                      , \
                                     "Uuid"    : UUID                      , \
                                     "Type"    : PTYPE                     , \
                                     "Start"   : PSTART                    , \
                                     "Finish"  : PFINISH                   , \
                                     "States"  : PSTATES                     }
            LISTs   . append       ( JJ                                      )
      ########################################################################
      if                           ( NEWBIE                                ) :
        ######################################################################
        BASE = 3500000000000000000
        UUID = DB . LastUuid       ( PRDTAB , "uuid" , BASE                  )
        ######################################################################
        QQ   = f"""insert into {PRDTAB}
                   ( `uuid` , `type` , `realm` , `role` , `item` )
                   values
                   ( {UUID} , 4 , {PUID} , {GTYPE} , {ITEM} ) ;"""
        QQ   = " " . join          ( QQ . split (                          ) )
        DB   . Query               ( QQ                                      )
        ######################################################################
        JJ   =                     { "Item"    : ITEM                      , \
                                     "Marking" : MARK                      , \
                                     "Name"    : NAME                      , \
                                     "Uuid"    : UUID                      , \
                                     "Type"    : 4                         , \
                                     "Start"   : 0                         , \
                                     "Finish"  : 0                         , \
                                     "States"  : 0                           }
        LISTs . append             ( JJ                                      )
    ##########################################################################
    return LISTs
  ############################################################################
  def loading                     ( self                                   ) :
    ##########################################################################
    DB     = self . ConnectDB     (                                          )
    if                            ( DB == None                             ) :
      self . emitNamesShow . emit (                                          )
      return
    ##########################################################################
    self   . Notify               ( 3                                        )
    ##########################################################################
    FMT    = self . Translations  [ "UI::StartLoading"                       ]
    MSG    = FMT . format         ( self . windowTitle ( )                   )
    self   . ShowStatus           ( MSG                                      )
    self   . OnBusy  . emit       (                                          )
    self   . setBustle            (                                          )
    ##########################################################################
    self   . ObtainsInformation   ( DB                                       )
    LISTs  = self . LoadPeriods   ( DB                                       )
    ##########################################################################
    self   . setVacancy           (                                          )
    self   . GoRelax . emit       (                                          )
    self   . ShowStatus           ( ""                                       )
    DB     . Close                (                                          )
    ##########################################################################
    self   . emitAllNames . emit  ( LISTs                                    )
    ##########################################################################
    return
  ############################################################################
  def StartupAlbum ( self , uuid                                           ) :
    ##########################################################################
    self . AlbumUuid = uuid
    ##########################################################################
    self . startup (                                                         )
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
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def datetimeChanged                   ( self                             ) :
    ##########################################################################
    if                                  ( not self . isItemPicked (      ) ) :
      return False
    ##########################################################################
    KTZ    = self . TZ
    NOW    = StarDate                   (                                    )
    item   = self . CurrentItem         [ "Item"                             ]
    column = self . CurrentItem         [ "Column"                           ]
    dt     = self . CurrentItem         [ "Widget"                           ]
    uuid   = self . itemUuid            ( item , 0                           )
    DTX    = dt   . dateTime            (                                    )
    UTIME  = DTX  . toSecsSinceEpoch    (                                    )
    NOW    . setTime                    ( UTIME + self . TzDiff              )
    CDT    = int                        ( NOW  . Stardate                    )
    CDK    = str                        ( NOW  . Stardate                    )
    FDATE  = NOW . toLongDateTimeString ( KTZ , "%Y/%m/%d" , "%H:%M:%S"      )
    ##########################################################################
    item   . setText                    ( column , FDATE                     )
    item   . setData                    ( column , Qt . UserRole , CDK       )
    self   . removeParked               (                                    )
    ##########################################################################
    if                                  ( 1 == column                      ) :
      ########################################################################
      VAL  =                            ( item , uuid , "start" , CDT ,      )
      self . Go                         ( self . UpdatePeriodColumn , VAL    )
      ########################################################################
    elif                                ( 2 == column                      ) :
      ########################################################################
      VAL  =                            ( item , uuid , "end"   , CDT ,      )
      self . Go                         ( self . UpdatePeriodColumn , VAL    )
    ##########################################################################
    return
  ############################################################################
  def UpdatePeriodColumn      ( self , item , uuid , column , value        ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    NOW    = StarDate         (                                              )
    NOW    . Now              (                                              )
    CDT    = int              ( NOW . Stardate                               )
    PRDTAB = self . Tables    [ "Periods"                                    ]
    ##########################################################################
    DB     . LockWrites       ( [ PRDTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {PRDTAB}
                 set `{column}` = {value} ,
                     `modified` = {CDT}
                 where ( `uuid` = {uuid} ) ;"""
    DB     . Query            ( " " . join ( QQ . split (                ) ) )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def CommandParser ( self , language , message , timestamp                ) :
    return          { "Match" : False                                        }
  ############################################################################
  def TimeZoneMenu               ( self , mm                               ) :
    ##########################################################################
    MSG   = self  . getMenuItem  ( "TimeZone"                                )
    COL   = mm    . addMenu      ( MSG                                       )
    TZs   = self  . Translations [ self . ClassTag ] [ "TimeZones"           ]
    ##########################################################################
    for TZX in TZs                                                           :
      ########################################################################
      BXD = int                  ( TZX [ "Id" ]                              )
      TZK = TZX                  [ "TimeZone"                                ]
      MSG = TZX                  [ "Name"                                    ]
      CHK =                      ( TZK == self . TZ                          )
      mm  . addActionFromMenu    ( COL , BXD , MSG , True , CHK              )
    ##########################################################################
    return mm
  ############################################################################
  def RunTimeZoneMenu            ( self , at                               ) :
    ##########################################################################
    TZs   = self  . Translations [ self . ClassTag ] [ "TimeZones"           ]
    ##########################################################################
    for TZX in TZs                                                           :
      ########################################################################
      BXD = int                  ( TZX [ "Id" ]                              )
      TZK = TZX                  [ "TimeZone"                                ]
      MSG = TZX                  [ "Name"                                    ]
      ########################################################################
      if                         ( at == BXD                               ) :
        ######################################################################
        self . TZ = TZK
        ######################################################################
        return True
    ##########################################################################
    return False
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
    self   . AppendRenameAction       ( mm , 1002                            )
    mm     . addSeparator             (                                      )
    ##########################################################################
    self   . TimeZoneMenu             ( mm                                   )
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
    if                                ( self . RunTimeZoneMenu ( at )      ) :
      ########################################################################
      self . DoTzDiff                 (                                      )
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 1001                         ) :
      ########################################################################
      self . restart                  (                                      )
      ########################################################################
      return True
    ##########################################################################
    if                                ( at == 1002                         ) :
      self . RenameItem               (                                      )
      return True
    ##########################################################################
    return True
##############################################################################
