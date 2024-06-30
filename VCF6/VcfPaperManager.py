# -*- coding: utf-8 -*-
##############################################################################
## VcfPaperManager
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
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
##############################################################################
class VcfPaperManager (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################
"""
class Q_COMPONENTS_EXPORT VcfPaperManager
{
  public:

    Plan              *  paperPlan ;
    VcfPaperConf         paperConf ;
    QList<VcfPaper    *> papers    ;
    QList<VcfRuler    *> rulers    ;
    QList<VcfGrid     *> grids     ;
    QMap<int,VcfPaper *> pages     ;
    QMap<int,QString   > tables    ;
    QRectF               range     ;

    explicit VcfPaperManager (Plan * plan = NULL) ;
    virtual ~VcfPaperManager (void) ;

    void   ClearPapers       (void) ;
    QRectF CalculateRange    (void) ;
    QRectF CalculateView     (void) ;
    void   ClearRulers       (void) ;

    bool Add                 (QGraphicsView * View,QGraphicsScene * Scene,VcfOptions * Options,const char * method,PaperArrangement * Arrangement) ;
    void AddPaper            (QGraphicsView * view,QGraphicsScene * scene,VcfOptions * options,const char * method) ;
    bool Default             (QGraphicsView * View,QGraphicsScene * Scene,VcfOptions * Options,const char * method) ;
    int  AddGrid             (QGraphicsView * View,QGraphicsScene * Scene,VcfOptions * Options,QRectF Range);
    bool contains            (QGraphicsItem * item) ;

    #ifndef Q_OS_IOS
    QPrinter * PrintFile     (QWidget * widget,QString caption,QString filepath,QString filters);
    QRectF     startPage     (QPrinter * printer,int PageId);
    bool       endPage       (QPrinter * printer,int PageId);
    #endif

    VcfGrid  * CreateGrid    (QGraphicsView * View,QGraphicsScene * Scene,VcfOptions * Options,QRectF Range);
    virtual void PapersMenu  (QGraphicsView * View,const char * method) ;

  protected:

    VcfPaper * CreatePaper(
            int              dpi       ,
            QGraphicsView  * view      ,
            QGraphicsScene * scene     ,
            VcfOptions     * Options   ,
            const char     * method    ,
            int              direction ,
            QString          name      ,
            QString          paperSpec ,
            QPointF          Start     ,
            DMAPs            Borders ) ;

    void CreatePapers        (int dpi,QGraphicsView * View,QGraphicsScene * Scene,VcfOptions * Options,const char * method,int X,int Y,int Direction,QString paperSpec,DMAPs Borders);
    void CreateRulers        (int dpi,QGraphicsView * View,QGraphicsScene * Scene,VcfOptions * Options);

  private:

    #ifndef Q_OS_IOS
    QPrinter::PaperSize   paperSize        (QString name);
    QPrinter::Orientation paperOrientation (int orientation);
    #endif

};

N::VcfPaperManager:: VcfPaperManager (Plan *        p)
                   : paperPlan       (              p)
                   , range           (QRectF(0,0,0,0))
{
}

N::VcfPaperManager::~VcfPaperManager(void)
{
}

bool N::VcfPaperManager::contains(QGraphicsItem * item)
{
  bool checkIt = false                                  ;
  if (item->type()==VCF::Paper) checkIt = true          ;
  if (item->type()==VCF::Ruler) checkIt = true          ;
  if (!checkIt) return false                            ;
  VcfPaper * gpp = qgraphicsitem_cast<VcfPaper *>(item) ;
  VcfRuler * gpr = qgraphicsitem_cast<VcfRuler *>(item) ;
  if (papers.contains(gpp)) return true                 ;
  if (rulers.contains(gpr)) return true                 ;
  return false                                          ;
}

void N::VcfPaperManager::ClearPapers(void)
{
  for (int i=0;i<papers.count();i++) papers[i]->deleteLater() ;
  for (int i=0;i<rulers.count();i++) rulers[i]->deleteLater() ;
  for (int i=0;i<grids .count();i++) grids [i]->deleteLater() ;
  papers . clear()                                            ;
  rulers . clear()                                            ;
  grids  . clear()                                            ;
  pages  . clear()                                            ;
}

void N::VcfPaperManager::ClearRulers(void)
{
  for (int i=0;i<rulers.count();i++) {
    rulers[i]->deleteLater()         ;
  }                                  ;
  rulers . clear ( )                 ;
}

QRectF N::VcfPaperManager::CalculateRange(void)
{
  QRectF V (0,0,0,0)                              ;
  if (papers.count()>0)                           {
    QRectF R = papers[0]->ScreenRect              ;
    for (int i=1;i<papers.count();i++)            {
      QRectF P = papers[i]->ScreenRect            ;
      P = papers[i]->mapToScene(P).boundingRect() ;
      if (papers[i]->isVisible()) R = R.united(P) ;
    }                                             ;
    V = R                                         ;
  }                                               ;
  return V                                        ;
}

QRectF N::VcfPaperManager::CalculateView(void)
{
  QRectF V = range                                ;
  if (rulers.count()>0)                           {
    QRectF R = range                              ;
    for (int i=0;i<rulers.count();i++)            {
      QRectF P = rulers[i]->ScreenRect            ;
      P = rulers[i]->mapToScene(P).boundingRect() ;
      if (rulers[i]->isVisible()) R = R.united(P) ;
    }                                             ;
    V = R                                         ;
  }                                               ;
  return V                                        ;
}

N::VcfPaper * N::VcfPaperManager::CreatePaper (
        int              dpi            ,
        QGraphicsView  * view           ,
        QGraphicsScene * scene          ,
        VcfOptions     * Options        ,
        const char     * method         ,
        int              direction      ,
        QString          name           ,
        QString          paperSpec      ,
        QPointF          Start          ,
        DMAPs            Borders        )
{
  VcfPaper * Paper = new VcfPaper(view,NULL,paperPlan)           ;
  QRectF     PR    = paperPlan->paper[paperSpec].rect(direction) ;
  Paper->plan      = paperPlan                                   ;
  Paper->Options   = Options                                     ;
  Paper->Paper     = paperSpec                                   ;
  Paper->DPI       = dpi                                         ;
  Paper->Direction = direction                                   ;
  Paper->Name      = name                                        ;
  Paper->Borders   = Borders                                     ;
  Paper->setMargins ( 1.00 , 1.00 , 1.00 , 1.00 )                ;
  scene->addItem    (Paper)                                      ;
  Paper->setPos     (Start)                                      ;
  Paper->setRect    (PR   )                                      ;
  Paper->setZValue  (0.02f)                                      ;
  Paper->setOpacity (0.25f)                                      ;
  Paper->setFlag    (QGraphicsItem::ItemIsSelectable,true)       ;
  Paper->setAcceptHoverEvents(true)                              ;
  Paper->show       (     )                                      ;
  view->connect                                                  (
    Paper,SIGNAL(Moving     (QString,QPointF,QPointF,QPointF))   ,
    view ,method                                               ) ;
  return Paper                                                   ;
}

bool N::VcfPaperManager::Add          (
       QGraphicsView    * view        ,
       QGraphicsScene   * scene       ,
       VcfOptions       * Options     ,
       const char       * method      ,
       PaperArrangement * arrangement )
{
  arrangement->plan = paperPlan                                 ;
  if (!arrangement->prepare ()                   ) return false ;
  if ( arrangement->exec    ()!=QDialog::Accepted) return false ;
  if (!arrangement->retrieve()                   ) return false ;
  if (!arrangement->store   ()                   ) return false ;
  int              DPI       = arrangement->dpi                 ;
  int              X         = arrangement->paperX              ;
  int              Y         = arrangement->paperY              ;
  int              Direction = arrangement->direction           ;
  QString          PaperSpec = arrangement->paper               ;
  QMap<int,double> Borders                                      ;
  Borders[VcfPaper::Left  ] = 1.00                              ;
  Borders[VcfPaper::Top   ] = 1.00                              ;
  Borders[VcfPaper::Right ] = 1.00                              ;
  Borders[VcfPaper::Bottom] = 1.00                              ;
  ClearPapers ()                                                ;
  CreatePapers                                                  (
    DPI                                                         ,
    view                                                        ,
    scene                                                       ,
    Options                                                     ,
    method                                                      ,
    X                                                           ,
    Y                                                           ,
    Direction                                                   ,
    PaperSpec                                                   ,
    Borders                                                   ) ;
  range = CalculateRange (                                    ) ;
  if (arrangement->rulers)                                      {
    CreateRulers (DPI,view,scene,Options                      ) ;
    range = CalculateView()                                     ;
  }                                                             ;
  return (papers.count()>0)                                     ;
}

void N::VcfPaperManager::AddPaper  (
       QGraphicsView  * view    ,
       QGraphicsScene * scene   ,
       VcfOptions     * options ,
       const char     * method  )
{
  CUIDs   PIDs  = pages.keys()                     ;
  int     Page  = PIDs.count()                     ;
  int     DIRT  = paperConf.direction              ;
  QString PS    = paperConf.paper                  ;
  QRectF  RP    = paperPlan->paper[PS].rect(DIRT)  ;
  QRectF  BP    = paperConf.PaperAt(Page,RP)       ;
  QPointF Start = BP.topLeft()                     ;
  VcfPaper * Paper = CreatePaper                   (
    paperConf.dpi,view,scene,options               ,
    method,paperConf.direction                     ,
    QString::number(Page+1)                        ,
    PS,Start,paperConf.borders                   ) ;
  papers       << Paper                            ;
  pages[Page+1] = Paper                            ;
  ClearRulers ( )                                  ;
  range = CalculateRange (                       ) ;
  CreateRulers (paperPlan->dpi,view,scene,options) ;
  range = CalculateView()                          ;
}

bool N::VcfPaperManager::Default   (
       QGraphicsView  * view    ,
       QGraphicsScene * scene   ,
       VcfOptions     * Options ,
       const char     * method  )
{
  int DPI = paperPlan -> dpi                                                 ;
  QMap<int,double> Borders                                                   ;
  Borders[VcfPaper::Left  ] = 1.00                                           ;
  Borders[VcfPaper::Top   ] = 1.00                                           ;
  Borders[VcfPaper::Right ] = 1.00                                           ;
  Borders[VcfPaper::Bottom] = 1.00                                           ;
  ClearPapers  (                                                           ) ;
  CreatePapers (DPI,view,scene,Options,method,1,1,Qt::Vertical,"A4",Borders) ;
  range = CalculateRange (                                                 ) ;
  CreateRulers (DPI,view,scene,Options                                     ) ;
  range = CalculateView()                                                    ;
  return (papers.count()>0)                                                  ;
}

int N::VcfPaperManager::AddGrid(QGraphicsView * view,QGraphicsScene * scene,VcfOptions * Options,QRectF Range)
{
  VcfGrid * grid = CreateGrid(view,scene,Options,Range) ;
  grids  << grid                                        ;
  return grids.count()                                  ;
}

void N::VcfPaperManager::CreatePapers (
       int              dpi        ,
       QGraphicsView  * view       ,
       QGraphicsScene * scene      ,
       VcfOptions     * Options    ,
       const char     * method     ,
       int              X          ,
       int              Y          ,
       int              Direction  ,
       QString          paperSpec  ,
       DMAPs            Borders    )
{
  int ID = 1                                ;
  QPointF Start(0.0,0.0)                    ;
  QRectF  PaperRect                         ;
  QPointF PR                                ;
  for (int y=0;y<Y;y++)                     {
    for (int x=0;x<X;x++)                   {
      VcfPaper * Paper = CreatePaper        (
        dpi,view,scene,Options,method       ,
        Direction,QString::number(ID)       ,
        paperSpec,Start,Borders           ) ;
      PaperRect = Paper->ScreenRect         ;
      PR . setX (PaperRect.right ())        ;
      PR . setY (PaperRect.bottom())        ;
      PR = paperPlan->toCentimeter(PR,dpi)  ;
      Start.setX(PR.x())                    ;
      papers    << Paper                    ;
      pages[ID]  = Paper                    ;
      ID++                                  ;
    }                                       ;
    PR . setX (PaperRect.right ())          ;
    PR . setY (PaperRect.bottom())          ;
    PR = paperPlan->toCentimeter(PR,dpi)    ;
    Start.setX(1.0)                         ;
    Start.setY(PR.y())                      ;
  }                                         ;
}

N::VcfGrid * N::VcfPaperManager::CreateGrid (
               QGraphicsView  * view        ,
               QGraphicsScene * scene       ,
               VcfOptions     * Options     ,
               QRectF Range                 )
{
  VcfGrid * Grid = new VcfGrid(view,NULL,paperPlan) ;
  Grid  -> plan     = paperPlan                     ;
  Grid  -> Options  = Options                       ;
  scene -> addItem    (Grid )                       ;
  Grid  -> setRange   (range)                       ;
  Grid  -> setZValue  (0.01f)                       ;
  Grid  -> setOpacity (1.00f)                       ;
  Grid  -> CreatePath (     )                       ;
  Grid  -> show       (     )                       ;
  return Grid                                       ;
}

void N::VcfPaperManager::PapersMenu(QGraphicsView * View,const char * method)
{
  for (int i=0;i<papers.count();i++)                         {
    VcfPaper * vp = papers[i]                                ;
    QObject::disconnect(vp  ,SIGNAL(Menu(VcfPaper*,QPointF)) ,
                        NULL,NULL                          ) ;
    QObject::connect   (vp  ,SIGNAL(Menu(VcfPaper*,QPointF)) ,
                        View,method                        ) ;
  }                                                          ;
}

void N::VcfPaperManager::CreateRulers(int dpi,QGraphicsView * view,QGraphicsScene * scene,VcfOptions * Options)
{
  QRectF RX = paperPlan -> toCentimeter ( range , dpi )     ;
  QRectF WR(     -1.00,       0.00,      1.00,RX.height())  ;
  QRectF ER(RX.width(),       0.00,      1.00,RX.height())  ;
  QRectF UR(      0.00,      -1.00,RX.width(),       1.00)  ;
  QRectF DR(      0.00,RX.height(),RX.width(),       1.00)  ;
  ///////////////////////////////////////////////////////////
  VcfRuler * rulerNorth = new VcfRuler(view,NULL)           ;
  rulerNorth->plan    = paperPlan                           ;
  rulerNorth->Options = Options                             ;
  scene     ->addItem   (rulerNorth)                        ;
  rulerNorth->setRange  (UR        )                        ;
  rulerNorth->setZValue (0.10f     )                        ;
  rulerNorth->setOpacity(0.50f     )                        ;
  rulerNorth->direction = North                   ;
  rulerNorth->CreatePath(          )                        ;
  rulerNorth->show      (          )                        ;
  rulers << rulerNorth                                      ;
  ///////////////////////////////////////////////////////////
  VcfRuler * rulerSouth = new VcfRuler(view,NULL)           ;
  rulerSouth->plan    = paperPlan                           ;
  rulerSouth->Options = Options                             ;
  scene     ->addItem   (rulerSouth)                        ;
  rulerSouth->setRange  (DR        )                        ;
  rulerSouth->setZValue (0.10f     )                        ;
  rulerSouth->setOpacity(0.50f     )                        ;
  rulerSouth->direction = South                   ;
  rulerSouth->CreatePath(          )                        ;
  rulerSouth->show      (          )                        ;
  rulers << rulerSouth                                      ;
  ///////////////////////////////////////////////////////////
  VcfRuler * rulerWest = new VcfRuler(view,NULL)            ;
  rulerWest ->plan    = paperPlan                           ;
  rulerWest ->Options = Options                             ;
  scene     ->addItem   (rulerWest)                         ;
  rulerWest ->setRange  (WR       )                         ;
  rulerWest ->setZValue (0.10f    )                         ;
  rulerWest ->setOpacity(0.50f    )                         ;
  rulerWest ->direction = West                    ;
  rulerWest ->CreatePath(         )                         ;
  rulerWest ->show      (         )                         ;
  rulers << rulerWest                                       ;
  ///////////////////////////////////////////////////////////
  VcfRuler * rulerEast = new VcfRuler(view,NULL)            ;
  rulerEast ->plan    = paperPlan                           ;
  rulerEast ->Options = Options                             ;
  scene     ->addItem   (rulerEast)                         ;
  rulerEast ->setRange  (ER       )                         ;
  rulerEast ->setZValue (0.10f    )                         ;
  rulerEast ->setOpacity(0.50f    )                         ;
  rulerEast ->direction = East                    ;
  rulerEast ->CreatePath(         )                         ;
  rulerEast ->show      (         )                         ;
  rulers << rulerEast                                       ;
}

#ifndef Q_OS_IOS

QPrinter * N::VcfPaperManager::PrintFile(QWidget * widget,QString caption,QString filepath,QString filters)
{
  QString filename = QFileDialog::getSaveFileName(widget,caption,filepath,filters);
  if (filename.length()<=0) return NULL;
  QFileInfo   FI(filename);
  QString     suffix = FI.suffix().toLower();
  QStringList fmts;
  fmts << "pdf" ;
  fmts << "ps"  ;
  if (!fmts.contains(suffix)) return NULL;
  QPrinter * printer = new QPrinter(QPrinter::HighResolution);
  printer->setOutputFileName(filename);
  if (suffix=="pdf") printer->setOutputFormat(QPrinter::PdfFormat);// else
//  if (suffix=="ps" ) printer->setOutputFormat(QPrinter::PostScriptFormat);
  return printer ;
}

QRectF N::VcfPaperManager::startPage(QPrinter * printer,int PageId)
{
  QRectF paper(0,0,0,0);
  if (!pages.contains(PageId)) return paper;
  VcfPaper * gp = pages[PageId];
  paper = gp->boundingRect();
  printer->setPaperSize(paperSize(gp->Paper));
  printer->setOrientation(paperOrientation(gp->Direction));
  printer->setFullPage(true);
  return paper;
}

bool N::VcfPaperManager::endPage(QPrinter * printer,int PageId)
{
  QList<int> p = pages.keys();
  if (p.count()<=0) return false;
  qSort(p.begin(),p.end());
  int EndPage = p.last();
  if (EndPage==PageId) return false;
  printer->newPage();
  return true;
}

QPrinter::PaperSize N::VcfPaperManager::paperSize(QString name)
{
  #define PM(n) if (name==#n) return QPrinter::n
  PM(A0);
  PM(A1);
  PM(A2);
  PM(A3);
  PM(A4);
  PM(A5);
  PM(A6);
  PM(A7);
  PM(A8);
  PM(A9);
  PM(B0);
  PM(B1);
  PM(B2);
  PM(B3);
  PM(B4);
  PM(B5);
  PM(B6);
  PM(B7);
  PM(B8);
  PM(B9);
  #undef  PM
  return QPrinter::A4;
}

QPrinter::Orientation N::VcfPaperManager::paperOrientation(int orientation)
{
  if (orientation==Qt::Vertical  ) return QPrinter::Portrait  ;
  if (orientation==Qt::Horizontal) return QPrinter::Landscape ;
  return QPrinter::Portrait                                   ;
}

#endif
"""
