# -*- coding: utf-8 -*-
##############################################################################
## VcfPath
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
import PySide6
from   PySide6                       import QtCore
from   PySide6                       import QtGui
from   PySide6                       import QtWidgets
##############################################################################
from   PySide6 . QtCore              import *
from   PySide6 . QtGui               import *
from   PySide6 . QtWidgets           import *
##############################################################################
from   AITK    . Essentials . Object import Object  as Object
from           . VcfItem             import VcfItem as VcfItem
##############################################################################
class VcfPath                 ( VcfItem , Object                           ) :
  ############################################################################
  def __init__                ( self                                       , \
                                parent = None                              , \
                                item   = None                              , \
                                plan   = None                              ) :
    ##########################################################################
    super ( ) . __init__      ( parent , item , plan                         )
    self . setObjectEmpty     (                                              )
    self . setVcfPathDefaults (                                              )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfPathDefaults    ( self                                         ) :
    ##########################################################################
    self . Editing = False
    self . setObjectType    ( 67                                             )
    ##########################################################################
    self . Painter . addMap ( "Default" , 1                                  )
    self . Painter . addMap ( "Dots"    , 2                                  )
    self . Painter . addMap ( "Lines"   , 3                                  )
    ##########################################################################
    self . setPenColor      ( 1 , QColor ( 192 , 192 , 192 )                 )
    self . setPenColor      ( 2 , QColor ( 255 ,  64 , 255 )                 )
    self . setPenColor      ( 3 , QColor ( 192 , 192 , 255 )                 )
    self . setPenStyle      ( 3 , Qt . DashLine                              )
    ##########################################################################
    self . setFlag ( QGraphicsItem . ItemIsMovable            , True         )
    self . setFlag ( QGraphicsItem . ItemIsSelectable         , True         )
    self . setFlag ( QGraphicsItem . ItemIsFocusable          , True         )
    self . setFlag ( QGraphicsItem . ItemClipsToShape         , False        )
    self . setFlag ( QGraphicsItem . ItemClipsChildrenToShape , False        )
    ##########################################################################
    return
  ############################################################################
  def boundingRect  ( self                                                 ) :
    if              ( 0 not in self . Painter . pathes                     ) :
      return QRectF ( 0 , 0 , 0 , 0                                          )
    return self . Painter . pathes [ 0 ] . boundingRect (                    )
  ############################################################################
  def shape                 ( self                                         ) :
    ##########################################################################
    path   = QPainterPath   (                                                )
    if                      ( 0 in self . Painter . pathes                 ) :
      path = Painter.pathes [ 0                                              ]
    ##########################################################################
    return path
  ############################################################################
  def paint         ( self , painter , options , widget                    ) :
    ##########################################################################
    Z    = QRectF   ( 0 , 0 , 0 , 0                                          )
    self . Painting (        painter , Z , False , True                      )
    ##########################################################################
    return
  ############################################################################
  def Painting         ( self , p , region , clip , color                  ) :
    ##########################################################################
    self . PaintPathes ( p                                                   )
    ##########################################################################
    return
  ############################################################################
  def Polyline ( self , contour , closed = True ) :
    ##########################################################################
    P = QPolygonF ( )
    """
    if (IsNull(Options)) return P        ;
    int   DPI = Options->DPI             ;
    CUIDs I   = contour.index            ;
    CUID  i                              ;
    if (closed) I << contour . index [0] ;
    foreach (i,I)                        {
      P << contour.points[i].Point(DPI)  ;
    }                                    ;
    """
    ##########################################################################
    return P
  ############################################################################
  def setPoints ( self , Id , contour ) :
    ##########################################################################
    """
    if (IsNull(Options)) return                  ;
    int     DPI   = Options->DPI                 ;
    int     total = contour.index.count()        ;
    QPointF R     = contour.thickness.Point(DPI) ;
    QPainterPath path                            ;
    for (int i=0;i<total;i++)                    {
      int     k = contour.index [i]              ;
      QPointF c = contour.points[k].Point(DPI)   ;
      path.addEllipse(c,R.x(),R.y())             ;
    }                                            ;
    Painter . pathes [Id] = path                 ;
    update ( )                                   ;
    """
    ##########################################################################
    return
  ############################################################################
  def setLines ( self , Id , contour ) :
    ##########################################################################
    """
    if (contour.count()<2) return            ;
    if (contour.count()==2)                  {
      int     a  = contour.index[0]          ;
      int     b  = contour.index[1]          ;
      QPointF P1 = contour.points[a].Point() ;
      QPointF P2 = contour.points[b].Point() ;
      QLineF  LE (P1,P2)                     ;
      setWideLine(Id,contour.thickness.z,LE) ;
    } else setSplines ( Id , contour )       ;
    """
    ##########################################################################
    return
  ############################################################################
  def setSplines ( self , Id , contour ) :
    ##########################################################################
    """
    QPolygonF     G1                                    ;
    QPolygonF     G2                                    ;
    QList<QLineF> L1                                    ;
    QList<QLineF> L2                                    ;
    double        HP  = contour.thickness.z / 2         ;
    QPointF       H (HP,HP)                             ;
    int           Sum = contour.count()                 ;
    int           DPI = Options->DPI                    ;
    H  = toPaper(H)                                     ;
    HP = H.x()                                          ;
    for (int i=1;i<Sum;i++)                             {
      int     A  = contour . index [ i-1 ]              ;
      int     B  = contour . index [ i   ]              ;
      QPointF P1 = contour . points[ A   ] . Point(DPI) ;
      QPointF P2 = contour . points[ B   ] . Point(DPI) ;
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
    if (total<=0) return                                ;
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
    /////////////////////////////////////////////////////
    QPolygonF C1                                        ;
    QPolygonF C2                                        ;
    QPolygonF R1                                        ;
    QPolygonF R2                                        ;
    QPointF   P0                                        ;
    QPointF   P1                                        ;
    QPointF   P2                                        ;
    QPointF   P3                                        ;
    for (int a=0;a<Sum;a++)                             {
      int b = a + 1 ; b %= Sum                          ;
      int c = a + 2 ; c %= Sum                          ;
      P1 = G1[a]                                        ;
      P2 = G1[b]                                        ;
      P3 = G1[c]                                        ;
      P0 = P1 + P2 ; P0 /= 2                            ;
      C1 << P0                                          ;
      P0 = Quadratic(0.5,P1,P2,P3)                      ;
      R1 << P0                                          ;
      P1 = G2[a]                                        ;
      P2 = G2[b]                                        ;
      P3 = G2[c]                                        ;
      P0 = P1 + P2 ; P0 /= 2                            ;
      C2 << P0                                          ;
      P0 = Quadratic(0.5,P1,P2,P3)                      ;
      R2 << P0                                          ;
    }                                                   ;
    /////////////////////////////////////////////////////
    QPainterPath path                                   ;
    int i = 0                                           ;
    while (i<Sum)                                       {
      int j                                             ;
      int k                                             ;
      int A  = contour . index  [ i ]                   ;
      int B                                             ;
      int C                                             ;
      int T1 = contour . points [ A ] . Control()       ;
      int T2                                            ;
      int T3                                            ;
      switch (T1)                                       {
        case Graphics::Start                            :
          path . moveTo ( G1 [ i ] )                    ;
          i++                                           ;
        break                                           ;
        case Graphics::End                              :
        case Graphics::Flat                             :
          j  = i - 1 + Sum ; j %= Sum                   ;
          B  = contour . index  [ j ]                   ;
          T2 = contour . points [ B ] . Control()       ;
          if (T2==Graphics::Quadratic)                  {
            path . quadTo ( C1 [ j ] , G1 [ i ] )       ;
          } else                                        {
            path . lineTo ( G1 [ i ] )                  ;
          }                                             ;
          i++                                           ;
        break                                           ;
        case Graphics::Quadratic                        :
          j  = i - 1 + Sum ; j %= Sum                   ;
          k  = i + 1       ; k %= Sum                   ;
          B  = contour . index  [ j ]                   ;
          C  = contour . index  [ k ]                   ;
          T2 = contour . points [ B ] . Control()       ;
          T3 = contour . points [ C ] . Control()       ;
          if (T2!=Graphics::Quadratic                  &&
              T3!=Graphics::Quadratic )                 {
            path . quadTo ( G1[ i ] , G1[ k ] )         ;
            i += 2                                      ;
          } else if (T2==Graphics::Quadratic           &&
                     T3!=Graphics::Quadratic)           {
            path . quadTo ( C1 [ j ] , G1 [ i ] )       ;
            i++                                         ;
          } else                                        {
            path . quadTo ( C1 [ j ] , R1 [ j ] )       ;
            i++                                         ;
          }                                             ;
        break                                           ;
      }                                                 ;
    }                                                   ;
    i = Sum - 1                                         ;
    while (i>=0)                                        {
      int j                                             ;
      int k                                             ;
      int A  = contour . index  [ i ]                   ;
      int B                                             ;
      int C                                             ;
      int T1 = contour . points [ A ] . Control()       ;
      int T2                                            ;
      int T3                                            ;
      switch (T1)                                       {
        case Graphics::End                              :
          path . lineTo ( G2 [ i ] )                    ;
          i--                                           ;
        break                                           ;
        case Graphics::Start                            :
        case Graphics::Flat                             :
          j  = i + 1       ; j %= Sum                   ;
          B  = contour . index  [ j ]                   ;
          T2 = contour . points [ B ] . Control()       ;
          if (T2==Graphics::Quadratic)                  {
            path . quadTo ( C2 [ j ] , G2 [ i ] )       ;
          } else                                        {
            path . lineTo ( G2 [ i ] )                  ;
          }                                             ;
          i--                                           ;
        break                                           ;
        case Graphics::Quadratic                        :
          j  = i + 1       ; j %= Sum                   ;
          k  = i - 1 + Sum ; k %= Sum                   ;
          B  = contour . index  [ j ]                   ;
          C  = contour . index  [ k ]                   ;
          T2 = contour . points [ B ] . Control()       ;
          T3 = contour . points [ C ] . Control()       ;
          if (T2!=Graphics::Quadratic                  &&
              T3!=Graphics::Quadratic )                 {
            path . quadTo ( G2[ i ] , G1[ k ] )         ;
            i -= 2                                      ;
          } else if (T2!=Graphics::Quadratic           &&
                     T3==Graphics::Quadratic)           {
            path . quadTo ( C2 [ j ] , G2 [ i ] )       ;
            i--                                         ;
          } else                                        {
            path . quadTo ( C2 [ j ] , R2 [ j ] )       ;
            i--                                         ;
          }                                             ;
        break                                           ;
      }                                                 ;
    }                                                   ;
    /////////////////////////////////////////////////////
    Painter . pathes [Id] = path                        ;
    update ( )                                          ;
    """
    ##########################################################################
    return
  ############################################################################
  def setContour ( self , Id , contour ) :
    ##########################################################################
    """
    if (contour.count()<3) return                       ;
    QPolygonF    P                                      ;
    QPolygonF    M                                      ;
    QPolygonF    R                                      ;
    QPointF      P0                                     ;
    QPointF      P1                                     ;
    QPointF      P2                                     ;
    QPointF      P3                                     ;
    QPainterPath path                                   ;
    int          Sum = contour.count()                  ;
    int          DPI = Options->DPI                     ;
    for (int a=0;a<Sum;a++)                             {
      int i = contour . index [ a ]                     ;
      P << contour.points[i].Point(DPI)                 ;
    }                                                   ;
    for (int a=0;a<Sum;a++)                             {
      int b = a + 1 ; b %= Sum                          ;
      int c = a + 2 ; c %= Sum                          ;
      P1 = P[a]                                         ;
      P2 = P[b]                                         ;
      P3 = P[c]                                         ;
      P0 = P1 + P2 ; P0 /= 2                            ;
      M << P0                                           ;
      P0 = Quadratic(0.5,P1,P2,P3)                      ;
      R << P0                                           ;
    }                                                   ;
    int i = 0                                           ;
    int j                                               ;
    int k                                               ;
    int A                                               ;
    int B                                               ;
    int C                                               ;
    int T1                                              ;
    int T2                                              ;
    int T3                                              ;
    j  = i - 1 + Sum ; j %= Sum                         ;
    A  = contour . index  [ i ]                         ;
    B  = contour . index  [ j ]                         ;
    T1 = contour . points [ A ] . Control()             ;
    switch (T1)                                         {
      case Graphics::Start                              :
      case Graphics::End                                :
      case Graphics::Flat                               :
        path . moveTo ( P [ i ] )                       ;
        i++                                             ;
      break                                             ;
      case Graphics::Quadratic                          :
        path . moveTo ( R [ j ] )                       ;
        i++                                             ;
      break                                             ;
    }                                                   ;
    while (i<Sum)                                       {
      A  = contour . index  [ i ]                       ;
      T1 = contour . points [ A ] . Control()           ;
      switch (T1)                                       {
        case Graphics::Start                            :
          path . moveTo ( P [ i ] )                     ;
          i++                                           ;
        break                                           ;
        case Graphics::End                              :
        case Graphics::Flat                             :
          j  = i - 1 + Sum ; j %= Sum                   ;
          B  = contour . index  [ j ]                   ;
          T2 = contour . points [ B ] . Control()       ;
          if (T2==Graphics::Quadratic)                  {
            path . quadTo ( M [ j ] , P [ i ] )         ;
          } else                                        {
            path . lineTo ( P [ i ] )                   ;
          }                                             ;
          i++                                           ;
        break                                           ;
        case Graphics::Quadratic                        :
          j  = i - 1 + Sum ; j %= Sum                   ;
          k  = i + 1       ; k %= Sum                   ;
          B  = contour . index  [ j ]                   ;
          C  = contour . index  [ k ]                   ;
          T2 = contour . points [ B ] . Control()       ;
          T3 = contour . points [ C ] . Control()       ;
          if (T2!=Graphics::Quadratic                  &&
              T3!=Graphics::Quadratic )                 {
            path . quadTo ( P[ i ] , P[ k ] )           ;
            i += 2                                      ;
          } else if (T2==Graphics::Quadratic           &&
                     T3!=Graphics::Quadratic)           {
            path . quadTo ( M [ j ] , P [ i ] )         ;
            i++                                         ;
          } else                                        {
            path . quadTo ( M [ j ] , R [ j ] )         ;
            i++                                         ;
          }                                             ;
        break                                           ;
      }                                                 ;
    }                                                   ;
    i  = 0                                              ;
    j  = Sum - 1                                        ;
    k  = 1                                              ;
    A  = contour . index  [ i ]                         ;
    T1 = contour . points [ A ] . Control()             ;
    switch (T1)                                         {
      case Graphics::Start                              :
      case Graphics::End                                :
      case Graphics::Flat                               :
        B  = contour . index  [ j ]                     ;
        T2 = contour . points [ B ] . Control()         ;
        if (T2==Graphics::Quadratic)                    {
          path . quadTo ( M [ j ] , P [ i ] )           ;
        } else                                          {
          path . lineTo ( P [ i ] )                     ;
        }                                               ;
      break                                             ;
      case Graphics::Quadratic                          :
        B  = contour . index  [ j ]                     ;
        C  = contour . index  [ k ]                     ;
        T2 = contour . points [ B ] . Control()         ;
        T3 = contour . points [ C ] . Control()         ;
        if (T2!=Graphics::Quadratic                    &&
            T3!=Graphics::Quadratic )                   {
          path . quadTo ( P[ i ] , P[ k ] )             ;
          i += 2                                        ;
        } else if (T2==Graphics::Quadratic             &&
                   T3!=Graphics::Quadratic)             {
          path . quadTo ( M [ j ] , P [ i ] )           ;
          i++                                           ;
        } else                                          {
          path . quadTo ( M [ j ] , R [ j ] )           ;
          i++                                           ;
        }                                               ;
      break                                             ;
    }                                                   ;
    Painter . pathes [Id] = path                        ;
    update ( )                                          ;
    """
    ##########################################################################
    return
##############################################################################
