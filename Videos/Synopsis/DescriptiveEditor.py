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
from           . Fragment              import Fragment    as FragmentItem
from           . Scenario              import Scenario    as ScenarioItem
from           . Descriptive           import Descriptive as DescriptiveItem
from           . Descriptive           import Segment     as SegmentItem
from           . Descriptive           import Anchor      as AnchorItem
##############################################################################
class DescriptiveEditor  ( TreeDock                                        ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = Signal (                                                   )
  emitAllNames  = Signal ( list                                              )
  emitSegments  = Signal ( QWidget , str , str , dict , QIcon                )
  emitLog       = Signal ( str                                               )
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    ##########################################################################
    self . ClassTag           = "DescriptiveEditor"
    self . FetchTableKey      = self . ClassTag
    self . GType              = 212
    self . ScenarioUuid       = 0
    self . DJSON              = {                                            }
    ##########################################################################
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
                                      self . GotoSegments                    )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . restart         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
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
  def twiceClicked ( self , item , column                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PrepareItem ( self , POS , BT , JSON , BRUSH                         ) :
    ##########################################################################
    ##########################################################################
    return IT
  ############################################################################
  def RefreshToolTip          ( self , Total                               ) :
    ##########################################################################
    ## FMT  = self . getMenuItem ( "DisplayTotal"                               )
    ## MSG  = FMT  . format      ( Total , self . Total                         )
    ## self . setToolTip         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def refresh                     ( self , LISTs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    CNT    = 0
    POS    = 0
    BT     = 0
    MOD    = len                  ( self . TreeBrushes                       )
    ##########################################################################
    for JSON in LISTs                                                        :
      ########################################################################
      POS  = int                  ( POS + 1                                  )
      ########################################################################
      IT   = self . PrepareItem   ( POS                                    , \
                                    BT                                     , \
                                    JSON                                   , \
                                    self . TreeBrushes [ CNT ]               )
      self . addTopLevelItem      ( IT                                       )
      ########################################################################
      ## DURT = int                  ( JSON [ "Duration"                      ] )
      ## BT   = int                  ( BT + DURT                                )
      CNT  = int                  ( int ( CNT + 1 ) % MOD                    )
    ##########################################################################
    self   . RefreshToolTip       ( len ( LISTs )                            )
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def loading                   ( self                                     ) :
    ##########################################################################
    ##########################################################################
    ## self . emitAllNames  . emit ( L                                          )
    self . Notify               ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def startScenario  ( self , Uuid , JSON                                  ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . ScenarioUuid = Uuid
    self   . DJSON        = JSON
    ##########################################################################
    ## self   . Go      ( self . loading                                        )
    self   . show    (                                                       )
    ##########################################################################
    return
  ############################################################################
  def InsertItem              ( self                                       ) :
    ##########################################################################
    ## item = QTreeWidgetItem    (                                              )
    ## item . setData            ( 0 , Qt . UserRole , 0                        )
    ## item . setData            ( 1 , Qt . UserRole , 0                        )
    ## self . addTopLevelItem    ( item                                         )
    ## line = self . setLineEdit ( item                                       , \
    ##                             1                                          , \
    ##                             "editingFinished"                          , \
    ##                             self . nameChanged                           )
    ## line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    if                        ( not self . isGrouping ( )                  ) :
      return
    ##########################################################################
    ## self . defaultDeleteItems ( 0 , self . RemoveItems                       )
    ##########################################################################
    return
  ############################################################################
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
    ##########################################################################
    return
  ############################################################################
  def nameChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item , 0                                   )
    ##########################################################################
    if                          ( len ( msg ) <= 0                         ) :
      self . removeTopLevelItem ( item                                       )
      return
    ##########################################################################
    item   . setText            ( column , msg                               )
    ##########################################################################
    self   . removeParked       (                                            )
    VAL    =                    ( item , uuid , msg ,                        )
    ## self   . Go                 ( self . AssureUuidItem , VAL                )
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
    self . defaultPrepare ( self . ClassTag , 9                              )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def GotoSegments             ( self                                      ) :
    ##########################################################################
    uxid = str                 ( self . ScenarioUuid                         )
    head = self . windowTitle  (                                             )
    icon = self . windowIcon   (                                             )
    ##########################################################################
    self . emitSegments . emit ( self                                      , \
                                 head                                      , \
                                 uxid                                      , \
                                 self . DJSON                              , \
                                 icon                                        )
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
    if                             ( at >= 9001 ) and ( at <= 9013 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
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
    if                                 ( 1001 == at                        ) :
      ########################################################################
      self . restart                   (                                     )
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
    if                                 ( 2001 == at                        ) :
      self . GotoSegments              (                                     )
      return True
    ##########################################################################
    return True
##############################################################################
