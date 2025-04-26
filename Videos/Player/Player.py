# -*- coding: utf-8 -*-
##############################################################################
## Player
## 影片播放
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
import vlc
import math
import cv2
import dlib
##############################################################################
import pathlib
from   pathlib                                  import Path
##############################################################################
import AITK
##############################################################################
from   AITK    . Calendars . StarDate           import StarDate     as StarDate
from   AITK    . Documents . JSON               import Load         as LoadJson
from   AITK    . Documents . JSON               import Save         as SaveJson
##############################################################################
from   PySide6                                  import QtCore
from   PySide6                                  import QtGui
from   PySide6                                  import QtWidgets
from   PySide6 . QtCore                         import *
from   PySide6 . QtGui                          import *
from   PySide6 . QtWidgets                      import *
from   AITK    . Qt6                            import *
##############################################################################
from   AITK    . Qt6 . MenuManager              import MenuManager  as MenuManager
from   AITK    . Qt6 . AttachDock               import AttachDock   as AttachDock
from   AITK    . Qt6 . Widget                   import Widget       as Widget
from   AITK    . Qt6 . GraphicsView             import GraphicsView as GraphicsView
##############################################################################
from   AITK    . AI  . Pictures . Vision        import Vision       as AiVision
##############################################################################
from   AITK    . Pictures . Picture             import Picture      as PictureItem
from   AITK    . People   . Faces . Face        import Face         as FaceItem
from   AITK    . People   . Body  . Tit         import Tit          as TitItem
from   AITK    . People   . Body  . Body        import Body         as BodyItem
##############################################################################
from   AITK    . Videos   . Synopsis . Scenario import Scenario     as ScenarioItem
from                      . Panel               import Panel        as Panel
##############################################################################
class vlcPlayInternalLayer       ( QWidget                                 ) :
  ############################################################################
  def __init__                   ( self , parent = None                    ) :
    ##########################################################################
    super ( ) . __init__         ( parent , Qt.FramelessWindowHint           )
    self . setMouseTracking      ( True                                      )
    self . MoveCallback  = None
    self . WheelCallback = None
    ##########################################################################
    PAL  = self   . palette      (                                           )
    PAL  . setColor              ( QPalette . Window , Qt . black            )
    self . setAutoFillBackground ( True                                      )
    self . setPalette            ( PAL                                       )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent           ( self , e                                  ) :
    ##########################################################################
    super ( ) . mouseMoveEvent (        e                                    )
    self      . MoveCallback   (        e                                    )
    ##########################################################################
    return
  ############################################################################
  def wheelEvent              ( self , e                                   ) :
    ##########################################################################
    super ( ) . wheelEvent    (        e                                     )
    self      . WheelCallback (        e                                     )
    ##########################################################################
    return
##############################################################################
class vlcPlayEditor            ( QWidget                                   ) :
  ############################################################################
  DoReflush = Signal           (                                             )
  ############################################################################
  def __init__                 ( self , parent = None                      ) :
    ##########################################################################
    super ( ) . __init__       ( parent , Qt.FramelessWindowHint             )
    self . setMouseTracking    ( True                                        )
    self . MoveCallback  = None
    self . WheelCallback = None
    self . IMAGE         = None
    ##########################################################################
    self . DoReflush . connect ( self . update                               )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent           ( self , e                                  ) :
    ##########################################################################
    super ( ) . mouseMoveEvent (        e                                    )
    self      . MoveCallback   (        e                                    )
    ##########################################################################
    return
  ############################################################################
  def wheelEvent              ( self , e                                   ) :
    ##########################################################################
    super ( ) . wheelEvent    (        e                                     )
    self      . WheelCallback (        e                                     )
    ##########################################################################
    return
  ############################################################################
  def paintEvent                   ( self , e                              ) :
    ##########################################################################
    WW     = self . width          (                                         )
    HH     = self . height         (                                         )
    p      = QPainter              (                                         )
    ##########################################################################
    p      . begin                 ( self                                    )
    p      . fillRect              ( 0,  0 , WW , HH , Qt . black            )
    ##########################################################################
    if                             ( self . IMAGE not in [ False , None  ] ) :
      ########################################################################
      IW   = self . IMAGE . width  (                                         )
      IH   = self . IMAGE . height (                                         )
      ########################################################################
      RT   = float                 ( float ( IH ) / float ( IW )             )
      PW   = int                   ( WW                                      )
      PH   = int                   ( RT           * float ( WW )             )
      ########################################################################
      if                           ( PH > HH                               ) :
        ######################################################################
        RT = float                 ( float ( IW ) / float ( IH )             )
        PH = int                   ( HH                                      )
        PW = int                   ( RT           * float ( HH )             )
        ######################################################################
        X  = int                   ( ( WW - PW ) / 2                         )
        Y  = 0
        ######################################################################
      else                                                                   :
        ######################################################################
        X  = 0
        Y  = int                   ( ( HH - PH ) / 2                         )
      ########################################################################
      DSR  = QRectF                ( X , Y , PW , PH                         )
      ISR  = QRectF                ( 0 , 0 , IW , IH                         )
      p    . drawImage             ( DSR , self . IMAGE , ISR                )
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    p      . end                   (                                         )
    ##########################################################################
    return
  ############################################################################
  def AssignImage           ( self , IMG                                   ) :
    ##########################################################################
    self . IMAGE = IMG
    ##########################################################################
    self . DoReflush . emit (                                                )
    ##########################################################################
    return
##############################################################################
class Player               ( Widget , AttachDock                           ) :
  ############################################################################
  HavingMenu      = 1371434312
  ############################################################################
  Leave           = Signal ( QWidget                                         )
  attachNone      = Signal ( QWidget                                         )
  attachDock      = Signal ( QWidget , str , int , int                       )
  attachMdi       = Signal ( QWidget , int                                   )
  Clicked         = Signal ( int                                             )
  PlayerCompleted = Signal ( int                                             )
  FilmViewed      = Signal ( dict                                            )
  FilmStopped     = Signal ( dict                                            )
  TogglePlaylist  = Signal ( bool                                            )
  NormalWindow    = Signal (                                                 )
  PlayFull        = Signal (                                                 )
  GoMdi           = Signal ( int                                             )
  GoStack         = Signal ( int                                             )
  ClosePlayer     = Signal ( int                                             )
  NextAnalysis    = Signal (                                                 )
  AssignMajor     = Signal ( QWidget                                         )
  ############################################################################
  def __init__             ( self , parent = None , plan = None            ) :
    ##########################################################################
    super (                   ) . __init__ ( parent , plan                   )
    super ( AttachDock , self ) . __init__ (                                 )
    self . InitializeDock                  (          plan                   )
    self . Configure                       (                                 )
    ##########################################################################
    return
  ############################################################################
  def Configure ( self                                                     ) :
    ##########################################################################
    self . setMouseTracking ( True                                           )
    self . setFocusPolicy   ( Qt . WheelFocus                                )
    ##########################################################################
    ## self . Scene      = QGraphicsScene (                                     )
    ## self . setScene         ( self . Scene                                   )
    ##########################################################################
    self . isContinue = None
    self . CallLogger = None
    self . PID        = -1
    self . Delta      = 3000
    self . Method     = 0
    self . DockAt     = 0
    self . isPlayList = True
    self . Receivers  = [                                                    ]
    self . INSTANCE   = vlc . Instance (                                     )
    self . MEDIA      = None
    self . PLAYER     = self . INSTANCE . media_player_new (                 )
    self . SCENE      = ScenarioItem (                                       )
    ##########################################################################
    self . LAYER      = vlcPlayInternalLayer ( self                          )
    self . LAYER      . MoveCallback  = self . MoveCallback
    self . LAYER      . WheelCallback = self . WheelCallback
    ##########################################################################
    self . EDITOR     = vlcPlayEditor        ( self                          )
    self . EDITOR     . MoveCallback  = self . MoveCallback
    self . EDITOR     . WheelCallback = self . WheelCallback
    self . EDITOR     . hide     (                                           )
    ##########################################################################
    self . AIV        = AiVision (                                           )
    self . BDI        = None
    ##########################################################################
    self . ToolHeight  = 80
    self . Duration    = -1
    self . Range       = 1000
    self . Step        = 250
    self . VWidth      = 640
    self . VHeight     = 480
    self . FineRange   = 3000
    self . ShowPanel   = False
    self . isPause     = False
    self . isAnalyzing = False
    self . isFullScreen = False
    self . FilmJSON    = None
    self . InfoJSON    =      {                                              }
    self . ATS         =      [                                              ]
    self . ATJ         =      [                                              ]
    self . BarMutex    = threading . Lock (                                  )
    self . Viewed      =      { "Exists"   : False                         , \
                                "Duration" : 0                             , \
                                "At"       : -1                            , \
                                "Bars"     : [                             ] }
    self . FvRange     =      { "Start"    : 0                             , \
                                "Finish"   : 0                               }
    ##########################################################################
    self . setFunction        ( self . HavingMenu , True                     )
    ##########################################################################
    self . PANEL      = Panel ( self , self . PlanFunc                       )
    self . PANEL      . hide  (                                              )
    ##########################################################################
    self . PANEL . Play      . clicked . connect ( self . DoPlay             )
    self . PANEL . Stop      . clicked . connect ( self . DoStop             )
    self . PANEL . Pause     . clicked . connect ( self . DoPause            )
    self . PANEL . BWin      . clicked . connect ( self . BackToNormal       )
    self . PANEL . SWin      . clicked . connect ( self . DockStack          )
    self . PANEL . MWin      . clicked . connect ( self . DockMdi            )
    self . PANEL . PrevFrame . clicked . connect ( self . DoPreviousFrame    )
    self . PANEL . NextFrame . clicked . connect ( self . DoNextFrame        )
    self . PANEL . Analysis  . clicked . connect ( self . RunAnalysis        )
    self . PANEL . Drawing   . toggled . connect ( self . SwitchEditor       )
    ##########################################################################
    self . PANEL . Clock     . sliderMoved   . connect ( self . setPosition  )
    self . PANEL . Clock     . sliderPressed . connect ( self . setPosition  )
    ##########################################################################
    self . PANEL . FineTune  . sliderMoved    . connect ( self . setFineTune )
    self . PANEL . FineTune  . sliderPressed  . connect ( self . setFineTune )
    self . PANEL . FineTune  . sliderReleased . connect ( self . releaseFineTune )
    ##########################################################################
    AVL  = self  . PLAYER . audio_get_volume (                               )
    self . PANEL . Volume . setValue         ( AVL                           )
    self . PANEL . Volume . valueChanged  . connect ( self . setVolume       )
    self . PANEL . Volume . setToolTip       ( f"{AVL}%"                     )
    ##########################################################################
    self . CLOCK      = QTimer ( self                                        )
    self . CLOCK      . setInterval ( 25                                     )
    self . CLOCK      . timeout . connect ( self . UpdateINFO                )
    ##########################################################################
    self . AUDIO      = QTimer ( self                                        )
    self . AUDIO      . setInterval ( 1000                                   )
    self . AUDIO      . timeout . connect ( self . UpdateAudio               )
    ##########################################################################
    self . setWindowIcon      ( QIcon ( ":/images/videogroup.png"          ) )
    ##########################################################################
    self . NextAnalysis . connect ( self . DoAnalysis                        )
    self . FilmViewed   . connect ( self . PANEL . Bar . AcceptFilm          )
    ##########################################################################
    self . VMenu        = QMenu   (                                          )
    ##########################################################################
    ## self . setHorizontalScrollBarPolicy ( Qt . ScrollBarAlwaysOff            )
    ## self . setVerticalScrollBarPolicy   ( Qt . ScrollBarAlwaysOff            )
    ##########################################################################
    return
  ############################################################################
  def UpdatePanel                    ( self                                ) :
    ##########################################################################
    self . PANEL . Settings     = self . Settings
    self . PANEL . Translations = self . Translations
    self . PANEL . UpdatePanel       (                                       )
    ##########################################################################
    MSG  = self . Translations       [ "Player" ] [ "ChangeStep"             ]
    CSA  = self . VMenu . addAction  ( MSG                                   )
    CSA  . triggered . connect       ( self . ChangeStep                     )
    ##########################################################################
    self . PANEL . VMenu . setMenu   ( self . VMenu                          )
    self . VMenu . setFont           ( self . font (                       ) )
    ##########################################################################
    CONF = self  . Settings          [ "Classifier" ] [ "File"               ]
    MAXI = self  . Settings          [ "Classifier" ] [ "Max"                ]
    self . AIV   . setClassifierPath ( CONF , MAXI                           )
    ##########################################################################
    CONF = self  . Settings          [ "Objectron"  ] [ "File"               ]
    MAXI = self  . Settings          [ "Objectron"  ] [ "Max"                ]
    THRS = self  . Settings          [ "Objectron"  ] [ "Threshold"          ]
    self . AIV   . setObjectronPath  ( CONF , MAXI , THRS                    )
    ##########################################################################
    CONF = self  . Settings          [ "Stylizers"  ] [ "Sketch"             ]
    self . AIV   . setStylizerPath   ( CONF                                  )
    ##########################################################################
    self . BDI   = BodyItem          (                                       )
    self . BOOB  = TitItem           (                                       )
    ##########################################################################
    AI           = self . Settings   [ "AiData"                              ]
    DIR          = self . Settings   [ "Data"                                ]
    ##########################################################################
    SVM          = AI                [ "Boobs-SVM"                           ]
    SVM          = f"{DIR}/{SVM}"
    ##########################################################################
    CASCADE      = AI                [ "Boobs-Cascade"                       ]
    CASCADE      = f"{DIR}/{CASCADE}"
    ##########################################################################
    self . BOOB  . LoadClassifier    ( CASCADE                               )
    self . BOOB  . LoadDetector      ( SVM                                   )
    ##########################################################################
    HAAR         = AI                [ "HAAR"                                ]
    HAAR         = f"{DIR}/{HAAR}"
    ##########################################################################
    EYES         = AI                [ "Eyes"                                ]
    EYES         = f"{DIR}/{EYES}"
    ##########################################################################
    MOUTH        = AI                [ "Mouth"                               ]
    MOUTH        = f"{DIR}/{MOUTH}"
    ##########################################################################
    FIVEMARKS    = AI                [ "Fivemarks"                           ]
    FIVEMARKS    = f"{DIR}/{FIVEMARKS}"
    ##########################################################################
    LANDMARKS    = AI                [ "Landmarks"                           ]
    LANDMARKS    = f"{DIR}/{LANDMARKS}"
    ##########################################################################
    RESNET       = AI                [ "Resnet"                              ]
    RESNET       = f"{DIR}/{RESNET}"
    ##########################################################################
    self . FC        = cv2  . CascadeClassifier         ( HAAR               )
    self . FIVE      = dlib . shape_predictor           ( FIVEMARKS          )
    self . PREDICTOR = dlib . shape_predictor           ( LANDMARKS          )
    self . FACIAL    = dlib . face_recognition_model_v1 ( RESNET             )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 1024 , 768 )                      )
  ############################################################################
  def PrepareForActions           ( self                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def AttachActions     ( self , Enabled                                   ) :
    ##########################################################################
    if                  ( not self . isPrepared (                        ) ) :
      return False
    ##########################################################################
    isStop     = True
    isPlay     = False
    ##########################################################################
    if                  ( self . MEDIA  in [ False , None                ] ) :
      ########################################################################
      isStop   = False
      ########################################################################
    else                                                                     :
      ########################################################################
      if                ( self . PLAYER in [ False , None                ] ) :
        ######################################################################
        isStop = False
        ######################################################################
      else                                                                   :
        ######################################################################
        isPlay = self . PLAYER . is_playing (                                )
    ##########################################################################
    if                  ( self . isPause                                   ) :
      isStop   = False
    ##########################################################################
    if                  (        isPlay                                    ) :
      isStop   = False
    ##########################################################################
    if                  (        isPlay                                    ) :
      ########################################################################
      self . LinkAction ( "Play"         , self . DoPlay       , False       )
      self . LinkAction ( "Pause"        , self . DoPause      , True        )
      self . LinkAction ( "Stop"         , self . DoStop       , True        )
      self . LinkAction ( "Forward"      , self . PlayForward  , True        )
      self . LinkAction ( "Backward"     , self . PlayBackward , True        )
      ########################################################################
    elif                ( self . isPause                                   ) :
      ########################################################################
      self . LinkAction ( "Play"         , self . DoPlay       , True        )
      self . LinkAction ( "Pause"        , self . DoPause      , False       )
      self . LinkAction ( "Stop"         , self . DoStop       , True        )
      self . LinkAction ( "Forward"      , self . PlayForward  , True        )
      self . LinkAction ( "Backward"     , self . PlayBackward , True        )
      ########################################################################
    elif                (        isStop                                    ) :
      ########################################################################
      self . LinkAction ( "Play"         , self . DoPlay       , True        )
      self . LinkAction ( "Pause"        , self . DoPause      , False       )
      self . LinkAction ( "Stop"         , self . DoStop       , False       )
      self . LinkAction ( "Forward"      , self . PlayForward  , False       )
      self . LinkAction ( "Backward"     , self . PlayBackward , False       )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . LinkAction ( "Play"         , self . DoPlay       , False       )
      self . LinkAction ( "Pause"        , self . DoPause      , False       )
      self . LinkAction ( "Stop"         , self . DoStop       , False       )
      self . LinkAction ( "Forward"      , self . PlayForward  , False       )
      self . LinkAction ( "Backward"     , self . PlayBackward , False       )
    ##########################################################################
    self   . LinkAction ( "PlayPrevious" , self . PlayPrevious , False       )
    self   . LinkAction ( "PlayNext"     , self . PlayNext     , False       )
    ##########################################################################
    return
  ############################################################################
  def FocusIn             ( self                                           ) :
    ##########################################################################
    if                    ( not self . isPrepared ( )                      ) :
      return False
    ##########################################################################
    self . setActionLabel ( "Label" , self . windowTitle ( )                 )
    self . AttachActions  ( True                                             )
    ##########################################################################
    return True
  ############################################################################
  def focusInEvent           ( self , event                                ) :
    ##########################################################################
    if                       ( self . focusIn ( event )                    ) :
      return
    ##########################################################################
    super ( ) . focusInEvent ( event                                         )
    ##########################################################################
    return
  ############################################################################
  def FocusOut             ( self                                          ) :
    ##########################################################################
    if                     ( not self . isPrepared       (               ) ) :
      return False
    ##########################################################################
    if                     (     self . PANEL . hasFocus (               ) ) :
      return False
    ##########################################################################
    if                     (     self . LAYER . hasFocus (               ) ) :
      return False
    ##########################################################################
    WPLAN = self . GetPlan (                                                 )
    ##########################################################################
    if                     ( WPLAN in [ False , None ]                     ) :
      return False
    ##########################################################################
    WPLAN . Action ( "Play"         ) . setEnabled ( False                   )
    WPLAN . Action ( "Pause"        ) . setEnabled ( False                   )
    WPLAN . Action ( "Stop"         ) . setEnabled ( False                   )
    WPLAN . Action ( "Forward"      ) . setEnabled ( False                   )
    WPLAN . Action ( "Backward"     ) . setEnabled ( False                   )
    WPLAN . Action ( "PlayPrevious" ) . setEnabled ( False                   )
    WPLAN . Action ( "PlayNext"     ) . setEnabled ( False                   )
    ##########################################################################
    return True
  ############################################################################
  def focusOutEvent           ( self , event                               ) :
    ##########################################################################
    if                        ( self . focusOut ( event )                  ) :
      return
    ##########################################################################
    super ( ) . focusOutEvent ( event                                        )
    ##########################################################################
    return
  ############################################################################
  def contextMenuEvent           ( self , event                            ) :
    ##########################################################################
    if                           ( self . Menu ( event . pos ( ) )         ) :
      event . accept             (                                           )
      return
    ##########################################################################
    super ( ) . contextMenuEvent ( event                                     )
    ##########################################################################
    return
  ############################################################################
  def showEvent            ( self , e                                      ) :
    ##########################################################################
    super ( ) . showEvent  (        e                                        )
    self      . Relocation (                                                 )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent           ( self , e                                     ) :
    ##########################################################################
    super ( ) . resizeEvent (        e                                       )
    self      . Relocation  (                                                )
    ##########################################################################
    return
  ############################################################################
  def defaultCloseEvent ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Shutdown ( )                              ) :
      event . accept    (                                                    )
    else                                                                     :
      event . ignore    (                                                    )
    ##########################################################################
    return
  ############################################################################
  def closeEvent             ( self , e                                    ) :
    ##########################################################################
    self . defaultCloseEvent (        e                                      )
    ##########################################################################
    return
  ############################################################################
  def Shutdown                ( self                                       ) :
    ##########################################################################
    self . ClosePlayer . emit ( self . PID                                   )
    self . Leave       . emit ( self                                         )
    ##########################################################################
    return True
  ############################################################################
  def MoveCallback              ( self , e                                 ) :
    ##########################################################################
    if                          ( self . MEDIA in [ False , None         ] ) :
      ########################################################################
      self   . HideTool         (                                            )
      ########################################################################
      return
    ##########################################################################
    H = self . height   ( ) - self . ToolHeight
    Y = e    . position ( ) . y (                                            )
    ##########################################################################
    if                          ( Y < H                                    ) :
      ########################################################################
      if                        (     self . ShowPanel                     ) :
        ######################################################################
        self . HideTool         (                                            )
      ########################################################################
    else                                                                     :
      ########################################################################
      if                        ( not self . ShowPanel                     ) :
        ######################################################################
        self . DisplayTool      (                                            )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent           ( self , e                                  ) :
    ##########################################################################
    super ( ) . mouseMoveEvent (        e                                    )
    self      . MoveCallback   (        e                                    )
    ##########################################################################
    return
  ############################################################################
  def WheelCallback            ( self , e                                  ) :
    ##########################################################################
    Y = e . angleDelta ( ) . y (                                             )
    ##########################################################################
    if                         ( Y < 0                                     ) :
      ########################################################################
      self . PlayBackward      (                                             )
      ########################################################################
    elif                       ( Y > 0                                     ) :
      ########################################################################
      self . PlayForward       (                                             )
    ##########################################################################
    return
  ############################################################################
  def wheelEvent              ( self , e                                   ) :
    ##########################################################################
    super ( ) . wheelEvent    (        e                                     )
    self      . WheelCallback (        e                                     )
    ##########################################################################
    return
  ############################################################################
  def LOG             ( self , MSG                                         ) :
    ##########################################################################
    if                ( self . CallLogger in [ False , None              ] ) :
      return
    ##########################################################################
    if                ( len ( MSG ) <= 0                                   ) :
      return
    ##########################################################################
    self . CallLogger ( MSG                                                  )
    ##########################################################################
    return
  ############################################################################
  def DisplayTool         ( self                                           ) :
    ##########################################################################
    self . ShowPanel = True
    ##########################################################################
    self . PANEL . show   (                                                  )
    self . PANEL . raise_ (                                                  )
    ##########################################################################
    return
  ############################################################################
  def HideTool          ( self                                             ) :
    ##########################################################################
    self . ShowPanel = False
    ##########################################################################
    self . PANEL . hide (                                                    )
    ##########################################################################
    return
  ############################################################################
  def Relocation                      ( self                               ) :
    ##########################################################################
    W = self . width                  (                                      )
    H = self . height                 (                                      )
    T = self . ToolHeight
    X = 0
    Y = self . height ( ) - T
    ##########################################################################
    self . LAYER  . setGeometry       ( 0 , 0 , W , H                        )
    self . EDITOR . setGeometry       ( 0 , 0 , W , H                        )
    self . PANEL  . setGeometry       ( X , Y , W , T                        )
    ##########################################################################
    self . PANEL  . WinSize . setText ( f"{W} x {H}"                         )
    ##########################################################################
    return
  ############################################################################
  def SwitchFullScreen ( self , isFull                                     ) :
    ##########################################################################
    self . isFullScreen = isFull
    ##########################################################################
    if                 (        isFull                                     ) :
      ########################################################################
      self . isPlayList = False
      ########################################################################
      self . PANEL . BWin . show (                                           )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . PANEL . BWin . hide (                                           )
    ##########################################################################
    return
  ############################################################################
  def BackToNormal             ( self                                      ) :
    ##########################################################################
    self . NormalWindow . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def GoPlayFullScreen     ( self                                          ) :
    ##########################################################################
    self . PlayFull . emit (                                                 )
    ##########################################################################
    return
  ############################################################################
  def DockMdi                  ( self                                      ) :
    ##########################################################################
    self . DockAt = 0
    ##########################################################################
    self . PANEL . SWin . show (                                             )
    self . PANEL . MWin . hide (                                             )
    ##########################################################################
    self . GoMdi . emit        ( self . PID                                  )
    ##########################################################################
    return
  ############################################################################
  def DockStack                ( self                                      ) :
    ##########################################################################
    self . DockAt = 1
    ##########################################################################
    self . PANEL . SWin . hide (                                             )
    self . PANEL . MWin . show (                                             )
    ##########################################################################
    self . GoStack . emit      ( self . PID                                  )
    ##########################################################################
    return
  ############################################################################
  def SwitchPlayList ( self , visibility                                   ) :
    ##########################################################################
    self . isPlayList = visibility
    ##########################################################################
    return
  ############################################################################
  def SwitchEditor         ( self , CHECKED                                ) :
    ##########################################################################
    if                     ( CHECKED                                       ) :
      ########################################################################
      self . EDITOR . show (                                                 )
      ########################################################################
    else                                                                     :
      ########################################################################
      self . EDITOR . hide (                                                 )
    ##########################################################################
    return
  ############################################################################
  def ChangeStep            ( self                                         ) :
    ##########################################################################
    self . PANEL . addDelta ( self , self . Delta                            )
    ##########################################################################
    return
  ############################################################################
  def StepChanged ( self , DeltaValue                                      ) :
    ##########################################################################
    self . Delta = DeltaValue
    ##########################################################################
    return
  ############################################################################
  def AssignAsMajorPlayer     ( self                                       ) :
    ##########################################################################
    self . AssignMajor . emit ( self                                         )
    ##########################################################################
    return
  ############################################################################
  def AskToReceive            ( self , widget                              ) :
    ##########################################################################
    if                        ( widget in self . Receivers                 ) :
      return
    ##########################################################################
    self . Receivers . append ( widget                                       )
    ##########################################################################
    return
  ############################################################################
  def LeaveReceive  ( self , widget                                        ) :
    ##########################################################################
    if              ( widget not in self . Receivers                       ) :
      return
    ##########################################################################
    RR     =        [                                                        ]
    ##########################################################################
    for WW in self . Receivers                                               :
      if            ( WW != widget                                         ) :
        RR . append ( WW                                                     )
    ##########################################################################
    self . Receivers = RR
    ##########################################################################
    return
  ############################################################################
  def CurrentPlayJson           ( self , JSON                              ) :
    ##########################################################################
    if                          ( len ( self . Receivers ) <= 0            ) :
      return
    ##########################################################################
    for WW in self . Receivers                                               :
      ########################################################################
      WW . AcceptJsonFromPlayer ( JSON                                       )
    ##########################################################################
    return
  ############################################################################
  def MergeSegments       ( self , BARs                                    ) :
    ##########################################################################
    ORDERs   =            [                                                  ]
    SEGs     =            [                                                  ]
    MERGEs   =            [                                                  ]
    TOTAL    = len        ( BARs                                             )
    ##########################################################################
    if                    ( TOTAL <= 1                                     ) :
      return              ( True , BARs ,                                    )
    ##########################################################################
    for B in BARs                                                            :
      ########################################################################
      S    = B            [ "Start"                                          ]
      ########################################################################
      if                  ( S not in ORDERs                                ) :
        ######################################################################
        ORDERs . append   ( S                                                )
    ##########################################################################
    ORDERs . sort         (                                                  )
    ##########################################################################
    for T in ORDERs                                                          :
      ########################################################################
      for B in BARs                                                          :
        ######################################################################
        S  = B            [ "Start"                                          ]
        ######################################################################
        if                ( T == S                                         ) :
          ####################################################################
          MERGEs . append ( B                                                )
    ##########################################################################
    ATS    = 1
    SEGs   . append       ( MERGEs [ 0                                     ] )
    ##########################################################################
    while                 ( ATS < TOTAL                                    ) :
      ########################################################################
      SPOT = False
      ATG  = 0
      ########################################################################
      S1   = MERGEs       [ ATS ] [ "Start"                                  ]
      F1   = MERGEs       [ ATS ] [ "Finish"                                 ]
      ########################################################################
      for G in SEGs                                                          :
        ######################################################################
        if                ( not SPOT                                       ) :
          ####################################################################
          S2 = G          [ "Start"                                          ]
          F2 = G          [ "Finish"                                         ]
          E2 = int        ( F2 + 50                                          )
          ####################################################################
          if              ( ( S2 <= S1 ) and ( E2 >= S1 )                  ) :
            ##################################################################
            if            ( F1 > F2                                        ) :
              ################################################################
              F2 = F1
            ##################################################################
            SEGs          [ ATG ] [ "Finish" ] = F2
            ##################################################################
            SPOT = True
        ######################################################################
        ATG = int         ( ATG + 1                                          )
      ########################################################################
      if                  ( not SPOT                                       ) :
        ######################################################################
        SEGs . append     ( MERGEs [ ATS                                   ] )
      ########################################################################
      ATS  = int          ( ATS + 1                                          )
    ##########################################################################
    SAME   = True
    ##########################################################################
    if                    ( len ( SEGs ) != TOTAL                          ) :
      ########################################################################
      SAME = False
    ##########################################################################
    if                    ( SAME                                           ) :
      ########################################################################
      ATS  = 0
      ########################################################################
      while               ( ATS < TOTAL                                    ) :
        ######################################################################
        S1 = BARs         [ ATS ] [ "Start"                                  ]
        F1 = BARs         [ ATS ] [ "Finish"                                 ]
        ######################################################################
        S2 = SEGs         [ ATS ] [ "Start"                                  ]
        F2 = SEGs         [ ATS ] [ "Finish"                                 ]
        ######################################################################
        if                ( S1 != S2                                       ) :
          ####################################################################
          SAME = False
        ######################################################################
        if                ( F1 != F2                                       ) :
          ####################################################################
          SAME = False
        ######################################################################
        ATS    = ATS + 1
    ##########################################################################
    return                ( SAME , SEGs ,                                    )
  ############################################################################
  def AnalysisViewed                       ( self                          ) :
    ##########################################################################
    SEGs   =                               [                                 ]
    BARs   = self . Viewed                 [ "Bars"                          ]
    TOTAL  = len                           ( BARs                            )
    ##########################################################################
    if                                     ( TOTAL > 1                     ) :
      ########################################################################
      SAME = False
      SEGs = BARs
      ########################################################################
      while                                ( not SAME                      ) :
        ######################################################################
        SAME , SEGs = self . MergeSegments ( SEGs                            )
      ########################################################################
    elif                                   ( TOTAL > 0                     ) :
      ########################################################################
      SEGs . append                        ( BARs [ 0                      ] )
    ##########################################################################
    VIEWED = False
    ##########################################################################
    if                                     ( len ( SEGs ) == 1             ) :
      ########################################################################
      S1   = SEGs [ 0 ] [ "Start"                                            ]
      F1   = SEGs [ 0 ] [ "Finish"                                           ]
      DF   = int                           ( self . Duration - F1            )
      ########################################################################
      if                                   ( S1 == 0                       ) :
        ######################################################################
        if                                 ( DF <= 500                     ) :
          ####################################################################
          VIEWED = True
    ##########################################################################
    if                                     ( VIEWED                        ) :
      ########################################################################
      PLAYED = int                         ( self . FilmJSON [ "Played"    ] )
      PLAYED = int                         ( PLAYED + 1                      )
      ########################################################################
      self . FilmJSON [ "Played" ] = PLAYED
      ########################################################################
      self . BarMutex . acquire            (                                 )
      self . Viewed =                      { "Exists"   : False            , \
                                             "Duration" : self . Duration  , \
                                             "At"       : -1               , \
                                             "Bars"     : [                ] }
      self . BarMutex . release            (                                 )
      self . FilmJSON [ "Watching" ] = self . Viewed
      ########################################################################
    else                                                                     :
      ########################################################################
      SLEN = len                           ( SEGs                            )
      self . BarMutex . acquire            (                                 )
      self . Viewed =                      { "Exists"   : True             , \
                                             "Duration" : self . Duration  , \
                                             "At"       : SLEN - 1         , \
                                             "Bars"     : SEGs               }
      self . BarMutex . release            (                                 )
      self . FilmJSON [ "Watching" ] = self . Viewed
    ##########################################################################
    return
  ############################################################################
  def DoPlay ( self                                                        ) :
    ##########################################################################
    WPLAN  = self . GetPlan (                                                )
    ##########################################################################
    if                      ( WPLAN in [ False , None ]                    ) :
      return
    ##########################################################################
    if       ( self . MEDIA in [ False , None                            ] ) :
      return
    ##########################################################################
    if                                       ( self . isAnalyzing          ) :
      self . StoreAnalysis                   (                               )
    ##########################################################################
    self   . isPause = False
    self   . isAnalyzing = False
    ##########################################################################
    self   . PLAYER . play                   (                               )
    ##########################################################################
    self   . PANEL  . Play      . setEnabled ( True                          )
    self   . PANEL  . Play      . hide       (                               )
    self   . PANEL  . Stop      . setEnabled ( True                          )
    self   . PANEL  . Pause     . setEnabled ( True                          )
    self   . PANEL  . Pause     . show       (                               )
    self   . PANEL  . Analysis  . hide       (                               )
    self   . PANEL  . Drawing   . hide       (                               )
    self   . PANEL  . VMenu     . hide       (                               )
    self   . PANEL  . PrevFrame . hide       (                               )
    self   . PANEL  . NextFrame . hide       (                               )
    self   . PANEL  . FineTune  . hide       (                               )
    ##########################################################################
    WPLAN  . Action ( "Play"         ) . setEnabled ( False                  )
    WPLAN  . Action ( "Pause"        ) . setEnabled ( True                   )
    WPLAN  . Action ( "Stop"         ) . setEnabled ( True                   )
    WPLAN  . Action ( "Forward"      ) . setEnabled ( True                   )
    WPLAN  . Action ( "Backward"     ) . setEnabled ( True                   )
    WPLAN  . Action ( "PlayPrevious" ) . setEnabled ( True                   )
    WPLAN  . Action ( "PlayNext"     ) . setEnabled ( True                   )
    ##########################################################################
    self   . CLOCK             . start      (                                )
    self   . CurrentPlayJson                ( { "Action" : "Play" }          )
    ##########################################################################
    return
  ############################################################################
  def DoStop ( self                                                        ) :
    ##########################################################################
    WPLAN   = self . GetPlan (                                               )
    ##########################################################################
    if                       ( WPLAN in [ False , None ]                   ) :
      return
    ##########################################################################
    if       ( self . MEDIA in [ False , None                            ] ) :
      return
    ##########################################################################
    if                                       ( self . isAnalyzing          ) :
      self . StoreAnalysis                   (                               )
    ##########################################################################
    self   . isPause = False
    self   . isAnalyzing = False
    ##########################################################################
    self   . PLAYER . stop                   (                               )
    ##########################################################################
    self   . PANEL  . Play      . setEnabled ( True                          )
    self   . PANEL  . Play      . show       (                               )
    self   . PANEL  . Stop      . setEnabled ( False                         )
    self   . PANEL  . Pause     . setEnabled ( True                          )
    self   . PANEL  . Pause     . hide       (                               )
    self   . PANEL  . Analysis  . hide       (                               )
    self   . PANEL  . Drawing   . hide       (                               )
    self   . PANEL  . VMenu     . hide       (                               )
    self   . PANEL  . PrevFrame . hide       (                               )
    self   . PANEL  . NextFrame . hide       (                               )
    self   . PANEL  . FineTune  . hide       (                               )
    ##########################################################################
    WPLAN  . Action ( "Play"         ) . setEnabled ( True                   )
    WPLAN  . Action ( "Pause"        ) . setEnabled ( False                  )
    WPLAN  . Action ( "Stop"         ) . setEnabled ( False                  )
    WPLAN  . Action ( "Forward"      ) . setEnabled ( False                  )
    WPLAN  . Action ( "Backward"     ) . setEnabled ( False                  )
    WPLAN  . Action ( "PlayPrevious" ) . setEnabled ( True                   )
    WPLAN  . Action ( "PlayNext"     ) . setEnabled ( True                   )
    ##########################################################################
    self   . CLOCK             . stop       (                                )
    self   . FinishFilmBar                  (                                )
    self   . AUDIO             . stop       (                                )
    ##########################################################################
    self   . AnalysisViewed                 (                                )
    self   . FilmStopped . emit             ( self . FilmJSON                )
    self   . CurrentPlayJson                ( { "Action" : "Stop" }          )
    ##########################################################################
    return
  ############################################################################
  def DoPause ( self                                                       ) :
    ##########################################################################
    WPLAN = self . GetPlan (                                                 )
    ##########################################################################
    if                     ( WPLAN in [ False , None ]                     ) :
      return
    ##########################################################################
    if        ( self . MEDIA in [ False , None                           ] ) :
      return
    ##########################################################################
    self  . isPause = True
    ##########################################################################
    self  . PLAYER . pause                  (                                )
    ##########################################################################
    self  . PANEL  . Play      . setEnabled ( True                           )
    self  . PANEL  . Play      . show       (                                )
    self  . PANEL  . Stop      . setEnabled ( True                           )
    self  . PANEL  . Pause     . setEnabled ( True                           )
    self  . PANEL  . Pause     . hide       (                                )
    self  . PANEL  . Analysis  . show       (                                )
    self  . PANEL  . Drawing   . show       (                                )
    self  . PANEL  . VMenu     . show       (                                )
    self  . PANEL  . PrevFrame . show       (                                )
    self  . PANEL  . NextFrame . show       (                                )
    ##########################################################################
    WPLAN . Action ( "Play"         ) . setEnabled ( True                    )
    WPLAN . Action ( "Pause"        ) . setEnabled ( False                   )
    WPLAN . Action ( "Stop"         ) . setEnabled ( True                    )
    WPLAN . Action ( "Forward"      ) . setEnabled ( True                    )
    WPLAN . Action ( "Backward"     ) . setEnabled ( True                    )
    WPLAN . Action ( "PlayPrevious" ) . setEnabled ( True                    )
    WPLAN . Action ( "PlayNext"     ) . setEnabled ( True                    )
    ##########################################################################
    self  . FinishFilmBar                  (                                 )
    self  . CLOCK             . stop       (                                 )
    ##########################################################################
    self  . EnableFineTune                 (                                 )
    self  . CurrentPlayJson                ( { "Action" : "Pause" }          )
    ##########################################################################
    return
  ############################################################################
  def EnableFineTune                     ( self                            ) :
    ##########################################################################
    self . PANEL . FineTune . show       (                                   )
    self . PANEL . FineTune . setEnabled ( True                              )
    self . AdjustFineTune                (                                   )
    ##########################################################################
    return
  ############################################################################
  def AdjustFineTune                          ( self                       ) :
    ##########################################################################
    CTS     = self  . PLAYER . get_time       (                              )
    FRV     = int                             ( self . FineRange             )
    MRV     = int                             ( CTS - int ( FRV / 2 )        )
    ##########################################################################
    if                                        ( MRV < 0                    ) :
      ########################################################################
      MRV   = 0
    ##########################################################################
    ERV     = int                             ( MRV + FRV                    )
    ##########################################################################
    if                                        ( ERV >= self . Duration     ) :
      ########################################################################
      ERV   = self . Duration
      MRV   = int                             ( ERV - FRV                    )
      ########################################################################
      if                                      ( MRV < 0                    ) :
        ######################################################################
        MRV = 0
    ##########################################################################
    self    . PANEL . FineTune . blockSignals ( True                         )
    self    . PANEL . FineTune . setMinimum   ( MRV                          )
    self    . PANEL . FineTune . setMaximum   ( ERV                          )
    self    . PANEL . FineTune . setValue     ( CTS                          )
    self    . PANEL . FineTune . blockSignals ( False                        )
    ##########################################################################
    return
  ############################################################################
  def PlayForward                     ( self                               ) :
    ##########################################################################
    if                                ( self . MEDIA in [ False , None   ] ) :
      return
    ##########################################################################
    if                                ( self . isStopped (               ) ) :
      return
    ##########################################################################
    K    = self . PLAYER . get_time   (                                      )
    T    = int                        ( K + self . Delta                     )
    ##########################################################################
    if                                ( T >= self . Duration               ) :
      T  = self . Duration
    ##########################################################################
    self . PLAYER . set_time          ( T                                    )
    ##########################################################################
    self . BarMutex . acquire         (                                      )
    ##########################################################################
    self . FvRange [ "Finish" ]         = K
    VAT                                 = self . Viewed [ "At"               ]
    self . Viewed  [ "Bars"   ] [ VAT ] = self . FvRange
    ##########################################################################
    self . FvRange [ "Start"  ]         = T
    self . FvRange [ "Finish" ]         = T
    ##########################################################################
    self . Viewed  [ "Bars"   ] . append ( self . FvRange                    )
    self . Viewed  [ "At"     ]         = VAT + 1
    ##########################################################################
    self . BarMutex . release         (                                      )
    ##########################################################################
    self . CalculateFilmBar           (                                      )
    self . UpdateINFO                 (                                      )
    ##########################################################################
    return
  ############################################################################
  def PlayBackward                  ( self                                 ) :
    ##########################################################################
    if                              ( self . MEDIA in [ False , None     ] ) :
      return
    ##########################################################################
    if                              ( self . isStopped (                 ) ) :
      return
    ##########################################################################
    K    = self . PLAYER . get_time (                                        )
    T    = int                      ( K - self . Delta                       )
    ##########################################################################
    if                              ( T < 0                                ) :
      T  = 0
    ##########################################################################
    self . PLAYER . set_time        ( T                                      )
    ##########################################################################
    self . BarMutex . acquire       (                                        )
    ##########################################################################
    self . FvRange [ "Finish" ]         = K
    VAT                                 = self . Viewed [ "At"               ]
    self . Viewed  [ "Bars"   ] [ VAT ] = self . FvRange
    ##########################################################################
    self . FvRange [ "Start"  ]         = T
    self . FvRange [ "Finish" ]         = T
    ##########################################################################
    self . Viewed  [ "Bars"   ] . append ( self . FvRange                    )
    self . Viewed  [ "At"     ]         = VAT + 1
    ##########################################################################
    self . BarMutex . release       (                                        )
    ##########################################################################
    self . CalculateFilmBar         (                                        )
    self . UpdateINFO               (                                        )
    ##########################################################################
    return
  ############################################################################
  def DoPreviousFrame               ( self                                 ) :
    ##########################################################################
    if                              ( self . MEDIA in [ False , None ]     ) :
      return
    ##########################################################################
    if                              ( self . isStopped (                 ) ) :
      return
    ##########################################################################
    K    = self . PLAYER . get_time (                                        )
    T    = int                      ( K - 100                                )
    ##########################################################################
    if                              ( T < 0                                ) :
      T  = 0
    ##########################################################################
    self . PLAYER . set_time        ( T                                      )
    ##########################################################################
    self . CalculateFilmBar         (                                        )
    self . UpdateINFO               (                                        )
    ##########################################################################
    return
  ############################################################################
  def DoNextFrame              ( self                                      ) :
    ##########################################################################
    if                         ( self . MEDIA in [ False , None ]          ) :
      return
    ##########################################################################
    if                         ( self . isStopped (                      ) ) :
      return
    ##########################################################################
    self . PLAYER . next_frame (                                             )
    self . CalculateFilmBar    (                                             )
    self . UpdateINFO          (                                             )
    ##########################################################################
    return
  ############################################################################
  def PlayPrevious ( self                                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def PlayNext ( self                                                      ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def toClock  ( self , T                                                  ) :
    ##########################################################################
    R    = int ( T  % 1000                                                   )
    S    = int ( T  / 1000                                                   )
    ##########################################################################
    DD   = ""
    V    = R
    ##########################################################################
    for i in range ( 0 , 3                                                 ) :
      ########################################################################
      Z  = int     ( V % 10                                                  )
      V  = int     ( V / 10                                                  )
      ########################################################################
      DD = f"{Z}{DD}"
    ##########################################################################
    SS   = int ( S  % 60                                                     )
    MM   = int ( S  / 60                                                     )
    ##########################################################################
    SA   = int ( SS % 10                                                     )
    SB   = int ( SS / 10                                                     )
    SS   = f"{SB}{SA}"
    ##########################################################################
    HH   = int ( MM / 60                                                     )
    MM   = int ( MM % 60                                                     )
    ##########################################################################
    MA   = int ( MM % 10                                                     )
    MB   = int ( MM / 10                                                     )
    MM   = f"{MB}{MA}"
    ##########################################################################
    return f"{HH}:{MM}:{SS}.{DD}"
  ############################################################################
  def toTicks  ( self                                                      ) :
    ##########################################################################
    D =    int ( self . Duration                                             )
    S =    int ( self . Step                                                 )
    M =    int ( D + S - 1                                                   )
    ##########################################################################
    return int ( M / S                                                       )
  ############################################################################
  def toTick   ( self , T                                                  ) :
    ##########################################################################
    S =    int ( self . Step                                                 )
    ##########################################################################
    return int ( T / S                                                       )
  ############################################################################
  def toTimestamp ( self , T                                               ) :
    ##########################################################################
    D   = int     ( self . Duration                                          )
    S   = int     ( self . Step                                              )
    K   = int     ( T * S                                                    )
    ##########################################################################
    if            ( K > D                                                  ) :
      ########################################################################
      K = D
    ##########################################################################
    return K
  ############################################################################
  def UpdateINFO ( self                                                    ) :
    ##########################################################################
    if           ( self . MEDIA in [ False , None                        ] ) :
      return
    ##########################################################################
    if           ( self . Duration <= 0                                    ) :
      return
    ##########################################################################
    VPOS  = self  . PLAYER . get_time   (                                    )
    POS   = self  . toTick              ( VPOS                               )
    S     = self  . toClock             ( VPOS                               )
    ##########################################################################
    self  . PANEL . Clock  . setValue   ( POS                                )
    self  . PANEL . Clock  . setToolTip ( S                                  )
    self  . PANEL . CLabel . setText    ( S                                  )
    ##########################################################################
    if           ( not self . PLAYER . is_playing (                      ) ) :
      ########################################################################
      self . CLOCK . stop (                                                  )
      ########################################################################
      if         ( not self . isPause                                      ) :
        ######################################################################
        self . DoStop (                                                      )
        self . PANEL . Clock . setValue ( 0                                  )
        ######################################################################
        if            ( self . Method == 1                                 ) :
          ####################################################################
          self . TryAnotherPlaylist (                                        )
    ##########################################################################
    self . BarMutex . acquire       (                                        )
    ##########################################################################
    VAT = self . Viewed [ "At"                                               ]
    VNT = len           ( self  . Viewed  [ "Bars" ]                         )
    ##########################################################################
    if                  ( ( VAT >= 0 ) and ( VAT < VNT )                   ) :
      ########################################################################
      self . FvRange [ "Finish" ]         = VPOS
      self . Viewed  [ "Bars"   ] [ VAT ] = self . FvRange
    ##########################################################################
    self   . BarMutex . release     (                                        )
    ##########################################################################
    self   . CalculateFilmBar       (                                        )
    self   . CurrentPlayJson        ( { "Action" : "Update" , "PTS" : VPOS } )
    ##########################################################################
    return
  ############################################################################
  def UpdateAudio                            ( self                        ) :
    ##########################################################################
    V    = self  . PLAYER . audio_get_volume (                               )
    ##########################################################################
    self . PANEL . Volume . setToolTip       ( f"{V}%"                       )
    self . PANEL . Volume . setValue         ( V                             )
    ##########################################################################
    return
  ############################################################################
  def FinishFilmBar                         ( self                         ) :
    ##########################################################################
    self   . BarMutex . acquire             (                                )
    ##########################################################################
    CTS    = self   . PLAYER . get_time     (                                )
    ##########################################################################
    if                                      ( CTS >= 0                     ) :
      ########################################################################
      self . FvRange [ "Finish" ]         = CTS
    ##########################################################################
    VAT                                 = self . Viewed [ "At"               ]
    self   . Viewed  [ "Bars"   ] [ VAT ] = self . FvRange
    ##########################################################################
    SKT    = self . FvRange                 [ "Start"                        ]
    FKT    = self . FvRange                 [ "Finish"                       ]
    ##########################################################################
    if                                      ( CTS >= 0 ) and ( SKT != FKT )  :
      ########################################################################
      self . FvRange                      = { "Start" : CTS , "Finish" : CTS }
      ########################################################################
      self . Viewed  [ "Bars"   ] . append  ( self . FvRange                 )
      self . Viewed  [ "At"     ]         = VAT + 1
    ##########################################################################
    self   . BarMutex . release             (                                )
    ##########################################################################
    self   . CalculateFilmBar               (                                )
    ##########################################################################
    return
  ############################################################################
  def CalculateFilmBar       ( self                                        ) :
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    ##########################################################################
    self . FilmViewed . emit ( self . Viewed                                 )
    ##########################################################################
    return
  ############################################################################
  def AssignPlayerPTS        ( self , PTS                                  ) :
    ##########################################################################
    self . PLAYER . set_time (        PTS                                    )
    self . UpdateINFO        (                                               )
    ##########################################################################
    return
  ############################################################################
  def setPosition                           ( self                         ) :
    ##########################################################################
    self . CLOCK  . stop                    (                                )
    CTS  = self   . PLAYER . get_time       (                                )
    POS  = self   . PANEL  . Clock . value  (                                )
    RATE = self   . toTimestamp             ( POS                            )
    self . PLAYER . set_time                ( RATE                           )
    self . CLOCK  . start                   (                                )
    ##########################################################################
    if                                      ( self . isPause               ) :
      ########################################################################
      self . BarMutex . acquire             (                                )
      ########################################################################
      VAT                                 = self . Viewed [ "At"             ]
      self . FvRange [ "Start"  ]         = RATE
      self . FvRange [ "Finish" ]         = RATE
      self . Viewed  [ "Bars"   ] [ VAT ] = self . FvRange
      ########################################################################
      self . BarMutex . release             (                                )
      ########################################################################
      self . AdjustFineTune                 (                                )
      ########################################################################
      return
    ##########################################################################
    self   . BarMutex . acquire             (                                )
    ##########################################################################
    if                                      ( CTS >= 0                     ) :
      ########################################################################
      self . FvRange [ "Finish" ]         = CTS
    ##########################################################################
    VAT                                 = self . Viewed [ "At"               ]
    self   . Viewed  [ "Bars"   ] [ VAT ] = self . FvRange
    ##########################################################################
    SKT    = self . FvRange                 [ "Start"                        ]
    FKT    = self . FvRange                 [ "Finish"                       ]
    ##########################################################################
    if                                      ( SKT != FKT                   ) :
      ########################################################################
      self . FvRange                      = { "Start"  : RATE              , \
                                              "Finish" : RATE                }
      ########################################################################
      self . Viewed  [ "Bars"   ] . append  ( self . FvRange                 )
      self . Viewed  [ "At"     ]         = VAT + 1
      ########################################################################
    else                                                                     :
      ########################################################################
      self . FvRange [ "Start"  ]         = RATE
      self . FvRange [ "Finish" ]         = RATE
      ########################################################################
      VAT                                 = self . Viewed [ "At"             ]
      self . Viewed  [ "Bars"   ] [ VAT ] = self . FvRange
    ##########################################################################
    self   . BarMutex . acquire             (                                )
    ##########################################################################
    self   . CalculateFilmBar               (                                )
    ##########################################################################
    return
  ############################################################################
  def setFineTune ( self                                                   ) :
    ##########################################################################
    self . CLOCK  . stop                      (                              )
    RATE = self   . PANEL  . FineTune . value (                              )
    CPOS = self   . toTick                    ( RATE                         )
    self . PLAYER . set_time                  ( RATE                         )
    self . CLOCK  . start                     (                              )
    ##########################################################################
    self . BarMutex . acquire                 (                              )
    ##########################################################################
    VAT                                 = self . Viewed [ "At"               ]
    self . FvRange [ "Start"  ]         = RATE
    self . FvRange [ "Finish" ]         = RATE
    self . Viewed  [ "Bars"   ] [ VAT ] = self . FvRange
    ##########################################################################
    self . BarMutex . release                 (                              )
    ##########################################################################
    self . PANEL  . Clock . blockSignals      ( True                         )
    self . PANEL  . Clock . setValue          ( CPOS                         )
    self . PANEL  . Clock . value             (                              )
    ##########################################################################
    return
  ############################################################################
  def releaseFineTune     ( self                                           ) :
    ##########################################################################
    self . setFineTune    (                                                  )
    self . AdjustFineTune (                                                  )
    ##########################################################################
    return
  ############################################################################
  def setVolume                         ( self , volume                    ) :
    ##########################################################################
    self . PLAYER . audio_set_volume    ( volume                             )
    self . PANEL  . Volume . setToolTip ( f"{volume}%"                       )
    ##########################################################################
    return
  ############################################################################
  def isStopped ( self                                                     ) :
    ##########################################################################
    if          ( self . MEDIA in [ False , None                         ] ) :
      return True
    ##########################################################################
    if          ( self . isPause                                           ) :
      return False
    ##########################################################################
    if          ( self . PLAYER . is_playing (                           ) ) :
      return False
    ##########################################################################
    return   True
  ############################################################################
  def Prepare          ( self                                              ) :
    ##########################################################################
    self . setPrepared ( True                                                )
    ##########################################################################
    return
  ############################################################################
  def loading                         ( self                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self   . Go      ( self . loading                                        )
    ##########################################################################
    return
  ############################################################################
  def SnapShot      ( self                                                 ) :
    ##########################################################################
    if              ( self . MEDIA in [ False , None                     ] ) :
      return
    ##########################################################################
    NOW  = StarDate (                                                        )
    NOW  . Now      (                                                        )
    SDT  = NOW . Stardate
    ##########################################################################
    TEMP = self . Settings [ "Temp"                                          ]
    F    = f"{TEMP}\\{SDT}.png"
    ##########################################################################
    self . PLAYER . video_take_snapshot ( 0 , F , 0 , 0                      )
    ##########################################################################
    return
  ############################################################################
  def ShowFirstOnly              ( self                                    ) :
    ##########################################################################
    DURATION = self . PLAYER . get_length (                                  )
    ##########################################################################
    if                           ( DURATION <= 0                           ) :
      ########################################################################
      QTimer . singleShot        ( 100 , self , self . ShowFirstOnly         )
      ########################################################################
      return
    ##########################################################################
    self . PLAYER . set_time     ( 0                                         )
    self . PLAYER . stop         (                                           )
    ##########################################################################
    self . Duration = DURATION
    self . Range    = self . toTicks (                                       )
    ##########################################################################
    S    = self  . toClock       ( DURATION                                  )
    self . PANEL . FLabel . setText    ( S                                   )
    self . PANEL . Clock  . setMaximum ( self . Range                        )
    ##########################################################################
    ( W , H ) = self  . PLAYER . video_get_size (                            )
    self . VWidth  = W
    self . VHeight = H
    ##########################################################################
    self . PANEL . FilmSize . setText ( f"{W} x {H}"                         )
    ##########################################################################
    return
  ############################################################################
  def Play ( self , Filename                                               ) :
    ##########################################################################
    self . Method = 0
    self . MEDIA  = self . INSTANCE . media_new ( Filename                   )
    self . PLAYER . set_media                   ( self . MEDIA               )
    self . MEDIA  . parse                       (                            )
    ##########################################################################
    TITLE         = self . MEDIA  . get_meta    ( 0                          )
    self          . setWindowTitle              ( TITLE                      )
    ##########################################################################
    self          . PLAYER . set_hwnd ( int ( self . LAYER . winId (     ) ) )
    self          . PLAYER . video_set_mouse_input ( False                   )
    self          . PLAYER . video_set_key_input   ( False                   )
    ##########################################################################
    self . Duration = -1
    self . Range    = 1000
    self . isPause  = False
    self . PANEL . Clock . setMaximum     ( 1000                             )
    self . PANEL . Clock . setValue       ( 0                                )
    ##########################################################################
    self         . PLAYER . play          (                                  )
    ##########################################################################
    self . PANEL . Volume . setValue ( self . PLAYER . audio_get_volume ( )  )
    ##########################################################################
    self . PANEL . Play   . setEnabled ( True                                )
    self . PANEL . Play   . show       (                                     )
    self . PANEL . Stop   . setEnabled ( False                               )
    self . PANEL . Pause  . setEnabled ( True                                )
    self . PANEL . Pause  . hide       (                                     )
    ##########################################################################
    self . PANEL . raise_ (                                                  )
    ##########################################################################
    QTimer . singleShot   ( 100 , self , self . ShowFirstOnly                )
    ##########################################################################
    return
  ############################################################################
  def TryAnotherPlaylist          ( self                                   ) :
    ##########################################################################
    self . PlayerCompleted . emit ( self . PID                               )
    ##########################################################################
    return
  ############################################################################
  def FromPlaylist ( self , FILM                                           ) :
    ##########################################################################
    WPLAN = self . GetPlan (                                                 )
    ##########################################################################
    if                     ( WPLAN in [ False , None ]                     ) :
      return
    ##########################################################################
    self  . FilmJSON = FILM
    ##########################################################################
    self  . PANEL . Play   . setEnabled ( False                              )
    self  . PANEL . Play   . show       (                                    )
    self  . PANEL . Stop   . setEnabled ( False                              )
    self  . PANEL . Pause  . setEnabled ( False                              )
    self  . PANEL . Pause  . hide       (                                    )
    ##########################################################################
    qApp  . processEvents               (                                    )
    ##########################################################################
    Filename = FILM [ "Path"                                                 ]
    TITLE    = FILM [ "Name"                                                 ]
    ##########################################################################
    self  . setWindowTitle              (           TITLE                    )
    self  . setActionLabel              ( "Label" , TITLE                    )
    ##########################################################################
    self  . Method = 1
    self  . MEDIA  = self . INSTANCE . media_new ( Filename                  )
    self  . PLAYER . set_media                   ( self . MEDIA              )
    self  . MEDIA  . parse                       (                           )
    ##########################################################################
    self          . PLAYER . set_hwnd   ( int ( self . LAYER . winId (   ) ) )
    self          . PLAYER . video_set_mouse_input ( False                   )
    self          . PLAYER . video_set_key_input   ( False                   )
    ##########################################################################
    DURATION         = FILM [ "Duration"                                     ]
    DURATION         = int  ( DURATION / 1000                                )
    self  . Duration = DURATION
    self  . Range    = self . toTicks   (                                    )
    self  . isPause  = False
    S                = self . toClock   ( DURATION                           )
    self  . PANEL . FLabel . setText    ( S                                  )
    self  . PANEL . Clock  . setMaximum ( self . Range                       )
    self  . PANEL . Clock  . setValue   ( 0                                  )
    ##########################################################################
    self  . Viewed   = FILM [ "Watching"                                     ]
    self  . FvRange  =      { "Start"    : 0                               , \
                              "Finish"   : 0                                 }
    ##########################################################################
    self  . Viewed [ "Bars" ] . append ( self  . FvRange                     )
    ATI   = len             ( self  . Viewed [ "Bars"                      ] )
    self  . Viewed [ "At"   ] = int    ( ATI - 1                             )
    ##########################################################################
    self  . VWidth  = FILM [ "Width"                                         ]
    self  . VHeight = FILM [ "Height"                                        ]
    ##########################################################################
    self  . PANEL . FilmSize . setText  ( f"{self.VWidth} x {self.VHeight}"  )
    ##########################################################################
    self         . PLAYER . play        (                                    )
    qApp  . processEvents               (                                    )
    ##########################################################################
    self  . PANEL . Volume . setValue   ( self . PLAYER . audio_get_volume() )
    ##########################################################################
    self  . PANEL . Play   . setEnabled ( True                               )
    self  . PANEL . Play   . hide       (                                    )
    self  . PANEL . Stop   . setEnabled ( True                               )
    self  . PANEL . Pause  . setEnabled ( True                               )
    self  . PANEL . Pause  . show       (                                    )
    ##########################################################################
    WPLAN . Action ( "Play"         ) . setEnabled ( False                   )
    WPLAN . Action ( "Pause"        ) . setEnabled ( True                    )
    WPLAN . Action ( "Stop"         ) . setEnabled ( True                    )
    WPLAN . Action ( "Forward"      ) . setEnabled ( True                    )
    WPLAN . Action ( "Backward"     ) . setEnabled ( True                    )
    WPLAN . Action ( "PlayPrevious" ) . setEnabled ( True                    )
    WPLAN . Action ( "PlayNext"     ) . setEnabled ( True                    )
    ##########################################################################
    self  . PANEL . raise_             (                                     )
    self  . CLOCK . start              (                                     )
    self  . CalculateFilmBar           (                                     )
    ##########################################################################
    qApp  . processEvents              (                                     )
    ##########################################################################
    JJ    =                            { "Action" : "Open"                   }
    for KEY in FILM . keys             (                                   ) :
      ########################################################################
      JJ [ KEY ] = FILM                [ KEY                                 ]
    ##########################################################################
    self  . CurrentPlayJson            ( JJ                                  )
    ##########################################################################
    return
  ############################################################################
  def FromEpisode ( self , EPISODE                                         ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def StoreAnalysis ( self                                                 ) :
    ##########################################################################
    OFILE = self . Settings [ "Classifier" ] [ "Output"                      ]
    SaveJson        ( OFILE , self . ATJ                                     )
    ##########################################################################
    return
  ############################################################################
  def HandleAnalysis ( self , T , FILENAME                                 ) :
    ##########################################################################
    FE    = Path     ( FILENAME                                              )
    ##########################################################################
    if               ( not FE . exists (                                 ) ) :
      ########################################################################
      self . NextAnalysis . emit (                                           )
      ########################################################################
      return
    ##########################################################################
    if               ( not FE . is_file (                                ) ) :
      ########################################################################
      self . NextAnalysis . emit (                                           )
      ########################################################################
      return
    ##########################################################################
    self  . ATS  . append ( T                                                )
    ##########################################################################
    TRIGGER = self . Settings [ "Classifier" ] [ "Probability"               ]
    REMOVE  = self . Settings [ "Classifier" ] [ "Remove"                    ]
    ##########################################################################
    QIMG  = QImage                      ( FILENAME                           )
    self  . EDITOR . AssignImage        ( QIMG                               )
    ##########################################################################
    IMG   = self . AIV . Image          ( FILENAME                           )
    ITEMs = self . AIV . Classification ( IMG , TRIGGER                      )
    NAMEs = self . AIV . toCategories   ( ITEMs                              )
    ##########################################################################
    TRIGGER = self . Settings [ "Objectron" ] [ "Probability"                ]
    OBJs    = self  . AIV . ObjectDetection ( IMG , TRIGGER                  )
    ##########################################################################
    for OBJI in OBJs                                                         :
      ########################################################################
      ONAMEs = self . AIV . toCategories ( OBJI [ "Categories" ]             )
      ########################################################################
      for N in ONAMEs                                                        :
        ######################################################################
        if               ( N not in NAMEs                                  ) :
          ####################################################################
          NAMEs . append ( N                                                 )
    ##########################################################################
    SIMG    = self . AIV . Stylization ( IMG                                 )
    ## SPIC    = PictureItem   (                                                )
    if ( SIMG not in [ False , None ] ) :
      SFILE   = f"D:/AITK/Download/Video/{T}-Stylization.jpg"
      CVX     = cv2 . cvtColor ( SIMG . numpy_view ( ) , cv2 . COLOR_BGR2RGB  )
      cv2     . imwrite ( SFILE , CVX )
    ## SPIC    . FromMediapipe ( SIMG                                           )
    ## SPIC    . Save          ( SFILE                                          )
    ##########################################################################
    BODYs   =               [                                                ]
    BOOBs   =               [                                                ]
    FACEs   =               [                                                ]
    MESHs   =               [                                                ]
    PIC     = PictureItem   (                                                )
    OK      = PIC . Load    ( FILENAME                                       )
    ##########################################################################
    if                      ( OK                                           ) :
      ########################################################################
      IMX  = PIC . toOpenCV (                                                )
      GRAY = cv2 . cvtColor ( IMX , cv2 . COLOR_BGR2GRAY                     )
      RGB  = cv2 . cvtColor ( IMX , cv2 . COLOR_BGR2RGB                      )
      WW   = PIC . Width    (                                                )
      HH   = PIC . Height   (                                                )
      ########################################################################
      KPS = self . BDI . GetBodyKeyPoints ( RGB , WW , HH                    )
      ########################################################################
      if                   ( KPS [ "Body" ] [ "Exists" ]                   ) :
        ######################################################################
        BODYs . append     ( KPS                                             )
      ########################################################################
      BOOBz   = self . BOOB . ToBoobs         ( GRAY                         )
      DLIBs   = self . BOOB . ToDlibBoobs     ( RGB                          )
      BOOBs   = self . BOOB . BoobsToJson     ( BOOBz , BOOBs                )
      BOOBs   = self . BOOB . DlibBoobsToJson ( DLIBs , BOOBs                )
      ########################################################################
      FACE    = FaceItem                      (                              )
      FACE    . Classifier = self . FC
      FACE    . Fivemarks  = self . FIVE
      FACE    . Predictor  = self . PREDICTOR
      FACE    . Facial     = self . FACIAL
      ########################################################################
      FACEz   = FACE . ToFaces                ( GRAY                         )
      ########################################################################
      for F in FACEz                                                         :
        ######################################################################
        FACE . setFull                        ( WW , HH                      )
        SRQ  = FACE . RectangleFromOpenCV     ( F                            )
        KRQ  = FACE . ScaleRectangle          ( SRQ , 1.4                    )
        KQQ  = FACE . ToSquareRectangle       ( KRQ                          )
        SSK  = FACE . RestraintRectangle      ( FACE . Full , KQQ            )
        ######################################################################
        FACEs . append                        ( SSK                          )
    ##########################################################################
    J     = { "Time"       : T                                             , \
              "Categories" : NAMEs                                         , \
              "Items"      : ITEMs                                         , \
              "Objects"    : OBJs                                          , \
              "Bodies"     : BODYs                                         , \
              "Boobs"      : BOOBs                                         , \
              "Faces"      : FACEs                                         , \
              "Meshes"     : MESHs                                           }
    self  . ATJ . append ( J                                                 )
    ## print ( json . dumps ( J ) )
    ##########################################################################
    if                 ( REMOVE                                            ) :
      os . remove      ( FILENAME                                            )
    ##########################################################################
    self . NextAnalysis . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def DoAnalysis    ( self                                                 ) :
    ##########################################################################
    if              ( not self . isAnalyzing                               ) :
      return
    ##########################################################################
    L    = self . PLAYER . get_length (                                      )
    T    = self . PLAYER . get_time   (                                      )
    ##########################################################################
    if              ( T in self . ATS                                      ) :
      ########################################################################
      self . PLAYER . set_time   ( T + 100                                   )
      self . NextAnalysis . emit (                                           )
      ########################################################################
      return
    ##########################################################################
    if              ( ( L - T ) < 300                                      ) :
      ########################################################################
      self . isAnalyzing = False
      self . PANEL . Analysis . show (                                       )
      self . StoreAnalysis (                                                 )
      ########################################################################
      return
    ##########################################################################
    T     = self  . PLAYER . get_time   (                                    )
    POS   = self  . toTick              ( T                                  )
    S     = self  . toClock             ( T                                  )
    ##########################################################################
    self  . PANEL . Clock  . setValue   ( POS                                )
    self  . PANEL . Clock  . setToolTip ( S                                  )
    self  . PANEL . CLabel . setText    ( S                                  )
    ##########################################################################
    NOW  = StarDate (                                                        )
    NOW  . Now      (                                                        )
    SDT  = NOW . Stardate
    ##########################################################################
    K    = f"{T}"
    while           ( len ( K ) < 9                                        ) :
      K  = f"0{K}"
    ##########################################################################
    TEMP = self . Settings [ "Temp"                                          ]
    F    = f"{TEMP}\\{K}-{SDT}.png"
    ##########################################################################
    self . PLAYER . video_take_snapshot ( 0 , F , 0 , 0                      )
    ##########################################################################
    self . Go       ( self . HandleAnalysis , ( T , F ,                    ) )
    ##########################################################################
    self . PLAYER . next_frame (                                             )
    ##########################################################################
    return
  ############################################################################
  def RunAnalysis ( self                                                   ) :
    ##########################################################################
    if            ( self . isAnalyzing                                     ) :
      return
    ##########################################################################
    self . isAnalyzing = True
    self . ATS         =       [                                             ]
    self . ATJ         =       [                                             ]
    ##########################################################################
    self . PANEL . Analysis . hide (                                         )
    ##########################################################################
    self . NextAnalysis . emit (                                             )
    ##########################################################################
    return
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
    TRX    = self . Translations   [ "Player"                                ]
    mm     = MenuManager           ( self                                    )
    ##########################################################################
    if                             ( self . isPlayList                     ) :
      ########################################################################
      MSG  = TRX                   [ "HidePlayList"                          ]
      mm   . addAction             ( 9202 , MSG                              )
      ########################################################################
    else                                                                     :
      ########################################################################
      MSG  = TRX                   [ "ShowPlayList"                          ]
      mm   . addAction             ( 9201 , MSG                              )
    ##########################################################################
    MSG    = TRX                   [ "MajorPlayer"                           ]
    mm     . addAction             ( 9801 , MSG                              )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    if                             ( self . isFullScreen                   ) :
      ########################################################################
      MSG  = TRX                   [ "NormalWindow"                          ]
      ICO  = QIcon                 ( ":/images/GUI.png"                      )
      mm   . addActionWithIcon     ( 9301 , ICO , MSG                        )
      ########################################################################
    else                                                                     :
      ########################################################################
      MSG  = TRX                   [ "PlayFullWindow"                        ]
      ICO  = QIcon                 ( ":/images/fullscreen.png"               )
      mm   . addActionWithIcon     ( 9302 , ICO , MSG                        )
    ##########################################################################
    if                             ( 0 == self . DockAt                    ) :
      ########################################################################
      MSG  = TRX                   [ "Stacked"                               ]
      mm   . addAction             ( 9401 , MSG                              )
      ########################################################################
    elif                           ( 1 == self . DockAt                    ) :
      ########################################################################
      MSG  = TRX                   [ "MDI"                                   ]
      mm   . addAction             ( 9402 , MSG                              )
    ##########################################################################
    mm     . setFont               ( self    . menuFont ( )                  )
    aa     = mm . exec_            ( QCursor . pos      ( )                  )
    at     = mm . at               ( aa                                      )
    ##########################################################################
    if                             ( at == 9201                            ) :
      ########################################################################
      self . isPlayList = True
      self . TogglePlaylist . emit ( self . isPlayList                       )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 9202                            ) :
      ########################################################################
      self . isPlayList = False
      self . TogglePlaylist . emit ( self . isPlayList                       )
      ########################################################################
      return True
    ##########################################################################
    if                             ( at == 9301                            ) :
      self . BackToNormal          (                                         )
      return True
    ##########################################################################
    if                             ( at == 9302                            ) :
      self . GoPlayFullScreen      (                                         )
      return True
    ##########################################################################
    if                             ( at == 9401                            ) :
      self . DockStack             (                                         )
      return True
    ##########################################################################
    if                             ( at == 9402                            ) :
      self . DockMdi               (                                         )
      return True
    ##########################################################################
    if                             ( at == 9801                            ) :
      self . AssignAsMajorPlayer   (                                         )
      return True
    ##########################################################################
    return True
##############################################################################
