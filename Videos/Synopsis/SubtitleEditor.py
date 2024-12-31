# -*- coding: utf-8 -*-
##############################################################################
## Subtitle
## 字幕
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
from   AITK    . AI  . Pictures . Vision import Vision      as AiVision
##############################################################################
from   AITK    . Pictures . Picture      import Picture     as PictureItem
from   AITK    . People . Faces . Face   import Face        as FaceItem
from   AITK    . People . Body  . Tit    import Tit         as TitItem
from   AITK    . People . Body  . Body   import Body        as BodyItem
##############################################################################
