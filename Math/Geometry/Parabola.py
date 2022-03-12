# -*- coding: utf-8 -*-
##############################################################################
## Parabola
##############################################################################
## y = a * x ^ 2 + b * x + c
##############################################################################
class Parabola   (                                                         ) :
  ############################################################################
  def __init__   ( self                                                    ) :
    ##########################################################################
    self . clear (                                                           )
    ##########################################################################
    return
  ############################################################################
  def __del__    ( self                                                    ) :
    ##########################################################################
    ##########################################################################
    return
  ############################################################################
  def clear  ( self                                                        ) :
    ##########################################################################
    self . n   = 0
    self . a   = 0
    self . b   = 0
    self . c   = 0
    self . PA0 = 0
    self . PA1 = 0
    self . PA2 = 0
    self . T1  = 0
    self . T2  = 0
    self . T3  = 0
    self . T4  = 0
    self . pa0 = 0
    self . pa1 = 0
    self . pa2 = 0
    self . t1  = 0
    self . t2  = 0
    self . t3  = 0
    self . t4  = 0
    self . V1  = 0
    self . V2  = 0
    self . V3  = 0
    self . W1  = 0
    self . W2  = 0
    self . A   = 0
    self . B   = 0
    self . C   = 0
    self . D   = 0
    self . E   = 0
    self . F   = 0
    self . M   = 0
    self . P   = 0
    self . R   = 0
    self . p   = 0
    self . mp  = 0.00000000001
    ##########################################################################
    return
  ############################################################################
  def assign ( self , parabola                                             ) :
    ##########################################################################
    self . n   = parabola . n
    self . a   = parabola . a
    self . b   = parabola . b
    self . c   = parabola . c
    self . PA0 = parabola . PA0
    self . PA1 = parabola . PA1
    self . PA2 = parabola . PA2
    self . T1  = parabola . T1
    self . T2  = parabola . T2
    self . T3  = parabola . T3
    self . T4  = parabola . T4
    self . pa0 = parabola . pa0
    self . pa1 = parabola . pa1
    self . pa2 = parabola . pa2
    self . t1  = parabola . t1
    self . t2  = parabola . t2
    self . t3  = parabola . t3
    self . t4  = parabola . t4
    self . V1  = parabola . V1
    self . V2  = parabola . V2
    self . V3  = parabola . V3
    self . W1  = parabola . W1
    self . W2  = parabola . W2
    self . A   = parabola . A
    self . B   = parabola . B
    self . C   = parabola . C
    self . D   = parabola . D
    self . E   = parabola . E
    self . F   = parabola . F
    self . M   = parabola . M
    self . P   = parabola . P
    self . R   = parabola . R
    self . p   = parabola . p
    self . mp  = parabola . mp
    ##########################################################################
    return
  ############################################################################
  def setParameters ( self , a , b , c                                     ) :
    ##########################################################################
    self . a = a
    self . b = b
    self . c = c
    ##########################################################################
    return
  ############################################################################
  def Append         ( self , key , value                                  ) :
    ##########################################################################
    self . Add       (        key , value                                    )
    self . Epitomize (                                                       )
    ##########################################################################
    return
  ############################################################################
  def Add ( self , key , value                                             ) :
    ##########################################################################
    self . n   = self . n + 1
    self . t1  = key                                                        ## x
    self . t2  = self . t1  * self . t1                                     ## x ^ 2
    self . t3  = self . t2  * self . t1                                     ## x ^ 3
    self . t4  = self . t3  * self . t1                                     ## x ^ 4
    self . pa0 = value                                                      ## v
    self . pa1 = self . pa0 * self . t1                                     ## v * x
    self . pa2 = self . pa0 * self . t2                                     ## v * x * x
    self . T1  = self . T1  + self . t1
    self . T2  = self . T2  + self . t2
    self . T3  = self . T3  + self . t3
    self . T4  = self . T4  + self . t4
    self . PA0 = self . PA0 + self . pa0
    self . PA1 = self . PA1 + self . pa1
    self . PA2 = self . PA2 + self . pa2
    ##########################################################################
    return
  ############################################################################
  def Epitomize ( self                                                     ) :
    ##########################################################################
    self   . V1 =  self . T1 * self . T1
    self   . V2 =  self . T2 * self . T2
    self   . V3 =  self . T3 * self . T3
    ##########################################################################
    self   . W1 =  self . T1 * self . T3
    self   . W2 =  self . T2 * self . T4
    ##########################################################################
    self   . P  =  2         * ( self . T2 * self . W1 )
    self   . P  =  self . P  + ( self . n  * self . W2 )
    self   . P  =  self . P  - ( self . T4 * self . V1 )
    self   . P  =  self . P  - ( self . T2 * self . V2 )
    self   . P  =  self . P  - ( self . n  * self . V3 )
    ##########################################################################
    self   . A  =   self . W1 - self . V2
    self   . B  = ( self . T2 * self . T3 ) - ( self . T1 * self . T4 )
    self   . C  = ( self . T1 * self . T2 ) - ( self . n  * self . T3 )
    self   . D  = ( self . n  * self . T2 ) - self . V1
    self   . E  = ( self . n  * self . T4 ) - self . V2
    self   . F  =   self . W2 - self . V3
    ##########################################################################
    self   . a  = ( self . PA0 * self . A ) + ( self . PA1 * self . C ) + ( self . PA2 * self . D )
    self   . b  = ( self . PA0 * self . B ) + ( self . PA1 * self . E ) + ( self . PA2 * self . C )
    self   . c  = ( self . PA0 * self . F ) + ( self . PA1 * self . B ) + ( self . PA2 * self . A )
    ##########################################################################
    self   . p  = self . P
    ##########################################################################
    if          ( self . p < 0                                             ) :
      self . p = - self . p
    ##########################################################################
    if          ( self . p < self . mp                                     ) :
      ########################################################################
      self . a = 0.0
      self . b = 0.0
      self . c = 0.0
      ########################################################################
    else                                                                     :
      ########################################################################
      self . a = self . a / self . P
      self . b = self . b / self . P
      self . c = self . c / self . P
    ##########################################################################
    return
  ############################################################################
  def Equation ( self , k                                                  ) :
    ##########################################################################
    k2 = k * k
    ##########################################################################
    return ( k2 * self . a ) + ( k * self . b ) + c
  ############################################################################
  def Slope ( self , k                                                     ) :
    return  ( 2 * k * self . a ) + self . b
  ############################################################################
  def Degeneration ( self , minimum = 0.00000000000001                     ) :
    ##########################################################################
    aa   = self . a
    mm   = minimum
    ##########################################################################
    if             ( aa < 0                                                ) :
      aa = -aa
    ##########################################################################
    if             ( mm < 0                                                ) :
      mm = -mm
    ##########################################################################
    return         ( aa < mm                                                 )
  ############################################################################
  def Transit ( self , minimum = 0.00000000000001                          ) :
    ##########################################################################
    bb   = self . b
    mm   = minimum
    ##########################################################################
    if        ( bb < 0                                                     ) :
      bb = -bb
    ##########################################################################
    if        ( mm < 0                                                     ) :
      mm = -mm
    ##########################################################################
    return    ( bb < mm                                                      )
    ##########################################################################
    return
  ############################################################################
  def Extreme ( self                                                       ) :
    ##########################################################################
    aa =   self . a + self . a
    bb = - self . b
    ##########################################################################
    return    ( bb / aa                                                      )
    ##########################################################################
    return
  ############################################################################
  def Dissect ( self , v , minimum = 0.00000000000001                      ) :
    ##########################################################################
    minus   =   minimum
    plus    = - minimum
    ##########################################################################
    if        ( minimum > 0                                                ) :
      minus = - minimum
      plus  =   minimum
    ##########################################################################
    if        ( v < minus                                                  ) :
      return -1
    ##########################################################################
    if        ( v > plus                                                   ) :
      return  1
    ##########################################################################
    return 0
  ############################################################################
  def Determinant ( self , M                                               ) :
    ##########################################################################
    M [ 0 ] = self . A
    M [ 1 ] = self . B / 2
    M [ 2 ] = self . D / 2
    M [ 3 ] = M   [ 1                                                        ]
    M [ 4 ] = self . C
    M [ 5 ] = self . E / 2
    M [ 6 ] = M   [ 2                                                        ]
    M [ 7 ] = M   [ 5                                                        ]
    M [ 8 ] = self . F
    ##########################################################################
    return M
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

};
"""
