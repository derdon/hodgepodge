digitSum :: (Integral a) => a -> a
digitSum 0 = 0
digitSum x = digit + (digitSum rest)
    where (rest, digit) = x `divMod` 10

main = print $ digitSum $ 2 ^ 1000
