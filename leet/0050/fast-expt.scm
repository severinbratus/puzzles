(define (print a)
    (display a)
    (newline))

(define (expt-iter acc b count)
    (print acc)
    (print count)
    (newline)
    (cond
        ((= count 0) acc)
        ((even? count)
            (expt-iter acc (* b b) (/ count 2)))
        (else
            (expt-iter (* b acc) b (- count 1)))))

(define (fast-expt b n)
    (expt-iter 1 b n))
