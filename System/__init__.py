# -*- coding: utf-8 -*-

from . import Debugger
from . import Extract
from . import Files
from . import FTP
from . import Settings
from . import StarDate

__all__ = [ "Debugger" ,
            "Extract"  ,
            "Files"    ,
            "FTP"      ,
            "Settings" ]

SupportedLanguages = {
  1001 : "English" ,
  1002 : "正體中文" ,
  1003 : "简体中文" ,
  1004 : "香港粵語" ,
  1005 : "台灣國語" ,
  1006 : "日本語"
}

SupportedLocale =  {
  1001 : "en-US" ,
  1002 : "zh-TW" ,
  1003 : "zh-CN" ,
  1004 : "zh-HK" ,
  1005 : "zh-TN" ,
  1006 : "ja-JP"
}
