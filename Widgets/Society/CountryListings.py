# -*- coding: utf-8 -*-
##############################################################################
## CountryListings
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
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
##############################################################################
FLAGs = [ "AD.png" , "AE.png" , "AF.png" , "AG.png" , "AI.png" , "AL.png" ,
          "AM.png" , "AO.png" , "AQ.png" , "AR.png" , "AS.png" , "AT.png" ,
          "AU.png" , "AW.png" , "AX.png" , "AZ.png" , "BA.png" , "BB.png" ,
          "BD.png" , "BE.png" , "BF.png" , "BG.png" , "BH.png" , "BI.png" ,
          "BJ.png" , "BL.png" , "BM.png" , "BN.png" , "BO.png" , "BR.png" ,
          "BS.png" , "BT.png" , "BV.png" , "BW.png" , "BY.png" , "BZ.png" ,
          "CA.png" , "CC.png" , "CD.png" , "CF.png" , "CG.png" , "CH.png" ,
          "CI.png" , "CK.png" , "CL.png" , "CM.png" , "CN.png" , "CO.png" ,
          "CR.png" , "CU.png" , "CV.png" , "CW.png" , "CX.png" , "CY.png" ,
          "CZ.png" , "DE.png" , "DJ.png" , "DK.png" , "DM.png" , "DO.png" ,
          "DZ.png" , "EC.png" , "EE.png" , "EG.png" , "EH.png" , "ER.png" ,
          "ES.png" , "ET.png" , "FI.png" , "FJ.png" , "FK.png" , "FM.png" ,
          "FO.png" , "FR.png" , "GA.png" , "GB.png" , "GD.png" , "GE.png" ,
          "GF.png" , "GG.png" , "GH.png" , "GI.png" , "GL.png" , "GM.png" ,
          "GN.png" , "GP.png" , "GQ.png" , "GR.png" , "GS.png" , "GT.png" ,
          "GU.png" , "GW.png" , "GY.png" , "HK.png" , "HM.png" , "HN.png" ,
          "HR.png" , "HT.png" , "HU.png" , "ID.png" , "IE.png" , "IL.png" ,
          "IM.png" , "IN.png" , "IO.png" , "IQ.png" , "IR.png" , "IS.png" ,
          "IT.png" , "JE.png" , "JM.png" , "JO.png" , "JP.png" , "KE.png" ,
          "KG.png" , "KH.png" , "KI.png" , "KM.png" , "KN.png" , "KP.png" ,
          "KR.png" , "KW.png" , "KY.png" , "KZ.png" , "LA.png" , "LB.png" ,
          "LC.png" , "LI.png" , "LK.png" , "LR.png" , "LS.png" , "LT.png" ,
          "LU.png" , "LV.png" , "LY.png" , "MA.png" , "MC.png" , "MD.png" ,
          "ME.png" , "MF.png" , "MG.png" , "MH.png" , "MK.png" , "ML.png" ,
          "MM.png" , "MN.png" , "MO.png" , "MP.png" , "MQ.png" , "MR.png" ,
          "MS.png" , "MT.png" , "MU.png" , "MV.png" , "MW.png" , "MX.png" ,
          "MY.png" , "MZ.png" , "NA.png" , "NC.png" , "NE.png" , "NF.png" ,
          "NG.png" , "NI.png" , "NL.png" , "NO.png" , "NP.png" , "NR.png" ,
          "NU.png" , "NZ.png" , "OM.png" , "PA.png" , "PE.png" , "PF.png" ,
          "PG.png" , "PH.png" , "PK.png" , "PL.png" , "PM.png" , "PN.png" ,
          "PR.png" , "PS.png" , "PT.png" , "PW.png" , "PY.png" , "QA.png" ,
          "RE.png" , "RO.png" , "RS.png" , "RU.png" , "RW.png" , "SA.png" ,
          "SB.png" , "SC.png" , "SD.png" , "SE.png" , "SG.png" , "SH.png" ,
          "SI.png" , "SJ.png" , "SK.png" , "SL.png" , "SM.png" , "SN.png" ,
          "SO.png" , "SR.png" , "SS.png" , "ST.png" , "SV.png" , "SY.png" ,
          "SZ.png" , "TC.png" , "TD.png" , "TF.png" , "TG.png" , "TH.png" ,
          "TJ.png" , "TK.png" , "TL.png" , "TM.png" , "TN.png" , "TO.png" ,
          "TR.png" , "TT.png" , "TV.png" , "TW.png" , "TZ.png" , "UA.png" ,
          "UG.png" , "UM.png" , "US.png" , "UY.png" , "UZ.png" , "VA.png" ,
          "VC.png" , "VE.png" , "VG.png" , "VI.png" , "VN.png" , "VU.png" ,
          "WF.png" , "WS.png" , "YE.png" , "YT.png" , "ZA.png" , "ZM.png" ,
          "ZW.png"                                                           ]
##############################################################################
class CountryListings              ( TreeDock                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitNamesShow     = pyqtSignal   (                                         )
  emitAllNames      = pyqtSignal   ( dict                                    )
  emitAssignAmounts = pyqtSignal   ( str , int                               )
  PeopleGroup       = pyqtSignal   ( str , int , str                         )
  ############################################################################
  def __init__                     ( self , parent = None , plan = None    ) :
    ##########################################################################
    super ( ) . __init__           (        parent        , plan             )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 28
    self . Order              = "asc"
    ##########################################################################
    self . NationTypes        =    {                                         }
    self . CountryUsed        =    {                                         }
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 10                                      )
    for i in range                 ( 1 , 10                                ) :
      self . setColumnHidden       ( i , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAllNames      . connect ( self . refresh                      )
    self . emitAssignAmounts . connect ( self . AssignAmounts                )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                     ( self                                  ) :
    return QSize                   ( 320 , 640                               )
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
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( self . isItemPicked ( )                    ) :
      if                      ( column != self . CurrentItem [ "Column" ]  ) :
        self . removeParked   (                                              )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in range ( 0 , 8 )           ) :
      return
    ##########################################################################
    if ( ( self . EditAllNames != None ) and ( column in [ 0 ] ) )           :
      ########################################################################
      uuid = self . itemUuid     ( item , 0                                  )
      NAM  = self . Tables       [ "Names"                                   ]
      self . EditAllNames        ( self , "Country" , uuid , NAM             )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 1 , 5 , 6 , 7 ]             ) :
      line = self . setLineEdit  ( item                                    , \
                                   column                                  , \
                                   "editingFinished"                       , \
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
      return
    ##########################################################################
    if                           ( column in [ 2 ]                         ) :
      ########################################################################
      LL   = self . NationTypes
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . comboChanged                       )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 3 ]                         ) :
      ########################################################################
      LL   = self . CountryUsed
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . comboChanged                       )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
      ########################################################################
      return
    ##########################################################################
    if                           ( column in [ 4 ]                         ) :
      ########################################################################
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      sb   = self . setSpinBox   ( item                                      ,
                                   column                                    ,
                                   0                                         ,
                                   1000000000                                ,
                                   "editingFinished"                         ,
                                   self . spinChanged                        )
      sb   . setValue            ( val                                       )
      sb   . setAlignment        ( Qt . AlignRight                           )
      sb   . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                ( self , UUID , NAME , INFO               ) :
    ##########################################################################
    global FLAGs
    ##########################################################################
    UUID = int                   ( UUID                                      )
    UXID = str                   ( UUID                                      )
    ##########################################################################
    IT   = QTreeWidgetItem       (                                           )
    IT   . setData               ( 0 , Qt . UserRole , UUID                  )
    ##########################################################################
    IT   . setText               ( 0 , NAME                                  )
    IT   . setToolTip            ( 0 , UXID                                  )
    ##########################################################################
    NAME = self . BlobToString   ( INFO [ 7 ]                                )
    IT   . setText               ( 1 , NAME                                  )
    ##########################################################################
    TYID = int                   ( INFO [ 1 ]                                )
    IT   . setText               ( 2 , self . NationTypes [ TYID ]           )
    IT   . setData               ( 2 , Qt . UserRole , TYID                  )
    ##########################################################################
    USID = int                   ( INFO [ 2 ]                                )
    IT   . setText               ( 3 , self . CountryUsed [ USID ]           )
    IT   . setData               ( 3 , Qt . UserRole , USID                  )
    ##########################################################################
    CODE = int                   ( INFO [ 3 ]                                )
    IT   . setText               ( 4 , str ( CODE )                          )
    IT   . setTextAlignment      ( 4 , Qt . AlignRight                       )
    IT   . setData               ( 4 , Qt . UserRole , CODE                  )
    ##########################################################################
    TWO  = self . BlobToString   ( INFO [ 4 ]                                )
    IT   . setText               ( 5 , TWO                                   )
    ##########################################################################
    THRE = self . BlobToString   ( INFO [ 5 ]                                )
    IT   . setText               ( 6 , THRE                                  )
    ##########################################################################
    FOUR = self . BlobToString   ( INFO [ 6 ]                                )
    IT   . setText               ( 7 , FOUR                                  )
    ##########################################################################
    IT   . setText               ( 8 , ""                                    )
    IT   . setTextAlignment      ( 8 , Qt . AlignRight                       )
    ##########################################################################
    IT   . setText               ( 9 , ""                                    )
    ##########################################################################
    PNG  = f"{TWO}.png"
    if                           ( PNG in FLAGs                            ) :
      K  = QIcon                 ( f":/nations/{PNG}"                        )
      IT . setIcon               ( 9 , K                                     )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                      (                                           )
  def RenameItem                 ( self                                    ) :
    ##########################################################################
    IT = self . currentItem      (                                           )
    if                           ( IT is None                              ) :
      return
    ##########################################################################
    self . doubleClicked         ( IT , 0                                    )
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
    if                           (    ( column not in [ 1 , 5 , 6 , 7 ]    ) \
                                   or ( len ( msg ) <= 0                   ) \
                                   or ( msg == text                      ) ) :
      item . setText             ( column , text                             )
      self . removeParked        (                                           )
      return
    ##########################################################################
    if                           ( column == 1                             ) :
      na   = "name"
    elif                         ( column == 5                             ) :
      na   = "two"
    elif                         ( column == 6                             ) :
      na   = "three"
    elif                         ( column == 7                             ) :
      na   = "four"
    ##########################################################################
    self   . Go                  ( self . UpdateTypeItemBlob               , \
                                   ( uuid , na , msg , )                     )
    ##########################################################################
    item   . setText             ( column ,              msg                 )
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def comboChanged               ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    sb     = self . CurrentItem  [ "Widget"                                  ]
    v      = item . data         ( column , Qt . UserRole                    )
    v      = int                 ( v                                         )
    nv     = sb   . itemData     ( sb . currentIndex ( )                     )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    name   = ""
    na     = ""
    if                           ( column in [ 2 ]                         ) :
      name = self . NationTypes  [ nv                                        ]
      na   = "type"
    elif                         ( column in [ 3 ]                         ) :
      name = self . CountryUsed  [ nv                                        ]
      na   = "used"
    ##########################################################################
    if                           ( v == nv                                 ) :
      item . setText             ( column , name                             )
      self . removeParked        (                                           )
      return
    ##########################################################################
    self . Go                    ( self . UpdateTypeItemValue              , \
                                   ( uuid , na , nv , )                      )
    ##########################################################################
    item . setText               ( column , name                             )
    item . setData               ( column , Qt . UserRole , nv               )
    self . removeParked          (                                           )
    ##########################################################################
    return
  ############################################################################
  def spinChanged                ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    sb     = self . CurrentItem  [ "Widget"                                  ]
    v      = item . data         ( column , Qt . UserRole                    )
    v      = int                 ( v                                         )
    nv     = sb   . value        (                                           )
    uuid   = self . itemUuid     ( item , 0                                  )
    ##########################################################################
    if                           ( ( v == nv ) or ( column not in [ 4 ] ) )  :
      item . setText             ( column , str ( v )                        )
      self . removeParked        (                                           )
      return
    ##########################################################################
    self . Go                    ( self . UpdateTypeItemValue              , \
                                   ( uuid , "code" , nv , )                  )
    ##########################################################################
    item . setText               ( column , str ( nv )                       )
    item . setData               ( column , Qt . UserRole , nv               )
    self . removeParked          (                                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot(dict)
  def refresh                         ( self , JSON                        ) :
    ##########################################################################
    self    . clear                   (                                      )
    ##########################################################################
    UUIDs   = JSON                    [ "UUIDs"                              ]
    INFOs   = JSON                    [ "INFOs"                              ]
    NAMEs   = JSON                    [ "NAMEs"                              ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT    = self . PrepareItem      ( U , NAMEs [ U ] , INFOs [ U ]        )
      self  . addTopLevelItem         ( IT                                   )
    ##########################################################################
    self    . emitNamesShow . emit    (                                      )
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
  def ObtainsUuidInfos                ( self , DB , UUIDs                  ) :
    ##########################################################################
    INFOs   =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return INFOs
    ##########################################################################
    CUYTAB  = self . Tables           [ "Countries"                          ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ    = f"""select `uuid`,`type`,`used`,`code`,
                  `two`,`three`,`four`,`name` from {CUYTAB}
                  where ( `uuid` = {UUID} ) ;"""
      QQ    = " " . join              ( QQ . split ( )                       )
      ########################################################################
      DB    . Query                   ( QQ                                   )
      RR    = DB . FetchOne           (                                      )
      ########################################################################
      if                              ( RR in [ None , False ]             ) :
        continue
      ########################################################################
      if                              ( len ( RR ) <= 0                    ) :
        continue
      ########################################################################
      INFOs [ UUID ] = RR
    ##########################################################################
    return INFOs
  ############################################################################
  @pyqtSlot                           (        str  , int                    )
  def AssignAmounts                   ( self , UUID , Amounts              ) :
    ##########################################################################
    IT    = self . uuidAtItem         ( UUID , 0                             )
    if                                ( IT is None                         ) :
      return
    ##########################################################################
    IT . setText                      ( 8 , str ( Amounts )                  )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                 ( self , UUIDs                      ) :
    ##########################################################################
    time    . sleep                    ( 1.0                                 )
    ##########################################################################
    RELTAB  = self . Tables            [ "Relation"                          ]
    REL     = Relation                 (                                     )
    REL     . setT1                    ( "Nation"                            )
    REL     . setT2                    ( "People"                            )
    REL     . setRelation              ( "Subordination"                     )
    ##########################################################################
    DB      = self . ConnectDB         (                                     )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      REL   . set                      ( "first" , UUID                      )
      CNT   = REL . CountSecond        ( DB , RELTAB                         )
      ########################################################################
      self  . emitAssignAmounts . emit ( str ( UUID ) , CNT                  )
    ##########################################################################
    DB      . Close                    (                                     )
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
    NAMTAB  = self . Tables           [ "Names"                              ]
    self    . ObtainsInformation      ( DB                                   )
    ##########################################################################
    INFOs   =                         {                                      }
    NAMEs   =                         {                                      }
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( len ( UUIDs ) > 0                  ) :
      INFOs = self . ObtainsUuidInfos ( DB , UUIDs                           )
      NAMEs = self . GetNames         ( DB , NAMTAB , UUIDs                  )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitNamesShow . emit     (                                      )
      return
    ##########################################################################
    JSON             =                {                                      }
    JSON [ "UUIDs" ] = UUIDs
    JSON [ "INFOs" ] = INFOs
    JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self   . emitAllNames . emit      ( JSON                                 )
    ##########################################################################
    if                                ( not self . isColumnHidden ( 7 )    ) :
      self . Go                       ( self . ReportBelongings            , \
                                        ( UUIDs , )                          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
  ############################################################################
  def ObtainAllUuids             ( self , DB                               ) :
    ##########################################################################
    TABLE = self . Tables        [ "Countries"                               ]
    ##########################################################################
    QQ    = f"""select `uuid` from {TABLE}
                  where ( `used` > 0 )
                  order by `id` asc ;"""
    ##########################################################################
    QQ    = " " . join           ( QQ . split ( )                            )
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
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None" ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock" ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"  ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    NTSTAB  = self . Tables           [ "NationTypes"                        ]
    ENUTAB  = self . Tables           [ "Enumerations"                       ]
    NAMTAB  = self . Tables           [ "Names"                              ]
    TABLE   = self . Tables           [ "Countries"                          ]
    ##########################################################################
    QQ      = f"select `uuid` from {NTSTAB} order by `id` asc ;"
    NTIDs   = DB . ObtainUuids        ( QQ                                   )
    ##########################################################################
    if                                ( len ( NTIDs ) > 0                  ) :
      NTS   = self . GetNames         ( DB , NAMTAB , NTIDs                  )
      for NTID in NTIDs                                                      :
        ID = int                      ( int ( NTID ) - 7400000000100000000   )
        self . NationTypes [ ID ] = NTS [ NTID                               ]
    ##########################################################################
    self . CountryUsed = self . GetEnumerations ( DB                       , \
                                                  ENUTAB                   , \
                                                  NAMTAB                   , \
                                                  "used"                   , \
                                                  43                         )
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    QQ      = f"select count(*) from {TABLE} ;"
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
  def ObtainUuidsQuery        ( self                                       ) :
    ##########################################################################
    TABLE   = self . Tables   [ "Countries"                                  ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . Order
    ##########################################################################
    QQ      = f"""select `uuid` from {TABLE}
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join         ( QQ . split ( )                               )
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
    self . Go                  ( self . PeopleJoinCountry                  , \
                                 ( UUID , UUIDs , )                          )
    ##########################################################################
    return True
  ############################################################################
  def PeopleJoinCountry             ( self , UUID , UUIDs                  ) :
    ##########################################################################
    if                              ( UUID <= 0                            ) :
      return
    ##########################################################################
    COUNT   = len                   ( UUIDs                                  )
    if                              ( COUNT <= 0                           ) :
      return
    ##########################################################################
    Hide    = self . isColumnHidden ( 1                                      )
    ##########################################################################
    DB      = self . ConnectDB      (                                        )
    if                              ( DB == None                           ) :
      return
    ##########################################################################
    MSG     = "加入{0}個人物" . format ( COUNT )
    self    . ShowStatus            ( MSG                                    )
    self    . TtsTalk               ( MSG , 1002                             )
    ##########################################################################
    RELTAB  = self . Tables         [ "Relation"                             ]
    REL     = Relation              (                                        )
    REL     . set                   ( "first" , UUID                         )
    REL     . setT1                 ( "Nation"                               )
    REL     . setT2                 ( "People"                               )
    REL     . setRelation           ( "Subordination"                        )
    DB      . LockWrites            ( [ RELTAB ]                             )
    REL     . Joins                 ( DB , RELTAB , UUIDs                    )
    DB      . UnlockTables          (                                        )
    ##########################################################################
    if                              ( not Hide                             ) :
      TOTAL = REL . CountSecond     ( DB , RELTAB                            )
    ##########################################################################
    DB      . Close                 (                                        )
    ##########################################################################
    self    . ShowStatus            ( ""                                     )
    ##########################################################################
    if                              ( Hide                                 ) :
      return
    ##########################################################################
    IT      = self . uuidAtItem     ( UUID , 0                               )
    if                              ( IT is None                           ) :
      return
    ##########################################################################
    IT      . setText               ( 1 , str ( TOTAL )                      )
    self    . DoUpdate              (                                        )
    ##########################################################################
    return
  ############################################################################
  def Prepare                 ( self                                       ) :
    ##########################################################################
    self   . setColumnWidth   ( 9 , 3                                        )
    ##########################################################################
    TRX    = self . Translations
    LABELs =                  [ "國家" , \
                                "英文" , \
                                "種類" , \
                                "狀態" , \
                                "國碼" , \
                                "兩碼" , \
                                "三碼" , \
                                "四碼" , \
                                "總人數" , \
                                ""                                           ]
    self   . setCentralLabels ( LABELs                                       )
    ##########################################################################
    self   . setPrepared      ( True                                         )
    ##########################################################################
    return
  ############################################################################
  def PageHome                     ( self                                  ) :
    ##########################################################################
    self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageEnd                      ( self                                  ) :
    ##########################################################################
    self . StartId    = self . Total - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageUp                       ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId - self . Amount
    if                             ( self . StartId <= 0                   ) :
      self . StartId  = 0
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def PageDown                     ( self                                  ) :
    ##########################################################################
    self . StartId    = self . StartId + self . Amount
    if                             ( self . StartId > self . Total         ) :
      self . StartId  = self . Total
    ##########################################################################
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def UpdateTypeItemValue          ( self , uuid , item , value            ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    TYPTAB  = self . Tables        [ "Countries"                             ]
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
    TYPTAB  = self . Tables        [ "Countries"                             ]
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
  def CopyToClipboard             ( self                                   ) :
    ##########################################################################
    IT   = self . currentItem     (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    MSG  = IT . text              ( self . currentColumn ( )                 )
    LID  = self . getLocality     (                                          )
    qApp . clipboard ( ). setText ( MSG                                      )
    ##########################################################################
    self . TtsTalk                ( MSG , LID                                )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    COL    = mm . addMenu          ( TRX [ "UI::Columns" ]                   )
    ##########################################################################
    cols   = self . columnCount    (                                         )
    HIT    = self . headerItem     (                                         )
    ##########################################################################
    for i in range                 ( 1 , cols                              ) :
      ########################################################################
      T    = HIT . text            ( i                                       )
      if                           ( len ( T ) <= 0                        ) :
        T  = TRX                   [ "UI::Whitespace"                        ]
      hid  = self . isColumnHidden ( i                                       )
      mm   . addActionFromMenu     ( COL , 9000 + i , T , True , not hid     )
    ##########################################################################
    return mm
  ############################################################################
  @pyqtSlot(int)
  def GotoId                       ( self , Id                             ) :
    ##########################################################################
    self . StartId    = Id
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot(int)
  def AssignAmount                 ( self , Amount                         ) :
    ##########################################################################
    self . Amount    = Amount
    self . clear                   (                                         )
    self . startup                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
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
    T      = self . Total
    MSG    = f"總數量:{T}"
    mm     . addAction             ( 9999991 , MSG                           )
    ##########################################################################
    SIDB   = SpinBox               ( None , self . PlanFunc                  )
    SIDB   . setRange              ( 0 , self . Total                        )
    SIDB   . setValue              ( self . StartId                          )
    SIDB   . setPrefix             ( "本頁開始:" )
    mm     . addWidget             ( 9999992 , SIDB                          )
    SIDB   . valueChanged . connect ( self . GotoId                          )
    ##########################################################################
    SIDP   = SpinBox               ( None , self . PlanFunc                  )
    SIDP   . setRange              ( 0 , self . Total                        )
    SIDP   . setValue              ( self . Amount                           )
    SIDP   . setPrefix             ( "每頁數量:" )
    mm     . addWidget             ( 9999993 , SIDP                          )
    SIDP   . valueChanged . connect ( self . AssignAmount                    )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     . addAction             ( 1001 ,  TRX [ "UI::Refresh"           ] )
    ##########################################################################
    if                             ( atItem != None                        ) :
      FMT  = TRX                   [ "UI::AttachCrowds"                      ]
      MSG  = FMT . format          ( atItem . text ( 0 )                     )
      mm   . addSeparator          (                                         )
      mm   . addAction             ( 1201 ,  MSG                             )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( len ( items ) == 1                    ) :
      if                           ( self . EditAllNames != None           ) :
        mm . addAction             ( 1601 ,  TRX [ "UI::EditNames" ]         )
        mm . addSeparator          (                                         )
    ##########################################################################
    mm     = self . ColumnsMenu    ( mm                                      )
    mm     = self . LocalityMenu   ( mm                                      )
    mm     . addSeparator          (                                         )
    mm     . addAction             ( 3001 ,  TRX [ "UI::TranslateAll"      ] )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . HandleLocalityMenu ( at )      ) :
      return True
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9010 )         :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      if                           ( ( at == 9008 ) and ( hid )            ) :
        self . startup             (                                         )
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      self . startup               (                                         )
      return True
    ##########################################################################
    if                             ( at == 1201                            ) :
      head = atItem . text         ( 0                                       )
      self . PeopleGroup   . emit  ( head , 43 , str ( uuid )                )
      return True
    ##########################################################################
    if                             ( at == 1601                            ) :
      uuid = self . itemUuid       ( items [ 0 ] , 0                         )
      NAM  = self . Tables         [ "Names"                                 ]
      self . EditAllNames          ( self , "Country" , uuid , NAM           )
      return True
    ##########################################################################
    if                             ( at == 3001                            ) :
      self . Go                    ( self . TranslateAll                     )
      return True
    ##########################################################################
    return True
##############################################################################
