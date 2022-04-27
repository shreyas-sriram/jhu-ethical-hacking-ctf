// mjolnir

package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Wrong usage")
		os.Exit(0)
	}

	file := os.Args[1]
	character := os.Args[2]

	bytes, err := os.ReadFile(file)
	if err != nil {
		fmt.Println("Error reading file")
		os.Exit(0)
	}

	fmt.Println(strings.Count(string(bytes), character))
}
