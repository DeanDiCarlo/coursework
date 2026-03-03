(define (mix lst1 lst2)
    (if (null? lst1)
        '() 
        (cons (+ (car lst1) (car lst2))(mix (cdr lst1) (cdr lst2)))))


; (define (mix lst1 lst2)
;   (if (null? lst1)
;       '()
;       (cons (+ (car lst1) (car lst2))(mix (cdr lst1) (cdr lst2)))))