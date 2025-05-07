# -*- coding: utf-8 -*-
##############################################################################
## PictureEditor
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import binascii
import hashlib
import base64
##############################################################################
from   io                                                   import BytesIO
from   wand . image                                         import Image
from   PIL                                                  import Image            as Pillow
##############################################################################
from   PySide6                                              import QtCore
from   PySide6                                              import QtGui
from   PySide6                                              import QtWidgets
from   PySide6 . QtCore                                     import *
from   PySide6 . QtGui                                      import *
from   PySide6 . QtWidgets                                  import *
from   AITK    . Qt6                                        import *
from   AITK    . VCF6                                       import *
##############################################################################
from   AITK    . Pictures . Picture6                        import Picture          as PictureItem
from   AITK    . Pictures . Gallery                         import Gallery          as GalleryItem
##############################################################################
from   AITK    . People   . Faces6       . VcfFaceRegion    import VcfFaceRegion    as VcfFaceRegion
## from   AITK    . People   . Measurements . VcfMeasureRegion import VcfMeasureRegion as VcfMeasureRegion
from   AITK    . People   . Widgets6     . VcfPeoplePicture import VcfPeoplePicture as VcfPeoplePicture
from   AITK    . People   . Widgets6     . PeopleDetails    import PeopleDetails    as PeopleDetails
##############################################################################
class PictureEditor               ( VcfWidget                              ) :
  ############################################################################
  ObtainsCurrentPeople = Signal   ( QWidget                                  )
  ConnectHumanMeasure  = Signal   ( QWidget                                  )
  Adjustment           = Signal   ( QWidget , QSize                          )
  JsonCallback         = Signal   ( dict                                     )
  Leave                = Signal   ( QWidget                                  )
  emitGeometryChange   = Signal   ( QGraphicsItem                            )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          (        parent ,        plan              )
    ##########################################################################
    self . MainGui       = None
    self . HumanMeasure  = None
    self . RequestItem   = None
    self . MainTables    =              {                                    }
    self . CurrentPeople =              {                                    }
    self . setJsonCaller                ( self . JsonCaller                  )
    self . JsonCallback       . connect ( self . JsonAccepter                )
    self . emitGeometryChange . connect ( self . doGeometryChange            )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions ( self                                             ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    """
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Import"     , self . ImportPictures  , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Cut"        , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    """
    ##########################################################################
    self . LinkAction  ( "OriginalView" , self . OriginalView  , Enabled     )
    self . LinkAction  ( "ZoomIn"       , self . ZoomIn        , Enabled     )
    self . LinkAction  ( "ZoomOut"      , self . ZoomOut       , Enabled     )
    ##########################################################################
    self . AttachRatio (                                         Enabled     )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label" , self . windowTitle ( )              )
    self . AttachActions     ( True                                          )
    self . attachActionsTool (                                               )
    ## self . LinkVoice         ( self . CommandParser                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . LinkVoice         ( None                                          )
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def JsonCaller               ( self , JSON                               ) :
    ##########################################################################
    self . JsonCallback . emit (        JSON                                 )
    ##########################################################################
    return
  ############################################################################
  def JsonAccepter               ( self , JSON                             ) :
    ##########################################################################
    CALLER = JSON                [ "Function"                                ]
    ##########################################################################
    if                           ( CALLER == "DeleteItem"                  ) :
      ########################################################################
      ITEM = JSON                [ "Item"                                    ]
      self . takeItem            ( ITEM                                      )
      self . Scene . removeItem  ( ITEM                                      )
      ########################################################################
      return
    ##########################################################################
    if                           ( CALLER == "AddFaceRegion"               ) :
      ########################################################################
      ITEM   = JSON              [ "Item"                                    ]
      RECT   = JSON              [ "Rectangle"                               ]
      self   . AddFaceRegion     ( ITEM , RECT                               )
      ########################################################################
      return
    ##########################################################################
    if                           ( CALLER == "AddBodyRegion"               ) :
      ########################################################################
      ITEM   = JSON              [ "Item"                                    ]
      RECT   = JSON              [ "Region"                                  ]
      POINTS = JSON              [ "Points"                                  ]
      self   . AddBodyRegion     ( ITEM , RECT , POINTS                      )
      ########################################################################
      return
    ##########################################################################
    if                           ( CALLER == "AdjustFaceRegion"            ) :
      ########################################################################
      ITEM   = JSON              [ "Item"                                    ]
      PARENT = JSON              [ "Parent"                                  ]
      RECT   = JSON              [ "Rectangle"                               ]
      self   . AdjustFaceRegion  ( ITEM , PARENT , RECT                      )
      ########################################################################
      return
    ##########################################################################
    if                           ( CALLER == "AddPicture"                  ) :
      ########################################################################
      PIC  = JSON                [ "Picture"                                 ]
      Z    = JSON                [ "Z"                                       ]
      self . AddPicture          ( PIC , Z                                   )
      ########################################################################
      return
    ##########################################################################
    if                           ( CALLER == "AttachPeopleDetails"         ) :
      ########################################################################
      ITEM = JSON                [ "Item"                                    ]
      NAME = JSON                [ "Name"                                    ]
      self . AttachPeopleDetails ( NAME , ITEM                               )
      ########################################################################
      return
    ##########################################################################
    if                           ( CALLER == "GetCurrentPeople"            ) :
      ########################################################################
      ITEM = JSON                [ "Item"                                    ]
      self . RequestItem = ITEM
      ########################################################################
      self . ObtainsCurrentPeople . emit ( self                              )
      ########################################################################
      return
    ##########################################################################
    if                                  ( CALLER == "ConnectMeasure"       ) :
      ########################################################################
      ITEM = JSON                       [ "Item"                             ]
      self . RequestItem = ITEM
      ########################################################################
      self . ConnectHumanMeasure . emit ( self                               )
      ########################################################################
      return
    ##########################################################################
    if                                  ( CALLER == "GeometryChange"       ) :
      ########################################################################
      ITEM = JSON                       [ "Item"                             ]
      ########################################################################
      self . emitGeometryChange . emit ( ITEM                                )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def setCurrentPeople ( self , JSON                                       ) :
    ##########################################################################
    self . CurrentPeople = JSON
    ##########################################################################
    if                 ( self . RequestItem in self . EmptySet             ) :
      return
    ##########################################################################
    self . RequestItem . setCurrentPeople ( JSON                             )
    self . RequestItem = None
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
      widget . Leave . connect ( self . leaveHumanMeasure                    )
    ##########################################################################
    if                         ( self . RequestItem in self . EmptySet     ) :
      return
    ##########################################################################
    self . RequestItem . setHumanMeasure ( widget                            )
    self . RequestItem = None
    ##########################################################################
    return
  ############################################################################
  def WindowSizeView             ( self , size                             ) :
    ##########################################################################
    self . View = self . asPaper ( self . available ( size )                 )
    self . Scene . setSceneRect  ( self . View                               )
    self . setTransform          ( self . Transform                          )
    ##########################################################################
    return
  ############################################################################
  def AttachPeopleDetails ( self , Name , Item                             ) :
    ##########################################################################
    PDW = PeopleDetails   ( None , self . PlanFunc                           )
    ##########################################################################
    FUNC               = self  . MainGui . DynamicVariantTables
    FACE               = self  . MainGui . OpenFaceModel
    PDW . Settings     = self  . Settings
    PDW . Translations = self  . Translations
    PDW . Tables       = self  . MainTables [ "PeopleDetails"                ]
    PDW . DB           = self  . Settings   [ "Database"                     ]
    PDW . DynamicVariantTables . connect    ( FUNC                           )
    PDW . OpenFaceModel        . connect    ( FACE                           )
    ##########################################################################
    self . addControl             ( Name , PDW , self                        )
    Item . PeopleDetailsUI = PDW
    PDW  . AttachExternalFunction ( Item . PeopleDetailsChanged              )
    PDW  . startup                (                                          )
    ##########################################################################
    return
  ############################################################################
  def AddFaceRegion              ( self , parent , rect                    ) :
    ##########################################################################
    PM   = QPoint                ( rect . x     ( ) , rect . y      ( )      )
    SP   = self   . mapToScene   ( PM                                        )
    XS   = parent . mapFromScene ( SP                                        )
    XP   = parent . pointToPaper ( XS                                        )
    ##########################################################################
    PM   = QPoint                ( rect . width ( ) , rect . height ( )      )
    SP   = self   . mapToScene   ( PM                                        )
    FS   = parent . mapFromScene ( SP                                        )
    MP   = parent . pointToPaper ( FS                                        )
    ##########################################################################
    RR   = QRectF                ( XP . x ( ) , XP . y ( )                 , \
                                   MP . x ( ) , MP . y ( )                   )
    ##########################################################################
    VRIT = VcfFaceRegion         ( self , parent  , self . PlanFunc          )
    VRIT . setOptions            ( self . Options , False                    )
    self . assignItemProperties  ( VRIT                                      )
    VRIT . setMenuCaller         ( self . MenuCallerEmitter                  )
    VRIT . Region      = rect
    VRIT . PictureItem = parent
    VRIT . setRange              ( RR                                        )
    VRIT . PrepareForActions     (                                           )
    ##########################################################################
    VRIT . logFunc = self . addLog
    ##########################################################################
    self . addItem               ( VRIT , parent                             )
    ## self . Scene . addItem       ( VRIT                                      )
    ##########################################################################
    self . emitGeometryChange . emit ( VRIT                                  )
    ##########################################################################
    return
  ############################################################################
  def pixelToItemPaper       ( self , point , item                         ) :
    ##########################################################################
    SP = self . mapToScene   ( point                                         )
    XS = item . mapFromScene ( SP                                            )
    XP = item . pointToPaper ( XS                                            )
    ##########################################################################
    return XP
  ############################################################################
  def pjsonToItemPoint       ( self , JSON , item                          ) :
    ##########################################################################
    PM = QPoint              ( JSON [ "X" ] , JSON [ "Y" ]                   )
    SP = self . mapToScene   ( PM                                            )
    XP = item . mapFromScene ( SP                                            )
    ##########################################################################
    return                   { "X" : XP . x ( ) , "Y" : XP . y ( )           }
  ############################################################################
  def AddBodyRegion                 ( self , parent , rect , points        ) :
    ##########################################################################
    PM   = QPoint                   ( rect . x     ( ) , rect . y      ( )   )
    XP   = self . pixelToItemPaper  ( PM , parent                            )
    ##########################################################################
    PM   = QPoint                   ( rect . width ( ) , rect . height ( )   )
    MP   = self . pixelToItemPaper  ( PM , parent                            )
    ##########################################################################
    RR   = QRectF                   ( XP . x ( ) , XP . y ( )              , \
                                      MP . x ( ) , MP . y ( )                )
    ##########################################################################
    Draw =                          {                                        }
    Draw [ "Nose" ] = self . pjsonToItemPoint ( points [ "Nose" ] , parent   )
    ##########################################################################
    for Side in                     [ "Left" , "Right"                     ] :
      ########################################################################
      Draw [ Side ] =               {                                        }
      KEYs = points [ Side ] . keys (                                        )
      ########################################################################
      for KEY in KEYs                                                        :
        ######################################################################
        JP = points                 [ Side ] [ KEY                           ]
        Draw [ Side ] [ KEY ] = self . pjsonToItemPoint ( JP , parent        )
    ##########################################################################
    KJ   =                          { "Pose"   : True                      , \
                                      "Points" : points                    , \
                                      "Draws"  : Draw                        }
    ##########################################################################
    VRIT = VcfFaceRegion            ( self , parent  , self . PlanFunc       )
    VRIT . setOptions               ( self . Options , False                 )
    self . assignItemProperties     ( VRIT                                   )
    VRIT . setMenuCaller            ( self . MenuCallerEmitter               )
    VRIT . Region      = rect
    VRIT . POSEs       = KJ
    VRIT . PictureItem = parent
    VRIT . setRange                 ( RR                                     )
    ##########################################################################
    VRIT . logFunc = self . addLog
    ##########################################################################
    self . addItem                  ( VRIT , parent                          )
    ## self . Scene . addItem          ( VRIT                                   )
    ##########################################################################
    self . emitGeometryChange . emit ( VRIT                                  )
    ##########################################################################
    return
  ############################################################################
  def AdjustFaceRegion           ( self , item , parent , rect             ) :
    ##########################################################################
    PM   = QPoint                ( rect . x     ( ) , rect . y      ( )      )
    SP   = self   . mapToScene   ( PM                                        )
    XS   = parent . mapFromScene ( SP                                        )
    XP   = parent . pointToPaper ( XS                                        )
    ##########################################################################
    PM   = QPoint                ( rect . width ( ) , rect . height ( )      )
    SP   = self   . mapToScene   ( PM                                        )
    FS   = parent . mapFromScene ( SP                                        )
    MP   = parent . pointToPaper ( FS                                        )
    ##########################################################################
    RR   = QRectF                ( XP . x ( ) , XP . y ( )                 , \
                                   MP . x ( ) , MP . y ( )                   )
    ##########################################################################
    item . Region = rect
    item . setRange              ( RR                                        )
    ##########################################################################
    return
  ############################################################################
  def DoAdjustments            ( self , SIZE                               ) :
    ##########################################################################
    self . setSizeSuggestion   ( SIZE . width ( ) , SIZE . height ( )        )
    self . resize              ( SIZE                                        )
    ##########################################################################
    pw   = self . parentWidget (                                             )
    if                         ( "MdiSubWindow" not in type(pw).__name__   ) :
      return
    ##########################################################################
    self . Adjustment . emit   ( pw , SIZE                                   )
    ##########################################################################
    return
  ############################################################################
  def AddPicture                  ( self , PIC , Z                         ) :
    ##########################################################################
    VRIT = VcfPeoplePicture       ( self , None , self . PlanFunc            )
    VRIT . setOptions             ( self . Options , False                   )
    self . assignItemProperties   ( VRIT                                     )
    VRIT . setMenuCaller          ( self . MenuCallerEmitter                 )
    VRIT . setZValue              ( Z                                        )
    VRIT . PICOP = PIC
    VRIT . Image = PIC . toQImage (                                          )
    VRIT . asImageRect            (                                          )
    ##########################################################################
    VRIT . logFunc = self . addLog
    ##########################################################################
    self . addItem                ( VRIT                                     )
    self . Scene . addItem        ( VRIT                                     )
    ##########################################################################
    return
  ############################################################################
  def assignPicture             ( self , Uuid                              ) :
    ##########################################################################
    self . PerfectView          (                                            )
    ##########################################################################
    VRIT = VcfPeoplePicture     ( self , None , self . PlanFunc              )
    VRIT . setOptions           ( self . Options , False                     )
    self . assignItemProperties ( VRIT                                       )
    VRIT . setMenuCaller        ( self . MenuCallerEmitter                   )
    VRIT . LoadImage            ( Uuid                                       )
    VRIT . asImageRect          (                                            )
    VRIT . PrepareForActions    (                                            )
    ##########################################################################
    VRIT . logFunc = self . addLog
    ##########################################################################
    FS   = VRIT . ImageSize     (                                            )
    ##########################################################################
    self . addItem              ( VRIT                                       )
    self . Scene . addItem      ( VRIT                                       )
    self . setPrepared          ( True                                       )
    self . DoAdjustments        ( FS                                         )
    ##########################################################################
    return
  ############################################################################
  def assignFilename              ( self , FILENAME                        ) :
    ##########################################################################
    PIC  = PictureItem            (                                          )
    OK   = PIC . Load             ( FILENAME                                 )
    ##########################################################################
    if                            ( not OK                                 ) :
      return
    ##########################################################################
    self . PerfectView            (                                          )
    ##########################################################################
    VRIT = VcfPeoplePicture       ( self , None , self . PlanFunc            )
    VRIT . setOptions             ( self . Options , False                   )
    self . assignItemProperties   ( VRIT                                     )
    VRIT . setMenuCaller          ( self . MenuCallerEmitter                 )
    VRIT . setZValue              ( 10000                                    )
    VRIT . PICOP = PIC
    VRIT . Image = PIC . toQImage (                                          )
    VRIT . asImageRect            (                                          )
    VRIT . PrepareForActions      (                                          )
    ##########################################################################
    VRIT . logFunc = self . addLog
    ##########################################################################
    FS   = VRIT . ImageSize       (                                          )
    ##########################################################################
    self . addItem                ( VRIT                                     )
    self . Scene . addItem        ( VRIT                                     )
    self . setPrepared            ( True                                     )
    self . DoAdjustments          ( FS                                       )
    ##########################################################################
    return
##############################################################################
