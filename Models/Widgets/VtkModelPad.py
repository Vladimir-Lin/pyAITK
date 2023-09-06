# -*- coding: utf-8 -*-
##############################################################################
## VtkModelPad
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import math
import shutil
##############################################################################
import vtk
##############################################################################
from   PyQt5                               import QtCore
from   PyQt5                               import QtGui
from   PyQt5                               import QtWidgets
##############################################################################
from   PyQt5 . QtCore                      import QObject
from   PyQt5 . QtCore                      import pyqtSignal
from   PyQt5 . QtCore                      import pyqtSlot
from   PyQt5 . QtCore                      import Qt
from   PyQt5 . QtCore                      import QPoint
from   PyQt5 . QtCore                      import QPointF
from   PyQt5 . QtCore                      import QSize
from   PyQt5 . QtCore                      import QDateTime
##############################################################################
from   PyQt5 . QtGui                       import QIcon
from   PyQt5 . QtGui                       import QCursor
from   PyQt5 . QtGui                       import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets                   import QApplication
from   PyQt5 . QtWidgets                   import QWidget
from   PyQt5 . QtWidgets                   import qApp
from   PyQt5 . QtWidgets                   import QMenu
from   PyQt5 . QtWidgets                   import QAction
from   PyQt5 . QtWidgets                   import QShortcut
from   PyQt5 . QtWidgets                   import QAbstractItemView
from   PyQt5 . QtWidgets                   import QStackedWidget
from   PyQt5 . QtWidgets                   import QToolBox
from   PyQt5 . QtWidgets                   import QTreeWidget
from   PyQt5 . QtWidgets                   import QTreeWidgetItem
from   PyQt5 . QtWidgets                   import QLineEdit
from   PyQt5 . QtWidgets                   import QComboBox
from   PyQt5 . QtWidgets                   import QSpinBox
from   PyQt5 . QtWidgets                   import QMessageBox
##############################################################################
from   AITK  . Qt . VirtualGui             import VirtualGui     as VirtualGui
from   AITK  . Qt . MenuManager            import MenuManager    as MenuManager
from   AITK  . Qt . Widget                 import Widget         as Widget
##############################################################################
from   AITK  . Essentials . Relation       import Relation       as Relation
from   AITK  . Calendars  . StarDate       import StarDate       as StarDate
from   AITK  . Calendars  . Periode        import Periode        as Periode
from   AITK  . Documents  . Notes          import Notes          as Notes
from   AITK  . Documents  . Variables      import Variables      as Variables
from   AITK  . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK  . VTK . Wrapper               import Wrapper        as VtkWrapper
##############################################################################
from         . VtkModelPadUi               import Ui_VtkModelPadUi
##############################################################################
class VtkModelPad                  ( QStackedWidget , VirtualGui           ) :
  ############################################################################
  emitShow            = pyqtSignal (                                         )
  emitAskClose        = pyqtSignal (                                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super (                   ) . __init__ ( parent                          )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize              ( self                                    )
    self . setPlanFunction         ( plan                                    )
    ##########################################################################
    self . setAttribute            ( Qt . WA_InputMethodEnabled              )
    ##########################################################################
    self . ui = Ui_VtkModelPadUi   (                                         )
    self . ui . setupUi            ( self                                    )
    ##########################################################################
    self . ui . Camera . setWidget ( self . ui . CameraTemplate              )
    ##########################################################################
    self . ui . ToolBox . addItem                                            (
      self . ui . ActorsTemplate                                             ,
      self . ui . ActorsTemplate . toolTip (                               ) )
    ##########################################################################
    self . ui . PositionX  . setMinimum ( - sys . float_info . max           )
    self . ui . PositionY  . setMinimum ( - sys . float_info . max           )
    self . ui . PositionZ  . setMinimum ( - sys . float_info . max           )
    ##########################################################################
    self . ui . FocalX     . setMinimum ( - sys . float_info . max           )
    self . ui . FocalY     . setMinimum ( - sys . float_info . max           )
    self . ui . FocalZ     . setMinimum ( - sys . float_info . max           )
    ##########################################################################
    self . ui . ViewUpX    . setMinimum ( - sys . float_info . max           )
    self . ui . ViewUpY    . setMinimum ( - sys . float_info . max           )
    self . ui . ViewUpZ    . setMinimum ( - sys . float_info . max           )
    ##########################################################################
    self . ui . Distance   . setMinimum ( - sys . float_info . max           )
    self . ui . Roll       . setMinimum ( - sys . float_info . max           )
    self . ui . ViewAngle  . setMinimum ( - sys . float_info . max           )
    ##########################################################################
    self . ui . PositionX  . setMaximum (   sys . float_info . max           )
    self . ui . PositionY  . setMaximum (   sys . float_info . max           )
    self . ui . PositionZ  . setMaximum (   sys . float_info . max           )
    ##########################################################################
    self . ui . FocalX     . setMaximum (   sys . float_info . max           )
    self . ui . FocalY     . setMaximum (   sys . float_info . max           )
    self . ui . FocalZ     . setMaximum (   sys . float_info . max           )
    ##########################################################################
    self . ui . ViewUpX    . setMaximum (   sys . float_info . max           )
    self . ui . ViewUpY    . setMaximum (   sys . float_info . max           )
    self . ui . ViewUpZ    . setMaximum (   sys . float_info . max           )
    ##########################################################################
    self . ui . Distance   . setMaximum (   sys . float_info . max           )
    self . ui . Roll       . setMaximum (   sys . float_info . max           )
    self . ui . ViewAngle  . setMaximum (   sys . float_info . max           )
    ##########################################################################
    self . ClassTag       = "VtkModelPad"
    self . VoiceJSON      =        {                                         }
    self . ContentChanged = False
    ##########################################################################
    self . emitShow     . connect  ( self . show                             )
    self . emitAskClose . connect  ( self . AskToClose                       )
    ##########################################################################
    self . rWindow  = None
    self . renderer = None
    self . model    = None
    ##########################################################################
    return
  ############################################################################
  def closeEvent                    ( self , event                         ) :
    ##########################################################################
    if                              ( self . ContentChanged                ) :
      ########################################################################
      event   . ignore              (                                        )
      self    . emitAskClose . emit (                                        )
      ########################################################################
      return
    ##########################################################################
    super ( ) . closeEvent          ( event                                  )
    ##########################################################################
    return
  ############################################################################
  def AskToClose                  ( self                                   ) :
    ##########################################################################
    MSG  = self . getMenuItem     ( "ReallyQuit"                             )
    OKAY = QMessageBox . question ( self , self . windowTitle ( ) , MSG      )
    ##########################################################################
    if                            ( OKAY != QMessageBox . Yes              ) :
      return
    ##########################################################################
    self . ContentChanged = False
    self . close                  (                                          )
    ##########################################################################
    return
  ############################################################################
  def UpdateActors                         ( self                          ) :
    ##########################################################################
    CNT    = 0
    actors = self . renderer . GetActors   (                                 )
    ##########################################################################
    self   . ui . ActorsBox . blockSignals ( True                            )
    ##########################################################################
    self   . ui . ActorsBox . clear        (                                 )
    ##########################################################################
    NAME   = self . getMenuItem            ( "EmptyActor"                    )
    self   . ui . ActorsBox . addItem      ( NAME , -1                       )
    ##########################################################################
    for actor in actors                                                      :
      ########################################################################
      NAME = self . model . AitkJSON [ "Actors" ] [ f"{CNT}" ] [ "Name"      ]
      ########################################################################
      self . ui . ActorsBox . addItem      ( NAME , CNT                      )
      ########################################################################
      CNT  = CNT + 1
    ##########################################################################
    self   . ui . ActorsBox . blockSignals ( False                           )
    ##########################################################################
    return
  ############################################################################
  def UpdateCamera                           ( self                        ) :
    ##########################################################################
    c    = self . renderer . GetActiveCamera (                               )
    v    = self . renderer . GetVTKWindow    (                               )
    p    = c    . GetPosition                (                               )
    f    = c    . GetFocalPoint              (                               )
    u    = c    . GetViewUp                  (                               )
    d    = c    . GetDistance                (                               )
    r    = c    . GetRoll                    (                               )
    a    = c    . GetViewAngle               (                               )
    vw   = v    . GetSize                    (                               )
    w    = vw                                [ 0                             ]
    h    = vw                                [ 1                             ]
    ##########################################################################
    self . ui . PositionX  . blockSignals    ( True                          )
    self . ui . PositionY  . blockSignals    ( True                          )
    self . ui . PositionZ  . blockSignals    ( True                          )
    ##########################################################################
    self . ui . FocalX     . blockSignals    ( True                          )
    self . ui . FocalY     . blockSignals    ( True                          )
    self . ui . FocalZ     . blockSignals    ( True                          )
    ##########################################################################
    self . ui . ViewUpX    . blockSignals    ( True                          )
    self . ui . ViewUpY    . blockSignals    ( True                          )
    self . ui . ViewUpZ    . blockSignals    ( True                          )
    ##########################################################################
    self . ui . Distance   . blockSignals    ( True                          )
    self . ui . Roll       . blockSignals    ( True                          )
    self . ui . Width      . blockSignals    ( True                          )
    self . ui . Height     . blockSignals    ( True                          )
    self . ui . ViewAngle  . blockSignals    ( True                          )
    ##########################################################################
    self . ui . PositionX  . setValue        ( p [ 0                       ] )
    self . ui . PositionY  . setValue        ( p [ 1                       ] )
    self . ui . PositionZ  . setValue        ( p [ 2                       ] )
    ##########################################################################
    self . ui . FocalX     . setValue        ( f [ 0                       ] )
    self . ui . FocalY     . setValue        ( f [ 1                       ] )
    self . ui . FocalZ     . setValue        ( f [ 2                       ] )
    ##########################################################################
    self . ui . ViewUpX    . setValue        ( u [ 0                       ] )
    self . ui . ViewUpY    . setValue        ( u [ 1                       ] )
    self . ui . ViewUpZ    . setValue        ( u [ 2                       ] )
    ##########################################################################
    self . ui . Distance   . setValue        ( d                             )
    self . ui . Roll       . setValue        ( r                             )
    self . ui . Width      . setValue        ( w                             )
    self . ui . Height     . setValue        ( h                             )
    self . ui . ViewAngle  . setValue        ( a                             )
    ##########################################################################
    self . ui . PositionX  . blockSignals    ( False                         )
    self . ui . PositionY  . blockSignals    ( False                         )
    self . ui . PositionZ  . blockSignals    ( False                         )
    ##########################################################################
    self . ui . FocalX     . blockSignals    ( False                         )
    self . ui . FocalY     . blockSignals    ( False                         )
    self . ui . FocalZ     . blockSignals    ( False                         )
    ##########################################################################
    self . ui . ViewUpX    . blockSignals    ( False                         )
    self . ui . ViewUpY    . blockSignals    ( False                         )
    self . ui . ViewUpZ    . blockSignals    ( False                         )
    ##########################################################################
    self . ui . Distance   . blockSignals    ( False                         )
    self . ui . Roll       . blockSignals    ( False                         )
    self . ui . Width      . blockSignals    ( False                         )
    self . ui . Height     . blockSignals    ( False                         )
    self . ui . ViewAngle  . blockSignals    ( False                         )
    ##########################################################################
    return
  ############################################################################
  def loading ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot             (                                                    )
  def startup           ( self                                             ) :
    ##########################################################################
    self . UpdateCamera ( )
    self . UpdateActors ( )
    ##########################################################################
    self . Go           ( self . loading                                     )
    ##########################################################################
    return
##############################################################################
