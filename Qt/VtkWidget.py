# -*- coding: utf-8 -*-
##############################################################################
## Widget
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
import vtk
##############################################################################
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QWidget
##############################################################################
from   vtk   . qt . QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
##############################################################################
from         . VirtualGui             import VirtualGui  as VirtualGui
##############################################################################
class VtkWidget   ( QVTKRenderWindowInteractor , VirtualGui                ) :
  ############################################################################
  def __init__    ( self , parent = None , plan = None                     ) :
    ##########################################################################
    super (                   ) . __init__ ( parent                          )
    super ( VirtualGui , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    ##########################################################################
    self . setAttribute    ( Qt . WA_InputMethodEnabled                      )
    self . VoiceJSON =     {                                                 }
    ##########################################################################
    self . PrepareRenderer (                                                 )
    ##########################################################################
    return
  ############################################################################
  def PrepareRenderer      ( self                                          ) :
    ##########################################################################
    self . renderer   = vtk  . vtkRenderer (                                 )
    self . GetRenderWindow ( ) . AddRenderer ( self . renderer               )
    self . interactor = self . GetRenderWindow ( ) . GetInteractor (         )
    ##########################################################################
    return
  ############################################################################
  def PrepareContent       ( self                                          ) :
    ##########################################################################
    ## source = vtk.vtkSphereSource()
    ## source . SetCenter(0, 0, 0)
    ## source . SetRadius(5.0)
    ##########################################################################
    ## Create a mapper
    ## mapper = vtk.vtkPolyDataMapper()
    ## mapper.SetInputConnection(source.GetOutputPort())
    ##########################################################################
    # Create an actor
    ## actor = vtk.vtkActor()
    ## actor.SetMapper(mapper)
    ##########################################################################
    ## self . renderer . AddActor(actor)
    ## self . renderer . ResetCamera  ( )
    ##########################################################################
    self . interactor . Initialize ( )
    self . interactor . Start      ( )
    ##########################################################################
    return
##############################################################################
