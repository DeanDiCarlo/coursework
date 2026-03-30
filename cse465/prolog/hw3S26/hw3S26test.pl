/* Successes */
query(maxOfTwo(2, 3, 3)).

query(quadratic(4, 3, -1, Roots)).

query(isLargerCube(1, 2, 3, 1, 5, 1)).

query(clamp(-0.5, 0.0, 1.0, 0.0)).

query(isACity('Oxford', 'OH')).

query(getStateInfo('Oxford', 'OH', 45056)).

query(isConstantList([1, 1, 1])).

query(eo([1, 2, 3], L)).

query(positives([1, 2, 3], [1, 2, 3])).

query(greatGrandparent(ggm, self)).

query(kthDescendant(m, self, 1)).

query(nthCousinMTimesRemoved(self, c1, 1, 0)).

writeln(T) :- write(T), nl.

main :- consult(zipcodes), consult(hw3S26),
	forall(query(Q), (Q->writeln(yes:Q) ; writeln(no:Q))).
:- initialization(main).