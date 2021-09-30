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
##############################################################################
class TreeDock                ( TreeWidget                                 ) :
  ############################################################################
  def __init__                ( self , parent = None                       ) :
    ##########################################################################
    super ( TreeWidget , self ) . __init__   ( parent                        )
    ##########################################################################
    return
##############################################################################



"""



class Q_COMPONENTS_EXPORT TreeDock : public TreeWidget
                                   , public AttachDock
{
  Q_OBJECT
  public:

    int                 dockingOrientation ;
    Qt::DockWidgetArea  dockingPlace       ;
    Qt::DockWidgetAreas dockingPlaces      ;

    explicit TreeDock    (StandardConstructor) ;
    virtual ~TreeDock    (void);

  protected:

  private:

  public slots:

    virtual void Docking (QMainWindow * Main,QString title,Qt::DockWidgetArea area,Qt::DockWidgetAreas areas);
    virtual void DockIn  (bool shown);

    virtual QTreeWidgetItem * addItem (QString text,SUID uuid,int column = 0);
    virtual QTreeWidgetItem * addItem (QIcon icon,QString text,SUID uuid,int column = 0);

  protected slots:

    virtual void DockingMenu          (MenuManager & Menu) ;
    virtual bool RunDocking           (MenuManager & Menu,QAction * action) ;
    void         Visible              (bool visible);
    void         doubleClicked        (QTreeWidgetItem * item,int column);

  private slots:

  signals:

    DockSignals ;

    void Clicked         (SUID uuid);

};



#include <qtcomponents.h>

N::TreeDock:: TreeDock           ( QWidget * parent , Plan * p )
            : TreeWidget         (           parent ,        p )
            , AttachDock         (                           p )
            , dockingOrientation ( 0                           )
            , dockingPlace       ( Qt::RightDockWidgetArea     )
            , dockingPlaces      ( Qt::TopDockWidgetArea       |
                                   Qt::BottomDockWidgetArea    |
                                   Qt::LeftDockWidgetArea      |
                                   Qt::RightDockWidgetArea     )
{
  WidgetClass                                                       ;
  setRootIsDecorated      ( false                                 ) ;
  setAlternatingRowColors ( true                                  ) ;
  MountClicked            ( 2                                     ) ;
  setFunction             ( N::AttachDock::FunctionDocking , true ) ;
  LocalMsgs [ AttachToMdi  ] = tr("Move to window area")            ;
  LocalMsgs [ AttachToDock ] = tr("Move to dock area"  )            ;
}

N::TreeDock::~TreeDock (void)
{
}

void N::TreeDock::Docking        (
       QMainWindow      *  Main  ,
       QString             title ,
       Qt::DockWidgetArea  area  ,
       Qt::DockWidgetAreas areas )
{
  AttachDock::Docking(Main,this,title,area,areas) ;
  nConnect(Dock,SIGNAL(visibilityChanged(bool))   ,
           this,SLOT  (Visible          (bool)) ) ;
}

void N::TreeDock::Visible(bool visible)
{
  Visiblity(visible) ;
}

void N::TreeDock::DockIn(bool shown)
{
  Show(shown);
}

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

void N::TreeDock::doubleClicked(QTreeWidgetItem * item,int column)
{
  SUID uuid = nTreeUuid(item,column) ;
  emit Clicked (uuid)                ;
}

void N::TreeDock::DockingMenu(MenuManager & Menu)
{
  if ( ! isFunction ( N::AttachDock::FunctionDocking ) ) return          ;
  QMdiSubWindow  * mdi    = Casting(QMdiSubWindow,parent())              ;
  QDockWidget    * dock   = Casting(QDockWidget  ,parent())              ;
  if (NotNull(dock) || NotNull(mdi)) Menu . addSeparator ( )             ;
  nIfSafe(dock) Menu . add ( AttachToMdi  , LocalMsgs [ AttachToMdi  ] ) ;
  nIfSafe(mdi ) Menu . add ( AttachToDock , LocalMsgs [ AttachToDock ] ) ;
}

bool N::TreeDock::RunDocking(MenuManager & Menu,QAction * action)
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

