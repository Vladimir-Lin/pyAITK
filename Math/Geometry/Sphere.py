# -*- coding: utf-8 -*-
##############################################################################
## Sphere
##############################################################################
from . ControlPoint import ControlPoint as ControlPoint
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
    self . R = ControlPoint (                                                ) ## Radius Vector
    self . N =              {                                                } ## Sectors
    ##########################################################################
    return
  ############################################################################
  def assign ( self , sphere                                               ) :
    ##########################################################################
    self . O = sphere . O
    self . X = sphere . X
    self . Y = sphere . Y
    self . R = sphere . R
    self . N = sphere . N
    ##########################################################################
    return
##############################################################################