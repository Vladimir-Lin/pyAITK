# -*- coding: utf-8 -*-
##############################################################################
## 選單管理功能
##############################################################################
import os
import sys
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
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QActionGroup
from   PyQt5 . QtWidgets              import QWidgetAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
##############################################################################
class MenuManager           (                                              ) :
  ############################################################################
  def __init__              ( self , parent = None                         ) :
    ##########################################################################
    self . actions      =   [                                                ]
    self . menus        =   [                                                ]
    self . IDs          =   {                                                }
    self . Widgets      =   {                                                }
    self . actionGroups =   {                                                }
    ##########################################################################
    self . menu         = QMenu        ( parent                              )
    self . menu         . setAttribute ( Qt . WA_InputMethodEnabled          )
    ##########################################################################
    return
  ############################################################################
  def __del__                   ( self                                     ) :
    ##########################################################################
    try                                                                      :
      self . menu . deleteLater (                                            )
    except                                                                   :
      pass
    ##########################################################################
    return
  ############################################################################
  def setFont                          ( self , font                       ) :
    ##########################################################################
    self . menu . setFont              (        font                         )
    ##########################################################################
    for m in self . menus                                                    :
      m  . setFont                     (        font                         )
    ##########################################################################
    for a in self . actions                                                  :
      a  . setFont                     (        font                         )
    ##########################################################################
    for wid in self . Widgets . keys   (                                   ) :
      self . Widgets [ wid ] . setFont (        font                         )
    ##########################################################################
    return
  ############################################################################
  def widgetAt            ( self , Id                                      ) :
    ##########################################################################
    if                    ( Id not in self . Widgets                       ) :
      return None
    ##########################################################################
    return self . Widgets [ Id                                               ]
  ############################################################################
  def contains ( self , action                                             ) :
    ##########################################################################
    if         ( action in [ False , None ]                                ) :
      return False
    ##########################################################################
    return     ( action in self . actions                                    )
  ############################################################################
  def at              ( self , action                                      ) :
    ##########################################################################
    if                ( action in [ False , None ]                         ) :
      return -1
    ##########################################################################
    if                ( action not in self . IDs                           ) :
      return -1
    ##########################################################################
    return self . IDs [ action                                               ]
  ############################################################################
  def __getitem__    ( self , action                                       ) :
    return self . at (        action                                         )
  ############################################################################
  def ActionGroup          ( self , Id                                     ) :
    return self . setGroup ( Id , QActionGroup ( None )                      )
  ############################################################################
  def Group                    ( self , Id                                 ) :
    ##########################################################################
    if                         ( Id not in self . actionGroups             ) :
      return None
    ##########################################################################
    return self . actionGroups [ Id                                          ]
  ############################################################################
  def setGroup ( self , Id , group                                         ) :
    ##########################################################################
    self . actionGroups [ Id ]  = group
    ##########################################################################
    return Id
  ############################################################################
  def exec_                    ( self , pos                                ) :
    ##########################################################################
    if                         ( len ( self . actions ) <= 0               ) :
      return None
    ##########################################################################
    return self . menu . exec_ ( pos                                         )
  ############################################################################
  def addSeparator                    ( self                               ) :
    return self . menu . addSeparator (                                      )
  ############################################################################
  def addSeparatorFromMenu     ( self , menu                               ) :
    return menu . addSeparator (                                             )
  ############################################################################
  def addMenu                     ( self , title                           ) :
    ##########################################################################
    m    = self  . menu . addMenu (        title                             )
    f    = self  . menu . font    (                                          )
    m    . setFont                ( f                                        )
    self . menus . append         ( m                                        )
    ##########################################################################
    return m
  ############################################################################
  def addMenuFromMenu     ( self , m , title                               ) :
    ##########################################################################
    n    = m . addMenu    (            title                                 )
    f    = m . font       (                                                  )
    n    . setFont        ( f                                                )
    self . menus . append ( n                                                )
    ##########################################################################
    return n
  ############################################################################
  def addMaps            ( self , Menu                                     ) :
    ##########################################################################
    KK     = Menu . keys (                                                   )
    ##########################################################################
    for Id in KK                                                             :
      ########################################################################
      text = Menu        [ Id                                                ]
      self . addAction   ( Id , text                                         )
    ##########################################################################
    return
  ############################################################################
  def addAction                       ( self                               , \
                                        Id                                 , \
                                        text                               , \
                                        checkable = False                  , \
                                        checked   = False                  ) :
    ##########################################################################
    a    = self    . menu . addAction ( text                                 )
    self . actions . append           ( a                                    )
    self . IDs [ a ] = Id
    ##########################################################################
    a    . setCheckable               ( checkable                            )
    a    . setChecked                 ( checked                              )
    ##########################################################################
    return a
  ############################################################################
  def addActionWithIcon            ( self                                  , \
                                     Id                                    , \
                                     icon                                  , \
                                     text                                  , \
                                     checkable = False                     , \
                                     checked   = False                     ) :
    ##########################################################################
    a    = self . menu . addAction ( icon , text                             )
    self . actions     . append    ( a                                       )
    self . IDs [ a ] = Id
    ##########################################################################
    a    . setCheckable            ( checkable                               )
    a    . setChecked              ( checked                                 )
    ##########################################################################
    return a
  ############################################################################
  def addActionFromMenu        ( self                                      , \
                                 m                                         , \
                                 Id                                        , \
                                 text                                      , \
                                 checkable = False                         , \
                                 checked   = False                         ) :
    ##########################################################################
    a    = m       . addAction ( text                                        )
    self . actions . append    ( a                                           )
    self . IDs [ a ] = Id
    ##########################################################################
    a    . setCheckable        ( checkable                                   )
    a    . setChecked          ( checked                                     )
    ##########################################################################
    return a
  ############################################################################
  def addActionFromMenuWithIcon ( self                                     , \
                                  m                                        , \
                                  Id                                       , \
                                  icon                                     , \
                                  text                                     , \
                                  checkable = False                        , \
                                  checked   = False                        ) :
    ##########################################################################
    a    = m       . addAction  ( icon , text                                )
    self . actions . append     ( a                                          )
    self . IDs [ a ] = Id
    ##########################################################################
    a    . setCheckable         ( checkable                                  )
    a    . setChecked           ( checked                                    )
    ##########################################################################
    return a
  ############################################################################
  def addWidget                       ( self , Id , widget                 ) :
    ##########################################################################
    widgetAction   = QWidgetAction    ( self . menu . parentWidget ( )       )
    widgetAction   . setDefaultWidget ( widget                               )
    self . menu    . addAction        ( widgetAction                         )
    self . actions . append           ( widgetAction                         )
    ##########################################################################
    self . IDs     [  widgetAction ] = Id
    self . Widgets [ Id            ] = widget
    ##########################################################################
    return widgetAction
  ############################################################################
  def addWidgetWithMenu               ( self , m , Id , widget             ) :
    ##########################################################################
    widgetAction   = QWidgetAction    ( self . menu . parentWidget ( )       )
    widgetAction   . setDefaultWidget ( widget                               )
    m              . addAction        ( widgetAction                         )
    self . actions . append           ( widgetAction                         )
    ##########################################################################
    self . IDs     [  widgetAction ] = Id
    self . Widgets [ Id            ] = widget
    ##########################################################################
    return widgetAction
##############################################################################
