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

"""

class Q_ESSENTIALS_EXPORT VirtualProgress
{
  public:

    explicit     VirtualProgress (void) ;
    virtual     ~VirtualProgress (void) ;

    virtual int  Progress        (QString name,QString format) = 0 ;
    virtual void ProgressName    (int Id,QString name) = 0 ;
    virtual void ProgressText    (int Id,QString message) = 0 ;
    virtual void setProgress     (int Id,QString format) = 0 ;
    virtual void setRange        (int Id,qint64 Min,qint64 Max) = 0 ;
    virtual void setFrequency    (int Id,QString cFmt,QString rFmt) = 0 ;
    virtual void Start           (int Id,qint64 * Value,bool * Running) = 0 ;
    virtual void Finish          (int Id) = 0 ;
    virtual bool ProgressReady   (int Id,int msecs = 1000) = 0 ;

  protected:

  private:

} ;

#include <essentials.h>

N::VirtualProgress:: VirtualProgress(void)
{
}

N::VirtualProgress::~VirtualProgress(void)
{
}

"""
