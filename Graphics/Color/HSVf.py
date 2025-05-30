# -*- coding: utf-8 -*-
##############################################################################
## HSVf
## HSV顏色模型 0~1浮點值域
##############################################################################
import cv2
import numpy as np
import colour
from . CommonColor import CommonColor
##############################################################################
class HSVf                    ( CommonColor                                ) :
  ############################################################################
  def __init__                ( self                                       ) :
    ##########################################################################
    self . ColorModel = "HSV"
    self . ValueType  = "Double"
    ##########################################################################
    self . H          = float ( 0.0                                          )
    self . S          = float ( 0.0                                          )
    self . V          = float ( 0.0                                          )
    ##########################################################################
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  ## 轉成JSON格式
  ############################################################################
  def toJson ( self                                                        ) :
    return   { "Model" : "HSV"                                             , \
               "Value" : "Float"                                           , \
               "H"     : self . H                                          , \
               "S"     : self . S                                          , \
               "V"     : self . V                                            }
  ############################################################################
  ## 從JSON格式轉換顏色模型
  ############################################################################
  def fromJson       ( self , JSON                                         ) :
    ##########################################################################
    KEYs =           [ "Model" , "Value" , "H" , "S" , "V"                   ]
    ##########################################################################
    for K in KEYs                                                            :
      if             ( K not in JSON                                       ) :
        return False
    ##########################################################################
    if               ( "HSV"   != JSON [ "Model" ]                         ) :
      return   False
    ##########################################################################
    if               ( "Float" != JSON [ "Value" ]                         ) :
      return   False
    ##########################################################################
    self . H = float ( JSON [ "H" ]                                          )
    self . S = float ( JSON [ "S" ]                                          )
    self . V = float ( JSON [ "V" ]                                          )
    ##########################################################################
    return     True
  ############################################################################
  def fromHSVi                   ( self , iHSV                             ) :
    ##########################################################################
    self . H = self . ScaleFloat (        iHSV . H                           )
    self . S = self . ScaleFloat (        iHSV . S                           )
    self . V = self . ScaleFloat (        iHSV . V                           )
    ##########################################################################
    return
  ############################################################################
  def toHSV ( self                                                         ) :
    return  [ self . H , self . S , self . V                                 ]
  ############################################################################
  def toNpHSV         ( self                                               ) :
    return np . array ( [ [ self . toHSV ( ) ] ] , dtype = np . float64      )
  ############################################################################
  def fromCvHSV      ( self , HSV                                          ) :
    ##########################################################################
    self . H = float ( HSV [ 0 ]                                             )
    self . S = float ( HSV [ 1 ]                                             )
    self . V = float ( HSV [ 2 ]                                             )
    ##########################################################################
    return
  ############################################################################
  def Distance          ( self ,                       C                   ) :
    ##########################################################################
    NP = self . toNpHSV (                                                    )
    ##########################################################################
    return np . sqrt    ( np . sum ( ( NP [ 0 ][ 0 ] - C ) ** 2            ) )
##############################################################################
