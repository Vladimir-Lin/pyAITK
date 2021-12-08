# -*- coding: utf-8 -*-
##############################################################################
## ObjectTypesEditor
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
class ObjectTypesEditor            ( TreeDock                              ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = pyqtSignal       (                                         )
  emitAllNames  = pyqtSignal       ( dict                                    )
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
    self . setColumnCount          ( 9                                       )
    self . setColumnHidden         ( 8 , True                                )
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
    if                          ( column not in [ 2 , 3 , 4 , 5 , 6 , 7 ]  ) :
      return
    ##########################################################################
    if                          ( column in [ 2 , 3 , 4 , 7 ]              ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      return
    ##########################################################################
    if                          ( column in [ 5 , 6 ]                      ) :
      ########################################################################
      IV   = 0
      AV   = 100
      ########################################################################
      if                        ( column == 5                              ) :
        ######################################################################
        AV = 18
      ########################################################################
      sb   = self . setSpinBox  ( item                                       ,
                                  column                                     ,
                                  IV                                         ,
                                  AV                                         ,
                                  "editingFinished"                          ,
                                  self . spinChanged                         )
      sb   . setAlignment       ( Qt . AlignRight                            )
      sb   . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                ( self , UUID , TYPE                      ) :
    ##########################################################################
    UXID = str                   ( UUID                                      )
    IT   = QTreeWidgetItem       (                                           )
    IT   . setFlags              ( IT . flags ( ) | Qt . ItemIsUserCheckable )
    IT   . setData               ( 0 , Qt . UserRole , UUID                  )
    ##########################################################################
    USED = TYPE                  [ 1                                         ]
    USED = int                   ( USED                                      )
    if                           ( USED == 0                               ) :
      IT . setCheckState         ( 0 , Qt . Unchecked                        )
    else                                                                     :
      IT . setCheckState         ( 0 , Qt . Checked                          )
    ##########################################################################
    IT   . setText               ( 1 , str ( TYPE [ 0 ] )                    )
    IT   . setTextAlignment      ( 1 , Qt.AlignRight                         )
    ##########################################################################
    NAME = self . BlobToString   ( TYPE [ 2 ]                                )
    IT   . setText               ( 2 , NAME                                  )
    ##########################################################################
    WIKI = self . BlobToString   ( TYPE [ 7 ]                                )
    IT   . setText               ( 3 , WIKI                                  )
    ##########################################################################
    HEAD = int                   ( TYPE [ 3 ]                                )
    IT   . setText               ( 4 , str ( HEAD )                          )
    IT   . setTextAlignment      ( 4 , Qt.AlignRight                         )
    ##########################################################################
    DIGS = int                   ( TYPE [ 4 ]                                )
    IT   . setText               ( 5 , str ( DIGS )                          )
    IT   . setTextAlignment      ( 5 , Qt.AlignRight                         )
    ##########################################################################
    READ = int                   ( TYPE [ 5 ]                                )
    IT   . setText               ( 6 , str ( READ )                          )
    IT   . setTextAlignment      ( 6 , Qt.AlignRight                         )
    ##########################################################################
    COMM = self . BlobToString   ( TYPE [ 6 ]                                )
    IT   . setText               ( 7 , COMM                                  )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 2 , 3 , 4 , 5 , 6 , 7 ]                     )
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
    na     = ""
    ##########################################################################
    if                           ( column == 2                             ) :
      ########################################################################
      na   = "name"
      ########################################################################
    elif                         ( column == 3                             ) :
      ########################################################################
      na   = "wiki"
      ########################################################################
    elif                         ( column == 4                             ) :
      ########################################################################
      na   = "head"
      if                         ( len ( msg ) not in [ 1 , 19 ]           ) :
        ######################################################################
        item . setText           ( column , text                             )
        self . removeParked      (                                           )
        ######################################################################
        return
      ########################################################################
      try                                                                    :
        hu = int                 ( msg                                       )
        ######################################################################
        if                       ( hu < 1000000000000000000                ) :
          if                     ( hu > 0                                  ) :
            item . setText       ( column , text                             )
            self . removeParked  (                                           )
            return
        ######################################################################
        if                       ( hu > 9223372000000000000                ) :
          item   . setText       ( column , text                             )
          self   . removeParked  (                                           )
          return
        ######################################################################
      except                                                                 :
        item     . setText       ( column , text                             )
        self     . removeParked  (                                           )
        return
      ########################################################################
      item . setText             ( column , msg                              )
      self . removeParked        (                                           )
      ########################################################################
      self . Go                  ( self . UpdateTypeItemValue              , \
                                   ( uuid , na , hu , )                      )
      ########################################################################
      return
    elif                         ( column == 7                             ) :
      ########################################################################
      na   = "comment"
    ##########################################################################
    if                           ( len ( na ) > 0                          ) :
      ########################################################################
      item . setText             ( column ,              msg                 )
      ########################################################################
      self . Go                  ( self . UpdateTypeItemBlob               , \
                                   ( uuid , na , msg , )                     )
    ##########################################################################
    self   . removeParked        (                                           )
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
    v      = self . CurrentItem [ "Value"                                    ]
    v      = int                ( v                                          )
    nv     = sb   . value       (                                            )
    uuid   = self . itemUuid    ( item , 0                                   )
    ##########################################################################
    if                          ( v != nv                                  ) :
      ########################################################################
      na   = ""
      ########################################################################
      item . setText            ( column , str ( nv )                        )
      ########################################################################
      if                        ( column == 5                              ) :
        na = "digits"
      elif                      ( column == 6                              ) :
        na = "ready"
      ########################################################################
      if                        ( len ( na ) > 0                           ) :
        self . Go               ( self . UpdateTypeItemValue               , \
                                  ( uuid , na , nv , )                       )
    ##########################################################################
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
    self   . clear                   (                                       )
    ##########################################################################
    UUIDs  = JSON                    [ "UUIDs"                               ]
    TYPEs  = JSON                    [ "TYPEs"                               ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem      ( U , TYPEs [ U ]                       )
      self . addTopLevelItem         ( IT                                    )
    ##########################################################################
    FMT    = self . getMenuItem      ( "DisplayTotal"                        )
    MSG    = FMT  . format           ( len ( UUIDs )                         )
    self   . setToolTip              ( MSG                                   )
    ##########################################################################
    self   . emitNamesShow . emit    (                                       )
    ##########################################################################
    TOTAL  = self . columnCount      (                                       )
    self   . resizeColumnsToContents ( range ( 0 , TOTAL - 1 )               )
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
  def ObtainsUuidTypes                ( self , DB , UUIDs                  ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return                          {                                      }
    ##########################################################################
    TYPEs   =                         {                                      }
    TYPTAB  = self . Tables           [ "Types"                              ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select
                  `id`,`used`,`name`,`head`,`digits`,`ready`,`comment`,`wiki`
                  from {TYPTAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( ( RR is not False ) and ( RR is not None ) )                      :
        TYPEs [ UUID ] = RR
    ##########################################################################
    return TYPEs
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
    TYPEs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      TYPEs = self . ObtainsUuidTypes ( DB , UUIDs                           )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "TYPEs" ] = TYPEs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
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
    TYPTAB = self . Tables  [ "Types"                                        ]
    ##########################################################################
    QQ     = f"""select `uuid` from {TYPTAB}
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
  def UpdateTypeItemValue          ( self , uuid , item , value            ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TYPTAB  = self . Tables        [ "Types"                                 ]
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
    TYPTAB  = self . Tables        [ "Types"                                 ]
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
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Copy"       , self . RenameItem      , False   )
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
    TYPTAB = self . Tables [ "Types"                                         ]
    ##########################################################################
    QQ     = f"select count(*) from {TYPTAB} where ( `used` = 1 ) ;"
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
    TABLE   = self . Tables          [ "Types"                               ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . getSortingOrder (                                       )
    ##########################################################################
    QQ      = f"""select `uuid` from {TABLE}
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join                ( QQ . split ( )                        )
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    ## self   . setColumnWidth   ( 0 , 24                                       )
    self   . setColumnWidth   ( 8 , 3                                        )
    ##########################################################################
    TRX    = self . Translations
    LABELs = TRX              [ "ObjectTypesEditor" ] [ "Labels"             ]
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
    if                             ( at >= 9001 ) and ( at <= 9008 )         :
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
      self . EditAllNames           ( self , "Types" , uuid , NAM            )
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      self . Go                     ( self . TranslateAll                    )
      return True
    ##########################################################################
    return True
##############################################################################
