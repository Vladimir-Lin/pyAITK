# -*- coding: utf-8 -*-
##############################################################################
## tblRecordListings
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
##############################################################################
class tblRecordListings             ( TreeDock                             ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitAllHistory = pyqtSignal       ( list                                   )
  emitTblSerial  = pyqtSignal       ( str                                    )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            (        parent        , plan            )
    ##########################################################################
    self . Total     = 0
    self . StartId   = 0
    self . Amount    = 28
    self . SortOrder = "desc"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount           ( 10                                     )
    self . setRootIsDecorated       ( False                                  )
    self . setAlternatingRowColors  ( True                                   )
    ##########################################################################
    self . MountClicked             ( 1                                      )
    self . MountClicked             ( 2                                      )
    ##########################################################################
    self . assignSelectionMode      ( "ContiguousSelection"                  )
    ##########################################################################
    self . emitAllHistory . connect ( self . refresh                         )
    ##########################################################################
    self . setFunction              ( self . FunctionDocking , True          )
    self . setFunction              ( self . HavingMenu      , True          )
    ##########################################################################
    self . setDragEnabled           ( False                                  )
    self . setAcceptDrops           ( False                                  )
    self . setDragDropMode          ( QAbstractItemView . NoDragDrop         )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 800 , 640                               )
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    ##########################################################################
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                     ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    self . Notify             ( 0                                            )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                ( self , RECORD                           ) :
    ##########################################################################
    SERIAL  = RECORD             [  0                                        ]
    YEAR    = RECORD             [  1                                        ]
    MONTH   = RECORD             [  2                                        ]
    DAY     = RECORD             [  3                                        ]
    N1      = RECORD             [  4                                        ]
    N2      = RECORD             [  5                                        ]
    N3      = RECORD             [  6                                        ]
    N4      = RECORD             [  7                                        ]
    N5      = RECORD             [  8                                        ]
    N6      = RECORD             [  9                                        ]
    SPECIAL = RECORD             [ 10                                        ]
    ##########################################################################
    MM      = str                ( MONTH                                     )
    DD      = str                ( DAY                                       )
    if                           ( len ( MM ) == 1                         ) :
      MM    = f"0{MM}"
    if                           ( len ( DD ) == 1                         ) :
      DD    = f"0{DD}"
    ##########################################################################
    DATE    = f"{YEAR}/{MM}/{DD}"
    ##########################################################################
    IT   = QTreeWidgetItem       (                                           )
    IT   . setText               ( 0 , DATE                                  )
    IT   . setText               ( 1 , str ( SERIAL  )                       )
    IT   . setTextAlignment      ( 1 , Qt.AlignRight                         )
    IT   . setText               ( 2 , str ( N1      )                       )
    IT   . setTextAlignment      ( 2 , Qt.AlignRight                         )
    IT   . setText               ( 3 , str ( N2      )                       )
    IT   . setTextAlignment      ( 3 , Qt.AlignRight                         )
    IT   . setText               ( 4 , str ( N3      )                       )
    IT   . setTextAlignment      ( 4 , Qt.AlignRight                         )
    IT   . setText               ( 5 , str ( N4      )                       )
    IT   . setTextAlignment      ( 5 , Qt.AlignRight                         )
    IT   . setText               ( 6 , str ( N5      )                       )
    IT   . setTextAlignment      ( 6 , Qt.AlignRight                         )
    IT   . setText               ( 7 , str ( N6      )                       )
    IT   . setTextAlignment      ( 7 , Qt.AlignRight                         )
    IT   . setText               ( 8 , str ( SPECIAL )                       )
    IT   . setTextAlignment      ( 8 , Qt.AlignRight                         )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                     (        list                                )
  def refresh                   ( self , RECORDs                           ) :
    ##########################################################################
    self   . clear              (                                            )
    ##########################################################################
    for R in RECORDs                                                         :
      ########################################################################
      IT   = self . PrepareItem ( R                                          )
      self . addTopLevelItem    ( IT                                         )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    TBLTAB  = self . Tables           [ "Main"                               ]
    ##########################################################################
    QQ      = f"select count(*) from {TBLTAB} ;"
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self    . Total = RR              [ 0                                    ]
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery        ( self                                       ) :
    ##########################################################################
    TBLTAB  = self . Tables   [ "Main"                                       ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"""select `serial`,
                         `year`,`month`,`day`,
                         `n1`,`n2`,`n3`,`n4`,`n5`,`n6`,`special`
                  from {TBLTAB}
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join         ( QQ . split ( )                               )
  ############################################################################
  def ObtainsHistory                  ( self , DB                          ) :
    ##########################################################################
    QQ      = self . ObtainUuidsQuery (                                      )
    DB      . Query                   ( QQ                                   )
    RECORDs = DB . FetchAll           (                                      )
    ##########################################################################
    if ( RECORDs in [ False , None ] ) or ( len ( RECORDs ) <= 0 )           :
      return                          [                                      ]
    ##########################################################################
    return RECORDs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    RECORDs = self . ObtainsHistory   ( DB                                   )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( RECORDs ) <= 0               ) :
      return
    ##########################################################################
    self    . emitAllHistory . emit   ( RECORDs                              )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
  ############################################################################
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None" ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock" ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"  ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def Prepare                     ( self                                   ) :
    ##########################################################################
    for i in range                ( 2 , 8                                  ) :
      self . setColumnWidth       ( i , 60                                   )
    ##########################################################################
    self   . setColumnWidth       ( 8 , 120                                  )
    self   . setColumnWidth       ( 9 ,   3                                  )
    ##########################################################################
    TRX    = self . Translations
    self   . setCentralLabels     ( TRX [ "TBL" ] [ "History" ] [ "Labels" ] )
    ##########################################################################
    self   . setPrepared          ( True                                     )
    ##########################################################################
    return
  ############################################################################
  def PageHome                     ( self                                  ) :
    ##########################################################################
    self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageEnd                      ( self                                  ) :
    ##########################################################################
    self . StartId    = self . Total - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageUp                       ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageDown                     ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId + self . Amount
    if                             ( self . StartId > self . Total         ) :
      self . StartId  = self . Total
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard             ( self                                   ) :
    ##########################################################################
    IT   = self . currentItem     (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    items  = self . selectedItems   (                                        )
    atItem = self . currentItem     (                                        )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    mm     . addAction              ( 1001 ,  TRX [ "UI::Refresh"          ] )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      MSG  = self . getMenuItem     ( "Betting"                              )
      mm   . addAction              ( 1002 , MSG                             )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    mm     = self . SortingMenu     ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . font ( )                     )
    aa     = mm . exec_             ( QCursor . pos  ( )                     )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunAmountIndexMenu (        ) ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu ( at         ) ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunDocking     ( mm , aa    ) ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1002                           ) :
      ########################################################################
      serial = atItem . text        ( 1                                      )
      self   . emitTblSerial . emit ( serial                                 )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
