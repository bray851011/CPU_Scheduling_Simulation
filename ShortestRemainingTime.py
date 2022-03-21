
import copy
from helpers import *
from printHelpers import *

def SRT(f, processList, alpha, contextSwitchTime):
    
    algo = 'SRT'
    hCST = int(contextSwitchTime / 2)
    numContextSwitches = 0
    totalCPUBurstTime = 0
    time = 0
    waitTime = 0
    numPreemptions = 0

    originalBurstTimes = {}
    arrivalTimes = {}
    processes = {}
    blockedProcesses = {}
    for process in processList:
        originalBurstTimes[process.getName()] = copy.deepcopy(process.getCPUBurstTimes())
        arrivalTimes[process.getArrivalTime()] = copy.deepcopy(process)
        processes[process.getName()] = copy.deepcopy(process)
    readyQueue = []

    usingCPU = False
    preempted = False

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
                currentProcess = runningProcess
                totalCPUBurstTime += burstTime
                originalBurstTime = originalBurstTimes[runningProcess][0]
                # If the current process is a newcomer
                currentTau = processes[runningProcess].getTau()
                if burstTime == originalBurstTime or burstTime < 0:
                    printStartCPU(time, currentProcess, currentTau, originalBurstTime, readyQueue)
                    if burstTime < 0:
                        usingCPU = False
                else:
                    printRestartCPU(time, currentProcess, burstTime, originalBurstTime, currentTau, readyQueue)

            if time == runningEnd:
                currentProcess = runningProcess
                processes[currentProcess].popCurrCPUBurst()
                if not processes[currentProcess].getNumCPUBursts():
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    currentTau = processes[currentProcess].getTau()
                    printCPUComplete(time, currentProcess, currentTau, processes[currentProcess].getNumCPUBursts(),
                                     readyQueue)

                    blockTime = processes[currentProcess].popCurrIOBurst() + hCST
                    burstTime = originalBurstTimes[currentProcess].pop(0)

                    newTau = updateTau(alpha, burstTime, currentTau)
                    printRecalculateTau(time, currentTau, newTau, currentProcess, readyQueue)
                    processes[currentProcess].setTau(newTau)

                    unblockTime = time + blockTime
                    printIOBlock(time, currentProcess, unblockTime, readyQueue)
                    blockedProcesses[currentProcess] = unblockTime

            if time == runningEnd + hCST:
                usingCPU = False

        unblockedProcesses = []
        for proc, unblockTime in blockedProcesses.items():
            if time == unblockTime:
                readyQueue.append(copy.deepcopy(proc))
                unblockedProcesses.append(copy.deepcopy(proc))
        if unblockedProcesses:
            if usingCPU:
                readyQueue.sort(key=lambda x: (processes[x].getTau(), x))
                nextProcess = readyQueue[0]
                tempRunningTime = time - runningStart
                extra = originalBurstTimes[runningProcess][0] - processes[runningProcess].getCurrCPUBurst()
                if processes[nextProcess].getTau() < processes[runningProcess].getTau() - tempRunningTime - extra:
                    printPreemption(time, runningProcess, processes, readyQueue)
                    preempted = True
                    numPreemptions += 1
                    processes[runningProcess].getCPUBurstTimes()[0] -= tempRunningTime if tempRunningTime > 0 else 0
                    processes[runningProcess].decreaseTempTau(tempRunningTime)
                    runningEnd = time
                    totalCPUBurstTime -= tempRunningTime
                    if nextProcess in unblockedProcesses:
                        unblockedProcesses.remove(nextProcess)
            for proc in unblockedProcesses:
                printIOComplete(time, proc, processes[proc].getTau(), readyQueue)
            readyQueue.sort(key=lambda x: (processes[x].getTempTau(), x))

        getIncomingProcesses(time, processes, arrivalTimes, readyQueue, True)

        if not usingCPU and readyQueue:
            if preempted:
                readyQueue.insert(1, runningProcess)
                preempted = False
            usingCPU = True
            nextProcess = readyQueue.pop(0)
            runningStart = time + hCST
            runningEnd = runningStart + processes[nextProcess].getCurrCPUBurst()
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

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions,
              CPUUtilization)
    print()