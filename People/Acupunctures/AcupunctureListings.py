# -*- coding: utf-8 -*-
##############################################################################
## AcupunctureListings
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
from   AITK  . People     . People    import People
##############################################################################
from   opencc                         import OpenCC
##############################################################################
class AcupunctureListings  ( TreeDock                                      ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow       = pyqtSignal (                                         )
  emitAllNames        = pyqtSignal ( dict                                    )
  emitAssignAmounts   = pyqtSignal ( str , int , int                         )
  PeopleGroup         = pyqtSignal ( str , int , str                         )
  ShowPersonalGallery = pyqtSignal ( str , int , str , QIcon                 )
  OpenVariantTables   = pyqtSignal ( str , str , int , str , dict            )
  OpenLogHistory      = pyqtSignal ( str , str , str , str , str             )
  ############################################################################
  def __init__             ( self , parent = None , plan = None            ) :
    ##########################################################################
    super ( ) . __init__   (        parent        , plan                     )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "AcupunctureListings"
    self . FetchTableKey      = "AcupunctureListings"
    self . GType              = 17
    self . SortOrder          = "asc"
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . set          ( "first" , 0                             )
    self . Relation . setT2        ( "Acupuncture"                           )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 3                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnHidden         ( 2 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
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
    return self . SizeSuggestion ( QSize ( 240 , 360 )                       )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    self . AppendToolNamingAction (                                          )
    ##########################################################################
    self . AppendWindowToolSeparatorAction (                                 )
    ##########################################################################
    msg  = self . getMenuItem     ( "AcupunctureGallery"                     )
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/gallery.png" )         )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . GotoItemGallery                   )
    self . WindowActions . append ( A                                        )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                            Enabled  ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup           , Enabled    )
    self . LinkAction ( "Copy"       , self . CopyToClipboard   , Enabled    )
    self . LinkAction ( "Paste"      , self . PasteAcupunctures , Enabled    )
    self . LinkAction ( "Select"     , self . SelectOne         , Enabled    )
    self . LinkAction ( "SelectAll"  , self . SelectAll         , Enabled    )
    self . LinkAction ( "SelectNone" , self . SelectNone        , Enabled    )
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
    self . LinkVoice         ( self . CommandParser                          )
    ##########################################################################
    return True
  ############################################################################
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . LinkVoice         ( None                                          )
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
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery     ( self                                          ) :
    ##########################################################################
    ACUTAB = self . Tables [ "Acupunctures"                                  ]
    ORDER  = self . SortOrder
    ##########################################################################
    QQ     = f"select `uuid` from {ACUTAB} order by `id` {ORDER} ;"
    ##########################################################################
    return QQ
  ############################################################################
  def ObtainUuidsFromGroup ( self , DB                                     ) :
    ##########################################################################
    RELTAB = self . Tables [ "RelationPathway"                               ]
    ##########################################################################
    return self . Relation . Subordination ( DB , RELTAB                     )
  ############################################################################
  def ObtainsInformation  ( self , DB                                      ) :
    ##########################################################################
    self . ReloadLocality (        DB                                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem               ( self , UUID , NAME                       ) :
    ##########################################################################
    IT = self . PrepareUuidItem ( 0    , UUID , NAME                         )
    IT . setTextAlignment       ( 1    , Qt . AlignRight                     )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                (        str  , int     , int                     )
  def AssignAmounts        ( self , UUID , Amounts , Column                ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT in [ False , None ]                        ) :
      return
    ##########################################################################
    IT . setText           ( Column , str ( Amounts )                        )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                ( self , UUIDs                       ) :
    ##########################################################################
    time   . sleep                    ( 1.0                                  )
    ##########################################################################
    RELTAB = self . Tables            [ "RelationPeople"                     ]
    REL    = Relation                 (                                      )
    REL    . setT1                    ( "Hairs"                              )
    REL    . setT2                    ( "People"                             )
    REL    . setRelation              ( "Subordination"                      )
    ##########################################################################
    DB     = self . ConnectDB         (                                      )
    ##########################################################################
    if                                ( self . NotOkay ( DB )              ) :
      return
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      if                              ( not self . StayAlive               ) :
        continue
      ########################################################################
      REL  . set                      ( "first" , UUID                       )
      CNT  = REL . CountSecond        ( DB , RELTAB                          )
      ########################################################################
      self . emitAssignAmounts . emit ( str ( UUID ) , CNT , 1               )
    ##########################################################################
    self   . GoRelax . emit           (                                      )
    DB     . Close                    (                                      )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        dict                              )
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    NAMEs  = JSON                 [ "NAMEs"                                  ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U , NAMEs [ U ]                          )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    self   . setEnabled           ( True                                     )
    self   . emitNamesShow . emit (                                          )
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
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    FMT     = self . Translations     [ "UI::StartLoading"                   ]
    MSG     = FMT . format            ( self . windowTitle ( )               )
    self    . ShowStatus              ( MSG                                  )
    ##########################################################################
    self    . ObtainsInformation      ( DB                                   )
    if                                ( self . Relation . First > 0        ) :
      UUIDs = self . ObtainUuidsFromGroup ( DB                               )
    else                                                                     :
      UUIDs = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
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
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
    ##########################################################################
    self   . Notify                   ( 5                                    )
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
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "acupuncture/uuids"
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
  def allowedMimeTypes     ( self , mime                                   ) :
    ##########################################################################
    formats = "picture/uuids"
    ##########################################################################
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def DecideDropItems                    ( self                            , \
                                           sourceWidget                    , \
                                           mtype                           , \
                                           UUIDs                           , \
                                           HUID                            , \
                                           NAME                            ) :
    ##########################################################################
    if                                   ( mtype in [ "picture/uuids" ]    ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "GetPictures"                     )
      MSG   = FMT  . format              ( title , CNT , NAME                )
      ########################################################################
      self  . ShowStatus                 ( MSG                               )
    ##########################################################################
    return
  ############################################################################
  def HandleDropIn                      ( self                             , \
                                          sourceWidget                     , \
                                          mimeData                         , \
                                          mousePos                         , \
                                          Newbie                           ) :
    ##########################################################################
    if                                  ( self == sourceWidget             ) :
      return False
    ##########################################################################
    GDN         = False
    RDN         = False
    if                                  ( Newbie                           ) :
      GDN       = True
    elif                                ( "Mime" not in self . DropInJSON  ) :
      GDN       = True
    else                                                                     :
      RDN       = True
    ##########################################################################
    if                                  ( GDN                              ) :
      ########################################################################
      RDN       = self . RegularDropNew ( mimeData                           )
      if                                ( not RDN                          ) :
        return False
    ##########################################################################
    HUID , NAME = self . itemAtPos      ( mousePos , 0 , 0                   )
    if                                  ( HUID <= 0                        ) :
      return False
    ##########################################################################
    mtype       = self . DropInJSON     [ "Mime"                             ]
    UUIDs       = self . DropInJSON     [ "UUIDs"                            ]
    ##########################################################################
    self        . DecideDropItems       ( sourceWidget                     , \
                                          mtype                            , \
                                          UUIDs                            , \
                                          HUID                             , \
                                          NAME                               )
    ##########################################################################
    return RDN
  ############################################################################
  def dropNew                  ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    return self . HandleDropIn ( sourceWidget , mimeData , mousePos , True   )
  ############################################################################
  def dropMoving               ( self , sourceWidget , mimeData , mousePos ) :
    ##########################################################################
    return self . HandleDropIn ( sourceWidget , mimeData , mousePos , False  )
  ############################################################################
  def acceptPictureDrop        ( self                                      ) :
    return True
  ############################################################################
  def dropPictures                 ( self , source , pos , JSON            ) :
    ##########################################################################
    HUID , NAME = self . itemAtPos ( pos , 0 , 0                             )
    if                             ( HUID <= 0                             ) :
      return True
    ##########################################################################
    self . Go ( self . PicturesAppending , ( HUID , NAME , JSON , )          )
    ##########################################################################
    return True
  ############################################################################
  def PicturesAppending      ( self , atUuid , NAME , JSON                 ) :
    ##########################################################################
    T1   = "Acupuncture"
    TAB  = "RelationPictures"
    ##########################################################################
    self . AppendingPictures (        atUuid , NAME , JSON , TAB , T1        )
    ##########################################################################
    return
  ############################################################################
  def OpenItemGallery                 ( self , item                        ) :
    ##########################################################################
    uuid = item . data                ( 0 , Qt . UserRole                    )
    uuid = int                        ( uuid                                 )
    text = item . text                ( 0                                    )
    icon = self . windowIcon          (                                      )
    xsid = str                        ( uuid                                 )
    ##########################################################################
    self . ShowPersonalGallery . emit ( text , 20 , xsid , icon              )
    ##########################################################################
    return
  ############################################################################
  def GotoItemGallery           ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemGallery    ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemCrowd           ( self , item                                ) :
    ##########################################################################
    uuid = item . data        ( 0 , Qt . UserRole                            )
    uuid = int                ( uuid                                         )
    xsid = str                ( uuid                                         )
    text = item . text        ( 0                                            )
    ##########################################################################
    self . PeopleGroup . emit ( text , self . GType , str ( uuid )           )
    ##########################################################################
    return
  ############################################################################
  def GotoItemCrowd             ( self                                     ) :
    ##########################################################################
    atItem = self . currentItem (                                            )
    if                          ( self . NotOkay ( atItem )                ) :
      return
    ##########################################################################
    self   . OpenItemCrowd      ( atItem                                     )
    ##########################################################################
    return
  ############################################################################
  def OpenItemNamesEditor             ( self , item                        ) :
    ##########################################################################
    self . defaultOpenItemNamesEditor ( item                                 ,
                                        0                                    ,
                                        "Acupunctures"                       ,
                                        "NamesEditing"                       )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard ( False                                         )
    ##########################################################################
    return
  ############################################################################
  def PasteAcupunctures ( self                                             ) :
    ##########################################################################
    self . defaultPaste ( self . ImportAcupuncturesFromText                  )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 2                              )
    ##########################################################################
    return
  ############################################################################
  def FindAcupuncture           ( self , DB , NAME                         ) :
    ##########################################################################
    LOC    = self . getLocality (                                            )
    ACUTAB = self . Tables      [ "Acupunctures"                             ]
    NAMTAB = self . Tables      [ "Names"                                    ]
    ##########################################################################
    QA     = f"select `uuid` from {ACUTAB}"
    QQ     = f"""select `uuid` from {NAMTAB}
                    where ( `locality` = {LOC} )
                    and ( `uuid` in ( {QA} ) )
                    and ( `name` = %s )
                    order by `priority` asc
                    limit 0 , 1 ;"""
    QQ     = " " . join         ( QQ . split ( )                             )
    DB     . QueryValues        ( QQ , ( NAME , )                            )
    RR     = DB . FetchOne      (                                            )
    ##########################################################################
    if                          ( RR in [ False , None ]                   ) :
      return 0
    ##########################################################################
    if                          ( len ( RR ) != 1                          ) :
      return 0
    ##########################################################################
    return int                  ( RR [ 0 ]                                   )
  ############################################################################
  def AssureAcupunctures             ( self , DB , NAME                    ) :
    ##########################################################################
    UUID    = self . FindAcupuncture (        DB , NAME                      )
    ##########################################################################
    if                               ( UUID > 0                            ) :
      return UUID
    ##########################################################################
    LOC     = self . getLocality     (                                       )
    ACUTAB  = self . Tables          [ "Acupunctures"                        ]
    NAMTAB  = self . Tables          [ "NamesEditing"                        ]
    ##########################################################################
    Heading = 5433123000000040000
    UUID    = DB . LastUuid          ( ACUTAB , "uuid" , Heading             )
    ##########################################################################
    QQ      = f"""insert into {ACUTAB}
                  ( `uuid` , `type` )
                  values
                  ( {UUID} , 1 ) ;"""
    QQ      = " " . join             ( QQ . split ( )                        )
    DB      . Query                  ( QQ                                    )
    ##########################################################################
    self    . AssureUuidName         ( DB , NAMTAB , UUID , NAME             )
    ##########################################################################
    return UUID
  ############################################################################
  def ImportAcupunctures               ( self , LINES                      ) :
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    if                                 ( DB == None                        ) :
      return
    ##########################################################################
    self    . Notify                   ( 3                                   )
    self    . OnBusy  . emit           (                                     )
    self    . setBustle                (                                     )
    ##########################################################################
    FMT     = self . Translations      [ "UI::StartLoading"                  ]
    MSG     = FMT . format             ( self . windowTitle ( )              )
    self    . ShowStatus               ( MSG                                 )
    ##########################################################################
    RELTAB  = self . Tables            [ "RelationPathway"                   ]
    UUIDs   =                          [                                     ]
    ##########################################################################
    for NAME in LINES                                                        :
      ########################################################################
      UUID = self . AssureAcupunctures ( DB , NAME                           )
      ########################################################################
      if                               ( UUID not in UUIDs                 ) :
        UUIDs . append                 ( UUID                                )
    ##########################################################################
    if                                 ( self . Relation . First > 0       ) :
      ########################################################################
      if                               ( len ( UUIDs ) > 0                 ) :
        ######################################################################
        self . Relation . Joins        ( DB , RELTAB , UUIDs                 )
    ##########################################################################
    self    . setVacancy               (                                     )
    self    . GoRelax . emit           (                                     )
    self    . ShowStatus               ( ""                                  )
    DB      . Close                    (                                     )
    ##########################################################################
    self    . loading                  (                                     )
    ##########################################################################
    return
  ############################################################################
  def ImportAcupuncturesFromText   ( self , TEXT                           ) :
    ##########################################################################
    LINEX     = TEXT . splitlines  (                                         )
    if                             ( len ( LINEX ) <= 0                    ) :
      return
    ##########################################################################
    LINES     =                    [                                         ]
    ##########################################################################
    for L in LINEX                                                           :
      ########################################################################
      S       = L .  strip         (                                         )
      K       = S . rstrip         (                                         )
      ########################################################################
      if                           ( len ( K ) > 0                         ) :
        LINES . append             ( K                                       )
    ##########################################################################
    self      . ImportAcupunctures ( LINES                                   )
    ##########################################################################
    return
  ############################################################################
  def UpdateLocalityUsage       ( self                                     ) :
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return False
    ##########################################################################
    PAMTAB = self . Tables      [ "Parameters"                               ]
    DB     . LockWrites         ( [ PAMTAB                                 ] )
    ##########################################################################
    self   . SetLocalityByUuid  ( DB                                       , \
                                  PAMTAB                                   , \
                                  0                                        , \
                                  self . GType                             , \
                                  self . ClassTag                            )
    ##########################################################################
    DB     . UnlockTables       (                                            )
    DB     . Close              (                                            )
    self   . emitRestart . emit (                                            )
    ##########################################################################
    return True
  ############################################################################
  def ReloadLocality           ( self , DB                                 ) :
    ##########################################################################
    PAMTAB = self . Tables     [ "Parameters"                                ]
    self   . GetLocalityByUuid ( DB                                        , \
                                 PAMTAB                                    , \
                                 0                                         , \
                                 self . GType                              , \
                                 self . ClassTag                             )
    ##########################################################################
    return
  ############################################################################
  def CommandParser ( self , language , message , timestamp                ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectNone"   , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    return          { "Match" : False                                        }
  ############################################################################
  def FunctionsMenu                  ( self , mm , uuid , item             ) :
    ##########################################################################
    msg  = self . getMenuItem        ( "Functions"                           )
    LOM  = mm   . addMenu            ( msg                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "AssignTables"                        )
    mm   . addActionFromMenu         ( LOM , 25351301 , msg                  )
    ##########################################################################
    return mm
  ############################################################################
  def RunFunctionsMenu                 ( self , at , uuid , item           ) :
    ##########################################################################
    if                                 ( at == 25351301                    ) :
      ########################################################################
      TITLE = self . windowTitle       (                                     )
      ########################################################################
      self  . OpenVariantTables . emit ( str ( TITLE )                     , \
                                         "0"                               , \
                                         self . GType                      , \
                                         self . FetchTableKey              , \
                                         self . Tables                       )
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
    if                             ( at >= 9001 ) and ( at <= 9002 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      if                           ( ( at in [ 9001 ] ) and ( hid )        ) :
        ######################################################################
        self . restart             (                                         )
        ######################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def GroupsMenu                     ( self , mm , item                    ) :
    ##########################################################################
    if                               ( self . NotOkay ( item )             ) :
      return mm
    ##########################################################################
    TRX  = self . Translations
    NAME = item . text               ( 0                                     )
    FMT  = TRX                       [ "UI::Belongs"                         ]
    MSG  = FMT . format              ( NAME                                  )
    COL  = mm . addMenu              ( MSG                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "CopyAcupunctureUuid"                 )
    mm   . addActionFromMenu         ( COL , 38521001 , msg                  )
    ##########################################################################
    mm   . addSeparatorFromMenu      ( COL                                   )
    ##########################################################################
    msg  = self . getMenuItem        ( "AcupunctureGallery"                  )
    ICON = QIcon                     ( ":/images/gallery.png"                )
    mm   . addActionFromMenuWithIcon ( COL , 38521002 , ICON , msg           )
    ##########################################################################
    msg  = self . getMenuItem        ( "Description"                         )
    mm   . addActionFromMenu         ( COL , 38522001        , msg           )
    ##########################################################################
    return mm
  ############################################################################
  def RunGroupsMenu                 ( self , at , item                     ) :
    ##########################################################################
    if                              ( at == 38521001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      qApp . clipboard ( ). setText ( f"{uuid}"                              )
      self . Notify                 ( 5                                      )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38521002                       ) :
      ########################################################################
      self . OpenItemGallery        ( item                                   )
      ########################################################################
      return True
    ##########################################################################
    if                              ( at == 38522001                       ) :
      ########################################################################
      uuid = item . data            ( 0 , Qt . UserRole                      )
      uuid = int                    ( uuid                                   )
      head = item . text            ( 0                                      )
      LOC  = self . getLocality     (                                        )
      nx   = ""
      ########################################################################
      if                            ( "Notes" in self . Tables             ) :
        nx = self . Tables          [ "Notes"                                ]
      ########################################################################
      self . OpenLogHistory . emit  ( head                                   ,
                                      str ( uuid )                           ,
                                      "Description"                          ,
                                      nx                                     ,
                                      str ( LOC  )                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    if                                 ( not self . isPrepared ( )         ) :
      return False
    ##########################################################################
    doMenu = self . isFunction         ( self . HavingMenu                   )
    if                                 ( not doMenu                        ) :
      return False
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager               ( self                                )
    ##########################################################################
    self   . AppendRefreshAction       (          mm , 1001                  )
    self   . TryAppendEditNamesAction  ( atItem , mm , 1601                  )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . FunctionsMenu             ( mm , uuid , atItem                  )
    self   . GroupsMenu                ( mm ,        atItem                  )
    self   . ColumnsMenu               ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    OKAY   = self . RunDocking         ( mm , aa                             )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunFunctionsMenu   ( at , uuid , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . HandleLocalityMenu ( at                                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    OKAY   = self . RunColumnsMenu     ( at                                  )
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
    OKAY   = self . RunGroupsMenu      ( at , atItem                         )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 1001                        ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    return True
##############################################################################
