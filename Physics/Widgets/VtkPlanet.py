# -*- coding: utf-8 -*-
##############################################################################
## VtkPlanet
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import math
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
from   AITK  . VTK . VtkWidget        import VtkWidget   as VtkWidget
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
class VtkPlanet                 ( VtkWidget                                ) :
  ############################################################################
  def __init__                  ( self , parent = None , plan = None       ) :
    ##########################################################################
    super ( ) . __init__        (        parent        , plan                )
    self . setVtkPlanetDefaults (                                            )
    ##########################################################################
    return
  ############################################################################
  def setVtkPlanetDefaults ( self                                          ) :
    ##########################################################################
    self . dockingPlace = Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction     ( self . HavingMenu , True                        )
    ##########################################################################
    self . setAcceptDrops  ( True                                            )
    ## self . setDragEnabled  ( True                                            )
    ## self . setDragDropMode ( QAbstractItemView . DragDrop                    )
    ##########################################################################
    self . Actor    = vtk . vtkActor          (                              )
    self . Mapper   = vtk . vtkPolyDataMapper (                              )
    self . Model    = vtk . vtkPolyData       (                              )
    ##########################################################################
    self . Actor    . SetMapper               ( self . Mapper                )
    self . renderer . AddActor                ( self . Actor                 )
    self . Actor    . GetProperty ( ) . SetPointSize ( 1                     )
    ##########################################################################
    self . Sphere = Sphere     (                                             )
    self . Sphere . O . setXYZ (    0.0 ,    0.0 ,    0.0                    )
    self . Sphere . X . setXYZ ( 1000.0 ,    0.0 ,    0.0                    )
    self . Sphere . Y . setXYZ (    0.0 , 1000.0 ,    0.0                    )
    self . Sphere . Z . setXYZ (    0.0 ,    0.0 , 1000.0                    )
    self . Sphere . O . Unit = 108  ## Physics::Kilometer
    self . Sphere . X . Unit = 108  ## Physics::Kilometer
    self . Sphere . Y . Unit = 108  ## Physics::Kilometer
    self . Sphere . Z . Unit = 108  ## Physics::Kilometer
    ##########################################################################
    self . Planet = None
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
  def CreatePlanet                        ( self                           ) :
    ##########################################################################
    JSON       =                          { "Points"       : {           } , \
                                            "Vertices"     : [           ] , \
                                            "Poles"        :               { \
                                              "North"      : -1            , \
                                              "South"      : -1          } , \
                                            "Sectors"      :               { \
                                              "Horizontal" : 0             , \
                                              "Vertical"   : 0             } }
    JSON       = self . Sphere . GeneratePoints ( 0 , JSON                   )
    PIDs       = JSON                     [ "Vertices"                       ]
    self . Planet = JSON
    ##########################################################################
    C    = self . getSystemColor    (                                        )
    R    = C    . red               (                                        )
    G    = C    . green             (                                        )
    B    = C    . blue              (                                        )
    ##########################################################################
    TOTALs     = len                      ( PIDs                             )
    Points     = vtk . vtkPoints          (                                  )
    Vertices   = vtk . vtkCellArray       (                                  )
    ##########################################################################
    Points     . SetNumberOfPoints        ( TOTALs                           )
    Vertices   . InsertNextCell           ( TOTALs                           )
    ##########################################################################
    Colors     = vtk.vtkUnsignedCharArray (                                  )
    Colors     . SetNumberOfComponents    ( 4                                )
    Colors     . SetNumberOfTuples        ( TOTALs                           )
    Colors     . SetName                  ( "Colors"                         )
    ##########################################################################
    for id in PIDs                                                           :
      ########################################################################
      Vertices . InsertCellPoint          ( id                               )
      Colors   . SetTuple4                ( id , R , G , B , 192             )
      ########################################################################
      PS       = JSON [ "Points" ] [ id ] . toList3 (                        )
      Points   . SetPoint                 ( id , PS                          )
    ##########################################################################
    self       . Model . SetPoints        ( Points                           )
    self       . Model . SetVerts         ( Vertices                         )
    self       . Model . GetPointData ( ) . SetScalars ( Colors              )
    self       . Model . Modified         (                                  )
    ##########################################################################
    self       . Mapper   . SetInputData  ( self . Model                     )
    self       . renderer . ResetCamera   (                                  )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    msg    = TRX                   [ "UI::Refresh"                           ]
    icon   = QIcon                 ( ":/images/reload.png"                   )
    mm     . addActionWithIcon     ( 1001 , icon , msg                       )
    ##########################################################################
    msg    = self . getMenuItem    ( "ChangeBackgroundColor"                 )
    mm     . addAction             ( 12871311 , msg                          )
    ##########################################################################
    msg    = "產生行星模型"
    mm     . addAction             ( 12871312 , msg                          )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      ## self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 12871311                        ) :
      ########################################################################
      self . ChangeBackgroundColor (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 12871312                        ) :
      ########################################################################
      self . CreatePlanet          (                                         )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
