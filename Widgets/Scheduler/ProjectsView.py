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
from   AITK  . Scheduler  . Project   import Project     as Project
from   AITK  . Scheduler  . Projects  import Projects    as Projects
from   AITK  . Scheduler  . Event     import Event       as Event
from   AITK  . Scheduler  . Events    import Events      as Events
from   AITK  . Scheduler  . Task      import Task        as Task
from   AITK  . Scheduler  . Tasks     import Tasks       as Tasks
##############################################################################
from   AITK  . Networking . WSS       import wssClient   as wssClient
##############################################################################
class ProjectWssOnce          ( wssClient                                  ) :
  ############################################################################
  def onConnected             ( self , wss                                 ) :
    ##########################################################################
    self . sendJson           ( self . JSON                                  )
    self . stop               (                                              )
    ##########################################################################
    return True
##############################################################################
def SendOnceWssJson    ( WSS , JSON                                        ) :
  ############################################################################
  PWS = ProjectWssOnce ( WSS                                                 )
  PWS . JSON = JSON
  PWS . start          (                                                     )
  ############################################################################
  return
##############################################################################
class ProjectsView            ( IconDock                                   ) :
  ############################################################################
  HavingMenu   = 1371434312
  ############################################################################
  ProjectTasks = pyqtSignal   ( str , int , str , QIcon                      )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    super ( ) . __init__      (        parent        , plan                  )
    ##########################################################################
    self . SortOrder    = "asc"
    self . dockingPlace = Qt . BottomDockWidgetArea
    ##########################################################################
    self . MountClicked       ( 1                                            )
    self . MountClicked       ( 2                                            )
    ##########################################################################
    self . setFunction        ( self . HavingMenu , True                     )
    ##########################################################################
    self . setDragEnabled     ( True                                         )
    self . setAcceptDrops     ( True                                         )
    self . setDragDropMode    ( QAbstractItemView . DragDrop                 )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    self . LinkAction      ( "Refresh"    , self . startup                   )
    ##########################################################################
    self . LinkAction      ( "Insert"     , self . InsertItem                )
    self . LinkAction      ( "Rename"     , self . RenameItem                )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard           )
    ##########################################################################
    self . LinkAction      ( "SelectAll"  , self . SelectAll                 )
    self . LinkAction      ( "SelectNone" , self . SelectNone                )
    ##########################################################################
    self . LinkVoice       ( self . CommandParser                            )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut             ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkVoice       ( None                                            )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ReportTotalProjects     ( self                                       ) :
    ##########################################################################
    FMT  = self . getMenuItem ( "Total"                                      )
    MSG  = FMT  . format      ( self . count ( )                             )
    self . setToolTip         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def GetUuidIcon                    ( self , DB , Uuid                    ) :
    ##########################################################################
    RELTAB = self . Tables           [ "RelationIcons"                       ]
    ##########################################################################
    return self . defaultGetUuidIcon ( DB , RELTAB , "Project" , Uuid        )
  ############################################################################
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    ORDER  = self . SortOrder
    PRJTAB = self . Tables [ "Projects"                                      ]
    QQ     = f"""select `uuid` from {PRJTAB}
                 where ( `used` = 1 )
                 order by `id` {ORDER} ;"""
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def FetchIcons                    ( self , UUIDs                         ) :
    ##########################################################################
    if                              ( len ( UUIDs ) <= 0                   ) :
      return
    ##########################################################################
    self      . ReportTotalProjects (                                        )
    super ( ) . FetchIcons          ( UUIDs                                  )
    ##########################################################################
    return
  """
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
  """
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "project/uuids"
    message = self . getMenuItem ( "ProjectsSelected"                        )
    ##########################################################################
    return self . CreateDragMime ( self , mtype , message                    )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes     ( self , mime                                   ) :
    ##########################################################################
    FMTs    =              [ "picture/uuids"                               , \
                             "task/uuids"                                    ]
    formats = ";" . join   ( FMTs                                            )
    ##########################################################################
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def acceptPictureDrop ( self                                             ) :
    return True
  ############################################################################
  def acceptTasksDrop   ( self                                             ) :
    return True
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
    if                              ( mtype in [ "picture/uuids" ]          ) :
      ########################################################################
      title = sourceWidget . windowTitle ( )
      CNT   = len                   ( UUIDs                                  )
      MSG   = f"從「{title}」複製{CNT}個人物"
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "task/uuids" ]            ) :
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
  def dropPictures             ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("ProjectsView::dropPictures")
    print(JSOX)
    if ( atItem is not None ) :
      print("TO:",atItem.text())
    ##########################################################################
    return True
  ############################################################################
  def dropTasks                ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("ProjectsView::dropTasks")
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
    ##########################################################################
    return
  ############################################################################
  def UpdateItemName                  ( self , item , uuid , name          ) :
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    NAMTAB = self . Tables            [ "NamesLocal"                         ]
    DB     . LockWrites               ( [ NAMTAB ]                           )
    ##########################################################################
    self   . AssureUuidNameByLocality ( DB                                 , \
                                        NAMTAB                             , \
                                        uuid                               , \
                                        name                               , \
                                        self . getLocality ( )               )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    DB     . Close                    (                                      )
    self   . Notify                   ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def AppendItemName                  ( self , item , name                 ) :
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    PRJS   = Projects                 (                                      )
    PRJS   . Tables = self . Tables
    ##########################################################################
    PRJTAB = self . Tables            [ "Projects"                           ]
    PRDTAB = self . Tables            [ "Periods"                            ]
    NAMTAB = self . Tables            [ "NamesLocal"                         ]
    TABLES =                          [ PRJTAB , PRDTAB , NAMTAB             ]
    ##########################################################################
    DB     . LockWrites               ( TABLES                               )
    ##########################################################################
    uuid   = PRJS . AppendProject     ( DB                                   )
    self   . AssureUuidNameByLocality ( DB                                 , \
                                        NAMTAB                             , \
                                        uuid                               , \
                                        name                               , \
                                        self . getLocality ( )               )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    DB     . Close                    (                                      )
    ##########################################################################
    self   . PrepareItemContent       ( item , uuid , name                   )
    self   . assignToolTip            ( item , str ( uuid )                  )
    self   . ReportTotalProjects      (                                      )
    ##########################################################################
    ## 通知後台新增一個計畫
    ## SendToBack ( uuid )
    ##########################################################################
    self   . Notify                   ( 5                                    )
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
  def SendToBack           ( self , uuid                                   ) :
    ##########################################################################
    WSS  = self . Settings [ "Scheduling" ] [ "WSS"                          ]
    JSON = { "Role"    : "Administrator"                                     ,
             "Action"  : "Query"                                             ,
             "Project" : uuid                                                }
    SendOnceWssJson        ( WSS , JSON                                      )
    ##########################################################################
    return
  ############################################################################
  def DetailsMenu                ( self , mm , atItem                      ) :
    ##########################################################################
    LOM     = mm . addMenu       ( self . getMenuItem ( "Details" )          )
    ##########################################################################
    msg  = self . getMenuItem    ( "Tasks"                                   )
    mm   . addActionFromMenu     ( LOM , 406301 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunDetailsMenu             ( self , atId , atItem                    ) :
    ##########################################################################
    if                           ( atId == 406301                          ) :
      ########################################################################
      name = atItem . text       (                                           )
      uuid = atItem . data       ( Qt . UserRole                             )
      uuid = int                 ( uuid                                      )
      icon = atItem . icon       (                                           )
      self . ProjectTasks . emit ( name , 71 , str ( uuid ) , icon           )
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    self   . Notify                ( 0                                       )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    """
    items  = self . selectedItems  (                                         )
    atItem = self . itemAt         ( pos                                     )
    uuid   = 0
    ##########################################################################
    if                             ( atItem != None                        ) :
      uuid = atItem . data         ( Qt . UserRole                           )
      uuid = int                   ( uuid                                    )
    """
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      self . AppendRenameAction    ( mm , 1102                               )
      ########################################################################
      if                           ( self . doEditAllNames ( )             ) :
        ######################################################################
        self . AppendEditNamesAction ( mm , 1601                             )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      mm   . addAction             ( 1801 , "查詢" )
      ########################################################################
      self . DetailsMenu           ( mm , atItem                             )
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
    if                             ( self . RunDetailsMenu ( at , atItem ) ) :
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
    if                             ( at == 1601                            ) :
      ########################################################################
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Projects" , uuid , NAM          )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1801                            ) :
      self . SendToBack            ( uuid                                    )
    ##########################################################################
    return True
##############################################################################
