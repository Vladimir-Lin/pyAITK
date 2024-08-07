# -*- coding: utf-8 -*-
##############################################################################
## 曆法解譯器
##############################################################################
import time
import datetime
import pytz
##############################################################################
class Parser       (                                                       ) :
  ############################################################################
  def __init__     ( self                                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__      ( self                                                  ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def toHours    ( self , seconds                                          ) :
    ##########################################################################
    try                                                                      :
      ########################################################################
      HOUR = int ( seconds / 3600                                            )
      ########################################################################
    except                                                                   :
      return 0
    ##########################################################################
    return HOUR
  ############################################################################
  def toMinutes  ( self , seconds ) :
    ##########################################################################
    try                                                                      :
      ########################################################################
      HOUR = int ( seconds / 3600                                            )
      SECS = int ( seconds - ( HOUR * 3600 )                                 )
      MINS = int ( SECS    /  60                                             )
      ########################################################################
    except                                                                   :
      return 0
    ##########################################################################
    return MINS
  ############################################################################
  def toSeconds  ( self , seconds                                          ) :
    ##########################################################################
    try                                                                      :
      SECS = int ( seconds % 60                                              )
    except                                                                   :
      return 0
    ##########################################################################
    return SECS
  ############################################################################
  def KeywordExists     ( self , Format , Keywords , Start                 ) :
    ##########################################################################
    EXISTs     =        [                                                    ]
    WORD       = Format [ Start :                                            ]
    ##########################################################################
    for KEY in Keywords                                                      :
      ########################################################################
      if                ( KEY in WORD                                      ) :
        EXISTs . append ( KEY                                                )
    ##########################################################################
    return EXISTs
  ############################################################################
  def LocateKeyword     ( self , Format , Keywords , Start                 ) :
    ##########################################################################
    WORD       = Format [ Start :                                            ]
    FOUND      = ""
    AT         = len    ( WORD                                               )
    AT         = int    ( AT + 1                                             )
    ##########################################################################
    for KEY in Keywords                                                      :
      ########################################################################
      WHERE    = WORD . index ( KEY                                          )
      ########################################################################
      if                      ( ( WHERE >= 0 ) and ( WHERE < AT )          ) :
        ######################################################################
        AT     = WHERE
        FOUND  = KEY
    ##########################################################################
    return FOUND
  ############################################################################
  def Dissects                         ( self , Format , Keywords          ) :
    ##########################################################################
    RESULTs     =                      [                                     ]
    POS         = 0
    DONE        = False
    LEN         = len                  ( Format                              )
    ##########################################################################
    while                              ( not DONE                          ) :
      ########################################################################
      if                               ( POS >= LEN                        ) :
        ######################################################################
        DONE    = True
        ######################################################################
        continue
      ########################################################################
      EXISTs    = self . KeywordExists ( Format , Keywords , POS             )
      ########################################################################
      if                               ( len ( EXISTs ) <= 0               ) :
        ######################################################################
        RESULTs . append               ( Format [ POS : ]                    )
        DONE    = True
        ######################################################################
        continue
      ########################################################################
      KEY       = self . LocateKeyword ( Format , EXISTs   , POS             )
      ########################################################################
      if                               ( len ( KEY ) <= 0                  ) :
        ######################################################################
        RESULTs . append               ( Format [ POS : ]                    )
        DONE    = True
        ######################################################################
        continue
      ########################################################################
      WHERE     = Format . index       ( KEY , POS                           )
      ########################################################################
      if                               ( WHERE > POS                       ) :
        ######################################################################
        RESULTs . append               ( Format [ POS : WHERE ]              )
      ########################################################################
      RESULTs   . append               ( KEY                                 )
      POS       = WHERE + len          ( KEY                                 )
    ##########################################################################
    return RESULTs
  ############################################################################
  def Parsing               ( self , inputString , Keywords , Sequences    ) :
    ##########################################################################
    V           = inputString
    AT          = 0
    POS         = 0
    LEN         = len       ( V                                              )
    FRAGs       = len       ( Sequences                                      )
    JSON        =           {                                                }
    ##########################################################################
    if                      ( LEN   <= 0                                   ) :
      return                {                                                }
    ##########################################################################
    if                      ( FRAGs <= 0                                   ) :
      return                {                                                }
    ##########################################################################
    while                   ( AT < FRAGs                                   ) :
      ########################################################################
      KEY = Sequences       [ AT                                             ]
      ########################################################################
      if                    ( KEY in Keywords                              ) :
        ######################################################################
        if                  ( ( AT + 1 ) < FRAGs                           ) :
          ####################################################################
          try                                                                :
            ##################################################################
            NK  = Sequences [ AT + 1                                         ]
            EOV = V . index ( NK , POS                                       )
            ##################################################################
          except                                                             :
            return          {                                                }
          ####################################################################
        else                                                                 :
          EOV   = LEN
        ######################################################################
        R       = V         [ POS : EOV                                      ]
        JSON [ KEY ] = R
        ######################################################################
        POS     = EOV
        AT      = AT + 1
        ######################################################################
      else                                                                   :
        ######################################################################
        KLEN    = len       ( KEY                                            )
        R       = V         [ POS : POS + KLEN                               ]
        ######################################################################
        if                  ( R != KEY                                     ) :
          return            {                                                }
        ######################################################################
        POS     = POS + KLEN
        AT      = AT + 1
    ##########################################################################
    return JSON
  ############################################################################
  def Keywords                ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def Decoder                 ( self , Calendar , inputString , Format     ) :
    raise NotImplementedError (                                              )
##############################################################################
