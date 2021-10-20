# -*- coding: utf-8 -*-
##############################################################################
## ListWidget
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
from   PyQt5 . QtCore                 import QMimeData
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QDrag
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QToolTip
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QListWidget
from   PyQt5 . QtWidgets              import QListWidgetItem
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . VirtualGui             import VirtualGui as VirtualGui
##############################################################################
class ListWidget      ( QListWidget , VirtualGui                           ) :
  ############################################################################
  pickSelectionMode       = pyqtSignal ( str                                 )
  Leave                   = pyqtSignal ( QWidget                             )
  ############################################################################
  def __init__        ( self , parent = None , plan = None                 ) :
    ##########################################################################
    super (                    ) . __init__ ( parent                         )
    super ( VirtualGui  , self ) . __init__ (                                )
    self . Initialize                       ( self                           )
    self . setPlanFunction                  ( plan                           )
    self . DefaultItemIcon   = QIcon        (                                )
    ##########################################################################
    self . setAttribute                     ( Qt . WA_InputMethodEnabled     )
    self . setAcceptDrops                   ( True                           )
    self . setDragDropMode                  ( QAbstractItemView . DragDrop   )
    self . setHorizontalScrollBarPolicy     ( Qt . ScrollBarAsNeeded         )
    self . setVerticalScrollBarPolicy       ( Qt . ScrollBarAsNeeded         )
    self . setFunction                      ( self . FunctionDocking , False )
    ##########################################################################
    self . pickSelectionMode . connect      ( self . assignSelectionMode     )
    ##########################################################################
    return
  ############################################################################
  def Configure               ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def setDefaultIcon    ( self , icon                                      ) :
    self . DefaultItemIcon = icon
    return self . DefaultItemIcon
  ############################################################################
  def defaultIcon       ( self                                             ) :
    return self . DefaultItemIcon
  ############################################################################
  def focusInEvent      ( self , event                                     ) :
    ##########################################################################
    if                  ( self . focusIn ( event )                         ) :
      return
    ##########################################################################
    super ( QListWidget , self ) . focusInEvent ( event                      )
    ##########################################################################
    return
  ############################################################################
  def focusOutEvent     ( self , event                                     ) :
    ##########################################################################
    if                  ( self . focusOut ( event )                        ) :
      return
    ##########################################################################
    super ( QListWidget , self ) . focusOutEvent ( event                     )
    ##########################################################################
    return
  ############################################################################
  def contextMenuEvent  ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Menu ( event . pos ( ) )                  ) :
      event . accept    (                                                    )
      return
    ##########################################################################
    super ( QListWidget , self ) . contextMenuEvent ( event                  )
    ##########################################################################
    return
  ############################################################################
  def closeEvent        ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Shutdown ( )                              ) :
      event . accept    (                                                    )
      return
    ##########################################################################
    super ( QListWidget , self ) . closeEvent ( event                        )
    ##########################################################################
    return
  ############################################################################
  def resizeEvent       ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Relocation ( )                            ) :
      event . accept    (                                                    )
      return
    ##########################################################################
    super ( QListWidget , self ) . resizeEvent ( event                       )
    ##########################################################################
    return
  ############################################################################
  def showEvent         ( self , event                                     ) :
    ##########################################################################
    super ( QListWidget , self ) . showEvent ( event                         )
    self . Relocation   (                                                    )
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
      super ( QListWidget , self ) . dragEnterEvent ( event                  )
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
      super ( QListWidget , self ) . dragLeaveEvent ( event                  )
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
      super ( QListWidget , self ) . dragMoveEvent ( event                   )
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
      super ( QListWidget , self ) . dropEvent ( event                       )
      return
    ##########################################################################
    event . ignore      (                                                    )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent   ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Dumping                                   ) :
      event . ignore    (                                                    )
      return
    ##########################################################################
    if                  ( self . allowDrag ( self . dragDropMode ( ) )     ) :
      self . dragStart  ( event                                              )
    ##########################################################################
    super ( QListWidget , self ) . mousePressEvent ( event                   )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent    ( self , event                                     ) :
    ##########################################################################
    if                  ( self . Dumping                                   ) :
      event . ignore    (                                                    )
      return
    ##########################################################################
    moving = True
    ##########################################################################
    if                  ( self . allowDrag  ( self . dragDropMode ( ) )    ) :
      if                ( self . dragMoving ( event )                      ) :
        ######################################################################
        event  . accept (                                                    )
        moving = False
        ######################################################################
        super ( QListWidget , self ) . mouseReleaseEvent ( event             )
        ######################################################################
        self   . ReleasePickings (                                           )
    ##########################################################################
    if                  ( moving                                           ) :
      super ( QListWidget , self ) . mouseMoveEvent ( event                  )
    ##########################################################################
    return
  ############################################################################
  def mouseReleaseEvent   ( self , event                                   ) :
    ##########################################################################
    if                    ( self . Dumping                                 ) :
      event . ignore      (                                                  )
      return
    ##########################################################################
    if                    ( self . allowDrag ( self . dragDropMode ( ) )   ) :
      self . dragEnd      ( event                                            )
    ##########################################################################
    if                    ( self . isDrag ( )                              ) :
      ########################################################################
      self  . ReleaseDrag (                                                  )
      event . accept      (                                                  )
      ########################################################################
      return
    ##########################################################################
    super ( QListWidget , self ) . mouseReleaseEvent ( event                 )
    ##########################################################################
    return
  ############################################################################
  def hasDragItem                ( self                                    ) :
    ##########################################################################
    items = self . selectedItems (                                           )
    if                           ( len ( items ) <= 0                      ) :
      return False
    ##########################################################################
    return True
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
    ## return self . dropItems  ( source , mime , pos )
    ##########################################################################
    return False
  ############################################################################
  def CreateDragMime                 ( self , widget , mtype , message     ) :
    ##########################################################################
    items     = self . selectedItems (                                       )
    total     = len                  ( items                                 )
    if                               ( len ( items ) <= 0                  ) :
      return None
    ##########################################################################
    UUIDs     =                      [                                       ]
    for it in items                                                          :
      UUID    = it . data            ( Qt . UserRole                         )
      UUIDs   . append               ( str ( UUID )                          )
    ##########################################################################
    JSONs     =                      { "Widget" : id ( widget )            , \
                                       "UUIDs"  : UUIDs                      }
    ##########################################################################
    mime      = QMimeData            (                                       )
    cit       = self . currentItem   (                                       )
    self      . setMime              ( mime , mtype , JSONs                  )
    ##########################################################################
    if                               ( cit  is not None                    ) :
      icon    = cit . icon           (                                       )
      if                             ( icon is not None                    ) :
        s     = self . iconSize      (                                       )
        image = icon . pixmap ( s ) . toImage ( )
        if                           ( image is not None                   ) :
          mime . setImageData        ( image                                 )
    ##########################################################################
    tooltip   = message . format     ( total                                 )
    QToolTip  . showText             ( QCursor . pos ( ) , tooltip           )
    ##########################################################################
    return mime
  ############################################################################
  @pyqtSlot(str)
  def assignSelectionMode     ( self , mode                                ) :
    ##########################################################################
    mode = mode . lower       (                                              )
    if                        ( mode == "noselection"                      ) :
      self . setSelectionMode ( QAbstractItemView . NoSelection              )
    elif                      ( mode == "singleselection"                  ) :
      self . setSelectionMode ( QAbstractItemView . SingleSelection          )
    elif                      ( mode == "multiselection"                   ) :
      self . setSelectionMode ( QAbstractItemView . MultiSelection           )
    elif                      ( mode == "extendedselection"                ) :
      self . setSelectionMode ( QAbstractItemView . ExtendedSelection        )
    elif                      ( mode == "contiguousselection"              ) :
      self . setSelectionMode ( QAbstractItemView . ContiguousSelection      )
    ##########################################################################
    return
  ############################################################################
  def LocalityMenu                 ( self , mm                             ) :
    ##########################################################################
    DFL    = self  . getLocality   (                                         )
    LANGZ  = self  . getLanguages  (                                         )
    MENUZ  = self  . getMenus      (                                         )
    ##########################################################################
    LOM    = mm    . addMenu       ( MENUZ [ "Language" ]                    )
    ##########################################################################
    KEYs   = LANGZ . keys          (                                         )
    ##########################################################################
    for K in KEYs                                                            :
       msg = LANGZ                 [ K                                       ]
       V   = int                   ( K                                       )
       hid =                       ( V == DFL                                )
       mm  . addActionFromMenu     ( LOM , 10000000 + V , msg , True , hid   )
    ##########################################################################
    return mm
  ############################################################################
  def HandleLocalityMenu           ( self , atId                           ) :
    ##########################################################################
    if                             ( atId < 10000000                       ) :
      return False
    if                             ( atId > 11000000                       ) :
      return False
    ##########################################################################
    self . setLocality             ( atId - 10000000                         )
    ##########################################################################
    return True
  ############################################################################
  def startup                 ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def Shutdown                ( self                                       ) :
    self . Leave . emit       ( self                                         )
    return True
  ############################################################################
  def Relocation              ( self                                       ) :
    return False
  ############################################################################
  def ReleasePickings         ( self                                       ) :
    """
    if (PickedUuids.count()>0)                 {
      setSelections (PickedUuids)              ;
      PickedUuids . clear ( )                  ;
    }                                          ;
    """
    return
  ############################################################################
  def FocusIn                 ( self                                       ) :
    return True
  ############################################################################
  def FocusOut                ( self                                       ) :
    return True
  ############################################################################
  def SelectNone              ( self                                       ) :
    ##########################################################################
    if                        ( self . count ( ) <= 0                      ) :
      return
    ##########################################################################
    m = "清除選取"
    self . Talk               ( m , 1002                                     )
    ##########################################################################
    for i in range            ( 0 , self . count ( )                       ) :
      it = self . item        ( i                                            )
      it . setSelected        ( False                                        )
    ##########################################################################
    return
  ############################################################################
  def SelectAll               ( self                                       ) :
    ##########################################################################
    if                        ( self . count ( ) <= 0                      ) :
      return
    ##########################################################################
    m = "選取全部"
    self . Talk               ( m , 1002                                     )
    ##########################################################################
    for i in range            ( 0 , self . count ( )                       ) :
      it = self . item        ( i                                            )
      it . setSelected        ( True                                         )
    ##########################################################################
    return
  ############################################################################
  def removeParked            ( self                                       ) :
    return True
  ############################################################################
  def InsertItem              ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def DeleteItems             ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def Menu                    ( self , pos                                 ) :
    raise NotImplementedError (                                              )
##############################################################################

"""

class Q_COMPONENTS_EXPORT ListWidget : public QListWidget
                                     , public VirtualGui
                                     , public Thread
{
  Q_OBJECT
  Q_PROPERTY(bool designable READ canDesign WRITE setDesignable DESIGNABLE true)
  public:

    explicit ListWidget              (StandardConstructor) ;
    virtual ~ListWidget              (void);

    virtual QSize   sizeHint         (void) const ;
    QIcon           EmptyIcon        (QSize size) ;
    int             Page             (void) ;
    UUIDs           Selected         (void) ;
    UUIDs           ItemUuids        (void) ;

    virtual void    setDesignable    (bool gui) ;

    virtual QString writeCpp         (void) ;
    virtual QString writeHpp         (void) ;

  protected:

    QListWidgetItem         * ItemEditing    ;
    QWidget                 * ItemWidget     ;
    BMAPs                     EditAttributes ;
    QString                   InheritClass   ;
    UUIDs                     PickedUuids    ;
    QMap<int,ListWidgetItems> ItemMaps       ;
    QMap<int,UUIDs          > UuidMaps       ;

    virtual void paintEvent          (QPaintEvent       * event) ;

    virtual void resizeEvent         (QResizeEvent      * event) ;
    virtual void showEvent           (QShowEvent        * event) ;

    virtual void dragEnterEvent      (QDragEnterEvent   * event) ;
    virtual void dragLeaveEvent      (QDragLeaveEvent   * event) ;
    virtual void dragMoveEvent       (QDragMoveEvent    * event) ;
    virtual void dropEvent           (QDropEvent        * event) ;
    virtual void dragDone            (Qt::DropAction dropIt,QMimeData * mime) ;

    virtual void mousePressEvent     (QMouseEvent       * event) ;
    virtual void mouseMoveEvent      (QMouseEvent       * event) ;
    virtual void mouseReleaseEvent   (QMouseEvent       * event) ;

    virtual void closeEvent          (QCloseEvent       * event) ;
    virtual bool event               (QEvent * event) ;

    virtual void Configure           (void);

    SUID         ItemUuid            (QListWidgetItem * it) ;

    virtual bool acceptDrop          (nDeclWidget,const QMimeData * mime);
    virtual bool dropNew             (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropMoving          (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropAppend          (nDeclWidget,const QMimeData * mime,QPoint pos);

    virtual bool dropFont            (nDeclWidget,QPointF pos,const SUID font ) ;
    virtual bool dropPen             (nDeclWidget,QPointF pos,const SUID pen  ) ;
    virtual bool dropBrush           (nDeclWidget,QPointF pos,const SUID brush) ;

    virtual void assignFont          (Font  & font ) ;
    virtual void assignPen           (Pen   & pen  ) ;
    virtual void assignBrush         (Brush & brush) ;

    virtual void reportItems         (void) ;

    virtual void AdjustMenu          (MenuManager & Menu,QMenu   * adjustment) ;
    virtual bool RunAdjustment       (MenuManager & Menu,QAction * action    ) ;
    virtual void SelectionsMenu      (MenuManager & Menu,QMenu   * SelectMenu) ;
    virtual bool RunSelections       (MenuManager & Menu,QAction * action    ) ;

    virtual bool acceptTapHold       (QTapAndHoldGesture * gesture) ;

    virtual ListWidgetItems New      (UUIDs & Uuids) ;
    virtual bool MoveUuids           (SqlConnection & Connection       ,
                                      Group         & group            ,
                                      UUIDs         & Uuids            ,
                                      RMAPs         & Positions        ,
                                      QString         format = ""      ,
                                      bool            gui    = false ) ;
    virtual bool setUuidsName        (SqlConnection & Connection,int from,int to) ;
    virtual bool setUuidsName        (SqlConnection & Connection) ;
    virtual bool setUuidsNames       (SqlConnection & Connection,int from,int to) ;
    virtual bool setUuidsNames       (SqlConnection & Connection) ;

    virtual void ThreadEvent         (void) ;

    virtual bool Bustle              (void) ;
    virtual bool Vacancy             (void) ;

    virtual void DropInObjects       (ThreadData * data) ;

  private:

  public slots:

    QListWidgetItem * addItem        (SUID Uuid,QString Description,QIcon Icon) ;
    QListWidgetItem * addItem        (SUID Uuid,QIcon Icon,QString text,QString tooltip) ;
    virtual void appendItems         (ListWidgetItems & items) ;

    virtual void MountCommands       (void) ;
    virtual void WaitClear           (void) ;

    virtual bool startup             (void) ;
    virtual bool Shutdown            (void) ;
    virtual bool Relocation          (void) ;

    virtual void CopyToClipboard     (void) ;
    virtual void SelectNone          (void) ;
    virtual void SelectAll           (void) ;
    virtual void setFont             (void) ;
    virtual void Language            (void) ;
    virtual void ModifySpacing       (void) ;
    virtual void AssignGridSize      (void) ;

    virtual void setSelections       (UUIDs & Uuids) ;
    virtual void setSelections       (ListWidgetItems & Items) ;

    virtual void ExportToCpp         (void) ;

    virtual void MoveTo              (QListWidgetItem * at,ListWidgetItems & Items) ;

    virtual void Execute             (int command) ;

    virtual void PageHome            (void) ;
    virtual void PageEnd             (void) ;
    virtual void PageUp              (void) ;
    virtual void PageDown            (void) ;

    virtual bool PageChanged         (int StartId,int PageSize) ;

    virtual QMenu * PageMenu         (MenuManager & menu       ,
                                      QString       total      ,
                                      int         & StartId    ,
                                      int         & PageSize ) ;

  protected slots:

    virtual bool AppMenu             (void) ;
    virtual bool Menu                (QPoint pos);
    virtual void singleClicked       (QListWidgetItem * item) ;
    virtual void doubleClicked       (QListWidgetItem * item) ;
    virtual void DropCommands        (void) ;

    virtual void AtBusy              (void) ;
    virtual void OnRelax             (void) ;

    virtual void setWaitCursor       (void) ;
    virtual void setArrowCursor      (void) ;
    virtual void setEnabling         (bool enable) ;
    virtual void writeSortingEnabled (bool enable) ;
    virtual void writeToolTip        (QString tooltip) ;
    virtual void writeTitle          (QString title) ;
    virtual void cleanItems          (void) ;

    virtual bool RunPageMenu         (MenuManager & menu       ,
                                      QAction     * action     ,
                                      int         & StartId    ,
                                      int         & PageSize ) ;

    virtual void removeListItem      (QListWidgetItem * item) ;

  private slots:

  signals:

    void Adjustment                  (nDeclWidget,QSize size) ;
    void Adjustment                  (nDeclWidget) ;
    void Leave                       (nDeclWidget) ;
    void Command                     (SUID uuid);
    void Selected                    (SUID uuid);
    void assignSelections            (UUIDs & Uuids) ;
    void assignSelections            (ListWidgetItems & Items) ;
    void takeListItem                (QListWidgetItem * item) ;
    void ItemMenu                    (nDeclWidget,QPoint pos);
    void Command                     (nDeclWidget,QString name,SUID uuid);
    void assignToolTip               (QString tooltip) ;
    void assignWindowTitle           (QString tooltip) ;
    void Follow                      (int command) ;
    void assignEnabling              (bool enable) ;
    void assignSortingEnabled        (bool enable) ;
    void assignModified              (bool modified) ;
    void OnBusy                      (void) ;
    void GoRelax                     (void) ;
    void assignWaitCursor            (void) ;
    void assignArrowCursor           (void) ;
    void clearItems                  (void) ;

};

N::ListWidget:: ListWidget  ( QWidget * parent,Plan * p     )
              : QListWidget (           parent              )
              , VirtualGui  (           this  ,       p     )
              , Thread      (           0     ,       false )
              , ItemEditing ( NULL                          )
              , ItemWidget  ( NULL                          )
{
  WidgetClass                     ;
  addIntoWidget ( parent , this ) ;
  Configure     (               ) ;
}

void N::ListWidget::ThreadEvent(void)
{
  plan -> processEvents ( ) ;
}

void N::ListWidget::AtBusy(void)
{
  plan->StartBusy ( ) ;
}

void N::ListWidget::OnRelax(void)
{
  plan->StopBusy ( ) ;
}

void N::ListWidget::setWaitCursor(void)
{
  setCursor ( Qt::WaitCursor ) ;
}

void N::ListWidget::setArrowCursor(void)
{
  setCursor ( Qt::ArrowCursor ) ;
}

bool N::ListWidget::Bustle(void)
{
  Mutex . lock           ( ) ;
  emit assignWaitCursor  ( ) ;
  return true                ;
}

bool N::ListWidget::Vacancy(void)
{
  emit assignArrowCursor ( ) ;
  Mutex . unlock         ( ) ;
  return true                ;
}

void N::ListWidget::setEnabling(bool enable)
{
  setEnabled ( enable ) ;
}

void N::ListWidget::writeSortingEnabled(bool enable)
{
  setSortingEnabled ( enable ) ;
}

void N::ListWidget::writeToolTip(QString tooltip)
{
  setToolTip ( tooltip ) ;
}

void N::ListWidget::writeTitle(QString title)
{
  setWindowTitle ( title )                                           ;
  ////////////////////////////////////////////////////////////////////
  QMdiSubWindow * msw = qobject_cast<QMdiSubWindow *> ( parent ( ) ) ;
  if ( NULL != msw ) msw -> setWindowTitle ( title )                 ;
}

void N::ListWidget::cleanItems(void)
{
  clear ( ) ;
}

QSize N::ListWidget::sizeHint(void) const
{
  return SizeSuggestion ( QSize ( 400 , 320 ) ) ;
}

void N::ListWidget::setDesignable(bool gui)
{
  designable = gui                                     ;
  if (gui)                                             {
    setWindowTitle(tr("N::ListWidget (Editing mode)")) ;
  }                                                    ;
}

void N::ListWidget::paintEvent(QPaintEvent * event)
{
  nIsolatePainter(QListWidget) ;
}

bool N::ListWidget::startup(void)
{
  return true ;
}

QListWidgetItem * N::ListWidget::addItem(SUID uuid,QString Description,QIcon Icon)
{
  NewListWidgetItem         (TWI                         ) ;
  QListWidget::blockSignals (true                        ) ;
  if (Description.length()>0) TWI -> setText (Description) ;
  TWI -> setIcon            (Icon                        ) ;
  TWI -> setData            (Qt::UserRole,uuid           ) ;
  QListWidget::addItem      (TWI                         ) ;
  QListWidget::blockSignals (false                       ) ;
  return TWI                                               ;
}

QListWidgetItem * N::ListWidget::addItem(SUID uuid,QIcon Icon,QString text,QString tooltip)
{
  NewListWidgetItem         (TWI                    ) ;
  QListWidget::blockSignals (true                   ) ;
  if (text   .length()>0) TWI -> setText    (text   ) ;
  if (tooltip.length()>0) TWI -> setToolTip (tooltip) ;
  TWI -> setIcon            (Icon                   ) ;
  TWI -> setData            (Qt::UserRole,uuid      ) ;
  QListWidget::addItem      (TWI                    ) ;
  QListWidget::blockSignals (false                  ) ;
  return TWI                                          ;
}

QIcon N::ListWidget::EmptyIcon(QSize s)
{
  QImage I ( s , QImage::Format_ARGB32 ) ;
  I . fill ( 0                         ) ;
  return QIcon ( QPixmap::fromImage(I) ) ;
}

void N::ListWidget::Configure(void)
{
  setAcceptDrops                ( true                                     ) ;
  setAttribute                  ( Qt::WA_InputMethodEnabled                ) ;
  setDragDropMode               ( DragDrop                                 ) ;
  setHorizontalScrollBarPolicy  ( Qt::ScrollBarAsNeeded                    ) ;
  setVerticalScrollBarPolicy    ( Qt::ScrollBarAsNeeded                    ) ;
  setFunction                   ( N::AttachDock::FunctionDocking , false   ) ;
  ////////////////////////////////////////////////////////////////////////////
  LimitValues [  0 ] =  0                                                    ;
  LimitValues [  1 ] = 48                                                    ;
  LimitValues [  2 ] =  0                                                    ;
  LimitValues [  9 ] = 40                                                    ;
  LimitValues [ 11 ] = (int)Qt::AscendingOrder                               ;
  LimitValues [ 75 ] = 0                                                     ;
  LimitValues [ 76 ] = 100                                                   ;
  LimitValues [ 77 ] = 500                                                   ;
  ////////////////////////////////////////////////////////////////////////////
  addConnector  ( "AssignUUIDs"                                              ,
                  this      , SIGNAL ( assignSelections(UUIDs&))             ,
                  this      , SLOT   ( setSelections   (UUIDs&))           ) ;
  addConnector  ( "AssignItems"                                              ,
                  this      , SIGNAL ( assignSelections(ListWidgetItems&))   ,
                  this      , SLOT   ( setSelections   (ListWidgetItems&)) ) ;
  addConnector  ( "ToolTip"                                                  ,
                  this      , SIGNAL ( assignToolTip  (QString) )            ,
                  this      , SLOT   ( writeToolTip   (QString) )          ) ;
  addConnector  ( "WindowTitle"                                              ,
                  this      , SIGNAL ( assignWindowTitle (QString) )         ,
                  this      , SLOT   ( writeTitle        (QString) )       ) ;
  addConnector  ( "Execute"                                                  ,
                  this      , SIGNAL ( Follow         (int) )                ,
                  this      , SLOT   ( Execute        (int) )              ) ;
  addConnector  ( "Enabling"                                                 ,
                  this      , SIGNAL ( assignEnabling (bool) )               ,
                  this      , SLOT   ( setEnabling    (bool) )             ) ;
  addConnector  ( "Sorting"                                                  ,
                  this      , SIGNAL ( assignSortingEnabled (bool) )         ,
                  this      , SLOT   ( writeSortingEnabled  (bool) )       ) ;
  addConnector  ( "Modification"                                             ,
                  this      , SIGNAL ( assignModified    (bool) )            ,
                  this      , SLOT   ( setWindowModified (bool) )          ) ;
  addConnector  ( "Busy"                                                     ,
                  this      , SIGNAL ( OnBusy       ( ) )                    ,
                  this      , SLOT   ( AtBusy       ( ) )                  ) ;
  addConnector  ( "Relax"                                                    ,
                  this      , SIGNAL ( GoRelax      ( ) )                    ,
                  this      , SLOT   ( OnRelax      ( ) )                  ) ;
  addConnector  ( "WaitCursor"                                               ,
                  this      , SIGNAL ( assignWaitCursor  ( ) )               ,
                  this      , SLOT   ( setWaitCursor     ( ) )             ) ;
  addConnector  ( "ArrowCursor"                                              ,
                  this      , SIGNAL ( assignArrowCursor ( ) )               ,
                  this      , SLOT   ( setArrowCursor    ( ) )             ) ;
  addConnector  ( "Cleanup"                                                  ,
                  this      , SIGNAL( clearItems         ( ) )               ,
                  this      , SLOT  ( cleanItems         ( ) )             ) ;
  addConnector  ( "Removal"                                                  ,
                  this      , SIGNAL( takeListItem   (QListWidgetItem*) )    ,
                  this      , SLOT  ( removeListItem (QListWidgetItem*) )  ) ;
  addConnector  ( "Commando"                                                 ,
                  Commando                                                   ,
                  SIGNAL ( timeout      ( ) )                                ,
                  this                                                       ,
                  SLOT   ( DropCommands ( ) )                              ) ;
  onlyConnector ( "AssignUUIDs"                                            ) ;
  onlyConnector ( "AssignItems"                                            ) ;
  onlyConnector ( "ToolTip"                                                ) ;
  onlyConnector ( "WindowTitle"                                            ) ;
  onlyConnector ( "Execute"                                                ) ;
  onlyConnector ( "Enabling"                                               ) ;
  onlyConnector ( "Modification"                                           ) ;
  onlyConnector ( "Sorting"                                                ) ;
  onlyConnector ( "Busy"                                                   ) ;
  onlyConnector ( "Relax"                                                  ) ;
  onlyConnector ( "WaitCursor"                                             ) ;
  onlyConnector ( "ArrowCursor"                                            ) ;
  onlyConnector ( "Cleanup"                                                ) ;
  onlyConnector ( "Removal"                                                ) ;
  onlyConnector ( "Commando"                                               ) ;
  ////////////////////////////////////////////////////////////////////////////
  if ( NotNull ( plan ) )                                                    {
    Data . Controller = & ( plan->canContinue )                              ;
  }                                                                          ;
}

N::ListWidgetItems N::ListWidget::New(UUIDs & Uuids)
{
  ListWidgetItems Items                ;
  SUID            u                    ;
  foreach (u,Uuids)                    {
    QListWidgetItem * it               ;
    it  = new QListWidgetItem ( )      ;
    it -> setData ( Qt::UserRole , u ) ;
    Items << it                        ;
  }                                    ;
  return Items                         ;
}

void N::ListWidget::appendItems(ListWidgetItems & Items)
{
  for (int i=0;i<Items.count();i++)        {
    QListWidget :: addItem ( Items [ i ] ) ;
    plan -> processEvents ( )              ;
  }                                        ;
}

SUID N::ListWidget::ItemUuid(QListWidgetItem * it)
{
  return nListUuid ( it ) ;
}

int N::ListWidget::Page(void)
{
  QSize g = gridSize()                                       ;
  QSize s = size()                                           ;
  return ( (s.width()/g.width()) * (s.height()/g.height()) ) ;
}

UUIDs N::ListWidget::Selected(void)
{
  UUIDs Uuids                     ;
  for (int i=0;i<count();i++)     {
    if (item(i)->isSelected())    {
      Uuids << nListUuid(item(i)) ;
    }                             ;
  }                               ;
  return Uuids                    ;
}

UUIDs N::ListWidget::ItemUuids(void)
{
  UUIDs Uuids                   ;
  for (int i=0;i<count();i++)   {
    Uuids << nListUuid(item(i)) ;
  }                             ;
  return Uuids                  ;
}

void N::ListWidget::singleClicked(QListWidgetItem * item)
{
  SUID uuid = nListUuid ( item ) ;
  emit Selected         ( uuid ) ;
}

void N::ListWidget::doubleClicked(QListWidgetItem * item)
{
  SUID uuid = nListUuid ( item              ) ;
  emit Command ( uuid                       ) ;
  emit Command ( this , item->text() , uuid ) ;
}

void N::ListWidget::MountCommands(void)
{
  nConnect(this,SIGNAL(itemClicked      (QListWidgetItem*))   ,
           this,SLOT  (singleClicked    (QListWidgetItem*)) ) ;
  nConnect(this,SIGNAL(itemDoubleClicked(QListWidgetItem*))   ,
           this,SLOT  (doubleClicked    (QListWidgetItem*)) ) ;
}

void N::ListWidget::CopyToClipboard(void)
{
  QListWidgetItem * LWI = currentItem () ;
  if (IsNull(LWI)) return                ;
  QString text = LWI -> text ()          ;
  qApp -> clipboard() -> setText (text)  ;
  QString m                              ;
  m = tr("duplicate text to clipboard")  ;
  plan->Talk(m)                          ;
}

void N::ListWidget::SelectNone(void)
{
  QString m                        ;
  m = tr("Clear selections")       ;
  plan->Talk(m)                    ;
  nFullLoop(i,count())             {
    QListWidgetItem * it = item(i) ;
    it->setSelected ( false )      ;
  }                                ;
}

void N::ListWidget::SelectAll(void)
{
  QString m                        ;
  m = tr("Select all items")       ;
  plan->Talk(m)                    ;
  nFullLoop(i,count())             {
    QListWidgetItem * it = item(i) ;
    it->setSelected ( true  )      ;
  }                                ;
}

void N::ListWidget::setFont(void)
{
  changeFont ( ) ;
}

void N::ListWidget::Language(void)
{
  AbstractGui::assignLanguage ( this ) ;
}

bool N::ListWidget::dropFont(QWidget * source,QPointF pos,const SUID font)
{ Q_UNUSED           ( source               ) ;
  Q_UNUSED           ( pos                  ) ;
  nKickOut           ( IsNull(plan) , false ) ;
  Font            f                           ;
  GraphicsManager GM ( plan                 ) ;
  EnterSQL           ( SC , plan->sql       ) ;
    f = GM.GetFont   ( SC , font            ) ;
  LeaveSQL           ( SC , plan->sql       ) ;
  assignFont         ( f                    ) ;
  return true                                 ;
}

bool N::ListWidget::dropPen(QWidget * source,QPointF pos,const SUID pen)
{ Q_UNUSED            ( source               ) ;
  Q_UNUSED            ( pos                  ) ;
  nKickOut            ( IsNull(plan) , false ) ;
  Pen             p                          ;
  GraphicsManager GM  ( plan                 ) ;
  EnterSQL            ( SC , plan->sql       ) ;
    p = GM.GetPen     ( SC , pen             ) ;
  LeaveSQL            ( SC , plan->sql       ) ;
  assignPen           ( p                    ) ;
  return true                                  ;
}

bool N::ListWidget::dropBrush(QWidget * source,QPointF pos,const SUID brush)
{ Q_UNUSED           ( source               ) ;
  Q_UNUSED           ( pos                  ) ;
  nKickOut           ( IsNull(plan) , false ) ;
  Brush           b                           ;
  GraphicsManager GM ( plan                 ) ;
  EnterSQL           ( SC , plan->sql       ) ;
    b = GM.GetBrush  ( SC , brush           ) ;
  LeaveSQL           ( SC , plan->sql       ) ;
  assignBrush        ( b                    ) ;
  return true                                 ;
}

void N::ListWidget::assignFont(Font & f)
{
  QListWidget::setFont ( f ) ;
}

void N::ListWidget::assignPen(Pen & p)
{ Q_UNUSED ( p ) ;
}

void N::ListWidget::assignBrush(Brush & brush)
{
  QBrush   B   = brush                            ;
  QPalette P   = palette (                      ) ;
  P . setBrush           ( QPalette::Base , B   ) ;
  setPalette             ( P                    ) ;
}

void N::ListWidget::reportItems(void)
{
  QString m                                 ;
  m = tr ( "%1 items" ) . arg ( count ( ) ) ;
  emit assignToolTip          ( m         ) ;
  plan -> Talk                ( m         ) ;
}

void N::ListWidget::ModifySpacing(void)
{
  int  s    = spacing ( )  ;
  bool okay = true         ;
  s = QInputDialog::getInt (
        this               ,
        windowTitle()      ,
        tr("Spacing")      ,
        s                  ,
        0                  ,
        120                ,
        1                  ,
        &okay            ) ;
  if (okay)                {
    setSpacing ( s     )   ;
    Alert      ( Done  )   ;
  } else                   {
    Alert      ( Error )   ;
  }                        ;
}

void N::ListWidget::AssignGridSize(void)
{
  QSize   gs = gridSize()                       ;
  QSize   ns                                    ;
  QString ms                                    ;
  ms = tr("Grid size of %1").arg(windowTitle()) ;
  if (getGridSize(this,ms,gs,ns))               {
    setGridSize(ns)                             ;
  }                                             ;
}

void N::ListWidget::setSelections(UUIDs & Uuids)
{
  for (int i=0;i<count();i++)           {
    QListWidgetItem * it = item ( i )   ;
    if (NotNull(it))                    {
      SUID u = nListUuid(it)            ;
      bool selected = Uuids.contains(u) ;
      it->setSelected(selected)         ;
    }                                   ;
  }                                     ;
}

void N::ListWidget::setSelections(ListWidgetItems & Items)
{
  for (int i=0;i<Items.count();i++)     {
    Items [ i ] -> setSelected ( true ) ;
  }                                     ;
}

void N::ListWidget::MoveTo(QListWidgetItem * at,ListWidgetItems & Items)
{
  int StartId = 0                     ;
  int Total   = Items.count()         ;
  nDropOut ( Total <= 0 )             ;
  if (Items.contains(at)) return      ;
  /////////////////////////////////////
  for (int i=0;i<Total;i++)           {
    int r = row(Items[i])             ;
    if (r>=0) takeItem(r)             ;
  }                                   ;
  /////////////////////////////////////
  if (NotNull(at))                    {
    StartId = row(at)                 ;
  }                                   ;
  /////////////////////////////////////
  for (int i=0;i<Total;i++,StartId++) {
    insertItem(StartId,Items[i])      ;
  }                                   ;
}

void N::ListWidget::AdjustMenu(MenuManager & mm,QMenu * me)
{
  mm . addSeparator ( me                                  ) ;
  mm . add          ( me , 90203 , tr("Set font"        ) ) ;
  mm . add          ( me , 90204 , tr("Set spacing"     ) ) ;
  mm . add          ( me , 90205 , tr("Set grid size"   ) ) ;
  mm . add          ( me , 90206 , tr("Set minimum size") ) ;
  mm . add          ( me , 90207 , tr("Set maximum size") ) ;
  mm . add          ( me , 90208 , tr("Set style sheet" ) ) ;
}

bool N::ListWidget::RunAdjustment(MenuManager & Menu,QAction * action)
{
  switch (Menu[action])                                                  {
    nFastCast ( 90203 , setFont           (                          ) ) ;
    nFastCast ( 90204 , ModifySpacing     (                          ) ) ;
    nFastCast ( 90205 , AssignGridSize    (                          ) ) ;
    nFastCast ( 90206 , assignMinimumSize ( this                     ) ) ;
    nFastCast ( 90207 , assignMaximumSize ( this                     ) ) ;
    nFastCast ( 90208 , assignStyleSheet  ( tr("Style sheet") , this ) ) ;
    default: return false                                                ;
  }                                                                      ;
  return true                                                            ;
}

void N::ListWidget::SelectionsMenu(MenuManager & Menu,QMenu * me)
{
  Menu . add ( me , 90402 , tr("Select all" ) ) ;
  Menu . add ( me , 90403 , tr("Select none") ) ;
}

bool N::ListWidget::RunSelections(MenuManager & Menu,QAction * action)
{
  switch (Menu[action])                  {
    nFastCast ( 90402 , SelectAll  ( ) ) ;
    nFastCast ( 90403 , SelectNone ( ) ) ;
    default: return false                ;
  }                                      ;
  return true                            ;
}

bool N::ListWidget::MoveUuids    (
       SqlConnection & SC        ,
       Group         & group     ,
       UUIDs         & Uuids     ,
       RMAPs         & Positions ,
       QString         format    ,
       bool            gui       )
{
  ScopedProgress * pb = NULL                     ;
  int              t  = Uuids.count()            ;
  bool             s  = gui                      ;
  QString          Q                             ;
  SUID             u                             ;
  if ( s && t < 100 ) s = false                  ;
  ////////////////////////////////////////////////
  if ( s )                                       {
    pb  = new ScopedProgress                     (
                plan                             ,
                format                           ,
                10                             ) ;
    pb -> setRange ( 0 , t )                     ;
  }                                              ;
  ////////////////////////////////////////////////
  int pid = 0                                    ;
  int Id                                         ;
  startLoading ( )                               ;
  while (isLoading() && pid<Uuids.count())       {
    u  = Uuids     [ pid ]                       ;
    Id = Positions [ u   ]                       ;
    pid ++                                       ;
    Q = SC . sql . Update                        (
          PlanTable(Groups)                      ,
          SC . sql . Where                       (
            5                                    ,
            "first"                              ,
            "second"                             ,
            "t1"                                 ,
            "t2"                                 ,
            "relation"                         ) ,
          1                                      ,
          "position"                           ) ;
    SC . Prepare ( Q                           ) ;
    SC . Bind    ( "first"    , group.first    ) ;
    SC . Bind    ( "second"   , u              ) ;
    SC . Bind    ( "t1"       , group.t1       ) ;
    SC . Bind    ( "t2"       , group.t2       ) ;
    SC . Bind    ( "relation" , group.relation ) ;
    SC . Bind    ( "position" , Id             ) ;
    SC . Exec    (                             ) ;
    if (NotNull(pb))                             {
      ++(*pb)                                    ;
      plan -> processEvents ( )                  ;
    }                                            ;
  }                                              ;
  stopLoading ( )                                ;
  if (NotNull(pb)) delete pb                     ;
  return true                                    ;
}

bool N::ListWidget::setUuidsName(SqlConnection & SC,int from,int to)
{
  int i = from                 ;
  int L = -1                   ;
  if (LimitValues.contains(9)) {
    L = LimitValues [ 9 ]      ;
  }                            ;
  startLoading ( )             ;
  while (isLoading() && i<to)  {
    QListWidgetItem * it       ;
    SUID              u        ;
    it = item      ( i  )      ;
    u  = nListUuid ( it )      ;
    i++                        ;
    if (u>0)                   {
      QString n                ;
      n = SC . getName         (
            PlanTable(Names)   ,
            "uuid"             ,
            vLanguageId        ,
            u                ) ;
      if (n.length()>0)        {
        if (L>0)               {
          if (n.length()>L)    {
            n = n . left ( L ) ;
            n += " ..."        ;
          }                    ;
        }                      ;
        it -> setText  ( n )   ;
      }                        ;
    }                          ;
  }                            ;
  stopLoading  ( )             ;
  return true                  ;
}

bool N::ListWidget::setUuidsName(SqlConnection & SC)
{
  return setUuidsName ( SC , 0 , count ( ) ) ;
}

bool N::ListWidget::setUuidsNames(SqlConnection & SC,int from,int to)
{
  int i = from                   ;
  int L = -1                     ;
  if (LimitValues.contains(9))   {
    L = LimitValues [ 9 ]        ;
  }                              ;
  startLoading ( )               ;
  while (isLoading() && i<to)    {
    QListWidgetItem * it         ;
    SUID              u          ;
    it = item      ( i  )        ;
    u  = nListUuid ( it )        ;
    i++                          ;
    if (u>0)                     {
      UUIDs U                    ;
      Manager :: NameUuids       (
        *plan                    ,
        SC                       ,
        u                        ,
        U                      ) ;
      if (U.count()>0)           {
        QString n = ""           ;
        UUIDs   X                ;
        NAMEs   N                ;
        X << U [ 0 ]             ;
        Manager :: UuidNames     (
          *plan                  ,
          SC                     ,
          X                      ,
          N                    ) ;
        if (N.contains(U[0]))    {
          n = N [ U [ 0 ] ]      ;
        }                        ;
        if (n.length()>0)        {
          if (L>0)               {
            if (n.length()>L)    {
              n = n . left ( L ) ;
              n += " ..."        ;
            }                    ;
          }                      ;
          it -> setText  ( n )   ;
        }                        ;
      }                          ;
    }                            ;
  }                              ;
  stopLoading  ( )               ;
  return true                    ;
}

bool N::ListWidget::setUuidsNames(SqlConnection & SC)
{
  return setUuidsNames ( SC , 0 , count ( ) ) ;
}

QString N::ListWidget::writeCpp(void)
{
  #define NL C << ""
  #define NB C << "  "
  QStringList C                                                                ;
  QString     I = InheritClass                                                 ;
  int         L = I.length()                                                   ;
  QString     S = " "                                                          ;
  int         DD = 0                                                           ;
  S = S.repeated(L)                                                            ;
  return C.join("\n")                                                          ;
  #undef NL
  #undef NB
}

QString N::ListWidget::writeHpp(void)
{
  #define NL H << ""
  #define NB H << "    "
  QStringList H                                                                ;
  QString     I = InheritClass                                                 ;
  QString     U = I.toUpper()                                                  ;
  return H.join("\n")                                                          ;
  #undef NL
  #undef NB
}

void N::ListWidget::ExportToCpp(void)
{
  nDropOut ( InheritClass.length()<=0 )                 ;
  QString d = QFileDialog::getExistingDirectory         (
                this                                    ,
                tr("Export to C++ directory")           ,
                plan->Path("Development")               ,
                QFileDialog::ShowDirsOnly               |
                QFileDialog::DontResolveSymlinks      ) ;
  nDropOut ( d.length() <= 0 )                          ;
  QDir    D ( d )                                       ;
  QString N   = D.dirName( )                            ;
  QString Hpp = writeHpp ( )                            ;
  QString Cpp = writeCpp ( )                            ;
  QString H   = QString("%1.hpp").arg(InheritClass)     ;
  QString C   = QString("%1.cpp").arg(InheritClass)     ;
  QByteArray h = Hpp.toUtf8()                           ;
  QByteArray c = Cpp.toUtf8()                           ;
  QString HF   = D.absoluteFilePath(H)                  ;
  QString CF   = D.absoluteFilePath(C)                  ;
  File::toFile(HF,h)                                    ;
  File::toFile(CF,c)                                    ;
  N = N + ".pri"                                        ;
  N = D.absoluteFilePath(N)                             ;
  QFile F(N)                                            ;
  if (F.exists())                                       {
    QByteArray PRI                                      ;
    if (File::toByteArray(N,PRI))                       {
      QString P = QString::fromUtf8(PRI)                ;
      P.append("\n")                                    ;
      P.append(QString("HEADERS += $${PWD}/%1").arg(H)) ;
      P.append("\n")                                    ;
      P.append("\n")                                    ;
      P.append(QString("SOURCES += $${PWD}/%1").arg(C)) ;
      P.append("\n")                                    ;
      PRI = P.toUtf8()                                  ;
      File::toFile(N,PRI)                               ;
    }                                                   ;
  }                                                     ;
  Alert ( Done )                                        ;
}

void N::ListWidget::DropInObjects(ThreadData * data)
{
}

bool N::ListWidget::AppMenu(void)
{
  return Menu(QCursor::pos()) ;
}

bool N::ListWidget::Menu(QPoint pos)
{
  if (!designable)                                        {
    emit ItemMenu ( this , pos )                          ;
    return true                                           ;
  }                                                       ;
  /////////////////////////////////////////////////////////
  MenuManager       mm(this)                             ;
  QMenu            * mp                                   ;
  QMenu            * me                                   ;
  QMenu            * ms                                   ;
  QMenu            * mf                                   ;
  QAction          * aa                                   ;
  bool               singleClick = false                  ;
  bool               doubleClick = false                  ;
  bool               doDrag      = false                  ;
  bool               doDrop      = false                  ;
  bool               doDock      = false                  ;
  #define GB(N,ID)                                        \
    if (EditAttributes.contains(ID))                    { \
      N = EditAttributes[ID]                            ; \
    }
  GB ( singleClick , 11 )                                 ;
  GB ( doubleClick , 12 )                                 ;
  GB ( doDrag      , 13 )                                 ;
  GB ( doDrop      , 14 )                                 ;
  GB ( doDock      , 15 )                                 ;
  #undef  GB
  mm.add(101,tr("Assign class name"))                     ;
  mm.add(103,tr("Add test items"   ))                     ;
  mm.add(104,tr("Clear items"      ))                     ;
  mm.addSeparator()                                       ;
  mp = mm.addMenu(tr("Properties"))                       ;
  ms = mm.addMenu(tr("Styles"    ))                       ;
  mf = mm.addMenu(tr("Inherits"  ))                       ;
  mm.add(ms,311,tr("Set window title" ))                  ;
  mm.add(ms,302,tr("Set editor"       ))                  ;
  mm.add(ms,303,tr("Single clicked"   ),true,singleClick) ;
  mm.add(ms,304,tr("Double clicked"   ),true,doubleClick) ;
  mm.add(ms,305,tr("Drag"             ),true,doDrag     ) ;
  mm.add(ms,306,tr("Drop"             ),true,doDrop     ) ;
  mm.add(ms,307,tr("Dock"             ),true,doDock     ) ;
  mm.add(mf,401,tr("Classes"          )                 ) ;
  mm.add(mf,402,tr("Functions"        )                 ) ;
  if (InheritClass.length()>0)                            {
    me = mm.addMenu(tr("Export"       ))                  ;
    mm.add(me,901,tr("Export to C++"))                    ;
  }                                                       ;
  mm . setFont(plan)                                      ;
  aa = mm.exec()                                          ;
  if (IsNull(aa)) return true                             ;
  int  columns                                            ;
  bool okay = false                                       ;
  QString ncName                                          ;
  switch (mm[aa])                                         {
    case 101                                              :
      ncName = QInputDialog::getText                      (
                 this                                     ,
                 tr("Set class name")                     ,
                 tr("Class name:")                        ,
                 QLineEdit::Normal                        ,
                 InheritClass                             ,
                 &okay                                  ) ;
      if (okay)                                           {
        InheritClass = ncName                             ;
        setWindowTitle(InheritClass)                      ;
      }                                                   ;
    break                                                 ;
    case 103                                              :
      columns = QInputDialog::getInt                      (
                  this                                    ,
                  tr("Test items")                        ,
                  tr("Items:")                            ,
                  1                                       ,
                  1,10000,1,&okay                       ) ;
      if (okay)                                           {
      }                                                   ;
    break                                                 ;
    case 104                                              :
      clear ( )                                           ;
    break                                                 ;
    case 302                                              :
    break                                                 ;
    case 303                                              :
      EditAttributes[11] = aa->isChecked()                ;
    break                                                 ;
    case 304                                              :
      EditAttributes[12] = aa->isChecked()                ;
    break                                                 ;
    case 305                                              :
      EditAttributes[13] = aa->isChecked()                ;
    break                                                 ;
    case 306                                              :
      EditAttributes[14] = aa->isChecked()                ;
    break                                                 ;
    case 307                                              :
      EditAttributes[15] = aa->isChecked()                ;
    break                                                 ;
    case 311                                              :
      ncName = QInputDialog::getText                      (
                 this                                     ,
                 tr("Set window title")                   ,
                 tr("Title:")                             ,
                 QLineEdit::Normal                        ,
                 windowTitle()                            ,
                 &okay                                  ) ;
      if (okay)                                           {
        setWindowTitle(ncName)                            ;
      }                                                   ;
    break                                                 ;
    case 401                                              :
    break                                                 ;
    case 402                                              :
    break                                                 ;
    case 901                                              :
      ExportToCpp ( )                                     ;
    break                                                 ;
  }                                                       ;
  return true                                             ;
}

void N::ListWidget::DropCommands(void)
{
  LaunchCommands ( ) ;
}

void N::ListWidget::Execute(int command)
{
  start ( command ) ;
}

QMenu * N::ListWidget::PageMenu  (
          MenuManager & mm       ,
          QString       total    ,
          int         & StartId  ,
          int         & PageSize )
{
  if ( isLoading ( )          ) return NULL                     ;
  if ( LimitValues [ 2 ] <= 0 ) return NULL                     ;
  ///////////////////////////////////////////////////////////////
  QMenu   * mp  = NULL                                          ;
  QAction * aa  = NULL                                          ;
  SpinBox * spb = NULL                                          ;
  SpinBox * spp = NULL                                          ;
  QString   tms = QString ( total ) . arg ( LimitValues [ 2 ] ) ;
  ///////////////////////////////////////////////////////////////
  StartId  = LimitValues [ 0 ]                                  ;
  PageSize = LimitValues [ 1 ]                                  ;
  spb      = new SpinBox  ( NULL , plan                       ) ;
  spp      = new SpinBox  ( NULL , plan                       ) ;
  spb     -> setRange     ( 0    , LimitValues [ 2 ]          ) ;
  spp     -> setRange     ( 0    , LimitValues [ 2 ]          ) ;
  spb     -> setValue     ( StartId                           ) ;
  spp     -> setValue     ( PageSize                          ) ;
  mp       = mm . addMenu ( tr("Page")                        ) ;
  aa       = mm . add     ( mp , 90551 , tms                  ) ;
  aa      -> setEnabled   ( false                             ) ;
  mm       . addSeparator ( mp                                ) ;
  mm       . add          ( mp , 90560 , tr("View all"     )  ) ;
  mm       . add          ( mp , 90561 , tr("Home"         )  ) ;
  mm       . add          ( mp , 90562 , tr("Previous page")  ) ;
  mm       . add          ( mp , 90563 , tr("Next page"    )  ) ;
  mm       . add          ( mp , 90564 , tr("End page"     )  ) ;
  mm       . addSeparator ( mp                                ) ;
  mm       . add          ( mp , 90571 , spb                  ) ;
  mm       . add          ( mp , 90572 , spp                  ) ;
  ///////////////////////////////////////////////////////////////
  if ( isFunction ( 1004 ) )                                    {
    SpinBox * spt = NULL                                        ;
    spt  = new SpinBox  ( NULL , plan                         ) ;
    spt -> setRange     ( 0    , 1000                         ) ;
    spt -> setValue     ( LimitValues [ 9 ]                   ) ;
    spt -> setAlignment ( Qt::AlignRight|Qt::AlignVCenter     ) ;
    spt -> setPrefix    ( tr("Text length : ")                ) ;
    mm   . add          ( mp , 90573 , spt                    ) ;
  }                                                             ;
  ///////////////////////////////////////////////////////////////
  spb     -> External = &StartId                                ;
  spp     -> External = &PageSize                               ;
  ///////////////////////////////////////////////////////////////
  spb     -> setAlignment ( Qt::AlignRight|Qt::AlignVCenter   ) ;
  spp     -> setAlignment ( Qt::AlignRight|Qt::AlignVCenter   ) ;
  spb     -> setPrefix    ( tr("Start ID : "   )              ) ;
  spp     -> setPrefix    ( tr("Page size : "  )              ) ;
  ///////////////////////////////////////////////////////////////
  return mp                                                     ;
}

bool N::ListWidget::RunPageMenu (
       MenuManager & mm       ,
       QAction     * aa       ,
       int         & StartId  ,
       int         & PageSize )
{
  if ( isFunction ( 1004 ) )                {
    SpinBox * spt = NULL                    ;
    spt = (SpinBox *) mm . widget ( 90573 ) ;
    if ( NotNull ( spt ) )                  {
      LimitValues [ 9 ] = spt -> value ( )  ;
    }                                       ;
  }                                         ;
  ///////////////////////////////////////////
  switch ( mm [ aa ] )                      {
    case 90560                              :
      StartId  = 0                          ;
      PageSize = LimitValues [ 2 ]          ;
    break                                   ;
    case 90561                              :
      StartId = 0                           ;
    break                                   ;
    case 90562                              :
      StartId -= PageSize                   ;
      if ( StartId < 0 ) StartId = 0        ;
    break                                   ;
    case 90563                              :
      StartId += PageSize                   ;
      if ( StartId >= LimitValues [ 2 ] )   {
        StartId = LimitValues [ 2 ] - 1     ;
      }                                     ;
    break                                   ;
    case 90564                              :
      StartId  = LimitValues [ 2 ]          ;
      StartId -= PageSize                   ;
      if ( StartId < 0 ) StartId = 0        ;
    break                                   ;
    default                                 :
    return false                            ;
  }                                         ;
  return true                               ;
}

bool N::ListWidget::PageChanged(int StartId,int PageSize)
{
  if (isLoading()) return false             ;
  if ( ( StartId  != LimitValues [ 0 ] )   ||
       ( PageSize != LimitValues [ 1 ] )  ) {
    LimitValues [ 0 ] = StartId             ;
    LimitValues [ 1 ] = PageSize            ;
    if ( 0 == LimitValues [ 1 ] )           {
      LimitValues [ 1 ] = LimitValues [ 2 ] ;
    }                                       ;
    startup ( )                             ;
    return true                             ;
  }                                         ;
  return false                              ;
}

void N::ListWidget::PageHome(void)
{
  if ( ! isStopped ( )        ) return    ;
  if ( 0 == LimitValues [ 0 ] ) return    ;
  LimitValues [ 0 ] = 0                   ;
  if ( 0 == LimitValues [ 1 ] )           {
    LimitValues [ 1 ] = LimitValues [ 2 ] ;
  }                                       ;
  startup ( )                             ;
}

void N::ListWidget::PageEnd(void)
{
  if ( ! isStopped ( ) ) return           ;
  int StartId  = LimitValues [ 2 ]        ;
  if ( 0 == LimitValues [ 1 ] )           {
    LimitValues [ 1 ] = LimitValues [ 2 ] ;
  }                                       ;
  StartId            -= LimitValues [ 1 ] ;
  if ( StartId < 0 ) StartId = 0          ;
  LimitValues [ 0 ] = StartId             ;
  startup ( )                             ;
}

void N::ListWidget::PageUp(void)
{
  if ( ! isStopped ( ) ) return            ;
  if ( 0 == LimitValues [ 1 ] )            {
    LimitValues [ 1 ]  = LimitValues [ 2 ] ;
  }                                        ;
  LimitValues   [ 0 ] -= LimitValues [ 1 ] ;
  if ( LimitValues [ 0 ] < 0 )             {
    LimitValues [ 0 ] = 0                  ;
  }                                        ;
  startup ( )                              ;
}

void N::ListWidget::PageDown(void)
{
  if ( ! isStopped ( ) ) return                 ;
  if ( 0 == LimitValues [ 1 ] )                 {
    LimitValues [ 1 ]  = LimitValues [ 2 ]      ;
  }                                             ;
  LimitValues   [ 0 ] += LimitValues [ 1 ]      ;
  if ( LimitValues [ 0 ] >= LimitValues [ 2 ] ) {
    LimitValues [ 0 ]  = LimitValues [ 2 ] - 1  ;
  }                                             ;
  startup ( )                                   ;
}

void N::ListWidget::WaitClear(void)
{
  emit clearItems ( )                           ;
  while ( ( count ( ) > 0 ) && NotStopped ( ) ) {
    Time::skip ( 10 )                           ;
  }                                             ;
}

void N::ListWidget::removeListItem(QListWidgetItem * item)
{
  int r = row ( item ) ;
  if ( r < 0 ) return  ;
  takeItem ( r )       ;
}

"""
