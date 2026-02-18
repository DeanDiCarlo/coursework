% list.pl

ok([]).

ok([_|T]) :- \+ ok(T).
%ok([_|T]) :- T = [_|Y], ok(Y).

contains0([H | _]) :- H = 0.
contains0([_ | T]) :- contains0(T).

myreverse([], []).
myreverse([H | T], L) :- myreverse(T, R), append(R, [H], L).

app([], L, L).
app([H | L1], L2, [H | L3]) :- app(L1, L2, L3).

