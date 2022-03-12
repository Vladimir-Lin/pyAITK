# -*- coding: utf-8 -*-
##############################################################################
## Polyhedron
##############################################################################
## from . Nexus import Nexus as Nexus
##############################################################################
class Polyhedron          (                                                ) :
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
class Q_GEOMETRY_EXPORT Polyhedron
{
  public:

    enum                  {
      Tetrahedron  =  1   ,
      Hexahedron   =  2   ,
      Octahedron   =  3   ,
      Dodecahedron =  4   ,
      Icosahedron  =  5   ,
      Zonohedron   =  6 } ;

    int           type      ;
    ControlPoints points    ;
    VarArgs       arguments ;

    explicit Polyhedron     (void) ;
             Polyhedron     (const Polyhedron & polyhedron) ;
    virtual ~Polyhedron     (void) ;

    Polyhedron & operator = (const Polyhedron & polyhedron) ;

  protected:

  private:

};



N::Polyhedron:: Polyhedron(void)
{
}

N::Polyhedron:: Polyhedron(const Polyhedron & polyhedron)
{
  ME = polyhedron ;
}

N::Polyhedron::~Polyhedron(void)
{
}

N::Polyhedron & N::Polyhedron::operator = (const Polyhedron & polyhedron)
{
  nMemberCopy ( polyhedron , type      ) ;
  nMemberCopy ( polyhedron , points    ) ;
  nMemberCopy ( polyhedron , arguments ) ;
  return ME                              ;
}
"""
