# -*- coding: utf-8 -*-
##############################################################################
## VcfFaceRegion
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
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QPolygonF
from   PyQt5 . QtGui                  import QPainterPath
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QTransform
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
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
from   AITK  . VCF . VcfItem          import VcfItem      as VcfItem
from   AITK  . VCF . VcfRectangle     import VcfRectangle as VcfRectangle
from   AITK  . VCF . VcfCanvas        import VcfCanvas    as VcfCanvas
##############################################################################
class VcfFaceRegion                 ( VcfCanvas                            ) :
  ############################################################################
  def __init__                      ( self                                 , \
                                      parent = None                        , \
                                      item   = None                        , \
                                      plan   = None                        ) :
    ##########################################################################
    super ( ) . __init__            ( parent , item , plan                   )
    self . setVcfFaceRegionDefaults (                                        )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfFaceRegionDefaults ( self                                      ) :
    ##########################################################################
    self . PictureDPI      = 96
    self . PictureItem     = None
    self . Region          = None
    self . NoseBridge      = None
    self . FACEs           =   [                                             ]
    self . EYEs            =   [                                             ]
    self . MOUTHs          =   [                                             ]
    self . GeometryChanged = self . FaceGeometryChanged
    self . setZValue           ( 50000                                       )
    self . setOpacity          ( 1.0                                         )
    ##########################################################################
    self . Painter . addMap    ( "Face"         , 11                         )
    self . Painter . addMap    ( "Eyes"         , 12                         )
    self . Painter . addMap    ( "Mouth"        , 13                         )
    self . Painter . addMap    ( "Shape"        , 21                         )
    self . Painter . addMap    ( "RightEyebrow" , 22                         )
    self . Painter . addMap    ( "LeftEyebrow"  , 23                         )
    self . Painter . addMap    ( "NoseBridge"   , 24                         )
    self . Painter . addMap    ( "NoseNostril"  , 25                         )
    self . Painter . addMap    ( "RightEye"     , 26                         )
    self . Painter . addMap    ( "LeftEye"      , 27                         )
    self . Painter . addMap    ( "OuterMouth"   , 28                         )
    self . Painter . addMap    ( "InnerMouth"   , 29                         )
    ##########################################################################
    self . Painter . addPen    (  0 , QColor (  64 ,  64 ,  64 , 128 )       )
    self . Painter . addPen    ( 11 , QColor (   0 ,   0 , 255 , 255 )       )
    self . Painter . addPen    ( 12 , QColor ( 255 ,   0 ,   0 , 255 )       )
    self . Painter . addPen    ( 13 , QColor (   0 , 255 ,   0 , 255 )       )
    self . Painter . addPen    ( 21 , QColor ( 255 ,   0 ,   0 , 255 )       )
    self . Painter . addPen    ( 22 , QColor (   0 , 255 ,   0 , 255 )       )
    self . Painter . addPen    ( 23 , QColor (   0 , 255 ,   0 , 255 )       )
    self . Painter . addPen    ( 24 , QColor (   0 ,   0 , 255 , 255 )       )
    self . Painter . addPen    ( 25 , QColor (   0 , 255 , 255 , 255 )       )
    self . Painter . addPen    ( 26 , QColor ( 255 , 255 ,   0 , 255 )       )
    self . Painter . addPen    ( 27 , QColor ( 255 , 255 ,   0 , 255 )       )
    self . Painter . addPen    ( 28 , QColor ( 128 ,  64 , 255 , 255 )       )
    self . Painter . addPen    ( 29 , QColor ( 128 ,  64 , 255 , 255 )       )
    ##########################################################################
    self . Painter . addBrush  (  0 , QColor ( 255 , 255 , 255 ,  64 )       )
    self . Painter . addBrush  ( 21 , QColor (   0 ,   0 ,   0 ,   0 )       )
    self . Painter . addBrush  ( 22 , QColor (   0 ,   0 ,   0 ,   0 )       )
    self . Painter . addBrush  ( 23 , QColor (   0 ,   0 ,   0 ,   0 )       )
    self . Painter . addBrush  ( 24 , QColor (   0 ,   0 ,   0 ,   0 )       )
    self . Painter . addBrush  ( 25 , QColor (   0 ,   0 ,   0 ,   0 )       )
    self . Painter . addBrush  ( 26 , QColor (   0 ,   0 ,   0 ,   0 )       )
    self . Painter . addBrush  ( 27 , QColor (   0 ,   0 ,   0 ,   0 )       )
    self . Painter . addBrush  ( 28 , QColor (   0 ,   0 ,   0 ,   0 )       )
    self . Painter . addBrush  ( 29 , QColor (   0 ,   0 ,   0 ,   0 )       )
    ##########################################################################
    for Id in [ 11 , 12 , 13 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 ,29   ] :
      ########################################################################
      self . Painter . pens [ Id ] . setWidthF ( 2.5                         )
    ##########################################################################
    return
  ############################################################################
  def Painting                       ( self , p , region , clip , color    ) :
    ##########################################################################
    self . pushPainters              ( p                                     )
    ##########################################################################
    self . Painter . drawRect        ( p , "Default" , self . ScreenRect     )
    self . Painter . drawBorder      ( p , "Default" , self . ScreenRect     )
    ##########################################################################
    if                               ( len ( self . FACEs ) > 0            ) :
      for F in self . FACEs                                                  :
        self . Painter . drawBorder  ( p , "Face"    , F                     )
    ##########################################################################
    if                               ( len ( self . FACEs ) > 0            ) :
      for E in self . EYEs                                                   :
        self . Painter . drawBorder  ( p , "Eyes"    , E                     )
    ##########################################################################
    if                               ( len ( self . FACEs ) > 0            ) :
      for M in self . MOUTHs                                                 :
        self . Painter . drawBorder  ( p , "Mouth"   , M                     )
    ##########################################################################
    self . Painter . drawPainterPath ( p , "Shape"                           )
    self . Painter . drawPainterPath ( p , "RightEyebrow"                    )
    self . Painter . drawPainterPath ( p , "LeftEyebrow"                     )
    self . Painter . drawPainterPath ( p , "NoseBridge"                      )
    self . Painter . drawPainterPath ( p , "NoseNostril"                     )
    self . Painter . drawPainterPath ( p , "RightEye"                        )
    self . Painter . drawPainterPath ( p , "LeftEye"                         )
    self . Painter . drawPainterPath ( p , "OuterMouth"                      )
    self . Painter . drawPainterPath ( p , "InnerMouth"                      )
    ##########################################################################
    self . popPainters               ( p                                     )
    ##########################################################################
    return
  ############################################################################
  def itemChange ( self , change , value                                   ) :
    ##########################################################################
    if           ( change == QGraphicsItem . ItemPositionChange            ) :
      ########################################################################
      """
      W    = self . ScreenRect . width        (                              )
      H    = self . ScreenRect . height       (                              )
      self . ScreenRect . setTopLeft          ( value                        )
      self . ScreenRect . setWidth            ( W                            )
      self . ScreenRect . setHeight           ( H                            )
      self . PaperPos   = self . pointToPaper ( value                        )
      """
      ########################################################################
      self . signalGeometryChanged            (                              )
    ##########################################################################
    return super ( ) . itemChange             ( change , value               )
  ############################################################################
  def RotateAngle ( self                                                   ) :
    return        ( self . NoseBridge - 270.0                                )
  ############################################################################
  def ClearAll          ( self                                             ) :
    ##########################################################################
    self . NoseBridge = None
    ##########################################################################
    self . FACEs      = [                                                    ]
    self . EYEs       = [                                                    ]
    self . MOUTHs     = [                                                    ]
    ##########################################################################
    for Id in range     ( 21 , 30                                          ) :
      ########################################################################
      del self . Painter . pathes [ Id                                       ]
    ##########################################################################
    return
  ############################################################################
  def FaceGeometryChanged    ( self , item                                 ) :
    ##########################################################################
    self . CalculateGeometry (                                               )
    ##########################################################################
    return
  ############################################################################
  def CalculateGeometry ( self                                             ) :
    ##########################################################################
    if                  ( self . PictureItem in [ False , None ]           ) :
      return
    ##########################################################################
    R    = self . PictureItem . RectangleFromItem ( self                     )
    ##########################################################################
    if                  ( not R . isValid ( )                              ) :
      return
    ##########################################################################
    self . Region = R
    ##########################################################################
    return
  ############################################################################
  def CropCurrentImage                   ( self                            ) :
    ##########################################################################
    self . CalculateGeometry             (                                   )
    ##########################################################################
    self . PictureItem . CreateCropImage ( self . Region                     )
    ##########################################################################
    return
  ############################################################################
  def CvRectToQRectF       ( self , R                                      ) :
    ##########################################################################
    RX = self . PictureItem . Xratio
    RY = self . PictureItem . Yratio
    BX = self . Region . x (                                                 )
    BY = self . Region . y (                                                 )
    XX = R                 [ 0                                               ]
    YY = R                 [ 1                                               ]
    WW = R                 [ 2                                               ]
    HH = R                 [ 3                                               ]
    ##########################################################################
    XX = BX + XX
    YY = BY + YY
    ##########################################################################
    XX = float             ( float ( XX ) / RX                               )
    YY = float             ( float ( YY ) / RY                               )
    WW = float             ( float ( WW ) / RX                               )
    HH = float             ( float ( HH ) / RY                               )
    RF = QRectF            ( XX , YY , WW , HH                               )
    ##########################################################################
    RR = self . PictureItem . mapToItem ( self , RF                          )
    ##########################################################################
    XX = RR [ 0 ] . x      (                                                 )
    YY = RR [ 0 ] . y      (                                                 )
    WW = RR [ 2 ] . x      (                                                 )
    HH = RR [ 2 ] . y      (                                                 )
    WW = WW - XX
    HH = HH - YY
    ##########################################################################
    return QRectF          ( XX , YY , WW , HH                               )
  ############################################################################
  def BasicFacialRecognition             ( self                            ) :
    ##########################################################################
    self      . CalculateGeometry        (                                   )
    ##########################################################################
    X         = self . Region . x        (                                   )
    Y         = self . Region . y        (                                   )
    W         = self . Region . width    (                                   )
    H         = self . Region . height   (                                   )
    PIC       = self . PictureItem . PICOP . Crop ( X , Y , W , H            )
    if                                   ( PIC in [ False , None ]         ) :
      return
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
    EC        = cv2  . CascadeClassifier ( EYES                              )
    MC        = cv2  . CascadeClassifier ( MOUTH                             )
    FIVE      = dlib . shape_predictor   ( FIVEMARKS                         )
    PREDICTOR = dlib . shape_predictor   ( LANDMARKS                         )
    FACIAL    = dlib . face_recognition_model_v1 ( RESNET                    )
    ##########################################################################
    IMG       = PIC  . toOpenCV          (                                   )
    GRAY      = cv2  . cvtColor          ( IMG , cv2 . COLOR_BGR2GRAY        )
    WW        = PIC  . Width             (                                   )
    HH        = PIC  . Height            (                                   )
    ##########################################################################
    FACE      = FaceItem                 (                                   )
    FACE      . Classifier    = FC
    FACE      . EyesDetector  = EC
    FACE      . MouthDetector = MC
    FACE      . Fivemarks     = FIVE
    FACE      . Predictor     = PREDICTOR
    FACE      . Facial        = FACIAL
    ##########################################################################
    FACEs     = FACE . ToFaces           ( GRAY                              )
    EYEs      = FACE . ToEyes            ( GRAY                              )
    MOUTHs    = FACE . ToMouthes         ( GRAY                              )
    ##########################################################################
    self      . FACEs           =        [                                   ]
    self      . EYEs            =        [                                   ]
    self      . MOUTHs          =        [                                   ]
    ##########################################################################
    for F in FACEs                                                           :
      QR      = self . CvRectToQRectF    ( F                                 )
      self    . FACEs . append           ( QR                                )
    ##########################################################################
    for E in EYEs                                                            :
      QR      = self . CvRectToQRectF    ( E                                 )
      self    . EYEs . append            ( QR                                )
    ##########################################################################
    for M in MOUTHs                                                          :
      QR      = self . CvRectToQRectF    ( M                                 )
      self    . MOUTHs . append          ( QR                                )
    ##########################################################################
    self      . Notify                   ( 5                                 )
    ##########################################################################
    return
  ############################################################################
  def CvPointToPath          ( self , Id , Closed , Points                 ) :
    ##########################################################################
    PP   = QPainterPath      (                                               )
    PL   = QPolygonF         (                                               )
    ##########################################################################
    RX   = self . PictureItem . Xratio
    RY   = self . PictureItem . Yratio
    BX   = self . Region . x (                                               )
    BY   = self . Region . y (                                               )
    ##########################################################################
    for P in Points                                                          :
      ########################################################################
      XX = P                 [ 0                                             ]
      YY = P                 [ 1                                             ]
      XX = BX + XX
      YY = BY + YY
      ########################################################################
      XX = float             ( float ( XX ) / RX                             )
      YY = float             ( float ( YY ) / RY                             )
      PT = QPointF           ( XX , YY                                       )
      ########################################################################
      PX = self . PictureItem . mapToItem ( self , PT                        )
      ########################################################################
      PL . append            ( PX                                            )
    ##########################################################################
    if                       ( Closed                                      ) :
      ########################################################################
      PP . addPolygon        ( PL                                            )
      PP . closeSubpath      (                                               )
      ########################################################################
    else                                                                     :
      ########################################################################
      AT = 0
      ########################################################################
      for P in PL                                                            :
        ######################################################################
        if                   ( AT == 0                                     ) :
          PP . moveTo        ( P                                             )
        else                                                                 :
          PP . lineTo        ( P                                             )
        ######################################################################
        AT = AT + 1
    ##########################################################################
    self . Painter . pathes  [ Id ] = PP
    ##########################################################################
    return
  ############################################################################
  def Mark68Recognition                  ( self                            ) :
    ##########################################################################
    self      . CalculateGeometry        (                                   )
    ##########################################################################
    X         = self . Region . x        (                                   )
    Y         = self . Region . y        (                                   )
    W         = self . Region . width    (                                   )
    H         = self . Region . height   (                                   )
    PIC       = self . PictureItem . PICOP . Crop ( X , Y , W , H            )
    if                                   ( PIC in [ False , None ]         ) :
      return
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
    EC        = cv2  . CascadeClassifier ( EYES                              )
    MC        = cv2  . CascadeClassifier ( MOUTH                             )
    FIVE      = dlib . shape_predictor   ( FIVEMARKS                         )
    PREDICTOR = dlib . shape_predictor   ( LANDMARKS                         )
    FACIAL    = dlib . face_recognition_model_v1 ( RESNET                    )
    ##########################################################################
    IMG       = PIC  . toOpenCV          (                                   )
    GRAY      = cv2  . cvtColor          ( IMG , cv2 . COLOR_BGR2GRAY        )
    WW        = PIC  . Width             (                                   )
    HH        = PIC  . Height            (                                   )
    ##########################################################################
    FACE      = FaceItem                 (                                   )
    FACE      . Classifier    = FC
    FACE      . EyesDetector  = EC
    FACE      . MouthDetector = MC
    FACE      . Fivemarks     = FIVE
    FACE      . Predictor     = PREDICTOR
    FACE      . Facial        = FACIAL
    ##########################################################################
    FACEs     = FACE . ToFaces           ( GRAY                              )
    if                                   ( len ( FACEs ) != 1              ) :
      return
    ##########################################################################
    FACE      . setFull                  ( W , H                             )
    FACE      . setRectangleFromOpenCV   ( FACEs [ 0 ]                       )
    v         = FACE . ToFeatures        ( IMG , GRAY                        )
    FACE      . FeatureWeights           (                                   )
    SS        = FACE . ToFullFaceRectangle       (                           )
    FACE      . NoseBridge = FACE . GetNoseAngle (                           )
    self      . NoseBridge = FACE . NoseBridge
    if ( int ( self . RotateAngle ( ) * 100 ) == 0 )                         :
      self    . NoseBridge = None
    ##########################################################################
    ## 畫出臉型
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Shape"                           )
    self      . CvPointToPath            ( 21 , False , F                    )
    ##########################################################################
    ## 畫出右眉(在左邊)
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Eyebrow" , "Right"               )
    self      . CvPointToPath            ( 22 , False , F                    )
    ##########################################################################
    ## 畫出左眉(在右邊)
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Eyebrow" , "Left"                )
    self      . CvPointToPath            ( 23 , False , F                    )
    ##########################################################################
    ## 畫出鼻樑
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Nose" , "Bridge"                 )
    self      . CvPointToPath            ( 24 , False , F                    )
    ##########################################################################
    ## 畫出鼻孔部
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Nose" , "Nostril"                )
    self      . CvPointToPath            ( 25 , False , F                    )
    ##########################################################################
    ## 畫出右眼(在左邊)
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Eyes" , "Right"                  )
    self      . CvPointToPath            ( 26 , True  , F                    )
    ##########################################################################
    ## 畫出左眼(在右邊)
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Eyes" , "Left"                   )
    self      . CvPointToPath            ( 27 , True , F                    )
    ##########################################################################
    ## 畫出外嘴唇
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Mouth" , "Outer"                 )
    self      . CvPointToPath            ( 28 , True  , F                    )
    ##########################################################################
    ## 畫出內嘴唇
    ##########################################################################
    F         = FACE . LandmarkToNpArray ( "Mouth" , "Inner"                 )
    self      . CvPointToPath            ( 29 , True  , F                    )
    ##########################################################################
    self      . Notify                   ( 5                                 )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  def Menu                          ( self , gview , pos , spos            ) :
    ##########################################################################
    mm     = MenuManager            ( gview                                  )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    msg    = TRX                    [ "UI::ClearAll"                         ]
    mm     . addAction              ( 1001 , msg                             )
    ##########################################################################
    msg    = TRX                    [ "UI::Delete"                           ]
    icon   = QIcon                  ( ":/images/delete.png"                  )
    mm     . addActionWithIcon      ( 1002 , icon , msg                      )
    ##########################################################################
    MSG    = self . getMenuItem     ( "EyesMouthFacial"                      )
    mm     . addAction              ( 1003 , MSG                             )
    ##########################################################################
    MSG    = self . getMenuItem     ( "68Facial"                             )
    mm     . addAction              ( 1004 , MSG                             )
    ##########################################################################
    MSG    = self . getMenuItem     ( "CropImage"                            )
    mm     . addAction              ( 1005 , MSG                             )
    ##########################################################################
    if ( self . NoseBridge not in [ False , None ] )                         :
      ########################################################################
      FMT  = self . getMenuItem     ( "RotateImage"                          )
      MSG  = FMT  . format          ( self . RotateAngle ( )                 )
      mm   . addAction              ( 1006 , MSG                             )
    ##########################################################################
    mm     . setFont                ( gview   . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . ClearAll               (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 1002                           ) :
      ########################################################################
      self . DeleteItem             (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 1003                           ) :
      ########################################################################
      self . BasicFacialRecognition (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 1004                           ) :
      ########################################################################
      self . Mark68Recognition      (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 1005                           ) :
      ########################################################################
      self . CropCurrentImage       (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 1006                           ) :
      ########################################################################
      self . PictureItem . CreateRotateImage ( self . RotateAngle ( )        )
      ########################################################################
      return
    ##########################################################################
    return
##############################################################################
