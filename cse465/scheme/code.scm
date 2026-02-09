(define random (make-random 1234))
(define (randint n) (modulo (random) n))
;****************************************************
(newline)
(display "BASIC EVAL")

(define f (list '+ 2 3))
(define g (list '* '(- 1 3) '(+ 3 4)))

(newline)
(display f)   ; (+ 2 3)
(newline)
(display (eval f (interaction-environment)))   ; 5
(newline)
(display g)   ; (* (- 1 3) (+ 3 4)))
(newline)
(display (eval g (interaction-environment)))   ; -14
(newline)

;****************************************************
(newline)
(display "LAMBDA")
(newline)

(display ((lambda (x y) (* x y)) 4 5))	; 20
(NEWLINE)

(define (createLambdaExpr)
;;	(list 'lambda '(x y) '(+ (* x y) 100))
	'(lambda (x y) (+ (* x y) 100))
)

(define g (createLambdaExpr))
(define h (eval g (interaction-environment)))

(display g)     ; (lambda (x y) (+ (* x y) 100)
(NEWLINE)
(display h)     ; # compound procedure
(NEWLINE)
(display (apply h '(2 3)))   ; 106
(NEWLINE)
(display (h 2 3))	; 106
(NEWLINE)


(display "Random expressions")
(newline)

(define (randop)
	(define x (randint 3))
	(COND
		((= x 0) '+)
		((= x 1) '*)
		((= x 2) '-)
	)
)

(define (randexpr N)
	(COND
		((= N 1) (randint 10))
		(else (list (randop) (randexpr (- N 1)) (randexpr (- N 1))))
	)
)

(define f1 (randexpr 3))
(define f2 (randexpr 3))
(define f3 (randexpr 3))
(define f4 (randexpr 3))

(display f1)
(newline)
(display (eval f1 (interaction-environment)))
(newline)
(display f2)
(newline)
(display (eval f2 (interaction-environment)))
(newline)
(display f3)
(newline)
(display (eval f3 (interaction-environment)))
(newline)
(display f4)
(newline)
(display (eval f4 (interaction-environment)))
(newline)
(newline)
(display "Functional forms")
(newline)

(define (mymap F lst)
	(COND
		((= 0 (length lst)) '())
		(else (cons (F (car lst)) (mymap F (cdr lst))))
	)
)

(display (mymap (lambda (x) (cos x)) '(1 2 3)))  ; (.54 -.41 -.99)
(newline)

#t