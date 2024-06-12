# -*- coding: utf-8 -*-
##############################################################################
## Gradient
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
from   PySide6             import QtCore
from   PySide6             import QtGui
from   PySide6             import QtWidgets
##############################################################################
from   PySide6 . QtCore    import *
from   PySide6 . QtGui     import *
from   PySide6 . QtWidgets import *
##############################################################################
class Gradient             (                                               ) :
  ############################################################################
  def __init__             ( self , Type = QGradient . NoGradient          ) :
    ##########################################################################
    self      . Initialize ( Type                                            )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def CreateGradient         ( self , Type                                 ) :
    ##########################################################################
    if                       ( Type == QGradient . LinearGradient          ) :
      self . gradient = QLinearGradient  (                                   )
      return
    ##########################################################################
    if                       ( Type == QGradient . QRadialGradient         ) :
      self . gradient = QRadialGradient  (                                   )
      return
    ##########################################################################
    if                       ( Type == QGradient . QConicalGradient        ) :
      self . gradient = QConicalGradient (                                   )
      return
    ##########################################################################
    return
  ############################################################################
  def Initialize             ( self , Type                                 ) :
    ##########################################################################
    self . gradient = None
    self . Uuid     = 0
    self . Name     = ""
    self . Editable = True
    self . Step     = 0
    self . Color    = QColor (                                               )
    self . CreateGradient    (                                               )
    ##########################################################################
    return
  ############################################################################
  def Configuration        ( self                                          ) :
    ##########################################################################
    JSON =                 {                                                 }
    """
    DESC = self . toString (                                                 )
    UUID = self . Uuid
    ##########################################################################
    JSON [ "Type"        ] = "Gradient"
    JSON [ "Uuid"        ] = f"{UUID}"
    JSON [ "Name"        ] = self . Name
    JSON [ "CM"          ] = self . CM
    JSON [ "Editable"    ] = self . Editable
    JSON [ "Description" ] = DESC
    """
    ##########################################################################
    return JSON
  ############################################################################
  def setConfigure          ( self , JSON                                  ) :
    ##########################################################################
    """
    self . Uuid     = int   ( JSON [ "Uuid" ]                                )
    self . Name     = JSON  [ "Name"                                         ]
    self . CM       = float ( JSON [ "CM"   ]                                )
    self . Editable = JSON  [ "Editable"                                     ]
    ##########################################################################
    DESC = JSON             [ "Description"                                  ]
    self . fromString       ( DESC                                           )
    """
    ##########################################################################
    return
##############################################################################
"""
QLinearGradient * N::Gradient::linear(void)
{
  if (IsNull(gradient)) return NULL                            ;
  if (gradient->type()!=QGradient::LinearGradient) return NULL ;
  return (QLinearGradient *)gradient                           ;
}

QRadialGradient * N::Gradient::radial(void)
{
  if (IsNull(gradient)) return NULL ;
  if (gradient->type()!=QGradient::RadialGradient) return NULL ;
  return (QRadialGradient *)gradient                           ;
}

QConicalGradient * N::Gradient::conical(void)
{
  if (IsNull(gradient)) return NULL ;
  if (gradient->type()!=QGradient::ConicalGradient) return NULL ;
  return (QConicalGradient *)gradient                           ;
}

QBrush N::Gradient::Brush(void)
{
  if (IsNull(gradient)) return QBrush() ;
  return QBrush ( *gradient )           ;
}

QByteArray N::Gradient::Configure(void)
{
  QByteArray conf                                                ;
  conf.resize(sizeof(nGradientConfiguration))                    ;
  nGradientConfiguration ngc                                     ;
  QLinearGradient  * LINEAR  = (QLinearGradient  *)gradient      ;
  QRadialGradient  * RADIAL  = (QRadialGradient  *)gradient      ;
  QConicalGradient * CONICAL = (QConicalGradient *)gradient      ;
  QPointF           P                                            ;
  memset ( &ngc , 0 , sizeof(nGradientConfiguration) )           ;
  ngc.Type       = (int)gradient->type           ( )             ;
  ngc.Spread     = (int)gradient->spread         ( )             ;
  ngc.Coordinate = (int)gradient->coordinateMode ( )             ;
  switch (ngc.Type)                                              {
    case QGradient::LinearGradient                               :
      P = LINEAR  -> start     ()                                ;
      ngc.x1 = P.x             ()                                ;
      ngc.y1 = P.y             ()                                ;
      P = LINEAR  -> finalStop ()                                ;
      ngc.x2 = P.x             ()                                ;
      ngc.y2 = P.y             ()                                ;
    break                                                        ;
    case QGradient::RadialGradient                               :
      P = RADIAL  -> center        ()                            ;
      ngc.x1 = P.x                 ()                            ;
      ngc.y1 = P.y                 ()                            ;
      ngc.z1 = RADIAL->radius      ()                            ;
      P = RADIAL  -> focalPoint    ()                            ;
      ngc.x2 = P.x                 ()                            ;
      ngc.y2 = P.y                 ()                            ;
      ngc.z2 = RADIAL->focalRadius ()                            ;
    break                                                        ;
    case QGradient::ConicalGradient                              :
      P = CONICAL -> center   ()                                 ;
      ngc.x1 = P.x            ()                                 ;
      ngc.y1 = P.y            ()                                 ;
      ngc.z1 = CONICAL->angle ()                                 ;
    break                                                        ;
    case QGradient::NoGradient                                   :
    break                                                        ;
  }                                                              ;
  QGradientStops gs = gradient->stops()                          ;
  int total = gs.count()                                         ;
  if (total>256) total = 256                                     ;
  ngc.Size = total                                               ;
  for (int i=0;i<total;i++)                                      {
    QGradientStop s = gs [i]                                     ;
    double g = s.first                                           ;
    QColor c = s.second                                          ;
    ngc.Points[i].position = g                                   ;
    ngc.Points[i].R        = c . red   ()                        ;
    ngc.Points[i].G        = c . green ()                        ;
    ngc.Points[i].B        = c . blue  ()                        ;
    ngc.Points[i].A        = c . alpha ()                        ;
  }                                                              ;
  memcpy ( conf.data() , &ngc , sizeof(nGradientConfiguration) ) ;
  return     conf                                                ;
}

void N::Gradient::setConfigure(QByteArray & conf)
{
  if (conf.size()!=sizeof(nGradientConfiguration)) return                      ;
  nGradientConfiguration * ngc = (nGradientConfiguration *)conf.data()         ;
  QLinearGradient  * LINEAR  = NULL                                            ;
  QRadialGradient  * RADIAL  = NULL                                            ;
  QConicalGradient * CONICAL = NULL                                            ;
  switch (ngc->Type)                                                           {
    case QGradient::LinearGradient                                             :
      LINEAR   = new QLinearGradient  ()                                       ;
      LINEAR  -> setSpread        ((QGradient::Spread        )ngc->Spread    ) ;
      LINEAR  -> setCoordinateMode((QGradient::CoordinateMode)ngc->Coordinate) ;
      LINEAR  -> setStart     (ngc->x1,ngc->y1)                                ;
      LINEAR  -> setFinalStop (ngc->x2,ngc->y2)                                ;
      gradient = (QGradient *)LINEAR                                           ;
    break                                                                      ;
    case QGradient::RadialGradient                                             :
      RADIAL   = new QRadialGradient  ()                                       ;
      RADIAL  -> setSpread        ((QGradient::Spread        )ngc->Spread    ) ;
      RADIAL  -> setCoordinateMode((QGradient::CoordinateMode)ngc->Coordinate) ;
      gradient = (QGradient *)RADIAL                                           ;
      RADIAL  -> setCenter      (ngc->x1,ngc->y1)                              ;
      RADIAL  -> setRadius      (ngc->z1        )                              ;
      RADIAL  -> setFocalPoint  (ngc->x1,ngc->y1)                              ;
      RADIAL  -> setFocalRadius (ngc->z1        )                              ;
    break                                                                      ;
    case QGradient::ConicalGradient                                            :
      CONICAL  = new QConicalGradient ()                                       ;
      CONICAL -> setSpread        ((QGradient::Spread        )ngc->Spread    ) ;
      CONICAL -> setCoordinateMode((QGradient::CoordinateMode)ngc->Coordinate) ;
      CONICAL -> setCenter        (ngc->x1,ngc->y1)                            ;
      CONICAL -> setAngle         (ngc->z1        )                            ;
      gradient = (QGradient *)CONICAL                                          ;
    break                                                                      ;
    case QGradient::NoGradient                                                 :
      gradient = NULL                                                          ;
    break                                                                      ;
  }                                                                            ;
  if (IsNull(gradient)) return                                                 ;
  int total = ngc->Size                                                        ;
  for (int i=0;i<total;i++)                                                    {
    nGradientPoint GP = ngc->Points[i]                                         ;
    QColor c(GP.R,GP.G,GP.B,GP.A)                                              ;
    gradient->setColorAt(GP.position,c)                                        ;
  }                                                                            ;
}
"""
