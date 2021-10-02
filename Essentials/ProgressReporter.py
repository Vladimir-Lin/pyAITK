# -*- coding: utf-8 -*-
##############################################################################
##
##############################################################################
import os
import sys
import getopt
import time
import datetime
import requests
import threading
##############################################################################
import mysql . connector
from   mysql . connector              import Error
##############################################################################
import AITK
from   AITK . Database  . Query       import Query
from   AITK . Database  . Connection  import Connection
from   AITK . Database  . Columns     import Columns
##############################################################################

##############################################################################


##############################################################################

"""

class Q_ESSENTIALS_EXPORT ProgressReporter
{
  public:

    QString   name    ;
    QString   format  ;
    QDateTime start   ;
    qint64    total   ;
    qint64    value   ;
    int       users   ;
    int       state   ; // 0 - stop , 1 - running , 2 - pause , 3 - resume , 4 - stopping
    int       id      ;
    bool      running ;
    Mutexz    mutex   ;

    explicit         ProgressReporter (void) ;
    virtual         ~ProgressReporter (void) ;

    virtual void     setRunning       (bool enable) ;
    virtual void     Using            (void) ;
    virtual void     Leaving          (void) ;

    static  void     setVirtual       (VirtualProgress * vp) ;

    virtual int      Progress         (QString name,QString format) ;
    virtual void     ProgressName     (QString name) ;
    virtual void     ProgressText     (QString message) ;
    virtual void     setProgress      (QString format) ;
    virtual void     setRange         (qint64 Min,qint64 Max) ;
    virtual void     setFrequency     (QString cFmt,QString rFmt) ;
    virtual void     Start            (void) ;
    virtual void     Start            (qint64 * value,bool * running) ;
    virtual void     Finish           (void) ;
    virtual bool     ProgressReady    (int msecs = 1000) ;

    virtual qint64 & operator ++      (void) ;

  protected:

    static VirtualProgress * vp ;

  private:

} ;


#include <essentials.h>

N::VirtualProgress * N::ProgressReporter::vp = NULL ;

N::ProgressReporter:: ProgressReporter ( void     )
                    : name             ( ""       )
                    , format           ( ""       )
                    , start            ( nTimeNow )
                    , total            ( 0        )
                    , value            ( 0        )
                    , users            ( 0        )
                    , state            ( 0        )
                    , id               ( -1       )
                    , running          ( false    )
{
}

N::ProgressReporter::~ProgressReporter(void)
{
}

void N::ProgressReporter::setRunning(bool enable)
{
  mutex [ 0 ] . lock   ( ) ;
  running = enable         ;
  state   = enable ? 1 : 4 ;
  mutex [ 0 ] . unlock ( ) ;
}

void N::ProgressReporter::Using(void)
{
  mutex [ 0 ] . lock   ( ) ;
  users ++                 ;
  mutex [ 0 ] . unlock ( ) ;
}

void N::ProgressReporter::Leaving(void)
{
  mutex [ 0 ] . lock   ( ) ;
  users --                 ;
  mutex [ 0 ] . unlock ( ) ;
  if ( users <= 0 )        {
    delete this            ;
  }                        ;
}

void N::ProgressReporter::setVirtual(VirtualProgress * v)
{
  vp = v ;
}

int N::ProgressReporter::Progress(QString name,QString format)
{
  if ( NULL == vp ) return -1           ;
  id = vp -> Progress ( name , format ) ;
  return id                             ;
}

void N::ProgressReporter::ProgressName(QString name)
{
  if ( NULL == vp ) return         ;
  if ( id   <  0  ) return         ;
  vp -> ProgressName ( id , name ) ;
}

void N::ProgressReporter::ProgressText(QString message)
{
  if ( NULL == vp ) return            ;
  if ( id   <  0  ) return            ;
  vp -> ProgressText ( id , message ) ;
}

void N::ProgressReporter::setProgress(QString format)
{
  if ( NULL == vp ) return          ;
  if ( id   <  0  ) return          ;
  vp -> setProgress ( id , format ) ;
}

void N::ProgressReporter::setRange(qint64 Min,qint64 Max)
{
  if ( NULL == vp ) return          ;
  if ( id   <  0  ) return          ;
  vp -> setRange ( id , Min , Max ) ;
}

void N::ProgressReporter::setFrequency(QString cFmt,QString rFmt)
{
  if ( NULL == vp ) return                ;
  if ( id   <  0  ) return                ;
  vp -> setFrequency ( id , cFmt , rFmt ) ;
}

void N::ProgressReporter::Start(void)
{
  if ( NULL == vp ) return                 ;
  if ( id   <  0  ) return                 ;
  running = true                           ;
  vp -> Start ( id , & value , & running ) ;
}

void N::ProgressReporter::Start(qint64 * v,bool * r)
{
  if ( NULL == vp ) return   ;
  if ( id   <  0  ) return   ;
  vp -> Start ( id , v , r ) ;
}

void N::ProgressReporter::Finish(void)
{
  if ( NULL == vp ) return ;
  if ( id   <  0  ) return ;
  vp -> Finish ( id )      ;
  id  = -1                 ;
}

bool N::ProgressReporter::ProgressReady(int msecs)
{
  if ( NULL == vp ) return false            ;
  if ( id   <  0  ) return false            ;
  return vp -> ProgressReady ( id , msecs ) ;
}

qint64 & N::ProgressReporter::operator ++ (void)
{
  value ++     ;
  return value ;
}

"""
