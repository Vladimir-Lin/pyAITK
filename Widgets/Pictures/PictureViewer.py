# -*- coding: utf-8 -*-
##############################################################################
## PictureViewer
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import binascii
import hashlib
import base64
##############################################################################
from   io           import BytesIO
from   wand . image import Image
from   PIL          import Image as Pillow
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
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
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
from   PyQt5 . QtWidgets              import QScrollArea
from   PyQt5 . QtWidgets              import QLabel
##############################################################################
from   AITK  . Pictures . Picture     import Picture     as Picture
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . VirtualGui        import VirtualGui  as VirtualGui
##############################################################################
class PictureViewer               ( QScrollArea , VirtualGui               ) :
  ############################################################################
  AssignImage = pyqtSignal        ( QImage                                   )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super (                    ) . __init__ ( parent                         )
    super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize                       ( self                           )
    self . setPlanFunction                  ( plan                           )
    self . Image = None
    self . Ratio = QSize          ( 100 , 100                                )
    ##########################################################################
    self . AssignImage . connect  ( self . setImage                          )
    ##########################################################################
    return
  ############################################################################
  def AssignPixmap    ( self                                               ) :
    ##########################################################################
    if                ( self . Image == None                               ) :
      return
    ##########################################################################
    PIX   = QPixmap . fromImage ( self . Image )
    ##########################################################################
    if ( ( self . Ratio . width ( ) != 100 ) or ( self . Ratio . width ( ) != 100 ) ) :
      ws    = self . Image . size ( )
      W     = int ( ws . width  ( ) * self . Ratio . width  ( ) / 100 )
      H     = int ( ws . height ( ) * self . Ratio . height ( ) / 100 )
      PIX   = PIX . scaled ( QSize ( W , H ) )
    ##########################################################################
    label = QLabel    (                                                      )
    label . setPixmap ( PIX                                                  )
    self  . setWidget ( label                                                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot(QImage)
  def setImage          ( self , image                                     ) :
    ##########################################################################
    self . Image = image
    self . AssignPixmap (                                                    )
    ##########################################################################
    return
  ############################################################################
  def BackgroundLoadFile      ( self , filename                            ) :
    ##########################################################################
    IMG  = QImage             ( filename                                     )
    self . AssignImage . emit ( IMG                                          )
    ##########################################################################
    return
  ############################################################################
  def loadFile          ( self , filename                                  ) :
    ##########################################################################
    self . Go           ( self . BackgroundLoadFile , ( filename , )         )
    ##########################################################################
    return
  ############################################################################
  def FetchImage                ( self , Uuid                              ) :
    ##########################################################################
    DB       = self . ConnectDB (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    FOUND    = False
    SUFFIX   = ""
    BLOB     = None
    PICTAB   = self . Tables    [ "Information"                              ]
    DPTTAB   = self . Tables    [ "Depot"                                    ]
    ##########################################################################
    QQ       = f"select `suffix` from {PICTAB} where ( `uuid` = {Uuid} ) ;"
    DB       . Query            ( QQ                                         )
    INF      = DB . FetchOne    (                                            )
    if                          ( ( INF != None ) and ( len ( INF ) > 0 )  ) :
      SUFFIX = INF              [ 0                                          ]
      FOUND  = True
    ##########################################################################
    if                          ( FOUND                                    ) :
      QQ     = f"select `file` from {DPTTAB} where ( `uuid` = {Uuid} ) ;"
      DB     . Query            ( QQ                                         )
      BLOBs  = DB . FetchOne    (                                            )
      if ( ( BLOBs != None ) and ( len ( BLOBs ) > 0 )                     ) :
        BLOB = BLOBs            [ 0                                          ]
      else                                                                   :
        FOUND  = False
    ##########################################################################
    DB      . Close             (                                            )
    ##########################################################################
    if                          ( not FOUND                                ) :
      return
    ##########################################################################
    if                          ( len ( SUFFIX ) <= 0                      ) :
      return
    ##########################################################################
    if                          ( BLOB == None                             ) :
      return
    ##########################################################################
    SS        = SUFFIX
    SS        = SS . lower      (                                            )
    ALLOWED   =                 [ "jpeg" , "jpg" , "png"                     ]
    if                          ( SS in ALLOWED                            ) :
      IMG     = QImage          (                                            )
      IMG     . loadFromData    ( BLOB , SUFFIX                              )
    else                                                                     :
      INTL    = Image           ( blob = BLOB                                )
      INTL    . format = "png"
      DAT     = BytesIO         (                                            )
      INTL    . save            ( file = DAT                                 )
      BLOB    = DAT . getvalue  (                                            )
      IMG     = QImage          (                                            )
      IMG     . loadFromData    ( BLOB , "png"                               )
    ##########################################################################
    self . AssignImage . emit   ( IMG                                        )
    ##########################################################################
    return
  ############################################################################
  def loadUuid          ( self , Uuid                                      ) :
    ##########################################################################
    self . Go           ( self . FetchImage , ( Uuid , )                     )
    ##########################################################################
    return
##############################################################################
