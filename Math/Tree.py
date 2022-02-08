# -*- coding: utf-8 -*-
##############################################################################
## Tree
##############################################################################
class Tree       (                                                         ) :
  ############################################################################
  def __init__   ( self                                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    return
##############################################################################



class Q_DISCRETE_EXPORT Tree : public Graph
{
  public:

    Node * root ;

    explicit Tree         (void) ;
    virtual ~Tree         (void) ;

    void setRoot          (Node * node) ;

    virtual int parenting (Node * father,Node * child) ;

  protected:

    int RelationId ;

  private:

};


N::Tree:: Tree       (void)
        : Graph      (    )
        , root       (NULL)
        , RelationId (0   )
{
}

N::Tree::~Tree (void)
{
}

void N::Tree::setRoot(Node * node)
{
  if (addNode(node)) {
    root = node      ;
  } else             {
    root = node      ;
  }                  ;
}

int N::Tree::parenting(Node * father,Node * child)
{
  Relation * r                            ;
  r = new Relation ( RelationId , 0     ) ;
  Mount            ( r , father , child ) ;
  RelationId ++                           ;
  return RelationId                       ;
}

