SOURCES += $${PWD}/*.php
SOURCES += $${PWD}/*.js
SOURCES += $${PWD}/*.css
SOURCES += $${PWD}/*.html
SOURCES += $${PWD}/*.txt
SOURCES += $${PWD}/*.json
SOURCES += $${PWD}/*.py
SOURCES += $${PWD}/*.pl
SOURCES += $${PWD}/*.rb
SOURCES += $${PWD}/*.rs
SOURCES += $${PWD}/*.bat

include ($${PWD}/Essentials/Essentials.pri)
include ($${PWD}/Decisions/Decisions.pri)
include ($${PWD}/Calendars/Calendars.pri)
include ($${PWD}/Database/Database.pri)
include ($${PWD}/UUIDs/UUIDs.pri)
include ($${PWD}/Networking/Networking.pri)
include ($${PWD}/Documents/Documents.pri)
include ($${PWD}/Foundation/Foundation.pri)
include ($${PWD}/System/System.pri)
include ($${PWD}/Qt/Qt.pri)
