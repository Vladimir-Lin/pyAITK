# -*- coding: utf-8 -*-
##############################################################################
## ProjectsView
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
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . IconDock          import IconDock    as IconDock
##############################################################################
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
class ProjectsView            ( IconDock                                   ) :
  ############################################################################
  HavingMenu   = 1371434312
  ############################################################################
  ProjectTasks = pyqtSignal   ( str , str                                    )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super ( ) . __init__      (        parent        , plan                  )
    ##########################################################################
    self . SortOrder    = "desc"
    self . dockingPlace = Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction        ( self . HavingMenu , True                     )
    ##########################################################################
    self . setDragEnabled     ( True                                         )
    self . setAcceptDrops     ( True                                         )
    self . setDragDropMode    ( QAbstractItemView . DragDrop                 )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                ( self                                       ) :
    return QSize              ( 840 , 800                                    )
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
  def GetUuidIcon                ( self , DB , Uuid                        ) :
    ##########################################################################
    RELTAB = self . Tables       [ "Relation"                                ]
    REL    = Relation            (                                           )
    REL    . set                 ( "first" , Uuid                            )
    REL    . setT1               ( "Project"                                 )
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
  def ObtainUuidsQuery         ( self                                      ) :
    ##########################################################################
    ORDER  = self . SortOrder
    PRJTAB = self . Tables     [ "Projects"                                  ]
    QQ     = f"""select `uuid` from {PRJTAB}
                 where ( `used` = 1 )
                 order by `id` {ORDER} ;"""
    ##########################################################################
    return " " . join          ( QQ . split ( )                              )
  ############################################################################
  def FetchIcons                      ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    FMT     = self . getMenuItem      ( "Total"                              )
    MSG     = FMT  . format           ( len ( UUIDs )                        )
    self    . setToolTip              ( MSG                                  )
    ##########################################################################
    DB      = self . ConnectHost      ( self . IconDB , True                 )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    for U in UUIDs                                                           :
      if                              ( not self . LoopRunning             ) :
        continue
      if                              ( U in self . UuidItemMaps           ) :
        item = self . UuidItemMaps    [ U                                    ]
        PUID = self . GetUuidIcon     ( DB , U                               )
        if                            ( PUID > 0                           ) :
          icon = self . FetchIcon     ( DB , PUID                            )
          if                          ( icon != None                       ) :
            self . emitAssignIcon . emit ( item , icon                       )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "project/uuids"
    message = self . getMenuItem ( "ProjectsSelected" )
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
    formats = "people/uuids"
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
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( "ContiguousSelection"                       )
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def LineEditorFinished                ( self                             ) :
    ##########################################################################
    if                                  ( self . EditItem   == None        ) :
      return
    ##########################################################################
    if                                  ( self . EditWidget == None        ) :
      return
    ##########################################################################
    IT                = self . EditItem
    LE                = self . EditWidget
    self . EditItem   = None
    self . EditWidget = None
    CORRECT           = True
    ##########################################################################
    JSON              = self . itemJson ( IT                                 )
    TEXT              = LE   . text     (                                    )
    NAME              = ""
    UUID              = 0
    self              . setItemWidget   ( IT , None                          )
    ##########################################################################
    if ( ( CORRECT ) and ( "Uuid" not in JSON ) )                            :
      CORRECT         = False
    else                                                                     :
      UUID            = JSON            [ "Uuid"                             ]
    ##########################################################################
    if ( ( CORRECT ) and ( "Name" in JSON ) )                                :
      NAME            = JSON            [ "Name"                             ]
    ##########################################################################
    if ( ( CORRECT ) and ( UUID == 0 ) and ( len ( TEXT ) <= 0 ) )           :
      CORRECT         = False
    ##########################################################################
    if ( ( CORRECT ) and ( UUID >  0 ) and ( NAME == TEXT ) )                :
      CORRECT         = False
    ##########################################################################
    if                                  ( not CORRECT                      ) :
      if                                ( UUID <= 0                        ) :
        self . takeItem                 ( self . row ( IT )                  )
      return
    ##########################################################################
    if                                  ( UUID > 0                         ) :
      ########################################################################
      if                                ( self . UsingName                 ) :
        ######################################################################
        IT   . setText                  ( TEXT                               )
        self . PrepareItemContent       ( IT , UUID , TEXT                   )
        self . Go                       ( self . UpdateItemName            , \
                                          ( IT , UUID , TEXT , )             )
      ########################################################################
      return
    ##########################################################################
    IT   . setText                      ( TEXT                               )
    ##########################################################################
    self . Go                           ( self . AppendItemName            , \
                                          ( IT , TEXT , )                    )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                          (                                       )
  def InsertItem                     ( self                                ) :
    ##########################################################################
    IT     = self . PrepareEmptyItem (                                       )
    if                               ( self . SortOrder == "asc"           ) :
      self . addItem                 (     IT                                )
    else                                                                     :
      self . insertItem              ( 0 , IT                                )
    ##########################################################################
    self   . setLineEdit             ( IT                                  , \
                                       "editingFinished"                   , \
                                       self . LineEditorFinished             )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                        (                                         )
  def RenameItem                   ( self                                  ) :
    ##########################################################################
    IT   = self . currentItem      (                                         )
    ##########################################################################
    if                             ( IT == None                            ) :
      return
    ##########################################################################
    self . setLineEdit             ( IT                                    , \
                                     "editingFinished"                     , \
                                     self . LineEditorFinished               )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                                (                                 )
  def CopyToClipboard                      ( self                          ) :
    ##########################################################################
    items    = self . selectedItems        (                                 )
    ##########################################################################
    if                                     ( len ( items ) > 0             ) :
      ########################################################################
      T      =                             [                                 ]
      for item in items                                                      :
        T    . append                      ( item . text ( )                 )
      ########################################################################
      S      = "\n" . join                 ( T                               )
      qApp   . clipboard ( ) . setText     ( S                               )
      ########################################################################
      """
      mime   = self . dragMime             (                                 )
      if                                   ( mime not in [ False , None ]  ) :
        qApp . clipboard ( ) . setMimeData ( mime                            )
      """
    ##########################################################################
    """
    if                                     ( item not in [ False , None ]  ) :
      ########################################################################
      qApp   . clipboard ( ) . setText     ( item . text ( )                 )
    """
    ##########################################################################
    return
  ############################################################################
  def UpdateItemName                   ( self , item , uuid , name         ) :
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    if                                 ( DB == None                        ) :
      return
    ##########################################################################
    NAMTAB  = self . Tables            [ "Names"                             ]
    DB      . LockWrites               ( [ NAMTAB ]                          )
    ##########################################################################
    self    . AssureUuidNameByLocality ( DB                                , \
                                         NAMTAB                            , \
                                         uuid                              , \
                                         name                              , \
                                         self . getLocality ( )              )
    ##########################################################################
    DB      . UnlockTables             (                                     )
    DB      . Close                    (                                     )
    ##########################################################################
    return
  ############################################################################
  def AppendItemName                     ( self , item , name              ) :
    ##########################################################################
    DB       = self . ConnectDB          (                                   )
    if                                   ( DB == None                      ) :
      return
    ##########################################################################
    PRJTAB   = self . Tables             [ "Projects"                        ]
    PRDTAB   = self . Tables             [ "Periods"                         ]
    NAMTAB   = self . Tables             [ "Names"                           ]
    TABLES   =                           [ PRJTAB , PRDTAB , NAMTAB          ]
    ##########################################################################
    DB       . LockWrites                ( TABLES                            )
    ##########################################################################
    HEAD     = 5702000000000000000
    uuid     = DB   . LastUuid           ( PRJTAB , "uuid" , HEAD            )
    DB       . AddUuid                   ( PRJTAB ,  uuid  , 1               )
    ##########################################################################
    NOW      = StarDate                  (                                   )
    NOW      . Now                       (                                   )
    CDT      = NOW . Stardate
    ##########################################################################
    PRD      = Periode                   (                                   )
    PRID     = PRD  . GetUuid            ( DB , PRDTAB                       )
    ##########################################################################
    PRD      . Realm    = uuid
    PRD      . Role     = 71
    PRD      . Item     = 1
    PRD      . States   = 0
    PRD      . Creation = CDT
    PRD      . Modified = CDT
    Items    =                           [ "realm"                         , \
                                           "role"                          , \
                                           "item"                          , \
                                           "states"                        , \
                                           "creation"                      , \
                                           "modified"                        ]
    PRD      . UpdateItems               ( DB , PRDTAB , Items               )
    ##########################################################################
    self     . AssureUuidNameByLocality  ( DB                              , \
                                           NAMTAB                          , \
                                           uuid                            , \
                                           name                            , \
                                           self . getLocality ( )            )
    ##########################################################################
    DB       . UnlockTables              (                                   )
    DB       . Close                     (                                   )
    ##########################################################################
    self     . PrepareItemContent        ( item , uuid , name                )
    self     . assignToolTip             ( item , str ( uuid )               )
    ##########################################################################
    FMT      = self . getMenuItem        ( "Total"                           )
    MSG      = FMT  . format             ( self . count ( )                  )
    self     . setToolTip                ( MSG                               )
    ##########################################################################
    return
  ############################################################################
  def CommandParser ( self , language , message , timestamp                ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectNone"   , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    """
    if ( self . WithinCommand ( language , "UI::OpenSubgroup" , message )  ) :
      if            ( self . OpenCurrentSubgroup ( )                       ) :
        return      { "Match" : True , "Message" : TRX [ "UI::Processed" ]   }
      else                                                                   :
        return      { "Match" : True                                         }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::OpenAlbums"   , message )  ) :
      if            ( self . OpenCurrentAlbum ( )                          ) :
        return      { "Match" : True , "Message" : TRX [ "UI::Processed" ]   }
      else                                                                   :
        return      { "Match" : True                                         }
    """
    ##########################################################################
    return          { "Match" : False                                        }
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
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      mm   . addAction             ( 1102 ,  TRX [ "UI::Rename"   ]          )
      ########################################################################
      msg  = self . getMenuItem    ( "Tasks"                                 )
      mm   . addAction             ( 1301 , msg                              )
      ########################################################################
      if                           ( self . EditAllNames != None           ) :
        ######################################################################
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    mm     = self . SortingMenu    ( mm                                      )
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
    if                             ( self . RunSortingMenu     ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
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
      ########################################################################
      self . InsertItem            (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      ########################################################################
      self . RenameItem            (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1301                            ) :
      ########################################################################
      name = atItem . text         (                                         )
      self . ProjectTasks . emit   ( name , str ( uuid )                     )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      ########################################################################
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Projects" , uuid , NAM          )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
