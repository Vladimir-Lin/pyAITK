# -*- coding: utf-8 -*-
##############################################################################
import os
import sys
##############################################################################
from . Plan6 import Plan as Plan
##############################################################################
class ScriptPlan         ( Plan                                            ) :
  ############################################################################
  def __init__           ( self                                            ) :
    ##########################################################################
    super ( ) . __init__ (                                                   )
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__            ( self                                            ) :
    pass
##############################################################################

"""

class Q_COMPONENTS_EXPORT ScriptPlan : public QObject
                 , public QScriptable
                 , public Plan
{
  Q_OBJECT
  public:

    explicit     ScriptPlan  (QObject * parent = NULL) ;
    virtual     ~ScriptPlan  (void                   ) ;

    virtual int  type        (void) const { return Script ; }

    // Progress indicator
    virtual void StartBusy   (void) ;
    virtual void StopBusy    (void) ;

    virtual void showMessage (QString message) ;

  protected:

    QString statusMessage ;

  private:

  public slots:

    virtual void setObject   (QObject * parent) ;

  protected slots:

  private slots:

    void         AlertStart (void) ;
    void         AlertStop  (void) ;
    void         SendStatus (void) ;

  signals:

    void         EmitStart  (void) ;
    void         EmitStop   (void) ;
    void         EmitStatus (void) ;

};


#include <qtcomponents.h>

typedef struct       {
  N::ScriptPlan * pp ;
} ScriptPlanPacket   ;

N::ScriptPlan:: ScriptPlan  ( QObject * parent )
              : QObject     (           parent )
              , QScriptable (                  )
              , Plan        (                  )
{
  ScriptPlanPacket * pp = new ScriptPlanPacket ( ) ;
  pp -> pp  = this                                 ;
  Variables [ "ScriptPlan" ] = VoidVariant ( pp )  ;
  //////////////////////////////////////////////////
  ProgressReporter::setVirtual ( this )            ;
}

N::ScriptPlan::~ScriptPlan(void)
{
}

void N::ScriptPlan::setObject(QObject * parent)
{
  QObject::setParent ( parent                           ) ;
  QObject::connect   ( this , SIGNAL ( EmitStart  ( ) )   ,
                       this , SLOT   ( AlertStart ( ) ) ) ;
  QObject::connect   ( this , SIGNAL ( EmitStop   ( ) )   ,
                       this , SLOT   ( AlertStop  ( ) ) ) ;
  QObject::connect   ( this , SIGNAL ( EmitStatus ( ) )   ,
                       this , SLOT   ( SendStatus ( ) ) ) ;
}

void N::ScriptPlan::StartBusy(void)
{
  emit EmitStart ( ) ;
}

void N::ScriptPlan::StopBusy(void)
{
  emit EmitStop ( ) ;
}

void N::ScriptPlan::AlertStart(void)
{
  RealStart ( ) ;
}

void N::ScriptPlan::AlertStop(void)
{
  RealStop ( ) ;
}

void N::ScriptPlan::showMessage(QString message)
{
  if ( IsNull ( status ) ) return ;
  statusMessage = message         ;
  emit EmitStatus ( )             ;
}

void N::ScriptPlan::SendStatus(void)
{
  if ( IsNull ( status ) ) return         ;
  status -> showMessage ( statusMessage ) ;
}

"""
