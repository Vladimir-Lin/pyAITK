# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import datetime
import requests
import threading
import mysql.connector
from   mysql.connector import Error
from   .SqlConnection  import SqlConnection as SqlConnection
from   .SqlQuery       import SqlQuery      as SqlQuery

def isSQL ( parameters ) :
  if ( len ( parameters ) < 3 ) :
    return False
  hostname = parameters [ "hostname" ]
  username = parameters [ "username" ]
  password = parameters [ "password" ]
  if ( len ( hostname ) <= 0 ) :
    return False
  if ( len ( username ) <= 0 ) :
    return False
  if ( len ( password ) <= 0 ) :
    return False
  return True
