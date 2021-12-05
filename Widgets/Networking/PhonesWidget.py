# -*- coding: utf-8 -*-
##############################################################################
## PhonesWidget
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
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
from   AITK  . Telecom    . Phone     import Phone       as TelecomPhone
##############################################################################
FLAGs = [ "AD.png" , "AE.png" , "AF.png" , "AG.png" , "AI.png" , "AL.png" ,  \
          "AM.png" , "AO.png" , "AQ.png" , "AR.png" , "AS.png" , "AT.png" ,  \
          "AU.png" , "AW.png" , "AX.png" , "AZ.png" , "BA.png" , "BB.png" ,  \
          "BD.png" , "BE.png" , "BF.png" , "BG.png" , "BH.png" , "BI.png" ,  \
          "BJ.png" , "BL.png" , "BM.png" , "BN.png" , "BO.png" , "BR.png" ,  \
          "BS.png" , "BT.png" , "BV.png" , "BW.png" , "BY.png" , "BZ.png" ,  \
          "CA.png" , "CC.png" , "CD.png" , "CF.png" , "CG.png" , "CH.png" ,  \
          "CI.png" , "CK.png" , "CL.png" , "CM.png" , "CN.png" , "CO.png" ,  \
          "CR.png" , "CU.png" , "CV.png" , "CW.png" , "CX.png" , "CY.png" ,  \
          "CZ.png" , "DE.png" , "DJ.png" , "DK.png" , "DM.png" , "DO.png" ,  \
          "DZ.png" , "EC.png" , "EE.png" , "EG.png" , "EH.png" , "ER.png" ,  \
          "ES.png" , "ET.png" , "FI.png" , "FJ.png" , "FK.png" , "FM.png" ,  \
          "FO.png" , "FR.png" , "GA.png" , "GB.png" , "GD.png" , "GE.png" ,  \
          "GF.png" , "GG.png" , "GH.png" , "GI.png" , "GL.png" , "GM.png" ,  \
          "GN.png" , "GP.png" , "GQ.png" , "GR.png" , "GS.png" , "GT.png" ,  \
          "GU.png" , "GW.png" , "GY.png" , "HK.png" , "HM.png" , "HN.png" ,  \
          "HR.png" , "HT.png" , "HU.png" , "ID.png" , "IE.png" , "IL.png" ,  \
          "IM.png" , "IN.png" , "IO.png" , "IQ.png" , "IR.png" , "IS.png" ,  \
          "IT.png" , "JE.png" , "JM.png" , "JO.png" , "JP.png" , "KE.png" ,  \
          "KG.png" , "KH.png" , "KI.png" , "KM.png" , "KN.png" , "KP.png" ,  \
          "KR.png" , "KW.png" , "KY.png" , "KZ.png" , "LA.png" , "LB.png" ,  \
          "LC.png" , "LI.png" , "LK.png" , "LR.png" , "LS.png" , "LT.png" ,  \
          "LU.png" , "LV.png" , "LY.png" , "MA.png" , "MC.png" , "MD.png" ,  \
          "ME.png" , "MF.png" , "MG.png" , "MH.png" , "MK.png" , "ML.png" ,  \
          "MM.png" , "MN.png" , "MO.png" , "MP.png" , "MQ.png" , "MR.png" ,  \
          "MS.png" , "MT.png" , "MU.png" , "MV.png" , "MW.png" , "MX.png" ,  \
          "MY.png" , "MZ.png" , "NA.png" , "NC.png" , "NE.png" , "NF.png" ,  \
          "NG.png" , "NI.png" , "NL.png" , "NO.png" , "NP.png" , "NR.png" ,  \
          "NU.png" , "NZ.png" , "OM.png" , "PA.png" , "PE.png" , "PF.png" ,  \
          "PG.png" , "PH.png" , "PK.png" , "PL.png" , "PM.png" , "PN.png" ,  \
          "PR.png" , "PS.png" , "PT.png" , "PW.png" , "PY.png" , "QA.png" ,  \
          "RE.png" , "RO.png" , "RS.png" , "RU.png" , "RW.png" , "SA.png" ,  \
          "SB.png" , "SC.png" , "SD.png" , "SE.png" , "SG.png" , "SH.png" ,  \
          "SI.png" , "SJ.png" , "SK.png" , "SL.png" , "SM.png" , "SN.png" ,  \
          "SO.png" , "SR.png" , "SS.png" , "ST.png" , "SV.png" , "SY.png" ,  \
          "SZ.png" , "TC.png" , "TD.png" , "TF.png" , "TG.png" , "TH.png" ,  \
          "TJ.png" , "TK.png" , "TL.png" , "TM.png" , "TN.png" , "TO.png" ,  \
          "TR.png" , "TT.png" , "TV.png" , "TW.png" , "TZ.png" , "UA.png" ,  \
          "UG.png" , "UM.png" , "US.png" , "UY.png" , "UZ.png" , "VA.png" ,  \
          "VC.png" , "VE.png" , "VG.png" , "VI.png" , "VN.png" , "VU.png" ,  \
          "WF.png" , "WS.png" , "YE.png" , "YT.png" , "ZA.png" , "ZM.png" ,  \
          "ZW.png"                                                           ]
##############################################################################
class PhonesWidget                 ( TreeDock                              ) :
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
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . SortOrder          = "desc"
    self . DbProfile          = ""
    self . SearchLine         = None
    self . SearchKey          = ""
    self . UUIDs              = [                                            ]
    ##########################################################################
    self . Grouping           = "Original"
    self . OldGrouping        = "Original"
    ## self . Grouping           = "Subordination"
    ## self . Grouping           = "Reverse"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . Relation = Relation     (                                         )
    self . Relation . setT2        ( "Phone"                                 )
    self . Relation . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . OwnRel   = Relation     (                                         )
    self . OwnRel   . setT1        ( "People"                                )
    self . OwnRel   . setT2        ( "Phone"                                 )
    self . OwnRel   . setRelation  ( "Subordination"                         )
    ##########################################################################
    self . setColumnCount          ( 12                                      )
    self . setColumnHidden         ( 11 , True                               )
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
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( True                                    )
    self . setDragDropMode         ( QAbstractItemView . DragDrop            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 1024 , 640 )                      )
  ############################################################################
  def setGrouping                  ( self , group                          ) :
    self . Grouping = group
    return self . Grouping
  ############################################################################
  def getGrouping                  ( self                                  ) :
    return self . Grouping
  ############################################################################
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label"      , self . windowTitle ( )            )
    self . LinkAction     ( "Refresh"    , self . startup                    )
    ##########################################################################
    self . LinkAction     ( "Insert"     , self . InsertItem                 )
    self . LinkAction     ( "Delete"     , self . DeleteItems                )
    self . LinkAction     ( "Rename"     , self . RenameItem                 )
    self . LinkAction     ( "Copy"       , self . CopyToClipboard            )
    self . LinkAction     ( "Paste"      , self . Paste                      )
    self . LinkAction     ( "Search"     , self . Search                     )
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
  def FocusOut ( self                                                      ) :
    ##########################################################################
    if         ( not self . isPrepared ( )                                 ) :
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
    if                          ( column not in [ 0 , 1 , 2 , 3 ]          ) :
      return
    ##########################################################################
    if                          ( column in [ 0 , 1 , 2 , 3 ]              ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    return
  ############################################################################
  def getItemJson                 ( self , item                            ) :
    return item . data            ( 9 , Qt . UserRole                        )
  ############################################################################
  def PrepareItem                 ( self , phone                           ) :
    ##########################################################################
    global FLAGs
    ##########################################################################
    CLIST   = self . Translations [ "PhonesWidget" ] [ "Correctness"         ]
    MLIST   = self . Translations [ "PhonesWidget" ] [ "Mobile"              ]
    SLIST   = self . Translations [ "PhonesWidget" ] [ "Shareable"           ]
    FLIST   = self . Translations [ "PhonesWidget" ] [ "Confirm"             ]
    ##########################################################################
    UUID    = int                 ( phone . Uuid                             )
    UXID    = str                 ( UUID                                     )
    ##########################################################################
    PNUMBER = phone . toPhone     (                                          )
    COUNTRY = phone . Country
    AREA    = phone . Area
    NUMBER  = phone . Number
    REGION  = phone . Region
    NATION  = phone . Nation
    ##########################################################################
    CORRECT = CLIST               [ str ( phone . Correct   )                ]
    MOBILE  = MLIST               [ str ( phone . Mobile    )                ]
    SHARE   = SLIST               [ str ( phone . Shareable )                ]
    CONFIRM = FLIST               [ str ( phone . Confirm   )                ]
    ##########################################################################
    IT      = QTreeWidgetItem     (                                          )
    IT      . setText             (  0 , PNUMBER                             )
    IT      . setToolTip          (  0 , UXID                                )
    IT      . setData             (  0 , Qt . UserRole , UXID                )
    ##########################################################################
    IT      . setText             (  1 , COUNTRY                             )
    IT      . setToolTip          (  1 , UXID                                )
    ##########################################################################
    IT      . setText             (  2 , AREA                                )
    IT      . setToolTip          (  2 , UXID                                )
    ##########################################################################
    IT      . setText             (  3 , NUMBER                              )
    IT      . setToolTip          (  3 , UXID                                )
    ##########################################################################
    IT      . setText             (  4 , NATION                              )
    ##########################################################################
    PNG     = f"{REGION}.png"
    if                            ( PNG in FLAGs                           ) :
      K     = QIcon               ( f":/nations/{PNG}"                       )
      IT    . setIcon             (  5 , K                                   )
    ##########################################################################
    IT      . setText             (  6 , CORRECT                             )
    IT      . setText             (  7 , MOBILE                              )
    IT      . setText             (  8 , SHARE                               )
    IT      . setText             (  9 , CONFIRM                             )
    ##########################################################################
    IT      . setText             ( 10 , str ( phone . Owners )              )
    IT      . setTextAlignment    ( 10 , Qt . AlignRight                     )
    ##########################################################################
    IT      . setText             ( 11 , ""                                  )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                   (                                              )
  def InsertItem              ( self                                       ) :
    ##########################################################################
    item = QTreeWidgetItem    (                                              )
    item . setData            ( 0 , Qt . UserRole , 0                        )
    self . addTopLevelItem    ( item                                         )
    line = self . setLineEdit ( item                                       , \
                                0                                          , \
                                "editingFinished"                          , \
                                self . nameChanged                           )
    line . setFocus           ( Qt . TabFocusReason                          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (                                           )
  def DeleteItems                ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return
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
    """
    self   . Go                  ( self . AssureUuidItem                   , \
                                   ( item , uuid , msg , )                   )
    """
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                       (        list                              )
  def refresh                     ( self , PHONEs                          ) :
    ##########################################################################
    self   . clear                (                                          )
    ##########################################################################
    for PHONE in PHONEs                                                      :
      ########################################################################
      IT   = self . PrepareItem   ( PHONE                                    )
      self . addTopLevelItem      ( IT                                       )
    ##########################################################################
    FMT    = self . getMenuItem   ( "DisplayTotal"                           )
    MSG    = FMT  . format        ( len ( PHONEs )                           )
    self   . setToolTip           ( MSG                                      )
    ##########################################################################
    if                            ( self . Grouping in [ "Searching" ]     ) :
      ########################################################################
      T    = self . Translations  [ "PhonesWidget" ] [ "Title"               ]
      K    = self . SearchKey
      T    = f"{T}:{K}"
      ########################################################################
      self . setWindowTitle       ( T                                        )
    ##########################################################################
    self   . emitNamesShow . emit (                                          )
    ##########################################################################
    return
  ############################################################################
  def ObtainSubgroupUuids      ( self , DB                                 ) :
    ##########################################################################
    SID    = self . StartId
    AMOUNT = self . Amount
    ORDER  = self . getSortingOrder ( )
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
  def ObtainsItemUuids         ( self , DB                                 ) :
    ##########################################################################
    if                         ( self . Grouping == "Original"             ) :
      return self . DefaultObtainsItemUuids ( DB                             )
    ##########################################################################
    return self   . ObtainSubgroupUuids     ( DB                             )
  ############################################################################
  def looking                         ( self , name                        ) :
    ##########################################################################
    if                                ( len ( name ) <= 0                  ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    ##########################################################################
    PHSTAB  = self . Tables           [ "Phones"                             ]
    LIKE    = f"%{name}%"
    ORDER   = self . getSortingOrder  (                                      )
    UUIDs   =                         [                                      ]
    ##########################################################################
    QQ      = f"""select `uuid` from {PHSTAB}
                  where ( `number` like %s )
                  order by `uuid` {ORDER} ;"""
    DB      . QueryValues             ( QQ , ( LIKE , )                      )
    ALL     = DB . FetchAll           (                                      )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    DB      . Close                   (                                      )
    ##########################################################################
    if ( ( ALL in [ False , None ] ) or ( len ( ALL ) <= 0 ) )               :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    for U in ALL                                                             :
      UUIDs . append                  ( U [ 0 ]                              )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      ########################################################################
      self  . Notify                  ( 1                                    )
      ########################################################################
      return
    ##########################################################################
    self . SearchKey   = name
    self . UUIDs       = UUIDs
    self . OldGrouping = self . Grouping
    self . setGrouping                ( "Searching"                          )
    ##########################################################################
    self . loading                    (                                      )
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
    self    . OnBusy  . emit          (                                      )
    self    . setBustle               (                                      )
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    if                                ( self . Grouping in [ "Searching" ] ) :
      UUIDs = self . UUIDs
    else                                                                     :
      UUIDs = self . ObtainsItemUuids ( DB                                   )
    ##########################################################################
    PHSTAB  = self . Tables           [ "Phones"                             ]
    CRYTAB  = self . Tables           [ "Countries"                          ]
    PRZTAB  = self . Tables           [ "Properties"                         ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    RELTAB  = self . Tables           [ "Relation"                           ]
    IMACT   =                         [                                      ]
    for U in UUIDs                                                           :
      ########################################################################
      PHONE = TelecomPhone            (                                      )
      PHONE . Uuid = U
      PHONE . ObtainsFullPhone        ( DB , PHSTAB , PRZTAB                 )
      ########################################################################
      if                              ( len ( PHONE . Region ) > 0         ) :
        ######################################################################
        RG  = PHONE . Region
        QQ  = f"select `uuid` from {CRYTAB} where ( `two` = '{RG}' ) ;"
        DB  . Query                   ( QQ                                   )
        RR  = DB . FetchOne           (                                      )
        if ( ( RR not in [ False , None ] ) and ( len ( RR ) == 1 ) )        :
          CUID  = int                 ( RR [ 0 ]                             )
          CNAME = self . GetName      ( DB , NAMTAB , CUID                   )
          PHONE . Nation = CNAME
      ########################################################################
      self  . OwnRel . set            ( "second" , U                         )
      OWNED = self . OwnRel . CountFirst ( DB , RELTAB                       )
      PHONE . Owners = OWNED
      ########################################################################
      IMACT . append                  ( PHONE                                )
    ##########################################################################
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( IMACT ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    self   . emitAllNames . emit      ( IMACT                                )
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
    PHSTAB  = self . Tables [ "Phones"                                       ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"""select `uuid` from {PHSTAB}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    QQ    = " " . join      ( QQ . split ( )                                 )
    ##########################################################################
    return DB . ObtainUuids ( QQ , 0                                         )
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Rename"     , self . RenameItem      , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    self . LinkAction      ( "Paste"      , self . Paste           , False   )
    self . LinkAction      ( "Search"     , self . Search          , False   )
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
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    PHSTAB  = self . Tables           [ "Phones"                             ]
    ##########################################################################
    QQ      = f"select count(*) from {PHSTAB} where ( `used` > 0 ) ;"
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
  def FetchRegularDepotCount ( self , DB                                   ) :
    ##########################################################################
    PHSTAB = self . Tables   [ "Phones"                                      ]
    QQ     = f"select count(*) from {PHSTAB} where ( `used` > 0 ) ;"
    DB     . Query           ( QQ                                            )
    ONE    = DB . FetchOne   (                                               )
    ##########################################################################
    if                       ( ONE == None                                 ) :
      return 0
    ##########################################################################
    if                       ( len ( ONE ) <= 0                            ) :
      return 0
    ##########################################################################
    return ONE               [ 0                                             ]
  ############################################################################
  def FetchGroupMembersCount             ( self , DB                       ) :
    ##########################################################################
    RELTAB = self . Tables               [ "Relation"                        ]
    ##########################################################################
    return self . Relation . CountSecond ( DB , RELTAB                       )
  ############################################################################
  def FetchGroupOwnersCount             ( self , DB                        ) :
    ##########################################################################
    RELTAB = self . Tables              [ "Relation"                         ]
    ##########################################################################
    return self . Relation . CountFirst ( DB , RELTAB                        )
  ############################################################################
  def ObtainUuidsQuery               ( self                                ) :
    ##########################################################################
    PHSTAB  = self . Tables          [ "Phones"                              ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . getSortingOrder (                                       )
    ##########################################################################
    QQ      = f"""select `uuid` from {PHSTAB}
                  where ( `used` > 0 )
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join                ( QQ . split ( )                        )
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
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "people/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                       ( self                                 , \
                                      sourceWidget                         , \
                                      mimeData                             , \
                                      mousePos                             ) :
    ##########################################################################
    if                              ( self == sourceWidget                 ) :
      return False
    ##########################################################################
    RDN     = self . RegularDropNew ( mimeData                               )
    if                              ( not RDN                              ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON     [ "Mime"                                 ]
    UUIDs   = self . DropInJSON     [ "UUIDs"                                ]
    ##########################################################################
    if                              ( mtype in [ "people/uuids" ]          ) :
      ########################################################################
      title = sourceWidget . windowTitle ( )
      CNT   = len                   ( UUIDs                                  )
      MSG   = f"從「{title}」複製{CNT}個人物"
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
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople               ( self , source , pos , JSOX                ) :
    ##########################################################################
    if                         ( "UUIDs" not in JSOX                       ) :
      return True
    ##########################################################################
    UUIDs  = JSOX              [ "UUIDs"                                     ]
    if                         ( len ( UUIDs ) <= 0                        ) :
      return True
    ##########################################################################
    atItem = self . itemAt     ( pos                                         )
    if                         ( atItem is None                            ) :
      return True
    ##########################################################################
    UUID   = atItem . data     ( 0 , Qt . UserRole                           )
    UUID   = int               ( UUID                                        )
    ##########################################################################
    if                         ( UUID <= 0                                 ) :
      return True
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth (  0 , 200                                         )
    self . setColumnWidth (  1 ,  80                                         )
    self . setColumnWidth (  2 ,  80                                         )
    self . setColumnWidth (  3 , 160                                         )
    self . setColumnWidth (  5 ,  60                                         )
    self . setColumnWidth ( 10 , 100                                         )
    self . defaultPrepare ( "PhonesWidget" , 11                              )
    ##########################################################################
    return
  ############################################################################
  def Paste                      ( self                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot            (                                                     )
  def Finding          ( self                                              ) :
    ##########################################################################
    L    = self . SearchLine
    ##########################################################################
    if                 ( L in [ False , None ]                             ) :
      return
    ##########################################################################
    self . SearchLine = None
    T    = L . text    (                                                     )
    L    . deleteLater (                                                     )
    ##########################################################################
    if                 ( len ( T ) <= 0                                    ) :
      return
    ##########################################################################
    self . clear       (                                                     )
    self . Go          ( self . looking , ( T , )                            )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                            (                                     )
  def Search                           ( self                              ) :
    ##########################################################################
    L      = LineEdit                  ( None , self . PlanFunc              )
    OK     = self . attacheStatusBar   ( L , 1                               )
    ##########################################################################
    if                                 ( not OK                            ) :
      ########################################################################
      L    . deleteLater               (                                     )
      self . Notify                    ( 1                                   )
      ########################################################################
      return
    ##########################################################################
    L      . blockSignals              ( True                                )
    L      . editingFinished . connect ( self . Finding                      )
    L      . blockSignals              ( False                               )
    ##########################################################################
    self   . Notify                    ( 0                                   )
    ##########################################################################
    MSG    = self . getMenuItem        ( "Search"                            )
    L      . setPlaceholderText        ( MSG                                 )
    L      . setFocus                  ( Qt . TabFocusReason                 )
    ##########################################################################
    self   . SearchLine = L
    ##########################################################################
    return
  ############################################################################
  def AssureUuidItem               ( self , item , uuid , name             ) :
    ##########################################################################
    """
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TSKTAB  = self . Tables        [ "Tasks"                                 ]
    PRDTAB  = self . Tables        [ "Periods"                               ]
    NAMTAB  = self . Tables        [ "Names"                                 ]
    HEAD    = 5702000000000000000
    ##########################################################################
    DB      . LockWrites           ( [ PRJTAB , PRDTAB , NAMTAB ]            )
    ##########################################################################
    if                             ( uuid <= 0                             ) :
      ########################################################################
      uuid  = DB . LastUuid        ( PRJTAB , "uuid" , HEAD                  )
      DB    . AddUuid              ( PRJTAB , uuid   , 1                     )
      ########################################################################
      NOW   = StarDate             (                                         )
      NOW   . Now                  (                                         )
      CDT   = NOW . Stardate
      ########################################################################
      PRD   = Periode              (                                         )
      PRID  = PRD  . GetUuid       ( DB , PRDTAB                             )
      ########################################################################
      PRD   . Realm    = uuid
      PRD   . Role     = 71
      PRD   . Item     = 1
      PRD   . States   = 0
      PRD   . Creation = CDT
      PRD   . Modified = CDT
      Items =                      [ "realm"                               , \
                                     "role"                                , \
                                     "item"                                , \
                                     "states"                              , \
                                     "creation"                            , \
                                     "modified"                              ]
      PRD   . UpdateItems          ( DB , PRDTAB , Items                     )
    ##########################################################################
    self    . AssureUuidName       ( DB , NAMTAB , uuid , name               )
    ##########################################################################
    DB      . Close                (                                         )
    ##########################################################################
    item    . setData              ( 0 , Qt . UserRole , uuid                )
    """
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def DetectAllPhones             ( self                                   ) :
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    plan     = None
    if                            ( self . hasPlan ( )                     ) :
      plan   = self . GetPlan     (                                          )
    ##########################################################################
    self     . OnBusy  . emit     (                                          )
    ##########################################################################
    PHSTAB   = self . Tables      [ "Phones"                                 ]
    PRZTAB   = self . Tables      [ "Properties"                             ]
    ##########################################################################
    QQ       = f"""select `uuid` from {PHSTAB}
                   where ( `used` = 1 )
                   order by `id` asc ;"""
    PHONEs   = DB . ObtainUuids   ( " " . join ( QQ . split ( ) )            )
    ##########################################################################
    if                            ( len ( PHONEs ) > 0                     ) :
      ########################################################################
      if                          ( plan not in [ False , None ]           ) :
        ######################################################################
        NAME = self . getMenuItem ( "QueryAllPhones"                         )
        cFmt = self . getMenuItem ( "SecsCounting"                           )
        rFmt = self . getMenuItem ( "ItemCounting"                           )
        FMT  = self . getMenuItem ( "Percentage"                             )
        PID  = plan . Progress    ( NAME , FMT                               )
        plan . setFrequency       ( PID  , cFmt , rFmt                       )
      ########################################################################
      plan   . setRange           ( PID , 0 , len ( PHONEs )                 )
      plan   . Start              ( PID , 0 , True                           )
      plan   . ProgressReady      ( PID , 300                                )
      ########################################################################
      K      = 0
      while ( K < len ( PHONEs ) ) and ( plan . isProgressRunning ( PID ) )  :
        ######################################################################
        UUID = PHONEs             [ K                                        ]
        plan . setProgressValue   ( PID , K                                  )
        ######################################################################
        PHON = TelecomPhone       (                                          )
        PHON . Uuid = UUID        
        PHON . ObtainsFullPhone   ( DB , PHSTAB , PRZTAB                     )
        PNUM = PHON . toPhone     (                                          )
        plan . ProgressText       ( PID , str ( PNUM )                       )
        PHON . Verify             ( PNUM                                     )
        ######################################################################
        CORR = PHON . Correct
        MOBI = PHON . Mobile
        REGC = PHON . Region
        ######################################################################
        QQ   = f"""update {PRZTAB}
                   set `correct` = {CORR} ,
                       `mobile` = {MOBI} ,
                       `region` = '{REGC}'
                   where ( `uuid` = {UUID} ) ;"""
        QQ   = " " . join         ( QQ . split ( )                           )
        DB   . Query              ( QQ                                       )
        ######################################################################
        K    = K + 1
      ########################################################################
      plan   . Finish             ( PID                                      )
    ##########################################################################
    self     . GoRelax . emit     (                                          )
    DB       . Close              (                                          )
    self     . Notify             ( 5                                        )
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
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9011 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def PickDbMenu                   ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    MSG    = self . getMenuItem    ( "PickDB"                                )
    DBM    = mm . addMenu          ( MSG                                     )
    ##########################################################################
    DBs    = self . Hosts . keys   (                                         )
    i      = 121330001
    ##########################################################################
    for DBn in DBs                                                           :
      ########################################################################
      hid  =                       ( DBn == self . DbProfile                 )
      mm   . addActionFromMenu     ( DBM , i , DBn , True , hid              )
      ########################################################################
      i    = i + 1
    ##########################################################################
    return mm
  ############################################################################
  def RunPickDbMenu                ( self , at                             ) :
    ##########################################################################
    DBs    = self . Hosts . keys   (                                         )
    DBs    = list                  ( DBs                                     )
    b      = 121330001
    e      = b + len               ( DBs                                     )
    ##########################################################################
    if                             ( at <  b                               ) :
      return False
    ##########################################################################
    if                             ( at >= e                               ) :
      return False
    ##########################################################################
    e      = at - b
    N      = DBs                   [ e                                       ]
    ##########################################################################
    self   . DbProfile = N
    self   . DB = self . Hosts     [ N                                       ]
    ##########################################################################
    if                             ( N in [ "ERP" ]                        ) :
      ########################################################################
      self . OwnRel . set          ( "t1" , 103                              )
      self . OwnRel . set          ( "t2" , 114                              )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . OwnRel . setT1        ( "People"                                )
      self . OwnRel . setT2        ( "Phone"                                 )
    ##########################################################################
    return True
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
    mm     = self . AmountIndexMenu     ( mm                                 )
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    mm     = self . AppendInsertAction  ( mm , 1101                          )
    mm     = self . AppendDeleteAction  ( mm , 1102                          )
    mm     . addSeparator          (                                         )
    msg    = self . getMenuItem    ( "QueryAllPhones"                        )
    mm     . addAction             ( 6001 , msg                              )
    mm     . addSeparator          (                                         )
    mm     = self . PickDbMenu     ( mm                                      )
    mm     = self . ColumnsMenu    ( mm                                      )
    mm     = self . SortingMenu    ( mm                                      )
    mm     = self . LocalityMenu   ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunAmountIndexMenu ( )         ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . RunColumnsMenu     ( at )      ) :
      return True
    ##########################################################################
    if                             ( self . RunSortingMenu     ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( self . RunPickDbMenu      ( at )      ) :
      ########################################################################
      self . clear                 (                                         )
      self . startup               (                                         )
      ########################################################################
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
    if                             ( at == 6001                            ) :
      ########################################################################
      self . Go                    ( self . DetectAllPhones                  )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
