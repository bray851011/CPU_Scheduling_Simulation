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



def printBurstTimes(CPUBurstTimes, IOBurstTimes):

    numCPUBursts = len(CPUBurstTimes)
    for i in range(numCPUBursts):
        print(f"--> CPU burst {CPUBurstTimes[i]} ms", end="")
        if i < numCPUBursts - 1:
            print(f" --> I/O burst {IOBurstTimes[i]} ms")
        else:
            print()



if __name__ == "__main__":

    # argv[1], numProcesses -- the number of processes to stimulate
    # argv[2], seed -- the seed for random number generator
    # argv[3], lambda -- exponential distribution to determine interarrival time
    # argv[4], expDstUpperBound -- upper bound for the exponential distribution
    # argv[5], contextSwitchTime -- time to perform a context switch
    # argv[6], alpha -- constant for SJF and SRT algorithms
    # argv[7], timeSlice -- time slice for RR algorithm

    try:
        numProcesses = int(sys.argv[1])
        seed = int(sys.argv[2])
        lam = float(sys.argv[3])
        expDstUpperBound = int(sys.argv[4])
        contextSwitchTime = int(sys.argv[5])
        alpha = float(sys.argv[6])
        timeSlice = int(sys.argv[7])
    except ValueError:
        print("ERROR: There was a type error!")
        exit()

    TAU = int(1 / lam)

    rand = Rand48()
    rand.srand48(seed)
    threadsList = []

    for i in range(numProcesses):
        CPUBurstTimes = []
        IOBurstTimes = []

        # Get arrival time
        while True:
            arrivalTime = math.floor(-math.log(rand.drand48()) / lam)
            if arrivalTime <= expDstUpperBound:
                break

        # Get number of CPU bursts
        while True:
            numCPUBursts = math.ceil(rand.drand48() * 100)
            if numCPUBursts <= expDstUpperBound:
                break
        
        while len(CPUBurstTimes) < numCPUBursts:

            # CPU burst time
            while True:
                CPUBurstTime = math.ceil(-math.log(rand.drand48()) / lam)
                if CPUBurstTime <= expDstUpperBound:
                    break
            CPUBurstTimes.append(CPUBurstTime)

            # If this is the last CPU burst, don't make an I/O burst
            if len(CPUBurstTimes) == numCPUBursts:
                break
            else:
                # I/O burst time
                while True:
                    IOBurstTime = math.ceil(-math.log(rand.drand48()) / lam)
                    if IOBurstTime <= expDstUpperBound:
                        break
                IOBurstTimes.append(10 * IOBurstTime)

        # gather info for the thread
        threadName = str(chr(i + 65))

        # construct thread object
        threadsList.append(Thread(threadName, arrivalTime, numCPUBursts,
                                  CPUBurstTimes, IOBurstTimes, TAU))

        print(f'Process {threadName} (arrival time {arrivalTime} ms) '
                  f'{numCPUBursts} CPU burst{"s" if numCPUBursts > 1 else ""} '
                  f'(tau {int(1 / lam)}ms)')
        printBurstTimes(CPUBurstTimes, IOBurstTimes)
    
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
