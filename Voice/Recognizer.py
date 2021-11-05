# -*- coding: utf-8 -*-
##################################################################################
## 透過網路提供本機使用效能數據
##############################################################################
import os
import sys
import time
import datetime
import getopt
import logging
import threading
##############################################################################
from   pydub                        import AudioSegment
from   pydub . silence              import split_on_silence
##############################################################################
import speech_recognition                           as     vrt
##############################################################################
from   AITK  . Calendars . StarDate import StarDate as StarDate
##############################################################################
"""
def SplitVoiceByWords ( wave , chunkHeader , settings = { } ) :
  sound_file = AudioSegment . from_wav ( wave )
  silence    =  1000
  thresh     = -16
  lastest    = -1
  if ( "silence" in settings ) :
    silence = settings [ "silence" ]
  if ( "thresh" in settings ) :
    thresh = settings [ "thresh" ]
  audio_chunks = split_on_silence            (
                   sound_file                ,
                   min_silence_len = silence ,
                   silence_thresh  = thresh  )
  for i , chunk in enumerate ( audio_chunks ) :
    lastest  = i + 1
    out_file = "{0}-{1}.wav" . format ( chunkHeader , lastest )
    chunk . export ( out_file , format = "wav" )
  return lastest
"""
##############################################################################
class Recognizer         (                                                 ) :
  ############################################################################
  def __init__           ( self , Engine = 1                               ) :
    ##########################################################################
    self . Initialize    (        Engine                                     )
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Initialize         ( self , Engine = 1                               ) :
    ##########################################################################
    self . ear       = vrt . Recognizer ( )
    self . ear       . dynamic_energy_threshold = True
    self . ear       . energy_threshold = 30
    self . ear       . pause_threshold  = 0.5
    self . ear       . phrase_threshold = 0.6
    self . audio     = None
    self . mic       = None
    self . Engine    = 1
    self . Device    = None
    self . Stop      = None
    self . Parser    = None
    self . Error     = None
    self . Reading   = None
    self . Again     = self . Background
    self . NOW       = StarDate ( )
    self . Score     = 0
    self . Total     = 0
    self . Threshold = 0
    self . Average   = 0
    self . Continue  = 0
    self . Phrase    = 8000.0
    self . Language  = "en-US"
    self . Languages = [ "en-US" , "zh-TW" ]
    ##########################################################################
    return
  ############################################################################
  def AddScore           ( self , Language                                 ) :
    ##########################################################################
    self . Score    += self . ear . energy_threshold
    self . Total    += 1
    self . Continue += 1
    self . Average  = self . Score / self . Total
    ##########################################################################
    if                   ( None != self . Error                            ) :
      ########################################################################
      et            = self . ear . energy_threshold
      average       = self . Average
      msg           = f">> Average Threshold {average} at {et}"
      self . TellError   ( 2001 , msg , Language                             )
    ##########################################################################
    return
  ############################################################################
  def UseMicrophone      ( self                                            ) :
    ##########################################################################
    with self . mic as source                                                :
      # self . ear . adjust_for_ambient_noise ( source )
      self . audio = self . ear . listen ( source                            )
    ##########################################################################
    return True
  ############################################################################
  def OpenMicrophone                   ( self , Device = None              ) :
    ##########################################################################
    self   . Device = Device
    if                                 ( None == Device                    ) :
      self . mic    = vrt . Microphone (                                     )
    else                                                                     :
      self . mic    = vrt . Microphone ( device_index = Device               )
    if                                 ( None == self . mic                ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def OpenFile                           ( self , File                     ) :
    ##########################################################################
    if                                   ( len ( File ) <= 0               ) :
      return False
    ##########################################################################
    harvard = vrt . AudioFile            ( File                              )
    with harvard as source                                                   :
      # self . ear . adjust_for_ambient_noise ( source )
      self . audio = self . ear . record ( source                            )
    ##########################################################################
    return True
  ############################################################################
  def TellError  ( self , code , message , language                        ) :
    ##########################################################################
    if           ( None == self . Error                                    ) :
      return
    ##########################################################################
    self . NOW  . Now ( )
    TS   = self . NOW . Stardate
    self . Error ( language , code , message , TS                            )
    ##########################################################################
    return
  ############################################################################
  def ListenViaSphinx     ( self , audio , Language = "en-US"              ) :
    ##########################################################################
    try                                                                      :
      ########################################################################
      line = self . ear . recognize_sphinx ( audio                           )
      line = line . strip (                                                  )
      if                  ( len ( line ) > 0                               ) :
        self . AddScore   ( Language                                         )
        return line
      ########################################################################
      return ""
      ########################################################################
    except vrt . RequestError                                                :
      ########################################################################
      msg  = ">> Sphinx API unavailable"
      self . TellError    ( 1001 , msg , Language                            )
      ########################################################################
    except vrt . UnknownValueError                                           :
      ########################################################################
      msg  = ">> Sphinx Unable to recognize speech"
      self . TellError    ( 1002 , msg , Language                            )
    ##########################################################################
    return ""
  ############################################################################
  def ListenViaGoogle     ( self , audio , Language = "en-US"              ) :
    ##########################################################################
    try                                                                      :
      ########################################################################
      line = self . ear . recognize_google ( audio , language = Language     )
      line = line . strip (                                                  )
      ########################################################################
      ## recognize_google   (
      ##   self             ,
      ##   audio_data       ,
      ##   key=None         ,
      ##   language="en-US" ,
      ##   pfilter=0        ,
      ##   show_all=False   )
      ## ja , zh-TW , zh-CN
      ########################################################################
      if                  ( len ( line ) > 0                               ) :
        self . AddScore   ( Language                                         )
        return line
      ########################################################################
      return ""
      ########################################################################
    except vrt . RequestError                                                :
      ########################################################################
      msg  = ">> Google API unavailable"
      self . TellError    ( 1001 , msg , Language                            )
      ########################################################################
    except vrt . UnknownValueError                                           :
      ########################################################################
      msg  = ">> Google Unable to recognize speech"
      self . TellError    ( 1002 , msg , Language                            )
    ##########################################################################
    return ""
  ############################################################################
  def Listen                        ( self , Language = "en-US"            ) :
    ##########################################################################
    if                              ( self . Engine == 0                   ) :
      return self . ListenViaSphinx ( self . audio , Language                )
    ##########################################################################
    if                              ( self . Engine == 1                   ) :
      return self . ListenViaGoogle ( self . audio , Language                )
    ##########################################################################
    return   ""
  ############################################################################
  def ListenInBackground            ( self , audio , Language = "en-US"    ) :
    ##########################################################################
    Abnormal = False
    ##########################################################################
    if                              ( None != self . Reading               ) :
      self . NOW  . Now ( )
      TS   = self . NOW . Stardate
      self . Reading                ( Language , True  , TS                  )
    ##########################################################################
    if                              ( self . Engine == 0                   ) :
      line = self . ListenViaSphinx ( audio , Language                       )
      if                            ( len ( line ) > 0                     ) :
        return line
    ##########################################################################
    if                              ( self . Engine == 1                   ) :
      line = self . ListenViaGoogle ( audio , Language                       )
      if                            ( len ( line ) > 0                     ) :
        return line
    ##########################################################################
    if                              ( None != self . Reading               ) :
      self . NOW  . Now ( )
      TS   = self . NOW . Stardate
      self . Reading                ( Language , False , TS                  )
    ##########################################################################
    return ""
  ############################################################################
  def StopListening      ( self                                            ) :
    ##########################################################################
    if                   ( None == self . Stop                             ) :
      return False
    ##########################################################################
    self . Stop          ( wait_for_stop = False                             )
    ##########################################################################
    return True
  ############################################################################
  def ParallelParse                  ( self , audio , Language             ) :
    ##########################################################################
    line = self . ListenInBackground (        audio , Language               )
    if                               ( len ( line ) <= 0                   ) :
      return False
    ##########################################################################
    self . NOW . Now ( )
    TS   = self . NOW . Stardate
    self . Parser                    ( Language , line , TS                  )
    ##########################################################################
    return True
  ############################################################################
  def Callback           ( self , recognizer , audio                       ) :
    ##########################################################################
    if                   ( None == self . Parser                           ) :
      return False
    ##########################################################################
    for L in self . Languages                                                :
      threading . Thread ( target = self . ParallelParse                   , \
                           args   = ( audio , L , ) ) . start (              )
    ##########################################################################
    return True
  ############################################################################
  def Background         ( self , Language = "en-US"                       ) :
    ##########################################################################
    phrase            = self . Phrase
    phrase            = phrase / 1000.0
    self   . Language = Language
    self   . Continue = 0
    ##########################################################################
    Correct           = False
    while                ( not Correct                                     ) :
      ########################################################################
      try                                                                    :
        ######################################################################
        with self . mic as source                                            :
          self . ear . adjust_for_ambient_noise ( source                     )
        Correct       = True
        ######################################################################
      except                                                                 :
        self . TellError ( 3001 , "Microphone error" , Language              )
        time . sleep     ( 1.5                                               )
    ##########################################################################
    self . Stop       = self . ear . listen_in_background                  ( \
                          self . mic                                       , \
                          self . Callback                                  , \
                          phrase                                             )
    ##########################################################################
    return True
##############################################################################
