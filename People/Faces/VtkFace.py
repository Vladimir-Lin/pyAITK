# -*- coding: utf-8 -*-
##############################################################################
## VtkFace
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
from   PyQt5 . QtWidgets              import QFileDialog
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QDoubleSpinBox
##############################################################################
from   AITK  . VTK . VtkWidget        import VtkWidget as VtkWidget
from   AITK  . VTK . Wrapper          import Wrapper     as VtkWrapper
##############################################################################
from   AITK  . Qt  . MenuManager      import MenuManager as MenuManager
##############################################################################
from   AITK  . Math . Geometry . ControlPoint import ControlPoint as ControlPoint
from   AITK  . Math . Geometry . Contour      import Contour      as Contour
from   AITK  . Math . Geometry . Circle       import Circle       as Circle
from   AITK  . Math . Geometry . Cylinder     import Cylinder     as Cylinder
from   AITK  . Math . Geometry . Plane        import Plane        as Plane
from   AITK  . Math . Geometry . Parabola     import Parabola     as Parabola
from   AITK  . Math . Geometry . Sphere       import Sphere       as Sphere
from   AITK  . Math . Geometry . Polyhedron   import Polyhedron   as Polyhedron
##############################################################################
class VtkFace                 ( VtkWidget                                  ) :
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super ( ) . __init__      (        parent        , plan                  )
    self . setVtkFaceDefaults (                                              )
    ##########################################################################
    return
  ############################################################################
  def setVtkFaceDefaults   ( self                                          ) :
    ##########################################################################
    ## self . dockingPlace = Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction     ( self . HavingMenu , True                        )
    ##########################################################################
    self . setAcceptDrops  ( True                                            )
    ## self . setDragEnabled  ( True                                            )
    ## self . setDragDropMode ( QAbstractItemView . DragDrop                    )
    ##########################################################################
    self . PeopleUuid = 0
    self . SpinBoxs   =    {                                                 }
    self . Callbacks  =    [                                                 ]
    ##########################################################################
    return
  ############################################################################
  def EmitCallbacks ( self , JSON                                          ) :
    ##########################################################################
    for Callback in self . Callbacks                                         :
      Callback      (        JSON                                            )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def PeopleDetailsChanged ( self , WhatJSON                               ) :
    ##########################################################################
    ##########################################################################
    return                 { "Answer" : "Okay"                               }
  ############################################################################
  def AcceptFaceGeometry            ( self , JSON                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def startFromJson                 ( self , JSON                          ) :
    ##########################################################################
    self . PeopleUuid = JSON        [ "People"                               ]
    self . Callbacks  = JSON        [ "Plugins"                              ]
    CALLTO            = JSON        [ "Callback"                             ]
    ##########################################################################
    FUNC = self . PeopleDetailsChanged
    JSOX =                          { "FaceGeometry" : FUNC                  }
    CALLTO                          ( JSOX                                   )
    ##########################################################################
    FUNC = self . AcceptFaceGeometry
    JSOZ =                          { "Action"   : "Face"                  , \
                                      "Entry"    : "Acceptor"              , \
                                      "Callback" : FUNC                      }
    self . EmitCallbacks            ( JSOZ                                   )
    ##########################################################################
    self . renderer   . ResetCamera (                                        )
    ##########################################################################
    self . interactor . Initialize  (                                        )
    self . interactor . Start       (                                        )
    ##########################################################################
    return
  ############################################################################
  def startup                       ( self                                 ) :
    ##########################################################################
    self . renderer   . ResetCamera (                                        )
    ##########################################################################
    self . interactor . Initialize  (                                        )
    self . interactor . Start       (                                        )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
