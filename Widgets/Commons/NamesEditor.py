# -*- coding: utf-8 -*-
##############################################################################
## TreeWidget
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
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt        . VirtualGui import VirtualGui as VirtualGui
from   AITK  . Qt        . TreeWidget import TreeWidget as TreeWidget
##############################################################################
from   AITK  . Documents . Name       import Name       as NameItem
##############################################################################
class NamesEditor        ( TreeWidget , NameItem                           ) :
  ############################################################################
  def __init__           ( self , parent = None                            ) :
    ##########################################################################
    super ( TreeWidget , self ) . __init__   ( parent                        )
    super ( NameItem   , self ) . __init__   (                               )
    ##########################################################################
    return
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    Names  = self . Translations [ "NamesEditor" ] [ "Labels" ]
    Items  = self . tableItems   (                                           )
    ##########################################################################
    self . KEYs =                [                                           ]
    self . KEYs . append         ( "id"                                      )
    self . KEYs . append         ( "name"                                    )
    for it in Items                                                          :
      if ( ( it not in self . KEYs ) and ( it not in [ "uuid" ] ) )          :
       self  . KEYs . append     ( it                                        )
    ##########################################################################
    TOTAL    = len ( self . KEYs )
    self     . setColumnCount    ( TOTAL + 1                                 )
    ##########################################################################
    self     . LabelItem = QTreeWidgetItem (                                 )
    for i , it in enumerate      ( self . KEYs                             ) :
      self   . LabelItem . setText          ( i , Names [ it ]               )
      self   . LabelItem . setTextAlignment ( i , Qt . AlignHCenter          )
    self     . LabelItem . setText          ( TOTAL , ""                     )
    self     . setHeaderItem     ( self . LabelItem                          )
    ##########################################################################
    self     . setColumnWidth    ( TOTAL     , 3                             )
    ##########################################################################
    self     . setColumnHidden   ( 0         , True                          )
    self     . setColumnHidden   ( TOTAL - 1 , True                          )
    ##########################################################################
    return
  ############################################################################
  def Configure ( self ) :
    return
  ############################################################################
  def startup ( self ) :
    return
  ############################################################################
  def FocusIn ( self ) :
    return True
  ############################################################################
  def FocusOut ( self ) :
    return True
  ############################################################################
  def singleClicked ( self , item , column ) :
    return
  ############################################################################
  def doubleClicked ( self , item , column ) :
    return
  ############################################################################
  def Insert ( self ) :
    return
  ############################################################################
  def Delete ( self ) :
    return
  ############################################################################
  def Menu ( self , pos ) :
    return
##############################################################################
