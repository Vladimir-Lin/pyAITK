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
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QDoubleSpinBox
##############################################################################
from   AITK  . VTK . VtkWidget        import VtkWidget   as VtkWidget
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
class VtkPlanet                 ( VtkWidget                                ) :
  ############################################################################
  emitRenderWindow = pyqtSignal (                                            )
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
    ## self . dockingPlace = Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction     ( self . HavingMenu , True                        )
    ##########################################################################
    self . setAcceptDrops  ( True                                            )
    ## self . setDragEnabled  ( True                                            )
    ## self . setDragDropMode ( QAbstractItemView . DragDrop                    )
    ##########################################################################
    self . emitRenderWindow . connect ( self . DoRenderWindow                )
    ##########################################################################
    self . DoRotation     = False
    self . RotateAngle    = 0.5
    self . RotateInterval = 0.1
    self . PrepareObjects  (                                                 )
    self . SpinBoxs =      {                                                 }
    ##########################################################################
    return
  ############################################################################
  def PrepareObjects             ( self                                    ) :
    ##########################################################################
    NAMEs    =                   [ "Points"                                , \
                                   "Lines"                                 , \
                                   "Polygons"                              , \
                                   "Texture"                               , \
                                   "Atmosphere"                            , \
                                   "Shadow"                                  ]
    self     . PlanetObjects =   {                                           }
    self     . ObjectNAMEs   = NAMEs
    ##########################################################################
    TAS      =                   [ "Texture" , "Atmosphere"                  ]
    self . Radius = ControlPoint (                                           )
    self . Radius . setXYZ       ( 1000.0 , 1000.0 , 1000.0                  )
    ##########################################################################
    CACT = [ "Planet" , "Surface" , "Lighting" , "Label" , "Attachment"      ]
    for NAME in CACT                                                         :
      ########################################################################
      ZF   = vtk . vtkTransformFilter   (                                    )
      F    = vtk . vtkTransform         (                                    )
      F    . Identity                   (                                    )
      A    = vtk . vtkAssembly          (                                    )
      ########################################################################
      self . PlanetObjects [ NAME ] =   {                                    }
      self . PlanetObjects [ NAME ] [ "Actor"     ] = A
      self . PlanetObjects [ NAME ] [ "Transform" ] = F
      self . PlanetObjects [ NAME ] [ "TFilter"   ] = ZF
      self . PlanetObjects [ NAME ] [ "Mapper"    ] = None
      self . PlanetObjects [ NAME ] [ "Model"     ] = None
      self . PlanetObjects [ NAME ] [ "Sphere"    ] = None
      self . PlanetObjects [ NAME ] [ "Color"     ] = ControlPoint (         )
      self . PlanetObjects [ NAME ] [ "Texture"   ] = None
      self . PlanetObjects [ NAME ] [ "Loaded"    ] = False
      self . PlanetObjects [ NAME ] [ "Distance"  ] = 0.0
      self . PlanetObjects [ NAME ] [ "Enabled"   ] = True
      self . PlanetObjects [ NAME ] [ "JSON"      ] = {                      }
      ########################################################################
      self . renderer . AddActor        ( A                                  )
    ##########################################################################
    PLANETs = [ "Points" , "Lines" , "Polygons" , "Texture" ]
    PA      = self . PlanetObjects [ "Planet" ] [ "Actor" ]
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      E      = True
      T      = None
      ########################################################################
      if                         ( NAME in TAS                             ) :
        ######################################################################
        E    = False
        T    = vtk . vtkTexture  (                                           )
      ########################################################################
      A      = vtk . vtkActor           (                                    )
      D      = vtk . vtkPolyDataMapper  (                                    )
      M      = vtk . vtkPolyData        (                                    )
      F      = vtk . vtkTransform       (                                    )
      ZF     = vtk . vtkTransformFilter (                                    )
      ########################################################################
      F      . Identity                 (                                    )
      ZF     . SetTransform             ( F                                  )
      ########################################################################
      A      . SetMapper                ( D                                  )
      A      . GetProperty ( ) . SetPointSize ( 1                            )
      ########################################################################
      if                                ( E                                ) :
        ######################################################################
        if                              ( NAME in PLANETs                  ) :
          PA   . AddPart                ( A                                  )
        else                                                                 :
          self . renderer . AddActor    ( A                                  )
      ########################################################################
      C      = ControlPoint             (                                    )
      ########################################################################
      S      = Sphere                   (                                    )
      S      . O  . setXYZ              (    0.0 ,    0.0 ,    0.0           )
      S      . setRadiusVector          ( self . Radius                      )
      S      . O . Unit = 108  ## Physics::Kilometer
      S      . X . Unit = 108  ## Physics::Kilometer
      S      . Y . Unit = 108  ## Physics::Kilometer
      S      . Z . Unit = 108  ## Physics::Kilometer
      ########################################################################
      self   . PlanetObjects [ NAME ] = {                                    }
      self   . PlanetObjects [ NAME ] [ "Actor"     ] = A
      self   . PlanetObjects [ NAME ] [ "Transform" ] = F
      self   . PlanetObjects [ NAME ] [ "TFilter"   ] = ZF
      self   . PlanetObjects [ NAME ] [ "Mapper"    ] = D
      self   . PlanetObjects [ NAME ] [ "Model"     ] = M
      self   . PlanetObjects [ NAME ] [ "Sphere"    ] = S
      self   . PlanetObjects [ NAME ] [ "Color"     ] = C
      self   . PlanetObjects [ NAME ] [ "Texture"   ] = T
      self   . PlanetObjects [ NAME ] [ "Loaded"    ] = False
      self   . PlanetObjects [ NAME ] [ "Distance"  ] = 0.0
      self   . PlanetObjects [ NAME ] [ "Enabled"   ] = E
      self   . PlanetObjects [ NAME ] [ "JSON"      ] = {                    }
    ##########################################################################
    PP       = ControlPoint             (                                    )
    PL       = ControlPoint             (                                    )
    PG       = ControlPoint             (                                    )
    PW       = ControlPoint             (                                    )
    ##########################################################################
    PP       . setXYZT                  ( 0.23 , 0.97 , 0.90 , 0.75          )
    PL       . setXYZT                  ( 0.0  , 1.0  , 0.0  , 0.75          )
    PG       . setXYZT                  ( 0.8  , 0.8  , 0.8  , 0.25          )
    PW       . setXYZT                  ( 0.0  , 0.0  , 0.0  , 0.20          )
    ##########################################################################
    self . PlanetObjects [ "Points"     ] [ "Color"    ] . assign ( PP       )
    self . PlanetObjects [ "Lines"      ] [ "Color"    ] . assign ( PL       )
    self . PlanetObjects [ "Polygons"   ] [ "Color"    ] . assign ( PG       )
    self . PlanetObjects [ "Shadow"     ] [ "Color"    ] . assign ( PW       )
    ##########################################################################
    self . PlanetObjects [ "Points"     ] [ "Distance" ] = 0.030
    self . PlanetObjects [ "Lines"      ] [ "Distance" ] = 0.020
    self . PlanetObjects [ "Polygons"   ] [ "Distance" ] = 0.010
    self . PlanetObjects [ "Atmosphere" ] [ "Distance" ] = 2.0
    self . PlanetObjects [ "Shadow"     ] [ "Distance" ] = 1.0
    ##########################################################################
    A    = self . PlanetObjects [ "Points"     ] [ "Actor" ]
    A    . GetProperty ( ) . SetPointSize ( 1.25                             )
    ##########################################################################
    A    = self . PlanetObjects [ "Lines"      ] [ "Actor" ]
    A    . GetProperty ( ) . SetLineWidth ( 2.0                              )
    ##########################################################################
    A    = self . PlanetObjects [ "Atmosphere" ] [ "Actor" ]
    A    . GetProperty ( ) . SetOpacity ( 0.25                               )
    ##########################################################################
    A    = self . PlanetObjects [ "Shadow"     ] [ "Actor" ]
    A    . GetProperty ( ) . SetOpacity ( 0.40                               )
    ##########################################################################
    self . setRadius                    ( self . Radius                      )
    self . Shadow = None
    ##########################################################################
    ZF   = vtk . vtkTransformFilter     (                                    )
    F    = vtk . vtkTransform           (                                    )
    F    . Identity                     (                                    )
    ##########################################################################
    self . PlanetObjects [ "Axis" ] =   {                                    }
    self . PlanetObjects [ "Axis" ] [ "Actor"     ] = None
    self . PlanetObjects [ "Axis" ] [ "Transform" ] = F
    self . PlanetObjects [ "Axis" ] [ "TFilter"   ] = ZF
    self . PlanetObjects [ "Axis" ] [ "Mapper"    ] = None
    self . PlanetObjects [ "Axis" ] [ "Model"     ] = None
    self . PlanetObjects [ "Axis" ] [ "Sphere"    ] = None
    self . PlanetObjects [ "Axis" ] [ "Color"     ] = PW
    self . PlanetObjects [ "Axis" ] [ "Texture"   ] = None
    self . PlanetObjects [ "Axis" ] [ "Loaded"    ] = False
    self . PlanetObjects [ "Axis" ] [ "Distance"  ] = 0.0
    self . PlanetObjects [ "Axis" ] [ "Enabled"   ] = False
    self . PlanetObjects [ "Axis" ] [ "JSON"      ] = {                      }
    ##########################################################################
    return
  ############################################################################
  def SyncSystemColor                 ( self , Name                        ) :
    ##########################################################################
    Z    = self . PlanetObjects       [ Name ] [ "Color"                     ]
    C    = self . getSystemColor      (                                      )
    R    = C    . redF                (                                      )
    G    = C    . greenF              (                                      )
    B    = C    . blueF               (                                      )
    T    = Z    . t
    ##########################################################################
    PW   = ControlPoint               (                                      )
    PW   . setXYZT                    ( R , G , B , T                        )
    ##########################################################################
    self . PlanetObjects  [ Name ] [ "Color" ] = PW
    ##########################################################################
    A    = self . PlanetObjects       [ Name ] [ "Actor"                     ]
    A    . GetProperty ( ) . SetColor ( R , G , B                            )
    ##########################################################################
    return
  ############################################################################
  def GetRadius              ( self , R , Name                             ) :
    ##########################################################################
    D = self . PlanetObjects [ Name ] [ "Distance"                           ]
    ##########################################################################
    X = ControlPoint         (                                               )
    X . setXYZ               ( R . x + D , R . y + D , R . z + D             )
    ##########################################################################
    return X
  ############################################################################
  def setRadius                     ( self , R                             ) :
    ##########################################################################
    self . Radius . assign          ( R                                      )
    ##########################################################################
    self . PlanetObjects [ "Texture"    ] [ "Sphere" ] . setRadiusVector ( R )
    ##########################################################################
    X    = self . GetRadius         ( R , "Points"                           )
    self . PlanetObjects [ "Points"     ] [ "Sphere" ] . setRadiusVector ( X )
    ##########################################################################
    X    = self . GetRadius         ( R , "Lines"                            )
    self . PlanetObjects [ "Lines"      ] [ "Sphere" ] . setRadiusVector ( X )
    ##########################################################################
    X    = self . GetRadius         ( R , "Polygons"                         )
    self . PlanetObjects [ "Polygons"   ] [ "Sphere" ] . setRadiusVector ( X )
    ##########################################################################
    X    = self . GetRadius         ( R , "Atmosphere"                       )
    self . PlanetObjects [ "Atmosphere" ] [ "Sphere" ] . setRadiusVector ( X )
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
  def PreparePoints                            ( self , Item               ) :
    ##########################################################################
    E          = self . PlanetObjects [ Item ] [ "Enabled"                   ]
    if                                         ( not E                     ) :
      return
    ##########################################################################
    JSON       = self . PlanetObjects [ Item ] [ "JSON"                      ]
    ACTOR      = self . PlanetObjects [ Item ] [ "Actor"                     ]
    MAPPER     = self . PlanetObjects [ Item ] [ "Mapper"                    ]
    MODEL      = self . PlanetObjects [ Item ] [ "Model"                     ]
    ##########################################################################
    C          = self . PlanetObjects [ Item ] [ "Color"                     ]
    R          = int                           ( C . x * 255                 )
    G          = int                           ( C . y * 255                 )
    B          = int                           ( C . z * 255                 )
    T          = int                           ( C . t * 255                 )
    ##########################################################################
    PIDs       = JSON                          [ "Vertices"                  ]
    DOTs       = JSON                          [ "Dots"                      ]
    ##########################################################################
    TOTALs     = len                           ( PIDs                        )
    PIXELs     = len                           ( DOTs                        )
    Points     = vtk . vtkPoints               (                             )
    Vertices   = vtk . vtkCellArray            (                             )
    ##########################################################################
    Points     . SetNumberOfPoints             ( TOTALs                      )
    Vertices   . InsertNextCell                ( PIXELs                      )
    ##########################################################################
    Colors     = vtk . vtkUnsignedCharArray    (                             )
    Colors     . SetNumberOfComponents         ( 4                           )
    Colors     . SetNumberOfTuples             ( TOTALs                      )
    Colors     . SetName                       ( "Colors"                    )
    ##########################################################################
    for id in PIDs                                                           :
      ########################################################################
      Colors   . SetTuple4                     ( id , R , G , B , T          )
      PS       = JSON [ "Points" ] [ id ] . toList3 (                        )
      Points   . SetPoint                      ( id , PS                     )
    ##########################################################################
    for id in DOTs                                                           :
      ########################################################################
      Vertices . InsertCellPoint               ( id                          )
    ##########################################################################
    MODEL      . SetPoints                     ( Points                      )
    MODEL      . SetVerts                      ( Vertices                    )
    MODEL      . GetPointData ( ) . SetScalars ( Colors                      )
    MODEL      . Modified                      (                             )
    ##########################################################################
    MAPPER     . SetInputData                  ( MODEL                       )
    ##########################################################################
    ########################################################################
    ## ZF     . SetInputData             ( mesh                               )
    ## D      . SetInputConnection       ( ZF . GetOutputPort ( )             )
    ## A      . SetMapper                ( D                                  )
    return
  ############################################################################
  def PrepareLines                    ( self , Item                        ) :
    ##########################################################################
    E          = self . PlanetObjects [ Item ] [ "Enabled"                   ]
    if                                ( not E                              ) :
      return
    ##########################################################################
    JSON       = self . PlanetObjects [ Item ] [ "JSON"                      ]
    ACTOR      = self . PlanetObjects [ Item ] [ "Actor"                     ]
    MAPPER     = self . PlanetObjects [ Item ] [ "Mapper"                    ]
    MODEL      = self . PlanetObjects [ Item ] [ "Model"                     ]
    ##########################################################################
    C          = self . PlanetObjects [ Item ] [ "Color"                     ]
    R          = int                           ( C . x * 255                 )
    G          = int                           ( C . y * 255                 )
    B          = int                           ( C . z * 255                 )
    T          = int                           ( C . t * 255                 )
    ##########################################################################
    HH         = JSON                          [ "Sectors"  ] [ "Horizontal" ]
    VV         = JSON                          [ "Sectors"  ] [ "Vertical"   ]
    PIDs       = JSON                          [ "Vertices"                  ]
    ##########################################################################
    TOTALs     = len                           ( PIDs                        )
    Points     = vtk . vtkPoints               (                             )
    Lines      = vtk . vtkCellArray            (                             )
    ##########################################################################
    Points     . SetNumberOfPoints             ( TOTALs                      )
    ##########################################################################
    Colors     = vtk.vtkUnsignedCharArray      (                             )
    Colors     . SetNumberOfComponents         ( 4                           )
    Colors     . SetNumberOfTuples             ( TOTALs                      )
    Colors     . SetName                       ( "Colors"                    )
    ##########################################################################
    for id in PIDs                                                           :
      ########################################################################
      Colors   . SetTuple4                     ( id , R , G , B , T          )
      PS       = JSON [ "Points" ] [ id ] . toList3 (                        )
      Points   . SetPoint                      ( id , PS                     )
    ##########################################################################
    for id in range                            ( 1 , 12                    ) :
      ########################################################################
      LAT      = int                           ( id * 15                     )
      Lines    . InsertNextCell                ( HH + 1                      )
      ########################################################################
      for PID in JSON [ "Lines" ] [ "Weft" ] [ LAT ]                         :
        ######################################################################
        Lines  . InsertCellPoint               ( PID                         )
    ##########################################################################
    for id in range                            ( 0 , 12                    ) :
      ########################################################################
      LOA      = int                           ( id * 15                     )
      Lines    . InsertNextCell                ( ( VV * 2 ) + 1              )
      ########################################################################
      for PID in JSON [ "Lines" ] [ "Warp" ] [ LOA ]                         :
        ######################################################################
        Lines  . InsertCellPoint               ( PID                         )
    ##########################################################################
    MODEL      . SetPoints                     ( Points                      )
    MODEL      . SetLines                      ( Lines                       )
    MODEL      . GetPointData ( ) . SetScalars ( Colors                      )
    MODEL      . Modified                      (                             )
    ##########################################################################
    MAPPER     . SetInputData                  ( MODEL                       )
    ##########################################################################
    return
  ############################################################################
  def PreparePolygons                     ( self , Item                    ) :
    ##########################################################################
    E          = self . PlanetObjects     [ Item ] [ "Enabled"               ]
    if                                    ( not E                          ) :
      return
    ##########################################################################
    JSON       = self . PlanetObjects     [ Item ] [ "JSON"                  ]
    ACTOR      = self . PlanetObjects     [ Item ] [ "Actor"                 ]
    MAPPER     = self . PlanetObjects     [ Item ] [ "Mapper"                ]
    MODEL      = self . PlanetObjects     [ Item ] [ "Model"                 ]
    ##########################################################################
    C          = self . PlanetObjects     [ Item ] [ "Color"                 ]
    R          = int                      ( C . x * 255                      )
    G          = int                      ( C . y * 255                      )
    B          = int                      ( C . z * 255                      )
    T          = int                      ( C . t * 255                      )
    ##########################################################################
    HH         = JSON                     [ "Sectors"  ] [ "Horizontal"      ]
    VV         = JSON                     [ "Sectors"  ] [ "Vertical"        ]
    PIDs       = JSON                     [ "Vertices"                       ]
    ##########################################################################
    TOTALs     = len                      ( PIDs                             )
    Points     = vtk . vtkPoints          (                                  )
    Polygons   = vtk . vtkCellArray       (                                  )
    ##########################################################################
    Points     . SetNumberOfPoints        ( TOTALs                           )
    ##########################################################################
    Colors     = vtk.vtkUnsignedCharArray (                                  )
    Colors     . SetNumberOfComponents    ( 4                                )
    Colors     . SetNumberOfTuples        ( TOTALs                           )
    Colors     . SetName                  ( "Colors"                         )
    ##########################################################################
    for id in PIDs                                                           :
      ########################################################################
      Colors   . SetTuple4                ( id , R , G , B , T               )
      PS       = JSON [ "Points" ] [ id ] . toList3 (                        )
      Points   . SetPoint                 ( id , PS                          )
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
    MODEL      . SetPoints                ( Points                           )
    MODEL      . SetPolys                 ( Polygons                         )
    MODEL      . GetPointData ( ) . SetScalars ( Colors                      )
    MODEL      . Modified                 (                                  )
    ##########################################################################
    MAPPER     . SetInputData             ( MODEL                            )
    ##########################################################################
    return
  ############################################################################
  def PrepareShadow                       ( self , Item                    ) :
    ##########################################################################
    E          = self . PlanetObjects     [ Item ] [ "Enabled"               ]
    if                                    ( not E                          ) :
      return
    ##########################################################################
    JSON       = self . PlanetObjects     [ Item ] [ "JSON"                  ]
    ACTOR      = self . PlanetObjects     [ Item ] [ "Actor"                 ]
    MAPPER     = self . PlanetObjects     [ Item ] [ "Mapper"                ]
    MODEL      = self . PlanetObjects     [ Item ] [ "Model"                 ]
    ##########################################################################
    C          = self . PlanetObjects     [ Item ] [ "Color"                 ]
    R          = int                      ( C . x * 255                      )
    G          = int                      ( C . y * 255                      )
    B          = int                      ( C . z * 255                      )
    T          = int                      ( C . t * 255                      )
    ##########################################################################
    HH         = JSON                     [ "Sectors"  ] [ "Horizontal"      ]
    VV         = JSON                     [ "Sectors"  ] [ "Vertical"        ]
    PIDs       = JSON                     [ "Vertices"                       ]
    ##########################################################################
    TOTALs     = len                      ( PIDs                             )
    Points     = vtk . vtkPoints          (                                  )
    Polygons   = vtk . vtkCellArray       (                                  )
    ##########################################################################
    Points     . SetNumberOfPoints        ( TOTALs                           )
    ##########################################################################
    Colors     = vtk.vtkUnsignedCharArray (                                  )
    Colors     . SetNumberOfComponents    ( 4                                )
    Colors     . SetNumberOfTuples        ( TOTALs                           )
    Colors     . SetName                  ( "Colors"                         )
    ##########################################################################
    SHADOW     = self . Shadow
    ##########################################################################
    for id in PIDs                                                           :
      ########################################################################
      if                                  ( self . IsOkay ( SHADOW )       ) :
        ######################################################################
        R      = SHADOW . x
        G      = SHADOW . y
        B      = SHADOW . z
        T      = SHADOW . t
      ########################################################################
      Colors   . SetTuple4                ( id , R , G , B , T               )
      PS       = JSON [ "Points" ] [ id ] . toList3 (                        )
      Points   . SetPoint                 ( id , PS                          )
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
    MODEL      . SetPoints                ( Points                           )
    MODEL      . SetPolys                 ( Polygons                         )
    MODEL      . GetPointData ( ) . SetScalars ( Colors                      )
    MODEL      . Modified                 (                                  )
    ##########################################################################
    MAPPER     . SetInputData             ( MODEL                            )
    ##########################################################################
    return
  ############################################################################
  def PrepareTexture                      ( self , Item                    ) :
    ##########################################################################
    E          = self . PlanetObjects     [ Item ] [ "Enabled"               ]
    LOADED     = self . PlanetObjects     [ Item ] [ "Loaded"                ]
    ##########################################################################
    if                                    ( not E                          ) :
      return
    if                                    ( not LOADED                     ) :
      return
    ##########################################################################
    JSON       = self . PlanetObjects     [ Item ] [ "JSON"                  ]
    ACTOR      = self . PlanetObjects     [ Item ] [ "Actor"                 ]
    MAPPER     = self . PlanetObjects     [ Item ] [ "Mapper"                ]
    MODEL      = self . PlanetObjects     [ Item ] [ "Model"                 ]
    TEXTURE    = self . PlanetObjects     [ Item ] [ "Texture"               ]
    ##########################################################################
    C          = self . PlanetObjects     [ Item ] [ "Color"                 ]
    R          = int                      ( C . x * 255                      )
    G          = int                      ( C . y * 255                      )
    B          = int                      ( C . z * 255                      )
    T          = int                      ( C . t * 255                      )
    ##########################################################################
    HH         = JSON                     [ "Sectors"  ] [ "Horizontal"      ]
    VV         = JSON                     [ "Sectors"  ] [ "Vertical"        ]
    KIDs       = JSON                     [ "TPoints"                        ]
    PIDs       = KIDs . keys              (                                  )
    ##########################################################################
    TOTALs     = len                      ( PIDs                             )
    AT         = 0
    Points     = vtk . vtkPoints          (                                  )
    Polygons   = vtk . vtkCellArray       (                                  )
    TCoords    = vtk . vtkFloatArray      (                                  )
    ##########################################################################
    Points     . SetNumberOfPoints        ( TOTALs                           )
    TCoords    . SetNumberOfComponents    ( 2                                )
    TCoords    . SetNumberOfTuples        ( TOTALs                           )
    TCoords    . SetName                  ( "TextureCoordinates"             )
    ##########################################################################
    for id in PIDs                                                           :
      ########################################################################
      PS       = JSON [ "TPoints" ] [ id ] . toList3 (                       )
      CR       = JSON [ "TCoords" ] [ AT                                     ]
      Points   . SetPoint                 ( id , PS                          )
      TCoords  . SetTuple2                ( id , CR . x , CR . y             )
      ########################################################################
      AT       = AT + 1
    ##########################################################################
    for POLY  in JSON                     [ "TPolygons"                    ] :
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
    MODEL      . SetPoints                ( Points                           )
    MODEL      . SetPolys                 ( Polygons                         )
    MODEL      . GetPointData ( ) . SetTCoords ( TCoords                     )
    MODEL      . Modified                 (                                  )
    ##########################################################################
    MAPPER     . SetInputData             ( MODEL                            )
    ##########################################################################
    return
  ############################################################################
  def PrepareAxis                 ( self                                   ) :
    ##########################################################################
    X    = float                  ( self . Radius . x * 1.25                 )
    Y    = float                  ( self . Radius . y * 1.25                 )
    Z    = float                  ( self . Radius . z * 1.25                 )
    ##########################################################################
    F    = self . PlanetObjects   [ "Axis" ] [ "Transform"                   ]
    AXES = vtk  . vtkAxesActor    (                                          )
    AXES . SetUserTransform       ( F                                        )
    AXES . SetShaftTypeToCylinder (                                          )
    AXES . SetXAxisLabelText      ( "0°"                                     )
    AXES . SetYAxisLabelText      ( "90°"                                    )
    AXES . SetZAxisLabelText      ( "N"                                      )
    AXES . SetTotalLength         ( X , Y , Z                                )
    AXES . SetNormalizedTipLength   ( 0.05  , 0.05  , 0.05                   )
    AXES . SetNormalizedShaftLength ( 0.953 , 0.953 , 0.953                  )
    AXES . SetConeResolution      ( 360                                      )
    AXES . SetConeRadius          ( 0.4                                      )
    AXES . SetCylinderResolution  ( 360                                      )
    AXES . SetCylinderRadius      ( 0.005                                    )
    ##########################################################################
    PROP = vtk . vtkTextProperty  (                                          )
    PROP . SetFontSize            ( 32                                       )
    PROP . SetColor               ( 216.0/255.0 , 216.0/255.0 , 216.0/255.0  )
    ##########################################################################
    TA   = AXES . GetXAxisCaptionActor2D (                                   )
    TA   . GetTextActor ( ) . SetTextScaleModeToNone (                       )
    TA   . SetCaptionTextProperty ( PROP                                     )
    ##########################################################################
    TA   = AXES . GetYAxisCaptionActor2D (                                   )
    TA   . GetTextActor ( ) . SetTextScaleModeToNone (                       )
    TA   . SetCaptionTextProperty ( PROP                                     )
    ##########################################################################
    TA   = AXES . GetZAxisCaptionActor2D (                                   )
    TA   . GetTextActor ( ) . SetTextScaleModeToNone (                       )
    TA   . SetCaptionTextProperty ( PROP                                     )
    ##########################################################################
    self . PlanetObjects [ "Axis" ] [ "Actor"   ] = AXES
    ##########################################################################
    return
  ############################################################################
  def CreatePlanet                    ( self                               ) :
    ##########################################################################
    NAMEs    = self . ObjectNAMEs
    self     . setRadius              ( self . Radius                        )
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      JSON   = self . PlanetObjects   [ NAME ] [ "Sphere" ] . GenerateMesh ( )
      self   . PlanetObjects [ NAME ] [ "JSON" ] = JSON
    ##########################################################################
    E        = self . PlanetObjects   [ "Points"   ] [ "Enabled"             ]
    if                                ( E                                  ) :
      self   . PreparePoints          ( "Points"                             )
    ##########################################################################
    E        = self . PlanetObjects   [ "Lines"    ] [ "Enabled"             ]
    if                                ( E                                  ) :
      self   . PrepareLines           ( "Lines"                              )
    ##########################################################################
    E        = self . PlanetObjects   [ "Polygons" ] [ "Enabled"             ]
    if                                ( E                                  ) :
      self   . PreparePolygons        ( "Polygons"                           )
    ##########################################################################
    E        = self . PlanetObjects   [ "Shadow"   ] [ "Enabled"             ]
    if                                ( E                                  ) :
      self   . PrepareShadow          ( "Shadow"                             )
    ##########################################################################
    for NAME in                       [ "Texture" , "Atmosphere"           ] :
      ########################################################################
      E      = self . PlanetObjects   [ NAME       ] [ "Enabled"             ]
      if                              ( E                                  ) :
        self . PrepareTexture         ( NAME                                 )
    ##########################################################################
    self     . PrepareAxis            (                                      )
    ##########################################################################
    self     . renderer . ResetCamera (                                      )
    ##########################################################################
    camera   = self . renderer . GetActiveCamera (                           )
    ## CX       = float                  ( self . Radius . x * 4                )
    ## CY       = float                  ( self . Radius . y * 4                )
    ## CZ       = float                  ( self . Radius . z / 4                )
    ## camera   . SetFocalPoint          ( 0 ,  0 , 0                           )
    ## camera   . SetPosition            ( 0 , CY , 0                           )
    ## camera   . SetViewUp              ( 0 ,  0 , 1                           )
    ## camera   . SetRoll                ( 110.0                                )
    ## camera   . SetViewAngle           ( 30.0                                 )
    ##########################################################################
    self     . emitRenderWindow . emit (                                     )
    self     . Notify                  ( 5                                   )
    ##########################################################################
    return
  ############################################################################
  def DoRenderWindow        ( self                                         ) :
    ##########################################################################
    self . rWindow . Render (                                                )
    ##########################################################################
    return
  ############################################################################
  def RunRotation                    ( self                                ) :
    ##########################################################################
    self   . DoRotation = True
    ##########################################################################
    PA     = self . PlanetObjects [ "Planet" ] [ "Actor"                     ]
    AX     = self . PlanetObjects [ "Axis"   ] [ "Actor"                     ]
    ##########################################################################
    while                            ( self . DoRotation                   ) :
      ########################################################################
      PA   . RotateZ                 ( self . RotateAngle                    )
      self . emitRenderWindow . emit (                                       )
      time . sleep                   ( self . RotateInterval                 )
      ########################################################################
    return
  ############################################################################
  def TriggerRotation ( self                                               ) :
    ##########################################################################
    if                ( self . DoRotation                                  ) :
      ########################################################################
      self . DoRotation = False
      ########################################################################
      return
    ##########################################################################
    self . Go         ( self . RunRotation                                   )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  def LoadTextureForItem                     ( self , Item                 ) :
    ##########################################################################
    FILTERS  = self . getMenuItem            ( "OpenImageFilters"            )
    F , _    = QFileDialog . getOpenFileName ( self                          ,
                                               "載入材質圖片" ,
                                               ""                            ,
                                               FILTERS                       )
    ##########################################################################
    if                                       ( len ( F ) <= 0              ) :
      return
    ##########################################################################
    T        = self   . PlanetObjects        [ Item ] [ "Texture"            ]
    A        = self   . PlanetObjects        [ Item ] [ "Actor"              ]
    E        = self   . PlanetObjects        [ Item ] [ "Enabled"            ]
    ##########################################################################
    if                                       ( ".png" in F                 ) :
      Reader = vtk . vtkPNGReader            (                               )
    else                                                                     :
      Reader = vtk . vtkJPEGReader           (                               )
    ##########################################################################
    Reader   . SetFileName                   ( F                             )
    ##########################################################################
    T        . SetInputConnection            ( Reader . GetOutputPort ( )    )
    T        . InterpolateOn                 (                               )
    A        . SetTexture                    ( T                             )
    ##########################################################################
    self     . Notify                        ( 5                             )
    ##########################################################################
    if                                       ( E                           ) :
      return
    ##########################################################################
    PLANETs  = [ "Points" , "Lines" , "Polygons" , "Texture"                 ]
    PA       = self . PlanetObjects [ "Planet" ] [ "Actor"                   ]
    ##########################################################################
    if                           ( Item in PLANETs                         ) :
      PA   . AddPart             ( A                                         )
    else                                                                     :
      self . renderer . AddActor ( A                                         )
    ##########################################################################
    self     . PlanetObjects [ Item  ] [ "Enabled" ] = True
    self     . PlanetObjects [ Item  ] [ "Loaded"  ] = True
    ##########################################################################
    return
  ############################################################################
  def SwitchDisplayElement            ( self , Item                        ) :
    ##########################################################################
    E        = self . PlanetObjects   [ Item ] [ "Enabled"                   ]
    A        = self . PlanetObjects   [ Item ] [ "Actor"                     ]
    ##########################################################################
    PLANETs  = [ "Axis" , "Points" , "Lines" , "Polygons" , "Texture"        ]
    ## PLANETs  = [ "Points" , "Lines" , "Polygons" , "Texture"                 ]
    ##########################################################################
    if                                ( E                                  ) :
      ########################################################################
      E      = False
      ########################################################################
      if                              ( Item in PLANETs                    ) :
        ######################################################################
        S    = self . PlanetObjects   [ "Planet" ] [ "Actor"                 ]
        S    . RemovePart             ( A                                    )
        ######################################################################
      else                                                                   :
        self . renderer . RemoveActor ( A                                    )
      ########################################################################
    else                                                                     :
      ########################################################################
      E      = True
      ########################################################################
      if                              ( Item in PLANETs                    ) :
        ######################################################################
        S    = self . PlanetObjects   [ "Planet" ] [ "Actor"                 ]
        S    . AddPart                ( A                                    )
        ######################################################################
      else                                                                   :
        self . renderer . AddActor    ( A                                    )
    ##########################################################################
    self     . PlanetObjects [ Item ] [ "Enabled" ] = E
    ##########################################################################
    return
  ############################################################################
  def GetMenuParameters           ( self , at                              ) :
    ##########################################################################
    WT   = self . SpinBoxs [ "WindowTitle" ] . text (                        )
    self . setWindowTitle         ( WT                                       )
    ##########################################################################
    self . Radius . x = self . SpinBoxs [ "RadiusX" ] . value ( ) / 1000.0
    self . Radius . y = self . SpinBoxs [ "RadiusY" ] . value ( ) / 1000.0
    self . Radius . z = self . SpinBoxs [ "RadiusZ" ] . value ( ) / 1000.0
    ##########################################################################
    V    = self . SpinBoxs [ "PointSize"              ] . value (            )
    A    = self . PlanetObjects [ "Points"     ] [ "Actor" ]
    A    . GetProperty ( ) . SetPointSize ( V                                )
    ##########################################################################
    V    = self . SpinBoxs [ "LineWidth"              ] . value (            )
    A    = self . PlanetObjects [ "Lines"      ] [ "Actor" ]
    A    . GetProperty ( ) . SetLineWidth ( V                                )
    ##########################################################################
    V    = self . SpinBoxs [ "AtmosphereTransparency" ] . value (            )
    V    = float           ( 1.0 - ( V / 10000.0 )                           )
    A    = self . PlanetObjects [ "Atmosphere" ] [ "Actor" ]
    A    . GetProperty ( ) . SetOpacity ( V                                  )
    ##########################################################################
    V    = self . SpinBoxs [ "ShadowTransparency"     ] . value (            )
    V    = float           ( 1.0 - ( V / 10000.0 )                           )
    A    = self . PlanetObjects [ "Shadow"     ] [ "Actor" ]
    A    . GetProperty ( ) . SetOpacity ( V                                  )
    ##########################################################################
    V    = self . SpinBoxs [ "RotateAngle"            ] . value (            )
    self . RotateAngle = float ( V / 1000.0 )
    ##########################################################################
    V    = self . SpinBoxs [ "RotateInterval"         ] . value (            )
    self . RotateInterval = V
    ##########################################################################
    V    = self . SpinBoxs [ "CameraDistance"         ] . value (            )
    camera = self . renderer . GetActiveCamera (                             )
    camera . SetDistance   ( V                                               )
    ##########################################################################
    return
  ############################################################################
  def ElementsMenu              ( self , mm                                ) :
    ##########################################################################
    MSG  = self . getMenuItem   ( "DisplayObjects"                           )
    LOM  = mm   . addMenu       ( MSG                                        )
    ##########################################################################
    QLE  = QLineEdit            (                                            )
    QLE  . setText              ( self . windowTitle ( )                     )
    mm   . addWidgetWithMenu    ( LOM , 54238964 , QLE                       )
    self . SpinBoxs [ "WindowTitle" ] = QLE
    ##########################################################################
    mm   . addSeparatorFromMenu ( LOM                                        )
    ##########################################################################
    E    = self . PlanetObjects [ "Texture"    ] [ "Enabled"                 ]
    msg  = self . getMenuItem   ( "DisplayTextured"                          )
    mm   . addActionFromMenu    ( LOM , 54233101 , msg , True , E            )
    ##########################################################################
    E    = self . PlanetObjects [ "Points"     ] [ "Enabled"                 ]
    msg  = self . getMenuItem   ( "DisplayPoints"                            )
    mm   . addActionFromMenu    ( LOM , 54233102 , msg , True , E            )
    ##########################################################################
    E    = self . PlanetObjects [ "Lines"      ] [ "Enabled"                 ]
    msg  = self . getMenuItem   ( "DisplayLines"                             )
    mm   . addActionFromMenu    ( LOM , 54233103 , msg , True , E            )
    ##########################################################################
    E    = self . PlanetObjects [ "Polygons"   ] [ "Enabled"                 ]
    msg  = self . getMenuItem   ( "DisplayPolygons"                          )
    mm   . addActionFromMenu    ( LOM , 54233104 , msg , True , E            )
    ##########################################################################
    E    = self . PlanetObjects [ "Atmosphere" ] [ "Enabled"                 ]
    msg  = self . getMenuItem   ( "DisplayAtmosphere"                        )
    mm   . addActionFromMenu    ( LOM , 54233105 , msg , True , E            )
    ##########################################################################
    E    = self . PlanetObjects [ "Shadow"     ] [ "Enabled"                 ]
    msg  = self . getMenuItem   ( "DisplayShadow"                            )
    mm   . addActionFromMenu    ( LOM , 54233106 , msg , True , E            )
    ##########################################################################
    E    = self . PlanetObjects [ "Axis"       ] [ "Enabled"                 ]
    msg  = self . getMenuItem   ( "DisplayAxis"                              )
    mm   . addActionFromMenu    ( LOM , 54233107 , msg , True , E            )
    ##########################################################################
    return mm
  ############################################################################
  def RunElementsMenu             ( self , at                              ) :
    ##########################################################################
    if                            ( at == 54233101                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Texture"                               )
      ########################################################################
      return
    ##########################################################################
    if                            ( at == 54233102                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Points"                                 )
      ########################################################################
      return
    ##########################################################################
    if                            ( at == 54233103                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Lines"                                  )
      ########################################################################
      return
    ##########################################################################
    if                            ( at == 54233104                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Polygons"                               )
      ########################################################################
      return
    ##########################################################################
    if                            ( at == 54233105                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Atmosphere"                             )
      ########################################################################
      return
    ##########################################################################
    if                            ( at == 54233106                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Shadow"                                 )
      ########################################################################
      return
    ##########################################################################
    if                            ( at == 54233107                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Axis"                                   )
      ########################################################################
      return
    ##########################################################################
    return False
  ############################################################################
  def RenderMenu                 ( self , mm                               ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "RenderParameters"                        )
    LOM   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    E     = self . DoRotation
    msg   = self . getMenuItem   ( "DoRotation"                              )
    mm    . addActionFromMenu    ( LOM , 54232801 , msg , True , E           )
    ##########################################################################
    msg   = self . getMenuItem   ( "RotateAngle:"                            )
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( msg                                       )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 360000.0                                  )
    DSB   . setValue             ( self . RotateAngle * 1000.0               )
    mm    . addWidgetWithMenu    ( LOM , 54232802 , DSB                      )
    self  . SpinBoxs [ "RotateAngle" ] = DSB
    ##########################################################################
    msg   = self . getMenuItem   ( "RotateInterval:"                         )
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( msg                                       )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 86400.0                                   )
    DSB   . setValue             ( self . RotateInterval                     )
    mm    . addWidgetWithMenu    ( LOM , 54232803 , DSB                      )
    self  . SpinBoxs [ "RotateInterval" ] = DSB
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "ChangeBackgroundColor"                   )
    mm    . addActionFromMenu    ( LOM , 54231101 , msg                      )
    ##########################################################################
    msg   = self . getMenuItem   ( "ImportTexture"                           )
    mm    . addActionFromMenu    ( LOM , 54232001 , msg                      )
    ##########################################################################
    msg   = self . getMenuItem   ( "ImportAtmosphere"                        )
    mm    . addActionFromMenu    ( LOM , 54232002 , msg                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "PointsColor"                             )
    mm    . addActionFromMenu    ( LOM , 54232601 , msg                      )
    ##########################################################################
    msg   = self . getMenuItem   ( "LinesColor"                              )
    mm    . addActionFromMenu    ( LOM , 54232602 , msg                      )
    ##########################################################################
    msg   = self . getMenuItem   ( "PolygonsColor"                           )
    mm    . addActionFromMenu    ( LOM , 54232603 , msg                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    A     = self . PlanetObjects [ "Points"     ] [ "Actor"                  ]
    V     = A    . GetProperty ( ) . GetPointSize (                          )
    ##########################################################################
    msg   = self . getMenuItem   ( "PointSize:"                              )
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( msg                                       )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 1000.0                                    )
    DSB   . setValue             ( V                                         )
    mm    . addWidgetWithMenu    ( LOM , 54232721 , DSB                      )
    self  . SpinBoxs [ "PointSize" ] = DSB
    ##########################################################################
    A     = self . PlanetObjects [ "Lines"      ] [ "Actor"                  ]
    V     = A    . GetProperty ( ) . GetLineWidth (                          )
    ##########################################################################
    msg   = self . getMenuItem   ( "LineWidth:"                              )
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( msg                                       )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 1000.0                                    )
    DSB   . setValue             ( V                                         )
    mm    . addWidgetWithMenu    ( LOM , 54232722 , DSB                      )
    self  . SpinBoxs [ "LineWidth" ] = DSB
    ##########################################################################
    A     = self . PlanetObjects [ "Atmosphere" ] [ "Actor"                  ]
    V     = A    . GetProperty ( ) . GetOpacity (                            )
    V     = float                ( 10000.0 * ( 1.0 - V )                     )
    ##########################################################################
    msg   = self . getMenuItem   ( "AtmosphereTransparency:"                 )
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( msg                                       )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 10000.0                                   )
    DSB   . setValue             ( V                                         )
    mm    . addWidgetWithMenu    ( LOM , 54232723 , DSB                      )
    self  . SpinBoxs [ "AtmosphereTransparency" ] = DSB
    ##########################################################################
    A     = self . PlanetObjects [ "Shadow"   ] [ "Actor"                    ]
    V     = A    . GetProperty ( ) . GetOpacity (                            )
    V     = float                ( 10000.0 * ( 1.0 - V )                     )
    ##########################################################################
    msg   = self . getMenuItem   ( "ShadowTransparency:"                     )
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( msg                                       )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 10000.0                                   )
    DSB   . setValue             ( V                                         )
    mm    . addWidgetWithMenu    ( LOM , 54232724 , DSB                      )
    self  . SpinBoxs [ "ShadowTransparency" ] = DSB
    ##########################################################################
    camera = self . renderer . GetActiveCamera (                             )
    dist  = camera . GetDistance (                                           )
    ##########################################################################
    msg   = self . getMenuItem   ( "CameraDistance:"                         )
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( msg                                       )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 1000000000000.0                           )
    DSB   . setValue             ( dist                                      )
    mm    . addWidgetWithMenu    ( LOM , 54232724 , DSB                      )
    self  . SpinBoxs [ "CameraDistance" ] = DSB
    ##########################################################################
    return mm
  ############################################################################
  def RunRenderMenu                ( self , at                             ) :
    ##########################################################################
    if                             ( at == 54232801                        ) :
      ########################################################################
      self . TriggerRotation       (                                         )
      ########################################################################
      return
    ##########################################################################
    if                             ( at == 54231101                        ) :
      ########################################################################
      self . ChangeBackgroundColor (                                         )
      ########################################################################
      return
    ##########################################################################
    if                             ( at == 54232001                        ) :
      ########################################################################
      self . LoadTextureForItem    ( "Texture"                               )
      ########################################################################
      return
    ##########################################################################
    if                             ( at == 54232002                        ) :
      ########################################################################
      self . LoadTextureForItem    ( "Atmosphere"                            )
      ########################################################################
      return
    ##########################################################################
    if                             ( at == 54232601                        ) :
      ########################################################################
      self . SyncSystemColor       ( "Points"                                )
      ########################################################################
      return
    ##########################################################################
    if                             ( at == 54232602                        ) :
      ########################################################################
      self . SyncSystemColor       ( "Lines"                                 )
      ########################################################################
      return
    ##########################################################################
    if                             ( at == 54232603                        ) :
      ########################################################################
      self . SyncSystemColor       ( "Polygons"                              )
      ########################################################################
      return
    ##########################################################################
    return False
  ############################################################################
  def GeometryMenu               ( self , mm                               ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "ModelParameters"                         )
    LOM   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "CreatePlanet"                            )
    mm    . addActionFromMenu    ( LOM , 54235201 , msg                      )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    KM    = self . getMenuItem   ( " Meters"                                 )
    ##########################################################################
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( "X : "                                    )
    DSB   . setSuffix            ( KM                                        )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 100000000000.0                            )
    DSB   . setValue             ( self . Radius . x * 1000                  )
    mm    . addWidgetWithMenu    ( LOM , 54235701 , DSB                      )
    self  . SpinBoxs [ "RadiusX" ] = DSB
    ##########################################################################
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( "Y : "                                    )
    DSB   . setSuffix            ( KM                                        )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 100000000000.0                            )
    DSB   . setValue             ( self . Radius . y * 1000                  )
    mm    . addWidgetWithMenu    ( LOM , 54235702 , DSB                      )
    self  . SpinBoxs [ "RadiusY" ] = DSB
    ##########################################################################
    DSB   = QDoubleSpinBox       (                                           )
    DSB   . setPrefix            ( "Z : "                                    )
    DSB   . setSuffix            ( KM                                        )
    DSB   . setSingleStep        ( 0.01                                      )
    DSB   . setMinimum           ( 0.01                                      )
    DSB   . setMaximum           ( 100000000000.0                            )
    DSB   . setValue             ( self . Radius . z * 1000                  )
    mm    . addWidgetWithMenu    ( LOM , 54235703 , DSB                      )
    self  . SpinBoxs [ "RadiusZ" ] = DSB
    ##########################################################################
    ## mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    """
    self . PlanetObjects [ "Points"     ] [ "Distance" ] = 0.030
    self . PlanetObjects [ "Lines"      ] [ "Distance" ] = 0.020
    self . PlanetObjects [ "Polygons"   ] [ "Distance" ] = 0.010
    self . PlanetObjects [ "Atmosphere" ] [ "Distance" ] = 2.0
    self . PlanetObjects [ "Shadow"     ] [ "Distance" ] = 1.0
    """
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
    self   . ElementsMenu          ( mm                                      )
    self   . GeometryMenu          ( mm                                      )
    self   . RenderMenu            ( mm                                      )
    ## self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    self   . GetMenuParameters     ( at                                      )
    ##########################################################################
    if                             ( self . RunGeometryMenu ( at )         ) :
      return True
    ##########################################################################
    if                             ( self . RunRenderMenu   ( at )         ) :
      return True
    ##########################################################################
    if                             ( self . RunElementsMenu ( at )         ) :
      return True
    ##########################################################################
    if                             ( self . RunDocking      ( mm , aa )    ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
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
