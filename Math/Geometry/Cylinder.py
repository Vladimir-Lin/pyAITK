# -*- coding: utf-8 -*-
##############################################################################
## Cylinder
##############################################################################
## from . Nexus import Nexus as Nexus
##############################################################################
class Cylinder              (                                                ) :
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
class Q_GEOMETRY_EXPORT Cylinder
{
  public:

    IMAPs         sectors ;
    ControlPoints pathes  ;
    Circles       circles ;

    explicit Cylinder     (void) ;
             Cylinder     (const Cylinder & cylinder) ;
    virtual ~Cylinder     (void) ;

    Cylinder & operator = (const Cylinder & cylinder) ;

    void Cone             (ControlPoint & P1   ,
                           ControlPoint & P2   ,
                           ControlPoint & X1   ,
                           ControlPoint & Y1   ,
                           ControlPoint & X2   ,
                           ControlPoint & Y2 ) ;

  protected:

  private:

};

N::Cylinder:: Cylinder(void)
{
}

N::Cylinder:: Cylinder(const Cylinder & cylinder)
{
  ME = cylinder ;
}

N::Cylinder::~Cylinder(void)
{
}

N::Cylinder & N::Cylinder::operator = (const Cylinder & cylinder)
{
  nMemberCopy ( cylinder , sectors ) ;
  nMemberCopy ( cylinder , pathes  ) ;
  nMemberCopy ( cylinder , circles ) ;
  return ME                          ;
}

void N::Cylinder::Cone   (
       ControlPoint & P1 ,
       ControlPoint & P2 ,
       ControlPoint & X1 ,
       ControlPoint & Y1 ,
       ControlPoint & X2 ,
       ControlPoint & Y2 )
{
  Circle C1           ;
  Circle C2           ;
  /////////////////////
  C1 . O = P1         ;
  C1 . X = X1         ;
  C1 . Y = Y1         ;
  C1 . N = 72         ;
  C2 . O = P2         ;
  C2 . X = X2         ;
  C2 . Y = Y2         ;
  C2 . N = 72         ;
  /////////////////////
  sectors . clear ( ) ;
  pathes  . clear ( ) ;
  circles . clear ( ) ;
  /////////////////////
  sectors [ 0 ] = 0   ;
  sectors [ 1 ] = 1   ;
  pathes  [ 0 ] = P1  ;
  pathes  [ 1 ] = P2  ;
  circles [ 0 ] = C1  ;
  circles [ 1 ] = C2  ;
}
"""
