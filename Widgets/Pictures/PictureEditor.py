# -*- coding: utf-8 -*-
##############################################################################
## PictureEditor
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
from   io                              import BytesIO
from   wand . image                    import Image
from   PIL                             import Image        as Pillow
##############################################################################
from   PyQt5                           import QtCore
from   PyQt5                           import QtGui
from   PyQt5                           import QtWidgets
##############################################################################
from   PyQt5 . QtCore                  import QObject
from   PyQt5 . QtCore                  import pyqtSignal
from   PyQt5 . QtCore                  import pyqtSlot
from   PyQt5 . QtCore                  import Qt
from   PyQt5 . QtCore                  import QPoint
from   PyQt5 . QtCore                  import QPointF
from   PyQt5 . QtCore                  import QSize
from   PyQt5 . QtCore                  import QSizeF
from   PyQt5 . QtCore                  import QRect
from   PyQt5 . QtCore                  import QRectF
##############################################################################
from   PyQt5 . QtGui                   import QIcon
from   PyQt5 . QtGui                   import QPixmap
from   PyQt5 . QtGui                   import QImage
from   PyQt5 . QtGui                   import QCursor
from   PyQt5 . QtGui                   import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets               import QApplication
from   PyQt5 . QtWidgets               import QWidget
from   PyQt5 . QtWidgets               import qApp
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAction
from   PyQt5 . QtWidgets               import QShortcut
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QScrollArea
from   PyQt5 . QtWidgets               import QLabel
from   PyQt5 . QtWidgets               import QFileDialog
##############################################################################
from   AITK  . Pictures . Picture      import Picture      as PictureItem
from   AITK  . Pictures . Gallery      import Gallery      as GalleryItem
##############################################################################
from   AITK  . Qt       . MenuManager  import MenuManager  as MenuManager
from   AITK  . VCF      . VcfWidget    import VcfWidget    as VcfWidget
from   AITK  . VCF      . VcfItem      import VcfItem      as VcfItem
from   AITK  . VCF      . VcfRectangle import VcfRectangle as VcfRectangle
from   AITK  . People . Widgets . VcfPeoplePicture import VcfPeoplePicture as VcfPeoplePicture
##############################################################################
class PictureEditor        ( VcfWidget                                     ) :
  ############################################################################
  Adjustment = pyqtSignal  ( QWidget , QSize                                 )
  ############################################################################
  def __init__             ( self , parent = None , plan = None            ) :
    ##########################################################################
    super ( ) . __init__   (        parent ,        plan                     )
    ##########################################################################
    return
  ############################################################################
  def DoAdjustments            ( self , SIZE                               ) :
    ##########################################################################
    self . setSizeSuggestion   ( SIZE . width ( ) , SIZE . height ( )        )
    self . resize              ( SIZE                                        )
    ##########################################################################
    pw   = self . parentWidget (                                             )
    if                         ( "MdiSubWindow" not in type(pw).__name__   ) :
      return
    ##########################################################################
    self . Adjustment . emit   ( pw , SIZE                                   )
    ##########################################################################
    return
  ############################################################################
  def assignPicture             ( self , Uuid                              ) :
    ##########################################################################
    self . PerfectView          (                                            )
    ##########################################################################
    VRIT = VcfPeoplePicture     ( self , None , self . PlanFunc              )
    VRIT . setOptions           ( self . Options , False                     )
    self . assignItemProperties ( VRIT                                       )
    VRIT . LoadImage            ( Uuid                                       )
    VRIT . asImageRect          (                                            )
    FS   = VRIT . ImageSize     (                                            )
    ##########################################################################
    self . addItem              ( VRIT                                       )
    self . Scene . addItem      ( VRIT                                       )
    self . setPrepared          ( True                                       )
    self . DoAdjustments        ( FS                                         )
    ##########################################################################
    return
##############################################################################
