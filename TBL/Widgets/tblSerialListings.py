# -*- coding: utf-8 -*-
##############################################################################
## tblSerialListings
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
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QColor
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
class tblSerialListings             ( TreeDock                             ) :
  ############################################################################
  HavingMenu     = 1371434312
  ############################################################################
  emitBettings   = pyqtSignal       ( list                                   )
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
    self . Serial    = ""
    self . Six       =              [                                        ]
    self . Special   =              [                                        ]
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount           ( 11                                     )
    self . setRootIsDecorated       ( False                                  )
    self . setAlternatingRowColors  ( True                                   )
    ##########################################################################
    self . MountClicked             ( 1                                      )
    self . MountClicked             ( 2                                      )
    ##########################################################################
    self . assignSelectionMode      ( "ContiguousSelection"                  )
    ##########################################################################
    self . emitBettings . connect   ( self . refresh                         )
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
    return self . SizeSuggestion ( QSize ( 880 , 640 )                       )
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
  def MatchBall                    ( self , item , column , ball           ) :
    ##########################################################################
    if                             ( ball in self . Special                ) :
      C     = QColor               (   0 ,   0 , 255                         )
      item  . setForeground        ( column , QBrush ( C )                   )
    ##########################################################################
    if                             ( ball in self . Six                    ) :
      C     = QColor               ( 255 ,   0 ,   0                         )
      item  . setForeground        ( column , QBrush ( C )                   )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                  ( self , Id , BETTING                   ) :
    ##########################################################################
    POSITION = BETTING             [ 0                                       ]
    N1       = BETTING             [ 1                                       ]
    N2       = BETTING             [ 2                                       ]
    N3       = BETTING             [ 3                                       ]
    N4       = BETTING             [ 4                                       ]
    N5       = BETTING             [ 5                                       ]
    N6       = BETTING             [ 6                                       ]
    TWD      = BETTING             [ 7                                       ]
    RESULTS  = BETTING             [ 8                                       ]
    EARNINGS = BETTING             [ 9                                       ]
    ##########################################################################
    POSITION = int                 ( POSITION                                )
    RESULTS  = str                 ( RESULTS                                 )
    REWARDS  = self . Translations [ "TBL" ] [ "Rewards" ] [ RESULTS         ]
    ##########################################################################
    IT       = QTreeWidgetItem     (                                         )
    IT       . setText             ( 0 , str ( Id       )                    )
    IT       . setTextAlignment    ( 0 , Qt.AlignRight                       )
    IT       . setData             ( 0 , Qt . UserRole , POSITION            )
    IT       . setText             ( 1 , str ( N1       )                    )
    IT       . setTextAlignment    ( 1 , Qt.AlignRight                       )
    self     . MatchBall           ( IT , 1 , int ( N1 )                     )
    IT       . setText             ( 2 , str ( N2       )                    )
    IT       . setTextAlignment    ( 2 , Qt.AlignRight                       )
    self     . MatchBall           ( IT , 2 , int ( N2 )                     )
    IT       . setText             ( 3 , str ( N3       )                    )
    IT       . setTextAlignment    ( 3 , Qt.AlignRight                       )
    self     . MatchBall           ( IT , 3 , int ( N3 )                     )
    IT       . setText             ( 4 , str ( N4       )                    )
    IT       . setTextAlignment    ( 4 , Qt.AlignRight                       )
    self     . MatchBall           ( IT , 4 , int ( N4 )                     )
    IT       . setText             ( 5 , str ( N5       )                    )
    IT       . setTextAlignment    ( 5 , Qt.AlignRight                       )
    self     . MatchBall           ( IT , 5 , int ( N5 )                     )
    IT       . setText             ( 6 , str ( N6       )                    )
    IT       . setTextAlignment    ( 6 , Qt.AlignRight                       )
    self     . MatchBall           ( IT , 6 , int ( N6 )                     )
    IT       . setText             ( 7 , str ( TWD      )                    )
    IT       . setTextAlignment    ( 7 , Qt.AlignRight                       )
    IT       . setText             ( 8 , str ( REWARDS  )                    )
    IT       . setTextAlignment    ( 8 , Qt.AlignRight                       )
    IT       . setText             ( 9 , str ( EARNINGS )                    )
    IT       . setTextAlignment    ( 9 , Qt.AlignRight                       )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                     (        list                                )
  def refresh                   ( self , BETTINGs                          ) :
    ##########################################################################
    self   . clear              (                                            )
    ##########################################################################
    for i , B in enumerate      ( BETTINGs                                 ) :
      ########################################################################
      IT   = self . PrepareItem ( i + 1 , B                                  )
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
  def ObtainUuidsQuery        ( self                                       ) :
    ##########################################################################
    TBLTAB  = self . Tables   [ "Bettings"                                   ]
    SERIAL  = self . Serial
    ##########################################################################
    QQ      = f"""select `id`,
                         `n1`,`n2`,`n3`,`n4`,`n5`,`n6`,
                         `twd`,`results`,`earnings`
                  from {TBLTAB}
                  where ( `serial` = '{SERIAL}' )
                  order by `id` asc ;"""
    ##########################################################################
    return " " . join         ( QQ . split ( )                               )
  ############################################################################
  def ObtainsBettings                  ( self , DB                         ) :
    ##########################################################################
    QQ       = self . ObtainUuidsQuery (                                     )
    DB       . Query                   ( QQ                                  )
    BETTINGs = DB . FetchAll           (                                     )
    ##########################################################################
    if ( BETTINGs in [ False , None ] ) or ( len ( BETTINGs ) <= 0 )         :
      return                           [                                     ]
    ##########################################################################
    TBLTAB   = self . Tables           [ "Main"                              ]
    SERIAL   = self . Serial
    ##########################################################################
    QQ       = f"""select `n1`,`n2`,`n3`,`n4`,`n5`,`n6`,`special`
                   from {TBLTAB}
                   where ( `serial` = '{SERIAL}' ) ;"""
    ##########################################################################
    DB       . Query                   ( QQ                                  )
    RESULTS  = DB . FetchOne           (                                     )
    ##########################################################################
    if ( RESULTS in [ False , None ] ) or ( len ( RESULTS ) <= 0 )           :
      return                           [                                     ]
    ##########################################################################
    for i in range                     ( 0 , 6                             ) :
      self   . Six . append            ( int ( RESULTS [ i ] )               )
    ##########################################################################
    self     . Special . append        ( int ( RESULTS [ 6 ] )               )
    ##########################################################################
    return BETTINGs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    TRX      = self . Translations
    ##########################################################################
    msg      = TRX                    [ "UI::Loading"                        ]
    self     . TtsTalk                ( msg , self . getLocality ( )         )
    ##########################################################################
    DB       = self . ConnectDB       (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self     . Notify                 ( 3                                    )
    self     . OnBusy  . emit         (                                      )
    self     . setBustle              (                                      )
    ##########################################################################
    FMT      = self . Translations    [ "UI::StartLoading"                   ]
    MSG      = FMT . format           ( self . windowTitle ( )               )
    self     . ShowStatus             ( MSG                                  )
    ##########################################################################
    BETTINGs = self . ObtainsBettings ( DB                                   )
    ##########################################################################
    self     . setVacancy             (                                      )
    self     . GoRelax . emit         (                                      )
    self     . ShowStatus             ( ""                                   )
    DB       . Close                  (                                      )
    ##########################################################################
    if                                ( len ( BETTINGs ) <= 0              ) :
      return
    ##########################################################################
    self     . emitBettings . emit    ( BETTINGs                             )
    ##########################################################################
    return
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    for i in range            (  0 ,   7                                   ) :
      self . setColumnWidth   (  i ,  60                                     )
    ##########################################################################
    self   . setColumnWidth   (  7 , 180                                     )
    self   . setColumnWidth   (  8 , 100                                     )
    self   . setColumnWidth   (  9 , 120                                     )
    self   . setColumnWidth   ( 10 ,   3                                     )
    ##########################################################################
    TRX    = self . Translations
    self   . setCentralLabels ( TRX [ "TBL" ] [ "Serial" ] [ "Labels" ]      )
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
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager                ( self                               )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    mm     . setFont                    ( self    . menuFont ( )             )
    aa     = mm . exec_                 ( QCursor . pos      ( )             )
    at     = mm . at                    ( aa                                 )
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
    return True
##############################################################################
