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


class Process:
    
    def __init__(self, processName, arrivalTime, CPUBursts, CPUBurstTime, IOBurstTime, tau):
        self.processName = processName
        self.arrivalTime = arrivalTime
        self.CPUBursts = CPUBursts
        self.CPUBurstTime = CPUBurstTime
        self.IOBurstTime = IOBurstTime
        self.tau = tau

    def get(self):
        return self.processName, self.arrivalTime, self.CPUBursts, self.CPUBurstTime, self.IOBurstTime, self.tau

    def getName(self):
        return self.processName


    def getArrivalTime(self):
        return self.arrivalTime
    
    def getCPUBursts(self):
        return self.CPUBursts
    
    def getCPUBurstTime(self):
        return self.CPUBurstTime
    
    def getIOBurstTime(self):
        return self.IOBurstTime
    
    def getTau(self):
        return self.tau


def next_exp():

    rand = Rand48()
    rand.srand48(seed)

    for i in range(numProcesses):

        # name the process(A through Z)
        processName = str(chr(i + 65))

        # Get arrival time and number of CPU bursts
        arrivalTime = numCPUBursts = -1
        while True:
            if arrivalTime == -1 or arrivalTime > expDstUpperBound:
                arrivalTime = math.floor(-math.log(rand.drand48()) / lam)
            if numCPUBursts == -1 or numCPUBursts > expDstUpperBound:
                numCPUBursts = math.ceil(rand.drand48() * 100)
            if arrivalTime <= expDstUpperBound and numCPUBursts <= expDstUpperBound:
                break

        # Get CPU burst time and I/O burst time
        CPUBurstTimes = []
        IOBurstTimes = []
        while len(CPUBurstTimes) < numCPUBursts:

            # CPU burst time and I/O burst time
            CPUBurstTime = IOBurstTime = -1
            while True:
                if CPUBurstTime == -1 or CPUBurstTime > expDstUpperBound:
                    CPUBurstTime = math.ceil(-math.log(rand.drand48()) / lam)
                if IOBurstTime == - 1 or IOBurstTime > expDstUpperBound:
                    IOBurstTime = math.ceil(-math.log(rand.drand48()) / lam)
                if CPUBurstTime <= expDstUpperBound and IOBurstTime <= expDstUpperBound:
                    CPUBurstTimes.append(CPUBurstTime)
                    if len(CPUBurstTimes) != numCPUBursts:
                        IOBurstTimes.append(10 * IOBurstTime)
                    break

        # construct thread object
        processesList = []
        processesList.append(Process(processName, arrivalTime, numCPUBursts, CPUBurstTimes, IOBurstTimes, int(1 / lam)))

        print(f'Process {processName} (arrival time {arrivalTime} ms) '
              f'{numCPUBursts} CPU burst{"s" if numCPUBursts > 1 else ""} '
              f'(tau {int(1 / lam)}ms)')

        printBurstTimes(CPUBurstTimes, IOBurstTimes)

    return processesList


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

    processesList = next_exp()

    print()

    output = open("simout.txt", "a+")
    output.truncate(0)

    FCFS(copy.deepcopy(processesList), output)
    print()
    SJF(copy.deepcopy(processesList), output, alpha)
    print()
    SRT(copy.deepcopy(processesList), output, alpha)
    print()
    RR(copy.deepcopy(processesList), output, timeSlice)

