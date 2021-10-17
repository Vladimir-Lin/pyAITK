# -*- coding: utf-8 -*-
##############################################################################
## IconDock
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
from   AITK . Qt       . Widget       import Widget            as Widget
from   AITK . Pictures . Colors       import WaveLengthToRGB   as waveToRGB
from   AITK . Pictures . Colors       import RatioToWaveLength as RatioToWave
##############################################################################
class SpectrumColors         ( Widget , AttachDock                         ) :
  ############################################################################
  attachDock    = pyqtSignal ( QWidget , str , int , int                     )
  attachMdi     = pyqtSignal ( QWidget , int                                 )
  ############################################################################
  def __init__        ( self , parent = None , plan = None                 ) :
    ##########################################################################
    super (                   ) . __init__ ( parent , plan                   )
    super ( AttachDock , self ) . __init__ (                                 )
    self . InitializeDock                  (          plan                   )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    ## WidgetClass                                            ;
    self . setFunction     ( self . FunctionDocking , True                   )
    self . setLocalMessage ( self . AttachToMdi     , "移動到視窗區域" )
    self . setLocalMessage ( self . AttachToDock    , "移動到停泊區域" )
    ##########################################################################
    self . setMouseTracking ( True )
    ## self . Direction = "Left-Right"
    self . Direction = "Right-Left"
    ## self . Direction = "Top-Bottom"
    ## self . Direction = "Bottom-Top"
    self . FromWL = 380
    self . ToWL   = 780
    self . Image  = None
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
    super ( )  . Docking (        Main , title , area , areas                )
    if                   ( self . Dock == None                             ) :
      return
    ##########################################################################
    self . Dock . visibilityChanged . connect ( self . Visible               )
    ##########################################################################
    return
  ############################################################################
  def DockingMenu ( self , menu                                            ) :
    ##########################################################################
    if            ( not self . isFunction ( self . FunctionDocking )       ) :
      return
    ##########################################################################
    """
    QMdiSubWindow  * mdi    = Casting(QMdiSubWindow,parent())              ;
    QDockWidget    * dock   = Casting(QDockWidget  ,parent())              ;
    if (NotNull(dock) || NotNull(mdi)) Menu . addSeparator ( )             ;
    nIfSafe(dock) Menu . add ( AttachToMdi  , LocalMsgs [ AttachToMdi  ] ) ;
    nIfSafe(mdi ) Menu . add ( AttachToDock , LocalMsgs [ AttachToDock ] ) ;
    """
    ##########################################################################
    return
  ############################################################################
  def RunDocking               ( self , menu , action                      ) :
    ##########################################################################
    at = menu . at             ( action                                      )
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
      R , G , B = waveToRGB    ( Lambda / 10.0                               )
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
      R , G , B = waveToRGB    ( Lambda / 10.0                               )
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
  def HandleWaveLengthPosition             ( self , pos , globalPos        ) :
    ##########################################################################
    Lambda   = self . PositionToWaveLength ( pos                             )
    LSM      = "{:4.3f}" . format          ( Lambda                          )
    LSM      = f"{LSM}Å"
    QToolTip . showText                    ( globalPos , LSM                 )
    ##########################################################################
    return
  ############################################################################
  def WaveLengthPressed                    ( self , pos                    ) :
    ##########################################################################
    Lambda   = self . PositionToWaveLength ( pos                             )
    ##########################################################################
    return
  ############################################################################
##############################################################################
