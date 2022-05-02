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
from   AITK  . People . Faces   . VcfFaceRegion    import VcfFaceRegion    as VcfFaceRegion
from   AITK  . People . Widgets . VcfPeoplePicture import VcfPeoplePicture as VcfPeoplePicture
##############################################################################
class PictureEditor               ( VcfWidget                              ) :
  ############################################################################
  Adjustment   = pyqtSignal       ( QWidget , QSize                          )
  JsonCallback = pyqtSignal       ( dict                                     )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          (        parent ,        plan              )
    ##########################################################################
    self . setJsonCaller          ( self . JsonCaller                        )
    self . JsonCallback . connect ( self . JsonAccepter                      )
    ##########################################################################
    return
  ############################################################################
  def JsonCaller               ( self , JSON                               ) :
    ##########################################################################
    self . JsonCallback . emit (        JSON                                 )
    ##########################################################################
    return
  ############################################################################
  def JsonAccepter              ( self , JSON                              ) :
    ##########################################################################
    CALLER = JSON               [ "Function"                                 ]
    ##########################################################################
    if                          ( CALLER == "DeleteItem"                   ) :
      ########################################################################
      ITEM = JSON               [ "Item"                                     ]
      self . takeItem           ( ITEM                                       )
      self . Scene . removeItem ( ITEM                                       )
      ########################################################################
      return
    ##########################################################################
    if                          ( CALLER == "AddFaceRegion"                ) :
      ########################################################################
      ITEM = JSON               [ "Item"                                     ]
      RECT = JSON               [ "Rectangle"                                ]
      self . AddFaceRegion      ( ITEM , RECT                                )
      ########################################################################
      return
    ##########################################################################
    if                          ( CALLER == "AddPicture"                   ) :
      ########################################################################
      PIC  = JSON               [ "Picture"                                  ]
      Z    = JSON               [ "Z"                                        ]
      self . AddPicture         ( PIC , Z                                    )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def WindowSizeView             ( self , size                             ) :
    ##########################################################################
    self . View = self . asPaper ( self . available ( size )                 )
    self . Scene . setSceneRect  ( self . View                               )
    self . setTransform          ( self . Transform                          )
    ##########################################################################
    return
  ############################################################################
  def AddFaceRegion              ( self , parent , rect                    ) :
    ##########################################################################
    PM   = QPoint                ( rect . x     ( ) , rect . y      ( )      )
    SP   = self   . mapToScene   ( PM                                        )
    XS   = parent . mapFromScene ( SP                                        )
    XP   = parent . pointToPaper ( XS                                        )
    ##########################################################################
    PM   = QPoint                ( rect . width ( ) , rect . height ( )      )
    SP   = self   . mapToScene   ( PM                                        )
    FS   = parent . mapFromScene ( SP                                        )
    MP   = parent . pointToPaper ( FS                                        )
    ##########################################################################
    RR   = QRectF                ( XP . x ( ) , XP . y ( )                 , \
                                   MP . x ( ) , MP . y ( )                   )
    ##########################################################################
    VRIT = VcfFaceRegion         ( self , parent  , self . PlanFunc          )
    VRIT . setOptions            ( self . Options , False                    )
    self . assignItemProperties  ( VRIT                                      )
    VRIT . setMenuCaller         ( self . MenuCallerEmitter                  )
    VRIT . Region      = rect
    VRIT . PictureItem = parent
    VRIT . setRange              ( RR                                        )
    ##########################################################################
    self . addItem               ( VRIT , parent                             )
    ## self . Scene . addItem       ( VRIT                                      )
    ##########################################################################
    VRIT . prepareGeometryChange (                                           )
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
  def AddPicture                  ( self , PIC , Z                         ) :
    ##########################################################################
    VRIT = VcfPeoplePicture       ( self , None , self . PlanFunc            )
    VRIT . setOptions             ( self . Options , False                   )
    self . assignItemProperties   ( VRIT                                     )
    VRIT . setMenuCaller          ( self . MenuCallerEmitter                 )
    VRIT . setZValue              ( Z                                        )
    VRIT . PICOP = PIC
    VRIT . Image = PIC . toQImage (                                          )
    VRIT . asImageRect            (                                          )
    ##########################################################################
    self . addItem                ( VRIT                                     )
    self . Scene . addItem        ( VRIT                                     )
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
    VRIT . setMenuCaller        ( self . MenuCallerEmitter                   )
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
