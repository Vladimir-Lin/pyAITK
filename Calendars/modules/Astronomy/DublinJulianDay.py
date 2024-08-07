# -*- coding: utf-8 -*-
##############################################################################
## 都柏林儒略日數
##############################################################################
import  json
##############################################################################
from . JulianDay import JulianDay as JulianDay
##############################################################################
class DublinJulianDay    ( JulianDay                                       ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__      ( self                                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def typeStrings ( self                                                   ) :
    return        [ "DublinJulianDay" , "Dublin Julian Day" , "DJD"          ]
  ############################################################################
  def XJDsToStarDate ( self , XJDV                                         ) :
    ##########################################################################
    try                                                                      :
      ########################################################################
      XJDs = int     (        XJDV                                           )
      ########################################################################
    except                                                                   :
      return 0
    ##########################################################################
    return int       ( XJDs + 1420092375495048000                            )
  ############################################################################
  def StarDateToXJDs ( self                                                ) :
    return int       ( self . Stardate - 1420092375495048000                 )
  ############################################################################
  def toJson ( self                                                        ) :
    return   { "Type"      : self . typeStrings ( )                        , \
               "Signature" : self . Signature                              , \
               "StarDate"  : self . Stardate                               , \
               "TimeZone"  : self . TimeZone                               , \
               "TzOffset"  : self . TzShift                                , \
               "Format"    : self . Format                                 , \
               "DJD"       : self . Value                                  , \
               "Remain"    : self . Remain                                 , \
               "Norm"      : self . Norm                                     }
##############################################################################
