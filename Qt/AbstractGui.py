# -*- coding: utf-8 -*-
##############################################################################
## GUI抽象介面
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
##############################################################################
import mysql . connector
from   mysql . connector              import Error
##############################################################################
import AITK
from   AITK . Database  . Query       import Query
from   AITK . Database  . Connection  import Connection
from   AITK . Database  . Pair        import Pair
from   AITK . Database  . Columns     import Columns
##############################################################################
from   AITK . Calendars . StarDate    import StarDate
##############################################################################
class AbstractGui        (                                                 ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    NOW                 = StarDate (                                         )
    NOW  . Now           (                                                   )
    ##########################################################################
    self . Locality        = 1002
    self . Prepared        = False
    self . DB              = { }
    self . Settings        = { }
    self . Translations    = { }
    self . Tables          = { }
    self . Gui             = None
    self . focusState      = False
    self . CreatedDateTime = NOW . Stardate
    self . Speaker         = None
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
  ############################################################################
  def isPrepared         ( self                                            ) :
    return self . Prepared
  ############################################################################
  def setPrepared        ( self , prepared                                 ) :
    self . Prepared = prepared
    return self . Prepared
  ############################################################################
  def getLocality        ( self                                            ) :
    return self . Locality
  ############################################################################
  def setLocality        ( self , locality                                 ) :
    ##########################################################################
    self . Locality = locality
    ##########################################################################
    return self . Locality
  ############################################################################
  def Go                    ( self , func , arguments = ( )                ) :
    ##########################################################################
    if                      ( func == None                                 ) :
      return None
    ##########################################################################
    th = threading . Thread ( target = func , args = arguments               )
    th . start              (                                                )
    ##########################################################################
    return th
  ############################################################################
  def Initialize         ( self , widget = None                            ) :
    ##########################################################################
    self . Gui          = widget
    ##########################################################################
    return
  ############################################################################
  def focusIn            ( self , event                                    ) :
    ##########################################################################
    if                   ( event . gotFocus ( )                            ) :
      if                 ( self  . FocusIn  ( )                            ) :
        ######################################################################
        event . accept   (                                                   )
        self  . focusState = True
        ######################################################################
        return True
    ##########################################################################
    return False
  ############################################################################
  def focusOut           ( self , event                                    ) :
    ##########################################################################
    if                   ( event . lostFocus ( )                           ) :
      if                 ( self  . FocusOut  ( )                           ) :
        ######################################################################
        event . accept   (                                                   )
        self  . focusState = False
        ######################################################################
        return True
    ##########################################################################
    return False
  ############################################################################
  def FocusIn                 ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def FocusOut                ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def ConnectDB          ( self                                            ) :
    ##########################################################################
    DB = Connection      (                                                   )
    if                   ( not DB . ConnectTo ( self . DB )                ) :
      return None
    DB . Prepare         (                                                   )
    ##########################################################################
    return DB
  ############################################################################
  def setSpeaker         ( self , speaker                                  ) :
    self . Speaker = speaker
    return
  ############################################################################
  def canSpeak           ( self                                            ) :
    return               ( self . Speaker != None                            )
  ############################################################################
  def Talk               ( self , message , locality                       ) :
    ##########################################################################
    if                   ( self . Speaker == None                          ) :
      return
    ##########################################################################
    LC   = ""
    MAPS =               { 1001 : "en-US"                                    ,
                           1002 : "zh-TW"                                    ,
                           1003 : "zh-CN"                                    ,
                           1004 : "zh-TW"                                    ,
                           1005 : "zh-TW"                                    ,
                           1006 : "jp-JP"                                    ,
                           1007 : "fr-FR"                                    ,
                           1008 : "de-DE"                                    ,
                           1009 : "es-ES"                                    ,
                           1010 : "ru-RU"                                    }
    ##########################################################################
    if ( ( locality >= 1001 ) and ( locality <= 1010 ) )                     :
      LC = MAPS          [ locality                                          ]
    ##########################################################################
    self . Speaker       ( message , LC                                      )
    ##########################################################################
    return
##############################################################################


"""


bool getAbstractStopable(QVariant pointer) ;
bool setAbstractStopable(QVariant pointer,bool stopable) ;

class Q_COMPONENTS_EXPORT AbstractGui
{
  public:

    typedef enum          {
      DesktopGui = 300001 ,
      PadGui     = 300002 ,
      PhoneGui   = 300003 }
      GuiOperateMethod    ;

    typedef enum                 {
      GuiLeftButton   =   100001 ,
      GuiRightButton  =   100002 ,
      GuiMiddleButton =   100003 ,
      GuiShift        =   100004 ,
      GuiControl      =   100005 ,
      GuiAlt          =   100006 ,
      GuiMeta         =   100007 ,
      GuiResize       =   100101 ,
      GuiPainted      =   100102 ,
      GuiTap          =   100201 ,
      GuiTapHold      =   100202 ,
      GuiPan          =   100203 ,
      GuiPinch        =   100204 ,
      GuiSwipe        =   100205 ,
      GuiNotEvent     =   199999 }
      InputStatus                ; // For decision actions

    typedef enum                 {
      DropText          = 1001   ,
      DropUrls          = 1002   ,
      DropImage         = 1003   ,
      DropHtml          = 1004   ,
      DropColor         = 1005   ,
      DropTag           = 1006   ,
      DropPicture       = 1007   ,
      DropPeople        = 1008   ,
      DropAudio         = 1009   ,
      DropVideo         = 1010   ,
      DropAlbum         = 1011   ,
      DropGender        = 1012   ,
      DropDivision      = 1013   ,
      DropURIs          = 1014   ,
      DropBookmark      = 1015   ,
      DropFont          = 1016   ,
      DropPen           = 1017   ,
      DropBrush         = 1018   ,
      DropGradient      = 1019   ,
      DropShape         = 1020   ,
      DropMember        = 1021   ,
      DropSet           = 1022   ,
      DropActions       = 1023   ,
      DropDecision      = 1024   ,
      DropCondition     = 1025   ,
      DropExecution     = 1026   ,
      DropSqlTable      = 1027   ,
      DropDatabase      = 1028   ,
      DropTask          = 1029   ,
      DropNation        = 1030   ,
      DropContour       = 1031   ,
      DropManifold      = 1032   ,
      DropSource        = 1033   ,
      DropDocument      = 1034   ,
      DropEyes          = 1035   ,
      DropHairs         = 1036   ,
      DropKeyword       = 1037   ,
      DropTerminology   = 1038   ,
      DropKnowledge     = 1039   ,
      DropField         = 1040   ,
      DropKnowledgeBase = 1041   ,
      DropSqlColumn     = 1042   ,
      DropUuid          = 1043   ,
      DropCommodity     = 1044   ,
      DropOrganization  = 1045   ,
      DropBlob          = 1046   ,
      DropVariable      = 1047   ,
      DropTorrent       = 1048   ,
      DropCamera        = 1049   ,
      DropFace          = 1050   ,
      DropColorGroup    = 1051   ,
      DropSetsAlgebra   = 1052   ,
      DropName          = 1053   ,
      DropStar          = 1054   ,
      DropPhoneme       = 1055   ,
      DropModel         = 1056   ,
      DropReality       = 1057   }
      DropTypes                  ;

    typedef enum           {
      GuiNativeId =      0 ,
      GuiMainId   =  10001 ,
      GuiUserId   = 100001 }
      DecisionMapId        ; // Decision table id

    typedef enum               {
      InterfaceHasMenu  = 1001 ,
      CommonFunctionEnd = 1002
    } CommonFunctionIDs        ;

    Plan             *  plan       ;
    double              opacity    ;
    Pens                pens       ;
    Brushes             brushes    ;
    Pathes              pathes     ;
    DecisionTables      decisions  ;
    bool                designable ;
    QMap<QString,QIcon> LocalIcons ;
    NAMEs               LocalMsgs  ;

    explicit AbstractGui             (QWidget       * widget,Plan * plan = NULL);
    explicit AbstractGui             (QGraphicsItem * item  ,Plan * plan = NULL);
    virtual ~AbstractGui             (void);

    virtual bool    canDesign        (void) ;
    virtual void    setDesignable    (bool edit) ;

    void            setDropFlag      (DropTypes dropType,bool enabled);
    virtual bool    setAcceptVocal   (bool enabled) ;
    QIcon           Icon             (SUID ID) ;
    bool            changeFont       (void) ;

    void            acceptMouse      (Qt::MouseButtons      buttons  ) ;
    void            acceptModifiers  (Qt::KeyboardModifiers modifiers) ;

    virtual bool    addSequence      (VarArgs args) ;
    virtual bool    addSequence      (int command) ;
    virtual bool    Apportion        (void) ;

    virtual QString toCpp            (QString functionName) ;

    virtual void   assignTitle       (QString title) ;
    virtual void   assignLanguage    (nDeclWidget = NULL) ;
    virtual void   assignStyleSheet  (QString title,nDeclWidget = NULL) ;
    virtual void   assignMinimumSize (nDeclWidget) ;
    virtual void   assignMaximumSize (nDeclWidget) ;
    virtual bool   getGridSize       (nDeclWidget,QString title,QSize current,QSize & newSize) ;

    virtual QString GetName          (nConnectUuid) ;

    int             LimitValue       (int index) ;
    void            setLimitValue    (int index,int value) ;
    bool            ArgsToGroup      (int start,VarArgs & args,Group & group) ;
    bool            ArgsToUuids      (int start,VarArgs & args,UUIDs & uuids) ;
    bool            FixUuids         (UUIDs & Uuids) ;

    virtual void    setCanStop       (int value) ;
    virtual void    pushCanStop      (void) ;
    virtual void    popCanStop       (void) ;
    virtual bool    canStop          (void) ;
    virtual bool    isLoading        (void) ;
    virtual bool    isStopped        (void) ;
    virtual bool    startLoading     (void) ;
    virtual bool    stopLoading      (void) ;
    virtual void    stopForcely      (void) ;

    virtual bool    setFunction      (int Id,bool enable) ;
    virtual bool    isFunction       (int Id) ;
    virtual void    setGui           (QWidget * widget) ;

    void            setSuggestion    (QSize size) ;
    QSize           SizeSuggestion   (QSize size) const ;
    QSize           SizeSuggestion   (int width,int height) const ;

    virtual bool    RecoverySettings (QString scope) ;
    virtual bool    StoreSettings    (QString scope) ;

    virtual void    alert            (QString sound,QString message) ;

  protected:

    QTimer            * Commando        ;
    QMutex              Mutex           ;
    QMutex              PainterMutex    ;
    QMutex              CommandMutex    ;
    QWidget           * Gui             ;
    QDrag             * Drag            ;
    QString             localTitle      ;
    QShortcuts          Shortcuts       ;
    VcfWidgets          ChildWidgets    ;
    IMAPs               TimerIDs        ;
    bool                PassDragDrop    ;
    bool                Dumping         ;
    BMAPs               AllowDrops      ;
    BMAPs               Functionalities ;
    IMAPs               LimitValues     ;
    VarArgLists         Sequences       ;
    DataRetrievers      Retrievers      ;
    int                 vLanguageId     ;
    bool                allowGesture    ;
    bool                localModified   ;

    bool         EnterPainter        (void) ;
    void         LeavePainter        (void) ;

    void         StartCommando       (void) ;
    bool         EnterCommando       (void) ;
    void         LeaveCommando       (void) ;
    virtual void LaunchCommands      (void) ;
    virtual void DispatchCommands    (void) ;

    void         FadeIn              (nDeclWidget,int steps);
    void         FadeOut             (nDeclWidget,int steps);

    // message posting
    void         Notify              (QString message);
    void         Notify              (QString caption,QString message);

    // focus management
    virtual bool focusIn             (QFocusEvent * event) ;
    virtual bool focusOut            (QFocusEvent * event) ;

    virtual bool FocusIn             (void);
    virtual bool FocusOut            (void);

    // Shortcut management
    int          addShortcut         (const QKeySequence & key                                   ,
                                      QWidget            * parent                                ,
                                      const char         * member          = 0                   ,
                                      const char         * ambiguousMember = 0                   ,
                                      Qt::ShortcutContext  context         = Qt::WindowShortcut) ;

    QAction *    connectAction       (int Id,QObject * parent,const char * method,bool enable = true) ;
    QAction *    actionLabel         (int Id,QString message) ;

    QString      MimeType            (const QMimeData * mime,QString formats);

    // drag management
    bool         dragStart           (QMouseEvent * event);
    bool         dragMoving          (QMouseEvent * event);
    bool         dragEnd             (QMouseEvent * event);

    virtual bool hasItem             (void);
    virtual bool startDrag           (QMouseEvent * event);
    virtual bool fetchDrag           (QMouseEvent * event);
    virtual QMimeData * dragMime     (void);
    virtual void dragDone            (Qt::DropAction dropIt,QMimeData * mime);
    virtual bool finishDrag          (QMouseEvent * event);

    virtual bool acceptDrop          (nDeclWidget,const QMimeData * mime);
    virtual bool dropNew             (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropMoving          (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropAppend          (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool removeDrop          (void);

    virtual bool dragEnter           (QDragEnterEvent * event) ;
    virtual bool dragMove            (QDragMoveEvent  * event) ;
    virtual bool drop                (QDropEvent      * event) ;

    virtual void imState             (QInputMethodEvent * event) ;
    virtual void keyState            (QKeyEvent         * event) ;
    virtual void mouseState          (QMouseEvent       * event) ;
    virtual void wheelState          (QWheelEvent       * event) ;

    virtual bool permitGesture       (void) ;
    virtual bool gestureEvent        (QEvent             * event  ) ;
    virtual bool acceptTap           (QTapGesture        * gesture) ;
    virtual bool acceptTapHold       (QTapAndHoldGesture * gesture) ;
    virtual bool acceptPan           (QPanGesture        * gesture) ;
    virtual bool acceptPinch         (QPinchGesture      * gesture) ;
    virtual bool acceptSwipe         (QSwipeGesture      * gesture) ;
    virtual bool acceptCustom        (QGesture           * gesture) ;

    virtual void InstallDecisions    (void) ;

    void         Debug               (QEvent * event) ;

    UUIDs        GetUuids            (QByteArray & data) ;
    SUID         GetUuid             (QByteArray & data) ;
    QByteArray   CreateByteArray     (SUID    uuid ) ;
    QByteArray   CreateByteArray     (UUIDs & Uuids) ;
    void         setMime             (QMimeData * mime,QString mtype,SUID    uuid ) ;
    void         setMime             (QMimeData * mime,QString mtype,UUIDs & Uuids) ;

    virtual bool acceptTextDrop      (void) ;
    virtual bool acceptUrlsDrop      (void) ;
    virtual bool acceptImageDrop     (void) ;
    virtual bool acceptHtmlDrop      (void) ;
    virtual bool acceptColorDrop     (void) ;
    virtual bool acceptTagDrop       (void) ;
    virtual bool acceptPictureDrop   (void) ;
    virtual bool acceptPeopleDrop    (void) ;
    virtual bool acceptAudioDrop     (void) ;
    virtual bool acceptVideoDrop     (void) ;
    virtual bool acceptAlbumDrop     (void) ;
    virtual bool acceptGenderDrop    (void) ;
    virtual bool acceptDivisionDrop  (void) ;
    virtual bool acceptUriDrop       (void) ;
    virtual bool acceptBookmarkDrop  (void) ;
    virtual bool acceptFont          (void) ;
    virtual bool acceptPen           (void) ;
    virtual bool acceptBrush         (void) ;
    virtual bool acceptGradient      (void) ;
    virtual bool acceptShapes        (void) ;
    virtual bool acceptMembers       (void) ;
    virtual bool acceptSets          (void) ;
    virtual bool acceptActions       (void) ;
    virtual bool acceptDecision      (void) ;
    virtual bool acceptCondition     (void) ;
    virtual bool acceptExecution     (void) ;
    virtual bool acceptSqlTable      (void) ;
    virtual bool acceptDatabase      (void) ;
    virtual bool acceptTask          (void) ;
    virtual bool acceptNation        (void) ;
    virtual bool acceptContour       (void) ;
    virtual bool acceptManifold      (void) ;
    virtual bool acceptSources       (void) ;
    virtual bool acceptDocuments     (void) ;
    virtual bool acceptEyes          (void) ;
    virtual bool acceptHairs         (void) ;
    virtual bool acceptKeywords      (void) ;
    virtual bool acceptTerminologies (void) ;
    virtual bool acceptKnowledge     (void) ;
    virtual bool acceptFields        (void) ;
    virtual bool acceptKnowledgeBase (void) ;
    virtual bool acceptSqlColumn     (void) ;
    virtual bool acceptUuids         (void) ;
    virtual bool acceptCommodities   (void) ;
    virtual bool acceptOrganizations (void) ;
    virtual bool acceptBlobs         (void) ;
    virtual bool acceptVariables     (void) ;
    virtual bool acceptTorrents      (void) ;
    virtual bool acceptCameras       (void) ;
    virtual bool acceptFaces         (void) ;
    virtual bool acceptColorGroups   (void) ;
    virtual bool acceptSetsAlgebras  (void) ;
    virtual bool acceptNames         (void) ;
    virtual bool acceptStars         (void) ;
    virtual bool acceptPhonemes      (void) ;
    virtual bool acceptModels        (void) ;
    virtual bool acceptReality       (void) ;

    virtual bool acceptPrivate       (const QMimeData * mime) ;

    virtual bool dropHandler         (const QMimeData * mime) ;

    virtual bool dropItems           (nDeclWidget,const QMimeData * mime,QPoint  pos) ;
    virtual bool dropItems           (nDeclWidget,const QMimeData * mime,QPointF pos) ;
    virtual bool dropPrivate         (nDeclWidget,const QMimeData * mime,QPointF pos) ;

    virtual bool dropText            (nDeclWidget,QPointF pos,const QString & text    ) ;
    virtual bool dropUrls            (nDeclWidget,QPointF pos,const QList<QUrl> & urls) ;
    virtual bool dropImage           (nDeclWidget,QPointF pos,const QImage  & image   ) ;
    virtual bool dropHtml            (nDeclWidget,QPointF pos,const QString & html    ) ;
    virtual bool dropColor           (nDeclWidget,QPointF pos,const QColor  & color   ) ;
    virtual bool dropTags            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropPictures        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropPeople          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropAudios          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropVideos          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropAlbums          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropGender          (nDeclWidget,QPointF pos,const SUID      gender  ) ;
    virtual bool dropDivisions       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropURIs            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropBookmarks       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropFont            (nDeclWidget,QPointF pos,const SUID      font    ) ;
    virtual bool dropPen             (nDeclWidget,QPointF pos,const SUID      pen     ) ;
    virtual bool dropBrush           (nDeclWidget,QPointF pos,const SUID      brush   ) ;
    virtual bool dropGradient        (nDeclWidget,QPointF pos,const SUID      gradient) ;
    virtual bool dropShapes          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropMembers         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSets            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropActions         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropDecision        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropCondition       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropExecution       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSqlTable        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropDatabase        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropTask            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropNation          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropContour         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropManifold        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSources         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropDocuments       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropEyes            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropHairs           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropKeywords        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropTerminologies   (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropKnowledge       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropFields          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropKnowledgeBase   (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSqlColumn       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropUuids           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropCommodities     (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropOrganizations   (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropBlobs           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropVariables       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropTorrents        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropCameras         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropFaces           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropColorGroups     (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSetsAlgebras    (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropNames           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropStars           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropPhonemes        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropModels          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropReality         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;

    virtual bool Bustle              (void) ;
    virtual bool Vacancy             (void) ;
    virtual bool isLocked            (int timeout = 100) ;
    virtual void LockGui             (void) ;
    virtual void UnlockGui           (void) ;

    virtual bool ForUuid             (SUID & u,qint64 & i,UUIDs & U) ;

  private:

    void * PrivateStopable ;

    bool         allowDrops          (DropTypes dropType) ;

};




#include <qtcomponents.h>

#define DefaultMax  16777215
#define LoadingID   1000001
#define StoppedID   1000002
#define CanStopID   1000003

typedef struct              {
  bool             canstop  ;
  N::AbstractGui * abstract ;
} GuiStopable               ;

bool N::getAbstractStopable(QVariant pointer)
{
  GuiStopable * gs = (GuiStopable *) VariantToVoid ( pointer ) ;
  if ( NULL == gs ) return true                                ;
  return gs -> canstop                                         ;
}

bool N::setAbstractStopable(QVariant pointer,bool stopable)
{
  GuiStopable * gs = (GuiStopable *) VariantToVoid ( pointer ) ;
  if ( NULL == gs ) return true                                ;
  gs -> canstop = stopable                                     ;
  return gs -> canstop                                         ;
}

N::AbstractGui:: AbstractGui     ( QWidget * widget,Plan * p    )
               : plan            (                         p    )
               , Commando        ( new QTimer ( widget )        )
               , Gui             (              widget          )
               , opacity         ( 1.00                         )
               , PassDragDrop    ( true                         )
               , Dumping         ( false                        )
               , Drag            ( NULL                         )
               , localTitle      ( ""                           )
               , designable      ( false                        )
               , vLanguageId     ( 1819                         )
               , allowGesture    ( false                        )
               , PrivateStopable ( (void *) new GuiStopable ( ) )
               , localModified   ( false                        )
{
  decisions . Blank ( 0 )                                                  ;
  //////////////////////////////////////////////////////////////////////////
  if (IsNull(plan)) plan = AppPlan                                         ;
  nIfSafe(plan)                                                            {
    vLanguageId = plan->LanguageId                                         ;
  }                                                                        ;
  nIfSafe(Gui)                                                             {
    Gui -> setProperty ( "AbstractGui" , true                            ) ;
    Gui -> setProperty ( "CanStop"     , VoidVariant ( PrivateStopable ) ) ;
  }                                                                        ;
  //////////////////////////////////////////////////////////////////////////
  ( (GuiStopable *) PrivateStopable ) -> canstop  = true                   ;
  ( (GuiStopable *) PrivateStopable ) -> abstract = this                   ;
  //////////////////////////////////////////////////////////////////////////
  LimitValues [ LoadingID ] = 0                                            ;
  LimitValues [ StoppedID ] = 0                                            ;
  LimitValues [ CanStopID ] = 0                                            ;
  //////////////////////////////////////////////////////////////////////////
  InstallDecisions ( )                                                     ;
}

N::AbstractGui:: AbstractGui     ( QGraphicsItem * item,Plan * p )
               : plan            (                             p )
               , Gui             ( NULL                          )
               , opacity         ( 1.00                          )
               , PassDragDrop    ( true                          )
               , Dumping         ( false                         )
               , Drag            ( NULL                          )
               , designable      ( false                         )
               , PrivateStopable ( (void *) new GuiStopable ( )  )
{
  decisions.Blank(GuiNativeId)                                             ;
  //////////////////////////////////////////////////////////////////////////
  if (IsNull(plan)) plan = AppPlan                                         ;
  nIfSafe(plan)                                                            {
    vLanguageId = plan->LanguageId                                         ;
  }                                                                        ;
  //////////////////////////////////////////////////////////////////////////
  QGraphicsScene * gs = NULL                                               ;
  nIfSafe(item) gs = item->scene()                                         ;
  nIfSafe(gs)                                                              {
    QList<QGraphicsView *> vs = gs->views()                                ;
    if (vs.count()>0)                                                      {
      Gui = (QWidget *)vs[0]                                               ;
    }                                                                      ;
  }                                                                        ;
  Commando = new QTimer ( Gui )                                            ;
  nIfSafe ( Gui )                                                          {
    Gui -> setProperty ( "AbstractGui" , true                            ) ;
    Gui -> setProperty ( "CanStop"     , VoidVariant ( PrivateStopable ) ) ;
  }                                                                        ;
  //////////////////////////////////////////////////////////////////////////
  ( (GuiStopable *) PrivateStopable ) -> canstop  = true                   ;
  ( (GuiStopable *) PrivateStopable ) -> abstract = this                   ;
  //////////////////////////////////////////////////////////////////////////
  LimitValues [ LoadingID ] = 0                                            ;
  LimitValues [ StoppedID ] = 0                                            ;
  LimitValues [ CanStopID ] = 0                                            ;
  //////////////////////////////////////////////////////////////////////////
  InstallDecisions ( )                                                     ;
}

N::AbstractGui::~AbstractGui(void)
{
  if ( NotNull ( PrivateStopable ) ) {
    delete PrivateStopable           ;
    PrivateStopable = NULL           ;
  }                                  ;
}

bool N::AbstractGui::ForUuid(SUID & u,qint64 & i,UUIDs & U)
{
  if ( i >= U . count ( ) ) return false ;
  u = U [ i ]                            ;
  i++                                    ;
  return true                            ;
}

bool N::AbstractGui::FixUuids(UUIDs & Uuids)
{
  LimitValues [ 2 ] = Uuids . count ( )            ;
  if ( LimitValues[0] >= 0 && LimitValues[1] > 0 ) {
    UUIDs UX                                       ;
    int   sid = LimitValues[0]                     ;
    int   tid = LimitValues[1]                     ;
    int   eid = LimitValues[2]                     ;
    if ((sid+tid)<eid) eid = sid + tid             ;
    for (int i=sid;i<eid;i++) UX << Uuids[i]       ;
    Uuids = UX                                     ;
    return true                                    ;
  }                                                ;
  return false                                     ;
}

int N::AbstractGui::LimitValue(int index)
{
  if (!LimitValues.contains(index)) return 0 ;
  return LimitValues [ index ]               ;
}

void N::AbstractGui::setLimitValue(int index,int value)
{
  LimitValues [ index ] = value ;
}

void N::AbstractGui::setSuggestion(QSize s)
{
  LimitValues [ 11010001 ] = s . width  ( ) ;
  LimitValues [ 11010002 ] = s . height ( ) ;
}

QSize N::AbstractGui::SizeSuggestion (QSize size) const
{
  QSize s = size                               ;
  if ( LimitValues . contains ( 11010001 ) )   {
    s . setWidth  ( LimitValues [ 11010001 ] ) ;
  }                                            ;
  if ( LimitValues . contains ( 11010002 ) )   {
    s . setHeight ( LimitValues [ 11010002 ] ) ;
  }                                            ;
  return s                                     ;
}

QSize N::AbstractGui::SizeSuggestion(int w,int h) const
{
  return SizeSuggestion ( QSize ( w , h ) ) ;
}

bool N::AbstractGui::ArgsToGroup(int start,VarArgs & args,Group & group)
{
  if ( start >= args.count() ) return false               ;
  group.first      = args [ start     ] . toULongLong ( ) ;
  group.second     = args [ start + 1 ] . toULongLong ( ) ;
  group.t1         = args [ start + 2 ] . toInt       ( ) ;
  group.t2         = args [ start + 3 ] . toInt       ( ) ;
  group.relation   = args [ start + 4 ] . toInt       ( ) ;
  group.position   = args [ start + 5 ] . toInt       ( ) ;
  group.membership = args [ start + 6 ] . toDouble    ( ) ;
  return true                                             ;
}

bool N::AbstractGui::ArgsToUuids(int start,VarArgs & args,UUIDs & uuids)
{
  if ( start >= args.count() ) return false ;
  int t = args[start].toInt()               ;
  start++                                   ;
  if (t<=0) return false                    ;
  for (int i=0;i<t;i++,start++)             {
    uuids << args[start].toULongLong()      ;
  }                                         ;
  return true                               ;
}

void N::AbstractGui::setCanStop(int value)
{
  LimitValues [ CanStopID ] = value                             ;
  ( (GuiStopable *) PrivateStopable ) -> canstop  = canStop ( ) ;
}

void N::AbstractGui::pushCanStop(void)
{
  LimitValues [ CanStopID ] ++                                  ;
  ( (GuiStopable *) PrivateStopable ) -> canstop  = canStop ( ) ;
}

void N::AbstractGui::popCanStop(void)
{
  LimitValues [ CanStopID ] --                                  ;
  ( (GuiStopable *) PrivateStopable ) -> canstop  = canStop ( ) ;
}

bool N::AbstractGui::canStop(void)
{
  return ( 0 >= LimitValues [ CanStopID ] ) ;
}

bool N::AbstractGui::isLoading(void)
{
  return ( LimitValues [ LoadingID ] > 0 ) ;
}

bool N::AbstractGui::isStopped(void)
{
  return ( LimitValues [ StoppedID ] <= 0 ) ;
}

bool N::AbstractGui::startLoading(void)
{
  LimitValues [ LoadingID ] ++             ;
  LimitValues [ StoppedID ] ++             ;
  pushCanStop (           )                ;
  //////////////////////////////////////////
  return ( LimitValues [ LoadingID ] > 0 ) ;
}

bool N::AbstractGui::stopLoading(void)
{
  if ( LimitValues [ LoadingID ] > 0 )     {
    LimitValues [ LoadingID ] --           ;
  }                                        ;
  LimitValues [ StoppedID ] --             ;
  popCanStop  (           )                ;
  return ( LimitValues [ LoadingID ] > 0 ) ;
}

void N::AbstractGui::stopForcely(void)
{
  LimitValues [ LoadingID ] = 0 ;
}

bool N::AbstractGui::setFunction(int Id,bool enable)
{
  Functionalities [ Id ] = enable ;
  return enable                   ;
}

bool N::AbstractGui::isFunction(int Id)
{
  if ( !Functionalities.contains(Id) ) return false ;
  return Functionalities [ Id ]                     ;
}

void N::AbstractGui::alert(QString sound,QString message)
{
  nDropOut       ( IsNull ( plan ) ) ;
  plan -> Notify ( sound , message ) ;
}

void N::AbstractGui::setGui(QWidget * widget)
{
  Gui = widget                  ;
  Commando -> setParent ( Gui ) ;
}

bool N::AbstractGui::RecoverySettings(QString scope)
{
  return true ;
}

bool N::AbstractGui::StoreSettings(QString scope)
{
  return true ;
}

bool N::AbstractGui::canDesign(void)
{
  return designable ;
}

void N::AbstractGui::setDesignable(bool edit)
{
  designable = edit ;
}

bool N::AbstractGui::EnterPainter(void)
{
  bool canLock = PainterMutex . tryLock ( 25 )            ;
  if (canLock)                                            {
    decisions[GuiNativeId].setCondition(GuiPainted,false) ;
  }                                                       ;
  return canLock ;
}

void N::AbstractGui::LeavePainter(void)
{
  PainterMutex . unlock ( )                             ;
  decisions[GuiNativeId].setCondition(GuiPainted,true ) ;
}

void N::AbstractGui::InstallDecisions(void)
{
}

void N::AbstractGui::StartCommando(void)
{
  nDropOut ( Commando -> isActive() ) ;
  Commando -> start ( 100 )           ;
}

bool N::AbstractGui::EnterCommando(void)
{
  bool locked = CommandMutex . tryLock ( 100 ) ;
  Commando -> stop ( )                         ;
  return locked                                ;
}

void N::AbstractGui::LeaveCommando(void)
{
  CommandMutex . unlock ( ) ;
}

void N::AbstractGui::LaunchCommands(void)
{
  EnterCommando    ( ) ;
  DispatchCommands ( ) ;
  LeaveCommando    ( ) ;
}

void N::AbstractGui::DispatchCommands(void)
{
}

bool N::AbstractGui::Bustle(void)
{
  Mutex . lock     (                ) ;
  Gui -> setCursor ( Qt::WaitCursor ) ;
  return true                         ;
}

bool N::AbstractGui::Vacancy(void)
{
  Gui -> setCursor ( Qt::ArrowCursor ) ;
  Mutex . unlock   (                 ) ;
  return true                          ;
}

bool N::AbstractGui::isLocked(int timeout)
{
  nKickOut ( !Mutex.tryLock(timeout) , true ) ;
  Mutex . unlock ( )                          ;
  return false                                ;
}

void N::AbstractGui::LockGui(void)
{
  Mutex . lock ( ) ;
}

void N::AbstractGui::UnlockGui(void)
{
  Mutex . unlock ( ) ;
}

QIcon N::AbstractGui::Icon(SUID ID)
{
  QIcon I                       ;
  if (plan->icons.contains(ID)) {
    return plan->icons[ID]      ;
  }                             ;
  return I                      ;
}

bool N::AbstractGui::changeFont(void)
{
  bool  okay = false                ;
  QFont f    = Gui -> font()        ;
  f = QFontDialog::getFont(&okay,f) ;
  nKickOut ( !okay , false )        ;
  Gui -> setFont ( f )              ;
  return true                       ;
}

void N::AbstractGui::FadeIn(QWidget * widget,int steps)
{
  if (opacity<0.1) opacity = 0.1           ;
  qreal dw = opacity - 0.1                 ;
  qreal Opacity = 0.1                      ;
  dw /= steps                              ;
  for (int i=0;i<=steps;i++)               {
    widget->setWindowOpacity(Opacity)      ;
    Opacity += dw                          ;
    if (Opacity>opacity) Opacity = opacity ;
    widget->show()                         ;
    qApp->processEvents()                  ;
    qApp->sendPostedEvents()               ;
    Time::msleep(50)                       ;
  }                                        ;
  widget->setWindowOpacity(opacity)        ;
  widget->show()                           ;
}

void N::AbstractGui::FadeOut(QWidget * widget,int steps)
{
  if (opacity<0.1) opacity = 0.1      ;
  qreal dw = opacity - 0.1            ;
  qreal Opacity = opacity             ;
  dw /= steps                         ;
  for (int i=0;i<=steps;i++)          {
    widget->setWindowOpacity(Opacity) ;
    Opacity -= dw                     ;
    if (Opacity<0) Opacity = 0        ;
    widget->show()                    ;
    qApp->processEvents()             ;
    qApp->sendPostedEvents()          ;
    Time::msleep(50)                  ;
  }                                   ;
  widget->setWindowOpacity(Opacity)   ;
  widget->hide()                      ;
}

void N::AbstractGui::Notify(QString message)
{
  nDropOut ( IsNull(Gui) )                                 ;
  QMessageBox::information(Gui,Gui->windowTitle(),message) ;
}

void N::AbstractGui::Notify(QString caption,QString message)
{
  nDropOut ( IsNull(Gui) )                      ;
  QMessageBox::information(Gui,caption,message) ;
}

bool N::AbstractGui::focusIn(QFocusEvent * event)
{
  if (event->gotFocus() && FocusIn ()) {
    event->accept()                    ;
    return true                        ;
  }                                    ;
  return false                         ;
}

bool N::AbstractGui::focusOut(QFocusEvent * event)
{
  if (event->lostFocus() && FocusOut()) {
    event->accept()                     ;
    return true                         ;
  }                                     ;
  return false                          ;
}

bool N::AbstractGui::FocusIn(void)
{
  return false ;
}

bool N::AbstractGui::FocusOut(void)
{
  return false ;
}

bool N::AbstractGui::permitGesture(void)
{
  return allowGesture ;
}

bool N::AbstractGui::gestureEvent(QEvent * event)
{
  nKickOut ( NotEqual ( event->type() , QEvent::Gesture ) , false  )       ;
  QGestureEvent * gesture = static_cast<QGestureEvent *>  ( event  )       ;
  nKickOut ( IsNull(gesture)                              , false  )       ;
  QList<QGesture *> gestures = gesture->gestures()                         ;
  nKickOut ( gestures.count() <=0                         , false  )       ;
  bool responsed = false                                                   ;
  for (int i=0;i<gestures.count();i++)                                     {
    switch (gestures[i]->gestureType())                                    {
      case Qt::TapGesture                                                  :
        if (acceptTap    (static_cast<QTapGesture        *>(gestures[i]))) {
          responsed = true                                                 ;
        }                                                                  ;
      break                                                                ;
      case Qt::TapAndHoldGesture                                           :
        if (acceptTapHold(static_cast<QTapAndHoldGesture *>(gestures[i]))) {
          responsed = true                                                 ;
        }                                                                  ;
      break                                                                ;
      case Qt::PanGesture                                                  :
        if (acceptPan    (static_cast<QPanGesture        *>(gestures[i]))) {
          responsed = true                                                 ;
        }                                                                  ;
      break                                                                ;
      case Qt::PinchGesture                                                :
        if (acceptPinch  (static_cast<QPinchGesture      *>(gestures[i]))) {
          responsed = true                                                 ;
        }                                                                  ;
      break                                                                ;
      case Qt::SwipeGesture                                                :
        if (acceptSwipe  (static_cast<QSwipeGesture      *>(gestures[i]))) {
          responsed = true                                                 ;
        }                                                                  ;
      break                                                                ;
      default                                                              :
        if (acceptCustom(gestures[i])) responsed = true                    ;
      break                                                                ;
    }                                                                      ;
  }                                                                        ;
  return responsed                                                         ;
}

bool N::AbstractGui::acceptTap(QTapGesture * gesture)
{ Q_UNUSED ( gesture ) ;
  return false         ;
}

bool N::AbstractGui::acceptTapHold(QTapAndHoldGesture * gesture)
{ Q_UNUSED ( gesture ) ;
  return false         ;
}

bool N::AbstractGui::acceptPan(QPanGesture * gesture)
{ Q_UNUSED ( gesture ) ;
  return false         ;
}

bool N::AbstractGui::acceptPinch(QPinchGesture * gesture)
{ Q_UNUSED ( gesture ) ;
  return false         ;
}

bool N::AbstractGui::acceptSwipe(QSwipeGesture * gesture)
{ Q_UNUSED ( gesture ) ;
  return false         ;
}

bool N::AbstractGui::acceptCustom(QGesture * gesture)
{ Q_UNUSED ( gesture ) ;
  return false         ;
}

bool N::AbstractGui::addSequence(VarArgs args)
{
  Sequences << args ;
  return true       ;
}

bool N::AbstractGui::addSequence(int command)
{
  VarArgs V                 ;
  V << QVariant ( command ) ;
  Sequences << V            ;
  return true               ;
}

bool N::AbstractGui::Apportion(void)
{
  return false ;
}

QString N::AbstractGui::toCpp(QString functionName)
{
  return "" ;
}

bool N::AbstractGui::setAcceptVocal(bool enabled)
{
  return true ;
}

void N::AbstractGui::assignTitle(QString title)
{
  if ( IsNull ( Gui ) ) return          ;
  Gui -> setWindowTitle ( title )       ;
  ///////////////////////////////////////
  QWidget * w = Gui -> parentWidget ( ) ;
  if ( IsNull (  w  ) ) return          ;
  ///////////////////////////////////////
  QMdiSubWindow * msw                   ;
  msw  = Casting ( QMdiSubWindow , w )  ;
  if ( NotNull ( msw  ) )               {
    msw  -> setWindowTitle ( title )    ;
  }                                     ;
  ///////////////////////////////////////
  QDockWidget * dock                    ;
  dock = Casting ( QDockWidget , w )    ;
  if ( NotNull ( dock ) )               {
    dock -> setWindowTitle ( title )    ;
  }                                     ;
}

void N::AbstractGui::assignLanguage(QWidget * widget)
{
  if (IsNull(widget)) widget = Gui                                  ;
  nDropOut ( IsNull(widget) )                                       ;
  LanguageSelections * NLS = new LanguageSelections(widget,plan)    ;
  NLS->List(vLanguageId)                                            ;
  if (NLS->exec()==QDialog::Accepted) vLanguageId = NLS->Language() ;
  NLS -> deleteLater ( )                                            ;
}

void N::AbstractGui::assignStyleSheet(QString title,QWidget * widget)
{
  nDropOut ( IsNull(plan) )                                     ;
  if (IsNull(widget)) widget = Gui                              ;
  nDropOut ( IsNull(widget) )                                   ;
  QTextEdit       * TEW = new QTextEdit       ( widget        ) ;
  ContainerDialog * CDW = new ContainerDialog ( widget , plan ) ;
  QString           CSS = widget->styleSheet()                  ;
  TEW    -> setWindowTitle   ( title     )                      ;
  TEW    -> resize           ( 320 , 240 )                      ;
  CDW    -> setWidget        ( TEW       )                      ;
  TEW    -> setPlainText     ( CSS       )                      ;
  if ( QDialog::Accepted == CDW -> exec ( ) )                   {
    CSS = TEW -> toPlainText (           )                      ;
  }                                                             ;
  TEW    -> deleteLater      (           )                      ;
  CDW    -> deleteLater      (           )                      ;
  widget -> setStyleSheet    ( CSS       )                      ;
  ///////////////////////////////////////////////////////////////
  QMdiSubWindow * msw                                           ;
  msw = qobject_cast<QMdiSubWindow *>(widget->parentWidget())   ;
  if (NotNull(msw)) msw -> setStyleSheet ( CSS )                ;
  ///////////////////////////////////////////////////////////////
  QDockWidget   * qdw                                           ;
  qdw = qobject_cast<QDockWidget   *>(widget->parentWidget())   ;
  if (NotNull(qdw)) qdw -> setStyleSheet ( CSS )                ;
}

void N::AbstractGui::assignMinimumSize(QWidget * widget)
{
  GetSize  * ngs = new GetSize(widget,plan)                 ;
  QSize      s   = widget->minimumSize()                    ;
  QString    t   = widget->windowTitle()                    ;
  QString    m   = QObject::tr("Minimum size of %1").arg(t) ;
  ngs->setWindowTitle(m)                                    ;
  ngs->setRange(0,0,DefaultMax)                             ;
  ngs->setRange(1,0,DefaultMax)                             ;
  ngs->setPrefix(0,QObject::tr("Width : " ))                ;
  ngs->setPrefix(1,QObject::tr("Height : "))                ;
  ngs->setSize(s);                                          ;
  if (ngs->exec()==QDialog::Accepted)                       {
    s = ngs->Size()                                         ;
    widget->setMinimumSize(s)                               ;
  }                                                         ;
  ngs->deleteLater()                                        ;
}

void N::AbstractGui::assignMaximumSize(QWidget * widget)
{
  GetSize  * ngs = new GetSize(widget,plan)                 ;
  QSize      s   = widget->maximumSize()                    ;
  QString    t   = widget->windowTitle()                    ;
  QString    m   = QObject::tr("Maximum size of %1").arg(t) ;
  ngs->setWindowTitle(m)                                    ;
  ngs->setRange(0,0,DefaultMax)                             ;
  ngs->setRange(1,0,DefaultMax)                             ;
  ngs->setPrefix(0,QObject::tr("Width : " ))                ;
  ngs->setPrefix(1,QObject::tr("Height : "))                ;
  ngs->setSize(s);                                          ;
  if (ngs->exec()==QDialog::Accepted)                       {
    s = ngs->Size()                                         ;
    widget->setMaximumSize(s)                               ;
  }                                                         ;
  ngs->deleteLater()                                        ;
}

bool N::AbstractGui::getGridSize (
       QWidget * widget       ,
       QString   title        ,
       QSize     current      ,
       QSize   & newSize      )
{
  GetSize * ngs = new GetSize(widget,plan)   ;
  bool       correct = false                 ;
  ngs->setWindowTitle(title)                 ;
  ngs->setRange(0,0,DefaultMax)              ;
  ngs->setRange(1,0,DefaultMax)              ;
  ngs->setPrefix(0,QObject::tr("Width : " )) ;
  ngs->setPrefix(1,QObject::tr("Height : ")) ;
  ngs->setSize (current       )              ;
  if (ngs->exec()==QDialog::Accepted)        {
    newSize = ngs->Size()                    ;
    correct = true                           ;
  }                                          ;
  ngs->deleteLater()                         ;
  return correct                             ;
}

QString N::AbstractGui::GetName(SqlConnection & connection,SUID uuid)
{
  return connection.getName (
           PlanTable(Names) ,
           "uuid"           ,
           vLanguageId      ,
           uuid           ) ;
}

int N::AbstractGui::addShortcut            (
      const QKeySequence & key             ,
      QWidget            * parent          ,
      const char         * member          ,
      const char         * ambiguousMember ,
      Qt::ShortcutContext  context         )
{
  Shortcuts << new QShortcut(key,parent,member,ambiguousMember,context) ;
  return Shortcuts.count()                                              ;
}

QString N::AbstractGui::MimeType(const QMimeData * mime,QString formats)
{
  QByteArray  data                                    ;
  QString     mtype = ""                              ;
  QStringList mimes = formats.split(";")              ;
  data.clear()                                        ;
  for (int i=0;data.size()==0 && i<mimes.count();i++) {
    mtype = mimes[i]                                  ;
    data  = mime->data(mtype)                         ;
  }                                                   ;
  if (data.size()<=0) mtype = ""                      ;
  return mtype                                        ;
}

bool N::AbstractGui::dragStart(QMouseEvent * event)
{
  return startDrag(event) ;
}

bool N::AbstractGui::dragMoving(QMouseEvent * event)
{
  nKickOut ( NotNull(Drag)                            , false ) ;
  nKickOut ( !IsMask(event->buttons(),Qt::LeftButton) , false ) ;
  nKickOut ( !hasItem()                               , false ) ;
  nKickOut ( !fetchDrag(event)                        , false ) ;
  QMimeData * mime = dragMime  (   )                            ;
  if (NotNull(mime))                                            {
    QCursor DC ( Qt::ClosedHandCursor )                         ;
    Dumping = true                                              ;
    Drag = new QDrag (Gui)                                      ;
    Qt::DropAction dropAction                                   ;
    Drag->setMimeData(mime)                                     ;
    if (mime->hasImage())                                       {
      QImage image = qvariant_cast<QImage>(mime->imageData())   ;
      Drag -> setPixmap ( QPixmap::fromImage(image) )           ;
    } else                                                      {
      Drag -> setPixmap ( DC.pixmap()               )           ;
    }                                                           ;
    dropAction = Drag->exec ( Qt::CopyAction | Qt::MoveAction ) ;
    dragDone(dropAction,mime)                                   ;
    Dumping = false                                             ;
  }                                                             ;
  nKickOut ( !PassDragDrop                            , true  ) ;
  return true                                                   ;
}

bool N::AbstractGui::dragEnd(QMouseEvent * event)
{
  nKickOut ( !finishDrag(event) , true ) ;
  nKickOut ( !PassDragDrop      , true ) ;
  return false                           ;
}

bool N::AbstractGui::hasItem(void)
{
  return false ;
}

bool N::AbstractGui::startDrag(QMouseEvent * event)
{
  return false ;
}

bool N::AbstractGui::fetchDrag(QMouseEvent * event)
{
  return false ;
}

QMimeData * N::AbstractGui::dragMime(void)
{
  return NULL ;
}

void N::AbstractGui::dragDone(Qt::DropAction dropIt,QMimeData * mime)
{ // actually, mime was deleted before this function is called
//  mime -> deleteLater ( ) ;
  Gui -> setCursor ( Qt::ArrowCursor ) ;
  DoProcessEvents                      ;
}

bool N::AbstractGui::finishDrag(QMouseEvent * event)
{
  return true ;
}

bool N::AbstractGui::acceptDrop(QWidget * source,const QMimeData * mime)
{
  return false ;
}

bool N::AbstractGui::dropNew(QWidget * source,const QMimeData * mime,QPoint pos)
{
  return false ;
}

bool N::AbstractGui::dropMoving(QWidget * source,const QMimeData * mime,QPoint pos)
{
  return false ;
}

bool N::AbstractGui::dropAppend(QWidget * source,const QMimeData * mime,QPoint pos)
{
  return false ;
}

bool N::AbstractGui::removeDrop(void)
{
  return false ;
}

bool N::AbstractGui::dragEnter(QDragEnterEvent * event)
{
  nKickOut(!acceptDrop((QWidget *)event->source(),event->mimeData()             ),false) ;
  nKickOut(!dropNew   ((QWidget *)event->source(),event->mimeData(),event->pos()),false) ;
  return true                                                                            ;
}

bool N::AbstractGui::dragMove(QDragMoveEvent  * event)
{
  nKickOut(!acceptDrop ((QWidget *)event->source(),event->mimeData()             ),false) ;
  nKickOut(!dropMoving ((QWidget *)event->source(),event->mimeData(),event->pos()),false) ;
  return true                                                                             ;
}

bool N::AbstractGui::drop(QDropEvent * event)
{
  nKickOut(!acceptDrop ((QWidget *)event->source(),event->mimeData()             ),false) ;
  nKickOut(!dropAppend ((QWidget *)event->source(),event->mimeData(),event->pos()),false) ;
  return true                                                                             ;
}

void N::AbstractGui::acceptMouse(Qt::MouseButtons buttons)
{
  decisions[0].setCondition(GuiLeftButton  ,IsMask(buttons,Qt::LeftButton  )) ;
  decisions[0].setCondition(GuiRightButton ,IsMask(buttons,Qt::RightButton )) ;
  decisions[0].setCondition(GuiMiddleButton,IsMask(buttons,Qt::MiddleButton)) ;
}

void N::AbstractGui::acceptModifiers(Qt::KeyboardModifiers modifiers)
{
  decisions[0].setCondition(GuiShift  ,IsMask(modifiers,Qt::ShiftModifier  )) ;
  decisions[0].setCondition(GuiControl,IsMask(modifiers,Qt::ControlModifier)) ;
  decisions[0].setCondition(GuiAlt    ,IsMask(modifiers,Qt::AltModifier    )) ;
  decisions[0].setCondition(GuiMeta   ,IsMask(modifiers,Qt::MetaModifier   )) ;
}

void N::AbstractGui::imState (QInputMethodEvent * event)
{
}

void N::AbstractGui::keyState (QKeyEvent * event)
{
  acceptModifiers(event->modifiers()) ;
}

void N::AbstractGui::mouseState (QMouseEvent * event)
{
  acceptMouse(event->buttons()) ;
}

void N::AbstractGui::wheelState (QWheelEvent * event)
{
  acceptMouse(event->buttons()) ;
}

void N::AbstractGui::Debug(QEvent * event)
{
  nDropOut ( IsNull(plan) )                            ;
  plan->Debug(15,QString("QET:%1").arg(event->type())) ;
}

UUIDs N::AbstractGui::GetUuids(QByteArray & data)
{
  UUIDs Uuids                        ;
  SUID * suid  = (SUID *)data.data() ;
  int    total = (int)suid[0]        ;
  for (int i=0;i<total;i++)          {
    Uuids << suid[i+1]               ;
  }                                  ;
  return Uuids                       ;
}

SUID N::AbstractGui::GetUuid(QByteArray & data)
{
  SUID   * suid = (SUID *)data.data() ;
  return (*suid)                      ;
}

QByteArray N::AbstractGui::CreateByteArray(SUID uuid)
{
  return QByteArray((const char *)&uuid,sizeof(SUID));
}

QByteArray N::AbstractGui::CreateByteArray(UUIDs & Uuids)
{
  QByteArray  data                            ;
  data.resize(sizeof(SUID)*(Uuids.count()+1)) ;
  SUID * suid = (SUID *)data.data()           ;
  suid[0] = Uuids.count()                     ;
  for (int i=0;i<Uuids.count();i++)           {
    suid[i+1] = Uuids[i]                      ;
  }                                           ;
  return data                                 ;
}

void N::AbstractGui::setMime(QMimeData * mime,QString mtype,SUID uuid)
{
  QByteArray  data = CreateByteArray(uuid) ;
  mime -> setData ( mtype , data )         ;
}

void N::AbstractGui::setMime(QMimeData * mime,QString mtype,UUIDs & Uuids)
{
  QByteArray  data = CreateByteArray(Uuids) ;
  mime -> setData ( mtype , data )          ;
}

bool N::AbstractGui::allowDrops(DropTypes dropType)
{
  if (AllowDrops.contains((int)dropType)) {
    return AllowDrops[(int)dropType]      ;
  }                                       ;
  return false                            ;
}

void N::AbstractGui::setDropFlag(DropTypes dropType,bool enabled)
{
  AllowDrops[(int)dropType] = enabled ;
}

QAction * N::AbstractGui::connectAction(int Id,QObject * parent,const char * method,bool enable)
{
  if (IsNull(plan)) return NULL                       ;
  return plan->connectAction(Id,parent,method,enable) ;
}

QAction * N::AbstractGui::actionLabel(int Id,QString message)
{
  if ( IsNull(plan)              ) return NULL ;
  if (!plan->actions.contains(Id)) return NULL ;
  QAction * action                             ;
  action  = plan->actions[Id]                  ;
  action -> setText(message)                   ;
  return action                                ;
}

bool N::AbstractGui::acceptPrivate(const QMimeData * mime)
{
  return false ;
}

bool N::AbstractGui::dropPrivate(QWidget * source,const QMimeData * mime,QPointF pos)
{
  return false ;
}

#define VG(Function,Item)           \
bool N::AbstractGui::Function(void) \
{                                   \
  return allowDrops(Item)         ; \
}

VG( acceptTextDrop      , DropText          )
VG( acceptUrlsDrop      , DropUrls          )
VG( acceptImageDrop     , DropImage         )
VG( acceptHtmlDrop      , DropHtml          )
VG( acceptColorDrop     , DropColor         )
VG( acceptTagDrop       , DropTag           )
VG( acceptPictureDrop   , DropPicture       )
VG( acceptPeopleDrop    , DropPeople        )
VG( acceptVideoDrop     , DropVideo         )
VG( acceptAudioDrop     , DropAudio         )
VG( acceptAlbumDrop     , DropAlbum         )
VG( acceptGenderDrop    , DropGender        )
VG( acceptDivisionDrop  , DropDivision      )
VG( acceptUriDrop       , DropURIs          )
VG( acceptBookmarkDrop  , DropBookmark      )
VG( acceptFont          , DropFont          )
VG( acceptPen           , DropPen           )
VG( acceptBrush         , DropBrush         )
VG( acceptGradient      , DropGradient      )
VG( acceptShapes        , DropShape         )
VG( acceptMembers       , DropMember        )
VG( acceptSets          , DropSet           )
VG( acceptActions       , DropActions       )
VG( acceptDecision      , DropDecision      )
VG( acceptCondition     , DropCondition     )
VG( acceptExecution     , DropExecution     )
VG( acceptSqlTable      , DropSqlTable      )
VG( acceptDatabase      , DropDatabase      )
VG( acceptTask          , DropTask          )
VG( acceptNation        , DropNation        )
VG( acceptContour       , DropContour       )
VG( acceptManifold      , DropManifold      )
VG( acceptSources       , DropSource        )
VG( acceptDocuments     , DropDocument      )
VG( acceptEyes          , DropEyes          )
VG( acceptHairs         , DropHairs         )
VG( acceptKeywords      , DropKeyword       )
VG( acceptTerminologies , DropTerminology   )
VG( acceptKnowledge     , DropKnowledge     )
VG( acceptFields        , DropField         )
VG( acceptKnowledgeBase , DropKnowledgeBase )
VG( acceptSqlColumn     , DropSqlColumn     )
VG( acceptUuids         , DropUuid          )
VG( acceptCommodities   , DropCommodity     )
VG( acceptOrganizations , DropOrganization  )
VG( acceptBlobs         , DropBlob          )
VG( acceptVariables     , DropVariable      )
VG( acceptTorrents      , DropTorrent       )
VG( acceptCameras       , DropCamera        )
VG( acceptFaces         , DropFace          )
VG( acceptColorGroups   , DropColorGroup    )
VG( acceptSetsAlgebras  , DropSetsAlgebra   )
VG( acceptNames         , DropName          )
VG( acceptStars         , DropStar          )
VG( acceptPhonemes      , DropPhoneme       )
VG( acceptModels        , DropModel         )
VG( acceptReality       , DropReality       )

#undef  VG

bool N::AbstractGui::dropHandler(const QMimeData * mime)
{
  bool Accepted = false                                   ;
  #define CHECK(FORMAT,FUNCX)                             \
    if (mime->hasFormat(FORMAT) && FUNCX()) Accepted = true
  #define VERIF(HasSome,DropF)                            \
    if (mime->HasSome() && DropF()) Accepted = true
  CHECK( "uuid/uuid"           , acceptUuids         ) ;
  CHECK( "uuid/uuids"          , acceptUuids         ) ;
  CHECK( "division/uuid"       , acceptDivisionDrop  ) ;
  CHECK( "division/uuids"      , acceptDivisionDrop  ) ;
  CHECK( "gender/uuid"         , acceptGenderDrop    ) ;
  CHECK( "tag/uuid"            , acceptTagDrop       ) ;
  CHECK( "tag/uuids"           , acceptDivisionDrop  ) ;
  CHECK( "name/uuid"           , acceptNames         ) ;
  CHECK( "name/uuids"          , acceptNames         ) ;
  CHECK( "picture/uuid"        , acceptPictureDrop   ) ;
  CHECK( "picture/uuids"       , acceptPictureDrop   ) ;
  CHECK( "people/uuid"         , acceptPeopleDrop    ) ;
  CHECK( "people/uuids"        , acceptPeopleDrop    ) ;
  CHECK( "audio/uuid"          , acceptAudioDrop     ) ;
  CHECK( "audio/uuids"         , acceptAudioDrop     ) ;
  CHECK( "video/uuid"          , acceptVideoDrop     ) ;
  CHECK( "video/uuids"         , acceptVideoDrop     ) ;
  CHECK( "album/uuid"          , acceptAlbumDrop     ) ;
  CHECK( "album/uuids"         , acceptAlbumDrop     ) ;
  CHECK( "uri/uuid"            , acceptUriDrop       ) ;
  CHECK( "uri/uuids"           , acceptUriDrop       ) ;
  CHECK( "bookmark/uuid"       , acceptBookmarkDrop  ) ;
  CHECK( "bookmark/uuids"      , acceptBookmarkDrop  ) ;
  CHECK( "shape/uuid"          , acceptShapes        ) ;
  CHECK( "shape/uuids"         , acceptShapes        ) ;
  CHECK( "member/uuid"         , acceptMembers       ) ;
  CHECK( "member/uuids"        , acceptMembers       ) ;
  CHECK( "set/uuid"            , acceptSets          ) ;
  CHECK( "set/uuids"           , acceptSets          ) ;
  CHECK( "action/uuid"         , acceptActions       ) ;
  CHECK( "action/uuids"        , acceptActions       ) ;
  CHECK( "decision/uuid"       , acceptDecision      ) ;
  CHECK( "decision/uuids"      , acceptDecision      ) ;
  CHECK( "condition/uuid"      , acceptCondition     ) ;
  CHECK( "condition/uuids"     , acceptCondition     ) ;
  CHECK( "execution/uuid"      , acceptExecution     ) ;
  CHECK( "execution/uuids"     , acceptExecution     ) ;
  CHECK( "sql/uuid"            , acceptSqlTable      ) ;
  CHECK( "sql/uuids"           , acceptSqlTable      ) ;
  CHECK( "database/uuid"       , acceptDatabase      ) ;
  CHECK( "database/uuids"      , acceptDatabase      ) ;
  CHECK( "task/uuid"           , acceptTask          ) ;
  CHECK( "task/uuids"          , acceptTask          ) ;
  CHECK( "nation/uuid"         , acceptNation        ) ;
  CHECK( "nation/uuids"        , acceptNation        ) ;
  CHECK( "contour/uuid"        , acceptContour       ) ;
  CHECK( "contour/uuids"       , acceptContour       ) ;
  CHECK( "manifold/uuid"       , acceptManifold      ) ;
  CHECK( "manifold/uuids"      , acceptManifold      ) ;
  CHECK( "source/uuid"         , acceptSources       ) ;
  CHECK( "source/uuids"        , acceptSources       ) ;
  CHECK( "document/uuid"       , acceptDocuments     ) ;
  CHECK( "document/uuids"      , acceptDocuments     ) ;
  CHECK( "eyes/uuid"           , acceptEyes          ) ;
  CHECK( "eyes/uuids"          , acceptEyes          ) ;
  CHECK( "hairs/uuid"          , acceptHairs         ) ;
  CHECK( "hairs/uuids"         , acceptHairs         ) ;
  CHECK( "keyword/uuid"        , acceptKeywords      ) ;
  CHECK( "keyword/uuids"       , acceptKeywords      ) ;
  CHECK( "terminology/uuid"    , acceptTerminologies ) ;
  CHECK( "terminology/uuids"   , acceptTerminologies ) ;
  CHECK( "knowledge/uuid"      , acceptKnowledge     ) ;
  CHECK( "knowledge/uuids"     , acceptKnowledge     ) ;
  CHECK( "field/uuid"          , acceptFields        ) ;
  CHECK( "field/uuids"         , acceptFields        ) ;
  CHECK( "knowledgebase/uuid"  , acceptKnowledgeBase ) ;
  CHECK( "knowledgebase/uuids" , acceptKnowledgeBase ) ;
  CHECK( "sqlcolumn/uuid"      , acceptSqlColumn     ) ;
  CHECK( "sqlcolumn/uuids"     , acceptSqlColumn     ) ;
  CHECK( "commodity/uuid"      , acceptCommodities   ) ;
  CHECK( "commodity/uuids"     , acceptCommodities   ) ;
  CHECK( "organization/uuid"   , acceptOrganizations ) ;
  CHECK( "organization/uuids"  , acceptOrganizations ) ;
  CHECK( "blob/uuid"           , acceptBlobs         ) ;
  CHECK( "blob/uuids"          , acceptBlobs         ) ;
  CHECK( "variable/uuid"       , acceptVariables     ) ;
  CHECK( "variable/uuids"      , acceptVariables     ) ;
  CHECK( "torrent/uuid"        , acceptTorrents      ) ;
  CHECK( "torrent/uuids"       , acceptTorrents      ) ;
  CHECK( "camera/uuid"         , acceptCameras       ) ;
  CHECK( "camera/uuids"        , acceptCameras       ) ;
  CHECK( "face/uuid"           , acceptFaces         ) ;
  CHECK( "face/uuids"          , acceptFaces         ) ;
  CHECK( "star/uuid"           , acceptStars         ) ;
  CHECK( "star/uuids"          , acceptStars         ) ;
  CHECK( "phoneme/uuid"        , acceptPhonemes      ) ;
  CHECK( "phoneme/uuids"       , acceptPhonemes      ) ;
  CHECK( "model/uuid"          , acceptModels        ) ;
  CHECK( "model/uuids"         , acceptModels        ) ;
  CHECK( "reality/uuid"        , acceptReality       ) ;
  CHECK( "reality/uuids"       , acceptReality       ) ;
  CHECK( "colorgroup/uuid"     , acceptColorGroups   ) ;
  CHECK( "colorgroup/uuids"    , acceptColorGroups   ) ;
  CHECK( "setsalgebra/uuid"    , acceptSetsAlgebras  ) ;
  CHECK( "setsalgebra/uuids"   , acceptSetsAlgebras  ) ;
  CHECK( "font/uuid"           , acceptFont          ) ;
  CHECK( "pen/uuids"           , acceptPen           ) ;
  CHECK( "brush/uuid"          , acceptBrush         ) ;
  CHECK( "gradient/uuids"      , acceptGradient      ) ;
  VERIF( hasImage              , acceptImageDrop     ) ;
  VERIF( hasText               , acceptTextDrop      ) ;
  VERIF( hasHtml               , acceptHtmlDrop      ) ;
  VERIF( hasUrls               , acceptUrlsDrop      ) ;
  VERIF( hasColor              , acceptColorDrop     ) ;
  if ( acceptPrivate ( mime ) ) Accepted = true        ;
  #undef  VERIF
  #undef  CHECK
  return Accepted                                      ;
}

bool N::AbstractGui::dropItems(QWidget * source,const QMimeData * mime,QPoint pt)
{
  QPointF pos = pt                  ;
  return dropItems(source,mime,pos) ;
}

bool N::AbstractGui::dropItems(QWidget * source,const QMimeData * mime,QPointF pos)
{
  #define HASD(DUID,FUNCTION) (mime->hasFormat(DUID) && FUNCTION())
  #define DITE(DUID,FUNCTION)                                       \
    QByteArray data   = mime->data ( DUID  ) ;                      \
    SUID       uuid   = GetUuid    ( data  ) ;                      \
    UUIDs      Uuids                         ;                      \
    Uuids << uuid                            ;                      \
    return FUNCTION ( source , pos , Uuids )
  #define SITX(DUID,FUNCTION)                                       \
    QByteArray data   = mime->data ( DUID  ) ;                      \
    UUIDs      Uuids  = GetUuids   ( data  ) ;                      \
    return FUNCTION ( source , pos , Uuids )
  #define SITZ(DUID,FUNCTION)                                       \
    QByteArray data   = mime->data ( DUID  ) ;                      \
    SUID       uuid   = GetUuid    ( data  ) ;                      \
    return FUNCTION ( source , pos , uuid  )
  #define IFCAST(name,Drop,Toss)                                    \
    if (HASD( #name "/uuid" , Drop ))                             { \
        SITZ( #name "/uuid" , Toss )                              ; \
    }
  #define IFBOTH(name,Drop,Toss)                                    \
    if (HASD( #name "/uuid"  , Drop ))                            { \
        DITE( #name "/uuid"  , Toss )                             ; \
    }                                                               \
    if (HASD( #name "/uuids" , Drop ))                            { \
        SITX( #name "/uuids" , Toss )                             ; \
    }
  ///////////////////////////////////////////////////////////////////
  IFBOTH( uuid          , acceptUuids         , dropUuids         ) ;
  IFBOTH( division      , acceptDivisionDrop  , dropDivisions     ) ;
  IFCAST( gender        , acceptGenderDrop    , dropGender        ) ;
  IFBOTH( tag           , acceptTagDrop       , dropTags          ) ;
  IFBOTH( name          , acceptNames         , dropNames         ) ;
  IFBOTH( picture       , acceptPictureDrop   , dropPictures      ) ;
  IFBOTH( people        , acceptPeopleDrop    , dropPeople        ) ;
  IFBOTH( audio         , acceptAudioDrop     , dropAudios        ) ;
  IFBOTH( video         , acceptVideoDrop     , dropVideos        ) ;
  IFBOTH( album         , acceptAlbumDrop     , dropAlbums        ) ;
  IFBOTH( uri           , acceptUriDrop       , dropURIs          ) ;
  IFBOTH( bookmark      , acceptBookmarkDrop  , dropBookmarks     ) ;
  IFBOTH( shape         , acceptShapes        , dropShapes        ) ;
  IFBOTH( member        , acceptMembers       , dropMembers       ) ;
  IFBOTH( set           , acceptSets          , dropSets          ) ;
  IFBOTH( action        , acceptActions       , dropActions       ) ;
  IFBOTH( decision      , acceptDecision      , dropDecision      ) ;
  IFBOTH( condition     , acceptCondition     , dropCondition     ) ;
  IFBOTH( execution     , acceptExecution     , dropExecution     ) ;
  IFBOTH( sql           , acceptSqlTable      , dropSqlTable      ) ;
  IFBOTH( database      , acceptDatabase      , dropDatabase      ) ;
  IFBOTH( task          , acceptTask          , dropTask          ) ;
  IFBOTH( nation        , acceptNation        , dropNation        ) ;
  IFBOTH( contour       , acceptContour       , dropContour       ) ;
  IFBOTH( manifold      , acceptManifold      , dropManifold      ) ;
  IFBOTH( source        , acceptSources       , dropSources       ) ;
  IFBOTH( document      , acceptDocuments     , dropDocuments     ) ;
  IFBOTH( eyes          , acceptEyes          , dropEyes          ) ;
  IFBOTH( hairs         , acceptHairs         , dropHairs         ) ;
  IFBOTH( keyword       , acceptKeywords      , dropKeywords      ) ;
  IFBOTH( terminology   , acceptTerminologies , dropTerminologies ) ;
  IFBOTH( knowledge     , acceptKnowledge     , dropKnowledge     ) ;
  IFBOTH( field         , acceptFields        , dropFields        ) ;
  IFBOTH( knowledgebase , acceptKnowledgeBase , dropKnowledgeBase ) ;
  IFBOTH( sqlcolumn     , acceptSqlColumn     , dropSqlColumn     ) ;
  IFBOTH( commodity     , acceptCommodities   , dropCommodities   ) ;
  IFBOTH( organization  , acceptOrganizations , dropOrganizations ) ;
  IFBOTH( blob          , acceptBlobs         , dropBlobs         ) ;
  IFBOTH( variable      , acceptVariables     , dropVariables     ) ;
  IFBOTH( torrent       , acceptTorrents      , dropTorrents      ) ;
  IFBOTH( camera        , acceptCameras       , dropCameras       ) ;
  IFBOTH( face          , acceptFaces         , dropFaces         ) ;
  IFBOTH( star          , acceptStars         , dropStars         ) ;
  IFBOTH( phoneme       , acceptPhonemes      , dropPhonemes      ) ;
  IFBOTH( model         , acceptModels        , dropModels        ) ;
  IFBOTH( reality       , acceptReality       , dropReality       ) ;
  IFBOTH( colorgroup    , acceptColorGroups   , dropColorGroups   ) ;
  IFBOTH( setsalgebra   , acceptSetsAlgebras  , dropSetsAlgebras  ) ;
  IFCAST( font          , acceptFont          , dropFont          ) ;
  IFCAST( pen           , acceptPen           , dropPen           ) ;
  IFCAST( brush         , acceptBrush         , dropBrush         ) ;
  IFCAST( gradient      , acceptGradient      , dropGradient      ) ;
  ///////////////////////////////////////////////////////////////////
  if (mime->hasImage() && acceptImageDrop())                        {
    QImage image = qvariant_cast<QImage>(mime->imageData())         ;
    return dropImage ( source , pos , image )                       ;
  }                                                                 ;
  if (mime->hasText() && acceptTextDrop())                          {
    return dropText  ( source , pos , mime -> text () )             ;
  }                                                                 ;
  if (mime->hasHtml() && acceptHtmlDrop())                          {
    return dropHtml  ( source , pos , mime -> html () )             ;
  }                                                                 ;
  if (mime->hasUrls() && acceptUrlsDrop())                          {
    return dropUrls  ( source , pos , mime -> urls () )             ;
  }                                                                 ;
  if (mime->hasColor() && acceptColorDrop())                        {
    QColor color = qvariant_cast<QColor>(mime->colorData())         ;
    return dropColor ( source , pos , color )                       ;
  }                                                                 ;
  ///////////////////////////////////////////////////////////////////
  if (acceptPrivate(mime))                                          {
    return dropPrivate ( source , mime , pos )                      ;
  }                                                                 ;
  ///////////////////////////////////////////////////////////////////
  return false                                                      ;
  #undef  IFBOTH
  #undef  IFCAST
  #undef  SITX
  #undef  DITE
  #undef  HASD
}

#define GF(Function,IT)                                      \
bool N::AbstractGui::Function(QWidget * source,QPointF pos,IT) \
{                                                            \
  return false ;                                             \
}

GF( dropText  , const QString     & text  )
GF( dropUrls  , const QList<QUrl> & urls  )
GF( dropImage , const QImage      & image )
GF( dropHtml  , const QString     & html  )
GF( dropColor , const QColor      & color )

#undef  GF

#define DG(FUNCTION)                                                            \
bool N::AbstractGui::FUNCTION(QWidget * source,QPointF pos,const UUIDs & Uuids) \
{                                                                               \
  Q_UNUSED ( source )                                                         ; \
  Q_UNUSED ( pos    )                                                         ; \
  Q_UNUSED ( Uuids  )                                                         ; \
  return false ;                                                                \
}
#define DX(FUNCTION)                                                            \
bool N::AbstractGui::FUNCTION(QWidget * source,QPointF pos,const SUID uuid)     \
{                                                                               \
  Q_UNUSED ( source )                                                         ; \
  Q_UNUSED ( pos    )                                                         ; \
  Q_UNUSED ( uuid   )                                                         ; \
  return false ;                                                                \
}

///////////////////////
DG( dropUuids         )
DG( dropTags          )
DG( dropPictures      )
DG( dropPeople        )
DG( dropAudios        )
DG( dropVideos        )
DG( dropAlbums        )
DG( dropDivisions     )
DG( dropURIs          )
DG( dropBookmarks     )
DG( dropShapes        )
DG( dropMembers       )
DG( dropSets          )
DG( dropActions       )
DG( dropDecision      )
DG( dropCondition     )
DG( dropExecution     )
DG( dropSqlTable      )
DG( dropDatabase      )
DG( dropTask          )
DG( dropNation        )
DG( dropContour       )
DG( dropManifold      )
DG( dropSources       )
DG( dropDocuments     )
DG( dropEyes          )
DG( dropHairs         )
DG( dropKeywords      )
DG( dropTerminologies )
DG( dropKnowledge     )
DG( dropFields        )
DG( dropKnowledgeBase )
DG( dropSqlColumn     )
DG( dropCommodities   )
DG( dropOrganizations )
DG( dropBlobs         )
DG( dropVariables     )
DG( dropTorrents      )
DG( dropCameras       )
DG( dropFaces         )
DG( dropColorGroups   )
DG( dropSetsAlgebras  )
DG( dropNames         )
DG( dropStars         )
DG( dropPhonemes      )
DG( dropModels        )
DG( dropReality       )
///////////////////////
DX( dropGender        )
DX( dropFont          )
DX( dropPen           )
DX( dropBrush         )
DX( dropGradient      )
///////////////////////

#undef  DX
#undef  DG


"""


