; Returns the roots of the quadratic formula, given
; ax^2+bx+c=0. Return only real roots. The list will
; have 0, 1, or 2 roots. The list of roots should be
; sorted in ascending order.
; a is guaranteed to be non-zero.
; Use the quadratic formula to solve this.
; (quadratic 1.0 0.0 0.0) --> (0.0)
; (quadratic 1.0 3.0 -4.0) --> (-4.0 1.0)

(define (quadratic a b c)
  (let ((discriminant (- (* b b) (* 4 a c))))
	(cond 
		((< discriminant 0) '())
		((= discriminant 0) (list (/ (- 0 b) (* 2 a))))
		(else (let ((root1 (/ (+ (- 0 b) (sqrt discriminant)) (* 2 a)))
						(root2 (/ (- (- 0 b) (sqrt discriminant)) (* 2 a))))
						(if (<= root1 root2) (list root1 root2) (list root2 root1))))
	)
  )
)

; Ensures that a numeric value stays within a specified range. Values
; that are are within [lowest, highest] are kept. Values that are less
; than the lowest value are clamped to the lowest value. Values that
; exceed the highest value are clamped back to the highest possible.
; value.
; (clamp 0.5 0.0 1.0) --> 0.5
; (clamp -0.5 0.0 1.0) --> 0.0
; (clamp 1.5 0.0 1.0) --> 1.0
(define (clamp value lowest highest)
	(cond
		((< value lowest) lowest)
		((> value highest) highest)
		(else value)
	)
)

; Returns the fewest number of minutes between two times, where
; the two times are given in 24 hour format. For example, 12:05
; and 13:03 are separated by 58 minutes.
; (minutesBetween 12 5 13 3) --> 58
; (minutesBetween 13 3 12 5) --> 58
; (minutesBetween 0 0 23 59) --> 1
; (minutesBetween 23 59 0 0) --> 1
(define (minutesBetween h1 m1 h2 m2)
	(let ((mins1 (+ (* h1 60) m1))
	       (mins2 (+ (* h2 60) m2)))
	    (let ((diff (abs (- mins1 mins2))))
			(if (> diff 720)(- 1440 diff) diff)))
)

; Returns a list of two numeric values. The first is the smallest
; in the list and the second is the largest in the list.
; lst -- a flat list of numbers, with length >= 1.
;(minAndMax '(1 2 3 -9 20 5)) -> (-9 20)
(define (minAndMax lst)
	(minAndMaxHelper (cdr lst) (car lst) (car lst))	
)

(define (minAndMaxHelper lst currentMin currentMax)
	(if (null? lst)
		(list currentMin currentMax)
		(let ((head (car lst))
			(tail (cdr lst)))
			(minAndMaxHelper tail (if (< head currentMin) head currentMin)
								(if (> head currentMax) head currentMax))
		)
	)	
)

; Returns true iff the parameters is a flat list of numbers.
; (isFlatListOfNumbers '(1 2 3)) --> #t
; (isFlatListOfNumbers '(1 (2) 3)) --> #f
(define (isFlatListOfNumbers lst)
	(if (null? lst)
		#t
		(let ((head (car lst))
			(tail (cdr lst)))
			(if (number? head)		
				(isFlatListOfNumbers tail)
				#f)
		)
	)	
)

; Accepts a list of items and returns the list with the top-level
; items in reversed order. Do not use the Scheme function reverse
; (rev '(a b c d)) --> (d c b a)
; (rev '()) --> ()
(define (rev lst)
	(if (null? lst)
		'()
		(let ((head (car lst))
			(tail (cdr lst)))
			(append (rev tail) (list head))
		)
	)
)


; Returns a list containing the latitude and longitude of
; particular location. The location is specified by zipcode.
; If there is more than one match, give the first match. Return
; the empty list if the location does not exist.
(define (getLatLon zipCode places)
	(if (null? places)
		'()
		(let ((head (car places))
			(tail (cdr places)))
			(if (equal? (car head) zipCode)
				(list (car (cddddr head)) (cadr (cddddr head)))
				(getLatLon zipCode tail)
			)
		)
	)	
)

; The paramters are two lists. The result should contain the cross product
; between the two lists. That is, all elements of the first list are paired
; with all elements of the second lists. All of these pairs are put into a
; list of pairs. The order of the pairing is illustrated in the example.
; lst1 & lst2 -- two flat lists.
; (crossProduct '(1 2) '(a b c)) --> ((1 a) (1 b) (1 c) (2 a) (2 b) (2 c))
(define (crossProduct lst1 lst2)
	(if (null? lst1)
		'()
		(append (pairWithAll (car lst1) lst2) (crossProduct (cdr lst1) lst2))
	)
)

(define (pairWithAll num lst)
	(if (null? lst)
		'()
		(let ((head (car lst))
			(tail (cdr lst)))
			(cons (list num head) (pairWithAll num tail))
		)
	)
)

; Returns the list containing only the negative numbers from
; an input list. The order of the numbers will appear in the
; same order as the input list.
; This must be done using tail recursion.
;(negatives '(-1 2 3 -9 -20 5)) -> (-1 -9 -20)
(define (negatives lst)
	(negativesHelper lst '())
)

(define (negativesHelper lst result)
	(cond
		((null? lst) result)
		((< (car lst) 0) (negativesHelper (cdr lst) (append result (list (car lst)))))
		(else (negativesHelper (cdr lst) result))
	)
)

; Returns a list of items that satisfy a predicates.
; lst -- list of items
; theFilter -- predicates to apply to the individual elements
; (simpleFilter '(1 2 3 4 100) EVEN?) --> (2 4 100)
(define (filter lst theFilter)
	(if (null? lst)
		'()
		(let ((head (car lst))
			(tail (cdr lst)))
			(if (theFilter head) (cons head (filter tail theFilter)) (filter tail theFilter))
		)
	)
)

; I'm going to try the BST one 
; It looks like it still has points on the intro document
; We shall see how it goes
; I guess it's just a list here but not sure.
; I think I got it here, the head element will be the cadr of the first list
; There are 3 items thus the cadr is the middle one or the head, then recurse with the BST

(define (BSTContainsValue tree value)
	(if (null? tree)
		#f
		(let ((left (car tree))
			(head (cadr tree))
			(right (caddr tree)))
			(cond
				((= head value) #t)
				((< value head) (BSTContainsValue left value))
				(else (BSTContainsValue right value))
			)
		)
	)
)