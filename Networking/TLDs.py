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

  def __init__ ( self ) :
    self . Clear ( )
    return

  def __del__ ( self ) :
    pass

  def Clear ( self ) :
    pass

  def assign ( self , item ) :
    pass


