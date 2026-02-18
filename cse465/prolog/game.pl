% game.pl
% Two player, turn-taking game on 1D board (i.e., a list).
% Spots are filled with x, o, or e (empty). Board starts out
% as [e, e, e, e, e, e, e]. Player alternate putting pieces
% in an unoccupied spot. The winner is the first to get 3
% consecutive.

won([PLAYER, PLAYER, PLAYER|T], PLAYER) :- !.
won([_|T], PLAYER) :- won(T, PLAYER), !.

makeMove([e|T], PLAYER, [PLAYER|T]).
makeMove([H|T], PLAYER, [H|REST]) :- makeMove(T, PLAYER, REST).

playGame(BRD, PLAYER, NEWBRD) :- makeMove(BRD, PLAYER, NEWBRD),
									won(NEWBRD, PLAYER), !.
playGame(BRD, PLAYER, NEWBRD) :- makeMove(BRD, PLAYER, NEWBRD), !.


% assumes opponent will play an immediate win. Assumes the
% game is not over.

playGame2(BRD, PLAYER, NEWBRD) :- makeMove(BRD, PLAYER, NEWBRD),
									won(NEWBRD, PLAYER), !.
playGame2(BRD, x, NEWBRD) :- makeMove(BRD, x, NEWBRD),
								playGame(NEWBRD, o, NEWBRD2),
								not(won(NEWBRD2, o)), !.
playGame2(BRD, o, NEWBRD) :- makeMove(BRD, o, NEWBRD),
								playGame(NEWBRD, x, NEWBRD2),
								not(won(NEWBRD2, x)), !.
playGame2(BRD, PLAYER, NEWBRD) :- makeMove(BRD, PLAYER, NEWBRD).