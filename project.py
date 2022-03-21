import sys
import math
import copy

from FirstComeFirstServe import FCFS
from RoundRobin import RR
from ShortestJobFirst import SJF
from ShortestRemainingTime import SRT

class Rand48(object):

    def drand48(self):
        self.Xn = (0x5deece66d * self.Xn + 0xb) % pow(2, 48)
        return self.Xn / pow(2, 48)

    def srand48(self, seed):
        self.Xn = (seed << 16) + 0x330e


class Process:

    def __init__(self, processName, arrivalTime, CPUBursts, CPUBurstTimes, IOBurstTimes, tau):
        self.processName = processName
        self.arrivalTime = arrivalTime
        self.CPUBursts = CPUBursts
        self.CPUBurstTimes = CPUBurstTimes
        self.IOBurstTimes = IOBurstTimes
        self.tau = tau
        self.tempTau = tau

    def getName(self):
        return self.processName

    def getArrivalTime(self):
        return self.arrivalTime

    def getNumCPUBursts(self):
        return self.CPUBursts

    def getCPUBurstTimes(self):
        return self.CPUBurstTimes

    def getCurrCPUBurst(self):
        return self.CPUBurstTimes[0]

    def popCurrCPUBurst(self):
        self.CPUBursts -= 1
        return self.CPUBurstTimes.pop(0)

    def getIOBurstTimes(self):
        return self.IOBurstTimes

    def getCurrIOBurst(self):
        return self.IOBurstTimes[0]

    def popCurrIOBurst(self):
        return self.IOBurstTimes.pop(0)

    def getTau(self):
        return self.tau
    
    def getTempTau(self):
        return self.tempTau
    
    def decreaseTempTau(self, val):
        try:
            self.tempTau -= val
        except:
            self.tempTau = float("-inf")

    def setTau(self, tau):
        self.tau = tau
        self.tempTau = tau


def next_exp():
    return -math.log(rand.drand48())


def printBurstTimes(CPUBurstTimes, IOBurstTimes):
    numCPUBursts = len(CPUBurstTimes)
    for i in range(numCPUBursts):
        print(f"--> CPU burst {CPUBurstTimes[i]} ms", end="")
        if i < numCPUBursts - 1:
            print(f" --> I/O burst {IOBurstTimes[i]} ms")
        else:
            print()


if __name__ == "__main__":

    try:
        numProcesses = int(sys.argv[1])
        seed = int(sys.argv[2])
        lam = float(sys.argv[3])    # For interarrival time
        expDstUpperBound = int(sys.argv[4])
        contextSwitchTime = int(sys.argv[5])
        alpha = float(sys.argv[6])
        timeSlice = int(sys.argv[7])
    except:
        print("ERROR: There was a type error!")
        exit()

    TAU = int(1 / lam)

    rand = Rand48()
    rand.srand48(seed)
    processList = []

    for i in range(numProcesses):
        CPUBurstTimes = []
        IOBurstTimes = []

        # Get arrival time
        while True:
            arrivalTime = math.floor(next_exp() / lam)
            if arrivalTime <= expDstUpperBound:
                break

        # Get number of CPU bursts
        while True:
            numCPUBursts = math.ceil(rand.drand48() * 100)
            if numCPUBursts <= expDstUpperBound:
                break

        while len(CPUBurstTimes) < numCPUBursts:

            # Get CPU burst time
            while True:
                CPUBurstTime = math.ceil(next_exp() / lam)
                if CPUBurstTime <= expDstUpperBound:
                    break
            CPUBurstTimes.append(CPUBurstTime)

            # If this is the last CPU burst, don't get an I/O burst time
            if len(CPUBurstTimes) == numCPUBursts:
                break
            else:
                # Get I/O burst time
                while True:
                    IOBurstTime = math.ceil(next_exp() / lam)
                    if IOBurstTime <= expDstUpperBound:
                        break
                IOBurstTimes.append(10 * IOBurstTime)

        processName = str(chr(i + 65))
        processList.append(Process(processName, arrivalTime, numCPUBursts,
                                   CPUBurstTimes, IOBurstTimes, TAU))

        print(
            f'Process {processName} (arrival time {arrivalTime} ms) '
            f'{numCPUBursts} CPU burst{"s" if numCPUBursts > 1 else ""} '
            f'(tau {TAU}ms)')
        printBurstTimes(CPUBurstTimes, IOBurstTimes)

    print()

    output = open("simout.txt", "a+")
    output.truncate(0)

    FCFS(output, copy.deepcopy(processList), contextSwitchTime)

    SJF(output, copy.deepcopy(processList), alpha, contextSwitchTime)

    SRT(output, copy.deepcopy(processList), alpha, contextSwitchTime)

    RR(output, copy.deepcopy(processList), timeSlice, contextSwitchTime)

