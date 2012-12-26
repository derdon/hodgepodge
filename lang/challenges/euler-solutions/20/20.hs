digitSum :: (Integral a) => a -> a
digitSum 0 = 0
digitSum x = digit + (digitSum rest)
    where (rest, digit) = x `divMod` 10

fac n = product [1..n]

main = print $ digitSum $ fac 100
