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
    self . PrepareObjects  (                                                 )
    ##########################################################################
    return
  ############################################################################
  def PrepareObjects             ( self                                    ) :
    ##########################################################################
    NAMEs    =                   [ "Points"                                , \
                                   "Lines"                                 , \
                                   "Polygons"                              , \
                                   "Texture"                               , \
                                   "Atmosphere"                              ]
    self     . PlanetObjects =   {                                           }
    self     . ObjectNAMEs   = NAMEs
    ##########################################################################
    self . Radius = ControlPoint (                                           )
    self . Radius . setXYZ       ( 1000.0 , 1000.0 , 1000.0                  )
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      E      = True
      T      = None
      ########################################################################
      if                         ( NAME in [ "Texture" , "Atmosphere" ]    ) :
        ######################################################################
        E    = False
        T    = vtk . vtkTexture  (                                           )
      ########################################################################
      A      = vtk . vtkActor           (                                    )
      D      = vtk . vtkPolyDataMapper  (                                    )
      M      = vtk . vtkPolyData        (                                    )
      ########################################################################
      A      . SetMapper                ( D                                  )
      A      . GetProperty ( ) . SetPointSize ( 1                            )
      ########################################################################
      if                                ( E                                ) :
        self . renderer . AddActor      ( A                                  )
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
      self   . PlanetObjects [ NAME ] [ "Actor"    ] = A
      self   . PlanetObjects [ NAME ] [ "Mapper"   ] = D
      self   . PlanetObjects [ NAME ] [ "Model"    ] = M
      self   . PlanetObjects [ NAME ] [ "Sphere"   ] = S
      self   . PlanetObjects [ NAME ] [ "Color"    ] = C
      self   . PlanetObjects [ NAME ] [ "Texture"  ] = T
      self   . PlanetObjects [ NAME ] [ "Loaded"   ] = False
      self   . PlanetObjects [ NAME ] [ "Distance" ] = 0.0
      self   . PlanetObjects [ NAME ] [ "Enabled"  ] = E
      self   . PlanetObjects [ NAME ] [ "JSON"     ] = {                     }
    ##########################################################################
    PP       = ControlPoint             (                                    )
    PL       = ControlPoint             (                                    )
    PG       = ControlPoint             (                                    )
    ##########################################################################
    PP       . setXYZT                  ( 1.0 , 0.0 , 0.0 , 0.75             )
    PL       . setXYZT                  ( 0.0 , 0.0 , 1.0 , 0.75             )
    PG       . setXYZT                  ( 0.5 , 0.8 , 0.6 , 0.50             )
    ##########################################################################
    self . PlanetObjects [ "Points"     ] [ "Color"    ] . assign ( PP       )
    self . PlanetObjects [ "Lines"      ] [ "Color"    ] . assign ( PL       )
    self . PlanetObjects [ "Polygons"   ] [ "Color"    ] . assign ( PG       )
    ##########################################################################
    self . PlanetObjects [ "Points"     ] [ "Distance" ] = 0.020
    self . PlanetObjects [ "Lines"      ] [ "Distance" ] = 0.010
    self . PlanetObjects [ "Polygons"   ] [ "Distance" ] = 0.005
    self . PlanetObjects [ "Atmosphere" ] [ "Distance" ] = 2.0
    ##########################################################################
    self . setRadius                    ( self . Radius                      )
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
    for NAME in                       [ "Texture" , "Atmosphere"           ] :
      ########################################################################
      E      = self . PlanetObjects   [ NAME       ] [ "Enabled"             ]
      if                              ( E                                  ) :
        self . PrepareTexture         ( NAME                                 )
    ##########################################################################
    self     . renderer . ResetCamera (                                      )
    self     . Notify                 ( 5                                    )
    ##########################################################################
    return
  ############################################################################
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
    self     . renderer . AddActor           ( A                             )
    self     . PlanetObjects [ Item  ] [ "Enabled" ] = True
    self     . PlanetObjects [ Item  ] [ "Loaded"  ] = True
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
    msg   = self . getMenuItem ( "ImportAtmosphere"                          )
    mm    . addActionFromMenu  ( LOM , 54232002 , msg                        )
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
