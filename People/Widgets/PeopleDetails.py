# -*- coding: utf-8 -*-
##############################################################################
## PeopleDetails
## 人物詳細資訊
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
from         . PeopleDetailsUI             import Ui_PeopleDetailsUI
##############################################################################
class PeopleDetails                 ( Widget                               ) :
  ############################################################################
  DynamicVariantTables = pyqtSignal ( str , dict                             )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            (        parent        , plan            )
    ##########################################################################
    self . ui = Ui_PeopleDetailsUI  (                                        )
    self . ui . setupUi             ( self                                   )
    ##########################################################################
    self . PeopleUuid = 0
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
  def Relocation                            ( self                         ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachExternalFunction ( self , FUNC                                 ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PeopleUuidChanged                       ( self                       ) :
    ##########################################################################
    PUID      = self . ui . PeopleUuid . text (                              )
    try                                                                      :
      PUID    = int                           ( PUID                         )
    except                                                                   :
      return
    ##########################################################################
    self . PeopleUuid = PUID
    ##########################################################################
    return
  ############################################################################
  def TablesUpdated                       ( self , JSON                    ) :
    ##########################################################################
    print(JSON)
    ##########################################################################
    return
  ############################################################################
  def TablesEditing                     ( self                             ) :
    ##########################################################################
    TITLE = self . windowTitle          (                                    )
    JSON  =                             { "Callback" : self . TablesUpdated  ,
                                          "Tables"   : self . Tables         }
    self  . DynamicVariantTables . emit ( str ( TITLE ) , JSON               )
    ##########################################################################
    return
  ############################################################################
  def startup                             ( self                           ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################
