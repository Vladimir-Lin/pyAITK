# -*- coding: utf-8 -*-
#
# SQL Query Syntax Composer
# 資料庫語法合成器
#

import os
import sys

class Query ( ) :

  def __init__ ( self ) :
    self . lists = [ ]

  def __del__ ( self ) :
    pass

  # Clear Query Lists
  # 清除查詢項目清單
  def Clear ( self ) :
    self . lists = [ ]

  # Add a query entry
  # 新增一個查詢項目
  def Add ( self , query ) :
    self . lists . append ( query )

  def End ( self ) :
    self . Add ( ";" )

  # Merge all query entries
  # 合併所有的查詢項目
  def Query ( self , Tail = True ) :
    QQ = ' ' . join ( self . lists )
    if ( Tail ) :
      QQ = f"{QQ} ;" ;
    return QQ

  # SQL select
  def SelectFrom ( self , items , table ) :
    T = self . AssureTable ( table )
    self . Add ( f"select {items} from {T}" )

  # SQL insert into table
  def InsertInto ( self , table ) :
    T = self . AssureTable ( table )
    self . Add ( f"insert into {T}" )

  # SQL update
  def Update ( self ) :
    self . Add ( "update" )

  # SQL where
  def Where ( self ) :
    self . Add ( "where" )

  # SQL Where Uuid
  def WhereUuid ( self , U ) :
    return f"where ( `uuid` = {U} )"

  # Add Where ( `uuid` = UUID )
  def AddWhereUuid ( self , U ) :
    self . Add ( self . WhereUuid ( U ) )

  # SQL Where Id
  def WhereId ( self , U ) :
    return f"where ( `id` = {U} )"

  # Add Where ( `id` = ID )
  def AddWhereId ( self , U ) :
    self . Add ( self . WhereId ( U ) )

  # SQL values
  def Values ( self ) :
    self . Add ( "values" )

  # SQL set
  def Set ( self ) :
    self . Add ( "set" )

  def Use ( self , Database ) :
    X = self . AssureItem ( Database ) ;
    return f"use {X} ;"

  # SQL item pair
  def Pair ( self , item , value ) :
    X = self . AssureItem ( item ) ;
    return f"{X} = {value}"

  # SQL add item pair
  def AddPair ( self , item , value ) :
    return self . Add ( self . Pair ( item , value ) )

  # SQL items
  def Items ( self , items ) :
    quotes = [ ]
    for L in items :
      quotes . append ( self . AssureItem ( L ) )
    return ' , ' . join ( quotes )

  # SQL Bracket
  def RoundBracket ( self , item ) :
    return f"( {item} )"

  def rbItems ( self , items ) :
    return self . RoundBracket ( self . Items ( items ) )

  # SQL Order By
  def OrderBy ( self ) :
    self . Add ( "order by" )

  # SQL Limit
  def Limit ( self , start , total ) :
    self . Add ( f"limit {start} , {total}" )

  def Count ( self , Table , Options = "" ) :
    T = self . AssureTable ( Table )
    return f"select count(*) from {T} {Options};"

  # Append `` marks if not exits
  # 新增``記號到表格名稱項目上
  def AssureItem ( self , name ) :
    if ( "`" not in name ) :
      return f"`{name}`"
    return name

  # Append `` marks to item lists if not exits
  # 新增``記號到表格項目列表名稱上
  def AssureTable ( self , name ) :
    if ( "." in name ) :
      list = name . split ( "." )
      quotes = [ ]
      for L in list :
        quotes . append ( self . AssureItem ( L ) )
      return '.' . join ( quotes )
    else :
      return self . AssureItem ( name )
    return name

  # Make a legal table syntax
  # 將表格名稱正規化
  def MakeTable ( self , db , table ) :
    return self . AssureTable ( f"{db}.{table}" )

  # Make tables syntax legal
  # 將表格名稱列表正規化
  def MakeTables ( self , db , tables ) :
    T = [ ]
    for t in tables :
      T . append ( self . MakeTable ( db , t ) )
    return T

  # Drop a database table
  # 清除資料庫表格
  def DropTable ( self , table ) :
    ttt = self . AssureTable ( table )
    DTS = f"drop table if exists {ttt} ;"
    self . Add ( DTS )

  # Lock a table
  # 鎖住指定表格
  def LockWrite ( self , table ) :
    return self . LockWrites ( self , [ table ] )

  # Lock tables
  # 鎖住指定表格列表
  def LockWrites ( self , tables ) :
    if ( len ( tables ) <= 0 ) :
      return ""
    T = [ ]
    for t in tables :
      x = self . AssureTable ( t )
      T . append ( f"{x} write" )
    L = " , " . join ( T )
    return f"lock tables {L} ;"

  # Unlock tables
  # 釋放鎖住的表格列表
  def UnlockTables ( self ) :
    return "unlock tables ;"

  # Merge Table Options
  # 合併表格選項
  def MergeOptions ( self , tables , method = "last" ) :
    T = [ ]
    for t in tables :
      T . append ( self . AssureTable ( t ) )
    unions = " , " . join ( T )
    return f"insert_method = {method} union = ( {unions} ) ;"

  # Create a numbered combinational table
  # 產生編號化表格
  def CreateNumberedTable ( self , heading , n , fill = 4 ) :
    # numbered coding
    # 前面填充0的編號
    numbered = str ( n ) . zfill ( fill )
    # Combined Table
    # 組合的表格名稱
    table    = heading + numbered
    return table

  # Create a group of numbered tables
  # 產生編號化表格群
  def CreateTableLists ( self , db , heading , start , stop , fill = 4 ) :
    list = [ ]
    for i in range ( start , stop ) :
      table = self . CreateNumberedTable ( heading , i , fill )
      # With database name
      # 合併資料庫名稱
      t        = self . MakeTable ( db , table )
      list     . append           ( t          )
    return list

  # Create a group of numbered tables without database prefix
  # 產生無資料庫名稱的表格列表
  def CreateNameLists ( self , heading , start , stop , fill = 4 ) :
    list    = [ ]
    for i in range                       ( start , stop       ) :
      table = self . CreateNumberedTable ( heading , i , fill )
      list  . append                     ( table              )
    return list

  # Using JSONed table to create a group of numbered tables
  # 使用JSON數據產生編號表格群
  # heading : 前置表格名稱
  # start   : 開始編號
  # total   : 表格數量
  # fill    : 數字固定長度,未滿者前方填入0
  def CreateTableGroup ( self , db , Group ) :
    heading = Group [ "heading" ]
    start   = Group [ "start"   ]
    stop    = Group [ "total"   ] + start
    fill    = Group [ "fill"    ]
    return self . CreateTableLists ( db , heading , start , stop , fill )

  # Create Templated Table by replacing parameters
  # 透過替換表格參數的方式修改表格模板來產生新表格
  def GenerateTable ( self , Template , Parameters ) :
    Table = Template
    for P in Parameters :
      Table = Table . replace ( P , Parameters [ P ] )
    return Table
