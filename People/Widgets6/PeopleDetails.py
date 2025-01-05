# -*- coding: utf-8 -*-
##############################################################################
## PeopleDetails
## 人物詳細資訊
##############################################################################
import os
import sys
import time
import requests
import threading
import json
##############################################################################
from   PySide6                               import QtCore
from   PySide6                               import QtGui
from   PySide6                               import QtWidgets
from   PySide6 . QtCore                      import *
from   PySide6 . QtGui                       import *
from   PySide6 . QtWidgets                   import *
from   AITK    . Qt6                         import *
##############################################################################
from   AITK    . Essentials . Relation       import Relation       as Relation
from   AITK    . Calendars  . StarDate       import StarDate       as StarDate
from   AITK    . Calendars  . Periode        import Periode        as Periode
from   AITK    . Documents  . Notes          import Notes          as Notes
from   AITK    . Documents  . Variables      import Variables      as Variables
from   AITK    . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK    . Pictures   . Picture6       import Picture        as PictureItem
from   AITK    . Pictures   . Gallery        import Gallery        as GalleryItem
##############################################################################
from   AITK    . Scheduler  . Project        import Project        as Project
from   AITK    . Scheduler  . Projects       import Projects       as Projects
from   AITK    . Scheduler  . Event          import Event          as Event
from   AITK    . Scheduler  . Events         import Events         as Events
from   AITK    . Scheduler  . Task           import Task           as Task
from   AITK    . Scheduler  . Tasks          import Tasks          as Tasks
##############################################################################
from           . PeopleDetailsUI             import Ui_PeopleDetailsUI
##############################################################################
class PeopleDetails             ( Widget                                   ) :
  ############################################################################
  emitAssignIcon       = Signal ( QIcon                                      )
  emitBustle           = Signal (                                            )
  emitVacancy          = Signal (                                            )
  OnBusy               = Signal (                                            )
  GoRelax              = Signal (                                            )
  Leave                = Signal ( QWidget                                    )
  DynamicVariantTables = Signal ( str , dict                                 )
  OpenFaceModel        = Signal ( dict                                       )
  ############################################################################
  def __init__                  ( self , parent = None , plan = None       ) :
    ##########################################################################
    super ( ) . __init__        (        parent        , plan                )
    ##########################################################################
    self . ui = Ui_PeopleDetailsUI  (                                        )
    self . ui . setupUi             ( self                                   )
    ##########################################################################
    self . PeopleUuid = 0
    self . Callbacks  =             [                                        ]
    ##########################################################################
    self . emitAssignIcon . connect ( self . AssignIcon                      )
    self . emitBustle     . connect ( self . DoBustle                        )
    self . emitVacancy    . connect ( self . DoVacancy                       )
    self . OnBusy         . connect ( self . AtBusy                          )
    self . GoRelax        . connect ( self . OnRelax                         )
    ##########################################################################
    return
  ############################################################################
  def EmitCallbacks ( self , JSON                                          ) :
    ##########################################################################
    for Callback in self . Callbacks                                         :
      Callback      (        JSON                                            )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    if                     ( len ( self . Callbacks ) > 0                  ) :
      ########################################################################
      JSON =               { "Action" : "Detach" , "Widget" : self           }
      self . EmitCallbacks ( JSON                                            )
    ##########################################################################
    if                     ( self . Shutdown ( )                           ) :
      event . accept       (                                                 )
      return
    ##########################################################################
    super ( ) . closeEvent (        event                                    )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , event                                 ) :
    ##########################################################################
    if                      ( self . Relocation ( )                        ) :
      event . accept        (                                                )
      return
    ##########################################################################
    super ( ) . resizeEvent ( event                                          )
    ##########################################################################
    return
  ############################################################################
  def showEvent           ( self , event                                   ) :
    ##########################################################################
    super ( ) . showEvent ( event                                            )
    self . Relocation     (                                                  )
    ##########################################################################
    return
  ############################################################################
  def Shutdown                ( self                                       ) :
    self . Leave . emit       ( self                                         )
    return True
  ############################################################################
  def Relocation                            ( self                         ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachExternalFunction    ( self , FUNC                              ) :
    ##########################################################################
    if                          ( FUNC not in self . Callbacks             ) :
      self . Callbacks . append (        FUNC                                )
    ##########################################################################
    return
  ############################################################################
  def DoBustle                ( self                                       ) :
    self . Bustle             (                                              )
    return
  ############################################################################
  def setBustle               ( self                                       ) :
    self . emitBustle  . emit (                                              )
    return
  ############################################################################
  def DoVacancy               ( self                                       ) :
    self . Vacancy            (                                              )
    return
  ############################################################################
  def setVacancy              ( self                                       ) :
    self . emitVacancy . emit (                                              )
    return
  ############################################################################
  def AtBusy           ( self                                              ) :
    ##########################################################################
    self . doStartBusy (                                                     )
    ##########################################################################
    return
  ############################################################################
  def OnRelax          ( self                                              ) :
    ##########################################################################
    self . doStopBusy  (                                                     )
    ##########################################################################
    return
  ############################################################################
  def AssignIcon                      ( self , icon                        ) :
    ##########################################################################
    self . ui . ThumbButton . setIcon (        icon                          )
    ##########################################################################
    return
  ############################################################################
  def FetchIcon                ( self , DB , PUID                          ) :
    ##########################################################################
    if                         ( PUID <= 0                                 ) :
      return None
    ##########################################################################
    TUBTAB = self . Tables     [ "Thumb"                                     ]
    ISIZE  = QSize             ( 128 , 128                                   )
    ##########################################################################
    return self   . FetchQIcon ( DB , TUBTAB , PUID , ISIZE                  )
  ############################################################################
  def LoadPeopleIcon               ( self , DB , PUID                      ) :
    ##########################################################################
    RELTAB = self . Tables         [ "Relation"                              ]
    ##########################################################################
    GALM   = GalleryItem           (                                         )
    PICS   = GALM . GetIcons       ( DB , RELTAB , PUID , "People"           )
    ##########################################################################
    if                             ( len ( PICS ) <= 0                     ) :
      return
    ##########################################################################
    PUID   = PICS                  [ 0                                       ]
    ICON   = self . FetchIcon      ( DB , PUID                               )
    ##########################################################################
    if                             ( self . NotOkay ( ICON )               ) :
      return
    ##########################################################################
    self   . emitAssignIcon . emit ( ICON                                    )
    ##########################################################################
    return
  ############################################################################
  def ReloadPeopleInformation         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        ( UsePure = True                       )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    self    . LoadPeopleIcon          ( DB , self . PeopleUuid               )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    return
  ############################################################################
  def PeopleUuidChanged    ( self                                          ) :
    ##########################################################################
    PUID   = self . ui . PeopleUuid . text (                                 )
    try                                                                      :
      PUID = int           ( PUID                                            )
    except                                                                   :
      return
    ##########################################################################
    self   . PeopleUuid = PUID
    ##########################################################################
    JSON   =               { "Action" : "People"                           , \
                             "People" : self . PeopleUuid                    }
    self   . EmitCallbacks ( JSON                                            )
    ##########################################################################
    self   . Go            ( self . ReloadPeopleInformation                  )
    ##########################################################################
    return
  ############################################################################
  def TablesUpdated ( self , JSON                                          ) :
    ##########################################################################
    self . Tables = JSON
    ##########################################################################
    return
  ############################################################################
  def TablesEditing                     ( self                             ) :
    ##########################################################################
    TITLE = self . windowTitle          (                                    )
    TITLE = str                         ( TITLE                              )
    JSON  =                             { "Callback" : self . TablesUpdated  ,
                                          "Tables"   : self . Tables         }
    self  . DynamicVariantTables . emit ( TITLE , JSON                       )
    ##########################################################################
    return
  ############################################################################
  def FaceModel                 ( self                                     ) :
    ##########################################################################
    TITLE = self . windowTitle  (                                            )
    UUID  = int                 ( self . PeopleUuid                          )
    JSON  =                     { "Title"    : TITLE                         ,
                                  "People"   : UUID                          ,
                                  "Callback" : self . FaceCallback           ,
                                  "Plugins"  : self . Callbacks              }
    self . OpenFaceModel . emit ( JSON                                       )
    ##########################################################################
    return
  ############################################################################
  def FaceCallback ( self , JSON                                           ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def ExecuteSelected ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def startup                             ( self                           ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################
