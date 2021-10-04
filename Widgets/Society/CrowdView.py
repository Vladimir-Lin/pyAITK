# -*- coding: utf-8 -*-
##############################################################################
## PeopleView
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
from   PyQt5 . QtCore                 import QSize
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
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QListWidget
from   PyQt5 . QtWidgets              import QListWidgetItem
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from   AITK  . Qt . IconDock          import IconDock as IconDock
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager   as MenuManager
##############################################################################
from   AITK  . Essentials . Relation  import Relation
##############################################################################
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
class CrowdView               ( IconDock                                   ) :
  ############################################################################
  CrowdSubgroup = pyqtSignal  ( int , str                                    )
  PeopleGroup   = pyqtSignal  ( str                                          )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super ( ) . __init__      (        parent        , plan                  )
    ##########################################################################
    self . Relation = Relation    (                                          )
    self . Relation . setRelation ( "Subordination"                          )
    ##########################################################################
    self . Grouping = "Tag"
    ## self . Grouping = "Catalog"
    ## self . Grouping = "Subgroup"
    ##########################################################################
    return
  ############################################################################
  def sizeHint                ( self                                       ) :
    return QSize              ( 800 , 800                                    )
  ############################################################################
  def setGrouping             ( self , group                               ) :
    self . Grouping = group
    return self . Grouping
  ############################################################################
  def getGrouping             ( self                                       ) :
    return self . Grouping
  ############################################################################
  def GetUuidIcon                ( self , DB , Uuid                        ) :
    ##########################################################################
    """
    RELTAB = self . Tables       [ "Relation"                                ]
    REL    = Relation            (                                           )
    REL    . set                 ( "first" , Uuid                            )
    REL    . setT1               ( "People"                                  )
    REL    . setT2               ( "Picture"                                 )
    REL    . setRelation         ( "Using"                                   )
    ##########################################################################
    PICS   = REL . Subordination ( DB , RELTAB                               )
    ##########################################################################
    if                           ( len ( PICS ) > 0                        ) :
      return PICS                [ 0                                         ]
    """
    ##########################################################################
    return 0
  ############################################################################
  def ObtainUuidsQuery         ( self                                      ) :
    ##########################################################################
    TABLE = self . Tables      [ "Tags"                                      ]
    QQ    = f"select `uuid` from {TABLE} where ( `used` = 1 ) and ( `type` = 7 ) order by `id` asc ;"
    ##########################################################################
    return QQ
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    OPTS   = "order by `position` desc"
    RELTAB = self . Tables [ "Relation" ]
    ##########################################################################
    return self . Relation . Subordination ( DB , RELTAB , OPTS              )
  ############################################################################
  def ObtainsItemUuids                ( self , DB                          ) :
    ##########################################################################
    if                                ( self . Grouping == "Tag"           ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( "ContiguousSelection"                       )
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def InsertItem                   ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def DeleteItems                  ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    items  = self . selectedItems  (                                         )
    atItem = self . itemAt         ( pos                                     )
    uuid   = 0
    ##########################################################################
    if                             ( atItem != None                        ) :
      uuid = atItem . data         ( Qt . UserRole                           )
      uuid = int                   ( uuid                                    )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                             ( uuid > 0                              ) :
      mm   . addAction             ( 2001 ,  "子群組" )
      if                           ( self . Grouping == "Subgroup"         ) :
        mm . addAction             ( 2002 ,  "群組成員" )
      mm   . addSeparator          (                                         )
    mm     . addAction             ( 1001 ,  TRX [ "UI::Refresh"  ]          )
    mm     . addAction             ( 1101 ,  TRX [ "UI::Insert"   ]          )
    mm     . addSeparator          (                                         )
    if                             ( atItem != None                        ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    mm     = self . LocalityMenu   ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
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
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Projects" , uuid , NAM          )
      return True
    ##########################################################################
    if                             ( at == 2001                            ) :
      tid  = self . Relation . get ( "t2"                                    )
      self . CrowdSubgroup . emit  ( tid , str ( uuid )                      )
      return True
    ##########################################################################
    if                             ( at == 2002                            ) :
      self . PeopleGroup   . emit  ( str ( uuid )                            )
      return True
    ##########################################################################
    return True
##############################################################################
