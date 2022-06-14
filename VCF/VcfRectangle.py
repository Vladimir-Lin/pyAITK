# -*- coding: utf-8 -*-
##############################################################################
## VcfRectangle
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
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
from   PyQt5 . QtCore                 import QSize
from   PyQt5 . QtCore                 import QSizeF
from   PyQt5 . QtCore                 import QRect
from   PyQt5 . QtCore                 import QRectF
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetricsF
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QPen
from   PyQt5 . QtGui                  import QBrush
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QTransform
from   PyQt5 . QtGui                  import QPolygonF
from   PyQt5 . QtGui                  import QPainterPath
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import QFileDialog
from   PyQt5 . QtWidgets              import QGraphicsView
from   PyQt5 . QtWidgets              import QGraphicsItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QDoubleSpinBox
##############################################################################
from         . VcfItem                import VcfItem    as VcfItem
##############################################################################
class VcfRectangle              ( VcfItem                                  ) :
  ############################################################################
  vrNoSide        = 0
  vrTopLeft       = 1
  vrTopRight      = 2
  vrBottomLeft    = 3
  vrBottomRight   = 4
  vrLeftSide      = 5
  vrRightSide     = 6
  vrTopSide       = 7
  vrBottomSide    = 8
  vrInside        = 9
  ############################################################################
  def __init__                  ( self                                     , \
                                  parent = None                            , \
                                  item   = None                            , \
                                  plan   = None                            ) :
    ##########################################################################
    super ( ) . __init__        ( parent , item , plan                       )
    self . setRectangleDefaults (                                            )
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setRectangleDefaults         ( self                                  ) :
    ##########################################################################
    self . GeometryChanged = None
    ##########################################################################
    self . PaperPos   = QPointF    ( 0.0 , 0.0                               )
    self . PaperRect  = QRectF     ( 0.0 , 0.0 , 0.0 , 0.0                   )
    self . ScreenRect = QRectF     ( 0.0 , 0.0 , 0.0 , 0.0                   )
    self . Scaling    = False
    self . Editing    = False
    self . Angle      = 0.0
    self . Transform  = QTransform (                                         )
    self . Transform  . reset      (                                         )
    ##########################################################################
    """
    VcfProxys     Proxys     ;
    VcfWidgets    Widgets    ;
    VcfPoints     Points     ;
    VcfRectangles Rectangles ;
    """
    self . Proxys     =            {                                         }
    self . Widgets    =            {                                         }
    self . Points     =            {                                         }
    self . Rectangles =            {                                         }
    ##########################################################################
    self . Markers    =            {                                         }
    self . Markers [ 0 ] = 0
    ##########################################################################
    self . setFunction             ( 32001 , False                           )
    self . setFunction             ( 32002 , True                            )
    ##########################################################################
    self . setFunction             ( 33001 , True                            )
    self . setFunction             ( 33002 , True                            )
    self . setFunction             ( 33003 , True                            )
    self . setFunction             ( 33004 , True                            )
    self . setFunction             ( 33005 , True                            )
    self . setFunction             ( 33006 , True                            )
    self . setFunction             ( 33007 , True                            )
    self . setFunction             ( 33008 , True                            )
    ##########################################################################
    self . LineEditing    = False
    self . LineEditPoints = 0
    self . LimitValues [ "LineEditingId"     ] = 34621145
    self . LimitValues [ "LineEditingWidth"  ] = 6.0
    self . LimitValues [ "LineEditingCircle" ] = 20
    self . LineStartPoint =        {                                         }
    self . LineEndPoint   =        {                                         }
    ##########################################################################
    self . EditingMode      = 0
    self . MeasureRule      =      {                                         }
    self . AddingRule       = False
    self . AddMeasuring     = False
    self . MeasureSpin      = None
    self . MeasureLineWidth = None
    self . MeasurePoints    =      [                                         ]
    ##########################################################################
    self . LimitValues [ "RollImageAngle"     ] = 0.0
    self . LimitValues [ "RollImageAngleStep" ] = 0.001
    self . RollImageSpin = None
    ##########################################################################
    return
  ############################################################################
  def boundingRect ( self                                                  ) :
    return self . ScreenRect
  ############################################################################
  def signalGeometryChanged ( self                                         ) :
    ##########################################################################
    if                      ( self . GeometryChanged in [ False , None ]   ) :
      return
    ##########################################################################
    self . GeometryChanged  ( self                                           )
    ##########################################################################
    return
  ############################################################################
  def emitGeometryChanged         ( self                                   ) :
    ##########################################################################
    self . prepareGeometryChange  (                                          )
    self . update                 (                                          )
    self . signalGeometryChanged  (                                          )
    ##########################################################################
    return
  ############################################################################
  def PaperSize   ( self                                                   ) :
    return QSizeF ( self . PaperRect . width  ( )                          , \
                    self . PaperRect . height ( )                            )
  ############################################################################
  def PaperMiddle  ( self                                                  ) :
    return QPointF ( self . PaperRect . width  ( ) / 2                     , \
                     self . PaperRect . height ( ) / 2                       )
  ############################################################################
  def PaperRange  ( self                                                   ) :
    return QRectF ( self . PaperPos , self . PaperSize ( )                   )
  ############################################################################
  def setScaling       ( self , scale                                      ) :
    ##########################################################################
    self . Scaling = scale
    ##########################################################################
    return
  ############################################################################
  def CurrentPos               ( self                                      ) :
    return self . paperToPoint ( self . PaperPos                             )
  ############################################################################
  def setPos           ( self , CM                                         ) :
    ##########################################################################
    self      . PaperPos = CM
    ##########################################################################
    super ( ) . setPos ( self . CurrentPos ( )                               )
    ##########################################################################
    return
  ############################################################################
  def setRect                             ( self , Region                  ) :
    ##########################################################################
    self . PaperRect = Region
    ##########################################################################
    TL   = self . PaperRect . topLeft     (                                  )
    TL   = self . paperToPoint            ( TL                               )
    BR   = self . PaperRect . bottomRight (                                  )
    BR   = self . paperToPoint            ( BR                               )
    ##########################################################################
    self . ScreenRect . setTopLeft        ( TL                               )
    self . ScreenRect . setBottomRight    ( BR                               )
    ##########################################################################
    self . prepareGeometryChange          (                                  )
    ##########################################################################
    return
  ############################################################################
  def setRange     ( self , paper                                          ) :
    ##########################################################################
    R    = QRectF  ( 0 , 0 , paper . width ( ) , paper . height ( )          )
    self . setPos  ( paper . topLeft ( )                                     )
    self . setRect ( R                                                       )
    ##########################################################################
    return
  ############################################################################
  def atCorner                ( self , pos                                 ) :
    ##########################################################################
    SS        = self . ScreenRect
    ##########################################################################
    LL        = SS   . left   (                                              )
    RR        = SS   . right  (                                              )
    TT        = SS   . top    (                                              )
    BB        = SS   . bottom (                                              )
    WW        = SS   . width  (                                              )
    HH        = SS   . height (                                              )
    ##########################################################################
    Inner     = QRectF        ( LL + 4 , TT + 4 , WW - 8 , HH - 8            )
    ##########################################################################
    if                        ( Inner . contains ( pos )                   ) :
      return self . vrInside
    ##########################################################################
    LT        = QRectF        ( LL     , TT     ,      4 ,      4            )
    RT        = QRectF        ( RR - 4 , TT     ,      4 ,      4            )
    LB        = QRectF        ( LL     , BB - 4 ,      4 ,      4            )
    RB        = QRectF        ( RR - 4 , BB - 4 ,      4 ,      4            )
    LC        = QRectF        ( LL     , TT + 4 ,      4 , HH - 8            )
    RC        = QRectF        ( RR - 4 , TT + 4 ,      4 , HH - 8            )
    TC        = QRectF        ( LL + 4 , TT     , WW - 8 ,      4            )
    BC        = QRectF        ( LL + 4 , BB - 4 , WW - 8 ,      4            )
    ##########################################################################
    if                        ( LT . contains ( pos )                      ) :
      return self . vrTopLeft
    ##########################################################################
    if                        ( RT . contains ( pos )                      ) :
      return self . vrTopRight
    ##########################################################################
    if                        ( LB . contains ( pos )                      ) :
      return self . vrBottomLeft
    ##########################################################################
    if                        ( RB . contains ( pos )                      ) :
      return self . vrBottomRight
    ##########################################################################
    if                        ( LC . contains ( pos )                      ) :
      return self . vrLeftSide
    ##########################################################################
    if                        ( RC . contains ( pos )                      ) :
      return self . vrRightSide
    ##########################################################################
    if                        ( TC . contains ( pos )                      ) :
      return self . vrTopSide
    ##########################################################################
    if                        ( BC . contains ( pos )                      ) :
      return self . vrBottomSide
    ##########################################################################
    return   self . vrNoSide
  ############################################################################
  def hoverEnterEvent           ( self , event                             ) :
    ##########################################################################
    super ( ) . hoverEnterEvent (        event                               )
    ##########################################################################
    if                          ( not self . Scaling                       ) :
      return
    ##########################################################################
    return
  ############################################################################
  def hoverLeaveEvent           ( self , event                             ) :
    ##########################################################################
    super ( ) . hoverLeaveEvent (        event                               )
    ##########################################################################
    if                          ( not self . Scaling                       ) :
      return
    ##########################################################################
    self      . setCursor       ( Qt . ArrowCursor                           )
    ##########################################################################
    return
  ############################################################################
  def hoverMoveEvent            ( self , event                             ) :
    ##########################################################################
    super ( ) . hoverMoveEvent  (        event                               )
    ##########################################################################
    self      . Hovering        ( event . pos ( )                            )
    ##########################################################################
    if                          ( not self . Scaling                       ) :
      return
    ##########################################################################
    Corner    = self . atCorner ( event . pos ( )                            )
    self      . setCornerCursor ( Corner                                     )
    ##########################################################################
    return
  ############################################################################
  def Hovering                  ( self , pos                               ) :
    return
  ############################################################################
  def setCornerCursor           ( self , Corner                            ) :
    ##########################################################################
    if                          ( Corner == self . vrNoSide                ) :
      ########################################################################
      self . setCursor          ( Qt . ArrowCursor                           )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrInside                ) :
      ########################################################################
      self . setCursor          ( Qt . ArrowCursor                           )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrTopLeft               ) :
      ########################################################################
      if                        ( not self . isFunction ( 33005 )          ) :
        return
      ########################################################################
      self . setCursor          ( Qt . SizeFDiagCursor                       )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrTopRight              ) :
      ########################################################################
      if                        ( not self . isFunction ( 33006 )          ) :
        return
      ########################################################################
      self . setCursor          ( Qt . SizeBDiagCursor                       )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrBottomLeft            ) :
      ########################################################################
      if                        ( not self . isFunction ( 33007 )          ) :
        return
      ########################################################################
      self . setCursor          ( Qt . SizeBDiagCursor                       )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrBottomRight           ) :
      ########################################################################
      if                        ( not self . isFunction ( 33008 )          ) :
        return
      ########################################################################
      self . setCursor          ( Qt . SizeFDiagCursor                       )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrLeftSide              ) :
      ########################################################################
      if                        ( not self . isFunction ( 33001 )          ) :
        return
      ########################################################################
      self . setCursor          ( Qt . SizeHorCursor                         )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrRightSide             ) :
      ########################################################################
      if                        ( not self . isFunction ( 33002 )          ) :
        return
      ########################################################################
      self . setCursor          ( Qt . SizeHorCursor                         )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrTopSide               ) :
      ########################################################################
      if                        ( not self . isFunction ( 33003 )          ) :
        return
      ########################################################################
      self . setCursor          ( Qt . SizeVerCursor                         )
      ########################################################################
      return
    ##########################################################################
    if                          ( Corner == self . vrBottomSide            ) :
      ########################################################################
      if                        ( not self . isFunction ( 33004 )          ) :
        return
      ########################################################################
      self . setCursor          ( Qt . SizeVerCursor                         )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def ResizeRect                  ( self , P1 , P2                         ) :
    ##########################################################################
    x1   = P1 . x                 (                                          )
    x2   = P2 . x                 (                                          )
    y1   = P1 . y                 (                                          )
    y2   = P2 . y                 (                                          )
    t    = 0
    ##########################################################################
    if                            ( x1 > x2                                ) :
      t  = x1
      x1 = x2
      x2 = t
    ##########################################################################
    if                            ( y1 > y2                                ) :
      t  = y1
      y1 = y2
      y2 = t
    ##########################################################################
    self . ScreenRect . setLeft   ( x1                                       )
    self . ScreenRect . setTop    ( y1                                       )
    self . ScreenRect . setRight  ( x2                                       )
    self . ScreenRect . setBottom ( y2                                       )
    ##########################################################################
    self . emitGeometryChanged    (                                          )
    ##########################################################################
    return
  ############################################################################
  def ResizeWidth                 ( self , P1 , P2                         ) :
    ##########################################################################
    x1   = P1 . x                 (                                          )
    x2   = P2 . x                 (                                          )
    t    = 0
    ##########################################################################
    if                            ( x1 > x2                                ) :
      t  = x1
      x1 = x2
      x2 = t
    ##########################################################################
    self . ScreenRect . setLeft   ( x1                                       )
    self . ScreenRect . setRight  ( x2                                       )
    ##########################################################################
    self . emitGeometryChanged    (                                          )
    ##########################################################################
    return
  ############################################################################
  def ResizeHeight                ( self , P1 , P2                         ) :
    ##########################################################################
    y1   = P1 . y                 (                                          )
    y2   = P2 . y                 (                                          )
    t    = 0
    ##########################################################################
    if                            ( y1 > y2                                ) :
      t  = y1
      y1 = y2
      y2 = t
    ##########################################################################
    self . ScreenRect . setTop    ( y1                                       )
    self . ScreenRect . setBottom ( y2                                       )
    ##########################################################################
    self . emitGeometryChanged    (                                          )
    ##########################################################################
    return
  ############################################################################
  def CursorMoving         ( self , event                                  ) :
    ##########################################################################
    self . setCornerCursor ( self . atCorner ( event . pos ( ) )             )
    ##########################################################################
    return False
  ############################################################################
  def ResizeStart              ( self , event                              ) :
    ##########################################################################
    Corner   = self . atCorner ( event . pos ( )                             )
    ##########################################################################
    if                         ( Corner == self . vrNoSide ) :
      ########################################################################
      self   . setCursor       ( Qt . ArrowCursor                            )
      self   . Markers    [ 0 ] = 0
      self   . Markers    [ 1 ] = Corner
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrTopLeft                ) :
      ########################################################################
      if                       ( self . isFunction ( 33005 )               ) :
        ######################################################################
        self . setCursor       ( Qt . SizeFDiagCursor                        )
        self . Markers    [ 0 ] = 1
        self . Markers    [ 1 ] = Corner
        self . Points     [ 0 ] = event . pos                      (         )
        self . Points     [ 2 ] = self  . ScreenRect . topLeft     (         )
        self . Points     [ 3 ] = self  . ScreenRect . bottomRight (         )
        self . Rectangles [ 0 ] = self  . ScreenRect
        ######################################################################
        return True
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrTopRight               ) :
      ########################################################################
      if                       ( self . isFunction ( 33006 )               ) :
        self . setCursor       ( Qt . SizeBDiagCursor                        )
        self . Markers    [ 0 ] = 1
        self . Markers    [ 1 ] = Corner
        self . Points     [ 0 ] = event . pos                      (         )
        self . Points     [ 2 ] = self  . ScreenRect . topRight    (         )
        self . Points     [ 3 ] = self  . ScreenRect . bottomLeft  (         )
        self . Rectangles [ 0 ] = self  . ScreenRect
        return True
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrBottomLeft             ) :
      ########################################################################
      if                       ( self . isFunction ( 33007 )               ) :
        ######################################################################
        self . setCursor       ( Qt . SizeBDiagCursor                        )
        self . Markers    [ 0 ] = 1
        self . Markers    [ 1 ] = Corner
        self . Points     [ 0 ] = event . pos                      (         )
        self . Points     [ 2 ] = self  . ScreenRect . bottomLeft  (         )
        self . Points     [ 3 ] = self  . ScreenRect . topRight    (         )
        self . Rectangles [ 0 ] = self  . ScreenRect
        ######################################################################
        return True
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrBottomRight            ) :
      ########################################################################
      if                       ( self . isFunction ( 33008 )               ) :
        ######################################################################
        self . setCursor       ( Qt . SizeFDiagCursor                        )
        self . Markers    [ 0 ] = 1
        self . Markers    [ 1 ] = Corner
        self . Points     [ 0 ] = event . pos                      (         )
        self . Points     [ 2 ] = self  . ScreenRect . bottomRight (         )
        self . Points     [ 3 ] = self  . ScreenRect . topLeft     (         )
        self . Rectangles [ 0 ] = self  . ScreenRect
        ######################################################################
        return True
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrLeftSide               ) :
      ########################################################################
      if                       ( self . isFunction ( 33001 )               ) :
        ######################################################################
        self . setCursor       ( Qt . SizeHorCursor                          )
        self . Markers    [ 0 ] = 1
        self . Markers    [ 1 ] = Corner
        self . Points     [ 0 ] = event . pos                      (         )
        self . Points     [ 2 ] = self  . ScreenRect . topLeft     (         )
        self . Points     [ 3 ] = self  . ScreenRect . topRight    (         )
        self . Rectangles [ 0 ] = self  . ScreenRect
        ######################################################################
        return True
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrRightSide              ) :
      ########################################################################
      if                       ( self . isFunction ( 33002 )               ) :
        ######################################################################
        self . setCursor       ( Qt . SizeHorCursor                          )
        self . Markers    [ 0 ] = 1
        self . Markers    [ 1 ] = Corner
        self . Points     [ 0 ] = event . pos                      (         )
        self . Points     [ 2 ] = self  . ScreenRect . topRight    (         )
        self . Points     [ 3 ] = self  . ScreenRect . topLeft     (         )
        self . Rectangles [ 0 ] = self  . ScreenRect
        ######################################################################
        return True
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrTopSide                ) :
      ########################################################################
      if                       ( self . isFunction ( 33003 )               ) :
        ######################################################################
        self . setCursor       ( Qt .SizeVerCursor                           )
        self . Markers    [ 0 ] = 1
        self . Markers    [ 1 ] = Corner
        self . Points     [ 0 ] = event . pos                      (         )
        self . Points     [ 2 ] = self  . ScreenRect . topLeft     (         )
        self . Points     [ 3 ] = self  . ScreenRect . bottomLeft  (         )
        self . Rectangles [ 0 ] = self  . ScreenRect
        ######################################################################
        return True
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrBottomSide             ) :
      ########################################################################
      if                       ( self . isFunction ( 33004 )               ) :
        ######################################################################
        self . setCursor       ( Qt . SizeVerCursor                          )
        self . Markers    [ 0 ] = 1
        self . Markers    [ 1 ] = Corner
        self . Points     [ 0 ] = event . pos                      (         )
        self . Points     [ 2 ] = self  . ScreenRect . bottomLeft  (         )
        self . Points     [ 3 ] = self  . ScreenRect . topLeft     (         )
        self . Rectangles [ 0 ] = self  . ScreenRect
        ######################################################################
        return True
      ########################################################################
      return False
    ##########################################################################
    if                         ( Corner == self . vrInside                 ) :
      ########################################################################
      self   . setCursor       ( Qt . ArrowCursor                            )
      self   . Markers    [ 0 ] = 0
      self   . Markers    [ 1 ] = self . vrNoSide
      ########################################################################
      return False
    ##########################################################################
    return False
  ############################################################################
  def ResizeMoving          ( self , event                                 ) :
    ##########################################################################
    Corner = self . Markers [ 1                                              ]
    P1     = QPointF        (                                                )
    P2     = QPointF        (                                                )
    ##########################################################################
    CR     =                [ self . vrTopLeft                             , \
                              self . vrTopRight                            , \
                              self . vrBottomLeft                          , \
                              self . vrBottomRight                           ]
    LR     =                [ self . vrLeftSide , self . vrRightSide         ]
    TB     =                [ self . vrTopSide  , self . vrBottomSide        ]
    ##########################################################################
    if                      ( Corner in CR                                 ) :
      ########################################################################
      self . Points [ 1 ] = event . pos (                                    )
      P1   = self . Points [ 2 ] + self . Points [ 1 ] - self . Points [ 0 ]
      P2   = self . Points [ 3 ]
      self . ResizeRect     ( P1 , P2                                        )
      ########################################################################
      return True
    ##########################################################################
    if                      ( Corner in LR                                 ) :
      ########################################################################
      self . Points [ 1 ] = event . pos (                                    )
      P1   = self . Points [ 2 ] + self . Points [ 1 ] - self . Points [ 0 ]
      P2   = self . Points [ 3 ]
      self . ResizeWidth    ( P1 , P2                                        )
      ########################################################################
      return True
    ##########################################################################
    if                      ( Corner in TB                                 ) :
      ########################################################################
      self . Points [ 1 ] = event . pos (                                    )
      P1   = self . Points [ 2 ] + self . Points [ 1 ] - self . Points [ 0 ]
      P2   = self . Points [ 3 ]
      self . ResizeHeight   ( P1 , P2                                        )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def ResizeFinish                        ( self , event                   ) :
    ##########################################################################
    if                                    ( self . Markers [ 0 ] == 0      ) :
      return False
    ##########################################################################
    self . PaperRect = self . rectToPaper ( self . ScreenRect                )
    self . Markers [ 0 ] = 0
    ##########################################################################
    self . setCursor                      ( Qt . ArrowCursor                 )
    self . emitGeometryChanged            (                                  )
    ##########################################################################
    return True
  ############################################################################
  def scalePressEvent           ( self , event                             ) :
    ##########################################################################
    if                          ( self . Scaling                           ) :
      ########################################################################
      if ( self . IsMask ( event . buttons ( ) , Qt . LeftButton )         ) :
        ######################################################################
        if                      ( self . ResizeStart ( event )             ) :
          event . accept        (                                            )
        else                                                                 :
          super ( ) . mousePressEvent ( event                                )
        ######################################################################
        return
    ##########################################################################
    super ( ) . mousePressEvent ( event                                      )
    self      . DeleteGadgets   (                                            )
    ##########################################################################
    return
  ############################################################################
  def scaleMoveEvent                 ( self , event                        ) :
    ##########################################################################
    if                               ( self . Scaling                      ) :
      if ( self . IsMask ( event . buttons ( ) , Qt . LeftButton )         ) :
        ######################################################################
        if                           ( self . ResizeMoving ( event )       ) :
          ####################################################################
          event . accept             (                                       )
          ####################################################################
        else                                                                 :
          ####################################################################
          super ( ) . mouseMoveEvent ( event                                 )
        ######################################################################
        return
        ######################################################################
      else                                                                   :
        ######################################################################
        if                           ( self . CursorMoving ( event )       ) :
          ####################################################################
          event . accept             (                                       )
          ####################################################################
        else                                                                 :
          ####################################################################
          super ( ) . mouseMoveEvent ( event                                 )
        ######################################################################
        return
    ##########################################################################
    super ( ) . mouseMoveEvent       ( event                                 )
    ##########################################################################
    return
  ############################################################################
  def scaleReleaseEvent           ( self , event                           ) :
    ##########################################################################
    if                            ( self . Markers [ 0 ] == 1              ) :
      self . ResizeFinish         (        event                             )
    ##########################################################################
    super ( ) . mouseReleaseEvent (        event                             )
    ##########################################################################
    return
  ############################################################################
  def DeleteGadgets ( self ) :
    ##########################################################################
    """
    CUIDs K = Proxys . keys ( )                ;
    int k                                      ;
    foreach ( k , K )                          {
      scene ( ) -> removeItem ( Proxys [ k ] ) ;
      Proxys [ k ] -> deleteLater ( )          ;
    }                                          ;
    Widgets . clear ( )                        ;
    Proxys  . clear ( )                        ;
    update          ( )                        ;
    """
    ##########################################################################
    return
  ############################################################################
  def itemChange ( self , change , value                                   ) :
    ##########################################################################
    if           ( change == QGraphicsItem . ItemPositionChange            ) :
      self . signalGeometryChanged  (                                        )
    ##########################################################################
    return super ( ) . itemChange   ( change , value                         )
  ############################################################################
  def NewLineEdit ( self , Id ) :
    ##########################################################################
    """
    QLineEdit            * line  = new QLineEdit            (      ) ;
    QGraphicsProxyWidget * proxy = new QGraphicsProxyWidget ( this ) ;
    proxy -> setFlag   ( ItemAcceptsInputMethod , true )             ;
    proxy -> setWidget ( line )                                      ;
    Proxys  [ Id ] = proxy                                           ;
    Widgets [ Id ] = line                                            ;
    return line                                                      ;
    """
    ##########################################################################
    return None
  ############################################################################
  def NewComboBox ( self , Id                                              ) :
    ##########################################################################
    """
    QComboBox            * combo = new QComboBox            (      ) ;
    QGraphicsProxyWidget * proxy = new QGraphicsProxyWidget ( this ) ;
    proxy -> setFlag   ( ItemAcceptsInputMethod , true )             ;
    proxy -> setWidget ( combo )                                     ;
    Proxys  [ Id ] = proxy                                           ;
    Widgets [ Id ] = combo                                           ;
    return combo                                                     ;
    """
    ##########################################################################
    return None
  ############################################################################
  def AttachZLevel ( self ) :
    ##########################################################################
    """
    QSlider              * slider = new QSlider              ( Qt::Horizontal ) ;
    QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget ( this           ) ;
    proxy  -> setFlag   ( ItemAcceptsInputMethod , true )                       ;
    proxy  -> setWidget ( slider            )                                   ;
    MountZLevel         ( proxy    , slider )                                   ;
    slider -> setRange  ( 0        , 1000   )                                   ;
    slider -> setValue  ( zValue() * 1000   )                                   ;
    nConnect ( slider,SIGNAL(valueChanged(int)),this,SLOT(modifyZLevel(int)) )  ;
    """
    ##########################################################################
    return
  ############################################################################
  def MountZLevel            ( self , proxy , slider                       ) :
    return
  ############################################################################
  def modifyZLevel           ( self , Z                                    ) :
    ##########################################################################
    ZZ       = float         ( Z                                             )
    ZZ       = float         ( ZZ / 1000.0                                   )
    ##########################################################################
    pos      = QCursor . pos (                                               )
    msg      = f"Z : {ZZ}"
    ##########################################################################
    self     . setZValue     ( ZZ                                            )
    self     . update        (                                               )
    QToolTip . showText      ( pos , msg                                     )
    ##########################################################################
    return
  ############################################################################
  def AttachOpacity ( self                                                 ) :
    ##########################################################################
    """
    QSlider              * slider = new QSlider              ( Qt::Horizontal ) ;
    QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget ( this           ) ;
    proxy  -> setFlag   ( ItemAcceptsInputMethod , true   )                     ;
    proxy  -> setWidget ( slider                          )                     ;
    MountOpacity        ( proxy , slider                  )                     ;
    slider -> setRange  ( 0 , 1000                        )                     ;
    slider -> setValue  ( QGraphicsItem::opacity() * 1000 )                     ;
    nConnect (slider,SIGNAL(valueChanged(int)),this,SLOT(modifyOpacity(int))  ) ;
    """
    ##########################################################################
    return
  ############################################################################
  def MountOpacity  ( self , proxy , slider                                ) :
    return
  ############################################################################
  def modifyOpacity     ( self , Opacity                                   ) :
    ##########################################################################
    O   = float         ( Opacity                                            )
    O   = float         ( O / 1000.0                                         )
    ##########################################################################
    pos = QCursor . pos (                                                    )
    msg = f"Opacity : {O}"
    ##########################################################################
    self . setOpacity   ( O                                                  )
    self . update       (                                                    )
    QToolTip . showText ( pos , msg                                          )
    ##########################################################################
    return
  ############################################################################
  def AttachRotation       ( self                                          ) :
    ##########################################################################
    """
    QDial                * dial   = new QDial                (      )          ;
    QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget ( NULL )          ;
    proxy -> setFlag     ( ItemAcceptsInputMethod , true )                     ;
    proxy -> setWidget   ( dial         )                                      ;
    MountRotation        ( proxy , dial )                                      ;
    dial  -> setWrapping ( true         )                                      ;
    dial  -> setRange    ( 0 , 360000   )                                      ;
    dial  -> setValue    ( Angle * 1000 )                                      ;
    nConnect ( dial,SIGNAL(valueChanged(int)),this,SLOT(modifyRotation(int)) ) ;
    scene ( ) -> addItem ( proxy        )                                      ;
    """
    ##########################################################################
    return
  ############################################################################
  def MountRotation        ( self , proxy , dial                           ) :
    return
  ############################################################################
  def modifyRotation       ( self , Rotation                               ) :
    ##########################################################################
    self . Angle = float   ( Rotation                                        )
    self . Angle = float   ( self . Angle / 1000.0                           )
    ##########################################################################
    pos  = QCursor . pos   (                                                 )
    msg  = f"Angle : {Angle}"
    ##########################################################################
    self . RotationUpdated (                                                 )
    self . update          (                                                 )
    QToolTip . showText    ( pos , msg                                       )
    ##########################################################################
    return
  ############################################################################
  def RotationUpdated ( self                                               ) :
    return
  ############################################################################
  def defaultMeasurePoints    ( self                                       ) :
    ##########################################################################
    self . Painter . addMap   ( "LineEditing"   , 34621145                   )
    self . Painter . addMap   ( "LineEditingPt" , 34621146                   )
    self . Painter . addMap   ( "MeasureRule"   , 34621147                   )
    self . Painter . addMap   ( "MeasureFont"   , 34621148                   )
    ##########################################################################
    self . Painter . addPen   ( 34621145 , QColor (   0 ,   0 , 255 , 192 )  )
    self . Painter . addPen   ( 34621146 , QColor ( 255 ,   0 , 192 , 192 )  )
    self . Painter . addPen   ( 34621147 , QColor ( 255 ,   0 ,   0 , 192 )  )
    ##########################################################################
    self . Painter . pens [ 34621146 ] . setWidthF ( 2.5                     )
    self . Painter . pens [ 34621147 ] . setWidthF ( 8.0                     )
    ##########################################################################
    self . Painter . addBrush ( 34621145 , QColor (   0 ,   0 , 255 , 192 )  )
    self . Painter . addBrush ( 34621146 , QColor (   0 ,   0 ,   0 ,   0 )  )
    self . Painter . addBrush ( 34621147 , QColor ( 255 ,   0 ,   0 , 192 )  )
    ##########################################################################
    FNT  = QFont              (                                              )
    FNT  . setPixelSize       ( 60.0                                         )
    self . Painter . fonts [ 34621148 ] = FNT
    ##########################################################################
    return
  ############################################################################
  def PaintLineEditing          ( self , p , region , clip , color         ) :
    ##########################################################################
    if                          ( not self . LineEditing                   ) :
      return
    ##########################################################################
    if                          ( self . LineEditPoints <= 0               ) :
      return
    ##########################################################################
    ID   = self . LimitValues   [ "LineEditingId"                            ]
    PW   = self . LimitValues   [ "LineEditingWidth"                         ]
    CR   = self . LimitValues   [ "LineEditingCircle"                        ]
    self . Painter . pens [ ID ] . setWidthF ( PW                            )
    self . Painter . setPainter ( p , "LineEditing"                          )
    ##########################################################################
    L1   = self  . LineStartPoint
    L2   = self  . LineEndPoint
    ##########################################################################
    P1   = QPointF              ( L1 [ "X" ] , L1 [ "Y" ]                    )
    P2   = QPointF              ( L2 [ "X" ] , L2 [ "Y" ]                    )
    ##########################################################################
    p    . drawLine             ( P1 , P2                                    )
    ##########################################################################
    self . Painter . setPainter ( p , "LineEditingPt"                        )
    p    . drawEllipse          ( P1 , CR , CR                               )
    p    . drawEllipse          ( P2 , CR , CR                               )
    ##########################################################################
    return
  ############################################################################
  def PaintMeasureRule          ( self , p , region , clip , color         ) :
    ##########################################################################
    if                          ( "P1" not in self . MeasureRule           ) :
      return
    ##########################################################################
    if                          ( "P2" not in self . MeasureRule           ) :
      return
    ##########################################################################
    self . Painter . setPainter ( p , "MeasureRule"                          )
    ##########################################################################
    L1   = self . MeasureRule   [ "P1"                                       ]
    L2   = self . MeasureRule   [ "P2"                                       ]
    ##########################################################################
    P1   = QPointF              ( L1 [ "X" ] , L1 [ "Y" ]                    )
    P2   = QPointF              ( L2 [ "X" ] , L2 [ "Y" ]                    )
    ##########################################################################
    p    . drawLine             ( P1 , P2                                    )
    ##########################################################################
    return
  ############################################################################
  def PaintMeasurePoints ( self , p , region , clip , color                ) :
    ##########################################################################
    if                   ( len ( self . MeasurePoints ) <= 0               ) :
      return
    ##########################################################################
    FID  = self . Painter . Names [ "MeasureFont"                            ]
    ##########################################################################
    for MP in self . MeasurePoints                                           :
      ########################################################################
      CC = MP            [ "Color"                                           ]
      L1 = MP            [ "P1"                                              ]
      L2 = MP            [ "P2"                                              ]
      LL = self . CalculateMeasureLength ( L1 , L2                           )
      ########################################################################
      QC = QColor        ( CC [ "R" ] , CC [ "G" ] , CC [ "B" ]              )
      PX = QPen          ( QC                                                )
      PX . setWidthF     ( 7.0                                               )
      p  . setPen        ( PX                                                )
      p  . setBrush      ( QBrush ( QC                                     ) )
      ########################################################################
      P1 = QPointF       ( L1 [ "X" ] , L1 [ "Y" ]                           )
      P2 = QPointF       ( L2 [ "X" ] , L2 [ "Y" ]                           )
      ########################################################################
      p  . drawLine      ( P1 , P2                                           )
      ########################################################################
      p  . setFont       ( self . Painter . fonts [ FID ]                    )
      PX . setWidthF     ( 2.54                                              )
      p  . setPen        ( PX                                                )
      ########################################################################
      LT = int           ( LL                                                )
      LT = f"{LT}"
      p  . drawText      ( P2 . x ( ) + 60 , P2 . y ( ) + 60 , LT            )
    ##########################################################################
    return
  ############################################################################
  def lineEditingPressEvent ( self , event                                 ) :
    ##########################################################################
    if                      ( not self . LineEditing                       ) :
      return False
    ##########################################################################
    OKAY  = self . IsMask   ( event . buttons ( ) , Qt . LeftButton          )
    if                      ( not OKAY                                     ) :
      return False
    ##########################################################################
    p     = event . pos     (                                                )
    FP    =                 { "X" : p . x ( ) , "Y" : p . y ( )              }
    self  . LineEditPoints = 1
    self  . LineStartPoint = FP
    self  . LineEndPoint   = FP
    self  . update          (                                                )
    event . accept          (                                                )
    ##########################################################################
    return True
  ############################################################################
  def lineEditingMoveEvent  ( self , event                                 ) :
    ##########################################################################
    if                      ( not self . LineEditing                       ) :
      return False
    ##########################################################################
    if                      ( self  . LineEditPoints != 1                  ) :
      return False
    ##########################################################################
    p     = event . pos     (                                                )
    FP    =                 { "X" : p . x ( ) , "Y" : p . y ( )              }
    self  . LineEditPoints = 1
    self  . LineEndPoint   = FP
    self  . update          (                                                )
    event . accept          (                                                )
    ##########################################################################
    return True
  ############################################################################
  def lineEditingReleaseEvent ( self , event                               ) :
    ##########################################################################
    if                        ( not self . LineEditing                     ) :
      return False
    ##########################################################################
    if                        ( self  . LineEditPoints != 1                ) :
      return False
    ##########################################################################
    p     = event . pos       (                                              )
    FP    =                   { "X" : p . x ( ) , "Y" : p . y ( )            }
    self  . LineEditPoints = 2
    self  . LineEndPoint   = FP
    self  . update          (                                                )
    event . accept            (                                              )
    ##########################################################################
    self  . EndLineEditing    (                                              )
    ##########################################################################
    return True
  ############################################################################
  def StartLineEditing             ( self                                  ) :
    ##########################################################################
    self . LineEditing    = True
    self . LineEditPoints = 0
    self . LineStartPoint =       {                                          }
    self . LineEndPoint   =       {                                          }
    ##########################################################################
    return
  ############################################################################
  def EndLineEditing               ( self                                  ) :
    ##########################################################################
    if ( ( self . LineEditing ) and ( self . LineEditPoints == 2 ) )         :
      ########################################################################
      self . LinePointsEditingFinished ( self . LineStartPoint             , \
                                         self . LineEndPoint                 )
    ##########################################################################
    self . LineEditing    = False
    self . LineEditPoints = 0
    self . LineStartPoint =       {                                          }
    self . LineEndPoint   =       {                                          }
    ##########################################################################
    return
  ############################################################################
  def CalculateMeasureLength    ( self , P1 , P2                           ) :
    ##########################################################################
    if                          ( "Factor" not in self . MeasureRule       ) :
      return 1.0
    ##########################################################################
    FACTOR = self . MeasureRule [ "Factor"                                   ]
    ##########################################################################
    dX     = float              ( P1 [ "X" ] - P2 [ "X" ]                    )
    dY     = float              ( P1 [ "Y" ] - P2 [ "Y" ]                    )
    L      = math . sqrt        ( ( dX * dX ) + ( dY * dY )                  )
    ##########################################################################
    return float                ( L * FACTOR                                 )
  ############################################################################
  def RecalculateMeasureFactors ( self                                     ) :
    ##########################################################################
    if                          ( "P1" not in self . MeasureRule           ) :
      return
    ##########################################################################
    if                          ( "P2" not in self . MeasureRule           ) :
      return
    ##########################################################################
    MM   = 100
    ##########################################################################
    if                          ( "Value" in self . MeasureRule            ) :
      ########################################################################
      MM = self . MeasureRule   [ "Value"                                    ]
    ##########################################################################
    P1   = self . MeasureRule   [ "P1"                                       ]
    P2   = self . MeasureRule   [ "P2"                                       ]
    ##########################################################################
    dX   = float                ( P1 [ "X" ] - P2 [ "X" ]                    )
    dY   = float                ( P1 [ "Y" ] - P2 [ "Y" ]                    )
    L    = math . sqrt          ( ( dX * dX ) + ( dY * dY )                  )
    F    = 1.0
    if                          ( L > 0.0000000001                         ) :
      F  = float                ( float ( MM ) / L                           )
    ##########################################################################
    self . MeasureRule [ "Value"  ] = MM
    self . MeasureRule [ "Length" ] = L
    self . MeasureRule [ "Factor" ] = F
    ##########################################################################
    return
  ############################################################################
  def ClearMeasures        ( self                                          ) :
    ##########################################################################
    self . EditingMode   = 0
    self . MeasureRule   = {                                                 }
    self . AddingRule    = False
    self . AddMeasuring  = False
    self . MeasureSpin   = None
    self . MeasurePoints = [                                                 ]
    self . update          (                                                 )
    ##########################################################################
    return
  ############################################################################
  def AssignRuleLine                 ( self , P1 , P2                      ) :
    ##########################################################################
    self . MeasureRule [ "P1" ] = P1
    self . MeasureRule [ "P2" ] = P2
    ##########################################################################
    self . RecalculateMeasureFactors (                                       )
    self . AddingRule   = False
    ##########################################################################
    return
  ############################################################################
  def AssignMeasurePoints         ( self , P1 , P2                         ) :
    ##########################################################################
    CC   = self . getSystemColor  (                                          )
    R    = CC   . red             (                                          )
    G    = CC   . green           (                                          )
    B    = CC   . blue            (                                          )
    CW   =                        { "R" : R , "G" : G , "B" : B              }
    JP   =                        { "Color" : CW                             ,
                                    "P1"    : P1                             ,
                                    "P2"    : P2                             }
    self . MeasurePoints . append ( JP                                       )
    self . AddMeasuring = False
    ##########################################################################
    return
  ############################################################################
  def AddingRuleLine               ( self                                  ) :
    ##########################################################################
    self . EditingMode = 23521001
    self . AddingRule  = True
    self . StartLineEditing        (                                         )
    ##########################################################################
    return
  ############################################################################
  def AddingMeasuringLine          ( self                                  ) :
    ##########################################################################
    self . EditingMode  = 23521002
    self . AddMeasuring = True
    self . StartLineEditing        (                                         )
    ##########################################################################
    return
  ############################################################################
  def MeasureRuleMenu               ( self , mm , LOM                      ) :
    ##########################################################################
    MM     = 100
    if                              ( "Value" in self . MeasureRule        ) :
      ########################################################################
      MM   = self . MeasureRule     [ "Value"                                ]
    ##########################################################################
    PREFIX = self . getMenuItem     ( "RuleLength:"                          )
    LSP    = QSpinBox               (                                        )
    self   . MeasureSpin = LSP
    LSP    . setPrefix              ( PREFIX                                 )
    LSP    . setMinimum             ( 1                                      )
    LSP    . setMaximum             ( 2000000000                             )
    LSP    . setValue               ( MM                                     )
    ##########################################################################
    PID    = self . Painter . Names [ "MeasureRule"                          ]
    WF     = self . Painter . pens  [ PID ] . widthF (                       )
    PREFIX = self . getMenuItem     ( "RuleLineWidth:"                       )
    LWF    = QDoubleSpinBox         (                                        )
    self   . MeasureLineWidth = LWF
    LWF    . setPrefix              ( PREFIX                                 )
    LWF    . setSingleStep          ( 0.1                                    )
    LWF    . setMinimum             ( 0.1                                    )
    LWF    . setMaximum             ( 1000.0                                 )
    LWF    . setValue               ( WF                                     )
    ##########################################################################
    MSG    = self . getMenuItem     ( "MeasureRule"                          )
    ROM    = mm   . addMenuFromMenu ( LOM , MSG                              )
    ##########################################################################
    MSG    = self . getMenuItem     ( "AddingRule"                           )
    mm     . addActionFromMenu      ( ROM , 78021101 , MSG                   )
    ##########################################################################
    mm     . addWidgetWithMenu      ( ROM , 78021151 , LSP                   )
    mm     . addWidgetWithMenu      ( ROM , 78021152 , LWF                   )
    ##########################################################################
    return mm
  ############################################################################
  def MeasureLinesMenu           ( self , mm , LOM                         ) :
    ##########################################################################
    MSG = self . getMenuItem     ( "MeasuringLines"                          )
    ROM = mm   . addMenuFromMenu ( LOM , MSG                                 )
    ##########################################################################
    MSG = self . getMenuItem     ( "AddMeasuring"                            )
    mm  . addActionFromMenu      ( ROM , 78021201 , MSG                      )
    ##########################################################################
    MSG = self . getMenuItem     ( "ClearMeasurePoints"                      )
    mm  . addActionFromMenu      ( ROM , 78021202 , MSG                      )
    ##########################################################################
    return mm
  ############################################################################
  def MeasureMenu                   ( self , mm                            ) :
    ##########################################################################
    MSG   = self . getMenuItem      ( "Measurements"                         )
    LOM   = mm   . addMenu          ( MSG                                    )
    ##########################################################################
    MSG   = self . getMenuItem      ( "ClearMeasures"                        )
    mm    . addActionFromMenu       ( LOM , 78021001 , MSG                   )
    ##########################################################################
    if ( ( not self . AddingRule ) and ( not self . AddMeasuring ) )         :
      ########################################################################
      mm  = self . MeasureRuleMenu  ( mm , LOM                               )
      mm  = self . MeasureLinesMenu ( mm , LOM                               )
    ##########################################################################
    return
  ############################################################################
  def RunMeasureMenu                 ( self , at                           ) :
    ##########################################################################
    self . MeasureRule [ "Value" ] = self . MeasureSpin . value (            )
    self . RecalculateMeasureFactors (                                       )
    ##########################################################################
    WF   = self . MeasureLineWidth . value (                                 )
    PID  = self . Painter . Names    [ "MeasureRule"                         ]
    self . Painter . pens [ PID ] . setWidthF ( WF                           )
    ##########################################################################
    if                               ( at == 78021001                      ) :
      ########################################################################
      self . ClearMeasures           (                                       )
      ########################################################################
      return True
    ##########################################################################
    if                               ( at == 78021101                      ) :
      ########################################################################
      self . AddingRuleLine          (                                       )
      ########################################################################
      return True
    ##########################################################################
    if                               ( at == 78021201                      ) :
      ########################################################################
      self . AddingMeasuringLine     (                                       )
      ########################################################################
      return True
    ##########################################################################
    if                               ( at == 78021202                      ) :
      ########################################################################
      self . MeasurePoints =         [                                       ]
      self . update                  (                                       )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def RollImageMenu               ( self , mm , ROM                        ) :
    ##########################################################################
    angle  = self . LimitValues   [ "RollImageAngle"                         ]
    step   = self . LimitValues   [ "RollImageAngleStep"                     ]
    ##########################################################################
    ROLL   = QDoubleSpinBox       (                                          )
    PREFIX = self . getMenuItem   ( "RollAngle:"                             )
    ROLL   = QDoubleSpinBox       (                                          )
    self   . RollImageSpin = ROLL
    ROLL   . setPrefix            ( PREFIX                                   )
    ROLL   . setSingleStep        ( step                                     )
    ROLL   . setMinimum           ( -1080.0                                  )
    ROLL   . setMaximum           (  1080.0                                  )
    ROLL   . setValue             ( angle                                    )
    ##########################################################################
    mm     . addSeparatorFromMenu ( ROM                                      )
    ##########################################################################
    msg    = self . getMenuItem   ( "RollImage"                              )
    mm     . addActionFromMenu    ( ROM , 21451251 , msg                     )
    mm     . addWidgetWithMenu    ( ROM , 21451252 , ROLL                    )
    ##########################################################################
    return mm
  ############################################################################
  ## 框線編輯功能
  ############################################################################
  def ContourMouseEvent             ( self , event , convex , ACT , BTN    ) :
    ##########################################################################
    if                              ( BTN                                  ) :
      ########################################################################
      OKAY  = self . IsMask         ( event . buttons ( ) , Qt . LeftButton  )
      if                            ( not OKAY                             ) :
        return False
    ##########################################################################
    OKAY    = convex . HandleQPoint ( event . pos ( ) , ACT                  )
    if                              ( OKAY                                 ) :
      event . accept                (                                        )
      return True
    ##########################################################################
    return False
  ############################################################################
  ############################################################################
  def ImportContour                        ( self , convex                 ) :
    ##########################################################################
    TITLE  = self . getMenuItem            ( "ImportContour"                 )
    F , _  = QFileDialog . getOpenFileName ( self . GraphicsView ( )         ,
                                             TITLE                           ,
                                             ""                              ,
                                             "JSON (*.json)"                 )
    ##########################################################################
    if                                     ( len ( F ) <= 0                ) :
      return
    ##########################################################################
    try                                                                      :
      JSON = LoadJson                      ( F                               )
    except                                                                   :
      self . Notify                        ( 1                               )
      return
    ##########################################################################
    convex . fromJson                      ( JSON                            )
    self   . UpdateContourPoints           ( convex , 0 , True               )
    self   . Notify                        ( 5                               )
    ##########################################################################
    return
  ############################################################################
  def ExportContour                        ( self , convex                 ) :
    ##########################################################################
    TITLE  = self . getMenuItem            ( "ExportContour"                 )
    F , _  = QFileDialog . getSaveFileName ( self . GraphicsView ( )         ,
                                             TITLE                           ,
                                             ""                              ,
                                             "JSON (*.json)"                 )
    ##########################################################################
    if                                     ( len ( F ) <= 0                ) :
      return
    ##########################################################################
    JSON   = convex . toJson               (                                 )
    try                                                                      :
      SaveJson                             ( F , JSON                        )
    except                                                                   :
      self . Notify                        ( 1                               )
      return
    ##########################################################################
    self   . Notify                        ( 5                               )
    ##########################################################################
    return
  ############################################################################
  def ContourEditorMenu          ( self , mm , Base , convex               ) :
    ##########################################################################
    MSG   = self   . getMenuItem ( "ContourEditing"                          )
    LOM   = mm     . addMenu     ( MSG                                       )
    ##########################################################################
    NLE   = QLineEdit            (                                           )
    NLE   . setText              ( convex . Name                             )
    mm    . addWidgetWithMenu    ( LOM , Base + 901 , NLE                    )
    ##########################################################################
    VEX   = convex . getProperty ( "Mode"                                    )
    ##########################################################################
    VM    =                      ( VEX == 1                                  )
    MSG   = self . getMenuItem   ( "AddContourPoint"                         )
    mm    . addActionFromMenu    ( LOM , Base +   1 , MSG , True , VM        )
    ##########################################################################
    if                           ( len ( convex . Index ) > 0              ) :
      ########################################################################
      VM  =                      ( VEX == 2                                  )
      MSG = self . getMenuItem   ( "ModifyContourPoint"                      )
      mm  . addActionFromMenu    ( LOM , Base +   2 , MSG , True , VM        )
    ##########################################################################
    if                           ( len ( convex . Selected ) > 0           ) :
      ########################################################################
      VM  =                      ( VEX == 3                                  )
      MSG = self . getMenuItem   ( "InsertContourPoint"                      )
      mm  . addActionFromMenu    ( LOM , Base +   3 , MSG , True , VM        )
    ##########################################################################
    VM    =                      ( VEX == 4                                  )
    MSG   = self . getMenuItem   ( "PickContourPoint"                        )
    mm    . addActionFromMenu    ( LOM , Base +   4 , MSG , True , VM        )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    if                           ( len ( convex . Selected ) > 0           ) :
      ########################################################################
      MSG = self . getMenuItem   ( "ClearContourSelected"                    )
      mm  . addActionFromMenu    ( LOM , Base + 101 , MSG                    )
      ########################################################################
      MSG = self . getMenuItem   ( "DeleteContourSelected"                   )
      mm  . addActionFromMenu    ( LOM , Base + 102 , MSG                    )
    ##########################################################################
    MSG   = self . getMenuItem   ( "DeleteContour"                           )
    mm    . addActionFromMenu    ( LOM , Base + 103 , MSG                    )
    ##########################################################################
    VM    = convex . Closed
    MSG   = self . getMenuItem   ( "ClosedContour"                           )
    mm    . addActionFromMenu    ( LOM , Base + 201 , MSG , True , VM        )
    ##########################################################################
    VM    = convex . Substract
    MSG   = self . getMenuItem   ( "InvertedContour"                         )
    mm    . addActionFromMenu    ( LOM , Base + 202 , MSG , True , VM        )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    VM    = convex . getProperty ( "ShowPoints"                              )
    MSG   = self . getMenuItem   ( "ShowContourPoints"                       )
    mm    . addActionFromMenu    ( LOM , Base + 301 , MSG , True , VM        )
    ##########################################################################
    VM    = convex . getProperty ( "ShowLines"                               )
    MSG   = self . getMenuItem   ( "ShowContourLines"                        )
    mm    . addActionFromMenu    ( LOM , Base + 302 , MSG , True , VM        )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "ImportContour"                           )
    mm    . addActionFromMenu    ( LOM , Base + 401 , MSG                    )
    ##########################################################################
    MSG   = self . getMenuItem   ( "ExportContour"                           )
    mm    . addActionFromMenu    ( LOM , Base + 402 , MSG                    )
    ##########################################################################
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "ChangeContourPointColor"                 )
    mm    . addActionFromMenu    ( LOM , Base + 501 , MSG                    )
    ##########################################################################
    MSG   = self . getMenuItem   ( "ChangeContourLineColor"                  )
    mm    . addActionFromMenu    ( LOM , Base + 502 , MSG                    )
    ##########################################################################
    MSG   = self . getMenuItem   ( "ChangeContourBackground"                 )
    mm    . addActionFromMenu    ( LOM , Base + 503 , MSG                    )
    ##########################################################################
    return
  ############################################################################
  def RunContourEditorMenu        ( self , mm , at , Base , convex         ) :
    ##########################################################################
    NLE    = mm . widgetAt        ( Base + 901                               )
    if                            ( self . IsOkay ( NLE )                  ) :
      ########################################################################
      NAME = NLE . text           (                                          )
      convex . Name = NAME
    ##########################################################################
    AT     = at - 7000
    OKAY   = self . convex . ExecuteMenuCommand ( AT                         )
    if                            ( OKAY                                   ) :
      return True
    ##########################################################################
    if                            ( AT == 201                              ) :
      ########################################################################
      if                          ( convex . Closed                        ) :
        convex . Closed = False
      else                                                                   :
        convex . Closed = True
      ########################################################################
      convex   . DoPathUpdater    ( 0 , True                                 )
      ########################################################################
      return True
    ##########################################################################
    if                            ( AT == 202                              ) :
      ########################################################################
      if                          ( convex . Substract                     ) :
        convex . Substract = False
      else                                                                   :
        convex . Substract = True
      ########################################################################
      convex   . DoPathUpdater    ( 0 , True                                 )
      ########################################################################
      return True
    ##########################################################################
    if                            ( AT == 301                              ) :
      ########################################################################
      VM   = convex . getProperty ( "ShowPoints"                             )
      if                          ( VM                                     ) :
        convex . setProperty      ( "ShowPoints" , False                     )
      else                                                                   :
        convex . setProperty      ( "ShowPoints" , True                      )
      ########################################################################
      convex   . DoPathUpdater    ( 0 , True                                 )
      ########################################################################
      return True
    ##########################################################################
    if                            ( AT == 302                              ) :
      ########################################################################
      VM   = convex . getProperty ( "ShowLines"                              )
      if                          ( VM                                     ) :
        convex . setProperty      ( "ShowLines" , False                      )
      else                                                                   :
        convex . setProperty      ( "ShowLines" , True                       )
      ########################################################################
      convex   . DoPathUpdater    ( 0 , True                                 )
      ########################################################################
      return True
    ##########################################################################
    if                            ( AT == 401                              ) :
      ########################################################################
      self . ImportContour        ( convex                                   )
      ########################################################################
      return True
    ##########################################################################
    if                            ( AT == 402                              ) :
      ########################################################################
      self . ExportContour        ( convex                                   )
      ########################################################################
      return True
    ##########################################################################
    if                            ( AT == 501                              ) :
      ########################################################################
      COLOR = self   . getSystemColor (                                      )
      ID    = convex . getProperty    ( "PointsId"                           )
      PS    = convex . getProperty    ( "PointSize"                          )
      self . Painter . addPen     ( ID , COLOR                               )
      self . Painter . pens [ ID ] . setWidthF ( PS                          )
      ########################################################################
      return True
    ##########################################################################
    if                            ( AT == 502                              ) :
      ########################################################################
      COLOR = self   . getSystemColor (                                      )
      ID    = convex . getProperty    ( "ContourId"                          )
      LW    = convex . getProperty    ( "LineWidth"                          )
      self . Painter . addPen     ( ID , COLOR                               )
      self . Painter . pens [ ID ] . setWidthF ( LW                          )
      ########################################################################
      return True
    ##########################################################################
    if                            ( AT == 503                              ) :
      ########################################################################
      COLOR = self   . getSystemColor (                                      )
      ID    = convex . getProperty    ( "ContourId"                          )
      self . Painter . addBrush   ( ID , COLOR                               )
      ########################################################################
      return True
    ##########################################################################
    return False
##############################################################################
