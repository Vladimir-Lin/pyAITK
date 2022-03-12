# -*- coding: utf-8 -*-
##############################################################################
## Plane
##############################################################################
## from . Nexus import Nexus as Nexus
##############################################################################
class Plane               (                                                ) :
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
##############################################################################
"""
class Q_GEOMETRY_EXPORT Plane
{
  public:

    ControlPoint O ; // Base point
    ControlPoint X ; // X Axis
    ControlPoint Y ; // Y Axis
    ControlPoint T ; // Thickness
    ControlPoint N ; // Normal
    int          W ; // Width segments
    int          H ; // Height segments
    bool         A ; // Activation

    explicit Plane     (void) ;
             Plane     (const Plane & plane) ;
    virtual ~Plane     (void) ;

    Plane & operator = (const Plane & plane) ;

    bool    Upon       (ControlPoint & At                 ,
                        ControlPoint & Base               ,
                        ControlPoint & Vector             ,
                        double         detail = 0.000001) ;
    QPointF Axis       (ControlPoint & At) ;
    // For acceleration, this function will not divided X.length and Y.length

  protected:

  private:

};

N::Plane:: Plane (void )
         : A     (false)
{
}

N::Plane:: Plane (const Plane & plane)
{
  ME = plane ;
}

N::Plane::~Plane(void)
{
}

N::Plane & N::Plane::operator = (const Plane & plane)
{
  nMemberCopy ( plane , O ) ;
  nMemberCopy ( plane , X ) ;
  nMemberCopy ( plane , Y ) ;
  nMemberCopy ( plane , T ) ;
  nMemberCopy ( plane , N ) ;
  nMemberCopy ( plane , W ) ;
  nMemberCopy ( plane , H ) ;
  nMemberCopy ( plane , A ) ;
  return ME                 ;
}

bool N::Plane      :: Upon   (
       ControlPoint & At     ,
       ControlPoint & Base   ,
       ControlPoint & Vector ,
       double         detail )
{
  double d   = dotProduct(N,Vector) ;
  double vn  = d                    ;
  if (d<0) d = -d                   ;
  nKickOut ( d < detail , false )   ;
  double s   = 0                    ;
  double obn = 0                    ;
  ControlPoint OB                   ;
  OB  = O                           ;
  OB -= Base                        ;
  obn = dotProduct(OB,N)            ;
  s   = obn / vn                    ;
  OB  = Vector                      ;
  OB *= s                           ;
  At  = Base                        ;
  At += OB                          ;
  return true                       ;
}

QPointF N::Plane::Axis(ControlPoint & At)
{
  ControlPoint D             ;
  QPointF      P             ;
  D  = At                    ;
  D -= O                     ;
  P  . setX(dotProduct(D,X)) ;
  P  . setY(dotProduct(D,Y)) ;
  return P                   ;
}
"""
