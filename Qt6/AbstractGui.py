# -*- coding: utf-8 -*-
##############################################################################
## GUI抽象介面
##############################################################################
import os
import sys
import getopt
import time
import requests
import threading
import gettext
import json
##############################################################################
from   opencc                              import OpenCC
from   googletrans                         import Translator
##############################################################################
import PySide6
from   PySide6                             import QtCore
from   PySide6                             import QtGui
from   PySide6                             import QtWidgets
##############################################################################
from   PySide6 . QtCore                    import *
from   PySide6 . QtGui                     import *
from   PySide6 . QtWidgets                 import *
##############################################################################
import mysql . connector
from   mysql . connector                   import Error
##############################################################################
import AITK
from   AITK . Database    . Query          import Query
from   AITK . Database    . Connection     import Connection
from   AITK . Database    . Pair           import Pair
from   AITK . Database    . Columns        import Columns
##############################################################################
from   AITK . Linguistics . Translator     import Translate
##############################################################################
from   AITK . Documents   . Name           import Name           as NameItem
from   AITK . Documents   . Name           import Naming         as Naming
from   AITK . Documents   . ParameterQuery import ParameterQuery as ParameterQuery
from   AITK . Documents   . Variables      import Variables      as VariableItem
##############################################################################
from   AITK . Calendars   . StarDate       import StarDate
##############################################################################
class AbstractGui            (                                             ) :
  ############################################################################
  def __init__               ( self                                        ) :
    ##########################################################################
    NOW  = StarDate          (                                               )
    NOW  . Now               (                                               )
    ##########################################################################
    self . Locality        = 1002
    self . Prepared        = False
    self . DB              = {                                               }
    self . Settings        = {                                               }
    self . Translations    = {                                               }
    self . Tables          = {                                               }
    self . Hosts           = {                                               }
    self . DBs             = {                                               }
    self . Languages       = {                                               }
    self . Menus           = {                                               }
    self . RunningCounter  = 0
    self . RunningMutex    = threading . Lock (                              )
    self . Gui             = None
    self . StayAlive       = True
    self . Drag            = None
    self . PassDragDrop    = True
    self . dragPoint       = None
    self . Dumping         = False
    self . focusState      = False
    self . CreatedDateTime = NOW . Stardate
    self . Speaker         = None
    self . PlanFunc        = None
    self . SaveSettings    = None
    self . EmptySet        = [ False , None                                  ]
    self . LocalIcons      = {                                               }
    self . LocalMsgs       = {                                               }
    self . LimitValues     = {                                               }
    self . AllowDrops      = {                                               }
    self . Functionalities = {                                               }
    self . GuiMutex        = threading . Lock (                              )
    self . RunningThreads  = [                                               ]
    self . WindowActions   = [                                               ]
    self . HandleActions   = [                                               ]
    self . DropInJSON      = {                                               }
    self . DropDispatchers = [ { "Mime"     : "division/uuids"               ,
                                 "Function" : "acceptDivisionDrop"           ,
                                 "Drop"     : "dropDivision"               } ,
                               { "Mime"     : "gender/uuids"                 ,
                                 "Function" : "acceptGenderDrop"             ,
                                 "Drop"     : "dropGender"                 } ,
                               { "Mime"     : "tag/uuids"                    ,
                                 "Function" : "acceptTagDrop"                ,
                                 "Drop"     : "dropTags"                   } ,
                               { "Mime"     : "language/uuids"               ,
                                 "Function" : "acceptLanguagesDrop"          ,
                                 "Drop"     : "dropLanguages"              } ,
                               { "Mime"     : "picture/uuids"                ,
                                 "Function" : "acceptPictureDrop"            ,
                                 "Drop"     : "dropPictures"               } ,
                               { "Mime"     : "gallery/uuids"                ,
                                 "Function" : "acceptGalleriesDrop"          ,
                                 "Drop"     : "dropGalleries"              } ,
                               { "Mime"     : "gallerygroup/uuids"           ,
                                 "Function" : "acceptGalleryGroupsDrop"      ,
                                 "Drop"     : "dropGalleryGroups"          } ,
                               { "Mime"     : "project/uuids"                ,
                                 "Function" : "acceptProjectsDrop"           ,
                                 "Drop"     : "dropProjects"               } ,
                               { "Mime"     : "task/uuids"                   ,
                                 "Function" : "acceptTasksDrop"              ,
                                 "Drop"     : "dropTasks"                  } ,
                               { "Mime"     : "event/uuids"                  ,
                                 "Function" : "acceptEventsDrop"             ,
                                 "Drop"     : "dropEvents"                 } ,
                               { "Mime"     : "period/uuids"                 ,
                                 "Function" : "acceptPeriodsDrop"            ,
                                 "Drop"     : "dropPeriods"                } ,
                               { "Mime"     : "people/uuids"                 ,
                                 "Function" : "acceptPeopleDrop"             ,
                                 "Drop"     : "dropPeople"                 } ,
                               { "Mime"     : "crowd/uuids"                  ,
                                 "Function" : "acceptCrowdsDrop"             ,
                                 "Drop"     : "dropCrowds"                 } ,
                               { "Mime"     : "document/uuids"               ,
                                 "Function" : "acceptDocumentsDrop"          ,
                                 "Drop"     : "dropDocuments"              } ,
                               { "Mime"     : "race/uuids"                   ,
                                 "Function" : "acceptRaceDrop"               ,
                                 "Drop"     : "dropRaces"                  } ,
                               { "Mime"     : "role/uuids"                   ,
                                 "Function" : "acceptRoleDrop"               ,
                                 "Drop"     : "dropRoles"                  } ,
                               { "Mime"     : "occupation/uuids"             ,
                                 "Function" : "acceptOccupationsDrop"        ,
                                 "Drop"     : "dropOccupations"            } ,
                               { "Mime"     : "organization/uuids"           ,
                                 "Function" : "acceptOrganizationsDrop"      ,
                                 "Drop"     : "dropOrganizations"          } ,
                               { "Mime"     : "organizationgroup/uuids"      ,
                                 "Function" : "acceptOrganizationGroupsDrop" ,
                                 "Drop"     : "dropOrganizationGroups"     } ,
                               { "Mime"     : "audio/uuids"                  ,
                                 "Function" : "acceptAudioDrop"              ,
                                 "Drop"     : "dropAudios"                 } ,
                               { "Mime"     : "video/uuids"                  ,
                                 "Function" : "acceptVideoDrop"              ,
                                 "Drop"     : "dropVideos"                 } ,
                               { "Mime"     : "album/uuids"                  ,
                                 "Function" : "acceptAlbumsDrop"             ,
                                 "Drop"     : "dropAlbums"                 } ,
                               { "Mime"     : "albumgroup/uuids"             ,
                                 "Function" : "acceptAlbumGroupsDrop"        ,
                                 "Drop"     : "dropAlbumGroups"            } ,
                               { "Mime"     : "vfragment/uuids"              ,
                                 "Function" : "acceptVFragmentsDrop"         ,
                                 "Drop"     : "dropVFragments"             } ,
                               { "Mime"     : "scenario/uuids"               ,
                                 "Function" : "acceptScenariosDrop"          ,
                                 "Drop"     : "dropScenarios"              } ,
                               { "Mime"     : "eyes/uuids"                   ,
                                 "Function" : "acceptEyesDrop"               ,
                                 "Drop"     : "dropEyes"                   } ,
                               { "Mime"     : "eyeshape/uuids"               ,
                                 "Function" : "acceptEyeShapeDrop"           ,
                                 "Drop"     : "dropEyeShapes"              } ,
                               { "Mime"     : "hairs/uuids"                  ,
                                 "Function" : "acceptHairsDrop"              ,
                                 "Drop"     : "dropHairs"                  } ,
                               { "Mime"     : "blood/uuids"                  ,
                                 "Function" : "acceptBloodDrop"              ,
                                 "Drop"     : "dropBloods"                 } ,
                               { "Mime"     : "sexuality/uuids"              ,
                                 "Function" : "acceptSexualityDrop"          ,
                                 "Drop"     : "dropSexuality"              } ,
                               { "Mime"     : "face/uuids"                   ,
                                 "Function" : "acceptFacesDrop"              ,
                                 "Drop"     : "dropFaces"                  } ,
                               { "Mime"     : "faceshape/uuids"              ,
                                 "Function" : "acceptFaceShapesDrop"         ,
                                 "Drop"     : "dropFaceShapes"             } ,
                               { "Mime"     : "itu/uuids"                    ,
                                 "Function" : "acceptItuDrop"                ,
                                 "Drop"     : "dropITU"                    } ,
                               { "Mime"     : "stellar/uuids"                ,
                                 "Function" : "acceptStellarsDrop"           ,
                                 "Drop"     : "dropStellars"               } ,
                               { "Mime"     : "celestial/uuids"              ,
                                 "Function" : "acceptCelestialsDrop"         ,
                                 "Drop"     : "dropCelestials"             } ,
                               { "Mime"     : "place/uuids"                  ,
                                 "Function" : "acceptPlacesDrop"             ,
                                 "Drop"     : "dropPlaces"                 } ,
                               { "Mime"     : "position/uuids"               ,
                                 "Function" : "acceptPositionDrop"           ,
                                 "Drop"     : "dropPositions"              } ,
                               { "Mime"     : "nation/uuids"                 ,
                                 "Function" : "acceptNationsDrop"            ,
                                 "Drop"     : "dropNations"                } ,
                               { "Mime"     : "sexposition/uuids"            ,
                                 "Function" : "acceptSexPositionsDrop"       ,
                                 "Drop"     : "dropSexPositions"           } ,
                               { "Mime"     : "equation/uuids"               ,
                                 "Function" : "acceptEquationsDrop"          ,
                                 "Drop"     : "dropEquations"              } ,
                               { "Mime"     : "meridian/uuids"               ,
                                 "Function" : "acceptMeridiansDrop"          ,
                                 "Drop"     : "dropMeridians"              } ,
                               { "Mime"     : "acupuncture/uuids"            ,
                                 "Function" : "acceptAcupuncturesDrop"       ,
                                 "Drop"     : "dropAcupunctures"           } ]
    ##########################################################################
    return
  ############################################################################
  def __del__     ( self                                                   ) :
    ##########################################################################
    for th in self . RunningThreads                                          :
      ########################################################################
      try                                                                    :
        th . join (                                                          )
      except                                                                 :
        pass
    ##########################################################################
    return
  ############################################################################
  def DoProcessEvents    ( self                                            ) :
    ##########################################################################
    qApp . processEvents (                                                   )
    ##########################################################################
    return
  ############################################################################
  def isThreadRunning ( self                                               ) :
    ##########################################################################
    for th in self . RunningThreads                                          :
      ########################################################################
      if              ( th . is_alive ( )                                  ) :
        return True
    ##########################################################################
    return False
  ############################################################################
  def PushRunnings                  ( self                                 ) :
    ##########################################################################
    self . RunningMutex   . acquire (                                        )
    self . RunningCounter = int     ( self . RunningCounter + 1              )
    self . RunningMutex   . release (                                        )
    ##########################################################################
    return
  ############################################################################
  def PopRunnings                   ( self                                 ) :
    ##########################################################################
    self . RunningMutex   . acquire (                                        )
    self . RunningCounter = int     ( self . RunningCounter - 1              )
    self . RunningMutex   . release (                                        )
    ##########################################################################
    return
  ############################################################################
  def AnythingRunning ( self                                               ) :
    return            ( self . RunningCounter > 0                            )
  ############################################################################
  def isBitMask          ( self , a , b                                    ) :
    return               ( ( a & b ) == b                                    )
  ############################################################################
  def JsonToByteArray    ( self , jsox                                     ) :
    ##########################################################################
    S = json . dumps     ( jsox , ensure_ascii = False                       )
    B = S    . encode    ( "utf-8"                                           )
    ##########################################################################
    return QByteArray    ( B                                                 )
  ############################################################################
  def assureString       ( self , pb                                       ) :
    ##########################################################################
    BB   = pb
    ##########################################################################
    try                                                                      :
      BB = BB . decode   ( "utf-8"                                           )
    except                                                                   :
      pass
    ##########################################################################
    return BB
  ############################################################################
  def ByteArrayToJson    ( self , qbyte                                    ) :
    ##########################################################################
    if                   ( qbyte == None                                   ) :
      return             {                                                   }
    ##########################################################################
    try                                                                      :
      BB = qbyte . data  (                                                   )
    except                                                                   :
      return             {                                                   }
    ##########################################################################
    if                   ( BB == None                                      ) :
      return             {                                                   }
    ##########################################################################
    if                   ( len ( BB ) <= 0                                 ) :
      return             {                                                   }
    ##########################################################################
    try                                                                      :
      SS = BB . decode   ( "utf-8"                                           )
    except                                                                   :
      return             {                                                   }
    ##########################################################################
    try                                                                      :
      JX = json . loads  ( SS                                                )
    except                                                                   :
      return             {                                                   }
    ##########################################################################
    return JX
  ############################################################################
  def IsOkay             ( self , value                                    ) :
    return               ( value not in [ False , None ]                     )
  ############################################################################
  def NotOkay            ( self , value                                    ) :
    return               ( value in [ False , None ]                         )
  ############################################################################
  def isPrepared         ( self                                            ) :
    return self . Prepared
  ############################################################################
  def setPrepared        ( self , prepared                                 ) :
    self . Prepared = prepared
    return self . Prepared
  ############################################################################
  def getLocality        ( self                                            ) :
    return self . Locality
  ############################################################################
  def getLocalityUuid                ( self                                ) :
    return 1900000000000000000 + int ( self . Locality                       )
  ############################################################################
  def setLocality        ( self , locality                                 ) :
    ##########################################################################
    self . Locality = locality
    ##########################################################################
    return self . Locality
  ############################################################################
  def setLocalityUuid         ( self , UUID                                ) :
    ##########################################################################
    UUIDSEGS  = 1900000000000000000
    UUIDENDS  = UUIDSEGS + 10000000
    ##########################################################################
    if                        ( UUID < 1900000000000000000                 ) :
      return
    ##########################################################################
    if                        ( UUID > UUIDENDS                            ) :
      return
    ##########################################################################
    return self . setLocality ( int ( UUID - UUIDSEGS )                      )
  ############################################################################
  def GetLocalityByUuid   ( self , DB , TABLE , UUID , TYPE , SCOPE        ) :
    ##########################################################################
    PQ = ParameterQuery   ( TYPE , 89   , SCOPE , TABLE                      )
    RR = PQ . Value       ( DB   , UUID , "Language"                         )
    ##########################################################################
    if                    ( len ( str ( RR ) ) <= 0                        ) :
      return
    ##########################################################################
    self . Locality = int ( RR                                               )
    ##########################################################################
    return
  ############################################################################
  def SetLocalityByUuid   ( self , DB , TABLE , UUID , TYPE , SCOPE        ) :
    ##########################################################################
    PQ = ParameterQuery   ( TYPE , 89   , SCOPE , TABLE                      )
    PQ . assureValue      (        DB , UUID , "Language" , self . Locality  )
    ##########################################################################
    return
  ############################################################################
  def setLanguages       ( self , languages                                ) :
    ##########################################################################
    self . Languages = languages
    ##########################################################################
    return self . Languages
  ############################################################################
  def getLanguages       ( self                                            ) :
    return self . Languages
  ############################################################################
  def setFunction                 ( self , Id , enabled                    ) :
    ##########################################################################
    self . Functionalities [ Id ] = enabled
    ##########################################################################
    return self . Functionalities [ Id                                       ]
  ############################################################################
  def isFunction                  ( self , Id                              ) :
    ##########################################################################
    if                            ( Id not in self . Functionalities       ) :
      return False
    ##########################################################################
    return self . Functionalities [ Id                                       ]
  ############################################################################
  def setMenus           ( self , menus                                    ) :
    ##########################################################################
    self . Menus = menus
    ##########################################################################
    return self . Menus
  ############################################################################
  def getMenus           ( self                                            ) :
    return self . Menus
  ############################################################################
  def getMenuItem        ( self , item                                     ) :
    return self . Menus  [ item                                              ]
  ############################################################################
  def setPlanFunction       ( self , func                                  ) :
    ##########################################################################
    self . PlanFunc = func
    ##########################################################################
    return
  ############################################################################
  def hasPlan               ( self                                         ) :
    return                  ( self . PlanFunc != None                        )
  ############################################################################
  def GetPlan               ( self                                         ) :
    ##########################################################################
    if                      ( not self . hasPlan ( )                       ) :
      return None
    ##########################################################################
    return self . PlanFunc  (                                                )
  ############################################################################
  def GetRecognizer    ( self                                              ) :
    ##########################################################################
    p = self . GetPlan (                                                     )
    ##########################################################################
    if                 ( p in self . EmptySet                              ) :
      return None
    ##########################################################################
    return p . Recognizer
  ############################################################################
  def setLocalMessage       ( self , Id , message                          ) :
    self . LocalMsgs [ Id ] = message
    return self . LocalMsgs [ Id                                             ]
  ############################################################################
  def getLocalMessage       ( self , Id                                    ) :
    if                      ( Id not in self . LocalMsgs                   ) :
      return ""
    return self . LocalMsgs [ Id                                             ]
  ############################################################################
  def setLocalIcon           ( self , Id , icon                            ) :
    self . LocalIcons [ Id ] = icon
    return self . LocalIcons [ Id                                            ]
  ############################################################################
  def getLocalIcon           ( self , Id                                   ) :
    if                       ( Id not in self . LocalIcons                 ) :
      return None
    return self . LocalIcons [ Id                                            ]
  ############################################################################
  def isDrag                 ( self                                        ) :
    return                   ( self . Drag != None                           )
  ############################################################################
  def ReleaseDrag            ( self                                        ) :
    self . Drag = None
    return
  ############################################################################
  def setAllowDrops          ( self , IDs                                  ) :
    ##########################################################################
    for ID in IDs                                                            :
      self . setAllowDrop    ( ID , True                                     )
    ##########################################################################
    return
  ############################################################################
  def setAllowDrop           ( self , Id , enabled                         ) :
    self . AllowDrops [ Id ] = enabled
    return self . AllowDrops [ Id                                            ]
  ############################################################################
  def getAllowDrop           ( self , Id                                   ) :
    if                       ( Id not in self . AllowDrops                 ) :
      return False
    return self . AllowDrops [ Id                                            ]
  ############################################################################
  def statusMessage       ( self , message , timeout = 0                   ) :
    ##########################################################################
    if                    ( not self . hasPlan ( )                         ) :
      return
    ##########################################################################
    F   = self . PlanFunc (                                                  )
    if                    ( F . statusMessage is None                      ) :
      return
    ##########################################################################
    F . statusMessage     ( message , timeout                                )
    ##########################################################################
    return
  ############################################################################
  def LockGui                 ( self                                       ) :
    self . GuiMutex . acquire (                                              )
    return
  ############################################################################
  def UnlockGui               ( self                                       ) :
    self . GuiMutex . release (                                              )
    return
  ############################################################################
  def Bustle               ( self                                          ) :
    ##########################################################################
    if                     ( self . Gui == None                            ) :
      return False
    ##########################################################################
    self . LockGui         (                                                 )
    self . Gui . setCursor ( Qt . WaitCursor                                 )
    ##########################################################################
    return True
  ############################################################################
  def Vacancy              ( self                                          ) :
    ##########################################################################
    if                     ( self . Gui == None                            ) :
      return False
    ##########################################################################
    self . Gui . setCursor ( Qt . ArrowCursor                                )
    self . UnlockGui       (                                                 )
    ##########################################################################
    return True
  ############################################################################
  def Go                           ( self , func , arguments = ( )         ) :
    ##########################################################################
    if                             ( self . NotOkay ( func )               ) :
      return None
    ##########################################################################
    th   = threading . Thread      ( target = func , args = arguments        )
    th   . start                   (                                         )
    self . RunningThreads . append ( th                                      )
    ##########################################################################
    return th
  ############################################################################
  def Initialize         ( self , widget = None                            ) :
    ##########################################################################
    self . Gui          = widget
    ##########################################################################
    return
  ############################################################################
  def focusIn            ( self , event                                    ) :
    ##########################################################################
    if                   ( event . gotFocus ( )                            ) :
      if                 ( self  . FocusIn  ( )                            ) :
        ######################################################################
        event . accept   (                                                   )
        self  . focusState = True
        ######################################################################
        return True
    ##########################################################################
    return False
  ############################################################################
  def focusOut           ( self , event                                    ) :
    ##########################################################################
    if                   ( event . lostFocus ( )                           ) :
      if                 ( self  . FocusOut  ( )                           ) :
        ######################################################################
        event . accept   (                                                   )
        self  . focusState = False
        ######################################################################
        return True
    ##########################################################################
    return False
  ############################################################################
  def FocusIn                 ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def FocusOut                ( self                                       ) :
    raise NotImplementedError (                                              )
  ############################################################################
  def AssignDB           ( self , name , DBX                               ) :
    self . DBs [ name ] = DBX
    return DBX
  ############################################################################
  def GetDB                     ( self , name                              ) :
    ##########################################################################
    if                          ( name not in self . DBs                   ) :
      return
    ##########################################################################
    return self . DBs           [ name                                       ]
  ############################################################################
  def CloseDB                   ( self , name                              ) :
    ##########################################################################
    if                          ( name not in self . DBs                   ) :
      return
    ##########################################################################
    self . DBs [ name ] . Close (                                            )
    ##########################################################################
    del self . DBs              [ name                                       ]
    ##########################################################################
    return
  ############################################################################
  def ConnectHost        ( self , name , UsePure = False                   ) :
    ##########################################################################
    if                   ( name not in self . Hosts                        ) :
      return None
    ##########################################################################
    DBX = self . Hosts   [ name                                              ]
    ##########################################################################
    DB  = Connection     (                                                   )
    if                   ( not DB . ConnectTo ( DBX , UsePure )            ) :
      return None
    DB  . Prepare        (                                                   )
    ##########################################################################
    return DB
  ############################################################################
  def ConnectDB          ( self , UsePure = False                          ) :
    ##########################################################################
    DB = Connection      (                                                   )
    if                   ( not DB . ConnectTo ( self . DB , UsePure )      ) :
      return None
    DB . Prepare         (                                                   )
    ##########################################################################
    return DB
  ############################################################################
  def GetNameByLocality ( self                                             , \
                          DB                                               , \
                          TABLE                                            , \
                          Uuid                                             , \
                          Locality                                         , \
                          Usage = "Default"                                ) :
    ##########################################################################
    N     = Naming      (        DB , TABLE , Uuid  , Locality , Usage       )
    ##########################################################################
    return self . assureString ( N                                           )
  ############################################################################
  def GetName                       ( self                                 , \
                                      DB                                   , \
                                      TABLE                                , \
                                      Uuid                                 , \
                                      Usage = "Default"                    ) :
    return self . GetNameByLocality ( DB                                   , \
                                      TABLE                                , \
                                      Uuid                                 , \
                                      self . Locality                      , \
                                      Usage                                  )
  ############################################################################
  def AssureUuidNameByLocality ( self                                      , \
                                 DB                                        , \
                                 TABLE                                     , \
                                 Uuid                                      , \
                                 Name                                      , \
                                 Locality                                  , \
                                 Usage = "Default"                         ) :
    ##########################################################################
    N   = NameItem             (                                             )
    ##########################################################################
    S   = self . assureString  ( Name                                        )
    ##########################################################################
    N   . set                  ( "uuid"     , Uuid                           )
    N   . set                  ( "locality" , Locality                       )
    N   . setRelevance         ( Usage                                       )
    N   . set                  ( "name"     , S                              )
    ##########################################################################
    N   . Assure               ( DB         , TABLE                          )
    ##########################################################################
    return True
  ############################################################################
  def AssureUuidName ( self , DB , TABLE , Uuid , Name , Usage = "Default" ) :
    ##########################################################################
    return self . AssureUuidNameByLocality ( DB                            , \
                                             TABLE                         , \
                                             Uuid                          , \
                                             Name                          , \
                                             self . getLocality ( )        , \
                                             Usage                           )
  ############################################################################
  def GetNames      ( self , DB , TABLE , UUIDs , Usage = "Default"        ) :
    ##########################################################################
    NAMEs         = {                                                        }
    for U in UUIDs                                                           :
      NAMEs [ U ] = self . GetName ( DB , TABLE , U , Usage                  )
    ##########################################################################
    return NAMEs
  ############################################################################
  def setSpeaker         ( self , speaker                                  ) :
    self . Speaker = speaker
    return
  ############################################################################
  def canSpeak           ( self                                            ) :
    return               ( self . Speaker != None                            )
  ############################################################################
  def LocalityToGoogleLC ( self , LID                                      ) :
    ##########################################################################
    ## English
    ##########################################################################
    if                   ( LID == 1001                                     ) :
      return "en"
    ##########################################################################
    ## 正體中文
    ##########################################################################
    if                   ( LID == 1002                                     ) :
      return "zh-TW"
    ##########################################################################
    ## 简体中文
    ##########################################################################
    if                   ( LID == 1003                                     ) :
      return "zh-CN"
    ##########################################################################
    ## 日本語
    ##########################################################################
    if                   ( LID == 1006                                     ) :
      return "ja"
    ##########################################################################
    ## Français
    ##########################################################################
    if                   ( LID == 1007                                     ) :
      return "fr"
    ##########################################################################
    ## Deutsche
    ##########################################################################
    if                   ( LID == 1008                                     ) :
      return "de"
    ##########################################################################
    ## Español
    ##########################################################################
    if                   ( LID == 1009                                     ) :
      return "es"
    ##########################################################################
    ## русский
    ##########################################################################
    if                   ( LID == 1010                                     ) :
      return "ru"
    ##########################################################################
    return ""
  ############################################################################
  def Talk         ( self , message , locality                             ) :
    ##########################################################################
    if             ( self . Speaker == None                                ) :
      return
    ##########################################################################
    LC   = ""
    MAPS =         { 1001 : "en-US"                                          ,
                     1002 : "zh-TW"                                          ,
                     1003 : "zh-CN"                                          ,
                     1004 : "zh-TW"                                          ,
                     1005 : "zh-TW"                                          ,
                     1006 : "jp-JP"                                          ,
                     1007 : "fr-FR"                                          ,
                     1008 : "de-DE"                                          ,
                     1009 : "es-ES"                                          ,
                     1010 : "ru-RU"                                          }
    ##########################################################################
    if ( ( locality >= 1001 ) and ( locality <= 1010 ) )                     :
      LC = MAPS    [ locality                                                ]
    ##########################################################################
    VAL  =         ( message , LC ,                                          )
    self . Go      ( self . Speaker , VAL                                    )
    ## self . Speaker ( message , LC                                            )
    ##########################################################################
    return
  ############################################################################
  def LinkAction             ( self , Id , method , enable = True          ) :
    ##########################################################################
    plan = self . GetPlan    (                                               )
    if                       ( plan == None                                ) :
      return False
    ##########################################################################
    if                       ( plan . hasShortcut ( Id )                   ) :
      plan . connectShortcut ( Id , method                                   )
    elif                     ( plan . hasAction   ( Id )                   ) :
      plan . connectAction   ( Id , method , enable                          )
    else                                                                     :
      return False
    ##########################################################################
    return True
  ############################################################################
  def setActionLabel         ( self , Id , message                         ) :
    ##########################################################################
    plan = self . GetPlan    (                                               )
    if                       ( plan == None                                ) :
      return
    ##########################################################################
    if                       ( plan . hasAction   ( Id )                   ) :
      label = plan . Action  ( Id                                            )
      label . setText        ( message                                       )
    ##########################################################################
    return
  ############################################################################
  def ShowStatus                      ( self , message , timeout = 0       ) :
    return
  ############################################################################
  def BlobToString               ( self , BLOB                             ) :
    ##########################################################################
    if                           ( isinstance ( BLOB , bytearray )         ) :
      BLOB = bytes               ( BLOB                                      )
    ##########################################################################
    return self . assureString   ( BLOB                                      )
  ############################################################################
  def hasDragItem            ( self                                        ) :
    return False
  ############################################################################
  def dragStart              ( self , mouseEvent                           ) :
    ##########################################################################
    self . dragPoint = mouseEvent . pos ( )
    ##########################################################################
    return
  ############################################################################
  def fetchDrag              ( self , mouseEvent                           ) :
    return False
  ############################################################################
  def dragMoving             ( self , mouseEvent                           ) :
    ##########################################################################
    if                       ( self . Drag == None                         ) :
      return False
    ##########################################################################
    if ( not self . isBitMask ( mouseEvent.buttons ( ) , Qt.LeftButton )   ) :
      return False
    ##########################################################################
    if                       ( not self . hasDragItem ( )                  ) :
      return False
    ##########################################################################
    if                       ( not self . fetchDrag ( mouseEvent )         ) :
      return False
    ##########################################################################
    mime   = self . dragMime (                                               )
    ##########################################################################
    if                       ( mime == None                                ) :
      return True
    ##########################################################################
    DC               = QCursor       ( Qt . ClosedHandCursor                 )
    self   . Dumping = True
    self   . Drag    = QDrag         ( self . Gui                            )
    self   . Drag    . setMimeData   ( mime                                  )
    ##########################################################################
    if                       ( mime . hasImage ( )                         ) :
      image = mime . imageData       (                                       )
      self  . Drag . setPixmap       ( QPixmap . fromImage ( image )         )
    else                                                                     :
      self  . Drag . setPixmap       ( DC . pixmap ( )                       )
    ##########################################################################
    dropAction = self . Drag . exec_ ( Qt . CopyAction | Qt . MoveAction     )
    self   . dragDone                ( dropAction , mime                     )
    self   . Dumping = False
    ##########################################################################
    return True
  ############################################################################
  def dragEnd                ( self , mouseEvent                           ) :
    ##########################################################################
    if                       ( not self . finishDrag ( mouseEvent )        ) :
      return True
    ##########################################################################
    if                       ( not self . PassDragDrop                     ) :
      return True
    ##########################################################################
    return False
  ############################################################################
  def dragDone               ( self , dropIt , mime                        ) :
    ##########################################################################
    if                       ( self . Gui != None                          ) :
      self . Gui . setCursor ( Qt . ArrowCursor                              )
    ##########################################################################
    self . DoProcessEvents   (                                               )
    ##########################################################################
    return
  ############################################################################
  def finishDrag             ( self , mouseEvent                           ) :
    return True
  ############################################################################
  def dragMime               ( self                                        ) :
    return None
  ############################################################################
  def acceptDrop             ( self , sourceWidget , mimeData              ) :
    return False
  ############################################################################
  def dropNew                ( self , sourceWidget , mimeData , mousePos   ) :
    return False
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return False
  ############################################################################
  def dropAppend             ( self , sourceWidget , mimeData , mousePos   ) :
    return False
  ############################################################################
  def removeDrop             ( self                                        ) :
    return False
  ############################################################################
  def dragEnter                   ( self , dragEvent                       ) :
    ##########################################################################
    source = dragEvent . source   (                                          )
    mime   = dragEvent . mimeData (                                          )
    pos    = dragEvent . pos      (                                          )
    ##########################################################################
    if ( not self . acceptDrop ( source , mime       )                     ) :
      return False
    ##########################################################################
    if ( not self . dropNew    ( source , mime , pos )                     ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def dragMove                        ( self , dragMoveEvent               ) :
    ##########################################################################
    source = dragMoveEvent . source   (                                      )
    mime   = dragMoveEvent . mimeData (                                      )
    pos    = dragMoveEvent . pos      (                                      )
    ##########################################################################
    if ( not self . acceptDrop ( source , mime       )                     ) :
      return False
    ##########################################################################
    if ( not self . dropMoving ( source , mime , pos )                     ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def dropIn                 ( self , dropEvent                            ) :
    ##########################################################################
    source = dropEvent . source   (                                          )
    mime   = dropEvent . mimeData (                                          )
    pos    = dropEvent . pos      (                                          )
    ##########################################################################
    if ( not self . acceptDrop ( source , mime       )                     ) :
      return False
    ##########################################################################
    if ( not self . dropAppend ( source , mime , pos )                     ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def JsonFromMime           ( self , mime , mimetype                      ) :
    ##########################################################################
    QB    = mime . data      ( mimetype                                      )
    if                       ( QB . size ( ) <= 0                          ) :
      return                 {                                               }
    ##########################################################################
    try                                                                      :
      BDATA = QB    . data   (                                               )
      QDATA = BDATA . decode ( "utf-8"                                       )
      JSOX  = json  . loads  ( QDATA                                         )
    except                                                                   :
      return                 {                                               }
    ##########################################################################
    return JSOX
  ############################################################################
  def MimeType               ( self , mime , formats                       ) :
    ##########################################################################
    mimes  = formats . split ( ";"                                           )
    if                       ( len ( mimes ) <= 0                          ) :
      return ""
    ##########################################################################
    for mtype in mimes                                                       :
      data = mime . data     ( mtype                                         )
      if ( ( data != None ) and ( data . size ( ) > 0 )                    ) :
        return mtype
    ##########################################################################
    return ""
  ############################################################################
  def MimeTypeFromFormats  ( self , mime , formats                         ) :
    return self . MimeType (        mime , ";" . join ( formats )            )
  ############################################################################
  def allowedMimeTypes        ( self , mime                                ) :
    return ""
  ############################################################################
  def setMime                     ( self , mime , mtype , jsox             ) :
    ##########################################################################
    B    = self . JsonToByteArray ( jsox                                     )
    mime . setData                ( mtype , B                                )
    ##########################################################################
    return
  ############################################################################
  def CallMimeHandler           ( self , CanDo , widget , func             ) :
    ##########################################################################
    if                          ( not CanDo                                ) :
      return False
    ##########################################################################
    Caller = getattr            ( widget , func , None                       )
    if                          ( callable ( Caller )                      ) :
      return Caller             (                                            )
    ##########################################################################
    return False
  ############################################################################
  def CallDropHandler             ( self , mime , mimetype , widget , func ) :
    return self . CallMimeHandler ( mime . hasFormat ( mimetype )          , \
                                    widget                                 , \
                                    func                                     )
  ############################################################################
  def dropHandler                   ( self , source , widget , mime        ) :
    ##########################################################################
    for dropItem in self . DropDispatchers                                   :
      ########################################################################
      MT   = dropItem               [ "Mime"                                 ]
      MF   = dropItem               [ "Function"                             ]
      AT   = self . CallDropHandler ( mime , MT , widget , MF                )
      ########################################################################
      if                            ( AT                                   ) :
        return True
    ##########################################################################
    AT     = self . CallMimeHandler ( mime . hasImage ( )                  , \
                                      widget                               , \
                                      "acceptImageDrop"                      )
    if                              ( AT                                   ) :
      return True
    ##########################################################################
    AT     = self . CallMimeHandler ( mime . hasText  ( )                  , \
                                      widget                               , \
                                      "acceptTextDrop"                       )
    if                              ( AT                                   ) :
      return True
    ##########################################################################
    AT     = self . CallMimeHandler ( mime . hasHtml  ( )                  , \
                                      widget                               , \
                                      "acceptHtmlDrop"                       )
    if                              ( AT                                   ) :
      return True
    ##########################################################################
    AT     = self . CallMimeHandler ( mime . hasUrls  ( )                  , \
                                      widget                               , \
                                      "acceptUrlsDrop"                       )
    if                              ( AT                                   ) :
      return True
    ##########################################################################
    AT     = self . CallMimeHandler ( mime . hasColor ( )                  , \
                                      widget                               , \
                                      "acceptColorDrop"                      )
    if                              ( AT                                   ) :
      return True
    ##########################################################################
    if ( self . acceptPrivate ( source , widget , mime ) )                   :
      return True
    ##########################################################################
    return False
  ############################################################################
  def acceptPrivate                 ( self , source , widget , mime        ) :
    return False
  ############################################################################
  def RegularDropNew                ( self , mimeData                      ) :
    ##########################################################################
    self  . DropInJSON =            {                                        }
    mtype = self . allowedMimeTypes ( mimeData                               )
    if                              ( len ( mtype ) <= 0                   ) :
      return False
    ##########################################################################
    JSOX  = self . JsonFromMime     ( mimeData , mtype                       )
    if                              ( "Widget" not in JSOX                 ) :
      return False
    if                              ( "UUIDs"  not in JSOX                 ) :
      return False
    ##########################################################################
    if                              ( len ( JSOX [ "UUIDs" ] ) <= 0        ) :
      return False
    ##########################################################################
    self  . DropInJSON = JSOX
    self  . DropInJSON [ "Mime" ] = mtype
    ##########################################################################
    return True
  ############################################################################
  def CallDropItems  ( self , widget , func , source , pos , JSOX          ) :
    ##########################################################################
    Caller = getattr ( widget , func , None                                  )
    if               ( callable ( Caller )                                 ) :
      return Caller  (               source , pos , JSOX                     )
    ##########################################################################
    return False
  ############################################################################
  def HandleDropInImage      ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    widget = self . Gui
    ##########################################################################
    AT     = self . CallMimeHandler ( mimeData . hasImage ( )              , \
                                      widget                               , \
                                      "acceptImageDrop"                      )
    if                              ( not AT                               ) :
      return True , False
    ##########################################################################
    Caller = getattr                ( widget , "dropImage" , None            )
    if                              ( callable ( Caller )                  ) :
      ########################################################################
      img  = mimeData . imageData   (                                        )
      R    = Caller                 ( sourceWidget , mousePos , img          )
      ########################################################################
      return False , R
    ##########################################################################
    return True , False
  ############################################################################
  def HandleDropInText       ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    widget = self . Gui
    ##########################################################################
    AT     = self . CallMimeHandler ( mimeData . hasText  ( )              , \
                                      widget                               , \
                                      "acceptTextDrop"                       )
    if                              ( not AT                               ) :
      return True , False
    ##########################################################################
    Caller = getattr                ( widget , "dropText" , None             )
    if                              ( callable ( Caller )                  ) :
      ########################################################################
      txt  = mimeData . text        (                                        )
      R    = Caller                 ( sourceWidget , mousePos , txt          )
      ########################################################################
      return False , R
    ##########################################################################
    return True , False
  ############################################################################
  def HandleDropInHtml       ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    widget = self . Gui
    ##########################################################################
    AT     = self . CallMimeHandler ( mimeData . hasHtml  ( )              , \
                                      widget                               , \
                                      "acceptHtmlDrop"                       )
    if                              ( not AT                               ) :
      return True , False
    ##########################################################################
    Caller = getattr                ( widget , "dropHtml" , None             )
    if                              ( callable ( Caller )                  ) :
      ########################################################################
      html = mimeData . html        (                                        )
      R    = Caller                 ( sourceWidget , mousePos , html         )
      ########################################################################
      return False , R
    ##########################################################################
    return True , False
  ############################################################################
  def HandleDropInURLs       ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    widget = self . Gui
    ##########################################################################
    AT     = self . CallMimeHandler ( mimeData . hasUrls  ( )              , \
                                      widget                               , \
                                      "acceptUrlsDrop"                       )
    if                              ( not AT                               ) :
      return True , False
    ##########################################################################
    Caller = getattr                ( widget , "dropUrls" , None             )
    if                              ( callable ( Caller )                  ) :
      ########################################################################
      urls = mimeData . urls        (                                        )
      R    = Caller                 ( sourceWidget , mousePos , urls         )
      ########################################################################
      return False , R
    ##########################################################################
    return True , False
  ############################################################################
  def HandleDropInColor      ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    widget = self . Gui
    ##########################################################################
    AT     = self . CallMimeHandler ( mimeData . hasColor ( )              , \
                                      widget                               , \
                                      "acceptColorDrop"                      )
    if                              ( not AT                               ) :
      return True , False
    ##########################################################################
    Caller = getattr                ( widget , "dropColor" , None            )
    if                              ( callable ( Caller )                  ) :
      ########################################################################
      cld  = mimeData . colorData   (                                        )
      R    = Caller                 ( sourceWidget , mousePos , cld          )
      ########################################################################
      return False , R
    ##########################################################################
    return True , False
  ############################################################################
  def dropNormalItems        ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    Bypass , Result = self . HandleDropInImage ( sourceWidget              , \
                                                 mimeData                  , \
                                                 mousePos                    )
    if                               ( not Bypass                          ) :
      return Result
    ##########################################################################
    Bypass , Result = self . HandleDropInText  ( sourceWidget              , \
                                                 mimeData                  , \
                                                 mousePos                    )
    if                               ( not Bypass                          ) :
      return Result
    ##########################################################################
    Bypass , Result = self . HandleDropInHtml  ( sourceWidget              , \
                                                 mimeData                  , \
                                                 mousePos                    )
    if                               ( not Bypass                          ) :
      return Result
    ##########################################################################
    Bypass , Result = self . HandleDropInURLs  ( sourceWidget              , \
                                                 mimeData                  , \
                                                 mousePos                    )
    if                               ( not Bypass                          ) :
      return Result
    ##########################################################################
    Bypass , Result = self . HandleDropInColor ( sourceWidget              , \
                                                 mimeData                  , \
                                                 mousePos                    )
    if                               ( not Bypass                          ) :
      return Result
    ##########################################################################
    return False
  ############################################################################
  def dropItems              ( self , sourceWidget , mimeData , mousePos   ) :
    ##########################################################################
    widget = self . Gui
    mtype  = self . allowedMimeTypes ( mimeData                              )
    if                               ( len ( mtype ) <= 0                  ) :
      return self . dropNormalItems  ( sourceWidget , mimeData , mousePos    )
    ##########################################################################
    JSOX   = self . JsonFromMime     ( mimeData , mtype                      )
    if                               ( "Widget" not in JSOX                ) :
      return False
    if                               ( "UUIDs"  not in JSOX                ) :
      return False
    ##########################################################################
    for dropItem in self . DropDispatchers                                   :
      ########################################################################
      MT   = dropItem                [ "Mime"                                ]
      ########################################################################
      if                             ( MT != mtype                         ) :
        continue
      ########################################################################
      MF   = dropItem                [ "Function"                            ]
      DF   = dropItem                [ "Drop"                                ]
      AT   = self . CallDropHandler  ( mimeData , MT , widget , MF           )
      ########################################################################
      if                             ( not AT                              ) :
        continue
      ########################################################################
      CDI  = self . CallDropItems    ( widget                              , \
                                       DF                                  , \
                                       sourceWidget                        , \
                                       mousePos                            , \
                                       JSOX                                  )
      if                             ( not CDI                             ) :
        return False
      ########################################################################
      return True
    ##########################################################################
    return self   . dropNormalItems  ( sourceWidget , mimeData , mousePos    )
  ############################################################################
  def ObtainAllUuids             ( self , DB                               ) :
    return                       [                                           ]
  ############################################################################
  def AutoTranslateUUID                    ( self                          , \
                                             gt                            , \
                                             interval                      , \
                                             DB                            , \
                                             TABLE                         , \
                                             UUID                          ) :
    ##########################################################################
    LISTs      =                           [ 1001                          , \
                                             1002                          , \
                                             1003                          , \
                                             1006                          , \
                                             1007                          , \
                                             1008                          , \
                                             1009                          , \
                                             1010                            ]
    ##########################################################################
    KLISTs     =                           [ 1007                          , \
                                             1008                          , \
                                             1009                          , \
                                             1010                            ]
    ##########################################################################
    NAMEs      =                           {                                 }
    ##########################################################################
    for L in LISTs                                                           :
      K        = self . GetNameByLocality  ( DB , TABLE , UUID , L           )
      if                                   ( len ( K ) > 0                 ) :
        NAMEs [ L ] = K
    ##########################################################################
    if                                     ( 1002 not in NAMEs             ) :
      return
    ##########################################################################
    ## 由中文轉成簡體,日文,英文
    ##########################################################################
    TN         = NAMEs                     [ 1002                            ]
    if                                     ( len ( TN ) <= 0               ) :
      return
    ##########################################################################
    if                                     ( 1003 not in NAMEs             ) :
      ########################################################################
      cc       = OpenCC                    ( "t2s"                           )
      target   = cc . convert              ( TN                              )
      ########################################################################
      if                                   ( len ( target ) > 0            ) :
        ######################################################################
        NAMEs [ 1003 ] = target
        ######################################################################
        self . AssureUuidNameByLocality    ( DB                            , \
                                             TABLE                         , \
                                             UUID                          , \
                                             target                        , \
                                             1003                            )
    ##########################################################################
    zhTW       = self . LocalityToGoogleLC ( 1002                            )
    ##########################################################################
    for L in [ 1001 , 1006 ]                                                 :
      ########################################################################
      if                                   ( L in NAMEs                    ) :
        continue
      ########################################################################
      LC       = self . LocalityToGoogleLC ( L                               )
      target   = Translate                 ( TN , zhTW , LC                  )
      ########################################################################
      if                                  ( len ( target ) <= 0            ) :
        continue
      ########################################################################
      if ( ( L in [ 1001 ] ) and ( target == TN ) )                          :
        continue
      ########################################################################
      self . ShowStatus                   ( f"{LC} : {TN} => {target}"       )
      ########################################################################
      NAMEs [ L ] = target
      ########################################################################
      self . AssureUuidNameByLocality     ( DB                             , \
                                            TABLE                          , \
                                            UUID                           , \
                                            target                         , \
                                            L                                )
      ########################################################################
      if                                  ( interval > 0.01                ) :
        time . sleep                      ( interval                         )
    ##########################################################################
    ## 由英文轉成法文,德文,西班牙文,俄語
    ##########################################################################
    if                                    ( 1001 not in NAMEs              ) :
      return
    ##########################################################################
    EN        = NAMEs                     [ 1001                             ]
    if                                    ( len ( EN ) <= 0                ) :
      return
    ##########################################################################
    enUS      = self . LocalityToGoogleLC ( 1001                             )
    ##########################################################################
    for L in KLISTs                                                          :
      ########################################################################
      if                                  ( L in NAMEs                     ) :
        continue
      ########################################################################
      LC       = self . LocalityToGoogleLC ( L                               )
      target   = Translate                 ( EN , enUS , LC                  )
      ########################################################################
      if                                  ( len ( target ) <= 0            ) :
        continue
      ########################################################################
      if                                  ( target == TN                   ) :
        continue
      ########################################################################
      self . ShowStatus                   ( f"{LC} : {EN} => {target}"       )
      ########################################################################
      NAMEs [ L ] = target
      ########################################################################
      self . AssureUuidNameByLocality     ( DB                             , \
                                            TABLE                          , \
                                            UUID                           , \
                                            target                         , \
                                            L                                )
      ########################################################################
      if                                  ( interval > 0.01                ) :
        time . sleep                      ( interval                         )
    ##########################################################################
    return
  ############################################################################
  def DoAutoTranslation      ( self , DB , TABLE , UUID , FMT , interval   ) :
    ##########################################################################
    MSG  = FMT . format      ( UUID                                          )
    self . ShowStatus        ( MSG                                           )
    self . AutoTranslateUUID ( None , interval , DB , TABLE , UUID           )
    ##########################################################################
    return
  ############################################################################
  def DoTranslateAll               ( self , DB , TABLE , FMT , interval    ) :
    ##########################################################################
    UUIDs  = self . ObtainAllUuids ( DB                                      )
    if                             ( len ( UUIDs ) <= 0                    ) :
      return
    ##########################################################################
    ## DB     . LockWrites            ( [ TABLE ]                               )
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      MSG  = FMT . format          ( UUID                                    )
      self . ShowStatus            ( MSG                                     )
      ########################################################################
      self . AutoTranslateUUID     ( None , interval , DB , TABLE , UUID     )
    ##########################################################################
    ## DB     . UnlockTables          (                                         )
    ##########################################################################
    self   . ShowStatus            ( ""                                      )
    ##########################################################################
    return
  ############################################################################
  def GetEnumerations        ( self , DB , ENUTAB , NAMTAB , COLUMN , TYPE ) :
    ##########################################################################
    QQ    = f"""select `value`,`uuid` from {ENUTAB}
                where ( `type` = { TYPE } )
                  and ( `column` = '{COLUMN}' )
                order by `value` asc ;"""
    QQ    = " " . join       ( QQ . split ( )                                )
    DB    . Query            ( QQ                                            )
    ALL   = DB . FetchAll    (                                               )
    ##########################################################################
    if                       ( ALL in [ None , False ]                     ) :
      return                 {                                               }
    ##########################################################################
    if                       ( len ( ALL ) <= 0                            ) :
      return                 {                                               }
    ##########################################################################
    ENUMs =                  {                                               }
    for E in ALL                                                             :
      V   = int              ( E [ 0 ]                                       )
      U   = E                [ 1                                             ]
      N   = self . GetName   ( DB , NAMTAB , U                               )
      ENUMs [ V ] = N
    ##########################################################################
    return ENUMs
  ############################################################################
  def Notify                 ( self , Id                                   ) :
    ##########################################################################
    if                       ( not self . hasPlan ( )                      ) :
      return
    ##########################################################################
    p = self . GetPlan       (                                               )
    p . Notify               ( Id                                            )
    ##########################################################################
    return
  ############################################################################
  def DetachControl    ( self , widget                                     ) :
    ##########################################################################
    if                 ( not self . hasPlan ( )                            ) :
      return
    ##########################################################################
    p = self . GetPlan (                                                     )
    p . DetachControl  (        widget                                       )
    ##########################################################################
    return
  ############################################################################
  def addControl       ( self , name , widget , parent                     ) :
    ##########################################################################
    if                 ( not self . hasPlan ( )                            ) :
      return
    ##########################################################################
    p = self . GetPlan (                                                     )
    p . addControl     (        name , widget , parent                       )
    ##########################################################################
    return
  ############################################################################
  def SendIms                ( self , message , beau = "CIOS"              ) :
    ##########################################################################
    if                       ( not self . hasPlan ( )                      ) :
      return
    ##########################################################################
    p = self . GetPlan       (                                               )
    if                       ( p . IMS in [ False , None ]                 ) :
      return
    ##########################################################################
    p . IMS                  (        message , beau                         )
    ##########################################################################
    return
  ############################################################################
  def LinkVoice              ( self , func                                 ) :
    ##########################################################################
    if                       ( not self . hasPlan ( )                      ) :
      return
    ##########################################################################
    p = self . GetPlan       (                                               )
    p . LinkVoice            ( func                                          )
    ##########################################################################
    return
  ############################################################################
  def LimitValue              ( self , index                               ) :
    ##########################################################################
    if                        ( index not in self . LimitValues            ) :
      return 0
    ##########################################################################
    return self . LimitValues [ index                                        ]
  ############################################################################
  def setLimitValue           ( self , index , value                       ) :
    ##########################################################################
    self . LimitValues [ index ] = value
    ##########################################################################
    return
  ############################################################################
  def setSuggestion  ( self , size                                         ) :
    ##########################################################################
    self . LimitValues [ 1911010001 ] = size . width  (                      )
    self . LimitValues [ 1911010002 ] = size . height (                      )
    ##########################################################################
    return
  ############################################################################
  def SizeSuggestion ( self , size                                         ) :
    ##########################################################################
    s   = size
    ##########################################################################
    if               ( 1911010001 in self . LimitValues                    ) :
      s . setWidth   ( self . LimitValues [ 1911010001 ]                     )
    ##########################################################################
    if               ( 1911010002 in self . LimitValues                    ) :
      s . setHeight  ( self . LimitValues [ 1911010002 ]                     )
    ##########################################################################
    return s
  ############################################################################
  def setSizeSuggestion          ( self  , width , height                  ) :
    ##########################################################################
    self . LimitValues [ 1911010001 ] = width
    self . LimitValues [ 1911010002 ] = height
    ##########################################################################
    return self . SizeSuggestion ( QSize ( width , height )                  )
  ############################################################################
  def SaveOptions                ( self                                    ) :
    ##########################################################################
    if                           ( self . SaveSettings in [ False , None ] ) :
      return False
    ##########################################################################
    self . SaveSettings          ( self . Settings                           )
    ##########################################################################
    return True
  ############################################################################
  def skip ( self , msecs                                                  ) :
    ##########################################################################
    N = QDateTime . currentDateTime (                                        )
    ##########################################################################
    while  ( N . msecsTo( QDateTime . currentDateTime ( ) ) < msecs        ) :
      qApp . processEvents          (                                        )
      time . sleep                  ( 0.001                                  )
    ##########################################################################
    return
  ############################################################################
  def attacheStatusBar        ( self , widget , stretch = 0                ) :
    ##########################################################################
    if                        ( not self . hasPlan ( )                     ) :
      return False
    ##########################################################################
    p = self      . GetPlan   (                                              )
    p . statusBar . addWidget ( widget , stretch                             )
    ##########################################################################
    return True
  ############################################################################
  def menuFont              ( self                                         ) :
    ##########################################################################
    if                      ( self . Gui in [ False , None ]               ) :
      return QFont          (                                                )
    ##########################################################################
    fnt = self . Gui . font (                                                )
    fnt . setPointSize      ( 10                                             )
    ##########################################################################
    return fnt
  ############################################################################
  def doStartBusy      ( self                                              ) :
    ##########################################################################
    if                 ( not self . hasPlan ( )                            ) :
      return
    ##########################################################################
    p = self . GetPlan (                                                     )
    p . StartBusy      (                                                     )
    ##########################################################################
    return
  ############################################################################
  def doStopBusy       ( self                                              ) :
    ##########################################################################
    if                 ( not self . hasPlan ( )                            ) :
      return
    ##########################################################################
    p = self . GetPlan (                                                     )
    p . StopBusy       (                                                     )
    ##########################################################################
    return
  ############################################################################
  def GetRatioBox      ( self                                              ) :
    if                 ( not self . hasPlan ( )                            ) :
      return
    ##########################################################################
    p = self . GetPlan (                                                     )
    ##########################################################################
    return p . Ratio
  ############################################################################
  def DoSimpleSQLs ( self , DB , SQLs                                      ) :
    ##########################################################################
    for QQ in SQLs                                                           :
      ########################################################################
      try                                                                    :
        DB . Query ( QQ                                                      )
      except :
        pass
    ##########################################################################
    return
  ############################################################################
  def DoProgressSQLs            ( self , Title , DB , SQLs                 ) :
    ##########################################################################
    plan   = None
    if                          ( self . hasPlan ( )                       ) :
      plan = self . GetPlan     (                                            )
    ##########################################################################
    if                          ( plan in [ False , None ]                 ) :
      ########################################################################
      self . DoSimpleSQLs       ( DB , SQLs                                  )
      ########################################################################
      return
    ##########################################################################
    Total  = len                ( SQLs                                       )
    ##########################################################################
    NAME   = self . getMenuItem ( Title                                      )
    cFmt   = self . getMenuItem ( "SecsCounting"                             )
    rFmt   = self . getMenuItem ( "ItemCounting"                             )
    FMT    = self . getMenuItem ( "Percentage"                               )
    PID    = plan . Progress    ( NAME , FMT                                 )
    plan   . setFrequency       ( PID  , cFmt , rFmt                         )
    ##########################################################################
    plan   . setRange           ( PID , 0 , Total                            )
    plan   . Start              ( PID , 0 , True                             )
    plan   . ProgressReady      ( PID , 300                                  )
    ##########################################################################
    K      = 0
    while ( K < len ( SQLs ) ) and ( plan . isProgressRunning ( PID ) )      :
      ########################################################################
      SQL  = SQLs               [ K                                          ]
      plan . setProgressValue   ( PID , K                                    )
      ########################################################################
      DB   . Query              ( SQL                                        )
      ########################################################################
      K    = K + 1
    ##########################################################################
    plan   . Finish             ( PID                                        )
    ##########################################################################
    return
  ############################################################################
  def ExecuteSqlCommands    ( self , Title , DB , SQLs , Threshold         ) :
    ##########################################################################
    if                      ( len ( SQLs ) <= Threshold                    ) :
      ########################################################################
      self . DoSimpleSQLs   (                DB , SQLs                       )
      ########################################################################
      return
    ##########################################################################
    self   . DoProgressSQLs (        Title , DB , SQLs                       )
    ##########################################################################
    return
  ############################################################################
  def OrderingPUIDs           ( self , atUuid , UUIDs , PUIDs              ) :
    ##########################################################################
    atUuid    = int           ( atUuid                                       )
    UUIDs     = list          ( map ( int , UUIDs )                          )
    PUIDs     = list          ( map ( int , PUIDs )                          )
    ##########################################################################
    KUIDs     =               [                                              ]
    for UUID in PUIDs                                                        :
      if                      ( UUID not in UUIDs                          ) :
        KUIDs . append        ( UUID                                         )
    ##########################################################################
    if                        ( atUuid <= 0                                ) :
      for UUID in UUIDs                                                      :
        KUIDs . append        ( UUID                                         )
      return KUIDs
    ##########################################################################
    try                                                                      :
      ########################################################################
      atPos   = KUIDs . index ( atUuid                                       )
      ########################################################################
    except                                                                   :
      for UUID in UUIDs                                                      :
        KUIDs . append        ( UUID                                         )
      return KUIDs
    ##########################################################################
    if                        ( atPos <= 0                                 ) :
      for UUID in PUIDs                                                      :
        ######################################################################
        if                    ( UUID not in UUIDs                          ) :
          UUIDs . append      ( UUID                                         )
      return UUIDs
    ##########################################################################
    TOTAL     = len           ( KUIDs                                        )
    REMAIN    =               ( TOTAL - atPos                                )
    LEFTs     = KUIDs         [          : atPos                             ]
    RIGHTs    = KUIDs         [ - REMAIN :                                   ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      if                      ( UUID not in LEFTs                          ) :
        LEFTs . append        ( UUID                                         )
    ##########################################################################
    for UUID in RIGHTs                                                       :
      if                      ( UUID not in LEFTs                          ) :
        LEFTs . append        ( UUID                                         )
    ##########################################################################
    return LEFTs
  ############################################################################
  def ObtainsVariantTables   ( self                                        , \
                               DB                                          , \
                               VARTAB                                      , \
                               UUID                                        , \
                               TYPE                                        , \
                               NAME                                        , \
                               JSON                                        ) :
    ##########################################################################
    VARI   = VariableItem    (                                               )
    VARI   . Uuid = UUID
    VARI   . Type = TYPE
    VARI   . Name = NAME
    ##########################################################################
    BODY   = VARI . GetValue ( DB , VARTAB                                   )
    if                       ( BODY in [ False , None ]                    ) :
      return JSON
    ##########################################################################
    try                                                                      :
      BODY = BODY . decode   ( "utf-8"                                       )
    except                                                                   :
      pass
    ##########################################################################
    if                       ( len ( BODY ) <= 0                           ) :
      return JSON
    ##########################################################################
    try                                                                      :
      J    = json . loads    ( BODY                                          )
    except                                                                   :
      return JSON
    ##########################################################################
    JKS    = JSON . keys     (                                               )
    ##########################################################################
    for T in JKS                                                             :
      ########################################################################
      if                     ( T not in J                                  ) :
        J [ T ] = JSON       [ T                                             ]
    ##########################################################################
    return J
  ############################################################################
  def ObtainsOwnerVariantTables        ( self                              , \
                                         DB                                , \
                                         UUID                              , \
                                         TYPE                              , \
                                         NAME                              , \
                                         JSON                              ) :
    ##########################################################################
    VARTAB = self . Tables             [ "Variables"                         ]
    ##########################################################################
    return self . ObtainsVariantTables ( DB                                , \
                                         VARTAB                            , \
                                         UUID                              , \
                                         TYPE                              , \
                                         NAME                              , \
                                         JSON                                )
  ############################################################################
  def setVariable      ( self , key , value                                ) :
    ##########################################################################
    if                 ( not self . hasPlan ( )                            ) :
      return
    ##########################################################################
    p = self . GetPlan (                                                     )
    p . SystemVariables [ key ] = value
    ##########################################################################
    return
  ############################################################################
  def DbCountDepotTotal ( self , DB , QQ                                   ) :
    ##########################################################################
    DB  . Query         ( " " . join ( QQ . split (                      ) ) )
    ONE = DB . FetchOne (                                                    )
    ##########################################################################
    if                  ( ONE in self . EmptySet                           ) :
      return 0
    ##########################################################################
    if                  ( len ( ONE ) <= 0                                 ) :
      return 0
    ##########################################################################
    return int          ( ONE [ 0                                          ] )
  ############################################################################
  def FetchIconBlob                   ( self , DB , TABLE , PUID           ) :
    ##########################################################################
    QQ   = self . FetchThumbSqlSyntax ( TABLE , PUID                         )
    ##########################################################################
    return self . FetchIconBlobSql    ( DB , QQ                              )
  ############################################################################
  def FetchThumbSqlSyntax  ( self , TABLE , PUID                           ) :
    ##########################################################################
    WH   = f"where ( `usage` = 'ICON' ) and ( `uuid` = {PUID} )"
    OPTS = "order by `id` desc limit 0 , 1"
    QQ   = f"select `thumb` from {TABLE} {WH} {OPTS} ;"
    ##########################################################################
    return QQ
  ############################################################################
  def FetchIconBlobSql     ( self , DB , QQ                                ) :
    ##########################################################################
    DB     . Query         ( QQ                                              )
    THUMB  = DB . FetchOne (                                                 )
    ##########################################################################
    if                     ( THUMB == None                                 ) :
      return None
    ##########################################################################
    if                     ( len ( THUMB ) <= 0                            ) :
      return None
    ##########################################################################
    BLOB   = THUMB         [ 0                                               ]
    if                     ( isinstance ( BLOB , bytearray )               ) :
      BLOB = bytes         ( BLOB                                            )
    ##########################################################################
    if                     ( len ( BLOB ) <= 0                             ) :
      return None
    ##########################################################################
    return BLOB
  ############################################################################
  def BlobToImage      ( self , BLOB , FORMAT                              ) :
    ##########################################################################
    IMG = QImage       (                                                     )
    IMG . loadFromData ( QByteArray ( BLOB ) , FORMAT                        )
    ##########################################################################
    return IMG
  ############################################################################
  def ImageToIcon          ( self , IMAGE , SIZE = QSize ( 128 , 128 )     ) :
    ##########################################################################
    TSI = IMAGE . size     (                                                 )
    ICZ = QImage           ( SIZE , QImage . Format_ARGB32                   )
    ICZ . fill             ( QColor ( 255 , 255 , 255 )                      )
    ##########################################################################
    W   = int              ( ( SIZE . width  ( ) - TSI . width  ( ) ) / 2    )
    H   = int              ( ( SIZE . height ( ) - TSI . height ( ) ) / 2    )
    PTS = QPoint           ( W , H                                           )
    ##########################################################################
    p   = QPainter         (                                                 )
    p   . begin            ( ICZ                                             )
    p   . drawImage        ( PTS , IMAGE                                     )
    p   . end              (                                                 )
    ##########################################################################
    PIX = QPixmap          (                                                 )
    PIX . convertFromImage ( ICZ                                             )
    ##########################################################################
    return QIcon           ( PIX                                             )
  ############################################################################
  def FetchQIcon ( self , DB , TABLE , PUID , SIZE = QSize ( 128 , 128 )   ) :
    ##########################################################################
    BLOB = self . FetchIconBlob ( DB , TABLE , PUID                          )
    ##########################################################################
    if                          ( self . NotOkay ( BLOB )                  ) :
      return None
    ##########################################################################
    IMG  = self . BlobToImage   ( BLOB , "PNG"                               )
    ##########################################################################
    return self . ImageToIcon   ( IMG , SIZE                                 )
    ##########################################################################
    return
  ############################################################################
  def getSystemColor          ( self                                       ) :
    ##########################################################################
    if                        ( not self . hasPlan ( )                     ) :
      return QColor           ( 255 , 255 , 255                              )
    ##########################################################################
    p = self . GetPlan        (                                              )
    ##########################################################################
    return p . getSystemColor (                                              )
  ############################################################################
  def setSystemColor   ( self , color                                      ) :
    ##########################################################################
    if                 ( not self . hasPlan ( )                            ) :
      return False
    ##########################################################################
    p = self . GetPlan (                                                     )
    p . setSystemColor ( color                                               )
    ##########################################################################
    return True
  ############################################################################
  def getSearchLine           ( self                                       ) :
    ##########################################################################
    if                        ( not self . hasPlan ( )                     ) :
      return None
    ##########################################################################
    p = self . GetPlan        (                                              )
    ##########################################################################
    return p . SearchLine
  ############################################################################
  def getSearchLineText          ( self                                    ) :
    ##########################################################################
    if                           ( not self . hasPlan ( )                  ) :
      return ""
    ##########################################################################
    p = self . GetPlan           (                                           )
    ##########################################################################
    return p . SearchLine . text (                                           )
  ############################################################################
  def getSourceText              ( self                                    ) :
    ##########################################################################
    if                           ( not self . hasPlan ( )                  ) :
      return ""
    ##########################################################################
    p = self . GetPlan           (                                           )
    ##########################################################################
    return p . getSourceTextFunc (                                           )
  ############################################################################
  def getTargetText              ( self                                    ) :
    ##########################################################################
    if                           ( not self . hasPlan ( )                  ) :
      return ""
    ##########################################################################
    p = self . GetPlan           (                                           )
    ##########################################################################
    return p . getTargetTextFunc (                                           )
  ############################################################################
  def attachSearchTool   ( self , func , placeHolder = "" , text = ""      ) :
    ##########################################################################
    if                   ( not self . hasPlan ( )                          ) :
      return False
    ##########################################################################
    p   = self . GetPlan (                                                   )
    ##########################################################################
    try                                                                      :
      p . SearchLine . editingFinished . disconnect (                        )
    except                                                                   :
      pass
    ##########################################################################
    p   . SearchLine . blockSignals                 ( True                   )
    p   . SearchLine . setPlaceholderText           ( placeHolder            )
    p   . SearchLine . setText                      ( text                   )
    p   . SearchLine . blockSignals                 ( False                  )
    ##########################################################################
    p . SearchLine . editingFinished   . connect    ( func                   )
    p . SearchLine . parentWidget ( )  . show       (                        )
    p . SearchLine .                     show       (                        )
    p . SearchLine .                     setEnabled ( True                   )
    ##########################################################################
    return True
  ############################################################################
  def detachSearchTool   ( self                                            ) :
    ##########################################################################
    if                   ( not self . hasPlan ( )                          ) :
      return False
    ##########################################################################
    p   = self . GetPlan (                                                   )
    ##########################################################################
    p   . SearchLine . setPlaceholderText           ( ""                     )
    ##########################################################################
    try                                                                      :
      p . SearchLine . editingFinished . disconnect (                        )
    except                                                                   :
      pass
    ##########################################################################
    p . SearchLine . parentWidget ( )  . hide       (                        )
    p . SearchLine .                     setEnabled ( False                  )
    ##########################################################################
    return
  ############################################################################
  def attachSearchToolMessage      ( self , func , item , text = ""        ) :
    ##########################################################################
    msg  = self . getMenuItem      (               item                      )
    return self . attachSearchTool (        func , msg  , text               )
  ############################################################################
  def getSelectTool           ( self                                       ) :
    ##########################################################################
    if                        ( not self . hasPlan ( )                     ) :
      return None
    ##########################################################################
    p = self . GetPlan        (                                              )
    ##########################################################################
    return p . SelectTool
  ############################################################################
  def attachSelectTool   ( self , func                                     ) :
    ##########################################################################
    if                   ( not self . hasPlan ( )                          ) :
      return False
    ##########################################################################
    p   = self . GetPlan (                                                   )
    ##########################################################################
    try                                                                      :
      p . SelectTool . activated . disconnect (                              )
    except                                                                   :
      pass
    ##########################################################################
    p . SelectTool . activated         . connect    ( func                   )
    p . SelectTool . parentWidget ( )  . show       (                        )
    p . SelectTool .                     show       (                        )
    p . SelectTool .                     setEnabled ( True                   )
    ##########################################################################
    return True
  ############################################################################
  def detachSelectTool   ( self                                            ) :
    ##########################################################################
    if                   ( not self . hasPlan ( )                          ) :
      return False
    ##########################################################################
    p   = self . GetPlan (                                                   )
    ##########################################################################
    try                                                                      :
      p . SelectTool . activated . disconnect (                              )
    except                                                                   :
      pass
    ##########################################################################
    p . SelectTool . parentWidget ( )  . hide       (                        )
    p . SelectTool .                     setEnabled ( False                  )
    ##########################################################################
    return
  ############################################################################
  def LoadTextFromFile       ( self , Filename                             ) :
    ##########################################################################
    TEXT     = ""
    BODY     = ""
    ##########################################################################
    try                                                                      :
      with open              ( Filename , "rb" ) as File                     :
        TEXT = File . read   (                                               )
    except                                                                   :
      return ""
    ##########################################################################
    try                                                                      :
      BODY   = TEXT . decode ( "utf-8"                                       )
    except                                                                   :
      return ""
    ##########################################################################
    return BODY
  ############################################################################
  def GetUuidsFromText         ( self , BODY                               ) :
    ##########################################################################
    LISTS       = BODY . split ( "\n"                                        )
    UUIDs       =              [                                             ]
    ##########################################################################
    for L in LISTS                                                           :
      ########################################################################
      S         = L . split    (                                             )
      ########################################################################
      if                       ( len ( S ) <= 0                            ) :
        continue
      ########################################################################
      K         = S            [ 0                                           ]
      K         = K .  strip   (                                             )
      K         = K . rstrip   (                                             )
      ########################################################################
      if                       ( len ( K ) != 19                           ) :
        continue
      ########################################################################
      try                                                                    :
        U       = int          ( K                                           )
        if                     ( U not in UUIDs                            ) :
          UUIDs . append       ( U                                           )
      except                                                                 :
        pass
    ##########################################################################
    return UUIDs
  ############################################################################
  def LoadUuidsFromFile            ( self , Filename                       ) :
    ##########################################################################
    BODY = self . LoadTextFromFile (        Filename                         )
    if                             ( len ( BODY ) <= 0                     ) :
      return                       [                                         ]
    ##########################################################################
    return self . GetUuidsFromText ( BODY                                    )
  ############################################################################
  ############################################################################
  ############################################################################
  def getVariables     ( self                                              ) :
    ##########################################################################
    if                 ( not self . hasPlan ( )                            ) :
      return           {                                                     }
    ##########################################################################
    p = self . GetPlan (                                                     )
    ##########################################################################
    return p . Variables
  ############################################################################
  def StoreVariables          ( self                                       ) :
    ##########################################################################
    if                        ( not self . hasPlan ( )                     ) :
      return                  {                                              }
    ##########################################################################
    p = self . GetPlan        (                                              )
    ##########################################################################
    return p . StoreVariables (                                              )
  ############################################################################
  def attachActionsTool            ( self                                  ) :
    ##########################################################################
    if                             ( len ( self . WindowActions ) <= 0     ) :
      return
    ##########################################################################
    if                             ( not self . hasPlan ( )                ) :
      return False
    ##########################################################################
    p   = self . GetPlan           (                                         )
    ##########################################################################
    p   . ActionsTool . clear      (                                         )
    p   . ActionsTool . setToolTip ( self . Gui . windowTitle ( )            )
    ##########################################################################
    for ACTION in self . WindowActions                                       :
      ########################################################################
      p . ActionsTool . addAction  ( ACTION                                  )
    ##########################################################################
    p   . ActionsTool . show       (                                         )
    ##########################################################################
    return
  ############################################################################
  def detachActionsTool       ( self                                       ) :
    ##########################################################################
    if                        ( not self . hasPlan ( )                     ) :
      return False
    ##########################################################################
    p = self        . GetPlan (                                              )
    p . ActionsTool . clear   (                                              )
    ##########################################################################
    return
  ############################################################################
  def SwitchSideTools ( self , Enabled                                     ) :
    ##########################################################################
    for AA in self . HandleActions                                           :
      ########################################################################
      if              ( AA in self . EmptySet                              ) :
        continue
      ########################################################################
      AA . setEnabled (        Enabled                                       )
    ##########################################################################
    return
  ############################################################################
  def getAccessibleWidget  ( self , Name                                   ) :
    ##########################################################################
    WL = qApp . allWidgets (                                                 )
    for W in WL                                                              :
      ########################################################################
      if                   ( W . accessibleName ( ) == Name                ) :
        return W
    ##########################################################################
    return None
  ############################################################################
  def JoinPrimaryUuidsInOrder ( self , FIRST , ORIGINAL , ASC              ) :
    ##########################################################################
    for   U in ORIGINAL                                                      :
      ########################################################################
      if                      ( U in FIRST                                 ) :
        continue
      ########################################################################
      if                      ( ASC                                        ) :
        ######################################################################
        FIRST . insert        ( 0 , U                                        )
        ######################################################################
      else                                                                   :
        ######################################################################
        FIRST . append        ( U                                            )
    ##########################################################################
    return FIRST
  ############################################################################
  def ConvertCCCcode ( self , ID                                           ) :
    ##########################################################################
    CODE   = ""
    ##########################################################################
    if               ( 1 == ID                                             ) :
      CODE = "t2s"
    elif             ( 2 == ID                                             ) :
      CODE = "s2t"
    elif             ( 3 == ID                                             ) :
      CODE = "tw2s"
    elif             ( 4 == ID                                             ) :
      CODE = "s2tw"
    elif             ( 5 == ID                                             ) :
      CODE = "tw2sp"
    elif             ( 6 == ID                                             ) :
      CODE = "s2twp"
    elif             ( 7 == ID                                             ) :
      CODE = "hk2s"
    elif             ( 8 == ID                                             ) :
      CODE = "s2hk"
    ##########################################################################
    return CODE
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################
"""

bool getAbstractStopable(QVariant pointer) ;
bool setAbstractStopable(QVariant pointer,bool stopable) ;

class Q_COMPONENTS_EXPORT AbstractGui
{
  public:

    typedef enum          {
      DesktopGui = 300001 ,
      PadGui     = 300002 ,
      PhoneGui   = 300003 }
      GuiOperateMethod    ;

    typedef enum                 {
      GuiLeftButton   =   100001 ,
      GuiRightButton  =   100002 ,
      GuiMiddleButton =   100003 ,
      GuiShift        =   100004 ,
      GuiControl      =   100005 ,
      GuiAlt          =   100006 ,
      GuiMeta         =   100007 ,
      GuiResize       =   100101 ,
      GuiPainted      =   100102 ,
      GuiTap          =   100201 ,
      GuiTapHold      =   100202 ,
      GuiPan          =   100203 ,
      GuiPinch        =   100204 ,
      GuiSwipe        =   100205 ,
      GuiNotEvent     =   199999 }
      InputStatus                ; // For decision actions

    typedef enum                 {
      DropText          = 1001   ,
      DropUrls          = 1002   ,
      DropImage         = 1003   ,
      DropHtml          = 1004   ,
      DropColor         = 1005   ,
      DropTag           = 1006   ,
      DropPicture       = 1007   ,
      DropPeople        = 1008   ,
      DropAudio         = 1009   ,
      DropVideo         = 1010   ,
      DropAlbum         = 1011   ,
      DropGender        = 1012   ,
      DropDivision      = 1013   ,
      DropURIs          = 1014   ,
      DropBookmark      = 1015   ,
      DropFont          = 1016   ,
      DropPen           = 1017   ,
      DropBrush         = 1018   ,
      DropGradient      = 1019   ,
      DropShape         = 1020   ,
      DropMember        = 1021   ,
      DropSet           = 1022   ,
      DropActions       = 1023   ,
      DropDecision      = 1024   ,
      DropCondition     = 1025   ,
      DropExecution     = 1026   ,
      DropSqlTable      = 1027   ,
      DropDatabase      = 1028   ,
      DropTask          = 1029   ,
      DropNation        = 1030   ,
      DropContour       = 1031   ,
      DropManifold      = 1032   ,
      DropSource        = 1033   ,
      DropDocument      = 1034   ,
      DropEyes          = 1035   ,
      DropHairs         = 1036   ,
      DropKeyword       = 1037   ,
      DropTerminology   = 1038   ,
      DropKnowledge     = 1039   ,
      DropField         = 1040   ,
      DropKnowledgeBase = 1041   ,
      DropSqlColumn     = 1042   ,
      DropUuid          = 1043   ,
      DropCommodity     = 1044   ,
      DropOrganization  = 1045   ,
      DropBlob          = 1046   ,
      DropVariable      = 1047   ,
      DropTorrent       = 1048   ,
      DropCamera        = 1049   ,
      DropFace          = 1050   ,
      DropColorGroup    = 1051   ,
      DropSetsAlgebra   = 1052   ,
      DropName          = 1053   ,
      DropStar          = 1054   ,
      DropPhoneme       = 1055   ,
      DropModel         = 1056   ,
      DropReality       = 1057   }
      DropTypes                  ;

    typedef enum           {
      GuiNativeId =      0 ,
      GuiMainId   =  10001 ,
      GuiUserId   = 100001 }
      DecisionMapId        ; // Decision table id

    typedef enum               {
      InterfaceHasMenu  = 1001 ,
      CommonFunctionEnd = 1002
    } CommonFunctionIDs        ;

    Plan             *  plan       ;
    double              opacity    ;
    Pens                pens       ;
    Brushes             brushes    ;
    Pathes              pathes     ;
    DecisionTables      decisions  ;
    bool                designable ;
    QMap<QString,QIcon> LocalIcons ;
    NAMEs               LocalMsgs  ;

    explicit AbstractGui             (QWidget       * widget,Plan * plan = NULL);
    explicit AbstractGui             (QGraphicsItem * item  ,Plan * plan = NULL);
    virtual ~AbstractGui             (void);

    virtual bool    canDesign        (void) ;
    virtual void    setDesignable    (bool edit) ;

    void            setDropFlag      (DropTypes dropType,bool enabled);
    virtual bool    setAcceptVocal   (bool enabled) ;
    QIcon           Icon             (SUID ID) ;
    bool            changeFont       (void) ;

    void            acceptMouse      (Qt::MouseButtons      buttons  ) ;
    void            acceptModifiers  (Qt::KeyboardModifiers modifiers) ;

    virtual bool    addSequence      (VarArgs args) ;
    virtual bool    addSequence      (int command) ;
    virtual bool    Apportion        (void) ;

    virtual QString toCpp            (QString functionName) ;

    virtual void   assignTitle       (QString title) ;
    virtual void   assignLanguage    (nDeclWidget = NULL) ;
    virtual void   assignStyleSheet  (QString title,nDeclWidget = NULL) ;
    virtual void   assignMinimumSize (nDeclWidget) ;
    virtual void   assignMaximumSize (nDeclWidget) ;
    virtual bool   getGridSize       (nDeclWidget,QString title,QSize current,QSize & newSize) ;

    virtual QString GetName          (nConnectUuid) ;

    int             LimitValue       (int index) ;
    void            setLimitValue    (int index,int value) ;
    bool            ArgsToGroup      (int start,VarArgs & args,Group & group) ;
    bool            ArgsToUuids      (int start,VarArgs & args,UUIDs & uuids) ;
    bool            FixUuids         (UUIDs & Uuids) ;

    virtual void    setCanStop       (int value) ;
    virtual void    pushCanStop      (void) ;
    virtual void    popCanStop       (void) ;
    virtual bool    canStop          (void) ;
    virtual bool    isLoading        (void) ;
    virtual bool    isStopped        (void) ;
    virtual bool    startLoading     (void) ;
    virtual bool    stopLoading      (void) ;
    virtual void    stopForcely      (void) ;

    virtual bool    setFunction      (int Id,bool enable) ;
    virtual bool    isFunction       (int Id) ;
    virtual void    setGui           (QWidget * widget) ;

    void            setSuggestion    (QSize size) ;
    QSize           SizeSuggestion   (QSize size) const ;
    QSize           SizeSuggestion   (int width,int height) const ;

    virtual bool    RecoverySettings (QString scope) ;
    virtual bool    StoreSettings    (QString scope) ;

    virtual void    alert            (QString sound,QString message) ;

  protected:

    QTimer            * Commando        ;
    QMutex              Mutex           ;
    QMutex              PainterMutex    ;
    QMutex              CommandMutex    ;
    QWidget           * Gui             ;
    QDrag             * Drag            ;
    QString             localTitle      ;
    QShortcuts          Shortcuts       ;
    VcfWidgets          ChildWidgets    ;
    IMAPs               TimerIDs        ;
    bool                PassDragDrop    ;
    bool                Dumping         ;
    BMAPs               AllowDrops      ;
    BMAPs               Functionalities ;
    IMAPs               LimitValues     ;
    VarArgLists         Sequences       ;
    DataRetrievers      Retrievers      ;
    int                 vLanguageId     ;
    bool                allowGesture    ;
    bool                localModified   ;

    bool         EnterPainter        (void) ;
    void         LeavePainter        (void) ;

    void         StartCommando       (void) ;
    bool         EnterCommando       (void) ;
    void         LeaveCommando       (void) ;
    virtual void LaunchCommands      (void) ;
    virtual void DispatchCommands    (void) ;

    void         FadeIn              (nDeclWidget,int steps);
    void         FadeOut             (nDeclWidget,int steps);

    // message posting
    void         Notify              (QString message);
    void         Notify              (QString caption,QString message);

    // focus management
    virtual bool focusIn             (QFocusEvent * event) ;
    virtual bool focusOut            (QFocusEvent * event) ;

    virtual bool FocusIn             (void);
    virtual bool FocusOut            (void);

    // Shortcut management
    int          addShortcut         (const QKeySequence & key                                   ,
                                      QWidget            * parent                                ,
                                      const char         * member          = 0                   ,
                                      const char         * ambiguousMember = 0                   ,
                                      Qt::ShortcutContext  context         = Qt::WindowShortcut) ;

    QAction *    connectAction       (int Id,QObject * parent,const char * method,bool enable = true) ;
    QAction *    actionLabel         (int Id,QString message) ;

    QString      MimeType            (const QMimeData * mime,QString formats);

    // drag management
    bool         dragStart           (QMouseEvent * event);
    bool         dragMoving          (QMouseEvent * event);
    bool         dragEnd             (QMouseEvent * event);

    virtual bool hasItem             (void);
    virtual bool startDrag           (QMouseEvent * event);
    virtual bool fetchDrag           (QMouseEvent * event);
    virtual QMimeData * dragMime     (void);
    virtual void dragDone            (Qt::DropAction dropIt,QMimeData * mime);
    virtual bool finishDrag          (QMouseEvent * event);

    virtual bool acceptDrop          (nDeclWidget,const QMimeData * mime);
    virtual bool dropNew             (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropMoving          (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool dropAppend          (nDeclWidget,const QMimeData * mime,QPoint pos);
    virtual bool removeDrop          (void);

    virtual bool dragEnter           (QDragEnterEvent * event) ;
    virtual bool dragMove            (QDragMoveEvent  * event) ;
    virtual bool drop                (QDropEvent      * event) ;

    virtual void imState             (QInputMethodEvent * event) ;
    virtual void keyState            (QKeyEvent         * event) ;
    virtual void mouseState          (QMouseEvent       * event) ;
    virtual void wheelState          (QWheelEvent       * event) ;

    virtual bool permitGesture       (void) ;
    virtual bool gestureEvent        (QEvent             * event  ) ;
    virtual bool acceptTap           (QTapGesture        * gesture) ;
    virtual bool acceptTapHold       (QTapAndHoldGesture * gesture) ;
    virtual bool acceptPan           (QPanGesture        * gesture) ;
    virtual bool acceptPinch         (QPinchGesture      * gesture) ;
    virtual bool acceptSwipe         (QSwipeGesture      * gesture) ;
    virtual bool acceptCustom        (QGesture           * gesture) ;

    virtual void InstallDecisions    (void) ;

    void         Debug               (QEvent * event) ;

    UUIDs        GetUuids            (QByteArray & data) ;
    SUID         GetUuid             (QByteArray & data) ;
    QByteArray   CreateByteArray     (SUID    uuid ) ;
    QByteArray   CreateByteArray     (UUIDs & Uuids) ;
    void         setMime             (QMimeData * mime,QString mtype,SUID    uuid ) ;
    void         setMime             (QMimeData * mime,QString mtype,UUIDs & Uuids) ;

    virtual bool acceptTextDrop      (void) ;
    virtual bool acceptUrlsDrop      (void) ;
    virtual bool acceptImageDrop     (void) ;
    virtual bool acceptHtmlDrop      (void) ;
    virtual bool acceptColorDrop     (void) ;
    virtual bool acceptTagDrop       (void) ;
    virtual bool acceptPictureDrop   (void) ;
    virtual bool acceptPeopleDrop    (void) ;
    virtual bool acceptAudioDrop     (void) ;
    virtual bool acceptVideoDrop     (void) ;
    virtual bool acceptAlbumDrop     (void) ;
    virtual bool acceptGenderDrop    (void) ;
    virtual bool acceptDivisionDrop  (void) ;
    virtual bool acceptUriDrop       (void) ;
    virtual bool acceptBookmarkDrop  (void) ;
    virtual bool acceptFont          (void) ;
    virtual bool acceptPen           (void) ;
    virtual bool acceptBrush         (void) ;
    virtual bool acceptGradient      (void) ;
    virtual bool acceptShapes        (void) ;
    virtual bool acceptMembers       (void) ;
    virtual bool acceptSets          (void) ;
    virtual bool acceptActions       (void) ;
    virtual bool acceptDecision      (void) ;
    virtual bool acceptCondition     (void) ;
    virtual bool acceptExecution     (void) ;
    virtual bool acceptSqlTable      (void) ;
    virtual bool acceptDatabase      (void) ;
    virtual bool acceptTask          (void) ;
    virtual bool acceptNation        (void) ;
    virtual bool acceptContour       (void) ;
    virtual bool acceptManifold      (void) ;
    virtual bool acceptSources       (void) ;
    virtual bool acceptDocuments     (void) ;
    virtual bool acceptEyes          (void) ;
    virtual bool acceptHairs         (void) ;
    virtual bool acceptKeywords      (void) ;
    virtual bool acceptTerminologies (void) ;
    virtual bool acceptKnowledge     (void) ;
    virtual bool acceptFields        (void) ;
    virtual bool acceptKnowledgeBase (void) ;
    virtual bool acceptSqlColumn     (void) ;
    virtual bool acceptUuids         (void) ;
    virtual bool acceptCommodities   (void) ;
    virtual bool acceptOrganizations (void) ;
    virtual bool acceptBlobs         (void) ;
    virtual bool acceptVariables     (void) ;
    virtual bool acceptTorrents      (void) ;
    virtual bool acceptCameras       (void) ;
    virtual bool acceptFaces         (void) ;
    virtual bool acceptColorGroups   (void) ;
    virtual bool acceptSetsAlgebras  (void) ;
    virtual bool acceptNames         (void) ;
    virtual bool acceptStars         (void) ;
    virtual bool acceptPhonemes      (void) ;
    virtual bool acceptModels        (void) ;
    virtual bool acceptReality       (void) ;

    virtual bool acceptPrivate       (const QMimeData * mime) ;

    virtual bool dropHandler         (const QMimeData * mime) ;

    virtual bool dropItems           (nDeclWidget,const QMimeData * mime,QPoint  pos) ;
    virtual bool dropItems           (nDeclWidget,const QMimeData * mime,QPointF pos) ;
    virtual bool dropPrivate         (nDeclWidget,const QMimeData * mime,QPointF pos) ;

    virtual bool dropText            (nDeclWidget,QPointF pos,const QString & text    ) ;
    virtual bool dropUrls            (nDeclWidget,QPointF pos,const QList<QUrl> & urls) ;
    virtual bool dropImage           (nDeclWidget,QPointF pos,const QImage  & image   ) ;
    virtual bool dropHtml            (nDeclWidget,QPointF pos,const QString & html    ) ;
    virtual bool dropColor           (nDeclWidget,QPointF pos,const QColor  & color   ) ;
    virtual bool dropTags            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropPictures        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropPeople          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropAudios          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropVideos          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropAlbums          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropGender          (nDeclWidget,QPointF pos,const SUID      gender  ) ;
    virtual bool dropDivisions       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropURIs            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropBookmarks       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropFont            (nDeclWidget,QPointF pos,const SUID      font    ) ;
    virtual bool dropPen             (nDeclWidget,QPointF pos,const SUID      pen     ) ;
    virtual bool dropBrush           (nDeclWidget,QPointF pos,const SUID      brush   ) ;
    virtual bool dropGradient        (nDeclWidget,QPointF pos,const SUID      gradient) ;
    virtual bool dropShapes          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropMembers         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSets            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropActions         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropDecision        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropCondition       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropExecution       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSqlTable        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropDatabase        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropTask            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropNation          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropContour         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropManifold        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSources         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropDocuments       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropEyes            (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropHairs           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropKeywords        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropTerminologies   (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropKnowledge       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropFields          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropKnowledgeBase   (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSqlColumn       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropUuids           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropCommodities     (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropOrganizations   (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropBlobs           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropVariables       (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropTorrents        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropCameras         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropFaces           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropColorGroups     (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropSetsAlgebras    (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropNames           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropStars           (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropPhonemes        (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropModels          (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;
    virtual bool dropReality         (nDeclWidget,QPointF pos,const UUIDs   & Uuids   ) ;

    virtual bool Bustle              (void) ;
    virtual bool Vacancy             (void) ;
    virtual bool isLocked            (int timeout = 100) ;
    virtual void LockGui             (void) ;
    virtual void UnlockGui           (void) ;

    virtual bool ForUuid             (SUID & u,qint64 & i,UUIDs & U) ;

  private:

    void * PrivateStopable ;

    bool         allowDrops          (DropTypes dropType) ;

};

#include <qtcomponents.h>

#define DefaultMax  16777215
#define LoadingID   1000001
#define StoppedID   1000002
#define CanStopID   1000003

typedef struct              {
  bool             canstop  ;
  N::AbstractGui * abstract ;
} GuiStopable               ;

bool N::getAbstractStopable(QVariant pointer)
{
  GuiStopable * gs = (GuiStopable *) VariantToVoid ( pointer ) ;
  if ( NULL == gs ) return true                                ;
  return gs -> canstop                                         ;
}

bool N::setAbstractStopable(QVariant pointer,bool stopable)
{
  GuiStopable * gs = (GuiStopable *) VariantToVoid ( pointer ) ;
  if ( NULL == gs ) return true                                ;
  gs -> canstop = stopable                                     ;
  return gs -> canstop                                         ;
}

N::AbstractGui:: AbstractGui     ( QWidget * widget,Plan * p    )
               : plan            (                         p    )
               , Commando        ( new QTimer ( widget )        )
               , Gui             (              widget          )
               , opacity         ( 1.00                         )
               , PassDragDrop    ( true                         )
               , Dumping         ( false                        )
               , Drag            ( NULL                         )
               , localTitle      ( ""                           )
               , designable      ( false                        )
               , vLanguageId     ( 1819                         )
               , allowGesture    ( false                        )
               , PrivateStopable ( (void *) new GuiStopable ( ) )
               , localModified   ( false                        )
{
  decisions . Blank ( 0 )                                                  ;
  //////////////////////////////////////////////////////////////////////////
  if (IsNull(plan)) plan = AppPlan                                         ;
  nIfSafe(plan)                                                            {
    vLanguageId = plan->LanguageId                                         ;
  }                                                                        ;
  nIfSafe(Gui)                                                             {
    Gui -> setProperty ( "AbstractGui" , true                            ) ;
    Gui -> setProperty ( "CanStop"     , VoidVariant ( PrivateStopable ) ) ;
  }                                                                        ;
  //////////////////////////////////////////////////////////////////////////
  ( (GuiStopable *) PrivateStopable ) -> canstop  = true                   ;
  ( (GuiStopable *) PrivateStopable ) -> abstract = this                   ;
  //////////////////////////////////////////////////////////////////////////
  LimitValues [ LoadingID ] = 0                                            ;
  LimitValues [ StoppedID ] = 0                                            ;
  LimitValues [ CanStopID ] = 0                                            ;
  //////////////////////////////////////////////////////////////////////////
  InstallDecisions ( )                                                     ;
}

N::AbstractGui:: AbstractGui     ( QGraphicsItem * item,Plan * p )
               : plan            (                             p )
               , Gui             ( NULL                          )
               , opacity         ( 1.00                          )
               , PassDragDrop    ( true                          )
               , Dumping         ( false                         )
               , Drag            ( NULL                          )
               , designable      ( false                         )
               , PrivateStopable ( (void *) new GuiStopable ( )  )
{
  decisions.Blank(GuiNativeId)                                             ;
  //////////////////////////////////////////////////////////////////////////
  if (IsNull(plan)) plan = AppPlan                                         ;
  nIfSafe(plan)                                                            {
    vLanguageId = plan->LanguageId                                         ;
  }                                                                        ;
  //////////////////////////////////////////////////////////////////////////
  QGraphicsScene * gs = NULL                                               ;
  nIfSafe(item) gs = item->scene()                                         ;
  nIfSafe(gs)                                                              {
    QList<QGraphicsView *> vs = gs->views()                                ;
    if (vs.count()>0)                                                      {
      Gui = (QWidget *)vs[0]                                               ;
    }                                                                      ;
  }                                                                        ;
  Commando = new QTimer ( Gui )                                            ;
  nIfSafe ( Gui )                                                          {
    Gui -> setProperty ( "AbstractGui" , true                            ) ;
    Gui -> setProperty ( "CanStop"     , VoidVariant ( PrivateStopable ) ) ;
  }                                                                        ;
  //////////////////////////////////////////////////////////////////////////
  ( (GuiStopable *) PrivateStopable ) -> canstop  = true                   ;
  ( (GuiStopable *) PrivateStopable ) -> abstract = this                   ;
  //////////////////////////////////////////////////////////////////////////
  LimitValues [ LoadingID ] = 0                                            ;
  LimitValues [ StoppedID ] = 0                                            ;
  LimitValues [ CanStopID ] = 0                                            ;
  //////////////////////////////////////////////////////////////////////////
  InstallDecisions ( )                                                     ;
}

N::AbstractGui::~AbstractGui(void)
{
  if ( NotNull ( PrivateStopable ) ) {
    delete PrivateStopable           ;
    PrivateStopable = NULL           ;
  }                                  ;
}

bool N::AbstractGui::ForUuid(SUID & u,qint64 & i,UUIDs & U)
{
  if ( i >= U . count ( ) ) return false ;
  u = U [ i ]                            ;
  i++                                    ;
  return true                            ;
}

bool N::AbstractGui::FixUuids(UUIDs & Uuids)
{
  LimitValues [ 2 ] = Uuids . count ( )            ;
  if ( LimitValues[0] >= 0 && LimitValues[1] > 0 ) {
    UUIDs UX                                       ;
    int   sid = LimitValues[0]                     ;
    int   tid = LimitValues[1]                     ;
    int   eid = LimitValues[2]                     ;
    if ((sid+tid)<eid) eid = sid + tid             ;
    for (int i=sid;i<eid;i++) UX << Uuids[i]       ;
    Uuids = UX                                     ;
    return true                                    ;
  }                                                ;
  return false                                     ;
}

bool N::AbstractGui::ArgsToGroup(int start,VarArgs & args,Group & group)
{
  if ( start >= args.count() ) return false               ;
  group.first      = args [ start     ] . toULongLong ( ) ;
  group.second     = args [ start + 1 ] . toULongLong ( ) ;
  group.t1         = args [ start + 2 ] . toInt       ( ) ;
  group.t2         = args [ start + 3 ] . toInt       ( ) ;
  group.relation   = args [ start + 4 ] . toInt       ( ) ;
  group.position   = args [ start + 5 ] . toInt       ( ) ;
  group.membership = args [ start + 6 ] . toDouble    ( ) ;
  return true                                             ;
}

bool N::AbstractGui::ArgsToUuids(int start,VarArgs & args,UUIDs & uuids)
{
  if ( start >= args.count() ) return false ;
  int t = args[start].toInt()               ;
  start++                                   ;
  if (t<=0) return false                    ;
  for (int i=0;i<t;i++,start++)             {
    uuids << args[start].toULongLong()      ;
  }                                         ;
  return true                               ;
}

void N::AbstractGui::setCanStop(int value)
{
  LimitValues [ CanStopID ] = value                             ;
  ( (GuiStopable *) PrivateStopable ) -> canstop  = canStop ( ) ;
}

void N::AbstractGui::pushCanStop(void)
{
  LimitValues [ CanStopID ] ++                                  ;
  ( (GuiStopable *) PrivateStopable ) -> canstop  = canStop ( ) ;
}

void N::AbstractGui::popCanStop(void)
{
  LimitValues [ CanStopID ] --                                  ;
  ( (GuiStopable *) PrivateStopable ) -> canstop  = canStop ( ) ;
}

bool N::AbstractGui::canStop(void)
{
  return ( 0 >= LimitValues [ CanStopID ] ) ;
}

bool N::AbstractGui::isLoading(void)
{
  return ( LimitValues [ LoadingID ] > 0 ) ;
}

bool N::AbstractGui::isStopped(void)
{
  return ( LimitValues [ StoppedID ] <= 0 ) ;
}

bool N::AbstractGui::startLoading(void)
{
  LimitValues [ LoadingID ] ++             ;
  LimitValues [ StoppedID ] ++             ;
  pushCanStop (           )                ;
  //////////////////////////////////////////
  return ( LimitValues [ LoadingID ] > 0 ) ;
}

bool N::AbstractGui::stopLoading(void)
{
  if ( LimitValues [ LoadingID ] > 0 )     {
    LimitValues [ LoadingID ] --           ;
  }                                        ;
  LimitValues [ StoppedID ] --             ;
  popCanStop  (           )                ;
  return ( LimitValues [ LoadingID ] > 0 ) ;
}

void N::AbstractGui::stopForcely(void)
{
  LimitValues [ LoadingID ] = 0 ;
}

void N::AbstractGui::alert(QString sound,QString message)
{
  nDropOut       ( IsNull ( plan ) ) ;
  plan -> Notify ( sound , message ) ;
}

void N::AbstractGui::setGui(QWidget * widget)
{
  Gui = widget                  ;
  Commando -> setParent ( Gui ) ;
}

bool N::AbstractGui::RecoverySettings(QString scope)
{
  return true ;
}

bool N::AbstractGui::StoreSettings(QString scope)
{
  return true ;
}

bool N::AbstractGui::canDesign(void)
{
  return designable ;
}

void N::AbstractGui::setDesignable(bool edit)
{
  designable = edit ;
}

bool N::AbstractGui::EnterPainter(void)
{
  bool canLock = PainterMutex . tryLock ( 25 )            ;
  if (canLock)                                            {
    decisions[GuiNativeId].setCondition(GuiPainted,false) ;
  }                                                       ;
  return canLock ;
}

void N::AbstractGui::LeavePainter(void)
{
  PainterMutex . unlock ( )                             ;
  decisions[GuiNativeId].setCondition(GuiPainted,true ) ;
}

void N::AbstractGui::InstallDecisions(void)
{
}

void N::AbstractGui::StartCommando(void)
{
  nDropOut ( Commando -> isActive() ) ;
  Commando -> start ( 100 )           ;
}

bool N::AbstractGui::EnterCommando(void)
{
  bool locked = CommandMutex . tryLock ( 100 ) ;
  Commando -> stop ( )                         ;
  return locked                                ;
}

void N::AbstractGui::LeaveCommando(void)
{
  CommandMutex . unlock ( ) ;
}

void N::AbstractGui::LaunchCommands(void)
{
  EnterCommando    ( ) ;
  DispatchCommands ( ) ;
  LeaveCommando    ( ) ;
}

void N::AbstractGui::DispatchCommands(void)
{
}

bool N::AbstractGui::isLocked(int timeout)
{
  nKickOut ( !Mutex.tryLock(timeout) , true ) ;
  Mutex . unlock ( )                          ;
  return false                                ;
}

QIcon N::AbstractGui::Icon(SUID ID)
{
  QIcon I                       ;
  if (plan->icons.contains(ID)) {
    return plan->icons[ID]      ;
  }                             ;
  return I                      ;
}

bool N::AbstractGui::changeFont(void)
{
  bool  okay = false                ;
  QFont f    = Gui -> font()        ;
  f = QFontDialog::getFont(&okay,f) ;
  nKickOut ( !okay , false )        ;
  Gui -> setFont ( f )              ;
  return true                       ;
}

void N::AbstractGui::FadeIn(QWidget * widget,int steps)
{
  if (opacity<0.1) opacity = 0.1           ;
  qreal dw = opacity - 0.1                 ;
  qreal Opacity = 0.1                      ;
  dw /= steps                              ;
  for (int i=0;i<=steps;i++)               {
    widget->setWindowOpacity(Opacity)      ;
    Opacity += dw                          ;
    if (Opacity>opacity) Opacity = opacity ;
    widget->show()                         ;
    qApp->processEvents()                  ;
    qApp->sendPostedEvents()               ;
    Time::msleep(50)                       ;
  }                                        ;
  widget->setWindowOpacity(opacity)        ;
  widget->show()                           ;
}

void N::AbstractGui::FadeOut(QWidget * widget,int steps)
{
  if (opacity<0.1) opacity = 0.1      ;
  qreal dw = opacity - 0.1            ;
  qreal Opacity = opacity             ;
  dw /= steps                         ;
  for (int i=0;i<=steps;i++)          {
    widget->setWindowOpacity(Opacity) ;
    Opacity -= dw                     ;
    if (Opacity<0) Opacity = 0        ;
    widget->show()                    ;
    qApp->processEvents()             ;
    qApp->sendPostedEvents()          ;
    Time::msleep(50)                  ;
  }                                   ;
  widget->setWindowOpacity(Opacity)   ;
  widget->hide()                      ;
}

void N::AbstractGui::Notify(QString message)
{
  nDropOut ( IsNull(Gui) )                                 ;
  QMessageBox::information(Gui,Gui->windowTitle(),message) ;
}

void N::AbstractGui::Notify(QString caption,QString message)
{
  nDropOut ( IsNull(Gui) )                      ;
  QMessageBox::information(Gui,caption,message) ;
}

bool N::AbstractGui::focusIn(QFocusEvent * event)
{
  if (event->gotFocus() && FocusIn ()) {
    event->accept()                    ;
    return true                        ;
  }                                    ;
  return false                         ;
}

bool N::AbstractGui::focusOut(QFocusEvent * event)
{
  if (event->lostFocus() && FocusOut()) {
    event->accept()                     ;
    return true                         ;
  }                                     ;
  return false                          ;
}

bool N::AbstractGui::FocusIn(void)
{
  return false ;
}

bool N::AbstractGui::FocusOut(void)
{
  return false ;
}

bool N::AbstractGui::addSequence(VarArgs args)
{
  Sequences << args ;
  return true       ;
}

bool N::AbstractGui::addSequence(int command)
{
  VarArgs V                 ;
  V << QVariant ( command ) ;
  Sequences << V            ;
  return true               ;
}

bool N::AbstractGui::Apportion(void)
{
  return false ;
}

bool N::AbstractGui::setAcceptVocal(bool enabled)
{
  return true ;
}

void N::AbstractGui::assignTitle(QString title)
{
  if ( IsNull ( Gui ) ) return          ;
  Gui -> setWindowTitle ( title )       ;
  ///////////////////////////////////////
  QWidget * w = Gui -> parentWidget ( ) ;
  if ( IsNull (  w  ) ) return          ;
  ///////////////////////////////////////
  QMdiSubWindow * msw                   ;
  msw  = Casting ( QMdiSubWindow , w )  ;
  if ( NotNull ( msw  ) )               {
    msw  -> setWindowTitle ( title )    ;
  }                                     ;
  ///////////////////////////////////////
  QDockWidget * dock                    ;
  dock = Casting ( QDockWidget , w )    ;
  if ( NotNull ( dock ) )               {
    dock -> setWindowTitle ( title )    ;
  }                                     ;
}

void N::AbstractGui::assignLanguage(QWidget * widget)
{
  if (IsNull(widget)) widget = Gui                                  ;
  nDropOut ( IsNull(widget) )                                       ;
  LanguageSelections * NLS = new LanguageSelections(widget,plan)    ;
  NLS->List(vLanguageId)                                            ;
  if (NLS->exec()==QDialog::Accepted) vLanguageId = NLS->Language() ;
  NLS -> deleteLater ( )                                            ;
}

void N::AbstractGui::assignStyleSheet(QString title,QWidget * widget)
{
  nDropOut ( IsNull(plan) )                                     ;
  if (IsNull(widget)) widget = Gui                              ;
  nDropOut ( IsNull(widget) )                                   ;
  QTextEdit       * TEW = new QTextEdit       ( widget        ) ;
  ContainerDialog * CDW = new ContainerDialog ( widget , plan ) ;
  QString           CSS = widget->styleSheet()                  ;
  TEW    -> setWindowTitle   ( title     )                      ;
  TEW    -> resize           ( 320 , 240 )                      ;
  CDW    -> setWidget        ( TEW       )                      ;
  TEW    -> setPlainText     ( CSS       )                      ;
  if ( QDialog::Accepted == CDW -> exec ( ) )                   {
    CSS = TEW -> toPlainText (           )                      ;
  }                                                             ;
  TEW    -> deleteLater      (           )                      ;
  CDW    -> deleteLater      (           )                      ;
  widget -> setStyleSheet    ( CSS       )                      ;
  ///////////////////////////////////////////////////////////////
  QMdiSubWindow * msw                                           ;
  msw = qobject_cast<QMdiSubWindow *>(widget->parentWidget())   ;
  if (NotNull(msw)) msw -> setStyleSheet ( CSS )                ;
  ///////////////////////////////////////////////////////////////
  QDockWidget   * qdw                                           ;
  qdw = qobject_cast<QDockWidget   *>(widget->parentWidget())   ;
  if (NotNull(qdw)) qdw -> setStyleSheet ( CSS )                ;
}

void N::AbstractGui::assignMinimumSize(QWidget * widget)
{
  GetSize  * ngs = new GetSize(widget,plan)                 ;
  QSize      s   = widget->minimumSize()                    ;
  QString    t   = widget->windowTitle()                    ;
  QString    m   = QObject::tr("Minimum size of %1").arg(t) ;
  ngs->setWindowTitle(m)                                    ;
  ngs->setRange(0,0,DefaultMax)                             ;
  ngs->setRange(1,0,DefaultMax)                             ;
  ngs->setPrefix(0,QObject::tr("Width : " ))                ;
  ngs->setPrefix(1,QObject::tr("Height : "))                ;
  ngs->setSize(s);                                          ;
  if (ngs->exec()==QDialog::Accepted)                       {
    s = ngs->Size()                                         ;
    widget->setMinimumSize(s)                               ;
  }                                                         ;
  ngs->deleteLater()                                        ;
}

void N::AbstractGui::assignMaximumSize(QWidget * widget)
{
  GetSize  * ngs = new GetSize(widget,plan)                 ;
  QSize      s   = widget->maximumSize()                    ;
  QString    t   = widget->windowTitle()                    ;
  QString    m   = QObject::tr("Maximum size of %1").arg(t) ;
  ngs->setWindowTitle(m)                                    ;
  ngs->setRange(0,0,DefaultMax)                             ;
  ngs->setRange(1,0,DefaultMax)                             ;
  ngs->setPrefix(0,QObject::tr("Width : " ))                ;
  ngs->setPrefix(1,QObject::tr("Height : "))                ;
  ngs->setSize(s);                                          ;
  if (ngs->exec()==QDialog::Accepted)                       {
    s = ngs->Size()                                         ;
    widget->setMaximumSize(s)                               ;
  }                                                         ;
  ngs->deleteLater()                                        ;
}

bool N::AbstractGui::getGridSize (
       QWidget * widget       ,
       QString   title        ,
       QSize     current      ,
       QSize   & newSize      )
{
  GetSize * ngs = new GetSize(widget,plan)   ;
  bool       correct = false                 ;
  ngs->setWindowTitle(title)                 ;
  ngs->setRange(0,0,DefaultMax)              ;
  ngs->setRange(1,0,DefaultMax)              ;
  ngs->setPrefix(0,QObject::tr("Width : " )) ;
  ngs->setPrefix(1,QObject::tr("Height : ")) ;
  ngs->setSize (current       )              ;
  if (ngs->exec()==QDialog::Accepted)        {
    newSize = ngs->Size()                    ;
    correct = true                           ;
  }                                          ;
  ngs->deleteLater()                         ;
  return correct                             ;
}

QString N::AbstractGui::GetName(SqlConnection & connection,SUID uuid)
{
  return connection.getName (
           PlanTable(Names) ,
           "uuid"           ,
           vLanguageId      ,
           uuid           ) ;
}

int N::AbstractGui::addShortcut            (
      const QKeySequence & key             ,
      QWidget            * parent          ,
      const char         * member          ,
      const char         * ambiguousMember ,
      Qt::ShortcutContext  context         )
{
  Shortcuts << new QShortcut(key,parent,member,ambiguousMember,context) ;
  return Shortcuts.count()                                              ;
}

void N::AbstractGui::acceptMouse(Qt::MouseButtons buttons)
{
  decisions[0].setCondition(GuiLeftButton  ,IsMask(buttons,Qt::LeftButton  )) ;
  decisions[0].setCondition(GuiRightButton ,IsMask(buttons,Qt::RightButton )) ;
  decisions[0].setCondition(GuiMiddleButton,IsMask(buttons,Qt::MiddleButton)) ;
}

void N::AbstractGui::acceptModifiers(Qt::KeyboardModifiers modifiers)
{
  decisions[0].setCondition(GuiShift  ,IsMask(modifiers,Qt::ShiftModifier  )) ;
  decisions[0].setCondition(GuiControl,IsMask(modifiers,Qt::ControlModifier)) ;
  decisions[0].setCondition(GuiAlt    ,IsMask(modifiers,Qt::AltModifier    )) ;
  decisions[0].setCondition(GuiMeta   ,IsMask(modifiers,Qt::MetaModifier   )) ;
}

void N::AbstractGui::imState (QInputMethodEvent * event)
{
}

void N::AbstractGui::keyState (QKeyEvent * event)
{
  acceptModifiers(event->modifiers()) ;
}

void N::AbstractGui::mouseState (QMouseEvent * event)
{
  acceptMouse(event->buttons()) ;
}

void N::AbstractGui::wheelState (QWheelEvent * event)
{
  acceptMouse(event->buttons()) ;
}

void N::AbstractGui::Debug(QEvent * event)
{
  nDropOut ( IsNull(plan) )                            ;
  plan->Debug(15,QString("QET:%1").arg(event->type())) ;
}

UUIDs N::AbstractGui::GetUuids(QByteArray & data)
{
  UUIDs Uuids                        ;
  SUID * suid  = (SUID *)data.data() ;
  int    total = (int)suid[0]        ;
  for (int i=0;i<total;i++)          {
    Uuids << suid[i+1]               ;
  }                                  ;
  return Uuids                       ;
}

SUID N::AbstractGui::GetUuid(QByteArray & data)
{
  SUID   * suid = (SUID *)data.data() ;
  return (*suid)                      ;
}

bool N::AbstractGui::acceptPrivate(const QMimeData * mime)
{
  return false ;
}

bool N::AbstractGui::dropPrivate(QWidget * source,const QMimeData * mime,QPointF pos)
{
  return false ;
}

#define VG(Function,Item)           \
bool N::AbstractGui::Function(void) \
{                                   \
  return allowDrops(Item)         ; \
}

VG( acceptTextDrop      , DropText          )
VG( acceptUrlsDrop      , DropUrls          )
VG( acceptImageDrop     , DropImage         )
VG( acceptHtmlDrop      , DropHtml          )
VG( acceptColorDrop     , DropColor         )
VG( acceptTagDrop       , DropTag           )
VG( acceptPictureDrop   , DropPicture       )
VG( acceptPeopleDrop    , DropPeople        )
VG( acceptVideoDrop     , DropVideo         )
VG( acceptAudioDrop     , DropAudio         )
VG( acceptAlbumDrop     , DropAlbum         )
VG( acceptGenderDrop    , DropGender        )
VG( acceptDivisionDrop  , DropDivision      )
VG( acceptUriDrop       , DropURIs          )
VG( acceptBookmarkDrop  , DropBookmark      )
VG( acceptFont          , DropFont          )
VG( acceptPen           , DropPen           )
VG( acceptBrush         , DropBrush         )
VG( acceptGradient      , DropGradient      )
VG( acceptShapes        , DropShape         )
VG( acceptMembers       , DropMember        )
VG( acceptSets          , DropSet           )
VG( acceptActions       , DropActions       )
VG( acceptDecision      , DropDecision      )
VG( acceptCondition     , DropCondition     )
VG( acceptExecution     , DropExecution     )
VG( acceptSqlTable      , DropSqlTable      )
VG( acceptDatabase      , DropDatabase      )
VG( acceptTask          , DropTask          )
VG( acceptNation        , DropNation        )
VG( acceptContour       , DropContour       )
VG( acceptManifold      , DropManifold      )
VG( acceptSources       , DropSource        )
VG( acceptDocuments     , DropDocument      )
VG( acceptEyes          , DropEyes          )
VG( acceptHairs         , DropHairs         )
VG( acceptKeywords      , DropKeyword       )
VG( acceptTerminologies , DropTerminology   )
VG( acceptKnowledge     , DropKnowledge     )
VG( acceptFields        , DropField         )
VG( acceptKnowledgeBase , DropKnowledgeBase )
VG( acceptSqlColumn     , DropSqlColumn     )
VG( acceptUuids         , DropUuid          )
VG( acceptCommodities   , DropCommodity     )
VG( acceptOrganizations , DropOrganization  )
VG( acceptBlobs         , DropBlob          )
VG( acceptVariables     , DropVariable      )
VG( acceptTorrents      , DropTorrent       )
VG( acceptCameras       , DropCamera        )
VG( acceptFaces         , DropFace          )
VG( acceptColorGroups   , DropColorGroup    )
VG( acceptSetsAlgebras  , DropSetsAlgebra   )
VG( acceptNames         , DropName          )
VG( acceptStars         , DropStar          )
VG( acceptPhonemes      , DropPhoneme       )
VG( acceptModels        , DropModel         )
VG( acceptReality       , DropReality       )

#undef  VG

bool N::AbstractGui::dropItems(QWidget * source,const QMimeData * mime,QPoint pt)
{
  QPointF pos = pt                  ;
  return dropItems(source,mime,pos) ;
}

bool N::AbstractGui::dropItems(QWidget * source,const QMimeData * mime,QPointF pos)
{
  #define HASD(DUID,FUNCTION) (mime->hasFormat(DUID) && FUNCTION())
  #define DITE(DUID,FUNCTION)                                       \
    QByteArray data   = mime->data ( DUID  ) ;                      \
    SUID       uuid   = GetUuid    ( data  ) ;                      \
    UUIDs      Uuids                         ;                      \
    Uuids << uuid                            ;                      \
    return FUNCTION ( source , pos , Uuids )
  #define SITX(DUID,FUNCTION)                                       \
    QByteArray data   = mime->data ( DUID  ) ;                      \
    UUIDs      Uuids  = GetUuids   ( data  ) ;                      \
    return FUNCTION ( source , pos , Uuids )
  #define SITZ(DUID,FUNCTION)                                       \
    QByteArray data   = mime->data ( DUID  ) ;                      \
    SUID       uuid   = GetUuid    ( data  ) ;                      \
    return FUNCTION ( source , pos , uuid  )
  #define IFCAST(name,Drop,Toss)                                    \
    if (HASD( #name "/uuid" , Drop ))                             { \
        SITZ( #name "/uuid" , Toss )                              ; \
    }
  #define IFBOTH(name,Drop,Toss)                                    \
    if (HASD( #name "/uuid"  , Drop ))                            { \
        DITE( #name "/uuid"  , Toss )                             ; \
    }                                                               \
    if (HASD( #name "/uuids" , Drop ))                            { \
        SITX( #name "/uuids" , Toss )                             ; \
    }
  ///////////////////////////////////////////////////////////////////
  IFBOTH( uuid          , acceptUuids         , dropUuids         ) ;
  IFBOTH( division      , acceptDivisionDrop  , dropDivisions     ) ;
  IFCAST( gender        , acceptGenderDrop    , dropGender        ) ;
  IFBOTH( tag           , acceptTagDrop       , dropTags          ) ;
  IFBOTH( name          , acceptNames         , dropNames         ) ;
  IFBOTH( picture       , acceptPictureDrop   , dropPictures      ) ;
  IFBOTH( people        , acceptPeopleDrop    , dropPeople        ) ;
  IFBOTH( audio         , acceptAudioDrop     , dropAudios        ) ;
  IFBOTH( video         , acceptVideoDrop     , dropVideos        ) ;
  IFBOTH( album         , acceptAlbumDrop     , dropAlbums        ) ;
  IFBOTH( uri           , acceptUriDrop       , dropURIs          ) ;
  IFBOTH( bookmark      , acceptBookmarkDrop  , dropBookmarks     ) ;
  IFBOTH( shape         , acceptShapes        , dropShapes        ) ;
  IFBOTH( member        , acceptMembers       , dropMembers       ) ;
  IFBOTH( set           , acceptSets          , dropSets          ) ;
  IFBOTH( action        , acceptActions       , dropActions       ) ;
  IFBOTH( decision      , acceptDecision      , dropDecision      ) ;
  IFBOTH( condition     , acceptCondition     , dropCondition     ) ;
  IFBOTH( execution     , acceptExecution     , dropExecution     ) ;
  IFBOTH( sql           , acceptSqlTable      , dropSqlTable      ) ;
  IFBOTH( database      , acceptDatabase      , dropDatabase      ) ;
  IFBOTH( task          , acceptTask          , dropTask          ) ;
  IFBOTH( nation        , acceptNation        , dropNation        ) ;
  IFBOTH( contour       , acceptContour       , dropContour       ) ;
  IFBOTH( manifold      , acceptManifold      , dropManifold      ) ;
  IFBOTH( source        , acceptSources       , dropSources       ) ;
  IFBOTH( document      , acceptDocuments     , dropDocuments     ) ;
  IFBOTH( eyes          , acceptEyes          , dropEyes          ) ;
  IFBOTH( hairs         , acceptHairs         , dropHairs         ) ;
  IFBOTH( keyword       , acceptKeywords      , dropKeywords      ) ;
  IFBOTH( terminology   , acceptTerminologies , dropTerminologies ) ;
  IFBOTH( knowledge     , acceptKnowledge     , dropKnowledge     ) ;
  IFBOTH( field         , acceptFields        , dropFields        ) ;
  IFBOTH( knowledgebase , acceptKnowledgeBase , dropKnowledgeBase ) ;
  IFBOTH( sqlcolumn     , acceptSqlColumn     , dropSqlColumn     ) ;
  IFBOTH( commodity     , acceptCommodities   , dropCommodities   ) ;
  IFBOTH( organization  , acceptOrganizations , dropOrganizations ) ;
  IFBOTH( blob          , acceptBlobs         , dropBlobs         ) ;
  IFBOTH( variable      , acceptVariables     , dropVariables     ) ;
  IFBOTH( torrent       , acceptTorrents      , dropTorrents      ) ;
  IFBOTH( camera        , acceptCameras       , dropCameras       ) ;
  IFBOTH( face          , acceptFaces         , dropFaces         ) ;
  IFBOTH( star          , acceptStars         , dropStars         ) ;
  IFBOTH( phoneme       , acceptPhonemes      , dropPhonemes      ) ;
  IFBOTH( model         , acceptModels        , dropModels        ) ;
  IFBOTH( reality       , acceptReality       , dropReality       ) ;
  IFBOTH( colorgroup    , acceptColorGroups   , dropColorGroups   ) ;
  IFBOTH( setsalgebra   , acceptSetsAlgebras  , dropSetsAlgebras  ) ;
  IFCAST( font          , acceptFont          , dropFont          ) ;
  IFCAST( pen           , acceptPen           , dropPen           ) ;
  IFCAST( brush         , acceptBrush         , dropBrush         ) ;
  IFCAST( gradient      , acceptGradient      , dropGradient      ) ;
  ///////////////////////////////////////////////////////////////////
  if (mime->hasImage() && acceptImageDrop())                        {
    QImage image = qvariant_cast<QImage>(mime->imageData())         ;
    return dropImage ( source , pos , image )                       ;
  }                                                                 ;
  if (mime->hasText() && acceptTextDrop())                          {
    return dropText  ( source , pos , mime -> text () )             ;
  }                                                                 ;
  if (mime->hasHtml() && acceptHtmlDrop())                          {
    return dropHtml  ( source , pos , mime -> html () )             ;
  }                                                                 ;
  if (mime->hasUrls() && acceptUrlsDrop())                          {
    return dropUrls  ( source , pos , mime -> urls () )             ;
  }                                                                 ;
  if (mime->hasColor() && acceptColorDrop())                        {
    QColor color = qvariant_cast<QColor>(mime->colorData())         ;
    return dropColor ( source , pos , color )                       ;
  }                                                                 ;
  ///////////////////////////////////////////////////////////////////
  if (acceptPrivate(mime))                                          {
    return dropPrivate ( source , mime , pos )                      ;
  }                                                                 ;
  ///////////////////////////////////////////////////////////////////
  return false                                                      ;
  #undef  IFBOTH
  #undef  IFCAST
  #undef  SITX
  #undef  DITE
  #undef  HASD
}

#define GF(Function,IT)                                      \
bool N::AbstractGui::Function(QWidget * source,QPointF pos,IT) \
{                                                            \
  return false ;                                             \
}

GF( dropText  , const QString     & text  )
GF( dropUrls  , const QList<QUrl> & urls  )
GF( dropImage , const QImage      & image )
GF( dropHtml  , const QString     & html  )
GF( dropColor , const QColor      & color )

#undef  GF

#define DG(FUNCTION)                                                            \
bool N::AbstractGui::FUNCTION(QWidget * source,QPointF pos,const UUIDs & Uuids) \
{                                                                               \
  Q_UNUSED ( source )                                                         ; \
  Q_UNUSED ( pos    )                                                         ; \
  Q_UNUSED ( Uuids  )                                                         ; \
  return false ;                                                                \
}
#define DX(FUNCTION)                                                            \
bool N::AbstractGui::FUNCTION(QWidget * source,QPointF pos,const SUID uuid)     \
{                                                                               \
  Q_UNUSED ( source )                                                         ; \
  Q_UNUSED ( pos    )                                                         ; \
  Q_UNUSED ( uuid   )                                                         ; \
  return false ;                                                                \
}

///////////////////////
DG( dropUuids         )
DG( dropTags          )
DG( dropPictures      )
DG( dropPeople        )
DG( dropAudios        )
DG( dropVideos        )
DG( dropAlbums        )
DG( dropDivisions     )
DG( dropURIs          )
DG( dropBookmarks     )
DG( dropShapes        )
DG( dropMembers       )
DG( dropSets          )
DG( dropActions       )
DG( dropDecision      )
DG( dropCondition     )
DG( dropExecution     )
DG( dropSqlTable      )
DG( dropDatabase      )
DG( dropTask          )
DG( dropNation        )
DG( dropContour       )
DG( dropManifold      )
DG( dropSources       )
DG( dropDocuments     )
DG( dropEyes          )
DG( dropHairs         )
DG( dropKeywords      )
DG( dropTerminologies )
DG( dropKnowledge     )
DG( dropFields        )
DG( dropKnowledgeBase )
DG( dropSqlColumn     )
DG( dropCommodities   )
DG( dropOrganizations )
DG( dropBlobs         )
DG( dropVariables     )
DG( dropTorrents      )
DG( dropCameras       )
DG( dropFaces         )
DG( dropColorGroups   )
DG( dropSetsAlgebras  )
DG( dropNames         )
DG( dropStars         )
DG( dropPhonemes      )
DG( dropModels        )
DG( dropReality       )
///////////////////////
DX( dropGender        )
DX( dropFont          )
DX( dropPen           )
DX( dropBrush         )
DX( dropGradient      )
///////////////////////

#undef  DX
#undef  DG


"""
