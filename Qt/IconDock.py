# -*- coding: utf-8 -*-
##############################################################################
## IconDock
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
from   PyQt5                          import QtCore
from   PyQt5                          import QtGui
from   PyQt5                          import QtWidgets
##############################################################################
from   PyQt5 . QtCore                 import QObject
from   PyQt5 . QtCore                 import pyqtSignal
from   PyQt5 . QtCore                 import Qt
from   PyQt5 . QtCore                 import QPoint
from   PyQt5 . QtCore                 import QPointF
##############################################################################
from   PyQt5 . QtGui                  import QIcon
from   PyQt5 . QtGui                  import QCursor
from   PyQt5 . QtGui                  import QKeySequence
##############################################################################
from   PyQt5 . QtWidgets              import QApplication
from   PyQt5 . QtWidgets              import QWidget
from   PyQt5 . QtWidgets              import qApp
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QAction
from   PyQt5 . QtWidgets              import QShortcut
from   PyQt5 . QtWidgets              import QMenu
from   PyQt5 . QtWidgets              import QListWidget
from   PyQt5 . QtWidgets              import QListWidgetItem
from   PyQt5 . QtWidgets              import QTreeWidget
from   PyQt5 . QtWidgets              import QTreeWidgetItem
from   PyQt5 . QtWidgets              import QLineEdit
from   PyQt5 . QtWidgets              import QComboBox
from   PyQt5 . QtWidgets              import QSpinBox
##############################################################################
from         . ListDock               import ListDock as ListDock
##############################################################################
class IconDock           ( ListDock                                        ) :
  ############################################################################
  def __init__           ( self , parent = None , plan = None              ) :
    ##########################################################################
    super ( ) . __init__ ( parent , plan                                     )
    ##########################################################################
    return
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
  ############################################################################
##############################################################################


"""

class Q_COMPONENTS_EXPORT IconDock : public ListDock
{
  Q_OBJECT
  public:

    explicit IconDock      (StandardConstructor) ;
    virtual ~IconDock      (void);

  protected:

    virtual void Configure (void);

  private:

  public slots:

    virtual bool startup   (void);

  protected slots:

    virtual bool Menu      (QPoint pos) ;

  private slots:

  signals:

};

N::IconDock:: IconDock (QWidget * parent,Plan * p)
            : ListDock (          parent,       p)
{
  WidgetClass   ;
  Configure ( ) ;
}

N::IconDock::~IconDock (void)
{
}

void N::IconDock::Configure(void)
{
  setViewMode                  (IconMode             ) ;
  setIconSize                  (QSize(128,128)       ) ;
  setGridSize                  (QSize(140,192)       ) ;
  setDragDropMode              (DropOnly             ) ;
  setResizeMode                (QListView::Adjust    ) ;
  setWordWrap                  (true                 ) ;
  setHorizontalScrollBarPolicy (Qt::ScrollBarAsNeeded) ;
  setVerticalScrollBarPolicy   (Qt::ScrollBarAsNeeded) ;
  setMinimumSize               (QSize(144,200)       ) ;
}

bool N::IconDock::startup(void)
{
  if (IsNull(plan)) return false ;
  return true                    ;
}

bool N::IconDock::Menu(QPoint pos)
{ Q_UNUSED ( pos ) ;
  return false     ;
}

"""

