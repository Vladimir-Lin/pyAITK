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
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . VirtualGui        import VirtualGui  as VirtualGui
##############################################################################
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . Pictures   . Picture   import Picture     as Picture
from   AITK  . Pictures   . Gallery   import Gallery     as GalleryItem
##############################################################################
class PictureViewer               ( QScrollArea , VirtualGui               ) :
  ############################################################################
  AssignImage   = pyqtSignal      ( QImage                                   )
  AssignGallery = pyqtSignal      ( list                                     )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super (                    ) . __init__ ( parent                         )
    super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize                       ( self                           )
    self . setPlanFunction                  ( plan                           )
    self . Image    = None
    self . Pictures = [ ]
    self . LABELs   = [ ]
    self . Ratio = QSize           ( 100 , 100                               )
    self . ZoomLevel = 10
    self . MaxWidth  = 0
    ##########################################################################
    self . setPrepared             ( True                                    )
    ##########################################################################
    self . AssignImage   . connect ( self . setImage                         )
    self . AssignGallery . connect ( self . setGallery                       )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 320 , 320 )                       )
  ############################################################################
  def focusInEvent            ( self , event                               ) :
    ##########################################################################
    if                        ( self . focusIn ( event )                   ) :
      return
    ##########################################################################
    super ( ) . focusInEvent  ( event                                        )
    ##########################################################################
    return
  ############################################################################
  def focusOutEvent           ( self , event                               ) :
    ##########################################################################
    if                        ( self . focusOut ( event )                  ) :
      return
    ##########################################################################
    super ( ) . focusOutEvent ( event                                        )
    ##########################################################################
    return
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    ##########################################################################
    ## if                           ( self . Menu ( event . pos ( ) )         ) :
    ##   event . accept             (                                           )
    ##   return
    ##########################################################################
    super ( ) . contextMenuEvent ( event                                     )
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
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"    , self . windowTitle ( )              )
    ##########################################################################
    self . LinkAction     ( "ZoomIn"   , self . ZoomIn                       )
    self . LinkAction     ( "ZoomOut"  , self . ZoomOut                      )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "ZoomIn"  , self . ZoomIn  , False              )
    self . LinkAction      ( "ZoomOut" , self . ZoomOut , False              )
    ##########################################################################
    ## self . Leave . emit    ( self                                            )
    ## if                     ( self . Shutdown ( )                           ) :
    ##   event . accept       (                                                 )
    ##   return
    ##########################################################################
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def FocusOut                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def toPixmap                  ( self , image                             ) :
    ##########################################################################
    PIX   = QPixmap . fromImage (        image                               )
    ##########################################################################
    if ( ( self . Ratio . width ( ) != 100 ) or ( self . Ratio . width ( ) != 100 ) ) :
      ########################################################################
      ws  = image . size        (                                            )
      W   = int ( ws . width  ( ) * self . Ratio . width  ( ) / 100          )
      H   = int ( ws . height ( ) * self . Ratio . height ( ) / 100          )
      PIX = PIX . scaled        ( QSize ( W , H )                            )
    ##########################################################################
    return PIX
  ############################################################################
  def AssignPixmap          ( self                                         ) :
    ##########################################################################
    if                      ( self . Image == None                         ) :
      return
    ##########################################################################
    PIX   = self . toPixmap ( self . Image                                   )
    ##########################################################################
    label = QLabel          (                                                )
    lable . setAlignment    ( Qt . AlignCenter                               )
    label . setPixmap       ( PIX                                            )
    self  . setWidget       ( label                                          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot             ( QImage                                             )
  def setImage          ( self , image                                     ) :
    ##########################################################################
    self . Image = image
    self . AssignPixmap (                                                    )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   ( list                                         )
  def setGallery              ( self , Pictures                            ) :
    ##########################################################################
    WW      = 0
    HH      = 0
    G       = 8
    GW      = G * int         ( len ( Pictures ) + 1                         )
    PIXs    =                 [                                              ]
    ##########################################################################
    for IMAGE in Pictures                                                    :
      ########################################################################
      PIX   = self . toPixmap ( IMAGE                                        )
      PIXs  . append          ( PIX                                          )
      WX    = PIX  . width    (                                              )
      WY    = PIX  . height   (                                              )
      ########################################################################
      if                      ( WX > WW                                    ) :
       WW   = WX
      ########################################################################
      HH    = HH   + WY
    ##########################################################################
    WIDGET  = QWidget         (                                              )
    WIDGET  . resize          ( WW , HH + GW                                 )
    ##########################################################################
    YY      = 0
    self . MaxWidth  = WW
    self . LABELs = [ ]
    for PIX in PIXs                                                          :
      ########################################################################
      WY    = PIX  . height   (                                              )
      YY    = YY + G
      ########################################################################
      label = QLabel          ( WIDGET                                       )
      label . setAlignment    ( Qt . AlignCenter                             )
      label . setPixmap       ( PIX                                          )
      ########################################################################
      label . setGeometry     ( 0 , YY , WW , WY                             )
      self . LABELs . append  ( label                                        )
      ########################################################################
      YY    = YY + WY
    ##########################################################################
    self    . setWidget       ( WIDGET                                       )
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
  def doZoom                ( self                                         ) :
    ##########################################################################
    S            = 10 * int ( self . ZoomLevel                               )
    self . Ratio = QSize    ( S , S                                          )
    ##########################################################################
    if                      ( self . Image != None                         ) :
      self . AssignPixmap   (                                                )
      return
    ##########################################################################
    if                      ( len ( self . Pictures ) > 0                  ) :
      self . setGallery     ( self . Pictures                                )
      return
    ##########################################################################
    return
  ############################################################################
  def ZoomIn            ( self                                             ) :
    ##########################################################################
    self . ZoomLevel = self . ZoomLevel + 1
    self . doZoom       (                                                    )
    ##########################################################################
    return
  ############################################################################
  def ZoomOut           ( self                                             ) :
    ##########################################################################
    if ( self . ZoomLevel <= 1 ) :
      return
    ##########################################################################
    self . ZoomLevel = self . ZoomLevel - 1
    self . doZoom       (                                                    )
    ##########################################################################
    return
  ############################################################################
  def Relocation               ( self                                      ) :
    ##########################################################################
    if ( ( self . Image == None ) and ( len ( self . Pictures ) <= 0 )     ) :
      return True
    ##########################################################################
    WIDGET   = self . widget   (                                             )
    VSW      = self . verticalScrollBar (                                    )
    ##########################################################################
    DW       = 0
    if                         ( VSW != None                               ) :
      DW     = VSW . width     (                                             )
    ##########################################################################
    MX       = self . MaxWidth + DW + 2
    WX       = self   . width  (                                             )
    WY       = self   . height (                                             )
    WW       = WIDGET . width  (                                             )
    HH       = WIDGET . height (                                             )
    LW       = WW
    ##########################################################################
    if                         ( MX >= WX                                  ) :
      LW     = self . MaxWidth
    else                                                                     :
      LW     = WX - DW - 2
    ##########################################################################
    WIDGET   . resize          ( LW , HH                                     )
    ##########################################################################
    if                         ( self . Image != None                      ) :
      return True
    ##########################################################################
    if                         ( len ( self . Pictures ) <= 0              ) :
      return True
    ##########################################################################
    if                         ( len ( self . LABELs   ) <= 0              ) :
      return True
    ##########################################################################
    for LABEL in self . LABELs                                               :
      ########################################################################
      H      = LABEL . height  (                                             )
      LABEL  . resize          ( LW , H                                      )
    ##########################################################################
    return True
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
  def FetchGallery                   ( self , T1 , UUID , RELATED          ) :
    ##########################################################################
    DB          = self . ConnectDB   (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    PICTAB      = self . Tables      [ "Information"                         ]
    DPTTAB      = self . Tables      [ "Depot"                               ]
    RELTAB      = self . Tables      [ "Relation"                            ]
    ##########################################################################
    Pictures    =                    [                                       ]
    GALM        = GalleryItem        (                                       )
    UUIDs       = GALM . GetPictures ( DB , RELTAB , UUID , T1 , RELATED     )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      FOUND     = False
      SUFFIX    = ""
      BLOB      = None
      ########################################################################
      QQ        = f"select `suffix` from {PICTAB} where ( `uuid` = {UUID} ) ;"
      DB        . Query              ( QQ                                    )
      INF       = DB . FetchOne      (                                       )
      ########################################################################
      if ( ( INF != None ) and ( len ( INF ) > 0 ) )                         :
        SUFFIX  = INF                [ 0                                     ]
        FOUND   = True
      ########################################################################
      if                             ( FOUND                               ) :
        QQ      = f"select `file` from {DPTTAB} where ( `uuid` = {UUID} ) ;"
        DB      . Query              ( QQ                                    )
        BLOBs   = DB . FetchOne      (                                       )
        if ( ( BLOBs != None ) and ( len ( BLOBs ) > 0 )                   ) :
          BLOB  = BLOBs              [ 0                                     ]
        else                                                                 :
          FOUND = False
      ########################################################################
      if                             ( not FOUND                           ) :
        continue
      ########################################################################
      if                             ( len ( SUFFIX ) <= 0                 ) :
        continue
      ########################################################################
      if                             ( BLOB == None                        ) :
        continue
      ########################################################################
      SS        = SUFFIX
      SS        = SS . lower         (                                       )
      ALLOWED   =                    [ "jpeg" , "jpg" , "png"                ]
      ########################################################################
      if                             ( SS in ALLOWED                       ) :
        IMG     = QImage             (                                       )
        IMG     . loadFromData       ( BLOB , SUFFIX                         )
      else                                                                   :
        INTL    = Image              ( blob = BLOB                           )
        INTL    . format = "png"
        DAT     = BytesIO            (                                       )
        INTL    . save               ( file = DAT                            )
        BLOB    = DAT . getvalue     (                                       )
        IMG     = QImage             (                                       )
        IMG     . loadFromData       ( BLOB , "png"                          )
      ########################################################################
      Pictures  . append             ( IMG                                   )
    ##########################################################################
    DB          . Close              (                                       )
    ##########################################################################
    self . Pictures = Pictures
    self . AssignGallery . emit      ( Pictures                              )
    ##########################################################################
    return
  ############################################################################
  def loadUuid          ( self , Uuid                                      ) :
    ##########################################################################
    self . Go           ( self . FetchImage , ( Uuid , )                     )
    ##########################################################################
    return
  ############################################################################
  def loadGallery       ( self , T1 , UUID , RELATED                       ) :
    ##########################################################################
    ARGS =              ( T1 , UUID , RELATED ,                              )
    self . Go           ( self . FetchGallery , ARGS                         )
    ##########################################################################
    return
##############################################################################
