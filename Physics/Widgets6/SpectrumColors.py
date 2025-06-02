# -*- coding: utf-8 -*-
##############################################################################
## SpectrumColors
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
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QPainter
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QPainter
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QMenu
##############################################################################
from   AITK . Qt       . AttachDock   import AttachDock        as AttachDock
from   AITK . Qt       . MenuManager  import MenuManager       as MenuManager
from   AITK . Qt       . Widget       import Widget            as Widget
from   AITK . Qt       . SpinBox      import SpinBox           as SpinBox
from   AITK . Pictures . Colors       import WaveLengthToRGB   as waveToRGB
from   AITK . Pictures . Colors       import RatioToWaveLength as RatioToWave
##############################################################################
class SpectrumColors      ( Widget , AttachDock                            ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  attachNone = pyqtSignal ( QWidget                                          )
  attachDock = pyqtSignal ( QWidget , str , int , int                        )
  attachMdi  = pyqtSignal ( QWidget , int                                    )
  Angstrom   = pyqtSignal ( float , float , int , int , int                  )
  Nanometer  = pyqtSignal ( float , float , int , int , int                  )
  Leave      = pyqtSignal ( QWidget                                          )
  ############################################################################
  def __init__            ( self , parent = None , plan = None             ) :
    ##########################################################################
    super (                   ) . __init__ ( parent , plan                   )
    super ( AttachDock , self ) . __init__ (                                 )
    self . InitializeDock                  (          plan                   )
    ##########################################################################
    self . dockingOrientation = Qt . Horizontal
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    ## WidgetClass                                            ;
    self . setFunction     ( self . FunctionDocking , True                   )
    self . setFunction     ( self . HavingMenu      , True                   )
    ##########################################################################
    self . setMouseTracking ( True )
    ## self . Direction   = "Left-Right"
    self . Direction   = "Right-Left"
    ## self . Direction   = "Top-Bottom"
    ## self . Direction   = "Bottom-Top"
    self . minWL       =  380
    self . maxWL       =  780
    self . FromWL      =  380
    self . ToWL        =  780
    self . Luminance   = 1000
    self . minSpin     = None
    self . maxSpin     = None
    self . AudioReport = True
    self . ShowToolTip = True
    self . Image       = None
    ##########################################################################
    return
  ############################################################################
  def sizeHint       ( self                                                ) :
    return QSize     ( 1024 , 48                                             )
  ############################################################################
  def setSpectrumDirection          ( self , direction                     ) :
    self . Direction = direction
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
  def focusInEvent           ( self , event                                ) :
    ##########################################################################
    if                       ( self . focusIn ( event )                    ) :
      return
    ##########################################################################
    super ( ) . focusInEvent ( event                                         )
    ##########################################################################
    return
  ############################################################################
  def focusOutEvent           ( self , event                               ) :
    ##########################################################################
    if                        ( self . focusOut ( event )                  ) :
      return
    ##########################################################################
    super ( ) . focusOutEvent ( event                                        )
    ##########################################################################
    return
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    ##########################################################################
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . contextMenuEvent ( event                                     )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent                ( self  , event                        ) :
    ##########################################################################
    self . HandleWaveLengthPosition ( event . pos () , event . globalPos ()  )
    super ( ) . mouseMoveEvent      ( event                                  )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent             ( self  , event                          ) :
    ##########################################################################
    if                            ( event . button ( ) == Qt . LeftButton  ) :
      self . WaveLengthPressed    ( event . pos ( )                          )
    super ( ) . mousePressEvent   ( event                                    )
    ##########################################################################
    return
  ############################################################################
  def paintEvent           ( self , event                                  ) :
    ##########################################################################
    if                     ( self . Image == None                          ) :
      self . PrepareImage  (                                                 )
    ##########################################################################
    p = QPainter           ( self                                            )
    p . drawImage          ( 0 , 0 , self . Image                            )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    self . PrepareImage     (                                                )
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
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
  def toWaveString           ( self , Lambda                               ) :
    ##########################################################################
    LSM = "{:4.3f}" . format (        Lambda                                 )
    LSM = f"{LSM} Å"
    ##########################################################################
    return LSM
  ############################################################################
  def toFrequencyString ( self , Lambda                                    ) :
    ##########################################################################
    F   = 2997924.58 / Lambda
    FSM = "{:4.3f}" . format (        F                                 )
    FSM = f"{FSM} THz"
    ##########################################################################
    return FSM
  ############################################################################
  def DockLocationChanged ( self , area                                    ) :
    ##########################################################################
    if   ( area in [ Qt . LeftDockWidgetArea , Qt . RightDockWidgetArea  ] ) :
      ########################################################################
      self . dockingOrientation = Qt . Vertical
      self . Direction = "Bottom-Top"
      self . PrepareImage (                                                  )
      self . update       (                                                  )
      ########################################################################
    elif ( area in [ Qt . TopDockWidgetArea  , Qt . BottomDockWidgetArea ] ) :
      ########################################################################
      self . dockingOrientation = Qt . Horizontal
      self . Direction = "Right-Left"
      self . PrepareImage (                                                  )
      self . update       (                                                  )
    ##########################################################################
    return
  ############################################################################
  def Visible        ( self , visible                                      ) :
    self . Visiblity (        visible                                        )
    return
  ############################################################################
  def DockIn         ( self , shown                                        ) :
    self . ShowDock  (        shown                                          )
    return
  ############################################################################
  def Docking            ( self , Main , title , area , areas              ) :
    ##########################################################################
    super ( )  . Docking (        Main , self ,  title , area , areas        )
    if                   ( self . Dock == None                             ) :
      return
    ##########################################################################
    self . Dock . visibilityChanged . connect ( self . Visible               )
    ##########################################################################
    return
  ############################################################################
  def DockingMenu                    ( self , menu                         ) :
    ##########################################################################
    canDock = self . isFunction      ( self . FunctionDocking                )
    if                               ( not canDock                         ) :
      return
    ##########################################################################
    p       = self . parentWidget    (                                       )
    S       = False
    D       = False
    M       = False
    ##########################################################################
    if                               ( p == None                           ) :
      S     = True
    else                                                                     :
      ########################################################################
      if                             ( self . isDocking ( )                ) :
        D   = True
      else                                                                   :
        M   = True
    ##########################################################################
    menu    . addSeparator           (                                       )
    ##########################################################################
    if                               (     S or D                          ) :
      msg   = self . getLocalMessage ( self . AttachToMdi                    )
      menu  . addAction              ( self . AttachToMdi  , msg             )
    ##########################################################################
    if                               (     S or M                          ) :
      msg   = self . getLocalMessage ( self . AttachToDock                   )
      menu  . addAction              ( self . AttachToDock , msg             )
    ##########################################################################
    if                               ( not S                               ) :
      msg   = self . getLocalMessage ( self . AttachToNone                   )
      menu  . addAction              ( self . AttachToNone , msg             )
    ##########################################################################
    return
  ############################################################################
  def RunDocking               ( self , menu , action                      ) :
    ##########################################################################
    at = menu . at             ( action                                      )
    ##########################################################################
    if                         ( at == self . AttachToNone                 ) :
      self . attachNone . emit ( self                                        )
      return True
    ##########################################################################
    if                         ( at == self . AttachToMdi                  ) :
      self . attachMdi  . emit ( self , self . dockingOrientation            )
      return True
    ##########################################################################
    if                         ( at == self . AttachToDock                 ) :
      self . attachDock . emit ( self                                      , \
                                 self . windowTitle ( )                    , \
                                 self . dockingPlace                       , \
                                 self . dockingPlaces                        )
      return True
    ##########################################################################
    return False
  ############################################################################
  def PositionToWaveLength     ( self , pos                                ) :
    ##########################################################################
    x      = pos  . x          (                                             )
    y      = pos  . y          (                                             )
    w      = self . width      (                                             )
    h      = self . height     (                                             )
    fwl    = self . FromWL
    twl    = self . ToWL
    ##########################################################################
    s      = x
    m      = w
    ##########################################################################
    if                         ( self . Direction == "Right-Left"          ) :
      ########################################################################
      s    = w - x - 1
      ########################################################################
    elif                       ( self . Direction == "Top-Bottom"          ) :
      ########################################################################
      s    = y
      m    = h
      ########################################################################
    elif                       ( self . Direction == "Bottom-Top"          ) :
      ########################################################################
      s    = h - y - 1
      m    = h
    ##########################################################################
    Lambda = RatioToWave         ( s , m , fwl , twl                           )
    Lambda = Lambda * 10
    ##########################################################################
    return Lambda
  ############################################################################
  def PaintWlHorizontal        ( self , painter                            ) :
    ##########################################################################
    w      = self . width      (                                             )
    h      = self . height     (                                             )
    ey     = h - 1
    ##########################################################################
    for i in range             ( 0 , w                                     ) :
      Lambda = self . PositionToWaveLength ( QPoint ( i , 0 )                )
      R , G , B = waveToRGB    ( Lambda / 10.0 , self . Luminance            )
      C         = QColor       ( R , G , B                                   )
      painter   . setBrush     ( C                                           )
      painter   . setPen       ( QPen ( C , 1 , Qt.SolidLine )               )
      painter   . drawLine     ( i , 0 , i , ey                              )
    ##########################################################################
    return
  ############################################################################  
  def PaintWlVertical          ( self , painter                            ) :
    ##########################################################################
    w      = self . width      (                                             )
    h      = self . height     (                                             )
    ex     = w - 1
    ##########################################################################
    for i in range             ( 0 , h                                     ) :
      Lambda = self . PositionToWaveLength ( QPoint ( 0 , i )                )
      R , G , B = waveToRGB    ( Lambda / 10.0 , self . Luminance            )
      C         = QColor       ( R , G , B                                   )
      painter   . setBrush     ( C                                           )
      painter   . setPen       ( QPen ( C , 1 , Qt.SolidLine )               )
      painter   . drawLine     ( 0 , i , ex , i                              )
    ##########################################################################
    return
  ############################################################################
  def PaintWaveLength          ( self , painter                            ) :
    ##########################################################################
    if ( self . Direction in [ "Top-Bottom" , "Bottom-Top" ] )               :
      self . PaintWlVertical   (        painter                              )
    else                                                                     :
      self . PaintWlHorizontal (        painter                              )
    ##########################################################################
    return
  ############################################################################
  def PrepareImage             ( self                                      ) :
    ##########################################################################
    w    = self . width        (                                             )
    h    = self . height       (                                             )
    p    = QPainter            (                                             )
    self . Image = QImage      ( w , h , QImage . Format_RGB888              )
    p    . begin               ( self . Image                                )
    self . PaintWaveLength     ( p                                           )
    p    . end                 (                                             )
    ##########################################################################
    return
  ############################################################################
  def HandleWaveLengthPosition              ( self , pos , globalPos       ) :
    ##########################################################################
    if                                      ( not self . ShowToolTip       ) :
      return
    ##########################################################################
    L         = self . Luminance
    Lambda    = self . PositionToWaveLength ( pos                            )
    LSM       = self . toWaveString         ( Lambda                         )
    FSM       = self . toFrequencyString    ( Lambda                         )
    R , G , B = waveToRGB                   ( Lambda / 10.0 , L              )
    MSG       = f"{LSM} / {FSM} / ( {R} , {G} , {B} )"
    QToolTip  . showText                    ( globalPos , MSG                )
    ##########################################################################
    return
  ############################################################################
  def WaveLengthPressed                  ( self , pos                      ) :
    ##########################################################################
    L      = self . Luminance
    Lambda = self . PositionToWaveLength (        pos                        )
    R , G , B = waveToRGB                ( Lambda / 10.0 , L                 )
    FREQ   = 2997924.58 / Lambda
    self   . Angstrom  . emit            ( Lambda        , FREQ , R , G , B  )
    self   . Nanometer . emit            ( Lambda / 10.0 , FREQ , R , G , B  )
    ##########################################################################
    if                                   ( self . AudioReport              ) :
      ########################################################################
      LSM  = "{:4.3f}" . format          (        Lambda                     )
      LSM  = f"{LSM} Angstrom"
      self . Go ( self . Talk , ( LSM , self . getLocality ( ) , )           )
    ##########################################################################
    return
  ############################################################################
  def DirectionMenu          ( self , menu                                 ) :
    ##########################################################################
    LDM  = menu . addMenu    ( "顯示方向" )
    ##########################################################################
    msg  = "左高頻/右低頻"
    hid  =                   ( self . Direction == "Left-Right"              )
    menu . addActionFromMenu ( LDM , 20000001 , msg , True , hid             )
    ##########################################################################
    msg  = "左低頻/右高頻"
    hid  =                   ( self . Direction == "Right-Left"              )
    menu . addActionFromMenu ( LDM , 20000002 , msg , True , hid             )
    ##########################################################################
    msg  = "上高頻/下低頻"
    hid  =                   ( self . Direction == "Top-Bottom"              )
    menu . addActionFromMenu ( LDM , 20000003 , msg , True , hid             )
    ##########################################################################
    msg  = "上低頻/下高頻"
    hid  =                   ( self . Direction == "Bottom-Top"              )
    menu . addActionFromMenu ( LDM , 20000004 , msg , True , hid             )
    ##########################################################################
    return
  ############################################################################
  def RunDirection             ( self , menu , action                      ) :
    ##########################################################################
    at = menu . at             ( action                                      )
    ##########################################################################
    if                         ( at == 20000001                            ) :
      ########################################################################
      self . Direction = "Left-Right"
      self . PrepareImage      (                                             )
      self . update            (                                             )
      ########################################################################
      return True
    ##########################################################################
    if                         ( at == 20000002                            ) :
      ########################################################################
      self . Direction = "Right-Left"
      self . PrepareImage      (                                             )
      self . update            (                                             )
      ########################################################################
      return True
    ##########################################################################
    if                         ( at == 20000003                            ) :
      ########################################################################
      self . Direction = "Top-Bottom"
      self . PrepareImage      (                                             )
      self . update            (                                             )
      ########################################################################
      return True
    ##########################################################################
    if                         ( at == 20000004                            ) :
      ########################################################################
      self . Direction = "Bottom-Top"
      self . PrepareImage      (                                             )
      self . update            (                                             )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def LuminanceChanged            ( self , luminance                       ) :
    ##########################################################################
    self . Luminance = luminance
    ##########################################################################
    self   . PrepareImage         (                                          )
    self   . update               (                                          )
    ##########################################################################
    return
  ############################################################################
  def MinWaveLengthChanged        ( self , waveAngstrom                    ) :
    ##########################################################################
    self   . FromWL = float ( waveAngstrom ) / 10.0
    ##########################################################################
    if                            ( self . maxSpin is not None             ) :
      self . maxSpin . setMinimum ( int ( self . FromWL * 10 )               )
      self . maxSpin . setMaximum ( int ( self . maxWL  * 10 )               )
    ##########################################################################
    self   . PrepareImage         (                                          )
    self   . update               (                                          )
    ##########################################################################
    return
  ############################################################################
  def MaxWaveLengthChanged        ( self , waveAngstrom                    ) :
    ##########################################################################
    self   . ToWL   = float ( waveAngstrom ) / 10.0
    ##########################################################################
    if                            ( self . minSpin is not None             ) :
      self . minSpin . setMinimum ( int ( self . minWL  * 10 )               )
      self . minSpin . setMaximum ( int ( self . ToWL   * 10 )               )
    ##########################################################################
    self   . PrepareImage         (                                          )
    self   . update               (                                          )
    ##########################################################################
    return
  ############################################################################
  def FrequencyMenu               ( self , menu                            ) :
    ##########################################################################
    LDM   = menu . addMenu         ( "光譜範圍" )
    ##########################################################################
    minSB = SpinBox                ( None , self . PlanFunc                  )
    minSB . setMinimum             ( int ( self . minWL  * 10 )              )
    minSB . setMaximum             ( int ( self . ToWL   * 10 )              )
    minSB . setValue               ( int ( self . FromWL * 10 )              )
    minSB . setAlignment           ( Qt . AlignRight                         )
    minSB . setPrefix              ( "最小波長：" )
    minSB . setSuffix              ( " Å " )
    self  . minSpin = minSB
    menu  . addWidgetWithMenu      ( LDM , 999712343 , minSB                 )
    ##########################################################################
    maxSB = SpinBox                ( None , self . PlanFunc                  )
    maxSB . setMinimum             ( int ( self . FromWL * 10 )              )
    maxSB . setMaximum             ( int ( self . maxWL  * 10 )              )
    maxSB . setValue               ( int ( self . ToWL   * 10 )              )
    maxSB . setAlignment           ( Qt . AlignRight                         )
    maxSB . setPrefix              ( "最大波長：" )
    maxSB . setSuffix              ( " Å " )
    self  . maxSpin = maxSB
    menu  . addWidgetWithMenu      ( LDM , 999712344 , maxSB                 )
    ##########################################################################
    minSB . valueChanged . connect ( self . MinWaveLengthChanged             )
    maxSB . valueChanged . connect ( self . MaxWaveLengthChanged             )
    ##########################################################################
    return
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    msg    = "顯示數據"
    mm     . addAction              ( 2001 , msg , True , self . ShowToolTip )
    ##########################################################################
    msg    = "語音報告"
    mm     . addAction              ( 2002 , msg , True , self . AudioReport )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ligSB  = SpinBox                ( None , self . PlanFunc                 )
    ligSB  . setMinimum             ( 1                                      )
    ligSB  . setMaximum             ( 1000                                   )
    ligSB  . setValue               ( int ( self . Luminance )               )
    ## ligSB  . setAlignment           ( Qt . AlignRight                        )
    ligSB  . setPrefix              ( "亮度：" )
    ligSB  . valueChanged . connect ( self . LuminanceChanged                )
    mm     . addWidget              ( 999712345 , ligSB                      )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    self   . DirectionMenu          ( mm                                     )
    self   . FrequencyMenu          ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    self   . minSpin = None
    self   . maxSpin = None
    ##########################################################################
    if                              ( self . RunDirection ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( at == 2001                           ) :
      ########################################################################
      if                            ( self . ShowToolTip                   ) :
        self . ShowToolTip = False
      else                                                                   :
        self . ShowToolTip = True
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 2002                           ) :
      ########################################################################
      if                            ( self . AudioReport                   ) :
        self . AudioReport = False
      else                                                                   :
        self . AudioReport = True
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
