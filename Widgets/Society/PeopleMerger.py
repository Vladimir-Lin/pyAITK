# -*- coding: utf-8 -*-
##############################################################################
## PeopleMerger
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
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . TreeDock          import TreeDock    as TreeDock
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
from   AITK . People    . People      import People      as PeopleItem
##############################################################################
class PeopleMerger                 ( TreeDock                              ) :
  ############################################################################
  HavingMenu       = 1371434312
  ############################################################################
  emitNamesShow    = pyqtSignal    (                                         )
  emitAppendPeople = pyqtSignal    ( dict                                    )
  emitComplete     = pyqtSignal    (                                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 2                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAppendPeople  . connect ( self . appending                    )
    self . emitComplete      . connect ( self . CompleteMerge                )
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
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 320 , 640                               )
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    self . LinkAction      ( "Refresh"    , self . startup                   )
    ##########################################################################
    self . LinkAction      ( "Paste"      , self . PasteItems                )
    self . LinkAction      ( "Delete"     , self . DeleteItems               )
    ##########################################################################
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
    self . LinkAction      ( "Paste"      , self . PasteItems      , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem           ( self , UUID , NAME                           ) :
    ##########################################################################
    UXID = str              ( UUID                                           )
    IT   = QTreeWidgetItem  (                                                )
    IT   . setText          ( 0 , NAME                                       )
    IT   . setToolTip       ( 0 , UXID                                       )
    IT   . setData          ( 0 , Qt . UserRole , UUID                       )
    IT   . setTextAlignment ( 1 , Qt.AlignRight                              )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                           (                                      )
  def DeleteItems                     ( self                               ) :
    ##########################################################################
    items  = self . selectedItems     (                                      )
    for item in items                                                        :
      self . pendingRemoveItem . emit ( item                                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      ( dict                                      )
  ############################################################################
  def appending                  ( self , JSON                             ) :
    ##########################################################################
    UUIDs = JSON                 [ "Uuids"                                   ]
    NAMEs = JSON                 [ "Names"                                   ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME  = NAMEs              [ UUID                                      ]
      IT    = self . PrepareItem ( UUID , NAME                               )
      self  . addTopLevelItem    ( IT                                        )
    ##########################################################################
    self    . Notify             ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot          (                                                       )
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self . clear     (                                                       )
    self . show      (                                                       )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "people/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                            ( self                            , \
                                           sourceWidget                    , \
                                           mimeData                        , \
                                           mousePos                        ) :
    ##########################################################################
    if                                   ( self == sourceWidget            ) :
      return False
    ##########################################################################
    RDN     = self . RegularDropNew      ( mimeData                          )
    if                                   ( not RDN                         ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON          [ "Mime"                            ]
    UUIDs   = self . DropInJSON          [ "UUIDs"                           ]
    ##########################################################################
    if                                   ( mtype in [ "people/uuids" ]     ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "Copying"                         )
      MSG   = FMT  . format              ( title , CNT                       )
      self  . ShowStatus                 ( MSG                               )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople                    ( self , source , pos , JSON           ) :
    return self . defaultDropInside ( source                               , \
                                      JSON                                 , \
                                      self . PeopleToMerge                   )
  ############################################################################
  def PeopleToMerge                  ( self , UUIDs                        ) :
    ##########################################################################
    COUNT  = len                     ( UUIDs                                 )
    if                               ( COUNT <= 0                          ) :
      return
    ##########################################################################
    DB     = self . ConnectDB        ( UsePure = True                        )
    if                               ( DB in [ False , None ]              ) :
      return
    ##########################################################################
    self   . setDroppingAction       ( True                                  )
    self   . OnBusy  . emit          (                                       )
    self   . setBustle               (                                       )
    ##########################################################################
    FMT    = self . getMenuItem      ( "Joining"                             )
    MSG    = FMT  . format           ( COUNT                                 )
    self   . ShowStatus              ( MSG                                   )
    self   . TtsTalk                 ( MSG , 1002                            )
    ##########################################################################
    NAMTAB = self . Tables           [ "Names"                               ]
    ##########################################################################
    NAMEs  = self . GetNames         ( DB , NAMTAB , UUIDs                   )
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME = NAMEs                   [ UUID                                  ]
      if                             ( len ( NAME ) <= 0                   ) :
        NAMEs [ UUID ] = f"{UUID}"
    ##########################################################################
    self   . setVacancy              (                                       )
    self   . GoRelax . emit          (                                       )
    self   . setDroppingAction       ( False                                 )
    self   . ShowStatus              ( ""                                    )
    DB     . Close                   (                                       )
    ##########################################################################
    JSON   =                         { "Uuids" : UUIDs , "Names" : NAMEs     }
    self   . emitAppendPeople . emit ( JSON                                  )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "PeopleMerger" , 2                               )
    ##########################################################################
    return
  ############################################################################
  def PasteItems                        ( self                             ) :
    ##########################################################################
    T     = qApp . clipboard ( ) . text (                                    )
    ##########################################################################
    if                                  ( len ( T ) <= 0                   ) :
      return
    ##########################################################################
    L     = T . split                   (                                    )
    UUIDs =                             [                                    ]
    for U in L                                                               :
      ########################################################################
      UX  = f"{U}"
      UX  = UX . strip                  (                                    )
      UX  = UX . rstrip                 (                                    )
      UX  = int                         ( UX                                 )
      if                                ( UX not in UUIDs                  ) :
        UUIDs . append                  ( UX                                 )
    ##########################################################################
    if                                  ( len ( UUIDs ) <= 0               ) :
      return
    ##########################################################################
    self  . Go                          ( self . PeopleToMerge , ( UUIDs , ) )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def ExecuteMerge             ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in [ False , None ]                    ) :
      return
    ##########################################################################
    PIT  = PeopleItem          (                                             )
    PIT  . Settings = self . Settings
    PIT  . Tables   = self . Tables
    ##########################################################################
    PIT  . MergeAll            ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def CompleteMerge           ( self                                       ) :
    ##########################################################################
    self . setEnabled         ( True                                         )
    ##########################################################################
    msg  = self . getMenuItem ( "FinishMerge"                                )
    self . ShowStatus         ( msg                                          )
    self . Notify             ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def ExecuteMergePeople              ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . ExecuteMerge , VAL            )
    ##########################################################################
    return
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
    Total  = self . topLevelItemCount (                                      )
    items  = self . selectedItems     (                                      )
    atItem = self . currentItem       (                                      )
    uuid   = 0
    ##########################################################################
    if                                ( atItem != None                     ) :
      uuid = atItem . data            ( 0 , Qt . UserRole                    )
      uuid = int                      ( uuid                                 )
    ##########################################################################
    mm     = MenuManager              ( self                                 )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                                ( Total > 1                          ) :
      ########################################################################
      msg  = self . getMenuItem       ( "Merge"                              )
      mm   . addAction                ( 7001 , msg                           )
      mm   . addSeparator             (                                      )
    ##########################################################################
    self   . AppendRefreshAction      ( mm , 1001                            )
    ##########################################################################
    if                                ( len ( items ) > 0                  ) :
      self . AppendDeleteAction       ( mm , 1102                            )
    ##########################################################################
    mm     . addSeparator             (                                      )
    ##########################################################################
    mm     = self . LocalityMenu      ( mm                                   )
    self   . DockingMenu              ( mm                                   )
    ##########################################################################
    mm     . setFont                  ( self    . menuFont ( )               )
    aa     = mm . exec_               ( QCursor . pos      ( )               )
    at     = mm . at                  ( aa                                   )
    ##########################################################################
    if                                ( self . RunDocking   ( mm , aa )    ) :
      return True
    ##########################################################################
    if                                ( self . HandleLocalityMenu ( at )   ) :
      return True
    ##########################################################################
    if                                ( at == 1001                         ) :
      self . startup                  (                                      )
      return True
    ##########################################################################
    if                                ( at == 1102                         ) :
      self . DeleteItems              (                                      )
      return True
    ##########################################################################
    if                                ( at == 7001                         ) :
      ########################################################################
      self . ExecuteMergePeople       (                                      )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################