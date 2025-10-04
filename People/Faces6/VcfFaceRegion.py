# -*- coding: utf-8 -*-
##############################################################################
## VcfFaceRegion
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
from   io                                         import BytesIO
##############################################################################
from   PySide6                                    import QtCore
from   PySide6                                    import QtGui
from   PySide6                                    import QtWidgets
from   PySide6 . QtCore                           import *
from   PySide6 . QtGui                            import *
from   PySide6 . QtWidgets                        import *
from   AITK    . Qt6                              import *
from   AITK    . VCF6                             import *
##############################################################################
from   AITK    . Essentials . Object              import Object  as Object
from   AITK    . Pictures   . Picture6            import Picture as PictureItem
from   AITK    . Pictures   . Gallery             import Gallery as GalleryItem
from   AITK    . Math       . Geometry6 . Contour import Contour as Contour
from   AITK    . Graphics   . Color     . Color   import Color   as GColor
from   AITK    . People     . Faces     . Face    import Face    as FaceItem
from   AITK    . People     . Body      . Tit     import Tit     as TitItem
from   AITK    . People     . Body      . Body    import Body    as BodyItem
##############################################################################
class VcfFaceRegion                 ( VcfCanvas                            ) :
  ############################################################################
  def __init__                      ( self                                 , \
                                      parent = None                        , \
                                      item   = None                        , \
                                      plan   = None                        ) :
    ##########################################################################
    super ( ) . __init__            ( parent , item , plan                   )
    self . setVcfFaceRegionDefaults (                                        )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfFaceRegionDefaults ( self                                      ) :
    ##########################################################################
    self . PictureDPI      = 96
    self . PictureItem     = None
    self . Region          = None
    self . NoseBridge      = None
    self . PeopleDetailsUI = None
    self . PeopleUuid      = 0
    self . FACEs           =   [                                             ]
    self . EYEs            =   [                                             ]
    self . MOUTHs          =   [                                             ]
    self . POSEs           =   { "Pose"   : False                            }
    self . MESHs           =   { "Mesh"   : False                            }
    self . MeshRadius      = 8.0
    self . NIPPLEs         =   { "Nipple" : False                            }
    self . FEATUREs        =   { "Ready"  : False                            }
    self . GeometryChanged = self . FaceGeometryChanged
    self . FaceCallbacks   =   [                                             ]
    self . setZValue           ( 50000                                       )
    self . setOpacity          ( 1.0                                         )
    ##########################################################################
    self . Painter . addMap    ( "Face"         ,       11                   )
    self . Painter . addMap    ( "Eyes"         ,       12                   )
    self . Painter . addMap    ( "Mouth"        ,       13                   )
    self . Painter . addMap    ( "Shape"        ,       21                   )
    self . Painter . addMap    ( "RightEyebrow" ,       22                   )
    self . Painter . addMap    ( "LeftEyebrow"  ,       23                   )
    self . Painter . addMap    ( "NoseBridge"   ,       24                   )
    self . Painter . addMap    ( "NoseNostril"  ,       25                   )
    self . Painter . addMap    ( "RightEye"     ,       26                   )
    self . Painter . addMap    ( "LeftEye"      ,       27                   )
    self . Painter . addMap    ( "OuterMouth"   ,       28                   )
    self . Painter . addMap    ( "InnerMouth"   ,       29                   )
    self . Painter . addMap    ( "FaceRotation" ,       30                   )
    ##########################################################################
    self . Painter . addPen    (        0 , QColor (  64 ,  64 ,  64 , 128 ) )
    self . Painter . addPen    (       11 , QColor (   0 ,   0 , 255 , 255 ) )
    self . Painter . addPen    (       12 , QColor ( 255 ,   0 ,   0 , 255 ) )
    self . Painter . addPen    (       13 , QColor (   0 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       21 , QColor ( 255 ,   0 ,   0 , 255 ) )
    self . Painter . addPen    (       22 , QColor (   0 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       23 , QColor (   0 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       24 , QColor (   0 ,   0 , 255 , 255 ) )
    self . Painter . addPen    (       25 , QColor (   0 , 255 , 255 , 255 ) )
    self . Painter . addPen    (       26 , QColor ( 255 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       27 , QColor ( 255 , 255 ,   0 , 255 ) )
    self . Painter . addPen    (       28 , QColor ( 128 ,  64 , 255 , 255 ) )
    self . Painter . addPen    (       29 , QColor ( 128 ,  64 , 255 , 255 ) )
    self . Painter . addPen    (       30 , QColor (  48 ,  96 , 255 , 255 ) )
    ##########################################################################
    self . Painter . addBrush  (        0 , QColor ( 255 , 255 , 255 ,  64 ) )
    self . Painter . addBrush  (       21 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       22 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       23 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       24 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       25 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       26 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       27 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       28 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       29 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . addBrush  (       30 , QColor (   0 ,   0 ,   0 ,   0 ) )
    ##########################################################################
    for Id in                  [ 11 , 12 , 13 ,                              \
                                 21 , 22 , 23 , 24 , 25 ,                    \
                                 26 , 27 , 28 , 29 , 30                    ] :
      ########################################################################
      self . Painter . pens     [ Id ] . setWidthF ( 2.5                     )
    ##########################################################################
    self . defaultMeasurePoints  (                                           )
    self . PrepareContourDetails (                                           )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions                    ( self                          ) :
    ##########################################################################
    self . AppendSideActionWithIcon        ( "AdjustToSquare"              , \
                                             ":/images/minimize.png"       , \
                                             self . AdjustToSquare         , \
                                             True                          , \
                                             False                           )
    self . AppendWindowToolSeparatorAction (                                 )
    self . AppendSideActionWithIcon        ( "68Facial"                    , \
                                             ":/images/detect-faces.png"   , \
                                             self . Mark68Recognition      , \
                                             True                          , \
                                             False                           )
    self . AppendSideActionWithIcon        ( "468Facial"                   , \
                                             ":/images/human.png"          , \
                                             self . Mark468Recognition     , \
                                             True                          , \
                                             False                           )
    ##########################################################################
    return
  ############################################################################
  def AttachActions    ( self         ,                          Enabled   ) :
    ##########################################################################
    self . LinkAction  ( "OriginalView" ,self.Gui.OriginalView , Enabled     )
    self . LinkAction  ( "ZoomIn"     , self . Gui . ZoomIn    , Enabled     )
    self . LinkAction  ( "ZoomOut"    , self . Gui . ZoomOut   , Enabled     )
    ##########################################################################
    ## self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ## self . LinkAction ( "Load"       , self . LoadPeople      , Enabled      )
    ## self . LinkAction ( "Import"     , self . ImportPeople    , Enabled      )
    ## self . LinkAction ( "Export"     , self . SaveAs          , Enabled      )
    ## self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    ## self . LinkAction ( "Rename"     , self . RenamePeople    , Enabled      )
    self . LinkAction  ( "Delete"     , self.DeleteThisRegion  , Enabled     )
    self . LinkAction  ( "Cut"        , self.CropCurrentImage  , Enabled     )
    ## self . LinkAction ( "Copy"       , self . CopyItems       , Enabled      )
    ## self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    ## self . LinkAction ( "Search"     , self . Search          , Enabled      )
    ## self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    ## self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    ## self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    ## self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    ## self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    ## self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    ##########################################################################
    self . Gui . AttachRatio (                                   True        )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label" , self . Gui . windowTitle (        ) )
    self . AttachActions     ( True                                          )
    self . attachActionsTool (                                               )
    self . statusMessage     ( self . Gui . windowTitle (                  ) )
    self . SwitchSideTools   ( True                                          )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                 ( self                                      ) :
    ##########################################################################
    if                         ( not self . isPrepared ( )                 ) :
      return True
    ##########################################################################
    if                         ( not self . AtMenu                         ) :
      ########################################################################
      self . setActionLabel    ( "Label" , ""                                )
      self . AttachActions     ( False                                       )
      self . detachActionsTool (                                             )
      self . LinkVoice         ( None                                        )
      self . SwitchSideTools   ( False                                       )
    ##########################################################################
    return   True
  ############################################################################
  def Painting                       ( self , p , region , clip , color    ) :
    ##########################################################################
    self . pushPainters              ( p                                     )
    ##########################################################################
    self . Painter . drawRect        ( p , "Default" , self . ScreenRect     )
    self . Painter . drawBorder      ( p , "Default" , self . ScreenRect     )
    ##########################################################################
    self . PaintMeasureRule          (        p , region , clip , color      )
    self . PaintMeasurePoints        (        p , region , clip , color      )
    self . PaintLineEditing          (        p , region , clip , color      )
    ##########################################################################
    if                               ( len ( self . FACEs ) > 0            ) :
      for F in self . FACEs                                                  :
        self . Painter . drawBorder  ( p , "Face"    , F                     )
    ##########################################################################
    if                               ( len ( self . FACEs ) > 0            ) :
      for E in self . EYEs                                                   :
        self . Painter . drawBorder  ( p , "Eyes"    , E                     )
    ##########################################################################
    if                               ( len ( self . FACEs ) > 0            ) :
      for M in self . MOUTHs                                                 :
        self . Painter . drawBorder  ( p , "Mouth"   , M                     )
    ##########################################################################
    self . Painter . drawPainterPath ( p , "Shape"                           )
    self . Painter . drawPainterPath ( p , "RightEyebrow"                    )
    self . Painter . drawPainterPath ( p , "LeftEyebrow"                     )
    self . Painter . drawPainterPath ( p , "NoseBridge"                      )
    self . Painter . drawPainterPath ( p , "NoseNostril"                     )
    self . Painter . drawPainterPath ( p , "RightEye"                        )
    self . Painter . drawPainterPath ( p , "LeftEye"                         )
    self . Painter . drawPainterPath ( p , "OuterMouth"                      )
    self . Painter . drawPainterPath ( p , "InnerMouth"                      )
    self . Painter . drawPainterPath ( p , "FaceRotation"                    )
    ##########################################################################
    if                               ( self . MESHs   [ "Mesh"   ]         ) :
      ########################################################################
      self . DrawFaceMeshes          ( p                                     )
    ##########################################################################
    if                               ( self . POSEs   [ "Pose"   ]         ) :
      ########################################################################
      self . DrawPoseEstimation      ( p                                     )
    ##########################################################################
    if                               ( self . NIPPLEs [ "Nipple" ]         ) :
      ########################################################################
      self . DrawNipples             ( p                                     )
    ##########################################################################
    self . Painter . drawPainterPath ( p , "Contour"                         )
    self . Painter . drawPainterPath ( p , "Quadratic"                       )
    self . Painter . drawPainterPath ( p , "Points"                          )
    self . Painter . drawPainterPath ( p , "Selected"                        )
    ##########################################################################
    self . popPainters               ( p                                     )
    ##########################################################################
    return
  ############################################################################
  def PrepareContourDetails       ( self                                   ) :
    ##########################################################################
    self . convex  = Contour      (                                          )
    self . convex  . setDefaults  (                                          )
    self . convex  . setProperty  ( "MenuLoad"   , True                      )
    self . convex  . setProperty  ( "MenuAppend" , True                      )
    self . convex  . setProperty  ( "MenuStore"  , True                      )
    self . convex  . PathUpdater = self . UpdateContourPoints
    ##########################################################################
    self . Painter . addMap       ( "Contour"   , 10002                      )
    self . Painter . addPen       ( 10002 , QColor ( 255 , 128 ,  64 , 255 ) )
    self . Painter . addBrush     ( 10002 , QColor ( 224 , 255 , 224 ,  96 ) )
    self . Painter . pens [ 10002 ] . setWidthF ( 7.5                        )
    ##########################################################################
    self . Painter . addMap       ( "Quadratic" , 10003                      )
    self . Painter . addPen       ( 10003 , QColor ( 255 , 182 , 193 , 255 ) )
    self . Painter . addBrush     ( 10003 , QColor ( 255 , 224 , 240 ,  96 ) )
    self . Painter . pens [ 10003 ] . setWidthF ( 7.5                        )
    ##########################################################################
    self . Painter . addMap       ( "Points"    , 10008                      )
    self . Painter . addPen       ( 10008 , QColor ( 128 ,  64 , 255 , 255 ) )
    self . Painter . addBrush     ( 10008 , QColor (   0 ,   0 ,   0 ,   0 ) )
    self . Painter . pens [ 10008 ] . setWidthF ( 4.5                        )
    ##########################################################################
    self . Painter . addMap       ( "Selected"  , 10009                       )
    self . Painter . addPen       ( 10009 , QColor ( 128 , 255 ,  64 , 255 ) )
    self . Painter . addBrush     ( 10009 , QColor ( 255 , 128 ,  64 , 255 ) )
    self . Painter . pens [ 10009 ] . setWidthF ( 5.5                        )
    ##########################################################################
    return
  ############################################################################
  def UpdateContourPoints             ( self , convex , ACT , U = True     ) :
    ##########################################################################
    self . defaultUpdateContourPoints (        convex , ACT , U              )
    ##########################################################################
    return
  ############################################################################
  def pjsonToQPointF ( self , JSON                                         ) :
    return QPointF   ( JSON [ "X" ] , JSON [ "Y" ]                           )
  ############################################################################
  def pjsonDrawLine  ( self , p , M , PTS , FK , FI , TK , TI              ) :
    ##########################################################################
    self . Painter . setPainter     ( p , M                                  )
    ##########################################################################
    P1   = self    . pjsonToQPointF ( PTS [ FK ] [ FI ]                      )
    P2   = self    . pjsonToQPointF ( PTS [ TK ] [ TI ]                      )
    p    . drawLine                 ( P1 , P2                                )
    ##########################################################################
    return
  ############################################################################
  def DrawFaceMeshes             ( self , p                                ) :
    ##########################################################################
    self . Painter . setPainter  ( p , "NoseBridge"                          )
    ##########################################################################
    PTS  = self . MESHs          [ "Points" ] [ "Draws"                      ]
    MR   = self . MeshRadius
    ##########################################################################
    for JP in PTS                                                            :
      ########################################################################
      VT = self . pjsonToQPointF ( JP                                        )
      p  . drawEllipse           ( VT , MR , MR                              )
    ##########################################################################
    return
  ############################################################################
  def DrawPoseEstimation            ( self , p                             ) :
    ##########################################################################
    PTS  = self . POSEs             [ "Draws"                                ]
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "NoseNostril"                        , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Shoulder"                           , \
                                      "Right"                              , \
                                      "Shoulder"                             )
    self . pjsonDrawLine            ( p                                    , \
                                      "NoseNostril"                        , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Hip"                                , \
                                      "Right"                              , \
                                      "Hip"                                  )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Shoulder"                           , \
                                      "Left"                               , \
                                      "Elbow"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Elbow"                              , \
                                      "Left"                               , \
                                      "Wrist"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Shoulder"                           , \
                                      "Left"                               , \
                                      "Hip"                                  )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Hip"                                , \
                                      "Left"                               , \
                                      "Knee"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Knee"                               , \
                                      "Left"                               , \
                                      "Ankle"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Ankle"                              , \
                                      "Left"                               , \
                                      "Heel"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "FootIndex"                          , \
                                      "Left"                               , \
                                      "Heel"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "FootIndex"                          , \
                                      "Left"                               , \
                                      "Ankle"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Wrist"                              , \
                                      "Left"                               , \
                                      "Thumb"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Wrist"                              , \
                                      "Left"                               , \
                                      "Index"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Wrist"                              , \
                                      "Left"                               , \
                                      "Pinky"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Left"                               , \
                                      "Index"                              , \
                                      "Left"                               , \
                                      "Pinky"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Shoulder"                           , \
                                      "Right"                              , \
                                      "Elbow"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Elbow"                              , \
                                      "Right"                              , \
                                      "Wrist"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Shoulder"                           , \
                                      "Right"                              , \
                                      "Hip"                                  )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Hip"                                , \
                                      "Right"                              , \
                                      "Knee"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Eyes"                               , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Knee"                               , \
                                      "Right"                              , \
                                      "Ankle"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Ankle"                              , \
                                      "Right"                              , \
                                      "Heel"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "FootIndex"                          , \
                                      "Right"                              , \
                                      "Heel"                                 )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "FootIndex"                          , \
                                      "Right"                              , \
                                      "Ankle"                                )
    ##########################################################################
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Wrist"                              , \
                                      "Right"                              , \
                                      "Thumb"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Wrist"                              , \
                                      "Right"                              , \
                                      "Index"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Wrist"                              , \
                                      "Right"                              , \
                                      "Pinky"                                )
    self . pjsonDrawLine            ( p                                    , \
                                      "Mouth"                              , \
                                      PTS                                  , \
                                      "Right"                              , \
                                      "Index"                              , \
                                      "Right"                              , \
                                      "Pinky"                                )
    ##########################################################################
    self . Painter . setPainter     ( p , "Face"                             )
    ##########################################################################
    VT   = self . pjsonToQPointF    ( PTS [ "Nose" ]                         )
    p    . drawEllipse              ( VT , 8 , 8                             )
    ##########################################################################
    for Side in                     [ "Left" , "Right"                     ] :
      ########################################################################
      KEYs = PTS [ Side ] . keys    (                                        )
      ########################################################################
      for KEY in KEYs                                                        :
        ######################################################################
        JP = PTS                    [ Side ] [ KEY                           ]
        VT = self . pjsonToQPointF  ( JP                                     )
        p  . drawEllipse            ( VT , 8 , 8                             )
    ##########################################################################
    return
  ############################################################################
  def DrawNipples                ( self , p                                ) :
    ##########################################################################
    self  . Painter . setPainter ( p , "RightEye"                            )
    ##########################################################################
    DRAWs = self . NIPPLEs       [ "Draws"                                   ]
    ##########################################################################
    for R in DRAWs                                                           :
      ########################################################################
      X   = R                    [ "X"                                       ]
      Y   = R                    [ "Y"                                       ]
      W   = R                    [ "W"                                       ]
      H   = R                    [ "H"                                       ]
      ########################################################################
      p   . drawRect             ( X , Y , W , H                             )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent        ( self , event                                ) :
    ##########################################################################
    OKAY = self . ContourMouseEvent ( event , self . convex , 0 , True       )
    if                         ( OKAY                                      ) :
      return
    ##########################################################################
    OKAY = self . lineEditingPressEvent   ( event                            )
    if                                    ( OKAY                           ) :
      return
    ##########################################################################
    self . scalePressEvent   ( event                                         )
    self . DeleteGadgets     (                                               )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent         ( self , event                                ) :
    ##########################################################################
    OKAY = self . ContourMouseEvent ( event , self . convex , 1 , True       )
    if                         ( OKAY                                      ) :
      return
    ##########################################################################
    OKAY = self . lineEditingMoveEvent    ( event                            )
    if                                    ( OKAY                           ) :
      return
    ##########################################################################
    self . scaleMoveEvent    (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def mouseReleaseEvent      ( self , event                                ) :
    ##########################################################################
    OKAY = self . ContourMouseEvent ( event , self . convex , 2 , False      )
    if                         ( OKAY                                      ) :
      return
    ##########################################################################
    OKAY = self . lineEditingReleaseEvent ( event                            )
    if                                    ( OKAY                           ) :
      return
    ##########################################################################
    self . scaleReleaseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def Hovering                   ( self , pos                              ) :
    ##########################################################################
    self . convex . HandleQPoint ( pos , 3                                   )
    ##########################################################################
    return
  ############################################################################
  def LinePointsEditingFinished  ( self , P1 , P2                          ) :
    ##########################################################################
    EM     = self . EditingMode
    self   . EditingMode = 0
    ##########################################################################
    if                           ( EM == 23521001                          ) :
      ########################################################################
      self . AssignRuleLine      ( P1 , P2                                   )
      ########################################################################
      return
    ##########################################################################
    if                           ( EM == 23521002                          ) :
      ########################################################################
      self . AssignMeasurePoints ( P1 , P2                                   )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def itemChange ( self , change , value                                   ) :
    ##########################################################################
    if           ( change == QGraphicsItem . ItemPositionChange            ) :
      ########################################################################
      """
      W    = self . ScreenRect . width        (                              )
      H    = self . ScreenRect . height       (                              )
      self . ScreenRect . setTopLeft          ( value                        )
      self . ScreenRect . setWidth            ( W                            )
      self . ScreenRect . setHeight           ( H                            )
      self . PaperPos   = self . pointToPaper ( value                        )
      """
      ########################################################################
      self . signalGeometryChanged            (                              )
    ##########################################################################
    return super ( ) . itemChange             ( change , value               )
  ############################################################################
  def RotateAngle ( self                                                   ) :
    return        ( self . NoseBridge - 270.0                                )
  ############################################################################
  def ClearAll          ( self                                             ) :
    ##########################################################################
    self . NoseBridge = None
    ##########################################################################
    self . FACEs      = [                                                    ]
    self . EYEs       = [                                                    ]
    self . MOUTHs     = [                                                    ]
    self . POSEs      = { "Pose"   : False                                   }
    self . MESHs      = { "Mesh"   : False                                   }
    self . NIPPLEs    = { "Nipple" : False                                   }
    ##########################################################################
    for Id in range     ( 21 , 30                                          ) :
      ########################################################################
      self . Painter . switches = {                                          }
      ########################################################################
      if                ( Id not in self . Painter . pathes                ) :
        continue
      ########################################################################
      try                                                                    :
        ######################################################################
        del self . Painter . pathes [ Id                                     ]
        ######################################################################
      except                                                                 :
        pass
    ##########################################################################
    return
  ############################################################################
  def FaceGeometryChanged    ( self , item                                 ) :
    ##########################################################################
    self . CalculateGeometry (                                               )
    ##########################################################################
    return
  ############################################################################
  def CalculateGeometry ( self                                             ) :
    ##########################################################################
    if                  ( self . PictureItem in [ False , None ]           ) :
      return
    ##########################################################################
    R    = self . PictureItem . RectangleFromItem ( self                     )
    ##########################################################################
    if                  ( not R . isValid ( )                              ) :
      return
    ##########################################################################
    self . Region = R
    ##########################################################################
    return
  ############################################################################
  def CropCurrentImage                   ( self                            ) :
    ##########################################################################
    self . CalculateGeometry             (                                   )
    ##########################################################################
    self . PictureItem . CreateCropImage ( self . Region                     )
    ##########################################################################
    return
  ############################################################################
  def RectToQRectF                                     ( self , R          ) :
    ##########################################################################
    pt = self . Region . topLeft                       (                     )
    ##########################################################################
    return self . PictureItem . PictureRectToItemQRect ( self , pt , R       )
  ############################################################################
  def BasicFacialRecognition                ( self                         ) :
    ##########################################################################
    RECG   = self . GetRecognizer           (                                )
    ##########################################################################
    if                                      ( RECG in self . EmptySet      ) :
      self . Notify                         ( 1                              )
      return
    ##########################################################################
    self   . CalculateGeometry              (                                )
    PIC    = self . PictureItem . PICOP . CropQRect ( self . Region          )
    ##########################################################################
    if                                      ( PIC in self . EmptySet       ) :
      self . Notify                         ( 1                              )
      return
    ##########################################################################
    self   . Gui . OnBusy  . emit           (                                )
    ##########################################################################
    PT     = self . Region . topLeft        (                                )
    PARTs  = RECG . DoDetectSimpleFaceParts ( PIC                            )
    self   . FACEs  = self . PictureItem . PictureRectToItemQRect          ( \
                                              self                         , \
                                              PT                           , \
                                              PARTs [ "Faces" ]              )
    ##########################################################################
    for F in PARTs                          [ "Faces"                      ] :
      ########################################################################
      QR   = self . RectToQRectF            ( F                              )
      self . FACEs . append                 ( QR                             )
    ##########################################################################
    for E in PARTs                          [ "Eyes"                       ] :
      ########################################################################
      QR   = self . RectToQRectF            ( E                              )
      self . EYEs . append                  ( QR                             )
    ##########################################################################
    for M in PARTs                          [ "Mouthes"                    ] :
      ########################################################################
      QR   = self . RectToQRectF            ( M                              )
      self . MOUTHs . append                ( QR                             )
    ##########################################################################
    self   . Gui . GoRelax . emit           (                                )
    self   . CallGeometryChange             (                                )
    self   . Notify                         ( 5                              )
    ##########################################################################
    return
  ############################################################################
  def CvPointToPath          ( self , Id , Closed , Points                 ) :
    ##########################################################################
    PP   = QPainterPath      (                                               )
    PL   = QPolygonF         (                                               )
    ##########################################################################
    RX   = self . PictureItem . Xratio
    RY   = self . PictureItem . Yratio
    BX   = self . Region . x (                                               )
    BY   = self . Region . y (                                               )
    ##########################################################################
    for P in Points                                                          :
      ########################################################################
      XX = P                 [ 0                                             ]
      YY = P                 [ 1                                             ]
      XX = BX + XX
      YY = BY + YY
      ########################################################################
      XX = float             ( float ( XX ) / RX                             )
      YY = float             ( float ( YY ) / RY                             )
      PT = QPointF           ( XX , YY                                       )
      ########################################################################
      PX = self . PictureItem . mapToItem ( self , PT                        )
      ########################################################################
      PL . append            ( PX                                            )
    ##########################################################################
    if                       ( Closed                                      ) :
      ########################################################################
      PP . addPolygon        ( PL                                            )
      PP . closeSubpath      (                                               )
      ########################################################################
    else                                                                     :
      ########################################################################
      AT = 0
      ########################################################################
      for P in PL                                                            :
        ######################################################################
        if                   ( AT == 0                                     ) :
          PP . moveTo        ( P                                             )
        else                                                                 :
          PP . lineTo        ( P                                             )
        ######################################################################
        AT = AT + 1
    ##########################################################################
    self . Painter . pathes   [ Id ] = PP
    self . Painter . switches [ Id ] = True
    ##########################################################################
    return
  ############################################################################
  def DoMark68Recognition                 ( self                           ) :
    ##########################################################################
    RECG   = self . GetRecognizer         (                                  )
    ##########################################################################
    if                                    ( RECG in self . EmptySet        ) :
      self . Notify                       ( 1                                )
      return
    ##########################################################################
    self   . CalculateGeometry            (                                  )
    ##########################################################################
    PIC    = self . PictureItem . PICOP . CropQRect ( self . Region          )
    ##########################################################################
    if                                    ( PIC in self . EmptySet         ) :
      self . Notify                       ( 1                                )
      return
    ##########################################################################
    self   . Gui . OnBusy  . emit         (                                  )
    ##########################################################################
    LMANS  = RECG . DoDetectFaceLandmarks ( PIC                              )
    ##########################################################################
    if LMANS                              [ "Found"                        ] :
      ########################################################################
      LMS  = LMANS                        [ "Landmarks"                      ]
      ########################################################################
      ## self . NoseBridge = LMS             [ "Nose" ] [ "Angle"               ]
      self . NoseBridge = LMS             [ "Face" ] [ "Angle"               ]
      ZERO = int                          ( self . RotateAngle ( ) * 100     )
      if                                  ( 0 == ZERO                      ) :
        self . NoseBridge = None
      ########################################################################
      ## 畫出臉型
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Shape"                    )
      self . CvPointToPath                ( 21 , False , F                   )
      ########################################################################
      ## 畫出右眉(在左邊)
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Eyebrow" , "Right"        )
      self . CvPointToPath                ( 22 , False , F                   )
      ########################################################################
      ## 畫出左眉(在右邊)
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Eyebrow" , "Left"         )
      self . CvPointToPath                ( 23 , False , F                   )
      ########################################################################
      ## 畫出鼻樑
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Nose" , "Bridge"          )
      self . CvPointToPath                ( 24 , False , F                   )
      ########################################################################
      ## 畫出鼻孔部
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Nose" , "Nostril"         )
      self . CvPointToPath                ( 25 , False , F                   )
      ########################################################################
      ## 畫出右眼(在左邊)
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Eyes" , "Right"           )
      self . CvPointToPath                ( 26 , True  , F                   )
      ########################################################################
      ## 畫出左眼(在右邊)
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Eyes" , "Left"            )
      self . CvPointToPath                ( 27 , True , F                    )
      ########################################################################
      ## 畫出外嘴唇
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Mouth" , "Outer"          )
      self . CvPointToPath                ( 28 , True  , F                   )
      ########################################################################
      ## 畫出內嘴唇
      ########################################################################
      F    = RECG . LandmarkToNpArray     ( LMS , "Mouth" , "Inner"          )
      self . CvPointToPath                ( 29 , True  , F                   )
      ########################################################################
      ## 畫出臉部旋轉軸
      ########################################################################
      F    = LMS [ "Face" ]               [ "Axis"                           ]
      self . CvPointToPath                ( 30 , False , F                   )
    ##########################################################################
    self   . Gui . GoRelax . emit         (                                  )
    self   . CallGeometryChange           (                                  )
    self   . Notify                       ( 5                                )
    ##########################################################################
    return
  ############################################################################
  def Mark68Recognition ( self                                             ) :
    ##########################################################################
    self . Go           ( self . DoMark68Recognition                         )
    ##########################################################################
    return
  ############################################################################
  ## MediaPipe Face Mesh Recognition
  ############################################################################
  def DoMark468Recognition                ( self                           ) :
    ##########################################################################
    RECG   = self  . GetRecognizer        (                                  )
    ##########################################################################
    if                                    ( RECG in self . EmptySet        ) :
      self . Notify                       ( 1                                )
      return
    ##########################################################################
    self   . CalculateGeometry            (                                  )
    ##########################################################################
    PIC    = self  . PictureItem . PICOP . CropQRect ( self . Region         )
    ##########################################################################
    if                                    ( PIC in self . EmptySet         ) :
      self . Notify                       ( 1                                )
      return
    ##########################################################################
    self   . Gui   . OnBusy  . emit       (                                  )
    ##########################################################################
    REGZ   = self  . QRectToRectangle     ( self . Region                    )
    SCRZ   = self  . QRectToRectangle     ( self . ScreenRect                )
    OPTs   =                              { "Region" : REGZ                , \
                                            "Screen" : SCRZ                  }
    MESH   = RECG  . DoDetectFaceMeshes   ( PIC , OPTs                       )
    ##########################################################################
    self   . MESHs =                      { "Mesh" : False                   }
    ##########################################################################
    if                                    ( MESH [ "Ready"               ] ) :
      ########################################################################
      BLOB = BytesIO                      (                                  )
      PIC  . Image . format = "png"
      PIC  . Image . save                 ( file = BLOB                      )
      ########################################################################
      self . MESHs =                      { "Mesh"    : True               , \
                                            "Points"  : MESH               , \
                                            "Texture" : BLOB                 }
      self . SyncFaceMesh                 (                                  )
      ########################################################################
      self . Notify                       ( 5                                )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . Notify                       ( 1                                )
    ##########################################################################
    self   . Gui   . GoRelax . emit       (                                  )
    self   . CallGeometryChange           (                                  )
    ##########################################################################
    return
  ############################################################################
  def Mark468Recognition ( self                                            ) :
    ##########################################################################
    self . Go            ( self . DoMark468Recognition                       )
    ##########################################################################
    return
  ############################################################################
  def DoNippleRecognition            ( self                                ) :
    ##########################################################################
    RECG   = self . GetRecognizer    (                                       )
    ##########################################################################
    if                               ( RECG in self . EmptySet             ) :
      self . Notify                  ( 1                                     )
      return
    ##########################################################################
    self   . CalculateGeometry       (                                       )
    ##########################################################################
    PIC    = self . PictureItem . PICOP . CropQRect ( self . Region          )
    ##########################################################################
    if                               ( PIC in self . EmptySet              ) :
      self . Notify                  ( 1                                     )
      return
    ##########################################################################
    PT     = self . Region . topLeft (                                       )
    BOOBs  = RECG . DoDetectAllBoobs ( PIC                                   )
    DRAWs  = self . PictureItem . PictureRectsToLocalRects                 ( \
                                       self                                , \
                                       PT                                  , \
                                       BOOBs                                 )
    ##########################################################################
    if                               ( len ( BOOBs ) > 0                   ) :
      ########################################################################
      self . NIPPLEs =               { "Nipple" : True                     , \
                                       "Boobs"  : BOOBs                    , \
                                       "Draws"  : DRAWs                      }
      ########################################################################
      self . Notify                  ( 5                                     )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . NIPPLEs =               { "Nipple" : False                    , \
                                       "Boobs"  : [                      ] , \
                                       "Draws"  : [                      ]   }
      ########################################################################
      self . Notify                  ( 1                                     )
    ##########################################################################
    self   . CallGeometryChange      (                                       )
    ##########################################################################
    return
  ############################################################################
  def NippleRecognition ( self                                             ) :
    ##########################################################################
    self . Go           ( self . DoNippleRecognition                         )
    ##########################################################################
    return
  ############################################################################
  def DoExtractFaceFeatures               ( self                           ) :
    ##########################################################################
    RECG   = self . GetRecognizer         (                                  )
    ##########################################################################
    if                                    ( RECG in self . EmptySet        ) :
      self . Notify                       ( 1                                )
      return
    ##########################################################################
    self   . CalculateGeometry            (                                  )
    ##########################################################################
    PIC    = self . PictureItem . PICOP . CropQRect ( self . Region          )
    ##########################################################################
    if                                    ( PIC in self . EmptySet         ) :
      self . Notify                       ( 1                                )
      return
    ##########################################################################
    self   . Gui . OnBusy  . emit         (                                  )
    ##########################################################################
    FF     = RECG . DoExtractFaceFeatures ( PIC                              )
    self   . FEATUREs = FF
    ##########################################################################
    if                                    ( FF [ "Ready" ]                 ) :
      ########################################################################
      self . Notify                       ( 5                                )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . Notify                       ( 1                                )
    ##########################################################################
    self   . Gui . GoRelax . emit         (                                  )
    ##########################################################################
    return
  ############################################################################
  def ExtractFaceFeatures ( self                                           ) :
    ##########################################################################
    self . Go             ( self . DoExtractFaceFeatures                     )
    ##########################################################################
    return
  ############################################################################
  def DoIrisCircleDetect                ( self                             ) :
    ##########################################################################
    RECG   = self  . GetRecognizer      (                                    )
    ##########################################################################
    if                                  ( RECG in self . EmptySet          ) :
      self . Notify                     ( 1                                  )
      return
    ##########################################################################
    self   . CalculateGeometry          (                                    )
    ##########################################################################
    PIC    = self  . PictureItem . PICOP . CropQRect ( self . Region         )
    ##########################################################################
    if                                  ( PIC in self . EmptySet           ) :
      self . Notify                     ( 1                                  )
      return
    ##########################################################################
    REGZ   = self  . QRectToRectangle   ( self . Region                      )
    SCRZ   = self  . QRectToRectangle   ( self . ScreenRect                  )
    OPTs   =                            { "Region" : REGZ                  , \
                                          "Screen" : SCRZ                    }
    MESH   = RECG  . DoDetectFaceMeshes ( PIC , OPTs                         )
    ##########################################################################
    self   . MESHs =                    { "Mesh" : False                     }
    ##########################################################################
    if                                  ( MESH [ "Ready"                 ] ) :
      ########################################################################
      ECLR = RECG . DoDetectIrisColor   ( PIC , MESH                         )
      MSG  = json . dumps               ( ECLR                               )
      self . addLog                     ( MSG                                )
      ########################################################################
      self . Notify                     ( 5                                  )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . Notify                     ( 1                                  )
    ##########################################################################
    return
  ############################################################################
  def IrisCircleDetect ( self                                              ) :
    ##########################################################################
    self . Go          ( self . DoIrisCircleDetect                           )
    ##########################################################################
    return
  ############################################################################
  def AdjustToSquare                      ( self                           ) :
    ##########################################################################
    RT   = self . ScreenRect
    WW   = RT   . width                   (                                  )
    HH   = RT   . height                  (                                  )
    ##########################################################################
    RX   = self . PictureItem . Xratio
    RY   = self . PictureItem . Yratio
    ##########################################################################
    RW   = float                          ( RX * WW                          )
    RH   = float                          ( RY * HH                          )
    ##########################################################################
    if                                    ( RW > RH                        ) :
      ########################################################################
      XX = RT   . x                       (                                  )
      YY = RT   . y                       (                                  )
      ########################################################################
      WX = float                          ( RW / RY                          )
      CC = float                          ( YY + float ( HH / 2 )            )
      YY = float                          ( CC - float ( WX / 2 )            )
      self . ScreenRect = QRectF          ( XX , YY , WW , WX                )
      ########################################################################
    else                                                                     :
      ########################################################################
      XX = RT   . x                       (                                  )
      YY = RT   . y                       (                                  )
      ########################################################################
      HY = float                          ( RH / RX                          )
      CC = float                          ( XX + float ( WW / 2 )            )
      XX = float                          ( CC - float ( HY / 2 )            )
      self . ScreenRect = QRectF          ( XX , YY , HY , HH                )
    ##########################################################################
    self . PaperRect = self . rectToPaper ( self . ScreenRect                )
    self . CalculateGeometry              (                                  )
    self . CallGeometryChange             (                                  )
    self . Notify                         ( 5                                )
    ##########################################################################
    return
  ############################################################################
  def AdjustWithinPicture         ( self                                   ) :
    ##########################################################################
    X    = self . Region . x      (                                          )
    Y    = self . Region . y      (                                          )
    W    = self . Region . width  (                                          )
    H    = self . Region . height (                                          )
    L    = int                    ( X + W                                    )
    B    = int                    ( Y + H                                    )
    ##########################################################################
    WW   = self . PictureItem . PICOP . Width  (                             )
    HH   = self . PictureItem . PICOP . Height (                             )
    ##########################################################################
    if ( X >= 0 ) and ( Y >= 0 ) and ( L <= WW ) and ( B <= HH )             :
      return
    ##########################################################################
    if                            ( X < 0                                  ) :
      X  = 0
    ##########################################################################
    if                            ( Y < 0                                  ) :
      Y  = 0
    ##########################################################################
    if                            ( L > WW                                 ) :
      L  = WW
    ##########################################################################
    if                            ( B > HH                                 ) :
      B  = HH
    ##########################################################################
    W    = int                    ( L - X                                    )
    H    = int                    ( B - Y                                    )
    ##########################################################################
    R    = QRect                  ( X , Y , W , H                            )
    ##########################################################################
    JSON =                        { "Function"  : "AdjustFaceRegion"       , \
                                    "Item"      : self                     , \
                                    "Parent"    : self . PictureItem       , \
                                    "Rectangle" : R                          }
    self . DoJsonCaller           ( JSON                                     )
    ##########################################################################
    return
  ############################################################################
  def PeopleDetailsChanged ( self , WhatJSON                               ) :
    ##########################################################################
    Action   = WhatJSON    [ "Action"                                        ]
    ##########################################################################
    if                     ( Action == "Detach"                            ) :
      ########################################################################
      WIDGET = WhatJSON    [ "Widget"                                        ]
      if                   ( WIDGET == self . PeopleDetailsUI              ) :
        self . PeopleDetailsUI = None
        print("Empty PeopleDetailsUI")
      ########################################################################
    elif                   ( Action == "People"                            ) :
      ########################################################################
      self   . PeopleUuid      = WhatJSON [ "People"                         ]
      self   . PeopleUuidAssigned (                                          )
    ##########################################################################
    elif                   ( Action == "Face"                              ) :
      ########################################################################
      Entry  = WhatJSON    [ "Entry"                                         ]
      if                   ( Entry == "Acceptor"                           ) :
        ######################################################################
        CB   = WhatJSON    [ "Callback"                                      ]
        if                 ( CB not in self . FaceCallbacks                ) :
          self . FaceCallbacks . append ( CB                                 )
      ########################################################################
    return                 { "Answer" : "Okay"                               }
  ############################################################################
  def AttachPeopleDetails ( self                                           ) :
    ##########################################################################
    JSON =                { "Function" : "AttachPeopleDetails"             , \
                            "Item"     : self                              , \
                            "Name"     : "人物詳細資訊" }
    self . DoJsonCaller   ( JSON                                             )
    ##########################################################################
    return
  ############################################################################
  def PeopleUuidAssigned ( self                                            ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def DeleteThisRegion ( self                                              ) :
    ##########################################################################
    self . DeleteItem  (                                                     )
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
  def LinePointsEditingFinished  ( self , P1 , P2                          ) :
    ##########################################################################
    EM     = self . EditingMode
    self   . EditingMode = 0
    ##########################################################################
    if                           ( EM == 23521001                          ) :
      ########################################################################
      self . AssignRuleLine      ( P1 , P2                                   )
      ########################################################################
      return
    ##########################################################################
    if                           ( EM == 23521002                          ) :
      ########################################################################
      self . AssignMeasurePoints ( P1 , P2                                   )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def SyncFaceMesh ( self                                                  ) :
    ##########################################################################
    return
    ##########################################################################
    JSON = self . MESHs
    JSON [ "Measure" ]             =                    {                    }
    JSON [ "Measure" ] [ "P1"    ] = self . MeasureRule [ "P1"               ]
    JSON [ "Measure" ] [ "P2"    ] = self . MeasureRule [ "P2"               ]
    JSON [ "Measure" ] [ "Value" ] = self . MeasureRule [ "Value"            ]
    ##########################################################################
    for FCB in self . FaceCallbacks                                          :
      ########################################################################
      FCB          ( JSON                                                    )
    ##########################################################################
    return
  ############################################################################
  def DoCalculateMeanColor             ( self                              ) :
    ##########################################################################
    RECG   = self . GetRecognizer      (                                     )
    ##########################################################################
    if                                 ( RECG in self . EmptySet           ) :
      self . Notify                    ( 1                                   )
      return
    ##########################################################################
    self   . CalculateGeometry         (                                     )
    ##########################################################################
    PIC    = self . PictureItem . PICOP . CropQRect ( self . Region          )
    ##########################################################################
    if                                 ( PIC in self . EmptySet            ) :
      self . Notify                    ( 1                                   )
      return
    ##########################################################################
    RGB    = RECG . CalculateMeanColor ( PIC                                 )
    HSV    = RECG . ConvertRGBtoHSV    ( RGB                                 )
    YUV    = RECG . ConvertRGBtoYUV    ( RGB                                 )
    ##########################################################################
    RMSG   = json . dumps              ( RGB                                 )
    HMSG   = json . dumps              ( HSV                                 )
    YMSG   = json . dumps              ( YUV                                 )
    MSG    = f"{RMSG}\n{HMSG}\n{YMSG}"
    ##########################################################################
    self   . addLog                    ( MSG                                 )
    self   . Notify                    ( 5                                   )
    ##########################################################################
    return
  ############################################################################
  def CalculateMeanColor ( self                                            ) :
    ##########################################################################
    self . Go            ( self . DoCalculateMeanColor                       )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def RecognitionMenu                ( self , mm                           ) :
    ##########################################################################
    TRX  = self . Translations
    ##########################################################################
    MSG  = self . getMenuItem        ( "FeatureRecognition"                  )
    COL  = mm   . addMenu            ( MSG                                   )
    ##########################################################################
    msg  = TRX                       [ "UI::ClearAll"                        ]
    mm   . addActionFromMenu         ( COL , 21451101 , msg                  )
    ##########################################################################
    msg  = self . getMenuItem        ( "EyesMouthFacial"                     )
    mm   . addActionFromMenu         ( COL , 21451102 , msg                  )
    ##########################################################################
    msg  = self . getMenuItem        ( "68Facial"                            )
    ICON = QIcon                     ( ":/images/detect-faces.png"           )
    mm   . addActionFromMenuWithIcon ( COL , 21451103 , ICON , MSG           )
    ##########################################################################
    msg  = self . getMenuItem        ( "468Facial"                           )
    ICON = QIcon                     ( ":/images/human.png"                  )
    mm   . addActionFromMenuWithIcon ( COL , 21451104 , ICON , MSG           )
    ##########################################################################
    msg  = self . getMenuItem        ( "Nipple"                              )
    mm   . addActionFromMenu         ( COL , 21451105 , msg                  )
    ##########################################################################
    msg  = self . getMenuItem        ( "ExtractFaceFeatures"                 )
    mm   . addActionFromMenu         ( COL , 21451106 , msg                  )
    ##########################################################################
    msg  = self . getMenuItem        ( "IrisCircleDetect"                    )
    mm   . addActionFromMenu         ( COL , 21451107 , msg                  )
    ##########################################################################
    return mm
  ############################################################################
  def RunRecognitionMenu            ( self , at                            ) :
    ##########################################################################
    if                              ( at == 21451101                       ) :
      ########################################################################
      self . ClearAll               (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451102                       ) :
      ########################################################################
      self . BasicFacialRecognition (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451103                       ) :
      ########################################################################
      self . Mark68Recognition      (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451104                       ) :
      ########################################################################
      self . Mark468Recognition     (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451105                       ) :
      ########################################################################
      self . NippleRecognition      (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451106                       ) :
      ########################################################################
      self . ExtractFaceFeatures    (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 21451107                       ) :
      ########################################################################
      self . IrisCircleDetect       (                                        )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def PicturesMenu               ( self , mm                               ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "PicturesOperation"                       )
    COL   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "CropImage"                               )
    mm    . addActionFromMenu    ( COL , 21451201 , msg                      )
    ##########################################################################
    if                           ( self . IsOkay ( self . NoseBridge )     ) :
      ########################################################################
      FMT = self . getMenuItem   ( "RotateImage"                             )
      msg = FMT  . format        ( self . RotateAngle ( )                    )
      mm  . addActionFromMenu    ( COL , 21451202 , msg                      )
    ##########################################################################
    mm    = self . RollImageMenu ( mm , COL                                  )
    ##########################################################################
    return mm
  ############################################################################
  def RunPicturesMenu         ( self , at                                  ) :
    ##########################################################################
    angle = self . RollImageSpin . value    (                                )
    self  . LimitValues [ "RollImageAngle" ] = angle
    ##########################################################################
    if                        ( at == 21451201                             ) :
      ########################################################################
      self . CropCurrentImage (                                              )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 21451202                             ) :
      ########################################################################
      self . PictureItem . CreateRotateImage ( self . RotateAngle ( )        )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 21451251                             ) :
      ########################################################################
      self  . PictureItem . CreateRotateImage ( angle                        )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def RegionMenu                      ( self , mm                          ) :
    ##########################################################################
    MSG = self . getMenuItem          ( "RegionOperation"                    )
    COL = mm   . addMenu              ( MSG                                  )
    ##########################################################################
    msg = self . getMenuItem          ( "AdjustToSquare"                     )
    icon  = QIcon                     ( ":/images/minimize.png"              )
    mm    . addActionFromMenuWithIcon ( COL , 21451301 , icon , msg          )
    ##########################################################################
    msg = self . getMenuItem          ( "AdjustWithinPicture"                )
    mm  . addActionFromMenu           ( COL , 21451302 , msg                 )
    ##########################################################################
    msg = self . getMenuItem          ( "MeanColor"                          )
    mm  . addActionFromMenu           ( COL , 21451303 , msg                 )
    ##########################################################################
    return mm
  ############################################################################
  def RunRegionMenu              ( self , at                               ) :
    ##########################################################################
    if                           ( at == 21451301                          ) :
      ########################################################################
      self . AdjustToSquare      (                                           )
      ########################################################################
      return True
    ##########################################################################
    if                           ( at == 21451302                          ) :
      ########################################################################
      self . AdjustWithinPicture (                                           )
      ########################################################################
      return True
    ##########################################################################
    if                           ( at == 21451303                          ) :
      ########################################################################
      self . CalculateMeanColor  (                                           )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def PluginsMenu              ( self , mm                                 ) :
    ##########################################################################
    MSG   = self . getMenuItem ( "PluginsOperation"                          )
    COL   = mm   . addMenu     ( MSG                                         )
    ##########################################################################
    if                         ( self . NotOkay ( self . PeopleDetailsUI ) ) :
      msg = self . getMenuItem ( "AttachPeopleDetails"                       )
      mm  . addActionFromMenu  ( COL , 21451401 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunPluginsMenu             ( self , at                               ) :
    ##########################################################################
    if                           ( at == 21451401                          ) :
      ########################################################################
      self . AttachPeopleDetails (                                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , gview , pos , spos            ) :
    ##########################################################################
    mm     = MenuManager            ( gview                                  )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    R      = self . Region
    XX     = R . x                  (                                        )
    YY     = R . y                  (                                        )
    WW     = R . width              (                                        )
    HH     = R . height             (                                        )
    ##########################################################################
    MSG    = f"( {XX} , {YY} ) - ( {WW} x {HH} )"
    mm     . addAction              ( 34631001 , MSG                         )
    ##########################################################################
    msg    = TRX                    [ "UI::Delete"                           ]
    icon   = QIcon                  ( ":/images/delete.png"                  )
    mm     . addActionWithIcon      ( 1002 , icon , msg                      )
    ##########################################################################
    mm     . addSeparator           (                                        )
    self   . PicturesMenu           ( mm                                     )
    self   . RegionMenu             ( mm                                     )
    self   . RecognitionMenu        ( mm                                     )
    self   . MeasureMenu            ( mm                                     )
    self   . ContourEditorMenu      ( mm , 68727000 , self . convex          )
    self   . StatesMenu             ( mm                                     )
    self   . LayerMenu              ( mm                                     )
    self   . PluginsMenu            ( mm                                     )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                ( gview   . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunContourEditorMenu ( mm , at , 68727000 , self.convex  )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunLayerMenu    ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunMeasureMenu  ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunPicturesMenu ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunRegionMenu   ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunRecognitionMenu ( at                                  )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunPluginsMenu  ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    OKAY   = self . RunStatesMenu   ( at                                     )
    if                              ( OKAY                                 ) :
      return True
    ##########################################################################
    if                              ( at == 1002                           ) :
      ########################################################################
      self . DeleteThisRegion       (                                        )
      ########################################################################
      return True
    ##########################################################################
    return   True
##############################################################################
