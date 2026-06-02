SOURCES += $${PWD}/*.php
SOURCES += $${PWD}/*.js
SOURCES += $${PWD}/*.css
SOURCES += $${PWD}/*.html
SOURCES += $${PWD}/*.txt
SOURCES += $${PWD}/*.json
SOURCES += $${PWD}/*.py
SOURCES += $${PWD}/*.pyw
SOURCES += $${PWD}/*.pl
SOURCES += $${PWD}/*.rb
SOURCES += $${PWD}/*.rs
SOURCES += $${PWD}/*.bat
SOURCES += $${PWD}/*.ui
SOURCES += $${PWD}/*.sql

include ($${PWD}/Widgets/Widgets.pri)
include ($${PWD}/Widgets6/Widgets6.pri)
include ($${PWD}/Player/Player.pri)
include ($${PWD}/Synopsis/Synopsis.pri)
include ($${PWD}/Sources/Sources.pri)
