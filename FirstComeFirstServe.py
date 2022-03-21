
import copy
from helpers import *
from printHelpers import *

def FCFS(f, processList, contextSwitchTime):

    algo = "FCFS"
    hCST = int(contextSwitchTime / 2)
    numContextSwitches = 0
    totalCPUBurstTime = 0
    waitTime = 0
    time = 0

    processes = {}
    arrivalTimes = {}
    blockedProcesses = {}
    for process in processList:
        processes[process.getName()] = copy.deepcopy(process)
        arrivalTimes[process.getArrivalTime()] = copy.deepcopy(process)
    readyQueue = []

    usingCPU = False

    printStartSimulator(algo)

    while True:

        # If there are no processes left, then simulator is done
        if not processes:
            printEndSimulator(time + 1, algo)
            break

        currentProcess = None

        if usingCPU:
            if time == runningStart:
                burstTime = runningEnd - runningStart
                totalCPUBurstTime += burstTime
                printStartCPU(time, runningProcess, -1, burstTime, readyQueue)

            if time == runningEnd:
                currentProcess = runningProcess
                if not processes[currentProcess].getNumCPUBursts():
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    printCPUComplete(time, currentProcess, -1, processes[currentProcess].getNumCPUBursts(), readyQueue)

                    blockTime = processes[currentProcess].popCurrIOBurst() + hCST

                    unblockTime = time + blockTime
                    printIOBlock(time, currentProcess, unblockTime, readyQueue)
                    blockedProcesses[currentProcess] = unblockTime

            if time == runningEnd + hCST:
                usingCPU = False

        unblockedProcesses = []
        for proc, unblockTime in blockedProcesses.items():
            if time == unblockTime:
                unblockedProcesses.append(proc)
        unblockedProcesses.sort()
        readyQueue += unblockedProcesses
        for proc in unblockedProcesses:
            printIOComplete(time, proc, -1, readyQueue)

        getIncomingProcesses(time, None, arrivalTimes, readyQueue, False)

        if not usingCPU and readyQueue:
            usingCPU = True
            nextProcess = readyQueue.pop(0)
            runningStart = time + hCST
            runningEnd = runningStart + processes[nextProcess].popCurrCPUBurst()
            runningProcess = nextProcess

            if currentProcess is not None and nextProcess is not currentProcess:
                runningStart += hCST
                runningEnd += hCST
            
            numContextSwitches += 1

        waitTime += len(readyQueue)

        time += 1

    totalCPUBursts = sum([proc.getNumCPUBursts() for proc in processList])
    totalCPUBurstTime = sum([sum(proc.getCPUBurstTimes()) for proc in processList])
    avgCPUBurstTime = totalCPUBurstTime / totalCPUBursts
    avgWaitTime = waitTime / totalCPUBursts
    avgTurnaroundTime = (totalCPUBurstTime + waitTime + numContextSwitches * contextSwitchTime) / totalCPUBursts
    CPUUtilization = 100 * totalCPUBurstTime / (time + 1)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization)
    print()
