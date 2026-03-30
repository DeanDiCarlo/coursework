/*
	You'll need to manually load zipcodes.pl when working on
	the zip code rules.
*/

/*
A and B are instatiated integers. The third parameter is 
the maximum of the two numbers.  

	Queries that succeed:
		maxOfTwo(3, 4, 4).
		maxOfTwo(4, 3, MAX).      instaniates MAX to 4
	Queries that fail:
		maxOfTwo(3, 0, 9).
*/

maxOfTwo(A, B, C).


/*
A, B, and C are the coeficients of Ax^2 + Bx + C = 0. This function
will return a list with 0, 1, or 2 roots. If two roots are present,
the roots will be sorted in ascending order. You may assume, A is 
not 0.

	Queries that succeed:
		quadratic(4, 3, -1, Roots). instantiates 
				Roots to [-1, 0.25]
	Queries that fail:
		quadratic(4, 3, -1, []).
*/

quadratic(A, B, C, Roots).

/*
W1, L1, H1 are the width, length, and height of a 3D cube.
W2, L2, H2 are the width, length, and height of a second 3D cube.
The query will succeed if the volumn of the first cube is larger
than the volume of the second cube.

	Queries that succeed:
		isLargerCube(1, 2, 3, 1, 5, 1).
		isLargerCube(1, 2, 3, 2, 1, 2).
		isLargerCube(10, 2, 3, 1, 5, 1).
	Queries that fail:
		isLargerCube(1, 5, 1, 1, 2, 3).
*/

isLargerCube(W1, L1, H1, W2, L2, W2).

/*
Value is a value to be clamped.
Lo and Hi are define an interval.
ClampedValue is result of clamping Value into the range [Lo, Hi].

	Queries that succeed:
		clamp(0.5, 0.0, 1.0, X).    binds X to 0.5
		clamp(-0.5, 0.0, 1.0, 0.0).
	Queries that fail:
		clamp(0.5, 0.0, 1.0, 0.0).
*/

clamp(Value, Lo, Hi, ClampedValue).
 
/*
Succeeds if the CITY/STATE combination exists.
Queries that succeed:
	isACity('Oxford', 'OH').
	isACity('Oxford', S).   Binds S to 'OH'
*/

isACity(CITY, STATE).

/*
Succeeds if the PLACE/STATE/ZIPCODE combination exists.
Queries that succeed:
	getStateInfo('Oxford', 'OH', Z).   Binds Z to 45056
*/

getStateInfo(PLACENAME, STATE, ZIPCODE).

/*
	Succeeds if the incoming list of numbers
	contains all of the same value.
	
Queries that succeed:
	isConstantList([1, 1, 1]).
Queries that fail:
	isConstantList([1, 2, 1]).
*/

isConstantList(LST).

/*
	Creates the list containing only every other element,
	starting with the first.
	
Queries that succeed:
	eo([a,b,c,d], [a, c]).
	eo([a,b,c], [a, c]).
	eo([], []).
*/

eo(LST, EVERYOTHER).

/*
	Accepts a list of numbers and creates a list
	containing only the positive numbers, in the order
	in which they originally appeared.
	
Queries that succeed:
	positives([1,2,3], X).    Binds X to [1, 2, 3]
	positives([1,-2,3], X).    Binds X to [1, 3]
Queries that fail:
	positives([1,2,3], []).
*/

positives(LST, POS).

/*
Succeeds if OLD is the grandparent of NEW.
Queries that succeed:
	greatGrandparent(ggm, self).
	greatGrandparent(gm, d).
*/

greatGrandparent(OLD, NEW).

/*
Succeeds if OLD sits K generations directly above NEW. That
is, NEW is a direct descendant of OLD.
Queries that succeed:
	kthDescendant(ggm, self, 3).
*/
								
kthDescendant(OLD, NEW, K).

/*
Here are the parental relationships (see Google Docs file "GenerationNames"
located in the homework folder). The abbreviations used are based on females:
         D = daughther, A = aunt, N = niece, M = mother
So, ggm corresponds to great-grandmother. gn corresponds to great niece.
The following definitions are given to you for testing purposes. Your code should also work for other sets of people. The family tree will
not have cycles.
*/

parent(gggm, ggm).
parent(ggm, gm).
parent(gm, m).
parent(m, self).
parent(self, d).
parent(d, gd).

parent(gggm, gga). parent(gga, c12a). parent(c12a, c21a). parent(c21a, c3).
parent(ggm, ga). parent(ga, c11a). parent(c11a, c2).
parent(gm, a). parent(a, c1).

parent(m,s).
parent(s, n). parent(n, gn).
parent(c1, c11b). parent(c11b, c12b).

parent(c2, c21b). parent(c21b, c22).
parent(c3, c31). parent(c31, c32).

/*
Succeeds if P1 and P2 are Nth cousins M times removed.
N and M will be bound to integers when the query is issued.
You can add "parent" facts but you can't change those
that have been provided.

Successful queries:
 nthCousinMTimesRemoved(self, c3, 3, 0).
 nthCousinMTimesRemoved(self, c31, 3, 1).
 nthCousinMTimesRemoved(self, c32, 3, 2).

 nthCousinMTimesRemoved(self, c2, 2, 0).
 nthCousinMTimesRemoved(self, c21a, 2, 1).
 nthCousinMTimesRemoved(self, c21b, 2, 1).
 nthCousinMTimesRemoved(self, c22, 2, 2).

 nthCousinMTimesRemoved(self, c1, 1, 0).
 nthCousinMTimesRemoved(self, c11a, 1, 1).
 nthCousinMTimesRemoved(self, c11b, 1, 1).
 nthCousinMTimesRemoved(self, c12a, 1, 2).
 nthCousinMTimesRemoved(self, c12b, 1, 2).

 nthCousinMTimesRemoved(c1, c2, 2, 0).
 nthCousinMTimesRemoved(c2, c1, 2, 0).
 nthCousinMTimesRemoved(c11b, c32, 4, 1).
 nthCousinMTimesRemoved(c32, c11b, 4, 1).

Sample unsuccessful queries:
 nthCousinMTimesRemoved(self, gn, 1, 2).
 nthCousinMTimesRemoved(self, s, 1, 0).
 nthCousinMTimesRemoved(gd, ggm, 1, 1).
*/

nthCousinMTimesRemoved(X, Y, N, M).