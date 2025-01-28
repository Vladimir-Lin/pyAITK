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
from   PySide6                                  import QtCore
from   PySide6                                  import QtGui
from   PySide6                                  import QtWidgets
from   PySide6 . QtCore                         import *
from   PySide6 . QtGui                          import *
from   PySide6 . QtWidgets                      import *
from   AITK    . Qt6                            import *
##############################################################################
from   AITK    . Essentials . Relation          import Relation
from   AITK    . Calendars  . StarDate          import StarDate
from   AITK    . Calendars  . Periode           import Periode
from   AITK    . Society    . Country . Country import Country
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
class CountryListings          ( TreeDock                                  ) :
  ############################################################################
  HavingMenu          = 1371434312
  ############################################################################
  emitNamesShow       = Signal (                                             )
  emitAllNames        = Signal ( dict                                        )
  emitAssignAmounts   = Signal ( str , int , int                             )
  PeopleGroup         = Signal ( str , int , str                             )
  BelongingEarthSpots = Signal ( str , str , QIcon                           )
  OpenLogHistory      = Signal ( str , str , str , str , str                 )
  emitLog             = Signal ( str                                         )
  ############################################################################
  def __init__                 ( self , parent = None , plan = None        ) :
    ##########################################################################
    super ( ) . __init__       (        parent        , plan                 )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "CountryListings"
    self . FetchTableKey      = "CountryListings"
    self . GType              = 43
    ##########################################################################
    self . Total              = 0
    self . StartId            = 0
    self . Amount             = 35
    ##########################################################################
    self . SortOrder          = "asc"
    self . ValidOnly          = False
    ##########################################################################
    self . NationTypes        = {                                            }
    self . CountryUsed        = {                                            }
    self . UsedOptions        = [ 1 , 2                                      ]
    ##########################################################################
    self . COUNTRY            = Country (                                    )
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount               ( 10                                 )
    for i in range                      ( 1 , 10                           ) :
      self . setColumnHidden            ( i , True                           )
    ##########################################################################
    self . setRootIsDecorated           ( False                              )
    self . setAlternatingRowColors      ( True                               )
    ##########################################################################
    self . MountClicked                 ( 1                                  )
    self . MountClicked                 ( 2                                  )
    ##########################################################################
    self . assignSelectionMode          ( "ExtendedSelection"                )
    ##########################################################################
    self . emitNamesShow     . connect  ( self . show                        )
    self . emitAllNames      . connect  ( self . refresh                     )
    self . emitAssignAmounts . connect  ( self . AssignAmounts               )
    ##########################################################################
    self . setFunction                  ( self . FunctionDocking , True      )
    self . setFunction                  ( self . HavingMenu      , True      )
    ##########################################################################
    self . setAcceptDrops               ( True                               )
    self . setDragEnabled               ( True                               )
    self . setDragDropMode              ( QAbstractItemView . DragDrop       )
    ##########################################################################
    self . setMinimumSize               ( 80 , 80                            )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 320 , 640 )                       )
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendSideActionWithIcon ( "Crowds"                             , \
                                      ":/images/viewpeople.png"            , \
                                      self . GotoItemCrowd                   )
    self . AppendToolNamingAction   (                                        )
    self . AppendSideActionWithIcon ( "Description"                        , \
                                      ":/images/documents.png"             , \
                                      self . GotoItemDescription             )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenameItem      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
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
  def FocusIn                     ( self                                   ) :
    return self . defaultFocusIn  (                                          )
  ############################################################################
  def FocusOut                    ( self                                   ) :
    return self . defaultFocusOut (                                          )
  ############################################################################
  def Shutdown               ( self                                        ) :
    ##########################################################################
    self . StayAlive   = False
    self . LoopRunning = False
    ##########################################################################
    if                       ( self . isThreadRunning (                  ) ) :
      return False
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    ##########################################################################
    self . Leave . emit      ( self                                          )
    ##########################################################################
    return True
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked              ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in range ( 0 , 8 )            ) :
      return
    ##########################################################################
    if ( ( self . EditAllNames != None ) and ( column in [ 0 ] ) )           :
      ########################################################################
      uuid = self . itemUuid    ( item , 0                                   )
      NAM  = self . Tables      [ "Names"                                    ]
      self . EditAllNames       ( self , "Country" , uuid , NAM              )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [ 1 , 5 , 6 , 7 ]              ) :
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      return
    ##########################################################################
    if                          ( column in [ 2 ]                          ) :
      ########################################################################
      LL   = self . NationTypes
      val  = item . data        ( column , Qt . UserRole                     )
      val  = int                ( val                                        )
      cb   = self . setComboBox ( item                                       ,
                                  column                                     ,
                                  "activated"                                ,
                                  self . comboChanged                        )
      cb   . addJson            ( LL , val                                   )
      cb   . setMaxVisibleItems ( 20                                         )
      cb   . showPopup          (                                            )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [ 3 ]                          ) :
      ########################################################################
      LL   = self . CountryUsed
      val  = item . data        ( column , Qt . UserRole                     )
      val  = int                ( val                                        )
      cb   = self . setComboBox ( item                                       ,
                                  column                                     ,
                                  "activated"                                ,
                                  self . comboChanged                        )
      cb   . addJson            ( LL , val                                   )
      cb   . setMaxVisibleItems ( 20                                         )
      cb   . showPopup          (                                            )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [ 4 ]                         ) :
      ########################################################################
      val  = item . data        ( column , Qt . UserRole                    )
      val  = int                ( val                                       )
      sb   = self . setSpinBox  ( item                                      ,
                                  column                                    ,
                                  0                                         ,
                                  1000000000                                ,
                                  "editingFinished"                         ,
                                  self . spinChanged                        )
      sb   . setValue           ( val                                       )
      sb   . setAlignment       ( Qt . AlignRight                           )
      sb   . setFocus           ( Qt . TabFocusReason                       )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem              ( self , UUID , NAME , INFO , BRUSH         ) :
    ##########################################################################
    global FLAGs
    ##########################################################################
    UUID = int                 ( UUID                                        )
    UXID = str                 ( UUID                                        )
    ##########################################################################
    IT   = QTreeWidgetItem     (                                             )
    IT   . setData             ( 0 , Qt . UserRole , UUID                    )
    ##########################################################################
    IT   . setText             ( 0 , NAME                                    )
    IT   . setToolTip          ( 0 , UXID                                    )
    ##########################################################################
    NAME = self . BlobToString ( INFO [ 7 ]                                  )
    IT   . setText             ( 1 , NAME                                    )
    ##########################################################################
    TYID = int                 ( INFO [ 1 ]                                  )
    IT   . setText             ( 2 , self . NationTypes [ TYID ]             )
    IT   . setData             ( 2 , Qt . UserRole , TYID                    )
    ##########################################################################
    USID = int                 ( INFO [ 2 ]                                  )
    IT   . setText             ( 3 , self . CountryUsed [ USID ]             )
    IT   . setData             ( 3 , Qt . UserRole , USID                    )
    ##########################################################################
    CODE = int                 ( INFO [ 3 ]                                  )
    IT   . setText             ( 4 , str ( CODE )                            )
    IT   . setTextAlignment    ( 4 , Qt . AlignRight                         )
    IT   . setData             ( 4 , Qt . UserRole , CODE                    )
    ##########################################################################
    TWO  = self . BlobToString ( INFO [ 4 ]                                  )
    IT   . setText             ( 5 , TWO                                     )
    ##########################################################################
    THRE = self . BlobToString ( INFO [ 5 ]                                  )
    IT   . setText             ( 6 , THRE                                    )
    ##########################################################################
    FOUR = self . BlobToString ( INFO [ 6 ]                                  )
    IT   . setText             ( 7 , FOUR                                    )
    ##########################################################################
    IT   . setText             ( 8 , ""                                      )
    IT   . setTextAlignment    ( 8 , Qt . AlignRight                         )
    ##########################################################################
    IT   . setText             ( 9 , ""                                      )
    ##########################################################################
    PNG  = f"{TWO}.png"
    if                         ( PNG in FLAGs                              ) :
      K  = QIcon               ( f":/nations/{PNG}"                          )
      IT . setIcon             ( 9 , K                                       )
    ##########################################################################
    for COL in                 [ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9     ] :
      ########################################################################
      IT . setBackground       ( COL , BRUSH                                 )
    ##########################################################################
    return IT
  ############################################################################
  def RenameItem        ( self                                             ) :
    ##########################################################################
    self . goRenameItem ( 0                                                  )
    ##########################################################################
    return
  ############################################################################
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
  def RefreshToolTip          ( self , Total                               ) :
    ##########################################################################
    FMT  = self . getMenuItem ( "DisplayTotal"                               )
    MSG  = FMT  . format      ( Total                                        )
    self . setToolTip         ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def refresh                     ( self , JSON                            ) :
    ##########################################################################
    self   . clear                (                                          )
    self   . setEnabled           ( False                                    )
    ##########################################################################
    CNT    = 0
    MOD    = len                  ( self . TreeBrushes                       )
    ##########################################################################
    UUIDs  = JSON                 [ "UUIDs"                                  ]
    INFOs  = JSON                 [ "INFOs"                                  ]
    NAMEs  = JSON                 [ "NAMEs"                                  ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      IT   = self . PrepareItem   ( U                                      , \
                                    NAMEs [ U ]                            , \
                                    INFOs [ U ]                            , \
                                    self . TreeBrushes [ CNT ]               )
      self . addTopLevelItem      ( IT                                       )
      ########################################################################
      CNT  = int                  ( int ( CNT + 1 ) % MOD                    )
    ##########################################################################
    self   . RefreshToolTip       ( len ( UUIDs )                            )
    self   . setEnabled           ( True                                     )
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
  def ObtainsUuidInfos                    ( self , DB , UUIDs              ) :
    return  self . COUNTRY . ObtainsINFOs ( DB                             , \
                                            self . Tables [ "Countries" ]  , \
                                            UUIDs                            )
  ############################################################################
  def AssignAmounts        ( self , UUID , Amounts , COLUMN                ) :
    ##########################################################################
    IT = self . uuidAtItem ( UUID , 0                                        )
    if                     ( IT is None                                    ) :
      return
    ##########################################################################
    IT . setText           ( COLUMN , str ( Amounts )                        )
    ##########################################################################
    return
  ############################################################################
  def ReportBelongings                    ( self , UUIDs                   ) :
    ##########################################################################
    time   . sleep                        ( 1.0                              )
    ##########################################################################
    RELTAB = self . Tables                [ "RelationPeople"                 ]
    ##########################################################################
    DB     = self . ConnectDB             (                                  )
    self   . OnBusy  . emit               (                                  )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      CNT  = self . COUNTRY . CountCrowds ( DB                             , \
                                            RELTAB                         , \
                                            "Subordination"                , \
                                            UUID                             )
      self . emitAssignAmounts . emit     ( str ( UUID ) , CNT , 8           )
    ##########################################################################
    self   . GoRelax . emit               (                                  )
    DB     . Close                        (                                  )
    ##########################################################################
    return
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
    self    . setVacancy              (                                      )
    self    . GoRelax . emit          (                                      )
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
    if                                ( not self . isColumnHidden ( 8 )    ) :
      self . Go                       ( self . ReportBelongings            , \
                                        ( UUIDs , )                          )
    ##########################################################################
    return
  ############################################################################
  def GetOPTs       ( self                                                 ) :
    ##########################################################################
    OPTs   =        [                                                        ]
    ##########################################################################
    if              ( not self . ValidOnly                                 ) :
      OPTs . append ( 0                                                      )
    ##########################################################################
    for U in self . UsedOptions                                              :
      OPTs . append ( U                                                      )
    ##########################################################################
    return OPTs
  ############################################################################
  def ObtainAllUuids                   ( self , DB                         ) :
    return self . COUNTRY . FetchUuids ( DB                                , \
                                         self . Tables  [ "Countries" ]    , \
                                         self . GetOPTs (                  ) )
  ############################################################################
  def ObtainsInformation     ( self , DB                                   ) :
    ##########################################################################
    NTSTAB = self . Tables   [ "NationTypes"                                 ]
    ENUTAB = self . Tables   [ "Enumerations"                                ]
    NAMTAB = self . Tables   [ "Names"                                       ]
    TABLE  = self . Tables   [ "Countries"                                   ]
    ##########################################################################
    self   . ReloadLocality  ( DB                                            )
    NTIDs  = self . COUNTRY . GetNationTypes ( DB , NTSTAB                   )
    ##########################################################################
    if                       ( len ( NTIDs ) > 0                           ) :
      NTS  = self . GetNames ( DB , NAMTAB , NTIDs                           )
      for NTID in NTIDs                                                      :
        ID = int             ( int ( NTID ) - 7400000000100000000            )
        self . NationTypes [ ID ] = NTS [ NTID                               ]
    ##########################################################################
    self   . CountryUsed = self . GetEnumerations                          ( \
                               DB                                          , \
                               ENUTAB                                      , \
                               NAMTAB                                      , \
                               "used"                                      , \
                               self . GType                                  )
    ##########################################################################
    self   . Total = self . COUNTRY . CountOptions                           (
                               DB                                          , \
                               TABLE                                       , \
                               self . GetOPTs (                            ) )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery                  ( self                             ) :
    ##########################################################################
    return self . COUNTRY . QuerySyntax ( self . Tables [ "Countries"    ] , \
                                          self . GetOPTs         (       ) , \
                                          self . getSortingOrder (       ) , \
                                          self . StartId                   , \
                                          self . Amount                      )
  ############################################################################
  def dragMime                   ( self                                    ) :
    ##########################################################################
    mtype   = "nation/uuids"
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
      FMT   = self . getMenuItem    ( "Copying"                              )
      MSG   = FMT  . format         ( title , CNT                            )
      self  . ShowStatus            ( MSG                                    )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptPeopleDrop         ( self                                      ) :
    return True
  ############################################################################
  def dropPeople                       ( self , source , pos , JSON        ) :
    return self . defaultDropInObjects ( source                            , \
                                         pos                               , \
                                         JSON                              , \
                                         0                                 , \
                                         self . PeopleJoinCountry            )
  ############################################################################
  def PeopleJoinCountry                    ( self , UUID , UUIDs           ) :
    ##########################################################################
    if                                     ( UUID <= 0                     ) :
      return
    ##########################################################################
    COUNT   = len                          ( UUIDs                           )
    if                                     ( COUNT <= 0                    ) :
      return
    ##########################################################################
    Hide    = self . isColumnHidden        ( 1                               )
    ##########################################################################
    DB      = self . ConnectDB             (                                 )
    if                                     ( DB == None                    ) :
      return
    ##########################################################################
    FMT     = self . getMenuItem           ( "Joining"                       )
    MSG     = FMT  . format                ( COUNT                           )
    self    . ShowStatus                   ( MSG                             )
    self    . TtsTalk                      ( MSG , 1002                      )
    ##########################################################################
    RELTAB  = self . Tables                [ "RelationPeople"                ]
    RELATE  = "Subordination"
    ##########################################################################
    DB      . LockWrites                   ( [ RELTAB                      ] )
    self    . COUNTRY . PeopleJoinCountry  ( DB                            , \
                                             RELTAB                        , \
                                             RELATE                        , \
                                             UUID                          , \
                                             UUIDs                           )
    DB      . UnlockTables                 (                                 )
    ##########################################################################
    if                                     ( not Hide                      ) :
      TOTAL = self . COUNTRY . CountCrowds ( DB , RELTAB , RELATE , UUID     )
    ##########################################################################
    DB      . Close                        (                                 )
    ##########################################################################
    self    . ShowStatus                   ( ""                              )
    ##########################################################################
    if                                     ( Hide                          ) :
      return
    ##########################################################################
    IT      = self . uuidAtItem            ( UUID , 0                        )
    if                                     ( IT is None                    ) :
      return
    ##########################################################################
    IT      . setText                      ( 8 , str ( TOTAL )               )
    self    . DoUpdate                     (                                 )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 9                              )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def UpdateTypeItemValue          ( self , uuid , item , value            ) :
    ##########################################################################
    DB      = self . ConnectDB     (                                         )
    if                             ( DB == None                            ) :
      return
    ##########################################################################
    CTYTAB = self . Tables         [ "Countries"                             ]
    ##########################################################################
    DB     . LockWrites            ( [ CTYTAB                              ] )
    self   . COUNTRY . UpdateValue ( DB , CTYTAB , uuid , item , value       )
    DB     . UnlockTables          (                                         )
    DB     . Close                 (                                         )
    ##########################################################################
    return
  ############################################################################
  def UpdateTypeItemBlob          ( self , uuid , item , blob              ) :
    ##########################################################################
    DB      = self . ConnectDB    (                                          )
    if                            ( DB == None                             ) :
      return
    ##########################################################################
    CTYTAB = self . Tables        [ "Countries"                              ]
    ##########################################################################
    DB     . LockWrites           ( [ CTYTAB                               ] )
    self   . COUNTRY . UpdateBlob ( DB , CTYTAB , uuid , item , blob         )
    DB     . UnlockTables         (                                          )
    DB     . Close                (                                          )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
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
    self . defaultOpenItemNamesEditor ( item                               , \
                                        0                                  , \
                                        "Nation"                           , \
                                        "NamesCountry"                       )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9009 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      if                           ( ( at == 9008 ) and ( hid )            ) :
        ######################################################################
        self . restart             (                                         )
        ######################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                             ( self , pos                        ) :
    ##########################################################################
    if                                 ( not self . isPrepared (         ) ) :
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
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu    ( mm , True                           )
    ##########################################################################
    self   . AppendRefreshAction       ( mm , 1001                           )
    ##########################################################################
    msg    = self . getMenuItem        ( "ValidOnly"                         )
    mm     . addAction                 ( 3223                              , \
                                         msg                               , \
                                         True                              , \
                                         self . ValidOnly                    )
    ##########################################################################
    if                                 ( atItem not in self . EmptySet     ) :
      ########################################################################
      FMT  = TRX                       [ "UI::AttachCrowds"                  ]
      MSG  = FMT . format              ( atItem . text ( 0 )                 )
      mm   . addSeparator              (                                     )
      mm   . addAction                 ( 1201 ,  MSG                         )
      msg  = self . getMenuItem        ( "Positions"                         )
      mm   . addAction                 ( 7401 , msg                          )
      ########################################################################
      if                               ( self . EditAllNames != None       ) :
        ######################################################################
        mm . addAction                 ( 1601 ,  TRX [ "UI::EditNames" ]     )
    ##########################################################################
    mm     . addSeparator              (                                     )
    ##########################################################################
    self   . ColumnsMenu               ( mm                                  )
    self   . LocalityMenu              ( mm                                  )
    self   . SortingMenu               ( mm                                  )
    self   . DockingMenu               ( mm                                  )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                   ( self    . menuFont ( )              )
    aa     = mm . exec_                ( QCursor . pos      ( )              )
    at     = mm . at                   ( aa                                  )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    OKAY   = self . RunAmountIndexMenu ( at                                  )
    ##########################################################################
    if                                 ( OKAY                              ) :
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( self . RunDocking   ( mm , aa )   ) :
      return True
    ##########################################################################
    if                                 ( self . HandleLocalityMenu ( at )  ) :
      return True
    ##########################################################################
    if                                 ( self . RunColumnsMenu     ( at )  ) :
      return True
    ##########################################################################
    if                                 ( self . RunSortingMenu     ( at )  ) :
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
    if                                 ( at == 1201                        ) :
      ########################################################################
      self . OpenItemCrowd             ( item                                )
      ########################################################################
      return True
    ##########################################################################
    if                                 ( at == 3223                        ) :
      ########################################################################
      if                               ( self . ValidOnly                  ) :
        self . ValidOnly = False
      else                                                                   :
        self . ValidOnly = True
      ########################################################################
      self . restart                   (                                     )
      ########################################################################
      return True
    ##########################################################################
    OKAY   = self . AtItemNamesEditor  ( at , 1601 , atItem                  )
    if                                 ( OKAY                              ) :
      return True
    ##########################################################################
    if                                 ( at == 7401                        ) :
      ########################################################################
      head = atItem . text             ( 0                                   )
      uuid = self   . itemUuid         ( atItem , 0                          )
      icon = self   . windowIcon       (                                     )
      self . BelongingEarthSpots . emit ( str ( uuid ) , head , icon         )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
