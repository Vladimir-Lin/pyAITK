# -*- coding: utf-8 -*-
##############################################################################
## Ownership
##############################################################################
import os
import sys
import getopt
import time
import datetime
import requests
import threading
##############################################################################
class Ownership          (                                                 ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
##############################################################################
"""
class Q_ESSENTIALS_EXPORT Ownership : public Object
{
  public:

    int relation ;

    explicit Ownership (SUID uuid                               ,
                        int  type     = Types::None             ,
                        int  relation = Groups::Subordination ) ;
    explicit Ownership (void) ;
             Ownership (const Object & object) ;
             Ownership (      Object & object) ;
    virtual ~Ownership (void) ;

    int Connexion      (void) ;
    int setConnexion   (int relation) ;

  protected:

  private:

} ;

N::Ownership:: Ownership ( SUID uuid , int type , int R )
             : Object    (      uuid ,     type         )
             , relation  (                            R )
{
}

N::Ownership:: Ownership ( void                  )
             : Object    ( 0 , Types::None       )
             , relation  ( Groups::Subordination )
{
}

N::Ownership:: Ownership ( const Object & object )
             : Object    (                object )
             , relation  ( Groups::Subordination )
{
}

N::Ownership:: Ownership ( Object & object       )
             : Object    (          object       )
             , relation  ( Groups::Subordination )
{
}

N::Ownership::~Ownership (void)
{
}

int N::Ownership::Connexion(void)
{
  return relation ;
}

int N::Ownership::setConnexion(int R)
{
  relation = R    ;
  return relation ;
}
"""
