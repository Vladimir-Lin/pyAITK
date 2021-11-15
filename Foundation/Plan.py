# -*- coding: utf-8 -*-
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
from   PyQt5 . QtGui                  import QColor
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
from   AITK . Calendars . Periode     import Periode
##############################################################################
from   . PurePlan import PurePlan as PurePlan
##############################################################################
class Plan                 ( PurePlan                                      ) :
  ############################################################################
  def __init__             ( self                                          ) :
    ##########################################################################
    super ( ) . __init__   (                                                 )
    ##########################################################################
    self . Actions         = {                                                 }
    self . Shortcuts       = {                                                 }
    self . Stacked         = None
    self . Mdi             = None
    self . statusMessage   = None
    self . statusBar       = None
    self . Ratio           = None
    self . VoiceWidget     = None
    self . progressManager = None
    self . Indicator       = None
    self . MyFunc          = None
    ##########################################################################
    return
  ############################################################################
  def __del__              ( self                                          ) :
    return
  ############################################################################
  def setStacked           ( self , stacked                                ) :
    self . Stacked = stacked
    return self . Stacked
  ############################################################################
  def getStacked           ( self                                          ) :
    return self . Stacked
  ############################################################################
  def setMdi               ( self , mdi                                    ) :
    self . Mdi = mdi
    return self . Mdi
  ############################################################################
  def getMdi               ( self                                          ) :
    return self . Mdi
  ############################################################################
  def addAction            ( self , Id , action                            ) :
    self . Actions [ Id ] = action
    return len             ( self . Actions                                  )
  ############################################################################
  def Action               ( self , Id                                     ) :
    if                     ( Id not in self . Actions                      ) :
      return None
    return self . Actions  [ Id                                              ]
  ############################################################################
  def hasAction            ( self , Id                                     ) :
    return                 ( Id in self . Actions                            )
  ############################################################################
  def connectAction              ( self , Id , method , enable = True      ) :
    ##########################################################################
    a   = self . Action          (        Id                                 )
    if                           ( a == None                               ) :
      return None
    ##########################################################################
    try                                                                      :
      a . triggered . disconnect (                                           )
    except                                                                   :
      pass
    ##########################################################################
    a   . triggered . connect    ( method                                    )
    a   . setEnabled             ( enable                                    )
    ##########################################################################
    return a
  ############################################################################
  def disableAction              ( self , Id                               ) :
    ##########################################################################
    a   = self . Action          (        Id                                 )
    if                           ( a == None                               ) :
      return None
    ##########################################################################
    try                                                                      :
      a . triggered . disconnect (                                           )
    except                                                                   :
      pass
    ##########################################################################
    a   . setEnabled             ( False                                     )
    ##########################################################################
    return
  ############################################################################
  def actionVisible   ( self , Id , visible                                ) :
    ##########################################################################
    a = self . Action (        Id                                            )
    if                ( a == None                                          ) :
      return None
    ##########################################################################
    a . setVisible    ( visible                                              )
    ##########################################################################
    return
  ############################################################################
  def nameAction      ( self , Id , name                                   ) :
    ##########################################################################
    a = self . Action (        Id                                            )
    if                ( a == None                                          ) :
      return None
    ##########################################################################
    a . setText       ( name                                                 )
    ##########################################################################
    return
  ############################################################################
  def disableAllAction             ( self                                  ) :
    ##########################################################################
    KEYs   = self . Actions . keys (                                         )
    for K in KEYs                                                            :
      ########################################################################
      self . disableAction         ( K                                       )
    ##########################################################################
    return
  ############################################################################
  def addShortcut           ( self , Id , shortcut                         ) :
    self . Shortcuts [ Id ] = shortcut
    return len              ( self . Shortcuts                               )
  ############################################################################
  def Shortcut              ( self , Id                                    ) :
    if                      ( Id not in self . Shortcuts                   ) :
      return None
    return self . Shortcuts [ Id                                             ]
  ############################################################################
  def hasShortcut           ( self , Id                                    ) :
    return                  ( Id in self . Shortcuts                         )
  ############################################################################
  def connectShortcut            ( self , Id , method                      ) :
    ##########################################################################
    s   = self . Shortcut        (        Id                                 )
    if                           ( s == None                               ) :
      return None
    ##########################################################################
    try                                                                      :
      s . activated . disconnect (                                           )
    except                                                                   :
      pass
    ##########################################################################
    s   . activated . connect    ( method                                    )
    ##########################################################################
    return s
  ############################################################################
  def disableShortcut            ( self , Id                               ) :
    ##########################################################################
    s   = self . Shortcut        (        Id                                 )
    if                           ( s == None                               ) :
      return None
    ##########################################################################
    try                                                                      :
      s . activated . disconnect (                                           )
    except                                                                   :
      pass
    ##########################################################################
    return
  ############################################################################
  def LinkVoice        ( self , func                                       ) :
    ##########################################################################
    if                 ( self . VoiceWidget == None                        ) :
      return
    ##########################################################################
    self . VoiceWidget . Execution = func
    ##########################################################################
    return
  ############################################################################
  def PrepareActions   ( self , parent = None                              ) :
    ##########################################################################
    ## s    = QShortcut   ( QKeySequence ( "Ins"                 ) , parent     )
    ## self . addShortcut ( "Insert" , s                                        )
    ##########################################################################
    ## s    = QShortcut   ( QKeySequence ( QKeySequence . Delete ) , parent     )
    ## self . addShortcut ( "Delete" , s                                        )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ## Progress Manager
  ############################################################################
  def Progress              ( self , Name , Format                         ) :
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return -1
    ##########################################################################
    r    = self . progressManager . Request ( Name , Format                  )
    self . skip                             ( 300                            )
    ##########################################################################
    return r
  ############################################################################
  def ProgressName          ( self , Id , Name                             ) :
    ##########################################################################
    if                      ( Id < 0                                       ) :
      return
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return
    ##########################################################################
    self . progressManager . setName ( Id , Name                             )
    ##########################################################################
    return
  ############################################################################
  def ProgressText          ( self , Id , message                          ) :
    ##########################################################################
    if                      ( Id < 0                                       ) :
      return
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return
    ##########################################################################
    self . progressManager . setMessage ( Id , message                       )
    ##########################################################################
    return
  ############################################################################
  def setProgress           ( self , Id , Format                           ) :
    ##########################################################################
    if                      ( Id < 0                                       ) :
      return
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return
    ##########################################################################
    self . progressManager . setFormat ( Id , Format                         )
    ##########################################################################
    return
  ############################################################################
  def setRange              ( self , Id , Min , Max                        ) :
    ##########################################################################
    if                      ( Id < 0                                       ) :
      return
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return
    ##########################################################################
    self . progressManager . setRange ( Id , Min , Max                       )
    ##########################################################################
    return
  ############################################################################
  def setFrequency          ( self , Id , cFmt , rFmt                      ) :
    ##########################################################################
    if                      ( Id < 0                                       ) :
      return
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return
    ##########################################################################
    self . progressManager . setFrequency ( Id , cFmt , rFmt                 )
    ##########################################################################
    return
  ############################################################################
  def Start                 ( self , Id , Value , Running                  ) :
    ##########################################################################
    if                      ( Id < 0                                       ) :
      return
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return
    ##########################################################################
    self . progressManager . Start ( Id , Value , Running                    )
    ##########################################################################
    return
  ############################################################################
  def Finish                ( self , Id                                    ) :
    ##########################################################################
    if                      ( Id < 0                                       ) :
      return
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return
    ##########################################################################
    self . progressManager . Finish ( Id                                     )
    ##########################################################################
    return
  ############################################################################
  def ProgressReady         ( self , Id , msecs = 1000                     ) :
    ##########################################################################
    if                      ( Id < 0                                       ) :
      return True
    ##########################################################################
    if                      ( self . progressManager in [ False , None ]   ) :
      return True
    ##########################################################################
    return self . progressManager . WaitForReady ( Id , msecs                )
  ############################################################################
  ## Progress indicator
  ############################################################################
  def StartBusy             ( self                                         ) :
    ##########################################################################
    self . RealStart        (                                                )
    ##########################################################################
    return
  ############################################################################
  def StopBusy              ( self                                         ) :
    ##########################################################################
    self . RealStop         (                                                )
    ##########################################################################
    return
  ############################################################################
  def RealStart             ( self                                         ) :
    ##########################################################################
    if                      ( self . statusBar in [ False , None ]         ) :
      return
    ##########################################################################
    if                      ( self . Indicator in [ False , None ]         ) :
      ########################################################################
      blue = QColor         ( 0 , 0 , 255                                    )
      ########################################################################
      self . Indicator = ProgressIndicator  ( self . statusBar , self.MyFunc )
      self . Indicator . setColor           ( blue                           )
      self . Indicator . setAnimationDelay  ( 100                            )
      self . statusBar . addPermanentWidget ( self . Indicator               )
      self . Indicator . show               (                                )
    ##########################################################################
    self . Indicator . startAnimation ( )
    ##########################################################################
    return
  ############################################################################
  def RealStop              ( self                                         ) :
    ##########################################################################
    if                      ( self . Indicator in [ False , None ]         ) :
      return
    ##########################################################################
    cnt = self . Indicator . stopAnimation (                                 )
    if                                     ( cnt > 0                       ) :
      return
    ##########################################################################
    self . Indicator . deleteLater         (                                 )
    self . Indicator = None
    ##########################################################################
    return
##############################################################################

"""

class Q_COMPONENTS_EXPORT Plan : public PurePlan
{
  public:

    FullSettings             settings        ;
    FullSettings             site            ;
    int                      dpi             ;
    Screen                   screen          ;
    QMap<int,Screen       *> Screens         ;
    Paper                    paper           ;
    ICONs                    icons           ;
    Font                     font            ;
    FONTs                    fonts           ;
    QColors                  colors          ;
    Actions                  actions         ;
    QMap<int,QActionGroup *> actiongroups    ;
    NamedActions             menuitems       ;
    Widgets                  widgets         ;
    MENUs                    menus           ;
    QStatusBar             * status          ;
    DebugView              * debugWidget     ;
    ControlPad             * pad             ;
    XmlRpcLogHandler       * xmllog          ;
    XmlRpcErrorHandler     * xmlerr          ;
    RpcLogHandler          * rpclog          ;
    RpcErrorHandler        * rpcerr          ;
    MachineProfiler        * profiler        ;
    CvClassifiers            classifiers     ;
    bool                     Expiration      ;
    QDateTime                Trial           ;

    explicit Plan             (void) ;
    virtual ~Plan             (void) ;

    virtual int type (void) const { return GUI ; }

    virtual bool Initialize    (void) ;
    void      shutdown         (void) ;

    int       Port             (QString setting,QString username,QString application,int DefaultPort) ;

    // Network service
    bool      bindService      (QString hostname,int port) ;

    void      setWidget        (QWidget     * parent) ;
    void      setMain          (QMainWindow * window) ;

    // Fonts
    Font &    selectFont       (int FontId                 ) ;
    bool      setFont          (QFont   & font             ) ;
    void      setFont          (QWidget * widget,int FontId) ;
    void      setFont          (QObject * widget           ) ;

    // Menus
    int       addMenu          (int Id,QMenu * menu  ) ;
    QMenu   * Menu             (int Id) ;

    int       addWidget        (int Id,QWidget * widget) ;
    QWidget * Widget           (int Id) ;

    // Screen settings
    bool    loadScreen         (QString scope        ) ;
    bool    saveScreen         (QString scope        ) ;

    QPointF toCentimeter       (QPoint  point        ) ;
    QPoint  toScreen           (QPointF cmPoint      ) ;
    QRectF  toCentimeter       (QRect   rect         ) ;
    QRect   toScreen           (QRectF  cmRect       ) ;

    // Paper settings
    bool       loadPaper       (QString table        ) ;
    QTransform toPaper         (int DPI = 0          ) ;

    QSizeF  PaperPixels        (QString name   ,int DPI,int Direction);
    QPointF toCentimeter       (QPointF point  ,int DPI) ;
    QRectF  toCentimeter       (QRectF  rect   ,int DPI) ;
    QPointF toPaper            (QPointF cmPoint,int DPI) ;
    QPointF ScreenToPaper      (QPoint  point  ,int DPI) ;
    QPoint  PaperToScreen      (QPointF point  ,int DPI) ;

    // Events
    void    setExpiration      (QString timestring   ) ;
    virtual void processEvents (void                 ) ;
    virtual void showMessage   (QString message      ) ;

    // Debug
    virtual void Debug         (QString message);
    virtual void Debug         (int verbose,QString message);

    virtual void Notify        (QString sound,QString message) ;

    // GUI
    QComboBox    * ComboBox    (QWidget * parent = NULL);
    QTreeWidget  * TreeWidget  (QWidget * parent = NULL);
    QProgressBar * Progress    (QString format = "");

    virtual void * Percentage  (QString format = "") ;
    virtual void   setRange    (void * bar,int Min,int Max) ;
    virtual void   setValue    (void * bar,int value) ;
    virtual void   Finish      (void * bar) ;

    // Icon Manager
    void  addIcon              (int ObjectType,int ObjectId,int State,QIcon icon) ;
    QIcon Icon                 (int ObjectType,int ObjectId,int State,QIcon defaultIcon = QIcon()) ;

    void DetachControl         (QWidget * widget) ;
    void addControl            (QString name,QWidget * widget,QWidget * parent) ;
    void addControl            (QString name,QWidget * widget,QObject * parent) ;

    bool setManipulator        (QString key,int size) ;
    bool setProfiler           (QString key) ;
    bool Profiling             (void) ;

} ;

N::Plan:: Plan     (void)
        : PurePlan (    )
{
  SystemPlanPacket * pp      = new SystemPlanPacket ( )                  ;
  pp -> pp                   = this                                      ;
  Native                     = (Settings *)&settings                     ;
  Remote                     = (Settings *)&site                         ;
  status                     = NULL                                      ;
  debugWidget                = NULL                                      ;
  progressManager            = NULL                                      ;
  indicator                  = NULL                                      ;
  pad                        = NULL                                      ;
  Ears                       = NULL                                      ;
  Expiration                 = false                                     ;
  xmllog                     = XmlRpcLogHandler   :: getLogHandler   ( ) ;
  xmlerr                     = XmlRpcErrorHandler :: getErrorHandler ( ) ;
  rpclog                     = new RpcLogHandler   ( this )              ;
  rpcerr                     = new RpcErrorHandler ( this )              ;
  profiler                   = NULL                                      ;
  Variables [ "SystemPlan" ] = VoidVariant ( pp )                        ;
  ////////////////////////////////////////////////////////////////////////
  ProgressReporter::setVirtual ( this )                                  ;
}

N::Plan::~Plan(void)
{
}

bool N::Plan::Initialize(void)
{
  PurePlan::Initialize() ;

  ConnectSQL          ( SC , *(settings.SQL)           )                       ;

  settings.beginGroup("System")                                                ;
  if (settings.contains(SC,"FontFamily"))                                      {
    font.setFamily                                                             (
      QString::fromUtf8 ( settings.value(SC,"FontFamily").toByteArray()   )  ) ;
  }                                                                            ;
  if (settings.contains(SC,"FontSize"))                                        {
    font.setPointSizeF  ( settings.value(SC,"FontSize").toDouble() )           ;
  }                                                                            ;
  settings.endGroup  (        )                                                ;

  DisconnectSQL       ( SC                                                   ) ;

  loadScreen ( "Monitor" ) ;

  XmlRpcLogHandler::setVerbosity(Verbose) ;

  return (sql.isValid()) ;
}

void N::Plan::shutdown(void)
{
  QStringList MS = Manipulators . keys ( )                      ;
  QString     ms                                                ;
  foreach ( ms , MS ) delete Manipulators [ ms ]                ;
  Manipulators . clear    ( )                                   ;
  Request      . Alive = false                                  ;
  RPC          . Stop     ( )                                   ;
  Mouth        . Stop     ( )                                   ;
  Audio        . Shutdown ( )                                   ;
  Recorder     . Stop     ( )                                   ;
  if ( NotNull ( debugWidget ) )                                {
    debugWidget -> Stop        ( )                              ;
    debugWidget -> deleteLater ( )                              ;
    debugWidget  = NULL                                         ;
  }                                                             ;
  if ( NotNull ( progressManager ) )                            {
    progressManager -> Shutdown    ( )                          ;
    progressManager -> deleteLater ( )                          ;
    progressManager  = NULL                                     ;
  }                                                             ;
  if ( NotNull ( Ears  ) )                                      {
//    Ears -> Stop ( )                                            ;
  }                                                             ;
  if ( NotNull ( Knock ) )                                      {
    Knock -> Interpreter -> setParameter ( "Deletion" , true  ) ;
    Knock -> Interpreter -> setParameter ( "Running"  , false ) ;
    Knock  = NULL                                               ;
  }                                                             ;
  if ( NotNull ( House ) )                                      {
    House -> Interpreter -> setParameter ( "Deletion" , true  ) ;
    House -> Interpreter -> setParameter ( "Running"  , false ) ;
    House  = NULL                                               ;
  }                                                             ;
  if ( NotNull ( Ftp ) )                                        {
//      N::printf ( "Has FTP" , true , true ) ;
  }                                                             ;
//  parallel = NULL                                               ;
//  Destructor ( )                                                ;
}

int N::Plan::Port(QString setting,QString username,QString application,int DefaultPort)
{
  Settings Prefetch                                            ;
  Prefetch.Mode     = "SQL"                                    ;
  Prefetch.Username = username                                 ;
  Prefetch.SQL      = new Sql()                                ;
  Prefetch.SQL     -> SqlMode = "SQLITE"                       ;
  Prefetch.SQL     -> dbName  = Root.absoluteFilePath(setting) ;
  QFile F(Prefetch.SQL -> dbName)                              ;
  bool exists = F.exists()                                     ;
  if (exists)                                                  {
    Prefetch.Initialize()                                      ;
    Prefetch.beginGroup("Port")                                ;
    if (Prefetch.contains(application))                        {
      DefaultPort = Prefetch.value(application).toInt()        ;
    }                                                          ;
    Prefetch.endGroup()                                        ;
  } else                                                       {
    delete Prefetch.SQL                                        ;
    Prefetch.SQL = NULL                                        ;
  }                                                            ;
  return DefaultPort                                           ;
}

void N::Plan::setWidget(QWidget * parent)
{
  #ifdef CIOSDEBUG
  qDebug ( "N::Plan::setWidget" ) ;
  #endif
  settings . setParent ( parent         ) ;
  site     . setParent ( parent         ) ;
  Audio    . setParent ( parent         ) ;
//  Mouth    . setParent ( parent         ) ;
  font     = Font      ( parent->font() ) ;
}

void N::Plan::setMain(QMainWindow * window)
{
  status    = window -> statusBar ( )                 ;
  font      = Font              ( window -> font( ) ) ;
  Neighbors = new CiosNeighbors ( window            ) ;
}

bool N::Plan::setFont(QFont & f)
{
  ConnectSQL         ( SC , *(settings.SQL)                ) ;
  settings.beginGroup( "System"                            ) ;
  settings.setValue  ( SC,"FontFamily",f.family().toUtf8() ) ;
  settings.setValue  ( SC,"FontSize"  ,f.pointSizeF()      ) ;
  settings.endGroup  (                                     ) ;
  DisconnectSQL      ( SC                                  ) ;
  font =  Font       ( f                                   ) ;
  return true                                                ;
}

void N::Plan::setFont(QWidget * widget,int FontId)
{
  if (IsNull(widget)) return     ;
  if (fonts.contains(FontId))    {
    Font f = fonts[FontId]       ;
    f.setScreen(screen)          ;
    widget->setFont(f.toQFont()) ;
  }                              ;
}

void N::Plan::setFont(QObject * widget)
{
  if (IsNull(widget)) return               ;
  #define QCAST(O,N)                       \
    O * N = qobject_cast<O *>(widget)
  #define QFONT(W,F)                       \
    if (NotNull(W)) setFont(W,F); else
  QCAST(QMainWindow     ,qmainw          ) ;
  QCAST(QMenuBar        ,qmenub          ) ;
  QCAST(QMenu           ,qmenuw          ) ;
  QCAST(QStackedWidget  ,qstack          ) ;
  QCAST(QMdiArea        ,qmdiar          ) ;
  QCAST(QTextEdit       ,qtexte          ) ;
  QCAST(QTreeWidget     ,qtreew          ) ;
  QCAST(QTreeView       ,qtreev          ) ;
  QCAST(QStatusBar      ,qstatu          ) ;
  QCAST(QComboBox       ,qcombo          ) ;
  QCAST(QListView       ,qlistv          ) ;
  QCAST(QDockWidget     ,qdockw          ) ;
  QCAST(QHeaderView     ,qheade          ) ;
  QCAST(QTableView      ,qtable          ) ;
  QCAST(QTabWidget      ,qtabwt          ) ;
  QCAST(QTabBar         ,qtabar          ) ;
  QCAST(QLabel          ,qlabel          ) ;
  QCAST(QCheckBox       ,qcheck          ) ;
  QCAST(QProgressBar    ,qproge          ) ;
  QCAST(QAbstractButton ,qabutt          ) ;
  QCAST(QAbstractSpinBox,qaspin          ) ;
  QCAST(QsciScintilla   ,qscita          ) ;
  QFONT(qmainw,N::Fonts::Default         )
  QFONT(qmenub,N::Fonts::Menu            )
  QFONT(qmenuw,N::Fonts::Menu            )
  QFONT(qstack,N::Fonts::ToolTip         )
  QFONT(qmdiar,N::Fonts::ToolTip         )
  QFONT(qtexte,N::Fonts::Editor          )
  QFONT(qtreew,N::Fonts::Tree            )
  QFONT(qtreev,N::Fonts::TreeView        )
  QFONT(qstatu,N::Fonts::Status          )
  QFONT(qcombo,N::Fonts::ComboBox        )
  QFONT(qlistv,N::Fonts::ListView        )
  QFONT(qdockw,N::Fonts::ListView        )
  QFONT(qheade,N::Fonts::ListView        )
  QFONT(qtabwt,N::Fonts::ListView        )
  QFONT(qtabar,N::Fonts::ListView        )
  QFONT(qtable,N::Fonts::TableView       )
  QFONT(qlabel,N::Fonts::Label           )
  QFONT(qcheck,N::Fonts::CheckBox        )
  QFONT(qproge,N::Fonts::Progress        )
  QFONT(qabutt,N::Fonts::Button          )
  QFONT(qaspin,N::Fonts::Spin            )
  QFONT(qscita,N::Fonts::Editor          )
  //////////////////////////////////////////
  {
    QWidget * wt                           ;
    wt = qobject_cast<QWidget *>(widget)   ;
    setFont ( wt , N::Fonts::Default )     ;
  }                                        ;
  //////////////////////////////////////////
  if ( NotNull(qtabwt))                    {
    if ( NotNull(qtabwt->tabBar()) )       {
      setFont ( qtabwt->tabBar()           ,
                N::Fonts::ListView       ) ;
    }                                      ;
  }                                        ;
  //////////////////////////////////////////
  QObjectList QOList                       ;
  QObject *   olist                        ;
  QOList = widget->children()              ;
  if (QOList.count()>0)                    {
    foreach (olist,QOList) setFont(olist)  ;
  }                                        ;
}

N::Font & N::Plan::selectFont(int FontId)
{
  if (fonts.contains(FontId)) return fonts[FontId] ;
  return font                                      ;
}

int N::Plan::addMenu(int Id,QMenu * menu)
{
  menus[Id] = menu     ;
  return menus.size() ;
}

QMenu * N::Plan::Menu(int Id)
{
  nKickOut(!menus.contains(Id),NULL) ;
  return menus[Id]                   ;
}

int N::Plan::addWidget(int Id,QWidget * widget)
{
  widgets [Id] = widget    ;
  return widgets . count() ;
}

QWidget * N::Plan::Widget(int Id)
{
  if (!widgets.contains(Id)) return NULL ;
  return widgets [Id]                    ;
}

bool N::Plan::loadScreen(QString scope)
{
  Screen m;
  ConnectSQL           ( SC , *(settings.SQL)                              ) ;
  settings.beginGroup  (scope                                              ) ;
  if (settings.contains(SC,"MonitorWidth"   )) m.MonitorSize.setWidth (settings.value(SC,"MonitorWidth"       ).toInt   ()) ;
  if (settings.contains(SC,"MonitorHeight"  )) m.MonitorSize.setHeight(settings.value(SC,"MonitorHeight"      ).toInt   ()) ;
  if (settings.contains(SC,"MonitorWidthCM" )) screen.WidthInCentimeter  = settings.value(SC,"MonitorWidthCM" ).toDouble()  ;
  if (settings.contains(SC,"MonitorHeightCM")) screen.HeightInCentimeter = settings.value(SC,"MonitorHeightCM").toDouble()  ;
  if (settings.contains(SC,"WidthPixels"    )) m.WidthPixels             = settings.value(SC,"WidthPixels"    ).toInt   ()  ;
  if (settings.contains(SC,"WidthLength"    )) m.WidthLength             = settings.value(SC,"WidthLength"    ).toInt   ()  ;
  if (settings.contains(SC,"HeightPixels"   )) m.HeightPixels            = settings.value(SC,"HeightPixels"   ).toInt   ()  ;
  if (settings.contains(SC,"HeightLength"   )) m.HeightLength            = settings.value(SC,"HeightLength"   ).toInt   ()  ;
  settings.endGroup    (                                                   ) ;
  DisconnectSQL        ( SC                                                ) ;
  screen = m                                                                 ;
  return false                                                               ;
}

bool N::Plan::saveScreen(QString scope)
{
  QRect R = qApp->desktop()->screenGeometry()                                    ;
  ConnectSQL          ( SC , *(settings.SQL)                                   ) ;
  settings.beginGroup ( scope                                                  ) ;
  settings.setValue   ( SC,"MonitorWidth"    , screen.MonitorSize.width ()     ) ;
  settings.setValue   ( SC,"MonitorHeight"   , screen.MonitorSize.height()     ) ;
  settings.setValue   ( SC,"MonitorWidthCM"  , screen.WidthInCentimeter        ) ;
  settings.setValue   ( SC,"MonitorHeightCM" , screen.HeightInCentimeter       ) ;
  settings.setValue   ( SC,"Width"           , R.width ()                      ) ;
  settings.setValue   ( SC,"Height"          , R.height()                      ) ;
  settings.setValue   ( SC,"ScreenWidth"     , screen.widthLength (R.width ()) ) ;
  settings.setValue   ( SC,"ScreenHeight"    , screen.heightLength(R.height()) ) ;
  settings.setValue   ( SC,"WidthPixels"     , screen.WidthPixels              ) ;
  settings.setValue   ( SC,"WidthLength"     , screen.WidthLength              ) ;
  settings.setValue   ( SC,"HeightPixels"    , screen.HeightPixels             ) ;
  settings.setValue   ( SC,"HeightLength"    , screen.HeightLength             ) ;
  settings.endGroup   (                                                        ) ;
  DisconnectSQL       ( SC                                                     ) ;
  return false                                                                   ;
}

QPointF N::Plan::toCentimeter(QPoint point)
{
  qreal x = point.x()      ;
  qreal y = point.y()      ;
  x *= screen.WidthLength  ;
  x /= screen.WidthPixels  ; // mm
  x /= 10                  ; // cm
  y *= screen.HeightLength ;
  y /= screen.HeightPixels ; // mm
  y /= 10                  ; // cm
  return QPointF(x,y)      ;
}

QPoint N::Plan::toScreen(QPointF cmPoint)
{
  qreal x = cmPoint.x()    ;
  qreal y = cmPoint.y()    ;
  x *= 10                  ;
  y *= 10                  ;
  x *= screen.WidthPixels  ;
  x /= screen.WidthLength  ;
  y *= screen.HeightPixels ;
  y /= screen.HeightLength ;
  return QPoint(x,y)       ;
}

QRectF N::Plan::toCentimeter(QRect rect)
{
  QPoint  p1(rect.left(),rect.top())         ;
  QPoint  p2(rect.width(),rect.height())     ;
  QPointF P1 = toCentimeter(p1)              ;
  QPointF P2 = toCentimeter(p2)              ;
  return QRectF(P1.x(),P1.y(),P2.x(),P2.y()) ;
}

QRectF N::Plan::toCentimeter(QRectF rect,int DPI)
{
  QPointF LT = rect . topLeft     () ;
  QPointF RB = rect . bottomRight () ;
  LT = toCentimeter ( LT , DPI )     ;
  RB = toCentimeter ( RB , DPI )     ;
  return QRectF     ( LT , RB  )     ;
}

QRect N::Plan::toScreen(QRectF cmRect)
{
  QPointF P1(cmRect.left(),cmRect.top())     ;
  QPointF P2(cmRect.width(),cmRect.height()) ;
  QPoint  p1 = toScreen(P1)                  ;
  QPoint  p2 = toScreen(P2)                  ;
  return QRect(p1.x(),p1.y(),p2.x(),p2.y())  ;
}

bool N::Plan::loadPaper(QString table)
{
  return paper.load(sql,sql.Name(table)) ;
}

QTransform N::Plan::toPaper(int d)
{
  if (dpi==0) dpi = d                    ;
  QTransform T                           ;
  T.reset()                              ;
  qreal sx = screen.widthPixels  (200  ) ;
  qreal sy = screen.heightPixels (200  ) ;
  int   px = paper .Pixels       (d,200) ;
  int   py = paper .Pixels       (d,200) ;
  if (px<=0) return T                    ;
  if (py<=0) return T                    ;
  sx /= px                               ;
  sy /= py                               ;
  return T.scale(sx,sy)                  ;
}

QSizeF N::Plan::PaperPixels(QString name,int DPI,int d)
{
  QSizeF S                                   ;
  qreal  w = paper . WidthPixels  (name,DPI) ;
  qreal  h = paper . HeightPixels (name,DPI) ;
  if (d==Qt::Vertical)                       {
    S . setWidth  (w)                        ;
    S . setHeight (h)                        ;
  } else                                     {
    S . setWidth  (h)                        ;
    S . setHeight (w)                        ;
  }                                          ;
  return S                                   ;
}

QPointF N::Plan::toCentimeter(QPointF point,int dpi)
{
  qreal x = point.x() ;
  qreal y = point.y() ;
  x *= 254            ;
  x /= dpi            ;
  x /= 100            ;
  y *= 254            ;
  y /= dpi            ;
  y /= 100            ;
  return QPointF(x,y) ;
}

QPointF N::Plan::toPaper(QPointF cmPoint,int dpi)
{
  qreal x = cmPoint . x () ;
  qreal y = cmPoint . y () ;
  x *= dpi                 ;
  x *= 100                 ;
  x /= 254                 ;
  y *= dpi                 ;
  y *= 100                 ;
  y /= 254                 ;
  return QPointF(x,y)      ;
}

QPointF N::Plan::ScreenToPaper(QPoint point,int dpi)
{
  QPointF cm = toCentimeter(point) ;
  return toPaper(cm,dpi)           ;
}

QPoint N::Plan::PaperToScreen(QPointF point,int dpi)
{
  QPointF cm = toCentimeter(point,dpi) ;
  return toScreen(cm)                  ;
}

bool N::Plan::bindService(QString hostname,int port)
{
  if (   Request . Exists ( hostname , port ) ) return false ;
  if ( ! RPC     . Start  (            port ) ) return false ;
  return true                                                ;
}

void N::Plan::setExpiration(QString timestring)
{
  Trial = QDateTime::fromString(timestring,"yyyy/MM/dd hh:mm:ss") ;
}

void N::Plan::processEvents(void)
{
  if (IsNull(qApp)) return                      ;
  if (Expiration) /* Expiration lock up code */ {
    QDateTime NT = QDateTime::currentDateTime() ;
    int       ds = NT.secsTo(Trial)             ;
    if (ds<0)                                   {
      for (int i=0;i<100000000;i++)             {
        Time :: sleep ( 1 )                     ;
      }                                         ;
    }                                           ;
  }                                             ;
  #ifdef Q_OS_IOS
  qApp -> processEvents    ()                   ;
  #else
  if (!qApp->hasPendingEvents()) return         ;
  qApp -> processEvents    ()                   ;
  qApp -> sendPostedEvents ()                   ;
  qApp -> flush            ()                   ;
  #endif
}

void N::Plan::showMessage(QString message)
{
  if (IsNull(status)) return   ;
  status->showMessage(message) ;
}

QComboBox * N::Plan::ComboBox(QWidget * parent)
{
  N::ComboBox * combo = new N::ComboBox(parent,this) ;
  this -> setFont ( combo )                          ;
  return (QComboBox *)combo                          ;
}

QTreeWidget * N::Plan::TreeWidget(QWidget * parent)
{
  N::TreeWidget * tree = new N::TreeWidget(parent,this) ;
  this -> setFont ( tree )                              ;
  return (QTreeWidget *)tree                            ;
}

QProgressBar * N::Plan::Progress(QString format)
{
  if (IsNull(status)) return NULL          ;
  QProgressBar * P    = new QProgressBar() ;
  QFont          f    = status->font()     ;
  QSize          s    = status->size()     ;
  QSize          m(s.width()/6,s.height()) ;
  if (f.pixelSize()>0)                     {
    m   .setHeight    (f.pixelSize()-2)    ;
    f   .setPixelSize (f.pixelSize()-2)    ;
    P  ->setFont      (f              )    ;
  }                                        ;
  P -> setMinimumSize ( m )                ;
  P -> setMaximumSize ( m )                ;
  if (format.length()<=0)                  {
    P->setTextVisible(false)               ;
  } else                                   {
    P->setTextVisible(true  )              ;
    P->setFormat     (format)              ;
  }                                        ;
  status -> addPermanentWidget ( P )       ;
  P      -> show               (   )       ;
  return P                                 ;
}

void * N::Plan::Percentage(QString format)
{
  return (void *)Progress(format) ;
}

void N::Plan::setRange(void * bar,int Min,int Max)
{
  if (IsNull(bar)) return                ;
  QProgressBar * p = (QProgressBar *)bar ;
  p->setRange(Min,Max)                   ;
}

void N::Plan::setValue(void * bar,int value)
{
  if (IsNull(bar)) return                ;
  QProgressBar * p = (QProgressBar *)bar ;
  p->setValue(value)                     ;
}

void N::Plan::Finish(void * bar)
{
  if (IsNull(bar)) return                ;
  QProgressBar * p = (QProgressBar *)bar ;
  p -> hide        ( )                   ;
  p -> deleteLater ( )                   ;
}

void N::Plan::Debug(QString message)
{
  #ifdef Q_OS_IOS
  qDebug ( message.toUtf8().constData() ) ;
  #elif defined(Q_OS_ANDROID)
  qDebug ( message.toUtf8().constData() ) ;
  #else
  if (IsNull(debugWidget)) return;
  debugWidget->Append(message);
  if (MaxLogs<0) return ;
  if (debugWidget->document()->lineCount()>MaxLogs) debugWidget->clear() ;
  #endif
}

void N::Plan::Debug(int verbose,QString message)
{
  #ifdef Q_OS_IOS
  if (verbose>Verbose) return;
  qDebug ( message.toUtf8().constData() ) ;
  #elif defined(Q_OS_ANDROID)
  if (verbose>Verbose) return;
  qDebug ( message.toUtf8().constData() ) ;
  #else
  if (IsNull(debugWidget)) return;
  if (verbose>Verbose) return;
  debugWidget->Append(message);
  if (MaxLogs<0) return ;
  if (debugWidget->document()->lineCount()>MaxLogs) debugWidget->clear() ;
  #endif
}

void N::Plan::Notify(QString sound,QString message)
{
  if ( sound . length ( ) > 0 ) Play ( sound ) ;
  if ( message . length ( ) > 0 )              {
    Talk        ( message )                    ;
    Debug       ( message )                    ;
    showMessage ( message )                    ;
  }                                            ;
}

void N::Plan::addIcon(int ObjectType,int ObjectId,int State,QIcon icon)
{
  SUID uuid = 0      ;
  uuid  = ObjectType ;
  uuid *= 10000      ;
  uuid += ObjectId   ;
  uuid *= 1000       ;
  uuid += State      ;
  icons[uuid] = icon ;
}

QIcon N::Plan::Icon(int ObjectType,int ObjectId,int State,QIcon defaultIcon)
{
  QIcon icon = defaultIcon  ;
  SUID uuid = 0             ;
  uuid  = ObjectType        ;
  uuid *= 10000             ;
  uuid += ObjectId          ;
  uuid *= 1000              ;
  uuid += State             ;
  if (icons.contains(uuid)) {
    icon = icons[uuid]      ;
  }                         ;
  return icon               ;
}

void N::Plan::DetachControl(QWidget * widget)
{
  if (IsNull(pad)) return  ;
  pad -> Detach ( widget ) ;
}

void N::Plan::addControl(QString name,QWidget * widget,QWidget * parent)
{
  if (IsNull(pad)) return                      ;
  pad -> addControl ( name , widget , parent ) ;
}

void N::Plan::addControl(QString name,QWidget * widget,QObject * parent)
{
  if (IsNull(pad)) return                      ;
  pad -> addControl ( name , widget , parent ) ;
}

bool N::Plan::setManipulator(QString key,int size)
{
  if ( Manipulators . contains ( key ) ) return true ;
  DataManipulator * dm = new DataManipulator ( )     ;
  Manipulators [ key ] = dm                          ;
  dm -> setEnabled ( "Create" , true )               ;
  dm -> Manager    ( key      , size )               ;
  return true                                        ;
}

bool N::Plan::setProfiler(QString key)
{
  if ( ! Manipulators . contains ( key ) ) return false                      ;
  DataManipulator * dm = Manipulators [ key ]                                ;
  if ( NULL == dm                        ) return false                      ;
  ////////////////////////////////////////////////////////////////////////////
  if ( dm -> Mount ( "Machine" , N::MachineProfiler::sizeHint ( ) ) )        {
    if ( dm -> isCreated ( "Machine" ) ) dm -> Fill ( "Machine" , 0 )        ;
  } else return false                                                        ;
  ////////////////////////////////////////////////////////////////////////////
  QtCUDA::Initialize ( )                                                     ;
  profiler  = new MachineProfiler ( NULL )                                   ;
  profiler -> Data . Controller = &canContinue                               ;
  profiler -> personality       = personality                                ;
  ////////////////////////////////////////////////////////////////////////////
  void * pp = dm -> Memory ( "Machine" )                                     ;
  int    ss = dm -> Size   ( "Machine" )                                     ;
  profiler -> setData  ( pp     , ss          )                              ;
  profiler -> setValue ( "Name" , Application )                              ;
  ////////////////////////////////////////////////////////////////////////////
  if ( dm -> Mount ( "CPU" , "Machine" , CPU::Profiler::sizeHint ( ) ) )     {
    if ( dm -> isCreated ( "CPU" , "Machine" ) )                             {
      dm -> Fill ( "CPU" , "Machine" , 0 )                                   ;
    }                                                                        ;
    void * p = dm -> Memory ( "CPU" , "Machine" )                            ;
    int    s = dm -> Size   ( "CPU" , "Machine" )                            ;
    profiler -> profiler . setData  ( p , s                                ) ;
    profiler -> profiler . setValue ( "Record" , dm -> isEnabled("Create") ) ;
    profiler -> profiler . setValue ( "Flush"  , dm -> isEnabled("Create") ) ;
    profiler -> profiler . setValue ( "Path"   , Temporary("CPU")          ) ;
    profiler -> profiler . setValue ( "Name"   , Hostname                  ) ;
  }                                                                          ;
  ////////////////////////////////////////////////////////////////////////////
  if ( dm -> Create ( "CPU" , Application , CPU::Profiler::sizeHint ( ) ) )  {
    if ( dm -> isCreated ( "CPU" , Application ) )                           {
      dm -> Fill ( "CPU" , Application , 0 )                                 ;
    }                                                                        ;
    void * p = dm -> Memory ( "CPU" , Application )                          ;
    int    s = dm -> Size   ( "CPU" , Application )                          ;
    profiler -> self . setData  ( p , s                      )               ;
    profiler -> self . setValue ( "Flush" , true             )               ;
    profiler -> self . setValue ( "Path"  , Temporary("CPU") )               ;
    profiler -> self . setValue ( "Name"  , Application      )               ;
  }                                                                          ;
  ////////////////////////////////////////////////////////////////////////////
  return true                                                                ;
}

bool N::Plan::Profiling(void)
{
  if ( NULL == profiler                             ) return false ;
  if ( profiler -> value ( "Running" ) . toBool ( ) ) return true  ;
  profiler -> Data . Controller = & canContinue                    ;
  profiler -> startup ( )                                          ;
  return true                                                      ;
}

"""
