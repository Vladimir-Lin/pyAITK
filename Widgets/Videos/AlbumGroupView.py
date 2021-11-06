# -*- coding: utf-8 -*-
##############################################################################
## AlbumGroupView
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
class AlbumGroupView              ( IconDock                               ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  AlbumSubgroup = pyqtSignal      ( str , int , str                          )
  AlbumGroup    = pyqtSignal      ( str , int , str                          )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          (        parent        , plan              )
    ##########################################################################
    self . dockingPlace = Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation    (                                          )
    self . Relation . setRelation ( "Subordination"                          )
    ##########################################################################
    self . Grouping = "Tag"
    ## self . Grouping = "Catalog"
    ## self . Grouping = "Subgroup"
    ## self . Grouping = "Reverse"
    ##########################################################################
    self . setFunction            ( self . HavingMenu      , True            )
    ##########################################################################
    ## self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
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
  def isGrouping              ( self , tag                                 ) :
    return                    ( self . Grouping == tag                       )
  ############################################################################
  def FocusIn                 ( self                                       ) :
    ##########################################################################
    if                        ( not self . isPrepared ( )                  ) :
      return False
    ##########################################################################
    self . setActionLabel     ( "Label"      , self . windowTitle ( )        )
    self . LinkAction         ( "Refresh"    , self . startup                )
    ##########################################################################
    self . LinkAction         ( "Insert"     , self . InsertItem             )
    self . LinkAction         ( "Delete"     , self . DeleteItems            )
    self . LinkAction         ( "Paste"      , self . PasteItems             )
    self . LinkAction         ( "Copy"       , self . CopyToClipboard        )
    ##########################################################################
    self . LinkAction         ( "SelectAll"  , self . SelectAll              )
    self . LinkAction         ( "SelectNone" , self . SelectNone             )
    ##########################################################################
    self . LinkAction         ( "Rename"     , self . RenameItem             )
    ##########################################################################
    self . LinkVoice          ( self . CommandParser                         )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                ( self                                       ) :
    ##########################################################################
    if                        ( not self . isPrepared ( )                  ) :
      return True
    ##########################################################################
    return False
  ############################################################################
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
    QQ    = f"select `uuid` from {TABLE} where ( `used` = 1 ) and ( `type` = 76 ) order by `id` asc ;"
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
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "tag/uuids"
    message = "選擇了{0}個分類"
    ##########################################################################
    return self . CreateDragMime ( self , mtype , message                    )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    ##########################################################################
    if                        ( self . isGrouping ( "Tag"      )           ) :
      ########################################################################
      formats = "tag/uuids"
      ########################################################################
    elif                      ( self . isGrouping ( "Catalog"  )           ) :
      ########################################################################
      formats = "tag/uuids;people/uuids"
      ########################################################################
    elif                      ( self . isGrouping ( "Subgroup" )           ) :
      ########################################################################
      formats = "tag/uuids;people/uuids"
    ##########################################################################
    if                        ( len ( formats ) <= 0                       ) :
      return False
    ##########################################################################
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
    elif                            ( mtype in [ "tag/uuids" ]             ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      MSG   = f"從「{title}」複製{CNT}個分類"
      ########################################################################
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
    print("CrowdView::dropPeople")
    print(JSOX)
    if ( atItem is not None ) :
      print("TO:",atItem.text())
    ##########################################################################
    return True
  ############################################################################
  def acceptTagDrop            ( self                                      ) :
    return True
  ############################################################################
  def dropTags                 ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("CrowdView::dropTags")
    print(JSOX)
    if ( atItem is not None ) :
      print("TO:",atItem.text())
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
  @pyqtSlot                        (                                         )
  def InsertItem                   ( self                                  ) :
    ##########################################################################
    print("InsertItem")
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                        (                                         )
  def DeleteItems                  ( self                                  ) :
    ##########################################################################
    print("InsertItem")
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                        (                                         )
  def PasteItems                   ( self                                  ) :
    ##########################################################################
    print("PasteItems")
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                        (                                         )
  def RenameItem                   ( self                                  ) :
    ##########################################################################
    print("InsertItem")
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                        (                                         )
  def CopyToClipboard              ( self                                  ) :
    ##########################################################################
    print("InsertItem")
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage           ( self                                 ) :
    ##########################################################################
    print("InsertItem")
    ##########################################################################
    return True
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    items  = self . selectedItems   (                                        )
    atItem = self . itemAt          ( pos                                    )
    uuid   = 0
    ##########################################################################
    if                              ( atItem != None                       ) :
      uuid = atItem . data          ( Qt . UserRole                          )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                              ( uuid > 0                             ) :
      mm   . addAction              ( 2001 ,  "子群組" )
      if                            ( self . Grouping == "Subgroup"        ) :
        mm . addAction              ( 2002 ,  "影片群組" )
      mm   . addSeparator           (                                        )
    mm     . addAction              ( 1001 ,  TRX [ "UI::Refresh"  ]         )
    mm     . addAction              ( 1101 ,  TRX [ "UI::Insert"   ]         )
    mm     . addSeparator           (                                        )
    if                              ( atItem != None                       ) :
      if                            ( self . EditAllNames != None          ) :
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
        mm . addSeparator           (                                        )
    ##########################################################################
    mm     = self . LocalityMenu    ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . font ( )                     )
    aa     = mm . exec_             ( QCursor . pos  ( )                     )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      self . startup                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      self . InsertItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      NAM  = self . Tables          [ "Names"                                ]
      self . EditAllNames           ( self , "Albums" , uuid , NAM           )
      return True
    ##########################################################################
    if                              ( at == 2001                           ) :
      title = atItem . text         (                                        )
      tid   = self . Relation . get ( "t2"                                   )
      self  . AlbumSubgroup . emit  ( title , tid , str ( uuid )             )
      return True
    ##########################################################################
    if                              ( at == 2002                           ) :
      title = atItem . text         (                                        )
      tid   = self . Relation . get ( "t2"                                   )
      self  . AlbumGroup    . emit  ( title , tid , str ( uuid )             )
      return True
    ##########################################################################
    return True
  ############################################################################
  def CommandParser ( self , language , message , timestamp                ) :
    ##########################################################################
    print("CommandParser:",language , message , timestamp)
    ##########################################################################
    return          { "Match" : False                                        }
##############################################################################
