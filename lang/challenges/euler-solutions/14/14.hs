import Data.List
import Data.Ord

collatzSequence :: (Integral a) => a -> [a]
collatzSequence 1 = [1]
collatzSequence n
    | even n = n : collatzSequence (n `div` 2)
    | otherwise = n : collatzSequence (3 * n + 1)

main =
    let input = [500001,500003..999999]
    in print $ head $ maximumBy (comparing length) $ map collatzSequence input
