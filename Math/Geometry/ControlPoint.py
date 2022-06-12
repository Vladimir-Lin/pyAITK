# -*- coding: utf-8 -*-
##############################################################################
## ControlPoint
##############################################################################
import math
##############################################################################
from   PyQt5 . QtCore import QPoint
from   PyQt5 . QtCore import QPointF
##############################################################################
from   PyQt5 . QtGui  import QColor
from   PyQt5 . QtGui  import QVector3D
##############################################################################
"""
typedef enum       {
  Pixel       =   0, /* Not actual unit, used on computer rendition */
  /* Astronomy System */
  Parsec      =   1, /* 206265AU
                        30,856,804,798,079,115 Meters
                        about 3.261567 ly
                      */
  LightYear   =   2, /* 9,460,730,472,580,800 Meters */
  LightDay    =   3, /* 25,902,068,371,200 Meters */
  LightHour   =   4, /* 1,079,252,848,800 Meters */
  AU          =   5, /* 149,597,870,691 Meters */
  LightMinute =   6, /* 17,987,547,480 Meters */
  LightSpeed  =   7, /* 299,792,458 Meters */
  /* SI System */
  Yottametre  = 101, /* 10 ^  24 Meters */
  Zettametre  = 102, /* 10 ^  21 Meters */
  Exametre    = 103, /* 10 ^  18 Meters */
  Petametre   = 104, /* 10 ^  15 Meters */
  Terametre   = 105, /* 10 ^  12 Meters */
  Gigametre   = 106, /* 10 ^   9 Meters */
  Megametre   = 107, /* 10 ^   6 Meters */
  Kilometer   = 108, /* 10 ^   3 Meters */
  Hectometre  = 109, /* 10 ^   2 Meters */
  Decametre   = 110, /* 10 ^   1 Meters */
  Meter       = 111, /* Light Speed : 299792458 Meters */
  Decimeter   = 112, /* 10 ^ - 1 Meter */
  Centimeter  = 113, /* 10 ^ - 2 Meter */
  Millimeter  = 114, /* 10 ^ - 3 Meter */
  Micrometre  = 115, /* 10 ^ - 6 Meter */
  Nanometer   = 116, /* 10 ^ - 9 Meter */
  Angstrom    = 117, /* 10 ^ -10 Meter */
  Picometre   = 118, /* 10 ^ -12 Meter */
  Fermi       = 119, /* 10 ^ -15 Meter */
  Attometer   = 120, /* 10 ^ -18 Meter */
  Zeptometre  = 121, /* 10 ^ -21 Meter */
  Yoctometre  = 122, /* 10 ^ -24 Meter */
  SuperString = 123, /* 10 ^ -33 Meter */
  Planck      = 124, /* 10 ^ -36 Meter */
  MilliPlanck = 125, /* 10 ^ -39 Meter */
  NanoPlanck  = 126, /* 10 ^ -45 Meter */
  /* Imperial Units */
  Mile        = 201, /* 1609.344 Meters */
  Furlong     = 202, /* 220 Yards */
  Chain       = 203, /* 22 Yards */
  Rod         = 204, /* 5.5 Yards , 5.0292 Meters */
  Perch       = 205, /* 5.5 Yards , same name */
  Pole        = 206, /* 5.5 Yards , same name */
  Lug         = 207, /* 5.5 Yards , same name */
  Fathom      = 208, /* 2 Yards , 182.88 Centimeters */
  Yard        = 209, /* 91.44 Centimeters */
  Foot        = 210, /* 30.48 Centimeters */
  Hand        = 211, /* 10.16 Centimeters */
  Inch        = 212, /* 2.54 Centimeters */
  /* Chinese Modern Unit */
  ChineseLi   = 301, /* 500 Meters */
  ChineseYin  = 302, /* 15 Yin = 1 Li */
  ChineseZhang= 303, /* 150 Zhang = 1 Li */
  ChineseBu   = 304, /* 5 Chi */
  ChineseChi  = 305, /* 1500 Chi = 1 Li */
  ChineseCun  = 306, /* 0.1 Chi */
  ChineseFen  = 307, /* 0.01 Chi */
  TangBigFoot = 308, /* 29.6 Centimeters */
  /* Korea , Japan */
  KoreanChi   = 401, /* 35.6 Centimeters */
  /* India Unit */
  YojanaMin   = 501, /* 13 Kilometers */
  Yojana      = 502, /* Yojana average */
  YojanaMax   = 503, /* 16 Kilometers */
  /* Nautical mile */
  Nautical    = 601, /* 1852 Meters */
  Rig         = 602, /* 5556 Meters */
  /* Printing */
  Pica        = 701, /* 12 points */
  Point       = 702, /* 1 point = 127/360 mm about 352.7 um */
  /* Russian  */
  Verst       = 801  /* 1.0668 Kilometer */
} Unit             ;
"""
class ControlPoint        (                                                ) :
  ############################################################################
  DofNone      = 0
  DofTranslate = 1
  DofRotate    = 2
  DofScale     = 3
  ############################################################################
  ContourNone      = 0
  ContourStart     = 1
  ContourFlat      = 2
  ContourCubic     = 3
  ContourQuadratic = 4
  ContourEnd       = 5
  ############################################################################
  ContourLinear    = 0x00010000
  ContourPlane     = 0x00020000
  ContourSolid     = 0x00040000
  ############################################################################
  VerySmall        = 0.000000000000000000000000000000000000001
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
  def clear    ( self                                                      ) :
    ##########################################################################
    self . Uuid = 0
    self . Type = self . ContourLinear | self . ContourNone
    self . DOF  = self . DofNone
    self . Unit = 113
    ## self . Unit = Physics::Centimeter
    self . Flag = 0
    self . x    = 0.0
    self . y    = 0.0
    self . z    = 0.0
    self . t    = 0.0
    self . r    = 0.0
    self . f    = 1.0
    ##########################################################################
    return
  ############################################################################
  def assign   ( self , point                                              ) :
    ##########################################################################
    self . Uuid = point . Uuid
    self . Type = point . Type
    self . DOF  = point . DOF
    self . Unit = point . Unit
    self . Flag = point . Flag
    self . x    = point . x
    self . y    = point . y
    self . z    = point . z
    self . t    = point . t
    self . r    = point . r
    self . f    = point . f
    ##########################################################################
    return
  ############################################################################
  def toJson            ( self                                             ) :
    return              { "Uuid" : self . Uuid                             , \
                          "Type" : self . Type                             , \
                          "DOF"  : self . DOF                              , \
                          "Unit" : self . Unit                             , \
                          "Flag" : self . Flag                             , \
                          "X"    : self . x                                , \
                          "Y"    : self . y                                , \
                          "Z"    : self . z                                , \
                          "T"    : self . t                                , \
                          "R"    : self . r                                , \
                          "F"    : self . f                                  }
  ############################################################################
  def fromJson          ( self , JSON                                      ) :
    ##########################################################################
    self . Uuid = int   ( JSON [ "Uuid"                                    ] )
    self . Type = int   ( JSON [ "Type"                                    ] )
    self . DOF  = int   ( JSON [ "DOF"                                     ] )
    self . Unit = int   ( JSON [ "Unit"                                    ] )
    self . Flag = int   ( JSON [ "Flag"                                    ] )
    self . x    = float ( JSON [ "X"                                       ] )
    self . y    = float ( JSON [ "Y"                                       ] )
    self . z    = float ( JSON [ "Z"                                       ] )
    self . t    = float ( JSON [ "T"                                       ] )
    self . r    = float ( JSON [ "R"                                       ] )
    self . f    = float ( JSON [ "F"                                       ] )
    ##########################################################################
    return self
  ############################################################################
  def Control  ( self                                                      ) :
    return int ( self . Type & 0xFFFF                                        )
  ############################################################################
  def setXYZ       ( self , x , y , z                                      ) :
    ##########################################################################
    self . x = x
    self . y = y
    self . z = z
    ##########################################################################
    return
  ############################################################################
  def setXYZR      ( self , x , y , z , r                                  ) :
    ##########################################################################
    self . x = x
    self . y = y
    self . z = z
    self . r = r
    ##########################################################################
    return
  ############################################################################
  def setXYZT      ( self , x , y , z , t                                  ) :
    ##########################################################################
    self . x = x
    self . y = y
    self . z = z
    self . t = t
    ##########################################################################
    return
  ############################################################################
  def setUnit ( self , unit                                                ) :
    ##########################################################################
    self . Unit = unit
    ##########################################################################
    return
  ############################################################################
  def setDOF ( self , dof                                                  ) :
    ##########################################################################
    self . DOF = dof
    ##########################################################################
    return
  ############################################################################
  def setQPointF     ( self , p                                            ) :
    ##########################################################################
    self . x = p . x (                                                       )
    self . y = p . y (                                                       )
    ##########################################################################
    return self
  ############################################################################
  def setQVector3D   ( self , p                                            ) :
    ##########################################################################
    self . x = p . x (                                                       )
    self . y = p . y (                                                       )
    self . z = p . z (                                                       )
    ##########################################################################
    return self
  ############################################################################
  def setQColor           ( self , c                                       ) :
    ##########################################################################
    self . x = c . redF   (                                                  )
    self . y = c . greenF (                                                  )
    self . z = c . blueF  (                                                  )
    self . t = c . alphaF (                                                  )
    ##########################################################################
    return self
  ############################################################################
  def toQPoint    ( self                                                   ) :
    return QPoint ( int ( self . x ) , int ( self . y )                      )
  ############################################################################
  def toQPointF    ( self                                                  ) :
    return QPointF ( self . x , self . y                                     )
  ############################################################################
  def dpiToQPointF ( self , DPI                                            ) :
    ##########################################################################
    X = self . x
    X = X    * DPI
    X = X    * 100.0
    X = X    / 254.0
    ##########################################################################
    Y = self . y
    Y = Y    * DPI
    Y = Y    * 100.0
    Y = Y    / 254.0
    ##########################################################################
    return QPointF ( X , Y                                                   )
  ############################################################################
  def toQVector3D    ( self                                                ) :
    return QVector3D ( self . x , self . y , self . z                        )
  ############################################################################
  def toQColor    ( self                                                   ) :
    ##########################################################################
    C = QColor    (                                                          )
    ##########################################################################
    C . setRedF   ( self . x                                                 )
    C . setGreenF ( self . y                                                 )
    C . setBlueF  ( self . z                                                 )
    C . setAlphaF ( self . t                                                 )
    ##########################################################################
    return C
  ############################################################################
  def toList2 ( self                                                       ) :
    return    [ self . x , self . y                                          ]
  ############################################################################
  def toList3 ( self                                                       ) :
    return    [ self . x , self . y , self . z                               ]
  ############################################################################
  def toList4 ( self                                                       ) :
    return    [ self . x , self . y , self . z , self . t                    ]
  ############################################################################
  def toColorComponent3 ( self                                             ) :
    ##########################################################################
    R = int             ( self . x * 255                                     )
    G = int             ( self . y * 255                                     )
    B = int             ( self . z * 255                                     )
    ##########################################################################
    return              [ R , G , B                                          ]
  ############################################################################
  def toColorComponent4 ( self                                             ) :
    ##########################################################################
    R = int             ( self . x * 255                                     )
    G = int             ( self . y * 255                                     )
    B = int             ( self . z * 255                                     )
    T = int             ( self . t * 255                                     )
    ##########################################################################
    return [ R , G , B , T ]
  ############################################################################
  def multiply        ( self , factor                                      ) :
    ##########################################################################
    self . x = self . x * factor
    self . y = self . y * factor
    self . z = self . z * factor
    ##########################################################################
    return self
  ############################################################################
  def divide          ( self , divisor                                     ) :
    ##########################################################################
    self . x = self . x / divisor
    self . y = self . y / divisor
    self . z = self . z / divisor
    ##########################################################################
    return self
  ############################################################################
  def VectorDot       ( self , vector                                      ) :
    ##########################################################################
    self . x = self . x * vector . x
    self . y = self . y * vector . y
    self . z = self . z * vector . z
    ##########################################################################
    return self
  ############################################################################
  def VectorPlus      ( self , vector                                      ) :
    ##########################################################################
    self . x = self . x + vector . x
    self . y = self . y + vector . y
    self . z = self . z + vector . z
    ##########################################################################
    return self
  ############################################################################
  def VectorMinus     ( self , vector                                      ) :
    ##########################################################################
    self . x = self . x - vector . x
    self . y = self . y - vector . y
    self . z = self . z - vector . z
    ##########################################################################
    return self
  ############################################################################
  def Within              ( self , p , R2                                  ) :
    ##########################################################################
    dx = self . x - p . x (                                                  )
    dx = dx * dx
    ##########################################################################
    dy = self . y - p . y (                                                  )
    dy = dy * dy
    ##########################################################################
    return                ( ( dx + dy ) < R2                                 )
  ############################################################################
  def length           ( self                                              ) :
    return math . sqrt ( self . lengthSquared ( )                            )
  ############################################################################
  def lengthSquared ( self                                                 ) :
    return          ( self . x * self . x                                ) + \
                    ( self . y * self . y                                ) + \
                    ( self . z * self . z                                    )
  ############################################################################
  def normalize            ( self                                          ) :
    ##########################################################################
    L      = self . length (                                                 )
    ##########################################################################
    if                     ( L <= self . VerySmall                         ) :
      ########################################################################
      self . x = 0.0
      self . y = 0.0
      self . z = 0.0
      ########################################################################
      return
    ##########################################################################
    self   . x = self . x / L
    self   . y = self . y / L
    self   . z = self . z / L
    ##########################################################################
    return
  ############################################################################
  def normalized     ( self                                                ) :
    ##########################################################################
    p = ControlPoint (                                                       )
    p . assign       ( self                                                  )
    p . normalize    (                                                       )
    ##########################################################################
    return p
  ############################################################################
  def distanceToLine                 ( self , point , direction            ) :
    ##########################################################################
    v  = self      . toQVector3D     (                                       )
    p  = point     . toQVector3D     (                                       )
    d  = direction . toQVector3D     (                                       )
    ##########################################################################
    return v       . distanceToLine  ( p , d                                 )
  ############################################################################
  def distanceToPlaneNormal          ( self , plane , normalx              ) :
    ##########################################################################
    v  = self      . toQVector3D     (                                       )
    p  = plane     . toQVector3D     (                                       )
    n  = normalx   . toQVector3D     (                                       )
    ##########################################################################
    return v       . distanceToPlane ( p , n                                 )
  ############################################################################
  def distanceToPlane                ( self , plane1 , plane2 , plane3     ) :
    ##########################################################################
    v  = self      . toQVector3D     (                                       )
    p1 = plane1    . toQVector3D     (                                       )
    p2 = plane2    . toQVector3D     (                                       )
    p3 = plane3    . toQVector3D     (                                       )
    ##########################################################################
    return v       . distanceToPlane ( p1 , p2 , p3                          )
  ############################################################################
  def interpolate    ( self , v1 , v2 , t                                  ) :
    ##########################################################################
    u = ControlPoint (                                                       )
    v = ControlPoint (                                                       )
    u . assign       ( v2                                                    )
    u . VectorMinus  ( v1                                                    )
    u . multiply     ( t                                                     )
    v . assign       ( v1                                                    )
    v . VectorPlus   ( u                                                     )
    ##########################################################################
    return v
  ############################################################################
  def crossProduct        ( self , v1 , v2                                 ) :
    ##########################################################################
    cp     = ControlPoint (                                                  )
    cp . x =              ( v1 . y * v2 . z ) - ( v1 . z * v2 . y )
    cp . y =              ( v1 . z * v2 . x ) - ( v1 . x * v2 . z )
    cp . z =              ( v1 . x * v2 . y ) - ( v1 . y * v2 . x )
    cp . t = 1.0
    ##########################################################################
    return cp
  ############################################################################
  def dotProduct                  ( self , v1 , v2                         ) :
    ##########################################################################
    p1 = v1 . toQVector3D         (                                          )
    p2 = v2 . toQVector3D         (                                          )
    ##########################################################################
    return QVector3D . dotProduct ( p1 , p2                                  )
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
"""
class Q_GEOMETRY_EXPORT ControlPoint
{
  public:

    SUID   uuid ;
    int    Type ;
    int    DOF  ; // Degree of Freedom Type
    int    Unit ;
    int    Flag ;
    double x    ;
    double y    ;
    double z    ;
    double t    ;
    double r    ;
    double f    ;

    explicit ControlPoint          (void) ;
             ControlPoint          (const PackedPoint        & packp) ;
             ControlPoint          (const PackedControlPoint & packp) ;
    virtual ~ControlPoint          (void) ;

    bool           toPacked        (PackedPoint        & packp) ;
    bool           toPacked        (PackedControlPoint & packp) ;

    void Light                     (GLenum light,GLenum pname) ; // OpenGL glLightfv
    void Material                  (GLenum face ,GLenum pname) ; // OpenGL glMaterialfv
    void Vertex3f                  (void) ; // OpenGL glVertex3f
    void Vertex3d                  (void) ; // OpenGL glVertex3d
    void Normal3f                  (void) ; // OpenGL glNormal3f
    void Normal3d                  (void) ; // OpenGL glNormal3d
    void Translatef                (void) ; // OpenGL glTranslatef
    void Translate                 (void) ; // OpenGL glTranslated
    void Rotatef                   (void) ; // OpenGL glRotatef
    void Rotate                    (void) ; // OpenGL glRotated
    void Scalef                    (void) ; // OpenGL glScalef
    void Scale                     (void) ; // OpenGL glScaled
    void Color3f                   (void) ; // OpenGL glColor3f
    void Color4f                   (void) ; // OpenGL glColor4f
    void Color3d                   (void) ; // OpenGL glColor3d
    void Color4d                   (void) ; // OpenGL glColor4d

  protected:

  private:

};

N::ControlPoint:: ControlPoint ( const PackedPoint & p )
                : uuid         ( 0                     )
                , Type         ( Graphics::Linear      |
                                 Graphics::None        )
                , DOF          ( DofNone               )
                , Unit         ( Physics::Centimeter   )
                , Flag         ( 0                     )
                , x            ( p . x                 )
                , y            ( p . y                 )
                , z            ( p . z                 )
                , t            ( p . t                 )
                , r            ( 0                     )
                , f            ( 1                     )
{
}

N::ControlPoint:: ControlPoint ( const PackedControlPoint & p )
                : uuid         ( p . uuid                     )
                , Type         ( p . Type                     )
                , DOF          ( p . DOF                      )
                , Unit         ( p . Unit                     )
                , Flag         ( p . Flag                     )
                , x            ( p . x                        )
                , y            ( p . y                        )
                , z            ( p . z                        )
                , t            ( p . t                        )
                , r            ( p . r                        )
                , f            ( p . f                        )
{
}

N::ControlPoint::~ControlPoint(void)
{
}

bool N::ControlPoint::toPacked(PackedPoint & p)
{
  p . x = x   ;
  p . y = y   ;
  p . z = z   ;
  p . t = t   ;
  return true ;
}

bool N::ControlPoint::toPacked(PackedControlPoint & p)
{
  p . uuid = uuid ;
  p . Type = Type ;
  p . DOF  = DOF  ;
  p . Unit = Unit ;
  p . Flag = Flag ;
  p . x    = x    ;
  p . y    = y    ;
  p . z    = z    ;
  p . t    = t    ;
  p . r    = r    ;
  p . f    = f    ;
  return true     ;
}

void N::ControlPoint::Light(GLenum light,GLenum pname)
{
  GLfloat f [ 4 ] = { x , y , z , t } ;
  QtGL::Lightfv ( light , pname , f ) ;
}

void N::ControlPoint::Material(GLenum face,GLenum pname)
{
  GLfloat f [ 4 ] = { x , y , z , t }       ;
  QtGL::Materialfv ( face , pname , 4 , f ) ;
}

void N::ControlPoint::Vertex3f(void)
{
  #if defined(Q_OS_ANDROID)
  GLfloat F[3] = { x , y , z } ;
  QtGL::VertexPointer(3,GL_FLOAT,0,F);
  #elif defined(Q_OS_IOS)
  GLfloat F[3] = { x , y , z } ;
  QtGL::VertexPointer(3,GL_FLOAT,0,F);
  #else
  QtGL::Vertex3f ( x , y , z ) ;
  #endif
}

void N::ControlPoint::Vertex3d(void)
{
  #if defined(Q_OS_ANDROID)
  GLdouble F[3] = { x , y , z } ;
  QtGL::VertexPointer(3,GL_DOUBLE,0,F);
  #elif defined(Q_OS_IOS)
  GLfloat F[3] = { x , y , z } ;
  QtGL::VertexPointer(3,GL_FLOAT,0,F);
  #else
  QtGL::Vertex3dv ( &x ) ;
  #endif
}

void N::ControlPoint::Normal3f(void)
{
  QtGL::Normal3f ( x , y , z ) ;
}

void N::ControlPoint::Normal3d(void)
{
  QtGL::Normal3dv ( &x ) ;
}

void N::ControlPoint::Translatef(void)
{
  QtGL::Translatef ( x , y , z ) ;
}

void N::ControlPoint::Translate(void)
{
  QtGL::Translatedv ( &x ) ;
}

void N::ControlPoint::Rotatef(void)
{
  QtGL::Rotatef ( r , x , y , z ) ;
}

void N::ControlPoint::Rotate(void)
{
  #if defined(Q_OS_ANDROID)
  QtGL::Rotatef ( r , x , y , z ) ;
  #elif defined(Q_OS_IOS)
  QtGL::Rotatef ( r , x , y , z ) ;
  #else
  QtGL::Rotated ( r , x , y , z ) ;
  #endif
}

void N::ControlPoint::Scalef(void)
{
  QtGL::Scalef ( x , y , z ) ;
}

void N::ControlPoint::Scale(void)
{
  #if defined(Q_OS_ANDROID)
  QtGL::Scalef ( x , y , z ) ;
  #elif defined(Q_OS_IOS)
  QtGL::Scalef ( x , y , z ) ;
  #else
  QtGL::Scaled ( x , y , z ) ;
  #endif
}

void N::ControlPoint::Color3f(void)
{
  #if defined(Q_OS_ANDROID)
  QtGL::Color4f ( x , y , z , 1 ) ;
  #elif defined(Q_OS_IOS)
  QtGL::Color4f ( x , y , z , 1 ) ;
  #else
  QtGL::Color3f ( x , y , z ) ;
  #endif
}

void N::ControlPoint::Color4f(void)
{
  QtGL::Color4f  (  x , y , z , t ) ;
}

void N::ControlPoint::Color3d(void)
{
  QtGL::Color3dv ( &x ) ;
}

void N::ControlPoint::Color4d(void)
{
  QtGL::Color4dv ( &x ) ;
}

N::ControlPoint Normal (N::ControlPoint & v1,N::ControlPoint & v2)
{
  N::ControlPoint cp            ;
  QVector3D       vp            ;
  QVector3D       p1            ;
  QVector3D       p2            ;
  p1 = v1.Vertex()              ;
  p2 = v2.Vertex()              ;
  vp = QVector3D::normal(p1,p2) ;
  cp = vp                       ;
  return cp                     ;
}

N::ControlPoint Normal (N::ControlPoint & v1,N::ControlPoint & v2,N::ControlPoint & v3)
{
  N::ControlPoint cp               ;
  QVector3D       vp               ;
  QVector3D       p1               ;
  QVector3D       p2               ;
  QVector3D       p3               ;
  p1 = v1.Vertex()                 ;
  p2 = v2.Vertex()                 ;
  p3 = v3.Vertex()                 ;
  vp = QVector3D::normal(p1,p2,p3) ;
  cp = vp                          ;
  return cp                        ;
}

bool FuzzyCompare(N::ControlPoint & v1,N::ControlPoint & v2)
{
  QVector3D p1                ;
  QVector3D p2                ;
  p1 = v1.Vertex()            ;
  p2 = v2.Vertex()            ;
  return qFuzzyCompare(p1,p2) ;
}

bool operator != (N::ControlPoint & v1,N::ControlPoint & v2)
{
  QVector3D p1     ;
  QVector3D p2     ;
  p1 = v1.Vertex() ;
  p2 = v2.Vertex() ;
  return p1 != p2  ;
}

const N::ControlPoint operator * (double factor,N::ControlPoint & vector)
{
  N::ControlPoint cp ;
  cp  = vector       ;
  cp *= factor       ;
  cp  . uuid = 0     ;
  return cp          ;
}

const N::ControlPoint operator * (N::ControlPoint & vector,double factor)
{
  N::ControlPoint cp ;
  cp  = vector       ;
  cp *= factor       ;
  cp  . uuid = 0     ;
  return cp          ;
}

const N::ControlPoint operator * (N::ControlPoint & v1,N::ControlPoint & v2)
{
  N::ControlPoint cp ;
  cp  = v1           ;
  cp *= v2           ;
  cp  . uuid = 0     ;
  return cp          ;
}

const N::ControlPoint operator + (N::ControlPoint & v1,N::ControlPoint & v2)
{
  N::ControlPoint cp ;
  cp         = v1    ;
  cp        += v2    ;
  cp  . uuid = 0     ;
  return cp          ;
}

const N::ControlPoint operator - (N::ControlPoint & v1,N::ControlPoint & v2)
{
  N::ControlPoint cp ;
  cp         = v1    ;
  cp        -= v2    ;
  cp  . uuid = 0     ;
  return cp          ;
}

const N::ControlPoint operator - (N::ControlPoint & vector)
{
  N::ControlPoint cp  ;
  cp        = vector  ;
  cp . x    = -cp . x ;
  cp . y    = -cp . y ;
  cp . z    = -cp . z ;
  cp . uuid = 0       ;
  return cp           ;
}

const N::ControlPoint operator / (N::ControlPoint & vector,double divisor)
{
  N::ControlPoint cp ;
  cp  = vector       ;
  cp /= divisor      ;
  cp  . uuid = 0     ;
  return cp          ;
}

bool operator == (N::ControlPoint & v1,N::ControlPoint & v2)
{
  QVector3D p1     ;
  QVector3D p2     ;
  p1 = v1.Vertex() ;
  p2 = v2.Vertex() ;
  return p1 == p2  ;
}

const N::ControlPoint operator * (N::Matrix & m,N::ControlPoint & v)
{
  N::ControlPoint p                                            ;
  p = v                                                        ;
  if (m.Rows   ()!=4) return  p                                ;
  if (m.Columns()!=4) return  p                                ;
  double * d = (double *) m . array ( )                             ;
  #define EX(it,id) ( v . it * d [ id ] )
  p . x  = EX ( x , 0 ) + (v.y*d[ 4]) + (v.z*d[ 8]) + (v.t*d[12]) ;
  p . y  = ( v.x*d[ 1]) + (v.y*d[ 5]) + (v.z*d[ 9]) + (v.t*d[13]) ;
  p . z  = ( v.x*d[ 2]) + (v.y*d[ 6]) + (v.z*d[10]) + (v.t*d[14]) ;
  p . t  = ( v.x*d[ 3]) + (v.y*d[ 7]) + (v.z*d[11]) + (v.t*d[15]) ;
  #undef  EX
  return p                                                     ;
}

void N::OpenGL::Vertices(CUIDs Index,N::ControlPoints Points)
{
  if (Index .count()<=0) return ;
  if (Points.count()<=0) return ;
  CUID id                       ;
  foreach (id,Index)            {
    Points[id] . Vertex3f ( )   ;
  }                             ;
}

bool Between(N::ControlPoint & p,N::ControlPoint & pmin,N::ControlPoint & pmax)
{
  if ( p . x < pmin . x ) return false ;
  if ( p . y < pmin . y ) return false ;
  if ( p . z < pmin . z ) return false ;
  if ( p . x > pmax . x ) return false ;
  if ( p . y > pmax . y ) return false ;
  if ( p . z > pmax . z ) return false ;
  return true                          ;
}

bool IntersectRectangle     (
       N::ControlPoint & P  ,
       N::ControlPoint & Z0 ,
       N::ControlPoint & Z1 ,
       N::ControlPoint & Z3 ,
       N::ControlPoint & P1 ,
       N::ControlPoint & P2 )
{
  N::ControlPoint Vx                                                         ;
  N::ControlPoint Vy                                                         ;
  N::ControlPoint Np                                                         ;
  N::ControlPoint Vp                                                         ;
  N::ControlPoint Wp                                                         ;
  N::ControlPoint Sp                                                         ;
  double          t                                                          ;
  double          v                                                          ;
  double          pv                                                         ;
  double          dx                                                         ;
  double          dy                                                         ;
  double          fx                                                         ;
  double          fy                                                         ;
  ////////////////////////////////////////////////////////////////////////////
  // Vx = Z1 - Z0
  Vx . x = Z1 . x - Z0 . x                                                   ;
  Vx . y = Z1 . y - Z0 . y                                                   ;
  Vx . z = Z1 . z - Z0 . z                                                   ;
  ////////////////////////////////////////////////////////////////////////////
  // Vy = Z3 - Z0
  Vy . x = Z3 . x - Z0 . x                                                   ;
  Vy . y = Z3 . y - Z0 . y                                                   ;
  Vy . z = Z3 . z - Z0 . z                                                   ;
  ////////////////////////////////////////////////////////////////////////////
  // Vp = P2  - P1
  Vp . x = P2 . x - P1 . x                                                   ;
  Vp . y = P2 . y - P1 . y                                                   ;
  Vp . z = P2 . z - P1 . z                                                   ;
  ////////////////////////////////////////////////////////////////////////////
  // Wp = Z0 - P1
  Wp . x = Z0 . x - P1 . x                                                   ;
  Wp . y = Z0 . y - P1 . y                                                   ;
  Wp . z = Z0 . z - P1 . z                                                   ;
  ////////////////////////////////////////////////////////////////////////////
  // Np = Vx x Vy
  Np . x = ( Vx . y * Vy . z ) - ( Vx . z * Vy . y )                         ;
  Np . y = ( Vx . z * Vy . x ) - ( Vx . x * Vy . z )                         ;
  Np . z = ( Vx . x * Vy . y ) - ( Vx . y * Vy . x )                         ;
  ////////////////////////////////////////////////////////////////////////////
  // v = Np * Vp
  v      = ( Np . x * Vp . x ) + ( Np . y * Vp . y ) + ( Np . z * Vp . z )   ;
  pv     = v                                                                 ;
  if ( pv < 0         ) pv = -pv                                             ;
  if ( pv < VerySmall ) return false                                         ;
  ////////////////////////////////////////////////////////////////////////////
  // t = Np * Wp / Np * Vp
  t      = ( Np . x * Wp . x ) + ( Np . y * Wp . y ) + ( Np . z * Wp . z )   ;
  t     /= v                                                                 ;
  if ( t < 0          ) return false                                         ;
  ////////////////////////////////////////////////////////////////////////////
  // P =P1 + tVp
  P . x  = P1 . x + ( t * Vp . x )                                           ;
  P . y  = P1 . y + ( t * Vp . y )                                           ;
  P . z  = P1 . z + ( t * Vp . z )                                           ;
  P . t  = 1                                                                 ;
  ////////////////////////////////////////////////////////////////////////////
  // Sp = P - Z0
  Sp . x = P . x - Z0 . x                                                    ;
  Sp . y = P . y - Z0 . y                                                    ;
  Sp . z = P . z - Z0 . z                                                    ;
  ////////////////////////////////////////////////////////////////////////////
  dx     = ( Vx . x * Vx . x ) + ( Vx . y * Vx . y ) + ( Vx . z * Vx . z )   ;
  pv     = dx                                                                ;
  if ( pv < 0         ) pv = -pv                                             ;
  if ( pv < VerySmall ) return false                                         ;
  ////////////////////////////////////////////////////////////////////////////
  dy     = ( Vy . x * Vy . x ) + ( Vy . y * Vy . y ) + ( Vy . z * Vy . z )   ;
  pv     = dy                                                                ;
  if ( pv < 0         ) pv = -pv                                             ;
  if ( pv < VerySmall ) return false                                         ;
  ////////////////////////////////////////////////////////////////////////////
  fx     = ( Sp . x * Vx . x ) + ( Sp . y * Vx . y ) + ( Sp . z * Vx . z )   ;
  fy     = ( Sp . x * Vy . x ) + ( Sp . y * Vy . y ) + ( Sp . z * Vy . z )   ;
  fx    /= dx                                                                ;
  fy    /= dy                                                                ;
  ////////////////////////////////////////////////////////////////////////////
  if ( fx < 0.0 ) return false                                               ;
  if ( fy < 0.0 ) return false                                               ;
  if ( fx > 1.0 ) return false                                               ;
  if ( fy > 1.0 ) return false                                               ;
  ////////////////////////////////////////////////////////////////////////////
  return true                                                                ;
}
"""
