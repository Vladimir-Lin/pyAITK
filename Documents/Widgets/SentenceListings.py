# -*- coding: utf-8 -*-
##############################################################################
## SentenceListings
## 影片列表
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
from   PyQt5 . QtCore                 import QSizeF
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
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . TreeDock          import TreeDock    as TreeDock
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . People     . People    import People
##############################################################################
class SentenceListings             ( TreeDock                              ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( list                                    )
  OpenLogHistory    = pyqtSignal   ( str , str , str , str , str             )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . LType              = 0
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 40
    self . SortOrder          = "asc"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 2                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ## self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 400 , 640 )                       )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenSentenceNames                 )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    ##########################################################################
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    ##########################################################################
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    ##########################################################################
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                ( self                                        ) :
    ##########################################################################
    if                       ( not self . isPrepared ( )                   ) :
      return False
    ##########################################################################
    self . setActionLabel    ( "Label" , self . windowTitle ( )              )
    self . AttachActions     ( True                                          )
    self . attachActionsTool (                                               )
    self . LinkVoice         ( self . CommandParser                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . LinkVoice         ( None                                          )
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0 ]                        ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "SentenceListings" , 1                           )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem               ( self , JSOX                              ) :
    ##########################################################################
    UUID       = JSOX           [ "Uuid"                                     ]
    NAME       = JSOX           [ "Name"                                     ]
    ##########################################################################
    IT = self . PrepareUuidItem ( 0 , UUID , NAME                            )
    ##########################################################################
    IT . setTextAlignment       ( 1 , Qt . AlignRight                        )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                   (                                              )
  def InsertItem              ( self                                       ) :
    ##########################################################################
    item = QTreeWidgetItem    (                                              )
    item . setData            ( 0 , Qt . UserRole , 0                        )
    self . addTopLevelItem    ( item                                         )
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot             (                                                    )
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def nameChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item , 0                                   )
    ##########################################################################
    if                          ( len ( msg ) <= 0                         ) :
      self . removeTopLevelItem ( item                                       )
      return
    ##########################################################################
    item   . setText            ( column , msg                               )
    ##########################################################################
    self   . removeParked       (                                            )
    VAL    =                    ( item , uuid , msg ,                        )
    self   . Go                 ( self . AssureUuidItem , VAL                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , JSONs                           ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    for J in JSONs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( J                                        )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( JSONs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    UUIDs   = self . DefaultObtainsItemUuids ( DB                            )
    ##########################################################################
    ITEMs   =                         [                                      ]
    ##########################################################################
    NAMTAB  = self . Tables           [ "Names"                              ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME  = self . GetName          ( DB , NAMTAB , UUID , "Default"       )
      ########################################################################
      J     =                         { "Uuid" : UUID , "Name" : NAME        }
      ########################################################################
      ITEMs . append                  ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( ITEMs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( ITEMs                                )
    ##########################################################################
    self   . Notify                   ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot          (                                                       )
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . Go      ( self . loading                                        )
    ##########################################################################
    return
  ############################################################################
  def FetchRegularDepotCount        ( self , DB                            ) :
    ##########################################################################
    PHRTAB = self . GetDefaultTable (                                        )
    QQ     = f"select count(*) from {PHRTAB} where ( `used` > 0 ) ;"
    DB     . Query                  ( QQ                                     )
    ONE    = DB . FetchOne          (                                        )
    ##########################################################################
    if                              ( ONE == None                          ) :
      return 0
    ##########################################################################
    if                              ( len ( ONE ) <= 0                     ) :
      return 0
    ##########################################################################
    return ONE                      [ 0                                      ]
  ############################################################################
  def GetDefaultTable           ( self                                     ) :
    ##########################################################################
    PHRTAB = self . Tables      [ "Sentences"                                ]
    ##########################################################################
    LOC    = self . getLocality (                                            )
    ##########################################################################
    if                          ( 1002 == LOC                              ) :
      return "`appellations`.`sentences-0001`"
    ##########################################################################
    if                          ( 1003 == LOC                              ) :
      return "`appellations`.`sentences-0001`"
    ##########################################################################
    if                          ( 1001 == LOC                              ) :
      return "`appellations`.`sentences-0002`"
    ##########################################################################
    if                          ( 1006 == LOC                              ) :
      return "`appellations`.`sentences-0006`"
    ##########################################################################
    if                          ( 1007 == LOC                              ) :
      return "`appellations`.`sentences-0007`"
    ##########################################################################
    if                          ( 1008 == LOC                              ) :
      return "`appellations`.`sentences-0008`"
    ##########################################################################
    if                          ( 1009 == LOC                              ) :
      return "`appellations`.`sentences-0009`"
    ##########################################################################
    if                          ( 1010 == LOC                              ) :
      return "`appellations`.`sentences-0010`"
    ##########################################################################
    return PHRTAB
  ############################################################################
  def GetDefaultUuid            ( self                                     ) :
    ##########################################################################
    LOC    = self . getLocality (                                            )
    ##########################################################################
    if                          ( 1002 == LOC                              ) :
      return 5930000000000000001
    ##########################################################################
    if                          ( 1003 == LOC                              ) :
      return 5930000000000000001
    ##########################################################################
    if                          ( 1001 == LOC                              ) :
      return 5930000010000000001
    ##########################################################################
    if                          ( 1006 == LOC                              ) :
      return 5930000020000000001
    ##########################################################################
    if                          ( 1007 == LOC                              ) :
      return 5930000030000000001
    ##########################################################################
    if                          ( 1008 == LOC                              ) :
      return 5930000040000000001
    ##########################################################################
    if                          ( 1009 == LOC                              ) :
      return 5930000050000000001
    ##########################################################################
    if                          ( 1010 == LOC                              ) :
      return 5930000060000000001
    ##########################################################################
    return   5930000000000000001
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    PHRTAB = self . GetDefaultTable (                                        )
    STID   = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    QQ     = f"""select `uuid` from {PHRTAB}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def ObtainsInformation                         ( self , DB               ) :
    ##########################################################################
    self . Total = self . FetchRegularDepotCount (        DB                 )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    PHRTAB = self . GetDefaultTable (                                        )
    NAMTAB = self . Tables          [ "NamesEditing"                         ]
    LOC    = self . getLocality     (                                        )
    ##########################################################################
    DB     . LockWrites       ( [ PHRTAB , NAMTAB                          ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    if                        ( uuid <= 0                                  ) :
      ########################################################################
      uuid = DB . LastUuid    ( PHRTAB , "uuid" , self . GetDefaultUuid (  ) )
      ########################################################################
      QQ   = f"""insert into {PHRTAB}
                 ( `uuid` , `used` , `type` , `locality` )
                 values
                 ( {uuid} , 1 , 1 , {LOC} ) ;"""
      QQ   = " " . join       ( QQ . split ( )                               )
      DB   . Query            ( QQ                                           )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
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
    return          { "Match" : False                                        }
  ############################################################################
  def OpenSentenceNames         ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    uuid   = atItem . data      ( 0 , Qt . UserRole                          )
    uuid   = int                ( uuid                                       )
    head   = atItem . text      ( 0                                          )
    NAM    = self . Tables      [ "NamesEditing"                             ]
    self   . EditAllNames       ( self , "Sentence" , uuid , NAM             )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9001 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                ( self , mm , item                         ) :
    ##########################################################################
    if                          ( self . NotOkay ( item )                  ) :
      return mm
    ##########################################################################
    msg  = self . getMenuItem   ( "GroupFunctions"                           )
    COL  = mm . addMenu         ( msg                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "CopySentenceUuid"                         )
    mm   . addActionFromMenu    ( COL , 38521001 , msg                       )
    ##########################################################################
    mm   . addSeparatorFromMenu ( COL                                        )
    ##########################################################################
    msg  = self . getMenuItem   ( "Description"                              )
    mm   . addActionFromMenu    ( COL , 38522001 , msg                       )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , item                     ) :
    ##########################################################################
    if                              ( at == 38521001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38522001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      head = item . text            ( 0                                      )
      nx   = ""
      ########################################################################
      if                            ( "Notes" in self . Tables             ) :
        nx = self . Tables          [ "Notes"                                ]
      ########################################################################
      self . OpenLogHistory . emit  ( head                                   ,
                                      str ( uuid )                           ,
                                      "Description"                          ,
                                      nx                                     ,
                                      ""                                     )
      ########################################################################
      return True
    ##########################################################################
    return False
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
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    self   . AppendInsertAction    ( mm , 1101                               )
    self   . AppendRenameAction    ( mm , 1102                               )
    self   . TryAppendEditNamesAction ( atItem , mm , 1601                   )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . GroupsMenu            ( mm ,        atItem                      )
    self   . ColumnsMenu           ( mm                                      )
    self   . SortingMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu (                                     )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return
    ##########################################################################
    OKAY   = self . RunDocking     ( mm , aa                                 )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu ( at                                      )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu ( at                                      )
    if                             ( OKAY                                  ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu  ( at , atItem                             )
    if                             ( OKAY                                  ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      ########################################################################
      self . restart               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . RenameItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      ########################################################################
      uuid = self . itemUuid       ( atItem , 0                              )
      NAM  = self . Tables         [ "NamesEditing"                          ]
      self . EditAllNames          ( self , "Video" , uuid , NAM             )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
