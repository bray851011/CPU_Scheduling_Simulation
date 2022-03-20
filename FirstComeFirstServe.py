'''
The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
queue, waiting to use the CPU. This is your baseline algorithm (and could be implemented as RR
with an "infinite" time slice).
'''

import copy
from helpers import *
from printHelpers import *

def FCFS(processList, f, contextSwitchTime):

    algo = "FCFS"
    numContextSwitches = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0

    printStartSimulator(algo)

    readyQueue = []
    processes = {}
    arrivalTimes = {}
    for process in processList:
        processes[process.getName()] = copy.deepcopy(process)
        arrivalTimes[process.getArrivalTime()] = copy.deepcopy(process)

    time = 0
    usingCPU = False
    runningProcess = ''
    blockedProcesses = {}

    while True:

        currentProcess = ''

        # If there are no processes left, then simulator is done
        if not processes:
            printEndSimulator(time + 1, algo)
            break

        if usingCPU:
            # If a CPU burst is starting
            if time == runningStart:
                burstTime = runningEnd - runningStart
                CPUBurstStart += burstTime
                useful_time += burstTime
                CPUBurstEnd += 1
                printStartCPU(time, runningProcess, -1, burstTime, readyQueue)

            # If a CPU burst is complete
            if time == runningEnd:
                currentProcess = runningProcess
                # If no more CPU bursts
                if not processes[currentProcess].getNumCPUBursts():
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    printCPUComplete(time, currentProcess, -1, processes[currentProcess].getNumCPUBursts(), readyQueue)

                    blockTime = processes[currentProcess].popCurrIOBurst() + contextSwitchTime / 2

                    unblockTime = time + blockTime
                    printIOBlock(time, currentProcess, unblockTime, readyQueue)
                    blockedProcesses[currentProcess] = unblockTime

            if time == runningEnd + contextSwitchTime / 2:
                usingCPU = False

        # Get processes that are done with their IO block
        unblockedProcesses = []
        for proc, unblockTime in blockedProcesses.items():
            if time == unblockTime:
                unblockedProcesses.append(proc)
        unblockedProcesses.sort()
        readyQueue += unblockedProcesses
        for proc in unblockedProcesses:
            printIOComplete(time, proc, -1, readyQueue)

        # Check if there is a process coming at this time
        getIncomingProcesses(time, None, arrivalTimes, readyQueue, False)

        # no process is running and there is at least one ready process
        if not usingCPU and readyQueue:
            usingCPU = True
            nextProcess = readyQueue.pop(0)
            runningStart = time + contextSwitchTime / 2
            runningEnd = runningStart + processes[nextProcess].popCurrCPUBurst()
            runningProcess = nextProcess

            # context switch
            numContextSwitches += 1

            if currentProcess != '' and nextProcess != currentProcess:
                runningStart += contextSwitchTime / 2
                runningEnd += contextSwitchTime / 2

        waitTime += len(readyQueue)

        time += 1

    totalCPUBursts = sum([proc.getNumCPUBursts() for proc in processList])
    CPUBurstStart = sum([sum(proc.getCPUBurstTimes()) for proc in processList])
    avgCPUBurstTime = CPUBurstStart / totalCPUBursts
    avgWaitTime = waitTime / totalCPUBursts
    avgTurnaroundTime = (CPUBurstStart + waitTime + numContextSwitches * contextSwitchTime) / totalCPUBursts
    CPUUtilization = 100 * CPUBurstStart / (time + 1)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization)