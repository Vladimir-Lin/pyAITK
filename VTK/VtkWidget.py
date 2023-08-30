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
from   PyQt5                                   import QtCore
from   PyQt5                                   import QtGui
from   PyQt5                                   import QtWidgets
##############################################################################
from   PyQt5 . QtCore                          import QObject
from   PyQt5 . QtCore                          import pyqtSignal
from   PyQt5 . QtCore                          import Qt
from   PyQt5 . QtCore                          import QPoint
from   PyQt5 . QtCore                          import QPointF
##############################################################################
from   PyQt5 . QtGui                           import QIcon
from   PyQt5 . QtGui                           import QCursor
from   PyQt5 . QtGui                           import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets                       import QApplication
from   PyQt5 . QtWidgets                       import qApp
from   PyQt5 . QtWidgets                       import QWidget
##############################################################################
from   vtk   . qt . QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
##############################################################################
from   AITK  . Qt . VirtualGui                 import VirtualGui  as VirtualGui
from   AITK  . Qt . AttachDock                 import AttachDock  as AttachDock
from   AITK  . Qt . MenuManager                import MenuManager as MenuManager
##############################################################################
class VtkWidget   ( QVTKRenderWindowInteractor , VirtualGui , AttachDock   ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  attachNone = pyqtSignal ( QWidget                                          )
  attachDock = pyqtSignal ( QWidget , str , int , int                        )
  attachMdi  = pyqtSignal ( QWidget , int                                    )
  ############################################################################
  def __init__    ( self , parent = None , plan = None                     ) :
    ##########################################################################
    super (                   ) . __init__ ( parent                          )
    super ( VirtualGui , self ) . __init__ (                                 )
    super ( AttachDock , self ) . __init__ (                                 )
    self . Initialize                      ( self                            )
    self . setPlanFunction                 ( plan                            )
    self . InitializeDock                  ( plan                            )
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setFunction      ( self . FunctionDocking , True                  )
    ##########################################################################
    self . setAttribute     ( Qt . WA_InputMethodEnabled                     )
    self . VoiceJSON =      {                                                }
    self . bgColor = QColor ( 255 , 255 , 255                                )
    ##########################################################################
    self . PrepareRenderer  (                                                )
    ##########################################################################
    return
  ############################################################################
  def PrepareRenderer      ( self                                          ) :
    ##########################################################################
    self . rWindow    = self . GetRenderWindow (                             )
    self . renderer   = vtk  . vtkRenderer     (                             )
    self . renderer   . SetBackground          ( 1.0 , 1.0 , 1.0             )
    self . rWindow    . AddRenderer            ( self . renderer             )
    self . interactor = self . rWindow . GetInteractor (                     )
    ## self . Initialize      (                                                 )
    ##########################################################################
    return
  ############################################################################
  def ClearRenderer ( self                                                 ) :
    ##########################################################################
    if              ( self . rWindow . HasRenderer   ( self . renderer )   ) :
      ########################################################################
      self . rWindow  . RemoveRenderer ( self . renderer                     )
      self . renderer = None
    ##########################################################################
    return
  ############################################################################
  def ChangeBackgroundColor         ( self                                 ) :
    ##########################################################################
    C    = self . getSystemColor    (                                        )
    R    = C    . redF              (                                        )
    G    = C    . greenF            (                                        )
    B    = C    . blueF             (                                        )
    ##########################################################################
    self . bgColor = C
    ##########################################################################
    self . renderer . SetBackground ( R , G , B                              )
    ##########################################################################
    return
  ############################################################################
  def AssignBackgroundColor         ( self                                 ) :
    ##########################################################################
    C    = self . bgColor
    R    = C    . redF              (                                        )
    G    = C    . greenF            (                                        )
    B    = C    . blueF             (                                        )
    ##########################################################################
    self . renderer . SetBackground ( R , G , B                              )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    ##########################################################################
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . contextMenuEvent ( event                                     )
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
  ############################################################################
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None" ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock" ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"  ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def Visible        ( self , visible                                      ) :
    self . Visiblity (        visible                                        )
    return
  ############################################################################
  def DockIn         ( self , shown                                        ) :
    self . ShowDock  (        shown                                          )
    return
  ############################################################################
  def Docking            ( self , Main , title , area , areas              ) :
    ##########################################################################
    super ( )  . Docking (        Main , self ,  title , area , areas        )
    if                   ( self . Dock == None                             ) :
      return
    ##########################################################################
    self . Dock . visibilityChanged . connect ( self . Visible               )
    ##########################################################################
    return
  ############################################################################
  def DockingMenu                    ( self , menu                         ) :
    ##########################################################################
    canDock = self . isFunction      ( self . FunctionDocking                )
    if                               ( not canDock                         ) :
      return
    ##########################################################################
    p       = self . parentWidget    (                                       )
    S       = False
    D       = False
    M       = False
    ##########################################################################
    if                               ( p == None                           ) :
      S     = True
    else                                                                     :
      ########################################################################
      if                             ( self . isDocking ( )                ) :
        D   = True
      else                                                                   :
        M   = True
    ##########################################################################
    menu    . addSeparator           (                                       )
    ##########################################################################
    if                               (     S or D                          ) :
      msg   = self . getLocalMessage ( self . AttachToMdi                    )
      menu  . addAction              ( self . AttachToMdi  , msg             )
    ##########################################################################
    if                               (     S or M                          ) :
      msg   = self . getLocalMessage ( self . AttachToDock                   )
      menu  . addAction              ( self . AttachToDock , msg             )
    ##########################################################################
    if                               ( not S                               ) :
      msg   = self . getLocalMessage ( self . AttachToNone                   )
      menu  . addAction              ( self . AttachToNone , msg             )
    ##########################################################################
    return
  ############################################################################
  def RunDocking               ( self , menu , action                      ) :
    ##########################################################################
    at = menu . at             ( action                                      )
    ##########################################################################
    if                         ( at == self . AttachToNone                 ) :
      self . attachNone . emit ( self                                        )
      return True
    ##########################################################################
    if                         ( at == self . AttachToMdi                  ) :
      self . attachMdi  . emit ( self , self . dockingOrientation            )
      return True
    ##########################################################################
    if                         ( at == self . AttachToDock                 ) :
      self . attachDock . emit ( self                                      , \
                                 self . windowTitle ( )                    , \
                                 self . dockingPlace                       , \
                                 self . dockingPlaces                        )
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                         ( self , pos                            ) :
    return False
  ############################################################################
  def PrepareContent       ( self                                          ) :
    ##########################################################################
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
    self . renderer . ResetCamera  ( )
    ##########################################################################
    self . interactor . Initialize ( )
    self . interactor . Start      ( )
    ##########################################################################
    return
##############################################################################
