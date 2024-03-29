# -*- coding: utf-8 -*-
##############################################################################
## FaceShapeListings
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
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
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
class FaceShapeListings  ( MajorListings                                   ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
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
    return
  ############################################################################
  def ObtainUuidsQuery                ( self                               ) :
    ##########################################################################
    TABLE   = self . Tables           [ "FaceShapes"                         ]
    ##########################################################################
    QQ      = f"select `uuid` from {TABLE} order by `id` asc ;"
    ##########################################################################
    return QQ
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    LABELs = [ "臉型" ]
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
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    items  = self . selectedItems  (                                         )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    mm     . addSeparator          (                                         )
    if                             ( len ( items ) == 1                    ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    mm     = self . LocalityMenu   ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( items [ 0 ] , 0                         )
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Tasks" , uuid , NAM             )
      return True
    ##########################################################################
    return True
##############################################################################
