import sys
import math
import copy

from FirstComeFirstServe import FCFS
from RoundRobin import RR
from ShortestJobFirst import SJF
from ShortestRemainingTime import SRT

class Rand48(object):
    
    def drand48(self):
        self.Xn = (0x5deece66d * self.Xn + 0xb) % (2 ** 48)
        return self.Xn / (2 ** 48)

    def srand48(self, seedval):
        self.Xn = (seedval << 16) + 0x330E



class Thread:
    
    def __init__(self, threadName, arrivalTime, CPUBursts, CPUBurstTime, IOBurstTime, tau):
        self.threadName = threadName
        self.arrivalTime = arrivalTime
        self.CPUBursts = CPUBursts
        self.CPUBurstTime = CPUBurstTime
        self.IOBurstTime = IOBurstTime
        self.tau = tau

    def set(self, CPUBursts, CPUBurstTime, IOBurstTime, tau):
        self.CPUBursts = CPUBursts
        self.CPUBurstTime = CPUBurstTime
        self.IOBurstTime = IOBurstTime
        self.tau = tau

    def get(self):
        return self.threadName, self.arrivalTime, self.CPUBursts, self.CPUBurstTime, self.IOBurstTime, self.tau



def next_exp():
    pass

if __name__ == "__main__":

    # argv[1], numProcesses -- the number of processes to stimulate
    # argv[2], seed -- the seed for random number generator
    # argv[3], lambda -- exponential distribution to determine interarrival time
    # argv[4], expDstUpperBound -- upper bound for the exponential distribution
    # argv[5], contextSwitchTime -- time to perform a context switch
    # argv[6], alpha -- constant for SJF and SRT algorithms
    # argv[7], timeSlice -- time slice for RR algorithm

    # if there is a type error, throw Value Error
    try:
        numProcesses = int(sys.argv[1])
        seed = int(sys.argv[2])
        lam = float(sys.argv[3])
        expDstUpperBound = int(sys.argv[4])
        contextSwitchTime = int(sys.argv[5])
        alpha = float(sys.argv[6])
        timeSlice = int(sys.argv[7])
    except ValueError:
        print("There was a type error!")
        exit()

    TAU = int(1 / lam)

    rand = Rand48()
    rand.srand48(seed)
    threadsList = []

    for i in range(numProcesses):
        randList = []

        # flag -- track the total valid random number we expect
        flag = 2
        while len(randList) < flag:

            r = rand.drand48()

            # arrival time
            if len(randList) == 0:
                r = math.floor(-math.log(r) / lam)

                if r > expDstUpperBound:
                    continue

            # number of CPU bursts
            elif len(randList) == 1:
                r = math.ceil(r * 100)
                if r > expDstUpperBound:
                    continue
                else:
                    flag = 2 + r

            # CPU burst time and I/O burst time
            else:
                # CPU burst time
                r1 = math.ceil(-math.log(r) / lam)
                if r1 > expDstUpperBound:
                    continue

                # This is the last CPU burst, so we do not generate I/O burst time
                if len(randList) == flag - 1:
                    r = r1
                else:
                    # I/O burst time
                    while True:
                        r = rand.drand48()
                        r2 = math.ceil(-math.log(r) / lam)
                        if r2 <= expDstUpperBound:
                            break
                    r = r1, 10 * r2

            randList.append(r)

        # gather info for the thread
        threadName = str(chr(i + 65))
        arrivalTime = randList[0]
        CPUBursts = randList[1]
        CPUBurstTime = [item[0] for item in randList[2:-1]] + [randList[-1]]
        print("CPU Burst Time: ", CPUBurstTime)
        IOBurstTime = [item[1] for item in randList[2:-1]]

        # construct thread object
        threadsList.append(Thread(threadName, arrivalTime, CPUBursts,
                                  CPUBurstTime, IOBurstTime, TAU))

        if CPUBursts > 1:
            print(f'Process {threadName} (arrival time {arrivalTime} ms) '
                  f'{CPUBursts} CPU bursts (tau {int(1 / lam)}ms)')
        else:
            print(f'Process {threadName} (arrival time {arrivalTime} ms) '
                  f'{CPUBursts} CPU burst (tau {int(1 / lam)}ms)')
    print()

    output = open("simout.txt", "a+")
    output.truncate(0)

    FCFS(copy.deepcopy(threadsList), output)
    print()
    SJF(copy.deepcopy(threadsList), output, alpha)
    print()
    SRT(copy.deepcopy(threadsList), output, alpha)
    print()
    RR(copy.deepcopy(threadsList), output, timeSlice)
