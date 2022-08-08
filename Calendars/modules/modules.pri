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

include ($${PWD}/Artificial/Artificial.pri)
include ($${PWD}/Astronomy/Astronomy.pri)
include ($${PWD}/Dynastic/Dynastic.pri)
include ($${PWD}/Eras/Eras.pri)
include ($${PWD}/Ethnic/Ethnic.pri)
include ($${PWD}/Foundational/Foundational.pri)
include ($${PWD}/Gregorian/Gregorian.pri)
include ($${PWD}/Radiometric/Radiometric.pri)
include ($${PWD}/Reform/Reform.pri)
include ($${PWD}/Religious/Religious.pri)
