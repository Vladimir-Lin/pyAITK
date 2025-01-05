# -*- coding: utf-8 -*-
##############################################################################
## BodyShapeWidget
##############################################################################
import os
import sys
import time
import requests
import threading
import json
##############################################################################
from   PySide6                               import QtCore
from   PySide6                               import QtGui
from   PySide6                               import QtWidgets
from   PySide6 . QtCore                      import *
from   PySide6 . QtGui                       import *
from   PySide6 . QtWidgets                   import *
from   AITK    . Qt6                         import *
##############################################################################
from   AITK    . Essentials . Relation       import Relation
from   AITK    . Calendars  . StarDate       import StarDate
from   AITK    . Calendars  . Periode        import Periode
from   AITK    . Documents  . Notes          import Notes
from   AITK    . Documents  . JSON           import Save           as SaveJson
from   AITK    . Documents  . Variables      import Variables      as VariableItem
from   AITK    . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
class BodyShapeWidget    ( TreeDock                                        ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = Signal (                                                   )
  emitAllNames  = Signal (                                                   )
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    ##########################################################################
    self . ClassTag           = "BodyShapeWidget"
    self . Uuid               = 0
    self . Mode               = 0
    self . Scope              = "Features"
    self . CallbackFunctions  =    {                                         }
    self . JSON               =    {                                         }
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 3                                       )
    self . setColumnHidden         ( 2 , True                                )
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
    self . setAcceptDrops          ( False                                   )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . NoDragDrop          )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 480 , 640 )                       )
  ############################################################################
  def FocusIn              ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared ( )                     ) :
      return False
    ##########################################################################
    self . setActionLabel  ( "Label"      , self . windowTitle ( )           )
    self . LinkAction      ( "Refresh"    , self . startup                   )
    ##########################################################################
    self . LinkAction      ( "Insert"     , self . InsertItem                )
    self . LinkAction      ( "Delete"     , self . DeleteItems               )
    self . LinkAction      ( "Save"       , self . SaveToDatabase            )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard           )
    ##########################################################################
    self . LinkAction      ( "SelectAll"  , self . SelectAll                 )
    self . LinkAction      ( "SelectNone" , self . SelectNone                )
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
  def closeEvent           ( self , event                                  ) :
    ##########################################################################
    self . LinkAction      ( "Refresh"    , self . startup         , False   )
    ##########################################################################
    self . LinkAction      ( "Insert"     , self . InsertItem      , False   )
    self . LinkAction      ( "Delete"     , self . DeleteItems     , False   )
    self . LinkAction      ( "Save"       , self . SaveToDatabase  , False   )
    self . LinkAction      ( "Copy"       , self . CopyToClipboard , False   )
    ##########################################################################
    self . LinkAction      ( "SelectAll"  , self . SelectAll       , False   )
    self . LinkAction      ( "SelectNone" , self . SelectNone      , False   )
    ##########################################################################
    self . Leave . emit    ( self                                            )
    super ( ) . closeEvent ( event                                           )
    ##########################################################################
    return
  ############################################################################
  def setOwner ( self , UUID , Scope = "Features"                          ) :
    ##########################################################################
    self . Uuid  = UUID
    self . Scope = Scope
    ##########################################################################
    return
  ############################################################################
  def setConf                             ( self , CONF                    ) :
    ##########################################################################
    if                                    ( "Callback" in CONF             ) :
      CF   = CONF                         [ "Callback"                       ]
      if                                  ( CF not in [ False , None ]     ) :
        self . CallbackFunctions . append ( CF                               )
    ##########################################################################
    return
  ############################################################################
  def setJson                  ( self , JSON                               ) :
    ##########################################################################
    self . JSON = JSON
    self . emitAllNames . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def singleClicked           ( self , item , column                       ) :
    ##########################################################################
    if                        ( self . isItemPicked ( )                    ) :
      if                      ( column != self . CurrentItem [ "Column" ]  ) :
        self . removeParked   (                                              )
    ##########################################################################
    return
  ############################################################################
  def doubleClicked             ( self , item , column                     ) :
    ##########################################################################
    if                          ( column not in [ 0 , 1 ]                  ) :
      return
    ##########################################################################
    if                          ( column     in [ 0 , 1 ]                  ) :
      ########################################################################
      line = self . setLineEdit ( item                                       ,
                                  column                                     ,
                                  "editingFinished"                          ,
                                  self . nameChanged                         )
      line . setFocus           ( Qt . TabFocusReason                        )
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent  ( self , IT , KEY , VALUE                        ) :
    ##########################################################################
    IT . setText          ( 0 , str ( KEY   )                                )
    IT . setData          ( 0 , Qt . UserRole , 0                            )
    IT . setText          ( 1 , str ( VALUE )                                )
    IT . setTextAlignment ( 1 , Qt . AlignRight                              )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem             ( self , KEY , VALUE                         ) :
    ##########################################################################
    IT   = QTreeWidgetItem    (                                              )
    self . PrepareItemContent ( IT   , KEY , VALUE                           )
    ##########################################################################
    return IT
  ############################################################################
  def GetTableJson                ( self                                   ) :
    ##########################################################################
    J       =                     {                                          }
    ##########################################################################
    for i in range                ( 0 , self . topLevelItemCount ( )       ) :
      ########################################################################
      IT    = self . topLevelItem ( i                                        )
      KEY   = IT   . text         ( 0                                        )
      VALUE = IT   . text         ( 1                                        )
      ########################################################################
      if                          ( len ( KEY ) > 0                        ) :
        ######################################################################
        V   = 0
        try                                                                  :
          V = int                 ( VALUE                                    )
        except                                                               :
          pass
        ######################################################################
        J [ KEY ] = V
    ##########################################################################
    return J
  ############################################################################
  def InsertItem           ( self                                          ) :
    ##########################################################################
    IT   = QTreeWidgetItem (                                                 )
    IT   . setData         ( 0 , Qt . UserRole , 0                           )
    self . addTopLevelItem ( IT                                              )
    self . doubleClicked   ( IT , 0                                          )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems                       ( self                             ) :
    ##########################################################################
    items  = self . selectedItems       (                                    )
    for item in items                                                        :
      self . pendingRemoveItem . emit   ( item                               )
    ##########################################################################
    self   . Notify                     ( 0                                  )
    self   . JSON = self . GetTableJson (                                    )
    self   . FeedbackToCallback         (                                    )
    ##########################################################################
    return
  ############################################################################
  def refresh                        ( self                                ) :
    ##########################################################################
    self   . clear                   (                                       )
    ##########################################################################
    for K , V in self . JSON . items (                                     ) :
      ########################################################################
      IT   = self . PrepareItem      ( K , int ( V )                         )
      self . addTopLevelItem         ( IT                                    )
    ##########################################################################
    self   . emitNamesShow . emit    (                                       )
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def loading                             ( self                           ) :
    ##########################################################################
    DB          = self . ConnectDB        (                                  )
    if                                    ( DB in [ False , None ]         ) :
      self      . emitNamesShow . emit    (                                  )
      return
    ##########################################################################
    PAMTAB      = self . Tables           [ "Parameters"                     ]
    PQ          = ParameterQuery          ( 7 , 113 , self . Scope , PAMTAB  )
    self . JSON = PQ . GetJsonScopeValues ( DB , self . Uuid                 )
    ##########################################################################
    DB          . Close                   (                                  )
    ##########################################################################
    self        . emitAllNames  . emit    (                                  )
    self        . FeedbackToCallback      (                                  )
    ##########################################################################
    return
  ############################################################################
  def nameChanged                       ( self                             ) :
    ##########################################################################
    if                                  ( not self . isItemPicked ( )      ) :
      return False
    ##########################################################################
    item   = self . CurrentItem         [ "Item"                             ]
    column = self . CurrentItem         [ "Column"                           ]
    line   = self . CurrentItem         [ "Widget"                           ]
    text   = self . CurrentItem         [ "Text"                             ]
    msg    = line . text                (                                    )
    ##########################################################################
    if                                  ( msg != text                      ) :
      ########################################################################
      item . setText                    ( column , msg                       )
      self . Notify                     ( 0                                  )
    ##########################################################################
    self   . removeParked               (                                    )
    self   . JSON = self . GetTableJson (                                    )
    self   . FeedbackToCallback         (                                    )
    ##########################################################################
    return
  ############################################################################
  def FeedbackToCallback ( self                                            ) :
    ##########################################################################
    if                   ( self . Mode not in [ 0 ]                        ) :
      return
    ##########################################################################
    for CF in self . CallbackFunctions                                       :
      ########################################################################
      CF                 ( self . JSON                                       )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth ( 0               , 160                            )
    self . defaultPrepare ( self . ClassTag , 2                              )
    ##########################################################################
    return
  ############################################################################
  def SaveToDatabase ( self                                                ) :
    ##########################################################################
    self . Go        ( self . PushTablesToDatabase                           )
    ##########################################################################
    return
  ############################################################################
  def ExportJson  ( self                                                   ) :
    ##########################################################################
    Filename , _ = QFileDialog . getSaveFileName                             (
                     self                                                    ,
                     "匯出JSON" ,
                     ""                                                      ,
                     "JSON (*.json);;任意檔案類型 (*.*)" )
    if            ( len ( Filename ) <= 0                                  ) :
      return
    ##########################################################################
    J            = self . JSON
    J [ "Uuid" ] = self . Uuid
    J [ "Name" ] = self . windowTitle (                                      )
    ##########################################################################
    SaveJson      ( Filename , self . JSON                                   )
    self . Notify ( 5                                                        )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def PushTablesToDatabase           ( self                                ) :
    ##########################################################################
    DB     = self . ConnectDB        (                                       )
    if                               ( self . NotOkay ( DB )               ) :
      return
    ##########################################################################
    PAMTAB = self . Tables           [ "Parameters"                          ]
    PQ     = ParameterQuery          ( 7 , 113 , self . Scope , PAMTAB       )
    ##########################################################################
    DB     . LockWrites              ( [ PAMTAB                            ] )
    ##########################################################################
    for K , V in self . JSON . items (                                     ) :
      ########################################################################
      PQ   . assureValue             ( DB , self . Uuid , K , V              )
    ##########################################################################
    DB     . UnlockTables            (                                       )
    DB     . Close                   (                                       )
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction      ( self . HavingMenu                      )
    if                              ( not doMenu                           ) :
      return False
    ##########################################################################
    self   . Notify                 ( 0                                      )
    ##########################################################################
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    if                             ( self . Mode in [ 0 ]                  ) :
      self . AppendRefreshAction   ( mm , 1001                               )
    ##########################################################################
    self   . AppendInsertAction    ( mm , 1101                               )
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      self . AppendDeleteAction    ( mm , 1102                               )
    ##########################################################################
    if                             ( self . Mode in [ 0 ]                  ) :
      ########################################################################
      msg  = self . getMenuItem    ( "Save"                                  )
      icon = QIcon                 ( ":/images/save.png"                     )
      mm   . addActionWithIcon     ( 1103 , icon , msg                       )
      ########################################################################
      msg  = self . getMenuItem    ( "ExportJson"                            )
      mm   . addAction             ( 1104 , msg                              )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . SortingMenu           ( mm                                      )
    self   . DockingMenu           ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . RunSortingMenu     ( at )      ) :
      if                           ( self . Mode in [ 0 ]                  ) :
        self . restart             (                                         )
      return True
    ##########################################################################
    if                             ( at == 1001                            ) :
      if                           ( self . Mode in [ 0 ]                  ) :
        self . restart             (                                         )
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
    if                             ( at == 1103                            ) :
      self . SaveToDatabase        (                                         )
      return True
    ##########################################################################
    if                             ( at == 1104                            ) :
      self . ExportJson            (                                         )
      return True
    ##########################################################################
    return True
##############################################################################
