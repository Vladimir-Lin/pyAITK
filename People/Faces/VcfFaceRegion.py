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
import mediapipe                      as mp
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
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QFileDialog
from   PyQt5 . QtWidgets              import QGraphicsView
from   PyQt5 . QtWidgets              import QGraphicsItem
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QDoubleSpinBox
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager  as MenuManager
##############################################################################
from   AITK  . Essentials . Object    import Object       as Object
from   AITK  . Pictures   . Picture   import Picture      as PictureItem
from   AITK  . Pictures   . Gallery   import Gallery      as GalleryItem
from   AITK  . Pictures   . Face      import Face         as FaceItem
##############################################################################
from   AITK  . People . Body . Tit    import Tit          as TitItem
from   AITK  . People . Body . Body   import Body         as BodyItem
##############################################################################
from   AITK  . VCF . VcfItem          import VcfItem      as VcfItem
from   AITK  . VCF . VcfLines         import VcfLines     as VcfLines
from   AITK  . VCF . VcfContours      import VcfContours  as VcfContours
from   AITK  . VCF . VcfPoints        import VcfPoints    as VcfPoints
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
    self . PeopleDetailsUI = None
    self . PeopleUuid      = 0
    self . FACEs           =   [                                             ]
    self . EYEs            =   [                                             ]
    self . MOUTHs          =   [                                             ]
    self . POSEs           =   { "Pose"   : False                            }
    self . MESHs           =   { "Mesh"   : False                            }
    self . NIPPLEs         =   { "Nipple" : False                            }
    self . GeometryChanged = self . FaceGeometryChanged
    self . FaceCallbacks   =   [                                             ]
    self . setZValue           ( 50000                                       )
    self . setOpacity          ( 1.0                                         )
    ##########################################################################
    self . Painter . addMap    ( "Face"         ,       11                   )
    self . Painter . addMap    ( "Eyes"         ,       12                   )
    self . Painter . addMap    ( "Mouth"        ,       13                   )
    self . Painter . addMap    ( "Shape"        ,       21                   )
    self . Painter . addMap    ( "RightEyebrow" ,       22                   )
    self . Painter . addMap    ( "LeftEyebrow"  ,       23                   )
    self . Painter . addMap    ( "NoseBridge"   ,       24                   )
    self . Painter . addMap    ( "NoseNostril"  ,       25                   )
    self . Painter . addMap    ( "RightEye"     ,       26                   )
    self . Painter . addMap    ( "LeftEye"      ,       27                   )
    self . Painter . addMap    ( "OuterMouth"   ,       28                   )
    self . Painter . addMap    ( "InnerMouth"   ,       29                   )
    ##########################################################################
    self . Painter . addPen    (        0 , QColor (  64 ,  64 ,  64 , 128 ) )
    self . Painter . addPen    (       11 , QColor (   0 ,   0 , 255 , 255 ) )
    self . Painter . addPen    (       12 , QColor ( 255 ,   0 ,   0 , 255 ) )
    self . Painter . addPen    (       13 , QColor (   0 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       21 , QColor ( 255 ,   0 ,   0 , 255 ) )
    self . Painter . addPen    (       22 , QColor (   0 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       23 , QColor (   0 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       24 , QColor (   0 ,   0 , 255 , 255 ) )
    self . Painter . addPen    (       25 , QColor (   0 , 255 , 255 , 255 ) )
    self . Painter . addPen    (       26 , QColor ( 255 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       27 , QColor ( 255 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       28 , QColor ( 128 ,  64 , 255 , 255 ) )
    self . Painter . addPen    (       29 , QColor ( 128 ,  64 , 255 , 255 ) )
    ##########################################################################
    self . Painter . addBrush  (        0 , QColor ( 255 , 255 , 255 ,  64 ) )
    self . Painter . addBrush  (       21 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       22 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       23 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       24 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       25 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       26 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       27 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       28 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       29 , QColor (   0 ,   0 ,   0 ,   0 ) )
    ##########################################################################
    for Id in [ 11 , 12 , 13 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 ,29   ] :
      ########################################################################
      self . Painter . pens [ Id ] . setWidthF ( 2.5                         )
    ##########################################################################
    self . defaultMeasurePoints (                                            )
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
    self . PaintMeasureRule          (        p , region , clip , color      )
    self . PaintMeasurePoints        (        p , region , clip , color      )
    self . PaintLineEditing          (        p , region , clip , color      )
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
    if                               ( self . MESHs   [ "Mesh"   ]         ) :
      ########################################################################
      self . DrawFaceMeshes          ( p                                     )
    ##########################################################################
    if                               ( self . POSEs   [ "Pose"   ]         ) :
      ########################################################################
      self . DrawPoseEstimation      ( p                                     )
    ##########################################################################
    if                               ( self . NIPPLEs [ "Nipple" ]         ) :
      ########################################################################
      self . DrawNipples             ( p                                     )
    ##########################################################################
    self . popPainters               ( p                                     )
    ##########################################################################
    return
  ############################################################################
  def pjsonToQPointF ( self , JSON                                         ) :
    return QPointF   ( JSON [ "X" ] , JSON [ "Y" ]                           )
  ############################################################################
  def pjsonDrawLine  ( self , p , M , PTS , FK , FI , TK , TI              ) :
    ##########################################################################
    self . Painter . setPainter     ( p , M                                  )
    ##########################################################################
    P1   = self    . pjsonToQPointF ( PTS [ FK ] [ FI ]                      )
    P2   = self    . pjsonToQPointF ( PTS [ TK ] [ TI ]                      )
    p    . drawLine                 ( P1 , P2                                )
    ##########################################################################
    return
  ############################################################################
  def DrawFaceMeshes                ( self , p                             ) :
    ##########################################################################
    self . Painter . setPainter     ( p , "NoseBridge"                       )
    ##########################################################################
    PTS  = self . MESHs             [ "Points" ] [ "Draws"                   ]
    ##########################################################################
    for JP in PTS                                                            :
      VT = self . pjsonToQPointF    ( JP                                     )
      p  . drawEllipse              ( VT , 8 , 8                             )
    ##########################################################################
    return
  ############################################################################
  def DrawPoseEstimation            ( self , p                             ) :
    ##########################################################################
    PTS  = self . POSEs             [ "Draws"                                ]
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "NoseNostril"                        , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Shoulder"                           , \
                                      "Right"                              , \
                                      "Shoulder"                             )
    self . pjsonDrawLine            ( p                                    , \
                                      "NoseNostril"                        , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Hip"                                , \
                                      "Right"                              , \
                                      "Hip"                                  )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Shoulder"                           , \
                                      "Left"                               , \
                                      "Elbow"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Elbow"                              , \
                                      "Left"                               , \
                                      "Wrist"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Shoulder"                           , \
                                      "Left"                               , \
                                      "Hip"                                  )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Hip"                                , \
                                      "Left"                               , \
                                      "Knee"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Knee"                               , \
                                      "Left"                               , \
                                      "Ankle"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Ankle"                              , \
                                      "Left"                               , \
                                      "Heel"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "FootIndex"                          , \
                                      "Left"                               , \
                                      "Heel"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "FootIndex"                          , \
                                      "Left"                               , \
                                      "Ankle"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Wrist"                              , \
                                      "Left"                               , \
                                      "Thumb"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Wrist"                              , \
                                      "Left"                               , \
                                      "Index"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Wrist"                              , \
                                      "Left"                               , \
                                      "Pinky"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Index"                              , \
                                      "Left"                               , \
                                      "Pinky"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Shoulder"                           , \
                                      "Right"                              , \
                                      "Elbow"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Elbow"                              , \
                                      "Right"                              , \
                                      "Wrist"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Shoulder"                           , \
                                      "Right"                              , \
                                      "Hip"                                  )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Hip"                                , \
                                      "Right"                              , \
                                      "Knee"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Knee"                               , \
                                      "Right"                              , \
                                      "Ankle"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Ankle"                              , \
                                      "Right"                              , \
                                      "Heel"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "FootIndex"                          , \
                                      "Right"                              , \
                                      "Heel"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "FootIndex"                          , \
                                      "Right"                              , \
                                      "Ankle"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Wrist"                              , \
                                      "Right"                              , \
                                      "Thumb"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Wrist"                              , \
                                      "Right"                              , \
                                      "Index"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Wrist"                              , \
                                      "Right"                              , \
                                      "Pinky"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Index"                              , \
                                      "Right"                              , \
                                      "Pinky"                                )
    ##########################################################################
    self . Painter . setPainter     ( p , "Face"                             )
    ##########################################################################
    VT   = self . pjsonToQPointF    ( PTS [ "Nose" ]                         )
    p    . drawEllipse              ( VT , 8 , 8                             )
    ##########################################################################
    for Side in                     [ "Left" , "Right"                     ] :
      ########################################################################
      KEYs = PTS [ Side ] . keys    (                                        )
      ########################################################################
      for KEY in KEYs                                                        :
        ######################################################################
        JP = PTS                    [ Side ] [ KEY                           ]
        VT = self . pjsonToQPointF  ( JP                                     )
        p  . drawEllipse            ( VT , 8 , 8                             )
    ##########################################################################
    return
  ############################################################################
  def DrawNipples                ( self , p                                ) :
    ##########################################################################
    self  . Painter . setPainter ( p , "RightEye"                            )
    ##########################################################################
    DRAWs = self . NIPPLEs       [ "Draws"                                   ]
    ##########################################################################
    for R in DRAWs                                                           :
      ########################################################################
      X   = R                    [ "X"                                       ]
      Y   = R                    [ "Y"                                       ]
      W   = R                    [ "W"                                       ]
      H   = R                    [ "H"                                       ]
      ########################################################################
      p   . drawRect             ( X , Y , W , H                             )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent        ( self , event                                ) :
    ##########################################################################
    OKAY = self . lineEditingPressEvent   ( event                            )
    if                                    ( OKAY                           ) :
      return
    ##########################################################################
    self . scalePressEvent   ( event                                         )
    self . DeleteGadgets     (                                               )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent         ( self , event                                ) :
    ##########################################################################
    OKAY = self . lineEditingMoveEvent    ( event                            )
    if                                    ( OKAY                           ) :
      return
    ##########################################################################
    self . scaleMoveEvent    (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def mouseReleaseEvent      ( self , event                                ) :
    ##########################################################################
    OKAY = self . lineEditingReleaseEvent ( event                            )
    if                                    ( OKAY                           ) :
      return
    ##########################################################################
    self . scaleReleaseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def LinePointsEditingFinished  ( self , P1 , P2                          ) :
    ##########################################################################
    EM     = self . EditingMode
    self   . EditingMode = 0
    ##########################################################################
    if                           ( EM == 23521001                          ) :
      ########################################################################
      self . AssignRuleLine      ( P1 , P2                                   )
      ########################################################################
      return
    ##########################################################################
    if                           ( EM == 23521002                          ) :
      ########################################################################
      self . AssignMeasurePoints ( P1 , P2                                   )
      ########################################################################
      return
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
  ## MediaPipe Face Mesh Recognition
  ############################################################################
  def Mark468Recognition                   ( self                          ) :
    ##########################################################################
    self      . CalculateGeometry          (                                 )
    ##########################################################################
    X         = self . Region . x          (                                 )
    Y         = self . Region . y          (                                 )
    W         = self . Region . width      (                                 )
    H         = self . Region . height     (                                 )
    PIC       = self . PictureItem . PICOP . Crop ( X , Y , W , H            )
    if                                     ( PIC in [ False , None ]       ) :
      return
    ##########################################################################
    IMG       = PIC  . toOpenCV            (                                 )
    RGB       = cv2  . cvtColor            ( IMG , cv2 . COLOR_BGR2RGB       )
    WW        = PIC  . Width               (                                 )
    HH        = PIC  . Height              (                                 )
    BX        = self . ScreenRect . x      (                                 )
    BY        = self . ScreenRect . y      (                                 )
    SW        = self . ScreenRect . width  (                                 )
    SH        = self . ScreenRect . height (                                 )
    ##########################################################################
    F         = FaceItem                   (                                 )
    PTS       = F . Detect468Landmarks     ( RGB                           , \
                                             WW                            , \
                                             HH                            , \
                                             BX                            , \
                                             BY                            , \
                                             SW                            , \
                                             SH                              )
    ##########################################################################
    self . MESHs = { "Mesh" : False                                          }
    if                                     ( PTS [ "Ready" ]               ) :
      ########################################################################
      self . MESHs = { "Mesh" : True , "Points" : PTS                        }
    ##########################################################################
    self      . Notify                     ( 5                               )
    ##########################################################################
    return
  ############################################################################
  def NippleRecognition         ( self                                     ) :
    ##########################################################################
    AI      = self . Settings   [ "AI"                                       ]
    SVM     = AI                [ "Boobs-SVM"                                ]
    CASCADE = AI                [ "Boobs-Cascade"                            ]
    ##########################################################################
    IMG     = self . PictureItem . PICOP . toOpenCV (                        )
    GRAY    = cv2  . cvtColor               ( IMG , cv2 . COLOR_BGR2GRAY     )
    RGB     = cv2  . cvtColor               ( IMG , cv2 . COLOR_BGR2RGB      )
    WW      = self . PictureItem . PICOP . Width  (                          )
    HH      = self . PictureItem . PICOP . Height (                          )
    ##########################################################################
    TIT     = TitItem           (                                            )
    TIT     . LoadClassifier    ( CASCADE                                    )
    TIT     . LoadDetector      ( SVM                                        )
    ##########################################################################
    BOOBs   = TIT . ToBoobs     ( GRAY                                       )
    DLIBs   = TIT . ToDlibBoobs ( RGB                                        )
    ##########################################################################
    RECTs   =                   [                                            ]
    ##########################################################################
    for F in BOOBs                                                           :
      ########################################################################
      X     = F                 [ 0                                          ]
      Y     = F                 [ 1                                          ]
      W     = F                 [ 2                                          ]
      H     = F                 [ 3                                          ]
      R     =                   { "X" : X , "Y" : Y , "W" : W , "H" : H      }
      ########################################################################
      RECTs . append            ( R                                          )
    ##########################################################################
    for id in range ( 0 , len ( DLIBs ) )                                    :
      ########################################################################
      X     = DLIBs [ id ] . left   (                                        )
      Y     = DLIBs [ id ] . top    (                                        )
      W     = DLIBs [ id ] . width  (                                        )
      H     = DLIBs [ id ] . height (                                        )
      R     =                   { "X" : X , "Y" : Y , "W" : W , "H" : H      }
      ########################################################################
      RECTs . append            ( R                                          )
    ##########################################################################
    DRAWs   =                   [                                            ]
    RX      = self . PictureItem . Xratio
    RY      = self . PictureItem . Yratio
    ##########################################################################
    for R in RECTs                                                           :
      ########################################################################
      X     = R                 [ "X"                                        ]
      Y     = R                 [ "Y"                                        ]
      W     = R                 [ "W"                                        ]
      H     = R                 [ "H"                                        ]
      ########################################################################
      XX    = float             ( float ( X ) / RX                           )
      YY    = float             ( float ( Y ) / RY                           )
      PT    = QPointF           ( XX , YY                                    )
      ########################################################################
      PX    = self . PictureItem . mapToItem ( self , PT                     )
      ########################################################################
      WW    = float             ( float ( W ) / RX                           )
      HH    = float             ( float ( H ) / RY                           )
      PT    = QPointF           ( WW , HH                                    )
      ########################################################################
      PW    = self . PictureItem . mapToItem ( self , PT                     )
      ########################################################################
      X     = PX . x            (                                            )
      Y     = PX . y            (                                            )
      W     = PW . x            (                                            )
      H     = PW . y            (                                            )
      ########################################################################
      R     =                   { "X" : X , "Y" : Y , "W" : W , "H" : H      }
      ########################################################################
      DRAWs . append            ( R                                          )
    ##########################################################################
    self     . NIPPLEs =        { "Nipple" : True                          , \
                                  "Boobs"  : RECTs                         , \
                                  "Draws"  : DRAWs                           }
    ##########################################################################
    self     . Notify           ( 5                                          )
    ##########################################################################
    return
  ############################################################################
  def AdjustToSquare                      ( self                           ) :
    ##########################################################################
    RT   = self . ScreenRect
    WW   = RT   . width                   (                                  )
    HH   = RT   . height                  (                                  )
    ##########################################################################
    RX   = self . PictureItem . Xratio
    RY   = self . PictureItem . Yratio
    ##########################################################################
    RW   = float                          ( RX * WW                          )
    RH   = float                          ( RY * HH                          )
    ##########################################################################
    if                                    ( RW > RH                        ) :
      ########################################################################
      XX = RT   . x                       (                                  )
      YY = RT   . y                       (                                  )
      ########################################################################
      WX = float                          ( RW / RY                          )
      CC = float                          ( YY + float ( HH / 2 )            )
      YY = float                          ( CC - float ( WX / 2 )            )
      self . ScreenRect = QRectF          ( XX , YY , WW , WX                )
      ########################################################################
    else                                                                     :
      ########################################################################
      XX = RT   . x                       (                                  )
      YY = RT   . y                       (                                  )
      ########################################################################
      HY = float                          ( RH / RX                          )
      CC = float                          ( XX + float ( WW / 2 )            )
      XX = float                          ( CC - float ( HY / 2 )            )
      self . ScreenRect = QRectF          ( XX , YY , HY , HH                )
    ##########################################################################
    self . PaperRect = self . rectToPaper ( self . ScreenRect                )
    self . CalculateGeometry              (                                  )
    ##########################################################################
    return
  ############################################################################
  def AdjustWithinPicture         ( self                                   ) :
    ##########################################################################
    X    = self . Region . x      (                                          )
    Y    = self . Region . y      (                                          )
    W    = self . Region . width  (                                          )
    H    = self . Region . height (                                          )
    L    = int                    ( X + W                                    )
    B    = int                    ( Y + H                                    )
    ##########################################################################
    WW   = self . PictureItem . PICOP . Width  (                             )
    HH   = self . PictureItem . PICOP . Height (                             )
    ##########################################################################
    if ( X >= 0 ) and ( Y >= 0 ) and ( L <= WW ) and ( B <= HH )             :
      return
    ##########################################################################
    if                            ( X < 0                                  ) :
      X  = 0
    ##########################################################################
    if                            ( Y < 0                                  ) :
      Y  = 0
    ##########################################################################
    if                            ( L > WW                                 ) :
      L  = WW
    ##########################################################################
    if                            ( B > HH                                 ) :
      B  = HH
    ##########################################################################
    W    = int                    ( L - X                                    )
    H    = int                    ( B - Y                                    )
    ##########################################################################
    R    = QRect                  ( X , Y , W , H                            )
    ##########################################################################
    JSON =                        { "Function"  : "AdjustFaceRegion"       , \
                                    "Item"      : self                     , \
                                    "Parent"    : self . PictureItem       , \
                                    "Rectangle" : R                          }
    self . DoJsonCaller           ( JSON                                     )
    ##########################################################################
    return
  ############################################################################
  def PeopleDetailsChanged ( self , WhatJSON                               ) :
    ##########################################################################
    Action   = WhatJSON    [ "Action"                                        ]
    ##########################################################################
    if                     ( Action == "Detach"                            ) :
      ########################################################################
      WIDGET = WhatJSON    [ "Widget"                                        ]
      if                   ( WIDGET == self . PeopleDetailsUI              ) :
        self . PeopleDetailsUI = None
        print("Empty PeopleDetailsUI")
      ########################################################################
    elif                   ( Action == "People"                            ) :
      ########################################################################
      self   . PeopleUuid      = WhatJSON [ "People"                         ]
      self   . PeopleUuidAssigned (                                          )
    ##########################################################################
    elif                   ( Action == "Face"                              ) :
      ########################################################################
      Entry  = WhatJSON    [ "Entry"                                         ]
      if                   ( Entry == "Acceptor"                           ) :
        ######################################################################
        print("Face Acceptor")
        CB   = WhatJSON    [ "Callback"                                      ]
        if                 ( CB not in self . FaceCallbacks                ) :
          self . FaceCallbacks . append ( CB                                 )
      ########################################################################
    return                 { "Answer" : "Okay"                               }
  ############################################################################
  def AttachPeopleDetails ( self                                           ) :
    ##########################################################################
    JSON =                { "Function" : "AttachPeopleDetails"             , \
                            "Item"     : self                              , \
                            "Name"     : "人物詳細資訊" }
    self . DoJsonCaller   ( JSON                                             )
    ##########################################################################
    return
  ############################################################################
  def PeopleUuidAssigned ( self                                            ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def DeleteThisRegion ( self                                              ) :
    ##########################################################################
    self . DeleteItem  (                                                     )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def LinePointsEditingFinished  ( self , P1 , P2                          ) :
    ##########################################################################
    EM     = self . EditingMode
    self   . EditingMode = 0
    ##########################################################################
    if                           ( EM == 23521001                          ) :
      ########################################################################
      self . AssignRuleLine      ( P1 , P2                                   )
      ########################################################################
      return
    ##########################################################################
    if                           ( EM == 23521002                          ) :
      ########################################################################
      self . AssignMeasurePoints ( P1 , P2                                   )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def RecognitionMenu        ( self , mm                                   ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    MSG = self . getMenuItem ( "FeatureRecognition"                          )
    COL = mm   . addMenu     ( MSG                                           )
    ##########################################################################
    msg = TRX                [ "UI::ClearAll"                                ]
    mm  . addActionFromMenu  ( COL , 21451101 , msg                          )
    ##########################################################################
    msg = self . getMenuItem ( "EyesMouthFacial"                             )
    mm  . addActionFromMenu  ( COL , 21451102 , msg                          )
    ##########################################################################
    msg = self . getMenuItem ( "68Facial"                                    )
    mm  . addActionFromMenu  ( COL , 21451103 , msg                          )
    ##########################################################################
    msg = self . getMenuItem ( "468Facial"                                   )
    mm  . addActionFromMenu  ( COL , 21451104 , msg                          )
    ##########################################################################
    msg = self . getMenuItem ( "Nipple"                                      )
    mm  . addActionFromMenu  ( COL , 21451105 , msg                          )
    ##########################################################################
    return mm
  ############################################################################
  def RunRecognitionMenu            ( self , at                            ) :
    ##########################################################################
    if                              ( at == 21451101                       ) :
      ########################################################################
      self . ClearAll               (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451102                       ) :
      ########################################################################
      self . BasicFacialRecognition (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451103                       ) :
      ########################################################################
      self . Mark68Recognition      (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451104                       ) :
      ########################################################################
      self . Mark468Recognition     (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451105                       ) :
      ########################################################################
      self . NippleRecognition      (                                        )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def PicturesMenu               ( self , mm                               ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "PicturesOperation"                       )
    COL   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "CropImage"                               )
    mm    . addActionFromMenu    ( COL , 21451201 , msg                      )
    ##########################################################################
    if                           ( self . IsOkay ( self . NoseBridge )     ) :
      ########################################################################
      FMT = self . getMenuItem   ( "RotateImage"                             )
      msg = FMT  . format        ( self . RotateAngle ( )                    )
      mm  . addActionFromMenu    ( COL , 21451202 , msg                      )
    ##########################################################################
    mm    = self . RollImageMenu ( mm , COL                                  )
    ##########################################################################
    return mm
  ############################################################################
  def RunPicturesMenu         ( self , at                                  ) :
    ##########################################################################
    angle = self . RollImageSpin . value    (                                )
    self  . LimitValues [ "RollImageAngle" ] = angle
    ##########################################################################
    if                        ( at == 21451201                             ) :
      ########################################################################
      self . CropCurrentImage (                                              )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 21451202                             ) :
      ########################################################################
      self . PictureItem . CreateRotateImage ( self . RotateAngle ( )        )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 21451251                             ) :
      ########################################################################
      self  . PictureItem . CreateRotateImage ( angle                        )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def RegionMenu             ( self , mm                                   ) :
    ##########################################################################
    MSG = self . getMenuItem ( "RegionOperation"                             )
    COL = mm   . addMenu     ( MSG                                           )
    ##########################################################################
    msg = self . getMenuItem ( "AdjustToSquare"                              )
    mm  . addActionFromMenu  ( COL , 21451301 , msg                          )
    ##########################################################################
    msg = self . getMenuItem ( "AdjustWithinPicture"                         )
    mm  . addActionFromMenu  ( COL , 21451302 , msg                          )
    ##########################################################################
    return mm
  ############################################################################
  def RunRegionMenu              ( self , at                               ) :
    ##########################################################################
    if                           ( at == 21451301                          ) :
      ########################################################################
      self . AdjustToSquare      (                                           )
      ########################################################################
      return True
    ##########################################################################
    if                           ( at == 21451302                          ) :
      ########################################################################
      self . AdjustWithinPicture (                                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def PluginsMenu              ( self , mm                                 ) :
    ##########################################################################
    MSG   = self . getMenuItem ( "PluginsOperation"                          )
    COL   = mm   . addMenu     ( MSG                                         )
    ##########################################################################
    if                         ( self . NotOkay ( self . PeopleDetailsUI ) ) :
      msg = self . getMenuItem ( "AttachPeopleDetails"                       )
      mm  . addActionFromMenu  ( COL , 21451401 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunPluginsMenu             ( self , at                               ) :
    ##########################################################################
    if                           ( at == 21451401                          ) :
      ########################################################################
      self . AttachPeopleDetails (                                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , gview , pos , spos            ) :
    ##########################################################################
    mm     = MenuManager            ( gview                                  )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    R      = self . Region
    XX     = R . x                  (                                        )
    YY     = R . y                  (                                        )
    WW     = R . width              (                                        )
    HH     = R . height             (                                        )
    ##########################################################################
    MSG    = f"( {XX} , {YY} ) - ( {WW} x {HH} )"
    mm     . addAction              ( 34631001 , MSG                         )
    ##########################################################################
    msg    = TRX                    [ "UI::Delete"                           ]
    icon   = QIcon                  ( ":/images/delete.png"                  )
    mm     . addActionWithIcon      ( 1002 , icon , msg                      )
    ##########################################################################
    mm     . addSeparator           (                                        )
    self   . PicturesMenu           ( mm                                     )
    self   . RegionMenu             ( mm                                     )
    self   . RecognitionMenu        ( mm                                     )
    self   . MeasureMenu            ( mm                                     )
    self   . PluginsMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( gview   . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunMeasureMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunPicturesMenu    ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunRegionMenu      ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunRecognitionMenu ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunPluginsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( at == 1002                           ) :
      ########################################################################
      self . DeleteThisRegion       (                                        )
      ########################################################################
      return
    ##########################################################################
    return
##############################################################################
