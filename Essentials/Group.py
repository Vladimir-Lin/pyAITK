# -*- coding: utf-8 -*-
##############################################################################
## Group
##############################################################################
import os
import sys
import getopt
import time
import datetime
import requests
import threading
##############################################################################
class Group              (                                                 ) :
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
class Q_ESSENTIALS_EXPORT Group
{
  public:

    SUID   first      ;
    SUID   second     ;
    int    t1         ;
    int    t2         ;
    int    relation   ;
    int    position   ;
    int    reversal   ;
    double membership ;
    BMAPs  activated  ;

    explicit     Group         (void) ;
    explicit     Group         (VarArgs     & arguments) ;
    explicit     Group         (SUID First               ,
                                int  T1                  ,
                                int  T2                ) ;
    explicit     Group         (SUID First               ,
                                SUID Second              ,
                                int  T1                  ,
                                int  T2                  ,
                                int  Relation          ) ;
                 Group         (const Group & group    ) ;
    virtual     ~Group         (void) ;

    virtual int  packsize      (void) ;

    QByteArray   toByteArray   (void) ;

    Group &      operator =    (const Group & group) ;
    Group &      operator =    (const QByteArray & data) ;
    Object       First         (void) ;
    Object       Second        (void) ;
    void         First         (Object  & object      ) ;
    void         Second        (Object  & object      ) ;
    int          addParaments  (VarArgs & arguments   ) ;

    bool         setActivate   (int index,bool enable ) ;
    bool         activate      (int index) ;
    bool         isFirst       (void) ;
    bool         isSecond      (void) ;
    bool         hasRelation   (void) ;
    bool         hasPosition   (void) ;
    bool         hasMembership (void) ;

    virtual void setEmpty      (void) ;
    virtual void setFirst      (SUID first ,int t1,int relation = Groups::Subordination) ;
    virtual void setSecond     (SUID second,int t2,int relation = Groups::Subordination) ;

  protected:

  private:

} ;


typedef struct      {
  SUID   first      ;
  SUID   second     ;
  int    t1         ;
  int    t2         ;
  int    relation   ;
  int    position   ;
  int    reversal   ;
  double membership ;
} nGroupData        ;

N::Group:: Group(void)
{
  first      =   0 ;
  second     =   0 ;
  t1         =   0 ;
  t2         =   0 ;
  relation   =   0 ;
  position   =   0 ;
  reversal   =   0 ;
  membership = 1.0 ;
}

N::Group:: Group(VarArgs & arguments)
{
  if (arguments.count()>2) first      = arguments[2].toULongLong() ;
  if (arguments.count()>3) second     = arguments[3].toULongLong() ;
  if (arguments.count()>4) t1         = arguments[4].toInt      () ;
  if (arguments.count()>5) t2         = arguments[5].toInt      () ;
  if (arguments.count()>6) relation   = arguments[6].toInt      () ;
  if (arguments.count()>7) position   = arguments[7].toInt      () ;
  if (arguments.count()>8) membership = arguments[8].toDouble   () ;
}

N::Group:: Group(const Group & group)
{
  nMemberCopy ( group , first      ) ;
  nMemberCopy ( group , second     ) ;
  nMemberCopy ( group , t1         ) ;
  nMemberCopy ( group , t2         ) ;
  nMemberCopy ( group , relation   ) ;
  nMemberCopy ( group , position   ) ;
  nMemberCopy ( group , reversal   ) ;
  nMemberCopy ( group , membership ) ;
}

N::Group:: Group(SUID F,int T1,int T2)
{
  first      = F                       ;
  second     = 0                       ;
  t1         = T1                      ;
  t2         = T2                      ;
  relation   = Groups :: Subordination ;
  position   = 0                       ;
  reversal   = 0                       ;
  membership = 1.0                     ;
  Group :: activated [ 0 ] = true      ;
  Group :: activated [ 1 ] = false     ;
  Group :: activated [ 2 ] = true      ;
  Group :: activated [ 3 ] = true      ;
  Group :: activated [ 4 ] = true      ;
  Group :: activated [ 5 ] = true      ;
  Group :: activated [ 6 ] = false     ;
  Group :: activated [ 7 ] = false     ;
}

N::Group:: Group(SUID F,SUID S,int T1,int T2,int R)
{
  first      = F   ;
  second     = S   ;
  t1         = T1  ;
  t2         = T2  ;
  relation   = R   ;
  position   = 0   ;
  reversal   = 0   ;
  membership = 1.0 ;
}

N::Group::~Group(void)
{
}

int N::Group::packsize(void)
{
  return sizeof(nGroupData) ;
}

QByteArray N::Group::toByteArray(void)
{
  QByteArray Body                             ;
  Body.resize(sizeof(nGroupData))             ;
  nGroupData * gd = (nGroupData *)Body.data() ;
  gd->first       = first                     ;
  gd->second      = second                    ;
  gd->t1          = t1                        ;
  gd->t2          = t2                        ;
  gd->relation    = relation                  ;
  gd->position    = position                  ;
  gd->reversal    = reversal                  ;
  gd->membership  = membership                ;
  return Body                                 ;
}

N::Group & N::Group::operator = (const Group & group)
{
  nMemberCopy ( group , first      ) ;
  nMemberCopy ( group , second     ) ;
  nMemberCopy ( group , t1         ) ;
  nMemberCopy ( group , t2         ) ;
  nMemberCopy ( group , relation   ) ;
  nMemberCopy ( group , position   ) ;
  nMemberCopy ( group , reversal   ) ;
  nMemberCopy ( group , membership ) ;
  return ME                          ;
}

N::Group & N::Group::operator = (const QByteArray & data)
{
  if ( NotEqual( data . size ( ) , sizeof(nGroupData) ) ) return ME ;
  nGroupData * gd = (nGroupData *)data.data()                       ;
  first           = gd->first                                       ;
  second          = gd->second                                      ;
  t1              = gd->t1                                          ;
  t2              = gd->t2                                          ;
  relation        = gd->relation                                    ;
  position        = gd->position                                    ;
  reversal        = gd->reversal                                    ;
  membership      = gd->membership                                  ;
  return ME                                                         ;
}

N::Object N::Group::First(void)
{
  return Object(first,t1) ;
}

N::Object N::Group::Second(void)
{
  return Object(second,t2) ;
}

void N::Group::First(Object & object)
{
  object . setOwner ( first  , t1 ) ;
}

void N::Group::Second(Object & object)
{
  object . setOwner ( second , t2 ) ;
}

int N::Group::addParaments(VarArgs & arguments)
{
  arguments << QVariant(first     ) ;
  arguments << QVariant(second    ) ;
  arguments << QVariant(t1        ) ;
  arguments << QVariant(t2        ) ;
  arguments << QVariant(relation  ) ;
  arguments << QVariant(position  ) ;
  arguments << QVariant(membership) ;
  return arguments.count()          ;
}

bool N::Group::setActivate(int index,bool enable)
{
  activated[index] = enable ;
  return enable             ;
}

bool N::Group::activate(int index)
{
  nKickOut ( !activated.contains(index) , false ) ;
  return activated[index]                         ;
}

bool N::Group::isFirst(void)
{
  nKickOut ( !activate( 0 ) , false ) ;
  nKickOut ( !activate( 2 ) , false ) ;
  nKickOut ( ( first <=0  ) , false ) ;
  return true                         ;
}

bool N::Group::isSecond(void)
{
  nKickOut ( !activate( 1 ) , false ) ;
  nKickOut ( !activate( 3 ) , false ) ;
  nKickOut ( ( second <=0 ) , false ) ;
  return true                         ;
}

bool N::Group::hasRelation(void)
{
  return activate ( 4 ) ;
}

bool N::Group::hasPosition(void)
{
  return activate ( 5 ) ;
}

bool N::Group::hasMembership(void)
{
  return activate ( 6 ) ;
}

void N::Group::setEmpty(void)
{
  first                    = 0     ;
  second                   = 0     ;
  t1                       = 0     ;
  t2                       = 0     ;
  relation                 = 0     ;
  position                 = 0     ;
  reversal                 = 0     ;
  membership               = 0     ;
  Group :: activated [ 0 ] = false ;
  Group :: activated [ 1 ] = false ;
  Group :: activated [ 2 ] = false ;
  Group :: activated [ 3 ] = false ;
  Group :: activated [ 4 ] = false ;
  Group :: activated [ 5 ] = false ;
  Group :: activated [ 6 ] = false ;
  Group :: activated [ 7 ] = false ;
}

void N::Group::setFirst(SUID f,int t,int r)
{
  first                    = f    ;
  t1                       = t    ;
  relation                 = r    ;
  Group :: activated [ 0 ] = true ;
  Group :: activated [ 2 ] = true ;
  Group :: activated [ 4 ] = true ;
}

void N::Group::setSecond(SUID s,int t,int r)
{
  second                   = s    ;
  t2                       = t    ;
  relation                 = r    ;
  Group :: activated [ 1 ] = true ;
  Group :: activated [ 3 ] = true ;
  Group :: activated [ 4 ] = true ;
}
"""
