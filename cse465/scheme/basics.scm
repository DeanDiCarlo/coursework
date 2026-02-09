; basics.scm
; From within Scheme interpreter: (load "basics.scm")

(define COST 10)

(define (sqr x) (* x x))

(define (hyp s1 s2) 
	(sqrt (+ (sqr s1) (sqr s2)))
)

(define (logbase x base)
	(/ (log x) (log base))
)

(define (distance x1 y1 x2 y2)
 	(sqrt (+ (sqr (- x2 x1)) (sqr (- y2 y1))))
)

(define (mymax a b)
	(if (> a b) a b)
)

(define (isSmall x)
	(if (< (abs x) 1) #t #f)
)

(define (fib n)
	(cond
		((= n 1) 1)
		((= n 2) 1)
		(else (+ (fib (- n 1)) (fib (- n 2))))
	)
)

(define (isInQuadrant1 x y)
	(and (if (> x 0) #t #f) (if (> y 0) #t #f))	
)

(define (quadrant x y)
;;; Returns 1, 2, 3, 4 depending on which quadrant (x, y) is located in.
	(cond 
	  ((and (> x 0) (> y 0)) 1)
	  ((and (< x 0) (> y 0)) 2)
	  ((and (< x 0) (< y 0)) 3)
	  ((and (> x 0) (< y 0)) 4)
	  (else -1))
;;; Returns -1 if (x, y) lies on an axis
)

(define (computeGrossPay hours rate)
;;; Hours over 40 are given time and half. Hours over 60 are given double time.
	(cond
;	  ((if (> (hours 60)) (+ (* (40 rate)) (* (20 (* (rate 1.5)))) (* (- (hours 60)) (* (2 rate))))))
;	  ((if (> (hours 40)) (+ (* (40 rate)) (* (- (hours 40)) (* (1.5 rate))))))
;	  (else (* (hours rate))))
	  ((<= hours 40) (* hours rate))
	  ((<= hours 60) (+ (* 40 rate) (* rate 1.5 (- hours 40))))
	  (else (+ (* 40 rate) (* 20 1.5 rate) (* rate 2.0 (- hours 60))))
)
