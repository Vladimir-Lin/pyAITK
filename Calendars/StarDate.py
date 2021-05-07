# -*- coding: utf-8 -*-
##############################################################################
import os
import sys
import getopt
import time
import datetime
import pytz
##############################################################################
class StarDate (                                                           ) :
  ############################################################################
  def __init__ ( self                                                      ) :
    self . Stardate = 0
  ############################################################################
  def isValid  ( self                                                      ) :
    return ( self . Stardate > 0 )
  ############################################################################
  def set ( self , sd ) :
    self . Stardate = sd
    return self . Stardate
  ############################################################################
  def Seconds ( self , D , H , M , S ) :
    return self . Days    ( D ) + \
           self . Hours   ( H ) + \
           self . Minutes ( M ) + \
                            S     ;
  ############################################################################
  def Minutes ( self , M ) :
    return M * 60
  ############################################################################
  def Hours ( self , H ) :
    return H * 3600
  ############################################################################
  def Days ( self , D ) :
    return D * 84600
  ############################################################################
  def Add ( self , S ) :
    self . Stardate += S
    return self . Stardate
  ############################################################################
  def AddDuration ( self , S ) :
    SS   = S . split ( ":" )
    CNT  = len ( SS )
    if ( CNT <= 0 ) :
      return self . Stardate
    TT   = 0
    II   = 0
    while ( II < CNT ) :
      TT = TT * 60
      XX = SS [ II ]
      TT = TT + XX
      II = II + 1
    self . Add ( TT )
    return self . Stardate
  ############################################################################
  def Subtract ( self , S ) :
    self . Stardate -= S
    return self . Stardate
  ############################################################################
  def Timestamp ( self ) :
    return self . Stardate - 1420092377704080000
  ############################################################################
  def secondsTo ( self , SD ) :
    return SD . Stardate - self . Stardate
  ############################################################################
  def setTime ( self , ut ) :
    self . Stardate = ut   + 1420092377704080000
    return self . Stardate
  ############################################################################
  def fromDateTime ( self , dt ) :
    return self . setTime ( int ( dt . timestamp ( ) ) )
  ############################################################################
  def Now ( self ) :
    return self . fromDateTime ( datetime . datetime . now ( ) )
  ############################################################################
  def fromFormat ( self , dtString , TZ = "" ) :
    if ( len ( TZ ) > 0 ) :
      tzs = pytz . timezone ( TZ )
      dt = tzs . localize ( datetime . datetime . strptime ( dtString , "%Y/%m/%d %H:%M:%S" ) )
    else :
      dt = datetime . datetime . strptime ( dtString , "%Y/%m/%d %H:%M:%S" )
    return self . fromDateTime ( dt )
  ############################################################################
  def fromInput ( self , inpString , TZ = "" ) :
    dtString = inpString
    dtString = dtString . replace ( "T" , " " )
    dtString = dtString . replace ( "-" , "/" )
    cnt      = dtString . count   ( ":"       )
    if ( cnt == 0 ) :
      dtString = dtString + ":00:00" ;
    if ( cnt == 1 ) :
      dtString = dtString + ":00"    ;
    return self . fromFormat ( dtString , TZ )
  ############################################################################
  def ShrinkMinute ( self ) :
    TS = self . Timestamp ( )
    TS = TS % 60
    self . Stardate -= TS
    return self . Stardate
  ############################################################################
  def ShrinkHour ( self ) :
    return self . Subtract ( self . Timestamp ( ) % 3600 )
  ############################################################################
  def toDateTime ( self , TZ = "" ) :
    if ( len ( TZ ) > 0 ) :
      tzs = pytz . timezone ( TZ )
      return datetime . datetime . fromtimestamp ( self . Timestamp ( ) , tz = tzs )
    else :
      return datetime . datetime . fromtimestamp ( self . Timestamp ( ) )
  ############################################################################
  def Weekday ( self , TZ = "" ) :
    DT = self . toDateTime ( TZ )
    return DT . weekday ( ) + 1
  ############################################################################
  def isPM ( self , TZ = "" ) :
    DT   = self . toDateTime ( TZ )
    hour = DT   . today ( ) . weekday ( )
    if ( hour < 12 ) :
      return 0
    return 1
  ############################################################################
  def toDateString ( self , TZ , FMT = "%Y/%m/%d" ) :
    DT = self . toDateTime ( TZ  )
    return DT . strftime   ( FMT )
  ############################################################################
  def toTimeString ( self , TZ , FMT = "%H:%M:%S" ) :
    DT = self . toDateTime ( TZ  )
    return DT . strftime   ( FMT )
  ############################################################################
  def toDateTimeString ( self , TZ , JOIN ="T" , DateFormat = "%Y-%m-%d" , TimeFormat = "%H:%M:%S" ) :
    DS  = self . toDateString ( TZ , DateFormat )
    DT  = self . toTimeString ( TZ , TimeFormat )
    return DS + JOIN + DT
  ############################################################################
  def toLongDateTimeString ( self , TZ , DateFormat = "%Y-%m-%d" , TimeFormat = "%H:%M:%S" ) :
    WD   = self . Weekday          ( TZ                                      )
    WD   = int                     ( WD                                      )
    WS   = {  1 : "Monday"                                                 , \
              2 : "Tuesday"                                                , \
              3 : "Wednesday"                                              , \
              4 : "Thursday"                                               , \
              5 : "Friday"                                                 , \
              6 : "Saturday"                                               , \
              7 : "Sunday"                                                   }
    JOIZ = " "
    if                             ( WD in [ 1 , 2 , 3 , 4 , 5 , 6 , 7 ]   ) :
      KS   = WS [ WD ]
      JOIZ = f" {KS} "
    return self . toDateTimeString ( TZ , JOIZ , DateFormat , TimeFormat     )
  ############################################################################
  def SecondsOfDay ( self , TZ = "" ) :
    DX = self . toDateString ( TZ , "%Y-%m-%d" )
    DX = f"{DX}T00:00:00"
    XS = StarDate ( )
    XS . Stardate = XS . fromInput ( DX )
    return XS . secondsTo ( self )
##############################################################################
"""
datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

public function toLongString($TZ,$DateFormat="Y-m-d",$TimeFormat="H:i:s")
{
  $Correct = true                                                            ;
  ////////////////////////////////////////////////////////////////////////////
  if  ( isset ( $GLOBALS [ "WeekDays" ] )                                  ) {
    $WeekDays = $GLOBALS [ "WeekDays" ]                                      ;
  } else $Correct = false                                                    ;
  ////////////////////////////////////////////////////////////////////////////
  if  ( isset ( $GLOBALS [ "AMPM"     ] )                                  ) {
    $AMPM     = $GLOBALS [ "AMPM"     ]                                      ;
  } else $Correct = false                                                    ;
  ////////////////////////////////////////////////////////////////////////////
  if ( $Correct                                                            ) {
    $SW  = $WeekDays [ $this -> Weekday ( $TZ ) ]                            ;
    $SP  = $AMPM     [ $this -> isPM    ( $TZ ) ]                            ;
    $SJ  = " {$SW} {$SP} "                                                   ;
  } else $SJ = " "                                                           ;
  ////////////////////////////////////////////////////////////////////////////
  return $this -> toDateTimeString ( $TZ , $SJ , $DateFormat , $TimeFormat ) ;
}

// calcuate a person's age
public function YearsOld($TZ)
{
  $TDT = $this -> toDateTime ( $TZ  ) ;
  $NDT = new \DateTime       (      ) ;
  $DIF = $NDT -> diff        ( $TDT ) ;
  return $DIF -> y                    ;
}

public static function StarDateToString($DT,$Tz,$FMT)
{
  $SD  = new StarDate      (      ) ;
  $SD -> Stardate = $DT             ;
  $DX  = $SD -> toDateTime ( $Tz  ) ;
  $SS  = $DX -> format     ( $FMT ) ;
  ///////////////////////////////////
  unset                    ( $SD  ) ;
  unset                    ( $DX  ) ;
  ///////////////////////////////////
  return $SS                        ;
}

public static function StarDateString($DT,$FMT)
{
  $Tz = TimeZones::GetTZ        (                  ) ;
  return self::StarDateToString ( $DT , $Tz , $FMT ) ;
}

public static function UntilToday($DATE,$TZ,$YEARSTR,$MONTHSTR)
{
  //////////////////////////////////////////////////////
  if ( strlen ( $DATE ) <= 0 ) return ""               ;
  $NOW  = new StarDate ( )                             ;
  $NOW -> Now          ( )                             ;
  //////////////////////////////////////////////////////
  $XXXZ = $NOW -> toDateString ( $TZ , "Y-m-d" )       ;
  $DATE = str_replace ( "/" , "-" , $DATE  )           ;
  //////////////////////////////////////////////////////
  $ZZZ  = explode ( "-" , $DATE )                      ;
  $WWW  = explode ( "-" , $XXXZ )                      ;
  //////////////////////////////////////////////////////
  $YYY  = intval ( $WWW [ 0 ] , 10 )                   ;
  $YYY -= intval ( $ZZZ [ 0 ] , 10 )                   ;
  //////////////////////////////////////////////////////
  $MMM  = intval ( $WWW [ 1 ] , 10 )                   ;
  $MMM -= intval ( $ZZZ [ 1 ] , 10 )                   ;
  //////////////////////////////////////////////////////
  $DDD  = intval ( $WWW [ 2 ] , 10 )                   ;
  $DDD -= intval ( $ZZZ [ 2 ] , 10 )                   ;
  //////////////////////////////////////////////////////
  if ( $DDD < 0 ) $MMM = $MMM - 1                      ;
  if ( $MMM < 0 )                                      {
    $MMM = $MMM + 12                                   ;
    $YYY = $YYY - 1                                    ;
  }                                                    ;
  //////////////////////////////////////////////////////
  $YST = str_replace ( "$(TOTAL)" , $YYY , $YEARSTR  ) ;
  $MST = str_replace ( "$(TOTAL)" , $MMM , $MONTHSTR ) ;
  $MSG = ""                                            ;
  if ( $YYY > 0 ) $MSG = $MSG . $YST                   ;
  if ( $MMM > 0 ) $MSG = $MSG . $MST                   ;
  if ( strlen ( $MSG ) <= 0 ) $MSG = "0"               ;
  //////////////////////////////////////////////////////
  return $MSG                                          ;
}

"""
##############################################################################
