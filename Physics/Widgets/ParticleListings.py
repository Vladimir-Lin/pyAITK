# -*- coding: utf-8 -*-
##############################################################################
## ParticleListings
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
class ParticleListings             ( TreeDock                              ) :
  ############################################################################
  HavingMenu     = 1371434312
  ############################################################################
  emitNamesShow  = pyqtSignal      (                                         )
  emitAllNames   = pyqtSignal      ( list                                    )
  OpenLogHistory = pyqtSignal      ( str , str , str , str , str             )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ClassTag           = "ParticleListings"
    self . EditAllNames       = None
    self . SortOrder          = "asc"
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
    return self . SizeSuggestion ( QSize ( 800 , 640 )                       )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    """
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationNames             )
    self . WindowActions . append ( A                                        )
    """
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
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
    self . LinkVoice         ( self . CommandParser                          )
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
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in [ 1 , 6 ]                 ) :
      return
    ##########################################################################
    if                           ( column     in [ 1 , 6 ]                 ) :
      ########################################################################
      line = self . setLineEdit  ( item                                    , \
                                   column                                  , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                  ( self , JSON                           ) :
    ##########################################################################
    UUID       = JSON              [ "Uuid"                                  ]
    ID         = JSON              [ "Id"                                    ]
    USED       = JSON              [ "Used"                                  ]
    PTYPE      = JSON              [ "Type"                                  ]
    CATALOG    = JSON              [ "Catalog"                               ]
    THEORY     = JSON              [ "Theory"                                ]
    SYMBOL     = JSON              [ "Symbol"                                ]
    COMMENT    = JSON              [ "Comment"                               ]
    NAME       = JSON              [ "Name"                                  ]
    UXID       = str               ( UUID                                    )
    ##########################################################################
    IT         = QTreeWidgetItem   (                                         )
    ##########################################################################
    IT         . setText           ( 0 , str ( ID )                          )
    IT         . setToolTip        ( 0 , UXID                                )
    IT         . setData           ( 0 , Qt . UserRole , UXID                )
    IT         . setTextAlignment  ( 0 , Qt.AlignRight                       )
    ##########################################################################
    IT         . setText           ( 1 , SYMBOL                              )
    IT         . setText           ( 2 , NAME                                )
    ##########################################################################
    IT         . setText           ( 3 , str ( PTYPE   )                     )
    IT         . setTextAlignment  ( 3 , Qt.AlignRight                       )
    IT         . setData           ( 3 , Qt . UserRole , PTYPE               )
    ##########################################################################
    IT         . setText           ( 4 , str ( CATALOG )                     )
    IT         . setData           ( 4 , Qt . UserRole , CATALOG             )
    ##########################################################################
    IT         . setText           ( 5 , str ( THEORY  )                     )
    IT         . setData           ( 5 , Qt . UserRole , THEORY              )
    ##########################################################################
    IT         . setText           ( 6 , COMMENT                             )
    ##########################################################################
    IT         . setData           ( 7 , Qt . UserRole , JSON                )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 6                                         ] )
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
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    if                           ( column in [ 1 , 6 ]                     ) :
      ########################################################################
      self . Go                  ( self . UpdateColumnValue                , \
                                   ( item , uuid , column , msg , )          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , LISTs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for JSOX in LISTs                                                        :
      ########################################################################
      IT   = self . PrepareItem   ( JSOX                                     )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( LISTs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainParticles                    ( self , DB                         ) :
    ##########################################################################
    LISTs    =                         [                                     ]
    UUIDs    = self . ObtainsItemUuids ( DB                                  )
    NAMEs    =                         [                                     ]
    if                                 ( len ( UUIDs ) > 0                 ) :
      NAMEs  = self . ObtainsUuidNames ( DB , UUIDs                          )
    ##########################################################################
    PTSTAB   = self . Tables           [ "Particles"                         ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ     = f"""select
                   `id`,`used`,`type`,`catalog`,
                   `theory`,`name`,`comment`
                   from {PTSTAB}
                   where ( `uuid` = {UUID} ) ;"""
      QQ     = " " . join              ( QQ . split ( )                      )
      DB     . Query                   ( QQ                                  )
      RR     = DB . FetchOne           (                                     )
      ########################################################################
      if                               ( self . NotOkay ( RR )             ) :
        continue
      ########################################################################
      if                               ( len ( RR ) != 7                   ) :
        continue
      ########################################################################
      NAME   = ""
      if                               ( UUID in NAMEs                     ) :
        NAME = NAMEs                   [ UUID                                ]
      ########################################################################
      J               =                {                                     }
      J [ "Id"      ] = int            ( RR [ 0                            ] )
      J [ "Uuid"    ] = int            ( UUID                                )
      J [ "Used"    ] = int            ( RR [ 1                            ] )
      J [ "Type"    ] = int            ( RR [ 2                            ] )
      J [ "Catalog" ] = int            ( RR [ 3                            ] )
      J [ "Theory"  ] = int            ( RR [ 4                            ] )
      J [ "Symbol"  ] = self . assureString ( RR [ 5 ]                       )
      J [ "Comment" ] = self . assureString ( RR [ 6 ]                       )
      J [ "Name"    ] = NAME
      ########################################################################
      LISTs . append                   ( J                                   )
    ##########################################################################
    return LISTs
  ############################################################################
  def loading                       ( self                                 ) :
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      self . emitNamesShow . emit   (                                        )
      return
    ##########################################################################
    self   . Notify                 ( 3                                      )
    ##########################################################################
    FMT    = self . Translations    [ "UI::StartLoading"                     ]
    MSG    = FMT . format           ( self . windowTitle ( )                 )
    self   . ShowStatus             ( MSG                                    )
    self   . OnBusy  . emit         (                                        )
    self   . setBustle              (                                        )
    ##########################################################################
    self   . ObtainsInformation     ( DB                                     )
    LISTs  = self . ObtainParticles ( DB                                     )
    ##########################################################################
    self   . setVacancy             (                                        )
    self   . GoRelax . emit         (                                        )
    self   . ShowStatus             ( ""                                     )
    DB     . Close                  (                                        )
    ##########################################################################
    if                              ( len ( LISTs ) <= 0                   ) :
      self . emitNamesShow . emit   (                                        )
      return
    ##########################################################################
    self   . emitAllNames  . emit   ( LISTs                                  )
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
  def ObtainsInformation ( self , DB                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    PTSTAB = self . Tables          [ "Particles"                            ]
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    return f"select `uuid` from {PTSTAB} order by `id` {ORDER} ;"
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 7                              )
    self . setColumnWidth ( 0 , 80                                           )
    ##########################################################################
    return
  ############################################################################
  def UpdateColumnValue       ( self , item , uuid , column , name         ) :
    ##########################################################################
    ITEM   = ""
    ##########################################################################
    if                        ( column == 1                                ) :
      ITEM = "name"
    elif                      ( column == 6                                ) :
      ITEM = "comment"
    ##########################################################################
    if                        ( len ( ITEM ) <= 0                          ) :
      self . Notify           ( 2                                            )
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    PTSTAB = self . Tables    [ "Particles"                                  ]
    ##########################################################################
    DB     . LockWrites       ( [ PTSTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {PTSTAB}
               set `{ITEM}` = %s
               where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . QueryValues      ( QQ , ( name , )                              )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item                                 ,
                                        0                                    ,
                                        "Particles"                          ,
                                        "NamesEditing"                       )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard ( False                                         )
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
    if                             ( at >= 9001 ) and ( at <= 9007 )         :
      ########################################################################
      col  = at - 9000
      ########################################################################
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      return True
    ##########################################################################
    return False
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
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager               ( self                                )
    ##########################################################################
    self   . AppendRefreshAction       ( mm , 1001                           )
    self   . AppendRenameAction        ( mm , 1101                           )
    self   . TryAppendEditNamesAction  ( atItem , mm , 1601                  )
    ##########################################################################
    if                                 ( self . IsOkay ( atItem )          ) :
      ########################################################################
      msg  = self . getMenuItem        ( "CopyParticleUuid"                  )
      mm   . addAction                 ( 1201 , msg                          )
      ########################################################################
      msg  = self . getMenuItem        ( "Description"                       )
      mm   . addAction                 ( 1202 , msg                          )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . ColumnsMenu               ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
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
    OKAY   = self . RunColumnsMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1101                        ) :
      ########################################################################
      self . RenameItem                (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1201                        ) :
      ########################################################################
      uuid = atItem . data             ( 0 , Qt . UserRole                   )
      uuid = int                       ( uuid                                )
      qApp . clipboard ( ). setText    ( f"{uuid}"                           )
      self . Notify                    ( 5                                   )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1202                        ) :
      ########################################################################
      uuid = atItem . data             ( 0 , Qt . UserRole                   )
      uuid = int                       ( uuid                                )
      head = atItem . text             ( 0                                   )
      nx   = ""
      ########################################################################
      if                               ( "Notes" in self . Tables          ) :
        nx = self . Tables             [ "Notes"                             ]
      ########################################################################
      self . OpenLogHistory . emit     ( head                                ,
                                         str ( uuid )                        ,
                                         "Description"                       ,
                                         nx                                  ,
                                         ""                                  )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    return True
##############################################################################
