(define N 10)
(define TWO_N (* N 2))

(define (hyp a b)
	(define A2 (* a a))
	(define B2 (* b b))
	(sqrt (+ A2 B2)) 
)

(define (g a)
	(define A2 (* 2 a))
	(display A2)
	#t
)

(define (f a level)
	(define A2 (* 2 a))
	(display (list A2 "start level:" level))
	(newline)
	(if (= level 0) 0 (f (+ a 1) (- level 1)))
	(display (list A2 "end level:" level))
	(newline)
	#t
)

(define (hyp2 a b)
	(let ((A2 (* a a))
		 (B2 (* b b)))
		 (sqrt (+ A2 B2)) 
	)
)

(display "HYP" )
(newline)
(display (hyp 3 4))
(newline)

(display "G")
(newline)
(display (g 3))
(newline)

(display "F")
(newline)
(display (f 4 3))
(newline)

(display "HYP2")
(newline)
(display (hyp2 3 4))

(newline)
#t