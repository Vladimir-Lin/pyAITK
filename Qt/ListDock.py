# -*- coding: utf-8 -*-
##############################################################################
## ListWidget
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
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QListWidget
from   PyQt5 . QtWidgets              import QListWidgetItem
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . AttachDock             import AttachDock as AttachDock
from         . ListWidget             import ListWidget as ListWidget
##############################################################################
class ListDock        ( ListWidget , AttachDock                            ) :
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
##############################################################################
