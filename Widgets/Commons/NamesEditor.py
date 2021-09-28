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
  emitNamesShow = pyqtSignal     (                                           )
  emitAllNames  = pyqtSignal     ( list                                      )
  ############################################################################
  def __init__           ( self , parent = None                            ) :
    ##########################################################################
    super ( TreeWidget , self ) . __init__   ( parent                        )
    super ( NameItem   , self ) . __init__   (                               )
    ##########################################################################
    return
  ############################################################################
  def Prepare                     ( self                                   ) :
    ##########################################################################
    Names  = self . Translations  [ "NamesEditor" ] [ "Labels"               ]
    Items  = self . tableItems    (                                          )
    ##########################################################################
    self . KEYs =                 [ "id"                                     ,
                                    "name"                                   ,
                                    "locality"                               ,
                                    "relevance"                              ,
                                    "priority"                               ,
                                    "flags"                                  ,
                                    "utf8"                                   ,
                                    "length"                                 ,
                                    "ltime"                                  ]
    ##########################################################################
    TOTAL    = len                ( self . KEYs                              )
    self     . setColumnCount     ( TOTAL + 1                                )
    ##########################################################################
    self     . LabelItem = QTreeWidgetItem (                                 )
    for i , it in enumerate       ( self . KEYs                            ) :
      self   . LabelItem . setText          ( i , Names [ it ]               )
      self   . LabelItem . setTextAlignment ( i , Qt . AlignHCenter          )
    self     . LabelItem . setText          ( TOTAL , ""                     )
    self     . setHeaderItem      ( self . LabelItem                         )
    ##########################################################################
    self     . setColumnWidth     ( TOTAL     , 3                            )
    ##########################################################################
    self     . setColumnHidden    ( 0         , True                         )
    self     . setColumnHidden    ( TOTAL - 1 , True                         )
    ##########################################################################
    self     . setRootIsDecorated ( False                                    )
    ##########################################################################
    self     . emitNamesShow . connect ( self . show                         )
    self     . emitAllNames  . connect ( self . refresh                      )
    ##########################################################################
    self     . MountClicked       ( 2                                        )
    ##########################################################################
    self     . setPrepared        ( True                                     )
    ##########################################################################
    return
  ############################################################################
  def closeEvent                 ( self , event                            ) :
    ##########################################################################
    if                           ( self . TryClose ( )                     ) :
      event . accept             (                                           )
    else                                                                     :
      event . ignore             (                                           )
    ##########################################################################
    return
  ############################################################################
  def Configure                  ( self                                    ) :
    return
  ############################################################################
  def FocusIn                    ( self                                    ) :
    print("FocusIn")
    return False
  ############################################################################
  def FocusOut                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def singleClicked ( self , item , column ) :
    print("singleClicked")
    return
  ############################################################################
  def doubleClicked ( self , item , column ) :
    print("doubleClicked")
    return
  ############################################################################
  def stateChanged  ( self , item , column ) :
    print("stateChanged")
    return
  ############################################################################
  def Insert ( self ) :
    print("Insert")
    return
  ############################################################################
  def Delete ( self ) :
    print("Delete")
    return
  ############################################################################
  def Menu ( self , pos ) :
    print(pos)
    return
  ############################################################################
  def TryClose ( self ) :
    self . Prepared = False
    print("TryClose")
    return True
  ############################################################################
  def refresh                       ( self , All                           ) :
    ##########################################################################
    self . clear                    (                                        )
    TRX     = self . Translations   [ "NamesEditor"                          ]
    ##########################################################################
    for IT in All                                                            :
      ########################################################################
      NT    = QTreeWidgetItem       (                                        )
      ########################################################################
      L     = IT                    [ 2                                      ]
      R     = IT                    [ 4                                      ]
      REL   = TRX                   [ "Relevance" ] [ str ( R )              ]
      LANG  = TRX                   [ "Languages" ] [ str ( L )              ]
      S     = IT                    [ 8                                      ]
      try                                                                    :
        S   = S . decode            ( "utf-8"                                )
      except ( UnicodeDecodeError , AttributeError )                         :
        pass
      ########################################################################
      NT    . setText               ( 0 , str ( IT [  0 ] )                  )
      ########################################################################
      NT    . setText               ( 1 , str ( S         )                  )
      ########################################################################
      NT    . setText               ( 2 , str ( LANG      )                  )
      ########################################################################
      NT    . setText               ( 3 , str ( REL       )                  )
      ########################################################################
      NT    . setText               ( 4 , str ( IT [  3 ] )                  )
      NT    . setTextAlignment      ( 4 , Qt.AlignRight                      )
      ########################################################################
      NT    . setText               ( 5 , str ( IT [  5 ] )                  )
      NT    . setTextAlignment      ( 5 , Qt.AlignRight                      )
      ########################################################################
      NT    . setText               ( 6 , str ( IT [  6 ] )                  )
      NT    . setTextAlignment      ( 6 , Qt.AlignRight                      )
      ########################################################################
      NT    . setText               ( 7 , str ( IT [  7 ] )                  )
      NT    . setTextAlignment      ( 7 , Qt.AlignRight                      )
      ########################################################################
      NT    . setText               ( 8 , str ( IT [  9 ] )                  )
      ########################################################################
      NT    . setText               ( 9 , ""                                 )
      ########################################################################
      self  . addTopLevelItem       ( NT                                     )
    ##########################################################################
    self . emitNamesShow . emit     (                                        )
    ##########################################################################
    TOTAL   = len                   ( self . KEYs                            )
    for i in range                  ( 0 , TOTAL - 1                        ) :
      self  . resizeColumnToContents ( i )
    ##########################################################################
    return
  ############################################################################
  def loading                       ( self                                 ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      self . emitNamesShow . emit   (                                        )
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      self . emitNamesShow . emit   (                                        )
      return
    ##########################################################################
    ALL    = self . FetchEverything ( DB , self . Tables [ "Names" ]         )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    if                              ( len ( ALL ) <= 0                     ) :
      self . emitNamesShow . emit   (                                        )
    ##########################################################################
    self   . emitAllNames  . emit   ( ALL                                    )
    ##########################################################################
    return
  ############################################################################
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . Prepared                     ) :
      self . Prepare             (                                           )
    ##########################################################################
    threading . Thread ( target = self . loading ) . start (                 )
    ##########################################################################
    return
##############################################################################
