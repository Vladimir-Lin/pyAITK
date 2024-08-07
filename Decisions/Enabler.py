# -*- coding: utf-8 -*-
##############################################################################
## 常用狀態元件
##############################################################################
import os
import sys
import time
import datetime
from   threading import Thread
from   threading import Lock
##############################################################################
class Enabler                (                                             ) :
  ############################################################################
  ## 建構子
  ############################################################################
  def __init__               ( self , locking = True                       ) :
    ##########################################################################
    self . Enablings  =      {                                               }
    self . locker     = Lock (                                               )
    self . shouldLock = locking
    ##########################################################################
    return
  ############################################################################
  ## 解構子
  ############################################################################
  def __del__                ( self                                        ) :
    return
  ############################################################################
  ## 清除參數群
  ############################################################################
  def clear            ( self                                              ) :
    ##########################################################################
    self . __lockUp    (                                                     )
    self . Enablings = {                                                     }
    self . __unleash   (                                                     )
    ##########################################################################
    return
  ############################################################################
  ## 返回參數群
  ############################################################################
  def keys                         ( self                                  ) :
    return self . Enablings . keys (                                         )
  ############################################################################
  ## 返回參數組
  ############################################################################
  def values ( self                                                        ) :
    return self . Enablings
  ############################################################################
  ## 是否可以Mutex Lock
  ############################################################################
  def canLock ( self                                                       ) :
    return self . shouldLock
  ############################################################################
  ## 指定是否Mutex Lock
  ############################################################################
  def setLock ( self , locking = False                                     ) :
    self . shouldLock = locking
    return self . shouldLock
  ############################################################################
  ## 鎖住
  ############################################################################
  def __lockUp              ( self                                         ) :
    if                      ( not self . shouldLock                        ) :
      return
    self . locker . acquire (                                                )
    return
  ############################################################################
  ## 解鎖
  ############################################################################
  def __unleash             ( self                                         ) :
    if                      ( not self . shouldLock                        ) :
      return
    self . locker . release (                                                )
    return
  ############################################################################
  ## 取得陣列中的值
  ############################################################################
  def __getitem__     ( self , key                                         ) :
    return self . get ( key                                                  )
  ############################################################################
  ## 設定陣列中的值
  ############################################################################
  def __setitem__     ( self , key , value                                 ) :
    return self . set (        key , value                                   )
  ############################################################################
  ## 是否有關鍵字
  ############################################################################
  def hasEnabled      ( self , key                                         ) :
    return self . has (        key                                           )
  ############################################################################
  ## 是否有關鍵字
  ############################################################################
  def has  ( self , key                                                    ) :
    return ( key in self . Enablings                                         )
  ############################################################################
  ## 取得陣列中的值
  ############################################################################
  def isEnabled       ( self , key                                         ) :
    return self . get (        key                                           )
  ############################################################################
  ## 取得陣列中的值
  ############################################################################
  def get                ( self , key                                      ) :
    ##########################################################################
    self . __lockUp      (                                                   )
    v = self . Enablings [        key                                        ]
    self . __unleash     (                                                   )
    ##########################################################################
    return v
  ############################################################################
  ## 設定陣列中的值
  ############################################################################
  def setEnabled      ( self , key                                         ) :
    return self . set (        key , True                                    )
  ############################################################################
  ## 設定陣列中的值
  ############################################################################
  def set            ( self , key , value                                  ) :
    ##########################################################################
    self . __lockUp  (                                                       )
    self . Enablings [ key ] = value
    self . __unleash (                                                       )
    ##########################################################################
    return value
  ############################################################################
  ## 移除陣列中的關鍵字
  ############################################################################
  def remove             ( self , key                                      ) :
    ##########################################################################
    self . __lockUp      (                                                   )
    del self . Enablings [ key                                               ]
    self . __unleash     (                                                   )
    ##########################################################################
    return
  ############################################################################
  ## 全部為真
  ############################################################################
  def isAllTrue          ( self                                            ) :
    ##########################################################################
    self . __lockUp      (                                                   )
    ##########################################################################
    Keys = self . keys   (                                                   )
    for k in Keys                                                            :
      if                 ( not self . Enablings [ k ]                      ) :
        self . __unleash (                                                   )
        return False
    ##########################################################################
    self . __unleash     (                                                   )
    ##########################################################################
    return True
  ############################################################################
  ## 全部為假
  ############################################################################
  def isAllFalse         ( self                                            ) :
    ##########################################################################
    self . __lockUp      (                                                   )
    ##########################################################################
    Keys = self . keys   (                                                   )
    for k in Keys                                                            :
      ########################################################################
      if                 ( self . Enablings [ k ]                          ) :
        ######################################################################
        self . __unleash (                                                   )
        return False
    ##########################################################################
    self . __unleash     (                                                   )
    ##########################################################################
    return True
##############################################################################
