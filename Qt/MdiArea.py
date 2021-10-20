# -*- coding: utf-8 -*-
##############################################################################
## MdiArea
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
from   random                         import randint
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
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QActionGroup
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QMdiArea
##############################################################################
from         . VirtualGui             import VirtualGui   as VirtualGui
from         . MdiSubWindow           import MdiSubWindow as MdiSubWindow
##############################################################################
class MdiArea         ( QMdiArea , VirtualGui                              ) :
  ############################################################################
  def __init__        ( self , parent = None , plan = None                 ) :
    ##########################################################################
    super ( QMdiArea  , self ) . __init__ ( parent                           )
    super ( VirtualGui, self ) . __init__ (                                  )
    self . Initialize                     ( self                             )
    self . setPlanFunction                ( plan                             )
    self . setAttribute                   ( Qt . WA_InputMethodEnabled       )
    ##########################################################################
    self . setViewMode                    ( self . SubWindowView             )
    self . setHorizontalScrollBarPolicy   ( Qt . ScrollBarAlwaysOff          )
    self . setVerticalScrollBarPolicy     ( Qt . ScrollBarAlwaysOff          )
    self . setAcceptDrops                 ( True                             )
    ##########################################################################
    self . menu          = None
    self . group         = None
    ##########################################################################
    self . styleMenu     = None
    self . subWindow     = None
    self . tabbedAction  = None
    self . cascadeAction = None
    self . tiledAction   = None
    self . closeAll      = None
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                           (                                      )
  def FileAboutToShow                 ( self                               ) :
    ##########################################################################
    swlists    = self . subWindowList (                                      )
    ne         =                      ( len ( swlists ) > 0                  )
    ##########################################################################
    self . closeAll . setEnabled      ( ne                                   )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                             (                                    )
  def StyleAboutToShow                  ( self                             ) :
    ##########################################################################
    p          = self . GetPlan         (                                    )
    if                                  ( p == None                        ) :
      return
    ##########################################################################
    atMdi      = False
    stacked    = p    . getStacked      (                                    )
    if                                  ( stacked != None                  ) :
      CI       = stacked . currentIndex (                                    )
      WW       = stacked . widget       ( CI                                 )
      if                                ( WW == self                       ) :
        atMdi  = True
    ##########################################################################
    swlists    = self . subWindowList   (                                    )
    ne         =                        ( len ( swlists ) > 0                )
    ##########################################################################
    sSub       = False
    sTab       = False
    ##########################################################################
    if                                  ( atMdi                            ) :
      vm       = self . viewMode        (                                    )
      isSub    =                        ( vm == self . SubWindowView         )
      ########################################################################
      if                                ( isSub                            ) :
        sTab   = True
      else                                                                   :
        sSub   = True
        ne     = False
    ##########################################################################
    self . subWindow     . setEnabled   ( sSub                               )
    self . tabbedAction  . setEnabled   ( sTab                               )
    self . cascadeAction . setEnabled   ( ne                                 )
    self . tiledAction   . setEnabled   ( ne                                 )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem               ( self                                     , \
                                  menu                                     , \
                                  fileMenu                                 , \
                                  subwin                                   , \
                                  tabbed                                   , \
                                  cascade                                  , \
                                  tile                                     , \
                                  closeAll                                 ) :
    ##########################################################################
    self . styleMenu     = menu
    self . subWindow     = subwin
    self . tabbedAction  = tabbed
    self . cascadeAction = cascade
    self . tiledAction   = tile
    self . closeAll      = closeAll
    ##########################################################################
    self . styleMenu  . aboutToShow . connect ( self . StyleAboutToShow      )
    fileMenu          . aboutToShow . connect ( self . FileAboutToShow       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def MenuAboutToShow           ( self                                     ) :
    ##########################################################################
    self . AttachMenu           ( self . menu , self . group                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     ( QAction                                    )
  def WindowActionWidget        ( self , action                            ) :
    ##########################################################################
    w    = action . data        (                                            )
    ##########################################################################
    if                          ( w == None                                ) :
      return
    ##########################################################################
    self . setActiveSubWindow   ( w                                          )
    ##########################################################################
    s    = w . widget           (                                            )
    msg  = s . windowTitle      (                                            )
    self . Go                   ( self . Talk                              , \
                                  ( msg , self . getLocality ( ) , )         )
    ##########################################################################
    return
  ############################################################################
  def PrepareMenu               ( self , menu                              ) :
    ##########################################################################
    self . menu  = menu
    self . group = QActionGroup ( menu                                       )
    ##########################################################################
    self . menu  . aboutToShow . connect ( self . MenuAboutToShow            )
    self . group . triggered   . connect ( self . WindowActionWidget         )
    ##########################################################################
    self . AttachMenu           ( self . menu , self . group                 )
    ##########################################################################
    return
  ############################################################################
  def AttachMenu                     ( self , menu , group                 ) :
    ##########################################################################
    menu    . clear                  (                                       )
    ##########################################################################
    asw     = self . activeSubWindow (                                       )
    swlists = self . subWindowList   (                                       )
    ##########################################################################
    for w in swlists                                                         :
      ########################################################################
      s     = w    . widget       (                                          )
      a     = menu . addAction    ( s . windowTitle  ( )                     )
      a     . setData             ( w                                        )
      a     . setCheckable        ( True                                     )
      ########################################################################
      if                          ( w == asw                               ) :
        a   . setChecked          ( True                                     )
      ########################################################################
      group . addAction           ( a                                        )
    ##########################################################################
    return
  ############################################################################
  def Subwindow               ( self                                       ) :
    ##########################################################################
    self . setViewMode        ( self . SubWindowView                         )
    ## MenuStatus  (             )
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def Tabbed                  ( self                                       ) :
    ##########################################################################
    self . setViewMode        ( self . TabbedView                            )
    ## MenuStatus  (          ) ;
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def Tile                    ( self                                       ) :
    ##########################################################################
    self . tileSubWindows     (                                              )
    ## MenuStatus     ( ) ;
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def Cascade                 ( self                                       ) :
    ##########################################################################
    self . cascadeSubWindows  (                                              )
    ## MenuStatus         ( ) ;
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def CloseAll                ( self                                       ) :
    ##########################################################################
    self . closeAllSubWindows (                                              )
    ## MenuStatus         ( ) ;
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def append             ( self , widget                                   ) :
    ##########################################################################
    msw  = MdiSubWindow  (                                                   )
    msw  . setWidget     ( widget                                            )
    msw  . setAttribute  ( Qt . WA_DeleteOnClose                             )
    msw  . setAttribute  ( Qt . WA_InputMethodEnabled                        )
    self . addSubWindow  ( msw                                               )
    ##########################################################################
    return msw
  ############################################################################
  def Attach                   ( self , widget , direction                 ) :
    ##########################################################################
    msw    = self . append     ( widget                                      )
    ## msw->setFont(plan->fonts[N::Fonts::Default])
    ##########################################################################
    mw     = self   . geometry (                                             )
    sh     = widget . sizeHint (                                             )
    gw     = QSize             (                                             )
    sp     = QPoint            (                                             )
    ##########################################################################
    if                         ( direction == 0                            ) :
      ########################################################################
      gw   = widget . size     (                                             )
      sp   . setX ( ( ( mw . width ()-gw.width ())/16) * (randint(0,200)%16) )
      sp   . setY ( ( ( mw . height()-gw.height())/16) * (randint(0,200)%16) )
      ########################################################################
      if                       ( gw . width ( ) < sh . width ( )           ) :
        gw . setWidth          ( sh . width ( )                              )
      ########################################################################
      if                       ( gw . height ( ) < sh . height ( ) ) :
        gw . setHeight         ( sh . height ( ) )
      ########################################################################
    elif                       ( direction == Qt . Vertical ) :
      ########################################################################
      sp   . setX ( ( mw . width ( ) / 16 ) * ( randint ( 0 , 200 ) % 10 )   )
      sp   . setY              ( 0                                           )
      gw   . setWidth          ( mw . width  ( ) / 5                         )
      gw   . setHeight         ( mw . height ( )                             )
      ########################################################################
      if                       ( gw . width ( ) < sh . width ( )           ) :
        gw . setWidth          ( sh . width ( )                              )
      ########################################################################
    elif                       ( direction == Qt . Horizontal              ) :
      ########################################################################
      sp   . setX              ( 0                                           )
      sp   . setY ( ( mw . height ( ) / 16 ) * ( randint ( 0 , 200 ) % 8 )   )
      gw   . setWidth          ( mw . width  ( )                             )
      gw   . setHeight         ( mw . height ( ) / 3                         )
      ########################################################################
      if                       ( gw . height ( ) < sh . height ( )         ) :
        gw . setHeight         ( sh . height ( )                             )
    ##########################################################################
    msw    . move              ( sp                                          )
    msw    . resize            ( gw                                          )
    msw    . setWindowIcon     ( widget . windowIcon ( )                     )
    ## MenuStatus   ( )
    self   . update            (                                             )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################

"""

N::MdiArea:: MdiArea     (QWidget * parent,Plan * p     )
           : QMdiArea    (          parent              )
           , VirtualGui  (          this  ,       p     )
           , Thread      (          0     ,       false )
           , WindowLists (NULL                          )
{
  WidgetClass                   ;
  addIntoWidget ( parent,this ) ;
  Configure     (             ) ;
}

void N::MdiArea::focusInEvent(QFocusEvent * event)
{
  if (!focusIn (event))            {
    QMdiArea::focusInEvent (event) ;
  }                                ;
  MenuStatus ( )                   ;
}

void N::MdiArea::focusOutEvent(QFocusEvent * event)
{
  if (!focusOut(event))            {
    QMdiArea::focusOutEvent(event) ;
  }                                ;
  MenuStatus ( )                   ;
}

void N::MdiArea::contextMenuEvent(QContextMenuEvent * event)
{
  if (Menu(event->pos())) event->accept(); else
  QMdiArea::contextMenuEvent(event)           ;
}

void N::MdiArea::dragEnterEvent(QDragEnterEvent * event)
{
  if (dragEnter(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QMdiArea::dragEnterEvent(event)        ;
    else event->ignore()                                     ;
  }                                                          ;
}

void N::MdiArea::dragLeaveEvent(QDragLeaveEvent * event)
{
  if (removeDrop()) event->accept() ; else            {
    if (PassDragDrop) QMdiArea::dragLeaveEvent(event) ;
    else event->ignore()                              ;
  }                                                   ;
}

void N::MdiArea::dragMoveEvent(QDragMoveEvent * event)
{
  if (dragMove(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QMdiArea::dragMoveEvent(event)        ;
    else event->ignore()                                    ;
  }                                                         ;
}

void N::MdiArea::dropEvent(QDropEvent * event)
{
  if (drop(event)) event->acceptProposedAction() ; else {
    if (PassDragDrop) QMdiArea::dropEvent(event)        ;
    else event->ignore()                                ;
  }                                                     ;
}

bool N::MdiArea::acceptDrop(QWidget * source,const QMimeData * mime)
{
  Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  return true         ;
}

bool N::MdiArea::dropNew(QWidget * source,const QMimeData * mime,QPoint pos)
{
  Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  Q_UNUSED ( pos    ) ;
  return true         ;
}

bool N::MdiArea::dropMoving(QWidget * source,const QMimeData * mime,QPoint pos)
{
  Q_UNUSED ( source ) ;
  Q_UNUSED ( mime   ) ;
  Q_UNUSED ( pos    ) ;
  return true         ;
}

bool N::MdiArea::dropAppend(QWidget * source,const QMimeData * mime,QPoint pos)
{
  return dropItems ( source , mime , pos ) ;
}

void N::MdiArea::Connect(QWidget * widget)
{
  nConnect ( widget , SIGNAL(Adjustment(QWidget*,QSize))   ,
             this   , SLOT  (Adjustment(QWidget*,QSize)) ) ;
  nConnect ( widget , SIGNAL(Adjustment(QWidget*      ))   ,
             this   , SLOT  (Adjustment(QWidget*      )) ) ;
  nConnect ( widget , SIGNAL(Leave     (QWidget*      ))   ,
             this   , SLOT  (Leave     (QWidget*      )) ) ;
}

void N::MdiArea::Adjustment(QWidget * widget,QSize size)
{
  QMdiSubWindow * msw = Casting(QMdiSubWindow,widget)                   ;
  if (IsNull(msw)) return                                               ;
  QSize ws = size                                                       ;
  QRect mw = geometry()                                                 ;
  QSize wm = QSize(mw.width(),mw.height())                              ;
  QRect fg = msw->frameGeometry()                                       ;
  QRect wg = msw->geometry()                                            ;
  QSize ms = QSize(fg.width(),fg.height())                              ;
  QSize ds = QSize(wg.width(),wg.height())                              ;
  ms -= ds                                                              ;
  ms += ws                                                              ;
  wm -= ms                                                              ;
  ds  = QSize((wm.width()*(rand()%16)/16),(wm.height()*(rand()%16)/16)) ;
  if (ds.width ()<0) ds.setWidth (0)                                    ;
  if (ds.height()<0) ds.setHeight(0)                                    ;
  msw->move(ds.width(),ds.height())                                     ;
  msw->resize(ms)                                                       ;
  msw->setWindowIcon(widget->windowIcon())                              ;
  MenuStatus ( )                                                        ;
  update     ( )                                                        ;
}

void N::MdiArea::Adjustment(QWidget * widget)
{
  QMdiSubWindow * msw = Casting(QMdiSubWindow,widget)                   ;
  if (IsNull(msw)) return                                               ;
  QSize ws = widget -> size ( )                                         ;
  QRect mw = geometry()                                                 ;
  QSize wm = QSize(mw.width(),mw.height())                              ;
  QRect fg = msw->frameGeometry()                                       ;
  QRect wg = msw->geometry()                                            ;
  QSize ms = QSize(fg.width(),fg.height())                              ;
  QSize ds = QSize(wg.width(),wg.height())                              ;
  ms -= ds                                                              ;
  ms += ws                                                              ;
  wm -= ms                                                              ;
  ds  = QSize((wm.width()*(rand()%16)/16),(wm.height()*(rand()%16)/16)) ;
  if (ds.width ()<0) ds.setWidth (0)                                    ;
  if (ds.height()<0) ds.setHeight(0)                                    ;
  msw->move(ds.width(),ds.height())                                     ;
  msw->resize(ms)                                                       ;
  msw->setWindowIcon(widget->windowIcon())                              ;
  MenuStatus ( )                                                        ;
  update     ( )                                                        ;
}

void N::MdiArea::Leave(QWidget * widget)
{ Q_UNUSED          ( widget ) ;
  MenuStatus        (        ) ;
  update            (        ) ;
  emit childChanged (        ) ;
}

void N::MdiArea::Fit(QWidget * widget)
{
  QSize ws = widget->size()                                             ;
  QMdiSubWindow * msw = append(widget)                                  ;
  msw->setFont(plan->fonts[N::Fonts::Default])                          ;
  QRect mw = geometry()                                                 ;
  QSize wm = QSize(mw.width(),mw.height())                              ;
  QRect fg = msw->frameGeometry()                                       ;
  QRect wg = msw->geometry()                                            ;
  QSize ms = QSize(fg.width(),fg.height())                              ;
  QSize ds = QSize(wg.width(),wg.height())                              ;
  ms -= ds                                                              ;
  ms += ws                                                              ;
  wm -= ms                                                              ;
  ds  = QSize((wm.width()*(rand()%16)/16),(wm.height()*(rand()%16)/16)) ;
  if (ds.width ()<0) ds.setWidth (0)                                    ;
  if (ds.height()<0) ds.setHeight(0)                                    ;
  msw->move(ds.width(),ds.height())                                     ;
  msw->resize(ms)                                                       ;
  msw->setWindowIcon(widget->windowIcon())                              ;
  MenuStatus ( )                                                        ;
  update     ( )                                                        ;
}

void N::MdiArea::subActivated(QMdiSubWindow * window)
{
  if (IsNull(window)) emit lastClosed() ;
  MenuStatus ()                         ;
  update     ()                         ;
}

bool N::MdiArea::contains(QString accName)
{
  QList<QMdiSubWindow *> subws = subWindowList()   ;
  QMdiSubWindow       *  subw                      ;
  foreach (subw,subws)                             {
    if (subw->widget()->accessibleName()==accName) {
      return true                                  ;
    }                                              ;
  }                                                ;
  return false                                     ;
}

QWidget * N::MdiArea::findWidget(QString accName)
{
  QList<QMdiSubWindow *> subws = subWindowList()   ;
  QMdiSubWindow       *  subw                      ;
  foreach (subw,subws)                             {
    if (subw->widget()->accessibleName()==accName) {
      return subw->widget()                        ;
    }                                              ;
  }                                                ;
  return NULL                                      ;
}

QList<QWidget *> N::MdiArea::getWidgets(QString accName)
{
  QList<QWidget       *> Widgets                   ;
  QList<QMdiSubWindow *> subws = subWindowList()   ;
  QMdiSubWindow       *  subw                      ;
  foreach (subw,subws)                             {
    if (subw->widget()->accessibleName()==accName) {
      Widgets << subw->widget()                    ;
    }                                              ;
  }                                                ;
  return Widgets                                   ;
}

void N::MdiArea::Configure(void)
{
  setViewMode                  ( SubWindowView                      ) ;
  setAttribute                 ( Qt::WA_InputMethodEnabled          ) ;
  setHorizontalScrollBarPolicy ( Qt::ScrollBarAlwaysOff             ) ;
  setVerticalScrollBarPolicy   ( Qt::ScrollBarAlwaysOff             ) ;
  setAcceptDrops               ( true                               ) ;
  setDropFlag                  ( DropUrls , true                    ) ;
  /////////////////////////////////////////////////////////////////////
  Shadow = new QGraphicsDropShadowEffect ( this )                     ;
  setGraphicsEffect ( Shadow )                                        ;
  Shadow -> setBlurRadius ( 3                     )                   ;
  Shadow -> setColor      ( QColor  (224,224,224) )                   ;
  Shadow -> setOffset     ( QPointF (  3,  3    ) )                   ;
  Shadow -> setEnabled    ( true                  )                   ;
  /////////////////////////////////////////////////////////////////////
  addConnector  ( "Activated"                                         ,
                  this , SIGNAL(subWindowActivated(QMdiSubWindow*))   ,
                  this , SLOT  (subActivated      (QMdiSubWindow*)) ) ;
  addConnector  ( "Commando"                                          ,
                  Commando                                            ,
                  SIGNAL ( timeout      ( ) )                         ,
                  this                                                ,
                  SLOT   ( DropCommands ( ) )                       ) ;
  onlyConnector ( "Activated"                                       ) ;
  onlyConnector ( "Commando"                                        ) ;
  /////////////////////////////////////////////////////////////////////
  if ( NotNull ( plan ) )                                             {
    Data . Controller = & ( plan->canContinue )                       ;
  }                                                                   ;
}

bool N::MdiArea::dropUrls(QWidget * source,QPointF pos,const QList<QUrl> & urls)
{ Q_UNUSED  ( source ) ;
  Q_UNUSED  ( pos    ) ;
  emit Files( urls   ) ;
  return true          ;
}

bool N::MdiArea::Menu(QPoint pos)
{ Q_UNUSED    ( pos       )                                                                        ;
  nScopedMenu ( mm , this )                                                                        ;
  QAction     * aa                                                                                 ;
  QMenu       * me                                                                                 ;
  //////////////////////////////////////////////////////////////////////////////////////////////////
  me = mm . addMenu ( tr("Scroll bar")                                                           ) ;
  mm . add ( me,60001,tr("Horizontal"),true,horizontalScrollBarPolicy() == Qt::ScrollBarAsNeeded ) ;
  mm . add ( me,60002,tr("Vertical"  ),true,verticalScrollBarPolicy  () == Qt::ScrollBarAsNeeded ) ;
  //////////////////////////////////////////////////////////////////////////////////////////////////
  mm . setFont ( plan                )                                                             ;
  aa = mm.exec (                     )                                                             ;
  nKickOut     ( IsNull(aa) , true   )                                                             ;
  //////////////////////////////////////////////////////////////////////////////////////////////////
  switch ( mm [ aa ] )                                                                             {
    case 60001                                                                                     :
      if ( aa->isChecked() ) setHorizontalScrollBarPolicy ( Qt::ScrollBarAsNeeded  )               ;
                        else setHorizontalScrollBarPolicy ( Qt::ScrollBarAlwaysOff )               ;
    break                                                                                          ;
    case 60002                                                                                     :
      if ( aa->isChecked() ) setVerticalScrollBarPolicy   ( Qt::ScrollBarAsNeeded  )               ;
                        else setVerticalScrollBarPolicy   ( Qt::ScrollBarAlwaysOff )               ;
    break                                                                                          ;
  }                                                                                                ;
  return true                                                                                      ;
}

"""
