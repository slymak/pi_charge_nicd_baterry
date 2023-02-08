#!/usr/bin/python3
number_cycle = 5
cycle = 1
while  cycle < number_cycle:
	if (cycle % 2 ) == 0:
		bate = "down"
	else:
		bate = "top"

	print(f" cycle {cycle} baterka {bate}")
	cycle += 1
