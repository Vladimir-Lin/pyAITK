# -*- coding: utf-8 -*-
##############################################################################
## Parabola
##############################################################################
## from . Nexus import Nexus as Nexus
##############################################################################
class Parabola              (                                                ) :
  ############################################################################
  def __init__            ( self                                           ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def __del__     ( self                                                   ) :
    ##########################################################################
    ##########################################################################
    return
##############################################################################
"""
class Q_GEOMETRY_EXPORT Parabola
{ // y = a * x ^ 2 + b * x + c
  public:

    int    n   ;
    double a   ;
    double b   ;
    double c   ;
    double PA0 ;
    double PA1 ;
    double PA2 ;
    double T1  ;
    double T2  ;
    double T3  ;
    double T4  ;
    double pa0 ;
    double pa1 ;
    double pa2 ;
    double t1  ;
    double t2  ;
    double t3  ;
    double t4  ;
    double V1  ;
    double V2  ;
    double V3  ;
    double W1  ;
    double W2  ;
    double p   ;
    double A   ; // [ A * x ^ 2 + B * x * y + C * y ^ 2 + D * x + E * y + F ]
    double B   ;
    double C   ;
    double D   ; // if not used as
    double E   ; // [ A * x ^ 2 + B * x * y + C * y ^ 2 + D * x + E * y + F ]
    double F   ; // A-F will be used as the best fit line paraments
    double M   ;
    double P   ;
    double R   ;
    double mp  ;

    explicit Parabola        (void);
             Parabola        (const Parabola & parabola) ;
    virtual ~Parabola        (void);

    Parabola & operator =    (const Parabola & parabola) ;

    void       clear         (void) ;
    void       setParameters (double a,double b,double c) ;
    void       Append        (double key,double value) ;
    void       Add           (double key,double value) ;
    void       Epitomize     (void) ;
    double     Equation      (double key) ; // ( a * k * k ) + ( b * k ) + c
    double     Slope         (double key) ; // ( 2 * a * k ) + b
    double     Extreme       (void) ; // -b / 2a
    int        Dissect       (double v,double m = 0.00000000000001f) ; // -1 : ( v < -m ) , 1 : ( v > m ) , 0 : [ -m , m ]
    bool       Degeneration  (double minimum = 0.00000000000001f) ; // |a| < minimum
    bool       Transit       (double minimum = 0.00000000000001f) ; // |b| < minimum
    // Focus ( u , v )
    // Directrix : ax + by + c
    // ( [ ax + by + c ] ^ 2 / ( a ^ 2 + b ^2 ) ) = ( x - u ) ^ 2 + ( y - v ) ^ 2
    void       Determinant   (Matrix & matrix) ;
    QByteArray toByteArray   (void) ;
    void       toByteArray   (QByteArray & data) ;
    void       setByteArray  (QByteArray & data) ;
    void       operator =    (QByteArray & data) ;

};

typedef struct   {
  int    n       ;
  double a       ;
  double b       ;
  double c       ;
  double PA0     ;
  double PA1     ;
  double PA2     ;
  double T1      ;
  double T2      ;
  double T3      ;
  double T4      ;
  double pa0     ;
  double pa1     ;
  double pa2     ;
  double t1      ;
  double t2      ;
  double t3      ;
  double t4      ;
  double V1      ;
  double V2      ;
  double V3      ;
  double W1      ;
  double W2      ;
  double p       ;
  double A       ;
  double B       ;
  double C       ;
  double D       ;
  double E       ;
  double F       ;
  double M       ;
  double P       ;
  double R       ;
  double mp      ;
} ParabolaPacket ;

N::Parabola:: Parabola(void)
{
  mp = 0.00000000001 ;
  clear ( )          ;
}

N::Parabola:: Parabola(const Parabola & parabola)
{
  ME = parabola ;
}

N::Parabola::~Parabola(void)
{
}

void N::Parabola::clear(void)
{
  n   = 0             ;
  a   = 0             ;
  b   = 0             ;
  c   = 0             ;
  PA0 = 0             ;
  PA1 = 0             ;
  PA2 = 0             ;
  T1  = 0             ;
  T2  = 0             ;
  T3  = 0             ;
  T4  = 0             ;
  pa0 = 0             ;
  pa1 = 0             ;
  pa2 = 0             ;
  t1  = 0             ;
  t2  = 0             ;
  t3  = 0             ;
  t4  = 0             ;
  V1  = 0             ;
  V2  = 0             ;
  V3  = 0             ;
  W1  = 0             ;
  W2  = 0             ;
  A   = 0             ;
  B   = 0             ;
  C   = 0             ;
  D   = 0             ;
  E   = 0             ;
  F   = 0             ;
  M   = 0             ;
  P   = 0             ;
  R   = 0             ;
  p   = 0             ;
}

N::Parabola & N::Parabola::operator = (const Parabola & parabola)
{
  nMemberCopy ( parabola , n   ) ;
  nMemberCopy ( parabola , a   ) ;
  nMemberCopy ( parabola , b   ) ;
  nMemberCopy ( parabola , c   ) ;
  nMemberCopy ( parabola , PA0 ) ;
  nMemberCopy ( parabola , PA1 ) ;
  nMemberCopy ( parabola , PA2 ) ;
  nMemberCopy ( parabola , T1  ) ;
  nMemberCopy ( parabola , T2  ) ;
  nMemberCopy ( parabola , T3  ) ;
  nMemberCopy ( parabola , T4  ) ;
  nMemberCopy ( parabola , pa0 ) ;
  nMemberCopy ( parabola , pa1 ) ;
  nMemberCopy ( parabola , pa2 ) ;
  nMemberCopy ( parabola , t1  ) ;
  nMemberCopy ( parabola , t2  ) ;
  nMemberCopy ( parabola , t3  ) ;
  nMemberCopy ( parabola , t4  ) ;
  nMemberCopy ( parabola , V1  ) ;
  nMemberCopy ( parabola , V2  ) ;
  nMemberCopy ( parabola , V3  ) ;
  nMemberCopy ( parabola , W1  ) ;
  nMemberCopy ( parabola , W2  ) ;
  nMemberCopy ( parabola , A   ) ;
  nMemberCopy ( parabola , B   ) ;
  nMemberCopy ( parabola , C   ) ;
  nMemberCopy ( parabola , D   ) ;
  nMemberCopy ( parabola , E   ) ;
  nMemberCopy ( parabola , F   ) ;
  nMemberCopy ( parabola , M   ) ;
  nMemberCopy ( parabola , P   ) ;
  nMemberCopy ( parabola , R   ) ;
  nMemberCopy ( parabola , p   ) ;
  nMemberCopy ( parabola , mp  ) ;
  return ME                      ;
}

void N::Parabola::setParameters(double aa,double bb,double cc)
{
  a = aa ;
  b = bb ;
  c = cc ;
}

void N::Parabola::Append(double key,double value)
{
  Add       ( key , value ) ;
  Epitomize (             ) ;
}

void N::Parabola::Add(double key,double value)
{
  n++             ;
  t1   = key      ; // x
  t2   = t1  * t1 ; // x ^ 2
  t3   = t2  * t1 ; // x ^ 3
  t4   = t3  * t1 ; // x ^ 4
  pa0  = value    ; // v
  pa1  = pa0 * t1 ; // v * x
  pa2  = pa0 * t2 ; // v * x * x
  T1  += t1       ;
  T2  += t2       ;
  T3  += t3       ;
  T4  += t4       ;
  PA0 += pa0      ;
  PA1 += pa1      ;
  PA2 += pa2      ;
}

void N::Parabola::Epitomize(void)
{
  V1 =  T1 * T1                          ;
  V2 =  T2 * T2                          ;
  V3 =  T3 * T3                          ;
  W1 =  T1 * T3                          ;
  W2 =  T2 * T4                          ;
  P  =  2  * T2 * W1                     ;
  P +=  n  * W2                          ;
  P -=  T4 * V1                          ;
  P -=  T2 * V2                          ;
  P -=  n  * V3                          ;
  A  =  W1 - V2                          ;
  B  = (T2 * T3) - (T1 * T4)             ;
  C  = (T1 * T2) - ( n * T3)             ;
  D  = ( n * T2) - V1                    ;
  E  = ( n * T4) - V2                    ;
  F  = W2 - V3                           ;
  a  = (PA0 * A) + (PA1 * C) + (PA2 * D) ;
  b  = (PA0 * B) + (PA1 * E) + (PA2 * C) ;
  c  = (PA0 * F) + (PA1 * B) + (PA2 * A) ;
  p  = P                                 ;
  if ( p < 0  ) p = -p                   ;
  if ( p < mp )                          {
    a  = 0.0                             ;
    b  = 0.0                             ;
    c  = 0.0                             ;
  } else                                 {
    a /= P                               ;
    b /= P                               ;
    c /= P                               ;
  }                                      ;
}

double N::Parabola::Equation(double k)
{
  double k2 = nSquare( k )      ;
  return (k2 * a) + (k * b) + c ;
}

double N::Parabola::Slope(double k)
{
  return ( 2 * k * a ) + b ;
}

bool N::Parabola::Degeneration (double m)
{
  double aa = a          ;
  double mm = m          ;
  if ( aa < 0 ) aa = -aa ;
  if ( mm < 0 ) mm = -mm ;
  return ( aa < mm )     ;
}

bool N::Parabola::Transit (double m)
{
  double bb = b          ;
  double mm = m          ;
  if ( bb < 0 ) bb = -bb ;
  if ( mm < 0 ) mm = -mm ;
  return ( bb < mm )     ;
}

double N::Parabola::Extreme(void)
{
  double aa =  a     ;
  double bb = -b     ;
  aa += aa           ;
  return ( bb / aa ) ;
}

int N::Parabola::Dissect(double v,double m)
{
  double minus               ;
  double plus                ;
  if ( m > 0 )               {
    minus = - m              ;
    plus  =   m              ;
  } else                     {
    minus =   m              ;
    plus  = - m              ;
  }                          ;
  if ( v < minus ) return -1 ;
  if ( v > plus  ) return  1 ;
  return 0                   ;
}

void N::Parabola::Determinant(Matrix & M)
{
  M.set(Cpp::Double,3,3)            ;
  double *  V = (double *)M.array() ;
  V [ 0 ] = A                       ;
  V [ 1 ] = B / 2                   ;
  V [ 2 ] = D / 2                   ;
  V [ 3 ] = V [ 1 ]                 ;
  V [ 4 ] = C                       ;
  V [ 5 ] = E / 2                   ;
  V [ 6 ] = V [ 2 ]                 ;
  V [ 7 ] = V [ 5 ]                 ;
  V [ 8 ] = F                       ;
}

QByteArray N::Parabola::toByteArray (void)
{
  QByteArray B      ;
  toByteArray ( B ) ;
  return B          ;
}

void N::Parabola::toByteArray(QByteArray & data)
{
  data . resize ( sizeof ( ParabolaPacket ) )         ;
  ParabolaPacket * PP = (ParabolaPacket *)data.data() ;
  #define CPX(item) PP -> item = item
  CPX ( n   ) ;
  CPX ( a   ) ;
  CPX ( b   ) ;
  CPX ( c   ) ;
  CPX ( PA0 ) ;
  CPX ( PA1 ) ;
  CPX ( PA2 ) ;
  CPX ( T1  ) ;
  CPX ( T2  ) ;
  CPX ( T3  ) ;
  CPX ( T4  ) ;
  CPX ( pa0 ) ;
  CPX ( pa1 ) ;
  CPX ( pa2 ) ;
  CPX ( t1  ) ;
  CPX ( t2  ) ;
  CPX ( t3  ) ;
  CPX ( t4  ) ;
  CPX ( V1  ) ;
  CPX ( V2  ) ;
  CPX ( V3  ) ;
  CPX ( W1  ) ;
  CPX ( W2  ) ;
  CPX ( p   ) ;
  CPX ( A   ) ;
  CPX ( B   ) ;
  CPX ( C   ) ;
  CPX ( D   ) ;
  CPX ( E   ) ;
  CPX ( F   ) ;
  CPX ( M   ) ;
  CPX ( P   ) ;
  CPX ( R   ) ;
  CPX ( mp  ) ;
  #undef  CPX
}

void N::Parabola::setByteArray(QByteArray & data)
{
  if ( sizeof ( ParabolaPacket ) != data . size ( ) ) return ;
  ParabolaPacket * PP = (ParabolaPacket *)data.data()        ;
  #define CPX(item) item = PP -> item
  CPX ( n   ) ;
  CPX ( a   ) ;
  CPX ( b   ) ;
  CPX ( c   ) ;
  CPX ( PA0 ) ;
  CPX ( PA1 ) ;
  CPX ( PA2 ) ;
  CPX ( T1  ) ;
  CPX ( T2  ) ;
  CPX ( T3  ) ;
  CPX ( T4  ) ;
  CPX ( pa0 ) ;
  CPX ( pa1 ) ;
  CPX ( pa2 ) ;
  CPX ( t1  ) ;
  CPX ( t2  ) ;
  CPX ( t3  ) ;
  CPX ( t4  ) ;
  CPX ( V1  ) ;
  CPX ( V2  ) ;
  CPX ( V3  ) ;
  CPX ( W1  ) ;
  CPX ( W2  ) ;
  CPX ( p   ) ;
  CPX ( A   ) ;
  CPX ( B   ) ;
  CPX ( C   ) ;
  CPX ( D   ) ;
  CPX ( E   ) ;
  CPX ( F   ) ;
  CPX ( M   ) ;
  CPX ( P   ) ;
  CPX ( R   ) ;
  CPX ( mp  ) ;
  #undef  CPX
}

void N::Parabola::operator = (QByteArray & data)
{
  setByteArray ( data ) ;
}
"""
