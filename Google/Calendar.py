# -*- coding: utf-8 -*-
##############################################################################
## Google Calendar API Interface
##############################################################################
import os
import sys
import datetime
import os . path
import pickle
from   googleapiclient.discovery      import build            as GoogleBuild
from   google_auth_oauthlib.flow      import InstalledAppFlow as InstallGoogle
from   google.auth.transport.requests import Request          as RequestGoogle
##############################################################################
class Calendar    (                                                        ) :
  ############################################################################
  def __init__    ( self , options = { }                                   ) :
    self . Service = None
    self . Assign ( options                                                  )
  ############################################################################
  def __del__     ( self                                                   ) :
    pass
  ############################################################################
  def Assign ( self , options = { } )                                        :
    self . Credentials = ""
    self . Authorized  = ""
    self . Creds       = None
    self . Scopes      = [ "https://www.googleapis.com/auth/calendar" ]
    if ( "Secrets"    in options )                                           :
      self . Credentials = options [ "Secrets"   ]
    if ( "Authorized" in options )                                           :
      self . Authorized  = options [ "Authorized" ]
    if ( "Scopes"     in options )                                           :
      self . Scopes      = options [ "Scopes" ]
  ############################################################################
  def Connect ( self )                                                       :
    ##########################################################################
    if ( self . Creds != None ) and ( self . Creds . valid )                 :
      try                                                                    :
        self . Service = GoogleBuild                                         (
                           "calendar"                                        ,
                           "v3"                                              ,
                           credentials = self . Creds                        )
        return True
      except                                                                 :
        pass
    ##########################################################################
    self . Creds = None
    ##########################################################################
    if            ( len ( self . Authorized ) > 0            )               :
      if          ( os . path . exists ( self . Authorized ) )               :
        with open ( self . Authorized , 'rb'                 ) as token      :
          self . Creds = pickle . load ( token )
    ##########################################################################
    if ( not self . Creds ) or ( not self . Creds . valid )                  :
      if ( self . Creds                                                  ) and
         ( self . Creds . expired                                        ) and
         ( self . creds . refresh_token                                  )   :
        self . Creds . refresh ( RequestGoogle ( )                           )
      else                                                                   :
        flow  = InstallGoogle . from_client_secrets_file                     (
                  self . Credentials                                         ,
                  self . Scopes                                              )
        self . Creds = flow . run_local_server ( port = 0                    )
      ########################################################################
      ## Save the credentials for the next run
      ########################################################################
      if ( len ( self . Authorized ) > 0 )                                   :
        with open ( self . Authorized , 'wb' ) as token                      :
          pickle . dump ( self . Creds , token )
    ##########################################################################
    if ( self . Creds != None ) and ( self . Creds . valid )                 :
      try                                                                    :
        self . Service = GoogleBuild                                         (
                           "calendar"                                        ,
                           "v3"                                              ,
                           credentials = self . Creds                        )
        return True
      except                                                                 :
        pass
    ##########################################################################
    return False
  ############################################################################
