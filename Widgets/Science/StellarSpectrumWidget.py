# -*- coding: utf-8 -*-
##############################################################################
## WebPageListings
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
from   PyQt5 . QtCore                 import QUrl
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QDesktopServices
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
class StellarSpectrumWidget     ( TreeDock                                 ) :
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
    self . Catalogues         =    { 0 : True                              , \
                                     1 : True                              , \
                                     2 : True                              , \
                                     3 : True                              , \
                                     4 : True                              , \
                                     5 : True                                }
    self . Spectrums          =    { "Display"     : [ ]                   , \
                                     "Listings"    : { }                   , \
                                     "Information" : { }                     }
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 8                                       )
    self . setColumnHidden         ( 0 , True                                )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnHidden         ( 2 , True                                )
    self . setColumnHidden         ( 5 , True                                )
    self . setColumnHidden         ( 6 , True                                )
    self . setColumnHidden         ( 7 , True                                )
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
    return self . SizeSuggestion   ( QSize ( 400 , 640 )                     )
  ############################################################################
  def FocusIn                      ( self                                  ) :
    ##########################################################################
    if                             ( not self . isPrepared ( )             ) :
      return False
    ##########################################################################
    self . setActionLabel          ( "Label"      , self . windowTitle ( )   )
    self . LinkAction              ( "Refresh"    , self . startup           )
    ##########################################################################
    self . LinkAction              ( "Rename"     , self . RenameItem        )
    self . LinkAction              ( "Copy"       , self . CopyToClipboard   )
    ##########################################################################
    self . LinkAction              ( "Home"       , self . PageHome          )
    self . LinkAction              ( "End"        , self . PageEnd           )
    self . LinkAction              ( "PageUp"     , self . PageUp            )
    self . LinkAction              ( "PageDown"   , self . PageDown          )
    ##########################################################################
    self . LinkAction              ( "SelectAll"  , self . SelectAll         )
    self . LinkAction              ( "SelectNone" , self . SelectNone        )
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
  def doubleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 1 , 4 , 5 , 6 ]            ) :
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
  def PrepareItemContent           ( self , item , JSON                    ) :
    ##########################################################################
    ID          = JSON             [ "Id"                                    ]
    UUID        = JSON             [ "Uuid"                                  ]
    TYPE        = JSON             [ "Type"                                  ]
    PARENT      = JSON             [ "Parent"                                ]
    UXID        = str              ( UUID                                    )
    DESCRIPTION = JSON             [ "Description"                           ]
    NAME        = JSON             [ "Name"                                  ]
    COMMENT     = JSON             [ "Comment"                               ]
    WIKI        = JSON             [ "Wiki"                                  ]
    ##########################################################################
    PNAME       = ""
    PTIPS       = ""
    ##########################################################################
    if                             ( PARENT > 0                            ) :
      ########################################################################
      if ( PARENT in self . Spectrums [ "Listings" ] )                       :
        ######################################################################
        PNAME   = self . Spectrums [ "Listings" ] [ PARENT ] [ "Name"        ]
        PTIPS   = self . Spectrums [ "Listings" ] [ PARENT ] [ "Description" ]
    ##########################################################################
    item        . setText          ( 0 , str ( ID )                          )
    item        . setTextAlignment ( 0 , Qt . AlignRight                     )
    item        . setToolTip       ( 0 , UXID                                )
    item        . setData          ( 0 , Qt . UserRole , UXID                )
    ##########################################################################
    item        . setText          ( 1 , DESCRIPTION                         )
    item        . setToolTip       ( 1 , UXID                                )
    ##########################################################################
    item        . setText          ( 2 , str ( TYPE )                        )
    item        . setData          ( 2 , Qt . UserRole , TYPE                )
    ##########################################################################
    item        . setText          ( 3 , PNAME                               )
    item        . setToolTip       ( 3 , PTIPS                               )
    item        . setData          ( 3 , Qt . UserRole , PARENT              )
    ##########################################################################
    item        . setText          ( 4 , NAME                                )
    item        . setText          ( 5 , COMMENT                             )
    item        . setText          ( 6 , WIKI                                )
    ##########################################################################
    item        . setData          ( 7 , Qt . UserRole , JSON                )
    ##########################################################################
    return item
  ############################################################################
  def PrepareItem                    ( self , JSON                         ) :
    return self . PrepareItemContent ( QTreeWidgetItem ( ) , JSON            )
  ############################################################################
  @pyqtSlot                  (                                               )
  def RenameItem             ( self                                        ) :
    ##########################################################################
    self . defaultRenameItem ( [ 1 , 4 , 5 , 6                             ] )
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
    uuid   = self . itemUuid    ( item   , 0                                 )
    item   . setText            ( column , msg                               )
    ##########################################################################
    self   . removeParked       (                                            )
    VAL    =                    ( item , uuid , column , msg ,               )
    self   . Go                 ( self . UpdateItem , VAL                    )
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
    self   . emitNamesShow . emit (                                          )
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
  def ObtainsUuidNames        ( self , DB , UUIDs                          ) :
    ##########################################################################
    NAMEs   =                 {                                              }
    ##########################################################################
    if                        ( len ( UUIDs ) > 0                          ) :
      TABLE = self . Tables   [ "NamesEditing"                               ]
      NAMEs = self . GetNames ( DB , TABLE , UUIDs                           )
    ##########################################################################
    return NAMEs
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    SSWTAB  = self . Tables           [ "StellarSpectrum"                    ]
    LISTS   =                         [                                      ]
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    self    . Spectrums =             { "Display"     : [ ]                , \
                                        "Listings"    : { }                , \
                                        "Information" : { }                  }
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select
                  `id`,`uuid`,`type`,`parent`,`name`,`comment`,`wiki`
                  from {SSWTAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 7 ) )          :
        ######################################################################
        J   = { "Id"          : int   ( RR [ 0 ]                         ) , \
                "Uuid"        : int   ( RR [ 1 ]                         ) , \
                "Description" : NAMEs [ UUID                             ] , \
                "Type"        : int   ( RR [ 2 ]                         ) , \
                "Parent"      : int   ( RR [ 3 ]                         ) , \
                "Name"        : self . assureString ( RR [ 4 ]           ) , \
                "Comment"     : self . assureString ( RR [ 5 ]           ) , \
                "Wiki"        : self . assureString ( RR [ 6 ]           )   }
        ID  = J                       [ "Id"                                 ]
        self  . Spectrums [ "Listings" ] [ UUID ] = J
        ######################################################################
        DISPLAY   = False
        ######################################################################
        if                            ( ( ID > 1000 ) and ( ID < 2999 )    ) :
          DISPLAY = self . Catalogues [ 0                                    ]
        elif                          ( ( ID > 3000 ) and ( ID < 3999 )    ) :
          DISPLAY = self . Catalogues [ 1                                    ]
        elif                          ( ( ID > 5000 ) and ( ID < 5999 )    ) :
          DISPLAY = self . Catalogues [ 2                                    ]
        elif                          ( ( ID > 4000 ) and ( ID < 4999 )    ) :
          DISPLAY = self . Catalogues [ 3                                    ]
        elif                          ( ( ID > 6000 ) and ( ID < 6999 )    ) :
          DISPLAY = self . Catalogues [ 4                                    ]
        elif                          ( ( ID > 7000 ) and ( ID < 7999 )    ) :
          DISPLAY = self . Catalogues [ 5                                    ]
        ######################################################################
        if                            ( DISPLAY                            ) :
          self  . Spectrums [ "Display" ] . append ( J                       )
          LISTS . append              ( J                                    )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( LISTS ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames  . emit     ( LISTS                                )
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
    SSWTAB = self . Tables  [ "StellarSpectrum"                              ]
    ##########################################################################
    QQ     = f"select `uuid` from {SSWTAB} order by `id` asc ;"
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
  def ObtainsInformation   ( self , DB                                     ) :
    ##########################################################################
    self   . Total = 0
    ##########################################################################
    SSWTAB = self . Tables [ "StellarSpectrum"                               ]
    ##########################################################################
    QQ     = f"select count(*) from {SSWTAB} ;"
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
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    SSWTAB = self . Tables [ "StellarSpectrum"                               ]
    ##########################################################################
    QQ     = f"""select `uuid` from {SSWTAB} order by `id` asc ;"""
    ##########################################################################
    return " " . join      ( QQ . split ( )                                  )
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self   . setColumnWidth      ( 7 , 3                                     )
    ##########################################################################
    LABELs = self . Translations [ "StellarSpectrumWidget" ] [ "Labels"      ]
    self   . setCentralLabels    ( LABELs                                    )
    ##########################################################################
    self   . setPrepared         ( True                                      )
    ##########################################################################
    return
  ############################################################################
  def UpdateItem                   ( self , item , uuid , column , name    ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    SSWTAB  = self . Tables        [ "StellarSpectrum"                       ]
    NAMTAB  = self . Tables        [ "NamesEditing"                          ]
    ##########################################################################
    DB      . LockWrites           ( [ SSWTAB , NAMTAB                     ] )
    ##########################################################################
    uuid    = int                  ( uuid                                    )
    ##########################################################################
    if                             ( column in [ 4 , 5 , 6 ]               ) :
      ########################################################################
      if                           ( column == 4                           ) :
        ######################################################################
        QQ  = f"""update {SSWTAB}
                  set `name` = %s
                  where ( `uuid` = {uuid} ) ;"""
        ######################################################################
      elif                         ( column == 5                           ) :
        ######################################################################
        QQ  = f"""update {SSWTAB}
                  set `comment` = %s
                  where ( `uuid` = {uuid} ) ;"""
        ######################################################################
      elif                         ( column == 6                           ) :
        ######################################################################
        QQ  = f"""update {SSWTAB}
                  set `wiki` = %s
                  where ( `uuid` = {uuid} ) ;"""
      ########################################################################
      QQ    = " " . join           ( QQ . split ( )                          )
      DB    . QueryValues          ( QQ , ( name , )                         )
      ########################################################################
    else                                                                     :
      ########################################################################
      if                           ( column == 1                           ) :
        ######################################################################
        self . AssureUuidName      ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
    self    . Notify               ( 5                                       )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def CataloguesMenu                 ( self , mm                           ) :
    ##########################################################################
    TRX   = self . Translations      [ "StellarSpectrumWidget"               ]
    msg   = self . getMenuItem       ( "Catalogues"                          )
    CAT   = mm   . addMenu           ( msg                                   )
    ##########################################################################
    KEYs  = self . Catalogues . keys (                                       )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      hid = self . Catalogues        [ K                                     ]
      msg = TRX                      [ "Catalogues" ] [ str ( K )            ]
      mm  . addActionFromMenu        ( CAT , 9210 + K , msg , True , hid     )
    ##########################################################################
    return mm
  ############################################################################
  def RunCataloguesMenu            ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9210 ) and ( at <= 9250 )         :
      ########################################################################
      col  = at - 9210
      ########################################################################
      if                           ( self . Catalogues [ col ]             ) :
        self . Catalogues [ col ] = False
      else                                                                   :
        self . Catalogues [ col ] = True
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9000 ) and ( at <= 9007 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
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
    if                              ( atItem != None                       ) :
      uuid = atItem . data          ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
    ##########################################################################
    mm     = MenuManager            ( self                                   )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction    ( mm , 1001                              )
    if                              ( atItem not in [ False , None ]       ) :
      self . AppendRenameAction     ( mm , 1101                              )
    ##########################################################################
    mm     . addSeparator           (                                        )
    ##########################################################################
    if                              ( atItem not in [ False , None ]       ) :
      if                            ( self . EditAllNames != None          ) :
        mm . addAction              ( 1601 ,  TRX [ "UI::EditNames" ]        )
    ##########################################################################
    mm     . addAction              ( 3001 ,  TRX [ "UI::TranslateAll"     ] )
    mm     . addSeparator           (                                        )
    mm     = self . CataloguesMenu  ( mm                                     )
    mm     = self . ColumnsMenu     ( mm                                     )
    mm     = self . LocalityMenu    ( mm                                     )
    self   . DockingMenu            ( mm                                     )
    ##########################################################################
    mm     . setFont                ( self    . font ( )                     )
    aa     = mm . exec_             ( QCursor . pos  ( )                     )
    at     = mm . at                ( aa                                     )
    ##########################################################################
    if                              ( self . RunDocking   ( mm , aa )      ) :
      return True
    ##########################################################################
    if                              ( self . RunCataloguesMenu ( at )      ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( self . RunColumnsMenu    ( at )      ) :
      return True
    ##########################################################################
    if                              ( self . HandleLocalityMenu ( at )     ) :
      return True
    ##########################################################################
    if                              ( at == 1001                           ) :
      ########################################################################
      self . clear                  (                                        )
      self . startup                (                                        )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 1101                           ) :
      self . RenameItem             (                                        )
      return True
    ##########################################################################
    if                              ( at == 1601                           ) :
      ########################################################################
      uuid = self . itemUuid        ( items [ 0 ] , 0                        )
      NAM  = self . Tables          [ "NamesEditing"                         ]
      self . EditAllNames           ( self , "StellarSpectrums" , uuid , NAM )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 3001                           ) :
      ########################################################################
      self . Go                     ( self . TranslateAll                    )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
