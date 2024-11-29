# -*- coding: utf-8 -*-
##############################################################################
## 影片工具
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
import pathlib
import ffmpeg
##############################################################################
import AITK
##############################################################################
from   AITK . Database   . Query          import Query
from   AITK . Database   . Connection     import Connection
from   AITK . Database   . Pair           import Pair
from   AITK . Database   . Columns        import Columns
##############################################################################
from   AITK . Documents  . Name           import Name           as NameItem
from   AITK . Documents  . Name           import Naming         as Naming
from   AITK . Documents  . Notes          import Notes          as NoteItem
from   AITK . Documents  . Variables      import Variables      as VariableItem
from   AITK . Documents  . ParameterQuery import ParameterQuery as ParameterQuery
##############################################################################
from   AITK . Calendars  . StarDate       import StarDate       as StarDate
from   AITK . Calendars  . Periode        import Periode        as Periode
from   AITK . Essentials . Relation       import Relation       as Relation
##############################################################################
def M3UtoFilms                    ( M3U                                    ) :
  ############################################################################
  TEXT      = ""
  with open                       ( M3U , "rb" ) as F                        :
    TEXT    = F . read            (                                          )
  ############################################################################
  if                              ( len ( TEXT ) <= 0                      ) :
    return                        [                                          ]
  ############################################################################
  LM        = TEXT . find         ( b'# Playlist created by'                 )
  ############################################################################
  if                              ( LM > 0                                 ) :
    ##########################################################################
    TEXT    = TEXT                [ LM :                                     ]
    LM      = TEXT . find         ( b'\n'                                    )
    ##########################################################################
    if                            ( LM > 0                                 ) :
      TEXT  = TEXT                [ LM + 1 :                                 ]
  ############################################################################
  BODY      = TEXT . decode       ( "utf-8"                                  )
  if                              ( len ( BODY ) <= 0                      ) :
    return                        [                                          ]
  ############################################################################
  MDIR      = os . path . dirname ( os . path . realpath ( M3U )             )
  MDIR      = MDIR . replace      ( "\\" , "/"                               )
  ############################################################################
  LISTs     = BODY . split        ( "\n"                                     )
  FILMs     =                     [                                          ]
  ############################################################################
  for F in LISTs                                                             :
    ##########################################################################
    K       = F
    K       = K . replace         ( "\r" , ""                                )
    K       = K . replace         ( "\n" , ""                                )
    ##########################################################################
    if                            ( len ( K ) <= 0                         ) :
      continue
    ##########################################################################
    if                            ( "#" == K [ 0 : 1 ]                     ) :
      continue
    ##########################################################################
    if                            ( ( "/" in F ) or ( "\\" in F )          ) :
      ########################################################################
      T     = F
      ########################################################################
    else                                                                     :
      ########################################################################
      T     = f"{MDIR}/{K}"
    ##########################################################################
    if                           ( os . path . exists ( T )                ) :
      ########################################################################
      FILMs . append             ( T                                         )
  ############################################################################
  return FILMs
##############################################################################
