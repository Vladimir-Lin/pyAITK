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
from   PyQt5 . QtWidgets              import QDoubleSpinBox
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
from   AITK  . UUIDs      . UuidListings import appendUuid
from   AITK  . UUIDs      . UuidListings import appendUuids
from   AITK  . UUIDs      . UuidListings import getUuids
##############################################################################
class FaceView                       ( IconDock                            ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  OpenPictureEditor = pyqtSignal     ( str , dict                            )
  ShowRawFace       = pyqtSignal     ( str , str , QIcon                     )
  SearchFaces       = pyqtSignal     ( str                                   )
  ############################################################################
  def __init__                       ( self , parent = None , plan = None  ) :
    ##########################################################################
    super ( ) . __init__             (        parent        , plan           )
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 60
    self . SortOrder          = "desc"
    self . Method             = ""
    self . PeopleUuid         = 0
    self . FaceUuid           = 0
    self . Sigma              = 0.035
    self . SigmaSpin          = None
    self . SearchMax          = 300
    self . PictureTables      = {                                            }
    self . STATEs             = [ "0" , "10000" , "20000"                    ]
    ##########################################################################
    self . dockingPlace       = Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction               ( self . HavingMenu , True              )
    ##########################################################################
    self . setAcceptDrops            ( False                                 )
    self . setDragEnabled            ( True                                  )
    self . setDragDropMode           ( QAbstractItemView . DragOnly          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 840 , 800 )                       )
  ############################################################################
  def SwitchFaceStates       ( self , STATE                                ) :
    ##########################################################################
    if                       ( STATE in self . STATEs                      ) :
      ########################################################################
      self . STATEs . remove ( STATE                                         )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . STATEs . append ( STATE                                         )
    ##########################################################################
    return
  ############################################################################
  def GetUuidIcon ( self , DB , UUID                                       ) :
    return UUID
  ############################################################################
  def FetchRegularDepotCount   ( self , DB                                 ) :
    ##########################################################################
    if                         ( "Search" == self . Method                 ) :
      return 0
    ##########################################################################
    TABLE  = self . Tables     [ "FaceRegions"                               ]
    PUID   = self . PeopleUuid
    PQ     = ""
    ST     = ""
    ##########################################################################
    if                         ( PUID > 0                                  ) :
      ########################################################################
      PQ   = f"and ( `owner` = {PUID} )"
    ##########################################################################
    if                         ( len ( self . STATEs ) > 0                 ) :
      ########################################################################
      STL  = "," . join        ( self . STATEs                               )
      ST   = f"and ( `states` in ( {STL} ) )"
    ##########################################################################
    QQ     = f"""select count(*) from {TABLE}
                 where ( `used` = 1 ) {ST} {PQ} ;"""
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
  def ObtainUuidsByOwner            ( self                                 ) :
    ##########################################################################
    TABLE  = self . Tables          [ "FaceRegions"                          ]
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder (                                        )
    ##########################################################################
    PUID   = self . PeopleUuid
    PQ     = ""
    ST     = ""
    ##########################################################################
    if                              ( PUID > 0                             ) :
      ########################################################################
      PQ   = f"and ( `owner` = {PUID} )"
    ##########################################################################
    if                         ( len ( self . STATEs ) > 0                 ) :
      ########################################################################
      STL  = "," . join        ( self . STATEs                               )
      ST   = f"and ( `states` in ( {STL} ) )"
    ##########################################################################
    QQ     = f"""select `uuid` from {TABLE}
                 where ( `used` = 1 ) {ST} {PQ}
                 order by `id` {ORDER}
                 limit {SID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join               ( QQ . split ( )                         )
  ############################################################################
  def ObtainsItemUuidsByOwner           ( self , DB                        ) :
    ##########################################################################
    QQ      = self . ObtainUuidsByOwner (                                    )
    UUIDs   =                           [                                    ]
    if                                  ( len ( QQ ) > 0                   ) :
      UUIDs = DB   . ObtainUuids        ( QQ                                 )
    ##########################################################################
    return UUIDs
  ############################################################################
  def SearchItemUuids          ( self , DB                                 ) :
    ##########################################################################
    UUIDs   =                  [                                             ]
    ##########################################################################
    FUID    = self . FaceUuid
    SIGMA   = self . Sigma
    SIGMA2  = float            ( SIGMA * SIGMA * 128.0                       )
    ##########################################################################
    if                         ( FUID <= 0                                 ) :
      return UUIDs
    ##########################################################################
    FUIDs   =                  [ FUID                                        ]
    COLs    =                  [                                             ]
    ##########################################################################
    for id in range            ( 1 , 129                                   ) :
      ########################################################################
      C     = f"{id}" . zfill  ( 3                                           )
      C     = f"`f{C}`"
      ########################################################################
      COLs  . append           ( C                                           )
    ##########################################################################
    COLX    = " , " . join     ( COLs                                        )
    TABLE   = self . Tables    [ "FaceRecognitions"                          ]
    ##########################################################################
    QQ      = f"""select {COLX} from {TABLE}
                  where ( `face` = {FUID} )
                  order by `id` desc
                  limit 0 , 1 ;"""
    DB      . Query            ( QQ                                          )
    RR      = DB . FetchOne    (                                             )
    ##########################################################################
    if                         ( RR in [ False , None ]                    ) :
      return FUIDs
    ##########################################################################
    if                         ( len ( RR ) != 128                         ) :
      return FUIDs
    ##########################################################################
    MULs    =                  [                                             ]
    ##########################################################################
    for id in range            ( 1 , 129                                   ) :
      ########################################################################
      FV    = float            ( RR [ id - 1 ]                               )
      C     = f"{id}" . zfill  ( 3                                           )
      C     = f"`f{C}`"
      ########################################################################
      X     = f"( {C} - {FV} )"
      Z     = f"( {X} * {X} )"
      ########################################################################
      MULs  . append           ( Z                                           )
    ##########################################################################
    MULX    = " + " . join     ( MULs                                        )
    ##########################################################################
    QQ      = f"""select `face` from {TABLE}
                  where ( ( {MULX} ) < {SIGMA2} ) ;"""
    ##########################################################################
    UUIDs   = DB . ObtainUuids ( QQ                                          )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                       ( UUID not in FUIDs                         ) :
        ######################################################################
        if                     ( len ( FUIDs ) < self . SearchMax          ) :
          ####################################################################
          FUIDs . append       ( UUID                                        )
    ##########################################################################
    return FUIDs
  ############################################################################
  def ObtainsItemUuids                      ( self , DB                    ) :
    ##########################################################################
    if                                      ( "Search" == self . Method    ) :
      return self . SearchItemUuids         (        DB                      )
    ##########################################################################
    return self   . ObtainsItemUuidsByOwner (        DB                      )
  ############################################################################
  def FetchIcon                       ( self , DB , UUID                   ) :
    ##########################################################################
    if                                ( UUID <= 0                          ) :
      return None
    ##########################################################################
    FRRTAB     = self . Tables        [ "FaceRegions"                        ]
    QQ         = f"""select `picture`,`x`,`y`,`width`,`height`,`rotation`,`states` from {FRRTAB}
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
    STATES     = int                  ( RR [ 6 ]                             )
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
    ## FF         = Face                 (                                      )
    ## WW         = INFO                 [ "Width"                              ]
    ## HH         = INFO                 [ "Height"                             ]
    ## XP , YP , WP , HP = FF . RotateArea ( WW , HH , XP , YP , WP , HP , ANGLE )
    ##########################################################################
    XC         = int ( float ( XP ) + ( float ( WP ) / 2 )                   )
    YC         = int ( float ( YP ) + ( float ( HP ) / 2 )                   )
    WP         = int ( float ( WP ) * 1.5                                    )
    HP         = int ( float ( HP ) * 1.5                                    )
    XP         = int ( XC - ( float ( WP ) / 2.0 )                           )
    YP         = int ( YC - ( float ( HP ) / 2.0 )                           )
    ##########################################################################
    if                              ( XP < 0                               ) :
      ########################################################################
      WP       = WP + XP
      XP       = 0
    ##########################################################################
    if                              ( YP < 0                               ) :
      ########################################################################
      HP       = HP + YP
      YP       = 0
    ##########################################################################
    ROTATED    =                      [ 10000 , 10001                      , \
                                        20000 , 20001                        ]
    ##########################################################################
    if                                ( STATES in [     0 ,     1 ]        ) :
      ########################################################################
      PART     = PIC  . Crop          ( XP , YP , WP , HP                    )
      ROT      = PART . Rotate        ( ANGLE                                )
      ########################################################################
      IMG      = ROT  . toQImage      (                                      )
      TSIZE    = IMG  . size          (                                      )
      ########################################################################
    elif                              ( STATES in ROTATED                  ) :
      ########################################################################
      PART     = PIC  . Rotate        ( ANGLE                                )
      ROT      = PART . Crop          ( XP , YP , WP , HP                    )
      ########################################################################
      IMG      = ROT  . toQImage      (                                      )
      TSIZE    = IMG  . size          (                                      )
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
  def ObtainsUuidNames        ( self , DB , UUIDs                          ) :
    ##########################################################################
    NAMEs   =                 {                                              }
    ##########################################################################
    FRRTAB  = self . Tables   [ "FaceRegions"                                ]
    ##########################################################################
    if                        ( len ( UUIDs ) > 0                          ) :
      ########################################################################
      for UUID in UUIDs                                                      :
        ######################################################################
        QQ  = f"""select `picture`,`x`,`y`,`width`,`height`,`rotation` from {FRRTAB}
                  where ( `uuid` = {UUID} ) ;"""
        QQ  = " " . join      ( QQ . split ( )                               )
        DB  . Query           ( QQ                                           )
        RR  = DB . FetchOne   (                                              )
        ######################################################################
        if                    ( RR in [ False , None ]                     ) :
          continue
        ######################################################################
        PU  = int             ( RR [ 0 ]                                     )
        XP  = int             ( RR [ 1 ]                                     )
        YP  = int             ( RR [ 2 ]                                     )
        WP  = int             ( RR [ 3 ]                                     )
        HP  = int             ( RR [ 4 ]                                     )
        DA  = float           ( RR [ 5 ]                                     )
        ######################################################################
        NS  = f"{PU}\n({XP},{YP},{WP},{HP})\n{DA}"
        ######################################################################
        NAMEs [ UUID ] = NS
    ##########################################################################
    return NAMEs
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
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "face/uuids"
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
  def Prepare                  ( self                                      ) :
    ##########################################################################
    self . assignSelectionMode ( "ContiguousSelection"                       )
    self . setPrepared         ( True                                        )
    ##########################################################################
    return
  ############################################################################
  def AssignWrongPeople               ( self , UUID                        ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . getMenuItem      ( "WrongPeopleFaceUuid"                )
    MSG     = FMT . format            ( UUID                                 )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FRRTAB  = self . Tables           [ "FaceRegions"                        ]
    QQ      = f"""select `states` from {FRRTAB}
                  where ( `uuid` = {UUID} ) ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . Query                   ( QQ                                   )
    RR      = DB . FetchOne           (                                      )
    ##########################################################################
    if                                ( RR not in [ False , None ]         ) :
      ########################################################################
      if                              ( len ( RR ) == 1                    ) :
        ######################################################################
        STA = int                     ( RR [ 0 ]                             )
        ######################################################################
        if                            ( 0 == STA                           ) :
          ####################################################################
          STA = 1
          ####################################################################
        elif                          ( 10000 == STA                       ) :
          ####################################################################
          STA = 10001
        ######################################################################
        QQ  = f"""update {FRRTAB}
                  set `states` = {STA}
                  where ( `uuid` = {UUID} ) ;"""
        QQ  = " " . join              ( QQ . split ( )                       )
        DB  . Query                   ( QQ                                   )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    self    . Notify                  ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def AssignCorrectFace               ( self , UUID                        ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . getMenuItem      ( "AssignCorrectFace"                  )
    MSG     = FMT . format            ( UUID                                 )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FRRTAB  = self . Tables           [ "FaceRegions"                        ]
    QQ      = f"""update {FRRTAB}
                  set `states` = 20000
                  where ( `uuid` = {UUID} ) ;"""
    QQ      = " " . join              ( QQ . split ( )                       )
    DB      . Query                   ( QQ                                   )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    self    . Notify                  ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def AssignSelectedCorrectFace       ( self , UUIDs                       ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self    . Notify                  ( 3                                    )
    ##########################################################################
    FMT     = self . getMenuItem      ( "AssignCorrectFace"                  )
    MSG     = FMT . format            ( len ( UUIDs )                        )
    self    . ShowStatus              ( MSG                                  )
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FRRTAB  = self . Tables           [ "FaceRegions"                        ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""update {FRRTAB}
                  set `states` = 20000
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      DB    . Query                   ( QQ                                   )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    self    . ShowStatus              ( ""                                   )
    DB      . Close                   (                                      )
    ##########################################################################
    self    . Notify                  ( 5                                    )
    ##########################################################################
    return
  ############################################################################
  def EditFacePicture                   ( self , UUID                      ) :
    ##########################################################################
    DB       = self . ConnectDB         (                                    )
    if                                  ( DB == None                       ) :
      return
    ##########################################################################
    self     . Notify                   ( 3                                  )
    ##########################################################################
    PUID     = 0
    ##########################################################################
    FRRTAB   = self . Tables            [ "FaceRegions"                      ]
    QQ       = f"""select `picture` from {FRRTAB}
                  where ( `uuid` = {UUID} ) ;"""
    QQ       = " " . join               ( QQ . split ( )                     )
    DB       . Query                    ( QQ                                 )
    RR       = DB . FetchOne            (                                    )
    ##########################################################################
    if                                  ( RR not in [ False , None ]       ) :
      ########################################################################
      if                                ( len ( RR ) == 1                  ) :
        ######################################################################
        PUID = int                      ( RR [ 0                           ] )
    ##########################################################################
    DB       . Close                    (                                    )
    ##########################################################################
    self     . Notify                   ( 5                                  )
    ##########################################################################
    if                                  ( PUID > 0                         ) :
      ########################################################################
      self   . OpenPictureEditor . emit ( str(PUID) , self . PictureTables   )
    ##########################################################################
    return
  ############################################################################
  def RotateFaceRecognition ( self                                         ) :
    ##########################################################################
    Host    = "http://iosdb.oriphase.com:8364"
    UUIDs   = getUuids      (                                                )
    ##########################################################################
    if                      ( len ( UUIDs ) <= 0                           ) :
      return
    ##########################################################################
    CMD     = f"{Host}/People"
    Headers = { "Username" : "foxman"                                      , \
                "Password" : "actionsfox2019"                                }
    JSON    = { "Action"   : "DeepRotateFaces"                             , \
                "Faces"    : UUIDs                                           }
    ##########################################################################
    try                                                                      :
      requests . post       ( CMD                                            ,
                              data    = json . dumps ( JSON )                ,
                              headers = Headers                              )
    except                                                                   :
      pass
    ##########################################################################
    self . Notify           ( 5                                              )
    ##########################################################################
    return
  ############################################################################
  def DetectFaceControlPoints ( self                                       ) :
    ##########################################################################
    Host    = "http://iosdb.oriphase.com:8364"
    UUIDs   = getUuids        (                                              )
    ##########################################################################
    if                        ( len ( UUIDs ) <= 0                         ) :
      return
    ##########################################################################
    CMD     = f"{Host}/People"
    Headers = { "Username" : "foxman"                                      , \
                "Password" : "actionsfox2019"                                }
    JSON    = { "Action"   : "FaceMeshPoints"                              , \
                "Faces"    : UUIDs                                           }
    ##########################################################################
    try                                                                      :
      requests . post         ( CMD                                          ,
                                data    = json . dumps ( JSON )              ,
                                headers = Headers                            )
    except                                                                   :
      pass
    ##########################################################################
    self . Notify             ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def ReloadLocality               ( self , DB                             ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def StatesMenu              ( self , mm                                  ) :
    ##########################################################################
    TRX = self . Translations [ "FaceView" ] [ "States"                      ]
    ##########################################################################
    MSG = self . getMenuItem  ( "RecognitionStates"                          )
    COL = mm . addMenu        ( MSG                                          )
    ##########################################################################
    CHK =                     ( "0"     in self . STATEs                     )
    msg = TRX                 [ "0"                                          ]
    mm  . addActionFromMenu   ( COL , 43521001 , msg , True , CHK            )
    ##########################################################################
    CHK =                     ( "1"     in self . STATEs                     )
    msg = TRX                 [ "1"                                          ]
    mm  . addActionFromMenu   ( COL , 43521002 , msg , True , CHK            )
    ##########################################################################
    CHK =                     ( "10000" in self . STATEs                     )
    msg = TRX                 [ "10000"                                      ]
    mm  . addActionFromMenu   ( COL , 43521003 , msg , True , CHK            )
    ##########################################################################
    CHK =                     ( "10001" in self . STATEs                     )
    msg = TRX                 [ "10001"                                      ]
    mm  . addActionFromMenu   ( COL , 43521004 , msg , True , CHK            )
    ##########################################################################
    CHK =                     ( "20000" in self . STATEs                     )
    msg = TRX                 [ "20000"                                      ]
    mm  . addActionFromMenu   ( COL , 43521005 , msg , True , CHK            )
    ##########################################################################
    return mm
  ############################################################################
  def RunStatesMenu           ( self , at                                  ) :
    ##########################################################################
    if                        ( at == 43521001                             ) :
      ########################################################################
      self . SwitchFaceStates ( "0"                                          )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 43521002                             ) :
      ########################################################################
      self . SwitchFaceStates ( "1"                                          )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 43521003                             ) :
      ########################################################################
      self . SwitchFaceStates ( "10000"                                      )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 43521004                             ) :
      ########################################################################
      self . SwitchFaceStates ( "10001"                                      )
      ########################################################################
      return True
    ##########################################################################
    if                        ( at == 43521005                             ) :
      ########################################################################
      self . SwitchFaceStates ( "20000"                                      )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu               ( self , mm , uuid , item                   ) :
    ##########################################################################
    if                         ( uuid <= 0                                 ) :
      return mm
    ##########################################################################
    TRX = self . Translations
    FMT = self . getMenuItem   ( "Belongs"                                   )
    MSG = FMT  . format        ( str ( uuid )                                )
    LOM = mm   . addMenu       ( MSG                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "CopyFaceUuid"                              )
    mm  . addActionFromMenu    ( LOM , 24231101 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "AppendFaceUuid"                            )
    mm  . addActionFromMenu    ( LOM , 24231102 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "AppendFaceUuids"                           )
    mm  . addActionFromMenu    ( LOM , 24231103 , msg                        )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "WrongPeopleFace"                           )
    mm  . addActionFromMenu    ( LOM , 24231201 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "AssignCorrectFace"                         )
    mm  . addActionFromMenu    ( LOM , 24231202 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "AssignSelectedCorrect"                     )
    mm  . addActionFromMenu    ( LOM , 24231203 , msg                        )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "EditFacePicture"                           )
    mm  . addActionFromMenu    ( LOM , 24231301 , msg                        )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "RotateFaceRecognition"                     )
    mm  . addActionFromMenu    ( LOM , 24231401 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "DetectFaceControlPoints"                   )
    mm  . addActionFromMenu    ( LOM , 24231402 , msg                        )
    ##########################################################################
    msg = self . getMenuItem   ( "SearchThisFace"                            )
    mm  . addActionFromMenu    ( LOM , 24231403 , msg                        )
    ##########################################################################
    mm  . addSeparatorFromMenu ( LOM                                         )
    ##########################################################################
    msg = self . getMenuItem   ( "VtkRawFace"                                )
    mm  . addActionFromMenu    ( LOM , 24231501 , msg                        )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , uuid , item              ) :
    ##########################################################################
    if                              ( at == 24231101                       ) :
      ########################################################################
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231102                       ) :
      ########################################################################
      appendUuid                    ( uuid                                   )
      self . Notify                 ( 5                                      )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231103                       ) :
      ########################################################################
      items = self . selectedItems  (                                        )
      ########################################################################
      for it in items                                                        :
        ######################################################################
        UUIX = it . data            ( Qt . UserRole                          )
        appendUuid                  ( UUIX                                   )
      ########################################################################
      self . Notify                 ( 5                                      )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231201                       ) :
      ########################################################################
      self . Go                     ( self . AssignWrongPeople , ( uuid , )  )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231202                       ) :
      ########################################################################
      self . Go                     ( self . AssignCorrectFace , ( uuid , )  )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231203                       ) :
      ########################################################################
      items = self . selectedItems  (                                        )
      UUIDs =                       [                                        ]
      ########################################################################
      for it in items                                                        :
        ######################################################################
        UUIX = it . data            ( Qt . UserRole                          )
        UUIDs . append              ( UUIX                                   )
      ########################################################################
      self . Go                     ( self . AssignSelectedCorrectFace     , \
                                      ( UUIDs , )                            )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231301                       ) :
      ########################################################################
      self . Go                     ( self . EditFacePicture , ( uuid , )    )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231401                       ) :
      ########################################################################
      self . Go                     ( self . RotateFaceRecognition           )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231402                       ) :
      ########################################################################
      self . Go                     ( self . DetectFaceControlPoints         )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231403                       ) :
      ########################################################################
      self . SearchFaces . emit     ( str ( uuid )                           )
      ########################################################################
      return
    ##########################################################################
    if                              ( at == 24231501                       ) :
      ########################################################################
      head = self . windowTitle     (                                        )
      icon = self . windowIcon      (                                        )
      xsid = str                    ( uuid                                   )
      ########################################################################
      self . ShowRawFace . emit     ( head , xsid , icon                     )
      ########################################################################
      return
    ##########################################################################
    return False
  ############################################################################
  def SigmaMenu                       ( self , mm                          ) :
    ##########################################################################
    MSG  = self . getMenuItem         ( "FaceSigma:"                         )
    ##########################################################################
    self . SigmaSpin = QDoubleSpinBox (                                      )
    self . SigmaSpin . setPrefix      ( MSG                                  )
    self . SigmaSpin . setRange       ( 0 , 100                              )
    self . SigmaSpin . setValue       ( self . Sigma                         )
    self . SigmaSpin . setSingleStep  ( 0.0001                               )
    self . SigmaSpin . setDecimals    ( 6                                    )
    self . SigmaSpin . setAlignment   ( Qt . AlignRight                      )
    ##########################################################################
    mm   . addWidget                  ( 9999912 , self . SigmaSpin           )
    ##########################################################################
    mm   . addSeparator               (                                      )
    ##########################################################################
    return mm
  ############################################################################
  def RunSigmaMenu                          ( self                         ) :
    ##########################################################################
    if                                      ( self . SigmaSpin == None     ) :
      return False
    ##########################################################################
    self . Sigma = self . SigmaSpin . value (                                )
    ##########################################################################
    return   False
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
    if                                 ( "Search" == self . Method         ) :
      ########################################################################
      self . SigmaMenu                 ( mm                                  )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . AmountIndexMenu           ( mm                                  )
    ##########################################################################
    self   . AppendRefreshAction       ( mm , 1001                           )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . GroupsMenu                ( mm , uuid , atItem                  )
    self   . StatesMenu                ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    if                                 ( "Search" == self . Method         ) :
      ########################################################################
      self . RunSigmaMenu              (                                     )
      ########################################################################
    else                                                                     :
      ########################################################################
      OKAY = self . RunAmountIndexMenu (                                     )
      if                               ( OKAY                              ) :
        ######################################################################
        self . restart                 (                                     )
        ######################################################################
        return True
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( self . RunStatesMenu ( at )       ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . RunGroupsMenu      ( at , uuid , atItem                  )
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
