# -*- coding: utf-8 -*-
##############################################################################
## DescriptiveEditor
## 場景描述
##############################################################################
import os
import sys
import time
import requests
import threading
import json
##############################################################################
from   opencc                             import OpenCC
##############################################################################
from   PySide6                            import QtCore
from   PySide6                            import QtGui
from   PySide6                            import QtWidgets
from   PySide6 . QtCore                   import *
from   PySide6 . QtGui                    import *
from   PySide6 . QtWidgets                import *
from   AITK    . Qt6                      import *
##############################################################################
from   AITK    . Essentials  . Relation   import Relation
from   AITK    . Calendars   . StarDate   import StarDate
from   AITK    . Calendars   . Periode    import Periode
from   AITK    . Linguistics . Translator import Translate
##############################################################################
from           . Fragment                 import Fragment    as FragmentItem
from           . Scenario                 import Scenario    as ScenarioItem
from           . Descriptive              import Descriptive as DescriptiveItem
##############################################################################
class DescriptiveEditor        ( TreeDock                                  ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow       = Signal (                                             )
  emitReload          = Signal (                                             )
  emitUpdated         = Signal (                                             )
  emitUpdatePTS       = Signal (                                             )
  emitUpdatePtsItem   = Signal (                                             )
  emitFocusIn         = Signal ( int                                         )
  emitSegments        = Signal ( QWidget , str , str , dict , QIcon          )
  emitPlayer          = Signal ( QWidget                                     )
  emitConnector       = Signal ( QWidget                                     )
  emitDetachConnector = Signal ( QWidget                                     )
  emitLog             = Signal ( str                                         )
  AssignPlayerPTS     = Signal ( int                                         )
  ############################################################################
  def __init__                 ( self , parent = None , plan = None        ) :
    ##########################################################################
    super ( ) . __init__       (        parent        , plan                 )
    ##########################################################################
    self . ClassTag           = "DescriptiveEditor"
    self . FetchTableKey      = self . ClassTag
    self . GType              = 212
    self . PlayerWidget       = None
    self . AlbumUuid          = 0
    self . FragmentUuid       = 0
    self . ScenarioUuid       = 0
    self . DefaultTitle       = ""
    self . TimeGap            = 5000
    self . sourceLocality     = 1001
    self . ConvertAllCC       = False
    self . SortOrder          = "asc"
    self . BaseTimeEditor     = None
    self . ConnectedFilmJson  = {                                            }
    self . CurrentPTS         = -1
    self . PlayerConnected    = False
    self . UsePtsForAdd       = False
    self . UsePtsForItem      = False
    self . TrackPtsForItem    = False
    self . SyncPlayerTime     = False
    ##########################################################################
    self . SCENE              = ScenarioItem    (                            )
    self . DESCRIBE           = DescriptiveItem (                            )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount              ( 7                                   )
    self . setColumnWidth              ( 0 , 120                             )
    self . setColumnWidth              ( 1 , 120                             )
    ## self . setColumnHidden             ( 1 , True                            )
    self . setColumnWidth              ( 2 , 600                             )
    ## self . setColumnHidden             ( 3 , True                            )
    self . setColumnHidden             ( 4 , True                            )
    ## self . setColumnHidden             ( 5 , True                            )
    self . setColumnHidden             ( 6 , True                            )
    self . setRootIsDecorated          ( False                               )
    ##########################################################################
    self . MountClicked                ( 1                                   )
    self . MountClicked                ( 2                                   )
    ##########################################################################
    self . assignSelectionMode         ( "ExtendedSelection"                 )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitReload        . connect ( self . reload                       )
    self . emitFocusIn       . connect ( self . clickIn                      )
    self . emitUpdatePTS     . connect ( self . FilmUpdatePTS                )
    self . emitUpdatePtsItem . connect ( self . PtsUpdateItem                )
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
    return self . SizeSuggestion ( QSize ( 960 , 200 )                       )
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendSideActionWithIcon ( "OpenSegments"                       , \
                                      ":/images/addcolumn.png"             , \
                                      self . GotoSegments                  , \
                                      True                                 , \
                                      False                                  )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . reload          , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Save"       , self . SaveToDatabase  , Enabled      )
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
  def AssignPlayer           ( self , widget                               ) :
    ##########################################################################
    self . PlayerWidget = widget
    ##########################################################################
    self . emitPlayer . emit (        widget                                 )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked   (        item , column                     )
    ##########################################################################
    if                            ( not self . SyncPlayerTime              ) :
      return
    ##########################################################################
    dlen = item . data            ( 0 , Qt . UserRole                        )
    slen = int                    ( dlen                                     )
    plen = int                    ( slen / 1000                              )
    self . AssignPlayerPTS . emit ( plen                                     )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked ( self , item , column                                  ) :
    ##########################################################################
    if                              ( column in [ 0 ]                      ) :
      ########################################################################
      slen = item . data            ( column , Qt . UserRole                 )
      vlen = self . DESCRIBE . shiftTime ( int ( slen                      ) )
      xlen = self . SCENE . toFTime ( vlen                                   )
      line = self . setLineEdit     ( item                                 , \
                                      column                               , \
                                      "editingFinished"                    , \
                                      self . nameChanged                     )
      line . blockSignals           ( True                                   )
      line . setText                ( xlen                                   )
      line . blockSignals           ( False                                  )
      line . setFocus               ( Qt . TabFocusReason                    )
    ##########################################################################
    if                              ( column in [ 1 ]                      ) :
      ########################################################################
      slen = item . data            ( column , Qt . UserRole                 )
      xlen = self . SCENE . toFTime ( int ( slen )                           )
      line = self . setLineEdit     ( item                                 , \
                                      column                               , \
                                      "editingFinished"                    , \
                                      self . nameChanged                     )
      line . blockSignals           ( True                                   )
      line . setText                ( xlen                                   )
      line . blockSignals           ( False                                  )
      line . setFocus               ( Qt . TabFocusReason                    )
    ##########################################################################
    if                              ( column in [ 2 ]                      ) :
      ########################################################################
      line = self . setLineEdit     ( item                                 , \
                                      column                               , \
                                      "editingFinished"                    , \
                                      self . nameChanged                     )
      line . setFocus               ( Qt . TabFocusReason                    )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                    ( self , JSON , BRUSH                 ) :
    ##########################################################################
    STIME   = int                    ( JSON [ "Shift"                      ] )
    RTIME   = str                    ( JSON [ "Timestamp"                  ] )
    KTIME   = int                    ( RTIME                                 )
    NAME    =                          JSON [ "Name"                         ]
    ##########################################################################
    FTIME   = self . SCENE . toLTime         ( STIME                         )
    COPTs   = self . DESCRIBE . OptionString ( KTIME                         )
    PTOTs   = self . DESCRIBE . TotalPeople  ( KTIME                         )
    STOTs   = str                            ( PTOTs                         )
    LTIME   = self . DESCRIBE . getOption    ( KTIME , "Duration"            )
    ##########################################################################
    if                               ( LTIME in [ False , None ]           ) :
      ########################################################################
      LTIME = 0
    ##########################################################################
    VTIME   = self . SCENE . toLTime ( LTIME                                 )
    ##########################################################################
    IT      = QTreeWidgetItem        (                                       )
    IT      . setData                ( 0 , Qt . UserRole , str ( RTIME )     )
    IT      . setText                ( 0 , FTIME                             )
    IT      . setTextAlignment       ( 0 , Qt . AlignRight                   )
    IT      . setData                ( 1 , Qt . UserRole , str ( LTIME )     )
    IT      . setText                ( 1 , VTIME                             )
    IT      . setTextAlignment       ( 1 , Qt . AlignRight                   )
    IT      . setText                ( 2 , NAME                              )
    IT      . setText                ( 3 , COPTs                             )
    IT      . setTextAlignment       ( 3 , Qt . AlignCenter                  )
    IT      . setText                ( 5 , STOTs                             )
    IT      . setData                ( 5 , Qt . UserRole , STOTs             )
    IT      . setTextAlignment       ( 5 , Qt . AlignRight                   )
    ##########################################################################
    for COL in range                 ( 0 , self . columnCount (          ) ) :
      ########################################################################
      IT    . setBackground          ( COL , BRUSH                           )
    ##########################################################################
    return IT
  ############################################################################
  def RefreshToolTip          ( self , Total                               ) :
    ##########################################################################
    FMT  = self . getMenuItem ( "DisplayTotal"                               )
    MSG  = FMT  . format      ( Total                                        )
    self . setToolTip         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def loading                   ( self                                     ) :
    ##########################################################################
    ##########################################################################
    ## self . emitAllNames  . emit ( L                                          )
    ## self . Notify               ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def reload                               ( self                          ) :
    ##########################################################################
    self      . clear                      (                                 )
    self      . setEnabled                 ( False                           )
    ##########################################################################
    CNT       = 0
    MOD       = len                        ( self . TreeBrushes              )
    TOTAL     = len                        ( self . DESCRIBE . TIMESTAMPs    )
    ##########################################################################
    for T in self . DESCRIBE . TIMESTAMPs                                    :
      ########################################################################
      OK , JJ = self . DESCRIBE . itemJson ( T                               )
      ########################################################################
      if                                   ( not OK                        ) :
        continue
      ########################################################################
      IT      = self . PrepareItem         ( JJ , self . TreeBrushes [ CNT ] )
      ########################################################################
      if                                   ( self . SortOrder in [ "asc" ] ) :
        self  . addTopLevelItem            (     IT                          )
      else                                                                   :
        self  . insertTopLevelItem         ( 0 , IT                          )
      ########################################################################
      CNT     = int                        ( int ( CNT + 1 ) % MOD           )
    ##########################################################################
    self      . RefreshToolTip             ( TOTAL                           )
    self      . setEnabled                 ( True                            )
    self      . emitNamesShow . emit       (                                 )
    self      . Notify                     ( 5                               )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes     ( self , mime                                   ) :
    FMTs =                 [ "people/uuids"                                  ]
    return self . MimeType ( mime , ";" . join ( FMTs  )                     )
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
    if                               ( mtype in [ "people/uuids"         ] ) :
      ########################################################################
      if                             ( atItem not in self . EmptySet       ) :
        ######################################################################
        TXT  = atItem . text         ( 0                                     )
        UID  = atItem . data         ( 0 , Qt . UserRole                     )
        FMT  = self   . getMenuItem  ( "PeopleFrom"                          )
        MSG  = FMT    . format       ( title , CNT , TXT , UID               )
        self . ShowStatus            ( MSG                                   )
      ########################################################################
      return True
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving                  ( self , source , mimeData , mousePos    ) :
    ##########################################################################
    if                            ( self . droppingAction                  ) :
      return False
    ##########################################################################
    mtype  = self   . DropInJSON  [ "Mime"                                   ]
    UUIDs  = self   . DropInJSON  [ "UUIDs"                                  ]
    atItem = self   . itemAt      ( mousePos                                 )
    title  = source . windowTitle (                                          )
    CNT    = len                  ( UUIDs                                    )
    ##########################################################################
    if                            ( mtype in [ "people/uuids"            ] ) :
      ########################################################################
      if                          ( atItem in self . EmptySet              ) :
        return False
      ########################################################################
      TXT  = atItem . text        ( 0                                        )
      UID  = atItem . data        ( 0 , Qt . UserRole                        )
      FMT  = self   . getMenuItem ( "PeopleFrom"                             )
      MSG  = FMT    . format      ( title , CNT , TXT , UID                  )
      self . ShowStatus           ( MSG                                      )
      ########################################################################
      return True
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop ( self                                              ) :
    return True
  ############################################################################
  def dropPeople                           ( self , source , pos , JSOX    ) :
    ##########################################################################
    if                                     ( "UUIDs" not in JSOX           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX                          [ "UUIDs"                         ]
    if                                     ( len ( UUIDs ) <= 0            ) :
      return True
    ##########################################################################
    atItem = self . itemAt                 ( pos                             )
    if                                     ( atItem in self . EmptySet     ) :
      return True
    ##########################################################################
    slen   = atItem . data                 ( 0 , Qt . UserRole               )
    vlen   = int                           ( slen                            )
    ##########################################################################
    self   . DESCRIBE . addCrowds          ( vlen , UUIDs                    )
    TOTAL  = self . DESCRIBE . TotalPeople ( vlen                            )
    sTOTAL = str                           ( TOTAL                           )
    ##########################################################################
    atItem . setText                       ( 5 ,                 sTOTAL      )
    atItem . setData                       ( 5 , Qt . UserRole , sTOTAL      )
    self   . Notify                        ( 5                               )
    ##########################################################################
    return True
  ############################################################################
  def startScenario                         ( self , Uuid , JSON           ) :
    ##########################################################################
    if                                      ( not self . isPrepared (    ) ) :
      self . Prepare                        (                                )
    ##########################################################################
    self   . ScenarioUuid = int             ( Uuid                           )
    ##########################################################################
    if                                      ( "Description" in JSON        ) :
      ########################################################################
      self . DESCRIBE     = DescriptiveItem (                                )
      self . DESCRIBE     . setScenario     ( JSON                           )
      self . setLocality                    ( self . DESCRIBE . Locality     )
      self . sourceLocality = self . DESCRIBE . Locality
    ##########################################################################
    if                                      ( "Album"       in JSON        ) :
      ########################################################################
      self . AlbumUuid    = int             ( JSON [ "Album"               ] )
    ##########################################################################
    if                                      ( "Fragment"    in JSON        ) :
      ########################################################################
      self . FragmentUuid = int             ( JSON [ "Fragment"            ] )
    ##########################################################################
    if                                      ( "Name"        in JSON        ) :
      ########################################################################
      self . DefaultTitle = JSON            [ "Name"                         ]
    ##########################################################################
    self   . reload                         (                                )
    ##########################################################################
    return
  ############################################################################
  def clickIn                        ( self , IDX                          ) :
    ##########################################################################
    if                               ( IDX < 0                             ) :
      ########################################################################
      IDX = self . topLevelItemCount (                                       )
      IDX = int                      ( IDX - 1                               )
    ##########################################################################
    CIT   = self . topLevelItem      ( IDX                                   )
    self  . setCurrentItem           ( CIT                                   )
    self  . twiceClicked             ( CIT , 2                               )
    ##########################################################################
    return
  ############################################################################
  def WaitFocusIn             ( self , IDX                                 ) :
    ##########################################################################
    time . sleep              ( 0.2                                          )
    self . emitFocusIn . emit (        IDX                                   )
    ##########################################################################
    return
  ############################################################################
  def InsertItem                        ( self                             ) :
    ##########################################################################
    IDX    = -1
    CIT    = self . currentItem         (                                    )
    ##########################################################################
    if                                  ( self . UsePtsForAdd              and
                                        ( self . CurrentPTS >= 0         ) ) :
      ########################################################################
      vlen = self . CurrentPTS
      IDX  = self . DESCRIBE . TimestampIndex ( vlen                         )
      IDX  = int                        ( IDX + 1                            )
      ########################################################################
    elif                                ( CIT in self . EmptySet           ) :
      ########################################################################
      vlen = self . DESCRIBE . LastestTimestamp ( self . TimeGap             )
      ########################################################################
    else                                                                     :
      ########################################################################
      IDX  = self . indexOfTopLevelItem ( CIT                                )
      slen = CIT  . data                ( 0 , Qt . UserRole                  )
      vlen = int                        ( int ( slen ) + self . TimeGap      )
      IDX  = int                        ( IDX + 1                            )
    ##########################################################################
    self   . DESCRIBE . addItem         ( vlen , ""                          )
    self   . reload                     (                                    )
    self   . Go                         ( self . WaitFocusIn , ( IDX , )     )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveItems                       )
    ##########################################################################
    return
  ############################################################################
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 2                                                  )
    ##########################################################################
    return
  ############################################################################
  def nameChanged                          ( self                          ) :
    ##########################################################################
    if                                     ( not self . isItemPicked (   ) ) :
      return False
    ##########################################################################
    item     = self . CurrentItem          [ "Item"                          ]
    column   = self . CurrentItem          [ "Column"                        ]
    line     = self . CurrentItem          [ "Widget"                        ]
    text     = self . CurrentItem          [ "Text"                          ]
    msg      = line . text                 (                                 )
    uuid     = self . itemUuid             ( item , 0                        )
    ##########################################################################
    self     . removeParked                (                                 )
    ##########################################################################
    if                                     ( 0 == column                   ) :
      ########################################################################
      OK , dlen = self . SCENE . FromFTime ( msg                             )
      ########################################################################
      if                                   ( OK                            ) :
        ######################################################################
        slen = item . data                 ( 0 , Qt . UserRole               )
        vlen = int                         ( slen                            )
        rlen = self . DESCRIBE . realTime  ( dlen                            )
        self . DESCRIBE . Replace          ( vlen , rlen                     )
        item . setText                     ( column , msg                    )
        self . emitReload . emit           (                                 )
      ########################################################################
    elif                                   ( 1 == column                   ) :
      ########################################################################
      OK , dlen = self . SCENE . FromFTime ( msg                             )
      ########################################################################
      if                                   ( OK                            ) :
        ######################################################################
        slen = item . data                 ( 0 , Qt . UserRole               )
        vlen = int                         ( slen                            )
        DTS  = str                         ( dlen                            )
        msg  = self . SCENE . toLTime      ( dlen                            )
        self . DESCRIBE . setOption        ( vlen , "Duration" , dlen        )
        item . setText                     ( column , msg                    )
        item . setData                     ( column , Qt . UserRole , DTS    )
        self . Notify                      ( 5                               )
      ########################################################################
    elif                                   ( 2 == column                   ) :
      ########################################################################
      slen   = item . data                 ( 0 , Qt . UserRole               )
      vlen   = int                         ( slen                            )
      item   . setText                     ( column , msg                    )
      self   . DESCRIBE . setContext       ( vlen , msg                      )
      self   . Notify                      ( 5                               )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 6                              )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                  ( self , TUIDs                          ) :
    ##########################################################################
    for T in TUIDs                                                           :
      ########################################################################
      self . DESCRIBE . deleteItem ( int ( T )                               )
    ##########################################################################
    self . emitReload . emit       (                                         )
    ##########################################################################
    return
  ############################################################################
  def FilmUpdatePTS                   ( self                               ) :
    ##########################################################################
    if                                ( self . CurrentPTS < 0              ) :
      return
    ##########################################################################
    item = self . currentItem         (                                      )
    ##########################################################################
    if                                ( item in self . EmptySet            ) :
      return
    ##########################################################################
    if                                ( not item . isSelected (          ) ) :
      return
    ##########################################################################
    dlen = self . CurrentPTS
    slen = item . data                ( 0 , Qt . UserRole                    )
    vlen = int                        ( slen                                 )
    DTS  = str                        ( dlen                                 )
    rlen = self . DESCRIBE . realTime ( dlen                                 )
    self . DESCRIBE . Replace         ( vlen , rlen                          )
    msg  = self . SCENE . toLTime     ( dlen                                 )
    item . setText                    ( 0 , msg                              )
    item . setData                    ( 0 , Qt . UserRole , DTS              )
    ##########################################################################
    return
  ############################################################################
  def PtsUpdateItem                         ( self                         ) :
    ##########################################################################
    if                                      ( self . CurrentPTS < 0        ) :
      return
    ##########################################################################
    IDX  = self . DESCRIBE . TimestampIndex ( self . CurrentPTS              )
    ##########################################################################
    if                                      ( IDX < 0                      ) :
      return
    ##########################################################################
    TLC  = self . topLevelItemCount         (                                )
    if                                      ( IDX >= TLC                   ) :
      return
    ##########################################################################
    PIT  = self . topLevelItem              ( IDX                            )
    CIT  = self . currentItem               (                                )
    ##########################################################################
    if                                      ( PIT == CIT                   ) :
      return
    ##########################################################################
    PIT  . setSelected                      ( True                           )
    self . setCurrentItem                   ( PIT                            )
    ##########################################################################
    return
  ############################################################################
  def GotoSegments                      ( self                             ) :
    ##########################################################################
    uxid = str                          ( self . ScenarioUuid                )
    head = self . windowTitle           (                                    )
    icon = self . windowIcon            (                                    )
    ##########################################################################
    JJ   = self . DESCRIBE . toScenario (                                    )
    ##########################################################################
    JJ [ "Album"    ] = self . AlbumUuid
    JJ [ "Fragment" ] = self . FragmentUuid
    JJ [ "Name"     ] = head
    ##########################################################################
    self . emitSegments . emit          ( self , head , uxid , JJ , icon     )
    ##########################################################################
    return
  ############################################################################
  def CloneFromSource         ( self                                       ) :
    ##########################################################################
    SL   = int                ( self . sourceLocality                        )
    TL   = self . getLocality (                                              )
    self . DESCRIBE . Clone   ( SL , TL                                      )
    self . reload             (                                              )
    ##########################################################################
    return
  ############################################################################
  def BackgroundSaveToDatabase         ( self                              ) :
    ##########################################################################
    if                                 ( self . ScenarioUuid <= 0          ) :
      ########################################################################
      self . Notify                    ( 1                                   )
      ########################################################################
      return
    ##########################################################################
    DB     = self . ConnectDB          (                                     )
    ##########################################################################
    if                                 ( self . NotOkay ( DB )             ) :
      ########################################################################
      self . Notify                    ( 1                                   )
      ########################################################################
      return
    ##########################################################################
    SCNTAB = self  . Tables            [ "Scenarios"                         ]
    DJSON  = self  . DESCRIBE . toJson (                                     )
    SJSON  = json  . dumps             ( DJSON                               )
    RJSON  = SJSON . encode            ( "utf-8"                             )
    UUID   = self  . ScenarioUuid
    ##########################################################################
    DB     . LockWrites                ( [ SCNTAB                          ] )
    ##########################################################################
    QQ     = f"""update {SCNTAB}
                 set `description` = %s
                 where ( `uuid` = {UUID} ) ;"""
    QQ     = " " . join                ( QQ . split (                      ) )
    DB     . QueryValues               ( QQ , ( RJSON ,                    ) )
    ##########################################################################
    DB     . UnlockTables              (                                     )
    DB     . Close                     (                                     )
    self   . Notify                    ( 5                                   )
    self   . emitUpdated . emit        (                                     )
    ##########################################################################
    return
  ############################################################################
  def SaveToDatabase ( self                                                ) :
    ##########################################################################
    self . Go        ( self . BackgroundSaveToDatabase                       )
    ##########################################################################
    return
  ############################################################################
  def AcceptJsonFromPlayer                ( self , PlayerJson              ) :
    ##########################################################################
    if                                    ( "Action" not in PlayerJson     ) :
      return
    ##########################################################################
    ACTION     = PlayerJson               [ "Action"                         ]
    ##########################################################################
    if                                    ( "Update" == ACTION             ) :
      ########################################################################
      if                                  ( "PTS" in PlayerJson            ) :
        ######################################################################
        PTS    = PlayerJson               [ "PTS"                            ]
        self   . CurrentPTS = int         ( int ( PTS ) * 1000               )
        ######################################################################
        if                                ( self . UsePtsForItem           ) :
          ####################################################################
          self . emitUpdatePtsItem . emit (                                  )
        ######################################################################
        if                                ( self . TrackPtsForItem         ) :
          ####################################################################
          self . emitUpdatePTS     . emit (                                  )
      ########################################################################
    elif                                  ( "Open"   == ACTION             ) :
    ##########################################################################
      self     . ConnectedFilmJson = PlayerJson
      ## print ( json . dumps ( PlayerJson ) )
    ##########################################################################
    return
  ############################################################################
  def ConnectingToPlayer               ( self , PLAYER                     ) :
    ##########################################################################
    self   . PlayerConnected = True
    self   . PlayerWidget = PLAYER
    ##########################################################################
    PLAYER . AskToReceive              ( self                                )
    self   . Leave           . connect ( PLAYER . LeaveReceive               )
    self   . AssignPlayerPTS . connect ( PLAYER . AssignPlayerPTS            )
    PLAYER . Leave           . connect ( self   . DisconnectFromPlayer       )
    ##########################################################################
    return
  ############################################################################
  def DisconnectFromPlayer ( self , PLAYER                                 ) :
    ##########################################################################
    if                     ( PLAYER != self . PlayerWidget                 ) :
      return
    ##########################################################################
    self . PlayerWidget    = None
    self . PlayerConnected = False
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
  def ColumnsMenu                   ( self , mm                            ) :
    ##########################################################################
    TRX     = self . Translations
    head    = self . headerItem     (                                        )
    COL     = mm   . addMenu        ( TRX [ "UI::Columns" ]                  )
    ##########################################################################
    msg     = self . getMenuItem    ( "ShowAllColumns"                       )
    mm      . addActionFromMenu     ( COL , 9501 , msg                       )
    ##########################################################################
    mm      . addSeparatorFromMenu  ( COL                                    )
    ##########################################################################
    for i in range                  ( 1 , self . columnCount ( )           ) :
      ########################################################################
      msg   = head . text           ( i                                      )
      if                            ( len ( msg ) <= 0                     ) :
        msg = TRX                   [ "UI::Whitespace"                       ]
      ########################################################################
      hid   = self . isColumnHidden ( i                                      )
      mm    . addActionFromMenu     ( COL , 9000 + i , msg , True , not hid  )
    ##########################################################################
    return mm
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( 9501 == at                            ) :
      ########################################################################
      for i in range               ( 1 , self . columnCount (            ) ) :
        ######################################################################
        self . setColumnHidden     ( i , False                               )
      ########################################################################
      return
    ##########################################################################
    DCOLs  = self . columnCount    (                                         )
    MCOLs  = int                   ( 9000 + DCOLs                            )
    ##########################################################################
    if                             ( ( at >= 9001 ) and ( at <= MCOLs )    ) :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def LocalityMenu               ( self , mm                               ) :
    ##########################################################################
    BASE  = int                  ( 10000000                                  )
    DFL   = self  . getLocality  (                                           )
    LANGZ = self  . getLanguages (                                           )
    MENUZ = self  . getMenus     (                                           )
    ##########################################################################
    LOM   = mm    . addMenu      ( MENUZ [ "Language" ]                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "CloneFromSource"                         )
    mm    . addActionFromMenu    ( LOM , BASE , MSG                          )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    KEYs  = LANGZ . keys         (                                           )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      MSG = LANGZ                [ K                                         ]
      V   = int                  ( K                                         )
      hid =                      ( V == DFL                                  )
      mm  . addActionFromMenu    ( LOM , BASE + V , MSG , True , hid         )
    ##########################################################################
    return mm
  ############################################################################
  def HandleLocalityMenu     ( self , atId                                 ) :
    ##########################################################################
    if                       ( 10000000 == atId                            ) :
      ########################################################################
      self . CloneFromSource (                                               )
      ########################################################################
      return False
    ##########################################################################
    if                       ( atId < 10000000                             ) :
      return False
    ##########################################################################
    if                       ( atId > 11000000                             ) :
      return False
    ##########################################################################
    self . setLocality       ( atId - 10000000                               )
    self . Go                ( self . UpdateLocalityUsage                    )
    ##########################################################################
    return True
  ############################################################################
  def SourceLocalityMenu         ( self , mm                               ) :
    ##########################################################################
    BASE  = int                  ( 11000000                                  )
    DFL   = int                  ( self  . sourceLocality                    )
    LANGZ = self  . Translations [ self . ClassTag ] [ "SourceLanguages"     ]
    MENUZ = self  . getMenus     (                                           )
    ##########################################################################
    MSG   = self  . getMenuItem  ( "SourceLanguage"                          )
    LOM   = mm    . addMenu      ( MSG                                       )
    ##########################################################################
    KEYs  = LANGZ . keys         (                                           )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      MSG = LANGZ                [ K                                         ]
      V   = int                  ( K                                         )
      hid =                      ( V == DFL                                  )
      mm  . addActionFromMenu    ( LOM , BASE + V , MSG , True , hid         )
    ##########################################################################
    return mm
  ############################################################################
  def HandleSourceLocalityMenu  ( self , atId                              ) :
    ##########################################################################
    if                          ( atId < 11000000                          ) :
      return False
    ##########################################################################
    if                          ( atId > 12000000                          ) :
      return False
    ##########################################################################
    self . sourceLocality = int ( atId - 11000000                            )
    ##########################################################################
    return True
  ############################################################################
  def TranslationsMenu            ( self , mm , item                       ) :
    ##########################################################################
    if                            ( item in self . EmptySet                ) :
      return mm
    ##########################################################################
    TRX    = self . Translations  [ "Translations"                           ]
    msg    = self . Translations  [ "UI::Translations"                       ]
    KEYs   = TRX  . keys          (                                          )
    ##########################################################################
    LOT    = mm   . addMenu       ( msg                                      )
    ##########################################################################
    MSG    = self . getMenuItem   ( "ConvertAllCC"                           )
    mm     . addActionFromMenu    ( LOT                                    , \
                                    7000                                   , \
                                    MSG                                    , \
                                    True                                   , \
                                    self . ConvertAllCC                      )
    ##########################################################################
    mm     . addSeparatorFromMenu ( LOT                                      )
    ##########################################################################
    for K in KEYs                                                            :
       msg = TRX                  [ K                                        ]
       V   = int                  ( K                                        )
       mm  . addActionFromMenu    ( LOT , V , msg                            )
    ##########################################################################
    return mm
  ############################################################################
  def ConvertItemCC                ( self , item , CODE                    ) :
    ##########################################################################
    column = 2
    pid    = item . data           ( 0 , Qt . UserRole                       )
    text   = item . text           ( column                                  )
    pid    = int                   ( pid                                     )
    cc     = OpenCC                ( CODE                                    )
    target = cc . convert          ( text                                    )
    UTF8   = len                   ( target                                  )
    LENZ   = 0
    ##########################################################################
    try                                                                      :
      ########################################################################
      S    = target . encode       ( "utf-8"                                 )
      LENZ = len                   ( S                                       )
      ########################################################################
    except                                                                   :
      return False
    ##########################################################################
    item   . setText               ( column , target                         )
    self   . DESCRIBE . setContext ( pid , target                            )
    ##########################################################################
    return   True
  ############################################################################
  def HandleTranslations             ( self , item , ID                    ) :
    ##########################################################################
    if                               ( 7000 == ID                          ) :
      ########################################################################
      self   . ConvertAllCC = not self . ConvertAllCC
      ########################################################################
      return
    ##########################################################################
    if                               ( ( ID < 7001 ) or ( ID > 7008 )      ) :
      return False
    ##########################################################################
    CODE     = self . ConvertCCCcode ( int ( ID - 7000  )                    )
    ##########################################################################
    if                               ( len ( CODE ) <= 0                   ) :
      return False
    ##########################################################################
    if                               ( self . ConvertAllCC                 ) :
      ########################################################################
      for ait in range               ( 0 , self . topLevelItemCount (    ) ) :
        ######################################################################
        ITX  = self . topLeveItem    ( ait                                   )
        self . ConvertItemCC         ( self , item , CODE                    )
      ########################################################################
      self   . Notify                ( 5                                     )
      ########################################################################
    else                                                                     :
      ########################################################################
      OKAY   = self . ConvertItemCC  ( self , item , CODE                    )
      ########################################################################
      if                             ( OKAY                                ) :
        ######################################################################
        self . Notify                ( 1                                     )
        ######################################################################
      else                                                                   :
        ######################################################################
        self . Notify                ( 5                                     )
    ##########################################################################
    return True
  ############################################################################
  def TranslateMenu            ( self , mm , item                          ) :
    ##########################################################################
    if                         ( item in self . EmptySet                   ) :
      return mm
    ##########################################################################
    BASE   = 15000000
    TRX    = self . Translations
    LOC    = TRX               [ self . ClassTag ] [ "Languages"             ]
    ##########################################################################
    msg    = TRX               [ "UI::Translate"                             ]
    LOM    = mm . addMenu      ( msg                                         )
    ##########################################################################
    KEYs   = LOC . keys        (                                             )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      V    = int               ( K                                           )
      ########################################################################
      if                       ( V < 1000                                  ) :
        continue
      ########################################################################
      if                       ( V in [ 1004 , 1005 ]                      ) :
        continue
      ########################################################################
      msg  = LOC               [ K                                           ]
      mm   . addActionFromMenu ( LOM , BASE + V , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunTranslate                     ( self , at , item                  ) :
    ##########################################################################
    if                                 ( item in self . EmptySet           ) :
      return
    ##########################################################################
    BASE   = 15000000
    ##########################################################################
    if                                 ( at < BASE                         ) :
      return False
    ##########################################################################
    if                                 ( at > ( BASE + 100000 )            ) :
      return False
    ##########################################################################
    SRC    = self . LocalityToGoogleLC ( self . sourceLocality               )
    DEST   = self . LocalityToGoogleLC ( int ( at - BASE )                   )
    ##########################################################################
    if                                 ( len ( SRC ) <= 0                  ) :
      return True
    ##########################################################################
    if                                 ( len ( DEST ) <= 0                 ) :
      return True
    ##########################################################################
    pid    = item . data               ( 0 , Qt . UserRole                   )
    txt    = item . text               ( 2                                   )
    pid    = int                       ( pid                                 )
    ##########################################################################
    if                                 ( len ( txt ) <= 0                  ) :
      ########################################################################
      self . Notify                    ( 1                                   )
      ########################################################################
      return True
    ##########################################################################
    target = Translate                 ( txt , SRC , DEST                    )
    UTF8   = len                       ( target                              )
    ##########################################################################
    if                                 ( UTF8 <= 0                         ) :
      ########################################################################
      self . Notify                    ( 1                                   )
      ########################################################################
      return True
    ##########################################################################
    LENZ   = 0
    ##########################################################################
    try                                                                      :
      S    = target . encode           ( "utf-8"                             )
      LENZ = len                       ( S                                   )
    except                                                                   :
      ########################################################################
      self . Notify                    ( 1                                   )
      ########################################################################
      return True
    ##########################################################################
    item   . setText                   ( 2   , target                        )
    self   . DESCRIBE . setContext     ( pid , target                        )
    self   . Notify                    ( 5                                   )
    ##########################################################################
    return False
  ############################################################################
  def MarkerMenu                   ( self , mm , item                      ) :
    ##########################################################################
    if                             ( item in self . EmptySet               ) :
      return mm
    ##########################################################################
    pid       = item . data                 ( 0 , Qt . UserRole              )
    pid       = int                         ( pid                            )
    CHAPTER   = self . DESCRIBE . getOption ( pid , "Chapter"                )
    PARAGRAPH = self . DESCRIBE . getOption ( pid , "Paragraph"              )
    SUBTITLE  = self . DESCRIBE . getOption ( pid , "Subtitle"               )
    ##########################################################################
    msg       = self . getMenuItem ( "Markers"                               )
    LOM       = mm   . addMenu     ( msg                                     )
    ##########################################################################
    msg       = self . getMenuItem ( "Chapter"                               )
    mm        . addActionFromMenu  ( LOM , 77410001 , msg , True , CHAPTER   )
    ##########################################################################
    msg       = self . getMenuItem ( "Paragraph"                             )
    mm        . addActionFromMenu  ( LOM , 77410002 , msg , True , PARAGRAPH )
    ##########################################################################
    msg       = self . getMenuItem ( "Subtitle"                              )
    mm        . addActionFromMenu  ( LOM , 77410003 , msg , True , SUBTITLE  )
    ##########################################################################
    return mm
  ############################################################################
  def RunMarkerMenu                        ( self , at , item              ) :
    ##########################################################################
    if                                     ( item in self . EmptySet       ) :
      return
    ##########################################################################
    items    = self . selectedItems        (                                 )
    ##########################################################################
    if                                     ( 77410001 == at                ) :
      ########################################################################
      for it in items                                                        :
        ######################################################################
        pid  = it . data                   ( 0 , Qt . UserRole               )
        pid  = int                         ( pid                             )
        ######################################################################
        OPT  = self . DESCRIBE . getOption ( pid , "Chapter"                 )
        ######################################################################
        if                                 ( OPT                           ) :
          ####################################################################
          self      . DESCRIBE . setOption ( pid , "Chapter"   , False       )
          self      . DESCRIBE . setOption ( pid , "Paragraph" , False       )
          ####################################################################
        else                                                                 :
          ####################################################################
          self      . DESCRIBE . setOption ( pid , "Chapter"   , True        )
          self      . DESCRIBE . setOption ( pid , "Paragraph" , False       )
        ######################################################################
        OPS  = self . DESCRIBE . OptionString ( pid                          )
        it   . setText                     ( 3 , OPS                         )
    ##########################################################################
    if                                     ( 77410002 == at                ) :
      ########################################################################
      for it in items                                                        :
        ######################################################################
        pid  = it . data                   ( 0 , Qt . UserRole               )
        pid  = int                         ( pid                             )
        ######################################################################
        OPT  = self . DESCRIBE . getOption ( pid , "Paragraph"               )
        ######################################################################
        if                                 ( OPT                           ) :
          ####################################################################
          self      . DESCRIBE . setOption ( pid , "Chapter"   , False       )
          self      . DESCRIBE . setOption ( pid , "Paragraph" , False       )
          ####################################################################
        else                                                                 :
          ####################################################################
          self      . DESCRIBE . setOption ( pid , "Chapter"   , False       )
          self      . DESCRIBE . setOption ( pid , "Paragraph" , True        )
        ######################################################################
        OPS  = self . DESCRIBE . OptionString ( pid                          )
        it   . setText                     ( 3 , OPS                         )
    ##########################################################################
    if                                     ( 77410003 == at                ) :
      ########################################################################
      for it in items                                                        :
        ######################################################################
        pid  = it . data                   ( 0 , Qt . UserRole               )
        pid  = int                         ( pid                             )
        ######################################################################
        OPT  = self . DESCRIBE . getOption ( pid , "Subtitle"                )
        self        . DESCRIBE . setOption ( pid , "Subtitle" , not OPT      )
        ######################################################################
        OPS  = self . DESCRIBE . OptionString ( pid                          )
        it   . setText                     ( 3 , OPS                         )
    ##########################################################################
    return False
  ############################################################################
  def BaseTimeMenu ( self , mm                                             ) :
    ##########################################################################
    FTIME = self . SCENE . toFTime     ( self . DESCRIBE . BaseTime          )
    self  . BaseTimeEditor = QLineEdit (                                     )
    self  . BaseTimeEditor . setText   ( FTIME                               )
    mm    . addWidget                  ( 9929991 , self . BaseTimeEditor     )
    ##########################################################################
    return mm
  ############################################################################
  def RunBaseTime ( self                                                   ) :
    ##########################################################################
    if            ( None == self . BaseTimeEditor                          ) :
      return False
    ##########################################################################
    FTIME      = self . BaseTimeEditor . text (                              )
    OK , RTIME = self . SCENE . FromFTime     ( FTIME                        )
    self       . BaseTimeEditor = None
    ##########################################################################
    if            ( not OK                                                 ) :
      return False
    ##########################################################################
    if            ( RTIME == self . DESCRIBE . BaseTime                    ) :
      return False
    ##########################################################################
    self . DESCRIBE . BaseTime = RTIME
    ##########################################################################
    return True
  ############################################################################
  def Menu                              ( self , pos                       ) :
    ##########################################################################
    if                                  ( not self . isPrepared (        ) ) :
      return False
    ##########################################################################
    doMenu = self . isFunction          ( self . HavingMenu                  )
    if                                  ( not doMenu                       ) :
      return False
    ##########################################################################
    self   . Notify                     ( 0                                  )
    items  , atItem , uuid = self . GetMenuDetails ( 0                       )
    mm     = MenuManager                ( self                               )
    ##########################################################################
    self   . BaseTimeMenu               ( mm                                 )
    self   . AppendRefreshAction        ( mm , 1001                          )
    ##########################################################################
    msg    = self . getMenuItem         ( "Save"                             )
    icon   = QIcon                      ( ":/images/vtsave.png"              )
    mm     . addActionWithIcon          ( 1501 , icon , msg                  )
    ##########################################################################
    self   . AppendInsertAction         ( mm , 1102                          )
    self   . AppendRenameAction         ( mm , 1103                          )
    self   . AppendDeleteAction         ( mm , 1104                          )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    msg    = self . getMenuItem         ( "OpenSegments"                     )
    icon   = QIcon                      ( ":/images/addcolumn.png"           )
    mm     . addActionWithIcon          ( 2001 , icon , msg                  )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    if                                  ( self . PlayerConnected           ) :
      ########################################################################
      msg  = self . getMenuItem         ( "DisconnectPlayer"                 )
      mm   . addAction                  ( 3002 , msg                         )
      ########################################################################
    else                                                                     :
      ########################################################################
      msg  = self . getMenuItem         ( "ConnectPlayer"                    )
      mm   . addAction                  ( 3001 , msg                         )
    ##########################################################################
    msg    = self . getMenuItem         ( "UsePtsForAdd"                     )
    mm     . addAction                  ( 4001                             , \
                                          msg                              , \
                                          True                             , \
                                          self . UsePtsForAdd                )
    ##########################################################################
    msg    = self . getMenuItem         ( "UsePtsForItem"                    )
    mm     . addAction                  ( 4002                             , \
                                          msg                              , \
                                          True                             , \
                                          self . UsePtsForItem               )
    ##########################################################################
    msg    = self . getMenuItem         ( "TrackPtsForItem"                  )
    mm     . addAction                  ( 4003                             , \
                                          msg                              , \
                                          True                             , \
                                          self . TrackPtsForItem             )
    ##########################################################################
    msg    = self . getMenuItem         ( "SyncPlayerTime"                   )
    mm     . addAction                  ( 4004                             , \
                                          msg                              , \
                                          True                             , \
                                          self . SyncPlayerTime              )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    self   . MarkerMenu                 ( mm , atItem                        )
    self   . TranslateMenu              ( mm , atItem                        )
    self   . TranslationsMenu           ( mm , atItem                        )
    self   . LocalityMenu               ( mm                                 )
    self   . SourceLocalityMenu         ( mm                                 )
    self   . ColumnsMenu                ( mm                                 )
    self   . SortingMenu                ( mm                                 )
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                    ( self    . menuFont (             ) )
    aa     = mm . exec_                 ( QCursor . pos      (             ) )
    at     = mm . at                    ( aa                                 )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunBaseTime         (                                    )
    if                                  ( OKAY                             ) :
      ########################################################################
      self . reload                     (                                    )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunDocking          ( mm , aa                            )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu  ( at                                 )
    ##########################################################################
    if                                  ( OKAY                             ) :
      ########################################################################
      self . DESCRIBE . setLocality     ( self . getLocality (             ) )
      self . reload                     (                                    )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu      ( at                                 )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu      ( at                                 )
    if                                  ( OKAY                             ) :
      ########################################################################
      self . reload                     (                                    )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunTranslate        ( at , atItem                        )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . HandleSourceLocalityMenu ( at                            )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . HandleTranslations  ( atItem , at                        )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    OKAY   = self . RunMarkerMenu       ( at , atItem                        )
    if                                  ( OKAY                             ) :
      return True
    ##########################################################################
    if                                  ( 1001 == at                       ) :
      ########################################################################
      self . reload                     (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( 1102 == at                       ) :
      self . InsertItem                 (                                    )
      return True
    ##########################################################################
    if                                  ( 1103 == at                       ) :
      self . RenameItem                 (                                    )
      return True
    ##########################################################################
    if                                  ( 1104 == at                       ) :
      self . DeleteItems                (                                    )
      return True
    ##########################################################################
    if                                  ( 1501 == at                       ) :
      self . SaveToDatabase             (                                    )
      return True
    ##########################################################################
    if                                  ( 2001 == at                       ) :
      self . GotoSegments               (                                    )
      return True
    ##########################################################################
    if                                  ( 3001 == at                       ) :
      self . emitConnector       . emit ( self                               )
      return True
    ##########################################################################
    if                                  ( 3002 == at                       ) :
      ########################################################################
      self . emitDetachConnector . emit ( self                               )
      ########################################################################
      self . ConnectedFilmJson =        {                                    }
      self . CurrentPTS        = -1
      self . PlayerConnected   = False
      ########################################################################
      return True
    ##########################################################################
    if                                  ( 4001 == at                       ) :
      self . UsePtsForAdd    = not self . UsePtsForAdd
      return True
    ##########################################################################
    if                                  ( 4002 == at                       ) :
      self . UsePtsForItem   = not self . UsePtsForItem
      return True
    ##########################################################################
    if                                  ( 4003 == at                       ) :
      self . TrackPtsForItem = not self . TrackPtsForItem
      return True
    ##########################################################################
    if                                  ( 4004 == at                       ) :
      self . SyncPlayerTime  = not self . SyncPlayerTime
      return True
    ##########################################################################
    return True
##############################################################################
