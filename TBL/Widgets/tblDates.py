# -*- coding: utf-8 -*-
##############################################################################
## tblDates
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import random
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
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QBrush
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
from   AITK  . Documents  . JSON      import Load        as LoadJson
from   AITK  . Essentials . Relation  import Relation
from   AITK  . Calendars  . StarDate  import StarDate
from   AITK  . Calendars  . Periode   import Periode
##############################################################################
class tblDates                      ( TreeDock                             ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  emitDates  = pyqtSignal           ( list                                   )
  addText    = pyqtSignal           ( str                                    )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            (        parent        , plan            )
    ##########################################################################
    self . Total     = 0
    self . StartId   = 0
    self . Amount    = 28
    self . SortOrder = "desc"
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . LeftDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . emitDates . connect      ( self . refresh                         )
    ##########################################################################
    self . setColumnCount           ( 4                                      )
    self . setRootIsDecorated       ( False                                  )
    self . setAlternatingRowColors  ( True                                   )
    ##########################################################################
    self . MountClicked             ( 0                                      )
    self . MountClicked             ( 1                                      )
    self . MountClicked             ( 2                                      )
    ##########################################################################
    self . assignSelectionMode      ( "ContiguousSelection"                  )
    self . setFunction              ( self . HavingMenu      , True          )
    ##########################################################################
    self . setDragEnabled           ( False                                  )
    self . setAcceptDrops           ( False                                  )
    self . setDragDropMode          ( QAbstractItemView . NoDragDrop         )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 480 , 640 )                       )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    """
    msg  = self . Translations    [ "UI::EditNames"                          ]
    A    = QAction                (                                          )
    A    . setIcon                ( QIcon ( ":/images/names.png" )           )
    A    . setToolTip             ( msg                                      )
    A    . triggered . connect    ( self . OpenOrganizationNames             )
    self . WindowActions . append ( A                                        )
    """
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    ##########################################################################
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
    ##########################################################################
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
    self . LinkVoice         ( self . CommandParser                          )
    self . Notify            ( 0                                             )
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
  def closeEvent             ( self , event                                ) :
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . LinkVoice         ( None                                          )
    self . defaultCloseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard             ( self                                   ) :
    ##########################################################################
    IT   = self . currentItem     (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def CommandParser           ( self , language , message , timestamp      ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      self . DoPickAll        (                                              )
      return                  { "Match"   : True                           , \
                                "Message" : TRX [ "UI::SelectAll" ]          }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectNone"   , message )  ) :
      self . DoPickNone       (                                              )
      return                  { "Match"   : True                           , \
                                "Message" : TRX [ "UI::SelectNone" ]         }
    ##########################################################################
    return                    { "Match" : False                              }
  ############################################################################
  def Prepare                    ( self                                    ) :
    ##########################################################################
    self . setColumnWidth        ( 3 ,   3                                   )
    ##########################################################################
    TRX  = self . Translations
    self . setCentralLabels      ( TRX [ "TBL" ] [ "Dates" ] [ "Labels" ]    )
    ##########################################################################
    self . setPrepared           ( True                                      )
    ##########################################################################
    return
  ############################################################################
  def singleClicked ( self , item , column                                 ) :
    ##########################################################################
    self . Notify   ( 0                                                      )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column in [ 0 ]                          ) :
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . serialChanged                       )
      line . setFocus           ( Qt . TabFocusReason                        )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [ 1 ]                          ) :
      ########################################################################
      line = self . setLineEdit ( item                                     , \
                                  column                                   , \
                                  "editingFinished"                        , \
                                  self . dateChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
      ########################################################################
      return
    ##########################################################################
    if                          ( column in [ 2 ]                          ) :
      ########################################################################
      self . SwitchBonus        ( item                                       )
      ########################################################################
      return
    ##########################################################################
    return
  ############################################################################
  def PrepareItem             ( self , LDATE                               ) :
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    SID    = LDATE            [ 0                                            ]
    SERIAL = LDATE            [ 1                                            ]
    ODATE  = LDATE            [ 2                                            ]
    BONUS  = LDATE            [ 3                                            ]
    ##########################################################################
    BSTR   = ""
    if                        ( BONUS > 0                                  ) :
      ########################################################################
      BSTR = TRX              [ "TBL" ] [ "Dates" ] [ "Bonus"                ]
    ##########################################################################
    IT     = QTreeWidgetItem  (                                              )
    IT     . setText          ( 0 ,                 str ( SERIAL )           )
    IT     . setTextAlignment ( 0 , Qt.AlignRight                            )
    IT     . setData          ( 1 , Qt . UserRole , str ( SERIAL )           )
    IT     . setText          ( 1 ,                 str ( ODATE  )           )
    IT     . setData          ( 1 , Qt . UserRole , str ( ODATE  )           )
    IT     . setText          ( 2 ,                 str ( BSTR   )           )
    IT     . setData          ( 2 , Qt . UserRole , BONUS                    )
    IT     . setData          ( 3 , Qt . UserRole , SID                      )
    ##########################################################################
    return IT
  ############################################################################
  @pyqtSlot                     (        list                                )
  def refresh                   ( self , DATEs                             ) :
    ##########################################################################
    self   . clear              (                                            )
    ##########################################################################
    for D in DATEs                                                           :
      ########################################################################
      IT   = self . PrepareItem ( D                                          )
      self . addTopLevelItem    ( IT                                         )
    ##########################################################################
    TRX    = self . Translations
    msg    = TRX                [ "UI::Ready"                                ]
    self   . TtsTalk            ( msg , self . getLocality ( )               )
    ##########################################################################
    return
  ############################################################################
  def ObtainsInformation              ( self , DB                          ) :
    ##########################################################################
    self    . Total = 0
    ##########################################################################
    TBLTAB  = self . Tables           [ "Calendars"                          ]
    ##########################################################################
    QQ      = f"select count(*) from {TBLTAB} ;"
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
    TBLTAB  = self . Tables   [ "Calendars"                                  ]
    STID    = self . StartId
    AMOUNT  = self . Amount
    ORDER   = self . SortOrder
    ##########################################################################
    QQ      = f"""select `id`,`serial`,`date`,`bonus` from {TBLTAB}
                  order by `id` {ORDER}
                  limit {STID} , {AMOUNT} ;"""
    ##########################################################################
    return " " . join         ( QQ . split ( )                               )
  ############################################################################
  def LoadDates                       ( self , DB                          ) :
    ##########################################################################
    QQ      = self . ObtainUuidsQuery (                                      )
    DB      . Query                   ( QQ                                   )
    RECORDs = DB . FetchAll           (                                      )
    ##########################################################################
    if                                ( RECORDs in [ False , None ]        ) :
      return                          [                                      ]
    ##########################################################################
    if                                ( len ( RECORDs ) <= 0               ) :
      return                          [                                      ]
    ##########################################################################
    return RECORDs
  ############################################################################
  def loading                  ( self                                      ) :
    ##########################################################################
    TRX  = self . Translations
    ##########################################################################
    msg  = TRX                 [ "UI::Loading"                               ]
    self . TtsTalk             ( msg , self . getLocality ( )                )
    ##########################################################################
    msg  = TRX [ "TBL" ] [ "Dates" ] [ "Loading"                             ]
    self . ShowStatus          ( msg                                         )
    ##########################################################################
    DB   = self . ConnectDB    (                                             )
    if                         ( self . NotOkay ( DB )                     ) :
      return
    ##########################################################################
    self . Notify              ( 3                                           )
    self . OnBusy  . emit      (                                             )
    self . setBustle           (                                             )
    ##########################################################################
    FMT  = self . Translations [ "UI::StartLoading"                          ]
    MSG  = FMT . format        ( self . windowTitle ( )                      )
    self . ShowStatus          ( MSG                                         )
    ##########################################################################
    self . ObtainsInformation  ( DB                                          )
    RR   = self . LoadDates    ( DB                                          )
    ##########################################################################
    self . setVacancy          (                                             )
    self . GoRelax . emit      (                                             )
    self . ShowStatus          ( ""                                          )
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( RR ) <= 0                           ) :
      return
    ##########################################################################
    self . emitDates . emit    ( RR                                          )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def serialChanged             ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item , 3                                   )
    ##########################################################################
    if                          ( len ( msg ) <= 0                         ) :
      self . removeTopLevelItem ( item                                       )
      return
    ##########################################################################
    item   . setText            ( column ,              msg                  )
    ##########################################################################
    self   . removeParked       (                                            )
    self   . Go                 ( self . UpdateCalendarItem                , \
                                  ( uuid , "serial" , msg , )                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def dateChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    uuid   = self . itemUuid    ( item , 3                                   )
    ##########################################################################
    if                          ( len ( msg ) <= 0                         ) :
      self . removeTopLevelItem ( item                                       )
      return
    ##########################################################################
    item   . setText            ( column ,              msg                  )
    ##########################################################################
    self   . removeParked       (                                            )
    self   . Go                 ( self . UpdateCalendarItem                , \
                                  ( uuid , "date" , msg , )                  )
    ##########################################################################
    return
  ############################################################################
  def SwitchBonus             ( self , item                                ) :
    ##########################################################################
    TRX     = self . Translations
    ##########################################################################
    uuid    = self . itemUuid ( item , 3                                     )
    bonus   = self . itemUuid ( item , 2                                     )
    ##########################################################################
    if                        ( bonus == 0                                 ) :
      bonus = 1
    else                                                                     :
      bonus = 0
    ##########################################################################
    BSTR    = ""
    if                        ( bonus > 0                                  ) :
      ########################################################################
      BSTR  = TRX             [ "TBL" ] [ "Dates" ] [ "Bonus"                ]
    ##########################################################################
    item    . setText         ( 2 ,                 str ( BSTR   )           )
    item    . setData         ( 2 , Qt . UserRole , bonus                    )
    ##########################################################################
    self    . Go              ( self . UpdateCalendarItem                  , \
                                ( uuid , "bonus" , bonus , )                 )
    ##########################################################################
    return
  ############################################################################
  def UpdateCalendarItem      ( self , ID , COLUMN , VALUE                 ) :
    ##########################################################################
    DB     = self . ConnectDB (                                              )
    if                        ( self . NotOkay ( DB )                      ) :
      return
    ##########################################################################
    V      = VALUE
    ##########################################################################
    if                        ( COLUMN not in [ "bonus" ]                  ) :
      ########################################################################
      V    = f"'{VALUE}'"
    ##########################################################################
    TBLTAB = self . Tables [ "Calendars"                                    ]
    ##########################################################################
    QQ      = f"""update {TBLTAB}
                  set `{COLUMN}` = {V}
                  where ( `id` = {ID} ) ;"""
    QQ      = " " . join    ( QQ . split ( )                                 )
    DB      . Query         ( QQ                                             )
    ##########################################################################
    DB   . Close            (                                                )
    ##########################################################################
    return
  ############################################################################
  def AppendSerial          ( self                                         ) :
    ##########################################################################
    DB   = self . ConnectDB (                                                )
    if                      ( self . NotOkay ( DB )                        ) :
      return
    ##########################################################################
    NOW     = StarDate      (                                                )
    TBLTAB  = self . Tables [ "Calendars"                                    ]
    ##########################################################################
    QQ      = f"""select `serial`,`date` from {TBLTAB}
                  order by `serial` desc
                  limit 0 , 1 ;"""
    QQ      = " " . join    ( QQ . split ( )                                 )
    DB      . Query         ( QQ                                             )
    RR      = DB . FetchOne (                                                )
    ##########################################################################
    if ( RR not in [ False , None ] ) and ( len ( RR ) == 2 )                :
      ########################################################################
      S     = RR            [ 0                                              ]
      D     = RR            [ 1                                              ]
      ########################################################################
      S     = str           ( int ( int ( S ) + 1 )                          )
      ########################################################################
      NOW   . fromFormat    ( f"{D} 00:00:00" , "Asia/Taipei"                )
      CDT   = int           ( NOW . Stardate + 86400                         )
      LOOK  = True
      ########################################################################
      while LOOK                                                             :
        ######################################################################
        NOW . Stardate = CDT
        WD  = NOW . Weekday ( "Asia/Taipei"                                  )
        ######################################################################
        if                  ( WD in [ 2 , 5 ]                              ) :
          ####################################################################
          D = NOW . toDateString ( "Asia/Taipei"                             )
          LOOK = False
        ######################################################################
        CDT = int           ( CDT + 86400                                    )
      ########################################################################
      QQ    = f"""insert into {TBLTAB}
                  ( `serial` , `date` )
                  values
                  ( '{S}' , '{D}' ) ;"""
      QQ    = " " . join    ( QQ . split ( )                                 )
      DB    . Query         ( QQ                                             )
    ##########################################################################
    DB   . Close            (                                                )
    self . loading          (                                                )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot      (                                                           )
  def InsertItem ( self                                                    ) :
    ##########################################################################
    self . Go    ( self . AppendSerial                                       )
    ##########################################################################
    return
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
    ITEM   = self . itemAt              ( pos                                )
    ##########################################################################
    mm     = MenuManager                ( self                               )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    mm     = self . AmountIndexMenu     ( mm                                 )
    mm     = self . AppendRefreshAction ( mm , 1001                          )
    self   . AppendInsertAction         ( mm , 1101                          )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    mm     = self . SortingMenu         ( mm                                 )
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    mm     . setFont                    ( self    . menuFont ( )             )
    aa     = mm . exec_                 ( QCursor . pos      ( )             )
    at     = mm . at                    ( aa                                 )
    ##########################################################################
    if                                  ( self . RunAmountIndexMenu (    ) ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( self . RunSortingMenu ( at     ) ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( self . RunDocking ( mm , aa    ) ) :
      return True
    ##########################################################################
    if                                  ( at == 1001                       ) :
      ########################################################################
      self . restart                    (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 1101                       ) :
      self . InsertItem                 (                                    )
      return True
    ##########################################################################
    return True
##############################################################################
