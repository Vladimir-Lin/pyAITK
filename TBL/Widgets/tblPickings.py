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
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QBrush
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTableWidget
from   PyQt5 . QtWidgets              import QTableWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . TableDock         import TableDock   as TableDock
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
class tblPickings                   ( TableDock                            ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  attachNone = pyqtSignal           ( QWidget                                )
  attachDock = pyqtSignal           ( QWidget , str , int , int              )
  attachMdi  = pyqtSignal           ( QWidget , int                          )
  ############################################################################
  emitBalls  = pyqtSignal           (                                        )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            (        parent        , plan            )
    ##########################################################################
    random . seed                   ( time . time ( )                        )
    ##########################################################################
    self . Serial   = ""
    self . Pickings = [ ]
    self . Columns  = 7
    self . Rows     = 7
    ##########################################################################
    ## self . setColumnCount           ( 9                                      )
    ## self . setRootIsDecorated       ( False                                  )
    ## self . setAlternatingRowColors  ( True                                   )
    ##########################################################################
    ## self . MountClicked             ( 1                                      )
    ## self . MountClicked             ( 2                                      )
    ##########################################################################
    ## self . assignSelectionMode      ( "ContiguousSelection"                  )
    ##########################################################################
    self . emitBalls . connect      ( self . refresh                         )
    ##########################################################################
    ## self . setFunction              ( self . FunctionDocking , True          )
    self . setFunction              ( self . HavingMenu      , True          )
    ##########################################################################
    self . setDragEnabled           ( False                                  )
    self . setAcceptDrops           ( False                                  )
    self . setDragDropMode          ( QAbstractItemView . NoDragDrop         )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 400 , 400 )                       )
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
    ## self . LinkAction ( "Start"      , self . UpdateBettings  , Enabled      )
    ## self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    ## self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    ## self . LinkAction ( "Paste"      , self . Paste           , Enabled      )
    ##########################################################################
    ## self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    ## self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    ## self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    ## self . setActionLabel    ( "Label" , self . windowTitle ( )              )
    ## self . AttachActions     ( True                                          )
    ## self . attachActionsTool (                                               )
    ## self . LinkVoice         ( self . CommandParser                          )
    ## self . Notify            ( 0                                             )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut ( self                                                      ) :
    ##########################################################################
    ## if         ( not self . isPrepared ( )                                 ) :
    ##   return True
    ##########################################################################
    return False
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    ## self . AttachActions     ( False                                         )
    ## self . LinkVoice         ( None                                          )
    ## self . defaultCloseEvent (        event                                  )
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
  def setLabels                           ( self                           ) :
    ##########################################################################
    LineStr   = self . getMenuItem        ( "BallStatistics"                 )
    HLabels   =                           [                                  ]
    VLabels   =                           [                                  ]
    ##########################################################################
    for i in range                        ( 1 , self . Columns + 1         ) :
      HLabels . append                    ( str ( i )                        )
    ##########################################################################
    for i in range                        ( 1 , self . Rows    + 1         ) :
      VLabels . append                    ( str ( i )                        )
    ##########################################################################
    HLabels   . append                    ( LineStr                          )
    VLabels   . append                    ( LineStr                          )
    ##########################################################################
    self      . setHorizontalHeaderLabels ( HLabels                          )
    self      . setVerticalHeaderLabels   ( VLabels                          )
    ##########################################################################
    return
  ############################################################################
  def Prepare          ( self                                              ) :
    ##########################################################################
    self . setPrepared ( True                                                )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  @pyqtSlot                         (                                        )
  def refresh                       ( self                                 ) :
    ##########################################################################
    XLINE  =                        {                                        }
    YLINE  =                        {                                        }
    ##########################################################################
    for   x in range                ( 0 , self . Columns                   ) :
      ########################################################################
      XLINE [ x ] = 0
    ##########################################################################
    for   y in range                ( 0 , self . Rows                      ) :
      ########################################################################
      YLINE [ y ] = 0
    ##########################################################################
    for   x in range                ( 0 , self . Columns + 1               ) :
      for y in range                ( 0 , self . Rows    + 1               ) :
        ######################################################################
        BALL     = int              ( ( y * self . Columns ) + x + 1 )
        ITEM     = QTableWidgetItem (                                        )
        ITEM     . setTextAlignment ( Qt . AlignRight | Qt . AlignVCenter    )
        ######################################################################
        if ( ( x < self . Columns ) and ( y < self . Rows )                ) :
          ####################################################################
          if                        ( BALL < 50                            ) :
            ##################################################################
            ITEM . setData          ( Qt . UserRole , 1                      )
            ITEM . setFlags         ( Qt . ItemIsSelectable                | \
                                      Qt . ItemIsEnabled                     )
            ITEM . setForeground    ( QBrush ( QColor ( 0 , 0 , 255 ) )      )
            ##################################################################
            if                      ( BALL in self . Pickings              ) :
              ################################################################
              ITEM . setText        ( str ( BALL )                           )
              ################################################################
              XLINE [ x ] = XLINE [ x ] + 1
              YLINE [ y ] = YLINE [ y ] + 1
            ##################################################################
          else                                                               :
            ##################################################################
            ITEM . setData          ( Qt . UserRole , 0                      )
            ITEM . setFlags         ( Qt . NoItemFlags                       )
          ####################################################################
        else                                                                 :
          ####################################################################
          ITEM   . setData          ( Qt . UserRole , 2                      )
          ITEM   . setFlags         ( Qt . NoItemFlags                       )
        ######################################################################
        self     . setItem          ( y , x , ITEM                           )
    ##########################################################################
    for   x in range                ( 0 , self . Columns                   ) :
      ########################################################################
      ITEM = self . item            ( self . Rows , x                        )
      ITEM . setText                ( str ( XLINE [ x ] )                    )
    ##########################################################################
    for   y in range                ( 0 , self . Rows                      ) :
      ########################################################################
      ITEM = self . item            ( y , self . Columns                     )
      ITEM . setText                ( str ( YLINE [ y ] )                    )
    ##########################################################################
    ITEM   = self . item            ( self . Rows , self . Columns           )
    ITEM   . setText                ( str ( len ( self . Pickings ) )        )
    ITEM   . setData                ( Qt . UserRole , 3                      )
    ITEM   . setFlags               ( Qt . ItemIsSelectable                | \
                                      Qt . ItemIsEditable                  | \
                                      Qt . ItemIsEnabled                     )
    ITEM   . setForeground          ( QBrush ( QColor ( 0 , 128 , 0 ) )      )
    ##########################################################################
    self . resizeColumnsToContents  (                                        )
    ##########################################################################
    return
  ############################################################################
  def LoadPickings                  ( self , DB                            ) :
    ##########################################################################
    SERIAL          = self . Serial
    self . Pickings =               [                                        ]
    ##########################################################################
    ITEMs           =               [                                        ]
    ##########################################################################
    for i in range                  ( 1 , 50                               ) :
      ########################################################################
      if                            ( i < 10                               ) :
        NN          = f"`n0{i}`"
      else                                                                   :
        NN          = f"`n{i}`"
      ########################################################################
      ITEMs         . append        ( NN                                     )
    ##########################################################################
    ITEMX           = " , " . join  ( ITEMs                                  )
    QQ              = f"""select {ITEMX} from `predictions`.`tbl-pickings`
                          where ( `serial` = '{SERIAL}' ) ;"""
    QQ              = " " . join    ( QQ . split ( )                         )
    DB              . Query         ( QQ                                     )
    ALLs            = DB . FetchAll (                                        )
    ##########################################################################
    if                              ( self . NotOkay ( ALLs )              ) :
      return
    ##########################################################################
    if                              ( len ( ALLs       ) != 1              ) :
      return
    ##########################################################################
    if                              ( len ( ALLs [ 0 ] ) != 49             ) :
      return
    ##########################################################################
    ALL             = ALLs          [ 0                                      ]
    BALLs           =               [                                        ]
    ##########################################################################
    for i in range                  ( 0 , 49                               ) :
      ########################################################################
      try                                                                    :
        ######################################################################
        BALL        = int           ( i + 1                                  )
        BV          = int           ( ALL [ i ]                              )
        if                          ( BV > 0                               ) :
          BALLs     . append        ( BALL                                   )
        ######################################################################
      except                                                                 :
        pass
    ##########################################################################
    self . Pickings = BALLs
    ##########################################################################
    return
  ############################################################################
  def loading                  ( self                                      ) :
    ##########################################################################
    TRX  = self . Translations
    ##########################################################################
    msg  = TRX                 [ "UI::Loading"                               ]
    self . TtsTalk             ( msg , self . getLocality ( )                )
    ##########################################################################
    msg  = TRX [ "TBL" ] [ "Predictions" ] [ "Loading"                       ]
    self . ShowStatus          ( msg                                         )
    ##########################################################################
    DB   = self . ConnectDB    (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return
    ##########################################################################
    self . Notify              ( 3                                           )
    self . OnBusy  . emit      (                                             )
    self . setBustle           (                                             )
    ##########################################################################
    FMT  = self . Translations [ "UI::StartLoading"                          ]
    MSG  = FMT . format        ( self . windowTitle ( )                      )
    self . ShowStatus          ( MSG                                         )
    ##########################################################################
    self . LoadPickings        ( DB                                          )
    ##########################################################################
    self . setVacancy          (                                             )
    self . GoRelax . emit      (                                             )
    self . ShowStatus          ( ""                                          )
    DB   . Close               (                                             )
    ##########################################################################
    self . emitBalls . emit    (                                             )
    self . ShowStatus          ( ""                                          )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  @pyqtSlot                (                                                 )
  def startup              ( self , SERIAL                                 ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      self . Prepare       (                                                 )
    ##########################################################################
    self . Serial = SERIAL
    ##########################################################################
    Title = self . Translations [ "TBL" ] [ "Predictions" ] [ "Title"        ]
    MSG   = f"{Title} : {SERIAL}"
    self  . setWindowTitle ( MSG                                             )
    ##########################################################################
    self  . setColumnCount ( self . Columns + 1                              )
    self  . setRowCount    ( self . Rows    + 1                              )
    self  . setLabels      (                                                 )
    ##########################################################################
    self  . Go             ( self . loading                                  )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
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
    ITEM = self . itemAt ( pos )
    if ( self . IsOkay ( ITEM ) ) :
      print(ITEM.text())
    """
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
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    """
    ##########################################################################
    return True
##############################################################################
