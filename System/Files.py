# -*- coding: utf-8 -*-

import os
import sys
import getopt
import time
import datetime
import pytz

def Delete ( file ) :
  if os.path.isfile ( file ) :
    os.remove ( file )
    return True
  return False
