# -*- coding: utf-8 -*-
##############################################################################
## ProgressManager
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
from   opencc                          import OpenCC
from   googletrans                     import Translator
##############################################################################
from   PyQt5                           import QtCore
from   PyQt5                           import QtGui
from   PyQt5                           import QtWidgets
##############################################################################
from   PyQt5 . QtCore                  import QObject
from   PyQt5 . QtCore                  import pyqtSignal
from   PyQt5 . QtCore                  import pyqtSlot
from   PyQt5 . QtCore                  import Qt
from   PyQt5 . QtCore                  import QPoint
from   PyQt5 . QtCore                  import QPointF
from   PyQt5 . QtCore                  import QSize
from   PyQt5 . QtCore                  import QTimer
from   PyQt5 . QtCore                  import QMutex
from   PyQt5 . QtCore                  import QMutexLocker
from   PyQt5 . QtCore                  import QDateTime
##############################################################################
from   PyQt5 . QtGui                   import QIcon
from   PyQt5 . QtGui                   import QCursor
from   PyQt5 . QtGui                   import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets               import QApplication
from   PyQt5 . QtWidgets               import QWidget
from   PyQt5 . QtWidgets               import qApp
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAction
from   PyQt5 . QtWidgets               import QShortcut
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAbstractItemView
from   PyQt5 . QtWidgets               import QTreeWidget
from   PyQt5 . QtWidgets               import QTreeWidgetItem
from   PyQt5 . QtWidgets               import QLineEdit
from   PyQt5 . QtWidgets               import QComboBox
from   PyQt5 . QtWidgets               import QSpinBox
from   PyQt5 . QtWidgets               import QProgressBar
from   PyQt5 . QtWidgets               import QToolButton
##############################################################################
from   AITK  . Qt        . VirtualGui  import VirtualGui  as VirtualGui
from   AITK  . Qt        . MenuManager import MenuManager as MenuManager
from   AITK  . Qt        . TreeWidget  import TreeWidget  as TreeWidget
from   AITK  . Qt        . TreeDock    import TreeDock    as TreeDock
##############################################################################
class ProgressManager           ( TreeDock                                 ) :
  ############################################################################
  HavingMenu       = 1371434312
  AutoCleanId      = 1212001160
  RunningId        = 1212001161
  FittingId        = 1212001164
  TimerPeriodId    = 1212001271
  TimeoutId        = 1212001301
  ############################################################################
  Requesting       = pyqtSignal (                                            )
  LocalRequest     = pyqtSignal (                                            )
  EmitTimer        = pyqtSignal (                                            )
  Hidden           = pyqtSignal ( QWidget                                    )
  ############################################################################
  def __init__                  ( self , parent = None , plan = None       ) :
    ##########################################################################
    super ( ) . __init__        ( parent , plan                              )
    ##########################################################################
    self . dockingOrientation = Qt . Horizontal
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea
    ##########################################################################
    self . setDragEnabled               ( False                              )
    self . setAcceptDrops               ( False                              )
    self . setDragDropMode              ( QAbstractItemView . NoDragDrop     )
    ##########################################################################
    self . setFunction                  ( self . FunctionDocking , False     )
    self . setFunction                  ( self . HavingMenu      , True      )
    self . setFunction                  ( self . TimeoutId       , False     )
    self . setFunction                  ( 212001302              , False     )
    ##########################################################################
    self . setColumnCount               ( 7                                  )
    self . setRootIsDecorated           ( False                              )
    self . setAlternatingRowColors      ( True                               )
    self . setHorizontalScrollBarPolicy ( Qt . ScrollBarAsNeeded             )
    self . setVerticalScrollBarPolicy   ( Qt . ScrollBarAsNeeded             )
    ##########################################################################
    self . MountClicked                 ( 1                                  )
    self . MountClicked                 ( 2                                  )
    ##########################################################################
    self . assignSelectionMode          ( "ContiguousSelection"              )
    self . setAccessibleName            ( "ProgressManager"                  )
    ##########################################################################
    self . Requesting   . connect       ( self . Accepting                   )
    self . LocalRequest . connect       ( self . LocalAccept                 )
    self . EmitTimer    . connect       ( self . EnsureTimer                 )
    ##########################################################################
    self . setLimitValue                ( self . AutoCleanId   ,   1         )
    self . setLimitValue                ( self . RunningId     ,   0         )
    self . setLimitValue                ( 1212001162           ,   0         )
    self . setLimitValue                ( 1212001163           ,   0         )
    self . setLimitValue                ( self . FittingId     ,   0         )
    self . setLimitValue                ( self . TimerPeriodId , 125         )
    ##########################################################################
    self . Items         =              {                                    }
    self . Buttons       =              {                                    }
    self . Progress      =              {                                    }
    self . Booleans      =              {                                    }
    self . Values        =              {                                    }
    self . Begins        =              {                                    }
    self . Final         =              {                                    }
    ##########################################################################
    self . Stoppings     =              [                                    ]
    self . EnableButtons =              [                                    ]
    ##########################################################################
    self . Connects      =              {                                    }
    self . Message       =              {                                    }
    self . Formats       =              {                                    }
    self . FREQs         =              {                                    }
    self . FREQr         =              {                                    }
    ##########################################################################
    self . StartAt       =              {                                    }
    self . Maximum       =              {                                    }
    self . Minimum       =              { -1 : 0                             }
    ##########################################################################
    self . Queues        =              [                                    ]
    self . QueueMutex    = QMutex       (                                    )
    self . IdMutex       = QMutex       (                                    )
    ##########################################################################
    self . PassDragDrop  = False
    self . Id            = 0
    self . Fitting       = False
    self . Timer         = None
    self . ConfScope     = "ProgressManager"
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 1024 , 240 )                      )
  ############################################################################
  def DockLocationChanged      ( self , area                               ) :
    ##########################################################################
    s      = self . ConfScope
    ##########################################################################
    if                         ( s      not in self . Settings             ) :
      self . Settings [ s ] =  {                                             }
    ##########################################################################
    if                         ( "Dock" not in self . Settings [ s ]       ) :
      self . Settings [ s ] [ "Dock" ] =  {                                  }
    ##########################################################################
    self   . dockingPlace = area
    self   . Store             ( area                                        )
    ##########################################################################
    return
  ############################################################################
  def singleClicked            ( self , item , column                      ) :
    ##########################################################################
    self     . Notify          ( 0                                           )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    return
  ############################################################################
  def toETA                             ( self , START , V , MAX           ) :
    ##########################################################################
    if                                  ( V <= 0                           ) :
      return START
    ##########################################################################
    CTX   = QDateTime . currentDateTime (                                    )
    DTX   = START . msecsTo             ( CTX                                )
    ##########################################################################
    MTS   = int                         ( DTX * MAX / V                      )
    ##########################################################################
    return START . addMSecs             ( MTS                                )
  ############################################################################
  def Relocation               ( self                                      ) :
    ##########################################################################
    if                         ( not self . isPrepared ( )                 ) :
      return False
    ##########################################################################
    self . StoreSettings       ( self . ConfScope                            )
    self . Store               ( self . dockingPlace                         )
    ##########################################################################
    return False
  ############################################################################
  @pyqtSlot                    (                                             )
  def Accepting                ( self                                      ) :
    ##########################################################################
    self . LocalRequest . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                            (                                     )
  def EnsureTimer                      ( self                              ) :
    ##########################################################################
    if                                 ( self . Timer == None              ) :
      self . Timer = QTimer            ( self                                )
      self . Timer . timeout . connect ( self . Update                       )
    ##########################################################################
    if                                 ( self . Timer . isActive ( )       ) :
      return
    ##########################################################################
    PERIOD = self  . LimitValue        ( self . TimerPeriodId                )
    self   . Timer . start             ( PERIOD                              )
    ##########################################################################
    return
  ############################################################################
  def StartFlush            ( self                                         ) :
    ##########################################################################
    self . EmitTimer . emit (                                                )
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
    self   . setLocalMessage     ( 441212001           , "{0}.{1} t/s"       )
    self   . setLocalMessage     ( 441212002           , "{0}.{1} s/t"       )
    ##########################################################################
    icon   = QIcon               ( ":/images/yes.png"                        )
    self   . setLocalIcon        ( "Yes"  , icon                             )
    ##########################################################################
    icon   = QIcon               ( ":/images/StopPlay.png"                   )
    self   . setLocalIcon        ( "Stop" , icon                             )
    ##########################################################################
    s      = self . ConfScope
    ##########################################################################
    if                           ( s      in self . Settings               ) :
      if                         ( "Dock" in self . Settings [ s ]         ) :
        if                       ( "Area" in self . Settings [ s ]["Dock"] ) :
          self . dockingPlace = self . Settings [ s ] [ "Dock" ] [ "Area"    ]
    ##########################################################################
    return
  ############################################################################
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . setColumnWidth      ( 0 ,   3                                     )
    self . setColumnWidth      ( 1 , 200                                     )
    self . setColumnWidth      ( 2 , 200                                     )
    self . setColumnWidth      ( 3 , 200                                     )
    self . setColumnWidth      ( 4 , 200                                     )
    self . setColumnWidth      ( 5 , 240                                     )
    ##########################################################################
    TRX  = self . Translations [ "ProgressManager"                           ]
    self . setCentralLabels    ( TRX [ "Labels" ]                            )
    ##########################################################################
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def DismantleTimer   ( self                                              ) :
    ##########################################################################
    if                 ( self . Timer == None                              ) :
      return
    ##########################################################################
    E    = self . Timer
    self . Timer = None
    ##########################################################################
    E    . stop        (                                                     )
    E    . deleteLater (                                                     )
    ##########################################################################
    return
  ############################################################################
  def Shutdown                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return False
    ##########################################################################
    self . Leave . emit          ( self                                      )
    ##########################################################################
    self . setPrepared           ( False                                     )
    self . DismantleTimer        (                                           )
    ##########################################################################
    return True
  ############################################################################
  @pyqtSlot                      (                                           )
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . GetSettings         ( "ProgressManager"                         )
    self   . show                (                                           )
    self   . StartFlush          (                                           )
    ##########################################################################
    return
  ############################################################################
  def GetSettings                 ( self , scope                           ) :
    ##########################################################################
    if                            ( scope not in self . Settings           ) :
      self   . ObtainWidths       (                                          )
      return
    ##########################################################################
    if                            ( "Fitting" in self . Settings [ scope ] ) :
      self   . Fitting = self . Settings [ scope ] [ "Fitting"               ]
    ##########################################################################
    if                            ( "Clean"   in self . Settings [ scope ] ) :
      ac     = self . Settings    [ scope ] [ "Clean"                        ]
      if                          ( ac                                     ) :
        self . setLimitValue      ( self . AutoCleanId , 1                   )
      else                                                                   :
        self . setLimitValue      ( self . AutoCleanId , 0                   )
    ##########################################################################
    W        = self . width       (                                          )
    H        = self . height      (                                          )
    ##########################################################################
    if                            ( "Width"   in self . Settings [ scope ] ) :
      W      = self . Settings    [ scope ] [ "Width"                        ]
    ##########################################################################
    if                            ( "Height"  in self . Settings [ scope ] ) :
      H      = self . Settings    [ scope ] [ "Height"                       ]
    ##########################################################################
    self     . setSuggestion      ( QSize ( W , H )                          )
    ##########################################################################
    self     . ObtainWidths       (                                          )
    if                            ( "Widths"  in self . Settings [ scope ] ) :
      self   . WIDTHs = self . Settings [ scope ] [ "Widths"                 ]
    ##########################################################################
    if                            ( not self . Fitting                     ) :
      self   . setLimitValue      ( self . FittingId , 1                     )
    ##########################################################################
    return
  ############################################################################
  def StoreSettings               ( self , scope                           ) :
    ##########################################################################
    if                            ( scope not in self . Settings           ) :
      self . Settings [ scope ] = {                                          }
    ##########################################################################
    self   . ObtainWidths         (                                          )
    ##########################################################################
    ac        = ( self . LimitValue ( self . AutoCleanId ) > 0               )
    self . Settings [ scope ] [ "Fitting" ] = self . Fitting
    self . Settings [ scope ] [ "Clean"   ] = ac
    self . Settings [ scope ] [ "Width"   ] = self . width  (                )
    self . Settings [ scope ] [ "Height"  ] = self . height (                )
    self . Settings [ scope ] [ "Widths"  ] = self . WIDTHs
    ##########################################################################
    return
  ############################################################################
  def LoadDockingSettings  ( self                                          ) :
    ##########################################################################
    s = self . ConfScope
    ##########################################################################
    if                     ( s      not in self . Settings                 ) :
      return               {                                                 }
    ##########################################################################
    if                     ( "Dock" not in self . Settings [ s ]           ) :
      return               {                                                 }
    ##########################################################################
    return self . Settings [ s ] [ "Dock"                                    ]
  ############################################################################
  def SaveDockingSettings      ( self , JSON                               ) :
    ##########################################################################
    s      = self . ConfScope
    ##########################################################################
    if                         ( s      not in self . Settings             ) :
      self . Settings [ s ] =  {                                             }
    ##########################################################################
    self . Settings [ s ] [ "Dock" ] = JSON
    ##########################################################################
    return
  ############################################################################
  def Report                              ( self , k                       ) :
    ##########################################################################
    if                                    ( k < 0                          ) :
      return
    ##########################################################################
    E       = QDateTime . currentDateTime (                                  )
    S       = self . Begins               [ k                                ]
    SAT     = self . StartAt              [ k                                ]
    MIN     = self . Minimum              [ k                                ]
    MAX     = self . Maximum              [ k                                ]
    CHECKED = True
    ##########################################################################
    if                                    ( k in self . Values             ) :
      V     = self . Values               [ k                                ]
    else                                                                     :
      V     = self . Final                [ k                                ]
    ##########################################################################
    if                                    ( k in self . Progress           ) :
      ########################################################################
      bar   = self . Progress             [ k                                ]
      bar   . setFormat                   ( self . Formats [ k ]             )
      ########################################################################
      if                                  ( MAX >= MIN                     ) :
        bar . setRange                    ( MIN , MAX                        )
      ########################################################################
      if                                  ( ( V >= MIN ) and ( V <= MAX )  ) :
        bar . setValue                    ( V                                )
    ##########################################################################
    V       = V   - SAT
    MAX     = MAX - SAT
    ##########################################################################
    if ( ( MAX >= MIN ) and ( MAX > 0 ) and ( MAX >= V ) )                   :
      ########################################################################
      E     = self . toETA                ( S , V , MAX                      )
      ########################################################################
      if                                  ( k in self . Items              ) :
        ######################################################################
        it  = self . Items                [ k                                ]
        Z   = E . toString                ( "yyyy/MM/dd hh:mm:ss"            )
        it  . setText                     ( 3 , Z                            )
      ########################################################################
      DS    = S . msecsTo                 ( QDateTime . currentDateTime ( )  )
      ########################################################################
      if ( ( V <= 0 ) or ( MAX <= 0 ) or ( DS <= 0 ) )                       :
        ######################################################################
        it  = self . Items                [ k                                ]
        it  . setText                     ( 3 , "\u221E"                     )
        it  . setText                     ( 4 , "\u05D0"                     )
        ######################################################################
      else                                                                   :
        ######################################################################
        VC  = int                         ( V * 1000                         )
        ######################################################################
        if                                ( VC > DS                        ) :
          ####################################################################
          RX   = float                    ( float ( VC ) / float ( DS )      )
          RT   = int                      ( RX                               )
          RV   = int                      ( int ( RX * 1000 ) % 1000         )
          RZ   = f"{RV}"
          RZ   = RZ . zfill               ( 3                                )
          TMX  = f"{RT}.{RZ}"
          FMT  = self . FREQs             [ k                                ]
          TMS  = FMT  . format            ( TMX                              )
          self . Items [ k ] . setText    ( 4 , TMS                          )
          ####################################################################
        else                                                                 :
          ####################################################################
          RX   = float                    ( float ( DS ) / float ( VC )      )
          RT   = int                      ( RX                               )
          RV   = int                      ( int ( RX * 1000 ) % 1000         )
          RZ   = f"{RV}"
          RZ   = RZ . zfill               ( 3                                )
          TMX  = f"{RT}.{RZ}"
          FMT  = self . FREQr             [ k                                ]
          TMS  = FMT  . format            ( TMX                              )
          self . Items [ k ] . setText    ( 4 , TMS                          )
      ########################################################################
    else                                                                     :
      ########################################################################
      if                                  ( k in self . Items              ) :
        ######################################################################
        item = self . Items               [ k                                ]
        item . setText                    ( 3 , "\u221E"                     )
        item . setText                    ( 4 , "\u05D0"                     )
    ##########################################################################
    if                                    ( k in self . Buttons            ) :
      CHECKED = self . Buttons [ k ] . isChecked (                           )
    ##########################################################################
    if                                    ( not CHECKED                    ) :
      ########################################################################
      if                                  ( k in self . Booleans           ) :
        self . Booleans [ k ] = False
      ########################################################################
      if                                  ( k in self . Buttons            ) :
        self . Buttons  [ k ] . setEnabled ( False                           )
    ##########################################################################
    if                                    ( k in self . Items              ) :
      ########################################################################
      item  = self . Items                [ k                                ]
      Z     = S    . toString             ( "yyyy/MM/dd hh:mm:ss"            )
      item  . setText                     ( 1 , self . Connects [ k ]        )
      item  . setText                     ( 2 , Z                            )
      item  . setText                     ( 5 , self . Message  [ k ]        )
    ##########################################################################
    return
  ############################################################################
  def RunningCounts                 ( self                                 ) :
    ##########################################################################
    COUNT     = 0
    ##########################################################################
    self      . LockGui             (                                        )
    ##########################################################################
    for i in range                  ( 0 , self . topLevelItemCount ( )     ) :
      ########################################################################
      IT      = self . topLevelItem ( i                                      )
      vid     = int                 ( IT . data ( 0 , Qt . UserRole )        )
      if                            ( vid == 1                             ) :
        COUNT = COUNT + 1
    ##########################################################################
    self      . UnlockGui           (                                        )
    ##########################################################################
    return COUNT
  ############################################################################
  def reportTasks                ( self                                    ) :
    ##########################################################################
    COUNT = self . RunningCounts (                                           )
    ##########################################################################
    if                           ( COUNT > 0                               ) :
      FMT = self . getMenuItem   ( "Operations"                              )
      msg = FMT  . format        ( COUNT                                     )
    else                                                                     :
      msg = self . Translations  [ "ProgressManager" ] [ "Title"             ]
    ##########################################################################
    self  . setWindowTitle       ( msg                                       )
    self  . setToolTip           ( msg                                       )
    ##########################################################################
    PW    = self . parentWidget  (                                           )
    if                           ( PW in [ False , None ]                  ) :
      return
    ##########################################################################
    PW    . setWindowTitle       ( msg                                       )
    ##########################################################################
    return
  ############################################################################
  def Update                     ( self                                    ) :
    ##########################################################################
    rid     = self . LimitValue  ( self . RunningId                          )
    if                           ( rid > 0                                 ) :
      return
    ##########################################################################
    if                           ( self . LimitValue ( 1212001162 ) > 0    ) :
      return
    ##########################################################################
    v       = self . LimitValue  ( self . FittingId                          )
    if                           ( v > 0                                   ) :
      self  . setLimitValue      ( self . FittingId , 0                      )
      self  . setWidths          (                                           )
    ##########################################################################
    rid     = rid + 1
    self    . setLimitValue      ( self . RunningId , rid                    )
    ##########################################################################
    while                        ( len ( self . Stoppings ) > 0            ) :
      idx   = self . Stoppings   [ 0                                         ]
      if                         ( self . End ( idx )                      ) :
        del self . Stoppings     [ 0                                         ]
      qApp  . processEvents      (                                           )
    ##########################################################################
    while                        ( len ( self . EnableButtons ) > 0        ) :
      idx   = self . EnableButtons [ 0                                       ]
      del self . EnableButtons   [ 0                                         ]
      if                         ( idx in self . Buttons                   ) :
        self . Buttons [ idx ] . setEnabled ( True                           )
        self . Buttons [ idx ] . setChecked ( True                           )
      qApp  . processEvents      (                                           )
    ##########################################################################
    self    . LockGui            (                                           )
    ##########################################################################
    KEYs    = self . Booleans . keys (                                       )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      u     = False
      ########################################################################
      if                         ( K in self . Booleans                    ) :
        ######################################################################
        u   = self . Booleans    [ K                                         ]
        if u                                                                 :
          self . Report          ( K                                         )
          self . skip            ( 2                                         )
    ##########################################################################
    ZE      = self . Minimum     [ -1                                        ]
    ZE      = ZE + 1
    self    . Minimum [ -1 ] = ZE
    self    . UnlockGui          (                                           )
    ##########################################################################
    self    . LocalAccept        (                                           )
    ##########################################################################
    if ( ( int ( self . Minimum [ -1 ] % 10 ) ) == 0 )                       :
      ########################################################################
      self . Minimum [ -1 ] = 0
      self . Clean               (                                           )
      ########################################################################
      if                         ( self . Fitting                          ) :
        self . AutoFit           (                                           )
    ##########################################################################
    v      = self .LimitValue    ( self . RunningId                          )
    v      = v - 1
    self   . setLimitValue       ( self . RunningId , v                      )
    ##########################################################################
    return
  ############################################################################
  def assignAccepting                ( self , Id , Name , Format           ) :
    ##########################################################################
    self    . LockGui                (                                       )
    ##########################################################################
    fnt     = self . font            (                                       )
    icon    = self . getLocalIcon    ( "Stop"                                )
    item    = QTreeWidgetItem        (                                       )
    bar     = QProgressBar           (                                       )
    button  = QToolButton            (                                       )
    ##########################################################################
    for i in range                   ( 0 , self . columnCount ( )          ) :
      item  . setFont                ( i , fnt                               )
    ##########################################################################
    bar     . setFormat              ( Format                                )
    bar     . setFont                ( fnt                                   )
    ##########################################################################
    button  . setFont                ( fnt                                   )
    button  . setEnabled             ( False                                 )
    button  . setIcon                ( icon                                  )
    button  . setCheckable           ( True                                  )
    button  . setChecked             ( False                                 )
    ##########################################################################
    item    . setText                ( 1    , Name                           )
    item    . setData                ( 0    , Qt . UserRole , 0              )
    ##########################################################################
    self    . insertTopLevelItem     ( 0    , item                           )
    self    . setItemWidget          ( item , 0 , button                     )
    self    . setItemWidget          ( item , 6 , bar                        )
    ##########################################################################
    self    . Items    [ Id ] = item
    self    . Buttons  [ Id ] = button
    self    . Progress [ Id ] = bar
    self    . Connects [ Id ] = Name
    self    . Message  [ Id ] = Name
    self    . Formats  [ Id ] = Format
    ##########################################################################
    msg     = self . getLocalMessage ( 441212001                             )
    self    . FREQs    [ Id ] = msg
    ##########################################################################
    msg     = self . getLocalMessage ( 441212002                             )
    self    . FREQr    [ Id ] = msg
    ##########################################################################
    self    . UnlockGui              (                                       )
    self    . reportTasks            (                                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (                                          )
  def LocalAccept                 ( self                                   ) :
    ##########################################################################
    if                            ( self . LimitValue ( 1212001162 ) > 0   ) :
      return
    ##########################################################################
    V        = self . LimitValues [ 1212001162                               ]
    V        = V + 1
    self     . LimitValues [ 1212001162 ] = V
    ##########################################################################
    L        = QMutexLocker       ( self . QueueMutex                        )
    ##########################################################################
    while                         ( len ( self . Queues ) > 0              ) :
      ########################################################################
      JSON   = self   . Queues    [ 0                                        ]
      self   . Queues . pop       ( 0                                        )
      ########################################################################
      ID     = JSON               [ "ID"                                     ]
      NAME   = JSON               [ "Name"                                   ]
      FORMAT = JSON               [ "Format"                                 ]
      self   . assignAccepting    ( ID , NAME , FORMAT                       )
      ########################################################################
      qApp   . processEvents      (                                          )
    ##########################################################################
    V        = self . LimitValues [ 1212001162                               ]
    V        = V - 1
    self     . LimitValues [ 1212001162 ] = V
    ##########################################################################
    return
  ############################################################################
  def Request               ( self , Name , Format                         ) :
    ##########################################################################
    ID   = self . Id
    ##########################################################################
    self . IdMutex . lock   (                                                )
    ##########################################################################
    self . Id = self . Id + 1
    JSON =                  { "ID"     : ID                                , \
                              "Name"   : Name                              , \
                              "Format" : Format                              }
    self . Queues  . append ( JSON                                           )
    ##########################################################################
    self . IdMutex . unlock (                                                )
    ##########################################################################
    return ID
  ############################################################################
  def setName        ( self , Id , Name                                    ) :
    ##########################################################################
    self . LockGui   (                                                       )
    self . Connects  [ Id ] = Name
    self . UnlockGui (                                                       )
    ##########################################################################
    return
  ############################################################################
  def setValue       ( self , Id , Value                                   ) :
    ##########################################################################
    self . Values [ Id ] = Value
    ##########################################################################
    return
  ############################################################################
  def isRunning            ( self , Id                                     ) :
    ##########################################################################
    if                     ( Id not in self . Booleans                     ) :
      return False
    ##########################################################################
    return self . Booleans [        Id                                       ]
  ############################################################################
  def setRange       ( self , Id , Min , Max                               ) :
    ##########################################################################
    if               ( Min >= Max                                          ) :
      return
    ##########################################################################
    self . LockGui   (                                                       )
    ##########################################################################
    self . Final     [ Id ] = 0
    self . Minimum   [ Id ] = Min
    self . Maximum   [ Id ] = Max
    ##########################################################################
    self . UnlockGui (                                                       )
    ##########################################################################
    return
  ############################################################################
  def setMessage     ( self , Id , message                                 ) :
    ##########################################################################
    self . LockGui   (                                                       )
    self . Message   [ Id ] = message
    self . UnlockGui (                                                       )
    ##########################################################################
    return
  ############################################################################
  def setFormat      ( self , Id , Format                                  ) :
    ##########################################################################
    self . LockGui   (                                                       )
    self . Formats   [ Id ] = Format
    self . UnlockGui (                                                       )
    ##########################################################################
    return
  ############################################################################
  def setFrequency   ( self , Id , cFmt , rFmt                             ) :
    ##########################################################################
    self . LockGui   (                                                       )
    ##########################################################################
    self . FREQs     [ Id ] = cFmt
    self . FREQr     [ Id ] = rFmt
    ##########################################################################
    self . UnlockGui (                                                       )
    ##########################################################################
    return
  ############################################################################
  def isReady ( self , Id                                                  ) :
    return    ( Id in self . Items                                           )
  ############################################################################
  def WaitForReady ( self , Id , msecs                                     ) :
    ##########################################################################
    S     = QDateTime . currentDateTime (                                    )
    tout  = False
    ##########################################################################
    while          ( ( not self . isReady ( Id ) ) and ( not tout )        ) :
      ########################################################################
      if           ( self . isFunction ( self . TimeoutId )                ) :
        ######################################################################
        E = QDateTime . currentDateTime (                                    )
        if         ( S . msecsTo ( E ) > msecs                             ) :
          ####################################################################
          tout = True
          ####################################################################
          return False
      ########################################################################
      time . sleep         ( 0.002                                           )
      qApp . processEvents (                                                 )
    ##########################################################################
    return True
  ############################################################################
  def Start                        ( self , Id , value , running           ) :
    ##########################################################################
    if                             ( not self . WaitForReady ( Id , 1000 ) ) :
      return
    ##########################################################################
    self   . EnableButtons . append ( Id                                     )
    self   . Values   [ Id ] = value
    self   . Booleans [ Id ] = running
    self   . StartAt  [ Id ] = value
    self   . Begins   [ Id ] = QDateTime . currentDateTime (                 )
    self   . Final    [ Id ] = 0
    ##########################################################################
    if                              ( Id not in self . Minimum             ) :
      self . Minimum [ Id ] = 0
    ##########################################################################
    if                              ( Id not in self . Maximum             ) :
      self . Maximum [ Id ] = 100
    ##########################################################################
    self   . Items   [ Id ] . setData    ( 0 , Qt . UserRole , 1             )
    ##########################################################################
    E      = QDateTime . currentDateTime (                                   )
    Z      = E . toString                ( "yyyy/MM/dd hh:mm:ss"             )
    self   . Items   [ Id ] . setText    ( 2 , Z                             )
    ##########################################################################
    return
  ############################################################################
  def Finish                       ( self , Id                             ) :
    ##########################################################################
    if                             ( not self . WaitForReady ( Id , 1000 ) ) :
      return
    ##########################################################################
    self . LockGui                 (                                         )
    ##########################################################################
    if                             ( Id in self . Final                    ) :
      if                           ( Id in self . Values                   ) :
        V    = self . Values       [ Id                                      ]
        self . Final [ Id ] = V
        del self . Values          [ Id                                      ]
    ##########################################################################
    self . UnlockGui               (                                         )
    self . Stoppings . append      ( Id                                      )
    ##########################################################################
    return
  ############################################################################
  def End                                  ( self , Id                     ) :
    ##########################################################################
    if                                     ( Id not in self . Booleans     ) :
      return False
    ##########################################################################
    self     . LockGui                     (                                 )
    ##########################################################################
    item     = None
    bar      = None
    tb       = None
    Now      = QDateTime . currentDateTime (                                 )
    ##########################################################################
    if                                     ( Id in self . Items            ) :
      item   = self . Items                [ Id                              ]
    ##########################################################################
    if                                     ( Id in self . Progress         ) :
      bar    = self . Progress             [ Id                              ]
    ##########################################################################
    if                                     ( Id in self . Buttons          ) :
      tb     = self . Buttons              [ Id                              ]
    ##########################################################################
    if                                     ( bar  is not None              ) :
      bar    . setValue                    ( self . Final [ Id ]             )
    ##########################################################################
    if                                     ( tb   is not None              ) :
      tb     . setEnabled                  ( False                           )
    ##########################################################################
    if                                     ( item is not None              ) :
      MSG    = Now . toString              ( "yyyy/MM/dd hh:mm:ss"           )
      item   . setData                     ( 0 , Qt . UserRole , 2           )
      item   . setText                     ( 3 , MSG                         )
    ##########################################################################
    del self . Buttons                     [ Id                              ]
    self     . Report                      ( Id                              )
    del self . Booleans                    [ Id                              ]
    ##########################################################################
    if                                     ( item is not None              ) :
      ########################################################################
      icon   = self . getLocalIcon         ( "Yes"                           )
      self   . removeItemWidget            ( item , 0                        )
      item   . setIcon                     ( 0    , icon                     )
    ##########################################################################
    self     . UnlockGui                   (                                 )
    ##########################################################################
    return True
  ############################################################################
  def CleanUpUnusedItems             ( self                                ) :
    ##########################################################################
    ITs        =                     [                                       ]
    ##########################################################################
    for i in range                   ( 0 , self . topLevelItemCount ( )    ) :
      ########################################################################
      IT       = self . topLevelItem ( i                                     )
      ITs      . append              ( IT                                    )
    ##########################################################################
    for IT in ITs                                                            :
      ########################################################################
      Id       = int                 ( IT . data ( 0 , Qt . UserRole )       )
      if                             ( Id == 2                             ) :
        index  = self . indexOfTopLevelItem ( IT                             )
        if                           ( index >= 0                          ) :
          self . takeTopLevelItem    ( index                                 )
    ##########################################################################
    return
  ############################################################################
  def Clean                ( self                                          ) :
    ##########################################################################
    cleanup     = False
    ##########################################################################
    if                     ( self . LimitValue ( 212001162          ) <= 0 ) :
      if                   ( self . LimitValue ( self . AutoCleanId ) >  0 ) :
        cleanup = True
    ##########################################################################
    if                     ( self . LimitValue ( 212001163          ) >  0 ) :
      self      . setLimitValue      ( 212001163 , 0                         )
      cleanup   = True
    ##########################################################################
    if                               ( self . topLevelItemCount ( ) <= 0   ) :
      cleanup   = False
    ##########################################################################
    if                               ( cleanup                             ) :
      self      . CleanUpUnusedItems (                                       )
    ##########################################################################
    self        . reportTasks        (                                       )
    ##########################################################################
    return
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    doTOut = self . isFunction      ( self . TimeoutId                       )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    AC     = self . LimitValue      ( self . AutoCleanId                     )
    AC     =                        ( AC > 0                                 )
    items  = self . selectedItems   (                                        )
    atItem = self . currentItem     (                                        )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                              ( not doTOut                           ) :
      msg  = TRX                    [ "UI::Hide"                             ]
      mm   . addAction              ( 201 , msg                              )
      mm   . addSeparator           (                                        )
    ##########################################################################
    msg    = TRX                    [ "UI::Clean"                            ]
    mm     . addAction              ( 101 , msg                              )
    ##########################################################################
    msg    = TRX                    [ "UI::AutoResizeColumns"                ]
    mm     . addAction              ( 102 , msg , True , self . Fitting      )
    ##########################################################################
    msg    = TRX                    [ "UI::AutoClean"                        ]
    mm     . addAction              ( 103 , msg , True , AC                  )
    ##########################################################################
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . font ( )                     )
    aa     = mm . exec_             ( QCursor . pos  ( )                     )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunDocking        ( mm , aa ) ) :
      return True
    ##########################################################################
    if                              ( at == 101                            ) :
      ########################################################################
      self . setLimitValue          ( 1212001163 , 1                         )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 102                            ) :
      ########################################################################
      self   . Fitting = aa . isChecked (                                    )
      self   . StoreSettings        ( self . ConfScope                       )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 103                            ) :
      ########################################################################
      if                            ( aa . isChecked ( )                   ) :
        self . setLimitValue        ( self . AutoCleanId , 1                 )
      else                                                                   :
        self . setLimitValue        ( self . AutoCleanId , 0                 )
      ########################################################################
      self   . StoreSettings        ( self . ConfScope                       )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 201                            ) :
      ########################################################################
      self . Hidden . emit          ( self                                   )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
