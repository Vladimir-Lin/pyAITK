# -*- coding: utf-8 -*-
##############################################################################
## Contour
##############################################################################
import math
##############################################################################
from   PyQt5 . QtCore import QPointF
from   PyQt5 . QtCore import QRectF
##############################################################################
from   PyQt5 . QtGui  import QColor
from   PyQt5 . QtGui  import QVector3D
##############################################################################
from . ControlPoint   import ControlPoint as ControlPoint
##############################################################################
class Contour    (                                                         ) :
  ############################################################################
  def __init__   ( self                                                    ) :
    ##########################################################################
    self . clear (                                                           )
    ##########################################################################
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def clear                          ( self                                ) :
    ##########################################################################
    self . Uuid       = 0
    self . Name       = ""
    self . Type       = 0x00010000
    self . Closed     = False
    self . Substract  = False
    self . Index      =              [                                       ]
    self . Thickness  = ControlPoint (                                       )
    self . Points     =              {                                       }
    self . Properties =              {                                       }
    ##########################################################################
    self . Thickness  . setXYZ       ( 0.05 , 0.05 , 0.05                    )
    ##########################################################################
    return
  ############################################################################
  def assign ( self , contour                                              ) :
    ##########################################################################
    self . Uuid       = contour . Uuid
    self . Name       = contour . Name
    self . Type       = contour . Type
    self . Closed     = contour . Closed
    self . Substract  = contour . Substract
    self . Index      = contour . Index
    self . Thickness  . assign ( contour . Thickness                         )
    self . Points     = contour . Points
    self . Properties = contour . Properties
    ##########################################################################
    return
  ############################################################################
  def setProperty ( self , item , value                                    ) :
    ##########################################################################
    self . Properties [ item ] = value
    ##########################################################################
    return
  ############################################################################
  def getProperty            ( self , item                                 ) :
    return self . Properties [        item                                   ]
  ############################################################################
  def toJson ( self                                                        ) :
    ##########################################################################
    JSON =   {                                                               }
    ##########################################################################
    return JSON
  ############################################################################
  def count    ( self                                                      ) :
    return len ( self . Index                                                )
  ############################################################################
  def begin         ( self                                                 ) :
    ##########################################################################
    self . Index  = [                                                        ]
    self . Points = {                                                        }
    ##########################################################################
    return
  ############################################################################
  def add                 ( self , Id , point                              ) :
    ##########################################################################
    self . Index . append ( Id                                               )
    self . Points [ Id ] = point
    ##########################################################################
    return self . count   (                                                  )
  ############################################################################
  def remove                ( self , Id                                    ) :
    ##########################################################################
    if                      ( Id in self . Index                           ) :
      self . Index . remove ( Id                                             )
    ##########################################################################
    if                      ( Id in self . Points                          ) :
      del self . Points     [ Id                                             ]
    ##########################################################################
    return self . count     (                                                )
  ############################################################################
  def end                   ( self                                         ) :
    ##########################################################################
    self . Closed = False
    if                      ( self . count ( ) < 1                         ) :
      return
    ##########################################################################
    a    = self . Index     [ 0                                              ]
    ##########################################################################
    self . Points [ a ] . Type = self . Type | 1
    ## self . Points [ a ] . Type = self . type | Graphics::Start
    ##########################################################################
    if                      ( self . count ( ) < 2                         ) :
      return
    ##########################################################################
    b    = self . Index     [ self . count ( ) - 1                           ]
    self . Points [ b ] . Type = Type | 5
    ## self . Points [ b ] . Type = Type | Graphics::End
    ##########################################################################
    return
  ############################################################################
  def close              ( self , t                                        ) :
    ##########################################################################
    self  . Closed = False
    Flags = self . Type | t
    a     = self . Index [ 0                                                 ]
    self  . Points [ a ] . Type = Flags
    ##########################################################################
    if                   ( self . count ( ) < 2                            ) :
      return
    ##########################################################################
    b    = self . Index  [ self . count ( ) - 1                              ]
    self . Points [ b ] . Type = Flags
    self . Closed = True
    ##########################################################################
    return
  ############################################################################
  def find ( self , point , R                                              ) :
    ##########################################################################
    R2 = R * R
    ##########################################################################
    for Id in self . Index                                                   :
      ########################################################################
      if   ( self . Points [ Id ] . Within ( point , R2 )                  ) :
        return i
    ##########################################################################
    return -1
  ############################################################################
  def boundingRect     ( self                                              ) :
    ##########################################################################
    if                 ( len ( self . Points ) <=0                         ) :
      return QRectF    ( 0 , 0 , 0 , 0                                       )
    ##########################################################################
    i      = self . Index  [ 0 ]
    left   = self . points [ i ] . x
    right  = self . points [ i ] . x
    top    = self . points [ i ] . y
    bottom = self . points [ i ] . y
    ##########################################################################
    if                 ( len ( self . Points ) > 1                         ) :
      ########################################################################
      for j in self . Index                                                  :
        ######################################################################
        if             ( i != j                                            ) :
          ####################################################################
          x = self . Points [ j ] . x
          y = self . Points [ j ] . y
          ####################################################################
          if           ( x < left                                          ) :
            left   = x
          ####################################################################
          if           ( x > right                                         ) :
            right  = x
          ####################################################################
          if           ( y < top                                           ) :
            top    = y
          ####################################################################
          if           ( y > bottom                                        ) :
            bottom = y
    ##########################################################################
    R      = QRectF    (                                                     )
    R      . setLeft   ( left                                                )
    R      . setRight  ( right                                               )
    R      . setTop    ( top                                                 )
    R      . setBottom ( bottom                                              )
    ##########################################################################
    return R
  ############################################################################
  def plus         ( self , center                                         ) :
    ##########################################################################
    x = center . x (                                                         )
    y = center . y (                                                         )
    ##########################################################################
    for Id in self . Index                                                   :
      ########################################################################
      self . Points [ Id ] . x = self . Points [ Id ] . x + x
      self . Points [ Id ] . y = self . Points [ Id ] . y + y
    ##########################################################################
    return self
  ############################################################################
  """
  N::Contour & N::Contour::operator += (FeaturePoints & features)
  {
    int L = 0                                           ;
    if (index.count()>0) L = index.last()               ;
    for (int i=0;i<features.count();i++)                {
      ControlPoint point(features[i]->x,features[i]->y) ;
      L++                                               ;
      index << L                                        ;
      points [ L ] = point                              ;
    }                                                   ;
    return ME                                           ;
  }
  """
  ############################################################################
  def minus        ( self , center                                         ) :
    ##########################################################################
    x = center . x (                                                         )
    y = center . y (                                                         )
    ##########################################################################
    for Id in self . Index                                                   :
      ########################################################################
      self . Points [ Id ] . x = self . Points [ Id ] . x - x
      self . Points [ Id ] . y = self . Points [ Id ] . y - y
    ##########################################################################
    return self
  ############################################################################
  def multiply                        ( self , factor                      ) :
    ##########################################################################
    for Id in self . Index                                                   :
      ########################################################################
      self . Points [ Id ] . multiply (        factor                        )
    ##########################################################################
    return self
  ############################################################################
  def Dot               ( self , s                                         ) :
    ##########################################################################
    w      = s . width  (                                                    )
    h      = s . height (                                                    )
    ##########################################################################
    for Id in self . Index                                                   :
      ########################################################################
      self . Points [ Id ] . x = self . Points [ Id ] . x * w
      self . Points [ Id ] . y = self . Points [ Id ] . y * h
    ##########################################################################
    return self
  ############################################################################
  def divide                        ( self , divisor                       ) :
    ##########################################################################
    for Id in self . Index                                                   :
      ########################################################################
      self . Points [ Id ] . divide (        divisor                         )
    ##########################################################################
    return self
##############################################################################
"""
class Q_GEOMETRY_EXPORT Contour
{
  public:

    SUID          uuid      ;
    QString       name      ;
    int           type      ;
    bool          closed    ;
    bool          substract ;
    CUIDs         index     ;
    ControlPoint  thickness ;
    ControlPoints points    ;

    explicit   Contour    (void) ;
               Contour    (const Contour & contour) ;
    virtual   ~Contour    (void) ;

    int        count      (void) ;

    void       begin      (void) ;
    int        add        (int Id,ControlPoint & point) ;
    int        remove     (int Id) ;
    void       end        (void);
    void       close      (int Type = Graphics::Quadratic) ;

    int        find       (QPointF & point,double R) ;

    QByteArray Data       (void);
    void       setData    (QByteArray & contour) ;

    QRectF boundingRect   (void) ;

    Contour & operator  = (const Contour & contour  ) ;
    Contour & operator += (QPointF         center   ) ;
    Contour & operator += (FeaturePoints & features ) ;
    Contour & operator -= (QPointF         center   ) ;
    Contour & operator *= (double          factor   ) ;
    Contour & operator *= (QSizeF          size     ) ;
    Contour & operator /= (double          divisor  ) ;

  protected:

  private:

};

typedef struct {
  int    Index ;
  SUID   Uuid  ;
  int    Type  ;
  int    Unit  ;
  double x     ;
  double y     ;
  double z     ;
  double r     ;
  double t     ;
} ncpData      ;

typedef struct      {
  int     Size      ;
  ncpData Thickness ;
  ncpData Points[1] ;
} ncrData           ;

QByteArray N::Contour::Data(void)
{
  QByteArray C                            ;
  ncrData *  R                            ;
  int Total                               ;
  int s = points . count ( )              ;
  Total  = sizeof(int)                    ;
  Total += sizeof(ncpData)                ;
  Total += sizeof(ncpData) * s            ;
  C . resize ( Total )                    ;
  R = (ncrData *)C.constData()            ;
  memset ( R , 0 , Total )                ;
  R->Size              = s                ;
  R->Thickness.Index   = 0                ;
  R->Thickness.Uuid    = thickness.uuid   ;
  R->Thickness.Type    = thickness.Type   ;
  R->Thickness.Unit    = thickness.Unit   ;
  R->Thickness.x       = thickness.x      ;
  R->Thickness.y       = thickness.y      ;
  R->Thickness.z       = thickness.z      ;
  R->Thickness.r       = thickness.r      ;
  R->Thickness.t       = thickness.t      ;
  for (int i=0;i<index.count();i++)       {
    int idx            = index [ i ]      ;
    R->Points[i].Index = idx              ;
    R->Points[i].Uuid  = points[idx].uuid ;
    R->Points[i].Type  = points[idx].Type ;
    R->Points[i].Unit  = points[idx].Unit ;
    R->Points[i].x     = points[idx].x    ;
    R->Points[i].y     = points[idx].y    ;
    R->Points[i].z     = points[idx].z    ;
    R->Points[i].r     = points[idx].r    ;
    R->Points[i].t     = points[idx].t    ;
  }                                       ;
  return     C                            ;
}

void N::Contour::setData(QByteArray & contours)
{
  ncrData * R = (ncrData *)contours.constData() ;
  int       s = R->Size                         ;
  index   . clear ( )                           ;
  points  . clear ( )                           ;
  thickness.uuid = R->Thickness.Uuid            ;
  thickness.Type = R->Thickness.Type            ;
  thickness.Unit = R->Thickness.Unit            ;
  thickness.x    = R->Thickness.x               ;
  thickness.y    = R->Thickness.y               ;
  thickness.z    = R->Thickness.z               ;
  thickness.r    = R->Thickness.r               ;
  thickness.t    = R->Thickness.t               ;
  for (int i=0;i<s;i++)                         {
    ControlPoint ncp                            ;
    ncp.uuid = R->Points[i].Uuid                ;
    ncp.Type = R->Points[i].Type                ;
    ncp.Unit = R->Points[i].Unit                ;
    ncp.x    = R->Points[i].x                   ;
    ncp.y    = R->Points[i].y                   ;
    ncp.z    = R->Points[i].z                   ;
    ncp.r    = R->Points[i].r                   ;
    ncp.t    = R->Points[i].t                   ;
    add ( R->Points[i].Index , ncp )            ;
  }                                             ;
}
"""
