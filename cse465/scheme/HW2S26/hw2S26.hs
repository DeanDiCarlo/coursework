-- To run this code:
-- $ ghc -o exe hw2S26.hs
-- $ ./exe
-- Some examples from the textbook

fac 0 = 1
fac n = n * fac (n-1)
 
fib n
    | n == 1 = 1
    | n == 2 = 1
    | otherwise = fib(n-1) + fib(n-2)

len [] = 0
len (a:x) = 1 + len x


member b [] = False
member b (a:x)
   | a == b = True
   | otherwise = member b x

-- Your assignment requires you to complete the following functions:

-- Accepts a flat list of numbers, followed by two numbers defining a low and hi value.
-- The returned value is corresponds to the number of values in the list that are
-- <= low and < hi. For example,
-- numsInRange [1,2,3,4,1,2,3,4,5] 2 4
-- should return 4

numsInRange [] lo hi = 0

-- Accepts a flat list of numbers and returns a list of the positive values.
-- The values in the returned list will be in the same order as the original list.
-- positives [-3,0,3,9,3,-10,8]
-- should return [3,9,3,8]

positives [] = []

-- Accepts a flat list of numbers and returns the list with the values in the reverse
-- order. For example
-- rev [1,2,3,4,5,5]
-- should return [5,5,4,3,2,1]

rev [] = []


main = print (member 5 [1,2,3,4,5,5])
