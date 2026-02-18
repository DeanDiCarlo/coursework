% parse.pl

noun([sun]).
noun([children]).

verb([shines]).
verb([illuminates]).

article([the]).
article([a]).

adjective([big]).
adjective([yellow]).

adverb([brightly]).

sentence(S) :- append(NP, VP, S), np(NP), vp(VP).

np([ART|NP]) :- article([ART]), np2(NP).
np(NP) :- np2(NP).

np2(NP2) :- noun(NP2).
np2([ADJ|NP2]) :- adjective([ADJ]), np2(NP2).

vp(VP) :- verb(VP).
vp([VERB|ADV]) :- verb([VERB]), adverb(ADV).

