import math


# solve x^(x^(x^(x^...)))) = N


N=3

SOLUTION = math.pow(N, 1.0/N)
# SOLUTION = math.sqrt(math.e)

print SOLUTION
print SOLUTION**2



def iter(number_of_iterations) :
    acc = 1.0
    for i in range (number_of_iterations):
        acc = math.pow(SOLUTION, acc)
    print number_of_iterations, acc


for i in range(1,10) :
    iter(i)

for i in range(1,10) :
    iter(10*i)

for i in range(1,10) :
    iter(100*i)

for i in range(1,10) :
    iter(1000*i)

#iter(1000)
