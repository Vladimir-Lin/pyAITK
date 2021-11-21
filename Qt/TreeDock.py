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
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . TreeWidget             import TreeWidget as TreeWidget
from         . AttachDock             import AttachDock as AttachDock
from         . LineEdit               import LineEdit   as LineEdit
from         . ComboBox               import ComboBox   as ComboBox
from         . SpinBox                import SpinBox    as SpinBox
##############################################################################
class TreeDock                ( TreeWidget , AttachDock                    ) :
  ############################################################################
  attachNone = pyqtSignal     ( QWidget                                      )
  attachDock = pyqtSignal     ( QWidget , str , int , int                    )
  attachMdi  = pyqtSignal     ( QWidget , int                                )
  Clicked    = pyqtSignal     ( int                                          )
  ############################################################################
  def __init__                ( self , parent = None , plan = None         ) :
    ##########################################################################
    ## super ( TreeWidget , self ) . __init__ ( parent , plan                   )
    super (                   ) . __init__ ( parent , plan                   )
    super ( AttachDock , self ) . __init__ (                                 )
    self . InitializeDock                  (          plan                   )
    ##########################################################################
    ## WidgetClass                                                       ;
    ##########################################################################
    self . SortOrder     = "asc"
    self . Total         = 0
    self . StartId       = 0
    self . Amount        = 60
    self . LoopRunning   = True
    self . SpinStartId   = None
    self . SpinAmount    = None
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = None
    self . dockingPlaces      = None
    ## dockingPlace       ( Qt::RightDockWidgetArea     )
    ## dockingPlaces      ( Qt::TopDockWidgetArea       |
    ##                      Qt::BottomDockWidgetArea    |
    ##                      Qt::LeftDockWidgetArea      |
    ##                      Qt::RightDockWidgetArea     )
    ##########################################################################
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    self . MountClicked            ( 2                                       )
    ##########################################################################
    return
  ############################################################################
  def PrepareMessages            ( self                                    ) :
    ##########################################################################
    IDPMSG = self . Translations [ "Docking" ] [ "None"                      ]
    DCKMSG = self . Translations [ "Docking" ] [ "Dock"                      ]
    MDIMSG = self . Translations [ "Docking" ] [ "MDI"                       ]
    ##########################################################################
    self   . setLocalMessage     ( self . AttachToNone , IDPMSG              )
    self   . setLocalMessage     ( self . AttachToMdi  , MDIMSG              )
    self   . setLocalMessage     ( self . AttachToDock , DCKMSG              )
    ##########################################################################
    return
  ############################################################################
  def ObtainUuidsQuery                ( self                               ) :
    raise NotImplementedError         (                                      )
  ############################################################################
  def DefaultObtainsItemUuids         ( self , DB                          ) :
    ##########################################################################
    QQ      = self . ObtainUuidsQuery (                                      )
    UUIDs   =                         [                                      ]
    if                                ( len ( QQ ) > 0                     ) :
      UUIDs = DB   . ObtainUuids      ( QQ                                   )
    ##########################################################################
    return UUIDs
  ############################################################################
  def ObtainsItemUuids                ( self , DB                          ) :
    return self . DefaultObtainsItemUuids ( DB                               )
  ############################################################################
  def ObtainsUuidNames                ( self , DB , UUIDs                  ) :
    ##########################################################################
    NAMEs   =                         {                                      }
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      TABLE = self . Tables           [ "Names"                              ]
      NAMEs = self . GetNames         ( DB , TABLE , UUIDs                   )
    ##########################################################################
    return NAMEs
  ############################################################################
  def FetchSessionInformation         ( self , DB                          ) :
    return
  ############################################################################
  def DockIn        ( self , shown                                         ) :
    ##########################################################################
    self . ShowDock (        shown                                           )
    ##########################################################################
    return
  ############################################################################
  def Visible        ( self , visible                                      ) :
    ##########################################################################
    self . Visiblity (        visible                                        )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked       ( self , item , column                           ) :
    ##########################################################################
    uuid      = int       ( item . data ( column , Qt . UserRole )           )
    self . Clicked . emit ( uuid                                             )
    ##########################################################################
    return
  ############################################################################
  def Docking            ( self , Main , title , area , areas              ) :
    ##########################################################################
    super ( )  . Docking (        Main , self ,  title , area , areas        )
    if                   ( self . Dock == None                             ) :
      return
    ##########################################################################
    self . Dock . visibilityChanged . connect ( self . Visible               )
    ##########################################################################
    return
  ############################################################################
  def DockingMenu                    ( self , menu                         ) :
    ##########################################################################
    canDock = self . isFunction      ( self . FunctionDocking                )
    if                               ( not canDock                         ) :
      return
    ##########################################################################
    p       = self . parentWidget    (                                       )
    S       = False
    D       = False
    M       = False
    ##########################################################################
    if                               ( p == None                           ) :
      S     = True
    else                                                                     :
      ########################################################################
      if                             ( self . isDocking ( )                ) :
        D   = True
      else                                                                   :
        M   = True
    ##########################################################################
    menu    . addSeparator           (                                       )
    ##########################################################################
    if                               (     S or D                          ) :
      msg   = self . getLocalMessage ( self . AttachToMdi                    )
      menu  . addAction              ( self . AttachToMdi  , msg             )
    ##########################################################################
    if                               (     S or M                          ) :
      msg   = self . getLocalMessage ( self . AttachToDock                   )
      menu  . addAction              ( self . AttachToDock , msg             )
    ##########################################################################
    if                               ( not S                               ) :
      msg   = self . getLocalMessage ( self . AttachToNone                   )
      menu  . addAction              ( self . AttachToNone , msg             )
    ##########################################################################
    return
  ############################################################################
  def RunDocking               ( self , menu , action                      ) :
    ##########################################################################
    at = menu . at             ( action                                      )
    ##########################################################################
    if                         ( at == self . AttachToNone                 ) :
      self . attachNone . emit ( self                                        )
      return True
    ##########################################################################
    if                         ( at == self . AttachToMdi                  ) :
      self . attachMdi  . emit ( self , self . dockingOrientation            )
      return True
    ##########################################################################
    if                         ( at == self . AttachToDock                 ) :
      self . attachDock . emit ( self                                      , \
                                 self . windowTitle ( )                    , \
                                 self . dockingPlace                       , \
                                 self . dockingPlaces                        )
      return True
    ##########################################################################
    return False
  ############################################################################
  def AmountIndexMenu                 ( self , mm                          ) :
    ##########################################################################
    T    = self . Total
    MSG  = self . getMenuItem         ( "Total"                              )
    SSI  = self . getMenuItem         ( "SpinStartId"                        )
    SSA  = self . getMenuItem         ( "SpinAmount"                         )
    MSG  = MSG . format               ( T                                    )
    ##########################################################################
    mm   . addAction                  ( 9999991 , MSG                        )
    ##########################################################################
    self . SpinStartId = SpinBox      ( None , self . PlanFunc               )
    self . SpinStartId . setPrefix    ( SSI                                  )
    self . SpinStartId . setRange     ( 0 , self . Total                     )
    self . SpinStartId . setValue     ( self . StartId                       )
    self . SpinStartId . setAlignment ( Qt . AlignRight                      )
    mm   . addWidget                  ( 9999992 , self . SpinStartId         )
    ##########################################################################
    self . SpinAmount  = SpinBox      ( None , self . PlanFunc               )
    self . SpinAmount  . setPrefix    ( SSA                                  )
    self . SpinAmount  . setRange     ( 0 , self . Total                     )
    self . SpinAmount  . setValue     ( self . Amount                        )
    self . SpinAmount  . setAlignment ( Qt . AlignRight                      )
    mm   . addWidget                  ( 9999993 , self . SpinAmount          )
    ##########################################################################
    mm   . addSeparator               (                                      )
    ##########################################################################
    return mm
  ############################################################################
  def RunAmountIndexMenu                ( self                             ) :
    ##########################################################################
    if                                  ( self . SpinStartId == None       ) :
      return False
    ##########################################################################
    if                                  ( self . SpinAmount  == None       ) :
      return False
    ##########################################################################
    SID    = self . SpinStartId . value (                                    )
    AMT    = self . SpinAmount  . value (                                    )
    ##########################################################################
    self . SpinStartId = None
    self . SpinAmount  = None
    ##########################################################################
    if ( ( SID != self . StartId ) or ( AMT != self . Amount ) )             :
      ########################################################################
      self . StartId = SID
      self . Amount  = AMT
      ########################################################################
      return True
    ##########################################################################
    return   False
  ############################################################################
  def SortingMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self  . Translations
    LOM    = mm    . addMenu       ( TRX [ "UI::Sorting" ]                   )
    ##########################################################################
    hid    = self . isSortingEnabled (                                       )
    msg    = TRX                   [ "UI::SortColumns"                       ]
    mm     . addActionFromMenu     ( LOM , 20000001 , msg , True , hid       )
    ##########################################################################
    hid    =                       ( self . SortOrder == "asc"               )
    msg    = TRX                   [ "UI::SortAsc"                           ]
    mm     . addActionFromMenu     ( LOM , 20000002 , msg , True , hid       )
    ##########################################################################
    hid    =                       ( self . SortOrder == "desc"              )
    msg    = TRX                   [ "UI::SortDesc"                          ]
    mm     . addActionFromMenu     ( LOM , 20000003 , msg , True , hid       )
    ##########################################################################
    return mm
  ############################################################################
  def RunSortingMenu               ( self , atId                           ) :
    ##########################################################################
    if                             ( atId == 20000001                      ) :
      ########################################################################
      if                           ( self . isSortingEnabled ( )           ) :
        self . setSortingEnabled   ( False                                   )
      else                                                                   :
        self . setSortingEnabled   ( True                                    )
      ########################################################################
      return False
    ##########################################################################
    if                             ( atId == 20000002                      ) :
      self . SortOrder = "asc"
      return True
    ##########################################################################
    if                             ( atId == 20000003                      ) :
      self . SortOrder = "desc"
      return True
    ##########################################################################
    return   False
  ############################################################################
  def AppendRefreshAction             ( self , mm , Id                     ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX                        [ "UI::Refresh"                        ]
    icon = QIcon                      ( ":/images/reload.png"                )
    mm   . addActionWithIcon          ( Id , icon , msg                      )
    ##########################################################################
    return mm
  ############################################################################
  def AppendInsertAction              ( self , mm , Id                     ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX                        [ "UI::Insert"                         ]
    icon = QIcon                      ( ":/images/plus.png"                  )
    mm   . addActionWithIcon          ( Id , icon , msg                      )
    ##########################################################################
    return mm
  ############################################################################
  def AppendRenameAction              ( self , mm , Id                     ) :
    ##########################################################################
    TRX  = self . Translations
    msg  = TRX                        [ "UI::Rename"                         ]
    mm   . addAction                  ( Id , msg                             )
    ##########################################################################
    return mm
  ############################################################################
  def TranslateAll              ( self                                     ) :
    ##########################################################################
    DB    = self . ConnectDB    (                                            )
    if                          ( DB in [ False , None ]                   ) :
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
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################

"""
    virtual QTreeWidgetItem * addItem (QString text,SUID uuid,int column = 0);
    virtual QTreeWidgetItem * addItem (QIcon icon,QString text,SUID uuid,int column = 0);

  signals:

    DockSignals ;


QTreeWidgetItem * N::TreeDock::addItem(QString text,SUID uuid,int column)
{
  NewTreeWidgetItem (IT                      ) ;
  IT->setText       (column,text             ) ;
  IT->setData       (column,Qt::UserRole,uuid) ;
  addTopLevelItem   (IT                      ) ;
  return IT                                    ;
}

QTreeWidgetItem * N::TreeDock::addItem(QIcon icon,QString text,SUID uuid,int column)
{
  NewTreeWidgetItem (IT                      ) ;
  IT->setText       (column,text             ) ;
  IT->setIcon       (column,icon             ) ;
  IT->setData       (column,Qt::UserRole,uuid) ;
  addTopLevelItem   (IT                      ) ;
  return IT                                    ;
}

"""
