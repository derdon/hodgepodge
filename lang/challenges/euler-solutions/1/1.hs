-- (c) Florian Mayer <flormayer@aim.com> under the ISC license.
-- See COPYING for more details.

dividesany ns x = any (\y -> rem x y == 0) ns
main = print (sum (filter (dividesany [3, 5]) [1..999]))
