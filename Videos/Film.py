# -*- coding: utf-8 -*-
##############################################################################
## 影片資訊
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
import pathlib
import ffmpeg
##############################################################################
from   AITK  . Database   . Connection     import Connection     as Connection
##############################################################################
from   AITK  . Documents  . Name           import Name           as NameItem
from   AITK  . Documents  . Name           import Naming         as Naming
from   AITK  . Documents  . Notes          import Notes          as NoteItem
from   AITK  . Documents  . Variables      import Variables      as VariableItem
from   AITK  . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK  . Calendars  . StarDate       import StarDate       as StarDate
from   AITK  . Calendars  . Periode        import Periode        as Periode
from   AITK  . Essentials . Relation       import Relation       as Relation
##############################################################################
class Film               (                                                 ) :
  ############################################################################
  def __init__          ( self                                             ) :
    ##########################################################################
    self . Details    = {                                                    }
    self . Uuid       = 0
    self . Name       = ""
    self . Path       = ""
    self . Format     = ""
    self . Duration   = 0
    self . FileSize   = 0
    self . Width      = 0
    self . Height     = 0
    self . vCodec     = ""
    self . FPS        = ""
    self . Frames     = 0
    self . vBitRate   = 0
    self . aCodec     = ""
    self . SampleRate = 0
    self . aBitRate   = 0
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def Probe                 ( self , Filename                              ) :
    ##########################################################################
    try                                                                      :
      return ffmpeg . probe ( Filename                                       )
    except                                                                   :
      pass
    ##########################################################################
    return                  {                                                }
  ############################################################################
  def Parse ( self , name , details                                        ) :
    ##########################################################################
    self . Name               = name
    self . Details            = details
    self . Details [ "Name" ] = name
    ##########################################################################
    try                                                                      :
      ########################################################################

      ########################################################################
      DURF            = float   ( details [ "format" ] [ "duration" ]        )
      self . Duration = int     ( DURF * 1000000                             )
      self . FileSize = details [ "format" ] [ "size"                        ]
      ########################################################################
      FN              = details [ "format" ] [ "filename"                    ]
      EXT             = pathlib . Path ( FN ) . suffix
      ########################################################################
      if                        ( "." in EXT                               ) :
        ######################################################################
        EXT           = EXT     [ 1 :                                        ]
      ########################################################################
      self . Format   = EXT . lower    (                                     )
      ########################################################################
      for S in details [ "streams" ]                                         :
        ######################################################################
        if                      ( "video" == S [ "codec_type" ]            ) :
          ####################################################################
          self . Width      = S [ "width"                                    ]
          self . Height     = S [ "height"                                   ]
          self . vCodec     = S [ "codec_name"                               ]
          self . FPS        = S [ "r_frame_rate"                             ]
          self . Frames     = int ( S [ "nb_frames" ]                        )
          self . vBitRate   = int ( S [ "bit_rate"  ]                        )
          ####################################################################
        elif                    ( "audio" == S [ "codec_type" ]            ) :
          ####################################################################
          self . aCodec     =       S [ "codec_name"                         ]
          self . SampleRate = int ( S [ "sample_rate" ]                      )
          self . aBitRate   = int ( S [ "bit_rate"    ]                      )
      ########################################################################
    except                                                                   :
      ########################################################################
      self . Format     = ""
      self . Duration   = 0
      self . FileSize   = 0
      self . Width      = 0
      self . Height     = 0
      self . vCodec     = ""
      self . FPS        = ""
      self . Frames     = 0
      self . vBitRate   = 0
      self . aCodec     = ""
      self . SampleRate = 0
      self . aBitRate   = 0
      ########################################################################
      return False
    ##########################################################################
    return True
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
