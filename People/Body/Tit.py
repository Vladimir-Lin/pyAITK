# -*- coding: utf-8 -*-
##############################################################################
## 乳頭
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
##############################################################################
class Tit         (                                                        ) :
  ############################################################################
  def __init__    ( self                                                   ) :
    ##########################################################################
    self . Classifier = None
    self . Detector   = None
    ##########################################################################
    ## self . Detector ( IMG )
    ##########################################################################
    return
  ############################################################################
  def __del__     ( self                                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def ToBoobs                      ( self                                  , \
                                     gray                                  , \
                                     scale     = 1.05                      , \
                                     neighbors = 5                         , \
                                     minsize   = ( 32 , 32 )               ) :
    return self . Classifier . detectMultiScale                              (
             gray                                                          , \
             scaleFactor  = scale                                          , \
             minNeighbors = neighbors                                      , \
             minSize      = minsize                                        , \
             flags        = cv2 . cv . CV_HAAR_SCALE_IMAGE                   )
  ############################################################################
  def ToDlibBoobs          ( self , image                                  ) :
    return self . Detector (        image                                    )
##############################################################################
