# -*- coding: utf-8 -*-
##############################################################################
## VcfPicture
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
from   io                             import BytesIO
from   wand . image                   import Image
from   PIL                            import Image as Pillow
##############################################################################
import cv2
import dlib
import skimage
import numpy                                               as np
##############################################################################
import PySide6
from   PySide6                             import QtCore
from   PySide6                             import QtGui
from   PySide6                             import QtWidgets
##############################################################################
from   PySide6 . QtCore                    import *
from   PySide6 . QtGui                     import *
from   PySide6 . QtWidgets                 import *
##############################################################################
from   AITK    . Qt6 . MenuManager         import MenuManager  as MenuManager
##############################################################################
from   AITK    . Essentials . Object       import Object       as Object
from   AITK    . Pictures   . Picture6     import Picture      as PictureItem
from   AITK    . Pictures   . Gallery      import Gallery      as GalleryItem
from   AITK    . People     . Faces . Face import Face         as FaceItem
##############################################################################
from           . VcfRectangle              import VcfRectangle as VcfRectangle
##############################################################################
class VcfPicture                 ( VcfRectangle                            , \
                                   Object                                  ) :
  ############################################################################
  def __init__                   ( self                                    , \
                                   parent = None                           , \
                                   item   = None                           , \
                                   plan   = None                           ) :
    ##########################################################################
    super ( ) . __init__         ( parent , item , plan                      )
    self . setObjectEmpty        (                                           )
    self . setRectangleDefaults  (                                           )
    self . setVcfPictureDefaults (                                           )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def setVcfPictureDefaults ( self                                         ) :
    ##########################################################################
    self . PictureDPI    = 96.0
    self . Image         = None
    self . Original      = None
    self . PICOP         = None
    self . Printable     = True
    self . Scaling       = False
    self . Xratio        = 0.0
    self . Yratio        = 0.0
    self . Details       =  {                                                }
    self . CurrentPeople =  {                                                }
    self . Descriptions  =  {                                                }
    ##########################################################################
    self . setFlag ( QGraphicsItem . ItemIsSelectable         , True         )
    self . setFlag ( QGraphicsItem . ItemIsFocusable          , True         )
    self . setFlag ( QGraphicsItem . ItemIsMovable            , True         )
    self . setFlag ( QGraphicsItem . ItemSendsGeometryChanges , True         )
    self . setFlag ( QGraphicsItem . ItemClipsToShape         , False        )
    self . setFlag ( QGraphicsItem . ItemClipsChildrenToShape , False        )
    ##########################################################################
    self . Painter . addMap ( "Border" , 0                                   )
    self . Painter . addPen ( 0 , QColor ( 224 , 224 , 224 )                 )
    self . Painter . pens [ 0 ] . setStyle ( Qt . DotLine                    )
    ##########################################################################
    self . setObjectType    ( 9                                              )
    ##########################################################################
    return
  ############################################################################
  def PanelRect  ( self ) :
    ##########################################################################
    X    = QPointF ( 3.0 , 0.40 )
    TL   = self . ScreenRect . topLeft ( )
    TL   = self . mapToScene ( TL )
    ## TL   = self . Options . Standard ( TL )
    Z    = QRectF ( TL . x ( ) , TL . y ( ) - X . y ( ) , X . x ( ) , X . y ( ) )
    ## Z    = self . Options . Region ( Z )
    Z    = self . mapFromScene ( Z ) . boundingRect ( )
    R    = QRectF ( self . ScreenRect.left(),Z.top(),self . ScreenRect.width(),Z.height() )
    ##########################################################################
    return R
  ############################################################################
  def CenterRect ( self ) :
    ##########################################################################
    X = QPointF ( 3.0 , 3.0 )
    H = X / 2
    C = self . ScreenRect . center (   )
    C = self . mapToScene          ( C )
    ## C = self . Options . Standard ( C )
    Z = QRectF ( C . x ( ) - H . x ( ) , C . y ( ) - H . y ( ) , X . x ( ) , X . y ( ) )
    ## Z = self . Options . Region ( Z )
    ##########################################################################
    return Z
  ############################################################################
  def setCenter ( self , center ) :
    ##########################################################################
    """
    PaperPos = center                                        ;
    QGraphicsItem::setPos(Options->position(center))         ;
    QTransform T                                             ;
    T.reset()                                                ;
    qreal sx = Options->DPI                                  ;
    qreal sy = Options->DPI                                  ;
    sx /= PictureDPI                                         ;
    sy /= PictureDPI                                         ;
    T = T.scale(sx,sy)                                       ;
    Transform = T                                            ;
    setTransform(T)                                          ;
    QSize S(Image.width(),Image.height())                    ;
    QPointF C(S.width()/2,S.height()/2)                      ;
    ScreenRect.setLeft     (-C.x     ())                     ;
    ScreenRect.setTop      (-C.y     ())                     ;
    ScreenRect.setWidth    (S.width  ())                     ;
    ScreenRect.setHeight   (S.height ())                     ;
    QRectF SR = mapToScene (ScreenRect ).boundingRect()      ;
    PaperRect = Options -> Standard (SR)                     ;
    setToolTip                                               (
      tr("Picture UUID : %1\n"
         "%2 x %3 pixels\n"
         "%4 DPI\n"
         "%5 x %6 cm\n"
         "Center : %7 x %8 cm"                      )
      .arg(uuid                                     )
      .arg(S        .width()).arg(S        .height())
      .arg(PictureDPI                               )
      .arg(PaperRect.width()).arg(PaperRect.height())
      .arg(PaperPos .x    ()).arg(PaperPos .y     ())
    )                                                        ;
    prepareGeometryChange  (           )                     ;
    """
    ##########################################################################
    return
  ############################################################################
  def atPixel                        ( self , pos                          ) :
    ##########################################################################
    if                               ( self . PICOP in [ False , None ]    ) :
      return QPoint                  ( 0 , 0                                 )
    ##########################################################################
    XX  = pos  . x                   (                                       )
    YY  = pos  . y                   (                                       )
    SW  = self . ScreenRect . width  (                                       )
    SH  = self . ScreenRect . height (                                       )
    WW  = self . PICOP      . Width  (                                       )
    HH  = self . PICOP      . Height (                                       )
    ##########################################################################
    X   = int                        ( XX * WW / SW                          )
    Y   = int                        ( YY * HH / SH                          )
    ##########################################################################
    return QPoint                    ( X , Y                                 )
  ############################################################################
  """
  def contextMenuEvent ( self , event                                      ) :
    ##########################################################################
    self  . CallMenu   ( self , event . pos ( )                              )
    event . accept     (                                                     )
    ##########################################################################
    return
  """
  ############################################################################
  def mouseDoubleClickEvent           ( self , event                       ) :
    ##########################################################################
    super ( ) . mouseDoubleClickEvent (        event                         )
    ##########################################################################
    return
  ############################################################################
  def mousePressEvent      ( self , event                                  ) :
    ##########################################################################
    self . scalePressEvent (        event                                    )
    ##########################################################################
    return
  ############################################################################
  def mouseMoveEvent      ( self , event                                   ) :
    ##########################################################################
    self . scaleMoveEvent (        event                                     )
    ##########################################################################
    return
  ############################################################################
  def mouseReleaseEvent      ( self , event                                ) :
    ##########################################################################
    self . scaleReleaseEvent (        event                                  )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                          Enabled    ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup         , Enabled      )
    self . LinkAction ( "Load"       , self . LoadPeople      , Enabled      )
    self . LinkAction ( "Import"     , self . ImportPeople    , Enabled      )
    self . LinkAction ( "Export"     , self . ExportSameNames , Enabled      )
    self . LinkAction ( "Insert"     , self . InsertItem      , Enabled      )
    self . LinkAction ( "Rename"     , self . RenamePeople    , Enabled      )
    self . LinkAction ( "Delete"     , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Cut"        , self . DeleteItems     , Enabled      )
    self . LinkAction ( "Copy"       , self . CopyItems       , Enabled      )
    self . LinkAction ( "Paste"      , self . PasteItems      , Enabled      )
    self . LinkAction ( "Search"     , self . Search          , Enabled      )
    self . LinkAction ( "Home"       , self . PageHome        , Enabled      )
    self . LinkAction ( "End"        , self . PageEnd         , Enabled      )
    self . LinkAction ( "PageUp"     , self . PageUp          , Enabled      )
    self . LinkAction ( "PageDown"   , self . PageDown        , Enabled      )
    self . LinkAction ( "SelectAll"  , self . SelectAll       , Enabled      )
    self . LinkAction ( "SelectNone" , self . SelectNone      , Enabled      )
    ##########################################################################
    return
  ############################################################################
  def FocusIn  ( self                                                      ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def FocusOut ( self                                                      ) :
    ##########################################################################
    ##########################################################################
    return True
  ############################################################################
  def ReportCursorXY          ( self , pos                                 ) :
    ##########################################################################
    p        = self . atPixel (        pos                                   )
    X        = p    . x       (                                              )
    Y        = p    . y       (                                              )
    TT       = f"{X} , {Y}"
    QToolTip . showText       ( QCursor . pos ( ) , TT                       )
    ##########################################################################
    return
  ############################################################################
  def Hovering            ( self , pos                                     ) :
    ##########################################################################
    self . ReportCursorXY (        pos                                       )
    ##########################################################################
    return
  ############################################################################
  def paint               ( self , painter , options , widget              ) :
    ##########################################################################
    self   . pushPainters ( painter                                          )
    ##########################################################################
    self   . Painting     ( painter , self . ScreenRect , False , True       )
    if                    ( self . isSelected ( )                          ) :
      self . PaintBorder  ( painter , self . ScreenRect , False , True       )
    ##########################################################################
    self   . popPainters  ( painter                                          )
    ##########################################################################
    return
  ############################################################################
  def Painting              ( self , p , region , clip , color             ) :
    ##########################################################################
    if                      ( clip                                         ) :
      self . PaintImageClip (        p , region , clip , color               )
    else                                                                     :
      self . PaintImage     (        p , region , clip , color               )
    ##########################################################################
    return
  ############################################################################
  def PaintImage  ( self , p , region , clip , color                       ) :
    ##########################################################################
    if            ( self . Image in [ False , None ]                       ) :
      return
    ##########################################################################
    p . drawImage ( self . ScreenRect , self . Image                         )
    ##########################################################################
    return
  ############################################################################
  def PaintImageClip       ( self , p , region , clip , color              ) :
    ##########################################################################
    if                     ( self . Image in [ False , None ]              ) :
      return
    ##########################################################################
    PS = self . mapToScene ( QPointF ( 0.0 , 0.0 )                           )
    PX = QPointF           ( PS.x() - region.left() , PS.y() - region.top()  )
    TM = self . transform  (                                                 )
    TX = TM . inverted     (                                                 )
    PX = TX . map          ( px                                              )
    p  . setTransform      ( TM                                              )
    p  . translate         ( PX                                              )
    p  . drawImage         ( self . ScreenRect , self . Image                )
    ##########################################################################
    return
  ############################################################################
  def PaintBorder               ( self , p , region , clip , color         ) :
    ##########################################################################
    self . Painter . drawBorder ( p , "Border" , self . ScreenRect           )
    ##########################################################################
    return
  ############################################################################
  def setCornerCursor           ( self , Corner                            ) :
    ##########################################################################
    """
    void N::VcfPicture::setCornerCursor(int Corner)
    {
      switch (Corner)                      {
        case NoSide                        :
          setCursor(Qt::ArrowCursor     )  ;
        break                              ;
        case TopLeft                       :
          setCursor(Qt::SizeFDiagCursor )  ;
        break                              ;
        case TopRight                      :
          setCursor(Qt::SizeBDiagCursor )  ;
        break                              ;
        case BottomLeft                    :
          setCursor(Qt::SizeBDiagCursor )  ;
        break                              ;
        case BottomRight                   :
          setCursor(Qt::SizeFDiagCursor )  ;
        break                              ;
        case LeftSide                      :
          setCursor(Qt::SizeHorCursor   )  ;
        break                              ;
        case RightSide                     :
          setCursor(Qt::SizeHorCursor   )  ;
        break                              ;
        case TopSide                       :
          setCursor(Qt::SizeVerCursor   )  ;
        break                              ;
        case BottomSide                    :
          setCursor(Qt::SizeVerCursor   )  ;
        break                              ;
        case Inside                        :
          setCursor(Qt::ClosedHandCursor)  ;
        break                              ;
      }                                    ;
    }
    """
    ##########################################################################
    return
  ############################################################################
  def itemChange ( self , change , value                                   ) :
    ##########################################################################
    if           ( change == QGraphicsItem . ItemPositionChange            ) :
      self . signalGeometryChanged  (                                        )
    ##########################################################################
    """
    QVariant N::VcfPicture::itemChange(GraphicsItemChange change,const QVariant & value)
    {
      switch (change)                                       {
        case ItemPositionChange                             :
        case ItemPositionHasChanged                         :
          if (NotNull(Options))                             {
            QPointF scenePos = value.toPointF(  )           ;
            PaperPos = Options->Standard(scenePos)          ;
            setToolTip                                      (
              tr("Picture UUID : %1\n"
                 "%2 x %3 pixels\n"
                 "%4 DPI\n"
                 "%5 x %6 cm\n"
                 "Center : %7 x %8 cm"                      )
              .arg(uuid                                     )
              .arg(Image    .width()).arg(Image    .height())
              .arg(PictureDPI                               )
              .arg(PaperRect.width()).arg(PaperRect.height())
              .arg(PaperPos .x    ()).arg(PaperPos .y     ())
            )                                               ;
            QToolTip::showText(QCursor::pos(),toolTip())    ;
          }                                                 ;
        break                                               ;
        case ItemSelectedHasChanged                         :
          DeleteGadgets()                                   ;
        break                                               ;
      }                                                     ;
      return QGraphicsItem::itemChange(change,value)        ;
    }
    """
    ##########################################################################
    return super ( ) . itemChange   ( change , value                         )
  ############################################################################
  def ImageWidth                 ( self                                    ) :
    ##########################################################################
    if                           ( self . Image in [ False , None ]        ) :
      return 0
    ##########################################################################
    return self . Image . width  (                                           )
  ############################################################################
  def ImageHeight                ( self                                    ) :
    ##########################################################################
    if                           ( self . Image in [ False , None ]        ) :
      return 0
    ##########################################################################
    return self . Image . height (                                           )
  ############################################################################
  def ImageSize                  ( self                                    ) :
    ##########################################################################
    if                           ( self . Image in [ False , None ]        ) :
      return QSize               ( 0 , 0                                     )
    ##########################################################################
    return self . Image . size   (                                           )
  ############################################################################
  def ImageCm                      ( self                                  ) :
    ##########################################################################
    S = self . ImageSize           (                                         )
    X = self . Options . imageToCm ( S . width  ( )                          )
    Y = self . Options . imageToCm ( S . height ( )                          )
    ##########################################################################
    return QSizeF                  ( X , Y                                   )
  ############################################################################
  def FetchImage                     ( self , DB , UUID                    ) :
    ##########################################################################
    PICTAB = self . Tables           [ "Information"                         ]
    DOPTAB = self . Tables           [ "Depot"                               ]
    ##########################################################################
    self . PICOP = PictureItem       (                                       )
    ##########################################################################
    INFO   = self . PICOP . GetInformation ( DB , PICTAB , UUID              )
    if                               ( INFO in [ False , None ]            ) :
      return None , { }
    ##########################################################################
    QQ     = f"select `file` from {DOPTAB} where ( `uuid` = {UUID} ) ;"
    OKAY   = self . PICOP . FromDB   ( DB , QQ                               )
    ##########################################################################
    if                               ( not OKAY                            ) :
      return None , INFO
    ##########################################################################
    IMAGE  = self . PICOP . toQImage (                                       )
    ##########################################################################
    return IMAGE , INFO
  ############################################################################
  def LoadImage             ( self , Uuid                                  ) :
    ##########################################################################
    self . setObjectUuid    ( Uuid                                           )
    ##########################################################################
    DB   = self . ConnectDB ( UsePure = True                                 )
    if                      ( DB in [ False , None ]                       ) :
      return False
    ##########################################################################
    self . Original = None
    self . Image , self . Details = self . FetchImage ( DB , Uuid            )
    ##########################################################################
    DB   . Close            (                                                )
    ##########################################################################
    return                  ( self . Image not in [ False , None ]           )
  ############################################################################
  def setImage                       ( self , image , details = { }        ) :
    ##########################################################################
    self . Image    = image
    self . Original = None
    self . Details  = details
    ##########################################################################
    return
  ############################################################################
  def asImageRect                    ( self                                ) :
    ##########################################################################
    SM   = self       . ImageSize    (                                       )
    PM   = QPoint                    ( SM . width ( ) , SM . height ( )      )
    SP   = self . Gui . mapToScene   ( PM                                    )
    FS   = self       . mapFromScene ( SP                                    )
    MP   = self       . pointToPaper ( FS                                    )
    ##########################################################################
    self . Xratio     = SM . width  ( ) / FS . x (                           )
    self . Yratio     = SM . height ( ) / FS . y (                           )
    ##########################################################################
    self . ScreenRect = QRectF       ( 0.0 , 0.0 , FS . x ( ) , FS . y ( )   )
    self . PaperRect  = QRectF       ( 0.0 , 0.0 , MP . x ( ) , MP . y ( )   )
    self . prepareGeometryChange     (                                       )
    ##########################################################################
    return
  ############################################################################
  def OriginalRect                   ( self                                ) :
    ##########################################################################
    SM   = self       . ImageSize    (                                       )
    WW   = SM . width  ( ) / self . Xratio
    HH   = SM . height ( ) / self . Yratio
    MP   = self       . pointToPaper ( QPointF ( WW , HH )                   )
    ##########################################################################
    self . ScreenRect = QRectF       ( 0.0 , 0.0 , WW         , HH           )
    self . PaperRect  = QRectF       ( 0.0 , 0.0 , MP . x ( ) , MP . y ( )   )
    ##########################################################################
    super ( ) . setPos     ( QPointF ( 0.0 , 0.0 )                           )
    self . prepareGeometryChange     (                                       )
    ##########################################################################
    return
  ############################################################################
  def PictureRectToItemQRect ( self , sitem , pt , RT                      ) :
    ##########################################################################
    RX = self . Xratio
    RY = self . Yratio
    ##########################################################################
    BX = pt   . x            (                                               )
    BY = pt   . y            (                                               )
    ##########################################################################
    XX = RT                  [ "X"                                           ]
    YY = RT                  [ "Y"                                           ]
    WW = RT                  [ "W"                                           ]
    HH = RT                  [ "H"                                           ]
    ##########################################################################
    XX = float               ( BX + XX                                       )
    YY = float               ( BY + YY                                       )
    ##########################################################################
    XX = float               ( float ( XX ) / RX                             )
    YY = float               ( float ( YY ) / RY                             )
    WW = float               ( float ( WW ) / RX                             )
    HH = float               ( float ( HH ) / RY                             )
    RF = QRectF              ( XX , YY , WW , HH                             )
    ##########################################################################
    RR = self . mapToItem    ( sitem , RF                                    )
    ##########################################################################
    XX = RR [ 0 ] . x        (                                               )
    YY = RR [ 0 ] . y        (                                               )
    WW = RR [ 2 ] . x        (                                               )
    HH = RR [ 2 ] . y        (                                               )
    ##########################################################################
    WW = float               ( WW - XX                                       )
    HH = float               ( HH - YY                                       )
    ##########################################################################
    return QRectF            ( XX , YY , WW , HH                             )
  ############################################################################
  def PictureRectsToItemQRects            ( self , sitem , pt , RECTs      ) :
    ##########################################################################
    QRs   =                               [                                  ]
    ##########################################################################
    for R in RECTs                                                           :
      ########################################################################
      D   = self . PictureRectToItemQRect ( sitem , pt , R                   )
      QRs . append                        ( D                                )
    ##########################################################################
    return QRs
  ############################################################################
  def PictureRectToLocalRect ( self , sitem , PT , RT                      ) :
    ##########################################################################
    RX = self . Xratio
    RY = self . Yratio
    ##########################################################################
    BX = PT   . x            (                                               )
    BY = PT   . y            (                                               )
    ##########################################################################
    XX = RT                  [ "X"                                           ]
    YY = RT                  [ "Y"                                           ]
    WW = RT                  [ "W"                                           ]
    HH = RT                  [ "H"                                           ]
    ##########################################################################
    XX = float               ( BX + XX                                       )
    YY = float               ( BY + YY                                       )
    ##########################################################################
    BX = float               ( float ( BX ) / RX                             )
    BY = float               ( float ( BY ) / RY                             )
    PZ = QPointF             ( BX , BY                                       )
    ##########################################################################
    PB = self . mapToItem    ( sitem , PZ                                    )
    ##########################################################################
    XX = float               ( float ( XX ) / RX                             )
    YY = float               ( float ( YY ) / RY                             )
    WW = float               ( float ( WW ) / RX                             )
    HH = float               ( float ( HH ) / RY                             )
    RF = QRectF              ( XX , YY , WW , HH                             )
    ##########################################################################
    RR = self . mapToItem    ( sitem , RF                                    )
    ##########################################################################
    XX = RR [ 0 ] . x        (                                               )
    YY = RR [ 0 ] . y        (                                               )
    WW = RR [ 2 ] . x        (                                               )
    HH = RR [ 2 ] . y        (                                               )
    ##########################################################################
    WW = float               ( WW - XX                                       )
    HH = float               ( HH - YY                                       )
    ##########################################################################
    return                   { "X" : XX , "Y" : YY , "W" : WW , "H" : HH     }
  ############################################################################
  def PictureRectsToLocalRects            ( self , sitem , PT , RECTs      ) :
    ##########################################################################
    QRs   =                               [                                  ]
    ##########################################################################
    for R in RECTs                                                           :
      ########################################################################
      D   = self . PictureRectToLocalRect (        sitem , PT , R            )
      QRs . append                        ( D                                )
    ##########################################################################
    return QRs
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  def MountZLevel            ( self , proxy , slider                       ) :
    ##########################################################################
    self . Proxys  [ 1 ] = proxy
    self . Widgets [ 1 ] = slider
    ##########################################################################
    R     = self . PanelRect (                                               )
    proxy . setGeometry      ( R                                             )
    proxy . setZValue        ( 0.90                                          )
    proxy . setOpacity       ( 0.50                                          )
    ##########################################################################
    return
  ############################################################################
  def MountOpacity           ( self , proxy , slider                       ) :
    ##########################################################################
    self . Proxys  [ 2 ] = proxy
    self . Widgets [ 2 ] = slider
    ##########################################################################
    R     = self . PanelRect (                                               )
    proxy . setGeometry      ( R                                             )
    proxy . setZValue        ( 0.90                                          )
    proxy . setOpacity       ( 0.50                                          )
    ##########################################################################
    return
  ############################################################################
  def MountRotation           ( self , proxy , dial                        ) :
    ##########################################################################
    self . Proxys  [ 3 ] = proxy
    self . Widgets [ 3 ] = dial
    ##########################################################################
    R     = self . CenterRect (                                              )
    z     = self . zValue     (                                              )
    z     = z + 0.90
    if                        ( z > 1.0                                    ) :
      z   = 1.0
    ##########################################################################
    proxy . setGeometry       ( R                                            )
    proxy . setZValue         ( z                                            )
    proxy . setOpacity        ( 0.75                                         )
    ##########################################################################
    return
  ############################################################################
  def RotationUpdated    ( self                                            ) :
    ##########################################################################
    T    = self . Transform
    T    = T    . rotate ( self . Angle                                      )
    self . setTransform  ( T                                                 )
    ##########################################################################
    return
  ############################################################################
  def NormalTransform   ( self                                             ) :
    ##########################################################################
    T    = QTransform   (                                                    )
    T    . reset        (                                                    )
    self . Angle = 0.0
    sx   = self . Options . DPIX
    sy   = self . Options . DPIY
    sx   = sx / self . PictureDPI
    sy   = sy / self . PictureDPI
    T    = T . scale    ( sx , sy                                            )
    self . Transform = T
    self . setTransform ( T                                                  )
    ##########################################################################
    return
  ############################################################################
  def AttachDPI ( self ) :
    ##########################################################################
    """
    QDoubleSpinBox * dpi = new QDoubleSpinBox();
    QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget(this);
    proxy->setWidget(dpi);
    dpi->setRange(1,9600);
    dpi->setValue(PictureDPI);
    dpi->setSingleStep(1);
    connect(dpi,SIGNAL(valueChanged(double)),this,SLOT(modifyDPI(double)));
    Proxys  [4] = proxy       ;
    Widgets [4] = dpi         ;
    QRectF R = PanelRect()    ;
    proxy->setGeometry(R    ) ;
    proxy->setZValue  (0.90f) ;
    proxy->setOpacity (0.50f) ;
    QFont Font = plan->fonts[Fonts::ComboBox] ;
    Font.setPixelSize(R.height());
    dpi->setFont(Font);
    """
    ##########################################################################
    return
  ############################################################################
  def ModifyDPI ( self , dpi ) :
    ##########################################################################
    """
    QTransform T                                        ;
    T.reset()                                           ;
    qreal sx = Options->DPI                             ;
    qreal sy = Options->DPI                             ;
    PictureDPI = dpi                                    ;
    sx /= PictureDPI                                    ;
    sy /= PictureDPI                                    ;
    T = T.scale(sx,sy)                                  ;
    Transform = T                                       ;
    T = T.rotate(Angle)                                 ;
    setTransform(T)                                     ;
    QRectF SR = mapToScene (ScreenRect ).boundingRect() ;
    PaperRect = Options -> Standard (SR)                ;
    setToolTip                                          (
      tr("Picture UUID : %1\n"
         "%2 x %3 pixels\n"
         "%4 DPI\n"
         "%5 x %6 cm\n"
         "Center : %7 x %8 cm"                      )
      .arg(uuid                                     )
      .arg(Image    .width()).arg(Image    .height())
      .arg(PictureDPI                               )
      .arg(PaperRect.width()).arg(PaperRect.height())
      .arg(PaperPos .x    ()).arg(PaperPos .y     ())
    )                                                   ;
    prepareGeometryChange  (           )                ;
    """
    ##########################################################################
    return
  ############################################################################
  def AdjustContrast ( self ) :
    ##########################################################################
    """
    QSlider              * slider = new QSlider(Qt::Horizontal);
    QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget(this);
    proxy->setWidget(slider);
    Proxys  [5] = proxy       ;
    Widgets [5] = slider      ;
    QRectF R = PanelRect()    ;
    proxy->setGeometry(R)     ;
    proxy->setZValue  (0.90f) ;
    proxy->setOpacity (0.50f) ;
    slider->setRange(-255,255);
    slider->setValue(0);
    Original = Image ;
    connect(slider,SIGNAL(valueChanged(int)),this,SLOT(contrastChanged(int)));
    """
    ##########################################################################
    return
  ############################################################################
  def ContrastChanged ( self , contrast ) :
    ##########################################################################
    """
    PictureManager PM ( plan )                   ;
    Image = PM.AdjustContrast(Original,contrast) ;
    update ( )                                   ;
    """
    ##########################################################################
    return
  ############################################################################
  def UnsharpMask ( self ) :
    ##########################################################################
    """
    QSlider              * slider = new QSlider(Qt::Horizontal);
    QGraphicsProxyWidget * proxy  = new QGraphicsProxyWidget(this);
    proxy->setWidget(slider);
    Proxys  [6] = proxy       ;
    Widgets [6] = slider      ;
    QRectF R = PanelRect()    ;
    proxy->setGeometry(R)     ;
    proxy->setZValue  (0.90f) ;
    proxy->setOpacity (0.50f) ;
    slider->setRange(-255,255);
    slider->setValue(0);
    Original = Image ;
    connect(slider,SIGNAL(valueChanged(int)),
            this,SLOT(usmChanged(int)));
    """
    ##########################################################################
    return
  ############################################################################
  def usmChanged ( self , sharpen ) :
    ##########################################################################
    """
    PictureManager PM ( plan )                         ;
    Image = PM.UnsharpMask(Original,20,3,0.0,contrast) ;
    update ( )                                         ;
    """
    ##########################################################################
    return
  ############################################################################
  def JoinColorGroup ( self ) :
    ##########################################################################
    """
    SUID            uu = 0                           ;
    UUIDs           Uuids                            ;
    Colors          Colors                           ;
    GraphicsManager GM ( plan )                      ;
    EnterSQL(SC,plan->sql)                           ;
      Uuids = SC.Uuids                               (
                PlanTable(ColorGroups)               ,
                "uuid"                               ,
                SC.OrderByAsc("id")                ) ;
    LeaveSQL(SC,plan->sql)                           ;
    //////////////////////////////////////////////////
    if (Uuids.count()<=0)                            {
      Alert ( Error )                                ;
      return                                         ;
    }                                                ;
    //////////////////////////////////////////////////
    UuidSelection * NUS                              ;
    NUS = new UuidSelection(GraphicsView(),plan)     ;
    NUS->setWindowTitle(tr("Join color group"))      ;
    NUS->setUuids(Uuids)                             ;
    if (NUS->exec()==QDialog::Accepted)              {
      uu = NUS->currentUuid()                        ;
    }                                                ;
    NUS->deleteLater()                               ;
    nDropOut ( uu <= 0 )                             ;
    //////////////////////////////////////////////////
    EnterSQL(XC,plan->sql)                           ;
      GM        . LoadColors ( XC,uu , Colors )      ;
      Graphics :: toColors   ( Image , Colors )      ;
      GM        . SaveColors ( XC,uu , Colors )      ;
    LeaveSQL(XC,plan->sql)                           ;
    //////////////////////////////////////////////////
    Alert ( Done )                                   ;
    """
    ##########################################################################
    return
  ############################################################################
  def SaveAs ( self ) :
    ##########################################################################
    """
    QString filename = QFileDialog::getSaveFileName (
                         GraphicsView()             ,
                         QString::number(uuid)      ,
                         plan->Path("Images")       ,
                         "*.png *.jpg"            ) ;
    if (filename.length()<=0) return                ;
    Image.save(filename)                            ;
    Alert ( Done )                                  ;
    """
    ##########################################################################
    return
  ############################################################################
  def InformationMenu              ( self , mm                             ) :
    ##########################################################################
    if                             ( self . Image in [ False , None ]      ) :
      return mm
    ##########################################################################
    UUID   = self . ObjectUuid     (                                         )
    if                             ( UUID > 0                              ) :
      ########################################################################
      UXID = str                   ( UUID                                    )
      mm   . addAction             ( 43521101 , UXID                         )
    ##########################################################################
    W      = self . Image . width  (                                         )
    H      = self . Image . height (                                         )
    MSG    = f"{W} x {H}"
    mm     . addAction             ( 43521102 , MSG                          )
    ##########################################################################
    mm     . addSeparator          (                                         )
    ##########################################################################
    return mm
  ############################################################################
  def Menu                    ( self , gview , pos , spos                  ) :
    ##########################################################################
    mm     = MenuManager      ( gview                                        )
    self   . InformationMenu  ( mm                                           )
    ##########################################################################
    self   . StatesMenu       ( mm                                           )
    ##########################################################################
    mm     . setFont          ( gview   . menuFont ( )                       )
    aa     = mm . exec_       ( QCursor . pos      ( )                       )
    at     = mm . at          ( aa                                           )
    ##########################################################################
    if                        ( self . RunStatesMenu ( at )                ) :
      return True
    ##########################################################################
    """
    bool N::VcfPicture::showMenu(QGraphicsView * view,QPoint global)
    {
      nScopedMenu ( mm , view )                          ;
      bool movable = IsMask (flags(),ItemIsMovable)      ;
      QMenu      * ma = NULL                             ;
      QMenu      * me = NULL                             ;
      QMenu      * mp = NULL                             ;
      QMenu      * mc = NULL                             ;
      QAction    * a  = NULL                             ;
      me = mm.addMenu(tr("Edit"))                        ;
      if (uuid> 0) mm.add(me,23,tr("Drag" ))             ;
      if (uuid<=0) mm.add(me,24,tr("Store" ))            ;
          mm.addSeparator(me)                            ;
      if (uuid> 0) mm.add(me,25,tr("Load selections"))   ;
          mm.add(me,21,tr("Create selection area"))      ;
          mm.add(me,22,tr("Create canvas"))              ;
          mm.addSeparator(me)                            ;
          mm.add(me,26,tr("Save as" ))                   ;
          mm.add(me, 1,tr("Delete" ))                    ;
      ma = mm.addMenu(tr("Adjustments"))                 ;
      a  = mm.add(ma, 2,tr("Overlay"))                   ;
      a->setCheckable(true); a->setChecked(Overlay)      ;
      a  = mm.add(ma, 3,tr("Movable"))                   ;
      a->setCheckable(true); a->setChecked(movable)      ;
      a  = mm.add(ma, 4,tr("Resizable"))                 ;
      a->setCheckable(true); a->setChecked(Scaling)      ;
          mm.addSeparator(ma)                            ;
          mm.add(ma,11,tr("DPI"    ))                    ;
          mm.add(ma,12,tr("Z Level"))                    ;
          mm.add(ma,13,tr("Opacity"))                    ;
          mm.add(ma,14,tr("Rotate" ))                    ;
          mm.add(ma,15,tr("Normal" ))                    ;
      mc = mm.addMenu(tr("Channels"))                    ;
      mm.add(mc,75,tr("Extract red channel"  ))          ;
      mm.add(mc,76,tr("Extract green channel"))          ;
      mm.add(mc,77,tr("Extract blue channel" ))          ;
      mm.add(mc,78,tr("Extract alpha channel"))          ;
      mm.addSeparator(mc)                                ;
      mm.add(mc,79,tr("Picture colors join color group"));
      mp = mm.addMenu(tr("Process"))                     ;
          mm.add(mp,81,tr("Filters"))                    ;
      if (plan->classifiers.count()>0)                   {
          mm.add(mp,52,tr("Human faces detection"))      ;
          mm.add(mp,53,tr("Human faces analysis" ))      ;
      }                                                  ;
          mm.addSeparator(mp)                            ;
          mm.add(mp,82,tr("Grey image"     ))            ;
          mm.add(mp,83,tr("Invert RGB"     ))            ;
          mm.add(mp,84,tr("Median smooth"  ))            ;
          mm.add(mp,85,tr("Gaussian smooth"))            ;
          mm.add(mp,86,tr("Blur"           ))            ;
          mm.addSeparator(mp                )            ;
          mm.add(mp,87,tr("Erode"          ))            ;
          mm.add(mp,88,tr("Dilate"         ))            ;
          mm.addSeparator(mp)                            ;
          mm.add(mp,89,tr("Contrast"))                   ;
          mm.add(mp,90,tr("Unsharp mask"))               ;
          mm.addSeparator(mp)                            ;
          mm.add(mp,91,tr("Color distribution"))         ;
          mm.add(mp,92,tr("Transform"))                  ;
          mm.addSeparator(mp)                            ;
          mm.add(mp,93,tr("Feature points"))             ;
          mm.setFont(plan)                               ;
      a = mm.exec(global)                                ;
      if (IsNull(a)) return false                        ;
      PictureManager PM ( plan )                         ;
      QImage   * II                                      ;
      IplImage * image                                   ;
      IplImage * result                                  ;
      switch (mm[a])                                     {
        case  1                                          :
          emit Delete (this)                             ;
        break                                            ;
        case  2                                          :
          Overlay   = a->isChecked()                     ;
        break                                            ;
        case  3                                          :
          movable   = a->isChecked()                     ;
          setFlag ( ItemIsMovable , movable )            ;
        break                                            ;
        case  4                                          :
          Scaling = a->isChecked()                       ;
        break                                            ;
        case 11                                          :
          DeleteGadgets  ()                              ;
          AttachDPI      ()                              ;
        break                                            ;
        case 12                                          :
          DeleteGadgets  ()                              ;
          AttachZLevel   ()                              ;
        break                                            ;
        case 13                                          :
          DeleteGadgets  ()                              ;
          AttachOpacity  ()                              ;
        break                                            ;
        case 14                                          :
          DeleteGadgets  ()                              ;
          AttachRotation ()                              ;
        break                                            ;
        case 15                                          :
          DeleteGadgets  ()                              ;
          NormalTransform()                              ;
        break                                            ;
        case 21                                          :
          emit Selection ( this , ScreenRect )           ;
        break                                            ;
        case 22                                          :
          emit Canvas    ( this , ScreenRect )           ;
        break                                            ;
        case 23                                          :
          Drag  ( )                                      ;
        break                                            ;
        case 24                                          :
          Store ( )                                      ;
        break                                            ;
        case 25                                          :
          emit LoadSelections ( this )                   ;
        break                                            ;
        case 26                                          :
          SaveAs              (      )                   ;
        break                                            ;
        case 52                                          :
          emit Faces          ( this )                   ;
        break                                            ;
        case 53                                          :
          emit FacesAnalysis  ( this )                   ;
        break                                            ;
        case 75                                          :
          emit Channel        ( this , 0 )               ;
        break                                            ;
        case 76                                          :
          emit Channel        ( this , 1 )               ;
        break                                            ;
        case 77                                          :
          emit Channel        ( this , 2 )               ;
        break                                            ;
        case 78                                          :
          emit Channel        ( this , 3 )               ;
        break                                            ;
        case 79                                          :
          JoinColorGroup      (          )               ;
        break                                            ;
        case 81                                          :
          emit Process        ( this )                   ;
        break                                            ;
        case 82                                          :
          image  = PM.toIplImage( Image  )               ;
          result = PM.toGrey    ( image  )               ;
          II     = PM.toImage   ( result )               ;
          Image  = *II                                   ;
          delete II                                      ;
          PM . Release ( image  )                        ;
          PM . Release ( result )                        ;
          update ( )                                     ;
        break                                            ;
        case 83                                          :
          Image.invertPixels ()                          ;
          update ( )                                     ;
        break                                            ;
        case 84                                          :
          image  = PM.toIplImage ( Image  )              ;
          result = PM.Median     ( image  )              ;
          II     = PM.toImage    ( result )              ;
          if (NotNull(II)) Image = *II                   ;
          PM     . Release       ( image  )              ;
          PM     . Release       ( result )              ;
          if (NotNull(II)) delete II                     ;
          update ( )                                     ;
        break                                            ;
        case 85                                          :
          image  = PM.toIplImage ( Image  )              ;
          result = PM.Gaussian   ( image  )              ;
          II     = PM.toImage    ( result )              ;
          if (NotNull(II)) Image = *II                   ;
          PM     . Release       ( image  )              ;
          PM     . Release       ( result )              ;
          if (NotNull(II)) delete II                     ;
          update ( )                                     ;
        break                                            ;
        case 86                                          :
          image  = PM.toIplImage ( Image  )              ;
          result = PM.Blur       ( image  )              ;
          II     = PM.toImage    ( result )              ;
          if (NotNull(II)) Image = *II                   ;
          PM     . Release       ( image  )              ;
          PM     . Release       ( result )              ;
          if (NotNull(II)) delete II                     ;
          update ( )                                     ;
        break                                            ;
        case 87                                          :
          image  = PM.toIplImage ( Image  )              ;
          result = PM.Erode      ( image  )              ;
          II     = PM.toImage    ( result )              ;
          if (NotNull(II)) Image = *II                   ;
          PM     . Release       ( image  )              ;
          PM     . Release       ( result )              ;
          if (NotNull(II)) delete II                     ;
          update ( )                                     ;
        break                                            ;
        case 88                                          :
          image  = PM.toIplImage ( Image  )              ;
          result = PM.Dilate     ( image  )              ;
          II     = PM.toImage    ( result )              ;
          if (NotNull(II)) Image = *II                   ;
          PM     . Release       ( image  )              ;
          PM     . Release       ( result )              ;
          if (NotNull(II)) delete II                     ;
          update ( )                                     ;
        break                                            ;
        case 89                                          :
          DeleteGadgets  ()                              ;
          AdjustContrast ()                              ;
        break                                            ;
        case 90                                          :
          DeleteGadgets  ()                              ;
          UnsharpMask    ()                              ;
        break                                            ;
        case 91                                          :
          emit ColorDistribution ( this )                ;
        break                                            ;
        case 92                                          :
          emit TransformPicture  ( this )                ;
        break                                            ;
        case 93                                          :
          emit KeyPoints         ( this )                ;
        break                                            ;
      }                                                  ;
      return true                                        ;
    }
    """
    ##########################################################################
    return
##############################################################################
"""
class Q_VCF_EXPORT VcfPicture : public VcfRectangle
                              , public Object
{
  Q_OBJECT
  public:

    enum { Type = UserType + VCF::Picture };
    virtual int type(void) const { return Type; }

    explicit VcfPicture                (VcfConstructor) ;
    virtual ~VcfPicture                (void);

    QByteArray Configuration           (void);
    bool       setConfiguration        (QByteArray & configuration);

  public slots:

    virtual void Drag                  (void) ;
    virtual void Store                 (void) ;

  signals:

    void Menu                          (VcfPicture * picture,QPointF pos);
    void Delete                        (VcfPicture * picture);
    void Process                       (VcfPicture * picture);
    void Faces                         (VcfPicture * picture);
    void FacesAnalysis                 (VcfPicture * picture);
    void Store                         (VcfPicture * picture);
    void LoadSelections                (VcfPicture * picture);
    void ColorDistribution             (VcfPicture * picture);
    void TransformPicture              (VcfPicture * picture);
    void KeyPoints                     (VcfPicture * picture);
    void Channel                       (VcfPicture * picture,int Component);

};

void N::VcfPicture::Drag(void)
{
  if (uuid<=0) return                                      ;
  QMimeData * mime = new QMimeData()                       ;
  QByteArray  data((const char *)&uuid,sizeof(SUID))       ;
  mime->setData("picture/uuid",data)                       ;
  QDrag * drag = new QDrag (GraphicsView())                ;
  Qt::DropAction dropAction                                ;
  drag->setMimeData(mime)                                  ;
  dropAction = drag->exec(Qt::CopyAction | Qt::MoveAction) ;
}

void N::VcfPicture::Store(void)
{
  PictureManager PM              ( plan ) ;
  SUID puid    = 0                        ;
  bool success = false                    ;
  success = PM . Import ( Image , puid )  ;
  if ( puid > 0 ) uuid = puid             ;
  emit Store ( this )                     ;
}

typedef struct            {
  bool   overlay          ;
  double x                ;
  double y                ;
  double z                ;
  double left             ;
  double top              ;
  double width            ;
  double height           ;
  double opacity          ;
  double rotation         ;
  double dpi              ;
  double m11              ;
  double m12              ;
  double m13              ;
  double m21              ;
  double m22              ;
  double m23              ;
  double m31              ;
  double m32              ;
  double m33              ;
} VcfPictureConfiguration ;

QByteArray N::VcfPicture::Configuration(void)
{
  QByteArray configuration                                          ;
  configuration.resize(sizeof(VcfPictureConfiguration))             ;
  VcfPictureConfiguration VPC                                       ;
  VPC.overlay  = Overlay                                            ;
  VPC.x        = PaperPos.x             ()                          ;
  VPC.y        = PaperPos.y             ()                          ;
  VPC.z        = zValue                 ()                          ;
  VPC.left     = ScreenRect.left        ()                          ;
  VPC.top      = ScreenRect.top         ()                          ;
  VPC.width    = ScreenRect.width       ()                          ;
  VPC.height   = ScreenRect.height      ()                          ;
  VPC.opacity  = QGraphicsItem::opacity ()                          ;
  VPC.rotation = Angle                                              ;
  VPC.dpi      = PictureDPI                                         ;
  VPC.m11      = Transform.m11          ()                          ;
  VPC.m12      = Transform.m12          ()                          ;
  VPC.m13      = Transform.m13          ()                          ;
  VPC.m21      = Transform.m21          ()                          ;
  VPC.m22      = Transform.m22          ()                          ;
  VPC.m23      = Transform.m23          ()                          ;
  VPC.m31      = Transform.m31          ()                          ;
  VPC.m32      = Transform.m32          ()                          ;
  VPC.m33      = Transform.m33          ()                          ;
  memcpy(configuration.data(),&VPC,sizeof(VcfPictureConfiguration)) ;
  return configuration                                              ;
}

bool N::VcfPicture::setConfiguration(QByteArray & configuration)
{
  if (IsNull(Options))                                       return false ;
  if (configuration.size()!=sizeof(VcfPictureConfiguration)) return false ;
  VcfPictureConfiguration * VPC = (VcfPictureConfiguration *)configuration.data();
  Overlay = VPC->overlay                                   ;
  PaperPos.setX(VPC->x)                                    ;
  PaperPos.setY(VPC->y)                                    ;
  QGraphicsItem::setPos(Options->position(PaperPos))       ;
  setZValue  (VPC->z      )                                ;
  setOpacity (VPC->opacity)                                ;
  ScreenRect . setLeft   (VPC->left  )                     ;
  ScreenRect . setTop    (VPC->top   )                     ;
  ScreenRect . setWidth  (VPC->width )                     ;
  ScreenRect . setHeight (VPC->height)                     ;
  Angle      = VPC->rotation                               ;
  PictureDPI = VPC->dpi                                    ;
  Transform.setMatrix                                      (
    VPC->m11,VPC->m12,VPC->m13                             ,
    VPC->m21,VPC->m22,VPC->m23                             ,
    VPC->m31,VPC->m32,VPC->m33                           ) ;
  QTransform T = Transform                                 ;
  T = T.rotate(Angle)                                      ;
  setTransform(T)                                          ;
  QRectF SR = mapToScene (ScreenRect ).boundingRect()      ;
  PaperRect = Options -> Standard (SR)                     ;
  setToolTip                                               (
    tr("%1 x %2 pixels\n"
       "%3 DPI\n"
       "%4 x %5 cm\n"
       "Center : %6 x %7 cm"
       )
    .arg(Image    .width()).arg(Image    .height())
    .arg(PictureDPI                               )
    .arg(PaperRect.width()).arg(PaperRect.height())
    .arg(PaperPos .x    ()).arg(PaperPos .y     ())
  )                                                        ;
  prepareGeometryChange  (           )                     ;
  return true;
}
"""
