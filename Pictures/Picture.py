# -*- coding: utf-8 -*-
##############################################################################
## 圖片
##############################################################################
import os
import sys
import time
import datetime
import logging
import requests
import threading
import gettext
import binascii
import hashlib
import base64
from   io           import BytesIO
from   wand . image import Image
from   PIL          import Image as Pillow
##############################################################################
class Picture     (                                                        ) :
  ############################################################################
  def __init__    ( self                                                   ) :
    self . UUID     = 0
    self . Filename = ""
    self . Data     = None
    self . Image    = None
    self . Icon     = None
    self . IconData = None
    self . CRC32    = 0
    return
  ############################################################################
  def __del__     ( self                                                   ) :
    pass
  ############################################################################
  def Load        ( self , Filename                                        ) :
    ##########################################################################
    self . Filename = Filename
    ##########################################################################
    with open ( Filename , "rb" ) as fp                                      :
      self. Data = fp . read ( )
    ##########################################################################
    if ( self . Data == None )                                               :
      return False
    ##########################################################################
    if ( len ( self . Data ) <= 0 )                                          :
      return False
    ##########################################################################
    try                                                                      :
      self . Image = Image ( blob = self . Data )
    except :
      return False
    return True
  ############################################################################
  def Assign      ( self , DAT                                             ) :
    ##########################################################################
    self. Data = DAT
    ##########################################################################
    if ( self . Data == None )                                               :
      return False
    ##########################################################################
    if ( len ( self . Data ) <= 0 )                                          :
      return False
    ##########################################################################
    try                                                                      :
      self . Image = Image ( blob = self . Data )
    except :
      return False
    return True
  ############################################################################
  def Iconize ( self )                                                       :
    self . Icon = Image ( self . Image )
    w = self . Icon . width
    h = self . Icon . height
    if ( ( w > 128 ) or ( h > 128 ) ) :
      if ( w > h ) :
        h = int ( h * 128 / w )
        w = 128
      else :
        w = int ( w * 128 / h )
        h = 128
      self . Icon . resize ( w , h )
    self . Icon . format = "png"
    self . IconData = BytesIO ( )
    self . Icon . save ( file = self . IconData )
  ############################################################################
  def toCRC32 ( self )                                                       :
    self . CRC32 = binascii . crc32 ( self . Data )
    return self . CRC32
  ############################################################################
  def toMD5 ( self )                                                         :
    m = hashlib . md5 ( )
    m . update        ( self . Data )
    self . MD5 = m . hexdigest ( )
    return self . MD5
  ############################################################################
  def toSHA256 ( self )                                                      :
    m = hashlib . sha256 ( )
    m . update        ( self . Data )
    self . SHA256 = base64 . b64encode ( m . digest ( ) ) . decode ('utf-8')
    return self . SHA256
  ############################################################################
  def toHistogram                  ( self                                  ) :
    ##########################################################################
    self . R      =                [                                         ]
    self . G      =                [                                         ]
    self . B      =                [                                         ]
    self . A      =                [                                         ]
    ##########################################################################
    fp            = BytesIO        ( self . Data                             )
    img           = Pillow . open  ( fp                                      )
    try                                                                      :
      channels    = img    . split (                                         )
      count       = len            ( channels                                )
    except                                                                   :
      return
    ##########################################################################
    if                             ( count == 3                            ) :
      r, g, b     = img . split    (                                         )
    elif                           ( count == 4                            ) :
      r, g, b , a = img . split    (                                         )
      self . A    = a . histogram  (                                         )
    else                                                                     :
      return
    ##########################################################################
    self . R      = r . histogram  (                                         )
    self . G      = g . histogram  (                                         )
    self . B      = b . histogram  (                                         )
    ##########################################################################
    return
  ############################################################################
  def PrepareForDB     ( self                                              ) :
    self . Iconize     (                                                     )
    self . toCRC32     (                                                     )
    self . toMD5       (                                                     )
    self . toSHA256    (                                                     )
    self . toHistogram (                                                     )
  ############################################################################
  def HistogramToBytes ( self , HIST                                       ) :
    B = BytesIO        (                                                     )
    for v in HIST                                                            :
      B . write        ( int ( v ) . to_bytes ( 4 , 'big' )                  )
    return B
  ############################################################################
  def StoreHistogram   ( self , DB , TABLE , UUID , Item , Data )            :
    ##########################################################################
    if                 ( len ( Data ) <= 0                                 ) :
      return
    ##########################################################################
    BB  = self . HistogramToBytes ( Data ) . getvalue ( )
    VAL = ( UUID , len ( BB ) , BB , )
    QQ  = f"insert into {TABLE} (`uuid`,`type`,`scope`,`name`,`length`,`value`) values (%s,2,'Histograph','{Item}',%s,%s) ;"
    DB  . QueryValues ( QQ , VAL )
    ##########################################################################
    return
  ############################################################################
  def ImportDB ( self , DB , Options ) :
    UUIX   = 0
    BASE   = Options [ "Base"       ]
    PREFER = Options [ "Prefer"     ]
    MASTER = Options [ "Master"     ]
    DEPOT  = Options [ "Depot"      ]
    THUMB  = Options [ "Thumb"      ]
    TDEPOT = Options [ "ThumbDepot" ]
    HASH   = Options [ "Hash"       ]
    HIST   = Options [ "Histogram"  ]
    MIMEM  = "mimeexts"
    EXTMX  = "extensions"
    PRETAB = "pictureorders"
    FMT    = self . Image . format
    FMT    = FMT  . lower ( )
    SW     = self . Image . width
    SH     = self . Image . height
    SIZE   = len ( self . Data )
    TW     = self . Icon  . width
    TH     = self . Icon  . height
    TSIZE  = self . IconData . getbuffer ( ) . nbytes
    CRC32  = self . CRC32
    DB     . LockWrites   ( [ MASTER , DEPOT , THUMB , TDEPOT , HASH , HIST , PRETAB , MIMEM , EXTMX ] )
    QQ     = f"select `uuid` from {MASTER} where ( `filesize` = {SIZE} ) and ( `checksum` = {CRC32} ) and ( `width` = {SW} ) and ( `height` = {SH} ) ;"
    DB     . Query ( QQ )
    LL     = DB . FetchAll ( )
    if ( ( LL == None ) or ( len ( LL ) <= 0 ) ) :
      UUIX = BASE
      QQ   = f"select `uuid` from {MASTER} order by `id` desc limit 0,1 ;"
      DB   . Query ( QQ )
      LX   = DB . FetchOne ( )
      if ( not ( ( LX == None ) or ( len ( LX ) <= 0 ) ) ) :
        UUIX = LX [ 0 ]
      UUIX = UUIX + 1
      MIMEID = 0
      QQ   = f"select `mime` from `mimeexts` where ( `extension` = ( select `id` from `extensions` where ( `extension` = '{FMT}' ) ) ) ;"
      DB   . Query ( QQ )
      FX   = DB . FetchAll ( )
      if ( not ( ( FX == None ) or ( len ( FX ) <= 0 ) ) ) :
        MIMEID = FX [ 0 ] [ 0 ]
      ########################################################################
      VAL = ( UUIX , MIMEID , FMT , SIZE , CRC32 , SW , SH , )
      QQ  = f"insert into {MASTER} (`uuid`,`mimeid`,`suffix`,`filesize`,`checksum`,`width`,`height`) values (%s,%s,%s,%s,%s,%s,%s) ;"
      DB  . QueryValues ( QQ , VAL )
      ########################################################################
      VAL = ( UUIX , self . Data , )
      QQ  = f"insert into {DEPOT} (`uuid`,`file`) values (%s,%s) ;"
      DB  . QueryValues ( QQ , VAL )
      ########################################################################
      VAL = ( UUIX , SIZE , TSIZE , SW , SH , TW , TH , )
      QQ  = f"insert into {THUMB} (`uuid`,`usage`,`filesize`,`iconsize`,`format`,`width`,`height`,`iconwidth`,`iconheight`) values (%s,'ICON',%s,%s,'png',%s,%s,%s,%s) ;"
      DB  . QueryValues ( QQ , VAL )
      ########################################################################
      VAL = ( UUIX , self . IconData . getvalue ( ) , )
      QQ  = f"insert into {TDEPOT} (`uuid`,`usage`,`thumb`) values (%s,'ICON',%s) ;"
      DB  . QueryValues ( QQ , VAL )
      ########################################################################
      VAL = ( UUIX , len ( self . MD5 ) , self . MD5 , )
      QQ  = f"insert into {HASH} (`uuid`,`type`,`scope`,`name`,`length`,`value`) values (%s,1,'Hash','MD5',%s,%s) ;"
      DB  . QueryValues ( QQ , VAL )
      ########################################################################
      VAL = ( UUIX , len ( self . SHA256 ) , self . SHA256 , )
      QQ  = f"insert into {HASH} (`uuid`,`type`,`scope`,`name`,`length`,`value`) values (%s,1,'Hash','SHA256',%s,%s) ;"
      DB  . QueryValues ( QQ , VAL )
      ########################################################################
      self . StoreHistogram   ( DB , HIST , UUIX , "R" , self . R            )
      self . StoreHistogram   ( DB , HIST , UUIX , "G" , self . G            )
      self . StoreHistogram   ( DB , HIST , UUIX , "B" , self . B            )
      self . StoreHistogram   ( DB , HIST , UUIX , "A" , self . A            )
      ########################################################################
      QQ  = f"insert into {PRETAB} ( `uuid` ) values ( {UUIX} ) ;"
      DB  . Query ( QQ )
      ########################################################################
    else                                                                     :
      ########################################################################
      if ( PREFER >= 0 )                                                     :
        UUIX = LL [ 0 ] [ 0 ]
        QQ  = f"update {PRETAB} set `position` = {PREFER} where ( `uuid` = {UUIX} ) ;"
        DB  . Query ( QQ )
      ########################################################################
    DB     . UnlockTables (     )
    self . UUID = UUIX
    return True
