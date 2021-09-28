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
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class ListWidget ( QListWidget , VirtualGui ) :
  ############################################################################
  def __init__ ( self , parent = None ) :
    ##########################################################################
    super ( QListWidget , self ) . __init__   ( parent )
    super ( VirtualGui  , self ) . Initialize ( self   )
    ##########################################################################
    return
  ############################################################################
  def Configure ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def focusInEvent ( self , event ) :
    if ( self . focusIn ( event ) ) :
      return
    super ( QListWidget , self ) . focusInEvent ( event )
    return
  ############################################################################
  def focusOutEvent ( self , event ) :
    if ( self . focusOut ( event ) ) :
      return
    super ( QListWidget , self ) . focusOutEvent ( event )
    return
  ############################################################################
  def contextMenuEvent ( self , event ) :
    if ( self . Menu ( event . pos ( ) ) ) :
      event . accept ( )
      return
    super ( QListWidget , self ) . contextMenuEvent ( event )
    return
  ############################################################################
  def startup ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def FocusIn ( self ) :
    return True
  ############################################################################
  def FocusOut ( self ) :
    return True
  ############################################################################
  def removeParked ( self ) :
    return True
  ############################################################################
  def singleClicked ( self , item , column ) :
    raise NotImplementedError ( )
  ############################################################################
  def doubleClicked ( self , item , column ) :
    raise NotImplementedError ( )
  ############################################################################
  def Insert ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def Delete ( self ) :
    raise NotImplementedError ( )
  ############################################################################
  def Menu ( self , pos ) :
    raise NotImplementedError ( )
##############################################################################




"""





class Q_COMPONENTS_EXPORT ListDock : public ListWidget
                                   , public AttachDock
{
  Q_OBJECT
  public:

    int                 dockingOrientation ;
    Qt::DockWidgetArea  dockingPlace       ;
    Qt::DockWidgetAreas dockingPlaces      ;

    explicit ListDock        (StandardConstructor) ;
    virtual ~ListDock        (void);

  protected:

  private:

  public slots:

    virtual void Docking     (QMainWindow *       Main    ,
                              QString             title   ,
                              Qt::DockWidgetArea  area    ,
                              Qt::DockWidgetAreas areas ) ;
    virtual void DockIn      (bool shown);

  protected slots:

    virtual void DockingMenu (MenuManager & Menu) ;
    virtual bool RunDocking  (MenuManager & Menu,QAction * action) ;
    void Visible             (bool visible);

  private slots:

  signals:

    DockSignals ;

};





#include <qtcomponents.h>

N::ListDock:: ListDock           ( QWidget * parent , Plan * p )
            : ListWidget         (           parent ,        p )
            , AttachDock         (                           p )
            , dockingOrientation ( 0                           )
            , dockingPlace       ( Qt::RightDockWidgetArea     )
            , dockingPlaces      ( Qt::TopDockWidgetArea       |
                                   Qt::BottomDockWidgetArea    |
                                   Qt::LeftDockWidgetArea      |
                                   Qt::RightDockWidgetArea     )
{
  WidgetClass                                            ;
  setFunction ( N::AttachDock::FunctionDocking , true )  ;
  LocalMsgs [ AttachToMdi  ] = tr("Move to window area") ;
  LocalMsgs [ AttachToDock ] = tr("Move to dock area"  ) ;
}

N::ListDock::~ListDock (void)
{
}

void N::ListDock::Docking(QMainWindow       * Main  ,
                          QString             title ,
                          Qt::DockWidgetArea  area  ,
                          Qt::DockWidgetAreas areas )
{
  AttachDock::Docking(Main,this,title,area,areas) ;
  nConnect(Dock,SIGNAL(visibilityChanged(bool))   ,
           this,SLOT  (Visible          (bool)) ) ;
}

void N::ListDock::Visible(bool visible)
{
  Visiblity(visible) ;
}

void N::ListDock::DockIn(bool shown)
{
  Show(shown);
}

void N::ListDock::DockingMenu(MenuManager & Menu)
{
  if ( ! isFunction ( N::AttachDock::FunctionDocking ) ) return          ;
  QMdiSubWindow  * mdi    = Casting(QMdiSubWindow,parent())              ;
  QDockWidget    * dock   = Casting(QDockWidget  ,parent())              ;
  if (NotNull(dock) || NotNull(mdi)) Menu . addSeparator ( )             ;
  nIfSafe(dock) Menu . add ( AttachToMdi  , LocalMsgs [ AttachToMdi  ] ) ;
  nIfSafe(mdi ) Menu . add ( AttachToDock , LocalMsgs [ AttachToDock ] ) ;
}

bool N::ListDock::RunDocking(MenuManager & Menu,QAction * action)
{
  switch (Menu[action])                        {
    case AttachToMdi                           :
      emit attachMdi (this,dockingOrientation) ;
    break                                      ;
    case AttachToDock                          :
      emit attachDock                          (
        this                                   ,
        windowTitle()                          ,
        dockingPlace                           ,
        dockingPlaces                        ) ;
    break                                      ;
    default: return false                      ;
  }                                            ;
  return true                                  ;
}




"""




