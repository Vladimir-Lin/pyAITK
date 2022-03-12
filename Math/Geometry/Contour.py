# -*- coding: utf-8 -*-
##############################################################################
## Contour
##############################################################################
## from . Nexus import Nexus as Nexus
##############################################################################
class Contour             (                                                ) :
  ############################################################################
  def __init__            ( self                                           ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__     ( self                                                   ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
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


N::Contour:: Contour   ( void             )
           : uuid      ( 0                )
           , type      ( Graphics::Linear )
           , closed    ( false            )
           , substract ( false            )
{
  thickness.x = 0.05 ;
  thickness.y = 0.05 ;
  thickness.z = 0.05 ;
}

N::Contour:: Contour(const Contour & contour)
{
  ME = contour ;
}

N::Contour::~Contour(void)
{
}

int N::Contour::count(void)
{
  return index . count ( ) ;
}

void N::Contour::begin(void)
{
  index  . clear ( ) ;
  points . clear ( ) ;
}

int N::Contour::add(int Id,ControlPoint & point)
{
  index << Id           ;
  points [ Id ] = point ;
  return count ( )      ;
}

int N::Contour::remove(int Id)
{
  if (index  . contains(Id)) index  . takeAt ( index.indexOf(Id) ) ;
  if (points . contains(Id)) points . remove ( Id                ) ;
  return count ( )                                                 ;
}

void N::Contour::end(void)
{
  closed = false                               ;
  if (count()<1) return                        ;
  int a = index [ 0 ]                          ;
  points [ a ] . Type = type | Graphics::Start ;
  if (count()<2) return                        ;
  int b = index [ count() - 1 ]                ;
  points [ b ] . Type = type | Graphics::End   ;
}

void N::Contour::close(int t)
{
  closed = false                ;
  int Flags = type | t          ;
  int a = index [ 0 ]           ;
  points [ a ] . Type = Flags   ;
  if (count()<2) return         ;
  int b = index [ count() - 1 ] ;
  points [ b ] . Type = Flags   ;
  closed = true                 ;
}

int N::Contour::find(QPointF & point,double R)
{
  double R2 = R * R                          ;
  CUID   i                                   ;
  foreach (i,index)                          {
    if (points[i].Within(point,R2)) return i ;
  }                                          ;
  return -1                                  ;
}

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

QRectF N::Contour::boundingRect(void)
{
  if (points.count()<=0) return QRectF(0,0,0,0) ;
  ///////////////////////////////////////////////
  int    i      = index [0]                     ;
  double left   = points[i].x                   ;
  double right  = points[i].x                   ;
  double top    = points[i].y                   ;
  double bottom = points[i].y                   ;
  ///////////////////////////////////////////////
  if (points.count()>1)                         {
    for (int j=1;j<index.count();j++)           {
      i = index[j]                              ;
      double x = points[i].x                    ;
      double y = points[i].y                    ;
      if ( x < left   ) left   = x              ;
      if ( x > right  ) right  = x              ;
      if ( y < top    ) top    = y              ;
      if ( y > bottom ) bottom = y              ;
    }                                           ;
  }                                             ;
  ///////////////////////////////////////////////
  QRectF R                                      ;
  R . setLeft   ( left   )                      ;
  R . setRight  ( right  )                      ;
  R . setTop    ( top    )                      ;
  R . setBottom ( bottom )                      ;
  return R                                      ;
}

N::Contour & N::Contour::operator = (const Contour & contour)
{
  int i                               ;
  nMemberCopy ( contour , uuid      ) ;
  nMemberCopy ( contour , name      ) ;
  nMemberCopy ( contour , type      ) ;
  nMemberCopy ( contour , closed    ) ;
  nMemberCopy ( contour , substract ) ;
  nMemberCopy ( contour , index     ) ;
  nMemberCopy ( contour , thickness ) ;
  foreach (i,index)                   {
    points[i] = contour.points[i]     ;
  }                                   ;
  return ME                           ;
}

N::Contour & N::Contour::operator += (QPointF center)
{
  int i                 ;
  double x = center.x() ;
  double y = center.y() ;
  foreach (i,index)     {
    points[i].x += x    ;
    points[i].y += y    ;
  }                     ;
  return ME             ;
}

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

N::Contour & N::Contour::operator -= (QPointF center)
{
  int i                 ;
  double x = center.x() ;
  double y = center.y() ;
  foreach (i,index)     {
    points[i].x -= x    ;
    points[i].y -= y    ;
  }                     ;
  return ME             ;
}

N::Contour & N::Contour::operator *= (double factor)
{
  int i                 ;
  foreach (i,index)     {
    points[i] *= factor ;
  }                     ;
  return ME             ;
}

N::Contour & N::Contour::operator *= (QSizeF s)
{
  int i                          ;
  foreach (i,index)              {
    points[i].x *= s . width  () ;
    points[i].y *= s . height () ;
  }                              ;
  return ME                      ;
}

N::Contour & N::Contour::operator /= (double divisor)
{
  int i                  ;
  foreach (i,index)      {
    points[i] /= divisor ;
  }                      ;
  return ME              ;
}
"""
