# -*- coding: utf-8 -*-
##############################################################################
## VtkRawFace
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
from   PyQt5                                  import QtCore
from   PyQt5                                  import QtGui
from   PyQt5                                  import QtWidgets
##############################################################################
from   PyQt5 . QtCore                         import QObject
from   PyQt5 . QtCore                         import pyqtSignal
from   PyQt5 . QtCore                         import pyqtSlot
from   PyQt5 . QtCore                         import Qt
from   PyQt5 . QtCore                         import QPoint
from   PyQt5 . QtCore                         import QPointF
from   PyQt5 . QtCore                         import QSize
##############################################################################
from   PyQt5 . QtGui                          import QIcon
from   PyQt5 . QtGui                          import QCursor
from   PyQt5 . QtGui                          import QColor
from   PyQt5 . QtGui                          import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets                      import QApplication
from   PyQt5 . QtWidgets                      import qApp
from   PyQt5 . QtWidgets                      import QWidget
from   PyQt5 . QtWidgets                      import QFileDialog
from   PyQt5 . QtWidgets                      import QSpinBox
from   PyQt5 . QtWidgets                      import QDoubleSpinBox
##############################################################################
from   AITK  . Documents . JSON               import Load         as LoadJson
from   AITK  . Documents . JSON               import Save         as SaveJson
##############################################################################
from   AITK  . VTK . VtkWidget                import VtkWidget    as VtkWidget
from   AITK  . VTK . Wrapper                  import Wrapper      as VtkWrapper
##############################################################################
from   AITK  . Qt  . MenuManager              import MenuManager  as MenuManager
from   AITK  . Qt  . LineEdit                 import LineEdit     as LineEdit
from   AITK  . Qt  . ComboBox                 import ComboBox     as ComboBox
from   AITK  . Qt  . SpinBox                  import SpinBox      as SpinBox
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
from   AITK  . Models     . AitkModel         import Model        as ModelJson
from   AITK  . Essentials . Relation          import Relation     as Relation
from   AITK  . Calendars  . StarDate          import StarDate     as StarDate
from   AITK  . Calendars  . Periode           import Periode      as Periode
from   AITK  . Pictures   . Picture           import Picture      as PictureItem
from   AITK  . Pictures   . Gallery           import Gallery      as GalleryItem
##############################################################################
from . Face                                   import Face         as FaceItem
##############################################################################
class VtkRawFace              ( VtkWidget                                  ) :
  ############################################################################
  emitStartModel = pyqtSignal (                                              )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super ( ) . __init__      (        parent        , plan                  )
    self . setVtkFaceDefaults (                                              )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 640 , 640 )                       )
  ############################################################################
  def setVtkFaceDefaults   ( self                                          ) :
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    ##########################################################################
    self . FaceUuid      = 0
    self . PeopleUuid    = 0
    self . PictureUuid   = 0
    ##########################################################################
    self . Name          = ""
    ##########################################################################
    self . FaceFactor    = 3000.0
    self . NoseZ         =  500.0
    self . BaseZ         =  500.0
    ##########################################################################
    self . PIC           = PictureItem (                                     )
    self . ModelJSON     = {                                                 }
    ##########################################################################
    self . Mouse         = True
    self . Pad           = False
    self . PadUi         = None
    ##########################################################################
    self . AitkJSON      = {                                                 }
    self . ActorsMapper  = {                                                 }
    self . Tables        = {                                                 }
    self . PictureTables = {                                                 }
    ##########################################################################
    self . setFunction     ( self . HavingMenu      , True                   )
    ##########################################################################
    self . setAcceptDrops  ( False                                           )
    ## self . setDragEnabled  ( False                                           )
    ## self . setDragDropMode ( QAbstractItemView . NoDragDrop                  )
    ##########################################################################
    self . emitStartModel . connect ( self . StartModel                      )
    ##########################################################################
    self . setPrepared     ( True                                            )
    ##########################################################################
    self . PrepareObjects  (                                                 )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self ,                         Enabled             ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def wheelEvent              ( self , event                               ) :
    ##########################################################################
    if                        ( self . handleMouse ( 4 , event )           ) :
      return
    ##########################################################################
    super ( ) . wheelEvent    (     event                                    )
    self      . dealWithMouse ( 4 , event                                    )
    ##########################################################################
    return
  ############################################################################
  def mouseDoubleClickEvent           ( self , event                       ) :
    ##########################################################################
    if                                ( self . handleMouse ( 3 , event )   ) :
      return
    ##########################################################################
    super ( ) . mouseDoubleClickEvent (     event                            )
    self      . dealWithMouse         ( 3 , event                            )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent           ( self , event                              ) :
    ##########################################################################
    if                         ( self . handleMouse ( 2 , event )          ) :
      return
    ##########################################################################
    super ( ) . mouseMoveEvent (     event                                   )
    self      . dealWithMouse  ( 2 , event                                   )
    ##########################################################################
    return
  ############################################################################
  def mouseReleaseEvent           ( self , event                           ) :
    ##########################################################################
    if                          ( self . handleMouse ( 1 , event )         ) :
      return
    ##########################################################################
    super ( ) . mouseReleaseEvent (     event                                )
    self      . dealWithMouse     ( 1 , event                                )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent           ( self , event                             ) :
    ##########################################################################
    if                          ( self . handleMouse ( 0 , event )         ) :
      return
    ##########################################################################
    super ( ) . mousePressEvent (     event                                  )
    self      . dealWithMouse   ( 0 , event                                  )
    ##########################################################################
    return
  ############################################################################
  def handleMouse   ( self , mType , event                                 ) :
    ##########################################################################
    if              ( self . Mouse                                         ) :
      return False
    ##########################################################################
    event . accept  (                                                        )
    ##########################################################################
    return True
  ############################################################################
  def dealWithMouse                 ( self , mType , event                 ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Relocation                  ( self                                   ) :
    ##########################################################################
    ##########################################################################
    return False
  ############################################################################
  def Shutdown           ( self                                            ) :
    ##########################################################################
    self . Leave . emit  ( self                                              )
    ## self . AttachActions ( False                                             )
    ##########################################################################
    return True
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def StartModel                    ( self                                 ) :
    ##########################################################################
    self . renderer   . ResetCamera (                                        )
    self . interactor . Initialize  (                                        )
    self . interactor . Start       (                                        )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
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
    self   . FaceObjects [ "Texture" ] [ "Texture" ] = vtk . vtkTexture (    )
    ##########################################################################
    self   . FacePoints      = None
    self   . FaceVertices    = None
    self   . FacePolygons    = None
    self   . FaceTextureMaps = None
    ##########################################################################
    self   . PreparePlate                   (                                )
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
  def GenerateTextureMappings    ( self , StartId                          ) :
    ##########################################################################
    PTS  = self . ModelJSON      [ "468" ] [ "Original"                      ]
    AT   = StartId
    ##########################################################################
    TC   = vtk . vtkFloatArray   (                                           )
    TC   . SetNumberOfComponents ( 2                                         )
    TC   . SetNumberOfTuples     ( len ( PTS )                               )
    TC   . SetName               ( "TextureCoordinates"                      )
    ##########################################################################
    for P in PTS                                                             :
      ########################################################################
      X  = float                 ( P [ "X" ]                                 )
      Y  = float                 ( P [ "Y" ]                                 )
      TC . SetTuple2             ( AT , X , 1.0 - Y                          )
      ########################################################################
      AT = AT + 1
    ##########################################################################
    return TC
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
    self    .        FaceObjects [ KEY ]      [ "Enabled" ] = False
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
    self    .        FaceObjects [ KEY ]      [ "Enabled" ] = False
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
    self    .        FaceObjects [ KEY ]    [ "Enabled" ] = False
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
                                              0.378 * 2.5                    ,
                                              0.296 * 2.5                    ,
                                              0.249 * 2.5                    ,
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
  def LoadTextureFromBlob                ( self , KEY                      ) :
    ##########################################################################
    ACTOR   = self . FaceObjects [ KEY ] [ "Actor"                           ]
    TEXTURE = self . FaceObjects [ KEY ] [ "Texture"                         ]
    ## BLOB    = self . ModelJSON           [ "Texture"                         ]
    ##########################################################################
    TMPDIR  = self . Settings            [ "ModelPath"                       ]
    FUID    = self . FaceUuid
    F       = f"{TMPDIR}/{FUID}.png"
    ##########################################################################
    QI      = self . PIC . toQImage      (                                   )
    QI      . save                       ( F , "PNG"                         )
    ##########################################################################
    Reader  = vtk . vtkPNGReader         (                                   )
    Reader  . SetFileName                ( F                                 )
    ## Reader  . SetMemoryBuffer            ( BLOB . getbuffer ( )              )
    ##########################################################################
    TEXTURE . SetInputConnection         ( Reader . GetOutputPort ( )        )
    TEXTURE . InterpolateOn              (                                   )
    ACTOR   . SetTexture                 ( TEXTURE                           )
    ##########################################################################
    os      . remove                     ( F                                 )
    ##########################################################################
    return
  ############################################################################
  def PrepareTexture                       ( self                          ) :
    ##########################################################################
    KEY    = "Texture"
    self   .        FaceObjects [ KEY ]    [ "Enabled" ] = True
    ##########################################################################
    ACTOR  = self . FaceObjects [ KEY ]    [ "Actor"                         ]
    MAPPER = self . FaceObjects [ KEY ]    [ "Mapper"                        ]
    MODEL  = self . FaceObjects [ KEY ]    [ "Model"                         ]
    ##########################################################################
    MODEL  . SetPoints                     ( self . FacePoints               )
    MODEL  . SetPolys                      ( self . FacePolygons             )
    MODEL  . GetPointData ( ) . SetTCoords ( self . FaceTextureMaps          )
    MODEL  . Modified                      (                                 )
    ##########################################################################
    MAPPER . SetInputData                  ( MODEL                           )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def RebuildFaceDetails             ( self                                ) :
    ##########################################################################
    PTS =                            [                                       ]
    LST =                            [                                       ]
    ##########################################################################
    FX  =   self . FaceFactor
    FY  = - self . FaceFactor
    FZ  = - self . FaceFactor
    ##########################################################################
    BX  = - ( self . FaceFactor / 2 )
    BY  =   ( self . FaceFactor / 2 )
    BZ  =   self . BaseZ
    ##########################################################################
    WW  = self . ModelJSON           [ "468"  ] [ "Width"                    ]
    HH  = self . ModelJSON           [ "468"  ] [ "Height"                   ]
    XX  = self . ModelJSON           [ "468"  ] [ "X"                        ]
    YY  = self . ModelJSON           [ "468"  ] [ "Y"                        ]
    SW  = self . ModelJSON           [ "468"  ] [ "SW"                       ]
    SH  = self . ModelJSON           [ "468"  ] [ "SH"                       ]
    NPS = self . ModelJSON           [ "468"  ] [ "Original"                 ]
    ##########################################################################
    for P in NPS                                                             :
      ########################################################################
      XP = ( P [ "X" ] * FX ) + BX
      YP = ( P [ "Y" ] * FY ) + BY
      ZP = ( P [ "Z" ] * FZ ) + BZ
      ########################################################################
      PTS . append                   ( { "X" : XP  , "Y" : YP  , "Z" : ZP  } )
      LST . append                   ( [ P [ "X" ] , P [ "Y" ] , P [ "Z" ] ] )
    ##########################################################################
    self . ModelJSON [ "Points" ] = {                                        }
    self . ModelJSON [ "Points" ] [ "3D"       ] = PTS
    self . ModelJSON [ "Points" ] [ "Listings" ] = LST
    ##########################################################################
    FI      = FaceItem              (                                        )
    WRAPPER = VtkWrapper            (                                        )
    ##########################################################################
    FP      = FI . Face468Polygons  (                                        )
    ##########################################################################
    self . FacePoints      = WRAPPER . GenerateFacePoints ( 0 ,       PTS    )
    self . FaceVertices    = WRAPPER . GenerateVertices   ( 0 , len ( PTS )  )
    self . FacePolygons    = WRAPPER . GeneratePolygons   ( FP               )
    self . FaceTextureMaps = self    . GenerateTextureMappings ( 0           )
    self . LoadTextureFromBlob      ( "Texture"                              )
    ##########################################################################
    self . PreparePoints            ( self . ModelJSON [ "Points" ]          )
    self . PrepareMeshes            ( self . ModelJSON [ "Points" ] , "Mesh" )
    self . PrepareFace              ( self . ModelJSON [ "Points" ]          )
    self . PrepareTexture           (                                        )
    ##########################################################################
    return
  ############################################################################
  def LoadFaceDetails                 ( self , DB                          ) :
    ##########################################################################
    FRNTAB     = self . Tables        [ "FaceRegions"                        ]
    FPSTAB     = self . Tables        [ "FacePoints"                         ]
    PICTAB     = self . Tables        [ "Information"                        ]
    DOPTAB     = self . Tables        [ "Depot"                              ]
    ##########################################################################
    FUID       = self . FaceUuid
    ##########################################################################
    QQ         = f"""select `picture` , `owner` ,
                            `x` , `y` , `width` , `height` ,
                            `rotation` from {FRNTAB}
                   where ( `uuid` = {FUID} ) ;"""
    QQ         = " " . join           ( QQ . split ( )                       )
    DB         . Query                ( QQ                                   )
    RR         = DB . FetchOne        (                                      )
    ##########################################################################
    if                                ( RR in [ False , None ]             ) :
      return False
    ##########################################################################
    if                                ( len ( RR ) != 7                    ) :
      return False
    ##########################################################################
    PCID       = int                  ( RR [ 0                             ] )
    PUID       = int                  ( RR [ 1                             ] )
    XP         = int                  ( RR [ 2                             ] )
    YP         = int                  ( RR [ 3                             ] )
    WP         = int                  ( RR [ 4                             ] )
    HP         = int                  ( RR [ 5                             ] )
    DEGREE     = float                ( RR [ 6                             ] )
    ##########################################################################
    QQ         = f"""select `points` from {FPSTAB}
                   where ( `uuid` = {FUID} ) ;"""
    QQ         = " " . join           ( QQ . split ( )                       )
    DB         . Query                ( QQ                                   )
    RR         = DB . FetchOne        (                                      )
    ##########################################################################
    if                                ( RR in [ False , None ]             ) :
      return False
    ##########################################################################
    if                                ( len ( RR ) != 1                    ) :
      return False
    ##########################################################################
    TEXT       = self . assureString  ( RR [ 0                             ] )
    ##########################################################################
    if                                ( len ( TEXT ) <= 0                  ) :
      return False
    ##########################################################################
    FJ         = json . loads         ( TEXT                                 )
    ##########################################################################
    PIC        = PictureItem          (                                      )
    INFO       = PIC . GetInformation ( DB , PICTAB , PCID                   )
    ##########################################################################
    QQ         = f"select `file` from {DOPTAB} where ( `uuid` = {PCID} ) ;"
    if                                ( not PIC . FromDB ( DB , QQ )       ) :
      return False
    ##########################################################################
    ROT        = PIC . Rotate         ( DEGREE                               )
    PART       = ROT . Crop           ( XP , YP , WP , HP                    )
    self . PIC . Image = PART . Image
    ##########################################################################
    self . PeopleUuid  = PUID
    self . PictureUuid = PCID
    self . ModelJSON   = FJ
    ##########################################################################
    return True
  ############################################################################
  def loading                       ( self                                 ) :
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      self . emitStartModel . emit  (                                        )
      return
    ##########################################################################
    self   . Notify                 ( 3                                      )
    ##########################################################################
    FMT    = self . Translations    [ "UI::StartLoading"                     ]
    MSG    = FMT . format           ( self . windowTitle ( )                 )
    self   . ShowStatus             ( MSG                                    )
    self   . OnBusy  . emit         (                                        )
    self   . setBustle              (                                        )
    ##########################################################################
    OKAY   = self . LoadFaceDetails ( DB )
    ##########################################################################
    self   . setVacancy             (                                        )
    self   . GoRelax . emit         (                                        )
    self   . ShowStatus             ( ""                                     )
    DB     . Close                  (                                        )
    ##########################################################################
    if                              ( OKAY                                 ) :
      ########################################################################
      self . RebuildFaceDetails     (                                        )
      ########################################################################
      self . Notify                 ( 5                                      )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . Notify                 ( 3                                      )
    ##########################################################################
    self   . emitStartModel . emit  (                                        )
    ##########################################################################
    return
  ############################################################################
  def startup                    ( self                                    ) :
    ##########################################################################
    self . emitStartModel . emit (                                           )
    ##########################################################################
    self . Go                    ( self . loading                            )
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
  ## 切換控制板
  ############################################################################
  def SwitchPad ( self                                                     ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  ## 切換滑鼠追蹤控制
  ############################################################################
  def SwitchMouse ( self                                                   ) :
    ##########################################################################
    if            ( self . Mouse                                           ) :
      ########################################################################
      self . Mouse = False
      ########################################################################
    else                                                                     :
      ########################################################################
      self . Mouse = True
    ##########################################################################
    return
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
    msg    = self . getMenuItem    ( "ControlPad"                            )
    mm     . addAction             ( 1101 , msg , True , self . Pad          )
    ##########################################################################
    msg    = self . getMenuItem    ( "TrackMouse"                            )
    mm     . addAction             ( 1102 , msg , True , self . Mouse        )
    ##########################################################################
    mm     . addSeparator          (                                         )
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
    if                            ( at == 1101                             ) :
      ########################################################################
      self . SwitchPad            (                                          )
      ########################################################################
      return True
    ##########################################################################
    if                            ( at == 1102                             ) :
      ########################################################################
      self . SwitchMouse          (                                          )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
