# -*- coding: utf-8 -*-
##############################################################################
## MdiArea
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
from   random                         import randint
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
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QActionGroup
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QMdiArea
##############################################################################
from         . VirtualGui             import VirtualGui   as VirtualGui
from         . MenuManager            import MenuManager  as MenuManager
from         . MdiSubWindow           import MdiSubWindow as MdiSubWindow
##############################################################################
class MdiArea         ( QMdiArea , VirtualGui                              ) :
  ############################################################################
  HavingMenu = 1371434312
  ############################################################################
  SubmitStatusMessage  = pyqtSignal ( str , int                              )
  Files                = pyqtSignal ( list                                   )
  childChanged         = pyqtSignal (                                        )
  ############################################################################
  def __init__        ( self , parent = None , plan = None                 ) :
    ##########################################################################
    super ( QMdiArea  , self ) . __init__ ( parent                           )
    super ( VirtualGui, self ) . __init__ (                                  )
    self . Initialize                     ( self                             )
    self . setPlanFunction                ( plan                             )
    self . setAttribute                   ( Qt . WA_InputMethodEnabled       )
    ##########################################################################
    self . setViewMode                    ( self . SubWindowView             )
    self . setHorizontalScrollBarPolicy   ( Qt . ScrollBarAlwaysOff          )
    self . setVerticalScrollBarPolicy     ( Qt . ScrollBarAlwaysOff          )
    self . setAcceptDrops                 ( True                             )
    ##########################################################################
    self . SubmitStatusMessage . connect  ( self . AssignStatusMessage       )
    ##########################################################################
    self . setFunction                    ( self . HavingMenu , True         )
    ##########################################################################
    self . droppingAction = False
    ##########################################################################
    self . menu           = None
    self . group          = None
    ##########################################################################
    self . styleMenu      = None
    self . subWindow      = None
    self . tabbedAction   = None
    self . cascadeAction  = None
    self . tiledAction    = None
    self . closeAll       = None
    ##########################################################################
    """
    WidgetClass                   ;
    addIntoWidget ( parent,this ) ;
    Shadow = new QGraphicsDropShadowEffect ( this )                     ;
    setGraphicsEffect ( Shadow )                                        ;
    Shadow -> setBlurRadius ( 3                     )                   ;
    Shadow -> setColor      ( QColor  (224,224,224) )                   ;
    Shadow -> setOffset     ( QPointF (  3,  3    ) )                   ;
    Shadow -> setEnabled    ( true                  )                   ;
    if ( NotNull ( plan ) )                                             {
      Data . Controller = & ( plan->canContinue )                       ;
    }                                                                   ;
    """
    ##########################################################################
    return
  ############################################################################
  def focusInEvent               ( self , event                            ) :
    ##########################################################################
    if                           ( self . focusIn ( event )                ) :
      return
    ##########################################################################
    super ( ) . focusInEvent     (        event                              )
    ##########################################################################
    return
  ############################################################################
  def focusOutEvent              ( self , event                            ) :
    ##########################################################################
    if                           ( self . focusOut ( event )               ) :
      return
    ##########################################################################
    super ( ) . focusOutEvent    (        event                              )
    ##########################################################################
    return
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    ##########################################################################
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . contextMenuEvent (        event                              )
    ##########################################################################
    return
  ############################################################################
  def closeEvent                 ( self , event                            ) :
    ##########################################################################
    if                           ( self . Shutdown ( )                     ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . closeEvent       (        event                              )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent                ( self , event                            ) :
    ##########################################################################
    if                           ( self . Relocation ( )                   ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . resizeEvent      (        event                              )
    ##########################################################################
    return
  ############################################################################
  def showEvent                  ( self , event                            ) :
    ##########################################################################
    super ( ) . showEvent        (        event                              )
    self . Relocation            (                                           )
    ##########################################################################
    return
  ############################################################################
  def dragEnterEvent    ( self , event                                     ) :
    ##########################################################################
    if                  ( self . allowDrop ( self . dragDropMode ( ) )     ) :
      if                ( self . dragEnter ( event )                       ) :
        event . acceptProposedAction (                                       )
        return
    ##########################################################################
    if                  ( self . PassDragDrop                              ) :
      super ( ) . dragEnterEvent ( event                                     )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def dragLeaveEvent    ( self , event                                     ) :
    ##########################################################################
    if                  ( self . removeDrop ( )                            ) :
      event . accept    (                                                    )
      return
    ##########################################################################
    if                  ( self . PassDragDrop                              ) :
      super ( ) . dragLeaveEvent ( event                                     )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def dragMoveEvent     ( self , event                                     ) :
    ##########################################################################
    if                  ( self . allowDrop ( self . dragDropMode ( ) )     ) :
      if                ( self . dragMove  ( event )                       ) :
        event . acceptProposedAction (                                       )
        return
    ##########################################################################
    if                  ( self . PassDragDrop                              ) :
      super ( ) . dragMoveEvent ( event                                      )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def dropEvent         ( self , event                                     ) :
    ##########################################################################
    if                  ( self . allowDrop ( self . dragDropMode ( ) )     ) :
      if                ( self . dropIn    ( event )                       ) :
        event . acceptProposedAction (                                       )
        return
    ##########################################################################
    if                  ( self . PassDragDrop                              ) :
      super ( ) . dropEvent ( event                                          )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def dragDone               ( self , dropIt , mime                        ) :
    return
  ############################################################################
  def dropNew                ( self , sourceWidget , mimeData , mousePos   ) :
    return True
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return True
  ############################################################################
  def dropAppend             ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    if                       ( self . droppingAction                       ) :
      return False
    ##########################################################################
    return self . dropItems  (        sourceWidget , mimeData , mousePos     )
  ############################################################################
  def removeDrop             ( self                                        ) :
    return True
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    formats = "url/uuids"
    return self . MimeType    ( mime , formats                               )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def acceptUrlsDrop          ( self                                       ) :
    return True
  ############################################################################
  def dropUrls                ( self , sourceWidget , pos , Urls           ) :
    ##########################################################################
    print (Urls)
    ## self . Files . emit ( URLs )
    ##########################################################################
    return True
  ############################################################################
  def contains                   ( self , accessibleName                   ) :
    ##########################################################################
    subws = self . subWindowList (                                           )
    for subw in subws                                                        :
      if ( subw . widget ( ) . accessibleName ( ) == accessibleName )        :
        return True
    ##########################################################################
    return False
  ############################################################################
  def findWidget                 ( self , accessibleName                   ) :
    ##########################################################################
    subws = self . subWindowList (                                           )
    for subw in subws                                                        :
      if ( subw . widget ( ) . accessibleName ( ) == accessibleName )        :
        return subw . widget     (                                           )
    ##########################################################################
    return None
  ############################################################################
  def getWidgets                 ( self , accessibleName                   ) :
    ##########################################################################
    subws = self . subWindowList (                                           )
    wgts  =                      [                                           ]
    for subw in subws                                                        :
      if ( subw . widget ( ) . accessibleName ( ) == accessibleName )        :
        wgts . append            ( subw . widget ( )                         )
    ##########################################################################
    return wgts
  ############################################################################
  @pyqtSlot                    (       QWidget                               )
  def Leave                    ( self , widget                             ) :
    ##########################################################################
    self . childChanged . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (       QWidget , QSize                     )
  def Adjustment                 ( self , msw ,  size                      ) :
    ##########################################################################
    ws     = size
    mw     = self . geometry     (                                           )
    wm     = QSize               ( mw . width ( ) , mw . height ( )          )
    fg     = msw . frameGeometry (                                           )
    wg     = msw . geometry      (                                           )
    ms     = QSize               ( fg . width ( ) , fg . height ( )          )
    ds     = QSize               ( wg . width ( ) , wg . height ( )          )
    ##########################################################################
    ms     = ms - ds
    ms     = ms + ws
    wm     = wm - ms
    ##########################################################################
    WW     = ( wm . width  ( ) * ( randint ( 0 , 200 ) % 16 ) / 16           )
    HH     = ( wm . height ( ) * ( randint ( 0 , 200 ) % 16 ) / 16           )
    ds     = QSize               ( WW , HH                                   )
    ##########################################################################
    if                           ( ds . width  ( ) < 0                     ) :
      ds   . setWidth            ( 0                                         )
    if                           ( ds . height ( ) < 0                     ) :
      ds   . setHeight           ( 0                                         )
    ##########################################################################
    msw    . move                ( ds . width ( ) , ds . height ( )          )
    msw    . resize              ( ms                                        )
    self   . update              (                                           )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                      (       QWidget                             )
  def Fit                        ( self , widget                           ) :
    ##########################################################################
    ws     = widget . size       (                                           )
    msw    = self   . append     ( widget                                    )
    ##########################################################################
    ## msw->setFont(plan->fonts[N::Fonts::Default])                          ;
    ##########################################################################
    mw     = self . geometry     (                                           )
    wm     = QSize               ( mw . width ( ) , mw . height ( )          )
    fg     = msw . frameGeometry (                                           )
    wg     = msw . geometry      (                                           )
    ms     = QSize               ( fg . width ( ) , fg . height ( )          )
    ds     = QSize               ( wg . width ( ) , wg . height ( )          )
    ##########################################################################
    ms     = ms - ds
    ms     = ms + ws
    wm     = wm - ms
    ##########################################################################
    WW     = ( wm . width  ( ) * ( randint ( 0 , 200 ) % 16 ) / 16           )
    HH     = ( wm . height ( ) * ( randint ( 0 , 200 ) % 16 ) / 16           )
    ds     = QSize               ( WW , HH                                   )
    ##########################################################################
    if                           ( ds . width  ( ) < 0                     ) :
      ds   . setWidth            ( 0                                         )
    if                           ( ds . height ( ) < 0                     ) :
      ds   . setHeight           ( 0                                         )
    ##########################################################################
    msw    . move                ( ds . width ( ) , ds . height ( )          )
    msw    . resize              ( ms                                        )
    msw    . setWindowIcon       ( widget . windowIcon ( )                   )
    self   . update              (                                           )
    ##########################################################################
    return
  ############################################################################
  def Connect                 ( self , widget                              ) :
    ##########################################################################
    Caller   = getattr        ( widget , "Adjustment" , None                 )
    if                        ( callable ( Caller )                        ) :
      Caller . connect        ( self . Adjustment                            )
    ##########################################################################
    Caller   = getattr        ( widget , "Leave"      , None                 )
    if                        ( callable ( Caller )                        ) :
      Caller . connect        ( self . Leave                                 )
    ##########################################################################
    return
  ############################################################################
  def Shutdown                ( self                                       ) :
    return True
  ############################################################################
  def Relocation              ( self                                       ) :
    return False
  ############################################################################
  def FocusIn                 ( self                                       ) :
    ##########################################################################
    self . LinkVoice          ( None                                         )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                ( self                                       ) :
    return True
  ############################################################################
  @pyqtSlot                   (        str     , int                         )
  def AssignStatusMessage     ( self , message , timeout = 0               ) :
    self . statusMessage      (        message , timeout                     )
    return
  ############################################################################
  def ShowStatus                      ( self , message , timeout = 0       ) :
    self . SubmitStatusMessage . emit (        message , timeout             )
    return
  ############################################################################
  @pyqtSlot                           (                                      )
  def FileAboutToShow                 ( self                               ) :
    ##########################################################################
    swlists    = self . subWindowList (                                      )
    ne         =                      ( len ( swlists ) > 0                  )
    ##########################################################################
    self . closeAll . setEnabled      ( ne                                   )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                             (                                    )
  def StyleAboutToShow                  ( self                             ) :
    ##########################################################################
    p          = self . GetPlan         (                                    )
    if                                  ( p == None                        ) :
      return
    ##########################################################################
    atMdi      = False
    stacked    = p    . getStacked      (                                    )
    if                                  ( stacked != None                  ) :
      CI       = stacked . currentIndex (                                    )
      WW       = stacked . widget       ( CI                                 )
      if                                ( WW == self                       ) :
        atMdi  = True
    ##########################################################################
    swlists    = self . subWindowList   (                                    )
    ne         =                        ( len ( swlists ) > 0                )
    ##########################################################################
    sSub       = False
    sTab       = False
    ##########################################################################
    if                                  ( atMdi                            ) :
      vm       = self . viewMode        (                                    )
      isSub    =                        ( vm == self . SubWindowView         )
      ########################################################################
      if                                ( isSub                            ) :
        sTab   = True
      else                                                                   :
        sSub   = True
        ne     = False
    ##########################################################################
    self . subWindow     . setEnabled   ( sSub                               )
    self . tabbedAction  . setEnabled   ( sTab                               )
    self . cascadeAction . setEnabled   ( ne                                 )
    self . tiledAction   . setEnabled   ( ne                                 )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem               ( self                                     , \
                                  menu                                     , \
                                  fileMenu                                 , \
                                  subwin                                   , \
                                  tabbed                                   , \
                                  cascade                                  , \
                                  tile                                     , \
                                  closeAll                                 ) :
    ##########################################################################
    self . styleMenu     = menu
    self . subWindow     = subwin
    self . tabbedAction  = tabbed
    self . cascadeAction = cascade
    self . tiledAction   = tile
    self . closeAll      = closeAll
    ##########################################################################
    self . styleMenu  . aboutToShow . connect ( self . StyleAboutToShow      )
    fileMenu          . aboutToShow . connect ( self . FileAboutToShow       )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     (                                            )
  def MenuAboutToShow           ( self                                     ) :
    ##########################################################################
    self . AttachMenu           ( self . menu , self . group                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot                     ( QAction                                    )
  def WindowActionWidget        ( self , action                            ) :
    ##########################################################################
    w    = action . data        (                                            )
    ##########################################################################
    if                          ( w == None                                ) :
      return
    ##########################################################################
    self . setActiveSubWindow   ( w                                          )
    ##########################################################################
    s    = w . widget           (                                            )
    msg  = s . windowTitle      (                                            )
    self . Go                   ( self . Talk                              , \
                                  ( msg , self . getLocality ( ) , )         )
    ##########################################################################
    return
  ############################################################################
  def PrepareMenu               ( self , menu                              ) :
    ##########################################################################
    self . menu  = menu
    self . group = QActionGroup ( menu                                       )
    ##########################################################################
    self . menu  . aboutToShow . connect ( self . MenuAboutToShow            )
    self . group . triggered   . connect ( self . WindowActionWidget         )
    ##########################################################################
    self . AttachMenu           ( self . menu , self . group                 )
    ##########################################################################
    return
  ############################################################################
  def AttachMenu                     ( self , menu , group                 ) :
    ##########################################################################
    menu    . clear                  (                                       )
    ##########################################################################
    asw     = self . activeSubWindow (                                       )
    swlists = self . subWindowList   (                                       )
    ##########################################################################
    for w in swlists                                                         :
      ########################################################################
      s     = w    . widget       (                                          )
      a     = menu . addAction    ( s . windowTitle  ( )                     )
      a     . setData             ( w                                        )
      a     . setCheckable        ( True                                     )
      ########################################################################
      if                          ( w == asw                               ) :
        a   . setChecked          ( True                                     )
      ########################################################################
      group . addAction           ( a                                        )
    ##########################################################################
    return
  ############################################################################
  def Subwindow               ( self                                       ) :
    ##########################################################################
    self . setViewMode        ( self . SubWindowView                         )
    ## MenuStatus  (             )
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def Tabbed                  ( self                                       ) :
    ##########################################################################
    self . setViewMode        ( self . TabbedView                            )
    ## MenuStatus  (          ) ;
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def Tile                    ( self                                       ) :
    ##########################################################################
    self . tileSubWindows     (                                              )
    ## MenuStatus     ( ) ;
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def Cascade                 ( self                                       ) :
    ##########################################################################
    self . cascadeSubWindows  (                                              )
    ## MenuStatus         ( ) ;
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def CloseAll                ( self                                       ) :
    ##########################################################################
    self . closeAllSubWindows (                                              )
    ## MenuStatus         ( ) ;
    self . update             (                                              )
    ##########################################################################
    return
  ############################################################################
  def append             ( self , widget                                   ) :
    ##########################################################################
    msw  = MdiSubWindow  (                                                   )
    msw  . setWidget     ( widget                                            )
    msw  . setAttribute  ( Qt . WA_DeleteOnClose                             )
    msw  . setAttribute  ( Qt . WA_InputMethodEnabled                        )
    self . addSubWindow  ( msw                                               )
    ##########################################################################
    return msw
  ############################################################################
  def Attach                   ( self , widget , direction                 ) :
    ##########################################################################
    msw    = self . append     ( widget                                      )
    ## msw->setFont(plan->fonts[N::Fonts::Default])
    ##########################################################################
    mw     = self   . geometry (                                             )
    sh     = widget . sizeHint (                                             )
    gw     = QSize             (                                             )
    sp     = QPoint            (                                             )
    ##########################################################################
    if                         ( direction == 0                            ) :
      ########################################################################
      gw   = widget . size     (                                             )
      sp   . setX ( ( ( mw . width ()-gw.width ())/16) * (randint(0,200)%16) )
      sp   . setY ( ( ( mw . height()-gw.height())/16) * (randint(0,200)%16) )
      ########################################################################
      if                       ( gw . width ( ) < sh . width ( )           ) :
        gw . setWidth          ( sh . width ( )                              )
      ########################################################################
      if                       ( gw . height ( ) < sh . height ( ) ) :
        gw . setHeight         ( sh . height ( ) )
      ########################################################################
    elif                       ( direction == Qt . Vertical ) :
      ########################################################################
      sp   . setX ( ( mw . width ( ) / 16 ) * ( randint ( 0 , 200 ) % 10 )   )
      sp   . setY              ( 0                                           )
      gw   . setWidth          ( mw . width  ( ) / 5                         )
      gw   . setHeight         ( mw . height ( )                             )
      ########################################################################
      if                       ( gw . width ( ) < sh . width ( )           ) :
        gw . setWidth          ( sh . width ( )                              )
      ########################################################################
    elif                       ( direction == Qt . Horizontal              ) :
      ########################################################################
      sp   . setX              ( 0                                           )
      sp   . setY ( ( mw . height ( ) / 16 ) * ( randint ( 0 , 200 ) % 8 )   )
      gw   . setWidth          ( mw . width  ( )                             )
      gw   . setHeight         ( mw . height ( ) / 3                         )
      ########################################################################
      if                       ( gw . height ( ) < sh . height ( )         ) :
        gw . setHeight         ( sh . height ( )                             )
    ##########################################################################
    msw    . move              ( sp                                          )
    msw    . resize            ( gw                                          )
    msw    . setWindowIcon     ( widget . windowIcon ( )                     )
    ## MenuStatus   ( )
    self   . update            (                                             )
    ##########################################################################
    return
  ############################################################################
  def ScrollBarMenu                ( self , mm                             ) :
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    LOM    = mm   . addMenu        ( TRX [ "UI::ScrollBar" ]                 )
    ##########################################################################
    status = self . horizontalScrollBarPolicy (                              )
    hid    =                       ( status == Qt . ScrollBarAsNeeded        )
    msg    = TRX                   [ "UI::Horizontal"                        ]
    mm     . addActionFromMenu     ( LOM , 60001 , msg , True , hid          )
    ##########################################################################
    status = self . verticalScrollBarPolicy   (                              )
    hid    =                       ( status == Qt . ScrollBarAsNeeded        )
    msg    = TRX                   [ "UI::Vertical"                          ]
    mm     . addActionFromMenu     ( LOM , 60002 , msg , True , hid          )
    ##########################################################################
    return mm
  ############################################################################
  def RunScrollBar                          ( self , menu , aa             ) :
    ##########################################################################
    at     = menu . at                      ( aa                             )
    ##########################################################################
    if                                      ( at == 60001                  ) :
      ########################################################################
      if                                    ( aa . isChecked ( )           ) :
        self . setHorizontalScrollBarPolicy ( Qt . ScrollBarAsNeeded         )
      else                                                                   :
        self . setHorizontalScrollBarPolicy ( Qt . ScrollBarAlwaysOff        )
      ########################################################################
      return True
    ##########################################################################
    elif                                    ( at == 60002                  ) :
      ########################################################################
      if                                    ( aa . isChecked ( )           ) :
        self . setVerticalScrollBarPolicy   ( Qt . ScrollBarAsNeeded         )
      else                                                                   :
        self . setVerticalScrollBarPolicy   ( Qt . ScrollBarAlwaysOff        )
      ########################################################################
      return True
    ##########################################################################
    return False
  ############################################################################
  def Menu                         ( self , pos                            ) :
    ##########################################################################
    doMenu = self . isFunction     ( self . HavingMenu                       )
    if                             ( not doMenu                            ) :
      return False
    ##########################################################################
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    TRX    = self . Translations
    ##########################################################################
    vp     = self . viewport       (                                         )
    W      = vp   . width          (                                         )
    H      = vp   . height         (                                         )
    MSG    = f"{W} x {H}"
    mm     . addAction             ( 9900124101 , MSG                        )
    mm     . addSeparator          (                                         )
    ##########################################################################
    mm     = self . ScrollBarMenu  ( mm                                      )
    ##########################################################################
    mm     . setFont               ( self    . font ( )                      )
    aa     = mm . exec_            ( QCursor . pos  ( )                      )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( self . RunScrollBar ( mm , aa )       ) :
      return True
    ##########################################################################
    return True
##############################################################################
