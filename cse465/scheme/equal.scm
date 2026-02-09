(define A "xyz")
(define B "xyz")
(define L (cons 1 2))

;;; = for comparing numbers
(newline)
(display "=")
(newline)
(display (= 4 4))         ; #t
(newline)
(display (= 3 4))         ; #f
(newline)
(display (= 7 (+ 3 4)))   ; #t
(newline)
;(display (= "abc" "abc"))  ; error

;;; EQ Checks for pointer equality
(display "EQ?")
(newline)
(display (EQ? A A))      ; #t
(newline)
(display (EQ? A B))      ; #f
(newline)
(display (EQ? '(1 2 3) '(1 2 3))) ; #t
(newline)
(display (EQ? (car '(1 2 3)) 1)) ; #t
(newline)
(display (EQ? 3.4 (+ 3 0.4))) ; #f
(newline)
(display (= 3.4 (+ 3 0.4))) ; #t
(newline)

;;; EQV value comparison of atoms
(display "EQV?")
(newline)
(display (EQV? 0 0)) ; #t
(newline)
(display (EQV? 3.4 3.4)) ; #t
(newline)
(display (EQV? 3.4 (+ 3 0.4))) ; #t
(newline)
(display (EQV? 3 3.0)) ; #f
(newline)
(display (EQV? A A))		; #t
(newline)
(display (EQV? A B))		; #f
(newline)
(display (EQV? (cons 1 2) (cons 1 2)))		; #f
(newline)
(display (EQV? L L))		; #t
(newline)

;;; EQUAL deep, logical, comparison

(display "EQUAL?")
(newline)
(display (EQUAL? "abc" "abc"))      ; #t
(newline)
(display (EQUAL? (car '(1 2 3)) 1)) ; #t
(newline)
(display (EQUAL? L (cons 1 2))) ; #t
(newline)
(display (EQUAL? A A))		; #t
(newline)
(display (EQUAL? A B))		; #t
(newline)

