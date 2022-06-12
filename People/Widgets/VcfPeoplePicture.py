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
import math
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
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QTransform
from   PyQt5 . QtGui                  import QPolygonF
from   PyQt5 . QtGui                  import QPainterPath
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
##############################################################################
from   AITK  . People . Faces . Face  import Face         as FaceItem
from   AITK  . People . Body  . Tit   import Tit          as TitItem
from   AITK  . People . Body  . Body  import Body         as BodyItem
##############################################################################
from   AITK  . VCF . VcfPicture       import VcfPicture   as VcfPicture
from   AITK  . People . Faces . VcfFaceRegion import VcfFaceRegion as VcfFaceRegion
##############################################################################
from   AITK  . Math . Geometry . Contour import Contour as Contour
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
    self . LastestZ       = None
    self . setFlag                ( QGraphicsItem . ItemIsMovable , False    )
    self . setZValue              ( 10000                                    )
    ##########################################################################
    self . defaultMeasurePoints   (                                          )
    ##########################################################################
    self . convex  = Contour      (                                          )
    self . convex  . setClosed    ( True                                     )
    self . convex  . setInvert    ( False                                    )
    self . convex  . setProperty  ( "Mode"        , 0                        )
    self . convex  . setProperty  ( "Picked"      , ""                       )
    self . convex  . setProperty  ( "State"       , 0                        )
    self . convex  . setProperty  ( "PointsId"    , 10009                    )
    self . convex  . setProperty  ( "ContourId"   , 10002                    )
    self . convex  . setProperty  ( "CubicId"     , 10003                    )
    self . convex  . setProperty  ( "QuadraticId" , 10004                    )
    self . convex  . setProperty  ( "Base"        , 0                        )
    self . convex  . setProperty  ( "Z"           , 0.0                      )
    self . convex  . setProperty  ( "RX"          , 10.0                     )
    self . convex  . setProperty  ( "RY"          , 10.0                     )
    self . convex  . setProperty  ( "Visible"     , True                     )
    self . convex  . PathUpdater = self . UpdateContourPoints
    ##########################################################################
    self . Painter . addMap       ( "Contour" , 10002                        )
    self . Painter . addPen       ( 10002 , QColor ( 255 , 128 ,  64 , 255 ) )
    self . Painter . addBrush     ( 10002 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . pens [ 10002 ] . setWidthF ( 7.5                        )
    ##########################################################################
    self . Painter . addMap       ( "Points"  , 10009                        )
    self . Painter . addPen       ( 10009 , QColor ( 128 ,  64 , 255 , 255 ) )
    self . Painter . addBrush     ( 10009 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . pens [ 10009 ] . setWidthF ( 4.5                        )
    ##########################################################################
    return
  ############################################################################
  def Painting                       ( self , p , region , clip , color    ) :
    ##########################################################################
    if                               ( clip                                ) :
      self . PaintImageClip          (        p , region , clip , color      )
    else                                                                     :
      self . PaintImage              (        p , region , clip , color      )
    ##########################################################################
    self   . PaintMeasureRule        (        p , region , clip , color      )
    self   . PaintMeasurePoints      (        p , region , clip , color      )
    self   . PaintLineEditing        (        p , region , clip , color      )
    self   . Painter . drawAllPathes (        p                              )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent          ( self , event                              ) :
    ##########################################################################
    OKAY      = self . IsMask  ( event . buttons ( ) , Qt . LeftButton       )
    if                         ( OKAY                                      ) :
      ########################################################################
      OKAY    = self . convex . HandleQPoint ( event . pos ( ) , 0           )
      if                       ( OKAY                                      ) :
        event . accept         (                                             )
        return
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
  def mouseMoveEvent           ( self , event                              ) :
    ##########################################################################
    OKAY      = self . IsMask  ( event . buttons ( ) , Qt . LeftButton       )
    if                         ( OKAY                                      ) :
      OKAY    = self . convex . HandleQPoint ( event . pos ( ) , 1           )
      if                       ( OKAY                                      ) :
        event . accept         (                                             )
        return
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
    OKAY    = self . convex . HandleQPoint ( event . pos ( ) , 2             )
    if                       ( OKAY                                        ) :
      event . accept         (                                               )
      return
    ##########################################################################
    OKAY = self . lineEditingReleaseEvent ( event                            )
    if                                    ( OKAY                           ) :
      return
    ##########################################################################
    self . scaleReleaseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def Hovering                   ( self , pos                              ) :
    ##########################################################################
    self . convex . HandleQPoint ( pos , 3                                   )
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
  def AddBodyRegion            ( self , KeyPoints                          ) :
    ##########################################################################
    SIZE = self . Image . size (                                             )
    W    = SIZE . width        (                                             )
    H    = SIZE . height       (                                             )
    RECT = QRect               ( 0 , 0 , W , H                               )
    ##########################################################################
    JSON =                     { "Function"  : "AddBodyRegion"             , \
                                 "Item"      : self                        , \
                                 "Region"    : RECT                        , \
                                 "Points"    : KeyPoints                     }
    self . DoJsonCaller        ( JSON                                        )
    ##########################################################################
    return
  ############################################################################
  def AddFaceRegion     ( self , rect                                      ) :
    ##########################################################################
    JSON =              { "Function"  : "AddFaceRegion"                    , \
                          "Item"      : self                               , \
                          "Rectangle" : rect                                 }
    self . DoJsonCaller ( JSON                                               )
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
  def FacialRecognition                      ( self , Square = False       ) :
    ##########################################################################
    ## self        . Gui . OnBusy  . emit       (                               )
    ##########################################################################
    AI          = self . Settings            [ "AI"                          ]
    HAAR        = AI                         [ "HAAR"                        ]
    EYES        = AI                         [ "Eyes"                        ]
    MOUTH       = AI                         [ "Mouth"                       ]
    FIVEMARKS   = AI                         [ "Fivemarks"                   ]
    LANDMARKS   = AI                         [ "Landmarks"                   ]
    RESNET      = AI                         [ "Resnet"                      ]
    ##########################################################################
    FC          = cv2  . CascadeClassifier   ( HAAR                          )
    FIVE        = dlib . shape_predictor     ( FIVEMARKS                     )
    PREDICTOR   = dlib . shape_predictor     ( LANDMARKS                     )
    FACIAL      = dlib . face_recognition_model_v1 ( RESNET                  )
    ##########################################################################
    IMG         = self . PICOP . toOpenCV    (                               )
    GRAY        = cv2  . cvtColor            ( IMG , cv2 . COLOR_BGR2GRAY    )
    WW          = self . PICOP . Width       (                               )
    HH          = self . PICOP . Height      (                               )
    ##########################################################################
    FACE        = FaceItem                   (                               )
    FACE        . Classifier = FC
    FACE        . Fivemarks  = FIVE
    FACE        . Predictor  = PREDICTOR
    FACE        . Facial     = FACIAL
    ##########################################################################
    FACEs       = FACE . ToFaces             ( GRAY                          )
    ##########################################################################
    for F in FACEs                                                           :
      ########################################################################
      if                                     ( Square                      ) :
        ######################################################################
        FACE    . setFull                    ( WW , HH                       )
        SRQ     = FACE . RectangleFromOpenCV ( F                             )
        KRQ     = FACE . ScaleRectangle      ( SRQ , 1.4                     )
        KQQ     = FACE . ToSquareRectangle   ( KRQ                           )
        SSK     = FACE . RestraintRectangle  ( FACE . Full , KQQ             )
        ######################################################################
        F [ 0 ] = SSK                        [ "X"                           ]
        F [ 1 ] = SSK                        [ "Y"                           ]
        F [ 2 ] = SSK                        [ "W"                           ]
        F [ 3 ] = SSK                        [ "H"                           ]
      ########################################################################
      X         = F                          [ 0                             ]
      Y         = F                          [ 1                             ]
      W         = F                          [ 2                             ]
      H         = F                          [ 3                             ]
      R         = QRect                      ( X , Y , W , H                 )
      ########################################################################
      self      . AddFaceRegion              ( R                             )
    ##########################################################################
    ## self        . Gui . GoRelax . emit       (                               )
    ## self        . prepareGeometryChange      (                               )
    self        . Notify                     ( 5                             )
    ##########################################################################
    return
  ############################################################################
  def BodyPoseEstimation           ( self                                  ) :
    ##########################################################################
    IMG  = self . PICOP . toOpenCV (                                         )
    RGB  = cv2  . cvtColor         ( IMG , cv2 . COLOR_BGR2RGB               )
    WW   = self . PICOP . Width    (                                         )
    HH   = self . PICOP . Height   (                                         )
    ##########################################################################
    BDI  = BodyItem                (                                         )
    KPS  = BDI . GetBodyKeyPoints  ( RGB , WW , HH                           )
    ##########################################################################
    self . AddBodyRegion           ( KPS                                     )
    ##########################################################################
    return
  ############################################################################
  def BoobsRecognition          ( self                                     ) :
    ##########################################################################
    AI       = self . Settings  [ "AI"                                       ]
    SVM      = AI               [ "Boobs-SVM"                                ]
    CASCADE  = AI               [ "Boobs-Cascade"                            ]
    ##########################################################################
    IMG      = self . PICOP . toOpenCV       (                               )
    GRAY     = cv2  . cvtColor               ( IMG , cv2 . COLOR_BGR2GRAY    )
    RGB      = cv2  . cvtColor               ( IMG , cv2 . COLOR_BGR2RGB     )
    WW       = self . PICOP . Width          (                               )
    HH       = self . PICOP . Height         (                               )
    ##########################################################################
    TIT     = TitItem           (                                            )
    TIT     . LoadClassifier    ( CASCADE                                    )
    TIT     . LoadDetector      ( SVM                                        )
    ##########################################################################
    BOOBs   = TIT . ToBoobs     ( GRAY                                       )
    DLIBs   = TIT . ToDlibBoobs ( RGB                                        )
    ##########################################################################
    for F in BOOBs                                                           :
      ########################################################################
      X     = F                 [ 0                                          ]
      Y     = F                 [ 1                                          ]
      W     = F                 [ 2                                          ]
      H     = F                 [ 3                                          ]
      R     = QRect             ( X , Y , W , H                              )
      ########################################################################
      self  . AddFaceRegion     ( R                                          )
    ##########################################################################
    for id in range ( 0 , len ( DLIBs ) )                                    :
      ########################################################################
      X     = DLIBs [ id ] . left   (                                        )
      Y     = DLIBs [ id ] . top    (                                        )
      W     = DLIBs [ id ] . width  (                                        )
      H     = DLIBs [ id ] . height (                                        )
      R     = QRect             ( X , Y , W , H                              )
      ########################################################################
      self  . AddFaceRegion     ( R                                          )
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
    self . DoJsonCaller          ( JSON                                      )
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
  def CropCurrentImage        ( self , region                              ) :
    ##########################################################################
    X   = region . x          (                                              )
    Y   = region . y          (                                              )
    W   = region . width      (                                              )
    H   = region . height     (                                              )
    PIC = self . PICOP . Crop ( X , Y , W , H                                )
    ##########################################################################
    return PIC
  ############################################################################
  def ProduceCropImage               ( self , region                       ) :
    ##########################################################################
    PIC    = self . CropCurrentImage (        region                         )
    ##########################################################################
    if                               ( self . LastestZ in [ False , None ] ) :
      self . LastestZ = self . zValue ( ) + 10.0
    else                                                                     :
      self . LastestZ = self . LastestZ   + 10.0
    ##########################################################################
    JSON =                           { "Function" : "AddPicture"           , \
                                       "Picture"  : PIC                    , \
                                       "Z"        : self . LastestZ          }
    self . DoJsonCaller              ( JSON                                  )
    ##########################################################################
    return
  ############################################################################
  def CreateCropImage              ( self , region                         ) :
    ##########################################################################
    VAL  =                         ( region ,                                )
    self . Go                      ( self . ProduceCropImage , VAL           )
    ##########################################################################
    return
  ############################################################################
  def SaveAs                       ( self                                  ) :
    ##########################################################################
    Filename , _ = QFileDialog . getSaveFileName                             (
                                     self . Gui                              ,
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
  def UpdateContourPoints                 ( self , convex , ACT , U = True ) :
    ##########################################################################
    if                                    ( ACT == 1                       ) :
      self . setCursor                    ( Qt . ArrowCursor                 )
    elif                                  ( ACT == 2                       ) :
      self . setCursor                    ( Qt . CrossCursor                 )
    elif                                  ( ACT == 3                       ) :
      self . setCursor                    ( Qt . PointingHandCursor          )
    elif                                  ( ACT == 4                       ) :
      self . setCursor                    ( Qt . OpenHandCursor              )
    elif                                  ( ACT == 5                       ) :
      self . setCursor                    ( Qt . ClosedHandCursor            )
    ##########################################################################
    if                                    ( not U                          ) :
      return
    ##########################################################################
    PID  = convex . getProperty           ( "PointsId"                       )
    CID  = convex . getProperty           ( "ContourId"                      )
    VID  = convex . getProperty           ( "CubicId"                        )
    QID  = convex . getProperty           ( "QuadraticId"                    )
    ##########################################################################
    p1   = QPainterPath                   (                                  )
    p2   = QPainterPath                   (                                  )
    p1   = convex . PointsToQPainterPath  ( p1                               )
    p2   = convex . ContourToQPainterPath ( p2                               )
    ##########################################################################
    self . Painter . pathes   [ PID ] = p1
    self . Painter . switches [ PID ] = True
    ##########################################################################
    self . Painter . pathes   [ CID ] = p2
    self . Painter . switches [ CID ] = True
    ##########################################################################
    self . update                         (                                  )
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
    MSG   = self . getMenuItem     ( "SquareFacial"                          )
    mm    . addActionFromMenu      ( LOM , 98438502 , MSG                    )
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
    MSG   = self . getMenuItem     ( "BoobsRecognition"                      )
    mm    . addActionFromMenu      ( LOM , 98438602 , MSG                    )
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
    mm    = self . RollImageMenu ( mm , LOM                                  )
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    self  . PeopleFaceMenu       ( mm , LOM                                  )
    self  . PeopleBodyMenu       ( mm , LOM                                  )
    ##########################################################################
    return
  ############################################################################
  def RunRecognitionMenu        ( self , at                                ) :
    ##########################################################################
    angle = self . RollImageSpin . value    (                              )
    self  . LimitValues [ "RollImageAngle" ] = angle
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
      self . Go                 ( self . FacialRecognition , ( False , )     )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438502                           ) :
      ########################################################################
      self . Go                 ( self . FacialRecognition , ( True  , )     )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438601                           ) :
      ########################################################################
      self . Go                 ( self . BodyPoseEstimation                  )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438602                           ) :
      ########################################################################
      self . Go                 ( self . BoobsRecognition                    )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 21451251                             ) :
      ########################################################################
      self  . CreateRotateImage ( angle                                      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                      ( self , gview , pos , spos                ) :
    ##########################################################################
    mm     = MenuManager        ( gview                                      )
    ##########################################################################
    self   . InformationMenu    ( mm                                         )
    mm     . addSeparator       (                                            )
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
    msg    = self . getMenuItem ( "OriginalPosition"                         )
    mm     . addAction          ( 1003 , msg                                 )
    ##########################################################################
    vexMode = self . convex  . getProperty  ( "Mode"                         )
    VM     =                    ( vexMode == 1                               )
    msg    = "新增點"
    mm     . addAction          ( 7001 , msg , True , VM                     )
    VM     =                    ( vexMode == 2                               )
    msg    = "修改點"
    mm     . addAction          ( 7002 , msg , True , VM                     )
    ##########################################################################
    mm     . addSeparator       (                                            )
    self   . RecognitionMenu    ( mm                                         )
    self   . MeasureMenu        ( mm                                         )
    self   . StatesMenu         ( mm                                         )
    self   . LayerMenu          ( mm                                         )
    ##########################################################################
    mm     . setFont            ( gview   . menuFont ( )                     )
    aa     = mm . exec_         ( QCursor . pos      ( )                     )
    at     = mm . at            ( aa                                         )
    ##########################################################################
    if                          ( self . RunLayerMenu       ( at         ) ) :
      return True
    ##########################################################################
    if                          ( self . RunMeasureMenu     ( at         ) ) :
      return True
    ##########################################################################
    if                          ( self . RunStatesMenu      ( at         ) ) :
      return True
    ##########################################################################
    if                          ( self . RunRecognitionMenu ( at         ) ) :
      return True
    ##########################################################################
    if                          ( at == 1001                               ) :
      ########################################################################
      self . DeleteItem         (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 1002                               ) :
      ########################################################################
      self . SaveAs             (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 1003                               ) :
      ########################################################################
      self . OriginalRect       (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 7001                               ) :
      ########################################################################
      vexMode = self . convex  . getProperty  ( "Mode"                       )
      VM     =                  ( vexMode == 1                               )
      if                        ( VM                                       ) :
        vexMode = 0
      else                                                                   :
        vexMode = 1
      self . convex . setProperty ( "Mode" , vexMode                         )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 7002                               ) :
      ########################################################################
      vexMode = self . convex  . getProperty  ( "Mode"                       )
      VM     =                  ( vexMode == 2                               )
      if                        ( VM                                       ) :
        vexMode = 0
      else                                                                   :
        vexMode = 2
      self . convex . setProperty ( "Mode" , vexMode                         )
      ########################################################################
      return True
    ##########################################################################
    return   True
##############################################################################
