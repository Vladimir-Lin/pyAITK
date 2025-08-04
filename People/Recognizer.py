# -*- coding: utf-8 -*-
##############################################################################
## 辨識引擎
##############################################################################
import os
import sys
import time
import datetime
import requests
import threading
import json
import math
##############################################################################
import cv2
import dlib
import numpy as np
##############################################################################
import mediapipe
from   mediapipe . tasks                    import python
from   mediapipe . tasks     . python       import vision
##############################################################################
from   AITK      . Calendars . StarDate     import StarDate
from   AITK      . Graphics  . Color . RGBi import RGBi
from   AITK      . Graphics  . Color . HSVi import HSVi
from   AITK      . People    . Eyes  . Iris import EyeColorRanges
from   AITK      . People    . Faces . Face import FaceLandmarks468Meshes
from   AITK      . People    . Faces . Face import FaceLandmarks468Polygons
##############################################################################
RVERSION = "2025-05-03"
##############################################################################
class Recognizer (                                                         ) :
  ############################################################################
  def __init__   ( self                                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    return
  ############################################################################
  def Initialize                        ( self , Settings                  ) :
    ##########################################################################
    self . Settings = Settings
    ##########################################################################
    self . CONF     =                   {                                    }
    ##########################################################################
    DIR             = self . Settings   [ "Data"                             ]
    ##########################################################################
    self            . PrepareAIdata     ( DIR , "HAAR"                       )
    self            . PrepareAIdata     ( DIR , "Eyes"                       )
    self            . PrepareAIdata     ( DIR , "Mouth"                      )
    self            . PrepareAIdata     ( DIR , "Landmarks"                  )
    self            . PrepareAIdata     ( DIR , "Fivemarks"                  )
    self            . PrepareAIdata     ( DIR , "Resnet"                     )
    self            . PrepareAIdata     ( DIR , "Boobs-SVM"                  )
    self            . PrepareAIdata     ( DIR , "Boobs-Cascade"              )
    self            . PrepareAIdata     ( DIR , "Boobs-Paired"               )
    self            . PrepareAIdata     ( DIR , "Boobs-Single"               )
    ##########################################################################
    HAAR            = self . CONF       [ "HAAR"                             ]
    EYES            = self . CONF       [ "Eyes"                             ]
    MOUTH           = self . CONF       [ "Mouth"                            ]
    FIVEMARKS       = self . CONF       [ "Fivemarks"                        ]
    LANDMARKS       = self . CONF       [ "Landmarks"                        ]
    RESNET          = self . CONF       [ "Resnet"                           ]
    CASCADE         = self . CONF       [ "Boobs-Cascade"                    ]
    SVM             = self . CONF       [ "Boobs-SVM"                        ]
    ##########################################################################
    FC              = cv2  . CascadeClassifier         ( HAAR                )
    EC              = cv2  . CascadeClassifier         ( EYES                )
    MC              = cv2  . CascadeClassifier         ( MOUTH               )
    FIVE            = dlib . shape_predictor           ( FIVEMARKS           )
    PREDICTOR       = dlib . shape_predictor           ( LANDMARKS           )
    FACIAL          = dlib . face_recognition_model_v1 ( RESNET              )
    CVBOOB          = cv2  . CascadeClassifier         ( CASCADE             )
    SVMBOOB         = dlib . simple_object_detector    ( SVM                 )
    ##########################################################################
    self            . Classifier    = FC
    self            . EyesDetector  = EC
    self            . MouthDetector = MC
    self            . Fivemarks     = FIVE
    self            . Predictor     = PREDICTOR
    self            . Facial        = FACIAL
    self            . CvBoob        = CVBOOB
    self            . DlibBoob      = SVMBOOB
    ##########################################################################
    CONF            = self . Settings   [ "Classifier" ] [ "File"            ]
    MAXI            = self . Settings   [ "Classifier" ] [ "Max"             ]
    self            . setClassifierPath ( CONF , MAXI                        )
    ##########################################################################
    CONF            = self . Settings   [ "Objectron"  ] [ "File"            ]
    MAXI            = self . Settings   [ "Objectron"  ] [ "Max"             ]
    THRS            = self . Settings   [ "Objectron"  ] [ "Threshold"       ]
    self            . setObjectronPath  ( CONF , MAXI , THRS                 )
    ##########################################################################
    CONF            = self . Settings   [ "Stylizers"  ] [ "Sketch"          ]
    self            . setStylizerPath   ( CONF                               )
    ##########################################################################
    self            . PreparePostures   (                                    )
    ##########################################################################
    self            . Creator = None
    ##########################################################################
    return
  ############################################################################
  def PrepareAIdata ( self , DIR , KEY                                     ) :
    ##########################################################################
    AIFILE              = self . Settings [ "AiData" ] [ KEY                 ]
    self . CONF [ KEY ] = f"{DIR}/{AIFILE}"
    ##########################################################################
    return
  ############################################################################
  def PreparePostures                            ( self                    ) :
    ##########################################################################
    self . mpPose = mediapipe . solutions . pose
    self . Pose   = self      . mpPose    . Pose (                           )
    ##########################################################################
    return
  ############################################################################
  ## 物件產生器
  ############################################################################
  def Create                ( self , Name                                  ) :
    ##########################################################################
    if                      ( self . Creator in [ False , None ]           ) :
      return None
    ##########################################################################
    return   self . Creator (        Name                                    )
  ############################################################################
  ## 取得Mediapipe影像
  ############################################################################
  def MediaPipeImage                            ( self , FILENAME          ) :
    return mediapipe . Image . create_from_file (        FILENAME            )
  ############################################################################
  ## CV影像轉Mediapipe
  ############################################################################
  def CvToMediaPipeImage     ( self , image                                ) :
    return mediapipe . Image ( image_format = mediapipe . ImageFormat . SRGB , data = image )
  ############################################################################
  ## 指定物件偵測參數
  ############################################################################
  def setObjectronPath ( self                                              , \
                         detection                                         , \
                         MAXITEMS  = 5000                                  , \
                         THRESHOLD = 0.5                                   ) :
    ##########################################################################
    ObjectDetector        = mediapipe . tasks . vision . ObjectDetector
    ObjectDetectorOptions = mediapipe . tasks . vision . ObjectDetectorOptions
    VisionRunningMode     = mediapipe . tasks . vision . RunningMode
    ##########################################################################
    try                                                                      :
      ########################################################################
      with open        ( detection , "rb" ) as mpFile                        :
        BUFF = mpFile . read (                                               )
      ########################################################################
    except                                                                   :
      return
    ##########################################################################
    self . Tron           = None
    self . DetectionPath  = detection
    ## self . TronOpts       = mediapipe . tasks . BaseOptions ( model_asset_path = detection )
    self . TronOpts       = mediapipe . tasks . BaseOptions ( model_asset_buffer = BUFF )
    ##########################################################################
    OPTS                  = ObjectDetectorOptions                          ( \
                              base_options    = self . TronOpts            , \
                              max_results     = MAXITEMS                   , \
                              score_threshold = THRESHOLD                  , \
                              running_mode    = VisionRunningMode . IMAGE    )
    ##########################################################################
    self . Tron      = ObjectDetector . create_from_options ( OPTS           )
    ##########################################################################
    return
  ############################################################################
  ## 執行物件偵測
  ############################################################################
  def ObjectDetection ( self                                               , \
                        IMAGE                                              , \
                        Probability = 0.1                                  ) :
    ##########################################################################
    ITEMs  =          [                                                      ]
    RESULT = self . Tron . detect ( IMAGE                                    )
    ##########################################################################
    for OBJ in RESULT . detections                                           :
      ########################################################################
      F = False
      J = { "Box"        : { }                                             , \
            "Categories" : [ ]                                               }
      ########################################################################
      J [ "Box" ] [ "X" ] = int ( OBJ . bounding_box . origin_x              )
      J [ "Box" ] [ "Y" ] = int ( OBJ . bounding_box . origin_y              )
      J [ "Box" ] [ "W" ] = int ( OBJ . bounding_box . width                 )
      J [ "Box" ] [ "H" ] = int ( OBJ . bounding_box . height                )
      ########################################################################
      for item in OBJ . categories                                           :
        ######################################################################
        IDX = -1
        NAM = ""
        PRT = 0.0
        CAX = ""
        ######################################################################
        if ( item . index         not in [ False , None                  ] ) :
          ####################################################################
          IDX = int ( item . index )
        ######################################################################
        if ( item . display_name  not in [ False , None                  ] ) :
          ####################################################################
          NAM = item . display_name
        ######################################################################
        if ( item . score         not in [ False , None                  ] ) :
          ####################################################################
          PRT = float ( item . score )
        ######################################################################
        if ( item . category_name not in [ False , None                  ] ) :
          ####################################################################
          CAX = item . category_name
        ######################################################################
        K = { "Id"          : IDX                                          , \
              "Name"        : NAM                                          , \
              "Probability" : PRT                                          , \
              "Category"    : CAX                                            }
        ######################################################################
        J [ "Categories" ] . append ( K                                      )
        ######################################################################
        if ( PRT >= Probability                                            ) :
          ####################################################################
          F = True
      ########################################################################
      if               ( F                                                 ) :
        ######################################################################
        ITEMs . append ( J                                                   )
    ##########################################################################
    return ITEMs
  ############################################################################
  ## 指定圖像分類參數
  ############################################################################
  def setClassifierPath ( self , classifier , MAXITEMS = 5000              ) :
    ##########################################################################
    ImageClassifier        = mediapipe . tasks . vision . ImageClassifier
    ImageClassifierOptions = mediapipe . tasks . vision . ImageClassifierOptions
    VisionRunningMode      = mediapipe . tasks . vision . RunningMode
    ##########################################################################
    try                                                                      :
      ########################################################################
      with open         ( classifier , "rb" ) as mpFile                      :
        BUFF = mpFile . read (                                               )
      ########################################################################
    except                                                                   :
      return
    ##########################################################################
    self . Catalog         = None
    self . ClassifierPath  = classifier
    self . BaseOpts        = mediapipe . tasks . BaseOptions ( model_asset_buffer = BUFF )
    ##########################################################################
    OPTS                   = ImageClassifierOptions                        ( \
                               base_options = self . BaseOpts              , \
                               max_results  = MAXITEMS                     , \
                               running_mode = VisionRunningMode . IMAGE      )
    ##########################################################################
    self . Catalog = ImageClassifier . create_from_options ( OPTS            )
    ##########################################################################
    return
  ############################################################################
  ## 執行圖像分類
  ############################################################################
  def Classification ( self                                                , \
                       IMAGE                                               , \
                       Probability = 0.00001                               ) :
    ##########################################################################
    if               ( self . Catalog in [ False , None                  ] ) :
      return         [                                                       ]
    ##########################################################################
    ITEMs  =         [                                                       ]
    ##########################################################################
    RESULT = self . Catalog . classify ( IMAGE                               )
    ##########################################################################
    for Scope in RESULT . classifications                                    :
      ########################################################################
      for item in Scope . categories                                         :
        ######################################################################
        if ( item . score < Probability                                    ) :
          continue
        ######################################################################
        J = { "Id"          : int   ( item . index )                       , \
              "Name"        : item . display_name                          , \
              "Probability" : float ( item . score )                       , \
              "Category"    : item . category_name                           }
        ######################################################################
        ITEMs . append ( J                                                   )
    ##########################################################################
    return ITEMs
  ############################################################################
  ## 集中分類名稱
  ############################################################################
  def toCategories   ( self , ITEMs                                        ) :
    ##########################################################################
    NAMEs   =        [                                                       ]
    ##########################################################################
    for item in ITEMs                                                        :
      ########################################################################
      NAMEs . append ( item [ "Category"                                   ] )
    ##########################################################################
    return NAMEs
  ############################################################################
  ## 指定物件偵測參數
  ############################################################################
  def setStylizerPath ( self , StylePath                                   ) :
    ##########################################################################
    FaceStylizer        = mediapipe . tasks . vision . FaceStylizer
    FaceStylizerOptions = mediapipe . tasks . vision . FaceStylizerOptions
    ##########################################################################
    try                                                                      :
      ########################################################################
      with open       ( StylePath , "rb" ) as mpFile                         :
        BUFF = mpFile . read (                                               )
      ########################################################################
    except                                                                   :
      return
    ##########################################################################
    self . Stylizer     = None
    self . StylePath    = StylePath
    ## self . StyleOpts    = mediapipe . tasks . BaseOptions ( model_asset_path = StylePath )
    self . StyleOpts    = mediapipe . tasks . BaseOptions ( model_asset_buffer = BUFF )
    ##########################################################################
    OPTS                = FaceStylizerOptions                              ( \
                          base_options    = self . StyleOpts                 )
    ##########################################################################
    self . Stylizer     = FaceStylizer . create_from_options ( OPTS          )
    ##########################################################################
    return
  ############################################################################
  def Stylization                    ( self , IMAGE                        ) :
    return self . Stylizer . stylize (        IMAGE                          )
  ############################################################################
  def CreateRectangle ( self , x , y , w , h                               ) :
    ##########################################################################
    R    = int ( x ) + int ( w     ) - 1
    B    = int ( y ) + int ( h     ) - 1
    CX   = int ( x ) + int ( w / 2 )
    CY   = int ( y ) + int ( h / 2 )
    ##########################################################################
    RECT =            { "X"     : int   ( x   )                            , \
                        "Y"     : int   ( y   )                            , \
                        "W"     : int   ( w   )                            , \
                        "H"     : int   ( h   )                            , \
                        "R"     : int   ( R   )                            , \
                        "B"     : int   ( B   )                            , \
                        "CX"    : int   ( CX  )                            , \
                        "CY"    : int   ( CY  )                            , \
                        "Angle" : float ( 0.0 )                              }
    ##########################################################################
    return RECT
  ############################################################################
  def CreateRectangleByJR         ( self , RT                              ) :
    ##########################################################################
    x = RT                        [ "X"                                      ]
    y = RT                        [ "Y"                                      ]
    w = RT                        [ "W"                                      ]
    h = RT                        [ "H"                                      ]
    ##########################################################################
    return self . CreateRectangle ( x , y , w , h                            )
  ############################################################################
  def RectangleToString ( self , RT                                        ) :
    ##########################################################################
    X = RT              [ "X"                                                ]
    Y = RT              [ "Y"                                                ]
    W = RT              [ "W"                                                ]
    H = RT              [ "H"                                                ]
    ##########################################################################
    return f"{X} {Y} {W} {H}"
  ############################################################################
  def RectanglesToStrings ( self , RECTs                                   ) :
    ##########################################################################
    RS   =                [                                                  ]
    ##########################################################################
    for R in RECTs                                                           :
      RS . append         ( self . RectangleToString ( R )                   )
    ##########################################################################
    return RS
  ############################################################################
  def RectToXYWH ( self , rect                                             ) :
    ##########################################################################
    x = rect     [ "X"                                                       ]
    y = rect     [ "Y"                                                       ]
    w = rect     [ "W"                                                       ]
    h = rect     [ "H"                                                       ]
    ##########################################################################
    return       ( x , y , w , h ,                                           )
  ############################################################################
  def NegativeXY      ( self , PT                                          ) :
    ##########################################################################
    PT [ "X" ] = - PT [ "X"                                                  ]
    PT [ "Y" ] = - PT [ "Y"                                                  ]
    ##########################################################################
    return PT
  ############################################################################
  def ShiftRectangle ( self , PT , RT                                      ) :
    ##########################################################################
    PX         = PT  [ "X"                                                   ]
    PY         = PT  [ "Y"                                                   ]
    ##########################################################################
    XX         = RT  [ "X"                                                   ]
    YY         = RT  [ "Y"                                                   ]
    ##########################################################################
    RT [ "X" ] = XX + PX
    RT [ "Y" ] = YY + PY
    ##########################################################################
    return RT
  ############################################################################
  def GetRectangleFromPoints      ( self , POINTs                          ) :
    ##########################################################################
    T     = int                   (  10000000000                             )
    L     = int                   (  10000000000                             )
    B     = int                   ( -10000000000                             )
    R     = int                   ( -10000000000                             )
    ##########################################################################
    for PT in POINTs                                                         :
      ########################################################################
      XP  = PT                    [ "X"                                      ]
      YP  = PT                    [ "Y"                                      ]
      ########################################################################
      if                          ( XP < L                                 ) :
        L = XP
      ########################################################################
      if                          ( XP > R                                 ) :
        R = XP
      ########################################################################
      if                          ( YP < T                                 ) :
        T = YP
      ########################################################################
      if                          ( YP > B                                 ) :
        B = YP
    ##########################################################################
    x     = int                   ( L                                        )
    y     = int                   ( T                                        )
    w     = int                   ( R - L + 1                                )
    h     = int                   ( B - T + 1                                )
    ##########################################################################
    return self . CreateRectangle ( x , y , w , h                            )
  ############################################################################
  def PointsToCvPoints ( self , BX , BY , POINTs                           ) :
    ##########################################################################
    PTs   =            [                                                     ]
    ##########################################################################
    for PT in POINTs                                                         :
      ########################################################################
      XP  = PT         [ "X"                                                 ]
      YP  = PT         [ "Y"                                                 ]
      ########################################################################
      PTs . append     ( [ int ( XP - BX ) , int ( YP - BY ) ]               )
    ##########################################################################
    return PTs
  ############################################################################
  def CvToRectangle               ( self , rect                            ) :
    ##########################################################################
    x = int                       ( rect [ 0                               ] )
    y = int                       ( rect [ 1                               ] )
    w = int                       ( rect [ 2                               ] )
    h = int                       ( rect [ 3                               ] )
    ##########################################################################
    return self . CreateRectangle ( x , y , w , h                            )
  ############################################################################
  def DlibToRectangle             ( self , rect                            ) :
    ##########################################################################
    x = rect . left               (                                          )
    y = rect . top                (                                          )
    w = rect . width              (                                          )
    h = rect . height             (                                          )
    ##########################################################################
    return self . CreateRectangle ( x , y , w , h                            )
  ############################################################################
  def ToDlibRectangle       ( self , rect                                  ) :
    ##########################################################################
    x = rect                [ "X"                                            ]
    y = rect                [ "Y"                                            ]
    r = rect                [ "R"                                            ]
    b = rect                [ "B"                                            ]
    ##########################################################################
    return dlib . rectangle ( left = x , top = y , right = r , bottom = b    )
  ############################################################################
  def CvToRectangles               ( self , RECTs                          ) :
    ##########################################################################
    LISTs   =                      [                                         ]
    ##########################################################################
    if                             ( len ( RECTs ) <= 0                    ) :
      return LISTs
    ##########################################################################
    for R in RECTs                                                           :
      ########################################################################
      CRV   = self . CvToRectangle ( R                                       )
      LISTs . append               ( CRV                                     )
    ##########################################################################
    return LISTs
  ############################################################################
  def ParseCoordinate ( self , KEYs , ITEM , W , H                         ) :
    ##########################################################################
    X = int           ( KEYs . landmark [ ITEM ] . x * W                     )
    Y = int           ( KEYs . landmark [ ITEM ] . y * H                     )
    ##########################################################################
    return            { "X" : X , "Y" : Y                                    }
  ############################################################################
  def LandmarkToNpArray ( self , LMS , major , minor = ""                  ) :
    ##########################################################################
    if                  ( len ( major ) <= 0                               ) :
      return            [                                                    ]
    ##########################################################################
    if                  ( len ( minor ) <= 0                               ) :
      ########################################################################
      F = LMS           [ major                                              ]
      ########################################################################
    else                                                                     :
      ########################################################################
      F = LMS           [ major ] [ minor                                    ]
    ##########################################################################
    return np . array   ( F , dtype = np . int32                             )
  ############################################################################
  def GetBodyKeyPoints ( self , Image , W , H                              ) :
    ##########################################################################
    J     =            { "Body"  : { "Exists" : False                    } , \
                         "Box"   : { "X" : 0                               , \
                                     "Y" : 0                               , \
                                     "W" : W                               , \
                                     "H" : H                             } , \
                         "Nose"  : { }                                     , \
                         "Left"  : { }                                     , \
                         "Right" : { }                                       }
    ##########################################################################
    MPX   = self . mpPose . PoseLandmark
    KPS   = self . Pose   . process (        Image                           )
    KPL   = KPS  . pose_landmarks
    ##########################################################################
    if                              ( KPL in [ False , None              ] ) :
      return J
    ##########################################################################
    J [ "Nose"                  ] = self . ParseCoordinate ( KPL , MPX . NOSE             , W , H )
    ##########################################################################
    J [ "Left"  ] [ "Ankle"     ] = self . ParseCoordinate ( KPL , MPX . LEFT_ANKLE       , W , H )
    J [ "Left"  ] [ "Ear"       ] = self . ParseCoordinate ( KPL , MPX . LEFT_EAR         , W , H )
    J [ "Left"  ] [ "Elbow"     ] = self . ParseCoordinate ( KPL , MPX . LEFT_ELBOW       , W , H )
    J [ "Left"  ] [ "Eye"       ] = self . ParseCoordinate ( KPL , MPX . LEFT_EYE         , W , H )
    J [ "Left"  ] [ "EyeInner"  ] = self . ParseCoordinate ( KPL , MPX . LEFT_EYE_INNER   , W , H )
    J [ "Left"  ] [ "EyeOuter"  ] = self . ParseCoordinate ( KPL , MPX . LEFT_EYE_OUTER   , W , H )
    J [ "Left"  ] [ "FootIndex" ] = self . ParseCoordinate ( KPL , MPX . LEFT_FOOT_INDEX  , W , H )
    J [ "Left"  ] [ "Heel"      ] = self . ParseCoordinate ( KPL , MPX . LEFT_HEEL        , W , H )
    J [ "Left"  ] [ "Hip"       ] = self . ParseCoordinate ( KPL , MPX . LEFT_HIP         , W , H )
    J [ "Left"  ] [ "Index"     ] = self . ParseCoordinate ( KPL , MPX . LEFT_INDEX       , W , H )
    J [ "Left"  ] [ "Knee"      ] = self . ParseCoordinate ( KPL , MPX . LEFT_KNEE        , W , H )
    J [ "Left"  ] [ "Mouth"     ] = self . ParseCoordinate ( KPL , MPX . MOUTH_LEFT       , W , H )
    J [ "Left"  ] [ "Pinky"     ] = self . ParseCoordinate ( KPL , MPX . LEFT_PINKY       , W , H )
    J [ "Left"  ] [ "Shoulder"  ] = self . ParseCoordinate ( KPL , MPX . LEFT_SHOULDER    , W , H )
    J [ "Left"  ] [ "Thumb"     ] = self . ParseCoordinate ( KPL , MPX . LEFT_THUMB       , W , H )
    J [ "Left"  ] [ "Wrist"     ] = self . ParseCoordinate ( KPL , MPX . LEFT_WRIST       , W , H )
    ##########################################################################
    J [ "Right" ] [ "Ankle"     ] = self . ParseCoordinate ( KPL , MPX . RIGHT_ANKLE      , W , H )
    J [ "Right" ] [ "Ear"       ] = self . ParseCoordinate ( KPL , MPX . RIGHT_EAR        , W , H )
    J [ "Right" ] [ "Elbow"     ] = self . ParseCoordinate ( KPL , MPX . RIGHT_ELBOW      , W , H )
    J [ "Right" ] [ "Eye"       ] = self . ParseCoordinate ( KPL , MPX . RIGHT_EYE        , W , H )
    J [ "Right" ] [ "EyeInner"  ] = self . ParseCoordinate ( KPL , MPX . RIGHT_EYE_INNER  , W , H )
    J [ "Right" ] [ "EyeOuter"  ] = self . ParseCoordinate ( KPL , MPX . RIGHT_EYE_OUTER  , W , H )
    J [ "Right" ] [ "FootIndex" ] = self . ParseCoordinate ( KPL , MPX . RIGHT_FOOT_INDEX , W , H )
    J [ "Right" ] [ "Heel"      ] = self . ParseCoordinate ( KPL , MPX . RIGHT_HEEL       , W , H )
    J [ "Right" ] [ "Hip"       ] = self . ParseCoordinate ( KPL , MPX . RIGHT_HIP        , W , H )
    J [ "Right" ] [ "Index"     ] = self . ParseCoordinate ( KPL , MPX . RIGHT_INDEX      , W , H )
    J [ "Right" ] [ "Knee"      ] = self . ParseCoordinate ( KPL , MPX . RIGHT_KNEE       , W , H )
    J [ "Right" ] [ "Mouth"     ] = self . ParseCoordinate ( KPL , MPX . MOUTH_RIGHT      , W , H )
    J [ "Right" ] [ "Pinky"     ] = self . ParseCoordinate ( KPL , MPX . RIGHT_PINKY      , W , H )
    J [ "Right" ] [ "Shoulder"  ] = self . ParseCoordinate ( KPL , MPX . RIGHT_SHOULDER   , W , H )
    J [ "Right" ] [ "Thumb"     ] = self . ParseCoordinate ( KPL , MPX . RIGHT_THUMB      , W , H )
    J [ "Right" ] [ "Wrist"     ] = self . ParseCoordinate ( KPL , MPX . RIGHT_WRIST      , W , H )
    ##########################################################################
    J [ "Body"  ] [ "Exists"    ] = True
    ##########################################################################
    return J
  ############################################################################
  def isRectInRect ( self , A , B                                          ) :
    ##########################################################################
    AX = A         [ "X"                                                     ]
    AR = A         [ "R"                                                     ]
    BX = B         [ "X"                                                     ]
    BR = B         [ "R"                                                     ]
    ##########################################################################
    if             ( AX > BX                                               ) :
      return False
    ##########################################################################
    if             ( AR < BX                                               ) :
      return False
    ##########################################################################
    if             ( AX > BR                                               ) :
      return False
    ##########################################################################
    if             ( AR < BR                                               ) :
      return False
    ##########################################################################
    AY = A         [ "Y"                                                     ]
    AB = A         [ "B"                                                     ]
    BY = B         [ "Y"                                                     ]
    BB = B         [ "B"                                                     ]
    ##########################################################################
    if             ( AY > BY                                               ) :
      return False
    ##########################################################################
    if             ( AB < BY                                               ) :
      return False
    ##########################################################################
    if             ( AY > BB                                               ) :
      return False
    ##########################################################################
    if             ( AB < BB                                               ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def hasRectsInRect ( self , RECT , RECTs                                 ) :
    ##########################################################################
    for R in RECTs                                                           :
      if             ( self . isRectInRect ( RECT , R )                    ) :
        return True
    ##########################################################################
    return     False
  ############################################################################
  def countRectsInRect ( self , RECT , RECTs                               ) :
    ##########################################################################
    CNT     = 0
    ##########################################################################
    for R in RECTs                                                           :
      if               ( self . isRectInRect ( RECT , R )                  ) :
        CNT = int      ( CNT + 1                                             )
    ##########################################################################
    return CNT
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def ClassifierToFaces ( self                                             , \
                          gray                                             , \
                          scale     = 1.05                                 , \
                          neighbors = 5                                    , \
                          minsize   = ( 32 , 32 )                          ) :
    ##########################################################################
    FACEs   =         [                                                      ]
    ##########################################################################
    try                                                                      :
      ########################################################################
      FACEs = self . Classifier . detectMultiScale                           (
               gray                                                        , \
               scaleFactor  = scale                                        , \
               minNeighbors = neighbors                                    , \
               minSize      = minsize                                        )
      ########################################################################
    except                                                                   :
      pass
    ##########################################################################
    return FACEs
  ############################################################################
  def ClassifierToEyes ( self                                              , \
                         gray                                              , \
                         scale     = 1.1                                   , \
                         neighbors = 10                                    , \
                         minsize   = ( 15 , 10 )                           ) :
    ##########################################################################
    EYEs   =           [                                                     ]
    ##########################################################################
    try                                                                      :
      ########################################################################
      EYEs = self . EyesDetector . detectMultiScale                          (
               gray                                                        , \
               scaleFactor  = scale                                        , \
               minNeighbors = neighbors                                    , \
               minSize      = minsize                                        )
      ########################################################################
    except                                                                   :
      pass
    ##########################################################################
    return EYEs
  ############################################################################
  def ClassifierToMouthes ( self                                           , \
                            gray                                           , \
                            scale     = 1.1                                , \
                            neighbors = 10                                 , \
                            minsize   = ( 15 , 10 )                        ) :
    ##########################################################################
    MOUTHes   =           [                                                  ]
    ##########################################################################
    try                                                                      :
      ########################################################################
      MOUTHes = self . MouthDetector . detectMultiScale                      (
                  gray                                                     , \
                  scaleFactor  = scale                                     , \
                  minNeighbors = neighbors                                 , \
                  minSize      = minsize                                     )
      ########################################################################
    except                                                                   :
      pass
    ##########################################################################
    return MOUTHes
  ############################################################################
  def ClassifierToBoobs ( self                                             , \
                          gray                                             , \
                          scale     = 1.05                                 , \
                          neighbors = 5                                    , \
                          minsize   = ( 32 , 32 )                          ) :
    ##########################################################################
    BOOBs   =           [                                                    ]
    ##########################################################################
    try                                                                      :
      ########################################################################
      BOOBs = self . CvBoob . detectMultiScale                               (
                gray                                                       , \
                scaleFactor  = scale                                       , \
                minNeighbors = neighbors                                   , \
                minSize      = minsize                                     , \
                flags        = cv2 . CASCADE_SCALE_IMAGE                     )
      ########################################################################
    except                                                                   :
      pass
    ##########################################################################
    return BOOBs
  ############################################################################
  def DoClassifierToFaces            ( self , GRAY , OPTs                  ) :
    ##########################################################################
    FACEs = self . ClassifierToFaces ( GRAY                                  )
    ##########################################################################
    return self . CvToRectangles     ( FACEs                                 )
  ############################################################################
  def DoClassifierToEyes            ( self , GRAY , OPTs                   ) :
    ##########################################################################
    FACEs = self . ClassifierToEyes ( GRAY                                   )
    ##########################################################################
    return self . CvToRectangles    ( FACEs                                  )
  ############################################################################
  def DoClassifierToMouthes            ( self , GRAY , OPTs                ) :
    ##########################################################################
    FACEs = self . ClassifierToMouthes ( GRAY                                )
    ##########################################################################
    return self . CvToRectangles       ( FACEs                               )
  ############################################################################
  def DoClassifierToBoobs            ( self , GRAY , OPTs                  ) :
    ##########################################################################
    FACEs = self . ClassifierToBoobs ( GRAY                                  )
    ##########################################################################
    return self . CvToRectangles     ( FACEs                                 )
  ############################################################################
  def DoDlibToBoobs                  ( self , RGB , OPTs                   ) :
    ##########################################################################
    LISTs   =                        [                                       ]
    try                                                                      :
      ########################################################################
      BOOBs = self . DlibBoob        (        RGB                            )
      ########################################################################
    except                                                                   :
      return LISTs
    ##########################################################################
    if                               ( BOOBs in [ False , None           ] ) :
      return LISTs
    ##########################################################################
    CNT     = len                    ( BOOBs                                 )
    ##########################################################################
    if                               ( CNT <= 0                            ) :
      return LISTs
    ##########################################################################
    for id in range                  ( 0 , CNT                             ) :
      ########################################################################
      CRV   = self . DlibToRectangle ( BOOBs [ id ]                          )
      ########################################################################
      LISTs . append                 ( CRV                                   )
    ##########################################################################
    return LISTs
  ############################################################################
  def FoundObjectDescription ( self , IT                                   ) :
    ##########################################################################
    if                       ( "Probability" not in IT                     ) :
      return ""
    ##########################################################################
    if                       ( "Category"    not in IT                     ) :
      return ""
    ##########################################################################
    NAME = IT                [ "Category"                                    ]
    PROB = IT                [ "Probability"                                 ]
    ##########################################################################
    return f"{NAME} : {PROB}"
  ############################################################################
  def ReportClassifications ( self , ITEMs , addLog                        ) :
    ##########################################################################
    if                      ( len ( ITEMs ) <= 0                           ) :
      return
    ##########################################################################
    LISTs     =             [                                                ]
    ##########################################################################
    for IT in ITEMs                                                          :
      ########################################################################
      TEXT    = self . FoundObjectDescription ( IT                           )
      ########################################################################
      if                    ( len ( TEXT ) > 0                             ) :
        LISTs . append      ( TEXT                                           )
    ##########################################################################
    if                      ( len ( LISTs ) <= 0                           ) :
      return
    ##########################################################################
    addLog                  ("\n" . join ( LISTs )                           )
    ##########################################################################
    return
  ############################################################################
  def ReportObjects                ( self , ITEMs , addLog                 ) :
    ##########################################################################
    if                             ( len ( ITEMs ) <= 0                    ) :
      return
    ##########################################################################
    LISTs  =                       [                                         ]
    ##########################################################################
    for IC in ITEMs                                                          :
      ########################################################################
      if                           ( "Categories" not in IC                ) :
        continue
      ########################################################################
      ITs  = IC                    [ "Categories"                            ]
      self . ReportClassifications ( ITs , addLog                            )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  def CollectThings       ( self , DESC                                    ) :
    ##########################################################################
    THINGs       =        [                                                  ]
    ##########################################################################
    if                    ( "Classification" in DESC                       ) :
      ########################################################################
      for IT in DESC      [ "Classification"                               ] :
        ######################################################################
        if                ( "Category" not in IT                           ) :
          continue
        ######################################################################
        THING    = IT     [ "Category"                                       ]
        ######################################################################
        if                ( THING in THINGs                                ) :
          continue
        ######################################################################
        THINGs   . append ( THING                                            )
    ##########################################################################
    if                    ( "Objects" in DESC                              ) :
      ########################################################################
      for IC in DESC      [ "Objects"                                      ] :
        ######################################################################
        if                ( "Categories" not in IC                         ) :
          continue
        ######################################################################
        for IT in IC      [ "Categories"                                   ] :
          ####################################################################
          if              ( "Category" not in IT                           ) :
            continue
          ####################################################################
          THING  = IT     [ "Category"                                       ]
          ####################################################################
          if              ( THING in THINGs                                ) :
            continue
          ####################################################################
          THINGs . append ( THING                                            )
    ##########################################################################
    DESC [ "Things" ] = THINGs
    ##########################################################################
    return DESC
  ############################################################################
  ############################################################################
  ############################################################################
  def CalculateMeanColor ( self , PIC , MASK = None                        ) :
    ##########################################################################
    if                   ( MASK in [ False , None ]                        ) :
      M = cv2 . mean     ( PIC . toOpenCV (                                ) )
    else                                                                     :
      M = cv2 . mean     ( PIC . toOpenCV ( ) , mask = MASK                  )
    ##########################################################################
    return               { "Model" : "RGB"                                 , \
                           "Value" : "Double"                              , \
                           "R"     : float ( M [ 2 ] / 255.0 )             , \
                           "G"     : float ( M [ 1 ] / 255.0 )             , \
                           "B"     : float ( M [ 0 ] / 255.0 )               }
  ############################################################################
  def ConvertRGBtoHSV  ( self , RGB                                        ) :
    ##########################################################################
    R = int            ( RGB [ "R"                                         ] )
    G = int            ( RGB [ "G"                                         ] )
    B = int            ( RGB [ "B"                                         ] )
    I = np  . array    ( [ [ [ B , G , R ] ] ] , dtype = np . uint8          )
    M = cv2 . cvtColor ( I , cv2 . COLOR_BGR2HSV                             )
    ##########################################################################
    H = int            ( M [ 0 ] [ 0 ] [ 0                                 ] )
    S = int            ( M [ 0 ] [ 0 ] [ 1                                 ] )
    V = int            ( M [ 0 ] [ 0 ] [ 2                                 ] )
    ##########################################################################
    return             { "Model" : "HSV"                                   , \
                         "Value" : "UInt8"                                 , \
                         "H"     : H                                       , \
                         "S"     : S                                       , \
                         "V"     : V                                         }
  ############################################################################
  def ConvertHSVtoRGB  ( self , HSV                                         ) :
    ##########################################################################
    H = int            ( HSV [ "H"                                         ] )
    S = int            ( HSV [ "S"                                         ] )
    V = int            ( HSV [ "V"                                         ] )
    I = np  . array    ( [ [ [ H , S , V ] ] ] , dtype = np . uint8          )
    M = cv2 . cvtColor ( I , cv2 . COLOR_HSV2BGR                             )
    ##########################################################################
    B = int            ( M [ 0 ] [ 0 ] [ 0                                 ] )
    G = int            ( M [ 0 ] [ 0 ] [ 1                                 ] )
    R = int            ( M [ 0 ] [ 0 ] [ 2                                 ] )
    ##########################################################################
    return             { "Model" : "RGB"                                   , \
                         "Value" : "UInt8"                                 , \
                         "R"     : R                                       , \
                         "G"     : G                                       , \
                         "B"     : B                                         }
  ############################################################################
  def ConvertRGBtoYUV  ( self , RGB                                        ) :
    ##########################################################################
    R = int            ( RGB [ "R"                                         ] )
    G = int            ( RGB [ "G"                                         ] )
    B = int            ( RGB [ "B"                                         ] )
    I = np  . array    ( [ [ [ B , G , R ] ] ] , dtype = np . uint8          )
    M = cv2 . cvtColor ( I , cv2 . COLOR_BGR2YUV                             )
    ##########################################################################
    Y = int            ( M [ 0 ] [ 0 ] [ 0                                 ] )
    U = int            ( M [ 0 ] [ 0 ] [ 1                                 ] )
    V = int            ( M [ 0 ] [ 0 ] [ 2                                 ] )
    ##########################################################################
    return             { "Model" : "YUV"                                   , \
                         "Value" : "UInt8"                                 , \
                         "Y"     : Y                                       , \
                         "U"     : U                                       , \
                         "V"     : V                                         }
  ############################################################################
  def ConvertYUVtoRGB  ( self , YUV                                        ) :
    ##########################################################################
    Y = int            ( YUV [ "Y"                                         ] )
    U = int            ( YUV [ "U"                                         ] )
    V = int            ( YUV [ "V"                                         ] )
    I = np  . array    ( [ [ [ Y , U , V ] ] ] , dtype = np . uint8          )
    M = cv2 . cvtColor ( I , cv2 . COLOR_YUV2BGR                             )
    ##########################################################################
    B = int            ( M [ 0 ] [ 0 ] [ 0                                 ] )
    G = int            ( M [ 0 ] [ 0 ] [ 1                                 ] )
    R = int            ( M [ 0 ] [ 0 ] [ 2                                 ] )
    ##########################################################################
    return             { "Model" : "RGB"                                   , \
                         "Value" : "UInt8"                                 , \
                         "R"     : R                                       , \
                         "G"     : G                                       , \
                         "B"     : B                                         }
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def FindOutEyeColor ( self , HUE                                         ) :
    ##########################################################################
    global EyeColorRanges
    ##########################################################################
    HV   = int        ( HUE                                                  )
    ##########################################################################
    for CN , ( LV , UV ) in EyeColorRanges . items (                       ) :
      ########################################################################
      HL = LV         [ 0                                                    ]
      HU = UV         [ 0                                                    ]
      ########################################################################
      if              ( ( HL <= HV ) and ( HV <= HU )                      ) :
        return CN
    ##########################################################################
    return ""
  ############################################################################
  def DoLookForIrisColor                 ( self                            , \
                                           PIC                             , \
                                           ESOCKET                         , \
                                           EBALL                           , \
                                           OPTs = {                      } ) :
    ##########################################################################
    RECT = self . GetRectangleFromPoints ( ESOCKET                           )
    RRCT = self . GetRectangleFromPoints ( EBALL                             )
    ##########################################################################
    XX   = int                           ( RECT [ "X"                      ] )
    YY   = int                           ( RECT [ "Y"                      ] )
    WW   = int                           ( RECT [ "W"                      ] )
    HH   = int                           ( RECT [ "H"                      ] )
    ##########################################################################
    MW   = 16
    MH   = 16
    MK   = True
    ##########################################################################
    if                                   ( "MinimumWidth"  in OPTs         ) :
      MW = OPTs                          [ "MinimumWidth"                    ]
    ##########################################################################
    if                                   ( "MinimumHeight" in OPTs         ) :
      MH = OPTs                          [ "MinimumWidth"                    ]
    ##########################################################################
    if                                   ( WW < MW                         ) :
      MK = False
    ##########################################################################
    if                                   ( HH < MH                         ) :
      MK = False
    ##########################################################################
    if                                   ( not MK                          ) :
      return                             { "Mean"     :                  {   \
                                             "Ready"  : False            } , \
                                           "Dominant" :                  {   \
                                             "Ready"  : False            }   }
    ##########################################################################
    EPIC = PIC  . Crop                   ( XX , YY , WW , HH                 )
    EW   = EPIC . Width                  (                                   )
    EH   = EPIC . Height                 (                                   )
    MPIC = self . Create                 ( "Picture"                         )
    MPIC . CreateMask                    ( EW , EH                           )
    ##########################################################################
    CX   = RRCT                          [ "CX"                              ]
    CY   = RRCT                          [ "CY"                              ]
    CX   = int                           ( CX - XX                           )
    CY   = int                           ( CY - YY                           )
    RH   = RRCT                          [ "H"                               ]
    RH   = int                           ( RH - 4                            )
    RZ   = int                           ( RH / 2                            )
    RP   = int                           ( RH / 5                            )
    MPIC . MaskCircle                    ( CX , CY , RZ                      )
    MPIC . MaskCircle                    ( CX , CY , RP , 0                  )
    ##########################################################################
    MRPC = MPIC . MaskImage              ( EPIC                              )
    IMG  = EPIC . toOpenCV               (                                   )
    HSV  = cv2  . cvtColor               ( IMG , cv2 . COLOR_BGR2HSV         )
    M    = cv2  . mean                   ( IMG , mask = MPIC . CvMask        )
    MC   = RGBi                          ( int ( M [ 2 ]                 ) , \
                                           int ( M [ 1 ]                 ) , \
                                           int ( M [ 0 ]                 )   )
    HC   = HSVi                          (                                   )
    HC   . fromRGBi                      ( MC                                )
    CR   = float                         ( M [ 2 ] / 255.0                   )
    CG   = float                         ( M [ 1 ] / 255.0                   )
    CB   = float                         ( M [ 0 ] / 255.0                   )
    HIST = cv2  . calcHist               ( [ HSV                         ] , \
                                           [ 0                           ] , \
                                           MPIC . CvMask                   , \
                                           [ 180                         ] , \
                                           [ 0 , 180                     ]   )
    HUE  = np   . argmax                 ( HIST                              )
    MEC  = self . FindOutEyeColor        ( HC . H                            )
    DEC  = self . FindOutEyeColor        ( HUE                               )
    ##########################################################################
    return                               { "Mean"      :                 {   \
                                             "Ready"   : True              , \
                                             "RGB"     :                 {   \
                                               "Model" : "RGB"             , \
                                               "Value" : "Double"          , \
                                               "R"     : CR                , \
                                               "G"     : CG                , \
                                               "B"     : CB              } , \
                                             "HSV"     : HC . toJson (   ) , \
                                             "Name"    : MEC             } , \
                                           "Dominant"  :                 {   \
                                             "Ready"   : True              , \
                                             "Hue"     : float ( HUE )     , \
                                             "Name"    : DEC             }   }
  ############################################################################
  def DoDetectIrisColor                ( self , PIC , MESH , OPTs = { }    ) :
    ##########################################################################
    RETS = self . GetPointsByMeshIndex ( MESH ,  72                          )
    RPTS = self . GetPointsByMeshIndex ( MESH , 139                          )
    REYE = self . DoLookForIrisColor   ( PIC  , RETS , RPTS , OPTs           )
    ##########################################################################
    LETS = self . GetPointsByMeshIndex ( MESH ,  76                          )
    LPTS = self . GetPointsByMeshIndex ( MESH , 140                          )
    LEYE = self . DoLookForIrisColor   ( PIC  , LETS , LPTS , OPTs           )
    ##########################################################################
    return                             { "Right" : REYE , "Left" : LEYE      }
  ############################################################################
  def DoExtractFaceFeatures         ( self , PIC , OPTs = { }              ) :
    ##########################################################################
    IMG    = PIC  . toOpenCV        (                                        )
    GRAY   = cv2  . cvtColor        ( IMG , cv2 . COLOR_BGR2GRAY             )
    RGB    = cv2  . cvtColor        ( IMG , cv2 . COLOR_BGR2RGB              )
    WW     = PIC  . Width           (                                        )
    HH     = PIC  . Height          (                                        )
    FR     = self . CreateRectangle ( 0 , 0 , WW , HH                        )
    RT     = self . ToDlibRectangle ( FR                                     )
    ##########################################################################
    try                                                                      :
      ########################################################################
      shp  = self . Predictor       ( GRAY , RT                              )
      desc = self . Facial . compute_face_descriptor ( RGB , shp             )
      FF   = np . array             ( desc                                   )
      ########################################################################
    except                                                                   :
      ########################################################################
      return                        { "Ready" : False                        }
    ##########################################################################
    t      = 0.0
    LL     =                        [                                        ]
    ##########################################################################
    for i in range                  ( 0 , 128                              ) :
      ########################################################################
      v    = FF                     [ i                                      ]
      LL   . append                 ( v                                      )
      t   += float                  ( v * v                                  )
    ##########################################################################
    return                          { "Ready"    : True                    , \
                                      "Weights"  : t                       , \
                                      "Features" : LL                        }
  ############################################################################
  def DoDetectSimpleBody           ( self , PIC , OPTs = { }               ) :
    ##########################################################################
    IMG = PIC . toOpenCV           (                                         )
    RGB = cv2 . cvtColor           ( IMG , cv2 . COLOR_BGR2RGB               )
    WW  = PIC . Width              (                                         )
    HH  = PIC . Height             (                                         )
    ##########################################################################
    return self . GetBodyKeyPoints ( RGB , WW , HH                           )
  ############################################################################
  def DoDetectSimpleFaces             ( self , PIC , OPTs = { }            ) :
    ##########################################################################
    IMG  = PIC  . toOpenCV            (                                      )
    GRAY = cv2  . cvtColor            ( IMG , cv2 . COLOR_BGR2GRAY           )
    ##########################################################################
    return self . DoClassifierToFaces ( GRAY , OPTs                          )
  ############################################################################
  def DoDetectSimpleFaceParts             ( self , PIC , OPTs = {        } ) :
    ##########################################################################
    IMG    = PIC  . toOpenCV              (                                  )
    GRAY   = cv2  . cvtColor              ( IMG , cv2 . COLOR_BGR2GRAY       )
    ##########################################################################
    FACEs  = self . DoClassifierToFaces   ( GRAY , OPTs                      )
    EYEs   = self . DoClassifierToEyes    ( GRAY , OPTs                      )
    MOUTHs = self . DoClassifierToMouthes ( GRAY , OPTs                      )
    ##########################################################################
    return                                { "Faces"   : FACEs              , \
                                            "Eyes"    : EYEs               , \
                                            "Mouthes" : MOUTHs               }
  ############################################################################
  def DecodeDlib68Landmarks ( self , shape                                 ) :
    ##########################################################################
    Landmarks =             { "Points"    :                 [          ]   , \
                              "Rectangle" :                 {          }   , \
                              "Quality"   : int             ( 0        )   , \
                              "Shape"     :                 [          ]   , \
                              "Eyes"      : { "Right"     : [          ]   , \
                                              "RightRect" : {          }   , \
                                              "Left"      : [          ]   , \
                                              "LeftRect"  : {          } } , \
                              "Eyebrow"   : { "Right"     : [          ]   , \
                                              "RightRect" : {          }   , \
                                              "Left"      : [          ]   , \
                                              "LeftRect"  : {          } } , \
                              "Nose"      : { "Bridge"    : [          ]   , \
                                              "Exact"     : True           , \
                                              "Angle"     : 270.0          , \
                                              "Rotate"    :   0.0          , \
                                              "Nostril"   : [          ] } , \
                              "Mouth"     : { "Outer"     : [          ]   , \
                                              "OuterRect" : {          }   , \
                                              "Inner"     : [          ]   , \
                                              "InnerRect" : {          } }   }
    ##########################################################################
    XL        =  100000000000000.0
    XR        = -100000000000000.0
    YT        =  100000000000000.0
    YB        = -100000000000000.0
    ##########################################################################
    try                                                                      :
      ########################################################################
      for i in range        ( 0 , 68                                       ) :
        ######################################################################
        x     = shape.part  ( i ) . x
        y     = shape.part  ( i ) . y
        ######################################################################
        if                  ( x < XL                                       ) :
          XL  = x
        ######################################################################
        if                  ( x > XR                                       ) :
          XR  = x
        ######################################################################
        if                  ( y < YT                                       ) :
          YT  = y
        ######################################################################
        if                  ( y > YB                                       ) :
          YB  = y
        ######################################################################
        Landmarks [ "Points" ] . append ( [ x , y ]                          )
      ########################################################################
    except                                                                   :
      ########################################################################
      return                ( False , {                                  } , )
    ##########################################################################
    SW        = int         ( XR - XL + 1                                    )
    SH        = int         ( YB - YT + 1                                    )
    RT        = self . CreateRectangle ( XL , YT , SW , SH                   )
    ##########################################################################
    Landmarks [ "Rectangle" ] = RT
    ##########################################################################
    ## 臉型
    ##########################################################################
    for i in range          ( 0 , 17                                       ) :
      ########################################################################
      p       = Landmarks   [ "Points" ]          [ i                        ]
      Landmarks             [ "Shape"  ] . append ( p                        )
    ##########################################################################
    ## 計算原始臉型數據品質
    ##########################################################################
    LP        = Landmarks   [ "Shape"  ] [  0 ] [ 0                          ]
    RP        = Landmarks   [ "Shape"  ] [ 16 ] [ 0                          ]
    Quality   = int         ( RP - LP                                        )
    ##########################################################################
    if                      ( Quality < 0                                  ) :
      Quality = 0 - Quality
    ##########################################################################
    Landmarks [ "Quality"  ] = Quality
    ##########################################################################
    ## 右眉(在左邊)
    ##########################################################################
    XL        =  100000000000000.0
    XR        = -100000000000000.0
    YT        =  100000000000000.0
    YB        = -100000000000000.0
    ##########################################################################
    for i in range          ( 17 , 22                                      ) :
      ########################################################################
      p       = Landmarks   [ "Points"  ]                       [ i          ]
      ########################################################################
      x       = p           [ 0                                              ]
      y       = p           [ 0                                              ]
      ########################################################################
      if                    ( x < XL                                       ) :
        XL    = x
      ########################################################################
      if                    ( x > XR                                       ) :
        XR    = x
      ########################################################################
      if                    ( y < YT                                       ) :
        YT    = y
      ########################################################################
      if                    ( y > YB                                       ) :
        YB    = y
      ########################################################################
      Landmarks             [ "Eyebrow" ] [ "Right"  ] . append ( p          )
    ##########################################################################
    SW        = int         ( XR - XL + 1                                    )
    SH        = int         ( YB - YT + 1                                    )
    RT        = self . CreateRectangle ( XL , YT , SW , SH                   )
    ##########################################################################
    Landmarks [ "Eyebrow" ] [ "RightRect" ] = RT
    ##########################################################################
    ## 左眉(在右邊)
    ##########################################################################
    XL        =  100000000000000.0
    XR        = -100000000000000.0
    YT        =  100000000000000.0
    YB        = -100000000000000.0
    ##########################################################################
    for i in range          ( 22 , 27                                      ) :
      ########################################################################
      p       = Landmarks   [ "Points"  ]                       [ i          ]
      ########################################################################
      x       = p           [ 0                                              ]
      y       = p           [ 0                                              ]
      ########################################################################
      if                    ( x < XL                                       ) :
        XL    = x
      ########################################################################
      if                    ( x > XR                                       ) :
        XR    = x
      ########################################################################
      if                    ( y < YT                                       ) :
        YT    = y
      ########################################################################
      if                    ( y > YB                                       ) :
        YB    = y
      ########################################################################
      Landmarks             [ "Eyebrow" ] [ "Left"   ] . append ( p          )
    ##########################################################################
    SW        = int         ( XR - XL + 1                                    )
    SH        = int         ( YB - YT + 1                                    )
    RT        = self . CreateRectangle ( XL , YT , SW , SH                   )
    ##########################################################################
    Landmarks [ "Eyebrow" ] [ "LeftRect" ] = RT
    ##########################################################################
    ## 鼻樑
    ##########################################################################
    for i in range          ( 27 , 31                                      ) :
      ########################################################################
      p       = Landmarks   [ "Points" ]                        [ i          ]
      Landmarks             [ "Nose"   ] [ "Bridge"  ] . append ( p          )
    ##########################################################################
    ## 鼻孔部
    ##########################################################################
    for i in range          ( 31 , 36                                      ) :
      ########################################################################
      p       = Landmarks   [ "Points" ]                        [ i          ]
      Landmarks             [ "Nose"   ] [ "Nostril" ] . append ( p          )
    ##########################################################################
    ## 右眼(在左邊)
    ##########################################################################
    XL        =  100000000000000.0
    XR        = -100000000000000.0
    YT        =  100000000000000.0
    YB        = -100000000000000.0
    ##########################################################################
    for i in range          ( 36 , 42                                      ) :
      ########################################################################
      p       = Landmarks   [ "Points" ]                        [ i          ]
      ########################################################################
      x       = p           [ 0                                              ]
      y       = p           [ 0                                              ]
      ########################################################################
      if                    ( x < XL                                       ) :
        XL    = x
      ########################################################################
      if                    ( x > XR                                       ) :
        XR    = x
      ########################################################################
      if                    ( y < YT                                       ) :
        YT    = y
      ########################################################################
      if                    ( y > YB                                       ) :
        YB    = y
      ########################################################################
      Landmarks             [ "Eyes"   ] [ "Right"   ] . append ( p          )
    ##########################################################################
    SW        = int         ( XR - XL + 1                                    )
    SH        = int         ( YB - YT + 1                                    )
    RT        = self . CreateRectangle ( XL , YT , SW , SH                   )
    ##########################################################################
    Landmarks [ "Eyes" ] [ "RightRect" ] = RT
    ##########################################################################
    ## 左眼(在右邊)
    ##########################################################################
    XL        =  100000000000000.0
    XR        = -100000000000000.0
    YT        =  100000000000000.0
    YB        = -100000000000000.0
    ##########################################################################
    for i in range          ( 42 , 48                                      ) :
      ########################################################################
      p       = Landmarks   [ "Points" ]                        [ i          ]
      ########################################################################
      x       = p           [ 0                                              ]
      y       = p           [ 0                                              ]
      ########################################################################
      if                    ( x < XL                                       ) :
        XL    = x
      ########################################################################
      if                    ( x > XR                                       ) :
        XR    = x
      ########################################################################
      if                    ( y < YT                                       ) :
        YT    = y
      ########################################################################
      if                    ( y > YB                                       ) :
        YB    = y
      ########################################################################
      Landmarks             [ "Eyes"   ] [ "Left"    ] . append ( p          )
    ##########################################################################
    SW        = int         ( XR - XL + 1                                    )
    SH        = int         ( YB - YT + 1                                    )
    RT        = self . CreateRectangle ( XL , YT , SW , SH                   )
    ##########################################################################
    Landmarks [ "Eyes" ] [ "LeftRect" ] = RT
    ##########################################################################
    ## 外嘴唇
    ##########################################################################
    XL        =  100000000000000.0
    XR        = -100000000000000.0
    YT        =  100000000000000.0
    YB        = -100000000000000.0
    ##########################################################################
    for i in range          ( 48 , 60                                      ) :
      ########################################################################
      p       = Landmarks   [ "Points" ]                        [ i          ]
      ########################################################################
      x       = p           [ 0                                              ]
      y       = p           [ 0                                              ]
      ########################################################################
      if                    ( x < XL                                       ) :
        XL    = x
      ########################################################################
      if                    ( x > XR                                       ) :
        XR    = x
      ########################################################################
      if                    ( y < YT                                       ) :
        YT    = y
      ########################################################################
      if                    ( y > YB                                       ) :
        YB    = y
      ########################################################################
      Landmarks             [ "Mouth"  ] [ "Outer"   ] . append ( p          )
    ##########################################################################
    SW        = int         ( XR - XL + 1                                    )
    SH        = int         ( YB - YT + 1                                    )
    RT        = self . CreateRectangle ( XL , YT , SW , SH                   )
    ##########################################################################
    Landmarks [ "Eyes" ] [ "OuterRect" ] = RT
    ##########################################################################
    ## 內嘴唇
    ##########################################################################
    XL        =  100000000000000.0
    XR        = -100000000000000.0
    YT        =  100000000000000.0
    YB        = -100000000000000.0
    ##########################################################################
    for i in range          ( 60 , 68                                      ) :
      ########################################################################
      p       = Landmarks   [ "Points" ]                        [ i          ]
      ########################################################################
      x       = p           [ 0                                              ]
      y       = p           [ 0                                              ]
      ########################################################################
      if                    ( x < XL                                       ) :
        XL    = x
      ########################################################################
      if                    ( x > XR                                       ) :
        XR    = x
      ########################################################################
      if                    ( y < YT                                       ) :
        YT    = y
      ########################################################################
      if                    ( y > YB                                       ) :
        YB    = y
      ########################################################################
      Landmarks             [ "Mouth"  ] [ "Inner"   ] . append ( p          )
    ##########################################################################
    SW        = int         ( XR - XL + 1                                    )
    SH        = int         ( YB - YT + 1                                    )
    RT        = self . CreateRectangle ( XL , YT , SW , SH                   )
    ##########################################################################
    Landmarks [ "Eyes" ] [ "InnerRect" ] = RT
    ##########################################################################
    T         = Landmarks   [ "Nose" ] [ "Bridge" ] [ 0                      ]
    ## B         = Landmarks   [ "Nose" ] [ "Bridge" ] [ 1                      ]
    B         = Landmarks   [ "Nose" ] [ "Bridge" ] [ 3                      ]
    dX        = int         ( T [ 0 ] - B [ 0 ]                              )
    dY        = int         ( T [ 1 ] - B [ 1 ]                              )
    ##########################################################################
    r         = np.degrees  ( np . arctan2 ( dY , dX ) ) + 540.0
    k         = int         ( r / 360                                        )
    r         = r -         ( k * 360                                        )
    ANGLE     =             ( 360.0 - r                                      )
    ROTA      =             ( ANGLE - 270.0                                  )
    ##########################################################################
    Landmarks [ "Nose" ] [ "Angle"  ] = ANGLE
    Landmarks [ "Nose" ] [ "Rotate" ] = ROTA
    ##########################################################################
    return                  ( True , Landmarks ,                             )
  ############################################################################
  def DoDetectFaceLandmarks                ( self , PIC , OPTs = {       } ) :
    ##########################################################################
    IMG     = PIC  . toOpenCV              (                                 )
    GRAY    = cv2  . cvtColor              ( IMG , cv2 . COLOR_BGR2GRAY      )
    ##########################################################################
    FACEs   = self . DoClassifierToFaces   ( GRAY , OPTs                     )
    FCNT    = len                          ( FACEs                           )
    ##########################################################################
    if                                     ( 1 != FCNT                     ) :
      return                               { "Found" : False                 }
    ##########################################################################
    DR      = self . ToDlibRectangle       ( FACEs [ 0                     ] )
    shape   = self . Predictor             ( GRAY  , DR                      )
    OK , LM = self . DecodeDlib68Landmarks ( shape                           )
    ##########################################################################
    if                                     ( not OK                        ) :
      return                               { "Found" : False                 }
    ##########################################################################
    return                                 { "Found"     : True            , \
                                             "Landmarks" : LM                }
  ############################################################################
  def ScaleMeshPoints ( self , WW , HH , PTs                               ) :
    ##########################################################################
    ZTs   =           [                                                      ]
    ##########################################################################
    for P in PTs                                                             :
      ########################################################################
      XX  = P         [ "X"                                                  ]
      YY  = P         [ "Y"                                                  ]
      ZZ  = P         [ "Z"                                                  ]
      ########################################################################
      PX  = float     ( XX * WW                                              )
      PY  = float     ( YY * HH                                              )
      ########################################################################
      ZTs . append    ( { "X" : PX , "Y" : PY , "Z" : ZZ }                   )
    ##########################################################################
    return ZTs
  ############################################################################
  def RectangleMeshPoints ( self , RT , PTs                                ) :
    ##########################################################################
    ZTs   =               [                                                  ]
    ##########################################################################
    BX    = RT            [ "X"                                              ]
    BY    = RT            [ "Y"                                              ]
    SW    = RT            [ "W"                                              ]
    SH    = RT            [ "H"                                              ]
    ##########################################################################
    for P in PTs                                                             :
      ########################################################################
      XX  = P             [ "X"                                              ]
      YY  = P             [ "Y"                                              ]
      ZZ  = P             [ "Z"                                              ]
      ########################################################################
      SX  = float         ( XX * SW                                          )
      SY  = float         ( YY * SH                                          )
      ########################################################################
      SX  = float         ( SX + BX                                          )
      SY  = float         ( SY + BY                                          )
      ########################################################################
      ZTs . append        ( { "X" : SX , "Y" : SY , "Z" : ZZ }               )
    ##########################################################################
    return ZTs
  ############################################################################
  def GetPointsFromMeshes ( self , MESHes , INDEXes , KEY = "Pixels"       ) :
    ##########################################################################
    POINTs   =            [                                                  ]
    ##########################################################################
    for id in INDEXes                                                        :
      ########################################################################
      POINTs . append     ( MESHes [ KEY ] [ id ]                            )
    ##########################################################################
    return POINTs
  ############################################################################
  def GetPointsByMeshIndex            ( self                               , \
                                        MESHes                             , \
                                        ID                                 , \
                                        KEY = "Pixels"                     ) :
    ##########################################################################
    TOTAL = len                       ( FaceLandmarks468Meshes               )
    ##########################################################################
    if                                ( ID < 0                             ) :
      return                          [                                      ]
    ##########################################################################
    if                                ( ID >= TOTAL                        ) :
      return                          [                                      ]
    ##########################################################################
    return self . GetPointsFromMeshes ( MESHes                             , \
                                        FaceLandmarks468Meshes [ ID ]      , \
                                        KEY                                  )
  ############################################################################
  def DoDetectFaceMeshes              ( self , PIC , OPTs = { }            ) :
    ##########################################################################
    if                                ( "Region" not in OPTs               ) :
      return                          { "Ready" : False                      }
    ##########################################################################
    if                                ( "Screen" not in OPTs               ) :
      return                          { "Ready" : False                      }
    ##########################################################################
    STATIC          = True
    FACEs           = 1
    REFINE          = True
    MinConfidence   = 0.5
    ##########################################################################
    if                                ( "Static"     in OPTs               ) :
      STATIC        = OPTs            [ "Static"                             ]
    ##########################################################################
    if                                ( "Faces"      in OPTs               ) :
      FACEs         = OPTs            [ "Faces"                              ]
    ##########################################################################
    if                                ( "Refine"     in OPTs               ) :
      REFINE        = OPTs            [ "Refine"                             ]
    ##########################################################################
    if                                ( "Confidence" in OPTs               ) :
      MinConfidence = OPTs            [ "Confidence"                         ]
    ##########################################################################
    IMG             = PIC . toOpenCV  (                                      )
    RGB             = cv2 . cvtColor  ( IMG , cv2 . COLOR_BGR2RGB            )
    WW              = PIC . Width     (                                      )
    HH              = PIC . Height    (                                      )
    ##########################################################################
    FM              = mediapipe . solutions . face_mesh
    FD              = FM . FaceMesh                                        ( \
                        static_image_mode        = STATIC                  , \
                        max_num_faces            = FACEs                   , \
                        refine_landmarks         = REFINE                  , \
                        min_detection_confidence = MinConfidence             )
    ##########################################################################
    try                                                                      :
      ########################################################################
      RR            = FD . process    ( RGB                                  )
      ########################################################################
    except                                                                   :
      return                          { "Ready" : False                      }
    ##########################################################################
    if                                ( not RR . multi_face_landmarks      ) :
      return                          { "Ready" : False                      }
    ##########################################################################
    CNT             = len             ( RR . multi_face_landmarks            )
    ##########################################################################
    if                                ( 1 != CNT                           ) :
      return                          { "Ready" : False                      }
    ##########################################################################
    BX              = OPTs            [ "Screen" ] [ "X"                     ]
    BY              = OPTs            [ "Screen" ] [ "Y"                     ]
    SW              = OPTs            [ "Screen" ] [ "W"                     ]
    SH              = OPTs            [ "Screen" ] [ "H"                     ]
    ##########################################################################
    LL              =                 [                                      ]
    PL              =                 [                                      ]
    SL              =                 [                                      ]
    ##########################################################################
    for F in RR . multi_face_landmarks                                       :
      ########################################################################
      for P in F . landmark                                                  :
        ######################################################################
        XX          = float           ( P  . x                               )
        YY          = float           ( P  . y                               )
        ZZ          = float           ( P  . z                               )
        ######################################################################
        PX          = float           ( XX * WW                              )
        PY          = float           ( YY * HH                              )
        ######################################################################
        SX          = float           ( XX * SW                              )
        SY          = float           ( YY * SH                              )
        ######################################################################
        SX          = float           ( SX + BX                              )
        SY          = float           ( SY + BY                              )
        ######################################################################
        LL          . append          ( { "X" : XX , "Y" : YY , "Z" : ZZ }   )
        PL          . append          ( { "X" : PX , "Y" : PY , "Z" : ZZ }   )
        SL          . append          ( { "X" : SX , "Y" : SY , "Z" : ZZ }   )
    ##########################################################################
    if                                ( len ( LL ) <= 0                    ) :
      return                          { "Ready" : False                      }
    ##########################################################################
    return                            { "Ready"    : True                  , \
                                        "Width"    : WW                    , \
                                        "Height"   : HH                    , \
                                        "X"        : BX                    , \
                                        "Y"        : BY                    , \
                                        "SW"       : SW                    , \
                                        "SH"       : SH                    , \
                                        "Region"   : OPTs [ "Region" ]     , \
                                        "Screen"   : OPTs [ "Screen" ]     , \
                                        "Original" : LL                    , \
                                        "Pixels"   : PL                    , \
                                        "Draws"    : SL                      }
  ############################################################################
  def DoDetectSimpleBoobs             ( self , PIC , OPTs = { }            ) :
    ##########################################################################
    IMG  = PIC  . toOpenCV            (                                      )
    GRAY = cv2  . cvtColor            ( IMG , cv2 . COLOR_BGR2GRAY           )
    ##########################################################################
    return self . DoClassifierToBoobs ( GRAY , OPTs                          )
  ############################################################################
  def DoDetectSimpleDlibBoobs   ( self , PIC , OPTs = { }                  ) :
    ##########################################################################
    IMG  = PIC  . toOpenCV      (                                            )
    IRGB = cv2  . cvtColor      ( IMG , cv2 . COLOR_BGR2RGB                  )
    ##########################################################################
    return self . DoDlibToBoobs ( IRGB , OPTs                                )
  ############################################################################
  def DoDetectAllBoobs                   ( self , PIC , OPTs = { }         ) :
    ##########################################################################
    IMG     = PIC  . toOpenCV            (                                   )
    GRAY    = cv2  . cvtColor            ( IMG , cv2 . COLOR_BGR2GRAY        )
    IRGB    = cv2  . cvtColor            ( IMG , cv2 . COLOR_BGR2RGB         )
    ##########################################################################
    BOOBs   = self . DoClassifierToBoobs ( GRAY , OPTs                       )
    BOOBz   = self . DoDlibToBoobs       ( IRGB , OPTs                       )
    ##########################################################################
    for B in BOOBz                                                           :
      BOOBs . append                     ( B                                 )
    ##########################################################################
    return BOOBs
  ############################################################################
  def DoBasicDescription                  ( self , PIC , INFO , OPTs       ) :
    ##########################################################################
    global RVERSION
    ##########################################################################
    try                                                                      :
      ########################################################################
      J    =                              { "Information" : INFO             }
      IMG  = PIC  . toOpenCV              (                                  )
      GRAY = cv2  . cvtColor              ( IMG , cv2 . COLOR_BGR2GRAY       )
      IRGB = cv2  . cvtColor              ( IMG , cv2 . COLOR_BGR2RGB        )
      MRGB = self . CvToMediaPipeImage    ( IRGB                             )
      ########################################################################
    except                                                                   :
      return                              {                                  }
    ##########################################################################
    WW     = PIC  . Width                 (                                  )
    HH     = PIC  . Height                (                                  )
    ##########################################################################
    FACEs  = self . DoClassifierToFaces   ( GRAY , OPTs                      )
    EYEs   = self . DoClassifierToEyes    ( GRAY , OPTs                      )
    MOUTHs = self . DoClassifierToMouthes ( GRAY , OPTs                      )
    BOOBs  = self . DoClassifierToBoobs   ( GRAY , OPTs                      )
    BOOBz  = self . DoDlibToBoobs         ( IRGB , OPTs                      )
    ##########################################################################
    D      =                              { "Faces"      :               {   \
                                              "Total"    : len ( FACEs   ) , \
                                              "Listings" :       FACEs   } , \
                                            "Eyes"       :               {   \
                                              "Total"    : len ( EYEs    ) , \
                                              "Listings" :       EYEs    } , \
                                            "Mouthes"    :               {   \
                                              "Total"    : len ( MOUTHs  ) , \
                                              "Listings" :       MOUTHs  } , \
                                            "Boobs"      :               {   \
                                              "Total"    : len ( BOOBs   ) , \
                                              "Listings" :       BOOBs   } , \
                                            "DlibBoobs"  :               {   \
                                              "Total"    : len ( BOOBz   ) , \
                                              "Listings" :       BOOBz   }   }
    ##########################################################################
    BODYs  = self . GetBodyKeyPoints      ( IRGB , WW , HH                   )
    ##########################################################################
    CTRIG  = self . Settings [ "Classifier" ] [ "Probability"                ]
    OTRIG  = self . Settings [ "Objectron"  ] [ "Probability"                ]
    ##########################################################################
    ITEMs  = self . Classification        ( MRGB , CTRIG                     )
    OBJs   = self . ObjectDetection       ( MRGB , OTRIG                     )
    ##########################################################################
    NOW    = StarDate                     (                                  )
    NOW    . Now                          (                                  )
    CDT    = NOW . Stardate
    ##########################################################################
    B      =                              { "Classification" : ITEMs       , \
                                            "Objects"        : OBJs        , \
                                            "Skeletons"      : BODYs       , \
                                            "Body"           : D             }
    B      = self . CollectThings         ( B                                )
    ##########################################################################
    J      =                              { "Foundation"     : True        , \
                                            "Version"        : RVERSION    , \
                                            "Timestamp"      : CDT         , \
                                            "Description"    : B             }
    ##########################################################################
    return J
  ############################################################################
  def hasFaces         ( self , INFO                                       ) :
    ##########################################################################
    if                 ( INFO in [ False , None ]                          ) :
      return False
    ##########################################################################
    if                 ( "Description" not in INFO                         ) :
      return False
    ##########################################################################
    JJJ   = INFO       [ "Description"                                       ]
    if                 ( "Body"        not in JJJ                          ) :
      return False
    ##########################################################################
    JJJ   = JJJ        [ "Body"                                              ]
    if                 ( "Faces"       not in JJJ                          ) :
      return False
    ##########################################################################
    KKK   = JJJ        [ "Faces"                                             ]
    if                 ( "Total"       not in KKK                          ) :
      return False
    ##########################################################################
    KKK   = JJJ        [ "Mouthes"                                           ]
    if                 ( "Total"       not in KKK                          ) :
      return False
    ##########################################################################
    KKK   = JJJ        [ "Eyes"                                              ]
    if                 ( "Total"       not in KKK                          ) :
      return False
    ##########################################################################
    KKK   = JJJ        [ "Faces"                                             ]
    TOTAL = KKK        [ "Total"                                             ]
    ##########################################################################
    if                 ( TOTAL <= 0                                        ) :
      return False
    ##########################################################################
    KKK   = JJJ        [ "Mouthes"                                           ]
    TOTAL = KKK        [ "Total"                                             ]
    ##########################################################################
    if                 ( TOTAL <= 0                                        ) :
      return False
    ##########################################################################
    KKK   = JJJ        [ "Eyes"                                              ]
    TOTAL = KKK        [ "Total"                                             ]
    ##########################################################################
    if                 ( TOTAL <= 0                                        ) :
      return False
    ##########################################################################
    KKK   = JJJ        [ "Faces"                                             ]
    FACEs = KKK        [ "Listings"                                          ]
    ##########################################################################
    KKK   = JJJ        [ "Mouthes"                                           ]
    MOUTH = KKK        [ "Listings"                                          ]
    ##########################################################################
    KKK   = JJJ        [ "Eyes"                                              ]
    EYEs  = KKK        [ "Listings"                                          ]
    ##########################################################################
    for F in FACEs                                                           :
      ########################################################################
      W   = F          [ "W"                                                 ]
      H   = F          [ "H"                                                 ]
      ########################################################################
      if               ( W < 128                                           ) :
        continue
      ########################################################################
      if               ( H < 128                                           ) :
        continue
      ########################################################################
      MM  = self . hasRectsInRect   ( F , MOUTH                              )
      ########################################################################
      if               ( not MM                                            ) :
        return False
      ########################################################################
      EE  = self . countRectsInRect ( F , EYEs                               )
      ########################################################################
      if               ( EE < 2                                            ) :
        return False
      ########################################################################
      return   True
    ##########################################################################
    return     False
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
