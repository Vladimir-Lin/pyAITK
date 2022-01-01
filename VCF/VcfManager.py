# -*- coding: utf-8 -*-
##############################################################################
## VcfManager
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
class VcfManager      (                                                    ) :
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
class Q_COMPONENTS_EXPORT VcfManager
{
  public:

    VcfItems Items ;
    VcfMaps  Maps  ;

    explicit VcfManager (void);
    virtual ~VcfManager (void);

    QList<VcfContours *> ItemContours (VcfItem * parent) ;

  protected:

    QRectF   United     (QGraphicsView * view) ;
    QRectF   United     (QGraphicsView * view,QRectF & rectangle) ;
    QRectF   toScene    (QGraphicsView * view,VcfItem * item) ;
    QRect    toView     (QGraphicsView * view,VcfItem * item) ;
    int      addItem    (VcfItem * item,VcfItem * parent) ;
    int      takeItem   (VcfItem * item) ;

  private:

};

N::VcfManager:: VcfManager(void)
{
}

N::VcfManager::~VcfManager(void)
{
}

int N::VcfManager::addItem(VcfItem * item,VcfItem * parent)
{
  if ( NULL == item )              {
    return Items . count ( )       ;
  }                                ;
  if ( Items . contains ( item ) ) {
    Maps [ item ] = parent         ;
    return Items . count ( )       ;
  }                                ;
  Items << item                    ;
  Maps [ item ] = parent           ;
  return Items . count ( )         ;
}

int N::VcfManager::takeItem(VcfItem * item)
{
  if ( NULL == item ) return Items . count( )             ;
  VcfItems its                                            ;
  for (int i = 0 ; i < Items . count ( ) ; i++ )          {
    VcfItem * vi = Items [ i ]                            ;
    if ( Maps [ vi ] == item ) its << vi                  ;
  }                                                       ;
  for (int i=0;i<its.count();i++)                         {
    if ( ( NULL != its [ i ] ) && ( item != its [ i ] ) ) {
      takeItem ( its [ i ] )                              ;
    }                                                     ;
  }                                                       ;
  Items . removeAt ( Items . indexOf ( item ) )           ;
  Maps  . remove   ( item                     )           ;
  item -> deleteLater ( )                                 ;
  return Items . count( )                                 ;
}

QRect N::VcfManager::toView(QGraphicsView * view,VcfItem * item)
{
  QRectF R = item->boundingRect ( )                    ;
  QRectF V = item->mapToScene   (R) . boundingRect ( ) ;
  QRect  Z = view->mapFromScene (V) . boundingRect ( ) ;
  return Z                                             ;
}

QRectF N::VcfManager::toScene(QGraphicsView * view,VcfItem * item)
{
  QRectF R = item->boundingRect ( )                    ;
  QRectF V = item->mapToScene   (R) . boundingRect ( ) ;
  return V                                             ;
}

QRectF N::VcfManager::United(QGraphicsView * view)
{
  QRectF V (0,0,0,0)                                  ;
  if (Items.count()<=0) return V                      ;
  if (Items.count()==1) return toScene(view,Items[0]) ;
  V = toScene(view,Items[0])                          ;
  for (int i=1;i<Items.count();i++)                   {
    QRectF R = toScene(view,Items[i])                 ;
    V = V.united(R)                                   ;
  }                                                   ;
  return V                                            ;
}

QRectF N::VcfManager::United(QGraphicsView * view,QRectF & rectangle)
{
  QRectF V = rectangle                ;
  for (int i=0;i<Items.count();i++)   {
    QRectF R = toScene(view,Items[i]) ;
    V = V.united(R)                   ;
  }                                   ;
  return V                            ;
}

QList<N::VcfContours *> N::VcfManager::ItemContours(VcfItem * parent)
{
  QList<VcfContours *> contours                      ;
  for (int i=0;i<Items.count();i++)                  {
    VcfItem * item = Items[i]                        ;
    if (nEqual(Maps[item],parent))                   {
      VcfContours * c = VcfCasting(VcfContours,item) ;
      nIfSafe(c) contours << c                       ;
    }                                                ;
  }                                                  ;
  return contours                                    ;
}
"""
