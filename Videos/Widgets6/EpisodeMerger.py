# -*- coding: utf-8 -*-
##############################################################################
## EpisodeMerger
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
from   PySide6                            import QtCore
from   PySide6                            import QtGui
from   PySide6                            import QtWidgets
from   PySide6 . QtCore                   import *
from   PySide6 . QtGui                    import *
from   PySide6 . QtWidgets                import *
from   AITK    . Qt6                      import *
##############################################################################
from   AITK    . Documents  . JSON        import Load as LoadJson
from   AITK    . Essentials . Relation    import Relation
##############################################################################
from   AITK    . Calendars  . StarDate    import StarDate
from   AITK    . Calendars  . Periode     import Periode
from   AITK    . Videos     . Film        import Film as FilmItem
##############################################################################
class EpisodeMerger         ( TreeDock                                     ) :
  ############################################################################
  HavingMenu       = 1371434312
  ############################################################################
  emitNamesShow    = Signal (                                                )
  emitAppendPeople = Signal ( dict                                           )
  emitComplete     = Signal (                                                )
  emitAnalysis     = Signal (                                                )
  emitLog          = Signal ( str                                            )
  ############################################################################
  def __init__              ( self , parent = None , plan = None           ) :
    ##########################################################################
    super ( ) . __init__    (        parent        , plan                    )
    ##########################################################################
    self . dockingOrientation = Qt . Vertical
    self . dockingPlace       = Qt . RightDockWidgetArea
    self . dockingPlaces      = Qt . TopDockWidgetArea                     | \
                                Qt . BottomDockWidgetArea                  | \
                                Qt . LeftDockWidgetArea                    | \
                                Qt . RightDockWidgetArea
    ##########################################################################
    self . setColumnCount          ( 2                                       )
    self . setColumnHidden         ( 1 , True                                )
    self . setRootIsDecorated      ( False                                   )
    self . setAlternatingRowColors ( True                                    )
    ##########################################################################
    self . MountClicked            ( 1                                       )
    ##########################################################################
    self . assignSelectionMode     ( "ContiguousSelection"                   )
    ##########################################################################
    self . emitNamesShow     . connect ( self . show                         )
    self . emitAppendPeople  . connect ( self . appending                    )
    self . emitComplete      . connect ( self . CompleteMerge                )
    ##########################################################################
    self . setFunction             ( self . FunctionDocking , True           )
    self . setFunction             ( self . HavingMenu      , True           )
    ##########################################################################
    self . setAcceptDrops          ( True                                    )
    self . setDragEnabled          ( False                                   )
    self . setDragDropMode         ( QAbstractItemView . DropOnly            )
    ##########################################################################
    self . setMinimumSize          ( 80 , 80                                 )
    ##########################################################################
    return
  ############################################################################
  def sizeHint                   ( self                                    ) :
    return self . SizeSuggestion ( QSize ( 320 , 640 )                       )
  ############################################################################
  def PrepareForActions             ( self                                 ) :
    ##########################################################################
    self . AppendSideActionWithIcon ( "LimitedMerge"                       , \
                                      ":/images/merge-episode.png"         , \
                                      self . RunMergeAlbumLIMITED          , \
                                      True                                 , \
                                      False                                  )
    ##########################################################################
    return
  ############################################################################
  def AttachActions   ( self         ,                             Enabled ) :
    ##########################################################################
    self . LinkAction ( "Refresh"    , self . startup            , Enabled   )
    self . LinkAction ( "Delete"     , self . DeleteItems        , Enabled   )
    self . LinkAction ( "Start"      , self . ExecuteMergeEpisode , Enabled  )
    self . LinkAction ( "Copy"       , self . CopyToClipboard    , Enabled   )
    self . LinkAction ( "Paste"      , self . PasteItems         , Enabled   )
    self . LinkAction ( "Import"     , self . ImportGroups       , Enabled   )
    self . LinkAction ( "Select"     , self . SelectOne          , Enabled   )
    self . LinkAction ( "SelectAll"  , self . SelectAll          , Enabled   )
    self . LinkAction ( "SelectNone" , self . SelectNone         , Enabled   )
    ##########################################################################
    return
  ############################################################################
  def FocusIn                     ( self                                   ) :
    return self . defaultFocusIn  (                                          )
  ############################################################################
  def FocusOut                    ( self                                   ) :
    return self . defaultFocusOut (                                          )
  ############################################################################
  def Shutdown               ( self                                        ) :
    ##########################################################################
    self . StayAlive   = False
    self . LoopRunning = False
    ##########################################################################
    if                       ( self . isThreadRunning (                  ) ) :
      return False
    ##########################################################################
    self . AttachActions     ( False                                         )
    self . detachActionsTool (                                               )
    self . LinkVoice         ( None                                          )
    ##########################################################################
    self . Leave . emit      ( self                                          )
    ##########################################################################
    return True
  ############################################################################
  def singleClicked             ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def twiceClicked              ( self , item , column                     ) :
    ##########################################################################
    self . defaultSingleClicked (        item , column                       )
    ##########################################################################
    return
  ############################################################################
  def PrepareItem                    ( self , UUID , NAME                  ) :
    ##########################################################################
    TOTAL = self . topLevelItemCount (                                       )
    ##########################################################################
    UXID  = str                      ( UUID                                  )
    IT    = QTreeWidgetItem          (                                       )
    ##########################################################################
    IT    . setText                  ( 0 , NAME                              )
    IT    . setToolTip               ( 0 , UXID                              )
    IT    . setData                  ( 0 , Qt . UserRole , UUID              )
    ##########################################################################
    if                               ( TOTAL == 0                          ) :
      IT  . setCheckState            ( 0 , Qt . Checked                      )
    else                                                                     :
      IT  . setCheckState            ( 0 , Qt . Unchecked                    )
    ##########################################################################
    IT    . setTextAlignment         ( 1 , Qt.AlignRight                     )
    ##########################################################################
    return IT
  ############################################################################
  def DeleteItems                     ( self                               ) :
    ##########################################################################
    items  = self . selectedItems     (                                      )
    for item in items                                                        :
      self . pendingRemoveItem . emit ( item                                 )
    ##########################################################################
    return
  ############################################################################
  def appending                  ( self , JSON                             ) :
    ##########################################################################
    UUIDs = JSON                 [ "Uuids"                                   ]
    NAMEs = JSON                 [ "Names"                                   ]
    ##########################################################################
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME  = NAMEs              [ UUID                                      ]
      IT    = self . PrepareItem ( UUID , NAME                               )
      self  . addTopLevelItem    ( IT                                        )
    ##########################################################################
    self    . Notify             ( 5                                         )
    ##########################################################################
    return
  ############################################################################
  def startup        ( self                                                ) :
    ##########################################################################
    if               ( not self . isPrepared ( )                           ) :
      self . Prepare (                                                       )
    ##########################################################################
    self . clear     (                                                       )
    self . show      (                                                       )
    ##########################################################################
    return
  ############################################################################
  def allowedMimeTypes     ( self , mime                                   ) :
    formats = "album/uuids"
    return self . MimeType ( mime , formats                                  )
  ############################################################################
  def acceptDrop              ( self , sourceWidget , mimeData             ) :
    ##########################################################################
    if                        ( self == sourceWidget                       ) :
      return False
    ##########################################################################
    return self . dropHandler ( sourceWidget , self , mimeData               )
  ############################################################################
  def dropNew                            ( self                            , \
                                           sourceWidget                    , \
                                           mimeData                        , \
                                           mousePos                        ) :
    ##########################################################################
    if                                   ( self == sourceWidget            ) :
      return False
    ##########################################################################
    RDN     = self . RegularDropNew      ( mimeData                          )
    if                                   ( not RDN                         ) :
      return False
    ##########################################################################
    mtype   = self . DropInJSON          [ "Mime"                            ]
    UUIDs   = self . DropInJSON          [ "UUIDs"                           ]
    ##########################################################################
    if                                   ( mtype in [ "album/uuids" ]      ) :
      ########################################################################
      title = sourceWidget . windowTitle (                                   )
      CNT   = len                        ( UUIDs                             )
      FMT   = self . getMenuItem         ( "Copying"                         )
      MSG   = FMT  . format              ( title , CNT                       )
      self  . ShowStatus                 ( MSG                               )
    ##########################################################################
    return RDN
  ############################################################################
  def dropMoving             ( self , sourceWidget , mimeData , mousePos   ) :
    return self . defaultDropMoving ( sourceWidget , mimeData , mousePos     )
  ############################################################################
  def acceptAlbumsDrop ( self                                              ) :
    return True
  ############################################################################
  def dropAlbums                    ( self , source , pos , JSON           ) :
    return self . defaultDropInside ( source                               , \
                                      JSON                                 , \
                                      self . EpisodeToMerge                  )
  ############################################################################
  def EpisodeToMerge                 ( self , UUIDs                        ) :
    ##########################################################################
    COUNT  = len                     ( UUIDs                                 )
    if                               ( COUNT <= 0                          ) :
      return
    ##########################################################################
    DB     = self . ConnectDB        ( UsePure = True                        )
    if                               ( DB in [ False , None ]              ) :
      return
    ##########################################################################
    self   . setDroppingAction       ( True                                  )
    self   . OnBusy  . emit          (                                       )
    self   . setBustle               (                                       )
    ##########################################################################
    FMT    = self . getMenuItem      ( "Joining"                             )
    MSG    = FMT  . format           ( COUNT                                 )
    self   . ShowStatus              ( MSG                                   )
    self   . TtsTalk                 ( MSG , 1002                            )
    ##########################################################################
    NAMTAB = self . Tables           [ "Names"                               ]
    ##########################################################################
    NAMEs  = self . GetNames         ( DB , NAMTAB , UUIDs                   )
    for UUID in UUIDs                                                        :
      ########################################################################
      NAME = NAMEs                   [ UUID                                  ]
      if                             ( len ( NAME ) <= 0                   ) :
        NAMEs [ UUID ] = f"{UUID}"
    ##########################################################################
    self   . setVacancy              (                                       )
    self   . GoRelax . emit          (                                       )
    self   . setDroppingAction       ( False                                 )
    self   . ShowStatus              ( ""                                    )
    DB     . Close                   (                                       )
    ##########################################################################
    JSON   =                         { "Uuids" : UUIDs , "Names" : NAMEs     }
    self   . emitAppendPeople . emit ( JSON                                  )
    ##########################################################################
    return
  ############################################################################
  def Prepare             ( self                                           ) :
    ##########################################################################
    self . defaultPrepare ( "EpisodeMerger" , 2                              )
    ##########################################################################
    return
  ############################################################################
  def PasteItems                        ( self                             ) :
    ##########################################################################
    T     = qApp . clipboard ( ) . text (                                    )
    ##########################################################################
    if                                  ( len ( T ) <= 0                   ) :
      return
    ##########################################################################
    L     = T . split                   (                                    )
    UUIDs =                             [                                    ]
    for U in L                                                               :
      ########################################################################
      UX  = f"{U}"
      UX  = UX . strip                  (                                    )
      UX  = UX . rstrip                 (                                    )
      UX  = int                         ( UX                                 )
      if                                ( UX not in UUIDs                  ) :
        UUIDs . append                  ( UX                                 )
    ##########################################################################
    if                                  ( len ( UUIDs ) <= 0               ) :
      return
    ##########################################################################
    self  . Go                          ( self . PeopleToMerge , ( UUIDs , ) )
    ##########################################################################
    return
  ############################################################################
  def CopyToClipboard        ( self                                        ) :
    ##########################################################################
    self . DoCopyToClipboard (                                               )
    ##########################################################################
    return
  ############################################################################
  def ExecuteMerge             ( self , UUID , PUIDs , ICON                ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem            (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergeAll            ( DB   , UUID , PUIDs , ICON                  )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeAlbumNOTEs          ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem            (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergeNOTEs          ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( FLT . SQLs ) > 0                    ) :
      self . emitLog    . emit ( "\n" . join ( FLT . SQLs                  ) )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeAlbumURLs           ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem            (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergeURLs           ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( FLT . SQLs ) > 0                    ) :
      self . emitLog    . emit ( "\n" . join ( FLT . SQLs                  ) )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeAlbumICONs          ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem            (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergeICONs          ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( FLT . SQLs ) > 0                    ) :
      self . emitLog    . emit ( "\n" . join ( FLT . SQLs                  ) )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeAlbumGALLERYs       ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem           (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergeGALLERYs       ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( FLT . SQLs ) > 0                    ) :
      self . emitLog    . emit ( "\n" . join ( FLT . SQLs                  ) )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeAlbumVIDEOs         ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem           (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergeVIDEOs         ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( FLT . SQLs ) > 0                    ) :
      self . emitLog    . emit ( "\n" . join ( FLT . SQLs                  ) )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeAlbumPEOPLEs        ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem            (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergePEOPLEs        ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( FLT . SQLs ) > 0                    ) :
      self . emitLog    . emit ( "\n" . join ( FLT . SQLs                  ) )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeAlbumORGANIZATIONs  ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem            (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergeORGANIZATIONs  ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( FLT . SQLs ) > 0                    ) :
      self . emitLog    . emit ( "\n" . join ( FLT . SQLs                  ) )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def MergeAlbumLIMITED        ( self , UUID , PUIDs                       ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    FLT  = FilmItem            (                                             )
    FLT  . Settings = self . Settings
    FLT  . Tables   = self . Tables
    ##########################################################################
    FLT  . MergeLIMITED        ( DB   , UUID , PUIDs                         )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    if                         ( len ( FLT . SQLs ) > 0                    ) :
      self . emitLog    . emit ( "\n" . join ( FLT . SQLs                  ) )
    ##########################################################################
    self . emitComplete . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def CompleteMerge           ( self                                       ) :
    ##########################################################################
    self . setEnabled         ( True                                         )
    ##########################################################################
    msg  = self . getMenuItem ( "FinishMerge"                                )
    self . ShowStatus         ( msg                                          )
    self . Notify             ( 5                                            )
    self . Talk               ( msg , self . getLocality (                 ) )
    ##########################################################################
    return
  ############################################################################
  def ExecuteMergeEpisode             ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    ICON   = 0
    for i in range                    ( 0 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      CHK  = IT   . checkState        ( 0                                    )
      ########################################################################
      if                              ( CHK == Qt . Checked                ) :
        ICON = PUID
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs , ICON ,                )
    self   . Go                       ( self . ExecuteMerge , VAL            )
    ##########################################################################
    return
  ############################################################################
  def RunMergeAlbumNOTEs              ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . MergeAlbumNOTEs , VAL         )
    ##########################################################################
    return
  ############################################################################
  def RunMergeAlbumURLs               ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . MergeAlbumURLs , VAL          )
    ##########################################################################
    return
  ############################################################################
  def RunMergeAlbumIcons              ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . MergeAlbumICONs , VAL         )
    ##########################################################################
    return
  ############################################################################
  def RunMergeAlbumGalleries          ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . MergeAlbumGALLERYs , VAL      )
    ##########################################################################
    return
  ############################################################################
  def RunMergeAlbumVideos             ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . MergeAlbumVIDEOs , VAL        )
    ##########################################################################
    return
  ############################################################################
  def RunMergeAlbumPEOPLEs            ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . MergeAlbumPEOPLEs , VAL       )
    ##########################################################################
    return
  ############################################################################
  def RunMergeAlbumORGANIZATIONs      ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . MergeAlbumORGANIZATIONs , VAL )
    ##########################################################################
    return
  ############################################################################
  def RunMergeAlbumLIMITED            ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartMerge"                         )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs ,                       )
    self   . Go                       ( self . MergeAlbumLIMITED , VAL       )
    ##########################################################################
    return
  ############################################################################
  def ImportGroups                ( self                                   ) :
    ##########################################################################
    Filters  = self . getMenuItem ( "JsonFilters"                            )
    Name , t = QFileDialog . getOpenFileName                                 (
                                    self                                   , \
                                    self . windowTitle ( )                 , \
                                    ""                                     , \
                                    Filters                                  )
    ##########################################################################
    if                            ( len ( Name ) <= 0                      ) :
      self   . Notify             ( 1                                        )
      return
    ##########################################################################
    VAL      =                    ( Name ,                                   )
    self     . Go                 ( self . ImportEpisodeGroups , VAL         )
    ##########################################################################
    return
  ############################################################################
  def ImportEpisodeGroups          ( self , Filename                       ) :
    ##########################################################################
    ## GROUPs    = LoadJson           ( Filename                                )
    ##########################################################################
    ## if                             ( len ( GROUPs ) <= 0                   ) :
    ##   self    . Notify             ( 1                                       )
    ##   return
    ##########################################################################
    ## DB        = self . ConnectDB   ( UsePure = True                          )
    ## if                             ( self . NotOkay ( DB )                 ) :
    ##   return
    ##########################################################################
    ## PIT       = PeopleItem         (                                         )
    ## PIT       . Settings = self . Settings
    ## PIT       . Tables   = self . Tables
    ##########################################################################
    ## PLAN      = self . GetPlan     (                                         )
    ## TOTAL     = len                ( GROUPs                                  )
    ##########################################################################
    ## NAME      = self . getMenuItem ( "GroupMerge"                            )
    ## SECSC     = self . getMenuItem ( "SecsCounting"                          )
    ## ITEMC     = self . getMenuItem ( "ItemCounting"                          )
    ##########################################################################
    ## PID       = PLAN . Progress    ( NAME , "%v / %m"                        )
    ## PLAN      . ProgressText       ( PID  , f"{TOTAL}"                       )
    ## PLAN      . setRange           ( PID  , 0 , TOTAL                        )
    ## AT        = 0
    ## PLAN      . Start              ( PID  , AT , True                        )
    ## PLAN      . ProgressReady      ( PID                                     )
    ## PLAN      . setFrequency       ( PID  , SECSC , ITEMC                    )
    ##########################################################################
    ## for GROUP in GROUPs                                                      :
    ##   ########################################################################
    ##   AT      = AT + 1
    ##   ########################################################################
    ##   RUNNING = PLAN . isProgressRunning ( PID                               )
    ##   if                           ( not RUNNING                           ) :
    ##     continue
    ##   ########################################################################
    ##   NAME    = "," . join         ( str ( u ) for u in GROUP                )
    ##   PLAN    . setProgressValue   ( PID , AT                                )
    ##   PLAN    . ProgressText       ( PID , NAME                              )
    ##   ########################################################################
    ##   if                           ( len ( GROUP ) > 1                     ) :
    ##     ######################################################################
    ##     UUID  = GROUP              [ 0                                       ]
    ##     ICON  = GROUP              [ 0                                       ]
    ##     ######################################################################
    ##     PIT   . MergeAll           ( DB   , UUID , GROUP , ICON              )
    ##########################################################################
    ## time      . sleep              ( 1.0                                     )
    ## PLAN      . Finish             ( PID                                     )
    ##########################################################################
    ## DB        . Close              (                                         )
    ##########################################################################
    ## self      . Notify             ( 5                                       )
    ##########################################################################
    return True
  ############################################################################
  def ExecuteAnalysis          ( self , UUID , PUIDs , ICON                ) :
    ##########################################################################
    DB   = self . ConnectDB    ( UsePure = True                              )
    if                         ( DB in self . EmptySet                     ) :
      return
    ##########################################################################
    ## PIT  = PeopleItem          (                                             )
    ## PIT  . Settings = self . Settings
    ## PIT  . Tables   = self . Tables
    ##########################################################################
    ## PIT  . MergeAll            ( DB   , UUID , PUIDs , ICON                  )
    ##########################################################################
    DB   . Close               (                                             )
    ##########################################################################
    self . emitAnalysis . emit (                                             )
    ##########################################################################
    return
  ############################################################################
  def CompleteAnalysis        ( self                                       ) :
    ##########################################################################
    self . setEnabled         ( True                                         )
    ##########################################################################
    msg  = self . getMenuItem ( "FinishAnalysis"                             )
    self . ShowStatus         ( msg                                          )
    self . Notify             ( 5                                            )
    ##########################################################################
    return
  ############################################################################
  def AnalysisMergeALBUMs             ( self                               ) :
    ##########################################################################
    Total  = self . topLevelItemCount (                                      )
    IT     = self . topLevelItem      ( 0                                    )
    UUID   = self . itemUuid          ( IT                                   )
    UUIDs  =                          [ UUID                                 ]
    PUIDs  =                          [                                      ]
    ##########################################################################
    for i in range                    ( 1 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      ########################################################################
      if                              ( PUID not in UUIDs                  ) :
        UUIDs . append                ( PUID                                 )
        PUIDs . append                ( PUID                                 )
    ##########################################################################
    ICON   = 0
    for i in range                    ( 0 , Total                          ) :
      ########################################################################
      IT   = self . topLevelItem      ( i                                    )
      PUID = self . itemUuid          ( IT                                   )
      CHK  = IT   . checkState        ( 0                                    )
      ########################################################################
      if                              ( CHK == Qt . Checked                ) :
        ICON = PUID
    ##########################################################################
    if                                ( len ( PUIDs ) <= 0                 ) :
      self . Notify                   ( 1                                    )
      return
    ##########################################################################
    msg    = self . getMenuItem       ( "StartAnalysis"                      )
    self   . ShowStatus               ( msg                                  )
    ##########################################################################
    self   . setEnabled               ( False                                )
    VAL    =                          ( UUID , PUIDs , ICON ,                )
    self   . Go                       ( self . ExecuteAnalysis , VAL         )
    ##########################################################################
    return
  ############################################################################
  def CommandParser ( self , language , message , timestamp                ) :
    ##########################################################################
    TRX = self . Translations
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectAll"    , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    if ( self . WithinCommand ( language , "UI::SelectNone"   , message )  ) :
      return        { "Match" : True , "Message" : TRX [ "UI::SelectAll" ]   }
    ##########################################################################
    return          { "Match" : False                                        }
  ############################################################################
  def Menu                              ( self , pos                       ) :
    ##########################################################################
    if                                  ( not self . isPrepared (        ) ) :
      return False
    ##########################################################################
    doMenu = self . isFunction          ( self . HavingMenu                  )
    if                                  ( not doMenu                       ) :
      return False
    ##########################################################################
    self   . Notify                     ( 0                                  )
    ##########################################################################
    Total  = self . topLevelItemCount   (                                    )
    items , atItem , uuid = self . GetMenuDetails ( 0                        )
    mm     = MenuManager                ( self                               )
    ##########################################################################
    if                                  ( Total > 1                        ) :
      ########################################################################
      msg  = self . getMenuItem         ( "Merge"                            )
      icon = QIcon                      ( ":/images/play.png"                )
      mm   . addActionWithIcon          ( 7001 , icon , msg                  )
      mm   . addSeparator               (                                    )
      ########################################################################
      msg  = self . getMenuItem         ( "LimitedMerge"                     )
      icon = QIcon                      ( ":/images/first.png"               )
      mm   . addActionWithIcon          ( 7002 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "NoteMerge"                        )
      icon = QIcon                      ( ":/images/notes.png"               )
      mm   . addActionWithIcon          ( 7003 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "UrlMerge"                         )
      icon = QIcon                      ( ":/images/geography.png"           )
      mm   . addActionWithIcon          ( 7004 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "IconMerge"                        )
      icon = QIcon                      ( ":/images/gallery.png"             )
      mm   . addActionWithIcon          ( 7005 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "GalleryMerge"                     )
      icon = QIcon                      ( ":/images/galleries.png"           )
      mm   . addActionWithIcon          ( 7006 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "VideoMerge"                       )
      icon = QIcon                      ( ":/images/videoclip.png"           )
      mm   . addActionWithIcon          ( 7007 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "PeopleMerge"                      )
      icon = QIcon                      ( ":/images/buddy.png"               )
      mm   . addActionWithIcon          ( 7008 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "OrganizationMerge"                )
      icon = QIcon                      ( ":/images/company.png"             )
      mm   . addActionWithIcon          ( 7009 , icon , msg                  )
      ########################################################################
      msg  = self . getMenuItem         ( "Analysis"                         )
      icon = QIcon                      ( ":/images/checklist.png"           )
      mm   . addActionWithIcon          ( 7010 , icon , msg                  )
      mm   . addSeparator               (                                    )
    ##########################################################################
    self   . AppendRefreshAction        ( mm , 1001                          )
    ##########################################################################
    if                                  ( len ( items ) > 0                ) :
      self . AppendDeleteAction         ( mm , 1102                          )
    ##########################################################################
    msg    = self . getMenuItem         ( "Import"                           )
    icon   = QIcon                      ( ":/images/NewProject.png"          )
    mm     . addActionWithIcon          ( 5001 , icon , msg                  )
    ##########################################################################
    mm     . addSeparator               (                                    )
    ##########################################################################
    self   . LocalityMenu               ( mm                                 )
    self   . DockingMenu                ( mm                                 )
    ##########################################################################
    self   . AtMenu = True
    ##########################################################################
    mm     . setFont                    ( self    . menuFont ( )             )
    aa     = mm . exec_                 ( QCursor . pos      ( )             )
    at     = mm . at                    ( aa                                 )
    ##########################################################################
    self   . AtMenu = False
    ##########################################################################
    if                                  ( self . RunDocking   ( mm , aa )  ) :
      return True
    ##########################################################################
    if                                  ( self . HandleLocalityMenu ( at ) ) :
      return True
    ##########################################################################
    if                                  ( at == 1001                       ) :
      self . restart                    (                                    )
      return True
    ##########################################################################
    if                                  ( at == 1102                       ) :
      self . DeleteItems                (                                    )
      return True
    ##########################################################################
    if                                  ( at == 5001                       ) :
      self . ImportGroups               (                                    )
      return True
    ##########################################################################
    if                                  ( at == 7001                       ) :
      ########################################################################
      self . ExecuteMergeEpisode        (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7002                       ) :
      ########################################################################
      self . RunMergeAlbumLIMITED       (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7003                       ) :
      ########################################################################
      self . RunMergeAlbumNOTEs         (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7004                       ) :
      ########################################################################
      self . RunMergeAlbumURLs          (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7005                       ) :
      ########################################################################
      self . RunMergeAlbumIcons         (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7006                       ) :
      ########################################################################
      self . RunMergeAlbumGalleries     (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7007                       ) :
      ########################################################################
      self . RunMergeAlbumVideos        (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7008                       ) :
      ########################################################################
      self . RunMergeAlbumPEOPLEs       (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7009                       ) :
      ########################################################################
      self . RunMergeAlbumORGANIZATIONs (                                    )
      ########################################################################
      return True
    ##########################################################################
    if                                  ( at == 7010                       ) :
      ########################################################################
      self . AnalysisMergeALBUMs        (                                    )
      ########################################################################
      return True
    ##########################################################################
    return True
##############################################################################
