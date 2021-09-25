# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
import getopt
import logging
import threading
from   pydub import AudioSegment
from   pydub . silence import split_on_silence

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
