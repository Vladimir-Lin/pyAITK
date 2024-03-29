# -*- coding: utf-8 -*-
##############################################################################
## ObjectRelationsEditor
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
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
from   PyQt5 . QtWidgets              import QCheckBox
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . TreeDock          import TreeDock    as TreeDock
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
from   AITK  . Qt . CheckBox          import CheckBox    as CheckBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
##############################################################################
class ObjectRelationsEditor        ( TreeDock                              ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( list                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 25
    self . SortOrder          = "asc"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 6                                       )
    self . setColumnHidden         ( 5 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow . connect ( self . show                             )
    self . emitAllNames  . connect ( self . refresh                          )
    self . itemChanged   . connect ( self . AcceptItemChanged                )
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
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 800 , 640                               )
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    ##########################################################################
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
    ##########################################################################
    self . LinkAction              ( "Rename"     , self . RenameItem        )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                     ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 2 , 3 , 4 ]              ) :
      return
    ##########################################################################
    if                          ( column     in [ 2 , 3 , 4 ]              ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent           ( self , item , JSON                    ) :
    ##########################################################################
    ID          = JSON             [ "Id"                                    ]
    UUID        = JSON             [ "Uuid"                                  ]
    UXID        = str              ( UUID                                    )
    USED        = JSON             [ "Used"                                  ]
    DESCRIPTION = JSON             [ "Description"                           ]
    NAME        = JSON             [ "Name"                                  ]
    COMMENT     = JSON             [ "Comment"                               ]
    ##########################################################################
    Flags       = item . flags     (                                         )
    Flags       = Flags | Qt . ItemIsUserCheckable
    item        . setFlags         ( Flags                                   )
    item        . setData          ( 0 , Qt . UserRole , UXID                )
    ##########################################################################
    if                             ( USED == 0                             ) :
      item      . setCheckState    ( 0 , Qt . Unchecked                      )
    else                                                                     :
      item      . setCheckState    ( 0 , Qt . Checked                        )
    ##########################################################################
    item        . setText          ( 1 , str ( ID )                          )
    item        . setToolTip       ( 1 , UXID                                )
    item        . setTextAlignment ( 1 , Qt.AlignRight                       )
    ##########################################################################
    item        . setText          ( 2 , DESCRIPTION                         )
    item        . setToolTip       ( 2 , UXID                                )
    ##########################################################################
    item        . setText          ( 3 , NAME                                )
    item        . setToolTip       ( 3 , UXID                                )
    ##########################################################################
    item        . setText          ( 4 , COMMENT                             )
    ##########################################################################
    item        . setData          ( 5 , Qt . UserRole , JSON                )
    ##########################################################################
    return item
  ############################################################################
  def PrepareItem                    ( self                , JSON          ) :
    return self . PrepareItemContent ( QTreeWidgetItem ( ) , JSON            )
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 2 , 3 , 4                                 ] )
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
    if                          ( column in [ 2 ]                          ) :
      ########################################################################
      item . setText            ( column ,              msg                  )
      self . removeParked       (                                            )
      ########################################################################
      self . Go                 ( self . UpdateItemName                    , \
                                  ( uuid , msg , )                           )
      ########################################################################
      return
    ##########################################################################
    if                          ( column not in [ 3 , 4 ]                  ) :
      ########################################################################
      item . setText            ( column , text                              )
      self . removeParked       (                                            )
      ########################################################################
      return
    ##########################################################################
    na     = ""
    ##########################################################################
    if                          ( column == 3                              ) :
      na   = "name"
    elif                        ( column == 4                              ) :
      na   = "comment"
    ##########################################################################
    item   . setText            ( column , msg                               )
    self   . removeParked       (                                            )
    self   . Go                 ( self . UpdateItemBlob                    , \
                                  ( uuid , na , msg , )                      )
    ##########################################################################
    return
  ############################################################################
  def AcceptItemChanged          ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in [ 0 ]                     ) :
      return
    ##########################################################################
    UUID     = item . data       ( 0 , Qt . UserRole                         )
    UUID     = int               ( UUID                                      )
    ##########################################################################
    if                           ( column == 0                             ) :
      ########################################################################
      cstate = item . checkState ( 0                                         )
      USED   = 0
      ########################################################################
      if                         ( cstate == Qt . Unchecked                ) :
        USED = 0
      elif                       ( cstate == Qt . Checked                  ) :
        USED = 1
      ########################################################################
      self   . Go                ( self . UpdateItemValue                  , \
                                   ( UUID , "used" , USED , )                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                           (        list                          )
  def refresh                         ( self , LISTs                       ) :
    ##########################################################################
    self   . clear                   (                                       )
    ##########################################################################
    for JSON in LISTs                                                        :
      ########################################################################
      IT   = self . PrepareItem      ( JSON                                  )
      self . addTopLevelItem         ( IT                                    )
    ##########################################################################
    FMT    = self . getMenuItem      ( "DisplayTotal"                        )
    MSG    = FMT  . format           ( len ( LISTs )                         )
    self   . setToolTip              ( MSG                                   )
    ##########################################################################
    self   . emitNamesShow . emit    (                                       )
    ##########################################################################
    TOTAL  = self . columnCount      (                                       )
    self   . resizeColumnsToContents ( range ( 0 , TOTAL - 2 )               )
    ##########################################################################
    return
  ############################################################################
  def ObtainsItemUuids                ( self , DB                          ) :
    ##########################################################################
    QQ      = self . ObtainUuidsQuery (                                      )
    UUIDs   =                         [                                      ]
    if                                ( len ( QQ ) > 0                     ) :
      UUIDs = DB   . ObtainUuids      ( QQ                                   )
    ##########################################################################
    return UUIDs
  ############################################################################
  def ObtainRelations          ( self , DB , UUIDs                         ) :
    ##########################################################################
    if                         ( len ( UUIDs ) <= 0                        ) :
      return                   {                                             }
    ##########################################################################
    LISTs     =                [                                             ]
    GRPTAB    = self . Tables  [ "Groups"                                    ]
    NAMTAB    = self . Tables  [ "Names"                                     ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME    = self . GetName ( DB , NAMTAB , UUID                          )
      ########################################################################
      QQ      = f"""select
                    `id`,`used`,`name`,`comment`
                    from {GRPTAB}
                    where ( `uuid` = {UUID} ) ;"""
      QQ      = " " . join     ( QQ . split ( )                              )
      DB      . Query          ( QQ                                          )
      RR      = DB . FetchOne  (                                             )
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 4 ) )          :
        ######################################################################
        J     = { "Id"          : int ( RR [ 0 ]                           ) ,
                  "Uuid"        : int ( UUID                               ) ,
                  "Used"        : int ( RR [ 1 ]                           ) ,
                  "Description" : NAME                                       ,
                  "Name"        : self . assureString ( RR [ 2 ]           ) ,
                  "Comment"     : self . assureString ( RR [ 3 ]           ) }
        LISTs . append         ( J                                           )
    ##########################################################################
    return LISTs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    LISTs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      LISTs = self . ObtainRelations  ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( LISTs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( LISTs                                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
  ############################################################################
  def ObtainAllUuids        ( self , DB                                    ) :
    ##########################################################################
    GRPTAB = self . Tables  [ "Groups"                                       ]
    ##########################################################################
    QQ     = f"""select `uuid` from {GRPTAB}
                where ( `used` = 1 )
                order by `id` asc ;"""
    ##########################################################################
    QQ     = " " . join     ( QQ . split ( )                                 )
    ##########################################################################
    return DB . ObtainUuids ( QQ , 0                                         )
  ############################################################################
  def TranslateAll              ( self                                     ) :
    ##########################################################################
    DB    = self . ConnectDB    (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    TABLE = self . Tables       [ "Names"                                    ]
    FMT   = self . Translations [ "UI::Translating"                          ]
    self  . DoTranslateAll      ( DB , TABLE , FMT , 15.0                    )
    ##########################################################################
    DB    . Close               (                                            )
    ##########################################################################
    return
  ############################################################################
  def UpdateItemValue         ( self , uuid , item , value                 ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    GRPTAB = self . Tables    [ "Groups"                                     ]
    ##########################################################################
    DB     . LockWrites       ( [ GRPTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    QQ     = f"update {GRPTAB} set `{item}` = {value} where ( `uuid` = {uuid} ) ;"
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def UpdateItemBlob          ( self , uuid , item , blob                  ) :
    ##########################################################################
    try                                                                      :
      blob = blob . encode    ( "utf-8"                                      )
    except                                                                   :
      pass
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    GRPTAB = self . Tables    [ "Groups"                                     ]
    ##########################################################################
    DB     . LockWrites       ( [ GRPTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    QQ     = f"update {GRPTAB} set `{item}` = %s where ( `uuid` = {uuid} ) ;"
    DB     . QueryValues      ( QQ , ( blob , )                              )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def UpdateItemName          ( self , uuid , name                         ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ NAMTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    ##########################################################################
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Home"       , self . PageHome        , False   )
    self . LinkAction      ( "End"        , self . PageEnd         , False   )
    self . LinkAction      ( "PageUp"     , self . PageUp          , False   )
    self . LinkAction      ( "PageDown"   , self . PageDown        , False   )
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation   ( self , DB                                     ) :
    ##########################################################################
    self   . Total = 0
    ##########################################################################
    GRPTAB = self . Tables [ "Groups"                                        ]
    ##########################################################################
    QQ     = f"select count(*) from {GRPTAB} where ( `used` = 1 ) ;"
    DB     . Query         ( QQ                                              )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self   . Total = RR    [ 0                                               ]
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery               ( self                                ) :
    ##########################################################################
    GRPTAB  = self . Tables          [ "Groups"                              ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . getSortingOrder (                                       )
    ##########################################################################
    QQ      = f"""select `uuid` from {GRPTAB}
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join                ( QQ . split ( )                        )
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    ## self   . setColumnWidth   ( 0 , 24                                       )
    self   . setColumnWidth   ( 5 , 3                                        )
    ##########################################################################
    TRX    = self . Translations
    LABELs = TRX              [ "ObjectRelationsEditor" ] [ "Labels"         ]
    self   . setCentralLabels ( LABELs                                       )
    ##########################################################################
    self   . setPrepared      ( True                                         )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9005 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      ## if                           ( ( at == 9001 ) and ( hid )            ) :
      ##   self . startup             (                                         )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                          ( self , pos                           ) :
    ##########################################################################
    if                              ( not self . isPrepared ( )            ) :
      return False
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items  = self . selectedItems   (                                        )
    atItem = self . currentItem     (                                        )
    uuid   = 0
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      uuid = atItem . data          ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu ( mm                                     )
    self   . AppendRefreshAction    ( mm , 1001                              )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      if                            ( self . EditAllNames != None          ) :
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
        mm . addSeparator           (                                        )
    ##########################################################################
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
    mm     . addSeparator           (                                        )
    mm     . addAction              ( 3001 ,  TRX [ "UI::TranslateAll"     ] )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . menuFont ( )                 )
    aa     = mm . exec_             ( QCursor . pos      ( )                 )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self   . RunAmountIndexMenu ( )      ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      self . startup                (                                        )
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      uuid = self . itemUuid        ( items [ 0 ] , 0                        )
      NAM  = self . Tables          [ "NamesEditing"                         ]
      self . EditAllNames           ( self , "Relations" , uuid , NAM        )
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      self . Go                     ( self . TranslateAll                    )
      return True
    ##########################################################################
    return True
##############################################################################
