# -*- coding: utf-8 -*-
##############################################################################
## PicturesView
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
class PicturesView                ( IconDock                               ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  ShowPicture = pyqtSignal        ( str                                      )
  ############################################################################
  def __init__                    ( self , parent = None , plan = None     ) :
    ##########################################################################
    super ( ) . __init__          (        parent        , plan              )
    ##########################################################################
    self . Total     = 0
    self . StartId   = 0
    self . Amount    = 60
    self . UsingName = False
    ##########################################################################
    self . Grouping = "Original"
    ## self . Grouping = "Subordination"
    ## self . Grouping = "Reverse"
    ##########################################################################
    self . Naming   = ""
    ## self . Naming   = "Size"
    ## self . Naming   = "Name"
    ## self . Naming   = "Uuid"
    ##########################################################################
    self . GroupOrder = "asc"
    ##########################################################################
    self . Relation = Relation    (                                          )
    self . Relation . setT2       ( "Picture"                                )
    self . Relation . setRelation ( "Subordination"                          )
    ##########################################################################
    self . setFunction            ( self . HavingMenu      , True            )
    ##########################################################################
    self . setDragEnabled         ( True                                     )
    ## self . setDragDropMode        ( QAbstractItemView . DropOnly             )
    self . setDragDropMode        ( QAbstractItemView . DragDrop             )
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
    return Uuid
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "Pictures"                                  ]
    QQ     = f"select count(*) from {TABLE} ;"
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
  def ObtainUuidsQuery          ( self                                     ) :
    ##########################################################################
    TABLE  = self . Tables      [ "Pictures"                                 ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getGroupOrder ( )
    QQ     = f"select `uuid` from {TABLE} order by `id` {ORDER} limit {SID} , {AMOUNT} ;"
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
    self . setActionLabel        ( "Label"    , self . windowTitle ( )       )
    self . LinkAction            ( "Home"     , self . PageHome              )
    self . LinkAction            ( "End"      , self . PageEnd               )
    self . LinkAction            ( "PageUp"   , self . PageUp                )
    self . LinkAction            ( "PageDown" , self . PageDown              )
    self . LinkAction            ( "Refresh"  , self . startup               )
    ##########################################################################
    return True
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "picture/uuids"
    message = "選擇了{0}張圖片"
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
    formats = "picture/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                       ( self                                 , \
                                      sourceWidget                         , \
                                      mimeData                             , \
                                      mousePos                             ) :
    ##########################################################################
    RDN     = self . RegularDropNew ( mimeData                               )
    if                              ( not RDN                              ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON     [ "Mime"                                 ]
    UUIDs   = self . DropInJSON     [ "UUIDs"                                ]
    ##########################################################################
    if                              ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        MSG = f"移動{CNT}張圖片"
      else                                                                   :
        MSG = f"從「{title}」複製{CNT}張圖片"
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
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures             ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("PictureView::dropPictures")
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
  def ObtainPictureSizes       ( self , DB , UUIDs                         ) :
    ##########################################################################
    TABLE = self . Tables      [ "Information"                               ]
    NAMEs =                    {                                             }
    ##########################################################################
    for UUID in UUIDs                                                        :
      QQ  = f"select `width`,`height` from {TABLE} where ( `uuid` = {UUID} ) ;"
      DB  . Query              ( QQ                                          )
      RR  = DB . FetchOne      (                                             )
      if                       ( ( RR != None ) and ( len ( RR ) > 0 )     ) :
        WW             = RR    [ 0                                           ]
        HH             = RR    [ 1                                           ]
        NAMEs [ UUID ] = f"{WW} x {HH}"
      else                                                                   :
        NAMEs [ UUID ] = ""
    ##########################################################################
    return NAMEs
  ############################################################################
  def ObtainsUuidNames                 ( self , DB , UUIDs                 ) :
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 0                ) :
      return                           {                                     }
    ##########################################################################
    if                                 ( self . Naming == "Uuid"           ) :
      NAMEs =                          {                                     }
      for UUID in UUIDs                                                      :
        NAMEs [ UUID ] = str           ( UUID                                )
      return NAMEs
    ##########################################################################
    if                                 ( self . Naming == "Name"           ) :
      TABLE = self . Tables            [ "Names"                             ]
      NAMEs = self . GetNames          ( DB , TABLE , UUIDs                  )
      return NAMEs
    ##########################################################################
    if                                 ( self . Naming == "Size"           ) :
      return self . ObtainPictureSizes ( DB , UUIDs                          )
    ##########################################################################
    return                            {                                      }
  ############################################################################
  def AssignAsIcon                 ( self , UUID                           ) :
    ##########################################################################
    print ("AssignAsIcon : " , UUID )
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
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
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
    mm     = self . AmountIndexMenu ( mm                                     )
    ##########################################################################
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     . addAction             ( 1301 ,  "不顯示訊息" )
    mm     . addAction             ( 1302 ,  "顯示圖片大小" )
    mm     . addAction             ( 1303 ,  "顯示圖片名稱" )
    mm     . addAction             ( 1304 ,  "顯示圖片編號" )
    ##########################################################################
    if                             ( uuid > 0                              ) :
      mm   . addSeparator          (                                         )
      mm   . addAction             ( 1101 ,  "觀看圖片" )
      mm   . addAction             ( 1102 ,  "指派為群組代表圖示" )
    ##########################################################################
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunAmountIndexMenu ( )         ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . ShowPicture . emit    ( str ( uuid )                            )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . Go                    ( self . AssignAsIcon , ( uuid , )        )
      return True
    ##########################################################################
    if                             ( at == 1301                            ) :
      self . UsingName = False
      self . Naming    = ""
      self . clear                 (                                         )
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1302                            ) :
      self . UsingName = True
      self . Naming    = "Size"
      self . clear                 (                                         )
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1303                            ) :
      self . UsingName = True
      self . Naming    = "Name"
      self . clear                 (                                         )
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1304                            ) :
      self . UsingName = True
      self . Naming    = "Uuid"
      self . clear                 (                                         )
      self . startup               (                                         )
      return True
    ##########################################################################
    return True
##############################################################################
