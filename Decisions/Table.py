# -*- coding: utf-8 -*-
#
# 決策表
#

import os
import sys
import time
import datetime
from   threading import Thread
from   threading import Lock

class Table ( ) :

  def __init__ ( self , uuid ) :
    self . Uuid   = uuid
    self . locker = Lock ( )
    self . clear         ( )
    return

  def __del__ ( self ) :
    pass

  # 檢查是否為相同的決策表
  def __eq__ ( self , another ) :
    return self . isEqual ( another )

  # 檢查是否為相同的決策表
  def isEqual ( self , another ) :
    return ( self . Uuid == another . Uuid )

  # 清除決策表
  def clear ( self ) :
    self . locker . acquire ( )
    self . conditions =     { }
    self . actions    =     { }
    self . locker . release ( )
    return

  # 新增決策行動
  def addAction ( self , action ) :
    self . locker . acquire (      )
    if ( action not in self . actions ) :
      self . actions [ action . Uuid ] = action
    self . locker . release (      )
    return

  # 移除決策行動
  def removeAction ( self , action ) :
    self . locker . acquire (      )
    if ( action . Uuid in self . actions ) :
      del self . actions [ action . Uuid ]
    self . locker . release (      )
    return

  # 判斷是否有決策行動
  def hasAction ( self , action ) :
    return ( action . Uuid in self . actions )

  # 決策行動列表
  def actionKeys ( self ) :
    return self . actions . keys ( )

  # 新增條件
  def addCondition ( self , condition ) :
    self . locker . acquire (      )
    if ( condition not in self . conditions ) :
      self . conditions [ condition . Uuid ] = condition
    self . locker . release (      )
    return

  # 移除條件
  def removeCondition ( self , condition ) :
    self . locker . acquire (      )
    if ( condition . Uuid in self . conditions ) :
      del self . conditions [ condition . Uuid ]
    self . locker . release (      )
    return

  # 判斷是否有條件
  def hasCondition ( self , condition ) :
    return ( condition . Uuid in self . conditions )

  # 條件列表
  def conditionKeys ( self ) :
    return self . conditions . keys ( )

  def attach ( self , action , condition ) :
    self . locker . acquire (      )
    if ( action not in self . actions ) :
      self . actions [ action . Uuid ] = action
    if ( condition not in self . conditions ) :
      self . conditions [ condition . Uuid ] = condition
    action . addCondition ( condition )
    self . locker . release (      )
    return
