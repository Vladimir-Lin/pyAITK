# -*- coding: utf-8 -*-
##############################################################################
## IconDock
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
from   PyQt5 . QtCore                 import QByteArray
##############################################################################
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
from   PyQt5 . QtGui                  import QPainter
from   PyQt5 . QtGui                  import QColor
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QPixmap
from   PyQt5 . QtGui                  import QImage
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAbstractItemView
from   PyQt5 . QtWidgets              import QListView
from   PyQt5 . QtWidgets              import QListWidget
from   PyQt5 . QtWidgets              import QListWidgetItem
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . LineEdit               import LineEdit as LineEdit
from         . ListDock               import ListDock as ListDock
##############################################################################
class IconDock           ( ListDock                                        ) :
  ############################################################################
  emitIconsShow  = pyqtSignal       (                                        )
  emitAllIcons   = pyqtSignal       ( dict                                   )
  emitAssignIcon = pyqtSignal       ( QListWidgetItem , QIcon                )
  ############################################################################
  def __init__                      ( self , parent = None , plan = None   ) :
    ##########################################################################
    super ( ) . __init__            ( parent , plan                          )
    ##########################################################################
    self . EditAllNames  = None
    self . IconFont      = None
    self . UsingName     = True
    self . SortOrder     = "asc"
    self . UuidItemMaps  =          {                                        }
    ##########################################################################
    self . setViewMode              ( QListView . IconMode                   )
    self . setIconSize              ( QSize ( 128 , 128 )                    )
    self . setGridSize              ( QSize ( 156 , 192 )                    )
    self . setSpacing               ( 4                                      )
    self . setDragDropMode          ( QAbstractItemView . DropOnly           )
    self . setResizeMode            ( QListView . Adjust                     )
    self . setWordWrap              ( True                                   )
    self . setHorizontalScrollBarPolicy ( Qt . ScrollBarAsNeeded             )
    self . setVerticalScrollBarPolicy   ( Qt . ScrollBarAsNeeded             )
    self . setMinimumSize           ( QSize ( 144 , 200 )                    )
    ##########################################################################
    self . emitIconsShow  . connect ( self . show                            )
    self . emitAllIcons   . connect ( self . refresh                         )
    self . emitAssignIcon . connect ( self . AssignIcon                      )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return False
    ##########################################################################
    self . setActionLabel        ( "Label"   , self . windowTitle ( )        )
    self . LinkAction            ( "Insert"  , self . InsertItem             )
    self . LinkAction            ( "Delete"  , self . DeleteItems            )
    self . LinkAction            ( "Refresh" , self . startup                )
    ##########################################################################
    return True
  ############################################################################
  def FocusOut                   ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def Prepare                         ( self                               ) :
    raise NotImplementedError         (                                      )
  ############################################################################
  def GetUuidIcon                     ( self , DB , Uuid                   ) :
    raise NotImplementedError         (                                      )
  ############################################################################
  def setIconFont                     ( self , fnt                         ) :
    self . IconFont = fnt
    return self . IconFont
  ############################################################################
  def iconFont                        ( self                               ) :
    ##########################################################################
    if                                ( self . IconFont != None            ) :
      return self . IconFont
    ##########################################################################
    return self . font                (                                      )
  ############################################################################
  @pyqtSlot(QListWidgetItem,QIcon)
  def AssignIcon                      ( self , item , icon                 ) :
    item . setIcon                    ( icon                                 )
    return
  ############################################################################
  def PrepareItemContent              ( self , item , UUID , NAME          ) :
    ##########################################################################
    FT     = self . iconFont          (                                      )
    if                                ( self . UsingName                   ) :
      item . setText                  ( NAME                                 )
    item   . setToolTip               ( str ( UUID )                         )
    item   . setTextAlignment         ( Qt   . AlignCenter                   )
    item   . setData                  ( Qt   . UserRole , str ( UUID )       )
    item   . setIcon                  ( self . defaultIcon ( )               )
    item   . setFont                  ( FT                                   )
    ##########################################################################
    JSOX   = self . itemJson          ( item                                 )
    ##########################################################################
    JSOX [ "Uuid" ] = UUID
    JSOX [ "Name" ] = NAME
    ##########################################################################
    self . setItemJson                ( item , JSOX                          )
    ##########################################################################
    return item
  ############################################################################
  def PrepareItem                     ( self ,        UUID , NAME          ) :
    ##########################################################################
    item = QListWidgetItem            (                                      )
    self . setItemJson                ( item , { }                           )
    ##########################################################################
    return self . PrepareItemContent  ( self , item , UUID , NAME            )
  ############################################################################
  def PrepareEmptyItem                ( self                               ) :
    ##########################################################################
    FT   = self . iconFont            (                                      )
    IT   = QListWidgetItem            (                                      )
    if                                ( self . UsingName                   ) :
      IT . setText                    ( ""                                   )
    IT   . setTextAlignment           ( Qt   . AlignCenter                   )
    IT   . setData                    ( Qt   . UserRole , str ( 0 )          )
    IT   . setIcon                    ( self . defaultIcon ( )               )
    IT   . setFont                    ( FT                                   )
    ##########################################################################
    JSOX =                            { "Uuid" : 0 , "Name" : ""             }
    self . setItemJson                ( IT , JSOX                            )
    ##########################################################################
    return IT
  ############################################################################
  def setLineEdit        ( self , item , signal , method                   ) :
    ##########################################################################
    text = item . text   (                                                   )
    LE   = LineEdit      ( self , self . PlanFunc                            )
    LE   . setFont       ( self . iconFont ( )                               )
    LE   . setText       ( text                                              )
    ##########################################################################
    self . EditItem   = item
    self . EditWidget = LE
    ##########################################################################
    try                                                                      :
      S  = getattr       ( LE, signal                                        )
      S  . connect       ( method                                            )
    except AttributeError                                                    :
      pass
    ##########################################################################
    self . setItemWidget ( item , LE                                         )
    LE   . setFocus      ( Qt . TabFocusReason                               )
    ##########################################################################
    return
  ############################################################################
  def FetchIcon                       ( self , DB , PUID                   ) :
    ##########################################################################
    if                                ( PUID <= 0                          ) :
      return None
    ##########################################################################
    TUBTAB     = self . Tables        [ "Thumb"                              ]
    WH         = f"where ( `usage` = 'ICON' ) and ( `uuid` = {PUID} )"
    OPTS       = "order by `id` desc limit 0 , 1"
    QQ         = f"select `thumb` from {TUBTAB} {WH} {OPTS} ;"
    DB         . Query                ( QQ                                   )
    THUMB      = DB . FetchOne        (                                      )
    ##########################################################################
    if                                ( THUMB == None                      ) :
      return None
    ##########################################################################
    if                                ( len ( THUMB ) <= 0                 ) :
      return None
    ##########################################################################
    BLOB       = THUMB                [ 0                                    ]
    if                                ( isinstance ( BLOB , bytearray )    ) :
      BLOB = bytes                    ( BLOB                                 )
    ##########################################################################
    if                                ( len ( BLOB ) <= 0                  ) :
      return None
    ##########################################################################
    IMG        = QImage               (                                      )
    IMG        . loadFromData         ( QByteArray ( BLOB ) , "PNG"          )
    TSIZE      = IMG . size           (                                      )
    ##########################################################################
    ISIZE      = self . iconSize      (                                      )
    ICZ        = QImage               ( ISIZE , QImage . Format_ARGB32       )
    ICZ        . fill                 ( QColor ( 255 , 255 , 255 )           )
    ##########################################################################
    W          = int       ( ( ISIZE . width  ( ) - TSIZE . width  ( ) ) / 2 )
    H          = int       ( ( ISIZE . height ( ) - TSIZE . height ( ) ) / 2 )
    PTS        = QPoint               ( W , H                                )
    ##########################################################################
    p          = QPainter             (                                      )
    p          . begin                ( ICZ                                  )
    p          . drawImage            ( PTS , IMG                            )
    p          . end                  (                                      )
    ##########################################################################
    PIX        = QPixmap              (                                      )
    PIX        . convertFromImage     ( ICZ                                  )
    ##########################################################################
    return QIcon                      ( PIX                                  )
  ############################################################################
  def FetchIcons                      ( self , UUIDs                       ) :
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      return
    ##########################################################################
    DB      = self . ConnectDB        ( True                                 )
    if                                ( DB == None                         ) :
      return
    ##########################################################################
    for U in UUIDs                                                           :
      if                              ( U in self . UuidItemMaps           ) :
        item = self . UuidItemMaps    [ U                                    ]
        PUID = self . GetUuidIcon     ( DB , U                               )
        if                            ( PUID > 0                           ) :
          icon = self . FetchIcon     ( DB , PUID                            )
          if                          ( icon != None                       ) :
            self . emitAssignIcon . emit ( item , icon                       )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot(dict)
  def refresh                         ( self , JSON                        ) :
    ##########################################################################
    self    . clear                   (                                      )
    ##########################################################################
    UUIDs   = JSON                    [ "UUIDs"                              ]
    if                                ( self . UsingName                   ) :
      NAMEs = JSON                    [ "NAMEs"                              ]
    ##########################################################################
    for U in UUIDs                                                           :
      ########################################################################
      if                              ( self . UsingName                   ) :
        IT  = self . PrepareItem      ( U , NAMEs [ U ]                      )
      else                                                                   :
        IT  = self . PrepareItem      ( U , ""                               )
      self  . addItem                 ( IT                                   )
      self  . UuidItemMaps [ U ] = IT
    ##########################################################################
    self    . emitIconsShow . emit    (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) > 0                  ) :
      self . Go                       ( self . FetchIcons , ( UUIDs , )      )
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
  def loading                         ( self                               ) :
    ##########################################################################
    DB      = self . ConnectDB        (                                      )
    if                                ( DB == None                         ) :
      self . emitIconsShow . emit     (                                      )
      return
    ##########################################################################
    self    . FetchSessionInformation ( DB                                   )
    UUIDs   = self . ObtainsItemUuids ( DB                                   )
    if                                ( self . UsingName                   ) :
      NAMEs = self . ObtainsUuidNames ( DB , UUIDs                           )
    ##########################################################################
    DB      . Close                   (                                      )
    ##########################################################################
    if                                ( len ( UUIDs ) <= 0                 ) :
      self . emitIconsShow . emit     (                                      )
    ##########################################################################
    JSON               =              {                                      }
    JSON   [ "UUIDs" ] = UUIDs
    if                                ( self . UsingName                   ) :
      JSON [ "NAMEs" ] = NAMEs
    ##########################################################################
    self   . emitAllIcons . emit      ( JSON                                 )
    ##########################################################################
    return
  ############################################################################
  @pyqtSlot()
  def startup                    ( self                                    ) :
    ##########################################################################
    if                           ( not self . isPrepared ( )               ) :
      self . Prepare             (                                           )
    ##########################################################################
    self   . Go                  ( self . loading                            )
    ##########################################################################
    return
##############################################################################


"""

class Q_COMPONENTS_EXPORT IconDock : public ListDock
{
  Q_OBJECT
  public:

    explicit IconDock      (StandardConstructor) ;
    virtual ~IconDock      (void);

  protected:

    virtual void Configure (void);

  private:

  public slots:

    virtual bool startup   (void);

  protected slots:

    virtual bool Menu      (QPoint pos) ;

  private slots:

  signals:

};

N::IconDock:: IconDock (QWidget * parent,Plan * p)
            : ListDock (          parent,       p)
{
  WidgetClass   ;
  Configure ( ) ;
}

N::IconDock::~IconDock (void)
{
}

void N::IconDock::Configure(void)
{
  setViewMode                  (IconMode             ) ;
  setIconSize                  (QSize(128,128)       ) ;
  setGridSize                  (QSize(140,192)       ) ;
  setDragDropMode              (DropOnly             ) ;
  setResizeMode                (QListView::Adjust    ) ;
  setWordWrap                  (true                 ) ;
  setHorizontalScrollBarPolicy (Qt::ScrollBarAsNeeded) ;
  setVerticalScrollBarPolicy   (Qt::ScrollBarAsNeeded) ;
  setMinimumSize               (QSize(144,200)       ) ;
}

bool N::IconDock::startup(void)
{
  if (IsNull(plan)) return false ;
  return true                    ;
}

bool N::IconDock::Menu(QPoint pos)
{ Q_UNUSED ( pos ) ;
  return false     ;
}

"""

