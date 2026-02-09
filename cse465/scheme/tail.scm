(load "zipcodes.scm")

(define (lengthTailRecursionHelper lst currLen)
	(if (NULL? lst) currLen (lengthTailRecursionHelper (cdr lst) (+ 1 currLen)))
)

(define (lengthTailRecursion lst)
	(lengthTailRecursionHelper lst 0)
)

(define (lengthNoTailRecursion lst)
	(if (NULL? lst) 0 (+ 1 (lengthNoTailRecursion (cdr lst))))
)

(display (lengthTailRecursion zipcodes))
(newline)
(display (lengthNoTailRecursion zipcodes))
(newline)
