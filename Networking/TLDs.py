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
    self . Names           = [ ]
    self . Reverses        = [ ]
    ##########################################################################
    self . NamesToIds      = { }
    self . NamesToUuids    = { }
    self . IdsToNames      = { }
    self . UuidsToNames    = { }
    ##########################################################################
    self . ReversesToIds   = { }
    self . ReversesToUuids = { }
    self . IdsToReverses   = { }
    self . UuidsToReverses = { }
    ##########################################################################
    return

  ############################################################################
  def assign ( self , item )                                                 :
    ##########################################################################
    self . Names           = item . Names
    self . Reverses        = item . Reverses
    ##########################################################################
    self . NamesToIds      = item . NamesToIds
    self . NamesToUuids    = item . NamesToUuids
    self . IdsToNames      = item . IdsToNames
    self . UuidsToNames    = item . UuidsToNames
    ##########################################################################
    self . ReversesToIds   = item . ReversesToIds
    self . ReversesToUuids = item . ReversesToUuids
    self . IdsToReverses   = item . IdsToReverses
    self . UuidsToReverses = item . UuidsToReverses
    ##########################################################################
    return

  ############################################################################
  def ToUuid ( self , id ) :
    return id + 8300000000001000000

  ############################################################################
  def FromUuid ( self , uuid ) :
    return uuid - 8300000000001000000

  ############################################################################
  def obtains ( self , DB , Table )                                          :
    ##########################################################################
    self . Clear ( )
    ##########################################################################
    QQ    = f"select `id`,`uuid`,`name`,`reverse` from {Table} where ( `used` > 0 ) order by `id` asc ;"
    DB    . Query         ( QQ )
    RR    = DB . FetchAll (    )
    if ( not ( ( RR == None ) or ( len ( RR ) <= 0 ) ) )                     :
      for R in RR                                                            :
        ######################################################################
        ID      = R [ 0 ]
        UUID    = R [ 1 ]
        N       = R [ 2 ]
        X       = R [ 3 ]
        NAME    = N . lower ( )
        REVERSE = X . lower ( )
        ######################################################################
        self . Names    . append ( NAME    )
        self . Reverses . append ( REVERSE )
        ////////////////////////////////////////////////////////////////////////
        self . NamesToIds      [ NAME    ] = ID
        self . NamesToUuids    [ NAME    ] = UUID
        self . IdsToNames      [ ID      ] = NAME
        self . UuidsToNames    [ UUID    ] = NAME
        ////////////////////////////////////////////////////////////////////////
        self . ReversesToIds   [ REVERSE ] = ID
        self . ReversesToUuids [ REVERSE ] = UUID
        self . IdsToReverses   [ ID      ] = REVERSE
        self . UuidsToReverses [ UUID    ] = REVERSE
    ##########################################################################
    return True

  ############################################################################
  def IdByName ( self , name                                               ) :
    n = name . lower ( )
    if         ( n not in self . Names                                     ) :
      return 0
    return self . NamesToIds [ n ]

  ############################################################################
  def UuidByName ( self , name                                             ) :
    n = name . lower ( )
    if         ( n not in self . Names                                     ) :
      return 0
    return self . NamesToUuids [ n ]

  ############################################################################
  def IdByReverse ( self , name                                            ) :
    n = name . lower ( )
    if         ( n not in self . Reverses                                  ) :
      return 0
    return self . ReversesToIds [ n ]

  ############################################################################
  def IdByReverse ( self , name                                            ) :
    n = name . lower ( )
    if         ( n not in self . Reverses                                  ) :
      return 0
    return self . ReversesToUuids [ n ]
