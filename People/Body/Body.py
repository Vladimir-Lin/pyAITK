# -*- coding: utf-8 -*-
##############################################################################
## 人體
##############################################################################
import os
import sys
import time
import datetime
import logging
import requests
import threading
import gettext
import binascii
import hashlib
import base64
import glob
##############################################################################
from   io           import BytesIO
from   wand . image import Image
from   PIL          import Image as Pillow
##############################################################################
import cv2
import dlib
import skimage
import numpy        as np
import mediapipe    as mp
##############################################################################
"""
int	LEFT_ANKLE	The landmark which corresponds to the left ankle.
int	LEFT_EAR	The landmark which corresponds to the left ear.
int	LEFT_ELBOW	The landmark which corresponds to the left elbow.
int	LEFT_EYE	The landmark which corresponds to the left eye.
int	LEFT_EYE_INNER	The landmark which corresponds to the inner left eye.

int	LEFT_EYE_OUTER	The landmark which corresponds to the outer left eye.
int	LEFT_FOOT_INDEX	The landmark which corresponds to the left foot index.
int	LEFT_HEEL	The landmark which corresponds to the left heel.
int	LEFT_HIP	The landmark which corresponds to the left hip.
int	LEFT_INDEX	The landmark which corresponds to the left index finger.

int	LEFT_KNEE	The landmark which corresponds to the left knee.
int	MOUTH_LEFT	The landmark which corresponds to the left mouth.
int	LEFT_PINKY	The landmark which corresponds to the left pinky.
int	LEFT_SHOULDER	The landmark which corresponds to the left shoulder.
int	LEFT_THUMB	The landmark which corresponds to the left thumb.
int	LEFT_WRIST	The landmark which corresponds to the left wrist.

int	NOSE	The landmark which corresponds to the nose.

int	RIGHT_ANKLE	The landmark which corresponds to the right ankle.
int	RIGHT_EAR	The landmark which corresponds to the right ear.
int	RIGHT_ELBOW	The landmark which corresponds to the right elbow.
int	RIGHT_EYE	The landmark which corresponds to the left eye.
int	RIGHT_EYE_INNER	The landmark which corresponds to the inner left eye.

int	RIGHT_EYE_OUTER	The landmark which corresponds to the outer left eye.
int	RIGHT_FOOT_INDEX	The landmark which corresponds to the right foot index.
int	RIGHT_HEEL	The landmark which corresponds to the right heel.
int	RIGHT_HIP	The landmark which corresponds to the right hip.
int	RIGHT_INDEX	The landmark which corresponds to the right index finger.

int	RIGHT_KNEE	The landmark which corresponds to the right knee.
int	MOUTH_RIGHT	The landmark which corresponds to the right mouth.
int	RIGHT_PINKY	The landmark which corresponds to the right pinky.
int	RIGHT_SHOULDER	The landmark which corresponds to the right shoulder.
int	RIGHT_THUMB	The landmark which corresponds to the right thumb.
int	RIGHT_WRIST	The landmark which corresponds to the right wrist.
"""
##############################################################################
class Body        (                                                        ) :
  ############################################################################
  def __init__    ( self                                                   ) :
    ##########################################################################
    self . mpPose = mp   . solutions . pose
    self . Pose   = self . mpPose    . Pose (                                )
    ##########################################################################
    return
  ############################################################################
  def __del__     ( self                                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def ParseCoordinate ( self , KEYs , ITEM , W , H                         ) :
    ##########################################################################
    X = int           ( KEYs . landmark [ ITEM ] . x * W                     )
    Y = int           ( KEYs . landmark [ ITEM ] . y * H                     )
    ##########################################################################
    return            { "X" : X , "Y" : Y                                    }
  ############################################################################
  def GetBodyKeyPoints              ( self , Image , W , H                 ) :
    ##########################################################################
    J     =                         { "Nose"  : { }                        , \
                                      "Left"  : { }                        , \
                                      "Right" : { }                          }
    ##########################################################################
    MPX   = self . mpPose . PoseLandmark
    KPS   = self . Pose   . process (        Image                           )
    KPL   = KPS  . pose_landmarks
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
    return J
##############################################################################
