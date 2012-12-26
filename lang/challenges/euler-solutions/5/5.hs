isDivisibleByAll :: (Integral a) => a -> [a] -> Bool
isDivisibleByAll i [] = True
isDivisibleByAll i (x:xs) = i `mod` x == 0 && isDivisibleByAll i xs

accumulator :: (Integral a) => a -> [a] -> a
accumulator acc numbers
    | acc `isDivisibleByAll` numbers = acc
    | otherwise = accumulator (succ acc) numbers


smallestMultiple :: (Integral a) => [a] -> a
smallestMultiple = accumulator 1

main = print $ smallestMultiple [1..20]
