# -*- coding: utf-8 -*-
##############################################################################
## FaceView
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
from   PyQt5 . QtGui                  import QPainter
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QFont
from   PyQt5 . QtGui                  import QFontMetrics
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
from   PyQt5 . QtWidgets              import QFileDialog
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
from   AITK  . Pictures   . Gallery   import Gallery     as GalleryItem
from   AITK  . Pictures   . Picture   import Picture     as Picture
from   AITK  . People     . People    import People      as PeopleItem
from   AITK  . People     . Faces . Face import Face     as Face
##############################################################################
class FaceView                       ( IconDock                            ) :
  ############################################################################
  HavingMenu            = 1371434312
  ############################################################################
  def __init__                       ( self , parent = None , plan = None  ) :
    ##########################################################################
    super ( ) . __init__             (        parent        , plan           )
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 60
    self . SortOrder          = "desc"
    self . PeopleUuid         = 0
    ##########################################################################
    self . dockingPlace       = Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction               ( self . HavingMenu , True              )
    ##########################################################################
    self . setAcceptDrops            ( False                                 )
    self . setDragEnabled            ( False                                 )
    self . setDragDropMode           ( QAbstractItemView . NoDragDrop        )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def GetUuidIcon ( self , DB , UUID                                       ) :
    return UUID
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    TABLE  = self . Tables     [ "FaceRegions"                               ]
    PUID   = self . PeopleUuid
    PQ     = ""
    ##########################################################################
    if                         ( PUID > 0                                  ) :
      ########################################################################
      PQ   = f"and ( `owner` = {PUID} )"
    ##########################################################################
    QQ     = f"""select count(*) from {TABLE}
                 where ( `used` = 1 )
                 {PQ} ;"""
    QQ     = " " . join        ( QQ . split ( )                              )
    ##########################################################################
    DB     . Query             ( QQ                                          )
    ONE    = DB . FetchOne     (                                             )
    ##########################################################################
    if                         ( ONE == None                               ) :
      return 0
    ##########################################################################
    if                         ( len ( ONE ) <= 0                          ) :
      return 0
    ##########################################################################
    return ONE                 [ 0                                           ]
  ############################################################################
  def ObtainUuidsQuery              ( self                                 ) :
    ##########################################################################
    TABLE  = self . Tables          [ "FaceRegions"                          ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    PUID   = self . PeopleUuid
    PQ     = ""
    ##########################################################################
    if                              ( PUID > 0                             ) :
      ########################################################################
      PQ   = f"and ( `owner` = {PUID} )"
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
                 where ( `used` = 1 )
                 {PQ}
                 order by `id` {ORDER}
                 limit {SID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def FetchIcon                       ( self , DB , UUID                   ) :
    ##########################################################################
    if                                ( UUID <= 0                          ) :
      return None
    ##########################################################################
    FRRTAB     = self . Tables        [ "FaceRegions"                        ]
    QQ         = f"""select `picture`,`x`,`y`,`width`,`height`,`rotation` from {FRRTAB}
                     where ( `uuid` = {UUID} ) ;"""
    QQ         = " " . join           ( QQ . split ( )                       )
    DB         . Query                ( QQ                                   )
    RR         = DB . FetchOne        (                                      )
    ##########################################################################
    if                                ( RR in [ False , None ]             ) :
      return None
    ##########################################################################
    PUID       = int                  ( RR [ 0 ]                             )
    XP         = int                  ( RR [ 1 ]                             )
    YP         = int                  ( RR [ 2 ]                             )
    WP         = int                  ( RR [ 3 ]                             )
    HP         = int                  ( RR [ 4 ]                             )
    ANGLE      = float                ( RR [ 5 ]                             )
    ##########################################################################
    PICTAB     = self . Tables        [ "Information"                        ]
    DOPTAB     = self . Tables        [ "Depot"                              ]
    ##########################################################################
    PIC        = Picture              (                                      )
    ##########################################################################
    INFO       = PIC . GetInformation ( DB , PICTAB , PUID                   )
    ##########################################################################
    QQ         = f"select `file` from {DOPTAB} where ( `uuid` = {PUID} ) ;"
    ##########################################################################
    if                                ( not PIC . FromDB ( DB , QQ )       ) :
      return None
    ##########################################################################
    PART       = PIC  . Crop          ( XP , YP , WP , HP                    )
    ROT        = PART . Rotate        ( ANGLE                                )
    IMG        = ROT  . toQImage      (                                      )
    TSIZE      = IMG . size           (                                      )
    ##########################################################################
    ISIZE      = self . iconSize      (                                      )
    ICZ        = QImage               ( ISIZE , QImage . Format_ARGB32       )
    ICZ        . fill                 ( QColor ( 255 , 255 , 255 )           )
    ##########################################################################
    SCALE      = False
    ##########################################################################
    if ( TSIZE . width  ( ) > ISIZE . width ( )                            ) :
      SCALE    = True
    ##########################################################################
    if ( TSIZE . height ( ) > ISIZE . height ( )                           ) :
      SCALE    = True
    ##########################################################################
    if                                ( SCALE                              ) :
      ########################################################################
      IMG      = IMG . scaled         ( ISIZE , Qt . KeepAspectRatio         )
    ##########################################################################
    XSIZE      = IMG . size           (                                      )
    ##########################################################################
    W          = int       ( ( ISIZE . width  ( ) - XSIZE . width  ( ) ) / 2 )
    H          = int       ( ( ISIZE . height ( ) - XSIZE . height ( ) ) / 2 )
    PTS        = QPoint               ( W , H                                )
    ##########################################################################
    p          = QPainter             (                                      )
    p          . begin                ( ICZ                                  )
    p          . drawImage            ( PTS , IMG                            )
    p          . end                  (                                      )
    ##########################################################################
    PIX        = QPixmap              (                                      )
    PIX        . convertFromImage     ( ICZ                                  )
    ##########################################################################
    return QIcon                      ( PIX                                  )
  ############################################################################
  def FetchSessionInformation             ( self , DB                      ) :
    ##########################################################################
    self . defaultFetchSessionInformation (        DB                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
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
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . defaultCloseEvent ( event                                         )
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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def ReloadLocality               ( self , DB                             ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    items , atItem , uuid = self . GetMenuDetails ( pos                      )
    ##########################################################################
    mm     = MenuManager               ( self                                )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AmountIndexMenu           ( mm                                  )
    self   . AppendRefreshAction       ( mm , 1001                           )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . SortingMenu               ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu (                                     )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunSortingMenu     ( at                                  )
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
