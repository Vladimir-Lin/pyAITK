# -*- coding: utf-8 -*-
##############################################################################
## GUI共同功能介面
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
from   PySide6               import QtCore
from   PySide6               import QtGui
from   PySide6               import QtWidgets
##############################################################################
from   PySide6 . QtCore      import *
from   PySide6 . QtGui       import *
from   PySide6 . QtWidgets   import *
##############################################################################
from           . AbstractGui import AbstractGui as AbstractGui
##############################################################################
class VirtualGui              ( AbstractGui                                ) :
  ############################################################################
  def __init__                ( self                                       ) :
    ##########################################################################
    super ( ) . __init__      (                                              )
    ##########################################################################
    self . SignalConnectors = {                                              }
    self . AtMenu           = False
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def Initialize               ( self , widget = None                      ) :
    super ( ) . Initialize     ( widget                                      )
    return
  ############################################################################
  def setAllFont                    ( self , widget , font                 ) :
    ##########################################################################
    widget  . setFont               ( font                                   )
    ##########################################################################
    widgets = widget . findChildren ( QtWidgets . QWidget                    )
    for w in widgets                                                         :
      self . setAllFont             ( w , font                               )
    ##########################################################################
    return
  ############################################################################
  def Frameless                     ( self , widget                        ) :
    ##########################################################################
    ## wflags   = widget . windowFlags (                                        )
    ## wflags   = Qt . WindowStaysOnTopHint
    wflags   = Qt . FramelessWindowHint
    wflags  |= Qt . CustomizeWindowHint
    wflags  &=                      ( 0xFFFFFFFF ^ Qt . WindowTitleHint      )
    widget . setWindowFlags         ( wflags                                 )
    ##########################################################################
    return wflags
  ############################################################################
  def addIntoWidget                 ( self , parent , widget               ) :
    ##########################################################################
    if                              ( parent == None                       ) :
      return
    ##########################################################################
    parent . addWidget              ( widget                                 )
    ##########################################################################
    return
  ############################################################################
  def allowDrag             ( self , dragDrop                              ) :
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . NoDragDrop   ) :
      return False
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . DragOnly     ) :
      return True
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . DropOnly     ) :
      return False
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . DragDrop     ) :
      return True
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . InternalMove ) :
      return False
    ##########################################################################
    return False
  ############################################################################
  def allowDrop             ( self , dragDrop                              ) :
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . NoDragDrop   ) :
      return False
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . DragOnly     ) :
      return False
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . DropOnly     ) :
      return True
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . DragDrop     ) :
      return True
    ##########################################################################
    if                      ( dragDrop == QAbstractItemView . InternalMove ) :
      return False
    ##########################################################################
    return False
  ############################################################################
  def StartingDrag                     ( self                              ) :
    ##########################################################################
    if                                 ( self . isDrag ( )                 ) :
      return
    ##########################################################################
    if                                 ( not self . hasDragItem ( )        ) :
      return
    ##########################################################################
    mime       = self . dragMime       (                                     )
    if                                 ( mime is None                      ) :
      return
    ##########################################################################
    DC                   = QCursor     ( Qt . ClosedHandCursor               )
    self       . Dumping = True
    self       . Drag    = QDrag       ( self . Gui                          )
    self       . Drag    . setMimeData ( mime                                )
    ##########################################################################
    if                                 ( mime . hasImage ( )               ) :
      image    = mime . imageData      (                                     )
      self     . Drag . setPixmap      ( QPixmap . fromImage ( image )       )
    else                                                                     :
      self     . Drag . setPixmap      ( DC . pixmap ( )                     )
    ##########################################################################
    dropAction = self . Drag . exec_   ( Qt . CopyAction | Qt . MoveAction   )
    self       . dragDone              ( dropAction , mime                   )
    self       . Dumping = False
    ##########################################################################
    return
  ############################################################################
  def CopyToFile            ( self                                         , \
                              filename                                     , \
                              toFile                                       , \
                              progressName                                 , \
                              progressFormat                               ) :
    ##########################################################################
    """
    bool      success = false                                                  ;
    QFileInfo SFI ( filename )                                                 ;
    QString   dFile      = QString("%1.part").arg(ToFile)                      ;
    int       dlen       = 1024 * 256                                          ;
    char      BUFF       [ 1024 * 256 ]                                        ;
    qint64    sourceSize = SFI . size ( )                                      ;
    qint64    destSize   = 0                                                   ;
    QFile     SF ( filename )                                                  ;
    QFile     TF ( dFile    )                                                  ;
    QDateTime StartT                                                           ;
    ////////////////////////////////////////////////////////////////////////////
    if ( SF . open ( QIODevice::ReadOnly ) )                                   {
      if ( TF . open ( QIODevice::WriteOnly ) )                                {
        bool      keepReading = true                                           ;
        int       pid                                                          ;
        qint64    value = 0                                                    ;
        bool      go    = true                                                 ;
        QDateTime T = nTimeNow                                                 ;
        pid   = plan -> Progress ( progressName , progressFormat )             ;
        plan -> Start ( pid , &value , &go )                                   ;
        qint64 ds = 0                                                          ;
        plan -> setRange ( pid , 0 , (int)(sourceSize/1024) )                  ;
        StartT = nTimeNow                                                      ;
        while ( keepReading && go )                                            {
          ds = SF . read ( BUFF , dlen )                                       ;
          if ( ds > 0 )                                                        {
            TF . write ( BUFF , ds )                                           ;
            destSize += ds                                                     ;
          } else keepReading = false                                           ;
          if ( sourceSize == destSize ) keepReading = false                    ;
          value = (int) ( destSize / 1024 )                                    ;
        }                                                                      ;
        if ( T.msecsTo(nTimeNow) < 1500 ) Time::skip(1500)                     ;
        plan -> Finish ( pid )                                                 ;
        TF . close ( )                                                         ;
      }                                                                        ;
      SF . close ( )                                                           ;
    }                                                                          ;
    ////////////////////////////////////////////////////////////////////////////
    success = ( sourceSize == destSize )                                       ;
    if ( success ) success = QFile::rename(dFile,ToFile)                       ;
    """
    ##########################################################################
    return False
  ############################################################################
  def addConnector                     ( self                              , \
                                         name                              , \
                                         sigfunc                           , \
                                         slotfunc                          , \
                                         ctype = Qt . AutoConnection       ) :
    ##########################################################################
    self . SignalConnectors [ name ] = { "signal" : sigfunc                , \
                                         "slot"   : slotfunc               , \
                                         "type"   : ctype                    }
    ##########################################################################
    return
  ############################################################################
  def onlyConnector             ( self , name                              ) :
    ##########################################################################
    if                          ( name not in self . SignalConnectors      ) :
      return
    ##########################################################################
    SIG   = self . SignalConnectors [ name ] [ "signal" ]
    SLT   = self . SignalConnectors [ name ] [ "slot"   ]
    ##########################################################################
    try                                                                      :
      SIG . disconnect          (                                            )
      SIG . connect             ( SLT                                        )
    except                                                                   :
      return
    ##########################################################################
    return
  ############################################################################
  def doConnector               ( self , name                              ) :
    ##########################################################################
    if                          ( name not in self . SignalConnectors      ) :
      return
    ##########################################################################
    SIG   = self . SignalConnectors [ name ] [ "signal" ]
    SLT   = self . SignalConnectors [ name ] [ "slot"   ]
    ##########################################################################
    try                                                                      :
      SIG . connect             ( SLT                                        )
    except                                                                   :
      return
    ##########################################################################
    return
  ############################################################################
  def undoConnector             ( self , name                              ) :
    ##########################################################################
    if                          ( name not in self . SignalConnectors      ) :
      return
    ##########################################################################
    SIG   = self . SignalConnectors [ name ] [ "signal" ]
    SLT   = self . SignalConnectors [ name ] [ "slot"   ]
    ##########################################################################
    try                                                                      :
      SIG . disconnect          ( SLT                                        )
    except                                                                   :
      return
    ##########################################################################
    return
  ############################################################################
  def removeConnector           ( self , name                              ) :
    ##########################################################################
    if                          ( name not in self . SignalConnectors      ) :
      return
    ##########################################################################
    del self . SignalConnectors [ name                                       ]
    ##########################################################################
    return
##############################################################################
