# -*- coding: utf-8 -*-
##############################################################################
## PeopleDetails
## 人物詳細資訊
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
from   PyQt5                               import QtCore
from   PyQt5                               import QtGui
from   PyQt5                               import QtWidgets
##############################################################################
from   PyQt5 . QtCore                      import QObject
from   PyQt5 . QtCore                      import pyqtSignal
from   PyQt5 . QtCore                      import pyqtSlot
from   PyQt5 . QtCore                      import Qt
from   PyQt5 . QtCore                      import QPoint
from   PyQt5 . QtCore                      import QPointF
from   PyQt5 . QtCore                      import QSize
from   PyQt5 . QtCore                      import QDateTime
##############################################################################
from   PyQt5 . QtGui                       import QIcon
from   PyQt5 . QtGui                       import QCursor
from   PyQt5 . QtGui                       import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets                   import QApplication
from   PyQt5 . QtWidgets                   import QWidget
from   PyQt5 . QtWidgets                   import qApp
from   PyQt5 . QtWidgets                   import QMenu
from   PyQt5 . QtWidgets                   import QAction
from   PyQt5 . QtWidgets                   import QShortcut
from   PyQt5 . QtWidgets                   import QAbstractItemView
from   PyQt5 . QtWidgets                   import QTreeWidget
from   PyQt5 . QtWidgets                   import QTreeWidgetItem
from   PyQt5 . QtWidgets                   import QLineEdit
from   PyQt5 . QtWidgets                   import QComboBox
from   PyQt5 . QtWidgets                   import QSpinBox
##############################################################################
from   AITK  . Qt . MenuManager            import MenuManager    as MenuManager
from   AITK  . Qt . Widget                 import Widget         as Widget
##############################################################################
from   AITK  . Essentials . Relation       import Relation       as Relation
from   AITK  . Calendars  . StarDate       import StarDate       as StarDate
from   AITK  . Calendars  . Periode        import Periode        as Periode
from   AITK  . Documents  . Notes          import Notes          as Notes
from   AITK  . Documents  . Variables      import Variables      as Variables
from   AITK  . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK  . Scheduler  . Project        import Project        as Project
from   AITK  . Scheduler  . Projects       import Projects       as Projects
from   AITK  . Scheduler  . Event          import Event          as Event
from   AITK  . Scheduler  . Events         import Events         as Events
from   AITK  . Scheduler  . Task           import Task           as Task
from   AITK  . Scheduler  . Tasks          import Tasks          as Tasks
##############################################################################
from         . PeopleDetailsUI             import Ui_PeopleDetailsUI
##############################################################################
class PeopleDetails                 ( Widget                               ) :
  ############################################################################
  emitAssignIcon       = pyqtSignal ( QIcon                                  )
  emitBustle           = pyqtSignal (                                        )
  emitVacancy          = pyqtSignal (                                        )
  OnBusy               = pyqtSignal (                                        )
  GoRelax              = pyqtSignal (                                        )
  Leave                = pyqtSignal ( QWidget                                )
  DynamicVariantTables = pyqtSignal ( str , dict                             )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            (        parent        , plan            )
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
  @pyqtSlot                   (                                              )
  def DoBustle                ( self                                       ) :
    self . Bustle             (                                              )
    return
  ############################################################################
  def setBustle               ( self                                       ) :
    self . emitBustle  . emit (                                              )
    return
  ############################################################################
  @pyqtSlot                   (                                              )
  def DoVacancy               ( self                                       ) :
    self . Vacancy            (                                              )
    return
  ############################################################################
  def setVacancy              ( self                                       ) :
    self . emitVacancy . emit (                                              )
    return
  ############################################################################
  @pyqtSlot                      (       QIcon                               )
  def AssignIcon                 ( self , icon                             ) :
    ##########################################################################
    self . ThumbButton . setIcon (        icon                               )
    ##########################################################################
    return
  ############################################################################
  def FetchIcon                       ( self , DB , PUID                   ) :
    ##########################################################################
    if                                ( PUID <= 0                          ) :
      return None
    ##########################################################################
    TUBTAB     = self . Tables        [ "Thumb"                              ]
    WH         = f"where ( `usage` = 'ICON' ) and ( `uuid` = {PUID} )"
    OPTS       = "order by `id` desc limit 0 , 1"
    QQ         = f"select `thumb` from {TUBTAB} {WH} {OPTS} ;"
    DB         . Query                ( QQ                                   )
    THUMB      = DB . FetchOne        (                                      )
    ##########################################################################
    if                                ( THUMB == None                      ) :
      return None
    ##########################################################################
    if                                ( len ( THUMB ) <= 0                 ) :
      return None
    ##########################################################################
    BLOB       = THUMB                [ 0                                    ]
    if                                ( isinstance ( BLOB , bytearray )    ) :
      BLOB = bytes                    ( BLOB                                 )
    ##########################################################################
    if                                ( len ( BLOB ) <= 0                  ) :
      return None
    ##########################################################################
    IMG        = QImage               (                                      )
    IMG        . loadFromData         ( QByteArray ( BLOB ) , "PNG"          )
    TSIZE      = IMG . size           (                                      )
    ##########################################################################
    ISIZE      = self . iconSize      (                                      )
    ICZ        = QImage               ( ISIZE , QImage . Format_ARGB32       )
    ICZ        . fill                 ( QColor ( 255 , 255 , 255 )           )
    ##########################################################################
    W          = int       ( ( ISIZE . width  ( ) - TSIZE . width  ( ) ) / 2 )
    H          = int       ( ( ISIZE . height ( ) - TSIZE . height ( ) ) / 2 )
    PTS        = QPoint               ( W , H                                )
    ##########################################################################
    p          = QPainter             (                                      )
    p          . begin                ( ICZ                                  )
    p          . drawImage            ( PTS , IMG                            )
    p          . end                  (                                      )
    ##########################################################################
    PIX        = QPixmap              (                                      )
    PIX        . convertFromImage     ( ICZ                                  )
    ##########################################################################
    return QIcon                      ( PIX                                  )
  ############################################################################
  def LoadPeopleIcon             ( self , DB , PUID                        ) :
    ##########################################################################
    RELTAB = self . Tables       [ "Relation"                                ]
    ##########################################################################
    REL    = Relation            (                                           )
    REL    . set                 ( "first" , PUID                            )
    REL    . setT1               ( "People"                                  )
    REL    . setT2               ( "Picture"                                 )
    REL    . setRelation         ( "Using"                                   )
    ##########################################################################
    PICS   = REL . Subordination ( DB      , RELTAB                          )
    ##########################################################################
    if                           ( len ( PICS ) <= 0                       ) :
      return
    ##########################################################################
    PUID   = PICS                [ 0                                         ]
    ICON   = self . FetchIcon    ( DB , PUID                                 )
    ##########################################################################
    if                           ( self . NotOkay ( ICON )                 ) :
      return
    ##########################################################################
    self   . emitAssignIcon      ( ICON                                      )
    ##########################################################################
    return
  ############################################################################
  def ReloadPeopleInformation         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
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
    print("ReloadPeopleInformation")
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    return
  ############################################################################
  def PeopleUuidChanged  ( self                                            ) :
    ##########################################################################
    PUID   = self . ui . PeopleUuid . text (                                 )
    try                                                                      :
      PUID = int         ( PUID                                              )
    except                                                                   :
      return
    ##########################################################################
    self   . PeopleUuid = PUID
    ##########################################################################
    JSON =               { "Action" : "People"                             , \
                           "People" : self . PeopleUuid                      }
    self . EmitCallbacks ( JSON                                              )
    ##########################################################################
    self   . Go          ( self . ReloadPeopleInformation                    )
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
    JSON  =                             { "Callback" : self . TablesUpdated  ,
                                          "Tables"   : self . Tables         }
    self  . DynamicVariantTables . emit ( str ( TITLE ) , JSON               )
    ##########################################################################
    return
  ############################################################################
  def startup                             ( self                           ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################
