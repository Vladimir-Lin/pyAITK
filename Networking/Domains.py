# -*- coding: utf-8 -*-
##############################################################################
##
##############################################################################
"""

CREATE TABLE `tld` (
  `id` int(11) NOT NULL,
  `uuid` bigint(20) NOT NULL,
  `used` int(11) DEFAULT 1,
  `type` int(11) DEFAULT 0,
  `owner` bigint(20) DEFAULT 0,
  `name` varchar(64) DEFAULT NULL,
  `reverse` varchar(64) DEFAULT NULL,
  `iana` varchar(16) DEFAULT NULL,
  `explain` blob DEFAULT '',
  `sld` bigint(20) DEFAULT 0,
  `domains` bigint(20) DEFAULT 0,
  `hosts` bigint(20) DEFAULT 0,
  `pages` bigint(20) DEFAULT 0,
  `ltime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `used` (`used`),
  KEY `type` (`type`),
  KEY `owner` (`owner`),
  KEY `name` (`name`(16)),
  KEY `reverse` (`reverse`(16)),
  KEY `iana` (`iana`),
  KEY `explain` (`explain`(128)),
  KEY `sld` (`sld`),
  KEY `domains` (`domains`),
  KEY `hosts` (`hosts`),
  KEY `pages` (`pages`),
  KEY `ltime` (`ltime`)
) ENGINE=Aria DEFAULT CHARSET=utf8mb4 ;

"""
##############################################################################
import os
import sys
##############################################################################
import mysql . connector
from   mysql . connector             import Error
##############################################################################
from   ..      Database . Query      import Query      as Query
from   ..      Database . Connection import Connection as Connection
from   ..      Database . Columns    import Columns    as Columns
##############################################################################

class Domains ( Columns ) :

  def __init__ ( self ) :
    super ( TLD , self ) . __init__ ( )
    self . Clear                    ( )

  def __del__ ( self ) :
    pass

  def Clear ( self ) :
    self . Columns  = [ ]
    self . Id       = -1
    self . Uuid     =  0
    self . Used     =  1
    self . Type     =  0
    self . Owner    =  0
    self . Name     =  ""
    self . Reverse  =  ""
    self . IANA     =  ""
    self . Explain  =  ""
    self . SLD      =  0
    self . Domains  =  0
    self . Hosts    =  0
    self . Pages    =  0
    self . Update   =  False

  def assign ( self , item ) :
    self . Columns  = item . Columns
    self . Id       = item . Id
    self . Uuid     = item . Uuid
    self . Used     = item . Used
    self . Type     = item . Type
    self . Owner    = item . Owner
    self . Name     = item . Name
    self . Reverse  = item . Reverse
    self . IANA     = item . IANA
    self . Explain  = item . Explain
    self . SLD      = item . SLD
    self . Domains  = item . Domains
    self . Hosts    = item . Hosts
    self . Pages    = item . Pages
    self . Update   = item . Update

  def set ( self , item , value ) :
    a = item . lower ( )
    if ( "id"       == a ) :
      self . Id      = value
    if ( "uuid"     == a ) :
      self . Uuid    = value
    if ( "used"     == a ) :
      self . Used    = value
    if ( "type"     == a ) :
      self . Type    = value
    if ( "owner"    == a ) :
      self . Owner   = value
    if ( "name"     == a ) :
      self . Name    = value
    if ( "reverse"  == a ) :
      self . Reverse = value
    if ( "iana"     == a ) :
      self . IANA    = value
    if ( "explain"  == a ) :
      self . Explain = value
    if ( "sld"      == a ) :
      self . SLD     = value
    if ( "domains"  == a ) :
      self . Domains = value
    if ( "hosts"    == a ) :
      self . Hosts   = value
    if ( "pages"    == a ) :
      self . Pages   = value
    if ( "ltime"    == a ) :
      self . Update  = value

  def get ( self , item ) :
    a = item . lower ( )
    if ( "id"       == a ) :
      return self . Id
    if ( "uuid"     == a ) :
      return self . Uuid
    if ( "used"     == a ) :
      return self . Used
    if ( "type"     == a ) :
      return self . Type
    if ( "owner"    == a ) :
      return self . Owner
    if ( "name"     == a ) :
      return self . Name
    if ( "reverse"  == a ) :
      return self . Reverse
    if ( "iana"     == a ) :
      return self . IANA
    if ( "explain"  == a ) :
      return self . Explain
    if ( "sld"      == a ) :
      return self . SLD
    if ( "domains"  == a ) :
      return self . Domains
    if ( "hosts"    == a ) :
      return self . Hosts
    if ( "pages"    == a ) :
      return self . Pages
    if ( "ltime"    == a ) :
      return self . Update
    return ""

  def tableItems ( self ) :
    return [ "id"      ,
             "uuid"    ,
             "used"    ,
             "type"    ,
             "owner"   ,
             "name"    ,
             "reverse" ,
             "iana"    ,
             "explain" ,
             "sld"     ,
             "domains" ,
             "hosts"   ,
             "pages"   ,
             "ltime"   ]

  def pair ( self , item ) :
    a = item . lower (      )
    v = self . get   ( item )
    if ( "id"       == a ) :
      return f"`{item}` = {v}"
    if ( "uuid"     == a ) :
      return f"`{item}` = {v}"
    if ( "used"     == a ) :
      return f"`{item}` = {v}"
    if ( "type"     == a ) :
      return f"`{item}` = {v}"
    if ( "owner"    == a ) :
      return f"`{item}` = {v}"
    if ( "name"     == a ) :
      return f"`{item}` = '{v}'"
    if ( "reverse"  == a ) :
      return f"`{item}` = '{v}'"
    if ( "iana"     == a ) :
      return f"`{item}` = '{v}'"
    if ( "explain"  == a ) :
      return f"`{item}` = '{v}'"
    if ( "sld"      == a ) :
      return f"`{item}` = {v}"
    if ( "domains"  == a ) :
      return f"`{item}` = {v}"
    if ( "hosts"    == a ) :
      return f"`{item}` = {v}"
    if ( "pages"    == a ) :
      return f"`{item}` = {v}"
    if ( "ltime"    == a ) :
      return f"`{item}` = '{v}'"
    return f"`{item}` = {v}"

  def valueItems ( self ) :
    return [ "used"    ,
             "type"    ,
             "owner"   ,
             "name"    ,
             "reverse" ,
             "iana"    ,
             "explain" ,
             "sld"     ,
             "domains" ,
             "hosts"   ,
             "pages"   ]

  def toJson ( self ) :
    return { "id"      : self . Id      ,
             "uuid"    : self . Uuid    ,
             "used"    : self . Used    ,
             "type"    : self . Type    ,
             "owner"   : self . Owner   ,
             "name"    : self . Name    ,
             "reverse" : self . Reverse ,
             "iana"    : self . IANA    ,
             "explain" : self . Explain ,
             "sld"     : self . SLD     ,
             "domains" : self . Domains ,
             "hosts"   : self . Hosts   ,
             "pages"   : self . Pages   ,
             "ltime"   : self . Update  }

  def isMatch ( self , tld ) :
    T = tld . lower ( )
    return ( self . Name == T )
