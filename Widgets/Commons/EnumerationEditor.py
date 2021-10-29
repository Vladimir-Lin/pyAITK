# -*- coding: utf-8 -*-
##############################################################################
## EnumerationEditor
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
class EnumerationEditor            ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( dict                                    )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . Total     = 0
    self . StartId   = 0
    self . Amount    = 25
    self . Order     = "asc"
    self . TypeIDs   =             [                                         ]
    self . TypeNames =             {                                         }
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 8                                       )
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
    return QSize                   ( 1024 , 640                              )
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
    self . LinkAction              ( "Insert"     , self . InsertItem        )
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
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( self . isItemPicked ( )                    ) :
      if                      ( column != self . CurrentItem [ "Column" ]  ) :
        self . removeParked   (                                              )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column > 6                               ) :
      return
    ##########################################################################
    if                          ( column in [ 0 , 1 , 2 , 4 , 6 ]          ) :
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [ 3 ]                          ) :
      ########################################################################
      LL   = self . TypeNames
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . comboChanged                       )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 5 ]                          ) :
      ########################################################################
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      sb   = self . setSpinBox   ( item                                      ,
                                   column                                    ,
                                   0                                         ,
                                   1000000000                                ,
                                   "editingFinished"                         ,
                                   self . spinChanged                        )
      sb   . setValue            ( val                                       )
      sb   . setAlignment        ( Qt . AlignRight                           )
      sb   . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                ( self , UUID , ENUM                      ) :
    ##########################################################################
    UXID = str                   ( UUID                                      )
    IT   = QTreeWidgetItem       (                                           )
    IT   . setText               ( 0 , str ( ENUM [ 0 ] )                    )
    IT   . setData               ( 0 , Qt . UserRole , UUID                  )
    ##########################################################################
    NAME = self . BlobToString   ( ENUM [ 4 ]                                )
    IT   . setText               ( 1 , NAME                                  )
    ##########################################################################
    WIKI = self . BlobToString   ( ENUM [ 6 ]                                )
    IT   . setText               ( 2 , WIKI                                  )
    ##########################################################################
    TID  = int                   ( ENUM [ 1 ]                                )
    TNAM = self . TypeNames      [ TID                                       ]
    IT   . setText               ( 3 , TNAM                                  )
    IT   . setData               ( 3 , Qt . UserRole , TID                   )
    ##########################################################################
    COL  = self . BlobToString   ( ENUM [ 2 ]                                )
    IT   . setText               ( 4 , COL                                   )
    ##########################################################################
    VID  = int                   ( ENUM [ 3 ]                                )
    IT   . setText               ( 5 , str ( VID )                           )
    IT   . setData               ( 5 , Qt . UserRole , VID                   )
    IT   . setTextAlignment      ( 5 , Qt.AlignRight                         )
    ##########################################################################
    COL  = self . BlobToString   ( ENUM [ 5 ]                                )
    IT   . setText               ( 6 , COL                                   )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                      (                                           )
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    item = QTreeWidgetItem       (                                           )
    item . setData               ( 0 , Qt . UserRole , 0                     )
    self . addTopLevelItem       ( item                                      )
    self . doubleClicked         ( item , 0                                  )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def RenameItem                 ( self                                    ) :
    ##########################################################################
    IT = self . currentItem      (                                           )
    if                           ( IT is None                              ) :
      return
    ##########################################################################
    self . doubleClicked         ( IT , 0                                    )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def nameChanged                ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    line   = self . CurrentItem  [ "Widget"                                  ]
    text   = self . CurrentItem  [ "Text"                                    ]
    msg    = line . text         (                                           )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    if                           ( text == msg                             ) :
      self . removeParked        (                                           )
      return
    ##########################################################################
    if                           ( column == 0                             ) :
      ########################################################################
      ALLOW    = False
      uxid     = 0
      ########################################################################
      if                         ( len ( msg ) == 19                       ) :
        try                                                                  :
          uxid = int             ( msg                                       )
        except                                                               :
          pass
      ########################################################################
      if                         ( uxid > 0                                ) :
        head = int               ( uxid / 1000000000000000                   )
        if                       ( head == 5502                            ) :
          ALLOW = True
      ########################################################################
      if                         ( ALLOW                                   ) :
        item . setText           ( column , msg                              )
        item . setData           ( 0 , Qt . UserRole , uxid                  )
        if                       ( uuid == 0                               ) :
          item . setData         ( 3 , Qt . UserRole , 0                     )
          item . setData         ( 5 , Qt . UserRole , 0                     )
          item . setText         ( 5 , "0"                                   )
          self . Go              ( self . AppendTypeItem , ( uxid , )        )
        else                                                                 :
          self . Go              ( self . UpdateTypeItemValue              , \
                                   ( uuid , "uuid" , uxid , )                )
      else                                                                   :
        item . setText           ( column , text                             )
      ########################################################################
      self . removeParked        (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column not in [ 1 , 2 , 4 , 6 ]         ) :
      ########################################################################
      item . setText             ( column , text                             )
      self . removeParked        (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column == 1                             ) :
      na   = "name"
    elif                         ( column == 2                             ) :
      na   = "wiki"
    elif                         ( column == 4                             ) :
      na   = "column"
    elif                         ( column == 6                             ) :
      na   = "comment"
    ##########################################################################
    self   . Go                  ( self . UpdateTypeItemBlob               , \
                                   ( uuid , na , msg , )                     )
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def comboChanged               ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    sb     = self . CurrentItem  [ "Widget"                                  ]
    v      = item . data         ( column , Qt . UserRole                    )
    v      = int                 ( v                                         )
    nv     = sb   . itemData     ( sb . currentIndex ( )                     )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    if                           ( v == nv                                 ) :
      name = self . TypeNames    [ v                                         ]
      item . setText             ( column , name                             )
      self . removeParked        (                                           )
      return
    ##########################################################################
    self . Go                    ( self . UpdateTypeItemValue              , \
                                   ( uuid , "type" , nv , )                  )
    ##########################################################################
    name = self . TypeNames      [ nv                                        ]
    item . setText               ( column , name                             )
    self . removeParked          (                                           )
    ##########################################################################
    return
  ############################################################################
  def spinChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    sb     = self . CurrentItem [ "Widget"                                   ]
    v      = item . data        ( column , Qt . UserRole                     )
    v      = int                ( v                                          )
    nv     = sb   . value       (                                            )
    uuid   = self . itemUuid    ( item , 0                                   )
    ##########################################################################
    if                          ( v == nv                                  ) :
      item . setText            ( column , str ( v )                         )
      self . removeParked       (                                            )
      return
    ##########################################################################
    self . Go                   ( self . UpdateTypeItemValue               , \
                                  ( uuid , "value" , nv , )                  )
    ##########################################################################
    item . setText              ( column , str ( nv )                        )
    self . removeParked         (                                            )
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
      self   . Go                ( self . UpdateTypeItemValue              , \
                                   ( UUID , "used" , USED , )                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                           (        dict                          )
  def refresh                         ( self , JSON                        ) :
    ##########################################################################
    self    . clear                   (                                      )
    ##########################################################################
    UUIDs   = JSON                    [ "UUIDs"                              ]
    ENUMs   = JSON                    [ "ENUMs"                              ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT    = self . PrepareItem      ( U , ENUMs [ U ]                      )
      self  . addTopLevelItem         ( IT                                   )
    ##########################################################################
    self    . emitNamesShow . emit    (                                      )
    ##########################################################################
    TOTAL   = self . columnCount      (                                      )
    self    . resizeColumnsToContents ( range ( 0 , TOTAL - 1 )              )
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
  def ObtainsUuidEnumerations         ( self , DB , UUIDs                  ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return                          {                                      }
    ##########################################################################
    ENUMs   =                         {                                      }
    TABLE   = self . Tables           [ "Enumerations"                       ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select `uuid`,`type`,`column`,`value`,`name`,`comment`,`wiki` from {TABLE}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( ( RR is not False ) and ( RR is not None ) )                      :
        ENUMs [ UUID ] = RR
    ##########################################################################
    return ENUMs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self    . ObtainTypeListings      ( DB                                   )
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    ENUMs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      ENUMs = self . ObtainsUuidEnumerations ( DB , UUIDs                    )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "ENUMs" ] = ENUMs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
  ############################################################################
  def ObtainAllUuids             ( self , DB                               ) :
    ##########################################################################
    TABLE = self . Tables        [ "Enumerations"                            ]
    ##########################################################################
    QQ    = f"select `uuid` from {TABLE} order by `id` asc ;"
    ##########################################################################
    QQ    = " " . join           ( QQ . split ( )                            )
    ##########################################################################
    return DB . ObtainUuids      ( QQ , 0                                    )
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
  def AppendTypeItem               ( self , uuid                           ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TYPTAB  = self . Tables        [ "Enumerations"                          ]
    ##########################################################################
    DB      . LockWrites           ( [ TYPTAB                              ] )
    ##########################################################################
    QQ      = f"insert into {TYPTAB} ( `uuid` ) values ( {uuid} ) ;"
    DB      . Query                ( QQ                                      )
    ##########################################################################
    QQ      = f"update {TYPTAB} set `value` = `id` where ( `uuid` = {uuid} ) ;"
    DB      . Query                ( QQ                                      )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    return
  ############################################################################
  def UpdateTypeItemValue          ( self , uuid , item , value            ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TYPTAB  = self . Tables        [ "Enumerations"                          ]
    ##########################################################################
    DB      . LockWrites           ( [ TYPTAB                              ] )
    ##########################################################################
    uuid    = int                  ( uuid                                    )
    ##########################################################################
    QQ      = f"update {TYPTAB} set `{item}` = {value} where ( `uuid` = {uuid} ) ;"
    DB      . Query                ( QQ                                      )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    return
  ############################################################################
  def UpdateTypeItemBlob           ( self , uuid , item , blob             ) :
    ##########################################################################
    try                                                                      :
      blob  = blob . encode        ( "utf-8"                                 )
    except                                                                   :
      pass
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TYPTAB  = self . Tables        [ "Enumerations"                          ]
    ##########################################################################
    DB      . LockWrites           ( [ TYPTAB                              ] )
    ##########################################################################
    uuid    = int                  ( uuid                                    )
    ##########################################################################
    QQ      = f"update {TYPTAB} set `{item}` = %s where ( `uuid` = {uuid} ) ;"
    DB      . QueryValues          ( QQ , ( blob , )                         )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    return
  ############################################################################
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None" ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock" ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"  ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainTypeListings              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    TYPTAB  = self . Tables           [ "Types"                              ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    ##########################################################################
    self    . TypeIDs   =             [                                      ]
    self    . TypeNames =             {                                      }
    UUIDs   =                         [                                      ]
    UuidIDs =                         {                                      }
    ##########################################################################
    QQ      = f"""select `id`,`uuid` from {TYPTAB}
                  where ( `used` > 0 )
                  order by `id` asc ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchAll           (                                      )
    ##########################################################################
    if ( ( RR in [ None , False ] ) or ( len ( RR ) <= 0 ) )                 :
      return
    ##########################################################################
    for R in RR                                                              :
      ID    =  R                      [ 0                                    ]
      UUID  =  R                      [ 1                                    ]
      self  . TypeIDs . append        ( ID                                   )
      UUIDs . append                  ( UUID                                 )
      UuidIDs [ UUID ] = ID
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . GetNames         ( DB , NAMTAB, UUIDs                   )
      for UUID in UUIDs                                                      :
        ID  = UuidIDs                 [ UUID                                 ]
        NAM = ""
        if                            ( UUID in NAMEs                      ) :
          NAM = NAMEs                 [ UUID                                 ]
        self . TypeNames [ ID ] = NAM
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    TABLE   = self . Tables           [ "Enumerations"                       ]
    ##########################################################################
    QQ      = f"select count(*) from {TABLE} ;"
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self    . Total = RR              [ 0                                    ]
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery        ( self                                       ) :
    ##########################################################################
    TABLE   = self . Tables   [ "Enumerations"                               ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . Order
    ##########################################################################
    QQ      = f"""select `uuid` from {TABLE}
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join         ( QQ . split ( )                               )
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    self   . setColumnWidth   ( 7 , 3                                        )
    ##########################################################################
    TRX    = self . Translations
    LABELs = [ "長編號" , "名稱" , "維基" , "物件類型" , "欄位" , "值" , "註解" , "" ]
    self   . setCentralLabels ( LABELs                                       )
    ##########################################################################
    self   . setPrepared      ( True                                         )
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
  def CopyToClipboard               ( self                                 ) :
    ##########################################################################
    column = self . currentColumn   (                                        )
    if                              ( column > 6                           ) :
      return
    ##########################################################################
    IT     = self . currentItem     (                                        )
    if                              ( IT is None                           ) :
      return
    ##########################################################################
    MSG    = IT . text              ( column                                 )
    LID    = self . getLocality     (                                        )
    qApp   . clipboard ( ). setText ( MSG                                    )
    ##########################################################################
    self   . TtsTalk                ( MSG , LID                              )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    COL    = mm . addMenu          ( TRX [ "UI::Columns" ]                   )
    ##########################################################################
    msg    = TRX                   [ "UI::Whitespace"                        ]
    hid    = self . isColumnHidden ( 7                                       )
    mm     . addActionFromMenu     ( COL , 9007 , msg , True , not hid       )
    ##########################################################################
    return mm
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
    atItem = self . currentItem    (                                         )
    uuid   = 0
    ##########################################################################
    if                             ( atItem != None                        ) :
      uuid = atItem . data         ( 0 , Qt . UserRole                       )
      uuid = int                   ( uuid                                    )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    T      = self . Total
    MSG    = f"總數量:{T}"
    mm     . addAction             ( 9999991 , MSG                           )
    ##########################################################################
    SIDB   = SpinBox               ( None , self . PlanFunc                  )
    SIDB   . setRange              ( 0 , self . Total                        )
    SIDB   . setValue              ( self . StartId                          )
    SIDB   . setPrefix             ( "本頁開始:" )
    mm     . addWidget             ( 9999992 , SIDB                          )
    SIDB   . valueChanged . connect ( self . GotoId                          )
    ##########################################################################
    SIDP   = SpinBox               ( None , self . PlanFunc                  )
    SIDP   . setRange              ( 0 , 10000                               )
    SIDP   . setValue              ( self . Amount                           )
    SIDP   . setPrefix             ( "每頁數量:" )
    mm     . addWidget             ( 9999993 , SIDP                          )
    SIDP   . valueChanged . connect ( self . AssignAmount                    )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     . addAction             ( 1001 ,  TRX [ "UI::Refresh"           ] )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( len ( items ) == 1                    ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    mm     = self . ColumnsMenu    ( mm                                      )
    mm     = self . LocalityMenu   ( mm                                      )
    mm     . addSeparator          (                                         )
    mm     . addAction             ( 3001 ,  TRX [ "UI::TranslateAll"      ] )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      return True
    ##########################################################################
    if                             ( at >= 9000 ) and ( at <= 9007 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( items [ 0 ] , 0                         )
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Types" , uuid , NAM             )
      return True
    ##########################################################################
    if                             ( at == 3001                            ) :
      self . Go                    ( self . TranslateAll                     )
      return True
    ##########################################################################
    return True
##############################################################################
