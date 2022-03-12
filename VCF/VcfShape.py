# -*- coding: utf-8 -*-
##############################################################################
## VcfShape
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
from   PyQt5 . QtCore                 import QLineF
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QPolygonF
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QGraphicsView
##############################################################################
class VcfShape        (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    return
  ############################################################################
  def __del__         ( self                                               ) :
    return
  ############################################################################
  def WideLineP     ( self , width ,          P1 , P2                      ) :
    return WideLine (        width , QLineF ( P1 , P2 )                      )
  ############################################################################
  def WideLine               ( self , width , line                         ) :
    ##########################################################################
    P  = QPolygonF           (                                               )
    HP = width / 2
    NL = line . normalVector (                                               )
    NL = NL   . unitVector   (                                               )
    P0 = QPointF             ( NL . dx ( ) , NL . dy ( )                     )
    PP = P0 * HO
    P1 = line . p1 ( ) + PP
    P2 = line . p2 ( ) + PP
    P3 = line . p2 ( ) - PP
    P4 = line . p1 ( ) - PP
    P  . append              ( P1                                            )
    P  . append              ( P2                                            )
    P  . append              ( P3                                            )
    P  . append              ( P4                                            )
    ##########################################################################
    return P
  ############################################################################
  def FoldLines ( self , width , lines ) :
    ##########################################################################
    """
    QPolygonF     P                                     ;
    QPolygonF     G1                                    ;
    QPolygonF     G2                                    ;
    QList<QLineF> L1                                    ;
    QList<QLineF> L2                                    ;
    double        HP =  width / 2                       ;
    for (int i=1;i<lines.count();i++)                   {
      QPointF P1 = lines [i-1]                          ;
      QPointF P2 = lines [i  ]                          ;
      QLineF  LL(P1,P2)                                 ;
      QLineF  NL = LL . normalVector ( )                ;
              NL = NL . unitVector   ( )                ;
      QPointF   P0 ( NL.dx() , NL.dy() )                ;
      QPointF   PP = P0 * HP                            ;
      QPointF   p1 = P1 + PP                            ;
      QPointF   p2 = P2 + PP                            ;
      QPointF   p3 = P1 - PP                            ;
      QPointF   p4 = P2 - PP                            ;
      L1 << QLineF ( p1 , p2 )                          ;
      L2 << QLineF ( p3 , p4 )                          ;
    }                                                   ;
    int total = L1 . count()                            ;
    if (total<=0) return P                              ;
    G1 << L1[0].p1()                                    ;
    G2 << L2[0].p1()                                    ;
    for (int i=1;i<total;i++)                           {
      QPointF PI                                        ;
      QLineF  LA                                        ;
      QLineF  LB                                        ;
      LA = L1[i-1]                                      ;
      LB = L1[i  ]                                      ;
      if (LA.intersect(LB,&PI)!=QLineF::NoIntersection) {
        G1 << PI                                        ;
      }                                                 ;
      LA = L2[i-1]                                      ;
      LB = L2[i  ]                                      ;
      if (LA.intersect(LB,&PI)!=QLineF::NoIntersection) {
        G2 << PI                                        ;
      }                                                 ;
    }                                                   ;
    G1 << L1[total-1].p2()                              ;
    G2 << L2[total-1].p2()                              ;
    P   = G1                                            ;
    for (int i=G2.count()-1;i>=0;i--) P << G2[i]        ;
    return    P                                         ;
    """
    ##########################################################################
    return
  ############################################################################
  def Triangle               ( self , width , length , line                ) :
    ##########################################################################
    HP = width
    HP = HP / 2.0
    LV = line . unitVector   (                                               )
    NL = line . normalVector (                                               )
    NL = NL   . unitVector   (                                               )
    P0 = QPointF             ( NL . dx ( ) , NL . dy ( )                     )
    PP = P0 * HP
    PZ = QPointF             ( LV . dx ( ) , LV . dy ( )                     )
    PB = PZ * length
    PB = line . p2 ( ) - PB
    P  = QPolygonF           (                                               )
    P  . append              ( PB + PP                                       )
    P  . append              ( line . p2 ( )                                 )
    P  . append              ( PB   - PP                                     )
    ##########################################################################
    return P
  ############################################################################
  def Symmetry ( self , Center , N , shift , radius ) :
    ##########################################################################
    P   = QPolygonF ( )
    if ( N < 3 ) :
      return P
    ##########################################################################
    B   = shift
    A   = 360.0
    A   = A / N
    ##########################################################################
    for i in range ( 0 , N ) :
      ########################################################################
      x = 0.0
      y = 0.0
      """
      double x = N::Math::fastCosine(B) ;
      double y = N::Math::fastSine  (B) ;
      """
      x = x * radius
      y = y * radius
      S = QPointF ( x , y )
      P . append ( Center + S )
      B += A
    ##########################################################################
    return P
##############################################################################
