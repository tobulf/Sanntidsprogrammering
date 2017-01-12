// Go 1.2
// go run helloworld_go.go

package main

import (
	"runtime"
	"time"
)

var i int = 0

func Goroutine_1() {
	for n := 0; n < 1000000; n++ {
		i++
	}
}

func Goroutine_2() {
	for n := 0; n < 1000000; n++ {
		i--
	}

}

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU()) // I guess this is a hint to what GOMAXPROCS does...
	// Try doing the exercise both with and without it!
	go Goroutine_1() // This spawns someGoroutine() as a goroutine
	go Goroutine_2()
	// We have no way to wait for the completion of a goroutine (without additional syncronization of some sort)
	// We'll come back to using channels in Exercise 2. For now: Sleep.
	time.Sleep(100 * time.Millisecond)
	println(i)

}
