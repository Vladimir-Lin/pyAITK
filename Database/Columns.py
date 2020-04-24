# -*- coding: utf-8 -*-
#
# 資料庫欄位處理元件
# 最後更新日期
#

import os
import sys

class Columns ( ) :

  def __init__ ( self ) :
    self . Columns = [ ]

  def __del__ ( self ) :
    self . Columns = [ ]

  # 清除欄位
  def clear ( self ) :
    self . Columns = [ ]
    return self . Columns

  # 新增欄位
  def append ( self , column ) :
    self . Columns . append ( column )
    return self . Columns

  # 擴展欄位
  def extend ( self , columns ) :
    self . Columns . extend ( columns )

  # 指定欄位項目
  def assign ( self , item ) :
    raise NotImplementedError ( )

  # 指定欄位值
  def set ( self , item , value ) :
    raise NotImplementedError ( )

  # 轉成JSON格式
  def toJson ( self ) :
    raise NotImplementedError ( )

  # 指定讀取欄位列表
  def tableItems ( self ) :
    raise NotImplementedError ( )

  # 欄=值
  def pair ( self , item ) :
    raise NotImplementedError ( )

  # 欄位列表
  def join ( self , Lists , Splitter = "," ) :
    U = [ ]
    for x in Lists :
      v = f'`{x}`'
      U . append ( v )
    L = Splitter . join ( U )
    return L

  # 讀取欄位列表
  def items ( self , Splitter = "," ) :
    List = self . tableItems ( )
    return self . join ( List , Splitter )

  # 語句尾部
  def tail ( self , Options , Limits ) :
    Q = ""
    if ( len ( Options ) > 0 ) :
      Q += " "
      Q += Options
    if ( len ( Limits ) > 0 ) :
      Q += " "
      Q += Limits
    return Q

  # 欄值列表
  def pairs ( self , items ) :
    I = [ ]
    for x in items :
      I . append ( "( " + self . pair ( x ) + " )" )
    L = " and " . join ( I )
    return L

  # 過濾欄位語法
  def QueryItems ( self , items , Options = "" , Limits = "" ) :
    IS    = self . pairs ( items )
    TAILs = self . tail  ( Options , Limits )
    QQ    = f" where {IS} {TAILs}"
    return QQ

  # 查詢欄位語法
  def SelectItems ( self , Table , items , Options , Limits ) :
    IS    = self . items ( " , " )
    QUERY = self . QueryItems ( items , Options , Limits )
    QQ    = f"select {IS} from {Table} {QUERY} ;"
    return QQ

  # 查詢欄位
  def SelectColumns ( self , Table , Options = "" , Limits = "" ) :
    return self . SelectItems ( Table , self . Columns , Options , Limits )

  # 取得欄位
  def obtain ( self , R ) :
    List = self . tableItems ( )
    CNT  = 0
    for x in List :
      self . set ( x , R [ CNT ] )
      CNT += 1
    return True

  # 透過uuid取得數據
  def ObtainsByUuid ( self , DB , Table ) :
    ITS = self . items ( )
    WHS = DB . WhereUuid ( self . Uuid , True )
    QQ = f"select {ITS} from {Table} {WHS}"
    DB . Execute ( QQ )
    LL = DB . FetchOne ( )
    if ( not LL ) :
      return False
    return self . obtain ( LL )

  # 透過id取得數據
  def ObtainsById ( self , DB , Table ) :
    ITS = self . items ( )
    WHS = DB . WhereId ( self . Id , True )
    QQ = f"select {ITS} from {Table} {WHS}"
    DB . Execute ( QQ )
    LL = DB . FetchOne ( )
    if ( not LL ) :
      return False
    return self . obtain ( LL )
