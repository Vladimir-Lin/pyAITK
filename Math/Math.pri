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

include ($${PWD}/documents/documents.pri)
include ($${PWD}/Geometry/Geometry.pri)
include ($${PWD}/Numbers/Numbers.pri)
include ($${PWD}/Widgets/Widgets.pri)
