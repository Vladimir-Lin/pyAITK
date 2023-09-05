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
class VtkModelPad                  ( QToolBox , VirtualGui                                ) :
  ############################################################################
  emitShow            = pyqtSignal (                                         )
  emitAskClose        = pyqtSignal (                                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super (                   ) . __init__ ( parent        , plan            )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize              ( self                                    )
    self . setPlanFunction         ( plan                                    )
    ##########################################################################
    self . setAttribute            ( Qt . WA_InputMethodEnabled              )
    ##########################################################################
    self . ui = Ui_VtkModelPadUi   (                                         )
    self . ui . setupUi            ( self                                    )
    ##########################################################################
    self . ClassTag       = "VtkModelPad"
    self . VoiceJSON      =        {                                         }
    self . ContentChanged = False
    ##########################################################################
    self . emitShow     . connect  ( self . show                             )
    self . emitAskClose . connect  ( self . AskToClose                       )
    ##########################################################################
    self . rWindow   = None
    self . renderer  = None
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
  def UpdateActors ( self                                                  ) :
    ##########################################################################
    print("UpdateActors")
    ##########################################################################
    return
  ############################################################################
  def UpdateCamera ( self                                                  ) :
    ##########################################################################
    print("UpdateCamera")
    ##########################################################################
    return
  ############################################################################
  def loading ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot   (                                                              )
  def startup ( self                                                       ) :
    ##########################################################################
    self . Go ( self . loading                                               )
    ##########################################################################
    return
##############################################################################
