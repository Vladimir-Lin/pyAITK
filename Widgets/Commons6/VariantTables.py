# -*- coding: utf-8 -*-
##############################################################################
## VariantTables
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
from   PySide6                            import QtCore
from   PySide6                            import QtGui
from   PySide6                            import QtWidgets
from   PySide6 . QtCore                   import *
from   PySide6 . QtGui                    import *
from   PySide6 . QtWidgets                import *
from   AITK    . Qt6                      import *
##############################################################################
from   AITK    . Qt6        . MenuManager import MenuManager as MenuManager
from   AITK    . Qt6        . TreeDock    import TreeDock    as TreeDock
##############################################################################
from   AITK    . Essentials . Relation    import Relation
from   AITK    . Calendars  . StarDate    import StarDate
from   AITK    . Calendars  . Periode     import Periode
from   AITK    . Documents  . Notes       import Notes
from   AITK    . Documents  . Variables   import Variables   as VariableItem
##############################################################################
from   AITK    . Scheduler  . Projects    import Projects    as Projects
from   AITK    . Scheduler  . Project     import Project     as Project
from   AITK    . Scheduler  . Tasks       import Tasks       as Tasks
from   AITK    . Scheduler  . Task        import Task        as Task
from   AITK    . Scheduler  . Events      import Events      as Events
from   AITK    . Scheduler  . Event       import Event       as Event
##############################################################################
class VariantTables      ( TreeDock                                        ) :
  ############################################################################
  HavingMenu    = 1371434312
  ############################################################################
  emitNamesShow = Signal (                                                   )
  emitAllNames  = Signal (                                                   )
  OpenSmartNote = Signal ( str , str , str , int                             )
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ (        parent        , plan                       )
    ##########################################################################
    self . ClassTag           = "VariantTables"
    self . Uuid               = 0
    self . Type               = 0
    self . Name               = ""
    self . Mode               = 0
    self . CallbackFunction   = None
    self . JSON               = { }
    self . SortOrder          = "desc"
    self . TITLE              = ""
    self . MODIFIED           = False
    ##########################################################################
    self . dockingOrientation = 0
    self . dockingPlace       = Qt . BottomDockWidgetArea
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
    self . setMinimumSize          ( 160 , 160                               )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 480 , 600 )                       )
  ############################################################################
  def PrepareForActions               ( self                               ) :
    ##########################################################################
    self . TITLE = self . windowTitle (                                      )
    ##########################################################################
    self . AppendSideActionWithIcon   ( "CopyTableToClipboard"             , \
                                        ":/images/copy.png"                , \
                                        self . CopyTableToClipboard        , \
                                        True                               , \
                                        False                                )
    self . AppendSideActionWithIcon   ( "PasteFromClipboard"               , \
                                        ":/images/paste.png"               , \
                                        self . PasteFromClipboard          , \
                                        True                               , \
                                        False                                )
    self . AppendSideActionWithIcon   ( "Save"                             , \
                                        ":/images/save.png"                , \
                                        self . SaveToDatabase              , \
                                        True                               , \
                                        False                                )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Save"       , self . SaveToDatabase  , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyToClipboard , Enabled      )
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
  def twiceClicked                ( self , item , column                   ) :
    ##########################################################################
    if                            ( column not in [ 0 , 1 ]                ) :
      ########################################################################
      self . defaultSingleClicked (        item , column                     )
      ########################################################################
      return
    ##########################################################################
    if                            ( column     in [ 0 , 1 ]                ) :
      ########################################################################
      line = self . setLineEdit   ( item                                     ,
                                    column                                   ,
                                    "editingFinished"                        ,
                                    self . nameChanged                       )
      line . setFocus             ( Qt . TabFocusReason                      )
    ##########################################################################
    return
  ############################################################################
  def setOwner        ( self , UUID , TYPE , NAME , JSON                   ) :
    ##########################################################################
    self . Uuid = int ( UUID                                                 )
    self . Type = int ( TYPE                                                 )
    self . Name = str ( NAME                                                 )
    self . JSON = JSON
    ##########################################################################
    return
  ############################################################################
  def PrepareItemContent ( self , IT , KEY , VALUE                         ) :
    ##########################################################################
    IT . setText         ( 0 , KEY                                           )
    IT . setData         ( 0 , Qt . UserRole , 0                             )
    IT . setText         ( 1 , VALUE                                         )
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
      TABLE = IT   . text         ( 1                                        )
      ########################################################################
      if                          ( len ( KEY ) > 0                        ) :
        J [ KEY ] = TABLE
    ##########################################################################
    return J
  ############################################################################
  def InsertItem           ( self                                          ) :
    ##########################################################################
    IT   = QTreeWidgetItem (                                                 )
    IT   . setData         ( 0 , Qt . UserRole , 0                           )
    self . addTopLevelItem ( IT                                              )
    self . twiceClicked    ( IT , 0                                          )
    self . Notify          ( 0                                               )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems                       ( self                             ) :
    ##########################################################################
    items  = self . selectedItems       (                                    )
    for item in items                                                        :
      self . pendingRemoveItem . emit   ( item                               )
    ##########################################################################
    self   . Notify                     ( 4                                  )
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
      IT   = self . PrepareItem      ( K , V                                 )
      self . addTopLevelItem         ( IT                                    )
    ##########################################################################
    self   . emitNamesShow . emit    (                                       )
    self   . Notify                  ( 5                                     )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB in [ False , None ]             ) :
      self  . emitNamesShow . emit    (                                      )
      return
    ##########################################################################
    self    . JSON = self . ObtainsOwnerVariantTables                      ( \
                                        DB                                 , \
                                        self . Uuid                        , \
                                        self . Type                        , \
                                        self . Name                        , \
                                        self . JSON                          )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    self    . emitAllNames  . emit    (                                      )
    ##########################################################################
    return
  ############################################################################
  def nameChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    line   = self . CurrentItem [ "Widget"                                   ]
    text   = self . CurrentItem [ "Text"                                     ]
    msg    = line . text        (                                            )
    ##########################################################################
    if                          ( msg != text                              ) :
      ########################################################################
      item . setText            ( column ,              msg                  )
      self . Notify             ( 0                                          )
    ##########################################################################
    self   . removeParked       (                                            )
    self   . JSON = self . GetTableJson (                                    )
    self   . FeedbackToCallback (                                            )
    ##########################################################################
    return
  ############################################################################
  def FeedbackToCallback    ( self                                         ) :
    ##########################################################################
    self . Notify           ( 0                                              )
    ##########################################################################
    if                      ( self . Mode not in [ 1 ]                     ) :
      return
    ##########################################################################
    if                      ( self . NotOkay ( self . CallbackFunction )   ) :
      return
    ##########################################################################
    self . CallbackFunction ( self . JSON                                    )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . setColumnWidth ( 0 , 160                                          )
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
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def PushTablesToDatabase      ( self                                     ) :
    ##########################################################################
    DB     = self . ConnectDB   (                                            )
    if                          ( DB in self . EmptySet                    ) :
      return
    ##########################################################################
    BODY   = json . dumps       ( self . JSON , ensure_ascii = False         )
    try                                                                      :
      BODY = BODY . encode      ( 'utf8'                                     )
    except                                                                   :
      pass
    ##########################################################################
    VARTAB = self . Tables      [ "Variables"                                ]
    ## VARTAB = "`factors`.`variables_apps_0031`"
    DB     . LockWrites         ( [ VARTAB                                 ] )
    VARI   = VariableItem       (                                            )
    VARI   . Uuid  = self . Uuid
    VARI   . Type  = self . Type
    VARI   . Name  = self . Name
    VARI   . Value = BODY
    VARI   . AssureValue        ( DB , VARTAB                                )
    DB     . UnlockTables       (                                            )
    ##########################################################################
    DB     . Close              (                                            )
    ##########################################################################
    self   . Notify             ( 5                                          )
    MSG    = self . getMenuItem ( "SaveCompleted"                            )
    self   . Talk               ( MSG , self . getLocality (               ) )
    ##########################################################################
    return
  ############################################################################
  def CopyTableToClipboard         ( self                                  ) :
    ##########################################################################
    qApp . clipboard ( ) . setText ( json . dumps ( self . JSON            ) )
    ##########################################################################
    self . Notify                  ( 0                                       )
    ##########################################################################
    return
  ############################################################################
  def PasteFromClipboard                ( self                             ) :
    ##########################################################################
    JTEXT = qApp . clipboard ( ) . text (                                    )
    ##########################################################################
    if                                  ( len ( JTEXT ) <= 0               ) :
      return
    ##########################################################################
    try                                                                      :
      ########################################################################
      JT  = json . loads                ( JTEXT                              )
      ########################################################################
    except                                                                   :
      return
    ##########################################################################
    self  . JSON = JT
    ##########################################################################
    self  . refresh                     (                                    )
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
    if                             ( self . Mode in [ 0 ]                  ) :
      msg  = self . getMenuItem    ( "Save"                                  )
      icon = QIcon                 ( ":/images/save.png"                     )
      mm   . addActionWithIcon     ( 1102 , icon , msg                       )
    ##########################################################################
    if                             ( atItem not in [ False , None ]        ) :
      ########################################################################
      self . AppendDeleteAction    ( mm , 1103                               )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    msg    = self . getMenuItem    ( "CopyTableToClipboard"                  )
    icon   = QIcon                 ( ":/images/copy.png"                     )
    mm     . addActionWithIcon     ( 4001 , icon , msg                       )
    ##########################################################################
    msg    = self . getMenuItem    ( "PasteFromClipboard"                    )
    icon   = QIcon                 ( ":/images/paste.png"                    )
    mm     . addActionWithIcon     ( 4002 , icon , msg                       )
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
      ########################################################################
      self . InsertItem            (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1102                            ) :
      ########################################################################
      self . SaveToDatabase        (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1103                            ) :
      ########################################################################
      self . DeleteItems           (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( 4001 == at                            ) :
      ########################################################################
      self . CopyTableToClipboard  (                                         )
      ########################################################################
      return True
    ##########################################################################
    if                             ( 4002 == at                            ) :
      ########################################################################
      self . PasteFromClipboard    (                                         )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
