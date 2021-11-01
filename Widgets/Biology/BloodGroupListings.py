# -*- coding: utf-8 -*-
##############################################################################
## BloodGroupListings
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
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import pyqtSlot
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
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager   as MenuManager
from   AITK  . Qt . MajorListings     import MajorListings as MajorListings
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
##############################################################################
class BloodGroupListings   ( MajorListings                                 ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  def __init__             ( self , parent = None , plan = None            ) :
    ##########################################################################
    super ( ) . __init__   (        parent        , plan                     )
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setFunction     ( self . FunctionDocking , True                   )
    self . setFunction     ( self . HavingMenu      , True                   )
    ##########################################################################
    self . setDragEnabled  ( False                                           )
    self . setDragDropMode ( QAbstractItemView . DropOnly                    )
    ## self . setDragDropMode ( QAbstractItemView . DragDrop                    )
    ##########################################################################
    return
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
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery                ( self                               ) :
    ##########################################################################
    TABLE   = self . Tables           [ "BloodGroups"                        ]
    ##########################################################################
    QQ      = f"select `uuid` from {TABLE} order by `id` asc ;"
    ##########################################################################
    return QQ
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "people/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                       ( self                                 , \
                                      sourceWidget                         , \
                                      mimeData                             , \
                                      mousePos                             ) :
    ##########################################################################
    if                              ( self == sourceWidget                 ) :
      return False
    ##########################################################################
    RDN     = self . RegularDropNew ( mimeData                               )
    if                              ( not RDN                              ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON     [ "Mime"                                 ]
    UUIDs   = self . DropInJSON     [ "UUIDs"                                ]
    ##########################################################################
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      title = sourceWidget . windowTitle ( )
      CNT   = len                   ( UUIDs                                  )
      MSG   = f"從「{title}」複製{CNT}個人物"
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    if                         ( sourceWidget != self                      ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    if                         ( atItem is None                            ) :
      return False
    if                         ( atItem . isSelected ( )                   ) :
      return False
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople               ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("SexualityListings::dropPeople")
    print(JSOX)
    if ( atItem is not None ) :
      UUID = atItem . data ( 0 , Qt . UserRole )
      print("TO : " , UUID , " => " , atItem . text ( 0 ) )
    ##########################################################################
    return True
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    LABELs = [ "血型分類" ]
    self   . setCentralLabels ( LABELs                                       )
    ##########################################################################
    self   . setPrepared      ( True                                         )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , name             ) :
    ##########################################################################
    """
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TSKTAB  = self . Tables        [ "Tasks"                                 ]
    PRDTAB  = self . Tables        [ "Periods"                               ]
    NAMTAB  = self . Tables        [ "Names"                                 ]
    HEAD    = 5702000000000000000
    ##########################################################################
    DB      . LockWrites           ( [ PRJTAB , PRDTAB , NAMTAB ]            )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      ########################################################################
      uuid  = DB . LastUuid        ( PRJTAB , "uuid" , HEAD                  )
      DB    . AddUuid              ( PRJTAB , uuid   , 1                     )
      ########################################################################
      NOW   = StarDate             (                                         )
      NOW   . Now                  (                                         )
      CDT   = NOW . Stardate
      ########################################################################
      PRD   = Periode              (                                         )
      PRID  = PRD  . GetUuid       ( DB , PRDTAB                             )
      ########################################################################
      PRD   . Realm    = uuid
      PRD   . Role     = 71
      PRD   . Item     = 1
      PRD   . States   = 0
      PRD   . Creation = CDT
      PRD   . Modified = CDT
      Items =                      [ "realm"                               , \
                                     "role"                                , \
                                     "item"                                , \
                                     "states"                              , \
                                     "creation"                            , \
                                     "modified"                              ]
      PRD   . UpdateItems          ( DB , PRDTAB , Items                     )
    ##########################################################################
    self    . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    item    . setData              ( 0 , Qt . UserRole , uuid                )
    """
    ##########################################################################
    return
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    items  = self . selectedItems  (                                         )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     . addAction             ( 1001 ,  TRX [ "UI::Refresh"  ]          )
    mm     . addAction             ( 1101 ,  TRX [ "UI::Insert"   ]          )
    mm     . addSeparator          (                                         )
    if                             ( len ( items ) == 1                    ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    mm     = self . LocalityMenu   ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( items [ 0 ] , 0                         )
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Sexuality" , uuid , NAM         )
      return True
    ##########################################################################
    return True
##############################################################################
