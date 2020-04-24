# -*- coding: utf-8 -*-

import os
import sys

def Delete ( file ) :
  if os.path.isfile ( file ) :
    os.remove ( file )
    return True
  return False
