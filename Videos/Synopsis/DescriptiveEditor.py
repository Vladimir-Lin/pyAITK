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
class DescriptiveEditor  ( TreeDock                                        ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = Signal (                                                   )
  emitReload    = Signal (                                                   )
  emitUpdated   = Signal (                                                   )
  emitFocusIn   = Signal ( int                                               )
  emitSegments  = Signal ( QWidget , str , str , dict , QIcon                )
  emitPlayer    = Signal ( QWidget                                           )
  emitLog       = Signal ( str                                               )
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
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
    self . SortOrder          = "asc"
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
    self . setColumnCount          ( 6                                       )
    self . setColumnWidth          ( 0 , 120                                 )
    self . setColumnWidth          ( 1 , 600                                 )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 3 , True                                )
    self . setColumnHidden         ( 4 , True                                )
    self . setColumnHidden         ( 5 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitReload    . connect ( self . reload                           )
    self . emitFocusIn   . connect ( self . clickIn                          )
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
    self . defaultSingleClicked (        item , column                       )
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
      line = self . setLineEdit     ( item                                 , \
                                      column                               , \
                                      "editingFinished"                    , \
                                      self . nameChanged                     )
      line . setFocus               ( Qt . TabFocusReason                    )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                  ( self , JSON , BRUSH                   ) :
    ##########################################################################
    STIME = int                    ( JSON [ "Shift"                        ] )
    RTIME = str                    ( JSON [ "Timestamp"                    ] )
    NAME  =                          JSON [ "Name"                           ]
    ##########################################################################
    FTIME = self . SCENE . toLTime ( STIME                                   )
    ##########################################################################
    IT    = QTreeWidgetItem        (                                         )
    IT    . setData                ( 0 , Qt . UserRole , str ( RTIME )       )
    IT    . setText                ( 0 , FTIME                               )
    IT    . setTextAlignment       ( 0 , Qt . AlignRight                     )
    IT    . setText                ( 1 , NAME                                )
    ##########################################################################
    for COL in range               ( 0 , self . columnCount (            ) ) :
      ########################################################################
      IT  . setBackground          ( COL , BRUSH                             )
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
    self  . twiceClicked             ( CIT , 1                               )
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
    if                                  ( CIT in self . EmptySet           ) :
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
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    self . defaultDeleteItems ( 0 , self . RemoveItems                       )
    ##########################################################################
    return
  ############################################################################
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 1                                                  )
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
    self . defaultPrepare ( self . ClassTag , 5                              )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                  ( self , TUIDs                          ) :
    ##########################################################################
    for T in TUIDs                                                           :
      ########################################################################
      self . DESCRIBE . deleteItem ( T                                       )
    ##########################################################################
    self . emitReload . emit       (                                         )
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
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    DCOLs  = self . columnCount    (                                         )
    MCOLs  = int                   ( 9000 + DCOLs                            )
    ##########################################################################
    if                             ( ( at >= 9002 ) and ( at <= MCOLs )    ) :
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
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    if                                 ( not self . isPrepared (         ) ) :
      return False
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    items  , atItem , uuid = self . GetMenuDetails ( 0                       )
    mm     = MenuManager               ( self                                )
    ##########################################################################
    self   . AppendRefreshAction       ( mm , 1001                           )
    ##########################################################################
    msg    = self . getMenuItem        ( "Save"                              )
    icon   = QIcon                     ( ":/images/vtsave.png"               )
    mm     . addActionWithIcon         ( 1501 , icon , msg                   )
    ##########################################################################
    self   . AppendInsertAction        ( mm , 1102                           )
    self   . AppendRenameAction        ( mm , 1103                           )
    self   . AppendDeleteAction        ( mm , 1104                           )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    msg    = self . getMenuItem        ( "OpenSegments"                      )
    icon   = QIcon                     ( ":/images/addcolumn.png"            )
    mm     . addActionWithIcon         ( 2001 , icon , msg                   )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . ColumnsMenu               ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . SourceLocalityMenu        ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                   ( self    . menuFont (              ) )
    aa     = mm . exec_                ( QCursor . pos      (              ) )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    ##########################################################################
    if                                 ( OKAY                              ) :
      ########################################################################
      self . DESCRIBE . setLocality    ( self . getLocality (              ) )
      self . reload                    (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . reload                    (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . HandleSourceLocalityMenu ( at                            )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( 1001 == at                        ) :
      ########################################################################
      self . reload                    (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( 1102 == at                        ) :
      self . InsertItem                (                                     )
      return True
    ##########################################################################
    if                                 ( 1103 == at                        ) :
      self . RenameItem                (                                     )
      return True
    ##########################################################################
    if                                 ( 1104 == at                        ) :
      self . DeleteItems               (                                     )
      return True
    ##########################################################################
    if                                 ( 1501 == at                        ) :
      self . SaveToDatabase            (                                     )
      return True
    ##########################################################################
    if                                 ( 2001 == at                        ) :
      self . GotoSegments              (                                     )
      return True
    ##########################################################################
    return True
##############################################################################
