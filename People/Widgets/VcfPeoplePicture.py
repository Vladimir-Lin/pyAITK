# -*- coding: utf-8 -*-
##############################################################################
## VcfPeoplePicture
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
from   io                             import BytesIO
from   wand . image                   import Image
from   PIL                            import Image as Pillow
##############################################################################
import cv2
import dlib
import skimage
import numpy                          as np
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
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QSizeF
from   PyQt5 . QtCore                 import QRect
from   PyQt5 . QtCore                 import QRectF
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QTransform
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QFileDialog
from   PyQt5 . QtWidgets              import QGraphicsView
from   PyQt5 . QtWidgets              import QGraphicsItem
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager  as MenuManager
##############################################################################
from   AITK  . Essentials . Object    import Object       as Object
from   AITK  . Pictures   . Picture   import Picture      as PictureItem
from   AITK  . Pictures   . Gallery   import Gallery      as GalleryItem
from   AITK  . Pictures   . Face      import Face         as FaceItem
##############################################################################
from   AITK  . VCF . VcfPicture       import VcfPicture   as VcfPicture
from   AITK  . People . Faces . VcfFaceRegion import VcfFaceRegion as VcfFaceRegion
##############################################################################
class VcfPeoplePicture           ( VcfPicture                              ) :
  ############################################################################
  def __init__                   ( self                                    , \
                                   parent = None                           , \
                                   item   = None                           , \
                                   plan   = None                           ) :
    ##########################################################################
    super ( ) . __init__         ( parent , item , plan                      )
    self . setVcfPeoplePictureDefaults (                                     )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfPeoplePictureDefaults ( self                                   ) :
    ##########################################################################
    self . JsonCaller = None
    self . LastestZ   = None
    self . setFlag                ( QGraphicsItem . ItemIsMovable , False    )
    self . setZValue              ( 10000                                    )
    ##########################################################################
    return
  ############################################################################
  def DeleteItem      ( self                                               ) :
    ##########################################################################
    JSON =            { "Function"  : "DeleteItem"                         , \
                        "Item"      : self                                   }
    self . JsonCaller ( JSON                                                 )
    ##########################################################################
    return
  ############################################################################
  def RectangleFromItem  ( self , item                                     ) :
    ##########################################################################
    R = item . mapToItem ( self , item . ScreenRect                          )
    ##########################################################################
    X = R [ 0 ] . x      (                                                   )
    Y = R [ 0 ] . y      (                                                   )
    W = R [ 2 ] . x      (                                                   )
    H = R [ 2 ] . y      (                                                   )
    W = W - X
    H = H - Y
    ##########################################################################
    X = int              ( X * self . Xratio                                 )
    Y = int              ( Y * self . Yratio                                 )
    W = int              ( W * self . Xratio                                 )
    H = int              ( H * self . Yratio                                 )
    ##########################################################################
    return QRect         ( X , Y , W , H                                     )
  ############################################################################
  def AddFaceRegion   ( self , rect                                        ) :
    ##########################################################################
    JSON =            { "Function"  : "AddFaceRegion"                      , \
                        "Item"      : self                                 , \
                        "Rectangle" : rect                                   }
    self . JsonCaller ( JSON                                                 )
    ##########################################################################
    return
  ############################################################################
  def AddSelectionRegion         ( self                                    ) :
    ##########################################################################
    W    = self . Image . width  (                                           )
    H    = self . Image . height (                                           )
    R    = QRect                 ( 0 , 0 , W , H                             )
    ##########################################################################
    self . AddFaceRegion         ( R                                         )
    self . Notify                ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def FacialRecognition                  ( self                            ) :
    ##########################################################################
    ## self      . Gui . OnBusy  . emit     (                                   )
    ##########################################################################
    AI        = self . Settings          [ "AI"                              ]
    HAAR      = AI                       [ "HAAR"                            ]
    EYES      = AI                       [ "Eyes"                            ]
    MOUTH     = AI                       [ "Mouth"                           ]
    FIVEMARKS = AI                       [ "Fivemarks"                       ]
    LANDMARKS = AI                       [ "Landmarks"                       ]
    RESNET    = AI                       [ "Resnet"                          ]
    ##########################################################################
    FC        = cv2  . CascadeClassifier ( HAAR                              )
    FIVE      = dlib . shape_predictor   ( FIVEMARKS                         )
    PREDICTOR = dlib . shape_predictor   ( LANDMARKS                         )
    FACIAL    = dlib . face_recognition_model_v1 ( RESNET                    )
    ##########################################################################
    IMG       = self . PICOP . toOpenCV  (                                   )
    GRAY      = cv2  . cvtColor          ( IMG , cv2 . COLOR_BGR2GRAY        )
    WW        = self . PICOP . Width     (                                   )
    HH        = self . PICOP . Height    (                                   )
    ##########################################################################
    FACE      = FaceItem                 (                                   )
    FACE      . Classifier = FC
    FACE      . Fivemarks  = FIVE
    FACE      . Predictor  = PREDICTOR
    FACE      . Facial     = FACIAL
    ##########################################################################
    FACEs     = FACE . ToFaces           ( GRAY                              )
    ##########################################################################
    for F in FACEs                                                           :
      ########################################################################
      X       = F                        [ 0                                 ]
      Y       = F                        [ 1                                 ]
      W       = F                        [ 2                                 ]
      H       = F                        [ 3                                 ]
      R       = QRect                    ( X , Y , W , H                     )
      ########################################################################
      self    . AddFaceRegion            ( R                                 )
    ##########################################################################
    ## self      . Gui . GoRelax . emit     (                                   )
    ## self      . prepareGeometryChange    (                                   )
    self      . Notify                   ( 5                                 )
    ##########################################################################
    return
  ############################################################################
  def ProduceRotateImage         ( self , degree                           ) :
    ##########################################################################
    PIC  = self . PICOP . Rotate ( degree                                    )
    ##########################################################################
    if                           ( self . LastestZ in [ False , None ]     ) :
      self . LastestZ = self . zValue ( ) + 10.0
    else                                                                     :
      self . LastestZ = self . LastestZ   + 10.0
    ##########################################################################
    JSON =                       { "Function"  : "AddPicture"              , \
                                   "Picture"   : PIC                       , \
                                   "Z"         : self . LastestZ             }
    self . JsonCaller            ( JSON                                      )
    ##########################################################################
    return
  ############################################################################
  def CreateRotateImage            ( self , degree                         ) :
    ##########################################################################
    VAL  =                         ( degree ,                                )
    self . Go                      ( self . ProduceRotateImage , VAL         )
    ##########################################################################
    return
  ############################################################################
  def ProduceCropImage           ( self , region                           ) :
    ##########################################################################
    X    = region . x            (                                           )
    Y    = region . y            (                                           )
    W    = region . width        (                                           )
    H    = region . height       (                                           )
    PIC  = self . PICOP . Crop   ( X , Y , W , H                             )
    ##########################################################################
    if                           ( self . LastestZ in [ False , None ]     ) :
      self . LastestZ = self . zValue ( ) + 10.0
    else                                                                     :
      self . LastestZ = self . LastestZ   + 10.0
    ##########################################################################
    JSON =                       { "Function"  : "AddPicture"              , \
                                   "Picture"   : PIC                       , \
                                   "Z"         : self . LastestZ             }
    self . JsonCaller            ( JSON                                      )
    ##########################################################################
    return
  ############################################################################
  def CreateCropImage              ( self , region                         ) :
    ##########################################################################
    VAL  =                         ( region ,                                )
    self . Go                      ( self . ProduceRotateImage , VAL         )
    ##########################################################################
    return
  ############################################################################
  def SaveAs                       ( self                                  ) :
    ##########################################################################
    Filename , _ = QFileDialog . getSaveFileName                             (
                                     self                                    ,
                                     "匯出圖片" ,
                                     ""                                      ,
                                     "JPEG (*.jpg);;PNG (*.png)"             )
    if                             ( len ( Filename ) <= 0                 ) :
      return
    ##########################################################################
    self . Image . save            ( Filename                                )
    self . Notify                  ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def PeopleFaceMenu               ( self , mm , Menu                      ) :
    ##########################################################################
    MSG   = self . getMenuItem     ( "FacialRecognition"                     )
    LOM   = mm   . addMenuFromMenu ( Menu , MSG                              )
    ##########################################################################
    MSG   = self . getMenuItem     ( "BasicFacial"                           )
    mm    . addActionFromMenu      ( LOM , 98438501 , MSG                    )
    ##########################################################################
    return
  ############################################################################
  def PeopleBodyMenu               ( self , mm , Menu                      ) :
    ##########################################################################
    MSG   = self . getMenuItem     ( "BodyRecognition"                       )
    LOM   = mm   . addMenuFromMenu ( Menu , MSG                              )
    ##########################################################################
    MSG   = self . getMenuItem     ( "PoseEstimation"                        )
    mm    . addActionFromMenu      ( LOM , 98438601 , MSG                    )
    ##########################################################################
    return
  ############################################################################
  def RecognitionMenu            ( self , mm                               ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "FeatureRecognition"                      )
    LOM   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "RelatePeople"                            )
    mm    . addActionFromMenu    ( LOM , 98438301 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "AddSelectionRegion"                      )
    mm    . addActionFromMenu    ( LOM , 98438302 , MSG                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    self  . PeopleFaceMenu       ( mm , LOM                                  )
    self  . PeopleBodyMenu       ( mm , LOM                                  )
    ##########################################################################
    return
  ############################################################################
  def RunRecognitionMenu        ( self , at                                ) :
    ##########################################################################
    if                          ( at == 98438301                           ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438302                           ) :
      ########################################################################
      self . AddSelectionRegion (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438501                           ) :
      ########################################################################
      self . Go                 ( self . FacialRecognition                   )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438601                           ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                      ( self , gview , pos , spos                ) :
    ##########################################################################
    mm     = MenuManager        ( gview                                      )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    msg    = TRX                [ "UI::Delete"                               ]
    icon   = QIcon              ( ":/images/delete.png"                      )
    mm     . addActionWithIcon  ( 1001 , icon , msg                          )
    ##########################################################################
    msg    = self . getMenuItem ( "SaveImage"                                )
    mm     . addAction          ( 1002 , msg                                 )
    ##########################################################################
    self   . InformationMenu   ( mm                                          )
    self   . RecognitionMenu   ( mm                                          )
    self   . StatesMenu        ( mm                                          )
    ##########################################################################
    mm     . setFont           ( gview   . menuFont ( )                      )
    aa     = mm . exec_        ( QCursor . pos      ( )                      )
    at     = mm . at           ( aa                                          )
    ##########################################################################
    if                         ( self . RunStatesMenu      ( at          ) ) :
      return True
    ##########################################################################
    if                         ( self . RunRecognitionMenu ( at          ) ) :
      return True
    ##########################################################################
    if                         ( at == 1001                                ) :
      ########################################################################
      self . DeleteItem        (                                             )
      ########################################################################
      return
    ##########################################################################
    if                         ( at == 1002                                ) :
      ########################################################################
      self . SaveAs            (                                             )
      ########################################################################
      return
    ##########################################################################
    return
##############################################################################
