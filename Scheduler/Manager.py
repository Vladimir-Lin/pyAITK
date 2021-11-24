# -*- coding: utf-8 -*-
##############################################################################
## 行程管理介面
##############################################################################
import os
import sys
import time
import datetime
##############################################################################
import mysql . connector
from   mysql . connector               import Error
##############################################################################
import AITK
from   AITK . Database   . Query       import Query
from   AITK . Database   . Connection  import Connection
from   AITK . Database   . Columns     import Columns
##############################################################################
from   AITK . Networking . WSS         import WSS         as WSS
from   AITK . Networking . WSS         import wssAccepter as wssAccepter
##############################################################################
from                     . Project     import Project     as Project
from                     . Projects    import Projects    as Projects
from                     . Event       import Event       as Event
from                     . Events      import Events      as Events
from                     . Task        import Task        as Task
from                     . Tasks       import Tasks       as Tasks
##############################################################################
class Manager                 (                                            ) :
  ############################################################################
  def __init__                ( self                                       ) :
    return
  ############################################################################
  def __del__                 ( self                                       ) :
    return
##############################################################################
