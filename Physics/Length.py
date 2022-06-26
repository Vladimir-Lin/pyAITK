# -*- coding: utf-8 -*-
##############################################################################
## 物理長度
##############################################################################
from   enum  import IntEnum
##############################################################################
import gmpy2
from   gmpy2 import mpz
from   gmpy2 import mpq
from   gmpy2 import mpfr
##############################################################################
class Length             ( IntEnum                                         ) :
  ############################################################################
  Pixel           =   0
  Parsec          =   1
  LightYear       =   2
  LightDay        =   3
  LightHour       =   4
  AU              =   5
  LightMinute     =   6
  LightSpeed      =   7
  Yottametre      = 101
  Zettametre      = 102
  Exametre        = 103
  Petametre       = 104
  Terametre       = 105
  Gigametre       = 106
  Megametre       = 107
  Kilometer       = 108
  Hectometre      = 109
  Decametre       = 110
  Meter           = 111
  Decimeter       = 112
  Centimeter      = 113
  Millimeter      = 114
  Decimillimetre  = 115
  Centimillimetre = 116
  Micrometre      = 117
  Nanometer       = 118
  Angstrom        = 119
  Picometre       = 120
  Fermi           = 121
  Attometer       = 122
  Zeptometre      = 123
  Yoctometre      = 124
  SuperString     = 125
  Planck          = 126
  MilliPlanck     = 127
  NanoPlanck      = 128
  Preon           = 129
  Mile            = 201
  Furlong         = 202
  Chain           = 203
  Rod             = 204
  Perch           = 205
  Pole            = 206
  Lug             = 207
  Fathom          = 208
  Yard            = 209
  Foot            = 210
  Hand            = 211
  Inch            = 212
  ChineseLi       = 301
  ChineseYin      = 302
  ChineseZhang    = 303
  ChineseBu       = 304
  ChineseChi      = 305
  ChineseCun      = 306
  ChineseFen      = 307
  TangBigFoot     = 308
  KoreanChi       = 401
  YojanaMin       = 501
  Yojana          = 502
  YojanaMax       = 503
  Nautical        = 601
  Rig             = 602
  Pica            = 701
  Point           = 702
  Verst           = 801
##############################################################################
PrivateAllLengths =                                                          [
  { "Id"          : Length . Pixel                                         , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 0                                                      , \
    "Name"        : "Pixel"                                                , \
    "Reference"   : 0                                                      , \
    "Conversion"  : ""                                                     } ,
  { "Id"          : Length . Parsec                                        , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 1                                                      , \
    "Name"        : "Parsec"                                               , \
    "Reference"   : Length . AU                                            , \
    "Conversion"  : "206265"                                               } ,
  { "Id"          : Length . LightYear                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 1                                                      , \
    "Name"        : "Light-Year"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "9460730472580800"                                     } ,
  { "Id"          : Length . LightDay                                      , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 1                                                      , \
    "Name"        : "Light-Day"                                            , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "25902068371200"                                       } ,
  { "Id"          : Length . LightHour                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 1                                                      , \
    "Name"        : "Light-Hour"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1079252848800"                                        } ,
  { "Id"          : Length . AU                                            , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 1                                                      , \
    "Name"        : "AU"                                                   , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "149597870691"                                         } ,
  { "Id"          : Length . LightMinute                                   , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 1                                                      , \
    "Name"        : "Light-Minute"                                         , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "17987547480"                                          } ,
  { "Id"          : Length . LightSpeed                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 1                                                      , \
    "Name"        : "Light-Speed"                                          , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "299792458"                                            } ,
  { "Id"          : Length . Yottametre                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Yotta-Metre"                                          , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1000000000000000000000000"                            } ,
  { "Id"          : Length . Zettametre                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Zetta-Metre"                                          , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1000000000000000000000"                               } ,
  { "Id"          : Length . Exametre                                      , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Exa-Metre"                                            , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1000000000000000000"                                  } ,
  { "Id"          : Length . Petametre                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Peta-Metre"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1000000000000000"                                     } ,
  { "Id"          : Length . Terametre                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Tera-Metre"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1000000000000"                                        } ,
  { "Id"          : Length . Gigametre                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Giga-Metre"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1000000000"                                           } ,
  { "Id"          : Length . Megametre                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Mega-Metre"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1000000"                                              } ,
  { "Id"          : Length . Kilometer                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Kilo-Metre"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1000"                                                 } ,
  { "Id"          : Length . Hectometre                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Hecto-Metre"                                          , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "100"                                                  } ,
  { "Id"          : Length . Decametre                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Deca-Metre"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "10"                                                   } ,
  { "Id"          : Length . Meter                                         , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Meter"                                                , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "1000000000000000"                                     } ,
  { "Id"          : Length . Decimeter                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Deci-Meter"                                           , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "100000000000000"                                      } ,
  { "Id"          : Length . Centimeter                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Centi-Meter"                                          , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "10000000000000"                                       } ,
  { "Id"          : Length . Millimeter                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Milli-Meter"                                          , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "1000000000000"                                        } ,
  { "Id"          : Length . Decimillimetre                                , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Deci-Milli-Meter"                                     , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "100000000000"                                         } ,
  { "Id"          : Length . Centimillimetre                               , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Centi-Milli-Meter"                                    , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "10000000000"                                          } ,
  { "Id"          : Length . Micrometre                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Micro-Metre"                                          , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "1000000000"                                           } ,
  { "Id"          : Length . Nanometer                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Nano-Meter"                                           , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "1000000"                                              } ,
  { "Id"          : Length . Angstrom                                      , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Angstrom"                                             , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "100000"                                               } ,
  { "Id"          : Length . Picometre                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Pico-Metre"                                           , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "1000"                                                 } ,
  { "Id"          : Length . Fermi                                         , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Fermi"                                                , \
    "Reference"   : Length . SuperString                                   , \
    "Conversion"  : "1000000000000000000"                                  } ,
  { "Id"          : Length . Attometer                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Atto-Meter"                                           , \
    "Reference"   : Length . SuperString                                   , \
    "Conversion"  : "1000000000000000"                                     } ,
  { "Id"          : Length . Zeptometre                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Zepto-Metre"                                          , \
    "Reference"   : Length . SuperString                                   , \
    "Conversion"  : "1000000000000"                                        } ,
  { "Id"          : Length . Yoctometre                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Yocto-Metre"                                          , \
    "Reference"   : Length . SuperString                                   , \
    "Conversion"  : "1000000000"                                           } ,
  { "Id"          : Length . SuperString                                   , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Super-String"                                         , \
    "Reference"   : Length . NanoPlanck                                    , \
    "Conversion"  : "1000000000000"                                        } ,
  { "Id"          : Length . Planck                                        , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Planck"                                               , \
    "Reference"   : Length . NanoPlanck                                    , \
    "Conversion"  : "1000000000"                                           } ,
  { "Id"          : Length . MilliPlanck                                   , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Milli-Planck"                                         , \
    "Reference"   : Length . NanoPlanck                                    , \
    "Conversion"  : "1000000"                                              } ,
  { "Id"          : Length . NanoPlanck                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Nano-Planck"                                          , \
    "Reference"   : Length . Preon                                         , \
    "Conversion"  : "100000000000000000000000000000000000"                 } ,
  { "Id"          : Length . Preon                                         , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 2                                                      , \
    "Name"        : "Preon"                                                , \
    "Reference"   : 0                                                      , \
    "Conversion"  : ""                                                     } ,
  { "Id"          : Length . Mile                                          , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Mile"                                                 , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "63360"                                                } ,
  { "Id"          : Length . Furlong                                       , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Furlong"                                              , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "7920"                                                 } ,
  { "Id"          : Length . Chain                                         , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Chain"                                                , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "792"                                                  } ,
  { "Id"          : Length . Rod                                           , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Rod"                                                  , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "198"                                                  } ,
  { "Id"          : Length . Perch                                         , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Perch"                                                , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "198"                                                  } ,
  { "Id"          : Length . Pole                                          , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Pole"                                                 , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "198"                                                  } ,
  { "Id"          : Length . Lug                                           , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Lug"                                                  , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "198"                                                  } ,
  { "Id"          : Length . Fathom                                        , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Fathom"                                               , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "72"                                                   } ,
  { "Id"          : Length . Yard                                          , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Yard"                                                 , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "36"                                                   } ,
  { "Id"          : Length . Foot                                          , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Foot"                                                 , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "12"                                                   } ,
  { "Id"          : Length . Hand                                          , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Foot"                                                 , \
    "Reference"   : Length . Inch                                          , \
    "Conversion"  : "4"                                                    } ,
  { "Id"          : Length . Inch                                          , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 3                                                      , \
    "Name"        : "Inch"                                                 , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "25400000000000"                                       } ,
  { "Id"          : Length . ChineseLi                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 4                                                      , \
    "Name"        : "Chinese-Li"                                           , \
    "Reference"   : Length . ChineseFen                                    , \
    "Conversion"  : "150000"                                               } ,
  { "Id"          : Length . ChineseYin                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 4                                                      , \
    "Name"        : "Chinese-Yin"                                          , \
    "Reference"   : Length . ChineseFen                                    , \
    "Conversion"  : "10000"                                                } ,
  { "Id"          : Length . ChineseZhang                                  , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 4                                                      , \
    "Name"        : "Chinese-Zhang"                                        , \
    "Reference"   : Length . ChineseFen                                    , \
    "Conversion"  : "1000"                                                 } ,
  { "Id"          : Length . ChineseBu                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 4                                                      , \
    "Name"        : "Chinese-Bu"                                           , \
    "Reference"   : Length . ChineseFen                                    , \
    "Conversion"  : "500"                                                  } ,
  { "Id"          : Length . ChineseChi                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 4                                                      , \
    "Name"        : "Chinese-Chi"                                          , \
    "Reference"   : Length . ChineseFen                                    , \
    "Conversion"  : "100"                                                  } ,
  { "Id"          : Length . ChineseCun                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 4                                                      , \
    "Name"        : "Chinese-Cun"                                          , \
    "Reference"   : Length . ChineseFen                                    , \
    "Conversion"  : "10"                                                   } ,
  { "Id"          : Length . ChineseFen                                    , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 4                                                      , \
    "Name"        : "Chinese-Fen"                                          , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "10000000000000/3"                                     } ,
  { "Id"          : Length . TangBigFoot                                   , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 4                                                      , \
    "Name"        : "Tang-Big-Foot"                                        , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "296000000000000"                                      } ,
  { "Id"          : Length . KoreanChi                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 5                                                      , \
    "Name"        : "Korean-Chi"                                           , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "356000000000000"                                      } ,
  { "Id"          : Length . YojanaMin                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 6                                                      , \
    "Name"        : "Yojana-Min"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "13000"                                                } ,
  { "Id"          : Length . Yojana                                        , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 6                                                      , \
    "Name"        : "Yojana"                                               , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "14600"                                                } ,
  { "Id"          : Length . YojanaMax                                     , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 6                                                      , \
    "Name"        : "Yojana-Max"                                           , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "16000"                                                } ,
  { "Id"          : Length . Nautical                                      , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 7                                                      , \
    "Name"        : "Nautical"                                             , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "1852"                                                 } ,
  { "Id"          : Length . Rig                                           , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 7                                                      , \
    "Name"        : "Rig"                                                  , \
    "Reference"   : Length . Meter                                         , \
    "Conversion"  : "5556"                                                 } ,
  { "Id"          : Length . Pica                                          , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 8                                                      , \
    "Name"        : "Pica"                                                 , \
    "Reference"   : Length . Point                                         , \
    "Conversion"  : "12"                                                   } ,
  { "Id"          : Length . Point                                         , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 8                                                      , \
    "Name"        : "Point"                                                , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "12700000000000/36"                                    } ,
  { "Id"          : Length . Verst                                         , \
    "Uuid"        : 0                                                      , \
    "Catalog"     : 9                                                      , \
    "Name"        : "Verst"                                                , \
    "Reference"   : Length . Fermi                                         , \
    "Conversion"  : "1066800000000000000"                                    }
]
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
  Decimillimetre  = 115, /* 10 ^ - 4 Meter */
  Centimillimetre = 116, /* 10 ^ - 5 Meter */
  Micrometre  = 117, /* 10 ^ - 6 Meter */
  Nanometer   = 118, /* 10 ^ - 9 Meter */
  Angstrom    = 119, /* 10 ^ -10 Meter */
  Picometre   = 120, /* 10 ^ -12 Meter */
  Fermi       = 121, /* 10 ^ -15 Meter */
  Attometer   = 122, /* 10 ^ -18 Meter */
  Zeptometre  = 123, /* 10 ^ -21 Meter */
  Yoctometre  = 124, /* 10 ^ -24 Meter */
  SuperString = 125, /* 10 ^ -33 Meter */
  Planck      = 126, /* 10 ^ -36 Meter */
  MilliPlanck = 127, /* 10 ^ -39 Meter */
  NanoPlanck  = 128, /* 10 ^ -45 Meter */
  Preon       = 129, /* Oriphase Ground State , 10 ^ -80 Meter */
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
  Yojana      = 502, /* Yojana average, 14.6 Kilometers */
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
class LengthConverter          (                                           ) :
  ############################################################################
  def __init__                 ( self                                      ) :
    ##########################################################################
    self . InitializeConverter (                                             )
    ##########################################################################
    return
  ############################################################################
  def __del__                  ( self                                      ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def InitializeConverter       ( self                                     ) :
    ##########################################################################
    global PrivateAllLengths
    ##########################################################################
    self . Denominator = ""
    self . Numerator   = ""
    self . FromUnit    = ""
    self . ToUnit      = ""
    self . Base        = 6810000000001000000
    ##########################################################################
    self . Units       =        [                                            ]
    self . Uuids       =        [                                            ]
    self . Names       =        {                                            }
    self . Profiles    =        {                                            }
    self . NameToIds   =        {                                            }
    self . UuidToIds   =        {                                            }
    ##########################################################################
    for L in PrivateAllLengths                                               :
      ########################################################################
      ID               = int    ( L [ "Id"                                 ] )
      UUID             = int    ( self . Base + ID                           )
      CATALOG          = int    ( L [ "Catalog"                            ] )
      NAME             = L      [ "Name"                                     ]
      REFERENCE        = int    ( L [ "Reference"                          ] )
      CONVERSION       = L      [ "Conversion"                               ]
      ########################################################################
      J                =        { "Uuid"       : UUID                      , \
                                  "Catalog"    : CATALOG                   , \
                                  "Name"       : NAME                      , \
                                  "Reference"  : REFERENCE                 , \
                                  "Conversion" : CONVERSION                  }
      ########################################################################
      self . Units     . append ( ID                                         )
      self . Uuids     . append ( UUID                                       )
      self . addName            ( NAME , ID                                  )
      ########################################################################
      self . Names     [ ID   ] = NAME
      self . Profiles  [ ID   ] = J
      self . UuidToIds [ UUID ] = ID
    ##########################################################################
    self   . addName            ( "km"          , Length . Kilometer         )
    self   . addName            ( "m"           , Length . Meter             )
    self   . addName            ( "cm"          , Length . Centimeter        )
    self   . addName            ( "mm"          , Length . Millimeter        )
    self   . addName            ( "nm"          , Length . Nanometer         )
    self   . addName            ( "Å"           , Length . Angstrom          )
    self   . addName            ( "å"           , Length . Angstrom          )
    self   . addName            ( "fm"          , Length . Fermi             )
    self   . addName            ( "Femto-Metre" , Length . Fermi             )
    ##########################################################################
    return
  ############################################################################
  def addName                    ( self , NAME , ID                        ) :
    ##########################################################################
    K    = NAME
    K    = K . lower             (                                           )
    self . NameToIds [ K ] = int ( ID                                        )
    ##########################################################################
    K    = NAME
    K    = K . replace           ( "-" , ""                                  )
    K    = K . lower             (                                           )
    self . NameToIds [ K ] = int ( ID                                        )
    ##########################################################################
    K    = NAME
    K    = K . replace           ( "-" , " "                                 )
    K    = K . lower             (                                           )
    self . NameToIds [ K ] = int ( ID                                        )
    ##########################################################################
    return
  ############################################################################
  def TraceUnit                  ( self , ID                               ) :
    ##########################################################################
    LISTS     =                  [                                           ]
    ##########################################################################
    if                           ( ID not in self . Profiles               ) :
      return LISTS
    ##########################################################################
    RID       = self . Profiles  [ ID ] [ "Reference"                        ]
    ##########################################################################
    LISTS     . append           ( ID                                        )
    if                           ( RID <= 0                                ) :
      return LISTS
    ##########################################################################
    TAILs     = self . TraceUnit ( RID                                       )
    ##########################################################################
    if                           ( len ( TAILs ) > 0                       ) :
      ########################################################################
      for T in TAILs                                                         :
        ######################################################################
        LISTS . append           ( T                                         )
    ##########################################################################
    return LISTS
  ############################################################################
  def LongMultiply      ( self , A , B                                     ) :
    ##########################################################################
    if                  ( len ( A ) <= 0                                   ) :
      return B
    ##########################################################################
    if                  ( len ( B ) <= 0                                   ) :
      return A
    ##########################################################################
    AV = mpz            ( A                                                  )
    BV = mpz            ( B                                                  )
    CV = gmpy2 . mul    ( AV , BV                                            )
    DS = gmpy2 . digits ( CV , 10                                            )
    ##########################################################################
    return DS
  ############################################################################
  def ConvertMPZ           ( self , PLEN , Denominator , Numerator         ) :
    ##########################################################################
    S   = mpz              ( f"{PLEN}"                                       )
    D   = mpz              ( Denominator                                     )
    R   = gmpy2 . mul      ( S , D                                           )
    ##########################################################################
    if                     ( len ( Numerator ) > 0                         ) :
      ########################################################################
      N = mpz              ( Numerator                                       )
      R = gmpy2 . divexact ( R , N                                           )
    ##########################################################################
    return R
  ############################################################################
  def ConvertMPFR     ( self , PLEN , Denominator , Numerator              ) :
    ##########################################################################
    S   = mpfr        ( f"{PLEN}"                                            )
    D   = mpfr        ( Denominator                                          )
    R   = gmpy2 . mul ( S , D                                                )
    ##########################################################################
    if                ( len ( Numerator ) > 0                              ) :
      ########################################################################
      N = mpfr        ( Numerator                                            )
      R = gmpy2 . div ( R , N                                                )
    ##########################################################################
    return R
  ############################################################################
  def GetConverter                  ( self , LISTS , AT                    ) :
    ##########################################################################
    ATV   = int                     ( AT                                     )
    D     = ""
    N     = ""
    ##########################################################################
    for V in LISTS                                                           :
      ########################################################################
      CDS = self . Profiles [ V ]   [ "Conversion"                           ]
      ########################################################################
      if                            ( len ( CDS ) > 0                      ) :
        ######################################################################
        if                          ( "/" in CDS                           ) :
          ####################################################################
          CDK = CDS . split         ( "/"                                    )
          DV  = CDK                 [ 0                                      ]
          NV  = CDK                 [ 1                                      ]
          ####################################################################
          D   = self . LongMultiply ( D , DV                                 )
          N   = self . LongMultiply ( N , NV                                 )
          ####################################################################
        else                                                                 :
          ####################################################################
          D   = self . LongMultiply ( D , CDS                                )
      ########################################################################
      if                            ( ATV == V                             ) :
        return                      ( D  , N ,                               )
    ##########################################################################
    return                          ( "" , "" ,                              )
  ############################################################################
  def MatchAnchor ( self , A , B                                           ) :
    ##########################################################################
    for V in A                                                               :
      ########################################################################
      if          ( V in B                                                 ) :
        return V
    ##########################################################################
    return -1
  ############################################################################
  def GetUnitId             ( self , NAME                                  ) :
    ##########################################################################
    K = NAME
    K = K . lower           (                                                )
    ##########################################################################
    if                      ( K not in self . NameToIds                    ) :
      return -1
    ##########################################################################
    return self . NameToIds [ K                                              ]
  ############################################################################
  def SimplifyGMP             ( self , D , N                               ) :
    ##########################################################################
    if                        ( len ( D ) <= 0                             ) :
      return                  ( D , N ,                                      )
    ##########################################################################
    if                        ( len ( N ) <= 0                             ) :
      return                  ( D  , N  ,                                    )
    ##########################################################################
    DZ     = mpz              ( D                                            )
    NZ     = mpz              ( N                                            )
    RZ     = gmpy2 . f_mod    ( DZ , NZ                                      )
    if                        ( RZ == 0                                    ) :
      ########################################################################
      XZ   = gmpy2 . divexact ( DZ , NZ                                      )
      ########################################################################
      return                  ( gmpy2 . digits ( XZ , 10 ) , ""              )
    ##########################################################################
    LZ     = gmpy2 . gcd      ( DZ , NZ                                      )
    DM     = gmpy2 . divexact ( DZ , LZ                                      )
    NM     = gmpy2 . divexact ( NZ , LZ                                      )
    ##########################################################################
    DV     = gmpy2 . digits   ( DM , 10                                      )
    NV     = gmpy2 . digits   ( NM , 10                                      )
    ##########################################################################
    return                    ( DV , NV ,                                    )
  ############################################################################
  def PrepareUnit               ( self , FROMU , TOU                       ) :
    ##########################################################################
    if                          ( len ( FROMU ) <= 0                       ) :
      return                    ( False , "" , ""                            )
    ##########################################################################
    if                          ( len ( TOU   ) <= 0                       ) :
      return                    ( False , "" , ""                            )
    ##########################################################################
    FID   = self . GetUnitId    ( FROMU                                      )
    ##########################################################################
    if                          ( FID < 0                                  ) :
      return                    ( False , "" , ""                            )
    ##########################################################################
    TID   = self . GetUnitId    ( TOU                                        )
    ##########################################################################
    if                          ( TID < 0                                  ) :
      return                    ( False , "" , ""                            )
    ##########################################################################
    LA    = self . TraceUnit    ( FID                                        )
    ##########################################################################
    if                          ( len ( LA ) <= 0                          ) :
      return                    ( False , "" , ""                            )
    ##########################################################################
    LB    = self . TraceUnit    ( TID                                        )
    ##########################################################################
    if                          ( len ( LB ) <= 0                          ) :
      return                    ( False , "" , ""                            )
    ##########################################################################
    AT    = self . MatchAnchor  ( LA , LB                                    )
    ##########################################################################
    if                          ( AT < 0                                   ) :
      return                    ( False , "" , ""                            )
    ##########################################################################
    RA    = self . GetConverter ( LA , AT                                    )
    RB    = self . GetConverter ( LB , AT                                    )
    ##########################################################################
    D     = self . LongMultiply ( RA [ 0 ] , RB [ 1 ]                        )
    N     = self . LongMultiply ( RB [ 0 ] , RA [ 1 ]                        )
    ##########################################################################
    RR    = self . SimplifyGMP  ( D , N                                      )
    D     = RR                  [ 0                                          ]
    N     = RR                  [ 1                                          ]
    ##########################################################################
    return                      ( True , D , N                               )
  ############################################################################
  def setFromUnit             ( self , NAME                                ) :
    ##########################################################################
    self . FromUnit = NAME
    RR   = self . PrepareUnit ( self . FromUnit , self . ToUnit              )
    ##########################################################################
    self . Denominator = RR   [ 1                                            ]
    self . Numerator   = RR   [ 2                                            ]
    ##########################################################################
    return RR                 [ 0                                            ]
  ############################################################################
  def setToUnit               ( self , NAME                                ) :
    ##########################################################################
    self . ToUnit = NAME
    RR   = self . PrepareUnit ( self . FromUnit , self . ToUnit              )
    ##########################################################################
    self . Denominator = RR   [ 1                                            ]
    self . Numerator   = RR   [ 2                                            ]
    ##########################################################################
    return RR                 [ 0                                            ]
  ############################################################################
  def setConverter            ( self , FROMU , TOU                         ) :
    ##########################################################################
    self . FromUnit = FROMU
    self . ToUnit   = TOU
    RR   = self . PrepareUnit ( self . FromUnit , self . ToUnit              )
    ##########################################################################
    self . Denominator = RR   [ 1                                            ]
    self . Numerator   = RR   [ 2                                            ]
    ##########################################################################
    return RR                 [ 0                                            ]
  ############################################################################
  def toMPZ                   ( self , PLEN                                ) :
    return self . ConvertMPZ  ( PLEN , self . Denominator , self . Numerator )
    ##########################################################################
    return float              ( R                                            )
  ############################################################################
  def toMPFR                  ( self , PLEN                                ) :
    return self . ConvertMPFR ( PLEN , self . Denominator , self . Numerator )
  ############################################################################
  def toInt               ( self , PLEN                                    ) :
    ##########################################################################
    R = self . ConvertMPZ ( PLEN , self . Denominator , self . Numerator     )
    ##########################################################################
    return int            ( gmpy2 . digits ( R , 10 )                        )
  ############################################################################
  def toFloat              ( self , PLEN                                   ) :
    ##########################################################################
    R = self . ConvertMPFR ( PLEN , self . Denominator , self . Numerator    )
    ##########################################################################
    return float              ( R                                            )
  ############################################################################
  def ConvertToInt          ( self , PLEN , FromUnit , ToUnit              ) :
    ##########################################################################
    RR = self . PrepareUnit ( FromUnit , ToUnit                              )
    ##########################################################################
    if                      ( not RR [ 0 ]                                 ) :
      return 0
    ##########################################################################
    D  = RR                 [ 1                                              ]
    N  = RR                 [ 2                                              ]
    ##########################################################################
    Z  = self . ConvertMPZ  ( PLEN , D , N                                   )
    ##########################################################################
    return int              ( gmpy2 . digits ( Z , 10 )                      )
  ############################################################################
  def ConvertToFloat        ( self , PLEN , FromUnit , ToUnit              ) :
    ##########################################################################
    RR = self . PrepareUnit ( FromUnit , ToUnit                              )
    ##########################################################################
    if                      ( not RR [ 0 ]                                 ) :
      return 0.0
    ##########################################################################
    D  = RR                 [ 1                                              ]
    N  = RR                 [ 2                                              ]
    ##########################################################################
    Z  = self . ConvertMPFR ( PLEN , D , N                                   )
    ##########################################################################
    return float            ( Z                                              )
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
