# -*- coding: utf-8 -*-
##############################################################################
## Google Calendar API Interface
##############################################################################
import os
import sys
import datetime
##############################################################################
import os . path
##############################################################################
import pickle
##############################################################################
import googleapiclient
from   googleapiclient . discovery          import build            as GoogleBuild
from   google_auth_oauthlib . flow          import InstalledAppFlow as InstallGoogle
from   google . auth . transport . requests import Request          as RequestGoogle
##############################################################################
class Calendar    (                                                        ) :
  ############################################################################
  ## +| __init__ |+
  ############################################################################
  def __init__    ( self , options = { }                                   ) :
    self . Service = None
    self . Assign ( options                                                  )
  ############################################################################
  ## -| __init__ |-
  ############################################################################
  ## +| __del__ |+
  ############################################################################
  def __del__     ( self                                                   ) :
    pass
  ############################################################################
  ## -| __del__ |-
  ############################################################################
  ## +| Assign |+
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
  ## -| Assign |-
  ############################################################################
  ## +| Connect |+
  ############################################################################
  def Connect ( self )                                                       :
    ##########################################################################
    if ( self . Creds != None ) and ( self . Creds . valid )                 :
      try                                                                    :
        self . Service = GoogleBuild                                         (
                           "calendar"                                        ,
                           "v3"                                              ,
                           credentials     = self . Creds                    ,
                           cache_discovery = False                           )
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
      if ( self . Creds                                                ) and \
         ( self . Creds . expired                                      ) and \
         ( self . Creds . refresh_token                                  )   :
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
                           credentials = self . Creds                        ,
                           cache_discovery = False                           )
        return True
      except googleapiclient . errors . HttpError as err                     :
        pass
    ##########################################################################
    return False
  ############################################################################
  ## -| Connect |-
  ############################################################################
  ## +| GetCalendars |+
  ############################################################################
  def GetCalendars ( self )                                                  :
    ##########################################################################
    if ( self . Service == None )                                            :
      return False
    ##########################################################################
    try                                                                      :
      calendarsResult = self . Service . calendarList ( ) . list ( ) . execute()
    except Exception as ex                                                   :
      return False
    return calendarsResult . get ( "items" , [ ] )
  ############################################################################
  ## -| GetCalendars |-
  ############################################################################
  ## +| GetEvents |+
  ############################################################################
  def GetEvents ( self , calendarId , options = { } )                        :
    ##########################################################################
    if ( self . Service == None )                                            :
      return False
    ##########################################################################
    sharedExtendedProperty  = None
    maxResults              = None
    timeZone                = None
    pageToken               = None
    orderBy                 = None
    timeMax                 = None
    timeMin                 = None
    syncToken               = None
    alwaysIncludeEmail      = None
    singleEvents            = None
    updatedMin              = None
    q                       = None
    privateExtendedProperty = None
    maxAttendees            = None
    showDeleted             = None
    showHiddenInvitations   = None
    iCalUID                 = None
    ##########################################################################
    if ( "sharedExtendedProperty"   in options                             ) :
      sharedExtendedProperty  = options [ "sharedExtendedProperty"           ]
    if ( "maxResults"               in options                             ) :
      maxResults              = options [ "maxResults"                       ]
    if ( "timeZone"                 in options                             ) :
      timeZone                = options [ "timeZone"                         ]
    if ( "pageToken"                in options                             ) :
      pageToken               = options [ "pageToken"                        ]
    if ( "orderBy"                  in options                             ) :
      orderBy                 = options [ "orderBy"                          ]
    if ( "timeMax"                  in options                             ) :
      timeMax                 = options [ "timeMax"                          ]
    if ( "timeMin"                  in options                             ) :
      timeMin                 = options [ "timeMin"                          ]
    if ( "syncToken"                in options                             ) :
      syncToken               = options [ "syncToken"                        ]
    if ( "alwaysIncludeEmail"       in options                             ) :
      alwaysIncludeEmail      = options [ "alwaysIncludeEmail"               ]
    if ( "singleEvents"             in options                             ) :
      singleEvents            = options [ "singleEvents"                     ]
    if ( "updatedMin"               in options                             ) :
      updatedMin              = options [ "updatedMin"                       ]
    if ( "q"                        in options                             ) :
      q                       = options [ "q"                                ]
    if ( "privateExtendedProperty"  in options                             ) :
      privateExtendedProperty = options [ "privateExtendedProperty"          ]
    if ( "maxAttendees"             in options                             ) :
      maxAttendees            = options [ "maxAttendees"                     ]
    if ( "showDeleted"              in options                             ) :
      showDeleted             = options [ "showDeleted"                      ]
    if ( "showHiddenInvitations"    in options                             ) :
      showHiddenInvitations   = options [ "showHiddenInvitations"            ]
    if ( "iCalUID"                  in options                             ) :
      iCalUID                 = options [ "iCalUID" ]
    ##########################################################################
    try                                                                      :
      Result = self . Service . events ( ) . list                            (
        calendarId              = calendarId                                 ,
        sharedExtendedProperty  = sharedExtendedProperty                     ,
        maxResults              = maxResults                                 ,
        timeZone                = timeZone                                   ,
        pageToken               = pageToken                                  ,
        orderBy                 = orderBy                                    ,
        timeMax                 = timeMax                                    ,
        timeMin                 = timeMin                                    ,
        syncToken               = syncToken                                  ,
        alwaysIncludeEmail      = alwaysIncludeEmail                         ,
        singleEvents            = singleEvents                               ,
        updatedMin              = updatedMin                                 ,
        q                       = q                                          ,
        privateExtendedProperty = privateExtendedProperty                    ,
        maxAttendees            = maxAttendees                               ,
        showDeleted             = showDeleted                                ,
        showHiddenInvitations   = showHiddenInvitations                      ,
        iCalUID                 = iCalUID                      ) . execute ( )
      return Result . get ( "items" , [ ]                                    )
    except googleapiclient . errors . HttpError as err                       :
      print ( str ( err ) )
      pass
    ##########################################################################
    return False
  ############################################################################
  ## -| GetEvents |-
  ############################################################################
  ## +| Get |+
  ############################################################################
  def Get ( self , calendarId , eventId , options = { } )                    :
    ##########################################################################
    if ( self . Service == None )                                            :
      return False
    ##########################################################################
    alwaysIncludeEmail = None
    timeZone           = None
    maxAttendees       = None
    ##########################################################################
    if ( "alwaysIncludeEmail"  in options                                  ) :
      alwaysIncludeEmail = options [ "alwaysIncludeEmail"                    ]
    if ( "timeZone"            in options                                  ) :
      timeZone           = options [ "timeZone"                              ]
    if ( "maxAttendees"        in options                                  ) :
      maxAttendees       = options [ "maxAttendees"                          ]
    ##########################################################################
    try                                                                      :
      return self . Service . events ( ) . get                               (
        calendarId         = calendarId                                      ,
        eventId            = eventId                                         ,
        alwaysIncludeEmail = alwaysIncludeEmail                              ,
        timeZone           = timeZone                                        ,
        maxAttendees       = maxAttendees                      ) . execute ( )
    except googleapiclient . errors . HttpError as err                       :
      pass
    ##########################################################################
    return False
  ############################################################################
  ## -| Get |-
  ############################################################################
  ## +| Append |+
  ############################################################################
  def Append ( self , calendarId , Body = { } , options = { } )              :
    ##########################################################################
    if ( self . Service == None )                                            :
      return False
    ##########################################################################
    sendNotifications     = None
    maxAttendees          = None
    sendUpdates           = None
    supportsAttachments   = None
    conferenceDataVersion = None
    ##########################################################################
    if ( "sendNotifications"     in options                                ) :
      sendNotifications     = options [ "sendNotifications"                  ]
    if ( "maxAttendees"          in options                                ) :
      maxAttendees          = options [ "maxAttendees"                       ]
    if ( "sendUpdates"           in options                                ) :
      sendUpdates           = options [ "sendUpdates"                        ]
    if ( "supportsAttachments"   in options                                ) :
      supportsAttachments   = options [ "supportsAttachments"                ]
    if ( "conferenceDataVersion" in options                                ) :
      conferenceDataVersion = options [ "conferenceDataVersion"              ]
    ##########################################################################
    try                                                                      :
      return self . Service . events ( ) . insert                            (
        calendarId            = calendarId                                   ,
        body                  = Body                                         ,
        sendNotifications     = sendNotifications                            ,
        maxAttendees          = maxAttendees                                 ,
        sendUpdates           = sendUpdates                                  ,
        supportsAttachments   = supportsAttachments                          ,
        conferenceDataVersion = conferenceDataVersion          ) . execute ( )
    except googleapiclient . errors . HttpError as err                       :
      pass
    ##########################################################################
    return False
  ############################################################################
  ## -| Append |-
  ############################################################################
  ## +| Update |+
  ############################################################################
  def Update ( self , calendarId , eventId , Body = { } , options = { } )    :
    ##########################################################################
    if ( self . Service == None )                                            :
      return False
    ##########################################################################
    alwaysIncludeEmail    = None
    sendNotifications     = None
    maxAttendees          = None
    sendUpdates           = None
    supportsAttachments   = None
    conferenceDataVersion = None
    ##########################################################################
    if ( "alwaysIncludeEmail"    in options                                ) :
      alwaysIncludeEmail    = options [ "alwaysIncludeEmail"                 ]
    if ( "sendNotifications"     in options                                ) :
      sendNotifications     = options [ "sendNotifications"                  ]
    if ( "maxAttendees"          in options                                ) :
      maxAttendees          = options [ "maxAttendees"                       ]
    if ( "sendUpdates"           in options                                ) :
      sendUpdates           = options [ "sendUpdates"                        ]
    if ( "supportsAttachments"   in options                                ) :
      supportsAttachments   = options [ "supportsAttachments"                ]
    if ( "conferenceDataVersion" in options                                ) :
      conferenceDataVersion = options [ "conferenceDataVersion"              ]
    ##########################################################################
    try                                                                      :
      return self . Service . events ( ) . update                            (
        calendarId            = calendarId                                   ,
        eventId               = eventId                                      ,
        body                  = Body                                         ,
        alwaysIncludeEmail    = alwaysIncludeEmail                           ,
        sendNotifications     = sendNotifications                            ,
        sendUpdates           = sendUpdates                                  ,
        supportsAttachments   = supportsAttachments                          ,
        maxAttendees          = maxAttendees                                 ,
        conferenceDataVersion = conferenceDataVersion          ) . execute ( )
    except googleapiclient . errors . HttpError as err                       :
      pass
    ##########################################################################
    return False
  ############################################################################
  ## -| Update |-
  ############################################################################
  ## +| Delete |+
  ############################################################################
  def Delete ( self , calendarId , eventId , options = { } )                 :
    ##########################################################################
    if ( self . Service == None )                                            :
      return False
    ##########################################################################
    sendUpdates       = None
    sendNotifications = None
    ##########################################################################
    if ( "sendUpdates"       in options                                    ) :
      sendUpdates       = options [ "sendUpdates"                            ]
    if ( "sendNotifications" in options                                    ) :
      sendNotifications = options [ "sendNotifications"                      ]
    ##########################################################################
    try                                                                      :
      self . Service . events ( ) . delete                                   (
        calendarId         = calendarId                                      ,
        eventId            = eventId                                         ,
        sendUpdates        = sendUpdates                                     ,
        sendNotifications  = sendNotifications                 ) . execute ( )
      return True
    except googleapiclient . errors . HttpError as err                       :
      pass
    ##########################################################################
    return False
  ############################################################################
  ## -| Delete |-
  ############################################################################
  ## +| Watch |+
  ############################################################################
  def Watch ( self , calendarId , Body = { } , options = { } )               :
    ##########################################################################
    if ( self . Service == None )                                            :
      return False
    ##########################################################################
    maxAttendees            = None
    privateExtendedProperty = None
    q                       = None
    updatedMin              = None
    maxResults              = None
    timeMin                 = None
    orderBy                 = None
    singleEvents            = None
    timeMax                 = None
    syncToken               = None
    timeZone                = None
    pageToken               = None
    sharedExtendedProperty  = None
    showHiddenInvitations   = None
    alwaysIncludeEmail      = None
    iCalUID                 = None
    showDeleted             = None
    ##########################################################################
    if ( "maxAttendees"            in options                              ) :
      maxAttendees            = options [ "maxAttendees"                     ]
    if ( "privateExtendedProperty" in options                              ) :
      privateExtendedProperty = options [ "privateExtendedProperty"          ]
    if ( "q"                       in options                              ) :
      q                       = options [ "q"                                ]
    if ( "updatedMin"              in options                              ) :
      updatedMin              = options [ "updatedMin"                       ]
    if ( "maxResults"              in options                              ) :
      maxResults              = options [ "maxResults"                       ]
    if ( "timeMin"                 in options                              ) :
      timeMin                 = options [ "timeMin"                          ]
    if ( "orderBy"                 in options                              ) :
      orderBy                 = options [ "orderBy"                          ]
    if ( "singleEvents"            in options                              ) :
      singleEvents            = options [ "singleEvents"                     ]
    if ( "timeMax"                 in options                              ) :
      timeMax                 = options [ "timeMax"                          ]
    if ( "syncToken"               in options                              ) :
      syncToken               = options [ "syncToken"                        ]
    if ( "timeZone"                in options                              ) :
      timeZone                = options [ "timeZone"                         ]
    if ( "pageToken"               in options                              ) :
      pageToken               = options [ "pageToken"                        ]
    if ( "sharedExtendedProperty"  in options                              ) :
      sharedExtendedProperty  = options [ "sharedExtendedProperty"           ]
    if ( "showHiddenInvitations"   in options                              ) :
      showHiddenInvitations   = options [ "showHiddenInvitations"            ]
    if ( "alwaysIncludeEmail"      in options                              ) :
      alwaysIncludeEmail      = options [ "alwaysIncludeEmail"               ]
    if ( "iCalUID"                 in options                              ) :
      iCalUID                 = options [ "iCalUID"                          ]
    if ( "showDeleted"             in options                              ) :
      showDeleted             = options [ "showDeleted"                      ]
    ##########################################################################
    try                                                                      :
      return self . Service . events ( ) . watch                             (
        calendarId              = calendarId                                 ,
        body                    = Body                                       ,
        maxAttendees            = maxAttendees                               ,
        privateExtendedProperty = privateExtendedProperty                    ,
        q                       = q                                          ,
        updatedMin              = updatedMin                                 ,
        maxResults              = maxResults                                 ,
        timeMin                 = timeMin                                    ,
        orderBy                 = orderBy                                    ,
        singleEvents            = singleEvents                               ,
        timeMax                 = timeMax                                    ,
        syncToken               = syncToken                                  ,
        timeZone                = timeZone                                   ,
        pageToken               = pageToken                                  ,
        sharedExtendedProperty  = sharedExtendedProperty                     ,
        showHiddenInvitations   = showHiddenInvitations                      ,
        alwaysIncludeEmail      = alwaysIncludeEmail                         ,
        iCalUID                 = iCalUID                                    ,
        showDeleted             = showDeleted                  ) . execute ( )
    except googleapiclient . errors . HttpError as err                       :
      print ( str ( err ) )
    ##########################################################################
    return False
  ############################################################################
  ## -| Watch |-
  ############################################################################
  ## +| Stop |+
  ############################################################################
  def Stop ( self , id , resource , address )                                :
    ##########################################################################
    if ( self . Service == None )                                            :
      return False
    ##########################################################################
    try                                                                      :
      self . Service . channels ( ) . stop ( body =                          {
        "id"           : id                                                , \
        "type"         : "web_hook"                                        , \
        "address"      : address                                           , \
        "kind"         : "api#channel"                                     , \
        "resourceId"   : resource                                          , \
      }                                                        ) . execute ( )
      return True
    except googleapiclient . errors . HttpError as err                       :
      print ( str ( err ) )
    ##########################################################################
    return False
  ############################################################################
  ## -| Stop |-
  ############################################################################
