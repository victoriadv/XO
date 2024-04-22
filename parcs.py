from Pyro4 import expose
import random


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        n = self.read_input()

        # map

        a = []
        for i in range(n):
            a.append(random.randint(1, 100000))

        out = self.chunk(a, len(self.workers))

        mapped = []
        for i in xrange(0, len(self.workers)):
            mapped.append(self.workers[i].insertion(out[i]))

        # reduce
        reduced = self.myreduce(mapped)

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def insertion(array):
        for i in range(len(array)):
            j = i-1
            key = array[i]
            while array[j] > key and j >= 0:
                array[j+1] = array[j]
                j -= 1
            array[j+1] = key
        return array

    @staticmethod
    @expose
    def myreduce(mapped):
        result = []
        indexes = []
        for arr in mapped:
            result.append(arr.value)
            indexes.append(0)
        first = result[0]
        for i in xrange(1, len(result)):
            second = result[i]
            third = []
            x = 0
            y = 0
            while x < len(first) and y < len(second):
                if first[x] <= second[y]:
                    third.append(first[x])
                    x += 1
                else:
                    third.append(second[y])
                    y += 1
            while x<len(first):
                third.append(first[x])
                x += 1
            while y < len(second):
                third.append(second[y])
                y +=1
            first = third
        return first

    def chunk(self, a, n):
        avg = len(a) / float(n)
        out = []
        last = 0.0
        while last < len(a):
            out.append(a[int(last):int(last + avg)])
            last += avg
        return out

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()