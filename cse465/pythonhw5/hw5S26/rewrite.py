from math import *

# Replace the given loop with another loop that
# does not use break or continue
def loop1(N):
	total = 0.0
	for i in range(N):
		if i % 2 != 0:
			total = cos(i)
	return total

# Replace the given loop with another loop that
# does not use break or continue
def loop2(N):
	total = 0.0
	for i in range(min(N, 7)):
		total = cos(i)
	return total

# Replace the given loop with another loop that
# does not use break or continue
def loop3(N, F):
	total = 0.0
	i = 0
	while i < N and not F(i):
		total = i
		i += 1
	return total

# Replace the following code with one that does not
# use the ternary operator (i.e., conditional expression)
def expression(N):
	if N >= 0:
		return N
	return -1


print(loop1(5))
print(loop2(5))
print(loop3(10, lambda x : x >= 5))
print(expression(5))
