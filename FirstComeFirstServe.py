'''
The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
queue, waiting to use the CPU. This is your baseline algorithm (and could be implemented as RR
with an "infinite" time slice).
'''

import copy
from helpers import *

def FCFS(processList, f):

    algo = "FCFS"
    numContextSwitches = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0

    printStartSimulator(algo)

    arrivalTimeDict = {}
    processes = {}
    readyQueue = []
    for process in processList:
        arrivalTimeDict[process.getArrivalTime()] = process.getName()
        processes[process.getName()] = copy.deepcopy(process)

    time = 0
    usingCPU = False
    runningProcess = ''
    blockDict = {}

    while True:

        prevReadyQueue = readyQueue
        currentProcess = ''

        # If there are no processes left, then simulator is done
        if not processes:
            printEndSimulator(time + 1, algo)
            break

        # print changes to the process
        if usingCPU:
            if time == runningStart:
                burstTime = runningEnd - runningStart
                CPUBurstStart += burstTime
                useful_time += burstTime
                CPUBurstEnd += 1
                printStartCPU(time, runningProcess, -1, burstTime, readyQueue)

        if usingCPU:
            if time == runningEnd:
                currentProcess = runningProcess

                if len(processes[currentProcess].getCPUBurstTimes()) == 0:
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    printCPUComplete(time, currentProcess, -1, processes[currentProcess].getNumCPUBursts(), readyQueue)

                    blockTime = processes[currentProcess].popNextIOBurstTime() + 2

                    printIOBlock(time, currentProcess, time + blockTime, readyQueue)

                    blockDict[currentProcess] = time + blockTime, currentProcess

        if usingCPU:
            if time == runningEnd + 2:
                usingCPU = False

        doneProcesses = []
        for v in blockDict.values():

            # in case there are multiple processes ending at this time
            if time == v[0]:
                doneProcesses.append(v[1])

        doneProcesses.sort()
        readyQueue += doneProcesses
        for proc in doneProcesses:
            printIOComplete(time, proc, -1, readyQueue)

        # check if there is a process coming at this time
        if time in arrivalTimeDict.keys():
            readyQueue.append(arrivalTimeDict[time])
            printProcessArrived(time, arrivalTimeDict[time], -1, readyQueue)

        # no process is running and there is at least one ready process
        if not usingCPU and len(readyQueue):
            usingCPU = True
            nextProcess = readyQueue.pop(0)
            runningStart = time + 2
            runningEnd = time + processes[nextProcess].popNextCPUBurstTime() + 2
            runningProcess = nextProcess

            # context switch
            numContextSwitches += 1

            if currentProcess != '' and nextProcess != currentProcess:
                runningStart += 2
                runningEnd += 2

        waitTime += addWaitTime(prevReadyQueue, readyQueue)

        time += 1

    avgCPUBurstTime = CPUBurstStart / CPUBurstEnd
    avgWaitTime = waitTime / sum([p.getNumCPUBursts() for p in processList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round( 100 * useful_time / (time+1), 3)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization)
