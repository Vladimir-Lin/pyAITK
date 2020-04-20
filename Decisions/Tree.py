# -*- coding: utf-8 -*-
#
# 決策樹
#

import os
import sys
import time
import datetime
from   threading import Thread
from   threading import Lock
from   .         import Condition
from   .         import Action
from   .         import Table
from   .         import Tables

class Tree ( Tables ) :

  def __init__ ( self ) :
    self . clear ( )
    pass

  def __del__ ( self ) :
    pass

  def clear ( self ) :
    self . Root       = [ ]
    self . Current    = [ ]
    self . Connectors = { }
    return

  ############################################################################
  def join ( self , tree )                                                   :
    ##########################################################################
    Ds = self . keys ( )
    Ts = tree . keys ( )
    Xs = list ( set ( Ts ) - set ( Ds ) )
    ##########################################################################
    if ( len ( Xs ) > 0 )                                                    :
      for u in Xs                                                            :
        self . Tables [ u ] = tree [ u ]
    ##########################################################################
    Ds = tree . Connectors . keys ( )
    Ts = self . Connectors . keys ( )
    ##########################################################################
    for u in Ds                                                              :
      if ( u in Ts )                                                         :
        Xs = tree . Connectors [ u ]
        Zs = self . Connectors [ u ]
        self . Connectors [ u ] = list ( set ( Zs ) + set ( Xs ) )
      else                                                                   :
        self . Connectors [ u ] = tree . Connectors [ u ]
    ##########################################################################
    self . roots ( )
    ##########################################################################
    return

  ############################################################################
  def roots ( self )                                                         :
    ##########################################################################
    R           =                          [ ]
    Ds          = self              . keys ( )
    Ks          = self . Connectors . keys ( )
    ##########################################################################
    for u in Ks                                                              :
      T = self . Connectors [ u ]
      R = list ( set ( R ) + set ( T ) )
    ##########################################################################
    self . Root = list ( set ( Ds ) - set ( R ) )
    ##########################################################################
    return

  ############################################################################
  def reactions ( self )                                                     :
    ##########################################################################
    R  = [ ]
    for u in self . Current                                                  :
      T = self . Tables [ u ] . actionKeys ( )
      R = list ( set ( R ) + set ( T ) )
    ##########################################################################
    return list ( set ( R ) )

  ############################################################################
  def next ( self , reacts )                                                 :
    ##########################################################################
    D = [ ]
    for u in reacts                                                          :
      if ( u in self . Connectors )                                          :
        T = self . Connectors [ u ]
        D = list ( set ( D ) + set ( T ) )
    ##########################################################################
    if ( len ( D ) > 0 )                                                     :
      self . Current = list ( set ( D ) )
    else                                                                     :
      self . Current = [ ]
      return False
    ##########################################################################
    return True
