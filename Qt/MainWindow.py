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
from   PyQt5 . QtCore                 import pyqtSlot
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
from   PyQt5 . QtWidgets              import QMdiSubWindow
from   PyQt5 . QtWidgets              import QStackedWidget
from   PyQt5 . QtWidgets              import QMainWindow
##############################################################################
from         . VirtualGui             import VirtualGui    as VirtualGui
from         . StatusBar              import StatusBar     as StatusBar
from         . StackedWidget          import StackedWidget as StackedWidget
from         . MdiArea                import MdiArea       as MdiArea
from         . MdiSubWindow           import MdiSubWindow  as MdiSubWindow
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
    SB   = StatusBar                ( self                                   )
    self . setStatusBar             ( SB                                     )
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
  def addMdi                  ( self , widget , showOptions = 1            ) :
    ##########################################################################
    subw = MdiSubWindow       (                                              )
    subw . setWidget          ( widget                                       )
    self . mdi . addSubWindow ( subw                                         )
    subw . setAttribute       ( Qt . WA_DeleteOnClose                        )
    ##########################################################################
    return subw
  ############################################################################
  def connectDockers              ( self , widget                          ) :
    ##########################################################################
    widget . attachNone . connect ( self . attachNone                        )
    widget . attachDock . connect ( self . attachDock                        )
    widget . attachMdi  . connect ( self . attachMdi                         )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                        (       QWidget                           )
  def attachNone                   ( self , widget                         ) :
    ##########################################################################
    if                             ( widget is None                        ) :
      return
    ##########################################################################
    widgetIsDocking = getattr      ( widget , "isDocking" , None             )
    if                             ( callable ( widgetIsDocking )          ) :
      if                           ( widget . isDocking ( )                ) :
        widget . Detach            ( self                                    )
    ##########################################################################
    p      = widget . parentWidget (                                         )
    widget . setParent             ( None                                    )
    widget . show                  (                                         )
    ##########################################################################
    if                             ( p is None                             ) :
      return
    ##########################################################################
    widgetIsMdiSubWindow = getattr ( p , "isMdiSubWindow" , None             )
    if                             ( callable ( widgetIsMdiSubWindow )     ) :
      p . deleteLater              (                                         )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot      (       QWidget , str , int , int                           )
  def attachDock ( self , widget , title , place , places                  ) :
    ##########################################################################
    subw     = widget . parentWidget (                                       )
    ##########################################################################
    widgetDocking = getattr          ( widget , "Docking" , None             )
    if                               ( callable ( widgetDocking )          ) :
      widget . Docking               ( self , title , place , places         )
    ##########################################################################
    if                               ( subw is None                        ) :
      return
    ##########################################################################
    widgetIsMdiSubWindow = getattr   ( subw , "isMdiSubWindow" , None        )
    if                               ( callable ( widgetIsMdiSubWindow )   ) :
      subw   . deleteLater           (                                       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                   (      QWidget , int                           )
  def attachMdi               ( self, widget , dockingOrientation          ) :
    ##########################################################################
    p = widget . parentWidget (                                              )
    ##########################################################################
    widget . setParent        ( self . mdi                                   )
    self   . mdi . Attach     ( widget , dockingOrientation                  )
    widget . show             (                                              )
    ##########################################################################
    if                        ( p is None                                  ) :
      return
    ##########################################################################
    dockDetach = getattr      ( widget , "Detach" , None                     )
    if                        ( dockDetach is None                         ) :
      return
    ##########################################################################
    if                        ( callable ( dockDetach )                    ) :
      widget . Detach         ( self                                         )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                          (       QWidget                         )
  def deleteLater                    ( self , widget                       ) :
    ##########################################################################
    if                               ( widget is None                      ) :
      return
    ##########################################################################
    p        = widget . parentWidget (                                       )
    if                               ( p is None                           ) :
      widget . deleteLater           (                                       )
      return
    ##########################################################################
    p        . deleteLater           (                                       )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
