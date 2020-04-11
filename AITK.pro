SOURCES += $${PWD}/*.php
SOURCES += $${PWD}/*.js
SOURCES += $${PWD}/*.css
SOURCES += $${PWD}/*.html
SOURCES += $${PWD}/*.txt
SOURCES += $${PWD}/*.bat
SOURCES += $${PWD}/*.json
SOURCES += $${PWD}/*.py
SOURCES += $${PWD}/*.pl
SOURCES += $${PWD}/*.rb
SOURCES += $${PWD}/*.rs
SOURCES += $${PWD}/*.md

include ($${PWD}/Bin/Bin.pri)
include ($${PWD}/Cpp/Cpp.pri)
include ($${PWD}/Python/Python.pri)
include ($${PWD}/Qt/Qt.pri)
include ($${PWD}/Ruby/Ruby.pri)
include ($${PWD}/SQL/SQL.pri)
include ($${PWD}/WWW/WWW.pri)
