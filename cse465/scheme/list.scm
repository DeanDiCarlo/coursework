;;; predicates: LIST? NULL? EQ? EQUAL?
;;; quote
;;; car cdr caddr
;;; cons list append
;;; mylength

(define random (make-random 1234))
(define (randint n) (modulo (random) n))

(newline)
(display (cons 0 '(1 2 3)))
(newline)
(display (cons '(a b) '(1 2 3)))
(newline)
(display (cons (+ 10 20) '(1 2 3)))
(newline)
(display (list '(a) '(b c d)))
(newline)
(display (append '(a) '(b c d)))
(newline)
(display (cdadr '((1 2) (3 4) (5 6))))
(newline)
(display (list (+ 2 3) 0))
(newline)
(display (list '(+ 2 3) 0))
(newline)
(display (cons (car '(1 2 3)) (list 'a 'b 'c)))
(newline)
(display (append '(1 2 3) (list 'a 'b 'c)))
(newline)

(define (mylength lst)
	(COND
		((NULL? lst) 0)
		((LIST? lst) (+ 1 (mylength (CDR lst))))
		(ELSE 0)
	)
)

(define (maxelt lst)
	(if (= (mylength lst) 1) (CAR lst) (max (CAR lst) (maxelt (CDR lst))))
)

(define (minelt lst)
	(if (= (mylength lst) 1) (CAR lst) (min (CAR lst) (minelt (CDR lst))))
)

(define (numZeros lst)
;;; FILL THIS in
;;; Returns the number of 0's that appear in a flat
;;; list of integers
	0
)

(define (randlist len)
	(if (= len 0)
		'()
		(cons (randint 100) 
			  (randlist (- len 1))
		)
	)
)

(define (allbutlast lst)
; fill this in. Returns the original list, but without the last element.
	0
)

(define (ismember atm lst)
	(cond
		((NULL? lst) #f)
		((EQUAL? atm (CAR lst)) #t)
		(ELSE (ismember atm (CDR lst)))
	)
)

(define (odds lst)
	(cond
		((NULL? lst) '())
		((ODD? (CAR lst)) (CONS (CAR lst) (odds (CDR lst))))
		(ELSE (odds (CDR lst)))
	)
)

(define (minAndMax lst)
;;; FILL THIS IN.
;;; Return the following list of two elements, where the 
;;; the first element is the minimum of the incoming list
;;; and the second element is the maximum of the list.
	'(0 0)
)

(define (zip lst1 lst2)
; Fill this in
; Input is two simple lists of same length: (1 2 3 4) (a b c d)
; returns ((1 a) (2 b) (3 c) (4 d))
	0
)

(define (remove v lst)
	(COND 
		((NULL? lst)
			'()
		)
		((= v (CAR lst))
			(CDR lst))
		(ELSE 
			(cons 
				(CAR lst) 
				(remove v (CDR lst))
			)
		)
	)
)

(define (sort lst)
	(if (NULL? lst)
		'()
		(cons (minelt lst) (sort (remove (minelt lst) lst)))
	)
)
