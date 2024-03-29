# -*- coding: utf-8 -*-
##############################################################################
## Sphere
##############################################################################
import math
##############################################################################
from . ControlPoint import ControlPoint as ControlPoint
from . Circle       import Circle       as Circle
##############################################################################
class Sphere     (                                                         ) :
  ############################################################################
  def __init__   ( self                                                    ) :
    ##########################################################################
    self . clear (                                                           )
    ##########################################################################
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def clear                 ( self                                         ) :
    ##########################################################################
    self . O = ControlPoint (                                                ) ## Center
    self . X = ControlPoint (                                                ) ## X Vector
    self . Y = ControlPoint (                                                ) ## Y Vector
    self . Z = ControlPoint (                                                ) ## Z Vector
    self . N =              { "Horizontal" : 360 , "Vertical" : 180          } ## Sectors
    ##########################################################################
    return
  ############################################################################
  def assign ( self , sphere                                               ) :
    ##########################################################################
    self . O = sphere . O
    self . X = sphere . X
    self . Y = sphere . Y
    self . Z = sphere . Z
    self . N = sphere . N
    ##########################################################################
    return
  ############################################################################
  def setCenter       ( self , P                                           ) :
    ##########################################################################
    self . O . assign (        P                                             )
    ##########################################################################
    return P
  ############################################################################
  def setX            ( self , V                                           ) :
    ##########################################################################
    self . X . assign (        V                                             )
    ##########################################################################
    return V
  ############################################################################
  def setY            ( self , V                                           ) :
    ##########################################################################
    self . Y . assign (        V                                             )
    ##########################################################################
    return V
  ############################################################################
  def setZ            ( self , V                                           ) :
    ##########################################################################
    self . Z . assign (        V                                             )
    ##########################################################################
    return V
  ############################################################################
  def setSectors ( self , hSectors , vSectors                              ) :
    ##########################################################################
    self . N [ "Horizontal" ] = hSectors
    self . N [ "Vertical"   ] = vSectors
    ##########################################################################
    return
  ############################################################################
  def setRadius       ( self , RX  , RY  , RZ                              ) :
    ##########################################################################
    self . X . setXYZ (        RX  , 0.0 , 0.0                               )
    self . Y . setXYZ (        0.0 , RY  , 0.0                               )
    self . Z . setXYZ (        0.0 , 0.0 , RZ                                )
    ##########################################################################
    return
  ############################################################################
  def setRadiusVector ( self , RV                                          ) :
    ##########################################################################
    self . X . setXYZ ( RV . x ,    0.0 ,    0.0                             )
    self . Y . setXYZ (    0.0 , RV . y ,    0.0                             )
    self . Z . setXYZ (    0.0 ,    0.0 , RV . z                             )
    ##########################################################################
    return
  ############################################################################
  def IndexLatitude ( self , Index                                         ) :
    ##########################################################################
    V = self . N    [ "Vertical"                                             ]
    F = float       ( float ( Index ) / float ( V )                          )
    ##########################################################################
    return float    ( 0.5 - F                                                )
  ############################################################################
  ## 設定北極
  ############################################################################
  def setNorth             ( self , P , JSON                               ) :
    ##########################################################################
    H       = self . N     [ "Horizontal"                                    ]
    NORTH   = JSON         [ "Poles" ] [ "North"                             ]
    PID     = NORTH
    ##########################################################################
    for id in range        ( 0 , H                                         ) :
      ########################################################################
      Z     = ControlPoint (                                                 )
      Z     . assign       ( P                                               )
      JSON [ "Points" ] [ PID ] = Z
      ########################################################################
      PID   = PID + 1
    ##########################################################################
    return JSON
  ############################################################################
  ## 設定南極
  ############################################################################
  def setSouth             ( self , P , JSON                               ) :
    ##########################################################################
    H       = self . N     [ "Horizontal"                                    ]
    SOUTH   = JSON         [ "Poles" ] [ "South"                             ]
    PID     = SOUTH
    ##########################################################################
    for id in range        ( 0 , H                                         ) :
      ########################################################################
      Z     = ControlPoint (                                                 )
      Z     . assign       ( P                                               )
      JSON [ "Points" ] [ PID ] = Z
      ########################################################################
      PID   = PID + 1
    ##########################################################################
    return JSON
  ############################################################################
  ## 產生經線
  ############################################################################
  def GenerateWarp     ( self , JSON                                       ) :
    ##########################################################################
    H       = self . N [ "Horizontal"                                        ]
    V       = self . N [ "Vertical"                                          ]
    M       = int      ( H / 2                                               )
    ##########################################################################
    NORTH   = JSON     [ "Poles" ] [ "North"                                 ]
    SOUTH   = JSON     [ "Poles" ] [ "South"                                 ]
    BASE    = int      ( NORTH + H                                           )
    ##########################################################################
    for id in range    ( 0 , M                                             ) :
      ########################################################################
      SEG   =          [                                                     ]
      ########################################################################
      SEG   . append   ( NORTH                                               )
      ########################################################################
      for zz in range  ( 1 , V                                             ) :
        ######################################################################
        K   = int      ( ( zz - 1 ) * H                                      )
        SEG . append   ( BASE + K + id                                       )
      ########################################################################
      SEG   . append   ( SOUTH                                               )
      ########################################################################
      for zz in range  ( 1 , V                                             ) :
        ######################################################################
        K   = int      ( ( V - zz - 1 ) * H                                  )
        SEG . append   ( BASE + K + id + M                                   )
      ########################################################################
      SEG   . append   ( NORTH                                               )
      ########################################################################
      JSON [ "Lines" ] [ "Warp" ] [ id ] = SEG
    ##########################################################################
    return JSON
  ############################################################################
  ## 產生緯線
  ############################################################################
  def GenerateWeft     ( self , JSON                                       ) :
    ##########################################################################
    H       = self . N [ "Horizontal"                                        ]
    V       = self . N [ "Vertical"                                          ]
    ##########################################################################
    NORTH   = JSON     [ "Poles" ] [ "North"                                 ]
    SOUTH   = JSON     [ "Poles" ] [ "South"                                 ]
    BASE    = int      ( NORTH + H                                           )
    ##########################################################################
    for   id in range  ( 1 , V                                             ) :
      ########################################################################
      SEG   =          [                                                     ]
      HBASE = int      ( BASE + int ( ( id - 1 ) * H )                       )
      ########################################################################
      for zz in range  ( 0 , H                                             ) :
        ######################################################################
        SEG . append   ( HBASE + zz                                          )
      ########################################################################
      SEG   . append   ( HBASE                                               )
      ########################################################################
      JSON [ "Lines" ] [ "Weft" ] [ id ] = SEG
    ##########################################################################
    return JSON
  ############################################################################
  ## 產生多邊形
  ############################################################################
  def GeneratePolygons               ( self , JSON                         ) :
    ##########################################################################
    H      = self . N                [ "Horizontal"                          ]
    V      = self . N                [ "Vertical"                            ]
    ##########################################################################
    NORTH  = JSON                    [ "Poles" ] [ "North"                   ]
    SOUTH  = JSON                    [ "Poles" ] [ "South"                   ]
    BASE   = int                     ( NORTH + H                             )
    ##########################################################################
    ## 產生北極多邊形
    ##########################################################################
    for id in range                  ( 0 , H                               ) :
      ########################################################################
      A    = int                     ( id                                    )
      B    = int                     ( ( id + 1 ) % H                        )
      ########################################################################
      JSON [ "Polygons" ] . append   ( [ NORTH , A + BASE , B + BASE       ] )
    ##########################################################################
    ## 產生中間多邊形
    ##########################################################################
    for   Weft in range              ( 1 , V - 1                           ) :
      ########################################################################
      U    = int                     ( ( Weft - 1 ) * H                      )
      T    = int                     ( U + H                                 )
      ########################################################################
      for Warp in range              ( 0 , H                               ) :
        ######################################################################
        A  = int                     (   Warp                                )
        B  = int                     ( ( Warp + 1 ) % H                      )
        ######################################################################
        P1 = int                     ( U + A                                 )
        P2 = int                     ( U + B                                 )
        P3 = int                     ( T + B                                 )
        P4 = int                     ( T + A                                 )
        ######################################################################
        JSON [ "Polygons" ] . append ( [ P1 , P2 , P3 , P4                 ] )
    ##########################################################################
    ## 產生南極多邊形
    ##########################################################################
    KBASE  = int                     ( BASE + int ( ( V - 2 ) * H )          )
    for id in range                  ( 0 , H                               ) :
      ########################################################################
      A    = int                     (   id                                  )
      B    = int                     ( ( id + 1 ) % H                        )
      ########################################################################
      JSON [ "Polygons" ] . append   ( [ A + KBASE , B + KBASE , SOUTH     ] )
    ##########################################################################
    return JSON
  ############################################################################
  ## 產生材質多邊形
  ############################################################################
  def GenerateTPolygons               ( self , JSON                        ) :
    ##########################################################################
    H      = self . N                 [ "Horizontal"                         ]
    V      = self . N                 [ "Vertical"                           ]
    ##########################################################################
    NORTH  = JSON                     [ "Poles" ] [ "North"                  ]
    SOUTH  = JSON                     [ "Poles" ] [ "South"                  ]
    BASE   = int                      ( NORTH                                )
    ##########################################################################
    for   Weft in range               ( 0 , V                              ) :
      ########################################################################
      U    = int                      ( Weft * ( H + 1 )                     )
      T    = int                      ( U    +   H + 1                       )
      ########################################################################
      for Warp in range               ( 0 , H                              ) :
        ######################################################################
        A  = int                      ( Warp                                 )
        B  = int                      ( Warp + 1                             )
        ######################################################################
        P1 = int                      ( U + A                                )
        P2 = int                      ( U + B                                )
        P3 = int                      ( T + B                                )
        P4 = int                      ( T + A                                )
        ######################################################################
        JSON [ "TPolygons" ] . append ( [ P1 , P2 , P3 , P4                ] )
    ##########################################################################
    return JSON
  ############################################################################
  ## 產生材質映射座標
  ############################################################################
  def GenerateTCoords               ( self , JSON                          ) :
    ##########################################################################
    H     = self . N                [ "Horizontal"                           ]
    V     = self . N                [ "Vertical"                             ]
    ##########################################################################
    LX    =                         [                                        ]
    LY    =                         [                                        ]
    ##########################################################################
    for Warp in range               ( 0 , H + 1                            ) :
      ########################################################################
      F   = float                   ( float ( Warp ) / float ( H )           )
      LX  . append                  ( F                                      )
    ##########################################################################
    for Weft in range               ( 0 , V + 1                            ) :
      ########################################################################
      F   = float                   ( float ( Weft ) / float ( V )           )
      LY  . append                  ( 1.0 - F                                )
    ##########################################################################
    for   Weft in range             ( 0 , V + 1                            ) :
      ########################################################################
      for Warp in range             ( 0 , H + 1                            ) :
        ######################################################################
        X = LX                      [ Warp                                   ]
        Y = LY                      [ Weft                                   ]
        P = ControlPoint            (                                        )
        P . setXYZ                  ( X , Y , 0                              )
        JSON [ "TCoords" ] . append ( P                                      )
    ##########################################################################
    return JSON
  ############################################################################
  def GeneratePoints                    ( self , StartId , JSON            ) :
    ##########################################################################
    PID      = StartId
    TID      = StartId
    H        = self . N                 [ "Horizontal"                       ]
    V        = self . N                 [ "Vertical"                         ]
    Z        = self . Z
    O        = self . O
    OP       = ControlPoint             (                                    )
    PP       = ControlPoint             (                                    )
    XP       = ControlPoint             (                                    )
    YP       = ControlPoint             (                                    )
    ZP       = ControlPoint             (                                    )
    ##########################################################################
    JSON   [ "Sectors"  ] [ "Horizontal" ] = H
    JSON   [ "Sectors"  ] [ "Vertical"   ] = V
    ##########################################################################
    JSON   [ "Dots"     ] . append      ( PID                                )
    JSON   [ "Poles"    ] [ "North" ] = PID
    ##########################################################################
    ## 產生北極
    ##########################################################################
    for id in range                     ( 0 , H                            ) :
      ########################################################################
      JSON [ "Points"   ] [ PID ] = Z
      JSON [ "TPoints"  ] [ TID ] = Z
      JSON [ "Vertices" ] . append      ( PID                                )
      PID    = PID + 1
      TID    = TID + 1
    ##########################################################################
    JSON   [ "TPoints"  ] [ TID ] = Z
    TID      = TID + 1
    ##########################################################################
    ## 產生頂點
    ##########################################################################
    for id in range                     ( 1 , V                            ) :
      ########################################################################
      DEGREE = self . IndexLatitude     ( id                                 )
      A      = float                    ( math . pi * DEGREE                 )
      C      = Circle                   (                                    )
      sinv   = math . sin               ( A                                  )
      cosv   = math . cos               ( A                                  )
      ########################################################################
      PP     . assign                   ( Z                                  )
      PP     . multiply                 ( cosv                               )
      ########################################################################
      ZP     . assign                   ( Z                                  )
      ZP     . multiply                 ( sinv                               )
      ########################################################################
      XP     . assign                   ( self . X                           )
      XP     . multiply                 ( cosv                               )
      ########################################################################
      YP     . assign                   ( self . Y                           )
      YP     . multiply                 ( cosv                               )
      ########################################################################
      OP     . assign                   ( O                                  )
      OP     . VectorPlus               ( ZP                                 )
      ########################################################################
      C      . setCenter                ( OP                                 )
      C      . setX                     ( XP                                 )
      C      . setY                     ( YP                                 )
      C      . setSectors               ( H                                  )
      C      . GeneratePoints           ( PID , TID , JSON                   )
      ########################################################################
      PID    = int                      ( PID + H                            )
      TID    = int                      ( TID + H + 1                        )
    ##########################################################################
    ZP       . assign                   ( Z                                  )
    ZP       . multiply                 ( -1.0                               )
    ##########################################################################
    JSON [ "Dots"     ] . append        ( PID                                )
    JSON [ "Poles"    ] [ "South" ] = PID
    ##########################################################################
    for id in range                     ( 0 , H                            ) :
      ########################################################################
      JSON [ "Points"   ] [ PID ] = ZP
      JSON [ "TPoints"  ] [ TID ] = ZP
      JSON [ "Vertices" ] . append      ( PID                                )
      ########################################################################
      PID    = PID + 1
      TID    = TID + 1
    ##########################################################################
    JSON   [ "TPoints"  ] [ TID ] = ZP
    ##########################################################################
    ## 產生緯線
    ##########################################################################
    JSON     = self . GenerateWeft      ( JSON                               )
    ##########################################################################
    ## 產生經線
    ##########################################################################
    JSON     = self . GenerateWarp      ( JSON                               )
    ##########################################################################
    ## 產生多邊形
    ##########################################################################
    JSON     = self . GeneratePolygons  ( JSON                               )
    ##########################################################################
    ## 產生材質多邊形
    ##########################################################################
    JSON     = self . GenerateTPolygons ( JSON                               )
    ##########################################################################
    ## 產生材質映射座標
    ##########################################################################
    JSON     = self . GenerateTCoords   ( JSON                               )
    ##########################################################################
    return JSON
  ############################################################################
  def GenerateMesh               ( self , StartId = 0                      ) :
    ##########################################################################
    JSON =                       { "Points"       : {                    } , \
                                   "TPoints"      : {                    } , \
                                   "Vertices"     : [                    ] , \
                                   "Dots"         : [                    ] , \
                                   "Lines"        :                        { \
                                     "Weft"       : {                  }   , \
                                     "Warp"       : {                  } } , \
                                   "Polygons"     : [                    ] , \
                                   "TPolygons"    : [                    ] , \
                                   "TCoords"      : [                    ] , \
                                   "Poles"        :                        { \
                                     "North"      : -1                     , \
                                     "South"      : -1                   } , \
                                   "Sectors"      :                        { \
                                     "Horizontal" : 0                      , \
                                     "Vertical"   : 0                      } }
    ##########################################################################
    return self . GeneratePoints ( StartId , JSON                            )
##############################################################################
