# -*- coding: utf-8 -*-

import os
import sys
import getopt

# type
# e extract
# x extract with directories

# options
# -aoa Overwrite All existing files without prompt.
# -aos Skip extracting of existing files.
# -aou aUto rename extracting file (for example, name.txt will be renamed to name_1.txt).
# -aot auto rename existing file (for example, name.txt will be renamed to name_1.txt).

def Extract ( file , type = "x" , options = [ "-aoa" ] ) :
  if ( len ( file ) <= 0 ) :
    return False
  if ( len ( type ) <= 0 ) :
    return False
  opts = ""
  if ( len ( options ) > 0 ) :
    opts = ' ' . join ( options )
  if ( len ( opts ) > 0 ) :
    cmd  = f"7z {opts} {type} {file}"
  else :
    cmd  = f"7z {type} {file}"
  r = os.system ( cmd )
  if ( r == 0 ) :
    return True
  return False

def Compress ( output , files , type = "a" , options = [ ] ) :
  if ( len ( output ) <= 0 ) :
    return False
  if ( len ( files  ) <= 0 ) :
    return False
  if ( len ( type   ) <= 0 ) :
    return False
  items = ' ' . join ( files )
  opts = ""
  if ( len ( options ) > 0 ) :
    opts = ' ' . join ( options )
  if ( len ( opts ) > 0 ) :
    cmd  = f"7z {opts} {type} {output} {items}"
  else :
    cmd  = f"7z {type} {output} {items}"
  r = os.system ( cmd )
  if ( r == 0 ) :
    return True
  return False
