# -*- coding: utf-8 -*-
##############################################################################
## PicturesView
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
from   AITK  . Qt . IconDock          import IconDock    as IconDock
##############################################################################
from   AITK  . Qt . MenuManager       import MenuManager as MenuManager
from   AITK  . Qt . LineEdit          import LineEdit    as LineEdit
from   AITK  . Qt . ComboBox          import ComboBox    as ComboBox
from   AITK  . Qt . SpinBox           import SpinBox     as SpinBox
##############################################################################
from   AITK  . Essentials . Relation  import Relation    as Relation
from   AITK  . Calendars  . StarDate  import StarDate    as StarDate
from   AITK  . Calendars  . Periode   import Periode     as Periode
from   AITK  . Pictures   . Picture   import Picture     as PictureItem
##############################################################################
class PicturesView                ( IconDock                               ) :
  ############################################################################
  HavingMenu  = 1371434312
  ############################################################################
  ShowPicture = pyqtSignal         ( str                                     )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . Total     = 0
    self . StartId   = 0
    self . Amount    = 60
    self . SortOrder = "asc"
    self . UsingName = False
    ##########################################################################
    self . Grouping  = "Original"
    ## self . Grouping  = "Subordination"
    ## self . Grouping  = "Reverse"
    ##########################################################################
    self . Property  =             {                                         }
    self . Naming    = ""
    ## self . Naming    = "Size"
    ## self . Naming    = "Name"
    ## self . Naming    = "Uuid"
    ##########################################################################
    self . Relation  = Relation    (                                         )
    self . Relation  . setT2       ( "Picture"                               )
    self . Relation  . setRelation ( "Subordination"                         )
    ##########################################################################
    self . setFunction             ( self . HavingMenu , True                )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
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
    return Uuid
  ############################################################################
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    TABLE  = self . Tables   [ "Pictures"                                    ]
    QQ     = f"select count(*) from {TABLE} ;"
    DB     . Query           ( QQ                                            )
    ONE    = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( ONE == None                                 ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
      return 0
    ##########################################################################
    return ONE                 [ 0                                           ]
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
    TABLE  = self . Tables          [ "Pictures"                             ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    QQ     = f"select `uuid` from {TABLE} order by `id` {ORDER} limit {SID} , {AMOUNT} ;"
    ##########################################################################
    return QQ
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
  def ObtainsItemUuids ( self , DB                                         ) :
    ##########################################################################
    if                 ( self . Grouping == "Original"                     ) :
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
    self . LinkAction     ( "Delete"     , self . DeleteItems                )
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
    self . LinkAction      ( "Refresh"    , self . startup     , False       )
    self . LinkAction      ( "Delete"     , self . DeleteItems , False       )
    self . LinkAction      ( "Home"       , self . PageHome    , False       )
    self . LinkAction      ( "End"        , self . PageEnd     , False       )
    self . LinkAction      ( "PageUp"     , self . PageUp      , False       )
    self . LinkAction      ( "PageDown"   , self . PageDown    , False       )
    self . LinkAction      ( "SelectAll"  , self . SelectAll   , False       )
    self . LinkAction      ( "SelectNone" , self . SelectNone  , False       )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "picture/uuids"
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
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "picture/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
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
    if                              ( mtype in [ "picture/uuids" ]         ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                   ( UUIDs                                  )
      if                            ( self == sourceWidget                 ) :
        FMT   = self . getMenuItem  ( "MoveTo"                               )
        MSG   = FMT . format        ( CNT                                    )
      else                                                                   :
        title = sourceWidget . windowTitle (                                 )
        FMT   = self . getMenuItem  ( "CopyFrom"                             )
        MSG   = FMT . format        ( title , CNT                            )
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
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures             ( self , sourceWidget , pos , JSOX          ) :
    ##########################################################################
    atItem = self . itemAt     ( pos                                         )
    ##########################################################################
    ## 在內部移動
    ##########################################################################
    if                         ( self == sourceWidget                      ) :
      ########################################################################
      uuid   = -1
      if                       ( atItem not in [ False , None ]            ) :
        ######################################################################
        uuid = atItem . data   ( Qt . UserRole                               )
        uuid = int             ( uuid                                        )
      ########################################################################
      self   . Go              ( self . PicturesMoving                     , \
                                 ( uuid , JSOX , )                           )
      ########################################################################
      return True
    ##########################################################################
    ## 從外部加入
    ##########################################################################
    uuid     = -1
    if                         ( atItem in [ False , None ]                ) :
      uuid   = atItem . data   ( Qt . UserRole                               )
      uuid   = int             ( uuid                                        )
    ##########################################################################
    self     . Go              ( self . PicturesAppending                  , \
                                 ( uuid , JSOX , )                           )
    ##########################################################################
    return True
  ############################################################################
  def OrderingPUIDs          ( self , atUuid , UUIDs , PUIDs               ) :
    ##########################################################################
    KUIDs    = list          ( set ( PUIDs ) - set ( UUIDs )                 )
    ##########################################################################
    if                       ( atUuid < 0                                  ) :
      RUIDs  = list          ( KUIDs + UUIDs                                 )
      return RUIDs
    ##########################################################################
    try                                                                      :
      atPos  = KUIDs . index ( atUuid                                        )
    except                                                                   :
      RUIDs  = list          ( KUIDs + UUIDs                                 )
      return RUIDs
    ##########################################################################
    TOTAL    = len           ( KUIDs                                         )
    LEFTs    =               [                                               ]
    RIGHTs   = KUIDs
    if                       ( atPos > 0                                   ) :
      ########################################################################
      REMAIN =               ( TOTAL - atPos                                 )
      LEFTs  = KUIDs         [          : atPos                              ]
      RIGHTs = KUIDs         [ - REMAIN :                                    ]
    ##########################################################################
    return list              ( LEFTs + UUIDs + RIGHTs                        )
  ############################################################################
  def GetLastestPosition    ( self , DB , LUID                             ) :
    ##########################################################################
    RELTAB = self . Tables  [ "Relation"                                     ]
    ITEM   = "`position`"
    OPTS   = ""
    LMTS   = "limit 0 , 1"
    ##########################################################################
    self   . Relation . set ( "second" , LUID                                )
    QQ     = self . Relation . ExactColumn ( RELTAB , ITEM , OPTS , LMTS     )
    DB     . Query          ( QQ                                             )
    RR     = DB . FetchOne  (                                                )
    ##########################################################################
    if                      ( RR in [ False , None ]                       ) :
      return 0
    ##########################################################################
    if                      ( len ( RR ) != 1                              ) :
      return 0
    ##########################################################################
    return int              ( RR [ 0 ]                                       )
  ############################################################################
  def GenerateMovingSQL       ( self , LAST , UUIDs                        ) :
    ##########################################################################
    RELTAB = self . Tables    [ "Relation"                                   ]
    SQLs   =                  [                                              ]
    ##########################################################################
    LUID   = LAST + 10000
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . Relation . set   ( "second" , UUID                              )
      WS   = self . Relation . ExactItem (                                   )
      QQ   = f"update {RELTAB} set `position` = {LUID} {WS} ;"
      SQLs . append           ( QQ                                           )
      ########################################################################
      LUID = LUID + 1
    ##########################################################################
    LUID   = 0
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . Relation . set   ( "second" , UUID                              )
      WS   = self . Relation . ExactItem (                                   )
      QQ   = f"update {RELTAB} set `position` = {LUID} {WS} ;"
      SQLs . append           ( QQ                                           )
      ########################################################################
      LUID = LUID + 1
    ##########################################################################
    return SQLs
  ############################################################################
  def ExecuteMovingSqlCommands ( self , DB , SQLs                          ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PicturesMoving          ( self , atUuid , JSON                       ) :
    ##########################################################################
    UUIDs  = JSON             [ "UUIDs"                                      ]
    if                        ( len ( UUIDs ) <= 0                         ) :
      return
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( DB == None                                 ) :
      return
    ##########################################################################
    self   . OnBusy  . emit   (                                              )
    self   . setBustle        (                                              )
    ##########################################################################
    RELTAB = self . Tables    [ "Relation"                                   ]
    DB     . LockWrites       ( [ RELTAB                                   ] )
    ##########################################################################
    OPTS   = f"order by `position` asc"
    PUIDs  = self . Relation . Subordination ( DB , RELTAB , OPTS            )
    LUID   = PUIDs            [ -1                                           ]
    LAST   = self . GetLastestPosition ( DB     , LUID                       )
    PUIDs  = self . OrderingPUIDs      ( atUuid , UUIDs , PUIDs              )
    SQLs   = self . GenerateMovingSQL  ( LAST   , PUIDs                      )
    self   . ExecuteMovingSqlCommands  ( DB     , SQLs                       )
    ##########################################################################
    print ( "PicturesMoving : " , SQLs )
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    self   . setVacancy       (                                              )
    self   . GoRelax . emit   (                                              )
    DB     . Close            (                                              )
    ##########################################################################
    self   . loading          (                                              )
    ##########################################################################
    return
  ############################################################################
  def PicturesAppending        ( self , atUuid , JSON                      ) :
    ##########################################################################
    UUIDs  = JSON              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return
    ##########################################################################
    DB     = self . ConnectDB  (                                             )
    if                         ( DB == None                                ) :
      return
    ##########################################################################
    self   . OnBusy  . emit    (                                             )
    self   . setBustle         (                                             )
    ##########################################################################
    RELTAB = self . Tables     [ "Relation"                                  ]
    ##########################################################################
    DB     . LockWrites        ( [ RELTAB                                  ] )
    self   . Relation  . Joins ( DB , RELTAB , UUIDs                         )
    OPTS   = f"order by `position` asc"
    PUIDs  = self . Relation . Subordination ( DB , RELTAB , OPTS            )
    ##########################################################################
    LUID   = PUIDs             [ -1                                          ]
    LAST   = self . GetLastestPosition ( DB     , LUID                       )
    PUIDs  = self . OrderingPUIDs      ( atUuid , UUIDs , PUIDs              )
    SQLs   = self . GenerateMovingSQL  ( LAST   , PUIDs                      )
    self   . ExecuteMovingSqlCommands  ( DB     , SQLs                       )
    ##########################################################################
    print ( "PicturesAppending : " , SQLs )
    ##########################################################################
    DB     . UnlockTables      (                                             )
    self   . setVacancy        (                                             )
    self   . GoRelax . emit    (                                             )
    DB     . Close             (                                             )
    ##########################################################################
    self   . loading           (                                             )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                     ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    RELTAB = self . Tables            [ "Relation"                           ]
    SQLs   =                          [                                      ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      self . Relation . set           ( "second" , UUID                      )
      QQ   = self . Relation . Delete ( RELTAB                               )
      SQLs . append                   ( QQ                                   )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self   . OnBusy  . emit           (                                      )
    self   . setBustle                (                                      )
    ##########################################################################
    DB     . LockWrites               ( [ RELTAB                           ] )
    ##########################################################################
    print ( "DeleteItems:" , SQLs )
    ##########################################################################
    DB     . UnlockTables             (                                      )
    self   . setVacancy               (                                      )
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    ##########################################################################
    self   . loading                  (                                      )
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
  def ObtainPictureSizes       ( self , DB , UUIDs                         ) :
    ##########################################################################
    PICTAB = self . Tables     [ "Information"                               ]
    NAMEs  =                   {                                             }
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ   = f"""select `width`,`height` from {PICTAB}
                where ( `uuid` = {UUID} ) ;"""
      QQ   = " " . join        ( QQ . split ( )                              )
      DB   . Query             ( QQ                                          )
      RR   = DB . FetchOne     (                                             )
      ########################################################################
      if ( ( RR not in [ False , None ] ) and ( len ( RR ) > 0 ) )           :
        WW             = RR    [ 0                                           ]
        HH             = RR    [ 1                                           ]
        NAMEs [ UUID ] = f"{WW} x {HH}"
      else                                                                   :
        NAMEs [ UUID ] = ""
    ##########################################################################
    return NAMEs
  ############################################################################
  def ObtainsUuidNames                 ( self , DB , UUIDs                 ) :
    ##########################################################################
    if                                 ( len ( UUIDs ) <= 0                ) :
      return                           {                                     }
    ##########################################################################
    if                                 ( self . Naming == "Uuid"           ) :
      NAMEs =                          {                                     }
      for UUID in UUIDs                                                      :
        NAMEs [ UUID ] = str           ( UUID                                )
      return NAMEs
    ##########################################################################
    if                                 ( self . Naming == "Name"           ) :
      TABLE = self . Tables            [ "Names"                             ]
      NAMEs = self . GetNames          ( DB , TABLE , UUIDs                  )
      return NAMEs
    ##########################################################################
    if                                 ( self . Naming == "Size"           ) :
      return self . ObtainPictureSizes ( DB , UUIDs                          )
    ##########################################################################
    return                            {                                      }
  ############################################################################
  def AssignAsIcon                 ( self , UUID                           ) :
    ##########################################################################
    print ( "AssignAsIcon : " , UUID )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems                   ( self                                 ) :
    ##########################################################################
    UUIDs = self . getSelectedUuids (                                        )
    if                              ( len ( UUIDs ) <= 0                   ) :
      return
    ##########################################################################
    self  . Go                      ( self . RemoveItems , ( UUIDs , )       )
    ##########################################################################
    return
  ############################################################################
  def PropertiesMenu         ( self , mm                                   ) :
    ##########################################################################
    MSG = self . getMenuItem ( "Properties"                                  )
    COL = mm   . addMenu     ( MSG                                           )
    ##########################################################################
    msg = self . getMenuItem ( "DisplayNone"                                 )
    mm  . addActionFromMenu  ( COL , 1301 , msg                              )
    ##########################################################################
    msg = self . getMenuItem ( "DisplaySize"                                 )
    mm  . addActionFromMenu  ( COL , 1302 , msg                              )
    ##########################################################################
    msg = self . getMenuItem ( "DisplayName"                                 )
    mm  . addActionFromMenu  ( COL , 1303 , msg                              )
    ##########################################################################
    msg = self . getMenuItem ( "DisplayUuid"                                 )
    mm  . addActionFromMenu  ( COL , 1304 , msg                              )
    ##########################################################################
    return mm
  ############################################################################
  def RunPropertiesMenu ( self , at                                        ) :
    ##########################################################################
    if                  ( at == 1301                                       ) :
      ########################################################################
      self . UsingName = False
      self . Naming    = ""
      ########################################################################
      self . clear      (                                                    )
      self . startup    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 1302                                       ) :
      ########################################################################
      self . UsingName = True
      self . Naming    = "Size"
      ########################################################################
      self . clear      (                                                    )
      self . startup    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 1303                                       ) :
      ########################################################################
      self . UsingName = True
      self . Naming    = "Name"
      ########################################################################
      self . clear      (                                                    )
      self . startup    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    if                  ( at == 1304                                       ) :
      ########################################################################
      self . UsingName = True
      self . Naming    = "Uuid"
      ########################################################################
      self . clear      (                                                    )
      self . startup    (                                                    )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                              ( self , pos                       ) :
    ##########################################################################
    if                                  ( not self . isPrepared ( )        ) :
      return False
    ##########################################################################
    doMenu = self . isFunction          ( self . HavingMenu                  )
    if                                  ( not doMenu                       ) :
      return False
    ##########################################################################
    self   . Notify                     ( 0                                  )
    ##########################################################################
    items  = self . selectedItems       (                                    )
    atItem = self . itemAt              ( pos                                )
    uuid   = 0
    ##########################################################################
    if                                  ( atItem not in [ False , None ]   ) :
      uuid = atItem . data              ( Qt . UserRole                      )
      uuid = int                        ( uuid                               )
    ##########################################################################
    mm     = MenuManager                ( self                               )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu     ( mm                                 )
    ##########################################################################
    mm     . addSeparator               (                                    )
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    ##########################################################################
    if                                  ( uuid > 0                         ) :
      ########################################################################
      mm   . addSeparator               (                                    )
      ########################################################################
      msg  = self . getMenuItem         ( "ViewPicture"                      )
      mm   . addAction                  ( 1101 , msg                         )
      ########################################################################
      msg  = self . getMenuItem         ( "AssignIcon"                       )
      mm   . addAction                  ( 1102 , msg                         )
    ##########################################################################
    mm     . addSeparator               (                                    )
    self   . PropertiesMenu             ( mm                                 )
    self   . SortingMenu                ( mm                                 )
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    mm     . setFont                    ( self    . menuFont ( )             )
    aa     = mm . exec_                 ( QCursor . pos      ( )             )
    at     = mm . at                    ( aa                                 )
    ##########################################################################
    if                                  ( self . RunAmountIndexMenu ( )    ) :
      ########################################################################
      self . clear                      (                                    )
      self . startup                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( self . RunDocking   ( mm , aa )  ) :
      return True
    ##########################################################################
    if                                  ( self . RunSortingMenu    ( at )  ) :
      ########################################################################
      self . clear                      (                                    )
      self . startup                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( self . RunPropertiesMenu ( at )  ) :
      return True
    ##########################################################################
    if                                  ( at == 1001                       ) :
      ########################################################################
      self . clear                      (                                    )
      self . startup                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 1101                       ) :
      self . ShowPicture . emit         ( str ( uuid )                       )
      return True
    ##########################################################################
    if                                  ( at == 1102                       ) :
      self . Go                         ( self . AssignAsIcon , ( uuid , )   )
      return True
    ##########################################################################
    return True
##############################################################################
