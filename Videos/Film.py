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
import AITK
##############################################################################
from   AITK . Database   . Query          import Query
from   AITK . Database   . Connection     import Connection
from   AITK . Database   . Pair           import Pair
from   AITK . Database   . Columns        import Columns
##############################################################################
from   AITK . Documents  . Name           import Name           as NameItem
from   AITK . Documents  . Name           import Naming         as Naming
from   AITK . Documents  . Notes          import Notes          as NoteItem
from   AITK . Documents  . Variables      import Variables      as VariableItem
from   AITK . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK . Calendars  . StarDate       import StarDate       as StarDate
from   AITK . Calendars  . Periode        import Periode        as Periode
from   AITK . Essentials . Relation       import Relation       as Relation
##############################################################################
class Film               ( Columns                                         ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    self      . Clear    (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def Clear             ( self                                             ) :
    ##########################################################################
    self . Columns    = [                                                    ]
    self . Details    = {                                                    }
    self . Id         = 0
    self . Uuid       = 0
    self . Used       = 0
    self . VType      = 0
    self . Name       = ""
    self . Path       = ""
    self . FileSize   = 0
    self . Duration   = 0
    self . Width      = 0
    self . Height     = 0
    self . Frames     = 0
    self . Format     = ""
    self . FPS        = ""
    self . vCodec     = ""
    self . vBitRate   = 0
    self . aCodec     = ""
    self . SampleRate = 0
    self . aBitRate   = 0
    self . ltime      = 0
    ##########################################################################
    return
  ############################################################################
  def assign ( self , item                                                 ) :
    ##########################################################################
    self . Columns    = item . Columns
    self . Details    = item . Details
    self . Id         = item . Id
    self . Uuid       = item . Uuid
    self . Used       = item . Used
    self . VType      = item . VType
    self . Name       = item . Name
    self . Path       = item . Path
    self . FileSize   = item . FileSize
    self . Duration   = item . Duration
    self . Width      = item . Width
    self . Height     = item . Height
    self . Frames     = item . Frames
    self . Format     = item . Format
    self . FPS        = item . FPS
    self . vCodec     = item . vCodec
    self . vBitRate   = item . vBitRate
    self . aCodec     = item . aCodec
    self . SampleRate = item . SampleRate
    self . aBitRate   = item . aBitRate
    self . ltime      = item . ltime
    ##########################################################################
    return
  ############################################################################
  def set            ( self , item , value                                 ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"         == a                                   ) :
      self . Id     = value
    ##########################################################################
    if               ( "uuid"       == a                                   ) :
      self . Uuid   = value
    ##########################################################################
    if               ( "used"       == a                                   ) :
      self . Used   = value
    ##########################################################################
    if               ( "type"       == a                                   ) :
      self . VType  = value
    ##########################################################################
    if               ( "filesize"   == a                                   ) :
      self . FileSize  = value
    ##########################################################################
    if               ( "duration"   == a                                   ) :
      self . Duration  = value
    ##########################################################################
    if               ( "width"      == a                                   ) :
      self . Width = value
    ##########################################################################
    if               ( "height"     == a                                   ) :
      self . Height = value
    ##########################################################################
    if               ( "frames"     == a                                   ) :
      self . Frames = value
    ##########################################################################
    if               ( "format"     == a                                   ) :
      self . Format = value
    ##########################################################################
    if               ( "fps"        == a                                   ) :
      self . FPS = value
    ##########################################################################
    if               ( "vcodec"     == a                                   ) :
      self . vCodec = value
    ##########################################################################
    if               ( "vbitrate"   == a                                   ) :
      self . vBitRate = value
    ##########################################################################
    if               ( "acodec"     == a                                   ) :
      self . aCodec = value
    ##########################################################################
    if               ( "samplerate" == a                                   ) :
      self . SampleRate = value
    ##########################################################################
    if               ( "abitrate"   == a                                   ) :
      self . aBitRate = value
    ##########################################################################
    if               ( "ltime"      == a                                   ) :
      self . ltime  = value
    ##########################################################################
    return
  ############################################################################
  def get            ( self , item                                         ) :
    ##########################################################################
    a = item . lower (                                                       )
    ##########################################################################
    if               ( "id"         == a                                   ) :
      return self . Id
    ##########################################################################
    if               ( "uuid"       == a                                   ) :
      return self . Uuid
    ##########################################################################
    if               ( "used"       == a                                   ) :
      return self . Used
    ##########################################################################
    if               ( "type"       == a                                   ) :
      return self . VType
    ##########################################################################
    if               ( "filesize"   == a                                   ) :
      return self . FileSize
    ##########################################################################
    if               ( "duration"   == a                                   ) :
      return self . Duration
    ##########################################################################
    if               ( "width"      == a                                   ) :
      return self . Width
    ##########################################################################
    if               ( "height"     == a                                   ) :
      return self . Height
    ##########################################################################
    if               ( "frames"     == a                                   ) :
      return self . Frames
    ##########################################################################
    if               ( "format"     == a                                   ) :
      return self . Format
    ##########################################################################
    if               ( "fps"        == a                                   ) :
      return self . FPS
    ##########################################################################
    if               ( "vcodec"     == a                                   ) :
      return self . vCodec
    ##########################################################################
    if               ( "vbitrate"   == a                                   ) :
      return self . vBitRate
    ##########################################################################
    if               ( "acodec"     == a                                   ) :
      return self . aCodec
    ##########################################################################
    if               ( "samplerate" == a                                   ) :
      return self . SampleRate
    ##########################################################################
    if               ( "abitrate"   == a                                   ) :
      return self . aBitRate
    ##########################################################################
    if               ( "ltime"      == a                                   ) :
      return self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems        ( self                                             ) :
    return [ "id"                                                            ,
             "uuid"                                                          ,
             "used"                                                          ,
             "type"                                                          ,
             "filesize"                                                      ,
             "duration"                                                      ,
             "width"                                                         ,
             "height"                                                        ,
             "frames"                                                        ,
             "format"                                                        ,
             "fps"                                                           ,
             "vcodec"                                                        ,
             "vbitrate"                                                      ,
             "acodec"                                                        ,
             "samplerate"                                                    ,
             "abitrate"                                                      ,
             "ltime"                                                         ]
  ############################################################################
  def pair              ( self , item                                      ) :
    v = self . get      (        item                                        )
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems        ( self                                             ) :
    return [ "used"                                                          ,
             "type"                                                          ,
             "filesize"                                                      ,
             "duration"                                                      ,
             "width"                                                         ,
             "height"                                                        ,
             "frames"                                                        ,
             "format"                                                        ,
             "fps"                                                           ,
             "vcodec"                                                        ,
             "vbitrate"                                                      ,
             "acodec"                                                        ,
             "samplerate"                                                    ,
             "abitrate"                                                      ]
  ############################################################################
  def toJson            ( self                                             ) :
    return              { "Id"         : self . Id                         , \
                          "Uuid"       : self . Uuid                       , \
                          "Used"       : self . Used                       , \
                          "Type"       : self . VType                      , \
                          "Name"       : self . Name                       , \
                          "Path"       : self . Path                       , \
                          "FileSize"   : self . FileSize                   , \
                          "Duration"   : self . Duration                   , \
                          "Width"      : self . Width                      , \
                          "Height"     : self . Height                     , \
                          "Frames"     : self . Frames                     , \
                          "Format"     : self . Format                     , \
                          "FPS"        : self . FPS                        , \
                          "vCodec"     : self . vCodec                     , \
                          "vBitRate"   : self . vBitRate                   , \
                          "aCodec"     : self . aCodec                     , \
                          "SampleRate" : self . SampleRate                 , \
                          "aBitRate"   : self . aBitRate                   , \
                          "Details"    : self . Details                      }
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
  ## 指定檔案路徑
  ############################################################################
  def setPath                   ( self , FilePath                          ) :
    ##########################################################################
    EXT           = pathlib . Path ( FilePath ) . suffix
    ##########################################################################
    if                          ( "." in EXT                               ) :
      ########################################################################
      EXT         = EXT         [ 1 :                                        ]
    ##########################################################################
    self . Path   = FilePath
    self . Format = EXT . lower (                                            )
    ##########################################################################
    return
  ############################################################################
  def Parse                       ( self , name , details                  ) :
    ##########################################################################
    self . Name               = name
    self . Details            = details
    self . Details [ "Name" ] = name
    ##########################################################################
    try                                                                      :
      ########################################################################
      DURF            = float     ( details [ "format" ] [ "duration"      ] )
      self . Duration = int       ( DURF * 1000000                           )
      self . FileSize = int       ( details [ "format" ] [ "size"          ] )
      ########################################################################
      FN              = str       ( details [ "format" ] [ "filename"      ] )
      self . setPath              ( FN                                       )
      ########################################################################
      for S in details            [ "streams"                              ] :
        ######################################################################
        if                        ( "video" == S [ "codec_type" ]          ) :
          ####################################################################
          self . Width      = str ( S [ "width"                            ] )
          self . Height     = str ( S [ "height"                           ] )
          self . vCodec     = str ( S [ "codec_name"                       ] )
          self . FPS        = str ( S [ "r_frame_rate"                     ] )
          self . Frames     = int ( S [ "nb_frames" ]                        )
          self . vBitRate   = int ( S [ "bit_rate"  ]                        )
          ####################################################################
        elif                      ( "audio" == S [ "codec_type" ]          ) :
          ####################################################################
          self . aCodec     = str ( S [ "codec_name"  ]                      )
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
##############################################################################
