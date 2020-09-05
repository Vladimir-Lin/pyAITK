# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import datetime
import logging
import requests
import threading
import gettext
import shutil

import gspread
from   oauth2client.service_account import ServiceAccountCredentials

from   Actions . System . StarDate  import StarDate

class Sheet ( ) :

  def __init__ ( self , Auth = "" ) :
    if ( len ( Auth ) <= 0 ) :
      return
    GSS           = [ 'https://spreadsheets.google.com/feeds' ,
                      'https://www.googleapis.com/auth/drive' ]
    credentials   = ServiceAccountCredentials.from_json_keyfile_name ( Auth , GSS )
    self . client = gspread.authorize ( credentials )

  def __del__ ( self ) :
    pass

  def Open ( self , URL ) :
    self . URL = URL
    self . sheet = self . client . open_by_key ( URL )
    return True

  def Share ( self , EMail , pType = "user" , Role = "writer" ) :
    self . sheet . share ( EMail , pType , Role ) ;
    return True

  def Permissions ( self ) :
    return self . sheet . list_permissions ( )

  def GetSheets ( self ) :
    return self . sheet . worksheets ( )

  def AssignSheet ( self , sheet ) :
    self . id      = sheet . id
    self . order   = -1
    self . current = -1
    self . rows    = -1
    self . columns = -1
    self . title   = str ( sheet . title )
    try :
      self . values  = sheet . get_all_values ( )
      time . sleep ( 2 )
    except :
      return False
    return True

  def AssignSheetByBrief ( self , brief ) :
    self . id      =       brief [ "Page"    ]
    self . order   =       brief [ "Order"   ]
    self . current =       brief [ "Current" ]
    self . rows    =       brief [ "Rows"    ]
    self . columns =       brief [ "Columns" ]
    self . title   = str ( brief [ "Title"   ] )
    self . values  = [ ]
    return True

  def SheetRows ( self ) :
    return len ( self . values )

  def SheetColumns ( self ) :
    columns = 0
    for i in self . values :
      cols = len ( i )
      if ( cols > columns ) :
        columns = cols
    return columns

  def GetSheetPage ( self , DB , URL ) :
    FIND = "select * from `google`.`titles` where `url` = %s and `page` = %s ;"
    VAL  = ( URL , self . id )
    DB . Read . QueryValues ( FIND , VAL )
    return DB . Read . FetchAll ( )

  def PrepareSheetTable ( self , DB , Logger ) :
    URL        = self . URL
    DROPSCHOOL = "drop table if exists `google`.`" + URL + "` ;"
    DB . Write . Query ( DROPSCHOOL )
    CREATETABLE = f"""create table `google`.`{URL}` (
                      `id` integer not null auto_increment primary key,
                      `page` integer default -1,
                      `row` integer default -1,
                      `column` integer default -1,
                      `value` blob default null,
                      `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
                      key(`page`),
                      key(`row`),
                      key(`column`),
                      key(`value`(256)),
                      key(`ltime`)
                      ) Engine = Aria default charset = utf8mb4 ;"""
    DB . Write . Query  ( CREATETABLE )
    Logger . info ( CREATETABLE )
    return True

  def AppendSheetPage ( self , DB , URL , order ) :
    SQL  = "insert into `google`.`titles` ( `url` , `order` , `page` , `title` , `rows` , `columns` ) values ( %s , %s , %s , %s , %s , %s ) ;"
    rows = self . SheetRows    ( )
    cols = self . SheetColumns ( )
    VAL  = ( URL , order , self . id , self . title , rows , cols )
    DB . Write . QueryValues ( SQL , VAL )
    DB . Write . Commit ( )
    return True

  def UpdateSheetPage ( self , DB , URL , order ) :
    UPDATE = "update `google`.`titles` set `title` = %s , `order` = %s , `rows` = %s , `columns` = %s where `url` = %s and `page` = %s ;"
    rows   = self . SheetRows    ( )
    cols   = self . SheetColumns ( )
    VAL    = ( self . title , order , rows , cols , URL , self . id )
    DB . Write . QueryValues ( UPDATE , VAL )
    DB . Write . Commit ( )
    return True

  def FetchTitle ( self , DB , URL , order ) :
    results = self . GetSheetPage ( DB , URL )
    if ( len ( results ) > 0 ) :
      self . UpdateSheetPage ( DB , URL , order )
    else :
      self . AppendSheetPage ( DB , URL , order )
    return True

  def FetchAllTitles ( self , DB , Logger ) :
    try :
      sheets = self . sheet . worksheets ( )
    except :
      return False
    if ( len ( sheets ) <= 0 ) :
      return False
    order   = 0
    for ws in sheets :
      self . AssignSheet ( ws )
      ID     = self . id
      TITLE  = self . title
      ROWS   = self . SheetRows ( )
      COLS   = self . SheetColumns ( )
      Logger . info ( f"== {ID} [ {ROWS} , {COLS} ] ==" )
      self . FetchTitle  ( DB , self . URL , order )
      order += 1
    return True

  def FetchData ( self , DB , URL ) :
    line = 0
    VALs = [ ]
    for v in self . values :
      columns = 0
      for c in v :
        VAL  = ( self . id , line , columns , c )
        VALs . append ( VAL )
        columns += 1
      line += 1
    COLS = f"insert into `google`.`{URL}` ( `page` , `row` , `column` , `value` ) values ( %s , %s , %s , %s )"
    DB . Write . mc . executemany ( COLS , VALs )
    DB . Write . Commit ( )
    return True

  def FetchAllSheets ( self , DB , Logger ) :
    try :
      sheets = self . sheet . worksheets ( )
    except :
      return False
    if ( len ( sheets ) <= 0 ) :
      return False
    URL   = self . URL
    STs   = [ ]
    order = 0
    for ws in sheets :
      ST = Sheet ( )
      if ( not ST . AssignSheet ( ws ) ) :
        return False
      STs . append ( ST )
      ID    = ST . id
      TITLE = ST . title
      Logger . info ( f"== Fetching {URL} : {ID} ==" )
    for ST in STs :
      ID    = ST . id
      TITLE = ST . title
      ROWS  = ST . SheetRows ( )
      COLS  = ST . SheetColumns ( )
      Logger . info ( f"== Importing {URL} : {ID} [ {ROWS} , {COLS} ]  ==" )
      ST     . FetchTitle ( DB , URL , order )
      ST     . FetchData  ( DB , URL )
      order += 1
    return True

  def ReturnSheetInfo ( self , INFO ) :
    if ( not INFO ) :
      return False
    if ( len ( INFO ) <= 0 ) :
      return False
    R = INFO [ 0 ]
    V = { }
    V [ "URL"     ] =       R [ 0 ]
    V [ "Order"   ] = int ( R [ 1 ] )
    V [ "Page"    ] = int ( R [ 2 ] )
    V [ "Current" ] = int ( R [ 3 ] )
    V [ "Rows"    ] = int ( R [ 4 ] )
    V [ "Columns" ] = int ( R [ 5 ] )
    V [ "Title"   ] =       R [ 6 ]
    return V

  def GetSheetInfoByOrder ( self , DB , TABLE , CODE , Order ) :
    QQ = f"select `url`,`order`,`page`,`current`,`rows`,`columns`,`title` from {TABLE} where ( `order` = {Order} ) and ( `url` = '{CODE}' ) ;"
    DB . Query ( QQ )
    R  = DB . FetchAll ( )
    return self . ReturnSheetInfo ( R )

  def GetSheetInfoByPage ( self , DB , TABLE , CODE , Page ) :
    QQ = f"select `url`,`order`,`page`,`current`,`rows`,`columns`,`title` from {TABLE} where ( `page` = {Page} ) and ( `url` = '{CODE}' ) ;"
    DB . Query ( QQ )
    R  = DB . FetchAll ( )
    return self . ReturnSheetInfo ( R )

  def GetSheetInfos ( self , DB , TABLE , CODE ) :
    R   = [ ]
    QQ  = f"select `order` from {TABLE} where ( `url` = '{CODE}' ) order by `order` asc ;"
    DB  . Query ( QQ )
    IDs = DB . FetchAll ( )
    if ( not IDs ) :
      return R
    elif ( len ( IDs ) <= 0 ) :
      return R
    for order in IDs :
      ORD = order [ 0 ]
      V = self . GetSheetInfoByOrder ( DB , TABLE , CODE , ORD )
      if ( not V ) :
        pass
      else :
        R . append ( V )
    return R

  def SetSheetCurrentByPage ( self , DB , TABLE , CODE , Page , Current ) :
    QQ   = f"update {TABLE} set `current` = {Current} where ( `url` = '{CODE}' ) and ( `page` = {Page} ) ;"
    DB   . Query ( QQ )
    return True

  def GetSheetPages ( self , SHEET ) :
    Pages = [ ]
    if ( not SHEET ) :
      return Pages
    for S in SHEET :
      Pages . append ( int ( S [ "Page" ] ) )
    return Pages

  def GetSheetPageByOrder ( self , SHEET , Order ) :
    if ( not SHEET ) :
      return False
    for S in SHEET :
      if ( int ( S [ "Order" ] ) == int ( Order ) ) :
        return int ( S [ "Page" ] )
    return False

  def GetSheetBriefByOrder ( self , SHEET , Order ) :
    if ( not SHEET ) :
      return False
    for S in SHEET :
      if ( int ( S [ "Order" ] ) == int ( Order ) ) :
        return S
    return False

  def GetSheetBriefByPage ( self , SHEET , Page ) :
    if ( not SHEET ) :
      return False
    for S in SHEET :
      if ( int ( S [ "Page" ] ) == int ( Page ) ) :
        return S
    return False

  def GetSheetValuesByRow ( self , DB , CODE , Page , Row ) :
    QQ = f"select `value` from `google`.`{CODE}` where ( `page` = {Page} ) and ( `row` = {Row} ) order by `column` asc ;"
    return DB . ObtainUuids ( QQ )

  def GetSheetValuesByBrief ( self , DB , Brief ) :
    VALUES =       [        ]
    CODE   = Brief [ "URL"  ]
    Rows   = Brief [ "Rows" ]
    Page   = Brief [ "Page" ]
    for r in range ( 0 , Rows ) :
      X = self . GetSheetValuesByRow ( DB , CODE , Page , r )
      VALUES . append ( X )
    return VALUES

  def isEmptyValues ( self , VALUES ) :
    for V in VALUES :
      W = f"{V}"
      X = W . strip ( )
      if ( len ( X ) > 0 ) :
        return False
    return True

  def StripValues ( self , VALUES ) :
    Z = [ ]
    for V in VALUES :
      X = str ( V )
      Z . append ( X . strip ( ) )
    return Z

  def isSheetUpdated ( self ) :
    current = self . current
    rows    = self . rows
    current = current + 1
    if ( current >= rows ) :
      return False
    return True

  def GetSheetByBrief ( self , DB , brief ) :
    self .                 AssignSheetByBrief    (      brief )
    self . values = self . GetSheetValuesByBrief ( DB , brief )
    return

  def GetSheetsByURL ( self , DB , Title , CODE ) :
    STs = [ ]
    R   = self . GetSheetInfos ( DB , Title , CODE )
    for X in R :
      ST  = Sheet           (        )
      ST  . GetSheetByBrief ( DB , X )
      STs . append          ( ST     )
    return STs

  def toRemittance ( self , VALUES ) :
    if ( self . isEmptyValues ( VALUES ) ) :
      return False
    R        = { }
    cols     = self . columns
    Z        = self . StripValues ( VALUES )
    Register = Z [ 0 ]
    dt       = self . ToDateTime ( Register )
    DateForm = self . ToDateForm ( Register )
    Skype    = Z [ 1 ]
    Email    = Z [ 2 ]
    Phone    = Z [ 3 ]
    Remit    = Z [ 4 ]
    Bank     = Z [ 5 ]
    if ( cols == 9 ) :
      Amount   = ""
      Comment  = Z [ 6 ]
      Others   = Z [ 7 ]
      Extras   = Z [ 8 ]
    else :
      Amount   = Z [ 6 ]
      Comment  = Z [ 7 ]
      Others   = Z [ 8 ]
      Extras   = Z [ 9 ]
    R [ "Date"     ] = dt
    R [ "DateForm" ] = DateForm
    R [ "Register" ] = Register
    R [ "Skype"    ] = Skype
    R [ "Email"    ] = Email
    R [ "Phone"    ] = Phone
    R [ "Remit"    ] = Remit
    R [ "Bank"     ] = Bank
    R [ "Amount"   ] = Amount
    R [ "Comment"  ] = Comment
    R [ "Others"   ] = Others
    R [ "Extras"   ] = Extras
    return R

  def isTimeForm ( self , dt ) :
    LS = dt . split ( " " )
    if ( len ( LS ) != 2 ) :
      return False
    DX = LS [ 0 ]
    DS = DX . split ( "/" )
    if ( len ( DS ) != 3 ) :
      return False
    return True

  def ToTimeForm ( self , dt ) :
    LS = dt . split ( " " )
    DX = LS [ 0 ]
    TD = LS [ 1 ]
    DS = DX . split ( "/" )
    TX = DS [ 2 ] + "/" + DS [ 1 ] + "/" + DS [ 0 ]
    return TX + " " + TD

  def ToDateTime ( self , DF ) :
    LS = DF . split ( " " )
    DS = LS [ 0 ]
    MS = LS [ 1 ]
    TS = LS [ 2 ]
    if ( MS == "下午" ) :
      TL = TS . split ( ":" )
      v  = int ( TL [ 0 ] ) + 12
      if ( v > 23 ) :
        v = 0
      TS = str ( v ) + ":" + TL [ 1 ] + ":" + TL [ 2 ]
      return DS + " " + TS
    return DS + " " + TS

  def ToDateForm ( self , DF ) :
    LS = DF . split ( " " )
    DS = LS [ 0 ]
    MS = LS [ 1 ]
    TS = LS [ 2 ]
    DL = DS . split ( "/" )
    TL = TS . split ( ":" )
    if ( MS == "下午" ) :
      v        = int ( TL [ 0 ] ) + 12
      if ( v > 23 ) :
        v = 0
      TL [ 0 ] = str ( v )
    if ( int ( DL [ 1 ] ) < 10 ) :
      DL [ 1 ] = "0" + str ( int ( DL [ 1 ] ) )
    if ( int ( DL [ 2 ] ) < 10 ) :
      DL [ 2 ] = "0" + str ( int ( DL [ 2 ] ) )
    if ( int ( TL [ 0 ] ) < 10 ) :
      TL [ 0 ] = "0" + str ( int ( TL [ 0 ] ) )
    if ( int ( TL [ 1 ] ) < 10 ) :
      TL [ 1 ] = "0" + str ( int ( TL [ 1 ] ) )
    if ( int ( TL [ 2 ] ) < 10 ) :
      TL [ 2 ] = "0" + str ( int ( TL [ 2 ] ) )
    Date = DL [ 0 ] + "/" + DL [ 1 ] + "/" + DL [ 2 ]
    Time = TL [ 0 ] + ":" + TL [ 1 ] + ":" + TL [ 2 ]
    return Date + " " + Time

  def VerifyOldRemittance ( self , DB , OLD , RECORD ) :
    ID = RECORD [ 0 ]
    QQ = f"update {OLD} set `step` = 1 where `id` = {ID} ;"
    DB . Query ( QQ )
    return

  def IdentifyOldRemittance ( self , DB , OLD , W , RECORDS ) :
    if ( not RECORDS ) :
      return W
    CNT = len ( RECORDS )
    if ( CNT <= 0 ) :
      return W
    if ( CNT == 1 ) :
      W [ "Actions"     ] = RECORDS [ 0 ] [ 1 ]
      W [ "Transaction" ] = RECORDS [ 0 ] [ 2 ]
      self . VerifyOldRemittance ( DB , OLD , RECORDS [ 0 ] )
      return W
    W [ "Duplicated" ] = 1
    ACTIONS     = RECORDS [ 0 ] [ 1 ]
    TRANSACTION = RECORDS [ 0 ] [ 2 ]
    SAME        = True
    for r in RECORDS :
      if ( ACTIONS     != r [ 1 ] ) :
        SAME = False
      if ( TRANSACTION != r [ 2 ] ) :
        SAME = False
      self . VerifyOldRemittance ( DB , OLD , r )
    if ( SAME ) :
      W [ "Actions"     ] = ACTIONS
      W [ "Transaction" ] = TRANSACTION
      return W
    return W

  def UpdateOldRemittance ( self , DB , OLD , REMIT , W ) :
    SDT    = StarDate         ( )
    Record = SDT . fromFormat ( W [ "Date" ] , "Asia/Taipei" )
    W [ "Record"      ] = Record
    W [ "Actions"     ] = "0"
    W [ "Transaction" ] = "0"
    W [ "Duplicated"  ] = 0
    DT                  = W [ "Date"   ]
    Skype               = W [ "Skype"  ]
    Email               = W [ "Email"  ]
    Phone               = W [ "Phone"  ]
    Remit               = W [ "Remit"  ]
    Bank                = W [ "Bank"   ]
    Amount              = W [ "Amount" ]
    QQ = f"""select `id`,`actions`,`transaction` from {OLD}
             where ( `dt` = %s )
             and ( `record` = %s )
             and ( `skype` like %s )
             and ( `email` like %s )
             and ( `phone` like %s )
             and ( `remit` like %s )
             and ( `bank` like %s )
             and ( `amount` like %s )
             order by `id` asc ;"""
    VAL = ( DT , Record , f"%{Skype}%" , f"%{Email}%" , f"%{Phone}%" , f"%{Remit}%" , f"%{Bank}%" , f"%{Amount}%" )
    DB . QueryValues ( QQ , VAL )
    RECORDS = DB . FetchAll ( )
    return self . IdentifyOldRemittance ( DB , OLD , W , RECORDS )

  def isRemittanceExists ( self , DB , REMIT , W ) :
    ROW  = W [ "Row"   ]
    PAGE = W [ "Page"  ]
    QQ   = f"select `id` from {REMIT} where ( `row` = {ROW} ) and ( `page` = {PAGE} ) ;"
    DB   . Query ( QQ )
    R    = DB . FetchAll ( )
    if ( not R ) :
      return False
    if ( len ( R ) <= 0 ) :
      return False
    if ( len ( R ) >  1 ) :
      return False
    return True

  def UpdateRemittanceItem ( self , DB , REMIT , W ) :
    Actions     = W [ "Actions"     ]
    Transaction = W [ "Transaction" ]
    Page        = W [ "Page"        ]
    Order       = W [ "Order"       ]
    Row         = W [ "Row"         ]
    Duplicated  = W [ "Duplicated"  ]
    Record      = W [ "Record"      ]
    DT          = W [ "Date"        ]
    DateForm    = W [ "DateForm"    ]
    Register    = W [ "Register"    ]
    Skype       = W [ "Skype"       ]
    Email       = W [ "Email"       ]
    Phone       = W [ "Phone"       ]
    Remit       = W [ "Remit"       ]
    Bank        = W [ "Bank"        ]
    Amount      = W [ "Amount"      ]
    Comment     = W [ "Comment"     ]
    Others      = W [ "Others"      ]
    Extras      = W [ "Extras"      ]
    QQ  = f"""update {REMIT} set
              `actions` = %s ,
              `transaction` = %s ,
              `order` = %s ,
              `duplicated` = %s ,
              `record` = %s ,
              `dt` = %s ,
              `dateform` = %s ,
              `register` = %s ,
              `skype` = %s ,
              `email` = %s ,
              `phone` = %s ,
              `remit` = %s ,
              `bank` = %s ,
              `amount` = %s ,
              `comment` = %s ,
              `others` = %s ,
              `extras` = %s
              where ( `page` = %s ) and ( `row` = %s ) ;"""
    VAL = ( Actions , Transaction , Order    , Duplicated , Record  ,
            DT      , DateForm    , Register , Skype      , Email   ,
            Phone   , Remit       , Bank     , Amount     , Comment ,
            Others  , Extras      , Page     , Row                  )
    DB . QueryValues ( QQ , VAL )
    return True

  def AppendRemittanceItem ( self , DB , REMIT , W ) :
    Actions     = W [ "Actions"     ]
    Transaction = W [ "Transaction" ]
    Page        = W [ "Page"        ]
    Order       = W [ "Order"       ]
    Row         = W [ "Row"         ]
    Duplicated  = W [ "Duplicated"  ]
    Record      = W [ "Record"      ]
    DT          = W [ "Date"        ]
    DateForm    = W [ "DateForm"    ]
    Register    = W [ "Register"    ]
    Skype       = W [ "Skype"       ]
    Email       = W [ "Email"       ]
    Phone       = W [ "Phone"       ]
    Remit       = W [ "Remit"       ]
    Bank        = W [ "Bank"        ]
    Amount      = W [ "Amount"      ]
    Comment     = W [ "Comment"     ]
    Others      = W [ "Others"      ]
    Extras      = W [ "Extras"      ]
    QQ  = f"""insert into {REMIT}
              ( `actions`,`transaction`,`page`,`order`,`row`,
                `duplicated`,`record`,`dt`,`dateform`,`register`,
                `skype`,`email`,`phone`,`remit`,`bank`,
                `amount`,`comment`,`others`,`extras`
              ) values (
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s ) ;"""
    VAL = ( Actions    , Transaction , Page   , Order    , Row      ,
            Duplicated , Record      , DT     , DateForm , Register ,
            Skype      , Email       , Phone  , Remit    , Bank     ,
            Amount     , Comment     , Others , Extras              )
    DB . QueryValues ( QQ , VAL )
    return True

  def AssureRemittance ( self , DB , REMIT , W ) :
    if ( not W ) :
      return False
    if ( self . isRemittanceExists ( DB , REMIT , W ) ) :
      self . UpdateRemittanceItem ( DB , REMIT , W )
    else :
      self . AppendRemittanceItem ( DB , REMIT , W )
    return True

  def Registration2019 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE . strip ( )
    REFERRAL     = VALUES [  6 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  7 ]
    SECTION      = SECTION . strip ( )
    SLOTS        = VALUES [  8 ]
    BANK         = VALUES [ 10 ]
    STARTDATE    = VALUES [ 11 ]
    HOURS        = VALUES [ 12 ]
    OTHERS       = VALUES [ 13 ]
    COMMENT      = VALUES [ 15 ]
    AGE          = VALUES [ 19 ]
    COMPANY      = VALUES [ 20 ]
    SUBSTITUTE   = VALUES [ 21 ]
    EV           = VALUES [ 22 ]
    DOC          = VALUES [ 23 ]
    RECEPTIONIST = VALUES [ 24 ]
    CARETAKER    = VALUES [ 25 ]
    E0001        = VALUES [ 26 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = AGE
    R [ "Company"      ] = COMPANY
    R [ "Substitute"   ] = SUBSTITUTE
    R [ "Append"       ] = ""
    R [ "EV"           ] = EV
    R [ "Document"     ] = DOC
    R [ "Receptionist" ] = RECEPTIONIST
    R [ "CareTaker"    ] = CARETAKER
    ##########################################################################
    R [ "E0001"        ] = E0001
    R [ "E0002"        ] = ""
    R [ "E0003"        ] = ""
    R [ "E0004"        ] = ""
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2018 ( self , VALs , row ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT             = self . ToTimeForm ( LOGTIME )
    NAME           = VALUES [  1 ]
    NAME           = NAME . strip ( )
    SKYPE          = VALUES [  2 ]
    SKYPE          = SKYPE . strip ( )
    EMAIL          = VALUES [  3 ]
    EMAIL          = EMAIL . strip ( )
    PHONE          = VALUES [  4 ]
    PHONE          = PHONE . strip ( )
    if ( row > 785 ) :
      REFERRAL     = VALUES [ 6 ]
      REFERRAL     = REFERRAL . strip ( )
      SECTION      = VALUES [ 7 ]
      SECTION      = SECTION . strip ( )
      SLOTS        = VALUES [ 8 ]
      BANK         = VALUES [ 10 ]
      STARTDATE    = VALUES [ 11 ]
      HOURS        = VALUES [ 12 ]
      OTHERS       = VALUES [ 13 ]
      COMMENT      = VALUES [ 15 ]
      AGE          = VALUES [ 19 ]
      COMPANY      = VALUES [ 20 ]
      APPEND       = VALUES [ 26 ]
      EV           = VALUES [ 22 ]
      DOC          = VALUES [ 23 ]
      RECEPTIONIST = VALUES [ 24 ]
      CARETAKER    = VALUES [ 25 ]
      E0001        = ""
    else :
      REFERRAL     = VALUES [ 8 ]
      REFERRAL     = REFERRAL . strip ( )
      SECTION      = VALUES [ 9 ]
      SECTION      = SECTION . strip ( )
      SLOTS        = VALUES [ 10 ]
      BANK         = VALUES [ 12 ]
      STARTDATE    = VALUES [ 13 ]
      HOURS        = VALUES [ 14 ]
      OTHERS       = VALUES [ 15 ]
      COMMENT      = VALUES [ 17 ]
      AGE          = VALUES [ 21 ]
      COMPANY      = VALUES [ 22 ]
      APPEND       = VALUES [ 23 ]
      EV           = VALUES [ 24 ]
      DOC          = VALUES [ 25 ]
      RECEPTIONIST = VALUES [ 26 ]
      CARETAKER    = VALUES [ 27 ]
      E0001        = VALUES [ 28 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = AGE
    R [ "Company"      ] = COMPANY
    R [ "Substitute"   ] = ""
    R [ "Append"       ] = APPEND
    R [ "EV"           ] = EV
    R [ "Document"     ] = DOC
    R [ "Receptionist" ] = RECEPTIONIST
    R [ "CareTaker"    ] = CARETAKER
    ##########################################################################
    R [ "E0001"        ] = E0001
    R [ "E0002"        ] = ""
    R [ "E0003"        ] = ""
    R [ "E0004"        ] = ""
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2017 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE . strip ( )
    REFERRAL     = VALUES [  8 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  9 ]
    SECTION      = SECTION . strip ( )
    SLOTS        = VALUES [ 10 ]
    BANK         = VALUES [ 12 ]
    STARTDATE    = VALUES [ 13 ]
    HOURS        = VALUES [ 14 ]
    OTHERS       = VALUES [ 15 ]
    COMMENT      = VALUES [ 17 ]
    AGE          = VALUES [ 21 ]
    COMPANY      = VALUES [ 22 ]
    SUBSTITUTE   = ""
    APPEND       = VALUES [ 23 ]
    EV           = VALUES [ 24 ]
    DOC          = VALUES [ 25 ]
    RECEPTIONIST = VALUES [ 26 ]
    CARETAKER    = VALUES [ 27 ]
    E0001        = VALUES [ 28 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = AGE
    R [ "Company"      ] = COMPANY
    R [ "Substitute"   ] = SUBSTITUTE
    R [ "Append"       ] = APPEND
    R [ "EV"           ] = EV
    R [ "Document"     ] = DOC
    R [ "Receptionist" ] = RECEPTIONIST
    R [ "CareTaker"    ] = CARETAKER
    ##########################################################################
    R [ "E0001"        ] = E0001
    R [ "E0002"        ] = ""
    R [ "E0003"        ] = ""
    R [ "E0004"        ] = ""
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2016 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE . strip ( )
    REFERRAL     = VALUES [  5 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  6 ]
    SECTION      = SECTION . strip ( )
    SLOTS        = VALUES [  7 ]
    BANK         = VALUES [  9 ]
    STARTDATE    = VALUES [ 10 ]
    HOURS        = VALUES [ 11 ]
    OTHERS       = VALUES [ 12 ]
    COMMENT      = VALUES [ 14 ]
    AGE          = VALUES [ 18 ]
    COMPANY      = VALUES [ 19 ]
    SUBSTITUTE   = ""
    APPEND       = VALUES [ 20 ]
    EV           = VALUES [ 21 ]
    DOC          = VALUES [ 22 ]
    RECEPTIONIST = VALUES [ 23 ]
    CARETAKER    = VALUES [ 24 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = AGE
    R [ "Company"      ] = COMPANY
    R [ "Substitute"   ] = SUBSTITUTE
    R [ "Append"       ] = APPEND
    R [ "EV"           ] = EV
    R [ "Document"     ] = DOC
    R [ "Receptionist" ] = RECEPTIONIST
    R [ "CareTaker"    ] = CARETAKER
    ##########################################################################
    R [ "E0001"        ] = ""
    R [ "E0002"        ] = ""
    R [ "E0003"        ] = ""
    R [ "E0004"        ] = ""
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2015 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE . strip ( )
    REFERRAL     = VALUES [  8 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  9 ]
    SECTION      = SECTION . strip ( )
    SLOTS        = VALUES [ 10 ]
    BANK         = VALUES [ 12 ]
    STARTDATE    = VALUES [ 13 ]
    HOURS        = VALUES [ 14 ]
    OTHERS       = VALUES [ 15 ]
    COMMENT      = VALUES [ 17 ]
    AGE          = VALUES [ 21 ]
    COMPANY      = VALUES [ 22 ]
    SUBSTITUTE   = ""
    EV           = ""
    DOC          = VALUES [ 25 ]
    RECEPTIONIST = ""
    CARETAKER    = ""
    E0001        = VALUES [ 24 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = AGE
    R [ "Company"      ] = COMPANY
    R [ "Substitute"   ] = SUBSTITUTE
    R [ "Append"       ] = ""
    R [ "EV"           ] = EV
    R [ "Document"     ] = DOC
    R [ "Receptionist" ] = RECEPTIONIST
    R [ "CareTaker"    ] = CARETAKER
    ##########################################################################
    R [ "E0001"        ] = E0001
    R [ "E0002"        ] = ""
    R [ "E0003"        ] = ""
    R [ "E0004"        ] = ""
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2014 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE . strip ( )
    REFERRAL     = VALUES [  5 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  6 ]
    SECTION      = SECTION . strip ( )
    SLOTS        = VALUES [  7 ]
    BANK         = VALUES [  9 ]
    STARTDATE    = VALUES [ 10 ]
    HOURS        = VALUES [ 11 ]
    OTHERS       = VALUES [ 12 ]
    COMMENT      = VALUES [ 14 ]
    AGE          = VALUES [ 18 ]
    COMPANY      = VALUES [ 19 ]
    SUBSTITUTE   = ""
    EV           = ""
    DOC          = VALUES [ 22 ]
    RECEPTIONIST = ""
    CARETAKER    = ""
    E0001        = VALUES [ 21 ]
    E0002        = VALUES [ 15 ]
    E0003        = VALUES [ 17 ]
    E0004        = VALUES [ 13 ]
    E0005        = VALUES [ 23 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = AGE
    R [ "Company"      ] = COMPANY
    R [ "Substitute"   ] = ""
    R [ "Append"       ] = ""
    R [ "EV"           ] = ""
    R [ "Document"     ] = DOC
    R [ "Receptionist" ] = ""
    R [ "CareTaker"    ] = ""
    ##########################################################################
    R [ "E0001"        ] = E0001
    R [ "E0002"        ] = E0002
    R [ "E0003"        ] = E0003
    R [ "E0004"        ] = E0004
    R [ "E0005"        ] = E0005
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2013 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE . strip ( )
    REFERRAL     = VALUES [  5 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  6 ]
    SECTION      = SECTION . strip ( )
    SLOTS        = VALUES [  7 ]
    BANK         = VALUES [  9 ]
    STARTDATE    = VALUES [ 10 ]
    HOURS        = VALUES [ 11 ]
    OTHERS       = VALUES [ 12 ]
    COMMENT      = VALUES [ 14 ]
    E0001        = VALUES [ 17 ]
    E0003        = VALUES [ 15 ]
    E0004        = VALUES [ 13 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = ""
    R [ "Company"      ] = ""
    R [ "Substitute"   ] = ""
    R [ "Append"       ] = ""
    R [ "EV"           ] = ""
    R [ "Document"     ] = ""
    R [ "Receptionist" ] = ""
    R [ "CareTaker"    ] = ""
    ##########################################################################
    R [ "E0001"        ] = E0001
    R [ "E0002"        ] = ""
    R [ "E0003"        ] = E0003
    R [ "E0004"        ] = E0004
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2012 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE . strip ( )
    REFERRAL     = VALUES [  8 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  9 ]
    SECTION      = SECTION . strip ( )
    SLOTS        = VALUES [ 10 ]
    BANK         = VALUES [ 12 ]
    STARTDATE    = VALUES [ 13 ]
    HOURS        = VALUES [ 14 ]
    OTHERS       = VALUES [ 15 ]
    COMMENT      = VALUES [ 16 ]
    E0002        = VALUES [ 17 ]
    E0003        = VALUES [ 18 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = ""
    R [ "Company"      ] = ""
    R [ "Substitute"   ] = ""
    R [ "Append"       ] = ""
    R [ "EV"           ] = ""
    R [ "Document"     ] = ""
    R [ "Receptionist" ] = ""
    R [ "CareTaker"    ] = ""
    ##########################################################################
    R [ "E0001"        ] = ""
    R [ "E0002"        ] = E0002
    R [ "E0003"        ] = E0003
    R [ "E0004"        ] = ""
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2011 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE . strip ( )
    REFERRAL     = VALUES [  8 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  9 ]
    SECTION      = SECTION . strip ( )
    SLOTS        = VALUES [ 10 ]
    BANK         = VALUES [ 12 ]
    STARTDATE    = VALUES [ 13 ]
    HOURS        = VALUES [ 14 ]
    OTHERS       = VALUES [ 15 ]
    COMMENT      = VALUES [ 16 ]
    EV           = VALUES [ 18 ]
    DOC          = VALUES [ 19 ]
    E0001        = VALUES [ 17 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = HOURS
    R [ "Others"       ] = OTHERS
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = ""
    R [ "Company"      ] = ""
    R [ "Substitute"   ] = ""
    R [ "Append"       ] = ""
    R [ "EV"           ] = EV
    R [ "Document"     ] = DOC
    R [ "Receptionist" ] = ""
    R [ "CareTaker"    ] = ""
    ##########################################################################
    R [ "E0001"        ] = E0001
    R [ "E0002"        ] = ""
    R [ "E0003"        ] = ""
    R [ "E0004"        ] = ""
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def Registration2010 ( self , VALs ) :
    ##########################################################################
    R            = { }
    ##########################################################################
    cols         = self . columns
    VALUES       = self . StripValues ( VALs )
    Page         = self . id
    ##########################################################################
    LOGTIME      = VALUES [  0 ]
    LOGTIME      = LOGTIME . strip ( )
    if ( not self . isTimeForm ( LOGTIME ) ) :
      return False
    DT           = self . ToTimeForm ( LOGTIME )
    NAME         = VALUES [  1 ]
    NAME         = NAME     . strip ( )
    SKYPE        = VALUES [  2 ]
    SKYPE        = SKYPE    . strip ( )
    EMAIL        = VALUES [  3 ]
    EMAIL        = EMAIL    . strip ( )
    PHONE        = VALUES [  4 ]
    PHONE        = PHONE    . strip ( )
    REFERRAL     = VALUES [  8 ]
    REFERRAL     = REFERRAL . strip ( )
    SECTION      = VALUES [  9 ]
    SECTION      = SECTION  . strip ( )
    SLOTS        = VALUES [ 10 ]
    BANK         = VALUES [ 12 ]
    STARTDATE    = VALUES [ 13 ]
    COMMENT      = VALUES [ 15 ]
    ##########################################################################
    R [ "DT"           ] = DT
    R [ "LogTime"      ] = LOGTIME
    R [ "Name"         ] = NAME
    R [ "Skype"        ] = SKYPE
    R [ "EMail"        ] = EMAIL
    R [ "Phone"        ] = PHONE
    R [ "Referral"     ] = REFERRAL
    R [ "Section"      ] = SECTION
    R [ "Slots"        ] = SLOTS
    R [ "Bank"         ] = BANK
    R [ "StartDate"    ] = STARTDATE
    R [ "Hours"        ] = ""
    R [ "Others"       ] = ""
    R [ "Comment"      ] = COMMENT
    R [ "Age"          ] = ""
    R [ "Company"      ] = ""
    R [ "Substitute"   ] = ""
    R [ "Append"       ] = ""
    R [ "EV"           ] = ""
    R [ "Document"     ] = ""
    R [ "Receptionist" ] = ""
    R [ "CareTaker"    ] = ""
    ##########################################################################
    R [ "E0001"        ] = ""
    R [ "E0002"        ] = ""
    R [ "E0003"        ] = ""
    R [ "E0004"        ] = ""
    R [ "E0005"        ] = ""
    R [ "E0006"        ] = ""
    R [ "E0007"        ] = ""
    R [ "E0008"        ] = ""
    R [ "E0009"        ] = ""
    ##########################################################################
    return R

  def toRegistration ( self , VALUES , row ) :
    if ( self . isEmptyValues ( VALUES ) ) :
      return False
    R    = { }
    if   ( "Sheet1" in self . title ) :
      R  =  self . Registration2019 ( VALUES )
    elif ( "2019"   in self . title ) :
      R  =  self . Registration2019 ( VALUES )
    elif ( "2018"   in self . title ) :
      R  =  self . Registration2018 ( VALUES , row )
    elif ( "2017"   in self . title ) :
      R  =  self . Registration2017 ( VALUES )
    elif ( "2016"   in self . title ) :
      R  =  self . Registration2016 ( VALUES )
    elif ( "2015"   in self . title ) :
      R  =  self . Registration2015 ( VALUES )
    elif ( "2014"   in self . title ) :
      R  =  self . Registration2014 ( VALUES )
    elif ( "2013"   in self . title ) :
      R  =  self . Registration2013 ( VALUES )
    elif ( "2012"   in self . title ) :
      R  =  self . Registration2012 ( VALUES )
    elif ( "2011"   in self . title ) :
      R  =  self . Registration2011 ( VALUES )
    elif ( "2010"   in self . title ) :
      R  =  self . Registration2010 ( VALUES )
    return R

  def VerifyOldRegistration ( self , DB , OLD , RECORD ) :
    ID = RECORD [ 0 ]
    QQ = f"update {OLD} set `applied` = 1 where `id` = {ID} ;"
    DB . Query ( QQ )
    return

  def IdentifyOldRegistration ( self , DB , OLD , W , RECORDS ) :
    if ( not RECORDS ) :
      return W
    CNT = len ( RECORDS )
    if ( CNT <= 0 ) :
      return W
    if ( CNT == 1 ) :
      W [ "Actions" ] = RECORDS [ 0 ] [ 1 ]
      self . VerifyOldRegistration ( DB , OLD , RECORDS [ 0 ] )
      return W
    W [ "Duplicated" ] = 1
    ACTIONS = RECORDS [ 0 ] [ 1 ]
    SAME    = True
    for r in RECORDS :
      if ( ACTIONS     != r [ 1 ] ) :
        SAME = False
      self . VerifyOldRegistration ( DB , OLD , r )
    if ( SAME ) :
      W [ "Actions" ] = ACTIONS
      return W
    return W

  def UpdateOldRegistration ( self , DB , OLD , REG , W ) :
    SDT    = StarDate         ( )
    Record = SDT . fromFormat ( W [ "DT" ] , "Asia/Taipei" )
    W [ "Record"      ] = Record
    W [ "Actions"     ] = "0"
    W [ "Duplicated"  ] = 0
    DT                  = W [ "DT"     ]
    Skype               = W [ "Skype"  ]
    Email               = W [ "EMail"  ]
    Phone               = W [ "Phone"  ]
    QQ = f"""select `id`,`actions` from {OLD}
             where ( `dt` = %s )
             and ( `skype` like %s )
             and ( `email` like %s )
             and ( `phone` like %s )
             order by `id` asc ;"""
    VAL = ( DT , f"%{Skype}%" , f"%{Email}%" , f"%{Phone}%" )
    DB . QueryValues ( QQ , VAL )
    RECORDS = DB . FetchAll ( )
    return self . IdentifyOldRegistration ( DB , OLD , W , RECORDS )

  def isRegistrationExists ( self , DB , REGISTER , W ) :
    ROW  = W [ "Row"   ]
    PAGE = W [ "Page"  ]
    QQ   = f"select `id` from {REGISTER} where ( `row` = {ROW} ) and ( `page` = {PAGE} ) ;"
    DB   . Query ( QQ )
    R    = DB . FetchAll ( )
    if ( not R ) :
      return False
    if ( len ( R ) <= 0 ) :
      return False
    if ( len ( R ) >  1 ) :
      return False
    return True

  def UpdateRegistrationItem ( self , DB , REGISTER , W ) :
    ##########################################################################
    Actions      = W [ "Actions"      ]
    Page         = W [ "Page"         ]
    Order        = W [ "Order"        ]
    Row          = W [ "Row"          ]
    Duplicated   = W [ "Duplicated"   ]
    Record       = W [ "Record"       ]
    DT           = W [ "DT"           ]
    LogTime      = W [ "LogTime"      ]
    Name         = W [ "Name"         ]
    Skype        = W [ "Skype"        ]
    Email        = W [ "EMail"        ]
    Phone        = W [ "Phone"        ]
    Referral     = W [ "Referral"     ]
    Section      = W [ "Section"      ]
    Slots        = W [ "Slots"        ]
    Bank         = W [ "Bank"         ]
    StartDate    = W [ "StartDate"    ]
    Hours        = W [ "Hours"        ]
    Others       = W [ "Others"       ]
    Comment      = W [ "Comment"      ]
    Age          = W [ "Age"          ]
    Company      = W [ "Company"      ]
    Substitute   = W [ "Substitute"   ]
    Append       = W [ "Append"       ]
    EV           = W [ "EV"           ]
    Document     = W [ "Document"     ]
    Receptionist = W [ "Receptionist" ]
    CareTaker    = W [ "CareTaker"    ]
    E0001        = W [ "E0001"        ]
    E0002        = W [ "E0002"        ]
    E0003        = W [ "E0003"        ]
    E0004        = W [ "E0004"        ]
    E0005        = W [ "E0005"        ]
    E0006        = W [ "E0006"        ]
    E0007        = W [ "E0007"        ]
    E0008        = W [ "E0008"        ]
    E0009        = W [ "E0009"        ]
    ##########################################################################
    QQ  = f"""update {REGISTER} set
              `actions` = %s ,
              `order` = %s ,
              `duplicate` = %s ,
              `record` = %s ,
              `dt` = %s ,
              `logtime` = %s ,
              `name` = %s ,
              `skype` = %s ,
              `email` = %s ,
              `phone` = %s ,
              `referral` = %s ,
              `section` = %s ,
              `slots` = %s ,
              `bank` = %s ,
              `startdate` = %s ,
              `hours` = %s ,
              `others` = %s ,
              `comment` = %s ,
              `age` = %s ,
              `company` = %s ,
              `substitute` = %s ,
              `append` = %s ,
              `ev` = %s ,
              `document` = %s ,
              `receptionist` = %s ,
              `caretaker` = %s ,
              `e0001` = %s ,
              `e0002` = %s ,
              `e0003` = %s ,
              `e0004` = %s ,
              `e0005` = %s ,
              `e0006` = %s ,
              `e0007` = %s ,
              `e0008` = %s ,
              `e0009` = %s
              where ( `page` = %s ) and ( `row` = %s ) ;"""
    VAL = ( Actions    , Order   , Duplicated , Record   , DT           ,
            LogTime    , Name    , Skype      , Email    , Phone        ,
            Referral   , Section , Slots      , Bank     , StartDate    ,
            Hours      , Others  , Comment    , Age      , Company      ,
            Substitute , Append  , EV         , Document , Receptionist ,
            CareTaker  , E0001   , E0002      , E0003    , E0004        ,
            E0005      , E0006   , E0007      , E0008    , E0009        ,
            Page       , Row                                            )
    DB . QueryValues ( QQ , VAL )
    ##########################################################################
    return True

  def AppendRegistrationItem ( self , DB , REGISTER , W ) :
    ##########################################################################
    Actions      = W [ "Actions"      ]
    Page         = W [ "Page"         ]
    Order        = W [ "Order"        ]
    Row          = W [ "Row"          ]
    Duplicated   = W [ "Duplicated"   ]
    Record       = W [ "Record"       ]
    DT           = W [ "DT"           ]
    LogTime      = W [ "LogTime"      ]
    Name         = W [ "Name"         ]
    Skype        = W [ "Skype"        ]
    Email        = W [ "EMail"        ]
    Phone        = W [ "Phone"        ]
    Referral     = W [ "Referral"     ]
    Section      = W [ "Section"      ]
    Slots        = W [ "Slots"        ]
    Bank         = W [ "Bank"         ]
    StartDate    = W [ "StartDate"    ]
    Hours        = W [ "Hours"        ]
    Others       = W [ "Others"       ]
    Comment      = W [ "Comment"      ]
    Age          = W [ "Age"          ]
    Company      = W [ "Company"      ]
    Substitute   = W [ "Substitute"   ]
    Append       = W [ "Append"       ]
    EV           = W [ "EV"           ]
    Document     = W [ "Document"     ]
    Receptionist = W [ "Receptionist" ]
    CareTaker    = W [ "CareTaker"    ]
    E0001        = W [ "E0001"        ]
    E0002        = W [ "E0002"        ]
    E0003        = W [ "E0003"        ]
    E0004        = W [ "E0004"        ]
    E0005        = W [ "E0005"        ]
    E0006        = W [ "E0006"        ]
    E0007        = W [ "E0007"        ]
    E0008        = W [ "E0008"        ]
    E0009        = W [ "E0009"        ]
    ##########################################################################
    QQ  = f"""insert into {REGISTER}
              ( `actions`,`page`,`order`,`row`,`duplicate`,
                `record`,`dt`,`logtime`,`name`,`skype`,
                `email`,`phone`,`referral`,`section`,`slots`,
                `bank`,`startdate`,`hours`,`others`,`comment`,
                `age`,`company`,`substitute`,`append`,`ev`,
                `document`,`receptionist`,`caretaker`,`e0001`,`e0002`,
                `e0003`,`e0004`,`e0005`,`e0006`,`e0007`,
                `e0008`,`e0009`
              ) values (
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s ) ;"""
    VAL = ( Actions      , Page         , Order      , Row     , Duplicated ,
            Record       , DT           , LogTime    , Name    , Skype      ,
            Email        , Phone        , Referral   , Section , Slots      ,
            Bank         , StartDate    , Hours      , Others  , Comment    ,
            Age          , Company      , Substitute , Append  , EV         ,
            Document     , Receptionist , CareTaker  , E0001   , E0002      ,
            E0003        , E0004        , E0005      , E0006   , E0007      ,
            E0008        , E0009                                            )
    DB . QueryValues ( QQ , VAL )
    ##########################################################################
    return True

  def AssureRegistration ( self , DB , REGISTER , W ) :
    if ( not W ) :
      return False
    if ( self . isRegistrationExists ( DB , REGISTER , W ) ) :
      self . UpdateRegistrationItem ( DB , REGISTER , W )
    else :
      self . AppendRegistrationItem ( DB , REGISTER , W )
    return True

  def moneyToNumber ( self , DIGITS ) :
    D = DIGITS . replace ( "," , "" )
    if ( len ( D ) <= 0 ) :
      return 0
    if ( " " in D ) :
      S = D . split ( )
      if ( len ( S ) > 0 ) :
        D = S [ 0 ]
    try :
      return int ( D )
    except ValueError :
      return 0
    return 0

  def BalanceTie  ( self , VALUES ) :
    DS          = VALUES [ 0 ]
    if ( "/" not in DS ) :
      return False
    DS = DS . strip ( )
    LS = DS . split ( "/" )
    if ( len ( LS ) != 3 ) :
      return False
    DD = int ( LS [ 0 ] )
    YY = int ( LS [ 2 ] )
    if ( DD > 100 ) :
      DT = LS [ 0 ] + "/" + LS [ 1 ] + "/" + LS [ 2 ]
    else :
      DT = LS [ 2 ] + "/" + LS [ 0 ] + "/" + LS [ 1 ]
    TRADEDATE   = DT
    LOGDATE     = VALUES [ 0 ]
    LOGDATE     = LOGDATE . strip ( )
    METHOD      = VALUES [ 1 ]
    METHOD      = METHOD . strip ( )
    CURRENCY    = VALUES [ 2 ]
    CURRENCY    = CURRENCY . strip ( )
    EXPENDITURE = VALUES [ 3 ]
    EXPENDITURE = EXPENDITURE . strip ( )
    DEPOSIT     = VALUES [ 4 ]
    DEPOSIT     = DEPOSIT . strip ( )
    BALANCE     = ""
    FROM        = VALUES [ 5 ]
    FROM        = FROM . strip ( )
    ACCOUNT     = VALUES [ 6 ]
    ACCOUNT     = ACCOUNT . strip ( )
    NOTE        = ""
    CONTACT     = VALUES [ 7 ]
    CONTACT     = CONTACT . strip ( )
    EXTRAS      = ""
    W           = { }
    W [ "TradeDate"   ] = TRADEDATE
    W [ "Actions"     ] = 0
    W [ "LogDate"     ] = LOGDATE
    W [ "Method"      ] = METHOD
    W [ "Currency"    ] = CURRENCY
    W [ "Expenditure" ] = EXPENDITURE
    W [ "Deposit"     ] = DEPOSIT
    W [ "Balance"     ] = BALANCE
    W [ "From"        ] = FROM
    W [ "Account"     ] = ACCOUNT
    W [ "Note"        ] = NOTE
    W [ "Contact"     ] = CONTACT
    W [ "Extras"      ] = EXTRAS
    return W

  def BalanceCut  ( self , VALUES ) :
    DS          = VALUES [ 0 ]
    if ( "/" not in DS ) :
      return False
    DS = DS . strip ( )
    LS = DS . split ( "/" )
    if ( len ( LS ) != 3 ) :
      return False
    DD = int ( LS [ 0 ] )
    YY = int ( LS [ 2 ] )
    if ( DD > 100 ) :
      DT = LS [ 0 ] + "/" + LS [ 1 ] + "/" + LS [ 2 ]
    else :
      DT = LS [ 2 ] + "/" + LS [ 0 ] + "/" + LS [ 1 ]
    TRADEDATE   = DT
    LOGDATE     = VALUES [ 0 ]
    LOGDATE     = LOGDATE . strip ( )
    METHOD      = VALUES [ 1 ]
    METHOD      = METHOD . strip ( )
    CURRENCY    = VALUES [ 2 ]
    CURRENCY    = CURRENCY . strip ( )
    EXPENDITURE = VALUES [ 3 ]
    EXPENDITURE = EXPENDITURE . strip ( )
    DEPOSIT     = VALUES [ 4 ]
    DEPOSIT     = DEPOSIT . strip ( )
    BALANCE     = VALUES [ 5 ]
    BALANCE     = BALANCE . strip ( )
    FROM        = VALUES [ 6 ]
    FROM        = FROM . strip ( )
    ACCOUNT     = VALUES [ 7 ]
    ACCOUNT     = ACCOUNT . strip ( )
    NOTE        = ""
    CONTACT     = VALUES [ 8 ]
    CONTACT     = CONTACT . strip ( )
    EXTRAS      = ""
    W           = { }
    W [ "TradeDate"   ] = TRADEDATE
    W [ "Actions"     ] = 0
    W [ "LogDate"     ] = LOGDATE
    W [ "Method"      ] = METHOD
    W [ "Currency"    ] = CURRENCY
    W [ "Expenditure" ] = EXPENDITURE
    W [ "Deposit"     ] = DEPOSIT
    W [ "Balance"     ] = BALANCE
    W [ "From"        ] = FROM
    W [ "Account"     ] = ACCOUNT
    W [ "Note"        ] = NOTE
    W [ "Contact"     ] = CONTACT
    W [ "Extras"      ] = EXTRAS
    return W

  def Balance2020 ( self , VALUES ) :
    DS          = str ( VALUES [ 0 ] )
    if ( "/" not in DS ) :
      return False
    DS = DS . strip ( )
    LS = DS . split ( "/" )
    if ( len ( LS ) != 3 ) :
      return False
    DD = int ( LS [ 0 ] )
    YY = int ( LS [ 2 ] )
    if ( DD > 100 ) :
      DT = LS [ 0 ] + "/" + LS [ 1 ] + "/" + LS [ 2 ]
    else :
      DT = LS [ 2 ] + "/" + LS [ 0 ] + "/" + LS [ 1 ]
    TRADEDATE   = DT
    LOGDATE     = str ( VALUES [ 0 ] )
    LOGDATE     = LOGDATE . strip ( )
    METHOD      = str ( VALUES [ 1 ] )
    METHOD      = METHOD . strip ( )
    CURRENCY    = str ( VALUES [ 2 ] )
    CURRENCY    = CURRENCY . strip ( )
    EXPENDITURE = str ( VALUES [ 3 ] )
    EXPENDITURE = EXPENDITURE . strip ( )
    OUTLAY      = self . moneyToNumber ( EXPENDITURE )
    DEPOSIT     = str ( VALUES [ 4 ] )
    DEPOSIT     = DEPOSIT . strip ( )
    REVENUE     = self . moneyToNumber ( DEPOSIT )
    BALANCE     = str ( VALUES [ 5 ] )
    BALANCE     = BALANCE . strip ( )
    FROM        = str ( VALUES [ 6 ] )
    FROM        = FROM . strip ( )
    ACCOUNT     = str ( VALUES [ 7 ] )
    ACCOUNT     = ACCOUNT . strip ( )
    NOTE        = str ( VALUES [ 8 ] )
    NOTE        = NOTE . strip ( )
    CONTACT     = str ( VALUES [ 9 ] )
    CONTACT     = CONTACT . strip ( )
    EXTRAS      = ""
    W           = { }
    W [ "TradeDate"   ] = TRADEDATE
    W [ "Actions"     ] = 0
    W [ "LogDate"     ] = LOGDATE
    W [ "Method"      ] = METHOD
    W [ "Currency"    ] = CURRENCY
    W [ "Expenditure" ] = EXPENDITURE
    W [ "Outlay"      ] = OUTLAY
    W [ "Deposit"     ] = DEPOSIT
    W [ "Revenue"     ] = REVENUE
    W [ "Balance"     ] = BALANCE
    W [ "From"        ] = FROM
    W [ "Account"     ] = ACCOUNT
    W [ "Note"        ] = NOTE
    W [ "Contact"     ] = CONTACT
    W [ "Extras"      ] = EXTRAS
    return W

  def toBalance ( self , VALUES ) :
    return self . Balance2020 ( VALUES )

  def AppendBalanceItem ( self , DB , TABLE , W ) :
    ##########################################################################
    Actions     = W [ "Actions"     ]
    Page        = W [ "Page"        ]
    Order       = W [ "Order"       ]
    Row         = W [ "Row"         ]
    TRADEDATE   = W [ "TradeDate"   ]
    LOGDATE     = W [ "LogDate"     ]
    METHOD      = W [ "Method"      ]
    CURRENCY    = W [ "Currency"    ]
    EXPENDITURE = W [ "Expenditure" ]
    OUTLAY      = W [ "Outlay"      ]
    DEPOSIT     = W [ "Deposit"     ]
    REVENUE     = W [ "Revenue"     ]
    BALANCE     = W [ "Balance"     ]
    FROM        = W [ "From"        ]
    ACCOUNT     = W [ "Account"     ]
    NOTE        = W [ "Note"        ]
    CONTACT     = W [ "Contact"     ]
    EXTRAS      = W [ "Extras"      ]
    ##########################################################################
    QQ  = f"""insert into {TABLE}
              ( `actions`,`page`,`order`,`row`,`tradedate`,
                `logdate`,`method`,`currency`,`expenditure`,`outlay`,
                `deposit`,`revenue`,`balance`,`from`,`account`,
                `note`,`contact`,`extras`
              ) values (
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s , %s , %s ,
                %s , %s , %s ) ;"""
    VAL = ( Actions , Page    , Order    , Row         , TRADEDATE ,
            LOGDATE , METHOD  , CURRENCY , EXPENDITURE , OUTLAY    ,
            DEPOSIT , REVENUE , BALANCE  , FROM        , ACCOUNT   ,
            NOTE    , CONTACT , EXTRAS                             )
    DB . QueryValues ( QQ , VAL )
    ##########################################################################
    return True

  def AssureBalance ( self , DB , BALANCE , W ) :
    if ( not W ) :
      return False
    # if ( self . isBalanceExists ( DB , BALANCE , W ) ) :
    #   self . UpdateBalanceItem ( DB , BALANCE , W )
    # else :
    return self . AppendBalanceItem ( DB , BALANCE , W )
    # return True
