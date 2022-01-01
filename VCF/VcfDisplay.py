# -*- coding: utf-8 -*-
##############################################################################
## VcfDisplay
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
from   PyQt5 . QtCore                 import QRect
from   PyQt5 . QtCore                 import QRectF
from   PyQt5 . QtCore                 import QMargins
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QTransform
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
from   PyQt5 . QtWidgets              import QGraphicsScene
##############################################################################
class VcfDisplay             (                                             ) :
  ############################################################################
  def __init__               ( self                                        ) :
    ##########################################################################
    self . InitializeDisplay (                                               )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def InitializeDisplay       ( self                                       ) :
    ##########################################################################
    print("InitializeDisplay")
    self . Scene         = QGraphicsScene (                                  )
    self . Zooms         =    [                                              ]
    ## VcfOptions Options
    self . Options       =    {                                              }
    self . Margins       = QMargins ( 0 , 0 , 3 , 3 )
    self . Margins       = None
    self . Transform     = QTransform ( )
    self . Transform     . reset ( )
    self . Origin        = QPointF ( 0 , 0 )
    self . View          = QRectF ( )
    ## Screen           screen
    ## self . screen        = False
    self . MonitorFactor = 1.0
    self . ZoomFactor    = 1.0
    self . DPI           = 300
    ##########################################################################
    return
  ############################################################################
  def Enlarge ( self                                                       ) :
    ##########################################################################
    self . ZoomFactor = self . FactorLevel ( self . ZoomFactor , True        )
    ##########################################################################
    return JSON
  ############################################################################
  def Shrink  ( self                                                       ) :
    ##########################################################################
    self . ZoomFactor = self . FactorLevel ( self . ZoomFactor , False       )
    ##########################################################################
    return
  ############################################################################
  def ZoomSpin ( self , parent , widget , method                           ) :
    ##########################################################################
    """
  QDoubleSpinBox * ds = new QDoubleSpinBox(parent) ;
  ds->setMinimum    (0.01000       )               ;
  ds->setMaximum    (1000000       )               ;
  ds->setValue      (ZoomFactor*100)               ;
  ds->setSingleStep (1.00          )               ;
  ds->setSuffix     ("%")                          ;
  ds->setAlignment(Qt::AlignRight|Qt::AlignVCenter);
  QObject::connect(ds,SIGNAL(valueChanged(double)) ,
                   widget,method                )  ;
  return ds                                        ;
    """
    ##########################################################################
    return
  ############################################################################
  def ZoomSpinChanged         ( self , value                               ) :
    ##########################################################################
    self . ZoomFactor = float ( value / 100                                  )
    ##########################################################################
    return
  ############################################################################
  def available ( self , size                                              ) :
    ##########################################################################
    """
  return QSize                                                        (
           size . width  () - Margins . left () - Margins . right  () ,
           size . height () - Margins . top  () - Margins . bottom ()
         )                                                            ;
    """
    ##########################################################################
    return
  ############################################################################
  def centimeter ( self , size                                             ) :
    ##########################################################################
    """
  double w = size.width () ;
  double h = size.height() ;
  w *= screen.WidthLength  ;
  w /= screen.WidthPixels  ;
  w /= 10                  ;
  h *= screen.HeightLength ;
  h /= screen.HeightPixels ;
  h /= 10                  ;
  return QSizeF(w,h)       ;
    """
    ##########################################################################
    return
  ############################################################################
  def toPaper ( self , cm                                             ) :
    ##########################################################################
    """
  double x = cm.width () ; x *= DPI ; x *= 100 ; x /= 254 ;
  double y = cm.height() ; y *= DPI ; y *= 100 ; y /= 254 ;
  return QSizeF(x,y)                                      ;
    """
    ##########################################################################
    return
  ############################################################################
  def asPaper ( self , size                                             ) :
    ##########################################################################
    """
  QSizeF S = size                      ;
  QSizeF P = toPaper(centimeter(size)) ;
  Transform.reset ()                   ;
  double sx = S.width  () / P.width () ;
  double sy = S.height () / P.height() ;
  sx *= ZoomFactor                     ;
  sy *= ZoomFactor                     ;
  Transform.scale (sx,sy)              ;
  QTransform I = Transform.inverted()  ;
  QPointF Z(S.width(),S.height())      ;
  Z = I.map(Z)                         ;
  return QRectF(0,0,Z.x(),Z.y())       ;
    """
    ##########################################################################
    return
  ############################################################################
  def Percentage ( self                                                ) :
    ##########################################################################
    """
  char P[1024]                        ;
  sprintf(P,"%4.2f",(ZoomFactor*100)) ;
  return QString("%1%").arg(P)        ;
    """
    ##########################################################################
    return
  ############################################################################
  def FactorLevel ( self , factor , enlarge                                ) :
    ##########################################################################
    """
  qreal f = factor;
  int   F = (int)(f * 100);
  bool  B = false;
  for (int i=1;!B && i<Zooms.count();i++) {
    if (Zooms[i-1]==F) {
      if (enlarge) {
        F = Zooms[i];
        B = true;
      } else {
        if (i>1) F = Zooms[i-2]; else F = Zooms[0];
        B = true;
      };
    } else
    if (Zooms[i]==F) {
      if (enlarge) {
        F = Zooms[i+1];
        B = true;
      } else {
        if (i>0) F = Zooms[i-1]; else F = Zooms[0];
        B = true;
      };
    } else
    if (Zooms[i-1]<F && F<Zooms[i]) {
      if (enlarge) {
        F = Zooms[i+1];
        B = true;
      } else {
        if (i>0) F = Zooms[i-1]; else F = Zooms[0];
        B = true;
      };
    };
  };
  f = F; f /= 100;
  return f;
    """
    ##########################################################################
    return
  ############################################################################
  def setDefaultZoom ( self                                                ) :
    ##########################################################################
    self . Zooms =   [    1 ,    2 ,    3 ,    4 ,    5 ,                    \
                          6 ,    7 ,    8 ,    9 ,   10 ,                    \
                         15 ,   20 ,   25 ,   30 ,   35 ,                    \
                         40 ,   45 ,   50 ,   55 ,   60 ,                    \
                         65 ,   70 ,   75 ,   80 ,   85 ,                    \
                         90 ,   95 ,  100 ,  110 ,  120 ,                    \
                        130 ,  140 ,  150 ,  160 ,  170 ,                    \
                        180 ,  190 ,  200 ,  300 ,  400 ,                    \
                        500 ,  600 ,  700 ,  800 ,  900 ,                    \
                       1000 , 1100 , 1200 , 1300 , 1400 ,                    \
                       1500 , 1600 , 1700 , 1800 , 1900 ,                    \
                       2000 , 2100 , 2200 , 2300 , 2400 ,                    \
                       2500 , 2600 , 2700 , 2800 , 2900 ,                    \
                       3000 , 3100 , 3200 , 3300 , 3400 ,                    \
                       3500 , 3600 , 3700 , 3800 , 3900 ,                    \
                       4000 , 4100 , 4200 , 4300 , 4400 ,                    \
                       4500 , 4600 , 4700 , 4800 , 4900 ,                    \
                       5000                                                  ]
    ##########################################################################
    return
##############################################################################
"""
class Q_COMPONENTS_EXPORT VcfDisplay
{
  public:

    CUIDs Zooms ;

    explicit VcfDisplay           (void) ;
    virtual ~VcfDisplay           (void) ;

    void     Enlarge              (void);
    void     Shrink               (void);

    QDoubleSpinBox * ZoomSpin     (QWidget * parent,QWidget * widget,const char * method);
    void ZoomSpinChanged          (double value);

  protected:

    QGraphicsScene * Scene         ;
    VcfOptions       Options       ;
    QMargins         Margins       ;
    QTransform       Transform     ;
    QPointF          Origin        ;
    QRectF           View          ;
    Screen           screen        ;
    double           MonitorFactor ;
    double           ZoomFactor    ;
    int              DPI           ;

    QSize          available      (QSize  size) ;
    QSizeF         centimeter     (QSize  size) ;
    QSizeF         toPaper        (QSizeF cm  ) ;
    QRectF         asPaper        (QSize  size) ;

    QString        Percentage     (void);

    qreal          FactorLevel    (qreal factor,bool enlarge);

    void           setDefaultZoom (void) ;

  private:

};

N::VcfDisplay:: VcfDisplay    (void        )
              : Margins       (0,0,3,3     )
              , DPI           (300         )
              , ZoomFactor    (1.00        )
              , MonitorFactor (1.00        )
              , Origin        (QPointF(0,0))
{
  Scene     = new QGraphicsScene ( ) ;
  Transform . reset              ( ) ;
}

N::VcfDisplay::~VcfDisplay (void)
{
}

QString N::VcfDisplay::Percentage(void)
{
  char P[1024]                        ;
  sprintf(P,"%4.2f",(ZoomFactor*100)) ;
  return QString("%1%").arg(P)        ;
}

QSize N::VcfDisplay::available(QSize size)
{
  return QSize                                                        (
           size . width  () - Margins . left () - Margins . right  () ,
           size . height () - Margins . top  () - Margins . bottom ()
         )                                                            ;
}

QSizeF N::VcfDisplay::centimeter(QSize size)
{
  double w = size.width () ;
  double h = size.height() ;
  w *= screen.WidthLength  ;
  w /= screen.WidthPixels  ;
  w /= 10                  ;
  h *= screen.HeightLength ;
  h /= screen.HeightPixels ;
  h /= 10                  ;
  return QSizeF(w,h)       ;
}

QSizeF N::VcfDisplay::toPaper(QSizeF cm)
{
  double x = cm.width () ; x *= DPI ; x *= 100 ; x /= 254 ;
  double y = cm.height() ; y *= DPI ; y *= 100 ; y /= 254 ;
  return QSizeF(x,y)                                      ;
}

QRectF N::VcfDisplay::asPaper(QSize size)
{
  QSizeF S = size                      ;
  QSizeF P = toPaper(centimeter(size)) ;
  Transform.reset ()                   ;
  double sx = S.width  () / P.width () ;
  double sy = S.height () / P.height() ;
  sx *= ZoomFactor                     ;
  sy *= ZoomFactor                     ;
  Transform.scale (sx,sy)              ;
  QTransform I = Transform.inverted()  ;
  QPointF Z(S.width(),S.height())      ;
  Z = I.map(Z)                         ;
  return QRectF(0,0,Z.x(),Z.y())       ;
}

qreal N::VcfDisplay::FactorLevel(qreal factor,bool enlarge)
{
  qreal f = factor;
  int   F = (int)(f * 100);
  bool  B = false;
  for (int i=1;!B && i<Zooms.count();i++) {
    if (Zooms[i-1]==F) {
      if (enlarge) {
        F = Zooms[i];
        B = true;
      } else {
        if (i>1) F = Zooms[i-2]; else F = Zooms[0];
        B = true;
      };
    } else
    if (Zooms[i]==F) {
      if (enlarge) {
        F = Zooms[i+1];
        B = true;
      } else {
        if (i>0) F = Zooms[i-1]; else F = Zooms[0];
        B = true;
      };
    } else
    if (Zooms[i-1]<F && F<Zooms[i]) {
      if (enlarge) {
        F = Zooms[i+1];
        B = true;
      } else {
        if (i>0) F = Zooms[i-1]; else F = Zooms[0];
        B = true;
      };
    };
  };
  f = F; f /= 100;
  return f;
}

void N::VcfDisplay::Enlarge(void)
{
  ZoomFactor = FactorLevel(ZoomFactor,true ) ;
}

void N::VcfDisplay::Shrink(void)
{
  ZoomFactor = FactorLevel(ZoomFactor,false) ;
}

QDoubleSpinBox * N::VcfDisplay::ZoomSpin(QWidget * parent,QWidget * widget,const char * method)
{
  QDoubleSpinBox * ds = new QDoubleSpinBox(parent) ;
  ds->setMinimum    (0.01000       )               ;
  ds->setMaximum    (1000000       )               ;
  ds->setValue      (ZoomFactor*100)               ;
  ds->setSingleStep (1.00          )               ;
  ds->setSuffix     ("%")                          ;
  ds->setAlignment(Qt::AlignRight|Qt::AlignVCenter);
  QObject::connect(ds,SIGNAL(valueChanged(double)) ,
                   widget,method                )  ;
  return ds                                        ;
}

void N::VcfDisplay::ZoomSpinChanged(double value)
{
  ZoomFactor = value / 100;
}

void N::VcfDisplay::setDefaultZoom(void)
{
  Zooms.clear() ;
  Zooms <<    1 ;
  Zooms <<    2 ;
  Zooms <<    3 ;
  Zooms <<    4 ;
  Zooms <<    5 ;
  Zooms <<    6 ;
  Zooms <<    7 ;
  Zooms <<    8 ;
  Zooms <<    9 ;
  Zooms <<   10 ;
  Zooms <<   15 ;
  Zooms <<   20 ;
  Zooms <<   25 ;
  Zooms <<   30 ;
  Zooms <<   35 ;
  Zooms <<   40 ;
  Zooms <<   45 ;
  Zooms <<   50 ;
  Zooms <<   55 ;
  Zooms <<   60 ;
  Zooms <<   65 ;
  Zooms <<   70 ;
  Zooms <<   75 ;
  Zooms <<   80 ;
  Zooms <<   85 ;
  Zooms <<   90 ;
  Zooms <<   95 ;
  Zooms <<  100 ;
  Zooms <<  110 ;
  Zooms <<  120 ;
  Zooms <<  130 ;
  Zooms <<  140 ;
  Zooms <<  150 ;
  Zooms <<  160 ;
  Zooms <<  170 ;
  Zooms <<  180 ;
  Zooms <<  190 ;
  Zooms <<  200 ;
  Zooms <<  300 ;
  Zooms <<  400 ;
  Zooms <<  500 ;
  Zooms <<  600 ;
  Zooms <<  700 ;
  Zooms <<  800 ;
  Zooms <<  900 ;
  Zooms << 1000 ;
  Zooms << 1100 ;
  Zooms << 1200 ;
  Zooms << 1300 ;
  Zooms << 1400 ;
  Zooms << 1500 ;
  Zooms << 1600 ;
  Zooms << 1700 ;
  Zooms << 1800 ;
  Zooms << 1900 ;
  Zooms << 2000 ;
  Zooms << 2100 ;
  Zooms << 2200 ;
  Zooms << 2300 ;
  Zooms << 2400 ;
  Zooms << 2500 ;
  Zooms << 2600 ;
  Zooms << 2700 ;
  Zooms << 2800 ;
  Zooms << 2900 ;
  Zooms << 3000 ;
  Zooms << 3100 ;
  Zooms << 3200 ;
  Zooms << 3300 ;
  Zooms << 3400 ;
  Zooms << 3500 ;
  Zooms << 3600 ;
  Zooms << 3700 ;
  Zooms << 3800 ;
  Zooms << 3900 ;
  Zooms << 4000 ;
  Zooms << 4100 ;
  Zooms << 4200 ;
  Zooms << 4300 ;
  Zooms << 4400 ;
  Zooms << 4500 ;
  Zooms << 4600 ;
  Zooms << 4700 ;
  Zooms << 4800 ;
  Zooms << 4900 ;
  Zooms << 5000 ;
}
"""
