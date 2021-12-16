# -*- coding: utf-8 -*-
##############################################################################
## CelestialListings
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
##############################################################################
class CelestialListings            ( TreeDock                              ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( list                                    )
  emitAssignAmounts = pyqtSignal   ( str , int                               )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . CKEY               = "CelestialListings"
    self . EditAllNames       = None
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 35
    self . Active             = True
    self . Usage              = 1
    self . SortOrder          = "asc"
    self . Method             = "Original"
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 9                                       )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 3 , True                                )
    self . setColumnHidden         ( 4 , True                                )
    self . setColumnHidden         ( 7 , True                                )
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
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 800 , 640 )                       )
  ############################################################################
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"      , self . windowTitle ( )            )
    self . LinkAction     ( "Refresh"    , self . startup                    )
    ##########################################################################
    self . LinkAction     ( "Rename"     , self . RenameItem                 )
    self . LinkAction     ( "Copy"       , self . CopyToClipboard            )
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
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
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
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in [ 1 , 2 , 3 , 5 , 6 ]     ) :
      return
    ##########################################################################
    if                           ( column     in [     2             ]     ) :
      ########################################################################
      LL   = self . Translations [ self . CKEY ] [ "Used"                    ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . usageChanged                       )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column     in [ 1 ,         5 , 6 ]     ) :
      ########################################################################
      line = self . setLineEdit  ( item                                    , \
                                   column                                  , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
      ########################################################################
      return
    ##########################################################################
    if                           ( column     in [         3         ]     ) :
      ########################################################################
      sb   = self . setSpinBox   ( item                                      ,
                                   column                                    ,
                                   0                                         ,
                                   99                                        ,
                                   "editingFinished"                         ,
                                   self . typeChanged                        )
      sb   . setAlignment        ( Qt . AlignRight                           )
      sb   . setFocus            ( Qt . TabFocusReason                       )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                 ( self , JSON                            ) :
    ##########################################################################
    USAGE   = self . Translations [ self . CKEY ] [ "Used"                   ]
    UUID    = JSON                [ "Uuid"                                   ]
    ID      = JSON                [ "Id"                                     ]
    USED    = JSON                [ "Used"                                   ]
    TYPE    = JSON                [ "Type"                                   ]
    PARENT  = JSON                [ "Parent"                                 ]
    PNAME   = JSON                [ "PName"                                  ]
    ENGLISH = JSON                [ "English"                                ]
    COMMENT = JSON                [ "Comment"                                ]
    NAME    = JSON                [ "Name"                                   ]
    UXID    = str                 ( JSON [ "Uuid" ]                          )
    ##########################################################################
    IT      = QTreeWidgetItem     (                                          )
    ##########################################################################
    IT      . setText             ( 0 , str ( ID )                           )
    IT      . setToolTip          ( 0 , UXID                                 )
    IT      . setData             ( 0 , Qt . UserRole , UXID                 )
    IT      . setTextAlignment    ( 0 , Qt.AlignRight                        )
    ##########################################################################
    IT      . setText             ( 1 , NAME                                 )
    IT      . setToolTip          ( 1 , UXID                                 )
    ##########################################################################
    IT      . setText             ( 2 , USAGE [ str ( USED ) ]               )
    IT      . setToolTip          ( 2 , UXID                                 )
    IT      . setData             ( 2 , Qt . UserRole , USED                 )
    ##########################################################################
    IT      . setText             ( 3 , str ( TYPE )                         )
    IT      . setTextAlignment    ( 3 , Qt.AlignRight                        )
    IT      . setData             ( 3 , Qt . UserRole , TYPE                 )
    ##########################################################################
    IT      . setText             ( 4 , PNAME                                )
    ##########################################################################
    IT      . setText             ( 5 , ENGLISH                              )
    IT      . setText             ( 6 , COMMENT                              )
    ##########################################################################
    IT      . setData             ( 8 , Qt . UserRole , JSON                 )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 1 , 2 , 3 , 5 , 6                         ] )
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
    if                           ( len ( msg ) <= 0                        ) :
      self . removeTopLevelItem  ( item                                      )
      return
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    if                           ( column in [ 1 ]                         ) :
      ########################################################################
      self . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , msg , )                   )
      ########################################################################
    elif                         ( column in [ 5 , 6 ]                     ) :
      ########################################################################
      self . Go                  ( self . UpdateColumnValue                , \
                                   ( item , uuid , column , msg , )          )
    ##########################################################################
    return
  ############################################################################
  def usageChanged               ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    cb     = self . CurrentItem  [ "Widget"                                  ]
    cbv    = self . CurrentItem  [ "Value"                                   ]
    index  = cb   . currentIndex (                                           )
    value  = cb   . itemData     ( index                                     )
    uuid   = item . data         ( 0 , Qt . UserRole                         )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      LL   = self . Translations [ self . CKEY ] [ "Used"                    ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      self . Go                  ( self . UpdateColumnNumber               , \
                                   ( item , uuid , "used" , value , )        )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def typeChanged               ( self                                     ) :
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
    uuid   = item . data         ( 0 , Qt . UserRole                         )
    ##########################################################################
    if                          ( v != nv                                  ) :
      ########################################################################
      item . setText            ( column , str ( nv )                        )
      ########################################################################
      self . Go                 ( self . UpdateColumnNumber                , \
                                  ( item , uuid , "type" , nv , )            )
    ##########################################################################
    self . removeParked         (                                            )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , LISTS                           ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for JSON in LISTS                                                        :
      ########################################################################
      IT   = self . PrepareItem   ( JSON                                     )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( LISTS )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    if                            ( self . Method in [ "Searching" ]       ) :
      ########################################################################
      T    = self . Translations  [ self . CKEY ] [ "Title"                  ]
      K    = self . SearchKey
      T    = f"{T}:{K}"
      ########################################################################
      self . setWindowTitle       ( T                                        )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                (        str  , int                               )
  def AssignAmounts        ( self , UUID , Amounts                         ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT in [ False , None ]                        ) :
      return
    ##########################################################################
    IT . setText           ( 7 , str ( Amounts )                             )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                ( self , UUIDs                       ) :
    ##########################################################################
    time   . sleep                    ( 1.0                                  )
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Celestial"                          )
    REL    . setT2                    ( "Star"                               )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL  . set                      ( "first" , UUID                       )
      CNT  = REL . CountSecond        ( DB , RELTAB                          )
      ########################################################################
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT                   )
    ##########################################################################
    DB     . Close                    (                                      )
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
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    LISTs   =                         [                                      ]
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    NAMEs   =                         [                                      ]
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    CLTTAB  = self . Tables           [ "Celestials"                         ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select
                  `id`,`used`,`type`,`parent`,`name`,`comment`
                  from {CLTTAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 6 ) )          :
        ######################################################################
        J               =             {                                      }
        J   [ "Uuid"    ] = int       ( UUID                                 )
        J   [ "Id"      ] = int       ( RR [ 0 ]                             )
        J   [ "Used"    ] = int       ( RR [ 1 ]                             )
        J   [ "Type"    ] = int       ( RR [ 2 ]                             )
        J   [ "Parent"  ] = int       ( RR [ 3 ]                             )
        J   [ "English" ] = self . assureString ( RR [ 4 ]                   )
        J   [ "Comment" ] = self . assureString ( RR [ 5 ]                   )
        J   [ "Name"    ] = NAMEs     [ UUID                                 ]
        J   [ "PName"   ] = ""
        ######################################################################
        if                            ( J [ "Parent" ] in NAMEs            ) :
          J [ "PName"   ] = NAMEs     [ J [ "Parent" ]                       ]
        ######################################################################
        LISTs          . append       ( J                                    )
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
    if                                ( not self . isColumnHidden ( 7 )    ) :
      self . Go                       ( self . ReportBelongings            , \
                                        ( UUIDs , )                          )
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
  def ObtainAllUuids        ( self , DB                                    ) :
    ##########################################################################
    USAGE  = self . Usage
    CLTTAB = self . Tables  [ "Celestials"                                   ]
    ##########################################################################
    if                      ( self . Active                                ) :
      QQ   = f"""select `uuid` from {CLTTAB}
                 where ( `used` = {USAGE} )
                 order by `id` asc ;"""
    else                                                                     :
      QQ   = f"""select `uuid` from {CLTTAB}
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
    TABLE = self . Tables       [ "NamesEditing"                             ]
    FMT   = self . Translations [ "UI::Translating"                          ]
    self  . DoTranslateAll      ( DB , TABLE , FMT , 15.0                    )
    ##########################################################################
    DB    . Close               (                                            )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation   ( self , DB                                     ) :
    ##########################################################################
    self   . Total = 0
    USAGE  = self . Usage
    ##########################################################################
    CLTTAB = self . Tables [ "Celestials"                                    ]
    ##########################################################################
    if                     ( self . Active                                 ) :
      QQ   = f"select count(*) from {CLTTAB} where ( `used` = {USAGE} ) ;"
    else                                                                     :
      QQ   = f"select count(*) from {CLTTAB} ;"
    DB     . Query                   ( QQ                                    )
    RR     = DB . FetchOne (                                                 )
    ##########################################################################
    if ( not RR ) or ( RR is None ) or ( len ( RR ) <= 0 )                   :
      return
    ##########################################################################
    self   . Total = RR    [ 0                                               ]
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    CLTTAB = self . Tables          [ "Celestials"                           ]
    STID   = self . StartId
    AMOUNT = self . Amount
    USAGE  = self . Usage
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    if                              ( self . Active                        ) :
      QQ   = f"""select `uuid` from {CLTTAB}
                 where ( `used` = {USAGE} )
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    else                                                                     :
      QQ   = f"""select `uuid` from {CLTTAB}
                 order by `id` {ORDER}
                 limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "celestial/uuids"
    message = self . getMenuItem ( "TotalPicked"                             )
    ##########################################################################
    return self . CreateDragMime ( self , 0 , mtype , message                )
  ############################################################################
  def startDrag         ( self , dropActions                               ) :
    ##########################################################################
    self . StartingDrag (                                                    )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "celestial/uuids;stellar/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                        ( self                                , \
                                       source                              , \
                                       mimeData                            , \
                                       mousePos                            ) :
    ##########################################################################
    RDN    = self . RegularDropNew   ( mimeData                              )
    if                               ( not RDN                             ) :
      return False
    ##########################################################################
    mtype  = self   . DropInJSON     [ "Mime"                                ]
    UUIDs  = self   . DropInJSON     [ "UUIDs"                               ]
    atItem = self   . itemAt         ( mousePos                              )
    title  = source . windowTitle    (                                       )
    CNT    = len                     ( UUIDs                                 )
    ##########################################################################
    if                               ( atItem in [ False , None ]          ) :
      return False
    ##########################################################################
    if                               ( mtype in [ "celestial/uuids"      ] ) :
      self . ShowMenuItemMessage     ( "AssignParent"                        )
    elif                             ( mtype in [ "stellar/uuids"        ] ) :
      self . ShowMenuItemTitleStatus ( "StarsFrom" , title , CNT             )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving               ( self , source , mimeData , mousePos       ) :
    ##########################################################################
    if                         ( self . droppingAction                     ) :
      return False
    ##########################################################################
    atItem = self . itemAt     ( mousePos                                    )
    ##########################################################################
    if                         ( atItem in [ False , None ]                ) :
      return False
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    mtype  = self . DropInJSON [ "Mime"                                      ]
    UUIDs  = self . DropInJSON [ "UUIDs"                                     ]
    ##########################################################################
    if                         ( mtype in [ "celestial/uuids" ]            ) :
      ########################################################################
      if                       ( int ( UUID ) == int ( UUIDs [ 0 ] )       ) :
        return False
    ##########################################################################
    return True
  ############################################################################
  def acceptCelestialsDrop ( self                                          ) :
    return True
  ############################################################################
  def acceptStellarsDrop   ( self                                          ) :
    return True
  ############################################################################
  def dropCelestials       ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( atItem in [ False , None ]                    ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( 0 , Qt . UserRole                               )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    self . Go              ( self . AssignCelestialParent                  , \
                             ( UUID , UUIDs , )                              )
    ##########################################################################
    return True
  ############################################################################
  def dropStellars         ( self , source , pos , JSOX                    ) :
    ##########################################################################
    if                     ( "UUIDs" not in JSOX                           ) :
      return True
    ##########################################################################
    UUIDs  = JSOX          [ "UUIDs"                                         ]
    if                     ( len ( UUIDs ) <= 0                            ) :
      return True
    ##########################################################################
    atItem = self . itemAt ( pos                                             )
    if                     ( atItem in [ False , None ]                    ) :
      return True
    ##########################################################################
    UUID   = atItem . data ( 0 , Qt . UserRole                               )
    UUID   = int           ( UUID                                            )
    ##########################################################################
    if                     ( UUID <= 0                                     ) :
      return True
    ##########################################################################
    self   . Go            ( self . AppendingStellars , ( UUID , UUIDs , )   )
    ##########################################################################
    return True
  ############################################################################
  def AssignCelestialParent          ( self , UUID , UUIDs                 ) :
    ##########################################################################
    if                               ( UUID <= 0                           ) :
      return
    ##########################################################################
    COUNT  = len                     ( UUIDs                                 )
    if                               ( COUNT <= 0                          ) :
      return
    ##########################################################################
    DB     = self . ConnectDB        (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    PARENT = UUIDs                   [ 0                                     ]
    CLTTAB = self . Tables           [ "Celestials"                          ]
    NAMTAB = self . Tables           [ "Names"                               ]
    DB     . LockWrites              ( [ CLTTAB                            ] )
    ##########################################################################
    QQ     = f"""update {CLTTAB}
                  set `parent` = {PARENT}
                  where ( `uuid` = {UUID} ) ;"""
    QQ     = " " . join              ( QQ . split ( )                        )
    DB     . Query                   ( QQ                                    )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    NAME   = self . GetName          ( DB , NAMTAB , PARENT                  )
    ##########################################################################
    DB     . Close                   (                                       )
    self   . Notify                  ( 5                                     )
    self   . ShowStatus              ( ""                                    )
    ##########################################################################
    IT     = self . uuidAtItem       ( UUID , 0                              )
    if                               ( IT in [ False , None ]              ) :
      return
    ##########################################################################
    self   . emitAssignColumn . emit ( IT , 4 , NAME                         )
    ##########################################################################
    return
  ############################################################################
  def AppendingStellars              ( self , UUID , UUIDs                 ) :
    ##########################################################################
    COUNT  = len                     ( UUIDs                                 )
    if                               ( COUNT <= 0                          ) :
      return
    ##########################################################################
    DB     = self . ConnectDB        (                                       )
    if                               ( DB == None                          ) :
      return
    ##########################################################################
    self   . OnBusy  . emit          (                                       )
    self   . setBustle               (                                       )
    FMT    = self . getMenuItem      ( "JoinStars"                           )
    MSG    = FMT  . format           ( COUNT                                 )
    self   . ShowStatus              ( MSG                                   )
    self   . TtsTalk                 ( MSG , 1002                            )
    ##########################################################################
    RELTAB = self . Tables           [ "RelationStars"                       ]
    DB     . LockWrites              ( [ RELTAB                            ] )
    ##########################################################################
    REL    = Relation                (                                       )
    REL    . set                     ( "first" , UUID                        )
    REL    . setT1                   ( "Celestial"                           )
    REL    . setT2                   ( "Star"                                )
    REL    . setRelation             ( "Subordination"                       )
    REL    . Joins                   ( DB , RELTAB , UUIDs                   )
    TOTAL  = REL . CountSecond       ( DB , RELTAB                           )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    ##########################################################################
    self   . setVacancy              (                                       )
    self   . GoRelax . emit          (                                       )
    DB     . Close                   (                                       )
    ##########################################################################
    self   . emitAssignColumn . emit ( IT , 7 , str ( TOTAL )                )
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . CKEY , 8                                  )
    self . setColumnWidth ( 2 , 100                                          )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
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
    self   . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    item   . setData          ( 0 , Qt . UserRole , uuid                     )
    ##########################################################################
    return
  ############################################################################
  def UpdateColumnValue       ( self , item , uuid , column , name         ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    CLTTAB = self . Tables    [ "Celestials"                                 ]
    ##########################################################################
    DB     . LockWrites       ( [ CLTTAB                                   ] )
    ##########################################################################
    ITEM   = ""
    if                        ( column == 5                                ) :
      ITEM = "name"
    elif                      ( column == 6                                ) :
      ITEM = "comment"
    ##########################################################################
    QQ     = f"""update {CLTTAB}
                 set `{ITEM}` = %s
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . QueryValues      ( QQ , ( name , )                              )
    ##########################################################################
    DB     . Close            (                                              )
    ##########################################################################
    return
  ############################################################################
  def UpdateColumnNumber      ( self , item , uuid , column , value        ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    CLTTAB = self . Tables    [ "Celestials"                                 ]
    ##########################################################################
    DB     . LockWrites       ( [ CLTTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {CLTTAB}
                 set `{column}` = {value}
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split ( )                               )
    DB     . Query            ( QQ                                           )
    ##########################################################################
    DB     . Close            (                                              )
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
    return self . DefaultColumnsMenu (        mm , 0                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9000 ) and ( at <= 9008 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      if                           ( ( at == 9007 ) and ( hid )            ) :
        ######################################################################
        self . clear               (                                         )
        self . startup             (                                         )
        ######################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def FiltersMenu                ( self , mm                               ) :
    ##########################################################################
    IBASE = 1782101
    BASE  = 1782110
    ##########################################################################
    msg   = self . getMenuItem   ( "FilterUsage"                             )
    COL   = mm   . addMenu       ( msg                                       )
    ##########################################################################
    msg   = self . getMenuItem   ( "ActiveFilters"                           )
    mm    . addActionFromMenu    ( COL , IBASE , msg , True , self . Active  )
    mm    . addSeparatorFromMenu ( COL                                       )
    ##########################################################################
    ITEMs = self  . Translations [ self . CKEY ] [ "Used"                    ]
    KEYs  = ITEMs . keys         (                                           )
    ##########################################################################
    for i in KEYs                                                            :
      ########################################################################
      v   = int                  ( i                                         )
      msg = ITEMs                [ i                                         ]
      hid =                      ( v == self . Usage                         )
      mm  . addActionFromMenu    ( COL , BASE + v , msg , True , hid         )
    ##########################################################################
    return mm
  ############################################################################
  def RunFiltersMenu   ( self , at                                         ) :
    ##########################################################################
    if                 ( at == 1782101                                     ) :
      ########################################################################
      if               ( self . Active                                     ) :
        self . Active = False
      else                                                                   :
        self . Active = True
      ########################################################################
      return True
    ##########################################################################
    BASE = 1782110
    if                 ( at < BASE                                         ) :
      return False
    ##########################################################################
    if                 ( at > ( BASE + 10 )                                ) :
      return False
    ##########################################################################
    ID           = int ( at - BASE                                           )
    self . Usage = ID
    ##########################################################################
    return True
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
    if                              ( atItem != None                       ) :
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
    if                              ( self . Method not in [ "Original" ]  ) :
      ########################################################################
      msg  = self . getMenuItem     ( "Original"                             )
      mm   . addAction              ( 1002 , msg                             )
    ##########################################################################
    self   . AppendRenameAction     ( mm , 1101                              )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      ########################################################################
      if                            ( self . EditAllNames != None          ) :
        ######################################################################
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
    ##########################################################################
    mm     . addAction              ( 3001 ,  TRX [ "UI::TranslateAll"     ] )
    mm     . addSeparator           (                                        )
    ##########################################################################
    mm     = self . FiltersMenu     ( mm                                     )
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . SortingMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
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
    if                              ( self . RunSortingMenu     ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunFiltersMenu     ( at )     ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu     ( at )     ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1002                           ) :
      ########################################################################
      self . Method = "Original"
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      ########################################################################
      self . RenameItem             (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      uuid = self . itemUuid        ( items [ 0 ] , 0                        )
      NAM  = self . Tables          [ "Names"                                ]
      self . EditAllNames           ( self , "Tasks" , uuid , NAM            )
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      self . Go                     ( self . TranslateAll                    )
      return True
    ##########################################################################
    return True
##############################################################################
