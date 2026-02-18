% speed.pl

speed(ford, 100).
speed(chevy, 105).
speed(dodge, 95).
speed(volvo, 80).

time(ford, 20).
time(chevy, 21).
time(dodge, 24).
time(volvo, 24).

distance(X, Y) :- speed(X, Speed),
		  time(X, Time),
		  Y is Speed * Time.


add(A, B, S) :- S is A + B.

add2(A, B, S) :- nonvar(A), nonvar(B), var(S),
			S is A + B.

add2(A, B, S) :- nonvar(A), nonvar(S), var(B),
			B is S - A.

add2(A, B, S) :- nonvar(B), nonvar(S), var(A),
			A is S - B.
