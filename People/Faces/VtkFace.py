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
from . Face                                   import Face         as FaceItem
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
    self . NoseZ      = 500.0
    self . BaseZ      = 500.0
    self . ModelJSON  =    {                                                 }
    self . SpinBoxs   =    {                                                 }
    self . Callbacks  =    [                                                 ]
    ##########################################################################
    self . PrepareObjects  (                                                 )
    ##########################################################################
    return
  ############################################################################
  def PrepareObjects                        ( self                         ) :
    ##########################################################################
    NAMEs  =                                [ "Points"                     , \
                                              "Mesh"                       , \
                                              "Face"                       , \
                                              "Texture"                    , \
                                              "Plate"                        ]
    self   . FaceObjects =                  {                                }
    self   . ObjectNAMEs = NAMEs
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      E    = True
      ########################################################################
      A    = vtk . vtkActor                 (                                )
      D    = vtk . vtkPolyDataMapper        (                                )
      M    = vtk . vtkPolyData              (                                )
      ########################################################################
      A    . SetMapper                      ( D                              )
      A    . GetProperty ( ) . SetPointSize ( 1                              )
      ########################################################################
      self . renderer . AddActor            ( A                              )
      ########################################################################
      C    = ControlPoint                   (                                )
      ########################################################################
      self . FaceObjects [ NAME ] =         {                                }
      self . FaceObjects [ NAME ] [ "Actor"    ] = A
      self . FaceObjects [ NAME ] [ "Mapper"   ] = D
      self . FaceObjects [ NAME ] [ "Model"    ] = M
      self . FaceObjects [ NAME ] [ "Color"    ] = C
      self . FaceObjects [ NAME ] [ "Texture"  ] = None
      self . FaceObjects [ NAME ] [ "Enabled"  ] = False
    ##########################################################################
    self   . FacePoints   = None
    self   . FaceVertices = None
    self   . FacePolygons = None
    ##########################################################################
    self   . PreparePlate                   (                                )
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
  def pjsonToVtkPoint ( self , JSON                                        ) :
    return            [ JSON [ "X" ] , JSON [ "Y" ] , JSON [ "Z" ]           ]
  ############################################################################
  def GenerateFacePoints              ( self , StartId , POINTs            ) :
    ##########################################################################
    TOTALs   = len                    ( POINTs                               )
    Points   = vtk . vtkPoints        (                                      )
    ##########################################################################
    Points   . SetNumberOfPoints      ( TOTALs                               )
    ##########################################################################
    id       = StartId
    for P in POINTs                                                          :
      ########################################################################
      PS     = self . pjsonToVtkPoint ( P                                    )
      Points . SetPoint               ( id , PS                              )
      ########################################################################
      id     = id + 1
    ##########################################################################
    return Points
  ############################################################################
  def GenerateFaceColors          ( self , KEY , Total , R , G , B , A     ) :
    ##########################################################################
    WRAP = VtkWrapper             (                                          )
    PP   = ControlPoint           (                                          )
    PP   . setXYZT                ( R , G , B , A                            )
    CC   = PP . toColorComponent4 (                                          )
    CR   = WRAP . GenerateColors  ( 0 , Total , CC                           )
    ##########################################################################
    self . FaceObjects [ KEY ] [ "Color" ] = PP
    ##########################################################################
    return CR
  ############################################################################
  def PreparePlate                      ( self                             ) :
    ##########################################################################
    self     . FaceObjects [ "Plate" ] [ "Enabled" ] = True
    ##########################################################################
    ACTOR    = self . FaceObjects       [ "Plate" ] [ "Actor"                ]
    MAPPER   = self . FaceObjects       [ "Plate" ] [ "Mapper"               ]
    MODEL    = self . FaceObjects       [ "Plate" ] [ "Model"                ]
    ##########################################################################
    PP       = ControlPoint             (                                    )
    PP       . setXYZT                  ( 0.5 , 0.5 , 0.5 , 0.5              )
    ##########################################################################
    self     . FaceObjects [ "Plate" ] [ "Color" ] = PP
    R        = int                      ( PP . x * 255                       )
    G        = int                      ( PP . y * 255                       )
    B        = int                      ( PP . z * 255                       )
    T        = int                      ( PP . t * 255                       )
    ##########################################################################
    Points   = vtk . vtkPoints          (                                    )
    Polygons = vtk . vtkCellArray       (                                    )
    ##########################################################################
    Points   . SetNumberOfPoints        ( 4                                  )
    ##########################################################################
    Colors   = vtk.vtkUnsignedCharArray (                                    )
    Colors   . SetNumberOfComponents    ( 4                                  )
    Colors   . SetNumberOfTuples        ( 4                                  )
    Colors   . SetName                  ( "Colors"                           )
    ##########################################################################
    Points   . SetPoint                 ( 0 , [  1500.0 ,  2000.0 , 0.0 ]    )
    Points   . SetPoint                 ( 1 , [  1500.0 , -2000.0 , 0.0 ]    )
    Points   . SetPoint                 ( 2 , [ -1500.0 , -2000.0 , 0.0 ]    )
    Points   . SetPoint                 ( 3 , [ -1500.0 ,  2000.0 , 0.0 ]    )
    ##########################################################################
    Colors   . SetTuple4                ( 0 , R , G , B , T                  )
    Colors   . SetTuple4                ( 1 , R , G , B , T                  )
    Colors   . SetTuple4                ( 2 , R , G , B , T                  )
    Colors   . SetTuple4                ( 3 , R , G , B , T                  )
    ##########################################################################
    P        = vtk . vtkPolygon         (                                    )
    P        . GetPointIds ( ) . SetNumberOfIds ( 4                          )
    ##########################################################################
    P        . GetPointIds ( ) . SetId  ( 0 , 0                              )
    P        . GetPointIds ( ) . SetId  ( 1 , 1                              )
    P        . GetPointIds ( ) . SetId  ( 2 , 2                              )
    P        . GetPointIds ( ) . SetId  ( 3 , 3                              )
    ##########################################################################
    Polygons . InsertNextCell           ( P                                  )
    ##########################################################################
    ACTOR    . GetProperty  ( ) . SetPointSize ( 1                           )
    MODEL    . SetPoints                ( Points                             )
    MODEL    . SetPolys                 ( Polygons                           )
    MODEL    . GetPointData ( ) . SetScalars   ( Colors                      )
    MODEL    . Modified                 (                                    )
    ##########################################################################
    MAPPER   . SetInputData             ( MODEL                              )
    ##########################################################################
    return
  ############################################################################
  def PreparePoints                           ( self , JSON                ) :
    ##########################################################################
    KEY     = "Points"
    self    .        FaceObjects [ KEY ]      [ "Enabled" ] = True
    ##########################################################################
    ACTOR   = self . FaceObjects [ KEY ]      [ "Actor"                      ]
    MAPPER  = self . FaceObjects [ KEY ]      [ "Mapper"                     ]
    MODEL   = self . FaceObjects [ KEY ]      [ "Model"                      ]
    ##########################################################################
    ITEM    = "3D"
    PTS     = JSON                            [ ITEM                         ]
    TOTALs  = len                             ( PTS                          )
    ##########################################################################
    Colors  = self . GenerateFaceColors       ( KEY                          ,
                                                TOTALs                       ,
                                                0.0                          ,
                                                0.0                          ,
                                                1.0                          ,
                                                1.0                          )
    Colors  . SetName                         ( "Colors"                     )
    ##########################################################################
    ACTOR   . GetProperty  ( ) . SetPointSize ( 2.5                          )
    MODEL   . SetPoints                       ( self . FacePoints            )
    MODEL   . SetVerts                        ( self . FaceVertices          )
    MODEL   . GetPointData ( ) . SetScalars   ( Colors                       )
    MODEL   . Modified                        (                              )
    ##########################################################################
    MAPPER  . SetInputData                    ( MODEL                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareMeshes                            ( self , JSON , KEY         ) :
    ##########################################################################
    FI      = FaceItem                        (                             )
    WRAPPER = VtkWrapper                      (                             )
    ##########################################################################
    self    .        FaceObjects [ KEY ]      [ "Enabled" ] = True
    ##########################################################################
    ACTOR   = self . FaceObjects [ KEY ]      [ "Actor"                      ]
    MAPPER  = self . FaceObjects [ KEY ]      [ "Mapper"                     ]
    MODEL   = self . FaceObjects [ KEY ]      [ "Model"                      ]
    ##########################################################################
    ITEM    = "3D"
    PTS     = JSON                            [ ITEM                         ]
    TOTALs  = len                             ( PTS                          )
    ##########################################################################
    Colors  = self . GenerateFaceColors       ( KEY                          ,
                                                TOTALs                       ,
                                                1.0                          ,
                                                0.0                          ,
                                                0.0                          ,
                                                1.0                          )
    Colors  . SetName                         ( "Colors"                     )
    ##########################################################################
    FM      = FI . Face468Mesh                (                              )
    LINEs   = WRAPPER . GenerateLines         ( FM                           )
    ##########################################################################
    ACTOR   . GetProperty  ( ) . SetLineWidth ( 2.0                          )
    MODEL   . SetPoints                       ( self . FacePoints            )
    MODEL   . SetLines                        ( LINEs                        )
    MODEL   . GetPointData ( ) . SetScalars   ( Colors                       )
    MODEL   . Modified                        (                              )
    ##########################################################################
    MAPPER  . SetInputData                    ( MODEL                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareFace                           ( self , JSON                  ) :
    ##########################################################################
    KEY     = "Face"
    self    .        FaceObjects [ KEY ]    [ "Enabled" ] = True
    ##########################################################################
    ACTOR   = self . FaceObjects [ KEY ]    [ "Actor"                        ]
    MAPPER  = self . FaceObjects [ KEY ]    [ "Mapper"                       ]
    MODEL   = self . FaceObjects [ KEY ]    [ "Model"                        ]
    ##########################################################################
    ITEM    = "3D"
    PTS     = JSON                          [ ITEM                           ]
    TOTALs  = len                           ( PTS                            )
    ##########################################################################
    Colors  = self . GenerateFaceColors     ( KEY                            ,
                                              TOTALs                         ,
                                              0.378 * 2                      ,
                                              0.296 * 2                      ,
                                              0.249 * 2                      ,
                                              1.0                            )
    Colors  . SetName                       ( "Colors"                       )
    ##########################################################################
    MODEL   . SetPoints                     ( self . FacePoints              )
    MODEL   . SetPolys                      ( self . FacePolygons            )
    MODEL   . GetPointData ( ) . SetScalars ( Colors                         )
    MODEL   . Modified                      (                                )
    ##########################################################################
    MAPPER  . SetInputData                  ( MODEL                          )
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
    FZ  = - self . NoseZ
    BZ  =   self . BaseZ
    P1  = JSON [ "Measure" ] [ "P1"     ]
    P2  = JSON [ "Measure" ] [ "P2"     ]
    VV  = JSON [ "Measure" ] [ "Value"  ]
    WW  = JSON [ "Points"  ] [ "Width"  ]
    HH  = JSON [ "Points"  ] [ "Height" ]
    XX  = JSON [ "Points"  ] [ "X"      ]
    YY  = JSON [ "Points"  ] [ "Y"      ]
    SW  = JSON [ "Points"  ] [ "SW"     ]
    SH  = JSON [ "Points"  ] [ "SH"     ]
    ##########################################################################
    CX  = XX + ( SW / 2 )
    CY  = YY + ( SH / 2 )
    ##########################################################################
    PTS = [ ]
    dX  = P1 [ "X" ] - P2 [ "X" ]
    dY  = P1 [ "Y" ] - P2 [ "Y" ]
    LL  = math . sqrt ( ( dX * dX ) + ( dY * dY ) )
    FX  = VV / LL
    FY  = VV / LL
    MZ  = 0
    ##########################################################################
    for P in JSON [ "Points" ] [ "Draws" ]                                   :
      Z = P [ "Z" ]
      if ( Z > MZ ) :
        MZ = Z
    ##########################################################################
    FZ = FZ / MZ
    ##########################################################################
    for P in JSON [ "Points" ] [ "Draws" ]                                   :
      ########################################################################
      X = P [ "X" ]
      Y = P [ "Y" ]
      Z = P [ "Z" ]
      ########################################################################
      X = X - CX
      Y = Y - CY
      ########################################################################
      X = X * FX
      Y = Y * FY
      Y = -Y
      Z = Z * FZ
      Z = Z + BZ
      ########################################################################
      J = { "X" : X , "Y" : Y , "Z" : Z }
      PTS . append ( J )
    ##########################################################################
    JSON [ "Points" ] [ "3D" ] = PTS
    self . ModelJSON  = JSON
    ##########################################################################
    FI      = FaceItem              (                                        )
    WRAPPER = VtkWrapper            (                                        )
    ##########################################################################
    FP      = FI . Face468Polygons  (                                        )
    ##########################################################################
    self . FacePoints   = WRAPPER . GenerateFacePoints ( 0 ,       PTS       )
    self . FaceVertices = WRAPPER . GenerateVertices   ( 0 , len ( PTS )     )
    self . FacePolygons = WRAPPER . GeneratePolygons   ( FP                  )
    ##########################################################################
    self . PreparePoints            ( JSON [ "Points" ]                      )
    self . PrepareMeshes            ( JSON [ "Points" ] , "Mesh"             )
    self . PrepareFace              ( JSON [ "Points" ]                      )
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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def SwitchDisplayElement          ( self , Item                          ) :
    ##########################################################################
    E      = self . FaceObjects     [ Item ] [ "Enabled"                     ]
    A      = self . FaceObjects     [ Item ] [ "Actor"                       ]
    ##########################################################################
    if                              ( E                                    ) :
      ########################################################################
      E    = False
      self . renderer . RemoveActor ( A                                      )
      ########################################################################
    else                                                                     :
      ########################################################################
      E    = True
      self . renderer . AddActor    ( A                                      )
    ##########################################################################
    self   . FaceObjects [ Item ] [ "Enabled" ] = E
    ##########################################################################
    return
  ############################################################################
  def ElementsMenu           ( self , mm                                   ) :
    ##########################################################################
    MSG = self . getMenuItem ( "DisplayObjects"                              )
    LOM = mm   . addMenu     ( MSG                                           )
    ##########################################################################
    E   = self . FaceObjects [ "Texture"    ] [ "Enabled"                    ]
    msg = self . getMenuItem ( "DisplayTextured"                             )
    mm  . addActionFromMenu  ( LOM , 54233101 , msg , True , E               )
    ##########################################################################
    E   = self . FaceObjects [ "Points"     ] [ "Enabled"                    ]
    msg = self . getMenuItem ( "DisplayPoints"                               )
    mm  . addActionFromMenu  ( LOM , 54233102 , msg , True , E               )
    ##########################################################################
    E   = self . FaceObjects [ "Mesh"       ] [ "Enabled"                    ]
    msg = self . getMenuItem ( "DisplayLines"                                )
    mm  . addActionFromMenu  ( LOM , 54233103 , msg , True , E               )
    ##########################################################################
    E   = self . FaceObjects [ "Face"       ] [ "Enabled"                    ]
    msg = self . getMenuItem ( "DisplayFace"                                 )
    mm  . addActionFromMenu  ( LOM , 54233104 , msg , True , E               )
    ##########################################################################
    E   = self . FaceObjects [ "Plate"      ] [ "Enabled"                    ]
    msg = self . getMenuItem ( "DisplayPlate"                                )
    mm  . addActionFromMenu  ( LOM , 54233105 , msg , True , E               )
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
      self . SwitchDisplayElement ( "Mesh"                                   )
      ########################################################################
      return
    ##########################################################################
    if                            ( at == 54233104                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Face"                                   )
      ########################################################################
      return
    ##########################################################################
    if                            ( at == 54233105                         ) :
      ########################################################################
      self . SwitchDisplayElement ( "Plate"                                  )
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
    self   . ElementsMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunElementsMenu ( at )         ) :
      return True
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
