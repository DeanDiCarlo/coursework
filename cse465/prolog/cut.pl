% cut.pl
% CUT !
% GOAL: a, b, !, c, d
% once a and b are satisfied, the satisfiability of the goal depends
% only on c and d. That is, the subgoals, a and b will not be reevaluated.
% Done for efficiency reasons.

member2(E, [E | _]).
member2(E, [_ | L]) :- member2(E, L).

member3(E, [E | _]) :- !.
member3(E, [_ | L]) :- member3(E, L).
