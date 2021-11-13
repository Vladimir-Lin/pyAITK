# -*- coding: utf-8 -*-
##############################################################################
## tblPredictListings
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
from   AITK  . Documents  . JSON      import Load        as LoadJson
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
class tblPredictListings            ( TreeDock                             ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitAllHistory = pyqtSignal       ( list                                   )
  addText        = pyqtSignal       ( str                                    )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            (        parent        , plan            )
    ##########################################################################
    self . ConfPath           = ""
    self . Serial             = ""
    self . Prediction         = ""
    self . Bettings           = [                                            ]
    self . tblSettings        = {                                            }
    self . tblParameters      = {                                            }
    self . tblAppears         = {                                            }
    ##########################################################################
    self . dockingOrientation = Qt . Horizontal
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount           ( 9                                      )
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
    return QSize                   ( 560 , 800                               )
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "SelectAll"  , self . PickAll           )
    self . LinkAction              ( "SelectNone" , self . PickNone          )
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
  def PrepareItem                ( self , Id , RECORD , Checked            ) :
    ##########################################################################
    if                           ( Checked                                 ) :
      PICK  = Qt . Checked
    else                                                                     :
      PICK  = Qt . Unchecked
    ##########################################################################
    N1      = RECORD             [  0                                        ]
    N2      = RECORD             [  1                                        ]
    N3      = RECORD             [  2                                        ]
    N4      = RECORD             [  3                                        ]
    N5      = RECORD             [  4                                        ]
    N6      = RECORD             [  5                                        ]
    ##########################################################################
    IT   = QTreeWidgetItem       (                                           )
    IT   . setCheckState         ( 0 , PICK                                  )
    IT   . setText               ( 1 , str ( Id )                            )
    IT   . setTextAlignment      ( 1 , Qt.AlignRight                         )
    IT   . setText               ( 2 , str ( N1 )                            )
    IT   . setTextAlignment      ( 2 , Qt.AlignRight                         )
    IT   . setText               ( 3 , str ( N2 )                            )
    IT   . setTextAlignment      ( 3 , Qt.AlignRight                         )
    IT   . setText               ( 4 , str ( N3 )                            )
    IT   . setTextAlignment      ( 4 , Qt.AlignRight                         )
    IT   . setText               ( 5 , str ( N4 )                            )
    IT   . setTextAlignment      ( 5 , Qt.AlignRight                         )
    IT   . setText               ( 6 , str ( N5 )                            )
    IT   . setTextAlignment      ( 6 , Qt.AlignRight                         )
    IT   . setText               ( 7 , str ( N6 )                            )
    IT   . setTextAlignment      ( 7 , Qt.AlignRight                         )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                     (        list                                )
  def refresh                   ( self , RECORDs                           ) :
    ##########################################################################
    self   . clear              (                                            )
    ##########################################################################
    for i , R in enumerate      ( RECORDs                                  ) :
      ########################################################################
      IT   = self . PrepareItem ( i + 1 , R , True                           )
      self . addTopLevelItem    ( IT                                         )
    ##########################################################################
    self . Bettings = RECORDs
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    TBLTAB  = self . Tables           [ "Main"                               ]
    ##########################################################################
    QQ      = f"""select `serial` from {TBLTAB}
                  order by `id` desc
                  limit 0 , 1 ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self    . Serial     = str        ( RR [ 0 ]                             )
    ##########################################################################
    NOW     = StarDate                (                                      )
    NOW     . Now                     (                                      )
    YY      = NOW . toDateString      ( "Asia/Taipei" , "%Y"                 )
    YY      = int                     ( YY                                   )
    ##########################################################################
    SERIAL  = int                     ( self . Serial                        )
    NO      = int                     ( SERIAL                               )
    YEAR    = int                     ( NO / 1000000                         )
    YAD     = int                     ( YEAR + 1911                          )
    NO      = int                     ( NO % 1000                            )
    ##########################################################################
    if                                ( YAD == YY                          ) :
      NO    = NO + 1
    else                                                                     :
      YEAR  = int                     ( YY - 1911                            )
      NO    = 1
    ##########################################################################
    PREDICT = int                     ( int ( YEAR * 1000000 ) + NO          )
    self    . Prediction = str        ( PREDICT                              )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery        ( self                                       ) :
    ##########################################################################
    TBLTAB  = self . Tables   [ "Bettings"                                   ]
    SERIAL  = self . Prediction
    ##########################################################################
    QQ      = f"""select `n1`,`n2`,`n3`,`n4`,`n5`,`n6` from {TBLTAB}
                  where ( `serial` = '{SERIAL}' )
                  order by `id` asc ;"""
    ##########################################################################
    return " " . join         ( QQ . split ( )                               )
  ############################################################################
  def ObtainsPrediction               ( self , DB                          ) :
    ##########################################################################
    SERIAL  = self . Prediction
    if                                ( len ( SERIAL ) <= 0                ) :
      return                          [                                      ]
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
  def appendText                       ( self , message                    ) :
    ##########################################################################
    self . addText . emit              ( message                             )
    ##########################################################################
    return
  ############################################################################
  def loading                          ( self                              ) :
    ##########################################################################
    CONF    = self . ConfPath
    tblSt   = f"{CONF}/tbl.json"
    tblPa   = f"{CONF}/tbl-parameters.json"
    tblAp   = f"{CONF}/tblAppears.json"
    ##########################################################################
    self . tblSettings   = LoadJson    ( tblSt                               )
    self . tblParameters = LoadJson    ( tblPa                               )
    self . tblAppears    = LoadJson    ( tblAp                               )
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    if                                 ( DB == None                        ) :
      return
    ##########################################################################
    self    . ObtainsInformation       ( DB                                  )
    RECORDs = self . ObtainsPrediction ( DB                                  )
    ##########################################################################
    DB      . Close                    (                                     )
    ##########################################################################
    if                                 ( len ( RECORDs ) <= 0              ) :
      return
    ##########################################################################
    self    . emitAllHistory . emit    ( RECORDs                             )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
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
    IDPMSG = self . Translations [ "Docking" ] [ "None"                      ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock"                      ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"                       ]
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
  def Prepare                 ( self                                       ) :
    ##########################################################################
    self   . setColumnWidth   ( 0 ,  3                                       )
    self   . setColumnWidth   ( 8 ,  3                                       )
    for i in range            ( 1 ,  8                                     ) :
      self . setColumnWidth   ( i , 60                                       )
    ##########################################################################
    TRX  = self . Translations
    self . setCentralLabels   ( TRX [ "TBL" ] [ "Predictions" ] [ "Labels" ] )
    ##########################################################################
    self . setPrepared        ( True                                         )
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
  def PredictBettings            ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def UpdateBettings             ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PickAll                    ( self                                    ) :
    ##########################################################################
    for i in range               ( 0 , self . topLevelItemCount ( )        ) :
      IT  = self . topLevelItem  ( i                                         )
      IT  . setCheckState        ( 0 , Qt . Checked                          )
    ##########################################################################
    return
  ############################################################################
  def PickNone                     ( self                                  ) :
    ##########################################################################
    for i in range               ( 0 , self . topLevelItemCount ( )        ) :
      IT  = self . topLevelItem  ( i                                         )
      IT  . setCheckState        ( 0 , Qt . Unchecked                        )
    ##########################################################################
    return
  ############################################################################
  def PredictionMenu               ( self , mm                             ) :
    ##########################################################################
    TRX    = self  . Translations
    LOM    = mm    . addMenu       ( "預測參數" )
    ##########################################################################
    hid    =                       ( self . SortOrder == "asc"               )
    msg    = TRX                   [ "UI::SortAsc"                           ]
    mm     . addActionFromMenu     ( LOM , 20000001 , msg , True , hid       )
    ##########################################################################
    hid    =                       ( self . SortOrder == "desc"              )
    msg    = TRX                   [ "UI::SortDesc"                          ]
    mm     . addActionFromMenu     ( LOM , 20000002 , msg , True , hid       )
    ##########################################################################
    return mm
  ############################################################################
  def RunPredictionMenu            ( self , atId                           ) :
    ##########################################################################
    ##########################################################################
    return   False
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items  = self . selectedItems   (                                        )
    atItem = self . currentItem     (                                        )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    SERL   = LineEdit               ( None , self . PlanFunc                 )
    SERL   . setText                ( self . Prediction                      )
    mm     . addWidget              ( 9999991 , SERL                         )
    ##########################################################################
    mm     . addSeparator           (                                        )
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     . addAction              ( 1002 , "預測投注" )
    mm     . addAction              ( 1003 , "更新投注" )
    mm     . addAction              ( 1004 , "全部選取" )
    mm     . addAction              ( 1005 , "全部不選" )
    ##########################################################################
    mm     = self . PredictionMenu  ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . font ( )                     )
    aa     = mm . exec_             ( QCursor . pos  ( )                     )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    RR     = SERL . text            (                                        )
    if                              ( RR != self . Prediction              ) :
      ########################################################################
      self . Prediction = RR
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunPredictionMenu ( at      ) ) :
      return True
    ##########################################################################
    if                              ( self . RunDocking        ( mm , aa ) ) :
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
      self . PredictBettings        (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1003                           ) :
      ########################################################################
      self . UpdateBettings         (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1004                           ) :
      ########################################################################
      self . PickAll                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1005                           ) :
      ########################################################################
      self . PickNone               (                                        )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
