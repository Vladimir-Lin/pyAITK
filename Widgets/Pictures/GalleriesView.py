# -*- coding: utf-8 -*-
##############################################################################
## GalleriesView
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
from   PyQt5 . QtCore                 import QMimeData
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QMouseEvent
from   PyQt5 . QtGui                  import QDrag
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
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
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . Pictures   . Gallery   import Gallery     as GalleryItem
##############################################################################
class GalleriesView                ( IconDock                              ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  ShowPersonalGallery = pyqtSignal ( str , int , str , QIcon                 )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . Total        =  0
    self . StartId      =  0
    self . Amount       = 60
    self . SortOrder    = "asc"
    ##########################################################################
    self . Grouping     = "Original"
    self . OldGrouping  = "Original"
    ## self . Grouping     = "Subordination"
    ## self . Grouping     = "Reverse"
    ##########################################################################
    self . dockingPlace = Qt . BottomDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "Gallery"                               )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( True                                    )
    self . setAcceptDrops          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
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
    RELTAB = self . Tables       [ "Relation"                                ]
    REL    = Relation            (                                           )
    REL    . set                 ( "first" , Uuid                            )
    REL    . setT1               ( "Gallery"                                 )
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
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    GALTAB = self . Tables   [ "Galleries"                                   ]
    QQ     = f"select count(*) from {GALTAB} where ( `used` = 1 ) ;"
    DB     . Query           ( QQ                                            )
    ONE    = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( ONE == None                                 ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
      return 0
    ##########################################################################
    return ONE               [ 0                                             ]
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
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    GALTAB = self . Tables          [ "Galleries"                            ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    QQ     = f"""select `uuid` from {GALTAB}
                 where ( `used` = 1 )
                 order by `id` {ORDER}
                 limit {SID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
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
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"      , self . windowTitle ( )            )
    self . LinkAction     ( "Refresh"    , self . startup                    )
    ##########################################################################
    self . LinkAction     ( "Insert"     , self . InsertItem                 )
    self . LinkAction     ( "Delete"     , self . DeleteItems                )
    self . LinkAction     ( "Rename"     , self . RenameItem                 )
    ##########################################################################
    self . LinkAction     ( "Home"       , self . PageHome                   )
    self . LinkAction     ( "End"        , self . PageEnd                    )
    self . LinkAction     ( "PageUp"     , self . PageUp                     )
    self . LinkAction     ( "PageDown"   , self . PageDown                   )
    ##########################################################################
    self . LinkAction     ( "SelectAll"  , self . SelectAll                  )
    self . LinkAction     ( "SelectNone" , self . SelectNone                 )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup      , False      )
    self . LinkAction      ( "Insert"     , self . InsertItem   , False      )
    self . LinkAction      ( "Delete"     , self . DeleteItems  , False      )
    self . LinkAction      ( "Rename"     , self . RenameItem   , False      )
    self . LinkAction      ( "Home"       , self . PageHome     , False      )
    self . LinkAction      ( "End"        , self . PageEnd      , False      )
    self . LinkAction      ( "PageUp"     , self . PageUp       , False      )
    self . LinkAction      ( "PageDown"   , self . PageDown     , False      )
    self . LinkAction      ( "SelectAll"  , self . SelectAll    , False      )
    self . LinkAction      ( "SelectNone" , self . SelectNone   , False      )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "gallery/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
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
    FMTs    =              [ "people/uuids"                                , \
                             "gallery/uuids"                               , \
                             "picture/uuids"                                 ]
    formats = ";" . join   ( FMTs                                            )
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
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
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        MSG = f"移動{CNT}個人物"
      else                                                                   :
        MSG = f"從「{title}」複製{CNT}個人物"
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    elif                            ( mtype in [ "picture/uuids" ]         ) :
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
    elif                            ( mtype in [ "gallery/uuids" ]         ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        MSG = f"移動{CNT}個圖庫"
      else                                                                   :
        MSG = f"從「{title}」複製{CNT}個圖庫"
      ########################################################################
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving           ( self , sourceWidget , mimeData , mousePos     ) :
    ##########################################################################
    if                     ( self . droppingAction                         ) :
      return False
    ##########################################################################
    if                     ( sourceWidget != self                          ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( mousePos                                        )
    if                     ( atItem in [ False , None ]                    ) :
      return False
    if                     ( atItem . isSelected ( )                       ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def acceptGalleriesDrop ( self                                           ) :
    ##########################################################################
    ALLOWED =             [ "Subordination" , "Reverse"                      ]
    ##########################################################################
    if                    ( self . Grouping not in ALLOWED                 ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def dropPeople               ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("PeopleView::dropPeople")
    print(JSOX)
    if ( atItem is not None ) :
      print("TO:",atItem.text())
    ##########################################################################
    return True
  ############################################################################
  def dropPictures             ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("PeopleView::dropPictures")
    print(JSOX)
    if ( atItem is not None ) :
      print("TO:",atItem.text())
    ##########################################################################
    return True
  ############################################################################
  def dropGalleries            ( self , source , pos , JSOX                ) :
    ##########################################################################
    atItem = self . itemAt ( pos )
    print("PeopleView::dropGalleries")
    print(JSOX)
    if ( atItem is not None ) :
      print("TO:",atItem.text())
    ##########################################################################
    return True
  ############################################################################
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
        ## self . Go                       ( self . UpdateItemName            , \
        ##                                   ( IT , UUID , TEXT , )             )
      ########################################################################
      return
    ##########################################################################
    IT   . setText                      ( TEXT                               )
    ##########################################################################
    ## self . Go                           ( self . AppendItemName            , \
    ##                                       ( IT , TEXT , )                    )
    ##########################################################################
    return
  ############################################################################
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( "ContiguousSelection"                       )
    self . setPrepared         ( True                                        )
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
  def DeleteItems             ( self                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def RenameItem              ( self                                       ) :
    ##########################################################################
    IT   = self . currentItem (                                              )
    ##########################################################################
    if                        ( IT == None                                 ) :
      return
    ##########################################################################
    self . setLineEdit        ( IT                                         , \
                                "editingFinished"                          , \
                                self . LineEditorFinished                    )
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
    atItem = self . itemAt         ( pos                                     )
    uuid   = 0
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
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
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    if                             ( uuid > 0                              ) :
      mm   . addSeparator          (                                         )
      mm   . addAction             ( 1201 ,  TRX [ "UI::PersonalGallery"   ] )
    ##########################################################################
    mm     . addSeparator          (                                         )
    if                             ( atItem != None                        ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    mm     = self . SortingMenu    ( mm                                      )
    mm     = self . LocalityMenu   ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
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
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1201                            ) :
      ########################################################################
      text = atItem . text         (                                         )
      icon = atItem . icon         (                                         )
      xsid = str                   ( uuid                                    )
      ########################################################################
      self . ShowPersonalGallery . emit ( text , 64 , xsid , icon            )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "People" , uuid , NAM            )
      return True
    ##########################################################################
    return True
##############################################################################
