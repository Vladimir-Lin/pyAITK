# -*- coding: utf-8 -*-
##############################################################################
## 樸克牌處理類別
##############################################################################
import os
import sys
import random
##############################################################################
class Card           (                                                     ) :
  ############################################################################
  def __init__       ( self , Suits = 1                                    ) :
    self . Index = 0
    self . Cards =   [                                                       ]
    for x in range   (        Suits                                        ) :
      self . addSuit (                                                       )
    return
  ############################################################################
  def __del__  ( self                                                      ) :
    return
  ############################################################################
  def addSuit      ( self                                                  ) :
    ##########################################################################
    for i in range ( 0 , 52                                                ) :
      self . Cards . append ( i                                              )
    ##########################################################################
    return
  ############################################################################
  def shuffle        ( self                                                ) :
    ##########################################################################
    random . shuffle ( self . Cards                                          )
    ##########################################################################
    return
  ############################################################################
  def Point          ( self , card                                         ) :
    return           int ( ( int ( card ) % 13 ) + 1                         )
  ############################################################################
  def Flower         ( self , card                                         ) :
    return           int   ( int ( card ) / 13                               )
##############################################################################
