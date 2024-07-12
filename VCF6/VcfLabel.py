# -*- coding: utf-8 -*-
##############################################################################
## VcfLabel
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
from           . VcfCanvas import VcfCanvas as VcfCanvas
##############################################################################
class VcfLabel                  ( VcfCanvas                                ) :
  ############################################################################
  EDITID = 10001
  ############################################################################
  def __init__                  ( self                                     , \
                                  parent = None                            , \
                                  item   = None                            , \
                                  plan   = None                            ) :
    ##########################################################################
    super ( ) . __init__        ( parent , item , plan                       )
    self . setVcfLabelDefaults  (                                            )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfLabelDefaults ( self                                           ) :
    ##########################################################################
    self . TextAlignment = Qt . AlignVCenter | Qt . AlignHCenter
    self . Content       = ""
    ##########################################################################
    self . Printable     = True
    self . Scaling       = False
    self . Editable      = True
    ##########################################################################
    self . setFlag            ( self . ItemIsMovable            , True       )
    self . setFlag            ( self . ItemIsSelectable         , True       )
    self . setFlag            ( self . ItemIsFocusable          , True       )
    self . setFlag            ( self . ItemClipsToShape         , False      )
    self . setFlag            ( self . ItemClipsChildrenToShape , False      )
    ##########################################################################
    self . Painter . addMap   ( "Default" , 0                                )
    self . Painter . addPen   ( 0 , QColor ( 192 , 192 , 192 )               )
    self . Painter . addPen   ( 1 , QColor (   0 ,   0 ,   0 )               )
    self . Painter . addBrush ( 0 , QColor ( 240 , 240 , 240 )               )
    ##########################################################################
    return
  ############################################################################
  def mouseDoubleClickEvent           ( self , event                       ) :
    ##########################################################################
    if                                ( self . Editable                    ) :
      ## self  . MountEditor             (                                      )
      event . accept                  (                                      )
      return
    ##########################################################################
    super ( ) . mouseDoubleClickEvent ( event                                )
    ##########################################################################
    return
  ############################################################################
  def Painting            ( self , p , region , clip , color               ) :
    ##########################################################################
    super ( ) . Painting  (        p , region , clip , color                 )
    self      . PaintText (        p , region , clip , color                 )
    ##########################################################################
    return
  ############################################################################
  def PaintText         ( self , p , region , clip , color                 ) :
    ##########################################################################
    self . pushPainters ( p                                                  )
    ##########################################################################
    R    = self . ContentRect             (                                  )
    ## self . Painter . fonts [ 0 ] . setDPI ( self . Options . PaperDPI        )
    p    . setFont                        ( self . Painter . fonts [ 0 ]     )
    self . Painter . assignPainterId      ( p , 0                            )
    ##########################################################################
    if                  ( clip                                             ) :
      p  . drawText     ( R , self . TextAlignment , self . Content , region )
    else                                                                     :
      p  . drawText     ( R , self . TextAlignment , self . Content          )
    ##########################################################################
    self . popPainters  ( p                                                  )
    ##########################################################################
    return
  ############################################################################
  def setText     ( self , text                                            ) :
    ##########################################################################
    self . Content = text
    self . update (                                                          )
    ##########################################################################
    return
  ############################################################################
  def ContentRect            ( self                                        ) :
    ##########################################################################
    ls = self . Options . LineSpace
    ##########################################################################
    G  = QPointF             ( ls , ls                                       )
    G  = self . paperToPoint ( G                                             )
    ##########################################################################
    return QRectF ( self . ScreenRect . left   ( ) +   G . x ( )           , \
                    self . ScreenRect . top    ( ) +   G . y ( )           , \
                    self . ScreenRect . width  ( ) - ( G . x ( ) * 2 )     , \
                    self . ScreenRect . height ( ) - ( G . y ( ) * 2 )       )
  ############################################################################
  def EditorRect             ( self                                        ) :
    ##########################################################################
    ls = self . Options . LineSpace
    ##########################################################################
    G  = QPointF             ( ls , ls                                       )
    G  = self . paperToPoint ( G                                             )
    ##########################################################################
    return QRectF ( self . ScreenRect . left   ( ) +   G . x ( )           , \
                    self . ScreenRect . top    ( ) +   G . y ( )           , \
                    self . ScreenRect . width  ( ) - ( G . x ( ) * 2 )     , \
                    self . ScreenRect . height ( ) - ( G . y ( ) * 2 )       )
  ############################################################################
  def FitSize                             ( self                           ) :
    ##########################################################################
    ## self . Painter . fonts [ 0 ] . setDPI ( self . Options . PaperDPI        )
    R    = self . Painter . boundingRect  ( 0 , self . Content               )
    S    = QPointF                        ( R . width ( ) , R . height ( )   )
    """
    S = Options -> Standard ( S )
    """
    ##########################################################################
    return QSizeF                         ( S . x ( ) , S . y ( )            )
  ############################################################################
  def MountEditor ( self ) :
    ##########################################################################
    """
    QLineEdit * LE = NewLineEdit ( EDITID )    ;
    QRectF      ER = EditorRect  (        )    ;
    Proxys[EDITID]->setGeometry  ( ER     )    ;
    Painter.fonts[0].setDPI(Options->DPI  )    ;
    LE -> setFont ( Painter.fonts[0]      )    ;
    LE -> setText ( Content               )    ;
    connect(LE  ,SIGNAL(editingFinished() )    ,
            this,SLOT  (NameFinished   () )  ) ;
    Alert ( Click )                            ;
    LE -> setFocus ( Qt::TabFocusReason      ) ;
    """
    ##########################################################################
    return
  ############################################################################
  def NameFinished ( self ) :
    ##########################################################################
    """
    QLineEdit * LE = qobject_cast<QLineEdit *>(Widgets[EDITID]) ;
    if (NotNull(LE))                                            {
      Content = LE -> text ( )                                  ;
      emit Changed ( this )                                     ;
    }                                                           ;
    """
    ##########################################################################
    self . DeleteGadgets ( )
    self . update        ( )
    ##########################################################################
    return
##############################################################################
