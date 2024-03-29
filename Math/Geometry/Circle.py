# -*- coding: utf-8 -*-
##############################################################################
## Circle
##############################################################################
import math
##############################################################################
from . ControlPoint import ControlPoint as ControlPoint
##############################################################################
class Circle     (                                                         ) :
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
    self . O = ControlPoint (                                                )
    self . X = ControlPoint (                                                )
    self . Y = ControlPoint (                                                )
    self . N = 0
    ##########################################################################
    return
  ############################################################################
  def assign ( self , circle                                               ) :
    ##########################################################################
    self . O = circle . O
    self . X = circle . X
    self . Y = circle . Y
    self . N = circle . N
    ##########################################################################
    return self
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
  def setSectors      ( self , Sectors                                     ) :
    ##########################################################################
    self . N = int    (        Sectors                                       )
    ##########################################################################
    return Sectors
  ############################################################################
  def Angle             ( self , angle , P                                 ) :
    ##########################################################################
    A    = float        ( math . pi * angle                                  )
    C    = ControlPoint (                                                    )
    sinv = math . sin   ( A                                                  )
    cosv = math . cos   ( A                                                  )
    ##########################################################################
    P    . assign       ( self . O                                           )
    C    . assign       ( self . X                                           )
    C    . multiply     ( cosv                                               )
    P    . VectorPlus   ( C                                                  )
    C    . assign       ( self . Y                                           )
    C    . multiply     ( sinv                                               )
    P    . VectorPlus   ( C                                                  )
    ##########################################################################
    return True
  ############################################################################
  def GeneratePoints               ( self , StartId , TextureId , JSON     ) :
    ##########################################################################
    for id in range                ( 0 , self . N                          ) :
      ########################################################################
      DEGREE = float               ( float ( id * 2 ) / float ( self . N )   )
      PID    = StartId   + id
      TID    = TextureId + id
      P      = ControlPoint        (                                         )
      self   . Angle               ( DEGREE , P                              )
      ########################################################################
      JSON [ "Points"   ] [ PID ] = P
      JSON [ "TPoints"  ] [ TID ] = P
      JSON [ "Vertices" ] . append ( PID                                     )
      JSON [ "Dots"     ] . append ( PID                                     )
    ##########################################################################
    TID      = TID + 1
    JSON   [ "TPoints"  ] [ TID ] = JSON [ "Points" ] [ StartId              ]
    ##########################################################################
    return JSON
##############################################################################
