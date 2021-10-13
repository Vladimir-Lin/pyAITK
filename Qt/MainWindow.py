# -*- coding: utf-8 -*-
##############################################################################
import os
import sys
import time
##############################################################################
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QMdiArea
from   PyQt5 . QtWidgets              import QStackedWidget
from   PyQt5 . QtWidgets              import QMainWindow
##############################################################################
from         . VirtualGui             import VirtualGui    as VirtualGui
from         . StackedWidget          import StackedWidget as StackedWidget
from         . MdiArea                import MdiArea       as MdiArea
##############################################################################
class MainWindow    ( QMainWindow , VirtualGui                             ) :
  ############################################################################
  def __init__      ( self , parent = None , plan = None                   ) :
    ##########################################################################
    super ( QMainWindow , self ) . __init__ ( parent                         )
    super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize                       ( self                           )
    self . setPlanFunction                  ( plan                           )
    ##########################################################################
    return
  ############################################################################
  def Configure                     ( self                                 ) :
    ##########################################################################
    self . stacked = StackedWidget  ( self           , self . PlanFunc       )
    self . mdi     = MdiArea        ( self . stacked , self . PlanFunc       )
    self . stacked . addWidget      ( self . mdi                             )
    self . setCentralWidget         ( self . stacked                         )
    ##########################################################################
    return
  ############################################################################
  def focusInEvent    ( self , event                                       ) :
    ##########################################################################
    if                ( self . focusIn ( event )                           ) :
      return
    super ( QMainWindow , self ) . focusInEvent ( event                      )
    ##########################################################################
    return
  ############################################################################
  def focusOutEvent   ( self , event                                       ) :
    ##########################################################################
    if                ( self . focusOut ( event )                          ) :
      return
    super ( QMainWindow , self ) . focusOutEvent ( event                     )
    ##########################################################################
    return
  ############################################################################
  def startup                 ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def FocusIn                 ( self                                       ) :
    return True
  ############################################################################
  def FocusOut                ( self                                       ) :
    return True
  ############################################################################
  def NormalWindow        ( self                                           ) :
    self . showNormal     (                                                  )
    return
  ############################################################################
  def FullScreen          ( self                                           ) :
    self . showFullScreen (                                                  )
    return
  ############################################################################
  def MinimizedWindow     ( self                                           ) :
    self . showMinimized  (                                                  )
    return
  ############################################################################
  def MaximizedWindow     ( self                                           ) :
    self . showMaximized  (                                                  )
    return
  ############################################################################
  def TileWindows               ( self                                     ) :
    ##########################################################################
    self . mdi . Tile           (                                            )
    ##########################################################################
    return
  ############################################################################
  def CascadeWindows            ( self                                     ) :
    ##########################################################################
    self . mdi . Cascade        (                                            )
    ##########################################################################
    return
  ############################################################################
  def TabbedView                ( self                                     ) :
    ##########################################################################
    self . mdi . Tabbed         (                                            )
    ##########################################################################
    return
  ############################################################################
  def SubwindowView             ( self                                     ) :
    ##########################################################################
    self . mdi . Subwindow      (                                            )
    ##########################################################################
    return
  ############################################################################
  def CloseAll                  ( self                                     ) :
    ##########################################################################
    self . mdi . CloseAll       (                                            )
    ##########################################################################
    return
  ############################################################################
  def addMdi                         ( self , widget , showOptions = 1     ) :
    ##########################################################################
    subw = self . mdi . addSubWindow ( widget                                )
    subw . setAttribute              ( Qt . WA_DeleteOnClose                 )
    ##########################################################################
    return subw
##############################################################################
