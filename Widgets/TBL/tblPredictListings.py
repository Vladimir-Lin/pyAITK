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
import random
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
from   AITK  . TBL . TblMaps          import tblStatisticsAC6        as tblStatisticsAC6
from   AITK  . TBL . TblMaps          import tblStatisticsAC7        as tblStatisticsAC7
from   AITK  . TBL . TblMaps          import tblStatisticsOdds6      as tblStatisticsOdds6
from   AITK  . TBL . TblMaps          import tblStatisticsOdds7      as tblStatisticsOdds7
from   AITK  . TBL . TblMaps          import tblStatisticsEvens6     as tblStatisticsEvens6
from   AITK  . TBL . TblMaps          import tblStatisticsEvens7     as tblStatisticsEvens7
from   AITK  . TBL . TblMaps          import tblStatisticsHead6      as tblStatisticsHead6
from   AITK  . TBL . TblMaps          import tblStatisticsHead7      as tblStatisticsHead7
from   AITK  . TBL . TblMaps          import tblStatisticsTail6      as tblStatisticsTail6
from   AITK  . TBL . TblMaps          import tblStatisticsTail7      as tblStatisticsTail7
from   AITK  . TBL . TblMaps          import tblStatisticsFirst6     as tblStatisticsFirst6
from   AITK  . TBL . TblMaps          import tblStatisticsFirst7     as tblStatisticsFirst7
from   AITK  . TBL . TblMaps          import tblStatisticsEnding6    as tblStatisticsEnding6
from   AITK  . TBL . TblMaps          import tblStatisticsEnding7    as tblStatisticsEnding7
from   AITK  . TBL . TblMaps          import tblStatisticsGaps6      as tblStatisticsGaps6
from   AITK  . TBL . TblMaps          import tblStatisticsGaps7      as tblStatisticsGaps7
from   AITK  . TBL . TblMaps          import tblStatisticsTotalSums6 as tblStatisticsTotalSums6
from   AITK  . TBL . TblMaps          import tblStatisticsTotalSums7 as tblStatisticsTotalSums7
from   AITK  . TBL . TblMaps          import tblStatisticsHeadSums6  as tblStatisticsHeadSums6
from   AITK  . TBL . TblMaps          import tblStatisticsHeadSums7  as tblStatisticsHeadSums7
from   AITK  . TBL . TblMaps          import tblStatisticsTailSums6  as tblStatisticsTailSums6
from   AITK  . TBL . TblMaps          import tblStatisticsTailSums7  as tblStatisticsTailSums7
from   AITK  . TBL . TblSquare        import tblStatisticsSquare6    as tblStatisticsSquare6
##############################################################################
from   AITK  . TBL . TblDistribution  import TblDistribution         as TblDistribution
from   AITK  . TBL . TaiwanBL         import TaiwanBL                as TaiwanBL
from   AITK  . TBL . TaiwanBLs        import TaiwanBLs               as TaiwanBLs
##############################################################################
Rotate10x6x5 = [ [ 0 , 1 , 2 , 3 , 4 , 5 ]                                 , \
                 [ 0 , 1 , 2 , 3 , 6 , 7 ]                                 , \
                 [ 0 , 1 , 2 , 3 , 8 , 9 ]                                 , \
                 [ 0 , 1 , 2 , 4 , 6 , 8 ]                                 , \
                 [ 0 , 1 , 2 , 4 , 7 , 9 ]                                 , \
                 [ 0 , 1 , 2 , 5 , 6 , 9 ]                                 , \
                 [ 0 , 1 , 2 , 5 , 7 , 8 ]                                 , \
                 [ 0 , 1 , 3 , 4 , 6 , 9 ]                                 , \
                 [ 0 , 1 , 3 , 4 , 7 , 8 ]                                 , \
                 [ 0 , 1 , 3 , 5 , 6 , 8 ]                                 , \
                 [ 0 , 1 , 3 , 5 , 7 , 9 ]                                 , \
                 [ 0 , 1 , 4 , 5 , 6 , 7 ]                                 , \
                 [ 0 , 1 , 4 , 5 , 8 , 9 ]                                 , \
                 [ 0 , 1 , 6 , 7 , 8 , 9 ]                                 , \
                 [ 2 , 3 , 4 , 5 , 6 , 7 ]                                 , \
                 [ 2 , 3 , 4 , 5 , 8 , 9 ]                                 , \
                 [ 2 , 3 , 6 , 7 , 8 , 9 ]                                 , \
                 [ 4 , 5 , 6 , 7 , 8 , 9 ]                                 ] ;
##############################################################################
Position12x6x5 = [ [  0 ,  2 ,  4 ,  6 ,  8 , 10 ]                         , \
                   [  0 ,  2 ,  4 ,  6 ,  9 , 11 ]                         , \
                   [  0 ,  2 ,  5 ,  7 ,  8 , 11 ]                         , \
                   [  0 ,  2 ,  5 ,  7 ,  9 , 10 ]                         , \
                   [  0 ,  3 ,  4 ,  7 ,  8 , 10 ]                         , \
                   [  0 ,  3 ,  4 ,  7 ,  9 , 11 ]                         , \
                   [  0 ,  3 ,  5 ,  6 ,  8 , 11 ]                         , \
                   [  0 ,  3 ,  5 ,  6 ,  9 , 10 ]                         , \
                   [  1 ,  2 ,  4 ,  7 ,  8 , 11 ]                         , \
                   [  1 ,  2 ,  4 ,  7 ,  9 , 10 ]                         , \
                   [  1 ,  2 ,  5 ,  6 ,  8 , 10 ]                         , \
                   [  1 ,  2 ,  5 ,  6 ,  9 , 11 ]                         , \
                   [  1 ,  3 ,  4 ,  6 ,  8 , 11 ]                         , \
                   [  1 ,  3 ,  4 ,  6 ,  9 , 10 ]                         , \
                   [  1 ,  3 ,  5 ,  7 ,  8 , 10 ]                         , \
                   [  1 ,  3 ,  5 ,  7 ,  9 , 11 ]                         ] ;
##############################################################################
class tblPredictListings            ( TreeDock                             ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitAllHistory = pyqtSignal       ( list                                   )
  emitBettings   = pyqtSignal       ( list                                   )
  addText        = pyqtSignal       ( str                                    )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            (        parent        , plan            )
    ##########################################################################
    random . seed                   ( time . time ( )                        )
    ##########################################################################
    self . ConfPath           = ""
    self . Serial             = ""
    self . Prediction         = ""
    self . ShowMessage        = False
    self . Optimizing         = False
    self . MinBalls           = -1
    self . MaxBalls           = -1
    self . Periods            = 100
    self . Bettings           = [                                            ]
    self . tblSettings        = {                                            }
    self . tblParameters      = {                                            }
    self . tblAppears         = {                                            }
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
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
    self . emitBettings   . connect ( self . AppendBettings                  )
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
    self . LinkAction              ( "Insert"     , self . InsertItem        )
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
  def doubleClicked        ( self , item , column                          ) :
    ##########################################################################
    if                     ( column not in range ( 2 , 8 )                 ) :
      return
    ##########################################################################
    sb = self . setSpinBox ( item                                            ,
                             column                                          ,
                             1                                               ,
                             49                                              ,
                             "editingFinished"                               ,
                             self . spinChanged                              )
    sb . setAlignment      ( Qt . AlignRight                                 )
    sb . setFocus          ( Qt . TabFocusReason                             )
    ##########################################################################
    return
  ############################################################################
  def spinChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    sb     = self . CurrentItem [ "Widget"                                   ]
    v      = self . CurrentItem [ "Value"                                    ]
    v      = int                ( v                                          )
    nv     = sb   . value       (                                            )
    ##########################################################################
    if                          ( v != nv                                  ) :
      ########################################################################
      item . setText            ( column , str ( nv )                        )
    ##########################################################################
    self . removeParked         (                                            )
    ##########################################################################
    return
  ############################################################################
  def PrepareEmptyItem           ( self , Id                               ) :
    ##########################################################################
    IT   = QTreeWidgetItem       (                                           )
    IT   . setCheckState         ( 0 , Qt . Unchecked                        )
    IT   . setText               ( 1 , str ( Id )                            )
    IT   . setTextAlignment      ( 1 , Qt.AlignRight                         )
    IT   . setText               ( 2 , "1"                                   )
    IT   . setTextAlignment      ( 2 , Qt.AlignRight                         )
    IT   . setData               ( 2 , Qt . UserRole , 1                     )
    IT   . setText               ( 3 , "2"                                   )
    IT   . setTextAlignment      ( 3 , Qt.AlignRight                         )
    IT   . setData               ( 3 , Qt . UserRole , 2                     )
    IT   . setText               ( 4 , "3"                                   )
    IT   . setTextAlignment      ( 4 , Qt.AlignRight                         )
    IT   . setData               ( 4 , Qt . UserRole , 3                     )
    IT   . setText               ( 5 , "4"                                   )
    IT   . setTextAlignment      ( 5 , Qt.AlignRight                         )
    IT   . setData               ( 5 , Qt . UserRole , 4                     )
    IT   . setText               ( 6 , "5"                                   )
    IT   . setTextAlignment      ( 6 , Qt.AlignRight                         )
    IT   . setData               ( 6 , Qt . UserRole , 5                     )
    IT   . setText               ( 7 , "6"                                   )
    IT   . setTextAlignment      ( 7 , Qt.AlignRight                         )
    IT   . setData               ( 7 , Qt . UserRole , 6                     )
    ##########################################################################
    return IT
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
    IT   . setData               ( 2 , Qt . UserRole , int ( N1 )            )
    IT   . setText               ( 3 , str ( N2 )                            )
    IT   . setTextAlignment      ( 3 , Qt.AlignRight                         )
    IT   . setData               ( 3 , Qt . UserRole , int ( N2 )            )
    IT   . setText               ( 4 , str ( N3 )                            )
    IT   . setTextAlignment      ( 4 , Qt.AlignRight                         )
    IT   . setData               ( 4 , Qt . UserRole , int ( N3 )            )
    IT   . setText               ( 5 , str ( N4 )                            )
    IT   . setTextAlignment      ( 5 , Qt.AlignRight                         )
    IT   . setData               ( 5 , Qt . UserRole , int ( N4 )            )
    IT   . setText               ( 6 , str ( N5 )                            )
    IT   . setTextAlignment      ( 6 , Qt.AlignRight                         )
    IT   . setData               ( 6 , Qt . UserRole , int ( N5 )            )
    IT   . setText               ( 7 , str ( N6 )                            )
    IT   . setTextAlignment      ( 7 , Qt.AlignRight                         )
    IT   . setData               ( 7 , Qt . UserRole , int ( N6 )            )
    ##########################################################################
    return IT
  ############################################################################
  def GetCurrentBettings          ( self                                   ) :
    ##########################################################################
    RR      =                     [                                          ]
    ##########################################################################
    for i in range                ( 0 , self . topLevelItemCount ( )       ) :
      ########################################################################
      IT    = self . topLevelItem ( i                                        )
      CHK   = IT   . checkState   ( 0                                        )
      FOUND =                     ( CHK == Qt . Checked                      )
      ########################################################################
      if                          ( not FOUND                              ) :
        continue
      ########################################################################
      L     =                     [                                          ]
      for c in range              ( 2 , 8                                  ) :
        V   = IT   . text         ( c                                        )
        V   = int                 ( V                                        )
        L   . append              ( V                                        )
      ########################################################################
      L     . append              ( 0                                        )
      ########################################################################
      T     = TaiwanBL            (                                          )
      T     . assign              ( i , self . Prediction , L                )
      ########################################################################
      if                          ( not T . isValid ( )                    ) :
        continue
      ########################################################################
      RR    . append              ( L                                        )
    ##########################################################################
    return RR
  ############################################################################
  @pyqtSlot                           (        list                          )
  def AppendBettings                  ( self , BETTINGs                    ) :
    ##########################################################################
    BASE   = self . topLevelItemCount (                                      )
    BASE   = BASE + 1
    ##########################################################################
    for i , R in enumerate            ( BETTINGs                           ) :
      ########################################################################
      IT   = self . PrepareItem       ( i + BASE , R , False                 )
      self . addTopLevelItem          ( IT                                   )
    ##########################################################################
    self . Notify                     ( 5                                    )
    ##########################################################################
    return
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
    if                                 ( not self . ShowMessage            ) :
      return
    ##########################################################################
    self . addText . emit              ( message                             )
    ##########################################################################
    return
  ############################################################################
  def LoadSettings                    ( self                               ) :
    ##########################################################################
    CONF   = self . ConfPath
    tblSt  = f"{CONF}/tbl.json"
    tblPa  = f"{CONF}/tbl-parameters.json"
    tblAp  = f"{CONF}/tblAppears.json"
    ##########################################################################
    self   . tblSettings   = LoadJson ( tblSt                                )
    self   . tblParameters = LoadJson ( tblPa                                )
    self   . tblAppears    = LoadJson ( tblAp                                )
    ##########################################################################
    MIN    = self . tblSettings       [ "Bettings" ] [ "Range" ] [ "Min"     ]
    MAX    = self . tblSettings       [ "Bettings" ] [ "Range" ] [ "Max"     ]
    ##########################################################################
    if                                ( self . MinBalls < 0                ) :
      self . MinBalls = MIN
    ##########################################################################
    if                                ( self . MaxBalls < 0                ) :
      self . MaxBalls = MAX
    ##########################################################################
    return
  ############################################################################
  def updating                   ( self , RECORDs                          ) :
    ##########################################################################
    TRX    = self . Translations
    msg    = TRX                 [ "TBL" ] [ "Predictions" ] [ "Updating"    ]
    self   . ShowStatus          ( msg                                       )
    ##########################################################################
    DB     = self . ConnectDB    (                                           )
    if                           ( DB == None                              ) :
      return
    ##########################################################################
    SERIAL = self . Prediction
    BETTAB = self . Tables       [ "Bettings"                                ]
    ##########################################################################
    DB     . LockWrites          ( [ BETTAB ]                                )
    ##########################################################################
    QQ     = f"delete from {BETTAB} where ( `serial` = '{SERIAL}' ) ;"
    QQ     = " " . join          ( QQ . split ( )                            )
    DB     . Query               ( QQ                                        )
    ##########################################################################
    for R in RECORDs                                                         :
      ########################################################################
      N1   = R                   [ 0                                         ]
      N2   = R                   [ 1                                         ]
      N3   = R                   [ 2                                         ]
      N4   = R                   [ 3                                         ]
      N5   = R                   [ 4                                         ]
      N6   = R                   [ 5                                         ]
      ########################################################################
      QQ   = f"""insert into {BETTAB}
                  ( `serial`,`n1`,`n2`,`n3`,`n4`,`n5`,`n6` )
                  values
                  ( '{SERIAL}',{N1},{N2},{N3},{N4},{N5},{N6} ) ;"""
      QQ   = " " . join          ( QQ . split ( )                            )
      DB   . Query               ( QQ                                        )
    ##########################################################################
    DB     . UnlockTables        (                                           )
    DB     . Close               (                                           )
    self   . loading             (                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainAllHistory     ( self , DB                                     ) :
    ##########################################################################
    TBLTAB = self . Tables [ "Main"                                          ]
    QQ     = f"""select `serial`,`n1`,`n2`,`n3`,`n4`,`n5`,`n6`,`special`
                 from {TBLTAB}
                 order by `id` asc ;"""
    QQ     = " " . join    ( QQ . split ( )                                  )
    DB     . Query         ( QQ                                              )
    return DB . FetchAll   (                                                 )
  ############################################################################
  def CombineRotate10x6x5IntoLists ( self , Balls                          ) :
    ##########################################################################
    global Rotate10x6x5
    ##########################################################################
    if                             ( len ( Balls ) != 10                   ) :
      return                       [                                         ]
    ##########################################################################
    LISTS   =                      [                                         ]
    ##########################################################################
    for R in Rotate10x6x5                                                    :
      P1    = R                    [ 0                                       ]
      P2    = R                    [ 1                                       ]
      P3    = R                    [ 2                                       ]
      P4    = R                    [ 3                                       ]
      P5    = R                    [ 4                                       ]
      P6    = R                    [ 5                                       ]
      N1    = Balls                [ P1                                      ]
      N2    = Balls                [ P2                                      ]
      N3    = Balls                [ P3                                      ]
      N4    = Balls                [ P4                                      ]
      N5    = Balls                [ P5                                      ]
      N6    = Balls                [ P6                                      ]
      LISTS . append               ( [ N1 , N2 , N3 , N4 , N5 , N6 ]         )
    ##########################################################################
    return LISTS
  ############################################################################
  def CombinePosition12x6x5IntoLists ( self , Balls                        ) :
    ##########################################################################
    global Position12x6x5
    ##########################################################################
    if                               ( len ( Balls ) != 12                 ) :
      return                         [                                       ]
    ##########################################################################
    LISTS   =                        [                                       ]
    ##########################################################################
    for R in Position12x6x5                                                  :
      P1    = R                      [ 0                                     ]
      P2    = R                      [ 1                                     ]
      P3    = R                      [ 2                                     ]
      P4    = R                      [ 3                                     ]
      P5    = R                      [ 4                                     ]
      P6    = R                      [ 5                                     ]
      N1    = Balls                  [ P1                                    ]
      N2    = Balls                  [ P2                                    ]
      N3    = Balls                  [ P3                                    ]
      N4    = Balls                  [ P4                                    ]
      N5    = Balls                  [ P5                                    ]
      N6    = Balls                  [ P6                                    ]
      LISTS . append                 ( [ N1 , N2 , N3 , N4 , N5 , N6 ]       )
    ##########################################################################
    return LISTS
  ############################################################################
  def GenerateBettings                    ( self , TBLs , BALLS , AP       ) :
    ##########################################################################
    PC            = TBLs . RandomBalls    ( 10 , BALLS , AP , [ ]            )
    random        . shuffle               ( PC                               )
    LZ            = self . CombineRotate10x6x5IntoLists   ( PC               )
    ##########################################################################
    PC            = TBLs . RandomBalls    ( 12 , BALLS , AP , [ ]            )
    random        . shuffle               ( PC                               )
    LL            = self . CombinePosition12x6x5IntoLists ( PC               )
    ##########################################################################
    LW            = LZ
    ##########################################################################
    for L in LL                                                              :
      ########################################################################
      MATCHED     = False
      ########################################################################
      for Z in LZ                                                            :
        RX        = TBLs . CompareTwoSets ( L , Z                            )
        if                                ( RX == 6                        ) :
          MATCHED = True
      ########################################################################
      if                                  ( not MATCHED                    ) :
        LW        . append                ( L                                )
    ##########################################################################
    return LW
  ############################################################################
  def FilterRules                ( self , TBLs , R                         ) :
    ##########################################################################
    JSOZ    = self . tblSettings [ "Bettings"                                ]
    ##########################################################################
    if                           ( R [ 0 ] not in JSOZ [ "First"  ]        ) :
      return False
    ##########################################################################
    if                           ( R [ 5 ] not in JSOZ [ "Ending" ]        ) :
      return False
    ##########################################################################
    X       =                    [                                           ]
    for i in range               ( 0 , 6                                   ) :
      X     . append             ( R [ i ]                                   )
    X       . append             ( 0                                         )
    ##########################################################################
    T       = TaiwanBL           (                                           )
    T       . assign             ( self . Prediction , 1 , X                 )
    ##########################################################################
    SUM     = T . IntValue       ( "Sums::Total"                             )
    if                           ( SUM     not in JSOZ [ "Sums"   ]        ) :
      return False
    ##########################################################################
    AC6     = T . IntValue       ( "AC"                                      )
    if                           ( AC6     not in JSOZ [ "AC"     ]        ) :
      return False
    ##########################################################################
    ODDS    = T . IntValue       ( "Odds"                                    )
    if                           ( ODDS    not in JSOZ [ "Odds"   ]        ) :
      return False
    ##########################################################################
    GAPS    = T . IntValue       ( "Gaps"                                    )
    if                           ( GAPS    not in JSOZ [ "Gaps"   ]        ) :
      return False
    ##########################################################################
    FSUM    = T . IntValue       ( "Sums::Head"                              )
    if                           ( FSUM    not in JSOZ [ "FirstSums" ]     ) :
      return False
    ##########################################################################
    ESUM    = T . IntValue       ( "Sums::Tail"                              )
    if                           ( ESUM    not in JSOZ [ "EndSums"   ]     ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def FilterAllRules                   ( self , TBLs , Bets                ) :
    ##########################################################################
    LX     =                           [                                     ]
    for L in Bets                                                            :
      ########################################################################
      X    = L
      X    . sort                      (                                     )
      ########################################################################
      if                               ( self . FilterRules ( TBLs , X )   ) :
        LX . append                    ( X                                   )
    ##########################################################################
    return LX
  ############################################################################
  def HistoryDuplicate        ( self , TBLs , Bets                         ) :
    ##########################################################################
    LASTEST  = TBLs . Serials (                                              )
    LW       =                [                                              ]
    ##########################################################################
    for B in Bets                                                            :
      ########################################################################
      ## 與歷史紀錄沒有五球或六球相同
      ########################################################################
      if                      ( not TBLs . isHistoryDuplicate ( B )        ) :
        T    = TBLs . at      ( LASTEST                                      )
        AT   = T    . numbers ( 6                                            )
        ######################################################################
        ## 首號不連莊
        ######################################################################
        if                    ( AT [ 0 ] != B [ 0 ]                        ) :
          ####################################################################
          ## 尾號不連莊
          ####################################################################
          if                  ( AT [ 5 ] != B [ 5 ]                        ) :
            LW . append       ( B                                            )
    ##########################################################################
    return LW
  ############################################################################
  ## 移除跟上次開獎三球相同的投注
  ############################################################################
  def TripleDuplicate         ( self , TBLs , Bets                         ) :
    ##########################################################################
    LASTEST  = TBLs . Serials (                                              )
    T        = TBLs . at      ( LASTEST                                      )
    LW       =                [                                              ]
    ##########################################################################
    for B in Bets                                                            :
      ########################################################################
      CNT    = T    . Matches ( 6 , B                                        )
      if                      ( CNT < 3                                    ) :
        LW   . append         ( B                                            )
    ##########################################################################
    return LW
  ############################################################################
  def Predicting                       ( self                              ) :
    ##########################################################################
    TRX     = self . Translations
    msg     = self . getMenuItem       ( "Prediction"                        )
    self    . ShowStatus               ( msg                                 )
    self    . TtsTalk                  ( msg , self . getLocality ( )        )
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    if                                 ( DB == None                        ) :
      return
    ##########################################################################
    HISTORY = self . ObtainAllHistory  ( DB                                  )
    TBLs    = TaiwanBLs                (                                     )
    TBLs    . setAppearanceWeight      ( self . tblAppears                   )
    TBLs    . ImportHistory            ( HISTORY                             )
    LASTEST = TBLs . Serials           (                                     )
    MSG     = TBLs . at ( LASTEST ) . toString (                             )
    NUMS    = TBLs . at ( LASTEST ) . numbers  ( 6                           )
    self    . appendText               ( MSG                                 )
    ##########################################################################
    MIN     = self . tblSettings [ "Bettings" ] [ "Range" ] [ "Min" ]
    MAX     = self . tblSettings [ "Bettings" ] [ "Range" ] [ "Max" ]
    ABALLS  = self . tblSettings [ "Bettings" ] [ "Balls" ]
    WORK    = False
    LX      =                          [                                     ]
    ##########################################################################
    APPEARS = TBLs . CreateAppears     ( 32 , 7                              )
    CDISAPP = TBLs . CountDisappears   ( LASTEST , 6                         )
    DISAPPW = TBLs . ConvertDisappearWeight ( CDISAPP                        )
    WETMT49 = TBLs . MultiplyTwo49     ( APPEARS , DISAPPW                   )
    ##########################################################################
    BALLX   =                          {                                     }
    BALLS   =                          [                                     ]
    BALLX   = TBLs . PickAppears       ( LASTEST                           , \
                                         self . Periods                    , \
                                         1                                 , \
                                         20                                , \
                                         BALLX                               )
    for i in range                     ( 0 , 20                            ) :
      BALLS . append                   ( BALLX [ i ]                         )
    ##########################################################################
    ## MSG     = f"{MIN} , {MAX} : {ABALLS}"
    ## self    . appendText               ( MSG                                 )
    ## self    . appendText               ( json . dumps ( APPEARS )            )
    ## self    . appendText               ( json . dumps ( CDISAPP )            )
    ## self    . appendText               ( json . dumps ( DISAPPW )            )
    ## self    . appendText               ( json . dumps ( WETMT49 )            )
    self    . appendText               ( json . dumps ( BALLS   )            )
    ##########################################################################
    while                              ( not WORK                          ) :
      ########################################################################
      LW    = self . GenerateBettings  ( TBLs , BALLS , WETMT49              )
      LW    = self . FilterAllRules    ( TBLs , LW                           )
      LW    = self . HistoryDuplicate  ( TBLs , LW                           )
      LW    = self . TripleDuplicate   ( TBLs , LW                           )
      self  . appendText               ( json . dumps ( LW )                 )
      ########################################################################
      LZ    = len                      ( LW                                  )
      ########################################################################
      if                               ( LZ < self . MinBalls              ) :
        continue
      ########################################################################
      if                               ( LZ > self . MaxBalls              ) :
        continue
      ########################################################################
      WORK     = True
    ##########################################################################
    DB      . Close                    (                                     )
    ##########################################################################
    if                                 ( len ( LW ) <= 0                   ) :
      self  . Notify                   ( 1                                   )
      return
    ##########################################################################
    self . emitBettings . emit         ( LW                                  )
    ##########################################################################
    return
  ############################################################################
  def loading                          ( self                              ) :
    ##########################################################################
    TRX     = self . Translations
    ##########################################################################
    msg     = TRX                      [ "UI::Loading"                       ]
    self    . TtsTalk                  ( msg , self . getLocality ( )        )
    ##########################################################################
    msg     = TRX [ "TBL" ] [ "Predictions" ] [ "Loading"                    ]
    self    . ShowStatus               ( msg                                 )
    ##########################################################################
    self    . LoadSettings             (                                     )
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
    self    . emitAllHistory . emit    ( RECORDs                             )
    self    . ShowStatus               ( ""                                  )
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
  def OptimizeParameters               ( self                              ) :
    ##########################################################################
    TRX     = self . Translations
    msg     = self . getMenuItem       ( "Optimize"                          )
    self    . ShowStatus               ( msg                                 )
    self    . TtsTalk                  ( msg , self . getLocality ( )        )
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    if                                 ( DB == None                        ) :
      return
    ##########################################################################
    ##########################################################################
    DB      . Close                    (                                     )
    ##########################################################################
    self    . Optimizing = False
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
  def InsertItem                    ( self                                 ) :
    ##########################################################################
    Id   = self . topLevelItemCount (                                        )
    Id   = int                      ( int ( Id ) + 1                         )
    IT   = self . PrepareEmptyItem  ( Id                                     )
    self . addTopLevelItem          ( IT                                     )
    self . setCurrentItem           ( IT                                     )
    ##########################################################################
    return
  ############################################################################
  def PredictBettings ( self                                               ) :
    ##########################################################################
    self . Go         ( self . Predicting                                    )
    ##########################################################################
    return
  ############################################################################
  def UpdateBettings                    ( self                             ) :
    ##########################################################################
    RECORDs = self . GetCurrentBettings (                                    )
    self    . Go                        ( self . updating , ( RECORDs , )    )
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
  def PredictionMenu                ( self , mm                            ) :
    ##########################################################################
    TRX    = self  . Translations
    MSG    = self  . getMenuItem    ( "Parameters"                           )
    LOM    = mm    . addMenu        ( MSG                                    )
    ##########################################################################
    MSG    = self  . getMenuItem    ( "ReloadSettings"                       )
    mm     . addActionFromMenu      ( LOM , 3001 , MSG                       )
    ##########################################################################
    hid    = self  . Optimizing
    msg    = self  . getMenuItem    ( "Optimize"                             )
    mm     . addActionFromMenu      ( LOM , 3002 , msg , True , hid          )
    ##########################################################################
    hid    = self  . ShowMessage
    msg    = self  . getMenuItem    ( "DisplayMessage"                       )
    mm     . addActionFromMenu      ( LOM , 3003 , msg , True , hid          )
    ##########################################################################
    mm     . addSeparatorFromMenu   ( LOM                                    )
    ##########################################################################
    msg    = self . getMenuItem     ( "MinBets"                              )
    self   . spinMin    = SpinBox   ( None , self . PlanFunc                 )
    self   . spinMin    . setPrefix ( msg                                    )
    self   . spinMin    . setRange  ( 1 , 1000                               )
    self   . spinMin    . setValue  ( self . MinBalls                        )
    mm     . addWidgetWithMenu      ( LOM , 312236326001 , self . spinMin    )
    ##########################################################################
    msg    = self . getMenuItem     ( "MaxBets"                              )
    self   . spinMax    = SpinBox   ( None , self . PlanFunc                 )
    self   . spinMax    . setPrefix ( msg                                    )
    self   . spinMax    . setRange  ( 1 , 1000                               )
    self   . spinMax    . setValue  ( self . MaxBalls                        )
    mm     . addWidgetWithMenu      ( LOM , 312236326002 , self . spinMax    )
    ##########################################################################
    msg    = self . getMenuItem     ( "AppearPeriods"                        )
    self   . spinPeriod = SpinBox   ( None , self . PlanFunc                 )
    self   . spinPeriod . setPrefix ( msg                                    )
    self   . spinPeriod . setRange  ( 5 , 5000                               )
    self   . spinPeriod . setValue  ( self . Periods                         )
    mm     . addWidgetWithMenu      ( LOM , 312236326003 , self . spinPeriod )
    ##########################################################################
    return mm
  ############################################################################
  def RunPredictionMenu            ( self , atId                           ) :
    ##########################################################################
    self . MinBalls = self . spinMin    . value (                            )
    self . MaxBalls = self . spinMax    . value (                            )
    self . Periods  = self . spinPeriod . value (                            )
    ##########################################################################
    ##########################################################################
    if                             ( atId == 3001                          ) :
      self . LoadSettings          (                                         )
      return True
    ##########################################################################
    if                             ( atId == 3002                          ) :
      if                           ( self . Optimizing                     ) :
        self . Optimizing = False
      else                                                                   :
        self . Optimizing = True
        self . Go                  ( self . OptimizeParameters               )
      return True
    ##########################################################################
    if                             ( atId == 3003                          ) :
      if                           ( self . ShowMessage                    ) :
        self . ShowMessage = False
      else                                                                   :
        self . ShowMessage = True
      return True
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
    mm     = self . AppendInsertAction  ( mm , 1002                          )
    mm     . addSeparator           (                                        )
    msg    = self . getMenuItem     ( "Prediction"                           )
    mm     . addAction              ( 1101 , msg                             )
    msg    = self . getMenuItem     ( "UpdateBets"                           )
    mm     . addAction              ( 1102 , msg                             )
    mm     . addSeparator           (                                        )
    msg    = self . getMenuItem     ( "SelectAll"                            )
    mm     . addAction              ( 1103 , msg                             )
    msg    = self . getMenuItem     ( "SelectNone"                           )
    mm     . addAction              ( 1104 , msg                             )
    ##########################################################################
    mm     . addSeparator           (                                        )
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
      self . InsertItem             (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      ########################################################################
      self . PredictBettings        (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1102                           ) :
      ########################################################################
      self . UpdateBettings         (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1103                           ) :
      ########################################################################
      self . PickAll                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1104                           ) :
      ########################################################################
      self . PickNone               (                                        )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
