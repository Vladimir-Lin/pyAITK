# -*- coding: utf-8 -*-
##############################################################################
## 電話
##############################################################################
import os
import sys
##############################################################################
import phonenumbers
from   phonenumbers                   import carrier
from   phonenumbers . phonenumberutil import number_type
from   phonenumbers . phonenumberutil import region_code_for_country_code
from   phonenumbers . phonenumberutil import region_code_for_number
##############################################################################
import mysql        . connector
from   mysql        . connector       import Error
##############################################################################
from   ..      Database . Query       import Query      as Query
from   ..      Database . Connection  import Connection as Connection
from   ..      Database . Columns     import Columns    as Columns
##############################################################################
"""
電話號碼類型

固定電話 FIXED_LINE = 0
手機 MOBILE = 1
手機或固定電話 FIXED_LINE_OR_MOBILE = 2
免費電話 TOLL_FREE = 3
優惠電話 PREMIUM_RATE = 4
費用分享服務 SHARED_COST = 5
VoIP電話 VOIP = 6
個人電話 PERSONAL_NUMBER = 7
傳呼機 PAGER = 8
通用接入號碼 UAN = 9
商業電訊郵箱 VOICEMAIL = 10
未知 UNKNOWN = 99
"""
##############################################################################
class Phone              ( Columns                                         ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    self . Clear         (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__ ( self                                                       ) :
    return
  ############################################################################
  def Clear            ( self                                              ) :
    ##########################################################################
    self . Columns   = [                                                     ]
    self . Id        = -1
    self . Uuid      =  0
    self . Used      =  1
    self . Country   =  ""
    self . Area      =  ""
    self . Number    =  ""
    self . ltime     =  False
    self . Correct   =  1
    self . Mobile    =  0
    self . Shareable =  0
    self . Confirm   =  0
    self . Owners    =  0
    self . Region    = ""
    self . Nation    = ""
    ##########################################################################
    return
  ############################################################################
  def assign ( self , item                                                 ) :
    ##########################################################################
    self . Columns   = item . Columns
    self . Id        = item . Id
    self . Uuid      = item . Uuid
    self . Used      = item . Used
    self . Country   = item . Country
    self . Area      = item . Area
    self . Number    = item . Number
    self . ltime     = item . ltime
    self . Correct   = item . Correct
    self . Mobile    = item . Mobile
    self . Shareable = item . Shareable
    self . Confirm   = item . Confirm
    self . Owners    = item . Owners
    self . Region    = item . Region
    self . Nation    = item . Nation
    ##########################################################################
    return
  ############################################################################
  def set                  ( self , item , value                           ) :
    ##########################################################################
    a    = item . lower    (                                                 )
    ##########################################################################
    if                     ( "id"      == a                                ) :
      self . Id      = int ( value                                           )
    if                     ( "uuid"    == a                                ) :
      self . Uuid    = int ( value                                           )
    if                     ( "used"    == a                                ) :
      self . Used    = int ( value                                           )
    if                     ( "country" == a                                ) :
      self . Country = str ( value                                           )
    if                     ( "area"    == a                                ) :
      self . Area    = str ( value                                           )
    if                     ( "number"  == a                                ) :
      self . Number  = str ( value                                           )
    if                     ( "ltime"   == a                                ) :
      self . ltime   = value
    ##########################################################################
    return
  ############################################################################
  def get                 ( self , item                                    ) :
    ##########################################################################
    a      = item . lower (                                                  )
    ##########################################################################
    if                    ( "id"      == a                                 ) :
      return self . Id
    if                    ( "uuid"    == a                                 ) :
      return self . Uuid
    if                    ( "used"    == a                                 ) :
      return self . Used
    if                    ( "country" == a                                 ) :
      return self . Country
    if                    ( "area"    == a                                 ) :
      return self . Area
    if                    ( "number"  == a                                 ) :
      return self . Number
    if                    ( "ltime"   == a                                 ) :
      return self . ltime
    ##########################################################################
    return ""
  ############################################################################
  def tableItems ( self                                                    ) :
    return       [ "id"                                                    , \
                   "uuid"                                                  , \
                   "used"                                                  , \
                   "country"                                               , \
                   "area"                                                  , \
                   "number"                                                , \
                   "ltime"                                                   ]
  ############################################################################
  def pair                ( self , item                                    ) :
    ##########################################################################
    a      = item . lower (                                                  )
    v      = self . get   ( item                                             )
    ##########################################################################
    if                    ( "id"      == a                                 ) :
      return f"`{item}` = {v}"
    if                    ( "uuid"    == a                                 ) :
      return f"`{item}` = {v}"
    if                    ( "used"    == a                                 ) :
      return f"`{item}` = {v}"
    if                    ( "country" == a                                 ) :
      return f"`{item}` = '{v}'"
    if                    ( "area"    == a                                 ) :
      return f"`{item}` = '{v}'"
    if                    ( "number"  == a                                 ) :
      return f"`{item}` = '{v}'"
    if                    ( "ltime"   == a                                 ) :
      return f"`{item}` = '{v}'"
    ##########################################################################
    return f"`{item}` = {v}"
  ############################################################################
  def valueItems ( self                                                    ) :
    return       [ "used"                                                  , \
                   "country"                                               , \
                   "area"                                                  , \
                   "number"                                                , \
                   "ltime"                                                   ]
  ############################################################################
  def toJson ( self                                                        ) :
    return   { "id"        : self . Id                                     , \
               "uuid"      : self . Uuid                                   , \
               "used"      : self . Used                                   , \
               "country"   : self . Country                                , \
               "area"      : self . Area                                   , \
               "number"    : self . Number                                 , \
               "ltime"     : self . ltime                                  , \
               "correct"   : self . Correct                                , \
               "mobile"    : self . Mobile                                 , \
               "shareable" : self . Shareable                              , \
               "confirm"   : self . Confirm                                , \
               "owners"    : self . Owners                                 , \
               "region"    : self . Region                                 , \
               "nation"    : self . Nation                                   }
  ############################################################################
  def checkFormat ( self , Number , FORMATs                                ) :
    ##########################################################################
    KEYs = list   ( Number                                                   )
    for K in KEYs                                                            :
      if          ( K not in FORMATs                                       ) :
        return False
    ##########################################################################
    return True
  ############################################################################
  def isNumberFormat          ( self , Number                              ) :
    return self . checkFormat ( Number , "0123456789"                        )
  ############################################################################
  def isPhoneFormat           ( self , Number                              ) :
    return self . checkFormat ( Number , "0123456789+-"                      )
  ############################################################################
  def assureString     ( self , pb                                         ) :
    ##########################################################################
    BB   = pb
    ##########################################################################
    try                                                                      :
      BB = BB . decode ( "utf-8"                                             )
    except                                                                   :
      pass
    ##########################################################################
    return BB
  ############################################################################
  def VerifyFormats                      ( self                            ) :
    ##########################################################################
    self . Country = self . assureString ( self . Country                    )
    self . Area    = self . assureString ( self . Area                       )
    self . Number  = self . assureString ( self . Number                     )
    ##########################################################################
    return
  ############################################################################
  def ObtainsPhone       ( self , DB , Table                               ) :
    ##########################################################################
    if                   ( not self . ObtainsByUuid ( DB , Table )         ) :
      return False
    ##########################################################################
    self . VerifyFormats (                                                   )
    ##########################################################################
    return True
  ############################################################################
  def ObtainsProperties     ( self , DB , Table                            ) :
    ##########################################################################
    ITS  = "`correct`,`mobile`,`shareable`,`confirm`,`region`"
    WHS  = DB . WhereUuid   ( self . Uuid , True                             )
    QQ   = f"select {ITS} from {Table} {WHS}"
    DB   . Execute          ( QQ                                             )
    ##########################################################################
    LL   = DB    . FetchOne (                                                )
    ##########################################################################
    if                      ( LL in [ False , None ]                       ) :
      return False
    ##########################################################################
    if                      ( len ( LL ) != 5                              ) :
      return False
    ##########################################################################
    self . Correct   = int  ( LL [ 0 ]                                       )
    self . Mobile    = int  ( LL [ 1 ]                                       )
    self . Shareable = int  ( LL [ 2 ]                                       )
    self . Confirm   = int  ( LL [ 3 ]                                       )
    self . Region    = self . assureString  ( LL [ 4 ]                       )
    ##########################################################################
    return True
  ############################################################################
  def ObtainsFullPhone ( self , DB , PhoneTable , PropertiesTable          ) :
    ##########################################################################
    if ( not self . ObtainsPhone      ( DB , PhoneTable      )             ) :
      return False
    ##########################################################################
    if ( not self . ObtainsProperties ( DB , PropertiesTable )             ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def isCorrect   ( self                                                   ) :
    return        ( self . Correct   > 0                                     )
  ############################################################################
  def isMobile    ( self                                                   ) :
    return        ( self . Mobile in [ 1 , 2 ]                               )
  ############################################################################
  def isShareable ( self                                                   ) :
    return        ( self . Shareable > 0                                     )
  ############################################################################
  def isConfirm   ( self                                                   ) :
    return        ( self . Confirm   > 0                                     )
  ############################################################################
  def setCountry         ( self , country                                  ) :
    self . Country = str ( country                                           )
    return
  ############################################################################
  def setArea            ( self , area                                     ) :
    self . Area    = str ( area                                              )
    return
  ############################################################################
  def setNumber          ( self , number                                   ) :
    self . Number  = str ( number                                            )
    return
  ############################################################################
  def toPhone ( self                                                       ) :
    ##########################################################################
    if        ( len ( self . Country ) <= 0                                ) :
      return ""
    ##########################################################################
    if        ( len ( self . Number  ) <= 0                                ) :
      return ""
    ##########################################################################
    COUNTRY = self . Country
    AREA    = self . Area
    NUMBER  = self . Number
    ##########################################################################
    if        ( len ( AREA    ) <= 0                                       ) :
      return f"+{COUNTRY}-{NUMBER}"
    ##########################################################################
    return   f"+{COUNTRY}-{AREA}-{NUMBER}"
  ############################################################################
  def Verify                                ( self , Number                ) :
    ##########################################################################
    try                                                                      :
      ppn            = phonenumbers . parse ( Number                         )
    except                                                                   :
      self . Correct = 0
      self . Mobile  = 99
      return False
    ##########################################################################
    self   . Mobile  = number_type          ( ppn                            )
    self   . Correct = 1
    self   . Region  = ""
    ##########################################################################
    if                                      ( self . Mobile in [ 99 ]      ) :
      self . Correct = 0
      return False
    ##########################################################################
    reg    = region_code_for_country_code ( ppn . country_code              )
    self   . Region  = reg
    ##########################################################################
    return   True
##############################################################################
