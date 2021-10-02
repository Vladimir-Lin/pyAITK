# -*- coding: utf-8 -*-
##############################################################################
## MajorListings
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
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt . TreeDock          import TreeDock as TreeDock
##############################################################################
class MajorListings                ( TreeDock                              ) :
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( dict                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames = None
    ##########################################################################
    self . setColumnCount          ( 1                                       )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                        ( self                               ) :
    return QSize                      ( 320 , 640                            )
  ############################################################################
  def FocusIn                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return False
    ##########################################################################
    self . LinkAction            ( "Insert" , self . InsertItem              )
    self . LinkAction            ( "Delete" , self . DeleteItems             )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def singleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( self . isItemPicked ( )                 ) :
      if ( column != self . CurrentItem [ "Column" ] )                       :
        self . removeParked      (                                           )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def stateChanged               ( self , item , column                    ) :
    return
  ############################################################################
  def Prepare                         ( self                               ) :
    raise NotImplementedError         (                                      )
  ############################################################################
  def PrepareItem                     ( self , UUID , NAME                 ) :
    ##########################################################################
    IT = QTreeWidgetItem              (                                      )
    IT . setText                      ( 0 , NAME                             )
    IT . setData                      ( 0 , Qt . UserRole , UUID             )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot()
  def InsertItem              ( self                                       ) :
    ##########################################################################
    item = QTreeWidgetItem    (                                              )
    item . setData            ( 0 , Qt . UserRole , 0                        )
    self . insertTopLevelItem ( 0 , item                                     )
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def DeleteItems                  ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def nameChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item , 0                                   )
    ##########################################################################
    if                          ( len ( msg ) <= 0                         ) :
      self . removeTopLevelItem ( item                                       )
      return
    ##########################################################################
    item   . setText            ( column ,              msg                  )
    ##########################################################################
    self   . removeParked       (                                            )
    self   . Go                 ( self . AssureUuidItem                    , \
                                  ( item , uuid , msg , )                    )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , name             ) :
    raise NotImplementedError      (                                         )
  ############################################################################
  @pyqtSlot(dict)
  def refresh                         ( self , JSON                        ) :
    ##########################################################################
    self    . clear                   (                                      )
    ##########################################################################
    UUIDs   = JSON                    [ "UUIDs"                              ]
    NAMEs   = JSON                    [ "NAMEs"                              ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT    = self . PrepareItem      ( U , NAMEs [ U ]                      )
      self  . addTopLevelItem         ( IT                                   )
    ##########################################################################
    self    . emitNamesShow . emit    (                                      )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery                ( self                               ) :
    raise NotImplementedError         (                                      )
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    UUIDs   =                         [                                      ]
    NAMEs   =                         {                                      }
    QQ      = self . ObtainUuidsQuery (                                      )
    if                                ( len ( QQ ) > 0                     ) :
      UUIDs = DB   . ObtainUuids      ( QQ                                   )
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "Names"                              ]
      NAMEs = self . GetNames         ( DB , TABLE , UUIDs                   )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
##############################################################################
