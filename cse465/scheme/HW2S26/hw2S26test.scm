(load "hw2S26.scm")
(load "zipcodes.scm")

(define (displayNL item)
	(display item)
	(newline)
)

(displayNL "quadratic")
(displayNL (quadratic 1.0 0.0 0.0))

(displayNL "clamp")
(displayNL (clamp 0.0 0.0 1.0))

(displayNL "minutesBetween")
(displayNL (minutesBetween 12 5 13 3))

(displayNL "minAndMax")
(displayNL (minAndMax '(1 2 -9 44 0)))

(displayNL "isFlatListOfNumbers")
(displayNL (isFlatListOfNumbers '(1 2 3)))

(displayNL "rev")
(displayNL (rev '(1 2 3)))

(displayNL "getLatLon")
(displayNL (getLatLon 45056 zipCodes))

(displayNL "crossProduct")
(displayNL (crossProduct '(a b) '(1 2 3)))

(displayNL "negatives")
(displayNL (negatives '(1 -2 -9 10)))

(displayNL "filter")
(displayNL (filter '(1 2 3 4 100 -1 -2 -3 -4 -100) EVEN?))