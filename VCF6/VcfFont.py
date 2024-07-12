# -*- coding: utf-8 -*-
##############################################################################
## VcfFont
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
class VcfFont         (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    ##########################################################################
    self . Initialize (                                                      )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Initialize              ( self                                       ) :
    ##########################################################################
    self . Uuid      = 0
    self . Size      = 0.40
    self . Font      = QFont  (                                              )
    self . Pen       = QPen   (                                              )
    self . PenBrush  = QBrush (                                              )
    self . Brush     = QBrush (                                              )
    self . Selection = QBrush (                                              )
    self . Changed   = False
    ##########################################################################
    return
  ############################################################################
  def toJson        ( self                                                 ) :
    ##########################################################################
    JSON =          {                                                        }
    ##########################################################################
    """
    VcfFontConfiguration VF                                  ;
    QByteArray FontConf                                      ;
    FontConf.resize(sizeof(VcfFontConfiguration))            ;
    QString family = font.family()                           ;
    memset(&VF,0,sizeof(VcfFontConfiguration))               ;
    strcpy(VF.Family,family.toUtf8().data())                 ;
    QColor C                                                 ;
    VF.Size            = size                                ;
    VF.Stretch         = font . stretch    ()                ;
    VF.Weight          = font . weight     ()                ;
    VF.FixedPitch      = font . fixedPitch () ? 1 : 0        ;
    VF.Bold            = font . bold       () ? 1 : 0        ;
    VF.Italic          = font . italic     () ? 1 : 0        ;
    VF.Kerning         = font . kerning    () ? 1 : 0        ;
    VF.Overline        = font . overline   () ? 1 : 0        ;
    VF.StrikeOut       = font . strikeOut  () ? 1 : 0        ;
    VF.Underline       = font . underline  () ? 1 : 0        ;
    VF.Pen.Style       = pen  . style      ()                ;
    C                  = pen  . color      ()                ;
    VF.Pen.R           = C    . red        ()                ;
    VF.Pen.G           = C    . green      ()                ;
    VF.Pen.B           = C    . blue       ()                ;
    VF.Pen.A           = C    . alpha      ()                ;
    VF.Pen.CapStyle    = pen  . capStyle   ()                ;
    VF.Pen.Cosmetics   = pen  . isCosmetic ()                ;
    VF.Pen.Width       = pen  . widthF     ()                ;
    VF.PenBrush.Style  = penBrush . style  ()                ;
    C                  = penBrush . color  ()                ;
    VF.PenBrush.R      = C    . red        ()                ;
    VF.PenBrush.G      = C    . green      ()                ;
    VF.PenBrush.B      = C    . blue       ()                ;
    VF.PenBrush.A      = C    . alpha      ()                ;
    VF.Brush.Style     = brush. style      ()                ;
    C                  = brush. color      ()                ;
    VF.Brush.R         = C    . red        ()                ;
    VF.Brush.G         = C    . green      ()                ;
    VF.Brush.B         = C    . blue       ()                ;
    VF.Brush.A         = C    . alpha      ()                ;
    VF.Selection.Style = selection . style ()                ;
    C                  = selection . color ()                ;
    VF.Selection.R     = C    . red        ()                ;
    VF.Selection.G     = C    . green      ()                ;
    VF.Selection.B     = C    . blue       ()                ;
    VF.Selection.A     = C    . alpha      ()                ;
    memcpy(FontConf.data(),&VF,sizeof(VcfFontConfiguration)) ;
    """
    ##########################################################################
    return JSON
  ############################################################################
  def fromJson      ( self , JSON                                          ) :
    ##########################################################################
    """
    VcfFontConfiguration * VF = (VcfFontConfiguration *)Conf.data() ;
    QColor C                                                        ;
    font.setFamily(QString::fromUtf8(VF->Family))                   ;
    size = VF->Size                                                 ;
    font . setStretch    (VF->Stretch      )                        ;
    font . setWeight     (VF->Weight       )                        ;
    font . setBold       (VF->Bold      ==1)                        ;
    font . setFixedPitch (VF->FixedPitch==1)                        ;
    font . setItalic     (VF->Italic    ==1)                        ;
    font . setKerning    (VF->Kerning   ==1)                        ;
    font . setOverline   (VF->Overline  ==1)                        ;
    font . setStrikeOut  (VF->StrikeOut ==1)                        ;
    font . setUnderline  (VF->Underline ==1)                        ;
    C.setRed   (VF->Pen.R)                                          ;
    C.setGreen (VF->Pen.G)                                          ;
    C.setBlue  (VF->Pen.B)                                          ;
    C.setAlpha (VF->Pen.A)                                          ;
    pen.setColor   (C                   )                           ;
    pen.setStyle   ((Qt::PenStyle)VF->Pen.Style)                    ;
    pen.setCapStyle((Qt::PenCapStyle)VF->Pen.CapStyle)              ;
    pen.setCosmetic(VF->Pen.Cosmetics==1)                           ;
    pen.setWidthF  (VF->Pen.Width       )                           ;
    C.setRed   (VF->PenBrush.R)                                     ;
    C.setGreen (VF->PenBrush.G)                                     ;
    C.setBlue  (VF->PenBrush.B)                                     ;
    C.setAlpha (VF->PenBrush.A)                                     ;
    penBrush.setColor(C)                                            ;
    penBrush.setStyle((Qt::BrushStyle)VF->PenBrush.Style)           ;
    C.setRed   (VF->Brush.R)                                        ;
    C.setGreen (VF->Brush.G)                                        ;
    C.setBlue  (VF->Brush.B)                                        ;
    C.setAlpha (VF->Brush.A)                                        ;
    brush.setColor(C)                                               ;
    brush.setStyle((Qt::BrushStyle)VF->Brush.Style)                 ;
    C.setRed   (VF->Selection.R)                                    ;
    C.setGreen (VF->Selection.G)                                    ;
    C.setBlue  (VF->Selection.B)                                    ;
    C.setAlpha (VF->Selection.A)                                    ;
    selection.setColor(C)                                           ;
    selection.setStyle((Qt::BrushStyle)VF->Selection.Style)         ;
    """
    ##########################################################################
    return
  ############################################################################
  def setFont              ( painter , dpi                                 ) :
    ##########################################################################
    fs      = int          ( self . Size * float ( dpi ) * 100.0 / 254.0     )
    ##########################################################################
    F       = self . Font
    F       . setPixelSize ( fs                                              )
    ##########################################################################
    PEN     = self . Pen
    PBS     = self . PenBrush . style (                                      )
    if                     ( PBS not in [ Qt . NoBrush ]                   ) :
      PEN   . setBrush     ( self . PenBrush                                 )
    ##########################################################################
    painter . setPen       ( PEN                                             )
    painter . setFont      ( F                                               )
    ##########################################################################
    return
  ############################################################################
  def boundingRect            ( self , text , dpi                          ) :
    ##########################################################################
    fs  = int                 ( self . Size * float ( dpi ) * 100.0 / 254.0  )
    ##########################################################################
    F   = self . Font
    F   . setPixelSize        ( fs                                           )
    ##########################################################################
    FMF = QFontMetricsF       ( F                                            )
    ##########################################################################
    return FMF . boundingRect ( text                                         )
  ############################################################################
  def assign ( self , font                                                 ) :
    ##########################################################################
    self . Font = font
    self . Size = font . CM
    ##########################################################################
    return
##############################################################################
