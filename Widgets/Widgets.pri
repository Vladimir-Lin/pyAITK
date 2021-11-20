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

include ($${PWD}/Biology/Biology.pri)
include ($${PWD}/Commons/Commons.pri)
include ($${PWD}/Networking/Networking.pri)
include ($${PWD}/Pictures/Pictures.pri)
include ($${PWD}/Scheduler/Scheduler.pri)
include ($${PWD}/Science/Science.pri)
include ($${PWD}/Society/Society.pri)
include ($${PWD}/Videos/Videos.pri)
include ($${PWD}/TBL/TBL.pri)
include ($${PWD}/Languages/Languages.pri)
