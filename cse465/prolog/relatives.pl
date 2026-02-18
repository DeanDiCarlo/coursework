% relatives.pl

female(janet).
female(jennifer).
female(hannah).
female(abigail).

male(todd).
male(matt).
male(mitch).
male(mike).
male(phil).

father(mike, abigail).
father(mike, hannah).

father(todd, matt).
father(todd, mitch).

father(phil, jennifer).
father(phil, todd).

mother(jennifer, abigail).
mother(jennifer, hannah).

mother(janet, matt).
mother(janet, mitch).

parent(X, Y) :- father(X, Y).
parent(X, Y) :- mother(X, Y).

grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
siblings(X, Y) :- parent(Z, X), parent(Z, Y).			% why multiple answers?

altSiblings(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

cousin(X, Y) :- parent(A, X), parent(B, Y), altSiblings(A, B).
uncle(X, Z) :- male(X), altSiblings(X, Y), parent(Y, Z).

ancestor(X, X).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
%ancestor(X, Y) :- ancestor(Z, Y), parent(X, Z).		% problematic
