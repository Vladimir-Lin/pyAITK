# -*- coding: utf-8 -*-
##############################################################################
## NamesEditor
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
from   opencc                              import OpenCC
##############################################################################
from   PySide6                             import QtCore
from   PySide6                             import QtGui
from   PySide6                             import QtWidgets
from   PySide6 . QtCore                    import *
from   PySide6 . QtGui                     import *
from   PySide6 . QtWidgets                 import *
from   AITK    . Qt6                       import *
##############################################################################
from   AITK    . Linguistics . Translator  import Translate
from   AITK    . Documents   . Name        import Name        as NameItem
##############################################################################
class NamesEditor            ( TreeDock , NameItem                         ) :
  ############################################################################
  HavingMenu        = 1371434312
  ############################################################################
  emitNamesShow     = Signal (                                               )
  emitAllNames      = Signal ( list                                          )
  emitNewItem       = Signal ( list                                          )
  emitRefreshItem   = Signal ( QTreeWidgetItem , list                        )
  CloseMyself       = Signal ( QWidget , str                                 )
  ############################################################################
  def __init__               ( self , parent = None , plan = None          ) :
    ##########################################################################
    super (                 ) . __init__ ( parent , plan                     )
    super ( NameItem , self ) . __init__ (                                   )
    ##########################################################################
    self . dockingOrientation = 0
    ## self . dockingOrientation = Qt . Horizontal
    self . dockingPlace       = Qt . BottomDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea
    ##########################################################################
    self . setFunction     ( self . FunctionDocking , True                   )
    self . setFunction     ( self . HavingMenu      , True                   )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 800 , 360 )                       )
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendSideActionWithIcon ( "AddItem"                            , \
                                      ":/images/plus.png"                  , \
                                      self . InsertItem                    , \
                                      True                                 , \
                                      False                                  )
    self . AppendSideActionWithIcon ( "QuickAdd"                           , \
                                      ":/images/quick-add.png"             , \
                                      self . QuickAppending                , \
                                      True                                 , \
                                      False                                  )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self      ,                          Enabled       ) :
    ##########################################################################
    self . LinkAction ( "Refresh" , self . startup         , Enabled         )
    self . LinkAction ( "Insert"  , self . InsertItem      , Enabled         )
    self . LinkAction ( "Delete"  , self . DeleteItems     , Enabled         )
    self . LinkAction ( "Copy"    , self . CopyToClipboard , Enabled         )
    self . LinkAction ( "Paste"   , self . PasteItems      , Enabled         )
    self . LinkAction ( "Rename"  , self . RenameItem      , Enabled         )
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
  def Prepare                      ( self                                  ) :
    ##########################################################################
    Names  = self . Translations   [ "NamesEditor" ] [ "Labels"              ]
    MENUs  = self . Translations   [ "NamesEditor" ] [ "Menus"               ]
    Items  = self . tableItems     (                                         )
    ##########################################################################
    self   . setMenus              ( MENUs                                   )
    ##########################################################################
    self   . defaultLocality  = 1001
    self   . defaultRelevance =    0
    self   . ShowCompact      = True
    self   . DisableCompact   = True
    ##########################################################################
    self   . KEYs =                [ "id"                                    ,
                                     "name"                                  ,
                                     "locality"                              ,
                                     "relevance"                             ,
                                     "priority"                              ,
                                     "flags"                                 ,
                                     "utf8"                                  ,
                                     "length"                                ,
                                     "ltime"                                 ]
    ##########################################################################
    TOTAL    = len                 ( self . KEYs                             )
    self     . setColumnCount      ( TOTAL + 1                               )
    ##########################################################################
    LABELs   =                     [                                         ]
    for it in self . KEYs                                                    :
      LABELs . append              ( Names [ it ]                            )
    LABELs   . append              ( ""                                      )
    self     . setCentralLabels    ( LABELs                                  )
    ##########################################################################
    self     . setColumnWidth      ( 1         , 320                         )
    self     . setColumnWidth      ( 2         , 160                         )
    self     . setColumnWidth      ( 3         , 100                         )
    self     . setColumnWidth      ( 4         , 100                         )
    self     . setColumnWidth      ( 6         ,  60                         )
    self     . setColumnWidth      ( 7         ,  60                         )
    self     . setColumnWidth      ( TOTAL     , 3                           )
    ##########################################################################
    self     . setColumnHidden     ( 0         , True                        )
    self     . setColumnHidden     ( TOTAL - 1 , True                        )
    ##########################################################################
    self     . setRootIsDecorated  ( False                                   )
    self     . setAlternatingRowColors ( True                                )
    ##########################################################################
    self     . emitNamesShow   . connect ( self . show                       )
    self     . emitAllNames    . connect ( self . refresh                    )
    self     . emitNewItem     . connect ( self . appendJsonItem             )
    self     . emitRefreshItem . connect ( self . RefreshItem                )
    ##########################################################################
    self     . MountClicked        ( 1                                       )
    self     . MountClicked        ( 2                                       )
    ##########################################################################
    self     . assignSelectionMode ( "ContiguousSelection"                   )
    ##########################################################################
    self     . setPrepared         ( True                                    )
    self     . PrepareForActions   (                                         )
    ##########################################################################
    return
  ############################################################################
  def Configure                  ( self                                    ) :
    return
  ############################################################################
  def CloseCompact ( self                                                  ) :
    ##########################################################################
    if             ( not self . DisableCompact                             ) :
      return
    ##########################################################################
    self . ShowCompact    = False
    self . DisableCompact = False
    ##########################################################################
    return
  ############################################################################
  def appendJsonItem             ( self , JSON                             ) :
    ##########################################################################
    item = self . jsonToItem     ( JSON                                      )
    self . addTopLevelItem       ( item                                      )
    self . setCurrentItem        ( item                                      )
    ##########################################################################
    return
  ############################################################################
  def singleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( self . isItemPicked ( )                 ) :
      if ( column != self . CurrentItem [ "Column" ] )                       :
        self . removeParked      (                                           )
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in [ 1 , 2 , 3 , 4 , 5 ]     ) :
      return
    ##########################################################################
    if                           ( column == 1                             ) :
      ########################################################################
      line = self . setLineEdit  ( item                                      ,
                                   column                                    ,
                                   "editingFinished"                         ,
                                   self . nameChanged                        )
      line . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    elif                         ( column == 2                             ) :
      ########################################################################
      LL   = self . Translations [ "NamesEditor" ] [ "Languages"             ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . localityChanged                    )
      cb   . addJson             ( LL , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
    ##########################################################################
    elif                         ( column == 3                             ) :
      ########################################################################
      RR   = self . Translations [ "NamesEditor" ] [ "Relevance"             ]
      val  = item . data         ( column , Qt . UserRole                    )
      val  = int                 ( val                                       )
      cb   = self . setComboBox  ( item                                      ,
                                   column                                    ,
                                   "activated"                               ,
                                   self . relevanceChanged                   )
      cb   . addJson             ( RR , val                                  )
      cb   . setMaxVisibleItems  ( 20                                        )
      cb   . showPopup           (                                           )
    ##########################################################################
    elif                         ( column in [ 4 , 5 ]                     ) :
      ########################################################################
      sb   = self . setSpinBox   ( item                                      ,
                                   column                                    ,
                                   0                                         ,
                                   999999999                                 ,
                                   "editingFinished"                         ,
                                   self . spinChanged                        )
      sb   . setAlignment        ( Qt . AlignRight                           )
      sb   . setFocus            ( Qt . TabFocusReason                       )
    ##########################################################################
    elif                         ( column == 5                             ) :
      pass
    ##########################################################################
    return
  ############################################################################
  def stateChanged               ( self , item , column                    ) :
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
      pid  = int                ( item . text ( 0 )                          )
      bmsg = str . encode       ( msg                                        )
      ########################################################################
      item . setText            ( column ,              msg                  )
      item . setText            ( 6      , str ( len (  msg ) )              )
      item . setText            ( 7      , str ( len ( bmsg ) )              )
      ########################################################################
      self . Go                 ( self . UpdateUuidName                    , \
                                  ( item , pid , msg , )                     )
    ##########################################################################
    self   . removeParked       (                                            )
    ##########################################################################
    return
  ############################################################################
  def localityChanged            ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    cb     = self . CurrentItem  [ "Widget"                                  ]
    cbv    = self . CurrentItem  [ "Value"                                   ]
    index  = cb   . currentIndex (                                           )
    value  = cb   . itemData     ( index                                     )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      pid  = int                 ( item . text ( 0 )                         )
      LL   = self . Translations [ "NamesEditor" ] [ "Languages"             ]
      msg  = LL                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      self . Go                  ( self . UpdateByLocality                 , \
                                   ( item , pid , value , )                  )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def relevanceChanged           ( self                                    ) :
    ##########################################################################
    if                           ( not self . isItemPicked ( )             ) :
      return False
    ##########################################################################
    item   = self . CurrentItem  [ "Item"                                    ]
    column = self . CurrentItem  [ "Column"                                  ]
    cb     = self . CurrentItem  [ "Widget"                                  ]
    cbv    = self . CurrentItem  [ "Value"                                   ]
    index  = cb   . currentIndex (                                           )
    value  = cb   . itemData     ( index                                     )
    cbv    = int                 ( cbv                                       )
    value  = int                 ( value                                     )
    ##########################################################################
    if                           ( value != cbv                            ) :
      ########################################################################
      pid  = int                 ( item . text ( 0 )                         )
      RR   = self . Translations [ "NamesEditor" ] [ "Relevance"             ]
      msg  = RR                  [ str ( value )                             ]
      ########################################################################
      item . setText             ( column ,  msg                             )
      item . setData             ( column , Qt . UserRole , value            )
      ########################################################################
      self . Go                  ( self . UpdateByRelevance                , \
                                   ( item , pid , value , )                  )
    ##########################################################################
    self   . removeParked        (                                           )
    ##########################################################################
    return
  ############################################################################
  def spinChanged               ( self                                     ) :
    ##########################################################################
    if                          ( not self . isItemPicked ( )              ) :
      return False
    ##########################################################################
    item   = self . CurrentItem [ "Item"                                     ]
    column = self . CurrentItem [ "Column"                                   ]
    sb     = self . CurrentItem [ "Widget"                                   ]
    v      = self . CurrentItem [ "Value"                                    ]
    v      = int                ( v                                          )
    nv     = sb   . value       (                                            )
    ##########################################################################
    if                          ( v != nv                                  ) :
      ########################################################################
      pid  = int                ( item . text ( 0 )                          )
      ########################################################################
      item . setText            ( column , str ( nv )                        )
      ########################################################################
      if                        ( column == 4                              ) :
        self . Go               ( self . UpdateByPriority                  , \
                                  ( item , pid , nv , )                      )
      elif                      ( column == 5                              ) :
        self . Go               ( self . UpdateByFlags                     , \
                                  ( item , pid , nv , )                      )
    ##########################################################################
    self . removeParked         (                                            )
    ##########################################################################
    return
  ############################################################################
  def InsertItem                 ( self                                    ) :
    ##########################################################################
    self . Go                    ( self . AppendItem                         )
    ##########################################################################
    return
  ############################################################################
  def DeleteItems                             ( self                       ) :
    ##########################################################################
    items        = self . selectedItems       (                              )
    if                                        ( len ( items ) <= 0         ) :
      return
    ##########################################################################
    Listings     =                            [                              ]
    for it in items                                                          :
      i          = self . indexOfTopLevelItem ( it                           )
      if                                      ( i >= 0                     ) :
        pid      = it . text                  ( 0                            )
        pid      = int                        ( pid                          )
        self     . takeTopLevelItem           ( i                            )
        Listings . append                     ( pid                          )
    ##########################################################################
    if                                        ( len ( Listings ) <= 0      ) :
      return
    ##########################################################################
    self         . Go ( self . RemoveItems , ( Listings , )                  )
    ##########################################################################
    return
  ############################################################################
  def RenameItem            ( self                                         ) :
    ##########################################################################
    IT = self . currentItem (                                                )
    if                      ( IT is None                                   ) :
      return
    ##########################################################################
    self . doubleClicked    ( IT , 1                                         )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard             ( self                                   ) :
    ##########################################################################
    IT   = self . currentItem     (                                          )
    if                            ( IT is None                             ) :
      return
    ##########################################################################
    MSG  = IT . text              ( 1                                        )
    LID  = IT . data              ( 2 , Qt . UserRole                        )
    LID  = int                    ( LID                                      )
    qApp . clipboard ( ). setText ( MSG                                      )
    ##########################################################################
    self . Go                     ( self . Talk , ( MSG , LID , )            )
    ##########################################################################
    return
  ############################################################################
  def ColumnsMenu                  ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    COL    = mm . addMenu          ( TRX [ "UI::Columns" ]                   )
    ##########################################################################
    for i , it in enumerate        ( self . KEYs                           ) :
       msg = TRX [ "NamesEditor" ] [ "Labels" ] [ it ]
       hid = self . isColumnHidden ( i                                       )
       mm  . addActionFromMenu     ( COL , 9000 + i , msg , True , not hid   )
    ##########################################################################
    K      = len                   ( self . KEYs                             )
    msg    = TRX                   [ "UI::Whitespace"                        ]
    hid    = self . isColumnHidden ( K                                       )
    mm     . addActionFromMenu     ( COL , 9000 + K , msg , True , not hid   )
    ##########################################################################
    return mm
  ############################################################################
  def TranslationsMenu             ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations   [ "Translations"                          ]
    msg    = self . Translations   [ "UI::Translations"                      ]
    KEYs   = TRX  . keys           (                                         )
    ##########################################################################
    LOT    = mm . addMenu          ( msg                                     )
    ##########################################################################
    for K in KEYs                                                            :
       msg = TRX                   [ K                                       ]
       V   = int                   ( K                                       )
       mm  . addActionFromMenu     ( LOT , V , msg                           )
    ##########################################################################
    return mm
  ############################################################################
  def LocalityMenu                 ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    LOC    = self . Translations   [ "NamesEditor" ] [ "Languages"           ]
    ##########################################################################
    msg    = TRX  [ "NamesEditor" ] [ "Menus" ] [ "Language"                 ]
    LOM    = mm . addMenu          ( msg                                     )
    ##########################################################################
    KEYs   = LOC . keys            (                                         )
    ##########################################################################
    for K in KEYs                                                            :
       msg = LOC                   [ K                                       ]
       V   = int                   ( K                                       )
       hid =                       ( V == self . defaultLocality             )
       mm  . addActionFromMenu     ( LOM , 10000000 + V , msg , True , hid   )
    ##########################################################################
    return mm
  ############################################################################
  def TranslateMenu                ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    LOC    = self . Translations   [ "NamesEditor" ] [ "Languages"           ]
    ##########################################################################
    msg    = TRX                   [ "UI::Translate"                         ]
    LOM    = mm . addMenu          ( msg                                     )
    ##########################################################################
    KEYs   = LOC . keys            (                                         )
    ##########################################################################
    for K in KEYs                                                            :
      ########################################################################
      V    = int                   ( K                                       )
      if                           ( V in [ 0 , 1004 , 1005 ]              ) :
        continue
      msg  = LOC                   [ K                                       ]
      mm   . addActionFromMenu     ( LOM , 11000000 + V , msg                )
    ##########################################################################
    return mm
  ############################################################################
  def RunTranslate                     ( self , menu , action              ) :
    ##########################################################################
    items  = self . selectedItems      (                                     )
    ##########################################################################
    if                                 ( len ( items ) != 1                ) :
      return False
    ##########################################################################
    at     = menu . at                 (               action                )
    ##########################################################################
    if                                 ( at < 11000000                     ) :
      return False
    ##########################################################################
    if                                 ( at > 11100000                     ) :
      return False
    ##########################################################################
    IT     = items                     [ 0                                   ]
    LID    = at   - 11000000
    DID    = self . defaultLocality
    SRC    = self . LocalityToGoogleLC ( DID                                 )
    DEST   = self . LocalityToGoogleLC ( LID                                 )
    ##########################################################################
    if                                 ( len ( SRC ) <= 0                  ) :
      return True
    ##########################################################################
    if                                 ( len ( DEST ) <= 0                 ) :
      return True
    ##########################################################################
    pid    = IT . text                 ( 0                                   )
    txt    = IT . text                 ( 1                                   )
    pid    = int                       ( pid                                 )
    ##########################################################################
    if                                 ( len ( txt ) <= 0                  ) :
      return True
    ##########################################################################
    target = Translate                 ( txt , SRC , DEST                    )
    target = target . replace          ( "·" , "・" )
    UTF8   = len                       ( target                              )
    ##########################################################################
    if                                 ( UTF8 <= 0                         ) :
      return True
    ##########################################################################
    LENZ   = 0
    ##########################################################################
    try                                                                      :
      S    = target . encode           ( "utf-8"                             )
      LENZ = len                       ( S                                   )
    except                                                                   :
      return True
    ##########################################################################
    IT     . setText                   ( 1 , target                          )
    IT     . setText                   ( 6 , str ( UTF8 )                    )
    IT     . setText                   ( 7 , str ( LENZ )                    )
    ##########################################################################
    self   . Go                        ( self . UpdateUuidName             , \
                                         ( IT , pid , target , )             )
    ##########################################################################
    return False
  ############################################################################
  def RelevanceMenu                ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    REL    = self . Translations   [ "NamesEditor" ] [ "Relevance"           ]
    ##########################################################################
    msg    = TRX  [ "NamesEditor" ] [ "Menus" ] [ "Relevance" ]
    LOR    = mm . addMenu          ( msg                                     )
    ##########################################################################
    KEYs   = REL . keys            (                                         )
    ##########################################################################
    for K in KEYs                                                            :
       msg = REL                   [ K                                       ]
       V   = int                   ( K                                       )
       hid =                       ( V == self . defaultRelevance            )
       mm  . addActionFromMenu     ( LOR , 8000 + V , msg , True , hid       )
    ##########################################################################
    return mm
  ############################################################################
  def HandleTranslations           ( self , item , ID                      ) :
    ##########################################################################
    if                             ( ( ID < 7001 ) or ( ID > 7008 )        ) :
      return False
    ##########################################################################
    CODE   = self . ConvertCCCcode ( int ( ID - 7000  )                      )
    ##########################################################################
    if                             ( len ( CODE ) <= 0                     ) :
      return False
    ##########################################################################
    pid    = item . text           ( 0                                       )
    text   = item . text           ( 1                                       )
    pid    = int                   ( pid                                     )
    cc     = OpenCC                ( CODE                                    )
    target = cc . convert          ( text                                    )
    UTF8   = len                   ( target                                  )
    LENZ   = 0
    ##########################################################################
    try                                                                      :
      S    = target . encode       ( "utf-8"                                 )
      LENZ = len                   ( S                                       )
    except                                                                   :
      return True
    ##########################################################################
    item   . setText               ( 1 , target                              )
    item   . setText               ( 6 , str ( UTF8 )                        )
    item   . setText               ( 7 , str ( LENZ )                        )
    ##########################################################################
    VAL    =                       ( item , pid , target ,                   )
    self   . Go                    ( self . UpdateUuidName , VAL             )
    ##########################################################################
    return True
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    items  = self . selectedItems  (                                         )
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    self   . AppendRefreshAction   ( mm , 1001                               )
    mm     . addSeparator          (                                         )
    ##########################################################################
    self   . AppendInsertAction    ( mm , 1101                               )
    ##########################################################################
    msg    = self . getMenuItem    ( "QuickAdd"                              )
    icon   = QIcon                 ( ":/images/add.png"                      )
    mm     . addActionWithIcon     ( 2001 , icon , msg                       )
    ##########################################################################
    if                             ( len ( items ) > 0                     ) :
      self . AppendDeleteAction    ( mm , 1102                               )
      if ( self . canSpeak ( ) ) and ( len ( items ) == 1 )                  :
        mm . addAction             ( 1501 ,  TRX [ "UI::Talk"  ]             )
    ##########################################################################
    mm     . addSeparator          (                                         )
    mm     . addAction             ( 1801                                  , \
                                     TRX [ "UI::AutoCompact" ]             , \
                                     True                                  , \
                                     self . ShowCompact                      )
    mm     . addSeparator          (                                         )
    self   . AppendTranslateAllAction ( mm , 3001                            )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . ColumnsMenu      ( mm                                    )
    if                               ( len ( items ) == 1                  ) :
      mm   = self . TranslateMenu    ( mm                                    )
      mm   = self . TranslationsMenu ( mm                                    )
    mm     = self . LocalityMenu     ( mm                                    )
    mm     = self . RelevanceMenu    ( mm                                    )
    self   . DockingMenu             ( mm                                    )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunDocking   ( mm , aa )       ) :
      return True
    ##########################################################################
    if                             ( self . RunTranslate ( mm , aa )       ) :
      return True
    ##########################################################################
    if ( ( at >= 10000000 ) and ( at < 11000000 ) )                          :
      self . defaultLocality  = at - 10000000
      return True
    ##########################################################################
    if                             ( len ( items ) == 1                    ) :
      if ( self . HandleTranslations ( items [ 0 ] , at )                  ) :
        return True
    ##########################################################################
    if                             ( at >= 9000                            ) :
      col  = at - 9000
      hid  = self . isColumnHidden ( col                                     )
      self . setColumnHidden       ( col , not hid                           )
      return True
    ##########################################################################
    if                             ( at >= 8000                            ) :
      self . defaultRelevance = at - 8000
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
    if                             ( at == 1501                            ) :
      ########################################################################
      item = items                 [ 0                                       ]
      T    = item . text           ( 1                                       )
      L    = item . data           ( 2 , Qt . UserRole                       )
      L    = int                   ( L                                       )
      ########################################################################
      self . Talk                  ( T , L                                   )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 1801                            ) :
      self . ShowCompact =         ( not self . ShowCompact                  )
    ##########################################################################
    if                             ( 2001 == at                            ) :
      ########################################################################
      self . Go                    ( self . QuickAppending                   )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 3001                            ) :
      self . Go                    ( self . TranslateAll                     )
      return True
    ##########################################################################
    return True
  ############################################################################
  def TryClose                   ( self                                    ) :
    ##########################################################################
    self . setPrepared           ( False                                     )
    self . CloseMyself . emit    ( self , str ( self . get ( "uuid" ) )      )
    self . Leave       . emit    ( self                                      )
    ##########################################################################
    return True
  ############################################################################
  def UpdateUuidName                ( self , item , pid , name             ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    ##########################################################################
    self   . set                    ( "id"   , pid                           )
    self   . set                    ( "name" , name                          )
    ##########################################################################
    DB     . LockWrites             ( [ TABLE ]                              )
    self   . UpdateNameById         ( DB , TABLE                             )
    DB     . UnlockTables           (                                        )
    ##########################################################################
    DB     . Close                  (                                        )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def UpdateMajorParameters         ( self , DB , TABLE                    ) :
    ##########################################################################
    IDX    = self . GetPosition     (        DB , TABLE                      )
    if                              ( IDX < 0                              ) :
      DB   . LockWrites             ( [ TABLE ]                              )
      self . UpdateParametersById   (        DB , TABLE                      )
      DB   . UnlockTables           (                                        )
    ##########################################################################
    self   . ObtainsById            (        DB , TABLE                      )
    ##########################################################################
    return self . toList            (                                        )
  ############################################################################
  def UpdateByLocality              ( self , item , pid , locality         ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    JSON   = self . itemToJson      ( item                                   )
    ##########################################################################
    self   . set                    ( "id"        , pid                      )
    self   . set                    ( "locality"  , locality                 )
    self   . set                    ( "relevance" , JSON [ "Relevance" ]     )
    self   . set                    ( "priority"  , JSON [ "Priority"  ]     )
    ##########################################################################
    CRX    = self . UpdateMajorParameters ( DB , TABLE                       )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    self   . emitRefreshItem . emit ( item , CRX                             )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def UpdateByRelevance             ( self , item , pid , relevance        ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    JSON   = self . itemToJson      ( item                                   )
    ##########################################################################
    self   . set                    ( "id"        , pid                      )
    self   . set                    ( "locality"  , JSON [ "Locality"  ]     )
    self   . set                    ( "relevance" , relevance                )
    self   . set                    ( "priority"  , JSON [ "Priority"  ]     )
    ##########################################################################
    CRX    = self . UpdateMajorParameters ( DB , TABLE                       )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    self   . emitRefreshItem . emit ( item , CRX                             )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def UpdateByPriority              ( self , item , pid , priority         ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    JSON   = self . itemToJson      ( item                                   )
    ##########################################################################
    self   . set                    ( "id"        , pid                      )
    self   . set                    ( "locality"  , JSON [ "Locality"  ]     )
    self   . set                    ( "relevance" , JSON [ "Relevance" ]     )
    self   . set                    ( "priority"  , priority                 )
    ##########################################################################
    CRX    = self . UpdateMajorParameters ( DB , TABLE                       )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    self   . emitRefreshItem . emit ( item , CRX                             )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def UpdateByFlags                 ( self , item , pid , flags            ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    self   . set                    ( "id"    , pid                          )
    self   . set                    ( "flags" , flags                        )
    ##########################################################################
    DB     . LockWrites             ( [ TABLE ]                              )
    self   . UpdateFlagsById        ( DB , TABLE                             )
    DB     . UnlockTables           (                                        )
    ##########################################################################
    DB     . Close                  (                                        )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def RemoveItems                   ( self , Listings                      ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    QQ     = self . DeleteIDs       ( TABLE , Listings                       )
    DB     . LockWrites             ( [ TABLE ]                              )
    DB     . Query                  ( QQ                                     )
    DB     . UnlockTables           (                                        )
    ##########################################################################
    DB     . Close                  (                                        )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def AppendItem                    ( self                                 ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( self . NotOkay ( DB )                ) :
      return
    ##########################################################################
    TABLE  = self . Tables          [ "Names"                                ]
    ##########################################################################
    self . set                      ( "name"      , ""                       )
    self . set                      ( "locality"  , self . defaultLocality   )
    self . set                      ( "relevance" , self . defaultRelevance  )
    self . set                      ( "priority"  , 0                        )
    self . set                      ( "flags"     , 0                        )
    self . set                      ( "utf8"      , 0                        )
    self . set                      ( "length"    , 0                        )
    ##########################################################################
    DONE = False
    ##########################################################################
    self . Append                   ( DB , TABLE                             )
    IDX  = self . GetPosition       ( DB , TABLE                             )
    if                              ( IDX >= 0                             ) :
      self . Id = IDX
      if                            ( self . ObtainsById ( DB , TABLE )    ) :
        DONE = True
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    if                              ( DONE                                 ) :
      ########################################################################
      JSON = self . toList          (                                        )
      self . emitNewItem . emit     ( JSON                                   )
      self . Notify                 ( 5                                      )
      ########################################################################
    else                                                                     :
      self . Notify                 ( 2                                      )
    ##########################################################################
    return
  ############################################################################
  def PasteAppendingNames         ( self , NAMEs                           ) :
    ##########################################################################
    if                            ( self . get ( "uuid" ) <= 0             ) :
      return
    ##########################################################################
    DB       = self . ConnectDB   (                                          )
    if                            ( self . NotOkay ( DB )                  ) :
      return
    ##########################################################################
    LANG     = self . defaultLocality
    RELV     = self . defaultRelevance
    ##########################################################################
    for NAME in NAMEs                                                        :
      ########################################################################
      TABLE  = self . Tables      [ "Names"                                  ]
      ########################################################################
      self   . set                ( "name"      , NAME                       )
      self   . set                ( "locality"  , LANG                       )
      self   . set                ( "relevance" , RELV                       )
      self   . set                ( "priority"  , 0                          )
      self   . set                ( "flags"     , 0                          )
      self   . set                ( "utf8"      , 0                          )
      self   . set                ( "length"    , 0                          )
      ########################################################################
      self   . Append             ( DB , TABLE                               )
      IDX    = self . GetPosition ( DB , TABLE                               )
      ########################################################################
      if                          ( IDX >= 0                               ) :
        ######################################################################
        self . Id = IDX
    ##########################################################################
    DB       . Close              (                                          )
    ##########################################################################
    self     . loading            (                                          )
    ##########################################################################
    return
  ############################################################################
  def PasteItems                         ( self                            ) :
    ##########################################################################
    TEXT  = qApp . clipboard  ( ) . text (                                   )
    ##########################################################################
    if                                   ( len ( TEXT ) <= 0               ) :
      return
    ##########################################################################
    LINEz = TEXT . splitlines            (                                   )
    ##########################################################################
    if                                   ( len ( LINEz ) <= 0              ) :
      return
    ##########################################################################
    CNT   = 0
    LANG  = self . defaultLocality
    RELV  = self . defaultRelevance
    TOTAL = self . topLevelItemCount     (                                   )
    NAMEs =                              [                                   ]
    ##########################################################################
    while                                ( CNT < TOTAL                     ) :
      ########################################################################
      IT  = self . topLevelItem          ( CNT                               )
      JJ  = self . itemToJson            ( IT                                )
      ########################################################################
      NN  = JJ                           [ "Name"                            ]
      LL  = JJ                           [ "Locality"                        ]
      RR  = JJ                           [ "Relevance"                       ]
      PP  = JJ                           [ "Priority"                        ]
      ########################################################################
      if                                 ( ( LANG == LL )                and \
                                           ( RELV == RR )                  ) :
        ######################################################################
        if                               ( NN not in NAMEs                 ) :
          NAMEs . append                 ( NN                                )
      ########################################################################
      CNT = int                          ( CNT + 1                           )
    ##########################################################################
    LINEs =                              [                                   ]
    ##########################################################################
    for L in LINEz                                                           :
      ########################################################################
      if                                 ( len ( L ) <= 0                  ) :
        continue
      ########################################################################
      X   = L . replace                  ( "\t" , ""                         )
      X   = X . replace                  ( "\r" , ""                         )
      X   = X . replace                  ( "\n" , ""                         )
      X   = " " . join                   ( X . split (                     ) )
      ########################################################################
      if                                 ( X in LINEs                      ) :
        continue
      ########################################################################
      if                                 ( X in NAMEs                      ) :
        continue
      ########################################################################
      LINEs . append                     ( X                                 )
    ##########################################################################
    if                                   ( len ( LINEs ) <= 0              ) :
      return
    ##########################################################################
    VAL     =                            ( LINEs ,                           )
    self    . Go                         ( self . PasteAppendingNames , VAL  )
    ##########################################################################
    return
  ############################################################################
  def QuickAppending               ( self                                  ) :
    ##########################################################################
    NAME     = ""
    ##########################################################################
    if                             ( self . topLevelItemCount ( ) > 0      ) :
      ########################################################################
      IT     = self . topLevelItem ( 0                                       )
      NAME   = IT   . text         ( 1                                       )
    ##########################################################################
    if                             ( self . get ( "uuid" ) <= 0            ) :
      return
    ##########################################################################
    DB       = self . ConnectDB    (                                         )
    if                             ( self . NotOkay ( DB )                 ) :
      return
    ##########################################################################
    for LC in                      [ 1002 , 1003 , 1006                    ] :
      ########################################################################
      TABLE  = self . Tables       [ "Names"                                 ]
      ########################################################################
      self   . set                 ( "name"      , NAME                      )
      self   . set                 ( "locality"  , LC                        )
      self   . set                 ( "relevance" , self . defaultRelevance   )
      self   . set                 ( "priority"  , 0                         )
      self   . set                 ( "flags"     , 0                         )
      self   . set                 ( "utf8"      , 0                         )
      self   . set                 ( "length"    , 0                         )
      ########################################################################
      self   . Append              ( DB , TABLE                              )
      IDX    = self . GetPosition  ( DB , TABLE                              )
      ########################################################################
      if                           ( IDX >= 0                              ) :
        ######################################################################
        self . Id = IDX
    ##########################################################################
    DB       . Close               (                                          )
    ##########################################################################
    self     . loading            (                                          )
    ##########################################################################
    return
  ############################################################################
  def itemToJson                       ( self , item                       ) :
    ##########################################################################
    JSON                 =             {                                     }
    JSON [ "Id"        ] = item . text ( 0                                   )
    JSON [ "Name"      ] = item . text ( 1                                   )
    JSON [ "Locality"  ] = item . data ( 2 , Qt . UserRole                   )
    JSON [ "Relevance" ] = item . data ( 3 , Qt . UserRole                   )
    JSON [ "Priority"  ] = item . text ( 4                                   )
    ##########################################################################
    JSON [ "Id"        ] = int         ( JSON [ "Id"        ]                )
    JSON [ "Locality"  ] = int         ( JSON [ "Locality"  ]                )
    JSON [ "Relevance" ] = int         ( JSON [ "Relevance" ]                )
    JSON [ "Priority"  ] = int         ( JSON [ "Priority"  ]                )
    ##########################################################################
    return JSON
  ############################################################################
  def RefreshItem                ( self , item , JSON                      ) :
    ##########################################################################
    TRX  = self . Translations   [ "NamesEditor"                             ]
    ##########################################################################
    L    = JSON                  [ 2                                         ]
    R    = JSON                  [ 4                                         ]
    REL  = TRX                   [ "Relevance" ] [ str ( R )                 ]
    LANG = TRX                   [ "Languages" ] [ str ( L )                 ]
    ##########################################################################
    item . setText               ( 2 , str ( LANG      )                     )
    item . setData               ( 2 , Qt . UserRole , int ( JSON [ 2 ] )    )
    ##########################################################################
    item . setText               ( 3 , str ( REL       )                     )
    item . setData               ( 3 , Qt . UserRole , int ( JSON [ 4 ] )    )
    ##########################################################################
    item . setText               ( 4 , str ( JSON [  3 ] )                   )
    item . setTextAlignment      ( 4 , Qt.AlignRight                         )
    item . setData               ( 4 , Qt . UserRole , int ( JSON [ 3 ] )    )
    ##########################################################################
    return
  ############################################################################
  def jsonToItem                 ( self , JSON                             ) :
    ##########################################################################
    TRX  = self . Translations   [ "NamesEditor"                             ]
    item = QTreeWidgetItem       (                                           )
    ##########################################################################
    L    = JSON                  [ 2                                         ]
    R    = JSON                  [ 4                                         ]
    REL  = TRX                   [ "Relevance" ] [ str ( R )                 ]
    LANG = TRX                   [ "Languages" ] [ str ( L )                 ]
    S    = JSON                  [ 8                                         ]
    try                                                                      :
      S  = S . decode            ( "utf-8"                                   )
    except ( UnicodeDecodeError , AttributeError )                           :
      pass
    ##########################################################################
    item . setText               ( 0 , str ( JSON [  0 ] )                   )
    item . setTextAlignment      ( 4 , Qt.AlignRight                         )
    ##########################################################################
    item . setText               ( 1 , str ( S         )                     )
    ##########################################################################
    item . setText               ( 2 , str ( LANG      )                     )
    item . setData               ( 2 , Qt . UserRole , int ( JSON [ 2 ] )    )
    ##########################################################################
    item . setText               ( 3 , str ( REL       )                     )
    item . setData               ( 3 , Qt . UserRole , int ( JSON [ 4 ] )    )
    ##########################################################################
    item . setText               ( 4 , str ( JSON [  3 ] )                   )
    item . setTextAlignment      ( 4 , Qt.AlignRight                         )
    item . setData               ( 4 , Qt . UserRole , int ( JSON [ 3 ] )    )
    ##########################################################################
    item . setText               ( 5 , str ( JSON [  5 ] )                   )
    item . setTextAlignment      ( 5 , Qt.AlignRight                         )
    item . setData               ( 5 , Qt . UserRole , JSON [ 5 ]            )
    ##########################################################################
    item . setText               ( 6 , str ( JSON [  6 ] )                   )
    item . setTextAlignment      ( 6 , Qt.AlignRight                         )
    ##########################################################################
    item . setText               ( 7 , str ( JSON [  7 ] )                   )
    item . setTextAlignment      ( 7 , Qt.AlignRight                         )
    ##########################################################################
    item . setText               ( 8 , str ( JSON [  9 ] )                   )
    ##########################################################################
    item . setText               ( 9 , ""                                    )
    ##########################################################################
    return item
  ############################################################################
  def TranslateAll              ( self                                     ) :
    ##########################################################################
    DB    = self . ConnectDB    (                                            )
    if                          ( DB == None                               ) :
      return
    ##########################################################################
    TABLE = self . Tables       [ "Names"                                    ]
    FMT   = self . Translations [ "UI::Translating"                          ]
    UUID  = self . get          ( "uuid"                                     )
    self  . DoAutoTranslation   ( DB , TABLE , UUID , FMT , 15.0             )
    ##########################################################################
    DB    . Close               (                                            )
    ##########################################################################
    return
  ############################################################################
  def refresh                         ( self , All                         ) :
    ##########################################################################
    self    . clear                   (                                      )
    TRX     = self . Translations     [ "NamesEditor"                        ]
    ##########################################################################
    for IT in All                                                            :
      ########################################################################
      NT    = self . jsonToItem       ( IT                                   )
      self  . addTopLevelItem         ( NT                                   )
    ##########################################################################
    self    . emitNamesShow . emit    (                                      )
    ##########################################################################
    if                                ( self . ShowCompact                 ) :
      ########################################################################
      TOTAL = len                     ( self . KEYs                          )
      self  . resizeColumnsToContents ( range ( 0 , TOTAL - 1 )              )
      self  . setColumnWidth          ( 2 , 160                              )
      self  . setColumnWidth          ( 4 , 120                              )
      self  . CloseCompact            (                                      )
    ##########################################################################
    return
  ############################################################################
  def loading                       ( self                                 ) :
    ##########################################################################
    if                              ( self . get ( "uuid" ) <= 0           ) :
      self . emitNamesShow . emit   (                                        )
      return
    ##########################################################################
    DB     = self . ConnectDB       (                                        )
    if                              ( DB == None                           ) :
      self . emitNamesShow . emit   (                                        )
      return
    ##########################################################################
    ALL    = self . FetchEverything ( DB , self . Tables [ "Names" ]         )
    ##########################################################################
    DB     . Close                  (                                        )
    ##########################################################################
    if                              ( len ( ALL ) <= 0                     ) :
      self . emitNamesShow . emit   (                                        )
    ##########################################################################
    self   . emitAllNames  . emit   ( ALL                                    )
    self   . Notify                 ( 5                                      )
    ##########################################################################
    return
  ############################################################################
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
##############################################################################
