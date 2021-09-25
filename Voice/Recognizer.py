# -*- coding: utf-8 -*-

""" 透過網路提供本機使用效能數據 """
import os
import sys
import time
import datetime
import getopt
import logging
import threading
import speech_recognition as vrt

class Recognizer ( ) :

  def __init__ ( self , Engine = 1 ) :
    self . Initialize ( Engine )

  def __del__ ( self ) :
    pass

  def Initialize ( self , Engine = 1) :
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
    self . Score     = 0
    self . Total     = 0
    self . Threshold = 0
    self . Average   = 0
    self . Continue  = 0
    self . Phrase    = 8000.0
    self . Language  = "en-US"
    self . Languages = [ "en-US" , "zh-TW" ]

  def AddScore ( self ) :
    self . Score    += self . ear . energy_threshold
    self . Total    += 1
    self . Continue += 1
    self . Average  = self . Score / self . Total
    """
    if ( None != self . Error ) :
      et      = self . ear . energy_threshold
      average = self . Average
      self . Error ( f">> Average Threshold {average} at {et}" )
    """

  def UseMicrophone ( self ) :
    with self . mic as source :
      # self . ear . adjust_for_ambient_noise ( source )
      self . audio = self . ear . listen    ( source )
    return True

  def OpenMicrophone ( self , Device = None ) :
    self . Device = Device
    if ( None == Device ) :
      self . mic = vrt . Microphone ( )
    else :
      self . mic = vrt . Microphone ( device_index = Device )
    if ( None == self . mic ) :
      return False
    return True

  def OpenFile ( self , File ) :
    if ( len ( File ) <= 0 ) :
      return False
    harvard = vrt . AudioFile ( File )
    with harvard as source:
      # self . ear . adjust_for_ambient_noise ( source )
      self . audio = self . ear . record    ( source )
    return True

  def Listen ( self , Language = "en-US" ) :
    if   ( self . Engine == 0 ) :
      try :
        line = self . ear . recognize_sphinx ( self . audio )
        line = line . strip ( )
        if ( len ( line ) > 0 ) :
          return line
        return ""
      except vrt . RequestError:
        if ( None != self . Error ) :
          self . Error ( ">> API unavailable" )
      except vrt . UnknownValueError:
        if ( None != self . Error ) :
          self . Error ( ">> Unable to recognize speech" )
    elif ( self . Engine == 1 ) :
      try :
        line = self . ear . recognize_google ( self . audio , language = Language )
        line = line . strip ( )
        # recognize_google ( self , audio_data , key=None , language="en-US" , pfilter=0 , show_all=False )
        # ja , zh-TW , zh-CN
        if ( len ( line ) > 0 ) :
          return line
        return ""
      except vrt . RequestError:
        if ( None != self . Error ) :
          self . Error ( ">> API unavailable" )
      except vrt . UnknownValueError:
        if ( None != self . Error ) :
          self . Error ( ">> Unable to recognize speech" )
    return ""

  def ListenInBackground ( self , audio , Language = "en-US" ) :
    Abnormal = False
    if ( None != self . Reading ) :
      self . Reading ( True )
    if   ( self . Engine == 0 ) :
      try :
        line = self . ear . recognize_sphinx ( audio )
        line = line . strip ( )
        if ( len ( line ) > 0 ) :
          self . AddScore ( )
          return line
        return ""
      except vrt . RequestError:
        pass
        """
        if ( None != self . Error ) :
          self . Error ( ">> API unavailable" )
        """
      except vrt . UnknownValueError:
        pass
        """
        if ( None != self . Error ) :
          self . Error ( ">> Unable to recognize speech" )
        """
    elif ( self . Engine == 1 ) :
      try :
        line = self . ear . recognize_google ( audio , language = Language )
        line = line . strip ( )
        # recognize_google ( self , audio_data , key=None , language="en-US" , pfilter=0 , show_all=False )
        # ja , zh-TW , zh-CN
        if ( len ( line ) > 0 ) :
          self . AddScore ( )
          return line
        return ""
      except vrt . RequestError:
        pass
        """
        if ( None != self . Error ) :
          self . Error ( ">> API unavailable" )
        """
      except vrt . UnknownValueError:
        pass
        """
        if ( None != self . Error ) :
          self . Error ( ">> Unable to recognize speech" )
        """
    if ( None != self . Reading ) :
      self . Reading ( False )
    return ""

  def StopListening ( self ) :
    if ( None == self . Stop ) :
      return False
    self . Stop ( wait_for_stop = False )
    return True

  def ParallelParse ( self , audio , Language ) :
    line = self . ListenInBackground ( audio , Language )
    if ( len ( line ) <= 0 ) :
      return False
    self . Parser ( line )
    return True

  def Callback ( self , recognizer , audio ) :
    if ( None == self . Parser ) :
      return False
    for L in self . Languages :
      threading . Thread ( target = self . ParallelParse , args = ( audio , L , ) ) . start ( )
    return True

  def Background ( self , Language = "en-US" ) :
    phrase = self . Phrase
    phrase = phrase / 1000.0
    self   . Language = Language
    self   . Continue = 0
    with self . mic as source :
      self . ear . adjust_for_ambient_noise ( source )
    self . Stop     = self . ear . listen_in_background ( self . mic , self . Callback , phrase )
    return True
