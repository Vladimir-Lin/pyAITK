# -*- coding: utf-8 -*-
##############################################################################
## VtkBody
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import pathlib
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
from   AITK  . VTK . VtkWidget                import VtkWidget    as VtkWidget
from   AITK  . VTK . Wrapper                  import Wrapper      as VtkWrapper
##############################################################################
from   AITK  . Qt  . MenuManager              import MenuManager  as MenuManager
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
from   AITK  . People . Faces  . Face         import Face         as FaceItem
##############################################################################
BODYDIR = os . path . dirname ( os . path . realpath ( __file__ )            )
##############################################################################
class VtkBody                 ( VtkWidget                                  ) :
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super ( ) . __init__      (        parent        , plan                  )
    self . setVtkBodyDefaults (                                              )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 640 , 640 )                       )
  ############################################################################
  def setVtkBodyDefaults   ( self                                          ) :
    ##########################################################################
    ## self . dockingPlace = Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction     ( self . HavingMenu , True                        )
    ##########################################################################
    self . setAcceptDrops  ( True                                            )
    ## self . setDragEnabled  ( True                                            )
    ## self . setDragDropMode ( QAbstractItemView . DragDrop                    )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def startup                       ( self                                 ) :
    ##########################################################################
    global BODYDIR
    ##########################################################################
    MALE   = os . path . join       ( BODYDIR , "Male.json"                  )
    FEMALE = os . path . join       ( BODYDIR , "Female.json"                )
    print ( MALE , FEMALE )
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
