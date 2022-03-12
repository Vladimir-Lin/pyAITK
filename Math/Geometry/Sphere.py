# -*- coding: utf-8 -*-
##############################################################################
## Sphere
##############################################################################
## from . Nexus import Nexus as Nexus
##############################################################################
class Sphere              (                                                ) :
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
class Q_GEOMETRY_EXPORT Sphere
{
  public:

    ControlPoint O ; // Center
    ControlPoint X ; // X Vector
    ControlPoint Y ; // Y Vector
    ControlPoint R ; // Radius Vector
    IMAPs        N ; // Sectors

    explicit Sphere     (void) ;
             Sphere     (const Sphere & sphere) ;
    virtual ~Sphere     (void) ;

    Sphere & operator = (const Sphere & sphere) ;

  protected:

  private:

};


N::Sphere:: Sphere(void)
{
}

N::Sphere:: Sphere(const Sphere & sphere)
{
  ME = sphere ;
}

N::Sphere::~Sphere(void)
{
}

N::Sphere & N::Sphere::operator = (const Sphere & sphere)
{
  nMemberCopy ( sphere , O ) ;
  nMemberCopy ( sphere , X ) ;
  nMemberCopy ( sphere , Y ) ;
  nMemberCopy ( sphere , R ) ;
  nMemberCopy ( sphere , N ) ;
  return ME                  ;
}
"""
