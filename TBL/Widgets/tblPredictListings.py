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
                 [ 4 , 5 , 6 , 7 , 8 , 9 ]                                   ]
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
                   [  1 ,  3 ,  5 ,  7 ,  9 , 11 ]                           ]
##############################################################################
PWL10x6x5 = [ [  0 ,  1 ,  2 ,  3 ,  4 , 8 ]                               , \
              [  0 ,  1 ,  2 ,  3 ,  6 , 9 ]                               , \
              [  0 ,  1 ,  2 ,  6 ,  7 , 8 ]                               , \
              [  0 ,  1 ,  3 ,  4 ,  5 , 7 ]                               , \
              [  0 ,  1 ,  3 ,  5 ,  8 , 9 ]                               , \
              [  0 ,  2 ,  4 ,  5 ,  7 , 9 ]                               , \
              [  0 ,  3 ,  4 ,  6 ,  7 , 9 ]                               , \
              [  0 ,  4 ,  5 ,  6 ,  8 , 9 ]                               , \
              [  1 ,  2 ,  3 ,  4 ,  5 , 6 ]                               , \
              [  1 ,  2 ,  5 ,  6 ,  7 , 9 ]                               , \
              [  1 ,  2 ,  5 ,  7 ,  8 , 9 ]                               , \
              [  1 ,  4 ,  6 ,  7 ,  8 , 9 ]                               , \
              [  2 ,  3 ,  4 ,  7 ,  8 , 9 ]                               , \
              [  2 ,  3 ,  5 ,  6 ,  7 , 8 ]                                 ]
##############################################################################
PWL11x6x5 = [ [  0 ,  1 ,  2 ,  3 ,  4 ,  9 ]                              , \
              [  0 ,  1 ,  2 ,  5 ,  9 , 10 ]                              , \
              [  0 ,  1 ,  2 ,  6 ,  8 , 10 ]                              , \
              [  0 ,  1 ,  3 ,  7 ,  8 , 10 ]                              , \
              [  0 ,  1 ,  4 ,  6 ,  8 , 10 ]                              , \
              [  0 ,  1 ,  5 ,  7 ,  8 ,  9 ]                              , \
              [  0 ,  1 ,  6 ,  7 ,  9 , 10 ]                              , \
              [  0 ,  2 ,  3 ,  4 ,  5 ,  8 ]                              , \
              [  0 ,  2 ,  3 ,  7 ,  9 , 10 ]                              , \
              [  0 ,  2 ,  4 ,  5 ,  6 ,  7 ]                              , \
              [  0 ,  2 ,  4 ,  6 ,  9 , 10 ]                              , \
              [  0 ,  3 ,  4 ,  5 ,  6 , 10 ]                              , \
              [  0 ,  3 ,  4 ,  7 ,  8 ,  9 ]                              , \
              [  0 ,  3 ,  5 ,  6 ,  8 ,  9 ]                              , \
              [  1 ,  2 ,  3 ,  5 ,  6 ,  7 ]                              , \
              [  1 ,  2 ,  4 ,  5 ,  6 ,  9 ]                              , \
              [  1 ,  2 ,  4 ,  7 ,  8 , 10 ]                              , \
              [  1 ,  3 ,  4 ,  5 ,  7 , 10 ]                              , \
              [  1 ,  3 ,  4 ,  6 ,  7 ,  8 ]                              , \
              [  1 ,  3 ,  5 ,  8 ,  9 , 10 ]                              , \
              [  2 ,  3 ,  4 ,  6 ,  9 , 10 ]                              , \
              [  2 ,  3 ,  6 ,  7 ,  8 ,  9 ]                              , \
              [  2 ,  5 ,  6 ,  7 ,  8 , 10 ]                              , \
              [  3 ,  4 ,  5 ,  7 ,  9 , 10 ]                              , \
              [  4 ,  5 ,  7 ,  8 ,  9 , 10 ]                                ]
##############################################################################
PWL12x6x5 = [ [  0 ,  1 ,  2 ,  3 ,  4 , 11 ]                              , \
              [  0 ,  1 ,  2 ,  3 ,  7 ,  8 ]                              , \
              [  0 ,  1 ,  2 ,  4 ,  9 , 10 ]                              , \
              [  0 ,  1 ,  2 ,  5 ,  6 ,  9 ]                              , \
              [  0 ,  1 ,  3 ,  4 ,  6 , 10 ]                              , \
              [  0 ,  1 ,  3 ,  5 ,  7 , 10 ]                              , \
              [  0 ,  1 ,  4 ,  5 ,  8 ,  9 ]                              , \
              [  0 ,  1 ,  4 ,  6 ,  7 , 11 ]                              , \
              [  0 ,  1 ,  6 ,  8 , 10 , 11 ]                              , \
              [  0 ,  1 ,  7 ,  8 ,  9 , 11 ]                              , \
              [  0 ,  2 ,  3 ,  4 ,  6 ,  8 ]                              , \
              [  0 ,  2 ,  4 ,  5 ,  7 , 11 ]                              , \
              [  0 ,  2 ,  5 ,  8 , 10 , 11 ]                              , \
              [  0 ,  2 ,  6 ,  7 ,  9 , 10 ]                              , \
              [  0 ,  2 ,  6 ,  7 , 10 , 11 ]                              , \
              [  0 ,  3 ,  4 ,  7 , 10 , 11 ]                              , \
              [  0 ,  3 ,  4 ,  8 ,  9 , 10 ]                              , \
              [  0 ,  3 ,  5 ,  6 ,  9 , 11 ]                              , \
              [  0 ,  3 ,  5 ,  8 ,  9 , 10 ]                              , \
              [  0 ,  4 ,  5 ,  6 ,  7 ,  8 ]                              , \
              [  0 ,  4 ,  7 ,  8 ,  9 , 11 ]                              , \
              [  0 ,  5 ,  6 ,  7 ,  8 , 11 ]                              , \
              [  1 ,  2 ,  3 ,  4 ,  5 ,  9 ]                              , \
              [  1 ,  2 ,  3 ,  5 ,  6 ,  8 ]                              , \
              [  1 ,  2 ,  3 ,  9 , 10 , 11 ]                              , \
              [  1 ,  2 ,  4 ,  7 ,  8 , 10 ]                              , \
              [  1 ,  2 ,  4 ,  8 ,  9 , 11 ]                              , \
              [  1 ,  2 ,  5 ,  6 ,  7 , 11 ]                              , \
              [  1 ,  3 ,  4 ,  5 ,  8 , 11 ]                              , \
              [  1 ,  3 ,  4 ,  6 ,  7 ,  9 ]                              , \
              [  1 ,  3 ,  6 ,  7 ,  8 ,  9 ]                              , \
              [  1 ,  4 ,  5 ,  6 , 10 , 11 ]                              , \
              [  1 ,  5 ,  6 ,  8 ,  9 , 10 ]                              , \
              [  1 ,  5 ,  7 ,  9 , 10 , 11 ]                              , \
              [  2 ,  3 ,  4 ,  5 ,  6 , 10 ]                              , \
              [  2 ,  3 ,  4 ,  7 ,  9 , 11 ]                              , \
              [  2 ,  3 ,  5 ,  6 ,  7 , 10 ]                              , \
              [  2 ,  3 ,  5 ,  7 ,  8 ,  9 ]                              , \
              [  2 ,  3 ,  8 ,  9 , 10 , 11 ]                              , \
              [  2 ,  4 ,  6 ,  8 ,  9 , 11 ]                              , \
              [  3 ,  4 ,  5 ,  6 ,  7 ,  9 ]                              , \
              [  3 ,  6 ,  7 ,  8 , 10 , 11 ]                              , \
              [  4 ,  5 ,  6 ,  9 , 10 , 11 ]                              , \
              [  4 ,  5 ,  7 ,  8 ,  9 , 10 ]                                ]
##############################################################################
class tblPredictListings            ( TreeDock                             ) :
  ############################################################################
  HavingMenu     = 1371434312
  ############################################################################
  emitAllHistory = pyqtSignal       ( list                                   )
  emitBettings   = pyqtSignal       ( list                                   )
  emitPredict    = pyqtSignal       (                                        )
  emitUpdate     = pyqtSignal       (                                        )
  emitPickAll    = pyqtSignal       (                                        )
  emitPickNone   = pyqtSignal       (                                        )
  emitPickings   = pyqtSignal       ( str , bool                             )
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
    self . WheelBalls         = 11
    self . SelectBalls        = 20
    self . Periods            = 100
    self . tblHost            = "http://insider.actions.com.tw:8364"
    self . Bettings           = [                                            ]
    self . tblSettings        = {                                            }
    self . tblParameters      = {                                            }
    self . tblAppears         = {                                            }
    self . WETMT49            = {                                            }
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
    self . emitPickAll    . connect ( self . PickAll                         )
    self . emitPickNone   . connect ( self . PickNone                        )
    self . emitPredict    . connect ( self . PredictBettings                 )
    self . emitUpdate     . connect ( self . UpdateBettings                  )
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
    return self . SizeSuggestion ( QSize ( 560 , 800 )                       )
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
    self . LinkAction ( "Start"      , self . UpdateBettings  , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Paste"      , self . Paste           , Enabled      )
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
    self . Notify            ( 0                                             )
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
  def GetItemBalls                ( self , item                            ) :
    ##########################################################################
    V    =                        [                                          ]
    for i in range                ( 2 , 8                                  ) :
      V  . append                 ( item . text ( i )                        )
    ##########################################################################
    return " " . join             ( V                                        )
  ############################################################################
  def GetSelectedBalls            ( self                                   ) :
    ##########################################################################
    items = self . selectedItems  (                                          )
    V     =                       [                                          ]
    for item in items                                                        :
      S   = self . GetItemBalls   ( item                                     )
      V   . append                ( S                                        )
    ##########################################################################
    return "\n" . join            ( V                                        )
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
    self   . setFocus           (                                            )
    self   . FocusIn            (                                            )
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
  def appendText          ( self , message                                 ) :
    ##########################################################################
    if                    ( not self . ShowMessage                         ) :
      return
    ##########################################################################
    self . addText . emit ( message                                          )
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
    BALLS  = self . tblSettings       [ "Bettings" ] [ "Range" ] [ "Balls"   ]
    ##########################################################################
    self   . SelectBalls = BALLS
    ##########################################################################
    if                                ( self . MinBalls < 0                ) :
      self . MinBalls = MIN
    ##########################################################################
    if                                ( self . MaxBalls < 0                ) :
      self . MaxBalls = MAX
    ##########################################################################
    return
  ############################################################################
  def GetOptionItems        ( self , DB , KEY                              ) :
    ##########################################################################
    QQ = f"""select `index` from `predictions`.`tbl-options`
             where ( `key` = '{KEY}' )
               and ( `value` > 0 )
             order by `index` asc ;"""
    QQ = " " . join         ( QQ . split (                                 ) )
    ##########################################################################
    return DB . ObtainUuids ( QQ                                             )
  ############################################################################
  def UpdateSettings               ( self , DB                             ) :
    ##########################################################################
    FIRST  = self . GetOptionItems ( DB , "First"                            )
    ENDING = self . GetOptionItems ( DB , "Ending"                           )
    SUMS   = self . GetOptionItems ( DB , "Sums"                             )
    AC     = self . GetOptionItems ( DB , "AC"                               )
    ODDS   = self . GetOptionItems ( DB , "Odd"                              )
    GAPS   = self . GetOptionItems ( DB , "Gaps"                             )
    FSUMS  = self . GetOptionItems ( DB , "Head-Sums"                        )
    ESUMS  = self . GetOptionItems ( DB , "Tail-Sums"                        )
    ##########################################################################
    self . tblSettings [ "Bettings" ] [ "First"     ] = FIRST
    self . tblSettings [ "Bettings" ] [ "Ending"    ] = ENDING
    self . tblSettings [ "Bettings" ] [ "Sums"      ] = SUMS
    self . tblSettings [ "Bettings" ] [ "AC"        ] = AC
    self . tblSettings [ "Bettings" ] [ "Odds"      ] = ODDS
    self . tblSettings [ "Bettings" ] [ "Gaps"      ] = GAPS
    self . tblSettings [ "Bettings" ] [ "FirstSums" ] = FSUMS
    self . tblSettings [ "Bettings" ] [ "EndSums"   ] = ESUMS
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
  def CombinePWL10x6x5IntoLists      ( self , Balls                        ) :
    ##########################################################################
    global PWL10x6x5
    ##########################################################################
    if                               ( len ( Balls ) != 10                 ) :
      return                         [                                       ]
    ##########################################################################
    LISTS   =                        [                                       ]
    ##########################################################################
    for R in PWL10x6x5                                                       :
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
  def CombinePosition11x6x5IntoLists ( self , Balls                        ) :
    ##########################################################################
    global PWL11x6x5
    ##########################################################################
    if                               ( len ( Balls ) != 11                 ) :
      return                         [                                       ]
    ##########################################################################
    LISTS   =                        [                                       ]
    ##########################################################################
    for R in PWL11x6x5                                                       :
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
  def CombinePosition12x6x5IntoLists ( self , Balls                        ) :
    ##########################################################################
    global Position12x6x5
    global PWL12x6x5
    ##########################################################################
    if                               ( len ( Balls ) != 12                 ) :
      return                         [                                       ]
    ##########################################################################
    LISTS   =                        [                                       ]
    ##########################################################################
    for R in PWL12x6x5                                                       :
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
    ## PC            = TBLs . RandomBalls    ( 10 , BALLS , AP , [ ]            )
    ## random        . shuffle               ( PC                               )
    ## LZ            = self . CombineRotate10x6x5IntoLists   ( PC               )
    ##########################################################################
    ## PC            = TBLs . RandomBalls    ( 10 , BALLS , AP , [ ]            )
    ## random        . shuffle               ( PC                               )
    ## LL            = self . CombinePWL10x6x5IntoLists ( PC                    )
    ##########################################################################
    PC            = TBLs . RandomBalls    ( 11 , BALLS , AP , [ ]            )
    random        . shuffle               ( PC                               )
    LL            = self . CombinePosition11x6x5IntoLists ( PC               )
    ##########################################################################
    ## PC            = TBLs . RandomBalls    ( 12 , BALLS , AP , [ ]            )
    ## random        . shuffle               ( PC                               )
    ## LL            = self . CombinePosition12x6x5IntoLists ( PC               )
    ##########################################################################
    ## LW            = LZ
    LW = LL
    ##########################################################################
    ## for L in LL                                                              :
      ########################################################################
    ##   MATCHED     = False
      ########################################################################
    ##   for Z in LZ                                                            :
    ##     RX        = TBLs . CompareTwoSets ( L , Z                            )
    ##     if                                ( RX == 6                        ) :
    ##       MATCHED = True
      ########################################################################
    ##   if                                  ( not MATCHED                    ) :
    ##     LW        . append                ( L                                )
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
  ## 與所有的歷史紀錄有三球或四球相同
  ############################################################################
  def HistoryInRange             ( self , TBLs , Bets                      ) :
    ##########################################################################
    LASTEST = TBLs . Serials     (                                           )
    LW      =                    [                                           ]
    JSOZ    = self . tblSettings [ "Bettings"                                ]
    R       = JSOZ               [ "HistoryInRange"                          ]
    ##########################################################################
    for B in Bets                                                            :
      ########################################################################
      if                         ( TBLs . isHistoryInRange ( B , R )       ) :
        LW  . append             ( B                                         )
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
  def RuleOutBettings        ( self , DB , TBLs , Bets                     ) :
    ##########################################################################
    NUMTAB  = self . Tables  [ "Numbers"                                     ]
    DIFTAB  = self . Tables  [ "Differences"                                 ]
    ##########################################################################
    LASTEST = TBLs . Serials (                                               )
    T       = TBLs . at      ( LASTEST                                       )
    LW      =                [                                               ]
    TBLZ    = TaiwanBL       (                                               )
    ##########################################################################
    for B in Bets                                                            :
      ########################################################################
      TBLZ  . N6 = B
      ########################################################################
      if                     ( TBLZ . isNumberAllowed ( DB , NUMTAB )      ) :
        LW  . append         ( B                                             )
    ##########################################################################
    return LW
  ############################################################################
  def JoinToOLDs               ( self , OLDs , TBLZ                        ) :
    ##########################################################################
    TBLX = TaiwanBL            (                                             )
    ##########################################################################
    for T in OLDs                                                            :
      ########################################################################
      for i in range           ( 0 , 6                                     ) :
        TBLX . N6 [ i ] = T    [ i                                           ]
      ########################################################################
      matches = TBLX . Matches ( 6 , TBLZ                                    )
      ########################################################################
      if                       ( matches == 6                              ) :
        return OLDs
    ##########################################################################
    OLDs . append              ( TBLZ                                        )
    ##########################################################################
    return OLDs
  ############################################################################
  def JoinTBLs                 ( self , OLDs , NEWs                        ) :
    ##########################################################################
    for N in NEWs                                                            :
      ########################################################################
      OLDs = self . JoinToOLDs ( OLDs , N                                    )
    ##########################################################################
    return OLDs
  ############################################################################
  def GetTBLs                                  ( self , DB                 ) :
    ##########################################################################
    HISTORY = self . ObtainAllHistory          ( DB                          )
    TBLs    = TaiwanBLs                        (                             )
    TBLs    . setAppearanceWeight              ( self . tblAppears           )
    TBLs    . ImportHistory                    ( HISTORY                     )
    LASTEST = TBLs . Serials                   (                             )
    MSG     = TBLs . at ( LASTEST ) . toString (                             )
    NUMS    = TBLs . at ( LASTEST ) . numbers  ( 6                           )
    self    . appendText                       ( MSG                         )
    ##########################################################################
    return TBLs
  ############################################################################
  def isBallPicked              ( self , DB , SERIAL                       ) :
    ##########################################################################
    ITEMs       =               [                                            ]
    ##########################################################################
    for i in range              ( 1 , 50                                   ) :
      ########################################################################
      if                        ( i < 10                                   ) :
        NN      = f"`n0{i}`"
      else                                                                   :
        NN      = f"`n{i}`"
      ########################################################################
      ITEMs     . append        ( NN                                         )
    ##########################################################################
    ITEMX       = " , " . join  ( ITEMs                                      )
    QQ          = f"""select {ITEMX} from `predictions`.`tbl-pickings`
                      where ( `serial` = '{SERIAL}' ) ;"""
    QQ          = " " . join    ( QQ . split ( )                             )
    DB          . Query         ( QQ                                         )
    ALLs        = DB . FetchAll (                                            )
    ##########################################################################
    if                          ( self . NotOkay ( ALLs )                  ) :
      return                    [                                            ]
    ##########################################################################
    if                          ( len ( ALLs       ) != 1                  ) :
      return                    [                                            ]
    ##########################################################################
    if                          ( len ( ALLs [ 0 ] ) != 49                 ) :
      return                    [                                            ]
    ##########################################################################
    ALL         = ALLs          [ 0                                          ]
    BALLs       =               [                                            ]
    ##########################################################################
    for i in range              ( 0 , 49                                   ) :
      ########################################################################
      try                                                                    :
        ######################################################################
        BALL    = int           ( i + 1                                      )
        BV      = int           ( ALL [ i ]                                  )
        if                      ( BV > 0                                   ) :
          BALLs . append        ( BALL                                       )
        ######################################################################
      except                                                                 :
        pass
    ##########################################################################
    return BALLs
  ############################################################################
  def GetPickingBalls                        ( self , DB , TBLs            ) :
    ##########################################################################
    MIN     = self . tblSettings [ "Bettings" ] [ "Range" ] [ "Min"          ]
    MAX     = self . tblSettings [ "Bettings" ] [ "Range" ] [ "Max"          ]
    ABALLS  = self . tblSettings [ "Bettings" ] [ "Balls"                    ]
    LASTEST = TBLs . Serials                 (                               )
    LX      =                                [                               ]
    ##########################################################################
    APPEARS = TBLs . CreateAppears           ( 32 , 7                        )
    CDISAPP = TBLs . CountDisappears         ( LASTEST , 6                   )
    DISAPPW = TBLs . ConvertDisappearWeight  ( CDISAPP                       )
    self    . WETMT49 = TBLs . MultiplyTwo49 ( APPEARS , DISAPPW             )
    ##########################################################################
    BALLX   =                                {                               }
    BALLS   =                                [                               ]
    KKBB    =                                [                               ]
    KKYY    =                                [                               ]
    ##########################################################################
    BALLX   = TBLs . PickAppears             ( LASTEST                     , \
                                               self . Periods              , \
                                               1                           , \
                                               self . SelectBalls          , \
                                               BALLX                         )
    for i in range                           ( 0 , self . SelectBalls      ) :
      ########################################################################
      BB    = BALLX                          [ i                             ]
      BALLS . append                         ( BB                            )
      ########################################################################
      if                                     ( BB < 10                     ) :
        NN  = f"`n0{BB}`"
      else                                                                   :
        NN  = f"`n{BB}`"
      ########################################################################
      KKBB  . append                         ( NN                            )
      KKYY  . append                         ( "1"                           )
    ##########################################################################
    SERIX   = self . Prediction
    QQ      = f"""delete from `predictions`.`tbl-pickings`
                  where ( `serial` = '{SERIX}' ) ;"""
    QQ      = " " . join                     ( QQ . split ( )                )
    DB      . Query                          ( QQ                            )
    ##########################################################################
    NLS     = "," . join                     ( KKBB                          )
    VLS     = "," . join                     ( KKYY                          )
    QQ      = f"""insert into `predictions`.`tbl-pickings`
                  ( `serial`,{NLS} ) values ( '{SERIX}',{VLS} ) ;"""
    QQ      = " " . join                     ( QQ . split ( )                )
    DB      . Query                          ( QQ                            )
    ##########################################################################
    self    . appendText                     ( json . dumps ( BALLS   )      )
    ##########################################################################
    return BALLS
  ############################################################################
  def PreparePickings                        ( self , DB , TBLs            ) :
    ##########################################################################
    MIN     = self . tblSettings [ "Bettings" ] [ "Range" ] [ "Min"          ]
    MAX     = self . tblSettings [ "Bettings" ] [ "Range" ] [ "Max"          ]
    ABALLS  = self . tblSettings [ "Bettings" ] [ "Balls"                    ]
    LASTEST = TBLs . Serials                 (                               )
    LX      =                                [                               ]
    ##########################################################################
    APPEARS = TBLs . CreateAppears           ( 32 , 7                        )
    CDISAPP = TBLs . CountDisappears         ( LASTEST , 6                   )
    DISAPPW = TBLs . ConvertDisappearWeight  ( CDISAPP                       )
    self    . WETMT49 = TBLs . MultiplyTwo49 ( APPEARS , DISAPPW             )
    ##########################################################################
    return
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
    TBLs    = self . GetTBLs           ( DB                                  )
    BALLS   = self . isBallPicked      ( DB , self . Prediction              )
    if                                 ( len ( BALLS ) > 0                 ) :
      self  . PreparePickings          ( DB , TBLs                           )
    else                                                                     :
      BALLS = self . GetPickingBalls   ( DB , TBLs                           )
    ##########################################################################
    WORK    = False
    TRYS    = 0
    LW      =                          [                                     ]
    OLDs    =                          [                                     ]
    ##########################################################################
    while                              ( not WORK                          ) :
      ########################################################################
      if                               ( TRYS > 900                        ) :
        WORK = True
        continue
      ########################################################################
      LW    = self . GenerateBettings  (      TBLs , BALLS , self . WETMT49  )
      LW    = self . FilterAllRules    (      TBLs , LW                      )
      LW    = self . HistoryDuplicate  (      TBLs , LW                      )
      LW    = self . HistoryInRange    (      TBLs , LW                      )
      LW    = self . TripleDuplicate   (      TBLs , LW                      )
      LW    = self . RuleOutBettings   ( DB , TBLs , LW                      )
      ########################################################################
      OLDs  = self . JoinTBLs          (      OLDs , LW                      )
      ########################################################################
      self  . appendText               ( json . dumps ( LW )                 )
      ########################################################################
      TRYS  = TRYS + 1
      LZ    = len                      ( OLDs                                )
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
    if                                 ( len ( OLDs ) <= 0                 ) :
      self  . Notify                   ( 1                                   )
      return
    ##########################################################################
    self . emitBettings . emit         ( OLDs                                )
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
    if                                 ( self . NotOkay ( DB )             ) :
      return
    ##########################################################################
    self    . UpdateSettings           ( DB                                  )
    ##########################################################################
    self    . Notify                   ( 3                                   )
    self    . OnBusy  . emit           (                                     )
    self    . setBustle                (                                     )
    ##########################################################################
    FMT     = self . Translations      [ "UI::StartLoading"                  ]
    MSG     = FMT . format             ( self . windowTitle ( )              )
    self    . ShowStatus               ( MSG                                 )
    ##########################################################################
    self    . ObtainsInformation       ( DB                                  )
    RECORDs = self . ObtainsPrediction ( DB                                  )
    ##########################################################################
    self    . setVacancy               (                                     )
    self    . GoRelax . emit           (                                     )
    self    . ShowStatus               ( ""                                  )
    DB      . Close                    (                                     )
    ##########################################################################
    self    . emitAllHistory . emit    ( RECORDs                             )
    self    . ShowStatus               ( ""                                  )
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
  def CommandParser           ( self , language , message , timestamp      ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      self . DoPickAll        (                                              )
      return                  { "Match"   : True                           , \
                                "Message" : TRX [ "UI::SelectAll" ]          }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectNone"   , message )  ) :
      self . DoPickNone       (                                              )
      return                  { "Match"   : True                           , \
                                "Message" : TRX [ "UI::SelectNone" ]         }
    ##########################################################################
    if ( self . WithinCommand ( language , "TBL::DoPredict"   , message )  ) :
      self . emitPredict . emit (                                            )
      return                  { "Match"   : True                             }
    ##########################################################################
    if ( self . WithinCommand ( language , "TBL::DoUpdate"    , message )  ) :
      self . emitUpdate . emit (                                             )
      return                  { "Match"   : True                             }
    ##########################################################################
    return                    { "Match" : False                              }
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
  ## 發送RPC命令
  ############################################################################
  def SendRPC                  ( self , Command , JSON                     ) :
    ##########################################################################
    HOST     = self . tblHost
    CMD      = f"{HOST}/{Command}"
    Headers  = { "Username" : "foxman"                                       ,
                 "Password" : "actionsfox2019"                               }
    try                                                                      :
      status = requests . post ( CMD                                         ,
                                 data    = json . dumps ( JSON )             ,
                                 headers = Headers                           )
    except                                                                   :
      return False
    ##########################################################################
    return status . status_code
  ############################################################################
  def CopyToClipboard              ( self                                  ) :
    ##########################################################################
    T = self . GetSelectedBalls    (                                         )
    if                             ( len ( T ) <= 0                        ) :
      return
    ##########################################################################
    qApp . clipboard ( ) . setText ( T                                       )
    ##########################################################################
    return
  ############################################################################
  def PasteItem                        ( self , Id , Line                  ) :
    ##########################################################################
    N      = Line . split              ( " "                                 )
    if                                 ( len ( N ) != 6                    ) :
      return  False
    ##########################################################################
    R      =                           [                                     ]
    for V in N                                                               :
      ########################################################################
      B    = int                       ( V                                   )
      ########################################################################
      if                               ( ( B < 1 ) or ( B > 49 )           ) :
        return False
      ########################################################################
      if                               ( B in R                            ) :
        return False
      ########################################################################
      R    . append                    ( B                                   )
    ##########################################################################
    IT     = self . PrepareItem        ( Id , R , False                      )
    self   . addTopLevelItem           ( IT                                  )
    ##########################################################################
    return True
  ############################################################################
  def Paste                                ( self                          ) :
    ##########################################################################
    T        = qApp . clipboard ( ) . text (                                 )
    L        = T    . split                ( "\n"                            )
    ##########################################################################
    if                                     ( len ( L ) <= 0                ) :
      return
    ##########################################################################
    BASE     = self . topLevelItemCount    (                                 )
    BASE     = BASE + 1
    ##########################################################################
    for X in L                                                               :
      OK     = self . PasteItem            ( BASE , X                        )
      if                                   ( OK                            ) :
        BASE = BASE + 1
    ##########################################################################
    self     . Notify                      ( 5                               )
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
  def DoPickAll                  ( self                                    ) :
    ##########################################################################
    self . emitPickAll . emit    (                                           )
    ##########################################################################
    return
  ############################################################################
  def PickNone                   ( self                                    ) :
    ##########################################################################
    for i in range               ( 0 , self . topLevelItemCount ( )        ) :
      IT  = self . topLevelItem  ( i                                         )
      IT  . setCheckState        ( 0 , Qt . Unchecked                        )
    ##########################################################################
    return
  ############################################################################
  def DoPickNone                 ( self                                    ) :
    ##########################################################################
    self . emitPickNone . emit   (                                           )
    ##########################################################################
    return
  ############################################################################
  def MaximumMatches                   ( self , tbl , TBLs , Total         ) :
    ##########################################################################
    if                                 ( Total < 2                         ) :
      return 0
    ##########################################################################
    MAXV     = 0
    A        = tbl  . numbers          ( 6                                   )
    A        = TBLs . toList           ( A                                   )
    ##########################################################################
    for i in range                     ( 1 , Total                         ) :
      ########################################################################
      T      = TBLs . at               ( i                                   )
      B      = T    . numbers          ( 6                                   )
      B      = TBLs . toList           ( B                                   )
      V      = TBLs . CompareTwoSets   ( A , B                               )
      ########################################################################
      if                               ( V > MAXV                          ) :
        MAXV = V
    ##########################################################################
    return MAXV
  ############################################################################
  def Analysis                         ( self                              ) :
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
    ##########################################################################
    DB      . Close                    (                                     )
    ##########################################################################
    RESULT  =                          { 0 : 0                             , \
                                         1 : 0                             , \
                                         2 : 0                             , \
                                         3 : 0                             , \
                                         4 : 0                             , \
                                         5 : 0                             , \
                                         6 : 0                               }
    ##########################################################################
    for i in range                     ( 1 , LASTEST + 1                   ) :
      tbl   = TBLs . at                ( i                                   )
      V     = self  . MaximumMatches   ( tbl , TBLs , i                      )
      if                               ( i > 400                           ) :
        RESULT [ V ] = RESULT [ V ] + 1
      print                            ( tbl . toString ( ) , " - " , V      )
    ##########################################################################
    print                              ( RESULT                              )
    ##########################################################################
    return
  ############################################################################
  ## 列印投注
  ############################################################################
  def PrintPdfNumbers           ( self                                     ) :
    ##########################################################################
    JSON              =         {                                            }
    PAPER             = self . tblSettings [ "Bettings" ] [ "Paper"          ]
    ##########################################################################
    JSON [ "Action" ] = "PrintBets"
    JSON [ "X"      ] = PAPER   [ "X"                                        ]
    JSON [ "Y"      ] = PAPER   [ "Y"                                        ]
    JSON [ "Gap"    ] = PAPER   [ "Gap"                                      ]
    JSON [ "W"      ] = PAPER   [ "Width"                                    ]
    JSON [ "H"      ] = PAPER   [ "Height"                                   ]
    JSON [ "L"      ] = PAPER   [ "Length"                                   ]
    JSON [ "Text"   ] = PAPER   [ "Text"                                     ]
    ##########################################################################
    self              . SendRPC ( "TBL" , JSON                               )
    ##########################################################################
    return
  ############################################################################
  def GeneratePickingBalls         ( self , DB                             ) :
    ##########################################################################
    TBLs  = self . GetTBLs         ( DB                                      )
    BALLS = self . GetPickingBalls ( DB , TBLs                               )
    ##########################################################################
    return BALLS
  ############################################################################
  def PickBalls                 ( self                                     ) :
    ##########################################################################
    DB   = self . ConnectDB     (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return
    ##########################################################################
    self . GeneratePickingBalls ( DB                                         )
    ##########################################################################
    DB   . Close                (                                            )
    ##########################################################################
    self . Notify               ( 5                                          )
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
    msg    = self . getMenuItem     ( "SelectBalls"                          )
    self   . spinBalls  = SpinBox   ( None , self . PlanFunc                 )
    self   . spinBalls  . setPrefix ( msg                                    )
    self   . spinBalls  . setRange  ( 6 , 49                                 )
    self   . spinBalls  . setValue  ( self . SelectBalls                     )
    mm     . addWidgetWithMenu      ( LOM , 312236326004 , self . spinBalls  )
    ##########################################################################
    return mm
  ############################################################################
  def RunPredictionMenu            ( self , atId                           ) :
    ##########################################################################
    self . MinBalls    = self . spinMin    . value (                         )
    self . MaxBalls    = self . spinMax    . value (                         )
    self . Periods     = self . spinPeriod . value (                         )
    self . SelectBalls = self . spinBalls  . value (                         )
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
    if                              ( len ( self . Prediction ) <= 0       ) :
      return False
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
    msg    = self . getMenuItem     ( "Pickings"                             )
    mm     . addAction              ( 5114 , msg                             )
    ##########################################################################
    msg    = self . getMenuItem     ( "OpenPickings"                         )
    mm     . addAction              ( 5115 , msg                             )
    ##########################################################################
    msg    = self . getMenuItem     ( "Analysis"                             )
    mm     . addAction              ( 5116 , msg                             )
    ##########################################################################
    msg    = self . getMenuItem     ( "PrintNumbers"                         )
    mm     . addAction              ( 5117 , msg                             )
    ##########################################################################
    mm     . addSeparator           (                                        )
    mm     = self . PredictionMenu  ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
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
    if                              ( at == 5114                           ) :
      ########################################################################
      self . Go                     ( self . PickBalls                       )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 5115                           ) :
      ########################################################################
      self . emitPickings . emit    ( self . Prediction , True               )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 5116                           ) :
      ########################################################################
      self . Go                     ( self . Analysis                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 5117                           ) :
      ########################################################################
      self . Go                     ( self . PrintPdfNumbers                 )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
