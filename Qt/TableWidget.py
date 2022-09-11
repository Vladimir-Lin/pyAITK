# -*- coding: utf-8 -*-
##############################################################################
## TableWidget
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
from   PyQt5 . QtCore                 import pyqtSlot
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QMimeData
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTableWidget
from   PyQt5 . QtWidgets              import QTableWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . VirtualGui             import VirtualGui  as VirtualGui
##############################################################################
class TableWidget ( QTableWidget , VirtualGui                              ) :
  ############################################################################
  SubmitStatusMessage     = pyqtSignal ( str , int                           )
  SubmitTtsTalk           = pyqtSignal ( str , int                           )
  SubmitUpdate            = pyqtSignal (                                     )
  emitBustle              = pyqtSignal (                                     )
  emitVacancy             = pyqtSignal (                                     )
  OnBusy                  = pyqtSignal (                                     )
  GoRelax                 = pyqtSignal (                                     )
  Leave                   = pyqtSignal ( QWidget                             )
  ############################################################################
  def __init__    ( self , parent = None , plan = None                     ) :
    ##########################################################################
    super (                   ) . __init__ ( parent                          )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    ##########################################################################
    self . SubmitStatusMessage . connect   ( self . AssignStatusMessage      )
    self . SubmitTtsTalk       . connect   ( self . DoTtsTalk                )
    self . SubmitUpdate        . connect   ( self . update                   )
    self . emitBustle          . connect   ( self . DoBustle                 )
    self . emitVacancy         . connect   ( self . DoVacancy                )
    self . OnBusy              . connect   ( self . AtBusy                   )
    self . GoRelax             . connect   ( self . OnRelax                  )
    ##########################################################################
    self . setAttribute                    ( Qt . WA_InputMethodEnabled      )
    self . setAcceptDrops                  ( True                            )
    self . setDragDropMode                 ( QAbstractItemView . DragDrop    )
    self . setHorizontalScrollBarPolicy    ( Qt . ScrollBarAsNeeded          )
    self . setVerticalScrollBarPolicy      ( Qt . ScrollBarAsNeeded          )
    ##########################################################################
    self . droppingAction = False
    self . VoiceJSON =  {                                                    }
    ##########################################################################
    return
  ############################################################################
  def Configure               ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def PrepareForActions ( self                                             ) :
    return
  ############################################################################
  def focusInEvent            ( self , event                               ) :
    ##########################################################################
    if                        ( self . focusIn ( event )                   ) :
      return
    ##########################################################################
    super ( ) . focusInEvent  ( event                                        )
    ##########################################################################
    return
  ############################################################################
  def focusOutEvent           ( self , event                               ) :
    ##########################################################################
    if                        ( self . focusOut ( event )                  ) :
      return
    ##########################################################################
    super ( ) . focusOutEvent ( event                                        )
    ##########################################################################
    return
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    ##########################################################################
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . contextMenuEvent ( event                                     )
    ##########################################################################
    return
  ############################################################################
  def defaultCloseEvent ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Shutdown ( )                              ) :
      event . accept    (                                                    )
    else                                                                     :
      event . ignore    (                                                    )
    ##########################################################################
    return
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    if                      ( self . Relocation ( )                        ) :
      event . accept        (                                                )
      return
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
    ##########################################################################
    return
  ############################################################################
  def showEvent           ( self , event                                   ) :
    ##########################################################################
    super ( ) . showEvent ( event                                            )
    self . Relocation     (                                                  )
    ##########################################################################
    return
  ############################################################################
  def dragEnterEvent    ( self , event                                     ) :
    ##########################################################################
    if                  ( self . allowDrop ( self . dragDropMode ( ) )     ) :
      if                ( self . dragEnter ( event )                       ) :
        event . acceptProposedAction (                                       )
        return
    ##########################################################################
    if                  ( self . PassDragDrop                              ) :
      super ( ) . dragEnterEvent ( event                                     )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def dragLeaveEvent    ( self , event                                     ) :
    ##########################################################################
    if                  ( self . removeDrop ( )                            ) :
      event . accept    (                                                    )
      return
    ##########################################################################
    if                  ( self . PassDragDrop                              ) :
      super ( ) . dragLeaveEvent ( event                                     )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def dragMoveEvent     ( self , event                                     ) :
    ##########################################################################
    if                  ( self . allowDrop ( self . dragDropMode ( ) )     ) :
      if                ( self . dragMove  ( event )                       ) :
        event . acceptProposedAction (                                       )
        return
    ##########################################################################
    if                  ( self . PassDragDrop                              ) :
      super ( ) . dragMoveEvent ( event                                      )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def dropEvent         ( self , event                                     ) :
    ##########################################################################
    if                  ( self . allowDrop ( self . dragDropMode ( ) )     ) :
      if                ( self . dropIn    ( event )                       ) :
        event . acceptProposedAction (                                       )
        return
    ##########################################################################
    if                  ( self . PassDragDrop                              ) :
      super ( ) . dropEvent ( event                                          )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent   ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Dumping                                   ) :
      event . ignore    (                                                    )
      return
    ##########################################################################
    if                  ( self . allowDrag ( self . dragDropMode ( ) )     ) :
      self . dragStart  ( event                                              )
    ##########################################################################
    super ( ) . mousePressEvent ( event                                      )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent    ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Dumping                                   ) :
      event . ignore    (                                                    )
      return
    ##########################################################################
    moving = True
    ##########################################################################
    if                  ( self . allowDrag  ( self . dragDropMode ( ) )    ) :
      if                ( self . dragMoving ( event )                      ) :
        ######################################################################
        event  . accept (                                                    )
        moving = False
        ######################################################################
        super ( ) . mouseReleaseEvent ( event                                )
        ######################################################################
        self   . ReleasePickings (                                           )
    ##########################################################################
    if                  ( moving                                           ) :
      super   ( ) . mouseMoveEvent    ( event                                )
    ##########################################################################
    return
  ############################################################################
  def mouseReleaseEvent   ( self , event                                   ) :
    ##########################################################################
    if                    ( self . Dumping                                 ) :
      event . ignore      (                                                  )
      return
    ##########################################################################
    if                    ( self . allowDrag ( self . dragDropMode ( ) )   ) :
      self . dragEnd      ( event                                            )
    ##########################################################################
    if                    ( self . isDrag ( )                              ) :
      ########################################################################
      self  . ReleaseDrag (                                                  )
      event . accept      (                                                  )
      ########################################################################
      return
    ##########################################################################
    super ( ) . mouseReleaseEvent ( event                                    )
    ##########################################################################
    return
  ############################################################################
  def hasDragItem                ( self                                    ) :
    ##########################################################################
    items = self . selectedItems (                                           )
    if                           ( len ( items ) <= 0                      ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def dragDone               ( self , dropIt , mime                        ) :
    return
  ############################################################################
  def dropNew                ( self , sourceWidget , mimeData , mousePos   ) :
    return True
  ############################################################################
  def dropMoving           ( self , sourceWidget , mimeData , mousePos     ) :
    return True
  ############################################################################
  def defaultDropMoving    ( self , sourceWidget , mimeData , mousePos     ) :
    ##########################################################################
    if                     ( self . droppingAction                         ) :
      return False
    ##########################################################################
    if                     ( sourceWidget != self                          ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( mousePos                                        )
    if                     ( self . NotOkay ( atItem )                     ) :
      return False
    if                     ( atItem . isSelected ( )                       ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def dropAppend             ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    if                       ( self . droppingAction                       ) :
      return False
    ##########################################################################
    return self . dropItems  (        sourceWidget , mimeData , mousePos     )
  ############################################################################
  def removeDrop             ( self                                        ) :
    return True
  ############################################################################
  def setDroppingAction ( self , dropping                                  ) :
    ##########################################################################
    self . droppingAction = dropping
    ##########################################################################
    return
  ############################################################################
  def defaultDropInObjects ( self , source , pos , JSON , column , func    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSON                           ) :
      return True
    ##########################################################################
    UUIDs  = JSON          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( atItem is None                                ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( column , Qt . UserRole                          )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    self . Go              ( func , ( UUID , UUIDs , )                       )
    ##########################################################################
    return   True
  ############################################################################
  def defaultDropInside ( self , source , JSON , func                      ) :
    ##########################################################################
    if                  ( "UUIDs" not in JSON                              ) :
      return True
    ##########################################################################
    UUIDs  = JSON       [ "UUIDs"                                            ]
    if                  ( len ( UUIDs ) <= 0                               ) :
      return True
    ##########################################################################
    self . Go           ( func , ( UUIDs , )                                 )
    ##########################################################################
    return   True
  ############################################################################
  def CreateDragMime                 ( self                                , \
                                       widget                              , \
                                       column                              , \
                                       mtype                               , \
                                       message                             ) :
    ##########################################################################
    items     = self . selectedItems (                                       )
    total     = len                  ( items                                 )
    if                               ( len ( items ) <= 0                  ) :
      return None
    ##########################################################################
    UUIDs     =                      [                                       ]
    for it in items                                                          :
      UUID    = it . data            ( column , Qt . UserRole                )
      UUIDs   . append               ( str ( UUID )                          )
    ##########################################################################
    JSONs     =                      { "Widget" : id ( widget )            , \
                                       "UUIDs"  : UUIDs                      }
    ##########################################################################
    mime      = QMimeData            (                                       )
    self      . setMime              ( mime , mtype , JSONs                  )
    ##########################################################################
    tooltip   = message . format     ( total                                 )
    QToolTip  . showText             ( QCursor . pos ( ) , tooltip           )
    ##########################################################################
    return mime
  ############################################################################
  @pyqtSlot                   (                                              )
  def DoBustle                ( self                                       ) :
    self . Bustle             (                                              )
    return
  ############################################################################
  def setBustle               ( self                                       ) :
    self . emitBustle  . emit (                                              )
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DoVacancy               ( self                                       ) :
    self . Vacancy            (                                              )
    return
  ############################################################################
  def setVacancy              ( self                                       ) :
    self . emitVacancy . emit (                                              )
    return
  ############################################################################
  @pyqtSlot                   (        str     , int                         )
  def AssignStatusMessage     ( self , message , timeout = 0               ) :
    self . statusMessage      (        message , timeout                     )
    return
  ############################################################################
  def ShowStatus                      ( self , message , timeout = 0       ) :
    self . SubmitStatusMessage . emit (        message , timeout             )
    return
  ############################################################################
  def DoTtsTalk                 ( self , message , locality                ) :
    ##########################################################################
    self . Talk                 (        message , locality                  )
    ##########################################################################
    return
  ############################################################################
  def TtsTalk                   ( self , message , locality                ) :
    ##########################################################################
    self . SubmitTtsTalk . emit (        message , locality                  )
    ##########################################################################
    return
  ############################################################################
  def DoUpdate                  ( self                                     ) :
    ##########################################################################
    self . SubmitUpdate . emit  (                                            )
    ##########################################################################
    return
  ############################################################################
  def AtBusy           ( self                                              ) :
    ##########################################################################
    self . doStartBusy (                                                     )
    ##########################################################################
    return
  ############################################################################
  def OnRelax          ( self                                              ) :
    ##########################################################################
    self . doStopBusy  (                                                     )
    ##########################################################################
    return
  ############################################################################
  def Shutdown                ( self                                       ) :
    ##########################################################################
    self . Leave . emit       ( self                                         )
    ##########################################################################
    return True
  ############################################################################
  def Relocation              ( self                                       ) :
    return False
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def Menu                    ( self , pos                                 ) :
    raise NotImplementedError (                                              )
  ############################################################################
  @pyqtSlot                   (                                              )
  def startup                 ( self                                       ) :
    raise NotImplementedError (                                              )
##############################################################################
