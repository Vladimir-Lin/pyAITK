# -*- coding: utf-8 -*-
##############################################################################
## 主體曆
##############################################################################
import   json
##############################################################################
from ... Base            import Base              as Base
from ... Formatter       import Formatter         as Formatter
from ... Parser          import Parser            as Parser
##############################################################################
from ... Eras . Holocene import HoloceneFormatter as HoloceneFormatter
from ... Eras . Holocene import HoloceneParser    as HoloceneParser
from ... Eras . Holocene import Holocene          as Holocene
##############################################################################
class JucheFormatter     ( HoloceneFormatter                               ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    ##########################################################################
    return
  ############################################################################
  def Keywords ( self                                                      ) :
    return     [ "%(JC)"                                                   , \
                 "%(R)"                                                    , \
                 "%(Y)"                                                    , \
                 "%(YT)"                                                   , \
                 "%(yyyy)"                                                 , \
                 "%(MM)"                                                   , \
                 "%(MT)"                                                   , \
                 "%(M)"                                                    , \
                 "%(DD)"                                                   , \
                 "%(DT)"                                                   , \
                 "%(D)"                                                    , \
                 "%(W)"                                                    , \
                 "%(WL)"                                                   , \
                 "%(WS)"                                                   , \
                 "%(AP)"                                                   , \
                 "%(hh)"                                                   , \
                 "%(ht)"                                                   , \
                 "%(hm)"                                                   , \
                 "%(hz)"                                                   , \
                 "%(h)"                                                    , \
                 "%(mm)"                                                   , \
                 "%(mt)"                                                   , \
                 "%(m)"                                                    , \
                 "%(ss)"                                                   , \
                 "%(st)"                                                   , \
                 "%(s)"                                                    , \
                 "%(SD)"                                                   , \
                 "%(TZ)"                                                     ]
  ############################################################################
  def jcToEra            ( self , Calendar , Format                        ) :
    ##########################################################################
    V      = Format
    ##########################################################################
    if                   ( "%(JC)" in V                                    ) :
      ########################################################################
      Y    = Calendar . YEAR
      JC   = Calendar . JC
      ########################################################################
      if                 ( Y < 0                                           ) :
        JC = Calendar . BJ
      ########################################################################
      V    = V . replace ( "%(JC)" , f"{JC}"                                 )
    ##########################################################################
    return V
  ############################################################################
  def jcToYears                ( self , Calendar , Format                  ) :
    ##########################################################################
    Y   = Calendar . YEAR
    P   = Y
    ##########################################################################
    if                         ( P < 0                                     ) :
      ########################################################################
      P = -P
    ##########################################################################
    KV  =                      { "%(Y)"    : f"{P}"                        , \
                                 "%(YT)"   : self . numberToText ( P )     , \
                                 "%(yyyy)" : f"{P:04}"                     , \
                                 "%(R)"    : f"{Y}"                          }
    ##########################################################################
    return self . ReplacePairs ( KV  , Format                                )
  ############################################################################
  def toString                ( self , Calendar , Format                   ) :
    ##########################################################################
    S   = Format
    ##########################################################################
    S   = self . jcToYears    ( Calendar , S                                 )
    S   = self . heToMonths   ( Calendar , S                                 )
    S   = self . heToDays     ( Calendar , S                                 )
    S   = self . heToHours    ( Calendar , S                                 )
    S   = self . heToMinutes  ( Calendar , S                                 )
    S   = self . heToSeconds  ( Calendar , S                                 )
    S   = self . heToStardate ( Calendar , S                                 )
    S   = self . heToTimeZone ( Calendar , S                                 )
    S   = self . heToWeekdays ( Calendar , S                                 )
    S   = self . heToAMPM     ( Calendar , S                                 )
    S   = self . jcToEra      ( Calendar , S                                 )
    ##########################################################################
    return S
##############################################################################
class JucheParser        ( HoloceneParser                                  ) :
  ############################################################################
  def           __init__ ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    ##########################################################################
    return
##############################################################################
class Juche                        ( Holocene                                ) :
  ############################################################################
  def __init__                   ( self                                    ) :
    ##########################################################################
    super ( ) . __init__         (                                           )
    ##########################################################################
    self      . JC = "JC"
    self      . BJ = "BJ"
    ##########################################################################
    FMT       = "%(yyyy)/%(MM)/%(DD) %(W) %(AP) %(hh):%(mm):%(ss) %(TZ) %(JC) %(SD)"
    ##########################################################################
    self      . setFormat        ( FMT                                       )
    self      . InstallFormatter ( JucheFormatter ( )                        )
    self      . InstallParser    ( JucheParser    ( )                        )
    ##########################################################################
    return
  ############################################################################
  def __del__      ( self                                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def Configure ( self , JSOX                                              ) :
    ##########################################################################
    if          ( "MG"            in JSOX                                  ) :
      self . MG            = JSOX [ "MG"                                     ]
    ##########################################################################
    if          ( "BM"            in JSOX                                  ) :
      self . BM            = JSOX [ "BM"                                     ]
    ##########################################################################
    if          ( "Morning"       in JSOX                                  ) :
      self . Morning       = JSOX [ "Morning"                                ]
    ##########################################################################
    if          ( "Afternoon"     in JSOX                                  ) :
      self . Afternoon     = JSOX [ "Afternoon"                              ]
    ##########################################################################
    if          ( "WeekDays"      in JSOX                                  ) :
      self . WeekDays      = JSOX [ "WeekDays"                               ]
    ##########################################################################
    if          ( "ShortWeekDays" in JSOX                                  ) :
      self . ShortWeekDays = JSOX [ "ShortWeekDays"                          ]
    ##########################################################################
    if          ( "TimeZone"      in JSOX                                  ) :
      ########################################################################
      TZ                   = JSOX [ "TimeZone"                               ]
      self . setTimeZone          ( f"{TZ}"                                  )
    ##########################################################################
    return
  ############################################################################
  def __str__              ( self                                          ) :
    return self . toString (                                                 )
  ############################################################################
  def __repr__          ( self                                             ) :
    return json . dumps ( self . toJson ( )                                  )
  ############################################################################
  def typeStrings ( self                                                   ) :
    return        [ "Juche" , "JC"                                           ]
  ############################################################################
  def heToJucheYear ( self , YEARS                                         ) :
    ##########################################################################
    if              ( YEARS >= 11912                                       ) :
      return int    ( YEARS -  11911                                         )
    ##########################################################################
    return   int    ( YEARS -  11912                                         )
  ############################################################################
  def JucheToHeYear ( self , YEARS                                         ) :
    ##########################################################################
    if              ( YEARS == 0                                           ) :
      return int    ( 11912                                                  )
    ##########################################################################
    if              ( YEARS < 0                                            ) :
      return int    ( 11912 + YEARS                                          )
    ##########################################################################
    return   int    ( 11911 + YEARS                                          )
  ############################################################################
  def toHeYear                  ( self                                     ) :
    return self . JucheToHeYear ( self . YEAR                                )
  ############################################################################
  def isLeapYear               ( self                                      ) :
    return self . heIsLeapYear ( self . toHeYear ( )                         )
  ############################################################################
  def JucheToStardate           ( self                                     , \
                                  YEAR                                     , \
                                  MONTH                                    , \
                                  DAY                                      , \
                                  HOURS                                    , \
                                  MINUTES                                  , \
                                  SECONDS                                  ) :
    ##########################################################################
    SOD = self . toSecondsOfDay ( HOURS , MINUTES , SECONDS                  )
    HSD = self . heToStardate   ( self . JucheToHeYear ( YEAR )              ,
                                  MONTH                                      ,
                                  DAY                                        )
    ##########################################################################
    return int                  ( HSD + SOD - self . TzShift                 )
  ############################################################################
  def localToStardate                        ( self                        ) :
    ##########################################################################
    self . Stardate = self . JucheToStardate ( self . YEAR                   ,
                                               self . MONTH                  ,
                                               self . DAY                    ,
                                               self . HOUR                   ,
                                               self . MINUTE                 ,
                                               self . SECOND                 )
    ##########################################################################
    return self . Stardate
  ############################################################################
  def valueChanged       ( self                                            ) :
    ##########################################################################
    CDT            = int ( self . Stardate + self . TzShift                  )
    ##########################################################################
    Y , MT , D , H , M , S = self . toHoloceneYNDHMS ( CDT                   )
    WD                     = self . toWeekOfDay      ( CDT                   )
    ##########################################################################
    self . YEAR    = self . heToJucheYear            ( Y                     )
    ##########################################################################
    self . MONTH   = MT
    self . DAY     = D
    self . HOUR    = H
    self . MINUTE  = M
    self . SECOND  = S
    self . WEEKDAY = WD
    ##########################################################################
    return
  ############################################################################
  def toJson ( self                                                        ) :
    return   { "Type"      : self . typeStrings ( )                        , \
               "Signature" : self . Signature                              , \
               "StarDate"  : self . Stardate                               , \
               "TimeZone"  : self . TimeZone                               , \
               "TzOffset"  : self . TzShift                                , \
               "Format"    : self . Format                                 , \
               "Year"      : self . YEAR                                   , \
               "Month"     : self . MONTH                                  , \
               "Day"       : self . DAY                                    , \
               "Hour"      : self . HOUR                                   , \
               "Minute"    : self . MINUTE                                 , \
               "Second"    : self . SECOND                                 , \
               "WeekDay"   : self . WEEKDAY                                , \
               "HE"        : self . HES                                    , \
               "BHE"       : self . BHE                                      }
  ############################################################################
  def toString                  ( self , format = ""                       ) :
    ##########################################################################
    MOD   = self . defaultFormatter
    ##########################################################################
    if                          ( MOD in [ False , None ]                  ) :
      raise ModuleNotFoundError (                                            )
    ##########################################################################
    FMT   = format
    if                          ( len ( FMT ) <= 0                         ) :
      FMT = self . Format
    ##########################################################################
    return MOD . toString       ( self , FMT                                 )
  ############################################################################
  def fromString                ( self , inputString , format = ""         ) :
    ##########################################################################
    MOD   = self . defaultParser
    ##########################################################################
    if                          ( MOD in [ False , None ]                  ) :
      raise ModuleNotFoundError (                                            )
    ##########################################################################
    FMT   = format
    if                          ( len ( FMT ) <= 0                         ) :
      FMT = self . Format
    ##########################################################################
    return MOD . Decoder        ( self , inputString , FMT                   )
  ############################################################################
  def setValue             ( self , key , value                            ) :
    ##########################################################################
    K        = key
    K        = K . lower   (                                                 )
    ##########################################################################
    if                     ( key in [ "sd" , "stardate" ]                  ) :
      ########################################################################
      try                                                                    :
        ######################################################################
        self . Stardate = int ( value                                        )
        self . valueChanged   (                                              )
        ######################################################################
      except                                                                 :
        pass
      ########################################################################
      return self . Stardate
    ##########################################################################
    if              ( key in [ "year"                                    ] ) :
      ########################################################################
      try                                                                    :
        self . YEAR = int ( value                                            )
      except                                                                 :
        pass
      ########################################################################
      return int    ( self . YEAR                                            )
    ##########################################################################
    if              ( key in [ "month"                                   ] ) :
      ########################################################################
      try                                                                    :
        self . MONTH = int ( value                                           )
      except                                                                 :
        pass
      ########################################################################
      return int    ( self . MONTH                                           )
    ##########################################################################
    if              ( key in [ "day"                                     ] ) :
      ########################################################################
      try                                                                    :
        self . DAY = int ( value                                             )
      except                                                                 :
        pass
      ########################################################################
      return int    ( self . DAY                                             )
    ##########################################################################
    if              ( key in [ "hour"                                    ] ) :
      ########################################################################
      try                                                                    :
        self . HOUR = int ( value                                            )
      except                                                                 :
        pass
      ########################################################################
      return int    ( self . HOUR                                            )
    ##########################################################################
    if              ( key in [ "minute"                                  ] ) :
      ########################################################################
      try                                                                    :
        self . MINUTE = int ( value                                          )
      except                                                                 :
        pass
      ########################################################################
      return int    ( self . MINUTE                                          )
    ##########################################################################
    if              ( key in [ "second"                                  ] ) :
      ########################################################################
      try                                                                    :
        self . SECOND = int ( value                                          )
      except                                                                 :
        pass
      ########################################################################
      return int    ( self . SECOND                                          )
    ##########################################################################
    if              ( key in [ "weekday"                                 ] ) :
      ########################################################################
      try                                                                    :
        self . WEEKDAY = int ( value                                         )
      except                                                                 :
        pass
      ########################################################################
      return int    ( self . WEEKDAY                                         )
    ##########################################################################
    if              ( key in [ "weekdays"                                ] ) :
      ########################################################################
      self . WeekDays = value
      ########################################################################
      return self . WeekDays
    ##########################################################################
    if              ( key in [ "shortweekdays"                           ] ) :
      ########################################################################
      self . ShortWeekDays = value
      ########################################################################
      return self . ShortWeekDays
    ##########################################################################
    if              ( key in [ "tzdiff" , "tzshift"                      ] ) :
      ########################################################################
      try                                                                    :
        self . TzShift = int ( value                                         )
      except                                                                 :
        pass
      ########################################################################
      return int    ( self . TzShift                                         )
    ##########################################################################
    if              ( key in [ "timezone" , "tz"                         ] ) :
      ########################################################################
      try                                                                    :
        self . TimeZone = str ( value                                        )
      except                                                                 :
        pass
      ########################################################################
      return str    ( self . TimeZone                                        )
    ##########################################################################
    if              ( key in [ "format"                                  ] ) :
      ########################################################################
      try                                                                    :
        self . Format = str ( value                                          )
      except                                                                 :
        pass
      ########################################################################
      return str    ( self . Format                                          )
    ##########################################################################
    if              ( key in [ "he"                                      ] ) :
      ########################################################################
      try                                                                    :
        self . HES = str ( value                                             )
      except                                                                 :
        pass
      ########################################################################
      return str    ( self . HES                                             )
    ##########################################################################
    if              ( key in [ "bhe"                                     ] ) :
      ########################################################################
      try                                                                    :
        self . BHE = str ( value                                             )
      except                                                                 :
        pass
      ########################################################################
      return str    ( self . BHE                                             )
    ##########################################################################
    if              ( key in [ "morning"                                 ] ) :
      ########################################################################
      try                                                                    :
        self . Morning = str ( value                                         )
      except                                                                 :
        pass
      ########################################################################
      return str    ( self . Morning                                         )
    ##########################################################################
    if              ( key in [ "afternoon"                               ] ) :
      ########################################################################
      try                                                                    :
        self . Afternoon = str ( value                                       )
      except                                                                 :
        pass
      ########################################################################
      return str    ( self . Afternoon                                       )
    ##########################################################################
    return self . Stardate
  ############################################################################
  def getValue      ( self , key                                           ) :
    ##########################################################################
    K = key
    K = K . lower   (                                                        )
    ##########################################################################
    if              ( key in [ "sd" , "stardate"                         ] ) :
      return int    ( self . Stardate                                        )
    ##########################################################################
    if              ( key in [ "year"                                    ] ) :
      return int    ( self . YEAR                                            )
    ##########################################################################
    if              ( key in [ "month"                                   ] ) :
      return int    ( self . MONTH                                           )
    ##########################################################################
    if              ( key in [ "day"                                     ] ) :
      return int    ( self . DAY                                             )
    ##########################################################################
    if              ( key in [ "hour"                                    ] ) :
      return int    ( self . HOUR                                            )
    ##########################################################################
    if              ( key in [ "minute"                                  ] ) :
      return int    ( self . MINUTE                                          )
    ##########################################################################
    if              ( key in [ "second"                                  ] ) :
      return int    ( self . SECOND                                          )
    ##########################################################################
    if              ( key in [ "weekday"                                 ] ) :
      return int    ( self . WEEKDAY                                         )
    ##########################################################################
    if              ( key in [ "weekdays"                                ] ) :
      return self . WeekDays
    ##########################################################################
    if              ( key in [ "shortweekdays"                           ] ) :
      return self . ShortWeekDays
    ##########################################################################
    if              ( key in [ "tzdiff" , "tzshift"                      ] ) :
      return int    ( self . TzShift                                         )
    ##########################################################################
    if              ( key in [ "timezone" , "tz"                         ] ) :
      return str    ( self . TimeZone                                        )
    ##########################################################################
    if              ( key in [ "format"                                  ] ) :
      return str    ( self . Format                                          )
    ##########################################################################
    if              ( key in [ "he"                                      ] ) :
      return str    ( self . HES                                             )
    ##########################################################################
    if              ( key in [ "bhe"                                     ] ) :
      return str    ( self . BHE                                             )
    ##########################################################################
    if              ( key in [ "morning"                                 ] ) :
      return str    ( self . Morning                                         )
    ##########################################################################
    if              ( key in [ "afternoon"                               ] ) :
      return str    ( self . Afternoon                                       )
    ##########################################################################
    raise NameError (                                                        )
##############################################################################