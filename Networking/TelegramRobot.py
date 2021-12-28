# -*- coding: utf-8 -*-
##############################################################################
## Telegram機器人
##############################################################################
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
import json
import ssl
import asyncio
##############################################################################
import urllib
import urllib   . parse
from   urllib                              import parse
##############################################################################
from   pathlib                             import Path
##############################################################################
from   http     . server                   import HTTPServer
from   http     . server                   import BaseHTTPRequestHandler
from   http     . server                   import ThreadingHTTPServer
##############################################################################
import telegram
from   telegram                            import Update
from   telegram                            import InputTextMessageContent
from   telegram                            import InlineQueryResultArticle
from   telegram                            import InlineKeyboardButton
from   telegram                            import InlineKeyboardMarkup
from   telegram . ext                      import Updater
from   telegram . ext                      import CallbackContext
from   telegram . ext                      import CallbackQueryHandler
from   telegram . ext                      import CommandHandler
from   telegram . ext                      import MessageHandler
from   telegram . ext                      import Filters
##############################################################################
class TelegramRobot (                                                      ) :
  ############################################################################
  def __init__      ( self                                                 , \
                      Account  = ""                                        , \
                      Token    = ""                                        , \
                      Options  = { }                                       ) :
    ##########################################################################
    self . TelegramLocker     = threading . Lock (                           )
    self . DebugLogger        = None
    self . Account            = Account
    self . Token              = Token
    self . TelegramUpdater    = None
    self . TelegramDispatcher = None
    self . Reply              = None
    self . SetOptions                            ( Options                   )
    ##########################################################################
    return
  ############################################################################
  def __del__       ( self                                                 ) :
    return
  ############################################################################
  def SetOptions ( self , Options                                          ) :
    ##########################################################################
    self . Options = Options
    ##########################################################################
    return
  ############################################################################
  def debug                        ( self , message , way = "info"         ) :
    ##########################################################################
    Logger   = self . DebugLogger
    ##########################################################################
    if                             ( Logger == None                        ) :
      return
    ##########################################################################
    if                             ( way == "debug"                        ) :
      Logger . debug               ( message                                 )
    elif                           ( way == "info"                         ) :
      Logger . info                ( message                                 )
    ##########################################################################
    return
  ############################################################################
  def lock                          ( self                                 ) :
    self . TelegramLocker . acquire (                                        )
    return
  ############################################################################
  def release                       ( self                                 ) :
    self . TelegramLocker . release (                                        )
    return
  ############################################################################
  def isWorking         ( self                                             ) :
    return self . Working
  ############################################################################
  def append       ( self , JSON                                           ) :
    ##########################################################################
    if             ( self . TelegramUpdater in [ False , None ]            ) :
      return
    ##########################################################################
    ACCOUNT = JSON [ "Account"                                               ]
    BEAU    = JSON [ "Beau"                                                  ]
    MSG     = JSON [ "Message"                                               ]
    CHATID  = int  ( ACCOUNT                                                 )
    ##########################################################################
    try                                                                      :
      ########################################################################
      self  . TelegramUpdater . bot . sendMessage                          ( \
                                chat_id    = CHATID                        , \
                                text       = MSG                           , \
                                parse_mode = "html"                          )
      MSG   = f"Sent {ACCOUNT} Message for {BEAU}"
      self  . debug           ( MSG                                          )
      ########################################################################
    except                                                                   :
      ########################################################################
      MSG   = f"Failure to send {ACCOUNT} Message for {BEAU}"
      self  . debug           ( MSG                                          )
    ##########################################################################
    return
  ############################################################################
  def AcceptCall     ( self , update: Update , context: CallbackContext    ) :
    ##########################################################################
    if               ( self . Reply in [ False , None ]                    ) :
      return
    ##########################################################################
    Account = update . effective_chat . id
    Account = f"{Account}"
    Message = update . message . text
    self . Reply     ( Account , "Reply" , Message                           )
    ##########################################################################
    return
  ############################################################################
  def MenuItem                  ( self , text , pattern                    ) :
    return InlineKeyboardButton ( text , callback_data = pattern             )
  ############################################################################
  def MarkupMenu                ( self , MENUs                             ) :
    return InlineKeyboardMarkup ( MENUs                                      )
  ############################################################################
  def addMenuItems                    ( self , JSON                        ) :
    ##########################################################################
    if                                ( isinstance ( JSON , list )         ) :
      ########################################################################
      MENUs     =                     [                                      ]
      ########################################################################
      for ITEM in JSON                                                       :
        ######################################################################
        SUBMENU = self . addMenuItems ( ITEM                                 )
        if                            ( SUBMENU != None                    ) :
          MENUs . append              ( SUBMENU                              )
      ########################################################################
      return MENUs
    ##########################################################################
    if ( ( "Menu" in JSON ) and ( "Pattern" in JSON ) )                      :
      ITEM      = self . MenuItem     ( JSON [ "Menu" ] , JSON [ "Pattern" ] )
      return ITEM
    ##########################################################################
    return None
  ############################################################################
  def addMarkupMenu             ( self , JSON                              ) :
    MENUs = self . addMenuItems (        JSON                                )
    return self  . MarkupMenu   ( self , MENUs                             ) :
  ############################################################################
  def addMenuHandler ( self , entry , func                                 ) :
    ##########################################################################
    if               ( self . TelegramDispatcher in [ False , None ]       ) :
      return
    ##########################################################################
    CQH  = CallbackQueryHandler             ( func , pattern = entry         )
    self . TelegramDispatcher . add_handler ( CQH                            )
    ##########################################################################
    return
  ############################################################################
  def addCommandHandler                        ( self , key , func         ) :
    ##########################################################################
    Handler = CommandHandler                   (        key , func           )
    self    . TelegramDispatcher . add_handler ( Handler                     )
    ##########################################################################
    return
  ############################################################################
  def Shutdown       ( self                                                ) :
    ##########################################################################
    if               ( self . TelegramUpdater in [ False , None ]          ) :
      return
    ##########################################################################
    self . TelegramUpdater . stop (                                          )
    self . TelegramUpdater = None
    ##########################################################################
    return
  ############################################################################
  def Start                                 ( self                         ) :
    ##########################################################################
    self . TelegramUpdater    = Updater     ( token       = self . Token   , \
                                              use_context = True             )
    self . TelegramDispatcher = self . TelegramUpdater . dispatcher
    ##########################################################################
    Hand = MessageHandler ( Filters . text & (~Filters . command )         , \
                            self    . AcceptCall                             )
    self . TelegramDispatcher . add_handler ( Hand                           )
    ##########################################################################
    self . TelegramUpdater . start_polling  (                                )
    ##########################################################################
    return
  ############################################################################
  def Idle                                  ( self                         ) :
    ##########################################################################
    self . TelegramUpdater . idle           (                                )
    ##########################################################################
    return
##############################################################################
