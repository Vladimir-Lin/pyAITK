# -*- coding: utf-8 -*-
##############################################################################
## EpisodeEditor
## 影集編輯
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import vlc
import math
import cv2
##############################################################################
import pathlib
from   pathlib                           import Path
##############################################################################
import AITK
##############################################################################
from   AITK    . Calendars . StarDate    import StarDate    as StarDate
from   AITK    . Documents . JSON        import Load        as LoadJson
from   AITK    . Documents . JSON        import Save        as SaveJson
##############################################################################
from   PySide6                           import QtCore
from   PySide6                           import QtGui
from   PySide6                           import QtWidgets
from   PySide6 . QtCore                  import *
from   PySide6 . QtGui                   import *
from   PySide6 . QtWidgets               import *
from   AITK    . Qt6                     import *
##############################################################################
from   AITK    . Qt6 . MenuManager       import MenuManager as MenuManager
from   AITK    . Qt6 . AttachDock        import AttachDock  as AttachDock
from   AITK    . Qt6 . Widget            import Widget      as Widget
##############################################################################
from                 . Episode           import Episode     as Episode
##############################################################################
class EpisodeEditor              ( ScrollArea                              ) :
  ############################################################################
  def           __init__         ( self , parent = None , plan = None      ) :
    ##########################################################################
    super ( ) . __init__         (        parent        , plan               )
    ##########################################################################
    self . cwidget = QWidget     (                                           )
    self . vlayout = QVBoxLayout ( self . cwidget                            )
    self . setMinimumHeight      ( 60                                        )
    self . setWidget             ( self . cwidget                            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 640 , 480 )                       )
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
