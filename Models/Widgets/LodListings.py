# -*- coding: utf-8 -*-
##############################################################################
## LodListings
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
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
class LodListings                  ( TreeDock                              ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow       = pyqtSignal (                                         )
  emitAllNames        = pyqtSignal ( list                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . CKEY               = "LodListings"
    self . EditAllNames       = None
    ##########################################################################
    self . Uuid               = 0
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
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
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 800 , 480 )                       )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    ##########################################################################
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    ##########################################################################
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
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
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 0 ]                      ) :
      return
    ##########################################################################
    if                          ( column     in [ 0 ]                      ) :
      ########################################################################
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItem           ( self , JSON                                  ) :
    ##########################################################################
    UUID  = JSON            [ "Id"                                           ]
    USED  = JSON            [ "Used"                                         ]
    LTYPE = JSON            [ "Type"                                         ]
    LEVEL = JSON            [ "Level"                                        ]
    USAGE = JSON            [ "Usage"                                        ]
    NAME  = JSON            [ "Name"                                         ]
    FMT   = JSON            [ "Format"                                       ]
    LPARM = JSON            [ "Parameters"                                   ]
    LBODY = JSON            [ "Body"                                         ]
    UXID  = str             ( UUID                                           )
    ##########################################################################
    IT    = QTreeWidgetItem (                                                )
    ##########################################################################
    IT    . setText         ( 0 , NAME                                       )
    IT    . setToolTip      ( 0 , UXID                                       )
    IT    . setData         ( 0 , Qt . UserRole , UXID                       )
    ##########################################################################
    IT    . setText         ( 1 , LEVEL                                      )
    IT    . setText         ( 2 , USED                                       )
    IT    . setText         ( 3 , LTYPE                                      )
    IT    . setText         ( 4 , USAGE                                      )
    IT    . setText         ( 5 , LPARM                                      )
    IT    . setText         ( 6 , LBODY                                      )
    ##########################################################################
    IT   . setData          ( 7 , Qt . UserRole , JSON                       )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 0                                         ] )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def nameChanged                ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    line   = self . CurrentItem  [ "Widget"                                  ]
    text   = self . CurrentItem  [ "Text"                                    ]
    msg    = line . text         (                                           )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    if                           ( len ( msg ) <= 0                        ) :
      self . removeTopLevelItem  ( item                                      )
      return
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    self   . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , msg , )                   )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , LISTS                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for JSON in LISTS                                                        :
      ########################################################################
      IT   = self . PrepareItem   ( JSON                                     )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( LISTS )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    self   . Notify               ( 5                                        )
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
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    LISTs   =                         [                                      ]
    UUID    = self . Uuid
    LODTAB  = self . Tables           [ "LOD"                                ]
    ##########################################################################
    QQ      = f"""select `id` , `used` , `type` , `level` ,
                         `usage` , `name` , `format` ,
                         length(`parameters`) , length(`body`) from {LODTAB}
                  where ( `used` > 0 )
                    and ( `uuid` = {UUID} )
                  order by `id` asc ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    ##########################################################################
    DB      . Query                   ( QQ                                   )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    if ( ( ALL not in [ False , None ] ) and ( len ( ALL ) > 0 ) )           :
      ########################################################################
      for ITEM in ALL                                                        :
        ######################################################################
        if                            ( len ( ITEM ) == 9                  ) :
          ####################################################################
          LOID  = int                 ( ITEM [ 0                           ] )
          USED  = int                 ( ITEM [ 1                           ] )
          LTYPE = int                 ( ITEM [ 2                           ] )
          LEVEL = int                 ( ITEM [ 3                           ] )
          USAGE = self . assureString ( ITEM [ 4                           ] )
          NAME  = self . assureString ( ITEM [ 5                           ] )
          FMT   = self . assureString ( ITEM [ 6                           ] )
          LPARM = int                 ( ITEM [ 7                           ] )
          LBODY = int                 ( ITEM [ 8                           ] )
          ####################################################################
          J     = { "Id"         : LOID                                    , \
                    "Used"       : USED                                    , \
                    "Type"       : LTYPE                                   , \
                    "Level"      : LEVEL                                   , \
                    "Usage"      : USAGE                                   , \
                    "Name"       : NAME                                    , \
                    "Format"     : FMT                                     , \
                    "Parameters" : LPARM                                   , \
                    "Body"       : LBODY                                     }
          ####################################################################
          LISTs . append              ( J                                    )
    ##########################################################################
    self    . Total = len             ( LISTs                                )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( LISTs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( LISTs                                )
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
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . CKEY , 7                                  )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    STOTAB = self . Tables    [ "StellarObjects"                             ]
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ STOTAB , NAMTAB                          ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      uuid = DB . LastUuid    ( STOTAB , "uuid" , self . BaseUuid            )
      DB   . AppendUuid       ( STOTAB ,  uuid                               )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
    ##########################################################################
    return
  ############################################################################
  def AppendLodItem           ( self                                       ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    LODTAB = self . Tables    [ "LOD"                                        ]
    UUID   = self . Uuid
    ##########################################################################
    DB     . LockWrites       ( [ LODTAB                                   ] )
    ##########################################################################
    QQ     = f"insert into {LODTAB} ( `uuid` ) values ( {UUID} ) ;"
    QQ     = " " . join       ( QQ . split ( )                               )
    ##########################################################################
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot      (                                                           )
  def InsertItem ( self                                                    ) :
    ##########################################################################
    self . Go    ( self . AppendLodItem                                      )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                              (                                   )
  def PasteItems                         ( self                            ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def GroupsMenu               ( self , mm , uuid , item                   ) :
    ##########################################################################
    if                         ( uuid <= 0                                 ) :
      return mm
    ##########################################################################
    TRX = self . Translations
    FMT = self . getMenuItem   ( "Belongs"                                   )
    MSG = FMT  . format        ( item . text ( 0 )                           )
    LOM = mm   . addMenu       ( MSG                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "CopyLodId"                                 )
    mm  . addActionFromMenu    ( LOM , 24231101 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "AppendLodId"                               )
    mm  . addActionFromMenu    ( LOM , 24231102 , msg                        )
    ##########################################################################
    ## mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    ## msg = self . getMenuItem   ( "Subgroup"                                  )
    ## mm  . addActionFromMenu    ( LOM , 24231201 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , uuid , item              ) :
    ##########################################################################
    if                              ( at == 24231101                       ) :
      ########################################################################
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231102                       ) :
      ########################################################################
      appendUuid                    ( uuid                                   )
      self . Notify                 ( 5                                      )
      ########################################################################
      return
    ##########################################################################
    return False
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
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
    if                              ( not self . isPrepared ( )            ) :
      return False
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items  = self . selectedItems   (                                        )
    atItem = self . currentItem     (                                        )
    uuid   = 0
    ##########################################################################
    if                              ( atItem != None                       ) :
      uuid = atItem . data          ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    self   . AppendInsertAction     ( mm , 1101                              )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      self . AppendRenameAction     ( mm , 1102                              )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . GroupsMenu             ( mm , uuid , atItem                     )
    self   . ColumnsMenu            ( mm                                     )
    self   . SortingMenu            ( mm                                     )
    self   . LocalityMenu           ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self   . RunAmountIndexMenu ( )      ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu   ( at , uuid , atItem                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      ########################################################################
      self . InsertItem             (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1102                           ) :
      ########################################################################
      self . RenameItem             (                                        )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
