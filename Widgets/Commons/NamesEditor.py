# -*- coding: utf-8 -*-
##############################################################################
## TreeWidget
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
from   opencc                          import OpenCC
##############################################################################
from   PyQt5                           import QtCore
from   PyQt5                           import QtGui
from   PyQt5                           import QtWidgets
##############################################################################
from   PyQt5 . QtCore                  import QObject
from   PyQt5 . QtCore                  import pyqtSignal
from   PyQt5 . QtCore                  import Qt
from   PyQt5 . QtCore                  import QPoint
from   PyQt5 . QtCore                  import QPointF
from   PyQt5 . QtCore                  import QSize
##############################################################################
from   PyQt5 . QtGui                   import QIcon
from   PyQt5 . QtGui                   import QCursor
from   PyQt5 . QtGui                   import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets               import QApplication
from   PyQt5 . QtWidgets               import QWidget
from   PyQt5 . QtWidgets               import qApp
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAction
from   PyQt5 . QtWidgets               import QShortcut
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAbstractItemView
from   PyQt5 . QtWidgets               import QTreeWidget
from   PyQt5 . QtWidgets               import QTreeWidgetItem
from   PyQt5 . QtWidgets               import QLineEdit
from   PyQt5 . QtWidgets               import QComboBox
from   PyQt5 . QtWidgets               import QSpinBox
##############################################################################
from   AITK  . Qt        . VirtualGui  import VirtualGui  as VirtualGui
from   AITK  . Qt        . MenuManager import MenuManager as MenuManager
from   AITK  . Qt        . TreeWidget  import TreeWidget  as TreeWidget
from   AITK  . Qt        . TreeDock    import TreeDock    as TreeDock
##############################################################################
from   AITK  . Documents . Name        import Name        as NameItem
##############################################################################
class NamesEditor        ( TreeDock , NameItem                             ) :
  ############################################################################
  emitNamesShow   = pyqtSignal (                                             )
  emitAllNames    = pyqtSignal ( list                                        )
  emitNewItem     = pyqtSignal ( list                                        )
  emitRefreshItem = pyqtSignal ( QTreeWidgetItem , list                      )
  CloseMyself     = pyqtSignal ( QWidget , int                               )
  ############################################################################
  def __init__           ( self , parent = None                            ) :
    ##########################################################################
    super ( TreeDock , self ) . __init__ ( parent                            )
    super ( NameItem , self ) . __init__ (                                   )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                    ( self                                   ) :
    return QSize                  ( 800 , 480                                )
  ############################################################################
  def Prepare                     ( self                                   ) :
    ##########################################################################
    Names  = self . Translations  [ "NamesEditor" ] [ "Labels"               ]
    Items  = self . tableItems    (                                          )
    ##########################################################################
    self   . defaultLocality  = 1001
    self   . defaultRelevance =    0
    self   . ShowCompact      = True
    ##########################################################################
    self   . KEYs =               [ "id"                                     ,
                                    "name"                                   ,
                                    "locality"                               ,
                                    "relevance"                              ,
                                    "priority"                               ,
                                    "flags"                                  ,
                                    "utf8"                                   ,
                                    "length"                                 ,
                                    "ltime"                                  ]
    ##########################################################################
    TOTAL    = len                ( self . KEYs                              )
    self     . setColumnCount     ( TOTAL + 1                                )
    ##########################################################################
    self     . LabelItem = QTreeWidgetItem (                                 )
    for i , it in enumerate       ( self . KEYs                            ) :
      self   . LabelItem . setText          ( i , Names [ it ]               )
      self   . LabelItem . setTextAlignment ( i , Qt . AlignHCenter          )
    self     . LabelItem . setText          ( TOTAL , ""                     )
    self     . setHeaderItem      ( self . LabelItem                         )
    ##########################################################################
    self     . setColumnWidth     ( TOTAL     , 3                            )
    ##########################################################################
    self     . setColumnHidden    ( 0         , True                         )
    self     . setColumnHidden    ( TOTAL - 1 , True                         )
    ##########################################################################
    self     . setRootIsDecorated ( False                                    )
    ##########################################################################
    self     . emitNamesShow   . connect ( self . show                       )
    self     . emitAllNames    . connect ( self . refresh                    )
    self     . emitNewItem     . connect ( self . appendJsonItem             )
    self     . emitRefreshItem . connect ( self . RefreshItem                )
    ##########################################################################
    self     . MountClicked       ( 1                                        )
    self     . MountClicked       ( 2                                        )
    ##########################################################################
    QShortcut ( QKeySequence ( "Ins"                 ) , self ) . activated . connect ( self . InsertItem  )
    QShortcut ( QKeySequence ( QKeySequence . Delete ) , self ) . activated . connect ( self . DeleteItems )
    ##########################################################################
    self     . setSelectionMode   ( QAbstractItemView . ContiguousSelection  )
    ##########################################################################
    self     . setPrepared        ( True                                     )
    ##########################################################################
    return
  ############################################################################
  def closeEvent                 ( self , event                            ) :
    ##########################################################################
    if                           ( self . TryClose ( )                     ) :
      event . accept             (                                           )
    else                                                                     :
      event . ignore             (                                           )
    ##########################################################################
    return
  ############################################################################
  def Configure                  ( self                                    ) :
    return
  ############################################################################
  def FocusIn                    ( self                                    ) :
    return False
  ############################################################################
  def FocusOut                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def appendJsonItem             ( self , JSON                             ) :
    ##########################################################################
    item = self . jsonToItem     ( JSON                                      )
    self . addTopLevelItem       ( item                                      )
    self . setCurrentItem        ( item                                      )
    ##########################################################################
    return
  ############################################################################
  def singleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( self . isItemPicked ( )                 ) :
      if ( column != self . CurrentItem [ "Column" ] )                       :
        self . removeParked      (                                           )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in [ 1 , 2 , 3 , 4 , 5 ]     ) :
      return
    ##########################################################################
    if                           ( column == 1                             ) :
      ########################################################################
      line = self . setLineEdit  ( item                                      ,
                                   column                                    ,
                                   "editingFinished"                         ,
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    elif                         ( column == 2                             ) :
      ########################################################################
      LL   = self . Translations [ "NamesEditor" ] [ "Languages"             ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . localityChanged                    )
      cb   . addJson             ( LL , val                                  )
      cb   . showPopup           (                                           )
    ##########################################################################
    elif                         ( column == 3                             ) :
      ########################################################################
      RR   = self . Translations [ "NamesEditor" ] [ "Relevance"             ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . relevanceChanged                   )
      cb   . addJson             ( RR , val                                  )
      cb   . showPopup           (                                           )
    ##########################################################################
    elif                         ( column in [ 4 , 5 ]                     ) :
      ########################################################################
      sb   = self . setSpinBox   ( item                                      ,
                                   column                                    ,
                                   0                                         ,
                                   999999999                                 ,
                                   "editingFinished"                         ,
                                   self . spinChanged                        )
      sb   . setAlignment        ( Qt . AlignRight                           )
      sb   . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    elif                         ( column == 5                             ) :
      pass
    ##########################################################################
    return
  ############################################################################
  def stateChanged               ( self , item , column                    ) :
    return
  ############################################################################
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
    ##########################################################################
    if                          ( msg != text                              ) :
      ########################################################################
      pid  = int                ( item . text ( 0 )                          )
      bmsg = str . encode       ( msg                                        )
      ########################################################################
      item . setText            ( column ,              msg                  )
      item . setText            ( 6      , str ( len (  msg ) )              )
      item . setText            ( 7      , str ( len ( bmsg ) )              )
      ########################################################################
      threading . Thread        ( target = self . UpdateUuidName             ,
                                  args   = ( item , pid , msg , ) ) . start ()
    ##########################################################################
    self . removeParked          (                                           )
    ##########################################################################
    return
  ############################################################################
  def localityChanged            ( self                                    ) :
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
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      pid  = int                 ( item . text ( 0 )                         )
      LL   = self . Translations [ "NamesEditor" ] [ "Languages"             ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      threading . Thread         ( target = self . UpdateByLocality          ,
                                   args   = ( item , pid , value , ) ) . start ()
    ##########################################################################
    self . removeParked          (                                           )
    ##########################################################################
    return
  ############################################################################
  def relevanceChanged           ( self                                    ) :
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
    cbv    = int                 ( cbv                                       )
    value  = int                 ( value                                     )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      pid  = int                 ( item . text ( 0 )                         )
      RR   = self . Translations [ "NamesEditor" ] [ "Relevance"             ]
      msg  = RR                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      threading . Thread         ( target = self . UpdateByRelevance         ,
                                   args   = ( item , pid , value , ) ) . start ()
    ##########################################################################
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
    v      = self . CurrentItem [ "Value"                                    ]
    v      = int                ( v                                          )
    nv     = sb   . value       (                                            )
    ##########################################################################
    if                          ( v != nv                                  ) :
      ########################################################################
      pid  = int                ( item . text ( 0 )                          )
      ########################################################################
      item . setText            ( column , str ( nv )                        )
      ########################################################################
      if                        ( column == 4                              ) :
        threading . Thread      ( target = self . UpdateByPriority           ,
                                  args   = ( item , pid , nv , ) ) . start ( )
      elif                      ( column == 5                              ) :
        threading . Thread      ( target = self . UpdateByFlags              ,
                                  args   = ( item , pid , nv , ) ) . start ( )
    ##########################################################################
    self . removeParked          (                                           )
    ##########################################################################
    return
  ############################################################################
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    th = threading . Thread      ( target = self . AppendItem                )
    th . start                   (                                           )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems                             ( self                       ) :
    ##########################################################################
    items        = self . selectedItems       (                              )
    if                                        ( len ( items ) <= 0         ) :
      return
    ##########################################################################
    Listings     =                            [                              ]
    for it in items                                                          :
      i          = self . indexOfTopLevelItem ( it                           )
      if                                      ( i >= 0                     ) :
        pid      = it . text                  ( 0                            )
        pid      = int                        ( pid                          )
        self     . takeTopLevelItem           ( i                            )
        Listings . append                     ( pid                          )
    ##########################################################################
    if                                        ( len ( Listings ) <= 0      ) :
      return
    ##########################################################################
    th           = threading . Thread         ( target = self . RemoveItems  ,
                                                args   = ( Listings , )      )
    th           . start                      (                              )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    COL    = mm . addMenu          ( TRX [ "UI::Columns" ]                   )
    ##########################################################################
    for i , it in enumerate        ( self . KEYs                           ) :
       msg = TRX [ "NamesEditor" ] [ "Labels" ] [ it ]
       hid = self . isColumnHidden ( i                                       )
       mm  . addActionFromMenu     ( COL , 9000 + i , msg , True , not hid   )
    ##########################################################################
    K      = len                   ( self . KEYs                             )
    msg    = TRX                   [ "UI::Whitespace"                        ]
    hid    = self . isColumnHidden ( K                                       )
    mm     . addActionFromMenu     ( COL , 9000 + K , msg , True , not hid   )
    ##########################################################################
    return mm
  ############################################################################
  def TranslationsMenu             ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations   [ "Translations"                          ]
    msg    = self . Translations   [ "UI::Translations"                      ]
    KEYs   = TRX  . keys           (                                         )
    ##########################################################################
    LOT    = mm . addMenu          ( msg                                     )
    ##########################################################################
    for K in KEYs                                                            :
       msg = TRX                   [ K                                       ]
       V   = int                   ( K                                       )
       mm  . addActionFromMenu     ( LOT , V , msg                           )
    ##########################################################################
    return mm
  ############################################################################
  def LocalityMenu                 ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    LOC    = self . Translations   [ "NamesEditor" ] [ "Languages"           ]
    ##########################################################################
    msg    = TRX  [ "NamesEditor" ] [ "Menus" ] [ "Language" ]
    LOM    = mm . addMenu          ( msg                                     )
    ##########################################################################
    KEYs   = LOC . keys            (                                         )
    ##########################################################################
    for K in KEYs                                                            :
       msg = LOC                   [ K                                       ]
       V   = int                   ( K                                       )
       hid =                       ( V == self . defaultLocality             )
       mm  . addActionFromMenu     ( LOM , 10000000 + V , msg , True , hid   )
    ##########################################################################
    return mm
  ############################################################################
  def RelevanceMenu                ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    REL    = self . Translations   [ "NamesEditor" ] [ "Relevance"           ]
    ##########################################################################
    msg    = TRX  [ "NamesEditor" ] [ "Menus" ] [ "Relevance" ]
    LOR    = mm . addMenu          ( msg                                     )
    ##########################################################################
    KEYs   = REL . keys            (                                         )
    ##########################################################################
    for K in KEYs                                                            :
       msg = REL                   [ K                                       ]
       V   = int                   ( K                                       )
       hid =                       ( V == self . defaultRelevance            )
       mm  . addActionFromMenu     ( LOR , 8000 + V , msg , True , hid       )
    ##########################################################################
    return mm
  ############################################################################
  def HandleTranslations     ( self , item , ID                            ) :
    ##########################################################################
    if                       ( ( ID < 7001 ) or ( ID > 7008 )              ) :
      return False
    ##########################################################################
    CODE   = ""
    if                       ( ID == 7001                                  ) :
      CODE = "t2s"
    elif                     ( ID == 7002                                  ) :
      CODE = "s2t"
    elif                     ( ID == 7003                                  ) :
      CODE = "tw2s"
    elif                     ( ID == 7004                                  ) :
      CODE = "s2tw"
    elif                     ( ID == 7005                                  ) :
      CODE = "tw2sp"
    elif                     ( ID == 7006                                  ) :
      CODE = "s2twp"
    elif                     ( ID == 7007                                  ) :
      CODE = "hk2s"
    elif                     ( ID == 7008                                  ) :
      CODE = "s2hk"
    ##########################################################################
    pid    = item . text     ( 0                                             )
    text   = item . text     ( 1                                             )
    pid    = int             ( pid                                           )
    cc     = OpenCC          ( CODE                                          )
    target = cc . convert    ( text                                          )
    UTF8   = len             ( target                                        )
    LENZ   = 0
    ##########################################################################
    try                                                                      :
      S    = target . encode ( "utf-8"                                       )
      LENZ = len             ( S                                             )
    except                                                                   :
      pass
    ##########################################################################
    item   . setText         ( 1 , target                                    )
    item   . setText         ( 6 , str ( UTF8 )                              )
    item   . setText         ( 7 , str ( LENZ )                              )
    ##########################################################################
    threading . Thread       ( target = self . UpdateUuidName                ,
                               args   = ( item , pid , target , ) ) . start ()
    ##########################################################################
    return True
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    items  = self . selectedItems  (                                         )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     . addAction             ( 1001 ,  TRX [ "UI::Refresh" ]           )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     . addAction             ( 1101 ,  TRX [ "UI::Insert"  ]           )
    if                             ( len ( items ) > 0                     ) :
      mm   . addAction             ( 1102 ,  TRX [ "UI::Delete"  ]           )
      if ( self . canSpeak ( ) ) and ( len ( items ) == 1 )                  :
        mm . addAction             ( 1501 ,  TRX [ "UI::Talk"  ]             )
    ##########################################################################
    mm     . addSeparator          (                                         )
    mm     . addAction             ( 1801                                  , \
                                     TRX [ "UI::AutoCompact" ]             , \
                                     True                                  , \
                                     self . ShowCompact                      )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . ColumnsMenu      ( mm                                    )
    if                               ( len ( items ) == 1                  ) :
      mm   = self . TranslationsMenu ( mm                                    )
    mm     = self . LocalityMenu     ( mm                                    )
    mm     = self . RelevanceMenu    ( mm                                    )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( at >= 10000000                        ) :
      self . defaultLocality  = at - 10000000
      return True
    ##########################################################################
    if                             ( len ( items ) == 1                    ) :
      if ( self . HandleTranslations ( items [ 0 ] , at )                  ) :
        return True
    ##########################################################################
    if                             ( at >= 9000                            ) :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      return True
    ##########################################################################
    if                             ( at >= 8000                            ) :
      self . defaultRelevance = at - 8000
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1101                            ) :
      self . InsertItem            (                                         )
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      self . DeleteItems           (                                         )
      return True
    ##########################################################################
    if                             ( at == 1501                            ) :
      ########################################################################
      item = items                 [ 0                                       ]
      T    = item . text           ( 1                                       )
      L    = item . data           ( 2 , Qt . UserRole                       )
      L    = int                   ( L                                       )
      ########################################################################
      self . Talk                  ( T , L                                   )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1801                            ) :
      self . ShowCompact =         ( not self . ShowCompact                  )
    ##########################################################################
    return True
  ############################################################################
  def TryClose                   ( self                                    ) :
    ##########################################################################
    self . setPrepared           ( False                                     )
    self . CloseMyself . emit    ( self , int ( self . get ( "uuid" ) )      )
    ##########################################################################
    return True
  ############################################################################
  def UpdateUuidName                ( self , item , pid , name             ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    ##########################################################################
    self   . set                    ( "id"   , pid                           )
    self   . set                    ( "name" , name                          )
    ##########################################################################
    DB     . LockWrites             ( [ TABLE ]                              )
    self   . UpdateNameById         ( DB , TABLE                             )
    DB     . UnlockTables           (                                        )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    return
  ############################################################################
  def UpdateMajorParameters         ( self , DB , TABLE                    ) :
    ##########################################################################
    IDX    = self . GetPosition     (        DB , TABLE                      )
    if                              ( IDX < 0                              ) :
      DB   . LockWrites             ( [ TABLE ]                              )
      self . UpdateParametersById   (        DB , TABLE                      )
      DB   . UnlockTables           (                                        )
    ##########################################################################
    self   . ObtainsById            (        DB , TABLE                      )
    ##########################################################################
    return self . toList            (                                        )
  ############################################################################
  def UpdateByLocality              ( self , item , pid , locality         ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    JSON   = self . itemToJson      ( item                                   )
    ##########################################################################
    self   . set                    ( "id"        , pid                      )
    self   . set                    ( "locality"  , locality                 )
    self   . set                    ( "relevance" , JSON [ "Relevance" ]     )
    self   . set                    ( "priority"  , JSON [ "Priority"  ]     )
    ##########################################################################
    CRX    = self . UpdateMajorParameters ( DB , TABLE                       )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    self   . emitRefreshItem . emit ( item , CRX                             )
    ##########################################################################
    return
  ############################################################################
  def UpdateByRelevance             ( self , item , pid , relevance        ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    JSON   = self . itemToJson      ( item                                   )
    ##########################################################################
    self   . set                    ( "id"        , pid                      )
    self   . set                    ( "locality"  , JSON [ "Locality"  ]     )
    self   . set                    ( "relevance" , relevance                )
    self   . set                    ( "priority"  , JSON [ "Priority"  ]     )
    ##########################################################################
    CRX    = self . UpdateMajorParameters ( DB , TABLE                       )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    self   . emitRefreshItem . emit ( item , CRX                             )
    ##########################################################################
    return
  ############################################################################
  def UpdateByPriority              ( self , item , pid , priority         ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    JSON   = self . itemToJson      ( item                                   )
    ##########################################################################
    self   . set                    ( "id"        , pid                      )
    self   . set                    ( "locality"  , JSON [ "Locality"  ]     )
    self   . set                    ( "relevance" , JSON [ "Relevance" ]     )
    self   . set                    ( "priority"  , priority                 )
    ##########################################################################
    CRX    = self . UpdateMajorParameters ( DB , TABLE                       )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    self   . emitRefreshItem . emit ( item , CRX                             )
    ##########################################################################
    return
  ############################################################################
  def UpdateByFlags                   ( self , item , pid , flags            ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    self   . set                    ( "id"    , pid                          )
    self   . set                    ( "flags" , flags                        )
    ##########################################################################
    DB     . LockWrites             ( [ TABLE ]                              )
    self   . UpdateFlagsById        ( DB , TABLE                             )
    DB     . UnlockTables           (                                        )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                   ( self , Listings                      ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    QQ     = self . DeleteIDs       ( TABLE , Listings                       )
    DB     . LockWrites             ( [ TABLE ]                              )
    DB     . Query                  ( QQ                                     )
    DB     . UnlockTables           (                                        )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    return
  ############################################################################
  def AppendItem                    ( self                                 ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    ##########################################################################
    self . set                      ( "name"      , ""                       )
    self . set                      ( "locality"  , self . defaultLocality   )
    self . set                      ( "relevance" , self . defaultRelevance  )
    self . set                      ( "priority"  , 0                        )
    self . set                      ( "flags"     , 0                        )
    self . set                      ( "utf8"      , 0                        )
    self . set                      ( "length"    , 0                        )
    ##########################################################################
    DONE = False
    ##########################################################################
    self . Append                   ( DB , TABLE                             )
    IDX  = self . GetPosition       ( DB , TABLE                             )
    if                              ( IDX >= 0                             ) :
      self . Id = IDX
      if                            ( self . ObtainsById ( DB , TABLE )    ) :
        DONE = True
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    if                              ( DONE                                 ) :
      ########################################################################
      JSON = self . toList          (                                        )
      self . emitNewItem . emit     ( JSON                                   )
    ##########################################################################
    return
  ############################################################################
  def itemToJson                       ( self , item                       ) :
    ##########################################################################
    JSON                 =             {                                     }
    JSON [ "Id"        ] = item . text ( 0                                   )
    JSON [ "Name"      ] = item . text ( 1                                   )
    JSON [ "Locality"  ] = item . data ( 2 , Qt . UserRole                   )
    JSON [ "Relevance" ] = item . data ( 3 , Qt . UserRole                   )
    JSON [ "Priority"  ] = item . text ( 4                                   )
    JSON [ "Relevance" ] = item . text ( 5                                   )
    ##########################################################################
    JSON [ "Id"        ] = int         ( JSON [ "Id"        ]                )
    JSON [ "Locality"  ] = int         ( JSON [ "Locality"  ]                )
    JSON [ "Relevance" ] = int         ( JSON [ "Relevance" ]                )
    JSON [ "Priority"  ] = int         ( JSON [ "Priority"  ]                )
    JSON [ "Relevance" ] = int         ( JSON [ "Relevance" ]                )
    ##########################################################################
    return JSON
  ############################################################################
  def RefreshItem                ( self , item , JSON                      ) :
    ##########################################################################
    TRX  = self . Translations   [ "NamesEditor"                             ]
    ##########################################################################
    L    = JSON                  [ 2                                         ]
    R    = JSON                  [ 4                                         ]
    REL  = TRX                   [ "Relevance" ] [ str ( R )                 ]
    LANG = TRX                   [ "Languages" ] [ str ( L )                 ]
    ##########################################################################
    item . setText               ( 2 , str ( LANG      )                     )
    item . setData               ( 2 , Qt . UserRole , JSON [ 2 ]            )
    ##########################################################################
    item . setText               ( 3 , str ( REL       )                     )
    item . setData               ( 3 , Qt . UserRole , JSON [ 4 ]            )
    ##########################################################################
    item . setText               ( 4 , str ( JSON [  3 ] )                   )
    item . setTextAlignment      ( 4 , Qt.AlignRight                         )
    item . setData               ( 4 , Qt . UserRole , JSON [ 3 ]            )
    ##########################################################################
    return
  ############################################################################
  def jsonToItem                 ( self , JSON                             ) :
    ##########################################################################
    TRX  = self . Translations   [ "NamesEditor"                             ]
    item = QTreeWidgetItem       (                                           )
    ##########################################################################
    L    = JSON                  [ 2                                         ]
    R    = JSON                  [ 4                                         ]
    REL  = TRX                   [ "Relevance" ] [ str ( R )                 ]
    LANG = TRX                   [ "Languages" ] [ str ( L )                 ]
    S    = JSON                  [ 8                                         ]
    try                                                                      :
      S  = S . decode            ( "utf-8"                                   )
    except ( UnicodeDecodeError , AttributeError )                           :
      pass
    ##########################################################################
    item . setText               ( 0 , str ( JSON [  0 ] )                   )
    item . setTextAlignment      ( 4 , Qt.AlignRight                         )
    ##########################################################################
    item . setText               ( 1 , str ( S         )                     )
    ##########################################################################
    item . setText               ( 2 , str ( LANG      )                     )
    item . setData               ( 2 , Qt . UserRole , JSON [ 2 ]            )
    ##########################################################################
    item . setText               ( 3 , str ( REL       )                     )
    item . setData               ( 3 , Qt . UserRole , JSON [ 4 ]            )
    ##########################################################################
    item . setText               ( 4 , str ( JSON [  3 ] )                   )
    item . setTextAlignment      ( 4 , Qt.AlignRight                         )
    item . setData               ( 4 , Qt . UserRole , JSON [ 3 ]            )
    ##########################################################################
    item . setText               ( 5 , str ( JSON [  5 ] )                   )
    item . setTextAlignment      ( 5 , Qt.AlignRight                         )
    item . setData               ( 5 , Qt . UserRole , JSON [ 5 ]            )
    ##########################################################################
    item . setText               ( 6 , str ( JSON [  6 ] )                   )
    item . setTextAlignment      ( 6 , Qt.AlignRight                         )
    ##########################################################################
    item . setText               ( 7 , str ( JSON [  7 ] )                   )
    item . setTextAlignment      ( 7 , Qt.AlignRight                         )
    ##########################################################################
    item . setText               ( 8 , str ( JSON [  9 ] )                   )
    ##########################################################################
    item . setText               ( 9 , ""                                    )
    ##########################################################################
    return item
  ############################################################################
  def refresh                       ( self , All                           ) :
    ##########################################################################
    self . clear                    (                                        )
    TRX     = self . Translations   [ "NamesEditor"                          ]
    ##########################################################################
    for IT in All                                                            :
      ########################################################################
      NT    = self . jsonToItem     ( IT                                     )
      self  . addTopLevelItem       ( NT                                     )
    ##########################################################################
    self . emitNamesShow . emit     (                                        )
    ##########################################################################
    if                              ( self . ShowCompact                   ) :
      TOTAL   = len                 ( self . KEYs                            )
      for i in range                ( 0 , TOTAL - 1                        ) :
        self  . resizeColumnToContents ( i                                   )
    ##########################################################################
    return
  ############################################################################
  def loading                       ( self                                 ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      self . emitNamesShow . emit   (                                        )
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      self . emitNamesShow . emit   (                                        )
      return
    ##########################################################################
    ALL    = self . FetchEverything ( DB , self . Tables [ "Names" ]         )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    if                              ( len ( ALL ) <= 0                     ) :
      self . emitNamesShow . emit   (                                        )
    ##########################################################################
    self   . emitAllNames  . emit   ( ALL                                    )
    ##########################################################################
    return
  ############################################################################
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . Prepared                     ) :
      self . Prepare             (                                           )
    ##########################################################################
    threading . Thread ( target = self . loading ) . start (                 )
    ##########################################################################
    return
##############################################################################

"""

QSize N::PhonemeItems::sizeHint(void) const
{
  return QSize ( 1024 , 720 ) ;
}

bool N::PhonemeItems::FocusIn(void)
{
  LinkAction ( Insert     , New             ( ) ) ;
  LinkAction ( Refresh    , startup         ( ) ) ;
  LinkAction ( Copy       , CopyToClipboard ( ) ) ;
  LinkAction ( SelectNone , SelectNone      ( ) ) ;
  LinkAction ( SelectAll  , SelectAll       ( ) ) ;
  return true                                     ;
}

void N::PhonemeItems::Configure(void)
{
  setEmpty                     (                                  ) ;
  NewTreeWidgetItem            ( head                             ) ;
  head -> setText              ( 0 , tr("Name"    )               ) ;
  head -> setText              ( 1 , tr("Mnemonic")               ) ;
  head -> setText              ( 2 , tr("Flags"   )               ) ;
  head -> setText              ( 3 , tr("Code"    )               ) ;
  head -> setText              ( 4 , tr("Type"    )               ) ;
  head -> setText              ( 5 , tr("Start"   )               ) ;
  head -> setText              ( 6 , tr("End"     )               ) ;
  head -> setText              ( 7 , tr("Length"  )               ) ;
  head -> setText              ( 8 , ""                           ) ;
  ///////////////////////////////////////////////////////////////////
  setWindowTitle               ( tr("Phoneme lists")              ) ;
  setWindowIcon                ( QIcon(":/images/audiofiles.png") ) ;
  setDragDropMode              ( DragDrop                         ) ;
  setRootIsDecorated           ( false                            ) ;
  setAlternatingRowColors      ( true                             ) ;
  setSelectionMode             ( ExtendedSelection                ) ;
  setColumnCount               ( 9                                ) ;
  setHorizontalScrollBarPolicy ( Qt::ScrollBarAsNeeded            ) ;
  setVerticalScrollBarPolicy   ( Qt::ScrollBarAsNeeded            ) ;
  assignHeaderItems            ( head                             ) ;
  MountClicked                 ( 2                                ) ;
  setDropFlag                  ( DropPhoneme , true               ) ;
  plan -> setFont              ( this                             ) ;
}

void N::PhonemeItems::List(void)
{
  blockSignals      ( true        )                           ;
  SqlConnection  SC ( plan -> sql )                           ;
  if ( SC . open ( "PhonemeItems" , "List" ) )                {
    QString Q                                                 ;
    QString N                                                 ;
    UUIDs   U                                                 ;
    SUID    u                                                 ;
    ///////////////////////////////////////////////////////////
    if (isFirst())                                            {
      U = GroupItems :: Subordination                         (
            SC                                                ,
            first                                             ,
            t1                                                ,
            Types::Phoneme                                    ,
            relation                                          ,
            SC.OrderByAsc("position")                       ) ;
    } else
    if (isSecond())                                           {
      U = GroupItems :: GetOwners                             (
            SC                                                ,
            second                                            ,
            Types::Phoneme                                    ,
            t2                                                ,
            relation                                          ,
            SC.OrderByAsc("id")                             ) ;
    } else
    if ( 0 == first )                                         {
      U = SC . Uuids                                          (
            PlanTable(Phonemes)                               ,
            "uuid"                                            ,
            SC.OrderByAsc("id")                             ) ;
    }                                                         ;
    ///////////////////////////////////////////////////////////
    foreach ( u , U )                                         {
      N = SC . getName                                        (
            PlanTable(Names)                                  ,
            "uuid"                                            ,
            vLanguageId                                       ,
            u                                               ) ;
      Q = SC . sql . SelectFrom                               (
            SC . Columns                                      (
              7                                               ,
              "mnemonic"                                      ,
              "flags"                                         ,
              "code"                                          ,
              "type"                                          ,
              "start"                                         ,
              "end"                                           ,
              "length"                                      ) ,
            PlanTable ( Phonemes )                            ,
            SC . WhereUuid ( u )                            ) ;
      if (SC.Fetch(Q))                                        {
        QByteArray MB = SC . ByteArray ( 0 )                  ;
        int32_t    mb                                         ;
        memcpy ( &mb , MB.data() , 4 )                        ;
        NewTreeWidgetItem ( it )                              ;
        Phoneme ph                                            ;
        ph  . Mnemonic  = (unsigned int)mb                    ;
        ph  . Flags     = SC . Value(1) . toUInt  (   )       ;
        ph  . Code      = (unsigned char)SC . Int ( 2 )       ;
        ph  . Type      = (unsigned char)SC . Int ( 3 )       ;
        ph  . StartType = (unsigned char)SC . Int ( 4 )       ;
        ph  . EndType   = (unsigned char)SC . Int ( 5 )       ;
        ph  . Length    = (unsigned char)SC . Int ( 6 )       ;
        it -> setData   ( 0 , Qt::UserRole , u              ) ;
        it -> setText   ( 0 , N                             ) ;
        it -> setText   ( 1 , ph.MnemonicString()           ) ;
        it -> setText   ( 2 , QString::number(ph.Flags,16 ) ) ;
        it -> setText   ( 3 , QString::number(ph.Code     ) ) ;
        it -> setText   ( 4 , QString::number(ph.Type     ) ) ;
        it -> setText   ( 5 , QString::number(ph.StartType) ) ;
        it -> setText   ( 6 , QString::number(ph.EndType  ) ) ;
        it -> setText   ( 7 , QString::number(ph.Length   ) ) ;
        addTopLevelItem ( it                                ) ;
      }                                                       ;
    }                                                         ;
    ///////////////////////////////////////////////////////////
    SC . close          (                                   ) ;
  }                                                           ;
  SC . remove           (                                   ) ;
  blockSignals          ( false                             ) ;
  reportItems           (                                   ) ;
  plan -> StopBusy      (                                   ) ;
  emit AutoFit          (                                   ) ;
  Alert                 ( Done                              ) ;
}

bool N::PhonemeItems::Menu(QPoint pos)
{
  nScopedMenu ( mm , this )                       ;
  QAction         * aa                            ;
  QTreeWidgetItem * it = itemAt ( pos )           ;
  mm . add ( 101 , tr("New"         ) )           ;
  if (NotNull(it))                                {
    mm . add ( 102 , tr("Edit"      ) )           ;
  }                                               ;
  mm . add ( 103 , tr("Refresh"     ) )           ;
  mm . addSeparator  (                )           ;
  mm . add ( 201 , tr("Copy"        ) )           ;
  mm . add ( 202 , tr("Select all"  ) )           ;
  mm . add ( 203 , tr("Select none" ) )           ;
  mm . addSeparator  (                )           ;
  mm . add ( 901 , tr("Translations") )           ;
  DockingMenu ( mm )                              ;
  mm.setFont(plan)                                ;
  aa = mm.exec()                                  ;
  if (IsNull(aa)) return true                     ;
  if (RunDocking(mm,aa)) return true              ;
  UUIDs U                                         ;
  switch (mm[aa])                                 {
    case 101                                      :
      New             ( )                         ;
    break                                         ;
    case 102                                      :
      emit Edit ( it->text(0) , nTreeUuid(it,0) ) ;
    break                                         ;
    case 103                                      :
      startup         ( )                         ;
    break                                         ;
    case 201                                      :
      CopyToClipboard ( )                         ;
    break                                         ;
    case 202                                      :
      SelectAll       ( )                         ;
    break                                         ;
    case 203                                      :
      SelectNone      ( )                         ;
    break                                         ;
    case 901                                      :
      U = itemUuids     ( 0                 )     ;
      emit Translations ( windowTitle() , U )     ;
    break                                         ;
  }                                               ;
  return true                                     ;
}

"""
