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
from   AITK  . Qt . IconDock          import IconDock    as IconDock
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation
##############################################################################
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
class PeopleView                   ( IconDock                              ) :
  ############################################################################
  ShowPersonalGallery = pyqtSignal ( int , str                               )
  ShowGalleries       = pyqtSignal ( int , str                               )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . Total    = 0
    self . StartId  = 0
    self . Amount   = 65
    ##########################################################################
    self . Grouping = "Original"
    ## self . Grouping = "Subordination"
    ## self . Grouping = "Reverse"
    ##########################################################################
    self . GroupOrder = "asc"
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "People"                                )
    self . Relation . setRelation  ( "Subordination"                         )
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
  def setGroupOrder           ( self , order                               ) :
    self . GroupOrder = order
    return self . GroupOrder
  ############################################################################
  def getGroupOrder           ( self                                       ) :
    return self . GroupOrder
  ############################################################################
  def GetUuidIcon                ( self , DB , Uuid                        ) :
    ##########################################################################
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
    ##########################################################################
    return 0
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "People"                                    ]
    QQ     = f"select count(*) from {TABLE} where ( `used` = 1 ) ;"
    DB     . Query             ( QQ                                          )
    ONE    = DB . FetchOne     (                                             )
    ##########################################################################
    if                         ( ONE == None                               ) :
      return 0
    ##########################################################################
    if                         ( len ( ONE ) <= 0                          ) :
      return 0
    ##########################################################################
    return ONE                 [ 0                                           ]
  ############################################################################
  def FetchGroupMembersCount             ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountSecond ( DB , RELTAB                       )
  ############################################################################
  def FetchGroupOwnersCount              ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountFirst  ( DB , RELTAB                       )
  ############################################################################
  def ObtainUuidsQuery         ( self                                      ) :
    ##########################################################################
    TABLE  = self . Tables      [ "People"                                    ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getGroupOrder ( )
    QQ     = f"select `uuid` from {TABLE} where ( `used` = 1 ) order by `id` {ORDER} limit {SID} , {AMOUNT} ;"
    ##########################################################################
    return QQ
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getGroupOrder ( )
    LMTS   = f"limit {SID} , {AMOUNT}"
    RELTAB = self . Tables [ "Relation" ]
    ##########################################################################
    if                         ( self . Grouping == "Subordination"        ) :
      OPTS = f"order by `position` {ORDER}"
      return self . Relation . Subordination ( DB , RELTAB , OPTS , LMTS     )
    if                         ( self . Grouping == "Reverse"              ) :
      OPTS = f"order by `reverse` {ORDER} , `position` {ORDER}"
      return self . Relation . GetOwners     ( DB , RELTAB , OPTS , LMTS     )
    ##########################################################################
    return                     [                                             ]
  ############################################################################
  def ObtainsItemUuids                ( self , DB                          ) :
    ##########################################################################
    if                                ( self . Grouping == "Original"      ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def FetchSessionInformation         ( self , DB                          ) :
    ##########################################################################
    if                                ( self . Grouping == "Original"      ) :
      ########################################################################
      self . Total = self . FetchRegularDepotCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . Grouping == "Subordination" ) :
      ########################################################################
      self . Total = self . FetchGroupMembersCount ( DB                      )
      ########################################################################
      return
    ##########################################################################
    if                                ( self . Grouping == "Reverse"       ) :
      ########################################################################
      self . Total = self . FetchGroupOwnersCount  ( DB                      )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def FocusIn                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return False
    ##########################################################################
    self . setActionLabel        ( "Label"      , self . windowTitle ( )     )
    self . LinkAction            ( "Refresh"    , self . startup             )
    ##########################################################################
    self . LinkAction            ( "Insert"     , self . InsertItem          )
    self . LinkAction            ( "Delete"     , self . DeleteItems         )
    self . LinkAction            ( "Home"       , self . PageHome            )
    self . LinkAction            ( "End"        , self . PageEnd             )
    self . LinkAction            ( "PageUp"     , self . PageUp              )
    self . LinkAction            ( "PageDown"   , self . PageDown            )
    ##########################################################################
    self . LinkAction            ( "SelectAll"  , self . SelectAll           )
    self . LinkAction            ( "SelectNone" , self . SelectNone          )
    ##########################################################################
    self . LinkAction            ( "Rename"     , self . RenamePeople        )
    ##########################################################################
    return True
  ############################################################################
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( "ContiguousSelection"                       )
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def PageHome                     ( self                                  ) :
    ##########################################################################
    self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageEnd                      ( self                                  ) :
    ##########################################################################
    self . StartId    = self . Total - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageUp                       ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageDown                     ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId + self . Amount
    if                             ( self . StartId > self . Total         ) :
      self . StartId  = self . Total
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def RenamePeople                 ( self                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot(int)
  def GotoId                       ( self , Id                             ) :
    ##########################################################################
    self . StartId    = Id
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot(int)
  def AssignAmount                 ( self , Amount                         ) :
    ##########################################################################
    self . Amount    = Amount
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
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
    T      = self . Total
    MSG    = f"總人數:{T}"
    mm     . addAction             ( 9999991 , MSG                           )
    ##########################################################################
    SIDB   = SpinBox               ( None , self . PlanFunc                  )
    SIDB   . setRange              ( 0 , self . Total                        )
    SIDB   . setValue              ( self . StartId                          )
    mm     . addWidget             ( 9999992 , SIDB                          )
    SIDB   . valueChanged . connect ( self . GotoId                          )
    ##########################################################################
    SIDP   = SpinBox               ( None , self . PlanFunc                  )
    SIDP   . setRange              ( 0 , self . Total                        )
    SIDP   . setValue              ( self . Amount                           )
    mm     . addWidget             ( 9999993 , SIDP                          )
    SIDP   . valueChanged . connect ( self . AssignAmount                    )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     . addAction             ( 1001 ,  TRX [ "UI::Refresh"  ]          )
    mm     . addAction             ( 1101 ,  TRX [ "UI::Insert"   ]          )
    if                             ( uuid > 0                              ) :
      mm   . addSeparator          (                                         )
      mm   . addAction             ( 1201 ,  TRX [ "UI::PersonalGallery"   ] )
      mm   . addAction             ( 1202 ,  TRX [ "UI::Galleries"         ] )
    ##########################################################################
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
    if                             ( at == 1201                            ) :
      self . ShowPersonalGallery . emit ( 7 , str ( uuid )                   )
      return True
    ##########################################################################
    if                             ( at == 1202                            ) :
      self . ShowGalleries       . emit ( 7 ,str ( uuid )                    )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Projects" , uuid , NAM          )
      return True
    ##########################################################################
    return True
##############################################################################