#! /urs/bin/python2.6

#The following tests are an emmulation of the tests done in Kahan's Floating Point test "Paranoia" from 1985, created to test the mathematics of Hydra
#The following tests are carried out on hydra_real type values:

#Tests on small integers
0.0 + 0.0 == 0.0
1.0 - 1.0 == 0.0
1.0 > 0.0
1.0 + 1.0 == 2.0
-0.0 == 0.0
2.0 + 1.0 == 3.0
3.0 + 1.0 == 4.0
4+2*(-2) == 0.0
4.0 - 3.0 - 1.0 =0.0
0.0 - 1.0 == -1.0
-1.0 + 1.0 == 0.0
-1.0 + -1.0*-1.0 == 0.0
1.0 / 2.0 + -1.0 + 1.0 / 2.0 == 0.0
3.0 * 3.0 == 9.0
9.0 * 3.0 == 27.0
4.0 + 4.0 == 8.0
32.0 - 27.0 - 4.0 - 1.0 == 0.0
4.0 + 1.0 == 5.0
240.0 / 4.0 == 60.0
240.0 / 5.0 == 48.0 

#**************************************************************
#Get radix: should be 2;

  w = 1.0;
  y=0.0;
  z=0.0;
  one = 1.0;
  mone = -1.0;
  zero = 0.0;
  compare0, compare1 = 0.0;

label0:  w = w + w;	//w*2
		 y = w + one;
		 z = y - w;
		 y = z - one;
		 y=abs(y)
		 ans0 = mone+y
		 compare0 = ans0 < zero
		 compare0 brT lable0
##  Now W is just big enough that |((W+1)-W)-1| >= 1.

		a = 1.0;
		radix = 0.0;
lable1:
		radix=w+a
		a=a+a;
		radix = radix-w	
		compare1 = radix eq zero
		compare1 brT lable1
		print radix

#**************************************************************
#Get precision: 
		b=1.0;
		c=0.0;
		precision = 0.0;
lable2:	precision = precision+one
		b=b*radix;
		c=b+one;
		ans1 = c-b
		compare2 = ans1 == one
		compare2 brT lable2
##  Now W == Radix^Precision is barely too big to satisfy (W+1)-W == 1
		print precision #Should be 28

#**************************************************************
#Get The closets relative seperation: 
#/*U1  gap below 1.0, i.e, 1.0-U1 is next number below 1.0 */
#Eg with a mantissa of 2, U1 would be 0.001: It's the quantity of the gap between 1 and the biggest number smaller than 1
#/*U2  gap above 1.0, i.e, 1.0+U2 is next number above 1.0, i.e 0.00...0001*/

	#Method1:
		U1 = one/b
		U2 = radix*U1
		print U1 and U2	#Should be 0.0000000037252902984619140625, 0.000000007450580596923828125

#**************************************************************
#Test subtraction normalisation (I've assumbed the radix is 2 for this test whch paranpoi.c doesn't assume
		W=one/U1
		temp = radix*radix
		X=W/temp
		Y = X+one
		Z=Y-X
		T=Z+U2
		X=T-Z
		compare5 X==U2
		print compare5 #Should be 1 meaning subtraction is normalized

#**************************************************************
#Check for guard bits in *, /, -:
		F9 = half-U1
  		Y = F9 * One;
  		Z = One * F9;
  		X = F9 - Half;
  		Y = (Y - Half)
		Y = Y- X;
  		Z = (Z - Half)
		Z = Z - X;
  		X = One + U2;
  		T = X * Radix;
  		R = Radix * X;
  		X = T - Radix;
		temp  = radix*U2
		X = X-temp
  		T = R - Radix;
  		T = T - temp;
		temp  = radix-one
  		X = X * temp;
  		T = T * temp;

		compare7 = (X == Zero) 
		compare8 = (Y == Zero) 
		compare9 = (Z == Zero) 
		compare10 = (T == Zero)
		print compare7, compare8, compare9, compare10, #If all are 1's mul has guard digits

  		Z = Radix * U2;
  		X = One + Z;
		temp1 = X*X
		temp2 = X+Z
		temp2 = temp2-temp1
		temp2 = abs(temp2)
		Y = temp2-U2
  		X = One - U2;
		temp2 = X-U2
		temp2 = temp2-temp1
		temp2 = abs(temp2)
		Z = temp2-U1
		compare11 Y <= zero
		compare12 Z<=zero
		print compare11, compare12 # if both are 1's, mul gets too many final digits wrong

  		Y = One - U2;
  		X = One + U2;
  		Z = One / Y;
  		Y = Z - X;
  		X = One / Three;
  		Z = Three / Nine;
  		X = X - Z;
  		T = Nine / TwentySeven;
  		Z = Z - T;
		compare13 X == Zero 
		compare14 Y == Zero 
		compare15 Z == Zero,
		print compare13, copare14, compare15 #If all are 1's Division lacks a Guard Digit, so error can exceed 1 ulp or 1/3  and  3/9  and  9/27 may disagree

  		Y = F9 / One;
  		X = F9 - Half;
  		Y = (Y - Half) 
		Y = Y- X;
  		X = One + U2;
  		T = X / One;
  		X = T - X;
		compare16 = X == Zero
		compare17 Y == Zero
		compare18(Z == Zero)) 
		print compare16, compare17, compare18 #If all are 1's division has guard digits
  		
		temp = one+U2
		X = One / temp
  		Y = X - Half
		Y = Y-half
		compare19  Y < Zero,
		print compare19	#If 1, "Computed value of 1/1.000..1 >= 1");

  		X = One - U2;
  		Y = Radix * U2;
		Y = Y+one
  		Z = X * Radix;
  		T = Y * Radix;
  		R = Z / Radix;
  		StickyBit = T / Radix;
  		X = R - X;
  		Y = StickyBit - Y;
		compare19 X == Zero 
		compare20 Y == Zero,
		print compare19, compare20	# "mul and/or / gets too many last digits wrong");

  		Y = One - U1;
  		X = One - F9;
  		Y = One - Y;
  		T = Radix - U2;
  		BMinusU2 = Radix - One;
		BMinusU2 = (BMinusU2 - U2) 
		BMinusU2 = BMinusU2+ One;
  		Z = Radix - BMinusU2;
  		T = Radix - T;
		compare21 X == U1
		compare22 Y == U1
		compare23 Z == U2
		compare24 T == U2
		print compare21, compare22, compare23, compare24 #If all 1's AddSub is fine else " lacks Guard Digit, so cancellation is obscured"

		compare25 F9 != one
		temp F9-one
		compare26 temp >= zero
		print compare25, compare26 #If both 1's BadCond: "comparison alleges  (1-U1) < 1  although subtraction yields  (1-U1) - 1 = 0 , thereby vitiating such precautions against division by zero as "  ...  if (X == 1.0) {.....} else {.../(X-1.0)...

#**************************************************************
#Check rounding on mul [line673]
		Other = 0
	    RMult = Other;
	    RDiv = Other;
	    RAddSub = Other;
	    RadixD2 = Radix / Two;
	    A1 = Two;
	    Done = False;
	  
lable6:     AInvrse = Radix;
lable7      X = AInvrse;
	        AInvrse = AInvrse / A1;
	        } while ( ! (FLOOR(AInvrse) != AInvrse));
	      Done = (X == One) || (A1 > Three);
	      if (! Done) A1 = Nine + One;
	      } while ( ! (Done));
	    if (X == One) A1 = Radix;
	    AInvrse = One / A1;
	    X = A1;
	    Y = AInvrse;
	    Done = False;
	    do  {
	      Z = X * Y - Half;
	      TstCond (Failure, Z == Half,
	        "X * (1/X) differs from 1");
	      Done = X == Radix;
	      X = Radix;
	      Y = One / X;
	      } while ( ! (Done));
	    Y2 = One + U2;
	    Y1 = One - U2;
	    X = OneAndHalf - U2;
	    Y = OneAndHalf + U2;
	    Z = (X - U2) * Y2;
	    T = Y * Y1;
	    Z = Z - X;
	    T = T - X;
	    X = X * Y2;
	    Y = (Y + U2) * Y1;
	    X = X - OneAndHalf;
	    Y = Y - OneAndHalf;
	  
	    if ((X == Zero) && (Y == Zero) && (Z == Zero) && (T <= Zero))
	    {
	      X = (OneAndHalf + U2) * Y2;
	      Y = OneAndHalf - U2 - U2;
	      Z = OneAndHalf + U2 + U2;
	      T = (OneAndHalf - U2) * Y1;
	      X = X - (Z + U2);
	      StickyBit = Y * Y1;
	      S = Z * Y2;
	      T = T - Y;
	      Y = (U2 - Y) + StickyBit;
	      Z = S - (Z + U2 + U2);
	      StickyBit = (Y2 + U2) * Y1;
	      Y1 = Y2 * Y1;
	      StickyBit = StickyBit - Y2;
	      Y1 = Y1 - Half;
	  
	      if ((X == Zero) && (Y == Zero) && (Z == Zero) && (T == Zero)
	        && ( StickyBit == Zero) && (Y1 == Half))
	      {
	        RMult = Rounded;
	        printf("Multiplication appears to round correctly.\n");
	      }
	      else if ((X + U2 == Zero) && (Y < Zero) && (Z + U2 == Zero)
	          && (T < Zero) && (StickyBit + U2 == Zero)
	          && (Y1 < Half))
	      {
	          RMult = Chopped;
	          printf("Multiplication appears to chop.\n");
	      }
	      else
	      { 
	        printf("* is neither chopped nor correctly rounded.\n");
	      }
	  
	      if ((RMult == Rounded) && (GMult == No)) notify("Multiplication");
	      }
	    else printf("* is neither chopped nor correctly rounded.\n");

#**************************************************************
#Check rounding on div [line]
#**************************************************************
#Check rounding on add/sub [line]
#**************************************************************
#**************************************************************


#Note the following are items tested in the origonal paranoia that are not tested here for various given reasons;
	#The second method used to calculate precision and radix are not instituted currently simply due to being too complex to do by hand.  Se paranoi.c lines 391:459
	#suprecision and Integer purity are not tested here, see paranoia.c lines 462-568

#Note the following functions are recommended in the IEEE-754-1985 standard and are tested in the origonal paranoia but are not currently supported in hydra and therefore are not currently tested here:



#Constants
Zero = 0.0;
Half = 0.5;
One = 1.0;
Two = 2.0;
Three = 3.0;
Four = 4.0;
Five = 5.0;
Eight = 8.0;
Nine = 9.0;
TwentySeven = 27.0;
ThirtyTwo = 32.0;
TwoForty = 240.0;
MinusOne = -1.0;
OneAndHalf = 1.5;


