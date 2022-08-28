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
  addText        = pyqtSignal       ( str                                    )
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
    self . dockingPlace       = Qt . LeftDockWidgetArea
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
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
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
    self . LinkVoice         ( self . CommandParser                          )
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
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . LinkVoice         ( None                                          )
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def singleClicked ( self , item , column                                 ) :
    ##########################################################################
    self . Notify   ( 0                                                      )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked ( self , item , column                                 ) :
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
    IT   . setText               ( 1 ,                 str ( SERIAL )        )
    IT   . setTextAlignment      ( 1 , Qt.AlignRight                         )
    IT   . setData               ( 1 , Qt . UserRole , str ( SERIAL )        )
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
    self   . Notify             ( 5                                          )
    ##########################################################################
    TRX    = self . Translations
    msg    = TRX                [ "UI::Ready"                                ]
    self   . TtsTalk            ( msg , self . getLocality ( )               )
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
  def loading                       ( self                                 ) :
    ##########################################################################
    TRX     = self . Translations
    ##########################################################################
    msg     = TRX                   [ "UI::Loading"                          ]
    self    . TtsTalk               ( msg , self . getLocality ( )           )
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    self    . Notify                ( 3                                      )
    self    . OnBusy  . emit        (                                        )
    self    . setBustle             (                                        )
    ##########################################################################
    FMT     = self . Translations   [ "UI::StartLoading"                     ]
    MSG     = FMT . format          ( self . windowTitle ( )                 )
    self    . ShowStatus            ( MSG                                    )
    ##########################################################################
    self    . ObtainsInformation    ( DB                                     )
    RECORDs = self . ObtainsHistory ( DB                                     )
    ##########################################################################
    self    . setVacancy            (                                        )
    self    . GoRelax . emit        (                                        )
    self    . ShowStatus            ( ""                                     )
    DB      . Close                 (                                        )
    ##########################################################################
    if                              ( len ( RECORDs ) <= 0                 ) :
      return
    ##########################################################################
    self    . emitAllHistory . emit ( RECORDs                                )
    ##########################################################################
    return
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    for i in range            ( 2 , 8                                      ) :
      self . setColumnWidth   ( i , 60                                       )
    ##########################################################################
    self   . setColumnWidth   ( 8 , 120                                      )
    self   . setColumnWidth   ( 9 ,   3                                      )
    ##########################################################################
    TRX    = self . Translations
    self   . setCentralLabels ( TRX [ "TBL" ] [ "History" ] [ "Labels" ]     )
    ##########################################################################
    self   . setPrepared      ( True                                         )
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
  def Menu                              ( self , pos                       ) :
    ##########################################################################
    if                                  ( not self . isPrepared ( )        ) :
      return False
    ##########################################################################
    doMenu = self . isFunction          ( self . HavingMenu                  )
    if                                  ( not doMenu                       ) :
      return False
    ##########################################################################
    self   . Notify                     ( 0                                  )
    items , atItem , uuid = self . GetMenuDetails ( 1                        )
    mm     = MenuManager                ( self                               )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu     ( mm                                 )
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    ##########################################################################
    if                                  ( self . NotOkay ( atItem )        ) :
      ########################################################################
      MSG  = self . getMenuItem         ( "Betting"                          )
      mm   . addAction                  ( 1002 , MSG                         )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    mm     = self . SortingMenu         ( mm                                 )
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    mm     . setFont                    ( self    . menuFont ( )             )
    aa     = mm . exec_                 ( QCursor . pos      ( )             )
    at     = mm . at                    ( aa                                 )
    ##########################################################################
    if                                  ( self . RunAmountIndexMenu (    ) ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( self . RunSortingMenu ( at     ) ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( self . RunDocking ( mm , aa    ) ) :
      return True
    ##########################################################################
    if                                  ( at == 1001                       ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 1002                       ) :
      ########################################################################
      serial = atItem . text            ( 1                                  )
      self   . emitTblSerial . emit     ( serial                             )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
