# -*- coding: utf-8 -*-
##############################################################################
## Circle
##############################################################################
## from . Nexus import Nexus as Nexus
##############################################################################
class Circle              (                                                ) :
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
class Q_GEOMETRY_EXPORT Circle
{
  public:

    ControlPoint O ; // Center
    ControlPoint X ; // X Vector
    ControlPoint Y ; // Y Vector
    int          N ; // N sectors

    explicit Circle     (void) ;
             Circle     (const Circle & circle) ;
    virtual ~Circle     (void) ;

    Circle & operator = (const Circle & circle) ;

    bool Angle          (double angle,ControlPoint & P) ;

  protected:

  private:

};

N::Circle:: Circle(void)
{
}

N::Circle:: Circle(const Circle & circle)
{
  ME = circle ;
}

N::Circle::~Circle(void)
{
}

N::Circle & N::Circle::operator = (const Circle & circle)
{
  nMemberCopy ( circle , O ) ;
  nMemberCopy ( circle , X ) ;
  nMemberCopy ( circle , Y ) ;
  nMemberCopy ( circle , N ) ;
  return ME                  ;
}

bool N::Circle::Angle(double angle,ControlPoint & P)
{
  ControlPoint C                       ;
  double sin = Math::fastSine  (angle) ;
  double cos = Math::fastCosine(angle) ;
  P          = O                       ;
  C          = X                       ;
  C         *= cos                     ;
  P         += C                       ;
  C          = Y                       ;
  C         *= sin                     ;
  P         += C                       ;
  return true                          ;
}
"""
