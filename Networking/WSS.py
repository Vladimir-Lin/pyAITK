# -*- coding: utf-8 -*-
##############################################################################
## Websocket Server SSL
##############################################################################
import os
import sys
import hashlib
import base64
import socket
import struct
import ssl
import errno
import codecs
import socketserver
import json
import asyncio
import traceback
import time
import datetime
import logging
import requests
import threading
import shutil
import websocket
##############################################################################
from   socketserver                   import ThreadingMixIn
from   http . server                  import HTTPServer
from   http . server                  import BaseHTTPRequestHandler
from   io                             import StringIO
from   io                             import BytesIO
from   collections                    import deque
from   select                         import select
from   binascii                       import hexlify
##############################################################################
## Websocket SSL Server
##############################################################################
WSS_VALID_STATUS_CODES = [ 1000                                              ,
                           1001                                              ,
                           1002                                              ,
                           1003                                              ,
                           1007                                              ,
                           1008                                              ,
                           1009                                              ,
                           1010                                              ,
                           1011                                              ,
                           3000                                              ,
                           3999                                              ,
                           4000                                              ,
                           4999                                              ]
WSS_HANDSHAKE =                                                              (
   "HTTP/1.1 101 Switching Protocols\r\n"
   "Upgrade: WebSocket\r\n"
   "Connection: Upgrade\r\n"
   "Sec-WebSocket-Accept: %(acceptstr)s\r\n\r\n"
)
WSS_FAILED_HANDSHAKE =                                                       (
   "HTTP/1.1 426 Upgrade Required\r\n"
   "Upgrade: WebSocket\r\n"
   "Connection: Upgrade\r\n"
   "Sec-WebSocket-Version: 13\r\n"
   "Content-Type: text/plain\r\n\r\n"
   "This service requires use of the WebSocket protocol\r\n"
)
WSS_GUID        = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
WSS_STREAM      = 0x0
WSS_TEXT        = 0x1
WSS_BINARY      = 0x2
WSS_CLOSE       = 0x8
WSS_PING        = 0x9
WSS_PONG        = 0xA
WSS_HEADERB1    = 1
WSS_HEADERB2    = 3
WSS_LENGTHSHORT = 4
WSS_LENGTHLONG  = 5
WSS_MASK        = 6
WSS_PAYLOAD     = 7
WSS_MAXHEADER   = 65536
WSS_MAXPAYLOAD  = 33554432
##############################################################################
class WssHttpRequest       ( BaseHTTPRequestHandler                        ) :
  ############################################################################
  def __init__             ( self , request_text                           ) :
    ##########################################################################
    self . rfile           = BytesIO                 ( request_text          )
    self . raw_requestline = self . rfile . readline (                       )
    self . error_code      = self . error_message = None
    self . parse_request   (                                                 )
    ##########################################################################
    return
##############################################################################
class wssClient                               (                            ) :
  ############################################################################
  def __init__                                ( self , Hostname            ) :
    ##########################################################################
    self . Logger       = logging . getLogger (                              )
    ##########################################################################
    self . Running      = False
    self . Working      = False
    self . Connected    = False
    self . Thread       = None
    self . Wss          = None
    self . URL          = Hostname
    self . Translations =                     {                              }
    ##########################################################################
    self . onInitialize                       (                              )
    ##########################################################################
    return
  ############################################################################
  def __del__               ( self                                         ) :
    return
  ############################################################################
  def __enter__             ( self                                         ) :
    return self
  ############################################################################
  def __exit__              ( self , exc_type , exc_value , traceback      ) :
    pass
  ############################################################################
  def isRunning           ( self                                           ) :
    return self . Running
  ############################################################################
  def toJson              ( self , data                                    ) :
    ##########################################################################
    if                    ( len ( data ) <= 0                              ) :
      return              {                                                  }
    try                                                                      :
      JSOX = json . loads ( data                                             )
    except                                                                   :
      return              {                                                  }
    ##########################################################################
    return JSOX
  ############################################################################
  def onInitialize          ( self                                         ) :
    return True
  ############################################################################
  def onConnected                ( self , wss                              ) :
    return True
  ############################################################################
  def onPrivateConnected         ( self , wss                              ) :
    ##########################################################################
    self . Connected = True
    ##########################################################################
    return self . onConnected    (        wss                                )
  ############################################################################
  def onDisconnected             ( self , wss , status , message           ) :
    return True
  ############################################################################
  def onPrivateDisconnected      ( self , wss , status , message           ) :
    ##########################################################################
    self . Connected = False
    ##########################################################################
    return self . onDisconnected (        wss , status , message             )
  ############################################################################
  def onClose                    ( self                                    ) :
    return True
  ############################################################################
  def onError                    ( self , wss , e                          ) :
    return True
  ############################################################################
  def onMessage                  ( self , wss , message                    ) :
    return True
  ############################################################################
  def onBinary                   ( self , wss , message , opcode , flag    ) :
    return True
  ############################################################################
  def Debug                 ( self , message , way ="info"                 ) :
    if                      ( way == "debug"                               ) :
      self . Logger . debug ( message                                        )
    elif                    ( way == "info"                                ) :
      self . Logger . info  ( message                                        )
    return
  ############################################################################
  def send            ( self , data, opcode = 1                            ) :
    ##########################################################################
    if                ( not self . Connected                               ) :
      return False
    ##########################################################################
    if                ( self . Wss in [ False , None ]                     ) :
      return False
    ##########################################################################
    self . Wss . send ( data , opcode                                        )
    ##########################################################################
    return True
  ############################################################################
  def sendJson        ( self , jsox                                        ) :
    ##########################################################################
    if                ( not self . Connected                               ) :
      return False
    ##########################################################################
    if                ( self . Wss in [ False , None ]                     ) :
      return False
    ##########################################################################
    self . Wss . send ( json . dumps ( jsox )                                )
    ##########################################################################
    return True
  ############################################################################
  def monitor                  ( self                                      ) :
    ##########################################################################
    self   . Running = True
    self   . Working = True
    ##########################################################################
    URL    = self . URL
    MSG    = f"Start Moniting Websocket SSL Client channel for {URL}"
    self   . Debug             ( MSG                                         )
    ##########################################################################
    while                      ( self . Running                            ) :
      ########################################################################
      self . Wss = websocket . WebSocketApp                                ( \
                               self       . URL                            , \
                               on_open    = self . onPrivateConnected      , \
                               on_message = self . onMessage               , \
                               on_data    = self . onBinary                , \
                               on_error   = self . onError                 , \
                               on_close   = self . onPrivateDisconnected     )
      self . Wss . run_forever (                                             )
      self . Wss = None
      for i in range           ( 0 , 50                                    ) :
        if                     ( not self . Running                        ) :
          continue
        time . sleep           ( 0.1                                         )
    ##########################################################################
    self   . onClose           (                                             )
    ##########################################################################
    MSG    = "Stop Moniting Websocket SSL Client channel for {URL}"
    self   . Debug             ( MSG                                         )
    ##########################################################################
    self   . Working = False
    ##########################################################################
    return
  ############################################################################
  def stop                  ( self , waiting = False                       ) :
    ##########################################################################
    self . Running = False
    ##########################################################################
    if                      ( self . Wss in [ False , None ]               ) :
      return
    ##########################################################################
    self . Wss . close      (                                                )
    self . Wss = None
    ##########################################################################
    if                      ( not waiting                                  ) :
      return
    ##########################################################################
    while self . Working                                                     :
      time . sleep          ( 0.01                                           )
    ##########################################################################
    return
  ############################################################################
  def start                 ( self                                         ) :
    ##########################################################################
    if                      ( self . Working                               ) :
      self . Debug          ( "WSS Client is still working now"              )
      return False
    ##########################################################################
    self . Thread = threading . Thread ( target = self . monitor             )
    self . Thread . start   (                                                )
    ##########################################################################
    return True
##############################################################################
class wssAccepter (                                                        ) :
  ############################################################################
  def __init__    ( self , server , sock , address                         ) :
    ##########################################################################
    self . Logger         = logging . getLogger (                            )
    ##########################################################################
    self . Server         = server
    self . Socket         = sock
    self . Address        = address
    self . Translations   = {                                                }
    ##########################################################################
    self . Name           = ""
    self . Owner          = ""
    ##########################################################################
    self . handshaked     = False
    self . headerbuffer   = bytearray ( )
    self . headertoread   = 2048
    ##########################################################################
    self . fin            = 0
    self . data           = bytearray ( )
    self . opcode         = 0
    self . hasmask        = 0
    self . maskarray      = None
    self . length         = 0
    self . lengtharray    = None
    self . index          = 0
    self . request        = None
    self . UseSsl         = self . Server . supportSSL ( )
    ##########################################################################
    self . frag_start     = False
    self . frag_type      = WSS_BINARY
    self . frag_buffer    = None
    self . frag_decoder   = codecs . getincrementaldecoder ( 'utf-8' ) ( errors = 'strict' )
    self . closed         = False
    self . sendq          = deque()
    self . state          = WSS_HEADERB1
    ## restrict the size of header and payload for security reasons
    self . maxheader      = WSS_MAXHEADER
    self . maxpayload     = WSS_MAXPAYLOAD
    self . onInitialize     (                                                )
    ##########################################################################
    return
  ############################################################################
  def __del__               ( self                                         ) :
    self . onClose          (                                                )
    return
  ############################################################################
  def Debug                 ( self , message , way ="info"                 ) :
    if                      ( way == "debug"                               ) :
      self . Logger . debug ( message                                        )
    elif                    ( way == "info"                                ) :
      self . Logger . info  ( message                                        )
    return
  ############################################################################
  def isUnicode             ( self , val                                   ) :
    return isinstance       ( val  , str                                     )
  ############################################################################
  def toJson                ( self                                         ) :
    if                      ( len ( self . data ) <= 0                     ) :
      return { }
    try                                                                      :
      JSOX = json . loads   ( self . data                                    )
    except                                                                   :
      return { }
    return JSOX
  ############################################################################
  def HotClose                      ( self , timeout = 3.0                 ) :
    ##########################################################################
    fileno = self . Socket . fileno (                                        )
    self   . sendJson               ( { "Action" : "Shutdown" }              )
    msg    = "{1}@{0} as {2} by {3} is hot closing" . format ( self . Name , self . Owner , self . Role , fileno )
    self   . Debug                  ( msg                                    )
    ##########################################################################
    th     = threading . Thread     ( target = self . Server . WaitAndRemoveClient ,
                                      args   = ( fileno , timeout , )        )
    th     . start                  (                                        )
    ##########################################################################
    return
  ############################################################################
  def onInitialize          ( self                                         ) :
    return True
  ############################################################################
  def onConnected           ( self                                         ) :
    return True
  ############################################################################
  def onDisconnected        ( self                                         ) :
    return True
  ############################################################################
  def onClose               ( self                                         ) :
    return True
  ############################################################################
  def onError               ( self                                         ) :
    return True
  ############################################################################
  def onMessage             ( self                                         ) :
    return True
  ############################################################################
  def onBinary              ( self                                         ) :
    return True
  ############################################################################
  def doClose                ( self                                        ) :
    self    . Feeding = False
    self    . Socket . close (                                               )
    if self . handshaked                                                     :
      self  . onDisconnected (                                               )
    return True
  ############################################################################
  def CloseFrame              ( self , status = 1000 , reason = u''        ) :
    ##########################################################################
    try                                                                      :
      if self . closed is False                                              :
        close_msg = bytearray (                                              )
        close_msg . extend    ( struct . pack ( "!H" , status )              )
        if self . isUnicode   ( reason                                     ) :
          close_msg . extend  ( reason . encode ( 'utf-8' )                  )
        else                                                                 :
          close_msg . extend  ( reason                                       )
        self . postMessage    ( False , WSS_CLOSE , close_msg                )
    finally                                                                  :
      self . closed = True
    ##########################################################################
    return True
  ############################################################################
  def flushBuffer             ( self , buff , send_all = False             ) :
    ##########################################################################
    size         = len        ( buff                                         )
    tosend       = size
    already_sent = 0
    ##########################################################################
    while                     ( tosend > 0                                 ) :
      try                                                                    :
        ######################################################################
        ## i should be able to send a bytearray
        ######################################################################
        sent = self . Socket . send ( buff [ already_sent : ]                )
        if                    ( sent == 0                                  ) :
          self . Debug ( "{0} socket connection broken" . format ( self . Socket . fileno ( ) ) )
          return None
        ######################################################################
        already_sent += sent
        tosend       -= sent
        ######################################################################
      except socket . error as e                                             :
        ######################################################################
        ## if we have full buffers then wait for them to drain and try again
        ######################################################################
        if e . errno in [ errno . EAGAIN , errno . EWOULDBLOCK             ] :
          if send_all                                                        :
            continue
          return buff   [ already_sent :                                     ]
        else                                                                 :
          raise e
    ##########################################################################
    return None
  ############################################################################
  def sendFragmentStart       ( self , data                                ) :
    ##########################################################################
    opcode    = WSS_BINARY
    if self . isUnicode       ( data                                       ) :
       opcode = WSS_TEXT
    return self . postMessage ( True , opcode , data                         )
  ############################################################################
  def sendFragment            ( self  , data                               ) :
    return self . postMessage ( True  , WSS_STREAM , data                    )
  ############################################################################
  def sendFragmentEnd         ( self  , data                               ) :
    return self . postMessage ( False , WSS_STREAM , data                    )
  ############################################################################
  def sendMessage             ( self , data                                ) :
    opcode   = WSS_BINARY
    if self . isUnicode       ( data                                       ) :
      opcode = WSS_TEXT
    return self . postMessage ( False , opcode , data                        )
  ############################################################################
  def sendJson                ( self , jsox                                ) :
    return self . sendMessage ( json . dumps ( jsox )                        )
  ############################################################################
  def postMessage             ( self , fin , opcode , data                 ) :
    ##########################################################################
    payload = bytearray       (                                              )
    b1      = 0
    b2      = 0
    ##########################################################################
    if fin is False                                                          :
      b1   |= 0x80
    ##########################################################################
    b1     |= opcode
    ##########################################################################
    if self . isUnicode       ( data                                       ) :
      data  = data . encode   ( 'utf-8'                                      )
    ##########################################################################
    length  = len             ( data                                         )
    payload . append          ( b1                                           )
    ##########################################################################
    if                        ( length <= 125                              ) :
      b2   |= length
      payload . append        ( b2                                           )
    elif                      ( ( length >= 126 ) and ( length <= 65535 )  ) :
      b2   |= 126
      payload . append        ( b2                                           )
      payload . extend        ( struct . pack ( "!H" , length )              )
    else                                                                     :
      b2   |= 127
      payload . append        ( b2                                           )
      payload . extend        ( struct . pack ( "!Q" , length )              )
    ##########################################################################
    if                        ( length > 0                                 ) :
      payload . extend        ( data                                         )
    ##########################################################################
    self . sendq . append     ( ( opcode , payload )                         )
    ##########################################################################
    return True
  ############################################################################
  def DoHandshaking         ( self                                         ) :
    ##########################################################################
    data   = self . Socket . recv ( self . headertoread )
    if ( not data ) or ( len ( data ) <= 0 )                                 :
      return False
    ##########################################################################
    ## accumulate
    ##########################################################################
    self . headerbuffer . extend ( data )
    if ( len ( self . headerbuffer ) >= self . maxheader )                   :
      self . Debug ( "header exceeded allowable size : {0}" . format ( len ( self . headerbuffer ) ) )
      return False
    ##########################################################################
    ## Indicates end of HTTP header
    ##########################################################################
    if b'\r\n\r\n' in self . headerbuffer                                    :
      self . request = WssHttpRequest ( self . headerbuffer )
    ##########################################################################
    ## handshake rfc 6455
    ##########################################################################
    try                                                                      :
      key  = self   . request . headers [ "Sec-WebSocket-Key" ]
      k    = key    . encode    ( 'ascii' ) + WSS_GUID . encode ( "ascii" )
      k_s  = base64 . b64encode ( hashlib . sha1 ( k ) . digest ( ) ) . decode ( "ascii" )
      hStr = WSS_HANDSHAKE % { 'acceptstr' : k_s }
      self . sendq . append ( ( WSS_BINARY , hStr . encode ( 'ascii' ) )     )
      self . handshaked = True
      self . onConnected    (                                                )
    except Exception as e                                                    :
      hStr = WSS_FAILED_HANDSHAKE
      self . flushBuffer    ( hStr . encode ( 'ascii' ) , True               )
      self . Socket . close (                                                )
      self . onDisconnected (                                                )
      self . Debug ( "handshake failed: {0}" . format ( str ( ex ) ) )
      return False
    ##########################################################################
    return True
  ############################################################################
  def ImportData                ( self                                     ) :
    ##########################################################################
    fileno = self . Socket . fileno ( )
    if                          ( fileno < 0                               ) :
      return False
    ##########################################################################
    try                                                                      :
      data = self . Socket . recv ( 4096                                     )
    except Exception as ex                                                   :
      ## self . Debug ( "Exception when receiving data from {0} : {1}" . format ( fileno , str ( ex ) ) )
      return False
    if ( not data ) or ( len ( data ) <= 0 )                                 :
      return False
    for d in data                                                            :
      self . parseMessage       ( d                                          )
    ##########################################################################
    return True
  ############################################################################
  def ReadData                    ( self                                   ) :
    if self       . handshaked is False                                      :
      return self . DoHandshaking (                                          )
    return self   . ImportData    (                                          )
  ############################################################################
  def DoB1                         ( self , b                              ) :
    ##########################################################################
    self . fin         = b & 0x80
    self . opcode      = b & 0x0F
    self . state       = WSS_HEADERB2
    ##########################################################################
    self . index       = 0
    self . length      = 0
    self . lengtharray = bytearray (                                         )
    self . data        = bytearray (                                         )
    ##########################################################################
    rsv                = b & 0x70
    if                             ( rsv != 0                              ) :
      self . Debug ( "{0} RSV bit must be 0, but now - {1}" . format ( self . Socket . fileno ( ) , rsv ) )
      return False
    ##########################################################################
    return True
  ############################################################################
  def DoB2                        ( self , b                               ) :
    ##########################################################################
    mask   = b & 0x80
    length = b & 0x7F
    ##########################################################################
    if ( self . opcode == WSS_PING ) and ( length > 125 )                    :
      self . Debug ( "{0} ping packet is too large" . format ( self . Socket . fileno ( ) ) )
      return False
    ##########################################################################
    if ( mask == 128 )                                                       :
      self . hasmask = True
    else                                                                     :
      self . hasmask = False
    ##########################################################################
    if   ( length <= 125                                                   ) :
      ########################################################################
      self . length = length
      ########################################################################
      ## if we have a mask we must read it
      ########################################################################
      if self . hasmask is True                                              :
        self . maskarray = bytearray ( )
        self . state     = WSS_MASK
      else                                                                   :
        ######################################################################
        ## if there is no mask and no payload we are done
        ######################################################################
        if ( self . length <= 0 )                                            :
          try:
            self . processPacket ( )
          finally:
            self . state = WSS_HEADERB1
            self . data  = bytearray ( )
        ######################################################################
        ## we have no mask and some payload
        ######################################################################
        else                                                                 :
          #self.index = 0
          self . data  = bytearray ( )
          self . state = WSS_PAYLOAD
      ########################################################################
    elif ( length == 126                                                   ) :
       self . lengtharray = bytearray ( )
       self . state       = WSS_LENGTHSHORT
    elif ( length == 127                                                   ) :
       self . lengtharray = bytearray ( )
       self . state       = WSS_LENGTHLONG
    ##########################################################################
    return True
  ############################################################################
  def DoShort                      ( self , b                              ) :
    ##########################################################################
    self . lengtharray . append    ( b                                       )
    ##########################################################################
    if                             ( len ( self . lengtharray ) > 2        ) :
      self . Debug ( "{0} short length exceeded allowable size" . format ( self . Socket . fileno ( ) ) )
      return False
    ##########################################################################
    if len ( self . lengtharray ) != 2                                       :
      return True
    ##########################################################################
    self . length = struct . unpack_from ( '!H' , self . lengtharray ) [ 0 ]
    ##########################################################################
    if self . hasmask is True                                                :
      self . maskarray = bytearray (                                         )
      self . state     = WSS_MASK
      return True
    ##########################################################################
    ## if there is no mask and no payload we are done
    ##########################################################################
    if ( self . length <= 0 )                                                :
      try                                                                    :
        self . processPacket       (                                         )
      finally                                                                :
        self . state = WSS_HEADERB1
        self . data  = bytearray   (                                         )
      return True
    ##########################################################################
    ## we have no mask and some payload
    ##########################################################################
    #self.index = 0
    self . data  = bytearray       (                                         )
    self . state = WSS_PAYLOAD
    return True
  ############################################################################
  def DoLong                       ( self , b                              ) :
    ##########################################################################
    self . lengtharray . append    ( b                                       )
    ##########################################################################
    if                             ( len ( self . lengtharray ) > 8        ) :
      self . Debug ( "{0} long length exceeded allowable size" . format ( self . Socket . fileno ( ) ) )
      return False
    ##########################################################################
    if                             ( len ( self . lengtharray ) != 8       ) :
      return True
    ##########################################################################
    self . length = struct . unpack_from ( '!Q' , self . lengtharray ) [ 0 ]
    ##########################################################################
    if self . hasmask is True                                                :
      self . maskarray = bytearray (                                         )
      self . state     = WSS_MASK
      return True
    ##########################################################################
    ## if there is no mask and no payload we are done
    ##########################################################################
    if                             ( self . length <= 0                    ) :
      try                                                                    :
        self . processPacket       (                                         )
      finally                                                                :
        self . state = WSS_HEADERB1
        self . data  = bytearray   (                                         )
    ##########################################################################
    ## we have no mask and some payload
    ##########################################################################
    #self.index = 0
    self . data  = bytearray       (                                         )
    self . state = WSS_PAYLOAD
    ##########################################################################
    return True
  ############################################################################
  def DoMask                      ( self , b                               ) :
    ##########################################################################
    self . maskarray . append     ( b                                        )
    if                            ( len ( self . maskarray ) > 4           ) :
      self . Debug ( "{0} mask exceeded allowable size" . format ( self . Socket . fileno ( ) ) )
      return False
    ##########################################################################
    if                            ( len ( self . maskarray ) < 4           ) :
      return True
    ##########################################################################
    ## if there is no mask and no payload we are done
    ##########################################################################
    if                            ( self . length <= 0                     ) :
      try                                                                    :
        self . processPacket      (                                          )
      finally                                                                :
        self . state = WSS_HEADERB1
        self . data  = bytearray  (                                          )
      return True
    ##########################################################################
    ## we have mask and some payload
    ##########################################################################
    #self.index = 0
    self . data  = bytearray      (                                          )
    self . state = WSS_PAYLOAD
    ##########################################################################
    return True
  ############################################################################
  def DoPayload                   ( self , b                               ) :
    ##########################################################################
    if self . hasmask is True                                                :
       self . data . append       ( b ^ self . maskarray [ self.index % 4 ]  )
    else                                                                     :
       self . data . append       ( b                                        )
    ##########################################################################
    ## if length exceeds allowable size then we except and remove the connection
    ##########################################################################
    if ( len ( self . data ) >= self . maxpayload )                          :
      self . Debug ( "{0} payload exceeded allowable size" . format ( self . Socket . fileno ( ) ) )
      return False
    ##########################################################################
    ## check if we have processed length bytes; if so we are done
    ##########################################################################
    if ( ( self . index + 1 ) == self . length )                             :
      try                                                                    :
        self . processPacket      (                                          )
      finally                                                                :
        #self.index = 0
        self . state = WSS_HEADERB1
        self . data  = bytearray  (                                          )
    else                                                                     :
       self . index += 1
    ##########################################################################
    return True
  ############################################################################
  def DoOpClose                     ( self                                 ) :
    ##########################################################################
    status   = 1000
    reason   = u''
    length   = len                  ( self . data                            )
    ##########################################################################
    if                              ( length >= 2                          ) :
      ########################################################################
      status = struct . unpack_from ( '!H' , self . data [ :2 ] ) [ 0 ]
      reason = self . data [ 2: ]
      ########################################################################
      if status not in WSS_VALID_STATUS_CODES                                :
        status   = 1002
      ########################################################################
      if                            ( len ( reason ) > 0                   ) :
        try                                                                  :
          reason = reason . decode  ( 'utf8' , errors ='strict'              )
        except                                                               :
          status = 1002
    elif ( length == 1 )                                                     :
      status     = 1002
    ##########################################################################
    self . CloseFrame ( status , reason )
    ##########################################################################
    return True
  ############################################################################
  def DoOpFragment                ( self                                   ) :
    ##########################################################################
    if ( self . opcode != WSS_STREAM )                                       :
      ########################################################################
      if ( self . opcode in [ WSS_PONG , WSS_PING ]                        ) :
        self . Debug ( "{0} control messages can not be fragmented" . format ( self . Socket . fileno ( ) ) )
        return False
      ########################################################################
      self . frag_type    = self . opcode
      self . frag_start   = True
      self . frag_decoder . reset ( )
      ########################################################################
      if ( self . frag_type == WSS_TEXT )                                    :
        self . frag_buffer = [ ]
        utf_str = self . frag_decoder . decode ( self . data , final = False )
        if utf_str                                                           :
          self . frag_buffer . append  ( utf_str                             )
      else                                                                   :
        self . frag_buffer = bytearray (                                     )
        self . frag_buffer . extend    ( self . data                         )
      ########################################################################
      return True
    ##########################################################################
    if self . frag_start is False                                            :
      self . Debug ( "{0} fragmentation protocol error" . format ( self . Socket . fileno ( ) ) )
      return False
    ##########################################################################
    if self . frag_type == TEXT                                              :
      utf_str = self . frag_decoder . decode ( self . data , final = False   )
      if utf_str                                                             :
        self . frag_buffer . append    ( utf_str                             )
    else                                                                     :
      self   . frag_buffer . extend    ( self . data                         )
    return True
  ############################################################################
  def DoOpLastFragment            ( self                                   ) :
    ##########################################################################
    if                            ( self . opcode == WSS_STREAM            ) :
      ########################################################################
      if self . frag_start is False                                          :
        self . Debug ( "{0} fragmentation protocol error" . format ( self . Socket . fileno ( ) )  )
        return False
      ########################################################################
      if self . frag_type == WSS_TEXT                                        :
        utf_str = self . frag_decoder . decode ( self . data , final = True  )
        self . frag_buffer . append            ( utf_str                     )
        self . data = u'' . join               ( self . frag_buffer          )
      else                                                                   :
        self . frag_buffer . extend            ( self . data                 )
        self . data = self . frag_buffer
      ########################################################################
      self . onMessage                         (                             )
      ########################################################################
      self .frag_decoder . reset               (                             )
      self .frag_type   = WSS_BINARY
      self .frag_start  = False
      self .frag_buffer = None
      ########################################################################
      return True
    ##########################################################################
    if                            ( self . opcode == WSS_PING              ) :
      self . postMessage          ( False , WSS_PONG , self . data           )
      return True
    ##########################################################################
    if                            ( self . opcode == WSS_PONG              ) :
      return True
    ##########################################################################
    if self . frag_start is True                                             :
      self . Debug ( "{0} fragmentation protocol error" . format ( self . Socket . fileno ( ) )  )
      return False
    ##########################################################################
    if ( self . opcode == WSS_TEXT )                                         :
      try                                                                    :
        self . data = self . data . decode ( 'utf8' , errors = 'strict'      )
      except Exception as ex                                                 :
        self . Debug ( "{0} invalid utf-8 payload" . format ( self . Socket . fileno ( ) )  )
        return False
    ##########################################################################
    self . onMessage              (                                          )
    ##########################################################################
    return True
  ############################################################################
  def processPacket                  ( self                                ) :
    ##########################################################################
    OPCODES = [ WSS_CLOSE  ,
                WSS_STREAM ,
                WSS_TEXT   ,
                WSS_BINARY ,
                WSS_PONG   ,
                WSS_PING   ]
    if self . opcode not in OPCODES                                          :
      self . Debug ( "Unknown opcode : {0}" . format ( self . opcode ) )
      return False
    ##########################################################################
    if   ( self . opcode in [ WSS_PONG , WSS_PING ]                        ) :
      if ( len ( self . data ) > 125                                       ) :
        self . Debug ( "{0} control frame length can not be > 125" . format ( self . Socket . fileno ( ) ) )
        return False
    ##########################################################################
    if self . opcode == WSS_CLOSE                                            :
      return self . DoOpClose        (                                       )
    ##########################################################################
    if self . fin == 0                                                       :
      return self . DoOpFragment     (                                       )
    return   self . DoOpLastFragment (                                       )
  ############################################################################
  def parseMessage                ( self , b                               ) :
    if   self . state == WSS_HEADERB1                                        :
      return self . DoB1          ( b                                        )
    elif self . state == WSS_HEADERB2                                        :
      return self . DoB2          ( b                                        )
    elif self . state == WSS_LENGTHSHORT                                     :
      return self . DoShort       ( b                                        )
    elif self . state == WSS_LENGTHLONG                                      :
      return self . DoLong        ( b                                        )
    elif self . state == WSS_MASK                                            :
      return self . DoMask        ( b                                        )
    elif self . state == WSS_PAYLOAD                                         :
      return self . DoPayload     ( b                                        )
    return False
##############################################################################
class WSS                   (                                              ) :
  ############################################################################
  def __init__              ( self                                           ,
                              wssClientWrapper = None                        ,
                              Hostname         = "0.0.0.0"                   ,
                              Port             = 7931                        ,
                              Interval         = 0.1                         ,
                              UseSsl           = True                        ,
                              SslCert          = ""                          ,
                              SslKey           = ""                          ,
                              SslProtocol      = ssl . PROTOCOL_SSLv23     ) :
    ##########################################################################
    self . Logger        = logging . getLogger (                             )
    ##########################################################################
    self . Running       = False
    self . Working       = False
    self . Thread        = None
    ##########################################################################
    self . ClientWrapper = wssClientWrapper
    self . Hostname      = Hostname
    self . Port          = Port
    self . Interval      = Interval
    self . UseSSL        = UseSsl
    self . SslCert       = SslCert
    self . SslKey        = SslKey
    self . SslProtocol   = SslProtocol
    ##########################################################################
    self . Translations  =  {                                                }
    ##########################################################################
    self . Prepared      = self . PrepareSSL (                               )
    self . Locker        = threading . Lock  (                               )
    ##########################################################################
    return
  ############################################################################
  def __del__               ( self                                         ) :
    pass
  ############################################################################
  def __enter__             ( self                                         ) :
    return self
  ############################################################################
  def __exit__              ( self , exc_type , exc_value , traceback      ) :
    pass
  ############################################################################
  def Debug                 ( self , message , way ="info"                 ) :
    if                      ( way == "debug"                               ) :
      self . Logger . debug ( message                                        )
    elif                    ( way == "info"                                ) :
      self . Logger . info  ( message                                        )
    return
  ############################################################################
  def Lock                  ( self                                         ) :
    self . Locker . acquire (                                                )
    return
  ############################################################################
  def Unlock                ( self                                         ) :
    self . Locker . release (                                                )
    return
  ############################################################################
  def supportSSL            ( self                                         ) :
    return                  ( ( self . Prepared ) and ( self . UseSSL )      )
  ############################################################################
  def WrapSocket            ( self , sock                                  ) :
    if self . supportSSL    (                                              ) :
      return self . SslContext . wrap_socket ( sock , server_side = True     )
    return sock
  ############################################################################
  def PrepareSSL            ( self                                         ) :
    ##########################################################################
    self . Channel    = "ws"
    self . SslContext = None
    if                      ( not self . UseSSL                            ) :
      return True
    if                      ( len ( self . SslCert ) <= 0                  ) :
      self . Debug          ( "Empty SSL Cert file"                          )
      return False
    ##########################################################################
    try                                                                      :
      self . Debug          ( "WSS Cert : " + self . SslCert                 )
      self . Debug          ( "WSS Key  : " + self . SslKey                  )
      self . SslContext = ssl . SSLContext ( self . SslProtocol              )
      self . SslContext . load_cert_chain  ( self . SslCert , self . SslKey  )
      self . Channel    = "wss"
    except Exception as e                                                    :
      msg               = "failed to use ssl: {0}" . format ( e )
      self . Debug          ( msg                                            )
      return False
    ##########################################################################
    return True
  ############################################################################
  def BindWss               ( self                                         ) :
    ##########################################################################
    Host          = None
    Family        = socket . AF_INET6
    if                      ( len ( self . Hostname ) > 0                  ) :
      Host        = self . Hostname
      Family      = 0
    ##########################################################################
    try                                                                      :
      ########################################################################
      msg = "Try binding WSS to {0}:{1}" . format ( Host , self . Port )
      self . Debug          ( msg                                            )
      ########################################################################
      hostInfo    = socket . getaddrinfo                                     (
                      Host                                                   ,
                      self . Port                                            ,
                      Family                                                 ,
                      socket . SOCK_STREAM                                   ,
                      socket . IPPROTO_TCP                                   ,
                      socket . AI_PASSIVE                                    )
      ########################################################################
      self . Socket = socket . socket ( hostInfo [ 0 ] [ 0 ]                 ,
                                        hostInfo [ 0 ] [ 1 ]                 ,
                                        hostInfo [ 0 ] [ 2 ]                 )
      self . Socket . setsockopt      ( socket . SOL_SOCKET                  ,
                                        socket . SO_REUSEADDR                ,
                                        1                                    )
      self . Socket . bind            ( hostInfo [ 0 ] [ 4 ]                 )
      self . Socket . listen          ( 5                                    )
      self . Connections =            {                                      }
      self . Listeners   =            [ self . Socket                        ]
      ########################################################################
    except Exception as e                                                    :
      msg               = "Failed to Bind WSS : {0}" . format ( e )
      self . Debug          ( msg                                            )
      return False
    ##########################################################################
    msg = "WSS is binded to {0}:{1}" . format ( Host , self . Port )
    self . Debug          ( msg                                              )
    ##########################################################################
    return True
  ############################################################################
  def TryBindWss             ( self , wssTimeout = 300.0                   ) :
    ##########################################################################
    Binded     = False
    UTS        = time . time ( )
    wssTimeout = 300.0
    ## 300 seconds
    while ( ( time . time ( ) - UTS ) < wssTimeout ) and ( not Binded )      :
      Binded   = self . BindWss ( )
      if ( not Binded                                                      ) :
        time . sleep        ( 1                                              )
    ##########################################################################
    if                      ( not Binded                                   ) :
      self . Debug          ( "Failure to Bind WSS"                          )
      self . Running = False
      self . Working = False
      return False
    ##########################################################################
    return True
  ############################################################################
  def CloseWss                 ( self                                      ) :
    ##########################################################################
    if                         ( self . Socket in [ False , None ]         ) :
      return False
    ##########################################################################
    try                                                                      :
      self . Socket . close    (                                             )
      self . Socket = None
    except Exception as ex                                                   :
      self . Debug ( "WSS Closing Exception : {0}" . format ( str ( ex ) )   )
    ##########################################################################
    for desc , client in self . Connections . items (                      ) :
      client . CloseFrame      (                                             )
      client . doClose         (                                             )
    ##########################################################################
    return True
  ############################################################################
  def CreateClient              ( self , sock , address                    ) :
    if                          ( self . ClientWrapper == None             ) :
      return None
    return self . ClientWrapper ( self, sock, address                        )
  ############################################################################
  def DispatchClient        ( self , sockno                                ) :
    ##########################################################################
    if                      ( sockno not in self . Connections             ) :
      False
    ##########################################################################
    client = self . Connections [ sockno ]
    ##########################################################################
    try                                                                      :
      while client . sendq                                                   :
        opcode , payload = client . sendq . popleft (                        )
        remaining        = client . flushBuffer     ( payload                )
        if remaining is not None                                             :
          client . sendq . appendleft ( ( opcode , remaining )               )
          break
        else                                                                 :
          if opcode == WSS_CLOSE                                             :
            self . Debug ( "{0} received client close" . format ( sockno )   )
            client . onClose  (                                              )
            self . RemoveClient ( sockno )
            return False
    except Exception as ex                                                   :
      ## self . Debug ( "DispatchClient Exception : {0}" . format ( str ( ex ) ) )
      ## self . RemoveClient ( sockno )
      return False
    return True
  ############################################################################
  def HandleClient          ( self , sockno                                ) :
    ##########################################################################
    if sockno not in self . Connections                                      :
      return False
    ##########################################################################
    try                                                                      :
      client = self . Connections [ sockno ]
      client . ReadData     (                                                )
    except Exception as ex                                                   :
      self . Debug ( "Client Exception : {0}" . format ( str ( ex ) )        )
      self . RemoveClient   ( sockno                                         )
    return True
  ############################################################################
  def RemoveClient                ( self , sockno                          ) :
    ##########################################################################
    if sockno not in self . Connections                                      :
      return False
    ##########################################################################
    self . Lock                   (                                          )
    ##########################################################################
    try                                                                      :
      client = self . Connections [ sockno                                   ]
      client . doClose            (                                          )
      del self . Connections      [ sockno                                   ]
      if                          ( sockno in self . Listeners             ) :
        self . Listeners . remove ( sockno                                   )
    except                                                                   :
      pass
    ##########################################################################
    self . Unlock                 (                                          )
    ##########################################################################
    return True
  ############################################################################
  def WaitAndRemoveClient       ( self , sockno , timeout                  ) :
    ##########################################################################
    time . sleep                ( timeout                                    )
    self . RemoveClient         ( sockno                                     )
    ##########################################################################
    return True
  ############################################################################
  def FindClient            ( self , Name , Owner                          ) :
    Keys = self . Connections . keys (                                       )
    for K in Keys                                                            :
      client = self . Connections [ K ]
      if ( client . Name == Name ) and ( client . Owner == Owner )           :
        return client
    return None
  ############################################################################
  def FindClients                        ( self , Name , Owner             ) :
    Clients  =                           [                                   ]
    Keys     = self . Connections . keys (                                   )
    for K in Keys                                                            :
      client = self . Connections        [ K                                 ]
      if ( client . Name == Name ) and ( client . Owner == Owner )           :
        Clients . append                 ( client                            )
    return Clients
  ############################################################################
  def FindClientsByName                  ( self , Name                     ) :
    Clients  =                           [                                   ]
    Keys     = self . Connections . keys (                                   )
    for K in Keys                                                            :
      client = self . Connections        [ K                                 ]
      if                                 ( client . Name == Name           ) :
        Clients . append                 ( client                            )
    return Clients
  ############################################################################
  def NewClient             ( self                                         ) :
    ##########################################################################
    sock = None
    ##########################################################################
    try                                                                      :
      sock , address = self . Socket . accept (                              )
      newsock        = self . WrapSocket      ( sock                         )
      newsock        . setblocking            ( 0                            )
      fileno         = newsock . fileno       (                              )
      WS             = self . CreateClient    ( newsock , address            )
      WS . Translations = self . Translations
      if                                      ( WS != None                 ) :
        self . Connections [ fileno ] = WS
        self . Listeners . append             ( fileno                       )
    except Exception as ex                                                   :
      if sock is not None                                                    :
        sock . close                          (                              )
    ##########################################################################
    return True
  ############################################################################
  def dispatcher            ( self                                         ) :
    ##########################################################################
    self . Lock             (                                                )
    writers = [ ]
    ##########################################################################
    for fileno in self . Listeners                                           :
      if                    ( not self . Running                           ) :
        continue
      if                    ( fileno == self . Socket                      ) :
        continue
      if                    ( fileno in self . Connections                 ) :
        client = self . Connections [ fileno ]
        if client . sendq                                                    :
          writers . append  ( fileno                                         )
    ##########################################################################
    rList , wList , xList = select ( self . Listeners                        ,
                                     writers                                 ,
                                     self . Listeners                        ,
                                     self . Interval                         )
    ##########################################################################
    self . Unlock           (                                                )
    ##########################################################################
    for ready in wList                                                       :
      self . DispatchClient ( ready                                          )
    ##########################################################################
    for ready in rList                                                       :
      if                    ( not self . Running                           ) :
        continue
      if                    ( ready == self . Socket                       ) :
        self . NewClient    (                                                )
      else                                                                   :
        self . HandleClient ( ready                                          )
    ##########################################################################
    for failed in xList                                                      :
      if                    ( not self . Running                           ) :
        continue
      if                    ( failed == self . Socket                      ) :
        self . CloseWss     (                                                )
        while               ( self . Running                               ) :
          self . TryBindWss ( 60.0                                           )
        return True
      else                                                                   :
        self . RemoveClient ( failed                                         )
    ##########################################################################
    return True
  ############################################################################
  def monitor               ( self                                         ) :
    ##########################################################################
    self . Running = True
    self . Working = True
    ##########################################################################
    self . Debug            ( "Start Moniting Websocket SSL channel"         )
    ##########################################################################
    if                      ( not self . TryBindWss ( 300.0 )              ) :
      return
    ##########################################################################
    while self . Running                                                     :
      self . dispatcher     (                                                )
    ##########################################################################
    self . CloseWss         (                                                )
    self . Debug            ( "Stop Moniting Websocket SSL channel"          )
    self . Working = False
    ##########################################################################
    return
  ############################################################################
  def stop                  ( self , waiting = False                       ) :
    ##########################################################################
    self . Running = False
    if                      ( not waiting                                  ) :
      return
    while self . Working                                                     :
      time . sleep          ( 0.01                                           )
    ##########################################################################
    return
  ############################################################################
  def start                 ( self                                         ) :
    ##########################################################################
    if                      ( self . Working                               ) :
      self . Debug          ( "WSS is still working now"                     )
      return False
    if                      ( not self . Prepared                          ) :
      self . Debug          ( "SSL channel is not prepared"                  )
      return False
    ##########################################################################
    self . Thread = threading . Thread ( target = self . monitor             )
    self . Thread . start   (                                                )
    ##########################################################################
    return True
##############################################################################
