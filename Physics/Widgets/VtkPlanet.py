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
    ##########################################################################
    self . Sphere = Sphere (                                                 )
    self . Sphere . R . x = 100000000.0
    self . Sphere . R . y = 100000000.0
    self . Sphere . R . z = 100000000.0
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
  def CreatePlanet                       ( self                            ) :
    ##########################################################################
    source = vtk.vtkSphereSource         (                                   )
    source . SetCenter                   ( 0 , 0 , 0                         )
    source . SetRadius                   ( 5.0                               )
    ##########################################################################
    self   . Mapper . SetInputConnection ( source . GetOutputPort ( )        )
    self   . renderer   . ResetCamera    (                                   )
    ##########################################################################
    """
    source = vtk.vtkSphereSource()
    source . SetCenter(0, 0, 0)
    source . SetRadius(5.0)
    ##########################################################################
    ## Create a mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())
    ##########################################################################
    # Create an actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    ##########################################################################
    self . renderer . AddActor     ( actor )
    
    
    # Create the geometry of a point (the coordinate)
    points = vtk.vtkPoints()
    p = [1.0, 2.0, 3.0]
    
    # Create the topology of the point (a vertex)
    vertices = vtk.vtkCellArray()
    
    id = points.InsertNextPoint(p)
    vertices.InsertNextCell(1)
    vertices.InsertCellPoint(id)
    
    # Create a polydata object
    point = vtk.vtkPolyData()
    
    # Set the points and vertices we created as the geometry and topology of the polydata
    point.SetPoints(points)
    point.SetVerts(vertices)
    
    # Visualize
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(point)
    else:
        mapper.SetInputData(point)
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(20)
    
    self . renderer . AddActor(actor)
    """
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
