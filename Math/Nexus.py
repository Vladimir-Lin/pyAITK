# -*- coding: utf-8 -*-
##############################################################################
## Nexus
##############################################################################
class Nexus      (                                                         ) :
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
class Q_DISCRETE_EXPORT Relation
{
  public:

    SUID    relation  ;
    int     linkType  ;
    SUID    flags     ;
    QString name      ;
    void  * data      ;
    VarArgs arguments ;
    Nodes   nodes     ;

    explicit Relation     (SUID relate,int linkType) ;
    explicit Relation     (void) ;
    virtual ~Relation     (void) ;

    Relation & operator = (Relation & relation) ;
    Relation & equalTo    (Relation & relation) ;

    void connect          (Node & first,Node & second) ;
    void disconnect       (void) ;

    // More than binary relation
    int  join             (Node & node) ;
    int  operator      += (Node & node) ;

    int  Indexing         (Node * node) ;
    bool isFirst          (Node * node) ;
    bool isEnd            (Node * node) ;
    bool isDating         (void) ;

    bool is               (N::Groups::Relations relate) ;

    int  connexion        (void) const ;

  protected:

  private:

};



N::Relation:: Relation (SUID relate,int lt)
            : relation (relate            )
            , linkType (                lt)
            , flags    (0                 )
            , name     (""                )
            , data     (NULL              )
{
}

N::Relation:: Relation (void)
            : relation (0   )
            , linkType (0   )
            , flags    (0   )
            , name     (""  )
            , data     (NULL)
{
}

N::Relation::~Relation(void)
{
}

N::Relation & N::Relation::operator = (Relation & relation)
{
  return equalTo ( relation ) ;
}

N::Relation & N::Relation::equalTo(Relation & relate)
{
  relation  = relate.relation  ;
  linkType  = relate.linkType  ;
  flags     = relate.flags     ;
  name      = relate.name      ;
  data      = relate.data      ;
  arguments = relate.arguments ;
  nodes     = relate.nodes     ;
  return ME                    ;
}

void N::Relation::connect(Node & first,Node & second)
{
  disconnect ( )                    ;
  nodes << &first                   ;
  nodes << &second                  ;
  for (int i=0;i<nodes.count();i++) {
    nodes[i]->Marriage(this)        ;
  }                                 ;
}

void N::Relation::disconnect(void)
{
  for (int i=0;i<nodes.count();i++) {
    nodes[i]->Divorce(this)         ;
  }                                 ;
  nodes . clear ( )                 ;
}

int N::Relation::join(Node & node)
{
  nodes << &node           ;
  node.Marriage(this)      ;
  return nodes . count ( ) ;
}

int N::Relation::operator += (Node & node)
{
  return join ( node ) ;
}

int N::Relation::Indexing(Node * node)
{
  return nodes . indexOf ( node ) ;
}

bool N::Relation::isFirst(Node * node)
{
  if (nodes.count()<=0) return false ;
  int index = Indexing(node)         ;
  if (index<0) return false          ;
  return ( index == 0 )              ;
}

bool N::Relation::isEnd(Node * node)
{
  if (nodes.count()<=1) return false ;
  int index = Indexing(node)         ;
  if (index<0) return false          ;
  index++                            ;
  return ( index == nodes.count() )  ;
}

bool N::Relation::isDating(void)
{
  return ( nodes . count () == 1 ) ;
}

bool N::Relation::is(N::Groups::Relations relate)
{
  return nEqual ( linkType , (int)relate ) ;
}

int N::Relation::connexion(void) const
{
  return relation ;
}
"""
