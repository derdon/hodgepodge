import System.Environment

divisibleBy :: (Integral a) => a -> a -> Bool
divisibleBy a b = a `mod` b == 0

fizzbuzz :: (Integral a, Show a) => a -> String
fizzbuzz n
    | n `divisibleBy` 15 = "FIZZBUZZ"
    | n `divisibleBy` 3 = "FIZZ"
    | n `divisibleBy` 5 = "BUZZ"
    | otherwise = show n

main = do
    (n:_) <- getArgs
    putStr $ unlines $ map fizzbuzz [1..read n]
