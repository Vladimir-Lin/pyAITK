# -*- coding: utf-8 -*-
##############################################################################
## VcfPeoplePicture
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
from   PySide6                                         import QtCore
from   PySide6                                         import QtGui
from   PySide6                                         import QtWidgets
from   PySide6 . QtCore                                import *
from   PySide6 . QtGui                                 import *
from   PySide6 . QtWidgets                             import *
from   AITK    . Qt6                                   import *
from   AITK    . VCF6                                  import *
##############################################################################
from   AITK    . Documents  . JSON                     import Load          as LoadJson
from   AITK    . Documents  . JSON                     import Save          as SaveJson
from   AITK    . Documents  . Variables                import Variables     as VariableItem
##############################################################################
from   AITK    . Essentials . Object                   import Object        as Object
from   AITK    . Pictures   . Picture6                 import Picture       as PictureItem
from   AITK    . Pictures   . Gallery                  import Gallery       as GalleryItem
##############################################################################
from   AITK    . People     . Faces    . Face          import Face          as FaceItem
from   AITK    . People     . Body     . Tit           import Tit           as TitItem
from   AITK    . People     . Body     . Body          import Body          as BodyItem
##############################################################################
from   AITK    . People     . Faces6   . VcfFaceRegion import VcfFaceRegion as VcfFaceRegion
##############################################################################
from   AITK    . Math       . Geometry . Contour       import Contour       as Contour
##############################################################################
class VcfPeoplePicture           ( VcfPicture                              ) :
  ############################################################################
  def __init__                   ( self                                    , \
                                   parent = None                           , \
                                   item   = None                           , \
                                   plan   = None                           ) :
    ##########################################################################
    super ( ) . __init__         ( parent , item , plan                      )
    self . setVcfPeoplePictureDefaults (                                     )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfPeoplePictureDefaults ( self                                   ) :
    ##########################################################################
    self . SquareFactor  = 1.5
    self . HumanMeasure  = None
    self . CurrentPeople =        {                                          }
    self . Descriptions  =        {                                          }
    ##########################################################################
    self . LastestZ      = None
    self . setFlag                ( QGraphicsItem . ItemIsMovable , False    )
    self . setZValue              ( 10000                                    )
    ##########################################################################
    self . defaultMeasurePoints   (                                          )
    self . PrepareContourDetails  (                                          )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendSideActionWithIcon ( "AddSelectionRegion"                 , \
                                      ":/images/selectimage.png"           , \
                                      self . AddSelectionRegion            , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "AddSmallRegion"                     , \
                                      ":/images/maximize.png"              , \
                                      self . AddSmallRegion                , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "SquareFacial"                       , \
                                      ":/images/frame.png"                 , \
                                      self . RunSquareFacial               , \
                                      True                                 , \
                                      False                                  )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "OriginalView" ,self.Gui.OriginalView , Enabled      )
    self . LinkAction ( "ZoomIn"     , self . Gui . ZoomIn    , Enabled      )
    self . LinkAction ( "ZoomOut"    , self . Gui . ZoomOut   , Enabled      )
    ##########################################################################
    ## self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ## self . LinkAction ( "Load"       , self . LoadPeople      , Enabled      )
    ## self . LinkAction ( "Import"     , self . ImportPeople    , Enabled      )
    self . LinkAction ( "Export"     , self . SaveAs          , Enabled      )
    ## self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    ## self . LinkAction ( "Rename"     , self . RenamePeople    , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItem      , Enabled      )
    ## self . LinkAction ( "Cut"        , self . DeleteItems     , Enabled      )
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
    self   . pushPainters            ( p                                     )
    ##########################################################################
    if                               ( clip                                ) :
      self . PaintImageClip          (        p , region , clip , color      )
    else                                                                     :
      self . PaintImage              (        p , region , clip , color      )
    ##########################################################################
    self   . PaintMeasureRule        (        p , region , clip , color      )
    self   . PaintMeasurePoints      (        p , region , clip , color      )
    self   . PaintLineEditing        (        p , region , clip , color      )
    self   . Painter . drawAllPathes (        p                              )
    ##########################################################################
    self   . popPainters             ( p                                     )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent          ( self , event                              ) :
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
  def mouseMoveEvent           ( self , event                              ) :
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
  def RectangleFromItem  ( self , item                                     ) :
    ##########################################################################
    R = item . mapToItem ( self , item . ScreenRect                          )
    ##########################################################################
    X = R [ 0 ] . x      (                                                   )
    Y = R [ 0 ] . y      (                                                   )
    W = R [ 2 ] . x      (                                                   )
    H = R [ 2 ] . y      (                                                   )
    W = W - X
    H = H - Y
    ##########################################################################
    X = int              ( X * self . Xratio                                 )
    Y = int              ( Y * self . Yratio                                 )
    W = int              ( W * self . Xratio                                 )
    H = int              ( H * self . Yratio                                 )
    ##########################################################################
    return QRect         ( X , Y , W , H                                     )
  ############################################################################
  def setCurrentPeople  ( self , JSON                                      ) :
    ##########################################################################
    self . CurrentPeople = JSON
    ##########################################################################
    PEOJ = json . dumps ( JSON                                               )
    self . addLog       ( f"VcfPeoplePicture : {PEOJ}"                       )
    ##########################################################################
    return
  ############################################################################
  def leaveHumanMeasure ( self , widget                                    ) :
    ##########################################################################
    if                  ( widget == self . HumanMeasure                    ) :
      self . HumanMeasure = None
    ##########################################################################
    return
  ############################################################################
  def setHumanMeasure          ( self , widget                             ) :
    ##########################################################################
    self . HumanMeasure = widget
    ##########################################################################
    if                         ( widget not in self . EmptySet             ) :
      ########################################################################
      widget . Leave . connect ( self . leaveHumanMeasure                    )
      self   . addLog          ( "Human Body Measurement connected"          )
    ##########################################################################
    return
  ############################################################################
  def GetCurrentPeople  ( self                                             ) :
    ##########################################################################
    JSON =              { "Function" : "GetCurrentPeople"                  , \
                          "Item"     : self                                  }
    self . DoJsonCaller ( JSON                                               )
    ##########################################################################
    return
  ############################################################################
  def ConnectMeasure    ( self                                             ) :
    ##########################################################################
    JSON =              { "Function" : "ConnectMeasure"                    , \
                          "Item"     : self                                  }
    self . DoJsonCaller ( JSON                                               )
    ##########################################################################
    return
  ############################################################################
  def AddBodyRegion            ( self , KeyPoints                          ) :
    ##########################################################################
    SIZE = self . Image . size (                                             )
    W    = SIZE . width        (                                             )
    H    = SIZE . height       (                                             )
    RECT = QRect               ( 0 , 0 , W , H                               )
    ##########################################################################
    JSON =                     { "Function"  : "AddBodyRegion"             , \
                                 "Item"      : self                        , \
                                 "Region"    : RECT                        , \
                                 "Points"    : KeyPoints                     }
    self . DoJsonCaller        ( JSON                                        )
    ##########################################################################
    return
  ############################################################################
  def AddFaceRegion     ( self , rect                                      ) :
    ##########################################################################
    JSON =              { "Function"  : "AddFaceRegion"                    , \
                          "Item"      : self                               , \
                          "Rectangle" : rect                                 }
    self . DoJsonCaller ( JSON                                               )
    ##########################################################################
    return
  ############################################################################
  def AddSelectionRegion         ( self                                    ) :
    ##########################################################################
    W    = self . Image . width  (                                           )
    H    = self . Image . height (                                           )
    R    = QRect                 ( 0 , 0 , W , H                             )
    ##########################################################################
    self . AddFaceRegion         ( R                                         )
    self . Notify                ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def AddSmallRegion             ( self                                    ) :
    ##########################################################################
    W    = self . Image . width  (                                           )
    H    = self . Image . height (                                           )
    R    = QRect                 ( 0 , 0 , W / 4 , H / 4                     )
    ##########################################################################
    self . AddFaceRegion         ( R                                         )
    self . Notify                ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def FacialRecognition                   ( self , Square = False          ) :
    ##########################################################################
    RECG     = self . GetRecognizer       (                                  )
    ##########################################################################
    if                                    ( RECG in self . EmptySet        ) :
      return
    ##########################################################################
    self     . Gui . OnBusy  . emit       (                                  )
    ##########################################################################
    WW       = self . PICOP . Width       (                                  )
    HH       = self . PICOP . Height      (                                  )
    FACEs    = RECG . DoDetectSimpleFaces ( self . PICOP                     )
    ##########################################################################
    if                                    ( len ( FACEs ) <= 0             ) :
      ########################################################################
      self   . Notify                     ( 1                                )
      ########################################################################
      return
    ##########################################################################
    for F in FACEs                                                           :
      ########################################################################
      WW     = F                          [ "W"                              ]
      HH     = F                          [ "H"                              ]
      ########################################################################
      if                                  ( WW < 96                        ) :
        continue
      ########################################################################
      if                                  ( HH < 96                        ) :
        continue
      ########################################################################
      if                                  ( Square                         ) :
        ######################################################################
        FACE = FaceItem                   (                                  )
        FACE . setFull                    ( WW , HH                          )
        F    = FACE . ToSquareRestraint   ( F , self . SquareFactor          )
      ########################################################################
      R      = self . RectangleToQRect    ( F                                )
      self   . AddFaceRegion              ( R                                )
    ##########################################################################
    self     . Gui . GoRelax . emit       (                                  )
    self     . CallGeometryChange         (                                  )
    self     . Notify                     ( 5                                )
    ##########################################################################
    return
  ############################################################################
  def RunSquareFacial ( self                                               ) :
    ##########################################################################
    self . Go         ( self . FacialRecognition , ( True  , )               )
    ##########################################################################
    return
  ############################################################################
  def BodyPoseEstimation             ( self                                ) :
    ##########################################################################
    RECG = self . GetRecognizer      (                                       )
    ##########################################################################
    if                               ( RECG in self . EmptySet             ) :
      return
    ##########################################################################
    KPS  = RECG . DoDetectSimpleBody ( self . PICOP                          )
    self . AddBodyRegion             ( KPS                                   )
    self . CallGeometryChange        (                                       )
    self . Notify                    ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def BoobsRecognition                       ( self                        ) :
    ##########################################################################
    RECG    = self . GetRecognizer           (                               )
    ##########################################################################
    if                                       ( RECG in self . EmptySet     ) :
      return
    ##########################################################################
    BOOBs   = RECG . DoDetectSimpleBoobs     ( self . PICOP                  )
    DLIBs   = RECG . DoDetectSimpleDlibBoobs ( self . PICOP                  )
    ##########################################################################
    for BF in DLIBs                                                          :
      BOOBs . append                         ( BF                            )
    ##########################################################################
    if                                       ( len ( BOOBs ) <= 0          ) :
      ########################################################################
      self  . Notify                         ( 1                             )
      ########################################################################
      return
    ##########################################################################
    for RT in BOOBs                                                          :
      ########################################################################
      R     = self . RectangleToQRect        ( RT                            )
      self  . AddFaceRegion                  ( R                             )
    ##########################################################################
    self    . CallGeometryChange             (                               )
    self    . Notify                         ( 5                             )
    ##########################################################################
    return
  ############################################################################
  def ProduceRotateImage         ( self , degree                           ) :
    ##########################################################################
    PIC  = self . PICOP . Rotate ( degree                                    )
    ##########################################################################
    if                           ( self . LastestZ in [ False , None ]     ) :
      self . LastestZ = self . zValue ( ) + 10.0
    else                                                                     :
      self . LastestZ = self . LastestZ   + 10.0
    ##########################################################################
    JSON =                       { "Function"  : "AddPicture"              , \
                                   "Picture"   : PIC                       , \
                                   "Z"         : self . LastestZ             }
    self . DoJsonCaller          ( JSON                                      )
    ##########################################################################
    return
  ############################################################################
  def CreateRotateImage            ( self , degree                         ) :
    ##########################################################################
    VAL  =                         ( degree ,                                )
    self . Go                      ( self . ProduceRotateImage , VAL         )
    ##########################################################################
    return
  ############################################################################
  def CropCurrentImage        ( self , region                              ) :
    ##########################################################################
    X   = region . x          (                                              )
    Y   = region . y          (                                              )
    W   = region . width      (                                              )
    H   = region . height     (                                              )
    PIC = self . PICOP . Crop ( X , Y , W , H                                )
    ##########################################################################
    return PIC
  ############################################################################
  def ProduceCropImage               ( self , region                       ) :
    ##########################################################################
    PIC    = self . CropCurrentImage (        region                         )
    ##########################################################################
    if                               ( self . LastestZ in [ False , None ] ) :
      self . LastestZ = self . zValue ( ) + 10.0
    else                                                                     :
      self . LastestZ = self . LastestZ   + 10.0
    ##########################################################################
    JSON =                           { "Function" : "AddPicture"           , \
                                       "Picture"  : PIC                    , \
                                       "Z"        : self . LastestZ          }
    self . DoJsonCaller              ( JSON                                  )
    ##########################################################################
    return
  ############################################################################
  def CreateCropImage              ( self , region                         ) :
    ##########################################################################
    VAL  =                         ( region ,                                )
    self . Go                      ( self . ProduceCropImage , VAL           )
    ##########################################################################
    return
  ############################################################################
  def SaveAs                          ( self                               ) :
    ##########################################################################
    TITLE        = self . getMenuItem ( "ExportPicture"                      )
    FILTERs      = self . getMenuItem ( "PictureFilters"                     )
    Filename , _ = QFileDialog . getSaveFileName                           ( \
                                        self . Gui                         , \
                                        TITLE                              , \
                                        ""                                 , \
                                        FILTERs                              )
    if                                ( len ( Filename ) <= 0              ) :
      return
    ##########################################################################
    self . Image . save               ( Filename                             )
    self . Notify                     ( 5                                    )
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
  def ReportDetections ( self , RECG                                       ) :
    ##########################################################################
    if                 ( "Description" not in self . Descriptions          ) :
      return
    ##########################################################################
    DESC    = self . Descriptions   [ "Description"                          ]
    ##########################################################################
    if                              ( "Things" not in DESC                 ) :
      DESC  = RECG . CollectThings  ( DESC                                   )
    ##########################################################################
    THINGs  = DESC                  [ "Things"                               ]
    self    . addLog                ( "\n" . join ( THINGs )                 )
    ##########################################################################
    ## print ( json . dumps ( DESC ) )
    ## if                              ( "Classification" in DESC             ) :
    ##   ########################################################################
    ##   ITEMs = DESC                  [ "Classification"                       ]
    ##   RECG  . ReportClassifications ( ITEMs , self . addLog                  )
    ##########################################################################
    ## if                              ( "Objects"        in DESC             ) :
    ##   ########################################################################
    ##   ITEMs = DESC                  [ "Objects"                              ]
    ##   RECG  . ReportObjects         ( ITEMs , self . addLog                  )
    ##########################################################################
    return
  ############################################################################
  def FetchPictureDetections        ( self                                 ) :
    ##########################################################################
    UUID   = self . ObjectUuid      (                                        )
    ##########################################################################
    if                              ( UUID <= 0                            ) :
      return
    ##########################################################################
    RECG   = self . GetRecognizer   (                                        )
    ##########################################################################
    if                              ( RECG in self . EmptySet              ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    ##########################################################################
    if                              ( self . NotOkay ( DB )                ) :
      ########################################################################
      self . Notify                 ( 1                                      )
      ########################################################################
      return
    ##########################################################################
    VARTAB = self . Tables          [ "DescribeVariables"                    ]
    ##########################################################################
    PV     = VariableItem           (                                        )
    ##########################################################################
    PV     . Type = 9
    PV     . Name = "Description"
    PV     . Uuid = UUID
    ##########################################################################
    RECJ   = PV   . GetValue        ( DB , VARTAB                            )
    ##########################################################################
    if                              ( RECJ not in self . EmptySet          ) :
      ########################################################################
      if                            ( len ( RECJ ) > 0                     ) :
        ######################################################################
        try                                                                  :
          ####################################################################
          BODY   = RECJ . decode    ( "utf-8"                                )
          ####################################################################
          if                        ( len ( BODY ) > 0                     ) :
            ##################################################################
            JJ   = json . loads     ( BODY                                   )
            self . Descriptions = JJ
            self . ReportDetections ( RECG                                   )
          ####################################################################
        except                                                               :
          pass
    ##########################################################################
    DB     . Close                  (                                        )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def ShowObjectRectangles ( self                                          ) :
    ##########################################################################
    if                     ( "Description" not in self . Descriptions      ) :
      return
    ##########################################################################
    DESC   = self . Descriptions     [ "Description"                         ]
    ##########################################################################
    if                               ( "Objects" not in DESC               ) :
      return
    ##########################################################################
    ITEMs  = DESC                    [ "Objects"                             ]
    ##########################################################################
    if                               ( len ( ITEMs ) <= 0                  ) :
      return
    ##########################################################################
    for IT in ITEMs                                                          :
      ########################################################################
      if                             ( "Box" not in IT                     ) :
        continue
      ########################################################################
      R    = self . RectangleToQRect ( IT [ "Box"                          ] )
      ########################################################################
      self . AddFaceRegion           ( R                                     )
    ##########################################################################
    self   . Notify                  ( 5                                     )
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
  def PictureOpsMenu          ( self , mm                                  ) :
    ##########################################################################
    UUID = self . ObjectUuid  (                                              )
    ##########################################################################
    if                        ( UUID <= 0                                  ) :
      return
    ##########################################################################
    MSG  = self . getMenuItem ( "PicturesProcess"                            )
    LOM  = mm   . addMenu     ( MSG                                          )
    ##########################################################################
    MSG  = self . getMenuItem ( "FetchDetections"                            )
    mm   . addActionFromMenu  ( LOM , 38913101 , MSG                         )
    ##########################################################################
    MSG  = self . getMenuItem ( "ShowObjectRectangles"                       )
    mm   . addActionFromMenu  ( LOM , 38913102 , MSG                         )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def RunPictureOpsMenu ( self , at                                        ) :
    ##########################################################################
    if                  ( 38913101 == at                                   ) :
      ########################################################################
      self . Go         ( self . FetchPictureDetections                      )
      ########################################################################
      return True
    ##########################################################################
    if                  ( 38913102 == at                                   ) :
      ########################################################################
      self . Go         ( self . ShowObjectRectangles                        )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def PeopleFaceMenu               ( self , mm , Menu                      ) :
    ##########################################################################
    MSG   = self . getMenuItem     ( "FacialRecognition"                     )
    LOM   = mm   . addMenuFromMenu ( Menu , MSG                              )
    ##########################################################################
    MSG   = self . getMenuItem     ( "BasicFacial"                           )
    mm    . addActionFromMenu      ( LOM , 98438501 , MSG                    )
    ##########################################################################
    MSG   = self . getMenuItem     ( "SquareFacial"                          )
    ICON  = QIcon                  ( ":/images/frame.png"                    )
    mm    . addActionFromMenuWithIcon ( LOM , 98438502 , ICON , MSG          )
    ##########################################################################
    return
  ############################################################################
  def PeopleBodyMenu               ( self , mm , Menu                      ) :
    ##########################################################################
    MSG   = self . getMenuItem     ( "BodyRecognition"                       )
    LOM   = mm   . addMenuFromMenu ( Menu , MSG                              )
    ##########################################################################
    MSG   = self . getMenuItem     ( "PoseEstimation"                        )
    mm    . addActionFromMenu      ( LOM , 98438601 , MSG                    )
    ##########################################################################
    MSG   = self . getMenuItem     ( "BoobsRecognition"                      )
    mm    . addActionFromMenu      ( LOM , 98438602 , MSG                    )
    ##########################################################################
    return
  ############################################################################
  def RecognitionMenu            ( self , mm                               ) :
    ##########################################################################
    MSG   = self . getMenuItem   ( "FeatureRecognition"                      )
    LOM   = mm   . addMenu       ( MSG                                       )
    ##########################################################################
    MSG   = self . getMenuItem   ( "RelatePeople"                            )
    mm    . addActionFromMenu    ( LOM , 98438301 , MSG                      )
    ##########################################################################
    MSG   = self . getMenuItem   ( "AddSelectionRegion"                      )
    ICON  = QIcon                ( ":/images/selectimage.png"                )
    mm    . addActionFromMenuWithIcon ( LOM , 98438302 , ICON , MSG          )
    ##########################################################################
    MSG   = self . getMenuItem   ( "AddSmallRegion"                          )
    ICON  = QIcon                ( ":/images/maximize.png"                   )
    mm    . addActionFromMenuWithIcon ( LOM , 98438303 , ICON , MSG          )
    ##########################################################################
    mm    = self . RollImageMenu ( mm , LOM                                  )
    mm    . addSeparatorFromMenu ( LOM                                       )
    ##########################################################################
    self  . PeopleFaceMenu       ( mm , LOM                                  )
    self  . PeopleBodyMenu       ( mm , LOM                                  )
    ##########################################################################
    return
  ############################################################################
  def RunRecognitionMenu        ( self , at                                ) :
    ##########################################################################
    angle = self . RollImageSpin . value    (                              )
    self  . LimitValues [ "RollImageAngle" ] = angle
    ##########################################################################
    if                          ( at == 98438301                           ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438302                           ) :
      ########################################################################
      self . AddSelectionRegion (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438303                           ) :
      ########################################################################
      self . AddSmallRegion     (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438501                           ) :
      ########################################################################
      self . Go                 ( self . FacialRecognition , ( False , )     )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438502                           ) :
      ########################################################################
      self . RunSquareFacial    (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438601                           ) :
      ########################################################################
      self . Go                 ( self . BodyPoseEstimation                  )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 98438602                           ) :
      ########################################################################
      self . Go                 ( self . BoobsRecognition                    )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 21451251                             ) :
      ########################################################################
      self  . CreateRotateImage ( angle                                      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                      ( self , gview , pos , spos                ) :
    ##########################################################################
    mm     = MenuManager        ( gview                                      )
    ##########################################################################
    self   . InformationMenu    ( mm                                         )
    mm     . addSeparator       (                                            )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    msg    = TRX                [ "UI::Delete"                               ]
    icon   = QIcon              ( ":/images/delete.png"                      )
    mm     . addActionWithIcon  ( 1001 , icon , msg                          )
    ##########################################################################
    msg    = self . getMenuItem ( "SaveImage"                                )
    icon   = QIcon              ( ":/images/GoRight.png"                     )
    mm     . addActionWithIcon  ( 1002 , icon , msg                          )
    ##########################################################################
    msg    = self . getMenuItem ( "OriginalPosition"                         )
    mm     . addAction          ( 1003 , msg                                 )
    ##########################################################################
    mm     . addSeparator       (                                            )
    ##########################################################################
    msg    = self . getMenuItem ( "ObtainsCurrentPeople"                     )
    mm     . addAction          ( 4001 , msg                                 )
    msg    = self . getMenuItem ( "ConnectHumanMeasure"                      )
    mm     . addAction          ( 4002 , msg                                 )
    msg    = self . getMenuItem ( "LoadDescriptions"                         )
    mm     . addAction          ( 4003 , msg                                 )
    ##########################################################################
    mm     . addSeparator       (                                            )
    self   . PictureOpsMenu     ( mm                                         )
    self   . ContourEditorMenu  ( mm , 7000 , self . convex                  )
    self   . RecognitionMenu    ( mm                                         )
    self   . MeasureMenu        ( mm                                         )
    self   . StatesMenu         ( mm                                         )
    self   . LayerMenu          ( mm                                         )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont            ( gview   . menuFont ( )                     )
    aa     = mm . exec_         ( QCursor . pos      ( )                     )
    at     = mm . at            ( aa                                         )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunLayerMenu       ( at                                  )
    if                          ( OKAY                                     ) :
      return True
    ##########################################################################
    OKAY   = self . RunMeasureMenu     ( at                                  )
    if                          ( OKAY                                     ) :
      return True
    ##########################################################################
    OKAY   = self . RunStatesMenu      ( at                                  )
    if                          ( OKAY                                     ) :
      return True
    ##########################################################################
    OKAY   = self . RunRecognitionMenu ( at                                  )
    if                          ( OKAY                                     ) :
      return True
    ##########################################################################
    OKAY   = self . RunContourEditorMenu ( mm , at , 7000 , self . convex    )
    if                          ( OKAY                                     ) :
      return True
    ##########################################################################
    OKAY   = self . RunPictureOpsMenu ( at                                   )
    if                          ( OKAY                                     ) :
      return True
    ##########################################################################
    if                          ( at == 1001                               ) :
      ########################################################################
      self . DeleteItem         (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 1002                               ) :
      ########################################################################
      self . SaveAs             (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( at == 1003                               ) :
      ########################################################################
      self . OriginalRect       (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 4001 == at                               ) :
      ########################################################################
      self . GetCurrentPeople   (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 4002 == at                               ) :
      ########################################################################
      self . ConnectMeasure     (                                            )
      ########################################################################
      return True
    ##########################################################################
    if                          ( 4003 == at                               ) :
      ########################################################################
      ########################################################################
      return True
    ##########################################################################
    return   True
##############################################################################
