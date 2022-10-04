import numpy
import statistics
import matplotlib.pyplot as plt

# I wanted to find the perfect balance of an increment factor and a decrement factor whose random
# application over a large number of times wouldn't explode the value in either direction.
# code is pretty self-explanatory

for i in range(950, 1050):
    print(i)
    for j in range(950, 1050):
        up = numpy.divide(i, 1000)
        down = -numpy.divide(j, 1000)
        val = 10
        vals = []
        for k in range(10000):
            vals.append(round(val, 10))
            val = numpy.add(val, val * numpy.divide(numpy.random.choice([up, down]), 100))

        avg = numpy.average(vals)
        stdv = statistics.stdev(vals)
        if 9.7 < avg < 10.3 and stdv < 2:
            open("updowns.txt", "a").write(f"{up}, {down}, {avg}, {stdv}\n")
