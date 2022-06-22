# -*- coding: utf-8 -*-
##############################################################################
## 物理長度
##############################################################################
from enum import IntEnum
##############################################################################
class Length             ( IntEnum                                         ) :
  ############################################################################
  Pixel        =   0
  Parsec       =   1
  LightYear    =   2
  LightDay     =   3
  LightHour    =   4
  AU           =   5
  LightMinute  =   6
  LightSpeed   =   7
  Yottametre   = 101
  Zettametre   = 102
  Exametre     = 103
  Petametre    = 104
  Terametre    = 105
  Gigametre    = 106
  Megametre    = 107
  Kilometer    = 108
  Hectometre   = 109
  Decametre    = 110
  Meter        = 111
  Decimeter    = 112
  Centimeter   = 113
  Millimeter   = 114
  Micrometre   = 115
  Nanometer    = 116
  Angstrom     = 117
  Picometre    = 118
  Fermi        = 119
  Attometer    = 120
  Zeptometre   = 121
  Yoctometre   = 122
  SuperString  = 123
  Planck       = 124
  MilliPlanck  = 125
  NanoPlanck   = 126
  Preon        = 127
  Mile         = 201
  Furlong      = 202
  Chain        = 203
  Rod          = 204
  Perch        = 205
  Pole         = 206
  Lug          = 207
  Fathom       = 208
  Yard         = 209
  Foot         = 210
  Hand         = 211
  Inch         = 212
  ChineseLi    = 301
  ChineseYin   = 302
  ChineseZhang = 303
  ChineseBu    = 304
  ChineseChi   = 305
  ChineseCun   = 306
  ChineseFen   = 307
  TangBigFoot  = 308
  KoreanChi    = 401
  YojanaMin    = 501
  Yojana       = 502
  YojanaMax    = 503
  Nautical     = 601
  Rig          = 602
  Pica         = 701
  Point        = 702
  Verst        = 801
  ############################################################################
  ############################################################################
##############################################################################
"""
typedef enum       {
  Pixel       =   0, /* Not actual unit, used on computer rendition */
  /* Astronomy System */
  Parsec      =   1, /* 206265AU
                        30,856,804,798,079,115 Meters
                        about 3.261567 ly
                      */
  LightYear   =   2, /* 9,460,730,472,580,800 Meters */
  LightDay    =   3, /* 25,902,068,371,200 Meters */
  LightHour   =   4, /* 1,079,252,848,800 Meters */
  AU          =   5, /* 149,597,870,691 Meters */
  LightMinute =   6, /* 17,987,547,480 Meters */
  LightSpeed  =   7, /* 299,792,458 Meters */
  /* SI System */
  Yottametre  = 101, /* 10 ^  24 Meters */
  Zettametre  = 102, /* 10 ^  21 Meters */
  Exametre    = 103, /* 10 ^  18 Meters */
  Petametre   = 104, /* 10 ^  15 Meters */
  Terametre   = 105, /* 10 ^  12 Meters */
  Gigametre   = 106, /* 10 ^   9 Meters */
  Megametre   = 107, /* 10 ^   6 Meters */
  Kilometer   = 108, /* 10 ^   3 Meters */
  Hectometre  = 109, /* 10 ^   2 Meters */
  Decametre   = 110, /* 10 ^   1 Meters */
  Meter       = 111, /* Light Speed : 299792458 Meters */
  Decimeter   = 112, /* 10 ^ - 1 Meter */
  Centimeter  = 113, /* 10 ^ - 2 Meter */
  Millimeter  = 114, /* 10 ^ - 3 Meter */
  Micrometre  = 115, /* 10 ^ - 6 Meter */
  Nanometer   = 116, /* 10 ^ - 9 Meter */
  Angstrom    = 117, /* 10 ^ -10 Meter */
  Picometre   = 118, /* 10 ^ -12 Meter */
  Fermi       = 119, /* 10 ^ -15 Meter */
  Attometer   = 120, /* 10 ^ -18 Meter */
  Zeptometre  = 121, /* 10 ^ -21 Meter */
  Yoctometre  = 122, /* 10 ^ -24 Meter */
  SuperString = 123, /* 10 ^ -33 Meter */
  Planck      = 124, /* 10 ^ -36 Meter */
  MilliPlanck = 125, /* 10 ^ -39 Meter */
  NanoPlanck  = 126, /* 10 ^ -45 Meter */
  Preon       = 127, /* 10 ^ -80 Meter */
  /* Imperial Units */
  Mile        = 201, /* 1609.344 Meters */
  Furlong     = 202, /* 220 Yards */
  Chain       = 203, /* 22 Yards */
  Rod         = 204, /* 5.5 Yards , 5.0292 Meters */
  Perch       = 205, /* 5.5 Yards , same name */
  Pole        = 206, /* 5.5 Yards , same name */
  Lug         = 207, /* 5.5 Yards , same name */
  Fathom      = 208, /* 2 Yards , 182.88 Centimeters */
  Yard        = 209, /* 91.44 Centimeters */
  Foot        = 210, /* 30.48 Centimeters */
  Hand        = 211, /* 10.16 Centimeters */
  Inch        = 212, /* 2.54 Centimeters */
  /* Chinese Modern Unit */
  ChineseLi   = 301, /* 500 Meters */
  ChineseYin  = 302, /* 15 Yin = 1 Li */
  ChineseZhang= 303, /* 150 Zhang = 1 Li */
  ChineseBu   = 304, /* 5 Chi */
  ChineseChi  = 305, /* 1500 Chi = 1 Li */
  ChineseCun  = 306, /* 0.1 Chi */
  ChineseFen  = 307, /* 0.01 Chi */
  TangBigFoot = 308, /* 29.6 Centimeters */
  /* Korea , Japan */
  KoreanChi   = 401, /* 35.6 Centimeters */
  /* India Unit */
  YojanaMin   = 501, /* 13 Kilometers */
  Yojana      = 502, /* Yojana average */
  YojanaMax   = 503, /* 16 Kilometers */
  /* Nautical mile */
  Nautical    = 601, /* 1852 Meters */
  Rig         = 602, /* 5556 Meters */
  /* Printing */
  Pica        = 701, /* 12 points */
  Point       = 702, /* 1 point = 127/360 mm about 352.7 um */
  /* Russian  */
  Verst       = 801  /* 1.0668 Kilometer */
} Unit             ;
"""
##############################################################################
class LengthConverter (                                                    ) :
  ############################################################################
  def __init__        ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__         ( self                                               ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################
