# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import datetime
import requests
import threading

import mysql . connector
from   mysql . connector import Error

class SqlColumns ( ) :

  def __init__ ( self ) :
    self . Columns = [ ]

  def __del__ ( self ) :
    self . Columns = [ ]

  def clear ( self ) :
    self . Columns = [ ]
    return self . Columns

  def append ( self , column ) :
    self . Columns . append ( column )
    return self . Columns

  def extend ( self , columns ) :
    self . Columns . extend ( columns )

  def assign ( self , item ) :
    raise NotImplementedError ( )

  def set ( self , item , value ) :
    raise NotImplementedError ( )

  def tableItems ( self ) :
    raise NotImplementedError ( )

  def pair ( self , item ) :
    raise NotImplementedError ( )

  def join ( self , Lists , Splitter = "," ) :
    U = [ ]
    for x in Lists :
      v = f'`{x}`'
      U . append ( v )
    L = Splitter . join ( U )
    return L

  def items ( self , Splitter = "," ) :
    List = self . tableItems ( )
    return self . join ( List , Splitter )

  def tail ( self , Options , Limits ) :
    Q = ""
    if ( len ( Options ) > 0 ) :
      Q += " "
      Q += Options
    if ( len ( Limits ) > 0 ) :
      Q += " "
      Q += Limits
    return Q

  def pairs ( self , items ) :
    I = [ ]
    for x in items :
      I . append ( self . pair ( x ) )
    L = " and " . join ( I )
    return L

  def QueryItems ( self , items , Options = "" , Limits = "" ) :
    IS    = self . pairs ( items )
    TAILs = self . tail ( Options , Limits )
    QQ    = f" where {IS} {TAILs}"
    return QQ

  def SelectItems ( self , Table , items , Options , Limits ) :
    IS    = self . items ( " , " )
    QUERY = self . QueryItems ( items , Options , Limits )
    QQ    = f"select {IS} from {Table} {QUERY} ;"
    return QQ

  def SelectColumns ( self , Table , Options = "order by `priority` asc" , Limits = "" ) :
    return self . SelectItems ( Table , self . Columns , Options , Limits )
