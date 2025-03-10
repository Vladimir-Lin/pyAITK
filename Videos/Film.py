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
import subprocess
import binascii
import hashlib
import re
import base64
import json
import pathlib
##############################################################################
import AITK
##############################################################################
from   AITK . Database   . Query          import Query
from   AITK . Database   . Connection     import Connection
from   AITK . Database   . Pair           import Pair
from   AITK . Database   . Columns        import Columns
##############################################################################
from   AITK . Documents  . JSON           import Load           as LoadJson
from   AITK . Documents  . JSON           import Save           as SaveJson
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
    self . Settings   = {                                                    }
    self . Tables     = {                                                    }
    self . Groups     = [                                                    ]
    self . SQLs       = [                                                    ]
    ##########################################################################
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
                          "Signature"  : self . toSignature ( )            , \
                          "Details"    : self . Details                      }
  ############################################################################
  def fromJson ( self , JSOX                                               ) :
    ##########################################################################
    self . Id         = JSOX [ "Id"                                          ]
    self . Uuid       = JSOX [ "Uuid"                                        ]
    self . Used       = JSOX [ "Used"                                        ]
    self . VType      = JSOX [ "Type"                                        ]
    self . Name       = JSOX [ "Name"                                        ]
    self . Path       = JSOX [ "Path"                                        ]
    self . FileSize   = JSOX [ "FileSize"                                    ]
    self . Duration   = JSOX [ "Duration"                                    ]
    self . Width      = JSOX [ "Width"                                       ]
    self . Height     = JSOX [ "Height"                                      ]
    self . Frames     = JSOX [ "Frames"                                      ]
    self . Format     = JSOX [ "Format"                                      ]
    self . FPS        = JSOX [ "FPS"                                         ]
    self . vCodec     = JSOX [ "vCodec"                                      ]
    self . vBitRate   = JSOX [ "vBitRate"                                    ]
    self . aCodec     = JSOX [ "aCodec"                                      ]
    self . SampleRate = JSOX [ "SampleRate"                                  ]
    self . aBitRate   = JSOX [ "aBitRate"                                    ]
    self . Details    = JSOX [ "Details"                                     ]
    ##########################################################################
    return
  ############################################################################
  def toSignature ( self                                                   ) :
    ##########################################################################
    LN = self . Duration
    FS = self . FileSize
    FP = self . FPS
    WW = self . Width
    HH = self . Height
    ##########################################################################
    return f"{LN}:{FS}:{FP}:{WW}:{HH}"
  ############################################################################
  def isEquivalent ( self , ITEM                                           ) :
    ##########################################################################
    if             ( self . VType      != ITEM . VType                     ) :
      return False
    ##########################################################################
    if             ( self . FileSize   != ITEM . FileSize                  ) :
      return False
    ##########################################################################
    if             ( self . Duration   != ITEM . Duration                  ) :
      return False
    ##########################################################################
    if             ( self . Width      != ITEM . Width                     ) :
      return False
    ##########################################################################
    if             ( self . Height     != ITEM . Height                    ) :
      return False
    ##########################################################################
    if             ( self . Frames     != ITEM . Frames                    ) :
      return False
    ##########################################################################
    if             ( self . Format     != ITEM . Format                    ) :
      return False
    ##########################################################################
    if             ( self . FPS        != ITEM . FPS                       ) :
      return False
    ##########################################################################
    if             ( self . vCodec     != ITEM . vCodec                    ) :
      return False
    ##########################################################################
    if             ( self . vBitRate   != ITEM . vBitRate                  ) :
      return False
    ##########################################################################
    if             ( self . aCodec     != ITEM . aCodec                    ) :
      return False
    ##########################################################################
    if             ( self . SampleRate != ITEM . SampleRate                ) :
      return False
    ##########################################################################
    if             ( self . aBitRate   != ITEM . aBitRate                  ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def assureString     ( self , pb                                         ) :
    ##########################################################################
    BB   = pb
    ##########################################################################
    try                                                                      :
      BB = BB . decode ( "utf-8"                                             )
    except                                                                   :
      pass
    ##########################################################################
    return BB
  ############################################################################
  def Probe                     ( self , Filename , FFPROBE = "ffprobe"    ) :
    ##########################################################################
    ARGs =                      [ FFPROBE                                  , \
                                  "-show_format"                           , \
                                  "-show_streams"                          , \
                                  "-of"                                    , \
                                  "json"                                   , \
                                  Filename                                   ]
    ##########################################################################
    FPRB = subprocess . Popen   ( ARGs                                     , \
                                  stdout        = subprocess . PIPE        , \
                                  stderr        = subprocess . PIPE        , \
                                  creationflags = 0x08000000                 )
    RJ , E = FPRB . communicate (                                            )
    ##########################################################################
    if                          ( FPRB . returncode != 0                   ) :
      return                    {                                            }
    ##########################################################################
    try                                                                      :
      ########################################################################
      BODY     = RJ   . decode  ( "utf-8"                                    )
      BODY     = BODY . replace ( "\r" , ""                                  )
      ########################################################################
      if                        ( len ( BODY ) <= 0                        ) :
        return                  {                                            }
      ########################################################################
      JSOX     = json . loads   ( BODY                                       )
      ########################################################################
    except                                                                   :
      ########################################################################
      return                    {                                            }
    ##########################################################################
    return JSOX
  ############################################################################
  def DistillingChapters        ( self , FFPROBE , Filename                ) :
    ##########################################################################
    ARGs =                      [ FFPROBE                                  , \
                                  "-v"                                     , \
                                  "quiet"                                  , \
                                  "-print_format"                          , \
                                  "json"                                   , \
                                  "-show_chapters"                         , \
                                  Filename                                   ]
    ##########################################################################
    FPRB = subprocess . Popen   ( ARGs                                     , \
                                  stdout        = subprocess . PIPE        , \
                                  stderr        = subprocess . PIPE        , \
                                  creationflags = 0x08000000                 )
    RJ , E = FPRB . communicate (                                            )
    ##########################################################################
    if                          ( FPRB . returncode != 0                   ) :
      return                    ( {  } , False ,                             )
    ##########################################################################
    try                                                                      :
      ########################################################################
      BODY     = RJ   . decode  ( "utf-8"                                    )
      BODY     = BODY . replace ( "\r" , ""                                  )
      ########################################################################
      if                        ( len ( BODY ) <= 0                        ) :
        return                  ( {  } , False ,                             )
      ########################################################################
      JSOX     = json . loads   ( BODY                                       )
      ########################################################################
    except                                                                   :
      ########################################################################
      return                    ( {  } , False ,                             )
    ##########################################################################
    if                          ( "chapters" not in JSOX                   ) :
      return                    ( {  } , False ,                             )
    ##########################################################################
    return                      ( JSOX [ "chapters" ] , True  ,              )
  ############################################################################
  ## 抽取影片幀資訊
  ############################################################################
  def DistillingFrames          ( self , FFPROBE , FILM                    ) :
    ##########################################################################
    ARGs =                      [ FFPROBE                                  , \
                                  "-show_frames"                           , \
                                  "-print_format"                          , \
                                  "json"                                   , \
                                  FILM                                       ]
    ##########################################################################
    FPRB = subprocess . Popen   ( ARGs                                     , \
                                  stdout        = subprocess . PIPE        , \
                                  stderr        = subprocess . PIPE        , \
                                  creationflags = 0x08000000                 )
    RJ , E = FPRB . communicate (                                            )
    ##########################################################################
    if                          ( FPRB . returncode != 0                   ) :
      return                    ( {  } , False ,                             )
    ##########################################################################
    try                                                                      :
      ########################################################################
      BODY     = RJ   . decode  ( "utf-8"                                    )
      BODY     = BODY . replace ( "\r" , ""                                  )
      ########################################################################
      if                        ( len ( BODY ) <= 0                        ) :
        return                  ( {  } , False ,                             )
      ########################################################################
      JSOX     = json . loads   ( BODY                                       )
      ########################################################################
    except                                                                   :
      ########################################################################
      return                    ( {  } , False ,                             )
    ##########################################################################
    return                      ( JSOX , True  ,                             )
  ############################################################################
  def KeepOnlyVideoFrames ( self , JSOX                                    ) :
    ##########################################################################
    VF     =              [                                                  ]
    ##########################################################################
    if                    ( "frames" not in JSOX                           ) :
      return VF
    ##########################################################################
    ID     = 0
    ##########################################################################
    for F in JSOX         [ "frames"                                       ] :
      ########################################################################
      if                  ( "media_type" not in F                          ) :
        continue
      ########################################################################
      if                  ( "video" == F [ "media_type" ]                  ) :
        ######################################################################
        del F             [ "media_type"                                     ]
        ######################################################################
        F [ "id" ] = ID
        ######################################################################
        VF . append       ( F                                                )
        ######################################################################
        ID = ID + 1
    ##########################################################################
    return VF
  ############################################################################
  def KeepOnlyAudioFrames ( self , JSOX                                    ) :
    ##########################################################################
    VF     =              [                                                  ]
    ##########################################################################
    if                    ( "frames" not in JSOX                           ) :
      return VF
    ##########################################################################
    ID     = 0
    ##########################################################################
    for F in JSOX         [ "frames"                                       ] :
      ########################################################################
      if                  ( "media_type" not in F                          ) :
        continue
      ########################################################################
      if                  ( "audio" == F [ "media_type" ]                  ) :
        ######################################################################
        del F             [ "media_type"                                     ]
        ######################################################################
        F [ "id" ] = ID
        ######################################################################
        VF . append       ( F                                                )
        ######################################################################
        ID = ID + 1
    ##########################################################################
    return VF
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
    self . Details [ "Extension" ] = EXT
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
  def Locate                 ( self , DB , VIDTAB                          ) :
    ##########################################################################
    if                       ( self . FileSize <= 0                        ) :
      return False
    ##########################################################################
    FMT  = self . Format
    DUR  = self . Duration
    VFS  = self . FileSize
    VW   = self . Width
    VH   = self . Height
    VCO  = self . vCodec
    FPS  = self . FPS
    FRS  = self . Frames
    VBR  = self . vBitRate
    ACO  = self . aCodec
    ASR  = self . SampleRate
    ABR  = self . aBitRate
    ##########################################################################
    QQ   = f"""select `uuid` from {VIDTAB}
               where ( `used` > 0 )
                 and ( `filesize` = {VFS} )
                 and ( `duration` = {DUR} )
                 and ( `width` = {VW} )
                 and ( `height` = {VH} )
                 and ( `frames` = {FRS} )
                 and ( `format` = '{FMT}' )
                 and ( `fps` = '{FPS}' )
                 and ( `vcodec` = '{VCO}' )
                 and ( `vbitrate` = {VBR} )
                 and ( `acodec` = '{ACO}' )
                 and ( `samplerate` = {ASR} )
                 and ( `abitrate` = {ABR} )
               order by `id` desc ;"""
    ##########################################################################
    QQ    = " " . join       ( QQ . split ( )                                )
    UUIDs = DB . ObtainUuids ( QQ                                            )
    ##########################################################################
    if                       ( len ( UUIDs ) <= 0                          ) :
      return False
    ##########################################################################
    UUID  = UUIDs            [ 0                                             ]
    ##########################################################################
    self . Uuid               = UUID
    self . Details [ "Uuid" ] = self . Uuid
    ##########################################################################
    return                   ( self . Uuid > 0                               )
  ############################################################################
  def Sync             ( self , DB , VIDTAB                                ) :
    ##########################################################################
    if                 ( self . Uuid <= 0                                  ) :
      return False
    ##########################################################################
    UUID = self . Uuid
    FMT  = self . Format
    DUR  = self . Duration
    VFS  = self . FileSize
    VW   = self . Width
    VH   = self . Height
    VCO  = self . vCodec
    FPS  = self . FPS
    FRS  = self . Frames
    VBR  = self . vBitRate
    ACO  = self . aCodec
    ASR  = self . SampleRate
    ABR  = self . aBitRate
    ##########################################################################
    QQ   = f"""update {VIDTAB}
               set `filesize` = {VFS} ,
                   `duration` = {DUR} ,
                      `width` = {VW} ,
                     `height` = {VH} ,
                     `frames` = {FRS} ,
                     `format` = '{FMT}' ,
                        `fps` = '{FPS}' ,
                     `vcodec` = '{VCO}' ,
                   `vbitrate` = {VBR} ,
                     `acodec` = '{ACO}' ,
                 `samplerate` = {ASR} ,
                   `abitrate` = {ABR}
               where ( `uuid` = {UUID} )  ;"""
    ##########################################################################
    QQ   =  " " . join ( QQ . split ( )                                      )
    DB   . Query       ( QQ                                                  )
    ##########################################################################
    return True
  ############################################################################
  def Assure             ( self , DB , VIDTAB                              ) :
    ##########################################################################
    if                   ( self . FileSize <= 0                            ) :
      return False
    ##########################################################################
    UUID = DB . LastUuid ( VIDTAB , "uuid" , 4500000000000000000             )
    ##########################################################################
    FMT  = self . Format
    DUR  = self . Duration
    VFS  = self . FileSize
    VW   = self . Width
    VH   = self . Height
    VCO  = self . vCodec
    FPS  = self . FPS
    FRS  = self . Frames
    VBR  = self . vBitRate
    ACO  = self . aCodec
    ASR  = self . SampleRate
    ABR  = self . aBitRate
    ##########################################################################
    QQ   = f"""insert into {VIDTAB}
               ( `uuid` , `used` , `type` , `filesize` , `duration`,
                 `width` , `height` , `frames` , `format` , `fps` ,
                 `vcodec` , `vbitrate` , `acodec` , `samplerate` , `abitrate` )
               values
               ( {UUID} , 1 , 1 , {VFS} , {DUR} ,
                 {VW} , {VH} , {FRS} , '{FMT}' , '{FPS}' ,
                 '{VCO}' , {VBR} , '{ACO}' , {ASR} , {ABR} ) ;"""
    ##########################################################################
    QQ   =  " " . join   ( QQ . split ( )                                    )
    DB   . Query         ( QQ                                                )
    ##########################################################################
    self . Uuid               = UUID
    self . Details [ "Uuid" ] = self . Uuid
    ##########################################################################
    return               ( self . Uuid > 0                                   )
  ############################################################################
  def MergeVariables          ( self , DB , PUID , MERGER                  ) :
    ##########################################################################
    VARTAB = self . Tables    [ "Variables"                                  ]
    ##########################################################################
    QQ     = f"lock tables {VARTAB} write , {VARTAB} as TT read ;"
    DB     . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""select `type`,`name` from {VARTAB} as TT
                 where ( `uuid` = {PUID} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ALL    = DB . FetchAll    (                                              )
    ##########################################################################
    for RR in ALL                                                            :
      ########################################################################
      TT   = RR               [ 0                                            ]
      NA   = RR               [ 1                                            ]
      ########################################################################
      try                                                                    :
        NA = NA . decode      ( "utf-8"                                      )
      except                                                                 :
        pass
      ########################################################################
      QQ   = f"""delete from {VARTAB}
                 where ( `uuid` = {MERGER} )
                 and ( `type` = {TT} )
                 and ( `name` = '{NA}' ) ;"""
      QQ   = " " . join       ( QQ . split ( )                               )
      DB   . Query            ( QQ                                           )
    ##########################################################################
    QQ     = f"""update {VARTAB}
                 set `uuid` = {PUID}
                 where ( `uuid` = {MERGER} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    return
  ############################################################################
  def MergeParameters                ( self , DB , PUID , MERGER           ) :
    ##########################################################################
    PAMTAB = self . Tables           [ "Parameters"                          ]
    ##########################################################################
    DB     . LockWrites              ( [ PAMTAB                            ] )
    ##########################################################################
    QQ     = f"""update {PAMTAB}
                 set `uuid` = {PUID}
                 where ( `uuid` = {MERGER} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    return
  ############################################################################
  def MergeNotes                     ( self , DB , PUID , MERGER           ) :
    ##########################################################################
    NOXTAB = self . Tables           [ "Notes"                               ]
    ##########################################################################
    DB     . LockWrites              ( [ NOXTAB                            ] )
    ##########################################################################
    QQ     = f"""update {NOXTAB}
                 set `uuid` = {PUID}
                 where ( `uuid` = {MERGER} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    return
  ############################################################################
  def PurgeNamesByCatalog            ( self                                , \
                                       DB                                  , \
                                       PUID                                , \
                                       LOCALITY                            , \
                                       RELEVANCE                           ) :
    ##########################################################################
    NAMTAB = self . Tables           [ "Names"                               ]
    NI     = NameItem                (                                       )
    ##########################################################################
    NI     . Uuid      = PUID
    NI     . Locality  = LOCALITY
    NI     . Relevance = RELEVANCE
    ##########################################################################
    IDs    = NI . ObtainsForPriority ( DB , NAMTAB                           )
    MAPs   =                         {                                       }
    TOTAL  = len                     ( IDs                                   )
    ##########################################################################
    if                               ( TOTAL <= 0                          ) :
      return
    ##########################################################################
    for ID in IDs                                                            :
      ########################################################################
      NX   = NameItem                (                                       )
      NX   . Id        = ID
      NX   . ObtainsById             ( DB , NAMTAB                           )
      MAPs [ ID ] = NX
    ##########################################################################
    PURGEs =                         [                                       ]
    AT     = 0
    ##########################################################################
    while                            ( AT < TOTAL                          ) :
      ########################################################################
      ID   = IDs                     [ AT                                    ]
      NAME = MAPs [ ID ] . Name
      NEXT = AT + 1
      ########################################################################
      while                          ( NEXT < TOTAL                        ) :
        ######################################################################
        IX = IDs                     [ NEXT                                  ]
        ######################################################################
        if                           ( IX not in PURGEs                    ) :
          ####################################################################
          NX = MAPs [ IX ] . Name
          if                         ( NAME == NX                          ) :
            ##################################################################
            PURGEs . append          ( IX                                    )
        ######################################################################
        NEXT = NEXT + 1
      ########################################################################
      AT   = AT + 1
    ##########################################################################
    if                               ( len ( PURGEs ) <= 0                 ) :
      return
    ##########################################################################
    DB     . LockWrites              ( [ NAMTAB                            ] )
    ##########################################################################
    for ID in PURGEs                                                         :
      ########################################################################
      QQ   = f"delete from {NAMTAB} where ( `id` = {ID} ) ;"
      DB   . Query                   ( QQ                                    )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    return
  ############################################################################
  def MergeNamesByCatalog            ( self                                , \
                                       DB                                  , \
                                       PUID                                , \
                                       MERGER                              , \
                                       LOCALITY                            , \
                                       RELEVANCE                           ) :
    ##########################################################################
    NAMTAB = self . Tables           [ "Names"                               ]
    NI     = NameItem                (                                       )
    ##########################################################################
    NI     . Uuid      = MERGER
    NI     . Locality  = LOCALITY
    NI     . Relevance = RELEVANCE
    ##########################################################################
    IDs    = NI . ObtainsForPriority ( DB , NAMTAB                           )
    ##########################################################################
    NI     . Uuid      = PUID
    POS    = NI . LastPosition       ( DB , NAMTAB                           )
    ##########################################################################
    DB     . LockWrites              ( [ NAMTAB                            ] )
    for ID in IDs                                                            :
      ########################################################################
      NI   . Id        = ID
      NI   . Priority  = POS
      NI   . UpdateUuidPriorityById  ( DB , NAMTAB                           )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    return
  ############################################################################
  def MergeNames                     ( self , DB , PUID , MERGER           ) :
    ##########################################################################
    NAMTAB   = self . Tables         [ "Names"                               ]
    NI       = NameItem              (                                       )
    ##########################################################################
    NI       . Uuid = MERGER
    CATALOGs = NI . SelectCatalogues ( DB , NAMTAB                           )
    ##########################################################################
    for C in CATALOGs                                                        :
      ########################################################################
      LC     = C                     [ "Locality"                            ]
      RX     = C                     [ "Relevance"                           ]
      self   . MergeNamesByCatalog   ( DB , PUID , MERGER , LC , RX          )
      self   . PurgeNamesByCatalog   ( DB , PUID          , LC , RX          )
    ##########################################################################
    return
  ############################################################################
  def GetFirstRelationCatalogues  ( self , DB , MERGER                     ) :
    ##########################################################################
    RELTAB = self . Tables        [ "Relation"                               ]
    ##########################################################################
    QQ     = f"""select `t2`,`relation` from {RELTAB}
                 where ( `first` = {MERGER} )
                 and ( `t1` = 7 )
                 group by `t2` asc ,`relation` asc ;"""
    QQ     = " " . join           ( QQ . split ( )                           )
    DB     . Query                ( QQ                                       )
    ALL    = DB . FetchAll        (                                          )
    ##########################################################################
    if                            ( ALL in [ False , None ]                ) :
      return                      [                                          ]
    ##########################################################################
    if                            ( len ( ALL ) <= 0                       ) :
      return                      [                                          ]
    ##########################################################################
    RELs   =                      [                                          ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      T2   = R                    [ 0                                        ]
      REL  = R                    [ 1                                        ]
      J    =                      { "T2" : T2 , "Relation" : REL             }
      RELs . append               ( J                                        )
    ##########################################################################
    return RELs
  ############################################################################
  def MergeFirstPosition      ( self , DB , PUID , MERGER , T2 , REL       ) :
    ##########################################################################
    RELTAB = self . Tables    [ "Relation"                                   ]
    ##########################################################################
    QQ     = f"lock tables {RELTAB} write , {RELTAB} as TT read ;"
    DB     . Query            ( QQ                                           )
    ##########################################################################
    FF     = f"""select `second` from {RELTAB} as TT
                   where ( `first` = {PUID} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )"""
    QQ     = f"""delete from {RELTAB}
                   where ( `first` = {MERGER} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )
                   and ( `second` in ( {FF} ) ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    POS    = -1
    QQ     = f"""select `position` from {RELTAB} as TT
                 where ( `first` = {PUID} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )
                   order by `position` desc
                   limit 0 , 1 ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    RR     = DB . FetchOne    (                                              )
    if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )            :
      POS  = RR               [ 0                                            ]
    POS    = POS + 1
    ##########################################################################
    QQ     = f"""select `second` from {RELTAB} as TT
                   where ( `first` = {MERGER} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )
                   order by `position` asc ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    UUIDs  = DB . ObtainUuids ( QQ                                           )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ   = f"""update {RELTAB}
                   set `first` = {PUID} , `position` = {POS}
                   where ( `first` = {MERGER} )
                   and ( `t1` = 7 )
                   and ( `t2` = {T2} )
                   and ( `relation` = {REL} )
                   and ( `second` = {UUID} ) ;"""
      QQ   = " " . join       ( QQ . split ( )                               )
      DB   . Query            ( QQ                                           )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    return
  ############################################################################
  def MergeFirstRelations         ( self , DB , PUID , MERGER              ) :
    ##########################################################################
    RELTAB   = self . Tables      [ "Relation"                               ]
    CATALOGs = self . GetFirstRelationCatalogues  ( DB , MERGER              )
    ##########################################################################
    for CATALOG in CATALOGs                                                  :
      ########################################################################
      T2     = CATALOG            [ "T2"                                     ]
      REL    = CATALOG            [ "Relation"                               ]
      self   . MergeFirstPosition ( DB , PUID , MERGER , T2 , REL            )
    ##########################################################################
    return
  ############################################################################
  def GetSecondRelationCatalogues ( self , DB , MERGER                     ) :
    ##########################################################################
    RELTAB = self . Tables        [ "Relation"                               ]
    ##########################################################################
    QQ     = f"""select `t1`,`relation` from {RELTAB}
                 where ( `second` = {MERGER} )
                 and ( `t2` = 7 )
                 group by `t1` asc ,`relation` asc ;"""
    QQ     = " " . join           ( QQ . split ( )                           )
    DB     . Query                ( QQ                                       )
    ALL    = DB . FetchAll        (                                          )
    ##########################################################################
    if                            ( ALL in [ False , None ]                ) :
      return                      [                                          ]
    ##########################################################################
    if                            ( len ( ALL ) <= 0                       ) :
      return                      [                                          ]
    ##########################################################################
    RELs   =                      [                                          ]
    ##########################################################################
    for R in ALL                                                             :
      ########################################################################
      T1   = R                    [ 0                                        ]
      REL  = R                    [ 1                                        ]
      J    =                      { "T1" : T1 , "Relation" : REL             }
      RELs . append               ( J                                        )
    ##########################################################################
    return RELs
  ############################################################################
  def MergeSecondPosition      ( self , DB , PUID , MERGER , T1 , REL      ) :
    ##########################################################################
    RELTAB  = self . Tables    [ "Relation"                                  ]
    ##########################################################################
    QQ     = f"lock tables {RELTAB} write , {RELTAB} as TT read ;"
    DB     . Query            ( QQ                                           )
    ##########################################################################
    FF      = f"""select `first` from {RELTAB} as TT
                   where ( `second` = {PUID} )
                   and ( `t1` = {T1} )
                   and ( `t2` = 7 )
                   and ( `relation` = {REL} )"""
    QQ      = f"""delete from {RELTAB}
                   where ( `second` = {MERGER} )
                   and ( `t1` = {T1} )
                   and ( `t2` = 7 )
                   and ( `relation` = {REL} )
                   and ( `first` in ( {FF} ) ) ;"""
    QQ      = " " . join       ( QQ . split ( )                              )
    DB      . Query            ( QQ                                          )
    ##########################################################################
    QQ      = f"""select `first` from {RELTAB} as TT
                   where ( `second` = {MERGER} )
                   and ( `t1` = {T1} )
                   and ( `t2` = 7 )
                   and ( `relation` = {REL} )
                   order by `position` asc ;"""
    QQ      = " " . join       ( QQ . split ( )                              )
    UUIDs   = DB . ObtainUuids ( QQ                                          )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      POS   = -1
      QQ    = f"""select `position` from {RELTAB} as TT
                   where ( `first` = {UUID} )
                     and ( `t1` = {T1} )
                     and ( `t2` = 7 )
                     and ( `relation` = {REL} )
                     order by `position` desc
                     limit 0 , 1 ;"""
      QQ    = " " . join       ( QQ . split ( )                              )
      DB    . Query            ( QQ                                          )
      RR    = DB . FetchOne    (                                             )
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )          :
        POS = RR               [ 0                                           ]
      POS   = POS + 1
      ########################################################################
      QQ    = f"""update {RELTAB}
                   set `second` = {PUID} , `position` = {POS}
                   where ( `second` = {MERGER} )
                   and ( `t1` = {T1} )
                   and ( `t2` = 7 )
                   and ( `relation` = {REL} )
                   and ( `first` = {UUID} ) ;"""
      QQ    = " " . join       ( QQ . split ( )                              )
      DB    . Query            ( QQ                                          )
      ########################################################################
      POS   = POS + 1
    ##########################################################################
    DB      . UnlockTables     (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeSecondRelations         ( self , DB , PUID , MERGER             ) :
    ##########################################################################
    RELTAB   = self . Tables       [ "Relation"                              ]
    CATALOGs = self . GetSecondRelationCatalogues ( DB , MERGER              )
    ##########################################################################
    for CATALOG in CATALOGs                                                  :
      ########################################################################
      T1     = CATALOG             [ "T1"                                    ]
      REL    = CATALOG             [ "Relation"                              ]
      self   . MergeSecondPosition ( DB , PUID , MERGER , T1 , REL           )
    ##########################################################################
    return
  ############################################################################
  def MergeRelations            ( self , DB , PUID , MERGER                ) :
    ##########################################################################
    self . MergeFirstRelations  (        DB , PUID , MERGER                  )
    self . MergeSecondRelations (        DB , PUID , MERGER                  )
    ##########################################################################
    return
  ############################################################################
  def MergeNOTE                      ( self , DB , PUID , MERGER           ) :
    ##########################################################################
    NOXTAB     = self . Tables       [ "Notes"                               ]
    ##########################################################################
    QQ         = f"""select `name` from {NOXTAB}
                     where ( `uuid` = {MERGER} )
                     order by `name` asc ;"""
    QQ         = " " . join          ( QQ . split (                        ) )
    DB         . Query               ( QQ                                    )
    ALL        = DB . FetchAll       (                                       )
    ##########################################################################
    if                               ( ALL in [ False , None ]             ) :
      return
    ##########################################################################
    NAMEs      =                     [                                       ]
    ##########################################################################
    for RR in ALL                                                            :
      ########################################################################
      NN       = self . assureString ( RR [ 0                              ] )
      NAMEs    . append              ( NN                                    )
    ##########################################################################
    if                               ( len ( NAMEs ) <= 0                  ) :
      return
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      QQ       = f"""select `extra` from {NOXTAB}
                     where ( `uuid` = {MERGER} )
                       and ( `name` = '{NAME}' )
                     order by `extra` asc ;"""
      QQ       = " " . join          ( QQ . split (                        ) )
      DB       . Query               ( QQ                                    )
      ALL      = DB . FetchAll       (                                       )
      ########################################################################
      if                             ( ALL in [ False , None             ] ) :
        continue
      ########################################################################
      LANGs    =                     [                                       ]
      ########################################################################
      for RR in ALL                                                          :
        ######################################################################
        LL     = self . assureString ( RR [ 0                              ] )
        LANGs  . append              ( LL                                    )
      ########################################################################
      if                             ( len ( LANGs ) <= 0                  ) :
        continue
      ########################################################################
      for LANG in LANGs                                                      :
        ######################################################################
        QQ     = f"""select `prefer` from {NOXTAB}
                     where ( `uuid` = {PUID} )
                       and ( `name` = '{NAME}' )
                       and ( `extra` = '{LANG}' )
                     order by `prefer` desc
                     limit 0 , 1 ;"""
        QQ     = " " . join          ( QQ . split (                        ) )
        POS    = DB  . GetOne        ( QQ , -1                               )
        ######################################################################
        QQ     = f"""select `id` from {NOXTAB}
                      where ( `uuid` = {MERGER} )
                        and ( `name` = '{NAME}' )
                        and ( `extra` = '{LANG}' )
                      order by `id` asc ;"""
        QQ     = " " . join          ( QQ . split (                        ) )
        NEIDs  = DB  . ObtainUuids   ( QQ                                    )
        ######################################################################
        for NEID in NEIDs                                                    :
          ####################################################################
          POS  = int                 ( int ( POS ) + 1                       )
          ####################################################################
          QQ   = f"""update {NOXTAB}
                    set `uuid` = {PUID} ,
                        `prefer` = {POS}
                    where ( `id` = {NEID} )"""
          QQ   = " " . join          ( QQ . split (                        ) )
          self . SQLs . append       ( QQ                                    )
          DB   . Query               ( QQ                                    )
    ##########################################################################
    QQ         = f"delete from {NOXTAB} where ( `uuid` = {MERGER} ) ;"
    self       . SQLs . append       ( QQ                                    )
    ## DB         . Query               ( QQ                                    )
    ##########################################################################
    return
  ############################################################################
  def MergeURL                        ( self , DB , PUID , MERGER          ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Album"                              )
    REL    . setT2                    ( "WebPage"                            )
    REL    . setRelation              ( "Equivalent"                         )
    ##########################################################################
    REL    . set                      ( "first" , MERGER                     )
    URLz   = REL . Subordination      ( DB      , RELTAB                     )
    ##########################################################################
    if                                ( len ( URLz ) <= 0                  ) :
      return
    ##########################################################################
    REL    . set                      ( "first" , PUID                       )
    URLs   = REL . Subordination      ( DB      , RELTAB                     )
    POS    = REL . GetLastestPosition ( DB      , RELTAB                     )
    ##########################################################################
    URLm   =                          [                                      ]
    ##########################################################################
    for U in URLz                                                            :
      ########################################################################
      if                              ( U not in URLs                      ) :
        ######################################################################
        if                            ( U not in URLm                      ) :
          ####################################################################
          URLm . append               ( U                                    )
    ##########################################################################
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    for U in URLm                                                            :
      ########################################################################
      QQ   = f"""update {RELTAB}
                 set `first` = {PUID} ,
                     `position` = {POS}
                 where ( `first` = {MERGER} )
                   and ( `second` = {U} )
                   and ( `t1` = 76 )
                   and ( `t2` = 208 )
                   and ( `relation` = 10 ) ;"""
      ########################################################################
      QQ   = " " . join               ( QQ . split (                       ) )
      self . SQLs . append            ( QQ                                   )
      DB   . Query                    ( QQ                                   )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    QQ     = f"""delete from {RELTAB}
                 where ( `first` = {MERGER} )
                   and ( `t1` = 76 )
                   and ( `t2` = 208 )
                   and ( `relation` = 10 ) ;"""
    ##########################################################################
    QQ     = " " . join               ( QQ . split (                       ) )
    self   . SQLs . append            ( QQ                                   )
    DB     . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def MergeICON                       ( self , DB , PUID , MERGER          ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Album"                              )
    REL    . setT2                    ( "Picture"                            )
    ##########################################################################
    for RID in                        [ 1 , 12                             ] :
      ########################################################################
      REL  . set                      ( "first"    , MERGER                  )
      REL  . set                      ( "relation" , RID                     )
      URLz = REL . Subordination      ( DB         , RELTAB                  )
      ########################################################################
      if                              ( len ( URLz ) <= 0                  ) :
        continue
      ########################################################################
      REL  . set                      ( "first"    , PUID                    )
      REL  . setRelation              ( "Subordination"                      )
      URLs = REL . Subordination      ( DB      , RELTAB                     )
      POS  = REL . GetLastestPosition ( DB      , RELTAB                     )
      ########################################################################
      URLm =                          [                                      ]
      ########################################################################
      for U in URLz                                                          :
        ######################################################################
        if                            ( U not in URLs                      ) :
          ####################################################################
          if                          ( U not in URLm                      ) :
            ##################################################################
            URLm . append             ( U                                    )
      ########################################################################
      DB   . LockWrites               ( [ RELTAB                           ] )
      ########################################################################
      for U in URLm                                                          :
        ######################################################################
        QQ = f"""update {RELTAB}
                 set `first` = {PUID} ,
                     `relation` = 1 ,
                     `position` = {POS}
                 where ( `first` = {MERGER} )
                   and ( `second` = {U} )
                   and ( `t1` = 76 )
                   and ( `t2` = 9 )
                   and ( `relation` = {RID} ) ;"""
        ######################################################################
        QQ = " " . join               ( QQ . split (                       ) )
        self . SQLs . append          ( QQ                                   )
        DB . Query                    ( QQ                                   )
        ######################################################################
        POS = POS + 1
      ########################################################################
      QQ   = f"""delete from {RELTAB}
                 where ( `first` = {MERGER} )
                   and ( `t1` = 76 )
                   and ( `t2` = 9 )
                   and ( `relation` = {RID} ) ;"""
      ########################################################################
      QQ   = " " . join               ( QQ . split (                       ) )
      self . SQLs . append            ( QQ                                   )
      DB   . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def MergeGALLERY                    ( self , DB , PUID , MERGER          ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Album"                              )
    REL    . setT2                    ( "Gallery"                            )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    REL    . set                      ( "first" , MERGER                     )
    URLz   = REL . Subordination      ( DB      , RELTAB                     )
    ##########################################################################
    if                                ( len ( URLz ) <= 0                  ) :
      return
    ##########################################################################
    REL    . set                      ( "first" , PUID                       )
    URLs   = REL . Subordination      ( DB      , RELTAB                     )
    POS    = REL . GetLastestPosition ( DB      , RELTAB                     )
    ##########################################################################
    URLm   =                          [                                      ]
    ##########################################################################
    for U in URLz                                                            :
      ########################################################################
      if                              ( U not in URLs                      ) :
        ######################################################################
        if                            ( U not in URLm                      ) :
          ####################################################################
          URLm . append               ( U                                    )
    ##########################################################################
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    for U in URLm                                                            :
      ########################################################################
      QQ   = f"""update {RELTAB}
                 set `first` = {PUID} ,
                     `position` = {POS}
                 where ( `first` = {MERGER} )
                   and ( `second` = {U} )
                   and ( `t1` = 76 )
                   and ( `t2` = 64 )
                   and ( `relation` = 1 ) ;"""
      ########################################################################
      QQ   = " " . join               ( QQ . split (                       ) )
      self . SQLs . append            ( QQ                                   )
      DB   . Query                    ( QQ                                   )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    QQ     = f"""delete from {RELTAB}
                 where ( `first` = {MERGER} )
                   and ( `t1` = 76 )
                   and ( `t2` = 64 )
                   and ( `relation` = 1 ) ;"""
    ##########################################################################
    QQ     = " " . join               ( QQ . split (                       ) )
    self   . SQLs . append            ( QQ                                   )
    DB     . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def MergeVIDEO                      ( self , DB , PUID , MERGER          ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Album"                              )
    REL    . setT2                    ( "Video"                              )
    ##########################################################################
    for RID in                        [ 1 , 11 , 15 , 27 , 33              ] :
      ########################################################################
      REL  . set                      ( "first"    , MERGER                  )
      REL  . set                      ( "relation" , RID                     )
      URLz = REL . Subordination      ( DB         , RELTAB                  )
      ########################################################################
      if                              ( len ( URLz ) <= 0                  ) :
        continue
      ########################################################################
      REL  . set                      ( "first" , PUID                       )
      URLs = REL . Subordination      ( DB      , RELTAB                     )
      POS  = REL . GetLastestPosition ( DB      , RELTAB                     )
      ########################################################################
      URLm =                          [                                      ]
      ########################################################################
      for U in URLz                                                          :
        ######################################################################
        if                            ( U not in URLs                      ) :
          ####################################################################
          if                          ( U not in URLm                      ) :
            ##################################################################
            URLm . append             ( U                                    )
      ########################################################################
      DB   . LockWrites               ( [ RELTAB                           ] )
      ########################################################################
      for U in URLm                                                          :
        ######################################################################
        QQ = f"""update {RELTAB}
                 set `first` = {PUID} ,
                     `position` = {POS}
                 where ( `first` = {MERGER} )
                   and ( `second` = {U} )
                   and ( `t1` = 76 )
                   and ( `t2` = 11 )
                   and ( `relation` = {RID} ) ;"""
        ######################################################################
        QQ = " " . join               ( QQ . split (                       ) )
        self . SQLs . append          ( QQ                                   )
        DB . Query                    ( QQ                                   )
        ######################################################################
        POS = POS + 1
      ########################################################################
      QQ   = f"""delete from {RELTAB}
                 where ( `first` = {MERGER} )
                   and ( `t1` = 76 )
                   and ( `t2` = 11 )
                   and ( `relation` = {RID} ) ;"""
      ########################################################################
      QQ   = " " . join               ( QQ . split (                       ) )
      self . SQLs . append            ( QQ                                   )
      DB   . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def MergePEOPLE                     ( self , DB , PUID , MERGER          ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "People"                             )
    REL    . setT2                    ( "Album"                              )
    ##########################################################################
    for RID in                        [ 1 , 33                             ] :
      ########################################################################
      REL  . set                      ( "second"   , MERGER                  )
      REL  . set                      ( "relation" , RID                     )
      URLz = REL . GetOwners          ( DB         , RELTAB                  )
      ########################################################################
      if                              ( len ( URLz ) <= 0                  ) :
        continue
      ########################################################################
      REL  . set                      ( "second", PUID                       )
      URLs = REL . GetOwners          ( DB      , RELTAB                     )
      POS  = REL . GetLastestReverse  ( DB      , RELTAB                     )
      ########################################################################
      URLm =                          [                                      ]
      ########################################################################
      for U in URLz                                                          :
        ######################################################################
        if                            ( U not in URLs                      ) :
          ####################################################################
          if                          ( U not in URLm                      ) :
            ##################################################################
            URLm . append             ( U                                    )
      ########################################################################
      DB   . LockWrites               ( [ RELTAB                           ] )
      ########################################################################
      for U in URLm                                                          :
        ######################################################################
        REL . set                     ( "first" , U                          )
        POZ = REL . GetLastestPosition ( DB     , RELTAB                     )
        ######################################################################
        QQ = f"""update {RELTAB}
                 set `second` = {PUID} ,
                     `position` = {POZ} ,
                     `reverse` = {POS}
                 where ( `first` = {U} )
                   and ( `second` = {MERGER} )
                   and ( `t1` = 76 )
                   and ( `t2` = 7 )
                   and ( `relation` = {RID} ) ;"""
        ######################################################################
        QQ = " " . join               ( QQ . split (                       ) )
        self . SQLs . append          ( QQ                                   )
        DB . Query                    ( QQ                                   )
        ######################################################################
        POS = POS + 1
      ########################################################################
      QQ   = f"""delete from {RELTAB}
                 where ( `second` = {MERGER} )
                   and ( `t1` = 76 )
                   and ( `t2` = 7 )
                   and ( `relation` = {RID} ) ;"""
      ########################################################################
      QQ   = " " . join               ( QQ . split (                       ) )
      self . SQLs . append            ( QQ                                   )
      DB   . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def MergeORGANIZATION               ( self , DB , PUID , MERGER          ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Organization"                       )
    REL    . setT2                    ( "Album"                              )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    REL    . set                      ( "second" , MERGER                    )
    URLz   = REL . GetOwners          ( DB       , RELTAB                    )
    ##########################################################################
    if                                ( len ( URLz ) <= 0                  ) :
      return
    ##########################################################################
    REL    . set                      ( "second" , PUID                      )
    URLs   = REL . GetOwners          ( DB       , RELTAB                    )
    POS    = REL . GetLastestReverse  ( DB       , RELTAB                    )
    ##########################################################################
    URLm   =                          [                                      ]
    ##########################################################################
    for U in URLz                                                            :
      ########################################################################
      if                              ( U not in URLs                      ) :
        ######################################################################
        if                            ( U not in URLm                      ) :
          ####################################################################
          URLm . append               ( U                                    )
    ##########################################################################
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    for U in URLm                                                            :
      ########################################################################
      REL  . set                      ( "first" , U                          )
      POZ  = REL . GetLastestPosition ( DB     , RELTAB                      )
      ########################################################################
      QQ   = f"""update {RELTAB}
                 set `second` = {PUID} ,
                     `position` = {POZ} ,
                     `reverse` = {POS}
                 where ( `first` = {U} )
                   and ( `second` = {MERGER} )
                   and ( `t1` = 38 )
                   and ( `t2` = 76 )
                   and ( `relation` = 1 ) ;"""
      ########################################################################
      QQ   = " " . join               ( QQ . split (                       ) )
      self . SQLs . append            ( QQ                                   )
      DB   . Query                    ( QQ                                   )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    QQ     = f"""delete from {RELTAB}
                 where ( `second` = {MERGER} )
                   and ( `t1` = 38 )
                   and ( `t2` = 76 )
                   and ( `relation` = 1 ) ;"""
    ##########################################################################
    QQ     = " " . join               ( QQ . split (                       ) )
    self   . SQLs . append            ( QQ                                   )
    DB     . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def MergeFRAG                       ( self , DB , PUID , MERGER          ) :
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Album"                              )
    REL    . setT2                    ( "vFragment"                          )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    REL    . set                      ( "first" , MERGER                     )
    URLz   = REL . Subordination      ( DB      , RELTAB                     )
    ##########################################################################
    if                                ( len ( URLz ) <= 0                  ) :
      return
    ##########################################################################
    REL    . set                      ( "first" , PUID                       )
    URLs   = REL . Subordination      ( DB      , RELTAB                     )
    POS    = REL . GetLastestPosition ( DB      , RELTAB                     )
    ##########################################################################
    URLm   =                          [                                      ]
    ##########################################################################
    for U in URLz                                                            :
      ########################################################################
      if                              ( U not in URLs                      ) :
        ######################################################################
        if                            ( U not in URLm                      ) :
          ####################################################################
          URLm . append               ( U                                    )
    ##########################################################################
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    for U in URLm                                                            :
      ########################################################################
      QQ   = f"""update {RELTAB}
                 set `first` = {PUID} ,
                     `position` = {POS}
                 where ( `first` = {MERGER} )
                   and ( `second` = {U} )
                   and ( `t1` = 76 )
                   and ( `t2` = 213 )
                   and ( `relation` = 1 ) ;"""
      ########################################################################
      QQ   = " " . join               ( QQ . split (                       ) )
      self . SQLs . append            ( QQ                                   )
      DB   . Query                    ( QQ                                   )
      ########################################################################
      POS  = POS + 1
    ##########################################################################
    QQ     = f"""delete from {RELTAB}
                 where ( `first` = {MERGER} )
                   and ( `t1` = 76 )
                   and ( `t2` = 213 )
                   and ( `relation` = 1 ) ;"""
    ##########################################################################
    QQ     = " " . join               ( QQ . split (                       ) )
    self   . SQLs . append            ( QQ                                   )
    DB     . Query                    ( QQ                                   )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    ##########################################################################
    return
  ############################################################################
  def Merge                   ( self , DB , PUID , MERGER                  ) :
    ##########################################################################
    return
    ##########################################################################
    ## self   . MergeVariables   (        DB , PUID , MERGER                    )
    ## self   . MergeParameters  (        DB , PUID , MERGER                    )
    ## self   . MergeNotes       (        DB , PUID , MERGER                    )
    ## self   . MergeNames       (        DB , PUID , MERGER                    )
    ## self   . MergeRelations   (        DB , PUID , MERGER                    )
    ##########################################################################
    PEOTAB = self . Tables    [ "People"                                     ]
    DB     . LockWrites       ( [ PEOTAB                                   ] )
    ## self   . UpdatePeopleUsed ( DB , PEOTAB , MERGER , 3                     )
    DB     . UnlockTables     (                                              )
    ##########################################################################
    return
  ############################################################################
  def MergeAll                 ( self , DB , PUID , MERGERs , ICON = 0     ) :
    ##########################################################################
    return
    ##########################################################################
    PXID     = 0
    ##########################################################################
    ## 取得指派的代表圖示
    ##########################################################################
    if                         ( ICON > 0                                  ) :
      ########################################################################
      RELTAB = self . Tables   [ "Relation"                                  ]
      PXIDs  = self . GetIcons ( DB , RELTAB , ICON                          )
      ########################################################################
      if                       ( len ( PXIDs ) > 0                         ) :
        ######################################################################
        PXID = PXIDs           [ 0                                           ]
    ##########################################################################
    ## 合併人物資訊
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . Merge             (        DB , PUID , MERGER                   )
    ##########################################################################
    ## 重新排序代表圖示
    ##########################################################################
    if                         ( ( ICON > 0 ) and ( PXID > 0 )             ) :
      ########################################################################
      RELTAB = self . Tables   [ "Relation"                                  ]
      PXIDs  = self . GetIcons ( DB , RELTAB , PUID                          )
      CXIDs  =                 [ PXID                                        ]
      ########################################################################
      for CUID in PXIDs                                                      :
        ######################################################################
        if                     ( CUID not in CXIDs                         ) :
          CXIDs . append       ( CUID                                        )
      ########################################################################
      if                       ( len ( CXIDs ) > 0                         ) :
        DB   . LockWrites      ( [ RELTAB                                  ] )
        self . RepositionIcons ( DB , RELTAB , PUID , CXIDs                  )
        DB   . UnlockTables    (                                             )
    ##########################################################################
    return
  ############################################################################
  ## 合併影集描述筆記
  ############################################################################
  def MergeNOTEs       ( self , DB , PUID , MERGERs                        ) :
    ##########################################################################
    self   . SQLs =    [                                                     ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . MergeNOTE (        DB , PUID , MERGER                           )
    ##########################################################################
    return
  ############################################################################
  ## 合併影集關聯網址資訊
  ############################################################################
  def MergeURLs       ( self , DB , PUID , MERGERs                         ) :
    ##########################################################################
    self   . SQLs =   [                                                      ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . MergeURL (        DB , PUID , MERGER                            )
    ##########################################################################
    return
  ############################################################################
  ## 合併影集所含圖片
  ############################################################################
  def MergeICONs       ( self , DB , PUID , MERGERs                        ) :
    ##########################################################################
    self   . SQLs =    [                                                     ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . MergeICON (        DB , PUID , MERGER                           )
    ##########################################################################
    return
  ############################################################################
  ## 合併影集所含圖庫
  ############################################################################
  def MergeGALLERYs       ( self , DB , PUID , MERGERs                     ) :
    ##########################################################################
    self   . SQLs =       [                                                  ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . MergeGALLERY (        DB , PUID , MERGER                        )
    ##########################################################################
    return
  ############################################################################
  ## 合併影集所含影片
  ############################################################################
  def MergeVIDEOs       ( self , DB , PUID , MERGERs                       ) :
    ##########################################################################
    self   . SQLs =     [                                                    ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . MergeVIDEO (        DB , PUID , MERGER                          )
    ##########################################################################
    return
  ############################################################################
  ## 合併影集隸屬人物
  ############################################################################
  def MergePEOPLEs       ( self , DB , PUID , MERGERs                      ) :
    ##########################################################################
    self   . SQLs =      [                                                   ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . MergePEOPLE (        DB , PUID , MERGER                         )
    ##########################################################################
    return
  ############################################################################
  ## 合併影集隸屬組織
  ############################################################################
  def MergeORGANIZATIONs       ( self , DB , PUID , MERGERs                ) :
    ##########################################################################
    self   . SQLs =            [                                             ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . MergeORGANIZATION (        DB , PUID , MERGER                   )
    ##########################################################################
    return
  ############################################################################
  ## 合併影集所屬影片段落
  ############################################################################
  def MergeFRAGs       ( self , DB , PUID , MERGERs                        ) :
    ##########################################################################
    self   . SQLs =    [                                                     ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      self . MergeFRAG (        DB , PUID , MERGER                           )
    ##########################################################################
    return
  ############################################################################
  def MergeLIMITED             ( self , DB , PUID , MERGERs                ) :
    ##########################################################################
    self   . SQLs =            [                                             ]
    ##########################################################################
    for MERGER in MERGERs                                                    :
      ########################################################################
      self . MergeNOTE         (        DB , PUID , MERGER                   )
      self . MergeURL          (        DB , PUID , MERGER                   )
      self . MergeICON         (        DB , PUID , MERGER                   )
      self . MergeGALLERY      (        DB , PUID , MERGER                   )
      self . MergeVIDEO        (        DB , PUID , MERGER                   )
      self . MergePEOPLE       (        DB , PUID , MERGER                   )
      self . MergeORGANIZATION (        DB , PUID , MERGER                   )
      self . MergeFRAG         (        DB , PUID , MERGER                   )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
