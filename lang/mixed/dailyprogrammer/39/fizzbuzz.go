package main

import "flag"

type MyInt int

var n = flag.Int("maxnum", 20, "at which number should this programm stop?")

func (x MyInt) isDivisibleBy(y MyInt) bool {
	return x % y == 0
}

func main() {
	flag.Parse()
	var fizz, buzz, fizzbuzz MyInt = 3, 5, 15
	var i MyInt
	for i = 1; i <= MyInt(*n); i++ {
		switch {
		case i.isDivisibleBy(fizzbuzz):
			println("FIZZBUZZ")
		case i.isDivisibleBy(fizz):
			println("FIZZ")
		case i.isDivisibleBy(buzz):
			println("BUZZ")
		default:
			println(i)
		}
	}
}
