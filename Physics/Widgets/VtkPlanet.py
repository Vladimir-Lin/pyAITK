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
from   PyQt5 . QtWidgets              import QFileDialog
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
    self . Colors   =               {                                        }
    self . Colors [ "Point"   ] = ControlPoint (                             )
    self . Colors [ "Line"    ] = ControlPoint (                             )
    self . Colors [ "Polygon" ] = ControlPoint (                             )
    ##########################################################################
    self . Colors [ "Point"   ] . setXYZT      ( 1.0 , 0.0 , 0.0 , 0.75      )
    self . Colors [ "Line"    ] . setXYZT      ( 0.0 , 0.0 , 1.0 , 0.75      )
    self . Colors [ "Polygon" ] . setXYZT      ( 0.5 , 0.8 , 0.6 , 0.75      )
    ##########################################################################
    self . Radius = ControlPoint    (                                        )
    self . Radius . setXYZ          ( 1000.0 , 1000.0 , 1000.0               )
    ##########################################################################
    self . Sphere = Sphere          (                                        )
    self . Sphere . O . setXYZ      (    0.0 ,    0.0 ,    0.0               )
    self . Sphere . setRadiusVector ( self . Radius                          )
    self . Sphere . O . Unit = 108  ## Physics::Kilometer
    self . Sphere . X . Unit = 108  ## Physics::Kilometer
    self . Sphere . Y . Unit = 108  ## Physics::Kilometer
    self . Sphere . Z . Unit = 108  ## Physics::Kilometer
    ##########################################################################
    self . Texture   = vtk . vtkTexture (                                    )
    self . isTexture = False
    ##########################################################################
    self . Planet    = None
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
                                            "Dots"         : [           ] , \
                                            "Lines"        :               { \
                                              "Weft"       : {         }   , \
                                              "Warp"       : {         } } , \
                                            "Polygons"     : [           ] , \
                                            "TPolygons"    : [           ] , \
                                            "TCoords"      : [           ] , \
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
    HH         = JSON                     [ "Sectors"  ] [ "Horizontal"      ]
    VV         = JSON                     [ "Sectors"  ] [ "Vertical"        ]
    ##########################################################################
    R          = int ( self . Colors [ "Point"   ] . x * 255 )
    G          = int ( self . Colors [ "Point"   ] . y * 255 )
    B          = int ( self . Colors [ "Point"   ] . z * 255 )
    T          = int ( self . Colors [ "Point"   ] . t * 255 )
    ##########################################################################
    TOTALs     = len                      ( PIDs                             )
    Points     = vtk . vtkPoints          (                                  )
    Vertices   = vtk . vtkCellArray       (                                  )
    Lines      = vtk . vtkCellArray       (                                  )
    Polygons   = vtk . vtkCellArray       (                                  )
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
      Colors   . SetTuple4                ( id , R , G , B , T               )
      ########################################################################
      PS       = JSON [ "Points" ] [ id ] . toList3 (                        )
      Points   . SetPoint                 ( id , PS                          )
    ##########################################################################
    for id in range                       ( 1 , 12                         ) :
      ########################################################################
      LAT      = int                      ( id * 15                          )
      Lines    . InsertNextCell           ( HH + 1                           )
      ########################################################################
      for PID in JSON [ "Lines" ] [ "Weft" ] [ LAT ]                         :
        ######################################################################
        Lines  . InsertCellPoint          ( PID                              )
    ##########################################################################
    for id in range                       ( 0 , 12                         ) :
      ########################################################################
      LOA      = int                      ( id * 15                          )
      ## CNT      = len ( JSON [ "Lines" ] [ "Vertical" ] [ LOA ] )
      Lines    . InsertNextCell           ( ( VV * 2 ) + 1                   )
      ## Lines    . InsertNextCell           ( CNT                              )
      ########################################################################
      for PID in JSON [ "Lines" ] [ "Warp" ] [ LOA ]                         :
        ######################################################################
        Lines  . InsertCellPoint          ( PID                              )
    ##########################################################################
    for POLY  in JSON                     [ "Polygons"                     ] :
      ########################################################################
      P        = vtk . vtkPolygon         (                                  )
      CNT      = len                      ( POLY                             )
      IDX      = 0
      P        . GetPointIds ( ) . SetNumberOfIds ( CNT                      )
      ########################################################################
      for PID in POLY                                                        :
        ######################################################################
        P      . GetPointIds ( ) . SetId  ( IDX , PID                        )
        ######################################################################
        IDX    = IDX + 1
      ########################################################################
      Polygons . InsertNextCell           ( P                                )
    ##########################################################################
    self       . Model . SetPoints        ( Points                           )
    self       . Model . SetVerts         ( Vertices                         )
    self       . Model . SetLines         ( Lines                            )
    self       . Model . SetPolys         ( Polygons                         )
    self       . Model . GetPointData ( ) . SetScalars ( Colors              )
    self       . Model . Modified         (                                  )
    ##########################################################################
    self       . Mapper   . SetInputData  ( self . Model                     )
    self       . renderer . ResetCamera   (                                  )
    ##########################################################################
    return
  ############################################################################
  """
  graphic_name = "../textures/"+planet.get_name()+".jpg"
              graphic_reader = vtk.vtkJPEGReader()
              graphic_reader.SetFileName(graphic_name)
              graphic_texture = vtk.vtkTexture()
              graphic_texture.SetInputConnection(graphic_reader.GetOutputPort())
              graphic_texture.InterpolateOn()
              actor.SetTexture(graphic_texture)
  """
  ############################################################################
  ############################################################################
  ############################################################################
  def LoadTexture                           ( self                         ) :
    ##########################################################################
    FILTERS = self . getMenuItem            ( "OpenImageFilters"             )
    F , _   = QFileDialog . getOpenFileName ( self                           ,
                                              "載入材質圖片" ,
                                              ""                             ,
                                              FILTERS                        )
    ##########################################################################
    if                                      ( len ( F ) <= 0               ) :
      return
    ##########################################################################
    print(F)
    ##########################################################################
    return
  ############################################################################
  def RenderMenu               ( self , mm                                 ) :
    ##########################################################################
    MSG   = self . getMenuItem ( "RenderParameters"                          )
    LOM   = mm   . addMenu     ( MSG                                         )
    ##########################################################################
    msg   = self . getMenuItem ( "ChangeBackgroundColor"                     )
    mm    . addActionFromMenu  ( LOM , 54231101 , msg                        )
    ##########################################################################
    msg   = self . getMenuItem ( "ImportTexture"                             )
    mm    . addActionFromMenu  ( LOM , 54232001 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunRenderMenu                ( self , at                             ) :
    ##########################################################################
    if                             ( at == 54231101                        ) :
      ########################################################################
      self . ChangeBackgroundColor (                                         )
      ########################################################################
      return
    ##########################################################################
    if                             ( at == 54232001                        ) :
      ########################################################################
      self . LoadTexture           (                                         )
      ########################################################################
      return
    ##########################################################################
    return False
  ############################################################################
  def GeometryMenu             ( self , mm                                 ) :
    ##########################################################################
    MSG   = self . getMenuItem ( "ModelParameters"                           )
    LOM   = mm   . addMenu     ( MSG                                         )
    ##########################################################################
    msg   = self . getMenuItem ( "CreatePlanet"                              )
    mm    . addActionFromMenu  ( LOM , 54235201 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunGeometryMenu     ( self , at                                      ) :
    ##########################################################################
    if                    ( at == 54235201                                 ) :
      ########################################################################
      self . CreatePlanet (                                                  )
      ########################################################################
      return
    ##########################################################################
    return False
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
    msg    = self . getMenuItem    ( "ImportModel"                           )
    mm     . addAction             ( 12876001 , msg                          )
    ##########################################################################
    msg    = self . getMenuItem    ( "ExportModel"                           )
    mm     . addAction             ( 12876002 , msg                          )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . GeometryMenu          ( mm                                      )
    self   . RenderMenu            ( mm                                      )
    ## self   . LocalityMenu          ( mm                                      )
    ## self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunRenderMenu   ( at )         ) :
      return True
    ##########################################################################
    if                             ( self . RunGeometryMenu ( at )         ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      ## self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 12876001                        ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 12876002                        ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
