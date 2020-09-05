# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import datetime
import logging
import requests
import threading
import gettext
import shutil

from   pydrive . auth  import GoogleAuth
from   pydrive . drive import GoogleDrive

class Drive ( ) :

  def __init__ ( self ) :
    self . Auth = GoogleAuth ( )

  def __del__ ( self ) :
    pass

  def WebAuth ( self ) :
    self . Auth . LocalWebserverAuth ( )
    return True

  def CommandAuth ( self ) :
    self . Auth . CommandLineAuth ( )

  def GetDrive ( self ) :
    self . Drive = GoogleDrive ( self . Auth )
    return self . Drive

  def ListFolder ( self , FOLDER ) :
    QX = f"'{FOLDER}' in parents and trashed=false"
    return self . Drive . ListFile ( { 'q': QX } ) . GetList ( )
