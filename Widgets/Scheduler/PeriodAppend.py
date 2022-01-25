# -*- coding: utf-8 -*-
##############################################################################
## PeriodEditor
## 時段列表
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
from   PyQt5 . QtWidgets                   import QTreeWidget
from   PyQt5 . QtWidgets                   import QTreeWidgetItem
from   PyQt5 . QtWidgets                   import QLineEdit
from   PyQt5 . QtWidgets                   import QComboBox
from   PyQt5 . QtWidgets                   import QSpinBox
##############################################################################
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
from   AITK  . Scheduler  . Project        import Project        as Project
from   AITK  . Scheduler  . Projects       import Projects       as Projects
from   AITK  . Scheduler  . Event          import Event          as Event
from   AITK  . Scheduler  . Events         import Events         as Events
from   AITK  . Scheduler  . Task           import Task           as Task
from   AITK  . Scheduler  . Tasks          import Tasks          as Tasks
##############################################################################
from         . AppendPeriod                import Ui_AppendPeriod
##############################################################################
class PeriodAppend                 ( Widget                                ) :
  ############################################################################
  emitShow            = pyqtSignal (                                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ui = Ui_AppendPeriod    (                                         )
    self . ui . setupUi            ( self                                    )
    ##########################################################################
    self . ClassTag  = "PeriodAppend"
    self . VoiceJSON =             {                                         }
    self . Period    = Periode     (                                         )
    self . Now       = StarDate    (                                         )
    ##########################################################################
    return
  ############################################################################
  def ProjectsChanged ( self , index ) :
    return
  ############################################################################
  def TasksChanged ( self , index ) :
    return
  
  ############################################################################
  def EventsChanged ( self , index ) :
    return
  ############################################################################
  def NameChanged ( self ) :
    return
  ############################################################################
  def StartTimeChanged( self , dt ) :
    return
  ############################################################################
  def FinishTimeChanged( self , dt ) :
    return
  ############################################################################
  def NoteChanged ( self ) :
    return
  ############################################################################
  def AppendPeriod ( self ) :
    return
##############################################################################
