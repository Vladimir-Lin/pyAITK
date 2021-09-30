# -*- coding: utf-8 -*-
##############################################################################
## TreeWidget
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
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . TreeWidget             import TreeWidget as TreeWidget
from         . AttachDock             import AttachDock as AttachDock
##############################################################################
class TreeDock                ( TreeWidget , AttachDock                    ) :
  ############################################################################
  Clicked    = pyqtSignal     ( int                                          )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super ( TreeWidget , self ) . __init__ ( parent , plan                   )
    self . setDockPlanFunction             (          plan                   )
    ##########################################################################
    ## WidgetClass                                                       ;
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = None
    self . dockingPlaces      = None
    ## dockingPlace       ( Qt::RightDockWidgetArea     )
    ## dockingPlaces      ( Qt::TopDockWidgetArea       |
    ##                      Qt::BottomDockWidgetArea    |
    ##                      Qt::LeftDockWidgetArea      |
    ##                      Qt::RightDockWidgetArea     )
    ##########################################################################
    self . setRootIsDecorated      ( False )
    self . setAlternatingRowColors ( True  )
    self . MountClicked ( 2 )
    ##########################################################################
    ## setFunction             ( N::AttachDock::FunctionDocking , true ) ;
    ## LocalMsgs [ AttachToMdi  ] = tr("Move to window area")            ;
    ## LocalMsgs [ AttachToDock ] = tr("Move to dock area"  )            ;
    ##########################################################################
    return
  ############################################################################
  def Docking ( self , Main , title , area , areas ) :
    ##########################################################################
    super ( AttachDock , self ) . Docking ( Main , self , title , area , areas )
    ## nConnect(Dock,SIGNAL(visibilityChanged(bool))   ,
    ##          this,SLOT  (Visible          (bool)) ) ;
    ##########################################################################
    return
  ############################################################################
  def DockIn  ( self , shown                                               ) :
    ##########################################################################
    super     ( AttachDock , self ) . ShowDock ( shown                       )
    ##########################################################################
    return
  ############################################################################
  def Visible ( self , visible                                             ) :
    ##########################################################################
    super     ( AttachDock , self ) . Visible ( visible                      )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked       ( self , item , column                           ) :
    ##########################################################################
    uuid      = int       ( item . data ( column , Qt . UserRole )           )
    self . Clicked . emit ( uuid                                             )
    ##########################################################################
    return
  ############################################################################
  def DockingMenu ( self , menu ) :
    ##########################################################################
    ##########################################################################
    ## if ( ! isFunction ( N::AttachDock::FunctionDocking ) ) return          ;
    ## QMdiSubWindow  * mdi    = Casting(QMdiSubWindow,parent())              ;
    ## QDockWidget    * dock   = Casting(QDockWidget  ,parent())              ;
    ## if (NotNull(dock) || NotNull(mdi)) Menu . addSeparator ( )             ;
    ## nIfSafe(dock) Menu . add ( AttachToMdi  , LocalMsgs [ AttachToMdi  ] ) ;
    ## nIfSafe(mdi ) Menu . add ( AttachToDock , LocalMsgs [ AttachToDock ] ) ;
    ##########################################################################
    return
  ############################################################################
  def RunDocking ( self , menu , action ) :
    ##########################################################################
    at = menu . at ( action )
    ##########################################################################
    if ( at == AttachDock . AttachToMdi ) :
      ## emit attachMdi (this,dockingOrientation) ;
      return True
    ##########################################################################
    if ( at == AttachDock . AttachToDock ) :
      ## emit attachDock                          (
      ##   this                                   ,
      ##   windowTitle()                          ,
      ##   dockingPlace                           ,
      ##   dockingPlaces                        ) ;
      return True
    ##########################################################################
    return False
##############################################################################

"""
    virtual QTreeWidgetItem * addItem (QString text,SUID uuid,int column = 0);
    virtual QTreeWidgetItem * addItem (QIcon icon,QString text,SUID uuid,int column = 0);

  signals:

    DockSignals ;


QTreeWidgetItem * N::TreeDock::addItem(QString text,SUID uuid,int column)
{
  NewTreeWidgetItem (IT                      ) ;
  IT->setText       (column,text             ) ;
  IT->setData       (column,Qt::UserRole,uuid) ;
  addTopLevelItem   (IT                      ) ;
  return IT                                    ;
}

QTreeWidgetItem * N::TreeDock::addItem(QIcon icon,QString text,SUID uuid,int column)
{
  NewTreeWidgetItem (IT                      ) ;
  IT->setText       (column,text             ) ;
  IT->setIcon       (column,icon             ) ;
  IT->setData       (column,Qt::UserRole,uuid) ;
  addTopLevelItem   (IT                      ) ;
  return IT                                    ;
}

"""
