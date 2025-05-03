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
##############################################################################
import mediapipe
from   mediapipe . tasks          import python
from   mediapipe . tasks . python import vision
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
  def RectToXYWH ( self , rect                                             ) :
    ##########################################################################
    x = rect     [ "X"                                                       ]
    y = rect     [ "Y"                                                       ]
    w = rect     [ "W"                                                       ]
    h = rect     [ "H"                                                       ]
    ##########################################################################
    return       ( x , y , w , h ,                                           )
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
  ############################################################################
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
    return self . Classifier . detectMultiScale                              (
             gray                                                          , \
             scaleFactor  = scale                                          , \
             minNeighbors = neighbors                                      , \
             minSize      = minsize                                          )
  ############################################################################
  def ClassifierToEyes ( self                                              , \
                         gray                                              , \
                         scale     = 1.1                                   , \
                         neighbors = 10                                    , \
                         minsize   = ( 15 , 10 )                           ) :
    return self . EyesDetector . detectMultiScale                            (
             gray                                                          , \
             scaleFactor  = scale                                          , \
             minNeighbors = neighbors                                      , \
             minSize      = minsize                                          )
  ############################################################################
  def ClassifierToMouthes ( self                                           , \
                            gray                                           , \
                            scale     = 1.1                                , \
                            neighbors = 10                                 , \
                            minsize   = ( 15 , 10 )                        ) :
    return self . MouthDetector . detectMultiScale                           (
             gray                                                          , \
             scaleFactor  = scale                                          , \
             minNeighbors = neighbors                                      , \
             minSize      = minsize                                          )
  ############################################################################
  def ClassifierToBoobs ( self                                             , \
                          gray                                             , \
                          scale     = 1.05                                 , \
                          neighbors = 5                                    , \
                          minsize   = ( 32 , 32 )                          ) :
    return self . CvBoob . detectMultiScale                                  (
             gray                                                          , \
             scaleFactor  = scale                                          , \
             minNeighbors = neighbors                                      , \
             minSize      = minsize                                        , \
             flags        = cv2 . CASCADE_SCALE_IMAGE                        )
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
    BOOBs   = self . DlibBoob        (        RGB                            )
    LISTs   =                        [                                       ]
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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def DoBasicDescription                  ( self , PIC , INFO , OPTs       ) :
    ##########################################################################
    global RVERSION
    ##########################################################################
    J      =                              { "Information" : INFO             }
    IMG    = PIC  . toOpenCV              (                                  )
    GRAY   = cv2  . cvtColor              ( IMG , cv2 . COLOR_BGR2GRAY       )
    IRGB   = cv2  . cvtColor              ( IMG , cv2 . COLOR_BGR2RGB        )
    MRGB   = self . CvToMediaPipeImage    ( IRGB                             )
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
    B      =                              { "Classification" : ITEMs       , \
                                            "Objects"        : OBJs        , \
                                            "Skeletons"      : BODYs       , \
                                            "Body"           : D             }
    ##########################################################################
    J      =                              { "Foundation"     : True        , \
                                            "Version"        : RVERSION    , \
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
    JJJ   = JJJ        [ "Faces"                                             ]
    if                 ( "Total"       not in JJJ                          ) :
      return False
    ##########################################################################
    TOTAL = JJJ        [ "Total"                                             ]
    ##########################################################################
    if                 ( TOTAL > 0                                         ) :
      return True
    ##########################################################################
    return   False
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
