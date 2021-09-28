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
from   PyQt5                           import QtCore
from   PyQt5                           import QtGui
from   PyQt5                           import QtWidgets
##############################################################################
from   PyQt5 . QtCore                  import QObject
from   PyQt5 . QtCore                  import pyqtSignal
from   PyQt5 . QtCore                  import Qt
from   PyQt5 . QtCore                  import QPoint
from   PyQt5 . QtCore                  import QPointF
##############################################################################
from   PyQt5 . QtGui                   import QIcon
from   PyQt5 . QtGui                   import QCursor
from   PyQt5 . QtGui                   import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets               import QApplication
from   PyQt5 . QtWidgets               import QWidget
from   PyQt5 . QtWidgets               import qApp
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QAction
from   PyQt5 . QtWidgets               import QShortcut
from   PyQt5 . QtWidgets               import QMenu
from   PyQt5 . QtWidgets               import QTreeWidget
from   PyQt5 . QtWidgets               import QTreeWidgetItem
from   PyQt5 . QtWidgets               import QLineEdit
from   PyQt5 . QtWidgets               import QComboBox
from   PyQt5 . QtWidgets               import QSpinBox
##############################################################################
from   AITK  . Qt        . VirtualGui  import VirtualGui  as VirtualGui
from   AITK  . Qt        . MenuManager import MenuManager as MenuManager
from   AITK  . Qt        . TreeWidget  import TreeWidget  as TreeWidget
##############################################################################
from   AITK  . Documents . Name        import Name        as NameItem
##############################################################################
class NamesEditor        ( TreeWidget , NameItem                           ) :
  ############################################################################
  emitNamesShow = pyqtSignal     (                                           )
  emitAllNames  = pyqtSignal     ( list                                      )
  CloseMyself   = pyqtSignal     ( QWidget                                   )
  ############################################################################
  def __init__           ( self , parent = None                            ) :
    ##########################################################################
    super ( TreeWidget , self ) . __init__   ( parent                        )
    super ( NameItem   , self ) . __init__   (                               )
    ##########################################################################
    return
  ############################################################################
  def Prepare                     ( self                                   ) :
    ##########################################################################
    Names  = self . Translations  [ "NamesEditor" ] [ "Labels"               ]
    Items  = self . tableItems    (                                          )
    ##########################################################################
    self . KEYs =                 [ "id"                                     ,
                                    "name"                                   ,
                                    "locality"                               ,
                                    "relevance"                              ,
                                    "priority"                               ,
                                    "flags"                                  ,
                                    "utf8"                                   ,
                                    "length"                                 ,
                                    "ltime"                                  ]
    ##########################################################################
    TOTAL    = len                ( self . KEYs                              )
    self     . setColumnCount     ( TOTAL + 1                                )
    ##########################################################################
    self     . LabelItem = QTreeWidgetItem (                                 )
    for i , it in enumerate       ( self . KEYs                            ) :
      self   . LabelItem . setText          ( i , Names [ it ]               )
      self   . LabelItem . setTextAlignment ( i , Qt . AlignHCenter          )
    self     . LabelItem . setText          ( TOTAL , ""                     )
    self     . setHeaderItem      ( self . LabelItem                         )
    ##########################################################################
    self     . setColumnWidth     ( TOTAL     , 3                            )
    ##########################################################################
    self     . setColumnHidden    ( 0         , True                         )
    self     . setColumnHidden    ( TOTAL - 1 , True                         )
    ##########################################################################
    self     . setRootIsDecorated ( False                                    )
    ##########################################################################
    self     . emitNamesShow . connect ( self . show                         )
    self     . emitAllNames  . connect ( self . refresh                      )
    ##########################################################################
    self     . MountClicked       ( 1                                        )
    self     . MountClicked       ( 2                                        )
    ##########################################################################
    self     . setPrepared        ( True                                     )
    ##########################################################################
    return
  ############################################################################
  def closeEvent                 ( self , event                            ) :
    ##########################################################################
    if                           ( self . TryClose ( )                     ) :
      event . accept             (                                           )
    else                                                                     :
      event . ignore             (                                           )
    ##########################################################################
    return
  ############################################################################
  def Configure                  ( self                                    ) :
    return
  ############################################################################
  def FocusIn                    ( self                                    ) :
    print("FocusIn")
    return False
  ############################################################################
  def FocusOut                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def singleClicked              ( self , item , column                    ) :
    print(f"singleClicked {column}")
    return
  ############################################################################
  def doubleClicked              ( self , item , column                    ) :
    ##########################################################################
    if                           ( column not in [ 1 , 2 , 3 , 4 , 5 ]     ) :
      return
    ##########################################################################
    print(f"doubleClicked {column}")
    if                           ( column == 1                             ) :
      pass
    ##########################################################################
    elif                         ( column == 2                             ) :
      pass
    ##########################################################################
    elif                         ( column == 3                             ) :
      pass
    ##########################################################################
    elif                         ( column == 4                             ) :
      pass
    ##########################################################################
    elif                         ( column == 5                             ) :
      pass
    ##########################################################################
    return
  ############################################################################
  def stateChanged               ( self , item , column                    ) :
    print(f"stateChanged {column}")
    return
  ############################################################################
  def Insert                     ( self                                    ) :
    print("Insert")
    return
  ############################################################################
  def Delete                     ( self                                    ) :
    print("Delete")
    return
  ############################################################################
  def Menu                       ( self , pos                              ) :
    ##########################################################################
    ##########################################################################
    print(pos)
    return
  ############################################################################
  def TryClose                   ( self                                    ) :
    ##########################################################################
    self . setPrepared           ( False                                     )
    self . CloseMyself . emit    ( self                                      )
    ##########################################################################
    print("TryClose")
    return True
  ############################################################################
  def refresh                       ( self , All                           ) :
    ##########################################################################
    self . clear                    (                                        )
    TRX     = self . Translations   [ "NamesEditor"                          ]
    ##########################################################################
    for IT in All                                                            :
      ########################################################################
      NT    = QTreeWidgetItem       (                                        )
      ########################################################################
      L     = IT                    [ 2                                      ]
      R     = IT                    [ 4                                      ]
      REL   = TRX                   [ "Relevance" ] [ str ( R )              ]
      LANG  = TRX                   [ "Languages" ] [ str ( L )              ]
      S     = IT                    [ 8                                      ]
      try                                                                    :
        S   = S . decode            ( "utf-8"                                )
      except ( UnicodeDecodeError , AttributeError )                         :
        pass
      ########################################################################
      NT    . setText               ( 0 , str ( IT [  0 ] )                  )
      NT    . setTextAlignment      ( 4 , Qt.AlignRight                      )
      ########################################################################
      NT    . setText               ( 1 , str ( S         )                  )
      ########################################################################
      NT    . setText               ( 2 , str ( LANG      )                  )
      NT    . setData               ( 2 , Qt . UserRole , IT [ 2 ]           )
      ########################################################################
      NT    . setText               ( 3 , str ( REL       )                  )
      NT    . setData               ( 3 , Qt . UserRole , IT [ 4 ]           )
      ########################################################################
      NT    . setText               ( 4 , str ( IT [  3 ] )                  )
      NT    . setTextAlignment      ( 4 , Qt.AlignRight                      )
      NT    . setData               ( 4 , Qt . UserRole , IT [ 3 ]           )
      ########################################################################
      NT    . setText               ( 5 , str ( IT [  5 ] )                  )
      NT    . setTextAlignment      ( 5 , Qt.AlignRight                      )
      NT    . setData               ( 5 , Qt . UserRole , IT [ 5 ]           )
      ########################################################################
      NT    . setText               ( 6 , str ( IT [  6 ] )                  )
      NT    . setTextAlignment      ( 6 , Qt.AlignRight                      )
      ########################################################################
      NT    . setText               ( 7 , str ( IT [  7 ] )                  )
      NT    . setTextAlignment      ( 7 , Qt.AlignRight                      )
      ########################################################################
      NT    . setText               ( 8 , str ( IT [  9 ] )                  )
      ########################################################################
      NT    . setText               ( 9 , ""                                 )
      ########################################################################
      self  . addTopLevelItem       ( NT                                     )
    ##########################################################################
    self . emitNamesShow . emit     (                                        )
    ##########################################################################
    TOTAL   = len                   ( self . KEYs                            )
    for i in range                  ( 0 , TOTAL - 1                        ) :
      self  . resizeColumnToContents ( i )
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
    ##########################################################################
    return
  ############################################################################
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . Prepared                     ) :
      self . Prepare             (                                           )
    ##########################################################################
    threading . Thread ( target = self . loading ) . start (                 )
    ##########################################################################
    return
##############################################################################

"""


#define LinkAction(ID,Function)       connectAction(N::Menus::ID,this,SLOT(Function))




N::PhonemeItems:: PhonemeItems ( QWidget * parent , Plan * p )
                : TreeDock     (           parent ,        p )
                , Group        (                             )
                , GroupItems   (                           p )
{
  WidgetClass   ;
  Configure ( ) ;
}

N::PhonemeItems::~PhonemeItems (void)
{
}

QSize N::PhonemeItems::sizeHint(void) const
{
  return QSize ( 1024 , 720 ) ;
}

QMimeData * N::PhonemeItems::dragMime (void)
{
  QMimeData * mime = standardMime("phoneme")                 ;
  nKickOut ( IsNull(mime) , NULL )                           ;
  QImage image = windowIcon().pixmap(QSize(32,32)).toImage() ;
  mime -> setImageData(image)                                ;
  return mime                                                ;
}

bool N::PhonemeItems::hasItem(void)
{
  UUIDs Uuids = selectedUuids(0) ;
  return ( Uuids.count() > 0 )   ;
}

bool N::PhonemeItems::startDrag(QMouseEvent * event)
{
  QTreeWidgetItem * atItem = itemAt(event->pos())           ;
  nKickOut ( IsNull(atItem) , false )                       ;
  nKickOut (!IsMask(event->buttons(),Qt::LeftButton),false) ;
  dragPoint = event->pos()                                  ;
  nKickOut (!atItem->isSelected(),false)                    ;
  nKickOut (!PassDragDrop,true)                             ;
  return true                                               ;
}

bool N::PhonemeItems::fetchDrag(QMouseEvent * event)
{
  nKickOut ( !IsMask(event->buttons(),Qt::LeftButton) , false) ;
  QPoint pos = event->pos()                                    ;
  pos -= dragPoint                                             ;
  return ( pos.manhattanLength() > qApp->startDragDistance() ) ;
}

void N::PhonemeItems::dragDone(Qt::DropAction dropIt,QMimeData * mime)
{
}

bool N::PhonemeItems::finishDrag(QMouseEvent * event)
{
  return true ;
}

bool N::PhonemeItems::acceptDrop(QWidget * source,const QMimeData * mime)
{
  nKickOut ( nEqual(source,this) , false ) ;
  return dropHandler(mime)                 ;
}

bool N::PhonemeItems::dropNew(QWidget * source,const QMimeData * mime,QPoint pos)
{
  Alert ( Action ) ;
  return true      ;
}

bool N::PhonemeItems::FocusIn(void)
{
  LinkAction ( Insert     , New             ( ) ) ;
  LinkAction ( Refresh    , startup         ( ) ) ;
  LinkAction ( Copy       , CopyToClipboard ( ) ) ;
  LinkAction ( SelectNone , SelectNone      ( ) ) ;
  LinkAction ( SelectAll  , SelectAll       ( ) ) ;
  return true                                     ;
}

void N::PhonemeItems::Configure(void)
{
  setEmpty                     (                                  ) ;
  NewTreeWidgetItem            ( head                             ) ;
  head -> setText              ( 0 , tr("Name"    )               ) ;
  head -> setText              ( 1 , tr("Mnemonic")               ) ;
  head -> setText              ( 2 , tr("Flags"   )               ) ;
  head -> setText              ( 3 , tr("Code"    )               ) ;
  head -> setText              ( 4 , tr("Type"    )               ) ;
  head -> setText              ( 5 , tr("Start"   )               ) ;
  head -> setText              ( 6 , tr("End"     )               ) ;
  head -> setText              ( 7 , tr("Length"  )               ) ;
  head -> setText              ( 8 , ""                           ) ;
  ///////////////////////////////////////////////////////////////////
  setWindowTitle               ( tr("Phoneme lists")              ) ;
  setWindowIcon                ( QIcon(":/images/audiofiles.png") ) ;
  setDragDropMode              ( DragDrop                         ) ;
  setRootIsDecorated           ( false                            ) ;
  setAlternatingRowColors      ( true                             ) ;
  setSelectionMode             ( ExtendedSelection                ) ;
  setColumnCount               ( 9                                ) ;
  setHorizontalScrollBarPolicy ( Qt::ScrollBarAsNeeded            ) ;
  setVerticalScrollBarPolicy   ( Qt::ScrollBarAsNeeded            ) ;
  assignHeaderItems            ( head                             ) ;
  MountClicked                 ( 2                                ) ;
  setDropFlag                  ( DropPhoneme , true               ) ;
  plan -> setFont              ( this                             ) ;
}

void N::PhonemeItems::run(int Type,ThreadData * data)
{ Q_UNUSED ( data ) ;
  switch   ( Type ) {
    case 10001      :
      List (      ) ;
    break           ;
  }                 ;
}

void N::PhonemeItems::List(void)
{
  blockSignals      ( true        )                           ;
  SqlConnection  SC ( plan -> sql )                           ;
  if ( SC . open ( "PhonemeItems" , "List" ) )                {
    QString Q                                                 ;
    QString N                                                 ;
    UUIDs   U                                                 ;
    SUID    u                                                 ;
    ///////////////////////////////////////////////////////////
    if (isFirst())                                            {
      U = GroupItems :: Subordination                         (
            SC                                                ,
            first                                             ,
            t1                                                ,
            Types::Phoneme                                    ,
            relation                                          ,
            SC.OrderByAsc("position")                       ) ;
    } else
    if (isSecond())                                           {
      U = GroupItems :: GetOwners                             (
            SC                                                ,
            second                                            ,
            Types::Phoneme                                    ,
            t2                                                ,
            relation                                          ,
            SC.OrderByAsc("id")                             ) ;
    } else
    if ( 0 == first )                                         {
      U = SC . Uuids                                          (
            PlanTable(Phonemes)                               ,
            "uuid"                                            ,
            SC.OrderByAsc("id")                             ) ;
    }                                                         ;
    ///////////////////////////////////////////////////////////
    foreach ( u , U )                                         {
      N = SC . getName                                        (
            PlanTable(Names)                                  ,
            "uuid"                                            ,
            vLanguageId                                       ,
            u                                               ) ;
      Q = SC . sql . SelectFrom                               (
            SC . Columns                                      (
              7                                               ,
              "mnemonic"                                      ,
              "flags"                                         ,
              "code"                                          ,
              "type"                                          ,
              "start"                                         ,
              "end"                                           ,
              "length"                                      ) ,
            PlanTable ( Phonemes )                            ,
            SC . WhereUuid ( u )                            ) ;
      if (SC.Fetch(Q))                                        {
        QByteArray MB = SC . ByteArray ( 0 )                  ;
        int32_t    mb                                         ;
        memcpy ( &mb , MB.data() , 4 )                        ;
        NewTreeWidgetItem ( it )                              ;
        Phoneme ph                                            ;
        ph  . Mnemonic  = (unsigned int)mb                    ;
        ph  . Flags     = SC . Value(1) . toUInt  (   )       ;
        ph  . Code      = (unsigned char)SC . Int ( 2 )       ;
        ph  . Type      = (unsigned char)SC . Int ( 3 )       ;
        ph  . StartType = (unsigned char)SC . Int ( 4 )       ;
        ph  . EndType   = (unsigned char)SC . Int ( 5 )       ;
        ph  . Length    = (unsigned char)SC . Int ( 6 )       ;
        it -> setData   ( 0 , Qt::UserRole , u              ) ;
        it -> setText   ( 0 , N                             ) ;
        it -> setText   ( 1 , ph.MnemonicString()           ) ;
        it -> setText   ( 2 , QString::number(ph.Flags,16 ) ) ;
        it -> setText   ( 3 , QString::number(ph.Code     ) ) ;
        it -> setText   ( 4 , QString::number(ph.Type     ) ) ;
        it -> setText   ( 5 , QString::number(ph.StartType) ) ;
        it -> setText   ( 6 , QString::number(ph.EndType  ) ) ;
        it -> setText   ( 7 , QString::number(ph.Length   ) ) ;
        addTopLevelItem ( it                                ) ;
      }                                                       ;
    }                                                         ;
    ///////////////////////////////////////////////////////////
    SC . close          (                                   ) ;
  }                                                           ;
  SC . remove           (                                   ) ;
  blockSignals          ( false                             ) ;
  reportItems           (                                   ) ;
  plan -> StopBusy      (                                   ) ;
  emit AutoFit          (                                   ) ;
  Alert                 ( Done                              ) ;
}

bool N::PhonemeItems::startup(void)
{
  clear             (       ) ;
  plan -> StartBusy (       ) ;
  start             ( 10001 ) ;
  return true                 ;
}

void N::PhonemeItems::New(void)
{
  NewTreeWidgetItem( item                 ) ;
  item -> setData  ( 0 , Qt::UserRole , 0 ) ;
  addTopLevelItem  ( item                 ) ;
  scrollToItem     ( item                 ) ;
  doubleClicked    ( item , 0             ) ;
}

void N::PhonemeItems::doubleClicked (QTreeWidgetItem * item,int column)
{
  SUID u = nTreeUuid ( item , 0 )                       ;
  QLineEdit * line                                      ;
  SpinBox   * sb                                        ;
  switch (column)                                       {
    case 0                                              :
      line = setLineEdit                                (
        item                                            ,
        column                                          ,
        SIGNAL(returnPressed())                         ,
        SLOT  (nameChanged  ()) )                       ;
      line->setFocus(Qt::TabFocusReason)                ;
    break                                               ;
    case 1                                              :
      if ( u <= 0 ) return                              ;
      line = setLineEdit                                (
        item                                            ,
        column                                          ,
        SIGNAL(returnPressed())                         ,
        SLOT  (signChanged  ()) )                       ;
      line->setFocus(Qt::TabFocusReason)                ;
    break                                               ;
    case 2                                              :
      if ( u <= 0 ) return                              ;
      line = setLineEdit                                (
        item                                            ,
        column                                          ,
        SIGNAL(returnPressed())                         ,
        SLOT  (flagsChanged ()) )                       ;
      line->setFocus(Qt::TabFocusReason)                ;
    break                                               ;
    case 3                                              :
    case 4                                              :
    case 5                                              :
    case 6                                              :
    case 7                                              :
      if ( u <= 0 ) return                              ;
      sb = (SpinBox *)setSpinBox                        (
        item                                            ,
        column                                          ,
        0                                               ,
        255                                             ,
        SIGNAL(editingFinished())                       ,
        SLOT  (spinChanged    ())                     ) ;
      sb -> blockSignals ( true                       ) ;
      sb -> setValue     ( item->text(column).toInt() ) ;
      sb -> blockSignals ( false                      ) ;
    break                                               ;
  }                                                     ;
}

void N::PhonemeItems::nameChanged(void)
{
  if (IsNull(ItemEditing)) return                     ;
  if (IsNull(ItemWidget )) return                     ;
  QLineEdit * line    = Casting(QLineEdit,ItemWidget) ;
  SUID        u       = nTreeUuid(ItemEditing,0)      ;
  QString     n       = ""                            ;
  bool        success = false                         ;
  if (NotNull(line)) n = line->text()                 ;
  if ( n . length ( ) > 0 )                           {
    EnterSQL ( SC , plan->sql )                       ;
      QString Q                                       ;
      if ( u <= 0 )                                   {
        QByteArray B                                  ;
        B . resize ( 4 )                              ;
        B . fill   ( 0 )                              ;
        u = SC . Unique                               (
              PlanTable(MajorUuid)                    ,
              "uuid"                                  ,
              87241600                              ) ;
        SC . assureUuid                               (
          PlanTable(MajorUuid)                        ,
          u                                           ,
          Types::Phoneme                            ) ;
        Q = SC . sql . InsertInto                     (
              PlanTable(Phonemes)                     ,
              2                                       ,
              "uuid"                                  ,
              "mnemonic"                            ) ;
        SC . Prepare ( Q                            ) ;
        SC . Bind    ( "uuid"     , u               ) ;
        SC . Bind    ( "mnemonic" , B               ) ;
        SC . Exec    (                              ) ;
      }                                               ;
      SC . assureName                                 (
        PlanTable(Names)                              ,
        u                                             ,
        vLanguageId                                   ,
        n                                           ) ;
      ItemEditing -> setText ( 0 , n )                ;
      success = true                                  ;
    LeaveSQL ( SC , plan->sql )                       ;
  }                                                   ;
  removeOldItem ( true , 0 )                          ;
  if (success)                                        {
    Alert ( Done  )                                   ;
  } else                                              {
    Alert ( Error )                                   ;
  }                                                   ;
}

void N::PhonemeItems::signChanged(void)
{
  if (IsNull(ItemEditing)) return                  ;
  if (IsNull(ItemWidget )) return                  ;
  QLineEdit * line = Casting(QLineEdit,ItemWidget) ;
  SUID        u    = nTreeUuid(ItemEditing,0)      ;
  QString     n    = ""                            ;
  if (NotNull(line)) n = line->text()              ;
  if (u>0 && n.length()>0)                         {
      unsigned int m = 0                           ;
      m = (unsigned int)n.at(0).toLatin1()         ;
      for (int i=1;i<n.length();i++)               {
        m <<= 8                                    ;
        n  += (unsigned int)n.at(i).toLatin1()     ;
      }                                            ;
      QByteArray B                                 ;
      uint32_t   v = (uint32_t)m                   ;
      B . append ( (const char *)&v , 4 )          ;
      EnterSQL  ( SC , plan->sql )                 ;
        QString Q                                  ;
        Q = SC . sql . Update                      (
              PlanTable(Phonemes)                  ,
              SC.WhereUuid(u)                      ,
              1                                    ,
              "mnemonic"                         ) ;
        SC . Prepare ( Q                         ) ;
        SC . Bind    ( "mnemonic" , B            ) ;
        SC . Exec    (                           ) ;
      LeaveSQL  ( SC , plan->sql )                 ;
      Alert     ( Done           )                 ;
  }                                                ;
  removeOldItem ( false , 1      )                 ;
}

void N::PhonemeItems::flagsChanged(void)
{
  if (IsNull(ItemEditing)) return                  ;
  if (IsNull(ItemWidget )) return                  ;
  QLineEdit * line = Casting(QLineEdit,ItemWidget) ;
  SUID        u    = nTreeUuid(ItemEditing,0)      ;
  QString     n    = ""                            ;
  if (NotNull(line)) n = line->text()              ;
  if (u>0 && n.length()>0)                         {
    bool         ok    = false                     ;
    unsigned int flags = n.toUInt(&ok,16)          ;
    if (ok)                                        {
      EnterSQL  ( SC , plan->sql )                 ;
        QString Q                                  ;
        Q = SC . sql . Update                      (
              PlanTable(Phonemes)                  ,
              SC.WhereUuid(u)                      ,
              1                                    ,
              "flags"                            ) ;
        SC . Prepare ( Q                         ) ;
        SC . Bind    ( "flags" , flags           ) ;
        SC . Exec    (                           ) ;
      LeaveSQL  ( SC , plan->sql )                 ;
      Alert     ( Done           )                 ;
    } else                                         {
      Alert     ( Error          )                 ;
    }                                              ;
  }                                                ;
  removeOldItem ( false , 2      )                 ;
}

void N::PhonemeItems::spinChanged(void)
{
  if (IsNull(ItemEditing)) return              ;
  if (IsNull(ItemWidget )) return              ;
  QSpinBox * sb = Casting(QSpinBox,ItemWidget) ;
  SUID       u  = nTreeUuid(ItemEditing,0)     ;
  int        L  = sb->value()                  ;
  if (u>0 && L>0)                              {
    EnterSQL ( SC , plan->sql )                ;
      QString Q                                ;
      QString column                           ;
      switch (ItemColumn)                      {
        case 3: column = "code"        ; break ;
        case 4: column = "type"        ; break ;
        case 5: column = "start"       ; break ;
        case 6: column = "end"         ; break ;
        case 7: column = "length"      ; break ;
      }                                        ;
      Q = SC . sql . Update                    (
            PlanTable(Phonemes)                ,
            SC.WhereUuid(u)                    ,
            1                                  ,
            column.toUtf8().constData()      ) ;
      SC . Prepare ( Q                       ) ;
      SC . Bind    ( column , L              ) ;
      SC . Exec    (                         ) ;
    LeaveSQL ( SC , plan->sql )                ;
    Alert    ( Done           )                ;
  }                                            ;
  removeOldItem ( false , ItemColumn )         ;
}

bool N::PhonemeItems::dropPhonemes(QWidget * widget,QPointF pos,const UUIDs & Uuids)
{
  return true ;
}

bool N::PhonemeItems::Menu(QPoint pos)
{
  nScopedMenu ( mm , this )                       ;
  QAction         * aa                            ;
  QTreeWidgetItem * it = itemAt ( pos )           ;
  mm . add ( 101 , tr("New"         ) )           ;
  if (NotNull(it))                                {
    mm . add ( 102 , tr("Edit"      ) )           ;
  }                                               ;
  mm . add ( 103 , tr("Refresh"     ) )           ;
  mm . addSeparator  (                )           ;
  mm . add ( 201 , tr("Copy"        ) )           ;
  mm . add ( 202 , tr("Select all"  ) )           ;
  mm . add ( 203 , tr("Select none" ) )           ;
  mm . addSeparator  (                )           ;
  mm . add ( 901 , tr("Translations") )           ;
  DockingMenu ( mm )                              ;
  mm.setFont(plan)                                ;
  aa = mm.exec()                                  ;
  if (IsNull(aa)) return true                     ;
  if (RunDocking(mm,aa)) return true              ;
  UUIDs U                                         ;
  switch (mm[aa])                                 {
    case 101                                      :
      New             ( )                         ;
    break                                         ;
    case 102                                      :
      emit Edit ( it->text(0) , nTreeUuid(it,0) ) ;
    break                                         ;
    case 103                                      :
      startup         ( )                         ;
    break                                         ;
    case 201                                      :
      CopyToClipboard ( )                         ;
    break                                         ;
    case 202                                      :
      SelectAll       ( )                         ;
    break                                         ;
    case 203                                      :
      SelectNone      ( )                         ;
    break                                         ;
    case 901                                      :
      U = itemUuids     ( 0                 )     ;
      emit Translations ( windowTitle() , U )     ;
    break                                         ;
  }                                               ;
  return true                                     ;
}




"""
