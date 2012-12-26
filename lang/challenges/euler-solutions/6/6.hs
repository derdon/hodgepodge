sumOfSquares :: (Fractional a) => a -> a
sumOfSquares n = (n * (n + 1) * (2 * n + 1)) / 6

squareOfSum :: (Fractional a) => a -> a
squareOfSum n = ((n * (n + 1)) / 2) ^ 2

squareOfSumMinusSumOfSquares :: (Fractional a) => a -> a
squareOfSumMinusSumOfSquares n = (squareOfSum n) - (sumOfSquares n)

main = print $ squareOfSumMinusSumOfSquares 100
