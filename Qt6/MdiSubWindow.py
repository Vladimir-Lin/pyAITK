# -*- coding: utf-8 -*-
##############################################################################
## MdiSubWindow
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
##############################################################################
import PySide6
from   PySide6             import QtCore
from   PySide6             import QtGui
from   PySide6             import QtWidgets
##############################################################################
from   PySide6 . QtCore    import *
from   PySide6 . QtGui     import *
from   PySide6 . QtWidgets import *
##############################################################################
class MdiSubWindow              ( QMdiSubWindow                            ) :
  ############################################################################
  def __init__                  ( self , parent = None                     ) :
    ##########################################################################
    super ( ) . __init__        ( parent                                     )
    self      .  setAttribute   ( Qt . WA_InputMethodEnabled                 )
    ##########################################################################
    return
  ############################################################################
  def closeEvent                ( self , event                             ) :
    ##########################################################################
    """
    if ( NULL != abstract )                                         {
      if ( ! abstract -> canStop ( ) )                              {
        e -> ignore ( )                                             ;
        return                                                      ;
      }                                                             ;
    } else                                                          {
      QWidget * w = widget ( )                                      ;
      if ( NULL != w )                                              {
        QVariant v = w -> property ( "AbstractGui" )                ;
        if ( v . isValid ( ) && v . toBool ( ) )                    {
          QVariant z = w -> property ( "CanStop" )                  ;
          if ( z . isValid ( ) && ( ! getAbstractStopable ( z ) ) ) {
            e -> ignore ( )                                         ;
            return                                                  ;
          }                                                         ;
        }                                                           ;
      }                                                             ;
    }                                                               ;
    """
    ##########################################################################
    super ( ) . closeEvent      (        event                               )
    ##########################################################################
    return
  ############################################################################
  def isMdiSubWindow            ( self                                     ) :
    return True
  ############################################################################
  ############################################################################
##############################################################################
