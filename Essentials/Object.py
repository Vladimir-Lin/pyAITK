# -*- coding: utf-8 -*-
##############################################################################
## Object
##############################################################################
import os
import sys
import getopt
import time
import datetime
import requests
import threading
##############################################################################
class Object             (                                                 ) :
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
class Q_ESSENTIALS_EXPORT Object
{
  public:

    SUID uuid ;
    int  type ;

    operator SUID          ( ) const ;

    explicit Object        (SUID uuid,int type = Types::None) ;
    explicit Object        (void) ;
             Object        (const Object & object) ;
             Object        (      Object & object) ;
    virtual ~Object        (void) ;

    void     empty         (void) ;
    Object & operator =    (const Object & object) ;
    Object & operator =    (      Object & object) ;
    Object & setOwner      (SUID uuid,int type) ;
    Object & setOwner      (Object & object) ;

    SUID     ObjectUuid    (void) const ;
    SUID     setObjectUuid (SUID uuid) ;
    int      ObjectType    (void) const ;
    int      setObjectType (int type) ;

    bool     is            (N::Types::ObjectTypes type) ;
    bool     isStandby     (void) ;
    bool     operator ==   (const Object & object) ;
    bool     identical     (const Object & object) ;

  protected:

  private:

} ;

N::Object:: Object ( SUID u , int t )
          : uuid   (      u         )
          , type   (              t )
{
}

N::Object:: Object (void)
          : uuid   (0   )
          , type   (0   )
{
}

N::Object:: Object (const Object & object)
{
  nMemberCopy ( object , uuid ) ;
  nMemberCopy ( object , type ) ;
}

N::Object:: Object (Object & object)
{
  nMemberCopy ( object , uuid ) ;
  nMemberCopy ( object , type ) ;
}

N::Object::~Object(void)
{
}

N::Object::operator SUID ( ) const
{
  return uuid ;
}

void N::Object::empty(void)
{
  uuid = 0 ;
  type = 0 ;
}

N::Object & N::Object::operator = (const Object & object)
{
  nMemberCopy ( object , uuid ) ;
  nMemberCopy ( object , type ) ;
  return ME                     ;
}

N::Object & N::Object::operator = (Object & object)
{
  nMemberCopy ( object , uuid ) ;
  nMemberCopy ( object , type ) ;
  return ME                     ;
}

N::Object & N::Object::setOwner(SUID u,int t)
{
  uuid = u  ;
  type = t  ;
  return ME ;
}

N::Object & N::Object::setOwner(Object & object)
{
  nMemberCopy ( object , uuid ) ;
  nMemberCopy ( object , type ) ;
  return ME                     ;
}

SUID N::Object::ObjectUuid(void) const
{
  return uuid ;
}

SUID N::Object::setObjectUuid(SUID u)
{
  uuid = u    ;
  return uuid ;
}

int N::Object::ObjectType(void) const
{
  return type ;
}

int N::Object::setObjectType(int t)
{
  type = t    ;
  return type ;
}

bool N::Object::is(N::Types::ObjectTypes t)
{
  return (nEqual(type,(int)t)) ;
}

bool N::Object::isStandby(void)
{
  nKickOut ( nEqual(uuid,0) , true ) ;
  nKickOut ( nEqual(type,0) , true ) ;
  return false                       ;
}

bool N::Object::operator == (const Object & object)
{
  nKickOut ( NotEqual ( uuid , object . uuid ) , false ) ;
  nKickOut ( NotEqual ( type , object . type ) , false ) ;
  return true                                            ;
}

bool N::Object::identical(const Object & object)
{
  nKickOut ( NotEqual ( uuid , object . uuid ) , false ) ;
  nKickOut ( NotEqual ( type , object . type ) , false ) ;
  return true                                            ;
}
"""
