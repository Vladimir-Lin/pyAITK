# -*- coding: utf-8 -*-
##############################################################################
##
##############################################################################
import os
import sys
##############################################################################
import mysql . connector
from   mysql . connector             import Error
##############################################################################
from   ..      Database . Query      import Query      as Query
from   ..      Database . Connection import Connection as Connection
from   ..      Database . Columns    import Columns    as Columns
##############################################################################
from   .       TLD                   import TLD        as TLD
##############################################################################

class TLDs ( ) :

  ############################################################################
  def __init__ ( self ) :
    self . Clear ( )
    return

  ############################################################################
  def __del__ ( self ) :
    pass

  ############################################################################
  def Clear ( self )                                                         :
    ##########################################################################
    self . Items    = { }
    self . Names    = { }
    self . Reverses = { }
    ##########################################################################
    return

  ############################################################################
  def assign ( self , item )                                                 :
    ##########################################################################
    self . Items    = item . Items
    self . Names    = item . Names
    self . Reverses = item . Reverses
    ##########################################################################
    return

  ############################################################################
  def ToUuid ( self , id ) :
    return id + 8300000000001000000

  ############################################################################
  def FromUuid ( self , uuid ) :
    return uuid - 8300000000001000000

  ############################################################################
  def IDs ( self )                                                           :
    return self . Items . keys ( )

  ############################################################################
  def keys( self )                                                           :
    return self . Names . keys ( )

  ############################################################################
  def __getitem__ ( self , id                                              ) :
    if            ( id not in self . Items                                 ) :
      return False
    return self . Items [ id ]

  ############################################################################
  def ByName ( self , name                                                 ) :
    if       ( name not in self . Names                                    ) :
      return -1
    return self . Names [ name ]

  ############################################################################
  def ByReverse ( self , reverse                                           ) :
    if          ( reverse not in self . Reverses                           ) :
      return -1
    return self . Reverses [ reverse ]

  ############################################################################
  def Fetch ( self , DB , Table )                                            :
    ##########################################################################
    self . Clear ( )
    QQ   = f"select `id` from {Table} order by `id` asc ;"
    IDs  = DB . ObtainUuids ( QQ )
    ##########################################################################
    for id in IDs                                                            :
      tld = TLD ( )
      tld . Id = id
      if ( tld . ObtainsById ( DB , Table ) ) :
        self   . Items    [ tld . Id      ] = tld
        if ( len ( tld . Name ) > 0 ) :
          self . Names    [ tld . Name    ] = tld . Id
          self . Reverses [ tld . Reverse ] = tld . Id
    ##########################################################################
    return True
