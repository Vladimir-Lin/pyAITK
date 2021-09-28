# -*- coding: utf-8 -*-
##############################################################################
## 選單管理功能
##############################################################################
import os
import sys
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
from   PyQt5 . QtWidgets              import QActionGroup
from   PyQt5 . QtWidgets              import QWidgetAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
##############################################################################
class MenuManager ( ) :
  ############################################################################
  def __init__ ( self , parent = None ) :
    ##########################################################################
    self . actions      = [ ]
    self . menus        = [ ]
    self . IDs          = { }
    self . Widgets      = { }
    self . actionGroups = { }
    ##########################################################################
    self . menu         = QMenu        ( parent                     )
    self . menu         . setAttribute ( Qt . WA_InputMethodEnabled )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setFont ( self , font ) :
    self . menu . setFont ( font )
    for m in self . menus :
      m  . setFont ( font )
    return
  ############################################################################
  def widgetAt ( self , Id ) :
    if not ( Id in self . Widgets ) :
      return None
    return self . Widgets [ Id ]
  ############################################################################
  def contains ( self , action ) :
    if ( None == action ) :
      return False
    return ( action in self . actions )
  ############################################################################
  def at ( self , action ) :
    if ( None == action ) :
      return -1
    if not ( action in self . IDs ) :
      return -1
    return self . IDs [ action ]
  ############################################################################
  def __getitem__ ( self , action ) :
    return self . at ( action )
  ############################################################################
  def ActionGroup ( self , Id ) :
    return self . setGroup ( Id , QActionGroup ( None ) )
  ############################################################################
  def Group ( self , Id ) :
    if not ( Id in self . actionGroups ) :
      return None
    return self . actionGroups [ Id ]
  ############################################################################
  def setGroup ( self , Id , group ) :
    self . actionGroups [ Id ]  = group ;
    return Id
  ############################################################################
  def exec_ ( self , pos ) :
    if ( len ( self . actions ) <= 0 ) :
      return None
    return self . menu . exec_ ( pos )
  ############################################################################
  def addSeparator ( self ) :
    return self . menu . addSeparator ( )
  ############################################################################
  def addSeparatorFromMenu ( self , menu ) :
    return menu . addSeparator ( )
  ############################################################################
  def addMenu ( self , title ) :
    m    = self  . menu . addMenu ( title )
    f    = self  . menu . font    (       )
    m    . setFont                ( f     )
    self . menus . append         ( m     )
    return m
  ############################################################################
  def addMenuFromMenu     ( self , m , title ) :
    n    = m . addMenu    ( title )
    f    = m . font       (       )
    n    . setFont        ( f     )
    self . menus . append ( n     )
    return n
  ############################################################################
  def addMaps ( self , Menu ) :
    KK = Menu . keys ( )
    for Id in KK :
      text = Menu [ Id ]
      self . addAction ( Id , text )
    return
  ############################################################################
  def addAction ( self , Id , text , checkable = False , checked = False ) :
    a    = self    . menu . addAction ( text      )
    self . actions . append           ( a         )
    self . IDs [ a ] = Id
    a    . setCheckable               ( checkable )
    a    . setChecked                 ( checked   )
    return a
  ############################################################################
  def addActionWithIcon ( self , Id , icon , text , checkable = False , checked = False ) :
    a    = self . menu . addAction ( icon , text )
    self . actions     . append    ( a           )
    self . IDs [ a ] = Id
    a    . setCheckable            ( checkable   )
    a    . setChecked              ( checked     )
    return a
  ############################################################################
  def addActionFromMenu ( self , m , Id , text , checkable = False , checked = False ) :
    a    = m       . addAction ( text      )
    self . actions . append    ( a         )
    self . IDs [ a ] = Id
    a    . setCheckable        ( checkable )
    a    . setChecked          ( checked   )
    return a
  ############################################################################
  def addActionFromMenuWithIcon ( self , m , Id , icon , text , checkable = False , checked = False ) :
    a    = m       . addAction ( icon , text )
    self . actions . append    ( a           )
    self . IDs [ a ] = Id
    a    . setCheckable        ( checkable   )
    a    . setChecked          ( checked     )
    return a
  ############################################################################
  def addWidget ( self , Id , widget ) :
    widgetAction   = QWidgetAction    ( self . menu . parentWidget ( ) )
    widgetAction   . setDefaultWidget ( widget                         )
    self . menu    . addAction        ( widgetAction                   )
    self . actions . append           ( widgetAction                   )
    self . IDs     [  widgetAction ] = Id
    self . Widgets [ Id            ] = widget
    return widgetAction
  ############################################################################
  def addWidgetWithMenu ( self , m , Id , widget ) :
    widgetAction   = QWidgetAction    ( self . menu . parentWidget ( ) )
    widgetAction   . setDefaultWidget ( widget                         )
    m              . addAction        ( widgetAction                   )
    self . actions . append           ( widgetAction                   )
    self . IDs     [  widgetAction ] = Id
    self . Widgets [ Id            ] = widget
    return widgetAction
##############################################################################


"""


class Q_COMPONENTS_EXPORT MenuManager
{
  public:

    QMenu * menu ;

    explicit MenuManager    (nDeclWidget) ;
    virtual ~MenuManager    (void);

    QAction * exec          (QPoint pos = QCursor::pos()) ;

    void      add           (NAMEs Menu);
    QAction * add           (int Id,QString text);
    QAction * add           (int Id,QIcon icon,QString text);
    QAction * add           (int Id,QString text,bool checkable,bool checked);
    QAction * add           (int Id,QIcon icon,QString text,bool checkable,bool checked);
    QAction * addSeparator  (void) ;

    QMenu   * addMenu       (QString title) ;
    QMenu   * addMenu       (QMenu * m,QString title) ;
    QAction * add           (QMenu * m,int Id,QString text);
    QAction * add           (QMenu * m,int Id,QIcon icon,QString text);
    QAction * add           (QMenu * m,int Id,QString text,bool checkable,bool checked);
    QAction * add           (QMenu * m,int Id,QIcon icon,QString text,bool checkable,bool checked);
    QAction * addSeparator  (QMenu * m) ;

    QAction * add           (int Id,nDeclWidget) ;
    QAction * add           (QMenu * m,int Id,nDeclWidget) ;

    bool      contains      (QAction * action) ;
    int       operator []   (QAction * action) ;

    void      setFont       (QFont  font) ;
    void      setFont       (Font   font) ;
    void      setFont       (Plan * plan) ;

    QActionGroup * group    (int Id) ;
    int            setGroup (int Id,QActionGroup * group) ;

    QWidget      * widget   (int Id) ;

  protected:

    QList<QAction *                > actions      ;
    QList<QMenu   *                > menus        ;
    QMap <QAction *, int           > IDs          ;
    QMap <int      , QWidget      *> Widgets      ;
    QMap <int      , QActionGroup *> actionGroups ;

  private:

};


#include <qtcomponents.h>

N::MenuManager:: MenuManager(QWidget * parent)
{
  menu  = new QMenu    ( parent                           ) ;
  menu -> setAttribute ( Qt::WA_InputMethodEnabled , true ) ;
}

N::MenuManager::~MenuManager(void)
{
  menu -> deleteLater ( ) ;
  menu  = NULL            ;
}

QAction * N::MenuManager::exec(QPoint pos)
{
  if (actions.count()<=0) return NULL ;
  return menu->exec(pos)              ;
}

void N::MenuManager::add(NAMEs Menu)
{
  UUIDs Uuids = Menu.keys() ;
  SUID  uuid                ;
  foreach (uuid,Uuids)      {
    add(uuid,Menu[uuid])    ;
  }                         ;
}

QAction * N::MenuManager::add(int Id,QString text)
{
  QAction   * a = menu->addAction(text) ;
  actions  << a                         ;
  IDs [ a ] = Id                        ;
  return a                              ;
}

QAction * N::MenuManager::add(int Id,QIcon icon,QString text)
{
  QAction   * a = menu->addAction(icon,text) ;
  actions  << a                              ;
  IDs [ a ] = Id                             ;
  return a                                   ;
}

QAction * N::MenuManager::add(int Id,QString text,bool checkable,bool checked)
{
  QAction   * a = menu->addAction(text) ;
  actions  << a                         ;
  IDs [ a ] = Id                        ;
  a -> setCheckable ( checkable )       ;
  a -> setChecked   ( checked   )       ;
  return a                              ;
}

QAction * N::MenuManager::add(int Id,QIcon icon,QString text,bool checkable,bool checked)
{
  QAction   * a = menu->addAction(icon,text) ;
  actions  << a                              ;
  IDs [ a ] = Id                             ;
  a -> setCheckable ( checkable )            ;
  a -> setChecked   ( checked   )            ;
  return a                                   ;
}

QAction * N::MenuManager::addSeparator (void)
{
  return menu -> addSeparator ( ) ;
}

QMenu * N::MenuManager::addMenu(QString title)
{
  QMenu * m = menu -> addMenu( title ) ;
  menus << m                           ;
  return  m                            ;
}

QMenu * N::MenuManager::addMenu(QMenu * m,QString title)
{
  QMenu * n = m -> addMenu( title ) ;
  menus << n                        ;
  return  n                         ;
}

QAction * N::MenuManager::add(QMenu * m,int Id,QString text)
{
  QAction  * a = m->addAction(text) ;
  actions << a                      ;
  IDs[a]   = Id                     ;
  return a                          ;
}

QAction * N::MenuManager::add(QMenu * m,int Id,QIcon icon,QString text)
{
  QAction  * a = m->addAction(icon,text) ;
  actions << a                           ;
  IDs[a]   = Id                          ;
  return a                               ;
}

QAction * N::MenuManager::add(QMenu * m,int Id,QString text,bool checkable,bool checked)
{
  QAction   * a = m->addAction(text) ;
  actions  << a                      ;
  IDs [ a ] = Id                     ;
  a -> setCheckable ( checkable )    ;
  a -> setChecked   ( checked   )    ;
  return a                           ;
}

QAction * N::MenuManager::add(QMenu * m,int Id,QIcon icon,QString text,bool checkable,bool checked)
{
  QAction   * a = m->addAction(icon,text) ;
  actions  << a                           ;
  IDs [ a ] = Id                          ;
  a -> setCheckable ( checkable )         ;
  a -> setChecked   ( checked   )         ;
  return a                                ;
}

QAction * N::MenuManager::addSeparator(QMenu * m)
{
  return m -> addSeparator ( ) ;
}

QAction * N::MenuManager::add(int Id,QWidget * W)
{
  QWidgetAction * widgetAction = new QWidgetAction(menu->parentWidget()) ;
  widgetAction->setDefaultWidget(W)                                      ;
  QAction       * a            = (QAction *)widgetAction                 ;
  menu     -> addAction ( a )                                            ;
  actions  << a                                                          ;
  IDs     [  a ] = Id                                                    ;
  Widgets [ Id ] = W                                                     ;
  return a                                                               ;
}

QAction * N::MenuManager::add(QMenu * m,int Id,QWidget * W)
{
  QWidgetAction * widgetAction = new QWidgetAction(menu->parentWidget()) ;
  widgetAction->setDefaultWidget(W)                                      ;
  QAction       * a            = (QAction *)widgetAction                 ;
  m        -> addAction ( a )                                            ;
  actions  << a                                                          ;
  IDs     [ a  ] = Id                                                    ;
  Widgets [ Id ] = W                                                     ;
  return a                                                               ;
}

bool N::MenuManager::contains(QAction * action)
{
  nKickOut ( IsNull(action) , false  ) ;
  return actions . contains ( action ) ;
}

int N::MenuManager::operator [] (QAction * action)
{
  if (!IDs.contains(action)) return -1 ;
  return IDs [ action ]                ;
}

void N::MenuManager::setFont(QFont font)
{
  menu -> setFont ( font )          ;
  for (int i=0;i<menus.count();i++) {
    menus[i]->setFont(font)         ;
  }                                 ;
}

void N::MenuManager::setFont(Font f)
{
  menu -> setFont ( f )             ;
  for (int i=0;i<menus.count();i++) {
    menus[i]->setFont(f)            ;
  }                                 ;
}

void N::MenuManager::setFont(Plan * plan)
{
  setFont ( plan -> fonts [ N::Fonts::Menu ] ) ;
}

QActionGroup * N::MenuManager::group(int Id)
{
  if ( ! actionGroups . contains ( Id ) ) return NULL ;
  return actionGroups [ Id ]                          ;
}

int N::MenuManager::setGroup(int Id,QActionGroup * group)
{
  actionGroups [ Id ]  = group ;
  return Id                    ;
}

QWidget * N::MenuManager::widget(int Id)
{
  if (!Widgets.contains(Id)) return NULL ;
  return Widgets [ Id ]                  ;
}




"""
