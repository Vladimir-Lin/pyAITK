# -*- coding: utf-8 -*-
##############################################################################
## CountryMembership
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
class CountryMembership  ( TreeDock                                        ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = Signal (                                                   )
  emitAllNames  = Signal ( dict                                              )
  emitLog       = Signal ( str                                               )
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    ##########################################################################
    self . EditAllNames       = None
    ##########################################################################
    self . ClassTag           = "CountryMembership"
    self . FetchTableKey      = "CountryMembership"
    self . GType              = 43
    ##########################################################################
    self . SortOrder          = "asc"
    self . ValidOnly          = True
    ##########################################################################
    self . NationTypes        = {                                            }
    self . CountryUsed        = {                                            }
    self . UsedOptions        = [ 1 , 2                                      ]
    self . PeopleCountries    = [                                            ]
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
    self . setColumnCount          ( 4                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setColumnWidth          ( 2 , 32                                  )
    self . setColumnHidden         ( 3 , True                                )
    ##########################################################################
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    self . MountClicked            ( 9                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ExtendedSelection"                     )
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
    self . setMinimumSize          ( 80 , 80                                 )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 320 , 640 )                       )
  ############################################################################
  def AttachActions   ( self      ,                  Enabled               ) :
    ##########################################################################
    self . LinkAction ( "Refresh" , self . startup , Enabled                 )
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
  def stateChanged            ( self , item , column                       ) :
    ##########################################################################
    if                        ( column not in [ 0                        ] ) :
      return
    ##########################################################################
    CHK   = item . checkState ( 0                                            )
    state =                   ( CHK == Qt . Checked                          )
    uuid  = item . data       ( 0 , Qt . UserRole                            )
    uuid  = int               ( uuid                                         )
    VAL   =                   ( uuid , state ,                               )
    ##########################################################################
    self  . Go                ( self . UpdateCountry , VAL                   )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem              ( self , UUID , NAME , INFO , BRUSH         ) :
    ##########################################################################
    global FLAGs
    ##########################################################################
    ST   = Qt . Unchecked
    ##########################################################################
    if                         ( UUID in self . PeopleCountries            ) :
      ST = Qt . Checked
    ##########################################################################
    UUID = int                 ( UUID                                        )
    UXID = str                 ( UUID                                        )
    ##########################################################################
    IT   = QTreeWidgetItem     (                                             )
    IT   . setData             ( 0 , Qt . UserRole , UUID                    )
    IT   . setText             ( 0 , NAME                                    )
    IT   . setToolTip          ( 0 , UXID                                    )
    IT   . setCheckState       ( 0 , ST                                      )
    ##########################################################################
    NAME = self . BlobToString ( INFO [ 7 ]                                  )
    IT   . setText             ( 1 , NAME                                    )
    ##########################################################################
    IT   . setText             ( 2 , ""                                      )
    ##########################################################################
    TWO  = self . BlobToString ( INFO [ 4 ]                                  )
    PNG  = f"{TWO}.png"
    ##########################################################################
    if                         ( PNG in FLAGs                              ) :
      K  = QIcon               ( f":/nations/{PNG}"                          )
      IT . setIcon             ( 2 , K                                       )
    ##########################################################################
    for COL in                 [ 0 , 1 , 2                                 ] :
      ########################################################################
      IT . setBackground       ( COL , BRUSH                                 )
    ##########################################################################
    return IT
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
    self   . Notify                   ( 5                                    )
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
    COUNTRYz = self . COUNTRY . FetchPeopleCountries ( DB                    )
    self  . PeopleCountries = COUNTRYz
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery                     ( self                          ) :
    ##########################################################################
    return self . COUNTRY . QuerySyntaxAll ( self . Tables [ "Countries" ] , \
                                             self . GetOPTs         (    ) , \
                                             self . getSortingOrder (    )   )
  ############################################################################
  def StartupMembership        ( self , title , uuid                       ) :
    ##########################################################################
    FMT  = self . getMenuItem  ( "Title"                                     )
    self . setWindowTitle      ( FMT . format ( title                      ) )
    ##########################################################################
    self . COUNTRY . setPeople (                uuid                         )
    self . startup             (                                             )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( self . ClassTag , 3                              )
    ##########################################################################
    self . LoopRunning = False
    ##########################################################################
    return
  ############################################################################
  def UpdateCountry             ( self , uuid , state                      ) :
    ##########################################################################
    if                          ( state                                    ) :
      ########################################################################
      if                        ( uuid not in self . PeopleCountries       ) :
        ######################################################################
        self . PeopleCountries . append ( uuid                               )
      ########################################################################
    else                                                                     :
      ########################################################################
      if                        ( uuid     in self . PeopleCountries       ) :
        ######################################################################
        self . PeopleCountries . remove ( uuid                               )
    ##########################################################################
    DB       = self . ConnectDB (                                            )
    if                          ( self . NotOkay ( DB )                    ) :
      return False
    ##########################################################################
    self     . COUNTRY . LockRelationTable   ( DB                            )
    self     . COUNTRY . AssignPeopleCountry ( DB , uuid , state             )
    ##########################################################################
    DB       . UnlockTables     (                                            )
    DB       . Close            (                                            )
    ##########################################################################
    self     . Notify           ( 5                                          )
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
  def ColumnsMenu                    ( self , mm                           ) :
    return self . DefaultColumnsMenu (        mm , 1                         )
  ############################################################################
  def RunColumnsMenu               ( self , at                             ) :
    ##########################################################################
    if                             ( at >= 9001 ) and ( at <= 9003 )         :
      ########################################################################
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                       ( self , pos                              ) :
    ##########################################################################
    if                           ( not self . isPrepared (               ) ) :
      return False
    ##########################################################################
    doMenu = self . isFunction   ( self . HavingMenu                         )
    if                           ( not doMenu                              ) :
      return False
    ##########################################################################
    self   . Notify              ( 0                                         )
    ##########################################################################
    items  , atItem , uuid = self . GetMenuDetails ( 0                       )
    ##########################################################################
    mm     = MenuManager         ( self                                      )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction ( mm , 1001                                 )
    mm     . addSeparator        (                                           )
    self   . ColumnsMenu         ( mm                                        )
    self   . LocalityMenu        ( mm                                        )
    self   . SortingMenu         ( mm                                        )
    self   . DockingMenu         ( mm                                        )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont             ( self    . menuFont (                    ) )
    aa     = mm . exec_          ( QCursor . pos      (                    ) )
    at     = mm . at             ( aa                                        )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    if                           ( self . RunDocking   ( mm , aa )         ) :
      return True
    ##########################################################################
    if                           ( self . HandleLocalityMenu ( at )        ) :
      return True
    ##########################################################################
    if                           ( self . RunColumnsMenu     ( at )        ) :
      return True
    ##########################################################################
    if                           ( self . RunSortingMenu     ( at )        ) :
      ########################################################################
      self . restart             (                                           )
      ########################################################################
      return True
    ##########################################################################
    if                           ( 1001 == at                              ) :
      ########################################################################
      self . restart             (                                           )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
