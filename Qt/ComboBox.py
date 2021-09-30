# -*- coding: utf-8 -*-
##############################################################################
## ComboBox
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
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QComboBox
##############################################################################
from         . AbstractGui            import AbstractGui as AbstractGui
from         . VirtualGui             import VirtualGui  as VirtualGui
##############################################################################
class ComboBox ( QComboBox , VirtualGui                                    ) :
  ############################################################################
  def __init__ ( self , parent = None , plan = None                        ) :
    ##########################################################################
    super ( QComboBox   , self ) . __init__        ( parent                  )
    super ( VirtualGui  , self ) . __init__        (                         )
    super ( VirtualGui  , self ) . Initialize      ( self                    )
    super ( AbstractGui , self ) . setPlanFunction ( plan                    )
    ##########################################################################
    return
  ############################################################################
  def addJson              ( self , JSON , currentIndex                    ) :
    ##########################################################################
    index   = 0
    atp     = 0
    KEYs    = JSON . keys  (                                                 )
    for K in KEYs                                                            :
      self . addItem       ( JSON [ K ] , K                                  )
      if                   ( K == currentIndex                             ) :
        atp = index
      index = index + 1
    ##########################################################################
    self . setCurrentIndex ( atp                                             )
    ##########################################################################
    return
##############################################################################



"""




class Q_COMPONENTS_EXPORT ComboBox : public QComboBox
                                   , public VirtualGui
                                   , public Thread
{
  Q_OBJECT
  Q_PROPERTY(bool designable READ canDesign WRITE setDesignable DESIGNABLE true)
  public:

    explicit     ComboBox        (StandardConstructor) ;
    virtual ~    ComboBox        (void               ) ;

    SUID         toUuid          (void) ;
    SUID         toUuid          (int index) ;

  protected:

    virtual void Configure       (void) ;

    virtual void paintEvent      (QPaintEvent     * event) ;

    virtual void focusInEvent    (QFocusEvent     * event) ;
    virtual void focusOutEvent   (QFocusEvent     * event) ;

    virtual void resizeEvent     (QResizeEvent    * event) ;

    virtual void dragEnterEvent  (QDragEnterEvent * event) ;
    virtual void dragLeaveEvent  (QDragLeaveEvent * event) ;
    virtual void dragMoveEvent   (QDragMoveEvent  * event) ;
    virtual void dropEvent       (QDropEvent      * event) ;

    virtual bool acceptDrop      (nDeclWidget,const QMimeData * mime);
    virtual bool dropNew         (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropMoving      (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropAppend      (nDeclWidget,const QMimeData * mime,QPoint pos);

    virtual bool dropFont        (nDeclWidget,QPointF pos,const SUID font ) ;
    virtual bool dropPen         (nDeclWidget,QPointF pos,const SUID pen  ) ;
    virtual bool dropBrush       (nDeclWidget,QPointF pos,const SUID brush) ;

    virtual void assignFont      (Font  & font ) ;
    virtual void assignPen       (Pen   & pen  ) ;
    virtual void assignBrush     (Brush & brush) ;

    virtual void run             (int Type,ThreadData * data) ;

  private:

  public slots:

    virtual void appendNames     (NAMEs & names) ;
    virtual void appendNames     (UUIDs & uuids,NAMEs & names) ;
    virtual void addItems        (UUIDs Uuids) ;
    virtual void addItems        (SqlConnection & Connection,UUIDs & Uuids) ;
    virtual void addItems        (QString table,enum Qt::SortOrder sorting) ;
    virtual void addGroups       (SUID group                                        ,
                                  int  t1                                           ,
                                  int  t2                                           ,
                                  int  relation                                     ,
                                  enum Qt::SortOrder sorting = Qt::AscendingOrder ) ;
    virtual void addDivision     (int  type                                         ,
                                  enum Qt::SortOrder sorting = Qt::AscendingOrder ) ;
    virtual void pendItems       (UUIDs Uuids) ;
    virtual void pendItems       (QString table,enum Qt::SortOrder sorting) ;
    virtual void pendGroups      (SUID group                                        ,
                                  int  t1                                           ,
                                  int  t2                                           ,
                                  int  relation                                     ,
                                  enum Qt::SortOrder sorting = Qt::AscendingOrder ) ;
    virtual void pendDivision    (int  type                                         ,
                                  enum Qt::SortOrder sorting = Qt::AscendingOrder ) ;

  protected slots:

    virtual void DropCommands    (void) ;

  private slots:

  signals:

    void assignNames             (NAMEs & names) ;

};

N::ComboBox:: ComboBox   ( QWidget * parent , Plan * p     )
            : QComboBox  (           parent                )
            , VirtualGui (           this   ,        p     )
            , Thread     (           0      ,        false )
{
  WidgetClass   ;
  Configure ( ) ;
}

N::ComboBox::~ComboBox(void)
{
}

SUID N::ComboBox::toUuid(void)
{
  return toUuid ( currentIndex ( ) ) ;
}

SUID N::ComboBox::toUuid(int index)
{
  return itemData ( index ) . toULongLong ( ) ;
}

void N::ComboBox::Configure(void)
{
  setAttribute   ( Qt::WA_InputMethodEnabled   ) ;
  setAcceptDrops ( true                        ) ;
  setDropFlag    ( DropFont  , true            ) ;
  setDropFlag    ( DropPen   , true            ) ;
  setDropFlag    ( DropBrush , true            ) ;
  addConnector   ( "AssignName"                  ,
                   this                          ,
                   SIGNAL(assignNames(NAMEs&))   ,
                   this                          ,
                   SLOT  (appendNames(NAMEs&)) ) ;
  addConnector   ( "Commando"                    ,
                   Commando                      ,
                   SIGNAL ( timeout      ( ) )   ,
                   this                          ,
                   SLOT   ( DropCommands ( ) ) ) ;
  onlyConnector  ( "AssignName"                ) ;
  onlyConnector  ( "Commando"                  ) ;
  ////////////////////////////////////////////////
  if ( NotNull ( plan ) )                        {
    Data . Controller = & ( plan->canContinue  ) ;
  }                                              ;
}

void N::ComboBox::paintEvent(QPaintEvent * event)
{
  nIsolatePainter ( QComboBox ) ;
}

void N::ComboBox::focusInEvent(QFocusEvent * event)
{
  if (!focusIn (event)) QComboBox::focusInEvent (event) ;
}

void N::ComboBox::focusOutEvent(QFocusEvent * event)
{
  if (!focusOut(event)) QComboBox::focusOutEvent(event) ;
}

void N::ComboBox::resizeEvent(QResizeEvent * event)
{
  QComboBox :: resizeEvent ( event ) ;
}

void N::ComboBox::dragEnterEvent(QDragEnterEvent * event)
{
  if (dragEnter(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QComboBox::dragEnterEvent(event)       ;
    else event->ignore()                                     ;
  }                                                          ;
}

void N::ComboBox::dragLeaveEvent(QDragLeaveEvent * event)
{
  if (removeDrop()) event->accept() ; else             {
    if (PassDragDrop) QComboBox::dragLeaveEvent(event) ;
    else event->ignore()                               ;
  }                                                    ;
}

void N::ComboBox::dragMoveEvent(QDragMoveEvent * event)
{
  if (dragMove(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QComboBox::dragMoveEvent(event)       ;
    else event->ignore()                                    ;
  }                                                         ;
}

void N::ComboBox::dropEvent(QDropEvent * event)
{
  if (drop(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QComboBox::dropEvent(event)       ;
    else event->ignore()                                ;
  }                                                     ;
}

bool N::ComboBox::acceptDrop(QWidget * source,const QMimeData * mime)
{ Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  return false        ;
}

bool N::ComboBox::dropNew(QWidget * source,const QMimeData * mime,QPoint pos)
{ Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  Q_UNUSED ( pos    ) ;
  return true         ;
}

bool N::ComboBox::dropMoving(QWidget * source,const QMimeData * mime,QPoint pos)
{ Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  Q_UNUSED ( pos    ) ;
  return true         ;
}

bool N::ComboBox::dropAppend(QWidget * source,const QMimeData * mime,QPoint pos)
{
  return dropItems ( source , mime , pos ) ;
}

bool N::ComboBox::dropFont(QWidget * source,QPointF pos,const SUID font)
{ Q_UNUSED           ( source               ) ;
  Q_UNUSED           ( pos                  ) ;
  nKickOut           ( IsNull(plan) , false ) ;
  Font            f                           ;
  GraphicsManager GM ( plan                 ) ;
  EnterSQL           ( SC , plan->sql       ) ;
    f = GM.GetFont   ( SC , font            ) ;
  LeaveSQL           ( SC , plan->sql       ) ;
  assignFont         ( f                    ) ;
  return true                                 ;
}

bool N::ComboBox::dropPen(QWidget * source,QPointF pos,const SUID pen)
{ Q_UNUSED           ( source               ) ;
  Q_UNUSED           ( pos                  ) ;
  nKickOut           ( IsNull(plan) , false ) ;
  Pen             p                           ;
  GraphicsManager GM ( plan                 ) ;
  EnterSQL           ( SC , plan->sql       ) ;
    p = GM.GetPen    ( SC , pen             ) ;
  LeaveSQL           ( SC , plan->sql       ) ;
  assignPen          ( p                    ) ;
  return true                                 ;
}

bool N::ComboBox::dropBrush(QWidget * source,QPointF pos,const SUID brush)
{ Q_UNUSED           ( source               ) ;
  Q_UNUSED           ( pos                  ) ;
  nKickOut           ( IsNull(plan) , false ) ;
  Brush           b                           ;
  GraphicsManager GM ( plan                 ) ;
  EnterSQL           ( SC , plan->sql       ) ;
    b = GM.GetBrush  ( SC , brush           ) ;
  LeaveSQL           ( SC , plan->sql       ) ;
  assignBrush        ( b                    ) ;
  return true                                 ;
}

void N::ComboBox::DropCommands(void)
{
  LaunchCommands ( ) ;
}

void N::ComboBox::assignFont(Font & f)
{
  QComboBox::setFont ( f ) ;
}

void N::ComboBox::assignPen(Pen & p)
{ Q_UNUSED ( p ) ;
}

void N::ComboBox::assignBrush(Brush & b)
{
  QBrush   B   = b                                ;
  QPalette P   = palette (                      ) ;
  P . setBrush           ( QPalette::Base , B   ) ;
  setPalette             ( P                    ) ;
}

void N::ComboBox::appendNames(NAMEs & names)
{
  N :: AddItems ( ME , names ) ;
}

void N::ComboBox::appendNames(UUIDs & uuids,NAMEs & names)
{
  SUID u                     ;
  foreach   ( u , uuids    ) {
    addItem ( names[u] , u ) ;
  }                          ;
}

void N::ComboBox::addItems(SqlConnection & SC,UUIDs & Uuids)
{
  SUID  uuid                                                            ;
  foreach (uuid,Uuids)                                                  {
    QString name = SC.getName(PlanTable(Names),"uuid",vLanguageId,uuid) ;
    addItem ( name , uuid )                                             ;
  }                                                                     ;
}

void N::ComboBox::addItems(UUIDs Uuids)
{
  SqlConnection SC(plan->sql)         ;
  if (SC.open("ComboBox","addItems")) {
    addItems ( SC , Uuids )           ;
    SC.close (            )           ;
  }                                   ;
  SC.remove()                         ;
}

void N::ComboBox::addItems(QString table,enum Qt::SortOrder sorting)
{
  SqlConnection SC(plan->sql)                  ;
  if (SC.open("ComboBox","addItems"))          {
    UUIDs Uuids = SC.Uuids                     (
                    table                      ,
                    "uuid"                     ,
                    SC.OrderBy("id",sorting) ) ;
    addItems ( SC , Uuids )                    ;
    SC.close (            )                    ;
  }                                            ;
  SC.remove()                                  ;
}

void N::ComboBox::addGroups       (
       SUID group                 ,
       int  t1                    ,
       int  t2                    ,
       int  relation              ,
       enum Qt::SortOrder sorting )
{
  GroupItems    GI ( plan        )         ;
  SqlConnection SC ( plan -> sql )         ;
  if (SC.open("ComboBox","addGroups"))     {
    UUIDs U                                ;
    U = GI . Subordination                 (
          SC                               ,
          group                            ,
          t1                               ,
          t2                               ,
          relation                         ,
          SC.OrderBy("position",sorting) ) ;
    addItems ( SC , U )                    ;
    SC.close (        )                    ;
  }                                        ;
  SC.remove()                              ;
}

void N::ComboBox::addDivision(int type,enum Qt::SortOrder sorting)
{
  GroupItems    GI ( plan        )       ;
  SqlConnection SC ( plan -> sql )       ;
  if (SC.open("ComboBox","addDivision")) {
    UUIDs U                              ;
    U = GI . Groups                      (
          SC                             ,
          (Types::ObjectTypes)type       ,
          SC.OrderBy("id",sorting)    )  ;
    addItems ( SC , U )                  ;
    SC.close (        )                  ;
  }                                      ;
  SC.remove()                            ;
}

void N::ComboBox::pendItems(UUIDs U)
{
  VarArgs V            ;
  V << U.count()       ;
  toVariants ( U , V ) ;
  start ( 10001 , V )  ;
}

void N::ComboBox::pendItems(QString table,enum Qt::SortOrder sorting)
{
  VarArgs V           ;
  V << table          ;
  V << (int)sorting   ;
  start ( 10002 , V ) ;
}

void N::ComboBox::pendGroups      (
       SUID group                 ,
       int  t1                    ,
       int  t2                    ,
       int  relation              ,
       enum Qt::SortOrder sorting )
{
  VarArgs V           ;
  V << group          ;
  V << t1             ;
  V << t2             ;
  V << relation       ;
  V << (int)sorting   ;
  start ( 10003 , V ) ;
}

void N::ComboBox::pendDivision(int type,enum Qt::SortOrder sorting)
{
  VarArgs V           ;
  V << type           ;
  V << (int)sorting   ;
  start ( 10004 , V ) ;
}

void N::ComboBox::run(int Type,ThreadData * data)
{
  UUIDs   U                            ;
  VarArgs V = data->Arguments          ;
  int     t                            ;
  switch ( Type )                      {
    case 10001                         :
      startLoading ( )                 ;
      t = V [ 0 ] . toInt ( )          ;
      for (int i=1;i<=t;i++)           {
        U << V [ i ] . toULongLong ( ) ;
      }                                ;
      addItems ( U )                   ;
      stopLoading  ( )                 ;
    break                              ;
    case 10002                         :
      startLoading ( )                 ;
      t = V [ 1 ] .toInt()             ;
      addItems                         (
        V [ 0 ] .toString()            ,
        (enum Qt::SortOrder)t        ) ;
      stopLoading  ( )                 ;
    break                              ;
    case 10003                         :
      startLoading ( )                 ;
      t = V [ 4 ] .toInt()             ;
      addGroups                        (
        V [ 0 ] . toULongLong ( )      ,
        V [ 1 ] . toInt       ( )      ,
        V [ 2 ] . toInt       ( )      ,
        V [ 3 ] . toInt       ( )      ,
        (enum Qt::SortOrder)t        ) ;
      stopLoading  ( )                 ;
    break                              ;
    case 10004                         :
      startLoading ( )                 ;
      t = V [ 1 ] .toInt()             ;
      addDivision                      (
        V[0].toInt()                   ,
        (enum Qt::SortOrder)t )        ;
      stopLoading  ( )                 ;
    break                              ;
  }                                    ;
}




"""



