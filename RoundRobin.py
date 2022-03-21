
import copy
from helpers import *
from printHelpers import *

def RR(f, processList, timeSlice, contextSwitchTime):
    
    algo = 'RR'
    hCST = int(contextSwitchTime / 2)
    numContextSwitches = 0
    numPreemptions = 0
    totalCPUBurstTime = 0
    waitTime = 0
    time = 0

    arrivalTimes = {}
    originalBurstTimes = {}
    processes = {}
    blockedProcesses = {}
    for process in processList:
        originalBurstTimes[process.getName()] = copy.deepcopy(process.getCPUBurstTimes())
        arrivalTimes[process.getArrivalTime()] = copy.deepcopy(process)
        processes[process.getName()] = copy.deepcopy(process)
    readyQueue = []

    nextCutoff = 0
    usingCPU = False

    print(f"time 0ms: Simulator started for RR with time slice {timeSlice}ms [Q empty]")

    while True:

        # If there are no processes left, then simulator is done
        if not processes:
            printEndSimulator(time + 1, algo)
            break
        
        currentProcess = None

        if usingCPU:
            if time == runningStart:
                currentProcess = runningProcess
                burstTime = runningEnd - runningStart
                totalCPUBurstTime += burstTime
                originalBurstTime = originalBurstTimes[runningProcess][0]
                # If the current process is a newcomer
                if burstTime == originalBurstTime:
                    printStartCPU(time, currentProcess, -1, burstTime, readyQueue)
                else:
                    printRestartCPU(time, currentProcess, burstTime, originalBurstTime, -1, readyQueue)
            
            if time == nextCutoff:
                if readyQueue:
                    totalCPUBurstTime -= (runningEnd - time)
                    numPreemptions += 1
                    currentProcess = runningProcess
                    processes[currentProcess].getCPUBurstTimes()[0] -= (time-runningStart)
                    printProcessPreempted(time, currentProcess, processes[currentProcess].getCPUBurstTimes()[0], readyQueue)
                    
                    usingCPU = False

                    readyQueue.append(currentProcess)
                else:
                    nextCutoff += timeSlice
                    printNoPreemption(time, readyQueue)
            
            if time == runningEnd:
                nextCutoff += timeSlice
                currentProcess = runningProcess
                processes[currentProcess].popCurrCPUBurst()
                if not processes[currentProcess].getNumCPUBursts():
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    printCPUComplete(time, currentProcess, -1, processes[currentProcess].getNumCPUBursts(), readyQueue)
                    
                    blockTime = processes[currentProcess].getCurrIOBurst() + hCST

                    processes[currentProcess].popCurrIOBurst()
                    originalBurstTimes[currentProcess].pop(0)
                    unblockTime = time + blockTime
                    printIOBlock(time, currentProcess, unblockTime, readyQueue)

                    blockedProcesses[currentProcess] = unblockTime

            if time == runningEnd + hCST:
                usingCPU = False

        unblockedProcesses = []
        for proc, unblockT in blockedProcesses.items():
            if time == unblockT:
                unblockedProcesses.append(proc)
        unblockedProcesses.sort()
        readyQueue += unblockedProcesses
        for process in unblockedProcesses:
            printIOComplete(time, process, -1, readyQueue)

        getIncomingProcesses(time, None, arrivalTimes, readyQueue, False)

        if not usingCPU and readyQueue:
            nextProcess = readyQueue.pop(0)
            usingCPU = True
            runningStart = time + hCST
            runningEnd = runningStart + processes[nextProcess].getCurrCPUBurst()
            runningProcess = nextProcess

            if currentProcess is not None and nextProcess is not currentProcess:
                runningStart += hCST
                runningEnd += hCST
            
            numContextSwitches += 1

            nextCutoff = runningStart + timeSlice

        waitTime += len(readyQueue)

        time += 1

    totalCPUBursts = sum([proc.getNumCPUBursts() for proc in processList])
    totalCPUBurstTime = sum([sum(proc.getCPUBurstTimes()) for proc in processList])
    avgCPUBurstTime = totalCPUBurstTime / totalCPUBursts
    avgWaitTime = waitTime / totalCPUBursts
    avgTurnaroundTime = (totalCPUBurstTime + waitTime + numContextSwitches * contextSwitchTime) / totalCPUBursts
    CPUUtilization = 100 * totalCPUBurstTime / (time + 1)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions, CPUUtilization)
