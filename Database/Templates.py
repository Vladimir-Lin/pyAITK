# -*- coding: utf-8 -*-

import os
import sys

Databases      =              { \
  "ERP"        : "erp"        , \
  "UUIDs"      : "uuids"      , \
  "Pictures"   : "pictures"   , \
  "People"     : "crowds"     , \
  "Cage"       : "cage"       , \
  "History"    : "history"    , \
  "Names"      : "names"      , \
  "Networks"   : "networks"   , \
  "Notes"      : "notes"      , \
  "Parameters" : "parameters" , \
  "Relations"  : "relations"  , \
  "Schedules"  : "schedules"  , \
  "Telecom"    : "telecom"    , \
  "Tasks"      : "tasks"      , \
  "Videos"     : "videos"       \
}

TemplateMyISAM =            { \
"$(Engine)"    : "MyISAM"   , \
"$(Options)"   : ";"          \
}

TemplateMerge =              { \
"$(Engine)"   : "MRG_MyISAM" , \
"$(Index)"    : "1"            \
}

# Single Unique IDentifier Table
UuidTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`type` integer default 0 ,
`used` integer default 1 ,
`previous` integer default 0 ,
`states` bigint default 0 ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `type` (`type`),
key `used` (`used`),
key `previous` (`previous`),
key `states` (`states`),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

ObjectUuidGroup       =                      { \
"heading"             : "uuids_object_"      , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

NamesUuidGroup        =                      { \
"heading"             : "uuids_names_"       , \
"start"               :  1                   , \
"total"               :  4                   , \
"fill"                :  4                     \
}

PhysicsUuidGroup      =                      { \
"heading"             : "uuids_physics_"     , \
"start"               :  1                   , \
"total"               :  4                   , \
"fill"                :  4                     \
}

HumanUuidGroup        =                      { \
"heading"             : "uuids_human_"       , \
"start"               :  1                   , \
"total"               :  4                   , \
"fill"                :  4                     \
}

FilesUuidGroup        =                      { \
"heading"             : "uuids_files_"       , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

PlainUuidGroup        =                      { \
"heading"             : "uuids_plain_"       , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

XmlUuidGroup          =                      { \
"heading"             : "uuids_xml_"         , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

DescriptionUuidGroup  =                      { \
"heading"             : "uuids_description_" , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

DecisionsUuidGroup    =                      { \
"heading"             : "uuids_decisions_"   , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

SocietyUuidGroup      =                      { \
"heading"             : "uuids_society_"     , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

PeopleUuidGroup       =                      { \
"heading"             : "uuids_people_"      , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

PictureUuidGroup      =                      { \
"heading"             : "uuids_picture_"     , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

VideosUuidGroup       =                      { \
"heading"             : "uuids_videos_"      , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

AudiosUuidGroup       =                      { \
"heading"             : "uuids_audios_"      , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

UsernameUuidGroup     =                      { \
"heading"             : "uuids_username_"    , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

HistoryUuidGroup      =                      { \
"heading"             : "uuids_history_"     , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

ResourceUuidGroup     =                      { \
"heading"             : "uuids_resource_"    , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

TasksUuidGroup        =                      { \
"heading"             : "uuids_tasks_"       , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

StarsUuidGroup        =                      { \
"heading"             : "uuids_stars_"       , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

NetworkUuidGroup      =                      { \
"heading"             : "uuids_network_"     , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

DomainsUuidGroup      =                      { \
"heading"             : "uuids_domains_"     , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

UrlsUuidGroup         =                      { \
"heading"             : "uuids_urls_"        , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

IpUuidGroup           =                      { \
"heading"             : "uuids_ip_"          , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

PhonesUuidGroup       =                      { \
"heading"             : "uuids_phones_"      , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

EmailsUuidGroup       =                      { \
"heading"             : "uuids_emails_"      , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

ImsUuidGroup          =                      { \
"heading"             : "uuids_ims_"         , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

CoursesUuidGroup      =                      { \
"heading"             : "uuids_courses_"     , \
"start"               :  1                   , \
"total"               :  4                   , \
"fill"                :  4                     \
}

ClassesUuidGroup      =                      { \
"heading"             : "uuids_classes_"     , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

LecturesUuidGroup     =                      { \
"heading"             : "uuids_lectures_"    , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

TradesUuidGroup       =                      { \
"heading"             : "uuids_trades_"      , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

TokensUuidGroup       =                      { \
"heading"             : "uuids_tokens_"      , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

RemitsUuidGroup       =                      { \
"heading"             : "uuids_remits_"      , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

RealityUuidGroup      =                      { \
"heading"             : "uuids_reality_"     , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

ModelUuidGroup        =                      { \
"heading"             : "uuids_model_"       , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

ShapesUuidGroup       =                      { \
"heading"             : "uuids_shapes_"      , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

EconomicsUuidGroup    =                      { \
"heading"             : "uuids_economics_"   , \
"start"               :  1                   , \
"total"               :  4                   , \
"fill"                :  4                     \
}

SecuritiesUuidGroup   =                      { \
"heading"             : "uuids_securities_"  , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

MonetaryUuidGroup     =                      { \
"heading"             : "uuids_monetary_"    , \
"start"               :  1                   , \
"total"               :  4                   , \
"fill"                :  4                     \
}

CommodityUuidGroup    =                      { \
"heading"             : "uuids_commodity_"   , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

AccountsUuidGroup     =                      { \
"heading"             : "uuids_accounts_"    , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

SpotsUuidGroup        =                      { \
"heading"             : "uuids_spots_"       , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

MeaningsUuidGroup     =                      { \
"heading"             : "uuids_meanings_"    , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

DocumentsUuidGroup    =                      { \
"heading"             : "uuids_documents_"   , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

DivisionsUuidGroup    =                      { \
"heading"             : "uuids_divisions_"   , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

BiologyUuidGroup      =                      { \
"heading"             : "uuids_biology_"     , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

VariablesUuidGroup    =                      { \
"heading"             : "uuids_variables_"   , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

SqlUuidGroup          =                      { \
"heading"             : "uuids_sql_"         , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

ChemistryUuidGroup    =                      { \
"heading"             : "uuids_chemistry_"   , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

CodingUuidGroup       =                      { \
"heading"             : "uuids_coding_"      , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

ClfUuidGroup          =                      { \
"heading"             : "uuids_clf_"         , \
"start"               :  1                   , \
"total"               :  4                   , \
"fill"                :  4                     \
}

LinguisticsUuidGroup  =                      { \
"heading"             : "uuids_linguistics_" , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

MathUuidGroup         =                      { \
"heading"             : "uuids_math_"        , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

DataUuidGroup         =                      { \
"heading"             : "uuids_data_"        , \
"start"               :  1                   , \
"total"               : 40                   , \
"fill"                :  4                     \
}

OthersUuidGroup       =                      { \
"heading"             : "uuids_others_"      , \
"start"               :  1                   , \
"total"               : 20                   , \
"fill"                :  4                     \
}

AllUuidsMaps          =                       { \
  "uuids_object"      : ObjectUuidGroup       , \
  "uuids_names"       : NamesUuidGroup        , \
  "uuids_physics"     : PhysicsUuidGroup      , \
  "uuids_human"       : HumanUuidGroup        , \
  "uuids_files"       : FilesUuidGroup        , \
  "uuids_plain"       : PlainUuidGroup        , \
  "uuids_xml"         : XmlUuidGroup          , \
  "uuids_description" : DescriptionUuidGroup  , \
  "uuids_decisions"   : DecisionsUuidGroup    , \
  "uuids_society"     : SocietyUuidGroup      , \
  "uuids_people"      : PeopleUuidGroup       , \
  "uuids_picture"     : PictureUuidGroup      , \
  "uuids_videos"      : VideosUuidGroup       , \
  "uuids_audios"      : AudiosUuidGroup       , \
  "uuids_username"    : UsernameUuidGroup     , \
  "uuids_history"     : HistoryUuidGroup      , \
  "uuids_resource"    : ResourceUuidGroup     , \
  "uuids_tasks"       : TasksUuidGroup        , \
  "uuids_stars"       : StarsUuidGroup        , \
  "uuids_network"     : NetworkUuidGroup      , \
  "uuids_domains"     : DomainsUuidGroup      , \
  "uuids_urls"        : UrlsUuidGroup         , \
  "uuids_ip"          : IpUuidGroup           , \
  "uuids_phones"      : PhonesUuidGroup       , \
  "uuids_emails"      : EmailsUuidGroup       , \
  "uuids_ims"         : ImsUuidGroup          , \
  "uuids_courses"     : CoursesUuidGroup      , \
  "uuids_classes"     : ClassesUuidGroup      , \
  "uuids_lectures"    : LecturesUuidGroup     , \
  "uuids_trades"      : TradesUuidGroup       , \
  "uuids_tokens"      : TokensUuidGroup       , \
  "uuids_remits"      : RemitsUuidGroup       , \
  "uuids_reality"     : RealityUuidGroup      , \
  "uuids_model"       : ModelUuidGroup        , \
  "uuids_shapes"      : ShapesUuidGroup       , \
  "uuids_economics"   : EconomicsUuidGroup    , \
  "uuids_securities"  : SecuritiesUuidGroup   , \
  "uuids_monetary"    : MonetaryUuidGroup     , \
  "uuids_commodity"   : CommodityUuidGroup    , \
  "uuids_accounts"    : AccountsUuidGroup     , \
  "uuids_spots"       : SpotsUuidGroup        , \
  "uuids_meanings"    : MeaningsUuidGroup     , \
  "uuids_documents"   : DocumentsUuidGroup    , \
  "uuids_divisions"   : DivisionsUuidGroup    , \
  "uuids_biology"     : BiologyUuidGroup      , \
  "uuids_variables"   : VariablesUuidGroup    , \
  "uuids_sql"         : SqlUuidGroup          , \
  "uuids_chemistry"   : ChemistryUuidGroup    , \
  "uuids_coding"      : CodingUuidGroup       , \
  "uuids_clf"         : ClfUuidGroup          , \
  "uuids_linguistics" : LinguisticsUuidGroup  , \
  "uuids_math"        : MathUuidGroup         , \
  "uuids_data"        : DataUuidGroup         , \
  "uuids_others"      : OthersUuidGroup         \
}

UuidTablesStructure =                       { \
  "Template"        : UuidTable             , \
  "All"             : AllUuidsMaps          , \
  "Major"           : "uuids"               , \
  "Master"          : Databases [ "ERP"   ] , \
  "Depot"           : Databases [ "UUIDs" ] , \
  "Engine"          : TemplateMyISAM        , \
  "Merger"          : TemplateMerge         , \
  "Starting"        : 1000000000000000001   , \
  "Gaps"            :           100000000     \
}

# Names Table
NamesTable = \
"""create table $(Table) (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `locality` integer not null,
  `priority` integer default 0,
  `relevance` integer default 0,
  `flags` bigint default 0,
  `length` integer default 0,
  `name` blob default null,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uniquenames` (`uuid`,`locality`,`priority`,`relevance`),
  key `namesuuid` (`uuid`),
  key `nameslocality` (`locality`),
  key `namespriority` (`priority`),
  key `namesrelevance` (`relevance`),
  key `namesflags` (`flags`),
  key `nameslength` (`length`),
  key `namesname` (`name`(512)) ,
  key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

CommonsNamesGroup   =                  { \
"heading"           : "names_commons_" , \
"start"             :  1               , \
"total"             : 40               , \
"fill"              :  4                 \
}

LanguagesNamesGroup =                    { \
"heading"           : "names_languages_" , \
"start"             :  1                 , \
"total"             :  4                 , \
"fill"              :  4                   \
}

PeopleNamesGroup    =                 { \
"heading"           : "names_people_" , \
"start"             :  1              , \
"total"             : 10              , \
"fill"              :  4                \
}

PlacesNamesGroup    =                 { \
"heading"           : "names_places_" , \
"start"             :  1              , \
"total"             :  4              , \
"fill"              :  4                \
}

TimeZonesNamesGroup =                    { \
"heading"           : "names_timezones_" , \
"start"             :  1                 , \
"total"             :  4                 , \
"fill"              :  4                   \
}

StarsNamesGroup     =                { \
"heading"           : "names_stars_" , \
"start"             :  1             , \
"total"             :  4             , \
"fill"              :  4               \
}

OthersNamesGroup    =                 { \
"heading"           : "names_others_" , \
"start"             :  1              , \
"total"             : 20              , \
"fill"              :  4                \
}

AllNamesMaps        =                     { \
  "names_commons"   : CommonsNamesGroup   , \
  "names_languages" : LanguagesNamesGroup , \
  "names_people"    : PeopleNamesGroup    , \
  "names_places"    : PlacesNamesGroup    , \
  "names_timezones" : TimeZonesNamesGroup , \
  "names_stars"     : StarsNamesGroup     , \
  "names_others"    : OthersNamesGroup      \
}

NamesTablesStructure =                       { \
  "Template"         : NamesTable            , \
  "All"              : AllNamesMaps          , \
  "Major"            : "names"               , \
  "Master"           : Databases [ "ERP"   ] , \
  "Depot"            : Databases [ "Names" ] , \
  "Engine"           : TemplateMyISAM        , \
  "Merger"           : TemplateMerge         , \
  "Starting"         : 1000000000000000001   , \
  "Gaps"             :           100000000     \
}

# Relations Table
RelationsTable = \
"""create table $(Table) (
  `id` bigint not null auto_increment primary key,
  `first` bigint not null,
  `t1` integer not null,
  `second` bigint not null,
  `t2` integer not null,
  `relation` integer not null,
  `position` integer default 0,
  `reverse` integer default 0,
  `prefer` integer default 0,
  `membership` double default 1,
  `description` bigint default 0,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uniquerelations` (`first`,`t1`,`second`,`t2`,`relation`),
  key `relationsfirstt1` (`first`,`t1`),
  key `relationssecondt2` (`second`,`t2`),
  key `relationsfirst` (`first`),
  key `relationst1` (`t1`),
  key `relationssecond` (`second`),
  key `relationst2` (`t2`),
  key `relationsrelation` (`relation`),
  key `relationsposition` (`position`),
  key `relationsreverse` (`reverse`),
  key `relationsprefer` (`prefer`),
  key `relationsmembership` (`membership`),
  key `relationsdescription` (`description`),
  key `relationsltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

CommonsRelationsGroup  =                      { \
"heading"              : "relations_commons_" , \
"start"                :  1                   , \
"total"                : 20                   , \
"fill"                 :  4                     \
}

PeopleRelationsGroup   =                     { \
"heading"              : "relations_people_" , \
"start"                :  1                  , \
"total"                : 20                  , \
"fill"                 :  4                    \
}

CoursesRelationsGroup  =                      { \
"heading"              : "relations_courses_" , \
"start"                :  1                   , \
"total"                : 10                   , \
"fill"                 :  4                     \
}

TokensRelationsGroup   =                     { \
"heading"              : "relations_tokens_" , \
"start"                :  1                  , \
"total"                : 10                  , \
"fill"                 :  4                    \
}

TradesRelationsGroup   =                     { \
"heading"              : "relations_trades_" , \
"start"                :  1                  , \
"total"                : 10                  , \
"fill"                 :  4                    \
}

PicturesRelationsGroup =                       { \
"heading"              : "relations_pictures_" , \
"start"                :  1                    , \
"total"                : 20                    , \
"fill"                 :  4                      \
}

AudiosRelationsGroup   =                     { \
"heading"              : "relations_audios_" , \
"start"                :  1                  , \
"total"                : 10                  , \
"fill"                 :  4                    \
}

VideosRelationsGroup   =                     { \
"heading"              : "relations_videos_" , \
"start"                :  1                  , \
"total"                : 10                  , \
"fill"                 :  4                    \
}

PlacesRelationsGroup   =                     { \
"heading"              : "relations_places_" , \
"start"                :  1                  , \
"total"                : 20                  , \
"fill"                 :  4                    \
}

StarsRelationsGroup    =                    { \
"heading"              : "relations_stars_" , \
"start"                :  1                 , \
"total"                : 20                 , \
"fill"                 :  4                   \
}

OthersRelationsGroup   =                     { \
"heading"              : "relations_others_" , \
"start"                :  1                  , \
"total"                : 20                  , \
"fill"                 :  4                    \
}

AllRelationsMaps       =                        { \
  "relations_commons"  : CommonsRelationsGroup  , \
  "relations_people"   : PeopleRelationsGroup   , \
  "relations_courses"  : CoursesRelationsGroup  , \
  "relations_tokens"   : TokensRelationsGroup   , \
  "relations_trades"   : TradesRelationsGroup   , \
  "relations_pictures" : PicturesRelationsGroup , \
  "relations_audios"   : AudiosRelationsGroup   , \
  "relations_videos"   : VideosRelationsGroup   , \
  "relations_places"   : PlacesRelationsGroup   , \
  "relations_stars"    : StarsRelationsGroup    , \
  "relations_others"   : OthersRelationsGroup     \
}

RelationsTablesStructure =                           { \
  "Template"             : RelationsTable            , \
  "All"                  : AllRelationsMaps          , \
  "Major"                : "relations"               , \
  "Master"               : Databases [ "ERP"       ] , \
  "Depot"                : Databases [ "Relations" ] , \
  "Engine"               : TemplateMyISAM            , \
  "Merger"               : TemplateMerge             , \
  "Starting"             : 1000000000000000001       , \
  "Gaps"                 :           100000000         \
}

# Picture Information Table
PictureTable = \
"""create table $(Table) (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `mimeid` bigint default 0,
  `suffix` tinyblob default null,
  `filesize` bigint default 0,
  `checksum` bigint default 0,
  `width` integer default 0,
  `height` integer default 0,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uuid` (`uuid`),
  key `mimeid` (`mimeid`),
  key `suffix` (`suffix`(32)),
  key `filesize` (`filesize`),
  key `checksum` (`checksum`),
  key `width` (`width`),
  key `height` (`height`),
  key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

IconPictureGroup      =                  { \
"heading"             : "pictures_icon_" , \
"start"               :  1               , \
"total"               : 10               , \
"fill"                :  4                 \
}

TexturesPictureGroup  =                      { \
"heading"             : "pictures_textures_" , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

CoverPictureGroup     =                   { \
"heading"             : "pictures_cover_" , \
"start"               :  1                , \
"total"               : 10                , \
"fill"                :  4                  \
}

FacesPictureGroup     =                   { \
"heading"             : "pictures_faces_" , \
"start"               :  1                , \
"total"               : 10                , \
"fill"                :  4                  \
}

PeoplePictureGroup    =                    { \
"heading"             : "pictures_people_" , \
"start"               :  1                 , \
"total"               : 20                 , \
"fill"                :  4                   \
}

AvPictureGroup        =                { \
"heading"             : "pictures_av_" , \
"start"               :  1             , \
"total"               : 40             , \
"fill"                :  4               \
}

OthersPictureGroup    =                    { \
"heading"             : "pictures_others_" , \
"start"               :  1                 , \
"total"               : 40                 , \
"fill"                :  4                   \
}

AllPictureMaps        =                      { \
  "pictures_icon"     : IconPictureGroup     , \
  "pictures_textures" : TexturesPictureGroup , \
  "pictures_covers"   : CoverPictureGroup    , \
  "pictures_faces"    : FacesPictureGroup    , \
  "pictures_people"   : PeoplePictureGroup   , \
  "pictures_av"       : AvPictureGroup       , \
  "pictures_others"   : OthersPictureGroup     \
}

PictureTablesStructure =                       { \
  "Template"        : PictureTable             , \
  "All"             : AllPictureMaps           , \
  "Major"           : "pictures"               , \
  "Master"          : Databases [ "ERP"      ] , \
  "Depot"           : Databases [ "Pictures" ] , \
  "Engine"          : TemplateMyISAM           , \
  "Merger"          : TemplateMerge            , \
  "Starting"        : 1000000000000000001      , \
  "Gaps"            :           100000000        \
}

# Picture Depot Table
PictureDepotTable = \
"""create table $(Table) (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `file` longblob not null,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uuid` (`uuid`),
  key `ltime` (`ltime`),
  key `file` (`file`(768))
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

IconPictureDepotGroup   =               { \
"heading"               : "depot_icon_" , \
"start"                 :  1            , \
"total"                 : 10            , \
"fill"                  :  4              \
}

CoverPictureDepotGroup  =                { \
"heading"               : "depot_cover_" , \
"start"                 :  1             , \
"total"                 : 10             , \
"fill"                  :  4               \
}

FacesPictureDepotGroup  =                { \
"heading"               : "depot_faces_" , \
"start"                 :  1             , \
"total"                 : 10             , \
"fill"                  :  4               \
}

PeoplePictureDepotGroup =                 { \
"heading"               : "depot_people_" , \
"start"                 :  1              , \
"total"                 : 20              , \
"fill"                  :  4                \
}

AvPictureDepotGroup     =             { \
"heading"               : "depot_av_" , \
"start"                 :  1          , \
"total"                 : 40          , \
"fill"                  :  4            \
}

OthersPictureDepotGroup =                 { \
"heading"               : "depot_others_" , \
"start"                 :  1              , \
"total"                 : 40              , \
"fill"                  :  4                \
}

AllPictureDepotMaps       =                         { \
  "pictures_depot_icon"   : IconPictureDepotGroup   , \
  "pictures_depot_covers" : CoverPictureDepotGroup  , \
  "pictures_depot_faces"  : FacesPictureDepotGroup  , \
  "pictures_depot_people" : PeoplePictureDepotGroup , \
  "pictures_depot_av"     : AvPictureDepotGroup     , \
  "pictures_depot_others" : OthersPictureDepotGroup   \
}

PictureDepotTablesStructure =                  { \
  "Template"        : PictureDepotTable        , \
  "All"             : AllPictureDepotMaps      , \
  "Major"           : "picturedepot"           , \
  "Master"          : Databases [ "ERP"      ] , \
  "Depot"           : Databases [ "Pictures" ] , \
  "Engine"          : TemplateMyISAM           , \
  "Merger"          : TemplateMerge            , \
  "Starting"        : 1000000000000000001      , \
  "Gaps"            :           100000000        \
}

# Picture Order Table
PictureOrderTable = \
"""create table $(Table) (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `position` bigint default -1,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uuid` (`uuid`),
  key `position` (`position`),
  key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

# Thumb Information Table
ThumbTable = \
"""create table $(Table) (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `filesize` bigint default 0,
  `iconsize` bigint default 0,
  `format` tinyblob default null,
  `width` integer default 0,
  `height` integer default 0,
  `iconwidth` integer default 0,
  `iconheight` integer default 0,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uuid` (`uuid`),
  key `filesize` (`filesize`),
  key `iconsize` (`iconsize`),
  key `format` (`format`(16)),
  key `width` (`width`),
  key `height` (`height`),
  key `iconwidth` (`iconwidth`),
  key `iconheight` (`iconheight`),
  key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

IconThumbGroup        =                { \
"heading"             : "thumbs_icon_" , \
"start"               :  1             , \
"total"               : 10             , \
"fill"                :  4               \
}

CoverThumbGroup       =                 { \
"heading"             : "thumbs_cover_" , \
"start"               :  1              , \
"total"               : 10              , \
"fill"                :  4                \
}

FacesThumbGroup       =                 { \
"heading"             : "thumbs_faces_" , \
"start"               :  1              , \
"total"               : 10              , \
"fill"                :  4                \
}

PeopleThumbGroup      =                  { \
"heading"             : "thumbs_people_" , \
"start"               :  1               , \
"total"               : 20               , \
"fill"                :  4                 \
}

AvThumbGroup          =              { \
"heading"             : "thumbs_av_" , \
"start"               :  1           , \
"total"               : 40           , \
"fill"                :  4             \
}

OthersThumbGroup      =                  { \
"heading"             : "thumbs_others_" , \
"start"               :  1               , \
"total"               : 40               , \
"fill"                :  4                 \
}

AllThumbMaps        =                  { \
  "thumbs_icon"     : IconThumbGroup   , \
  "thumbs_covers"   : CoverThumbGroup  , \
  "thumbs_faces"    : FacesThumbGroup  , \
  "thumbs_people"   : PeopleThumbGroup , \
  "thumbs_av"       : AvThumbGroup     , \
  "thumbs_others"   : OthersThumbGroup   \
}

ThumbTablesStructure =                          { \
  "Template"         : ThumbTable               , \
  "All"              : AllThumbMaps             , \
  "Major"            : "thumbs"                 , \
  "Master"           : Databases [ "ERP"      ] , \
  "Depot"            : Databases [ "Pictures" ] , \
  "Engine"           : TemplateMyISAM           , \
  "Merger"           : TemplateMerge            , \
  "Starting"         : 1000000000000000001      , \
  "Gaps"             :           100000000        \
}

# Thumb Depot Table
ThumbDepotTable = \
"""create table $(Table) (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `thumb` longblob not null,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `uuid` (`uuid`),
  key `ltime` (`ltime`),
  key `thumb` (`thumb`(512))
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

IconThumbDepotGroup   =                      { \
"heading"             : "thumbs_depot_icon_" , \
"start"               :  1                   , \
"total"               : 10                   , \
"fill"                :  4                     \
}

CoverThumbDepotGroup  =                       { \
"heading"             : "thumbs_depot_cover_" , \
"start"               :  1                    , \
"total"               : 10                    , \
"fill"                :  4                      \
}

FacesThumbDepotGroup  =                       { \
"heading"             : "thumbs_depot_faces_" , \
"start"               :  1                    , \
"total"               : 10                    , \
"fill"                :  4                      \
}

PeopleThumbDepotGroup =                        { \
"heading"             : "thumbs_depot_people_" , \
"start"               :  1                     , \
"total"               : 20                     , \
"fill"                :  4                       \
}

AvThumbDepotGroup     =                    { \
"heading"             : "thumbs_depot_av_" , \
"start"               :  1                 , \
"total"               : 40                 , \
"fill"                :  4                   \
}

OthersThumbDepotGroup =                        { \
"heading"             : "thumbs_depot_others_" , \
"start"               :  1                     , \
"total"               : 40                     , \
"fill"                :  4                       \
}

AllThumbDepotMaps       =                       { \
  "thumbs_depot_icon"   : IconThumbDepotGroup   , \
  "thumbs_depot_covers" : CoverThumbDepotGroup  , \
  "thumbs_depot_faces"  : FacesThumbDepotGroup  , \
  "thumbs_depot_people" : PeopleThumbDepotGroup , \
  "thumbs_depot_av"     : AvThumbDepotGroup     , \
  "thumbs_depot_others" : OthersThumbDepotGroup   \
}

ThumbDepotTablesStructure =                    { \
  "Template"        : ThumbDepotTable          , \
  "All"             : AllThumbDepotMaps        , \
  "Major"           : "thumbdepot"             , \
  "Master"          : Databases [ "ERP"      ] , \
  "Depot"           : Databases [ "Pictures" ] , \
  "Engine"          : TemplateMyISAM           , \
  "Merger"          : TemplateMerge            , \
  "Starting"        : 1000000000000000001      , \
  "Gaps"            :           100000000        \
}

# People Table
MainPeopleTable = \
"""create table $(Table) (
  `id` bigint not null auto_increment primary key,
  `uuid` bigint not null,
  `used` integer default 0,
  `state` bigint default 0,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp(),
  unique `peopleuuid` (`uuid`),
  key `peopleused` (`used`),
  key `peoplestate` (`state`),
  key `peopleltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

MembersPeopleGroup   =                    { \
"heading"            : "people_members_"  , \
"start"              :  1                 , \
"total"              : 50                 , \
"fill"               :  4                   \
}

ManagersPeopleGroup  =                    { \
"heading"            : "people_managers_" , \
"start"              :  1                 , \
"total"              : 10                 , \
"fill"               :  4                   \
}

WorksPeopleGroup     =                 { \
"heading"            : "people_works_" , \
"start"              :  1              , \
"total"              : 10              , \
"fill"               :  4                \
}

CelebrityPeopleGroup =                     { \
"heading"            : "people_celebrity_" , \
"start"              :  1                  , \
"total"              : 10                  , \
"fill"               :  4                    \
}

AvPeopleGroup        =              { \
"heading"            : "people_av_" , \
"start"              :  1           , \
"total"              : 10           , \
"fill"               :  4             \
}

OthersPeopleGroup    =                  { \
"heading"            : "people_others_" , \
"start"              :  1               , \
"total"              : 20               , \
"fill"               :  4                 \
}

AllPeopleMaps        =                      { \
  "people_members"   : MembersPeopleGroup   , \
  "people_managers"  : ManagersPeopleGroup  , \
  "people_works"     : WorksPeopleGroup     , \
  "people_celebrity" : CelebrityPeopleGroup , \
  "people_av"        : AvPeopleGroup        , \
  "people_others"    : OthersPeopleGroup      \
}

PeopleTablesStructure =                        { \
  "Template"          : MainPeopleTable        , \
  "All"               : AllPeopleMaps          , \
  "Major"             : "people"               , \
  "Master"            : Databases [ "ERP"    ] , \
  "Depot"             : Databases [ "People" ] , \
  "Engine"            : TemplateMyISAM         , \
  "Merger"            : TemplateMerge          , \
  "Starting"          : 1000000000000000001    , \
  "Gaps"              :           100000000      \
}

# Time Zone Table
TimeZoneTable = \
"""create table $(Table) (
  `id` integer not null auto_increment primary key ,
  `uuid` bigint not null ,
  `zonename` tinyblob default null ,
  `ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
  unique `uuid` (`uuid`) ,
  key `zonename` (`zonename`(255)) ,
  key `ltime` (`ltime`)
) Engine = $(Engine) auto_increment=$(Index) default charset = utf8mb4 $(Options)"""

# Task table
TaskTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`used` integer default 1 ,
`type` integer default 0 ,
`states` bigint default 0 ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `used` (`used`) ,
key `type` (`type`) ,
key `states` (`states`) ,
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

RealityTaskGroup      =                     { \
"heading"             : "tasks_reality_"    , \
"start"               :  1                  , \
"total"               : 10                  , \
"fill"                :  4                    \
}

TemplateTaskGroup     =                     { \
"heading"             : "tasks_template_"   , \
"start"               :  1                  , \
"total"               : 10                  , \
"fill"                :  4                    \
}

PublicTaskGroup       =                     { \
"heading"             : "tasks_public_"     , \
"start"               :  1                  , \
"total"               : 10                  , \
"fill"                :  4                    \
}

PrivateTaskGroup      =                     { \
"heading"             : "tasks_private_"    , \
"start"               :  1                  , \
"total"               : 10                  , \
"fill"                :  4                    \
}

AllTasksMaps        =                       { \
  "tasks_reality"   : RealityTaskGroup      , \
  "tasks_template"  : TemplateTaskGroup     , \
  "tasks_public"    : PublicTaskGroup       , \
  "tasks_private"   : PrivateTaskGroup        \
}

TaskTablesStructure =                       { \
  "Template"        : TaskTable             , \
  "All"             : AllTasksMaps          , \
  "Major"           : "tasks"               , \
  "Master"          : Databases [ "ERP"   ] , \
  "Depot"           : Databases [ "Tasks" ] , \
  "Engine"          : TemplateMyISAM        , \
  "Merger"          : TemplateMerge         , \
  "Starting"        : 1000000000000000001   , \
  "Gaps"            :           100000000     \
}

# VPathes table
VPathesTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`used` integer default 1 ,
`path` blob default '' ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `used` (`used`),
key `path` (`path`(256)),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

PrimaryVPathesGroup   =                         { \
"heading"             : "vpathes_primary_"      , \
"start"               :  1                      , \
"total"               : 10                      , \
"fill"                :  4                        \
}

ImporterVPathesGroup  =                         { \
"heading"             : "vpathes_importer_"     , \
"start"               :  1                      , \
"total"               : 10                      , \
"fill"                :  4                        \
}

AllVPathesMaps         =                        { \
  "vpathes_primary"    : PrimaryVPathesGroup    , \
  "vpathes_importer"   : ImporterVPathesGroup     \
}

VPathesTablesStructure =                        { \
  "Template"           : VPathesTable           , \
  "All"                : AllVPathesMaps         , \
  "Major"              : "vpathes"              , \
  "Master"             : Databases [ "ERP"    ] , \
  "Depot"              : Databases [ "Videos" ] , \
  "Engine"             : TemplateMyISAM         , \
  "Merger"             : TemplateMerge          , \
  "Starting"           : 1000000000000000001    , \
  "Gaps"               :           100000000      \
}

# Time Slots table
TimeSlotsTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`acting` bigint not null ,
`start` integer default 0 ,
`end` integer default 0 ,
`states` bigint default 0 ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
key `uuid` (`uuid`) ,
key `acting` (`acting`),
key `start` (`start`),
key `end` (`end`),
key `states` (`states`),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

OutdateTimeSlotsGroup    =                           { \
"heading"                : "timeslots_outdate_"      , \
"start"                  :  1                        , \
"total"                  : 10                        , \
"fill"                   :  4                          \
}

PrimaryTimeSlotsGroup    =                           { \
"heading"                : "timeslots_primary_"      , \
"start"                  :  1                        , \
"total"                  : 10                        , \
"fill"                   :  4                          \
}

ImporterTimeSlotsGroup   =                           { \
"heading"                : "timeslots_importer_"     , \
"start"                  :  1                        , \
"total"                  : 10                        , \
"fill"                   :  4                          \
}

AllTimeSlotsMaps         =                           { \
  "timeslots_outdate"    : OutdateTimeSlotsGroup     , \
  "timeslots_primary"    : PrimaryTimeSlotsGroup     , \
  "timeslots_importer"   : ImporterTimeSlotsGroup      \
}

TimeSlotsTablesStructure =                           { \
  "Template"             : TimeSlotsTable            , \
  "All"                  : AllTimeSlotsMaps          , \
  "Major"                : "timeslots"               , \
  "Master"               : Databases [ "ERP"       ] , \
  "Depot"                : Databases [ "Schedules" ] , \
  "Engine"               : TemplateMyISAM            , \
  "Merger"               : TemplateMerge             , \
  "Starting"             : 1000000000000000001       , \
  "Gaps"                 :           100000000         \
}

# Periods table
PeriodsTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`type` integer default 0 ,
`used` integer default 0 ,
`start` bigint default 0 ,
`end` bigint default 0 ,
`states` bigint default 0 ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `type` (`type`),
key `used` (`used`),
key `start` (`start`),
key `end` (`end`),
key `states` (`states`),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

OutdatePeriodsGroup      =                           { \
"heading"                : "periods_outdate_"        , \
"start"                  :  1                        , \
"total"                  : 10                        , \
"fill"                   :  4                          \
}

PrimaryPeriodsGroup      =                           { \
"heading"                : "periods_primary_"        , \
"start"                  :  1                        , \
"total"                  : 10                        , \
"fill"                   :  4                          \
}

ImporterPeriodsGroup     =                           { \
"heading"                : "periods_importer_"       , \
"start"                  :  1                        , \
"total"                  : 10                        , \
"fill"                   :  4                          \
}

AllPeriodsMaps           =                           { \
  "periods_outdate"      : OutdatePeriodsGroup       , \
  "periods_primary"      : PrimaryPeriodsGroup       , \
  "periods_importer"     : ImporterPeriodsGroup        \
}

PeriodsTablesStructure   =                           { \
  "Template"             : PeriodsTable              , \
  "All"                  : AllPeriodsMaps            , \
  "Major"                : "periods"                 , \
  "Master"               : Databases [ "ERP"       ] , \
  "Depot"                : Databases [ "Schedules" ] , \
  "Engine"               : TemplateMyISAM            , \
  "Merger"               : TemplateMerge             , \
  "Starting"             : 1000000000000000001       , \
  "Gaps"                 :           100000000         \
}

# Classes table
ClassesTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`type` integer default 0 ,
`used` integer default 0 ,
`states` bigint default 0 ,
`trainee` bigint default 0 ,
`tutor` bigint default 0 ,
`manager` bigint default 0 ,
`receptionist` bigint default 0 ,
`item` integer default 0 ,
`lecture` bigint default 0 ,
`description` bigint default 0 ,
`period` bigint default 0 ,
`start` bigint default 0 ,
`end` bigint default 0 ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `type` (`type`),
key `used` (`used`),
key `states` (`states`),
key `trainee` (`trainee`),
key `tutor` (`tutor`),
key `manager` (`manager`),
key `receptionist` (`receptionist`),
key `item` (`item`),
key `lecture` (`lecture`),
key `description` (`description`),
key `period` (`period`),
key `start` (`start`),
key `end` (`end`),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

OutdateClassesGroup    =                     { \
"heading"              : "classes_outdate_"  , \
"start"                :  1                  , \
"total"                : 20                  , \
"fill"                 :  4                    \
}

PrimaryClassesGroup    =                     { \
"heading"              : "classes_primary_"  , \
"start"                :  1                  , \
"total"                : 20                  , \
"fill"                 :  4                    \
}

ImporterClassesGroup   =                     { \
"heading"              : "classes_importer_" , \
"start"                :  1                  , \
"total"                : 10                  , \
"fill"                 :  4                    \
}

AllClassesMaps         =                           { \
  "classes_outdate"    : OutdateClassesGroup       , \
  "classes_primary"    : PrimaryClassesGroup       , \
  "classes_importer"   : ImporterClassesGroup        \
}

ClassesTablesStructure =                           { \
  "Template"           : ClassesTable              , \
  "All"                : AllClassesMaps            , \
  "Major"              : "classes"                 , \
  "Master"             : Databases [ "ERP"       ] , \
  "Depot"              : Databases [ "Schedules" ] , \
  "Engine"             : TemplateMyISAM            , \
  "Merger"             : TemplateMerge             , \
  "Starting"           : 1000000000000000001       , \
  "Gaps"               :           100000000         \
}

# Secrets table
SecretsTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`name` tinyblob default '' ,
`secret` tinyblob default '' ,
`unlock` tinyblob default '' ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `name` (`name`(64)),
key `secret` (`secret`(64)),
key `unlock` (`unlock`(64)),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

PrimarySecretsGroup    =                           { \
"heading"              : "secrets_primary_"        , \
"start"                :  1                        , \
"total"                : 10                        , \
"fill"                 :  4                          \
}

ImporterSecretsGroup   =                           { \
"heading"              : "secrets_importer_"       , \
"start"                :  1                        , \
"total"                : 10                        , \
"fill"                 :  4                          \
}

AllSecretsMaps         =                           { \
  "secrets_primary"    : PrimarySecretsGroup       , \
  "secrets_importer"   : ImporterSecretsGroup        \
}

SecretsTablesStructure =                           { \
  "Template"           : SecretsTable              , \
  "All"                : AllSecretsMaps            , \
  "Major"              : "secrets"                 , \
  "Master"             : Databases [ "ERP"       ] , \
  "Depot"              : Databases [ "Cage"      ] , \
  "Engine"             : TemplateMyISAM            , \
  "Merger"             : TemplateMerge             , \
  "Starting"           : 1000000000000000001       , \
  "Gaps"               :           100000000         \
}

# Parameters table
ParametersTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`type` integer not null ,
`variety` integer default 0 ,
`scope` tinyblob default '' ,
`name` tinyblob default '' ,
`value` bigint default 0 ,
`floating` double default 0 ,
`data` longblob default null ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
key `uuid` (`uuid`) ,
key `type` (`type`),
key `variety` (`variety`),
key `uuidtype` (`uuid`,`type`),
key `uuidall` (`uuid`,`type`,`variety`),
key `scope` (`scope`(128)),
key `name` (`name`(128)),
key `value` (`value`),
key `floating` (`floating`),
key `data` (`data`(255)),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

CommonsParametersGroup    =                            { \
"heading"                 : "parameters_commons_"      , \
"start"                   :  1                         , \
"total"                   : 20                         , \
"fill"                    :  4                           \
}

PeopleParametersGroup     =                            { \
"heading"                 : "parameters_people_"       , \
"start"                   :  1                         , \
"total"                   : 50                         , \
"fill"                    :  4                           \
}

PrimaryParametersGroup    =                            { \
"heading"                 : "parameters_primary_"      , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

ImporterParametersGroup   =                            { \
"heading"                 : "parameters_importer_"     , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

AllParametersMaps         =                            { \
  "parameters_commons"    : CommonsParametersGroup     , \
  "parameters_people"     : PeopleParametersGroup      , \
  "parameters_primary"    : PrimaryParametersGroup     , \
  "parameters_importer"   : ImporterParametersGroup      \
}

ParametersTablesStructure =                            { \
  "Template"              : ParametersTable            , \
  "All"                   : AllParametersMaps          , \
  "Major"                 : "parameters"               , \
  "Master"                : Databases [ "ERP"        ] , \
  "Depot"                 : Databases [ "Parameters" ] , \
  "Engine"                : TemplateMyISAM             , \
  "Merger"                : TemplateMerge              , \
  "Starting"              : 1000000000000000001        , \
  "Gaps"                  :           100000000          \
}

# Variables table
VariablesTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`type` integer default 0 ,
`name` tinyblob default '' ,
`value` blob default '' ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `type` (`type`),
key `name` (`name`(64)),
key `value` (`value`(256)),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

PrimaryVariablesGroup     =                            { \
"heading"                 : "variables_primary_"       , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

ImporterVariablesGroup    =                            { \
"heading"                 : "variables_importer_"      , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

AllVariablesMaps          =                            { \
  "variables_primary"     : PrimaryVariablesGroup      , \
  "variables_importer"    : ImporterVariablesGroup       \
}

VariablesTablesStructure =                             { \
  "Template"              : VariablesTable             , \
  "All"                   : AllVariablesMaps           , \
  "Major"                 : "variables"                , \
  "Master"                : Databases [ "ERP"        ] , \
  "Depot"                 : Databases [ "Parameters" ] , \
  "Engine"                : TemplateMyISAM             , \
  "Merger"                : TemplateMerge              , \
  "Starting"              : 1000000000000000001        , \
  "Gaps"                  :           100000000          \
}

# Notes table
NotesTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`name` tinyblob default '' ,
`prefer` integer default 0 ,
`note` longblob default '' ,
`title` longblob default '' ,
`comment` longblob default '' ,
`extra` longblob default '' ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
key `uuid` (`uuid`) ,
key `name` (`name`(64)),
key `prefer` (`prefer`),
key `note` (`note`(512)),
key `title` (`title`(512)),
key `comment` (`comment`(512)),
key `extra` (`extra`(512)),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

AddressesNotesGroup       =                            { \
"heading"                 : "notes_addresses_"         , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

CommentsNotesGroup        =                            { \
"heading"                 : "notes_comments_"          , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

ContractsNotesGroup       =                            { \
"heading"                 : "notes_contracts_"         , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

DescriptionsNotesGroup    =                            { \
"heading"                 : "notes_descriptions_"      , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

DocumentsNotesGroup       =                            { \
"heading"                 : "notes_documents_"         , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

FilmsNotesGroup           =                            { \
"heading"                 : "notes_films_"             , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

VideosNotesGroup          =                            { \
"heading"                 : "notes_videos_"            , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

MaterialsNotesGroup       =                            { \
"heading"                 : "notes_materials_"         , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

PreparationsNotesGroup    =                            { \
"heading"                 : "notes_preparations_"      , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

QuizletsNotesGroup        =                            { \
"heading"                 : "notes_quizlets_"          , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

RecordsNotesGroup         =                            { \
"heading"                 : "notes_records_"           , \
"start"                   :  1                         , \
"total"                   : 10                         , \
"fill"                    :  4                           \
}

TemplateNotesGroup        =                            { \
"heading"                 : "notes_template_"          , \
"start"                   :  1                         , \
"total"                   :  4                         , \
"fill"                    :  4                           \
}

VatNotesGroup             =                            { \
"heading"                 : "notes_vat_"               , \
"start"                   :  1                         , \
"total"                   :  4                         , \
"fill"                    :  4                           \
}

PrimaryNotesGroup         =                            { \
"heading"                 : "notes_primary_"           , \
"start"                   :  1                         , \
"total"                   :  4                         , \
"fill"                    :  4                           \
}

ImporterNotesGroup        =                            { \
"heading"                 : "notes_importer_"          , \
"start"                   :  1                         , \
"total"                   :  4                         , \
"fill"                    :  4                           \
}

AllNotesMaps              =                            { \
  "notes_addresses"       : AddressesNotesGroup        , \
  "notes_comments"        : CommentsNotesGroup         , \
  "notes_contracts"       : ContractsNotesGroup        , \
  "notes_descriptions"    : DescriptionsNotesGroup     , \
  "notes_documents"       : DocumentsNotesGroup        , \
  "notes_films"           : FilmsNotesGroup            , \
  "notes_videos"          : VideosNotesGroup           , \
  "notes_materials"       : MaterialsNotesGroup        , \
  "notes_preparations"    : PreparationsNotesGroup     , \
  "notes_quizlets"        : QuizletsNotesGroup         , \
  "notes_records"         : RecordsNotesGroup          , \
  "notes_template"        : TemplateNotesGroup         , \
  "notes_vat"             : VatNotesGroup              , \
  "notes_primary"         : PrimaryNotesGroup          , \
  "notes_importer"        : ImporterNotesGroup           \
}

NotesTablesStructure      =                            { \
  "Template"              : NotesTable                 , \
  "All"                   : AllNotesMaps               , \
  "Major"                 : "notes"                    , \
  "Master"                : Databases [ "ERP"        ] , \
  "Depot"                 : Databases [ "Notes"      ] , \
  "Engine"                : TemplateMyISAM             , \
  "Merger"                : TemplateMerge              , \
  "Starting"              : 1000000000000000001        , \
  "Gaps"                  :           100000000          \
}

# EMails table
EMailsTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`hostid` bigint default 0 ,
`account` blob default '' ,
`hostname` blob default '' ,
`email` blob default '' ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `emailshostid` (`hostid`),
key `emailsaccount` (`account`(64)),
key `emailshostname` (`hostname`(64)),
key `emailsemail` (`email`(128)),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

PrimaryEMailsGroup        =                            { \
"heading"                 : "emails_primary_"          , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

ImporterEMailsGroup       =                            { \
"heading"                 : "emails_importer_"         , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

AllEMailsMaps             =                            { \
  "emails_primary"        : PrimaryEMailsGroup         , \
  "emails_importer"       : ImporterEMailsGroup          \
}

EMailsTablesStructure     =                            { \
  "Template"              : EMailsTable                , \
  "All"                   : AllEMailsMaps              , \
  "Major"                 : "emails"                   , \
  "Master"                : Databases [ "ERP"        ] , \
  "Depot"                 : Databases [ "Networks"   ] , \
  "Engine"                : TemplateMyISAM             , \
  "Merger"                : TemplateMerge              , \
  "Starting"              : 1000000000000000001        , \
  "Gaps"                  :           100000000          \
}

# Instant Message table
ImsTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`used` integer default 0 ,
`imapp` integer default 0 ,
`account` blob default '' ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `used` (`used`),
key `imapp` (`imapp`),
key `account` (`account`(64)),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

PrimaryImsGroup           =                            { \
"heading"                 : "ims_primary_"             , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

ImporterImsGroup          =                            { \
"heading"                 : "ims_importer_"            , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

AllImsMaps                =                            { \
  "ims_primary"           : PrimaryImsGroup            , \
  "ims_importer"          : ImporterImsGroup             \
}

ImsTablesStructure        =                            { \
  "Template"              : ImsTable                   , \
  "All"                   : AllImsMaps                 , \
  "Major"                 : "instantmessage"           , \
  "Master"                : Databases [ "ERP"        ] , \
  "Depot"                 : Databases [ "Networks"   ] , \
  "Engine"                : TemplateMyISAM             , \
  "Merger"                : TemplateMerge              , \
  "Starting"              : 1000000000000000001        , \
  "Gaps"                  :           100000000          \
}

# Phones table
PhonesTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`used` integer default 0 ,
`country` char(8) default '' ,
`area` char(8) default '' ,
`number` char(64) default '' ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `uuid` (`uuid`) ,
key `used` (`used`),
key `country` (`country`),
key `area` (`area`),
key `number` (`number`),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

PrimaryPhonesGroup        =                            { \
"heading"                 : "phones_primary_"          , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

ImporterPhonesGroup       =                            { \
"heading"                 : "phones_importer_"         , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

AllPhonesMaps             =                            { \
  "phones_primary"        : PrimaryPhonesGroup         , \
  "phones_importer"       : ImporterPhonesGroup          \
}

PhonesTablesStructure     =                            { \
  "Template"              : PhonesTable                , \
  "All"                   : AllPhonesMaps              , \
  "Major"                 : "phones"                   , \
  "Master"                : Databases [ "ERP"        ] , \
  "Depot"                 : Databases [ "Telecom"    ] , \
  "Engine"                : TemplateMyISAM             , \
  "Merger"                : TemplateMerge              , \
  "Starting"              : 1000000000000000001        , \
  "Gaps"                  :           100000000          \
}

# Onlines table
OnlinesTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`wts` bigint default 0 ,
`start` bigint default 0 ,
`end` bigint default 0 ,
`attend` bigint default 0 ,
`complete` bigint default 0 ,
`flags` bigint default 0 ,
`json` longblob default '' ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
key `uuid` (`uuid`) ,
key `wts` (`wts`),
key `start` (`start`),
key `end` (`end`),
key `attend` (`attend`),
key `complete` (`complete`),
key `flags` (`flags`),
key `json` (`json`(768)),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

PrimaryOnlinesGroup       =                            { \
"heading"                 : "onlines_primary_"         , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

ImporterOnlinesGroup      =                            { \
"heading"                 : "onlines_importer_"        , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

AllOnlinesMaps            =                            { \
  "onlines_primary"       : PrimaryOnlinesGroup        , \
  "onlines_importer"      : ImporterOnlinesGroup         \
}

OnlinesTablesStructure    =                            { \
  "Template"              : OnlinesTable               , \
  "All"                   : AllOnlinesMaps             , \
  "Major"                 : "onlines"                  , \
  "Master"                : Databases [ "ERP"        ] , \
  "Depot"                 : Databases [ "History"    ] , \
  "Engine"                : TemplateMyISAM             , \
  "Merger"                : TemplateMerge              , \
  "Starting"              : 1000000000000000001        , \
  "Gaps"                  :           100000000          \
}

# Practices table
PracticesTable = \
"""create table $(Table) (
`id` bigint not null auto_increment primary key ,
`uuid` bigint not null ,
`english` blob not null ,
`inquery` integer default 1 ,
`ltime` timestamp not null default current_timestamp() on update current_timestamp() ,
unique key `englishuuid` (`uuid`,`english`(128)) ,
key `uuid` (`uuid`),
key `english` (`english`(128)),
key `inquery` (`inquery`),
key `ltime` (`ltime`)
) engine=$(Engine) auto_increment=$(Index) default charset=utf8mb4 $(Options)"""

PrimaryPracticesGroup     =                            { \
"heading"                 : "practices_primary_"       , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

ImporterPracticesGroup    =                            { \
"heading"                 : "practices_importer_"      , \
"start"                   :  1                         , \
"total"                   :  5                         , \
"fill"                    :  4                           \
}

AllPracticesMaps          =                            { \
  "practices_primary"     : PrimaryPracticesGroup      , \
  "practices_importer"    : ImporterPracticesGroup       \
}

PracticesTablesStructure  =                            { \
  "Template"              : PracticesTable             , \
  "All"                   : AllPracticesMaps           , \
  "Major"                 : "practices"                , \
  "Master"                : Databases [ "ERP"        ] , \
  "Depot"                 : Databases [ "History"    ] , \
  "Engine"                : TemplateMyISAM             , \
  "Merger"                : TemplateMerge              , \
  "Starting"              : 1000000000000000001        , \
  "Gaps"                  :           100000000          \
}

ActionsTableStructures        = [ \
  UuidTablesStructure         ,   \
  NamesTablesStructure        ,   \
  RelationsTablesStructure    ,   \
  PictureTablesStructure      ,   \
  PictureDepotTablesStructure ,   \
  ThumbTablesStructure        ,   \
  ThumbDepotTablesStructure   ,   \
  PeopleTablesStructure       ,   \
  TaskTablesStructure         ,   \
  VPathesTablesStructure      ,   \
  TimeSlotsTablesStructure    ,   \
  PeriodsTablesStructure      ,   \
  ClassesTablesStructure      ,   \
  SecretsTablesStructure      ,   \
  ParametersTablesStructure   ,   \
  VariablesTablesStructure    ,   \
  NotesTablesStructure        ,   \
  EMailsTablesStructure       ,   \
  ImsTablesStructure          ,   \
  PhonesTablesStructure       ,   \
  PracticesTablesStructure    ,   \
  OnlinesTablesStructure      ,   \
]
