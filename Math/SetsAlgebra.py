# -*- coding: utf-8 -*-
##############################################################################
## SetsAlgebra
##############################################################################
class SetsAlgebra (                                                         ) :
  ############################################################################
  def __init__   ( self                                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    return
##############################################################################
"""
class Q_DISCRETE_EXPORT SetsAlgebra
{
  public:

    SUID                        Uuid          ;
    QString                     Identifier    ;
    QString                     Expression    ;
    QString                     Result        ;
    QStringList                 Inputs        ;
    QStringList                 Elements      ;
    QStringList                 Sequences     ;
    QList<SetOperator        *> Operations    ;
    QMap<QString,SetOperator *> OpMaps        ;
    QMap<QString,UUIDs        > Uuids         ;
    int                         Intermediates ;

    explicit SetsAlgebra  (QString expression) ;
    explicit SetsAlgebra  (void) ;
    virtual ~SetsAlgebra  (void) ;

    void     clear        (void) ;
    void     EmptyUuids   (void) ;
    bool     AssignUuids  (QString name,UUIDs & uuids) ;
    int      Total        (void) ;
    bool     Decode       (QString expression) ;
    bool     Execute      (UUIDs & Results) ;
    QString  Expanding    (int level,int startId,QString op) ;
    QString  Construct    (void) ;
    VarArgs  Arguments    (QString name) ;
    VarArgs  Arguments    (int index) ;

  protected:

    int      Count        (QString expr,QChar c) ;
    bool     addCompose   (QString expression,QString & name) ;
    bool     addOperator  (QString token,QString & name) ;
    bool     addElement   (QString name) ;
    bool     addInput     (QString name) ;
    bool     isPure       (QString token) ;
    QString  Companion    (QString token) ;
    QString  Construct    (QString element) ;

  private:

};


N::SetsAlgebra:: SetsAlgebra   ( QString expression )
               : Intermediates ( 1000000            )
               , Uuid          ( 0                  )
{
  Decode ( expression ) ;
}

N::SetsAlgebra:: SetsAlgebra   ( void    )
               : Intermediates ( 1000000 )
               , Expression    ( ""      )
               , Uuid          ( 0       )
{
}

N::SetsAlgebra::~SetsAlgebra (void)
{
  clear ( ) ;
}

void N::SetsAlgebra::clear(void)
{
  Expression    = ""                     ;
  Result        = ""                     ;
  Intermediates = 1000000                ;
  Inputs        . clear ( )              ;
  Elements      . clear ( )              ;
  Sequences     . clear ( )              ;
  OpMaps        . clear ( )              ;
  Uuids         . clear ( )              ;
  if (Operations.count()<=0) return      ;
  for (int i=0;i<Operations.count();i++) {
    delete Operations[i]                 ;
  }                                      ;
  Operations . clear ( )                 ;
}

void N::SetsAlgebra::EmptyUuids(void)
{
  QString n            ;
  UUIDs   e            ;
  foreach (n,Elements) {
    Uuids[n] = e       ;
  }                    ;
}

bool N::SetsAlgebra::AssignUuids(QString name,UUIDs & uuids)
{
  Uuids[name] = uuids ;
  return true         ;
}

int N::SetsAlgebra::Total(void)
{
  return Sequences.count() ;
}

N::VarArgs N::SetsAlgebra::Arguments(QString name)
{
  VarArgs NVA                              ;
  nKickOut (!OpMaps.contains(name) , NVA ) ;
  SetOperator * nso = OpMaps[name]         ;
  nKickOut ( IsNull(nso)           , NVA ) ;
  return nso->Arguments()                  ;
}

N::VarArgs N::SetsAlgebra::Arguments(int index)
{
  VarArgs NVA                           ;
  nKickOut ( index >= Total ( ) , NVA ) ;
  return Arguments(Sequences[index])    ;
}

bool N::SetsAlgebra::Decode(QString expression)
{
  clear ( )                                    ;
  Expression = expression                      ;
  nKickOut( Expression.length() <= 0 , false ) ;
  int l = Count ( Expression , QChar('(')    ) ;
  int r = Count ( Expression , QChar(')')    ) ;
  nKickOut( l <= 0                   , false ) ;
  nKickOut( r <= 0                   , false ) ;
  nKickOut( l != r                   , false ) ;
  QString e = Expression                       ;
  e = e.replace  ( "("  , "( "   )             ;
  e = e.replace  ( ")"  , " )"   )             ;
  e = e.replace  ( "&"  , " & "  )             ;
  e = e.replace  ( "|"  , " | "  )             ;
  e = e.replace  ( "-"  , " - "  )             ;
  e = e.replace  ( "\\" , " \\ " )             ;
  e = e.replace  ( "^"  , " ^ "  )             ;
  e = e.replace  ( "\r" , ""     )             ;
  e = e.replace  ( "\n" , ""     )             ;
  e . simplified (               )             ;
  while (e.contains("  "))                     {
    e = e.replace("  "," ")                    ;
  }                                            ;
  if (l==1)                                    {
    nKickOut (!isPure(e) , false )             ;
    if (addOperator(e,Result))                 {
      Sequences << Result                      ;
      return true                              ;
    }                                          ;
  } else                                       {
    if (addCompose(e,Result))                  {
      return true                              ;
    }                                          ;
  }                                            ;
  return false                                 ;
}

bool N::SetsAlgebra::Execute(UUIDs & Results)
{
  QString e                                   ;
  Results . clear ( )                         ;
  nKickOut ( Sequences.count() <= 0 , false ) ;
  for (int i=0;i<Sequences.count();i++)       {
    SetOperator * nso                         ;
    e   = Sequences[i]                        ;
    nso = OpMaps[e]                           ;
    if (IsNull(nso)) return false             ;
    if (!nso->Execute                         (
           Uuids[nso->A]                      ,
           Uuids[nso->B]                      ,
           Uuids[nso->N])      ) return false ;
  }                                           ;
  Results = Uuids [ Result ]                  ;
  return true                                 ;
}

int N::SetsAlgebra::Count(QString expr,QChar c)
{
  int r = 0                ;
  int l = expr.length()    ;
  for (int i=0;i<l;i++)    {
    if (expr.at(i)==c) r++ ;
  }                        ;
  return r                 ;
}

bool N::SetsAlgebra::addCompose(QString expression,QString & name)
{
  if (isPure(expression))                                        {
    if (addOperator(expression,name))                            {
      if (!Sequences.contains(name)) Sequences << name           ;
      return true                                                ;
    } else return false                                          ;
  }                                                              ;
  ////////////////////////////////////////////////////////////////
  QString token                                                  ;
  int l                                                          ;
  int r                                                          ;
  l = expression . indexOf     ( '(' )                           ;
  r = expression . lastIndexOf ( ')' )                           ;
  nKickOut ( l <  0 , false )                                    ;
  nKickOut ( r <  0 , false )                                    ;
  nKickOut ( l >= r , false )                                    ;
  token = expression . mid     ( l+1  , r-l-1  )                 ;
  token = token      . replace ( "("  , "( "   )                 ;
  token = token      . replace ( ")"  , " )"   )                 ;
  token = token      . replace ( "&"  , " & "  )                 ;
  token = token      . replace ( "|"  , " | "  )                 ;
  token = token      . replace ( "-"  , " - "  )                 ;
  token = token      . replace ( "\\" , " \\ " )                 ;
  token = token      . replace ( "^"  , " ^ "  )                 ;
  token . simplified           (               )                 ;
  while (token.contains("  "))                                   {
    token = token.replace("  "," ")                              ;
  }                                                              ;
  l = token . length()                                           ;
  r = 0                                                          ;
  bool PureA = true                                              ;
  bool PureB = true                                              ;
  SetOperator * nso = new SetOperator()                          ;
  nso->O = SetOperator::Nothing                                  ;
  while (r<l)                                                    {
    QChar c = token.at(r)                                        ;
    if (c==QChar('&'))                                           {
      nso->O = SetOperator::Intersection                        ;
    } else
    if (c==QChar('|'))                                           {
      nso->O = SetOperator::Union                               ;
    } else
    if (c==QChar('-'))                                           {
      nso->O = SetOperator::Complement                          ;
    } else
    if (c==QChar('\\'))                                          {
      nso->O = SetOperator::Complement                          ;
    } else
    if (c==QChar('^'))                                           {
      nso->O = SetOperator::Symmetric                           ;
    } else
    if (c==QChar('('))                                           {
      QString companion                                          ;
      QString n                                                  ;
      companion  = token.mid(r,l-r)                              ;
      if (companion.length()<=0)                                 {
        delete nso                                               ;
        return false                                             ;
      }                                                          ;
      companion  = Companion(companion)                          ;
      if (companion.length()<=0)                                 {
        delete nso                                               ;
        return false                                             ;
      }                                                          ;
      if (nso->O==SetOperator::Nothing)                          {
        QString cn = companion                                   ;
        cn.simplified()                                          ;
        if (addCompose(cn,n))                                    {
          nso->A = n                                             ;
          if (!Sequences.contains(n)) Sequences << n             ;
          PureA = false                                          ;
        } else                                                   {
          delete nso                                             ;
          return false                                           ;
        }                                                        ;
        r += companion.length()                                  ;
      } else                                                     {
        QString cn = companion                                   ;
        cn.simplified()                                          ;
        if (addCompose(cn,n))                                    {
          nso->B = n                                             ;
          if (!Sequences.contains(n)) Sequences << n             ;
          PureB = false                                          ;
        } else                                                   {
          delete nso                                             ;
          return false                                           ;
        }                                                        ;
        r = l                                                    ;
      }                                                          ;
    } else
    if (c==QChar(')'))                                           {
      if (nso->B.length()<=0)                                    {
        delete nso                                               ;
        return false                                             ;
      }                                                          ;
      r = l                                                      ;
    } else
    if (c==QChar(' '))                                           {
    } else                                                       {
      if (nso->O==SetOperator::Nothing)                         {
        nso->A.append(c)                                         ;
      } else                                                     {
        nso->B.append(c)                                         ;
      }                                                          ;
    }                                                            ;
    r++                                                          ;
  }                                                              ;
  if (nso->O==SetOperator::Nothing)                             {
    delete nso                                                   ;
    return false                                                 ;
  }                                                              ;
  ////////////////////////////////////////////////////////////////
  for (int i=0;i<Operations.count();i++)                         {
    SetOperator * lso = Operations[i]                            ;
    if ((*lso)==(*nso))                                          {
      delete nso                                                 ;
      name = lso->N                                              ;
      return true                                                ;
    }                                                            ;
  }                                                              ;
  ////////////////////////////////////////////////////////////////
  Intermediates++                                                ;
  name = QString("`%1`").arg(Intermediates)                      ;
  nso->N               = name                                    ;
  Operations          << nso                                     ;
  OpMaps     [ name ]  = nso                                     ;
  ////////////////////////////////////////////////////////////////
  addElement ( nso->A )                                          ;
  addElement ( nso->B )                                          ;
  addElement ( nso->N )                                          ;
  if (PureA && !Inputs.contains(nso->A))                         {
    Inputs << nso->A                                             ;
  }                                                              ;
  if (PureB && !Inputs.contains(nso->B))                         {
    Inputs << nso->B                                             ;
  }                                                              ;
  ////////////////////////////////////////////////////////////////
  if (!Sequences.contains(name)) Sequences << name               ;
  return true                                                    ;
}

bool N::SetsAlgebra::addOperator(QString token,QString & name)
{
  SetOperator * nso = new SetOperator()              ;
  if (!nso->Assign(token))                           {
    delete nso                                       ;
    return false                                     ;
  }                                                  ;
  ////////////////////////////////////////////////////
  for (int i=0;i<Operations.count();i++)             {
    SetOperator * lso = Operations[i]                ;
    if ((*lso)==(*nso))                              {
      delete nso                                     ;
      name = lso->N                                  ;
      return true                                    ;
    }                                                ;
  }                                                  ;
  ////////////////////////////////////////////////////
  Intermediates++                                    ;
  name = QString("`%1`").arg(Intermediates)          ;
  nso->N               = name                        ;
  Operations          << nso                         ;
  OpMaps     [ name ]  = nso                         ;
  ////////////////////////////////////////////////////
  addInput   ( nso->A )                              ;
  addInput   ( nso->B )                              ;
  addElement ( nso->N )                              ;
  return true                                        ;
}

bool N::SetsAlgebra::addElement(QString name)
{
  nKickOut ( Elements.contains(name) , false ) ;
  UUIDs E                                      ;
  Uuids [ name ]  = E                          ;
  Elements       << name                       ;
  return true                                  ;
}

bool N::SetsAlgebra::addInput(QString name)
{
  nKickOut ( !addElement(name) , false ) ;
  if (!Inputs.contains(name))            {
    Inputs << name                       ;
  }                                      ;
  return true                            ;
}

bool N::SetsAlgebra::isPure(QString token)
{
  nKickOut( token.length() <= 0 , false ) ;
  int l = Count ( token  , QChar('(')   ) ;
  int r = Count ( token  , QChar(')')   ) ;
  nKickOut      ( l != 1 , false        ) ;
  nKickOut      ( r != 1 , false        ) ;
  l = token . indexOf     ('(')           ;
  r = token . lastIndexOf (')')           ;
  nKickOut      ( l >= r , false        ) ;
  return true                             ;
}

QString N::SetsAlgebra::Companion(QString token)
{
  QString s   = ""                           ;
  int     len = token.length()               ;
  nKickOut ( len   <= 0 , s )                ;
  int     index = token.indexOf('(')         ;
  nKickOut ( index <  0 , s )                ;
  if (index>0)                               {
    for (int i=0;i<index;i++)                {
      s.append(token.at(i))                  ;
    }                                        ;
  }                                          ;
  s.append('(')                              ;
  index++                                    ;
  while (index<len)                          {
    QChar c = token.at(index)                ;
    if (c==')')                              {
      s.append(')')                          ;
      return s                               ;
    } else
    if (c=='(')                              {
      QString companion                      ;
      companion = token.mid(index,len-index) ;
      companion = Companion(companion)       ;
      if (companion.length()<=0) return ""   ;
      s.append(companion)                    ;
      index = s.length()                     ;
    } else                                   {
      s.append(c)                            ;
    }                                        ;
    index++                                  ;
  }                                          ;
  return  ""                                 ;
}

QString N::SetsAlgebra::Expanding(int level,int startId,QString op)
{
  QString expr                                  ;
  if (level<2) return expr                      ;
  if (level==2)                                 {
    QString a = QString::number(startId  )      ;
    QString b = QString::number(startId+1)      ;
    expr = QString ( "(%1 %2 %3)"               )
            .arg(QString("#%1").arg(a)          )
            .arg(op                             )
            .arg(QString("#%1").arg(b)        ) ;
  } else                                        {
    QString a = QString::number(startId       ) ;
    QString b = Expanding(level-1,startId+1,op) ;
    expr = QString ( "(%1 %2 %3)"               )
            .arg(QString("#%1").arg(a)          )
            .arg(op                             )
            .arg(b                            ) ;
  }                                             ;
  return expr                                   ;
}

QString N::SetsAlgebra::Construct(void)
{
  if (Sequences.count()<=0) return "" ;
  return Construct(Sequences.last())  ;
}

QString N::SetsAlgebra::Construct(QString element)
{
  nKickOut ( !OpMaps.contains(element) , "" )             ;
  SetOperator * nso = OpMaps[element]                     ;
  nKickOut ( IsNull(nso)               , "" )             ;
  QString A                                               ;
  QString B                                               ;
  QString O                                               ;
  if (Inputs.contains(nso->A) && Inputs.contains(nso->B)) {
    return nso->Syntax()                                  ;
  } else
  if (Inputs.contains(nso->A))                            {
    A = nso->A                                            ;
    B = Construct(nso->B)                                 ;
  } else
  if (Inputs.contains(nso->B))                            {
    A = Construct(nso->A)                                 ;
    B = nso->B                                            ;
  } else                                                  {
    A = Construct(nso->A)                                 ;
    B = Construct(nso->B)                                 ;
  }                                                       ;
  switch (nso->O)                                         {
    case SetOperator::Intersection                        :
      O = "&"                                             ;
    break                                                 ;
    case SetOperator::Union                               :
      O = "|"                                             ;
    break                                                 ;
    case SetOperator::Complement                          :
      O = "-"                                             ;
    break                                                 ;
    case SetOperator::Symmetric                           :
      O = "^"                                             ;
    break                                                 ;
  }                                                       ;
  nKickOut ( A.length() <= 0 , "" )                       ;
  nKickOut ( B.length() <= 0 , "" )                       ;
  nKickOut ( O.length() <= 0 , "" )                       ;
  return QString("( %1 %2 %3 )").arg(A).arg(O).arg(B)     ;
}
"""
