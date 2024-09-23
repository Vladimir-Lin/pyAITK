# -*- coding: utf-8 -*-
##############################################################################
## GeocontourListings
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
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
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
##############################################################################
class GeocontourListings           ( TreeDock                              ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( dict                                    )
  emitAssignAmounts = pyqtSignal   ( str , int , int                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . ClassTag           = "GeocontourListings"
    self . EditAllNames       = None
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 8                                       )
    self . setColumnHidden         ( 6 , True                                )
    self . setColumnHidden         ( 7 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ## self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( False                                   )
    self . setAcceptDrops          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 800 , 240 )                       )
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    self . LinkAction ( "Select"     , self . SelectOne       , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                     ( self                                   ) :
    return self . defaultFocusIn  (                                          )
  ############################################################################
  def FocusOut                    ( self                                   ) :
    return self . defaultFocusOut (                                          )
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
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
    if                        ( column not in [ 0 , 3 , 4 , 5 ]            ) :
      return
    ##########################################################################
    line = self . setLineEdit ( item                                       , \
                                column                                     , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem           ( self , UUID , NAME , TYPE                    ) :
    ##########################################################################
    SXID = str              ( UUID % 1000                                    )
    UXID = str              ( UUID                                           )
    IT   = QTreeWidgetItem  (                                                )
    IT   . setText          ( 0 , NAME                                       )
    IT   . setToolTip       ( 0 , UXID                                       )
    IT   . setData          ( 0 , Qt . UserRole , UUID                       )
    IT   . setText          ( 1 , SXID                                       )
    IT   . setTextAlignment ( 1 , Qt.AlignRight                              )
    IT   . setText          ( 2 , UXID                                       )
    IT   . setTextAlignment ( 2 , Qt.AlignRight                              )
    IT   . setText          ( 3 , self . BlobToString ( TYPE [ 0 ] )         )
    IT   . setText          ( 4 , self . BlobToString ( TYPE [ 1 ] )         )
    IT   . setText          ( 5 , self . BlobToString ( TYPE [ 2 ] )         )
    IT   . setTextAlignment ( 6 , Qt.AlignRight                              )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot             (                                                    )
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
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
    if                           ( column in [ 0                         ] ) :
      ########################################################################
      self . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , msg , )                   )
    ##########################################################################
    if                           ( column in [ 3 , 4 , 5                 ] ) :
      ########################################################################
      self . Go                  ( self . AssureUuidColumn                 , \
                                   ( item , uuid , msg , column )            )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        dict                              )
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    NAMEs  = JSON                 [ "NAMEs"                                  ]
    TYPEs  = JSON                 [ "TYPEs"                                  ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U , NAMEs [ U ] , TYPEs [ U ]            )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( UUIDs )                            )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    self   . Notify               ( 5                                        )
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
  def ObtainsUuidNames                ( self , DB , UUIDs                  ) :
    ##########################################################################
    NAMEs   =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "Names"                              ]
      NAMEs = self . GetNames         ( DB , TABLE , UUIDs                   )
    ##########################################################################
    return NAMEs
  ############################################################################
  @pyqtSlot                           (        str  , int     , int          )
  def AssignAmounts                   ( self , UUID , Amounts , Column     ) :
    ##########################################################################
    IT    = self . uuidAtItem         ( UUID , 0                             )
    if                                ( IT is None                         ) :
      return
    ##########################################################################
    IT . setText                      ( Column , str ( Amounts )             )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                ( self , UUIDs                       ) :
    ##########################################################################
    time   . sleep                    ( 1.0                                  )
    ##########################################################################
    TABLE  = self . Tables            [ "Countries"                          ]
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      CNT  = 0
      TYPE = int                      ( UUID % 10000                         )
      QQ   = f"""select count(*) from {TABLE}
                  where ( `used` = 1 )
                  and ( `type` = {TYPE} ) ;"""
      CNT  = DB . GetOne              ( QQ , CNT                             )
      ########################################################################
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT , 6               )
    ##########################################################################
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( self . NotOkay ( DB )              ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . OnBusy        . emit    (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    TYPEs   =                         {                                      }
    TYPTAB  = self . Tables           [ "NationTypes"                        ]
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select
                  `name`,`comment`,`wiki`
                  from {TYPTAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      if ( ( RR is not False ) and ( RR is not None ) )                      :
        TYPEs [ UUID ] = RR
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax       . emit    (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "NAMEs" ] = NAMEs
    JSON [ "TYPEs" ] = TYPEs
    ##########################################################################
    self    . emitAllNames  . emit    ( JSON                                 )
    ##########################################################################
    if                                ( not self . isColumnHidden ( 1 )    ) :
      ########################################################################
      VAL   =                         ( UUIDs ,                              )
      self  . Go                      ( self . ReportBelongings , VAL        )
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
  def ObtainAllUuids             ( self , DB                               ) :
    ##########################################################################
    TABLE = self . Tables        [ "NationTypes"                             ]
    ##########################################################################
    QQ    = f"select `uuid` from {TABLE} order by `id` asc ;"
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
  def ObtainUuidsQuery    ( self                                           ) :
    ##########################################################################
    TABLE = self . Tables [ "NationTypes"                                    ]
    ##########################################################################
    return f"select `uuid` from {TABLE} order by `id` asc ;"
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 7                              )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem          ( self , item , uuid , name                  ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    NAMTAB = self . Tables    [ "NamesEditing"                               ]
    ##########################################################################
    DB     . LockWrites       ( [ NAMTAB                                   ] )
    ##########################################################################
    uuid   = int              ( uuid                                         )
    if                        ( uuid > 0                                   ) :
      self . AssureUuidName   ( DB , NAMTAB , uuid , name                    )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def AssureUuidColumn        ( self , item , uuid , name , column         ) :
    ##########################################################################
    try                                                                      :
      blob = name . encode    ( "utf-8"                                      )
    except                                                                   :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    TYPTAB = self . Tables    [ "NationTypes"                                ]
    COLN   = ""
    ##########################################################################
    if                        ( 3 == column                                ) :
      COLN = "name"
    elif                      ( 4 == column                                ) :
      COLN = "comment"
    elif                      ( 5 == column                                ) :
      COLN = "wiki"
    ##########################################################################
    DB     . LockWrites       ( [ TYPTAB                                   ] )
    ##########################################################################
    QQ     = f"""update {TYPTAB}
                 set `{COLN}` = %s
                 where ( `uuid` = {uuid} ) ;"""
    QQ     = " " . join       ( QQ . split (                               ) )
    DB     . QueryValues      ( QQ , ( blob , )                              )
    ##########################################################################
    DB     . Close            (                                              )
    self   . Notify           ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard ( False                                         )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 6                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9007 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      if                           ( ( at == 9006 ) and ( hid )            ) :
        ######################################################################
        self . restart             (                                         )
        ######################################################################
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
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    ##########################################################################
    if                             ( len ( items ) == 1                    ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ## mm     . addAction             ( 3001 ,  TRX [ "UI::TranslateAll"      ] )
    ## mm     . addSeparator          (                                         )
    ##########################################################################
    self   . ColumnsMenu           ( mm                                      )
    self   . LocalityMenu          ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      return True
    ##########################################################################
    if                             ( self . RunColumnsMenu     ( at )      ) :
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . restart               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( items [ 0 ] , 0                         )
      NAM  = self . Tables         [ "NamesEditing"                          ]
      self . EditAllNames          ( self , "NationTypes" , uuid , NAM       )
      return True
    ##########################################################################
    ## if                             ( at == 3001                            ) :
    ##   self . Go                    ( self . TranslateAll                     )
    ##   return True
    ##########################################################################
    return True
##############################################################################
