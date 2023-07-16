# -*- coding: utf-8 -*-
##############################################################################
## 物件關聯性
##############################################################################
import os
import sys
import getopt
import time
import datetime
import requests
import threading
##############################################################################
import mysql . connector
from   mysql . connector              import Error
##############################################################################
import AITK
from   AITK . Database  . Query       import Query
from   AITK . Database  . Connection  import Connection
from   AITK . Database  . Columns     import Columns
##############################################################################
Relations         =                                                        { \
  "Ignore"        :  0                                                     , \
  "Subordination" :  1                                                     , \
  "Icon"          :  2                                                     , \
  "Sexuality"     :  3                                                     , \
  "Trigger"       :  4                                                     , \
  "StartTrigger"  :  5                                                     , \
  "FinalTrigger"  :  6                                                     , \
  "Action"        :  7                                                     , \
  "Condition"     :  8                                                     , \
  "Synonymous"    :  9                                                     , \
  "Equivalent"    : 10                                                     , \
  "Contains"      : 11                                                     , \
  "Using"         : 12                                                     , \
  "Possible"      : 13                                                     , \
  "Originate"     : 14                                                     , \
  "Capable"       : 15                                                     , \
  "Estimate"      : 16                                                     , \
  "Alias"         : 17                                                     , \
  "Counterpart"   : 18                                                     , \
  "Explain"       : 19                                                     , \
  "Fuzzy"         : 20                                                     , \
  "Greater"       : 21                                                     , \
  "Less"          : 22                                                     , \
  "Before"        : 23                                                     , \
  "After"         : 24                                                     , \
  "Tendency"      : 25                                                     , \
  "Different"     : 26                                                     , \
  "Acting"        : 27                                                     , \
  "Forgotten"     : 28                                                     , \
  "Google"        : 29                                                     , \
  "Facebook"      : 30                                                     , \
  "Prerequisite"  : 31                                                     , \
  "Successor"     : 32                                                     , \
  "Candidate"     : 33                                                     , \
  "Face"          : 34                                                     , \
  "Mouth"         : 35                                                     , \
  "Eye"           : 36                                                     , \
  "Iris"          : 37                                                     , \
  "Nose"          : 38                                                     , \
  "Tit"           : 39                                                     , \
  "Umbilicus"     : 40                                                     , \
  "Pussy"         : 41                                                     , \
  "Tattoo"        : 42                                                     , \
  "Texture"       : 43                                                     , \
  "End"           : 44                                                     , \
}
##############################################################################
Types                 =                                                    { \
  "None"              :   0                                                , \
  "Type"              :   1                                                , \
  "Language"          :   2                                                , \
  "Name"              :   3                                                , \
  "Locality"          :   4                                                , \
  "Action"            :   5                                                , \
  "Relevance"         :   6                                                , \
  "People"            :   7                                                , \
  "Resource"          :   8                                                , \
  "Picture"           :   9                                                , \
  "Audio"             :  10                                                , \
  "Video"             :  11                                                , \
  "PlainText"         :  12                                                , \
  "XML"               :  13                                                , \
  "File"              :  14                                                , \
  "Schedule"          :  15                                                , \
  "Task"              :  16                                                , \
  "Acupuncture"       :  17                                                , \
  "DataTypes"         :  18                                                , \
  "Eyes"              :  19                                                , \
  "Hairs"             :  20                                                , \
  "Meridian"          :  21                                                , \
  "Star"              :  22                                                , \
  "TopLevelDomain"    :  23                                                , \
  "SecondLevelDomain" :  24                                                , \
  "Keyword"           :  25                                                , \
  "DomainName"        :  26                                                , \
  "Username"          :  27                                                , \
  "Encoding"          :  28                                                , \
  "KeywordRelation"   :  29                                                , \
  "URL"               :  30                                                , \
  "EMail"             :  31                                                , \
  "IPv4"              :  32                                                , \
  "IPv6"              :  33                                                , \
  "Race"              :  34                                                , \
  "Particle"          :  35                                                , \
  "Composite"         :  36                                                , \
  "Paper"             :  37                                                , \
  "Organization"      :  38                                                , \
  "NeuralTypes"       :  39                                                , \
  "Occupation"        :  40                                                , \
  "Meaning"           :  41                                                , \
  "MimeTypes"         :  42                                                , \
  "Nation"            :  43                                                , \
  "Administrative"    :  44                                                , \
  "Currency"          :  45                                                , \
  "CurrencyPair"      :  46                                                , \
  "Flow"              :  47                                                , \
  "Document"          :  48                                                , \
  "DecisionTable"     :  49                                                , \
  "DecisionTree"      :  50                                                , \
  "Equipment"         :  51                                                , \
  "Face"              :  52                                                , \
  "OperationSystem"   :  53                                                , \
  "ParamentType"      :  54                                                , \
  "Parameter"         :  55                                                , \
  "Surname"           :  56                                                , \
  "VCF"               :  57                                                , \
  "Script"            :  58                                                , \
  "Source"            :  59                                                , \
  "Palette"           :  60                                                , \
  "Knowledge"         :  61                                                , \
  "Field"             :  62                                                , \
  "KnowledgeBase"     :  63                                                , \
  "Gallery"           :  64                                                , \
  "Continent"         :  65                                                , \
  "Point"             :  66                                                , \
  "Contour"           :  67                                                , \
  "Line"              :  68                                                , \
  "Surface"           :  69                                                , \
  "MeaningTypes"      :  70                                                , \
  "Project"           :  71                                                , \
  "ProjectType"       :  72                                                , \
  "MathType"          :  73                                                , \
  "MathObject"        :  74                                                , \
  "Tag"               :  75                                                , \
  "Album"             :  76                                                , \
  "Sexuality"         :  77                                                , \
  "SqlDataType"       :  78                                                , \
  "Coding"            :  79                                                , \
  "Compound"          :  80                                                , \
  "RNA"               :  81                                                , \
  "DNA"               :  82                                                , \
  "Location"          :  83                                                , \
  "Chromosome"        :  84                                                , \
  "Statistics"        :  85                                                , \
  "DocumentFile"      :  86                                                , \
  "Calendar"          :  87                                                , \
  "Panel"             :  88                                                , \
  "Execution"         :  89                                                , \
  "GroupRelation"     :  90                                                , \
  "Division"          :  91                                                , \
  "Period"            :  92                                                , \
  "Variable"          :  93                                                , \
  "Body"              :  94                                                , \
  "Organ"             :  95                                                , \
  "Phone"             :  96                                                , \
  "CountryCode"       :  97                                                , \
  "AreaCode"          :  98                                                , \
  "Trigger"           :  99                                                , \
  "Rectangle"         : 100                                                , \
  "Painting"          : 101                                                , \
  "Graphics"          : 102                                                , \
  "Length"            : 103                                                , \
  "Shapes"            : 104                                                , \
  "Manifolds"         : 105                                                , \
  "POSet"             : 106                                                , \
  "SetMember"         : 107                                                , \
  "Condition"         : 108                                                , \
  "Indicator"         : 109                                                , \
  "Commodity"         : 110                                                , \
  "Package"           : 111                                                , \
  "Version"           : 112                                                , \
  "Camera"            : 113                                                , \
  "Light"             : 114                                                , \
  "IPA"               : 115                                                , \
  "SqlConnection"     : 116                                                , \
  "SqlItem"           : 117                                                , \
  "SqlTable"          : 118                                                , \
  "SqlPlan"           : 119                                                , \
  "Enumeration"       : 120                                                , \
  "SqlServer"         : 121                                                , \
  "Weight"            : 122                                                , \
  "Energy"            : 123                                                , \
  "Area"              : 124                                                , \
  "DNS"               : 125                                                , \
  "Newsgroup"         : 126                                                , \
  "Celestial"         : 127                                                , \
  "Equation"          : 128                                                , \
  "Component"         : 129                                                , \
  "SqlConstraint"     : 130                                                , \
  "Matrix"            : 131                                                , \
  "Sentence"          : 132                                                , \
  "Paragraph"         : 133                                                , \
  "Acoustic"          : 134                                                , \
  "Terminology"       : 135                                                , \
  "Array"             : 136                                                , \
  "Bound"             : 137                                                , \
  "Consanguinity"     : 138                                                , \
  "Kinship"           : 139                                                , \
  "Genealogy"         : 140                                                , \
  "Sketch"            : 141                                                , \
  "CppState"          : 142                                                , \
  "Spreadsheet"       : 143                                                , \
  "Nucleus"           : 144                                                , \
  "ClfType"           : 145                                                , \
  "RuleBase"          : 146                                                , \
  "Potential"         : 147                                                , \
  "SetsAlgebra"       : 148                                                , \
  "ColorGroup"        : 149                                                , \
  "InternetDomain"    : 150                                                , \
  "CCD"               : 151                                                , \
  "Obsolete"          : 152                                                , \
  "Pending"           : 153                                                , \
  "Coroutine"         : 154                                                , \
  "Semantic"          : 155                                                , \
  "Concept"           : 156                                                , \
  "Ideograph"         : 157                                                , \
  "Subgroup"          : 158                                                , \
  "FaceShape"         : 159                                                , \
  "Culture"           : 160                                                , \
  "Phoneme"           : 161                                                , \
  "EyesShape"         : 162                                                , \
  "StyleSheet"        : 163                                                , \
  "Stroke"            : 164                                                , \
  "Grapheme"          : 165                                                , \
  "Emotion"           : 166                                                , \
  "Entry"             : 167                                                , \
  "Reference"         : 168                                                , \
  "Constant"          : 169                                                , \
  "StellarSpectrum"   : 170                                                , \
  "EarthSpot"         : 171                                                , \
  "Account"           : 172                                                , \
  "FutureIndex"       : 173                                                , \
  "StockSecurity"     : 174                                                , \
  "EconomicIndex"     : 175                                                , \
  "VideoNote"         : 176                                                , \
  "Description"       : 177                                                , \
  "Reality"           : 178                                                , \
  "Model"             : 179                                                , \
  "MusicAlbum"        : 180                                                , \
  "HistoryType"       : 181                                                , \
  "History"           : 182                                                , \
  "ITU"               : 183                                                , \
  "Place"             : 184                                                , \
  "Station"           : 185                                                , \
  "Role"              : 186                                                , \
  "Course"            : 187                                                , \
  "Lesson"            : 188                                                , \
  "IMApp"             : 189                                                , \
  "InstantMessage"    : 190                                                , \
  "TimeZone"          : 191                                                , \
  "Address"           : 192                                                , \
  "Lecture"           : 193                                                , \
  "Trade"             : 194                                                , \
  "Token"             : 195                                                , \
  "Class"             : 196                                                , \
  "Fragment"          : 197                                                , \
  "AgeGroup"          : 198                                                , \
  "Proficiency"       : 199                                                , \
  "BankAccount"       : 200                                                , \
  "Taxonomy"          : 201                                                , \
  "Species"           : 202                                                , \
  "Blood"             : 203                                                , \
  "BloodGroup"        : 204                                                , \
  "NationType"        : 205                                                , \
  "FileExtension"     : 206                                                , \
  "Host"              : 207                                                , \
  "WebPage"           : 208                                                , \
  "SexPosition"       : 209                                                , \
}
##############################################################################
##
##############################################################################
class Relation           ( Columns                                         ) :
  ############################################################################
  global Relations
  global Types
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    self . Clear         (                                                   )
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    return
  ############################################################################
  def setRelationEmpty     ( self                                          ) :
    self . setColumnsEmpty (                                                 )
    self . Clear           (                                                 )
    return
  ############################################################################
  def Clear              ( self                                            ) :
    ##########################################################################
    self . Columns     = [                                                   ]
    self . Id          = 0
    self . First       = 0
    self . T1          = 0
    self . Second      = 0
    self . T2          = 0
    self . Relation    = 0
    self . Position    = 0
    self . Reverse     = 0
    self . Prefer      = 0
    self . Membership  = 0
    self . Description = 0
    self . Operator    = 0
    ##########################################################################
    return
  ############################################################################
  def assign             ( self , item                                     ) :
    ##########################################################################
    self . Columns     = item . Columns
    self . Id          = item . Id
    self . First       = item . First
    self . T1          = item . T1
    self . Second      = item . Second
    self . T2          = item . T2
    self . Relation    = item . Relation
    self . Position    = item . Position
    self . Reverse     = item . Reverse
    self . Prefer      = item . Prefer
    self . Membership  = item . Membership
    self . Description = item . Description
    self . Operator    = item . Operator
    ##########################################################################
    return
  ############################################################################
  def set                ( self , item , value                             ) :
    ##########################################################################
    a = item . lower     (                                                   )
    ##########################################################################
    if ( "id"           == a ) :
      self . Id          = value
    if ( "first"        == a ) :
      self . First       = int ( value )
    if ( "t1"           == a ) :
      self . T1          = int ( value )
    if ( "second"       == a ) :
      self . Second      = int ( value )
    if ( "t2"           == a ) :
      self . T2          = int ( value )
    if ( "relation"     == a ) :
      self . Relation    = int ( value )
    if ( "position"     == a ) :
      self . Position    = int ( value )
    if ( "reverse"      == a ) :
      self . Reverse     = int ( value )
    if ( "prefer"       == a ) :
      self . Prefer      = int ( value )
    if ( "membership"   == a ) :
      self . Membership  = value
    if ( "description"  == a ) :
      self . Description = int ( value )
    if ( "operator"     == a ) :
      self . Operator    = int ( value )
    ##########################################################################
    return
  ############################################################################
  def get                ( self , item                                     ) :
    ##########################################################################
    a = item . lower     (                                                   )
    ##########################################################################
    if ( "id"          == a ) :
      return self . Id
    if ( "first"       == a ) :
      return self . First
    if ( "t1"          == a ) :
      return self . T1
    if ( "second"      == a ) :
      return self . Second
    if ( "t2"          == a ) :
      return self . T2
    if ( "relation"    == a ) :
      return self . Relation
    if ( "position"    == a ) :
      return self . Position
    if ( "reverse"     == a ) :
      return self . Reverse
    if ( "prefer"      == a ) :
      return self . Prefer
    if ( "membership"  == a ) :
      return self . Membership
    if ( "description" == a ) :
      return self . Description
    if ( "operator"    == a ) :
      return self . Operator
    ##########################################################################
    return ""
  ############################################################################
  def toJson   ( self                                                      ) :
    ##########################################################################
    return     { "id"          : self . Id                                 , \
                 "first"       : self . First                              , \
                 "t1"          : self . T1                                 , \
                 "second"      : self . Second                             , \
                 "t2"          : self . T2                                 , \
                 "relation"    : self . Relation                           , \
                 "position"    : self . Position                           , \
                 "reverse"     : self . Reverse                            , \
                 "prefer"      : self . Prefer                             , \
                 "membership"  : self . Membership                         , \
                 "description" : self . Description                        , \
                 "operator"    : self . Operator                             }
  ############################################################################
  def fromJson ( self , JSON                                               ) :
    ##########################################################################
    self . Id          = JSON [ "id"                                         ]
    self . First       = JSON [ "first"                                      ]
    self . T1          = JSON [ "t1"                                         ]
    self . Second      = JSON [ "second"                                     ]
    self . T2          = JSON [ "t2"                                         ]
    self . Relation    = JSON [ "relation"                                   ]
    self . Position    = JSON [ "position"                                   ]
    self . Reverse     = JSON [ "reverse"                                    ]
    self . Prefer      = JSON [ "prefer"                                     ]
    self . Membership  = JSON [ "membership"                                 ]
    self . Description = JSON [ "description"                                ]
    self . Operator    = JSON [ "operator"                                   ]
    ##########################################################################
    return
  ############################################################################
  def Value           ( self , item                                        ) :
    return self . get (        item                                          )
  ############################################################################
  def Values            ( self , items                                     ) :
    ##########################################################################
    I   =               [                                                    ]
    ##########################################################################
    for x in items                                                           :
      I . append        ( str ( self . Value ( x ) )                         )
    ##########################################################################
    return " , " . join ( I                                                  )
  ############################################################################
  def tableItems ( self                                                    ) :
    ##########################################################################
    return       [ "id"                                                    , \
                   "first"                                                 , \
                   "t1"                                                    , \
                   "second"                                                , \
                   "t2"                                                    , \
                   "relation"                                              , \
                   "position"                                              , \
                   "reverse"                                               , \
                   "prefer"                                                , \
                   "membership"                                            , \
                   "description"                                             ]
                   ## "operator"                                             ]
  ############################################################################
  def pair         ( self , item                                           ) :
    v = self . get (        item                                             )
    return f"`{item}` = {v}"
  ############################################################################
  def FullList ( self                                                      ) :
    return     [ "t1"                                                      , \
                 "t2"                                                      , \
                 "relation"                                                , \
                 "first"                                                   , \
                 "second"                                                  , \
                 "position"                                                  ]
  ############################################################################
  def ExactList ( self                                                     ) :
    return      [ "t1"                                                     , \
                  "t2"                                                     , \
                  "relation"                                               , \
                  "first"                                                  , \
                  "second"                                                   ]
  ############################################################################
  def FirstList ( self                                                     ) :
    return      [ "t1"                                                     , \
                  "t2"                                                     , \
                  "relation"                                               , \
                  "first"                                                    ]
  ############################################################################
  def SecondList ( self                                                    ) :
    return       [ "t1"                                                    , \
                   "t2"                                                    , \
                   "relation"                                              , \
                   "second"                                                  ]
  ############################################################################
  def isFirst  ( self , F                                                  ) :
    return     ( F == self . First                                           )
  ############################################################################
  def isSecond ( self , S                                                  ) :
    return     ( S == self . Second                                          )
  ############################################################################
  def isType ( self , t1 , t2                                              ) :
    ##########################################################################
    if       ( self . T1 != t1                                             ) :
      return False
    ##########################################################################
    if       ( self . T2 != t2                                             ) :
      return False
    ##########################################################################
    return True
  ############################################################################
  def isT1 ( self , t1                                                     ) :
    return ( t1 == self . T1                                                 )
  ############################################################################
  def isT2 ( self , t2                                                     ) :
    return ( t2 == self . T2                                                 )
  ############################################################################
  def isRelation ( self , R                                                ) :
    return       ( R == self . Relation                                      )
  ############################################################################
  def setT1           ( self , N                                           ) :
    ##########################################################################
    self . T1 = Types [        N                                             ]
    ##########################################################################
    return
  ############################################################################
  def setT2           ( self , N                                           ) :
    ##########################################################################
    self . T2 = Types [        N                                             ]
    ##########################################################################
    return
  ############################################################################
  def setRelation               ( self , N                                 ) :
    ##########################################################################
    self . Relation = Relations [        N                                   ]
    ##########################################################################
    return
  ############################################################################
  def ExactItem           ( self , Options = "" , Limits = ""              ) :
    ##########################################################################
    L = self . ExactList  (                                                  )
    Q = self . QueryItems ( L , Options , Limits                             )
    ##########################################################################
    return Q
  ############################################################################
  def FirstItem           ( self , Options = "" , Limits = ""              ) :
    ##########################################################################
    L = self . FirstList  (                                                  )
    Q = self . QueryItems ( L , Options , Limits                             )
    ##########################################################################
    return Q
  ############################################################################
  def SecondItem          ( self , Options = "" , Limits = ""              ) :
    ##########################################################################
    L = self . SecondList (                                                  )
    Q = self . QueryItems ( L , Options , Limits                             )
    ##########################################################################
    return Q
  ############################################################################
  def Last                ( self , Table                                   ) :
    WS = self . FirstItem ( "order by `position` desc" , "limit 0,1"         )
    return f"select `position` from {Table} {WS} ;"
  ############################################################################
  def ExactColumn ( self , Table , Item , Options = "" , Limits = ""       ) :
    WS = self . ExactItem ( Options , Limits                                 )
    return f"select {Item} from {Table} {WS} ;"
  ############################################################################
  def InsertItems      ( self , Table , items                              ) :
    ##########################################################################
    JI = self . join   ( items , " , "                                       )
    VL = self . Values ( items                                               )
    ##########################################################################
    return f"insert into {Table} ( {JI} ) values ( {VL} ) ;"
  ############################################################################
  def Insert                  ( self , Table                               ) :
    L = self . FullList       (                                              )
    return self . InsertItems ( Table , L                                    )
  ############################################################################
  def DeleteItems          ( self , Table , items                          ) :
    QI = self . QueryItems (                items                            )
    return f"delete from {Table} {QI} ;"
  ############################################################################
  def Delete                  ( self , Table                               ) :
    L = self . ExactList      (                                              )
    return self . DeleteItems (        Table , L                             )
  ############################################################################
  def WipeOut                 ( self , Table                               ) :
    L = self . FirstList      (                                              )
    return self . DeleteItems (        Table , L                             )
  ############################################################################
  def obtain                   ( self , R                                  ) :
    ##########################################################################
    List   = self . tableItems (                                             )
    CNT    = 0
    ##########################################################################
    for x in List                                                            :
      self . set               ( x , R [ CNT ]                               )
      CNT += 1
    ##########################################################################
    return True
  ############################################################################
  def Subordination         ( self                                         , \
                              DB                                           , \
                              Table                                        , \
                              Options = "order by `position` asc"          , \
                              Limits  = ""                                 ) :
    W = self . FirstItem    ( Options , Limits                               )
    Q = f"select `second` from {Table} {W} ;"
    return DB . ObtainUuids ( Q                                              )
  ############################################################################
  def GetOwners             ( self                                         , \
                              DB                                           , \
                              Table                                        , \
                              Options = "order by `id` asc"                , \
                              Limits  = ""                                 ) :
    W = self . SecondItem   ( Options , Limits                               )
    Q = f"select `first` from {Table} {W} ;"
    return DB . ObtainUuids ( Q                                              )
  ############################################################################
  def CountFirst           ( self , DB , Table                             ) :
    ##########################################################################
    WW = self . SecondItem (                                                 )
    QQ = f"select count(*) from {Table} {WW} ;"
    DB . Query             ( QQ                                              )
    rr = DB   . FetchOne   (                                                 )
    ##########################################################################
    if                     ( rr in [ False , None                        ] ) :
      return 0
    ##########################################################################
    if                     ( len ( rr ) != 1                               ) :
      return 0
    ##########################################################################
    return int             ( rr [ 0                                        ] )
  ############################################################################
  def CountSecond         ( self , DB , Table                              ) :
    ##########################################################################
    WW = self . FirstItem (                                                  )
    QQ = f"select count(*) from {Table} {WW} ;"
    DB . Query            ( QQ                                               )
    rr = DB . FetchOne    (                                                  )
    ##########################################################################
    if                    ( rr in [ False , None                         ] ) :
      return 0
    ##########################################################################
    if                    ( len ( rr ) != 1                                ) :
      return 0
    ##########################################################################
    return int            ( rr [ 0                                         ] )
  ############################################################################
  def Assure            ( self , DB , Table                                ) :
    ##########################################################################
    QQ = self . WipeOut (             Table                                  )
    DB . Query          ( QQ                                                 )
    QQ = self . Insert  (             Table                                  )
    DB . Query          ( QQ                                                 )
    ##########################################################################
    return
  ############################################################################
  def Append           ( self , DB , Table                                 ) :
    QQ = self . Insert (             Table                                   )
    return DB . Query  ( QQ                                                  )
  ############################################################################
  def Join                     ( self , DB , Table                         ) :
    ##########################################################################
    QQ    = self . ExactColumn ( Table , "id"                                )
    DB    . Query              ( QQ                                          )
    Lists = DB . FetchAll      (                                             )
    if ( not Lists ) or ( Lists == None ) or ( len ( Lists ) <= 0 )          :
      pass
    else                                                                     :
      return False
    ##########################################################################
    ID    = -1
    QQ    = self . Last        ( Table                                       )
    DB    . Query              ( QQ                                          )
    rr    = DB . FetchOne      (                                             )
    if                         ( not rr                                    ) :
      pass
    else                                                                     :
      ID  = rr                 [ 0                                           ]
    ID    = ID + 1
    ##########################################################################
    self . Position = ID
    ##########################################################################
    return self . Append       ( DB , Table                                  )
  ############################################################################
  def Joins       ( self , DB , Table , Lists                              ) :
    ##########################################################################
    for x in Lists                                                           :
      self . set  ( "second" , x                                             )
      self . Join ( DB       , Table                                         )
    ##########################################################################
    return
  ############################################################################
  def PrefectOrder            ( self , DB , Table                          ) :
    ##########################################################################
    IX     =                  [                                              ]
    WH     = self . FirstItem ( "order by `position` asc"                    )
    QQ     = f"select `id` from {Table} {WH} ;"
    IX     = DB . ObtainUuids ( QQ                                           )
    pos    = 0
    ##########################################################################
    for xx in IX                                                             :
      ########################################################################
      QQ   = f"update {Table} set `position` = {pos} where `id` = {xx} ;"
      DB   . Query            ( QQ                                           )
      pos += 1
    ##########################################################################
    return
  ############################################################################
  def ObtainOwners               ( self , DB , Table , Members , TMP       ) :
    ##########################################################################
    for nsx in TMP                                                           :
      self    . set              ( "second" , nsx                            )
      CC      = self . GetOwners ( DB , Table                                )
      Members . extend           ( CC                                        )
    ##########################################################################
    return Members
  ############################################################################
  def RepositionByFirst ( self , DB , Table , UUIDs                        ) :
    ##########################################################################
    FIRST = self . get  ( "first"                                            )
    T1    = self . get  ( "t1"                                               )
    T2    = self . get  ( "t2"                                               )
    REL   = self . get  ( "relation"                                         )
    POS   = 0
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      QQ  = f"""update {Table} set `position` = {POS}
                where ( `first` = {FIRST} )
                  and ( `t1` = {T1} )
                  and ( `t2` = {T2} )
                  and ( `relation` = {REL} )
                  and ( `second` = {UUID} ) ;"""
      QQ  = " " . join  ( QQ . split ( )                                     )
      ########################################################################
      DB  . Query       ( QQ                                                 )
      POS = POS + 1
    ##########################################################################
    return True
  ############################################################################
  def Organize            ( self , DB , Table                              ) :
    ##########################################################################
    WH = self . FirstItem ( "order by `position` asc"                        )
    QQ = f"select `id` from {Table} {WH} ;"
    IX = DB . ObtainUuids ( QQ                                               )
    if                    ( len ( IX ) <= 0                                ) :
      return False
    ##########################################################################
    pos    = 0
    ##########################################################################
    DB     . LockWrites   ( [ Table                                        ] )
    ##########################################################################
    for iv in IX                                                             :
      QQ   = f"update {Table} set `position` = {pos} where `id` = {iv} ;"
      DB   . Query        ( QQ                                               )
      pos += 1
    ##########################################################################
    DB . UnlockTables     (                                                  )
    ##########################################################################
    return True
  ############################################################################
  def Ordering                ( self , DB , Table , UUIDs                  ) :
    ##########################################################################
    pos    = 0
    DB     . LockWrite        ( [ Table                                    ] )
    ##########################################################################
    for xu in UUIDs                                                          :
      ########################################################################
      self . set              ( "second" , xu                                )
      WH   = self . ExactItem (                                              )
      QQ   = f"update {Table} set `position` = {pos} {WH} ;"
      DB   . Query            ( QQ                                           )
      pos += 1
    ##########################################################################
    DB     . UnlockTables     (                                              )
    ##########################################################################
    return True
##############################################################################
