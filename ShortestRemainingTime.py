'''
The SRT algorithm is a preemptive version of the SJF algorithm. In SRT, when a process arrives, before it enters the ready queue, if it has a CPU burst time that is less than the remaining time of the currently running process, a preemption occurs. When such a preemption occurs, the currently running process is added back to the ready queue.
'''

import copy
from helpers import *
from printHelpers import *


def SRT(processList, f, alpha, contextSwitchTime):
    algo = 'SRT'
    numContextSwitches = 0
    CPUBurstStart = 0
    waitTime = 0
    numPreemptions = 0

    printStartSimulator(algo)

    originalBurstTimes = {}
    arrivalTimes = {}
    processes = {}
    readyQueue = []
    for process in processList:
        originalBurstTimes[process.getName()] = copy.deepcopy(process.getCPUBurstTimes())
        arrivalTimes[process.getArrivalTime()] = copy.deepcopy(process)
        processes[process.getName()] = copy.deepcopy(process)

    time = 0

    usingCPU = False
    preempted = False

    blockedProcesses = {}

    while True:

        currentProcess = ''

        # If there are no processes left, then simulator is done
        if not processes:
            printEndSimulator(time + 1, algo)
            break

        if usingCPU:
            # start running a process -- time == start time of the process
            if time == runningStart:
                burstTime = runningEnd - runningStart
                currentProcess = runningProcess
                CPUBurstStart += burstTime
                originalBurstTime = originalBurstTimes[runningProcess][0]
                # If the current process is a newcomer
                currentTau = processes[runningProcess].getTau()
                if burstTime == originalBurstTime:
                    printStartCPU(time, currentProcess, currentTau, burstTime, readyQueue)
                else:
                    printRestartCPU(time, currentProcess, burstTime, originalBurstTime, currentTau, readyQueue)

            # end running a process -- time == end time of the process
            if time == runningEnd:
                currentProcess = runningProcess
                processes[currentProcess].popCurrCPUBurst()
                # check if the process reaches the end -- cpu burst time list is empty
                if not processes[currentProcess].getNumCPUBursts():
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    # If there are more CPU bursts, then it's time for IO block
                    currentTau = processes[currentProcess].getTau()
                    printCPUComplete(time, currentProcess, currentTau, processes[currentProcess].getNumCPUBursts(),
                                     readyQueue)

                    blockTime = processes[currentProcess].popCurrIOBurst() + 2
                    burstTime = originalBurstTimes[currentProcess].pop(0)

                    # update tau <- alpha * burst time + (1 - alpha) * tau
                    newTau = updateTau(alpha, burstTime, currentTau)
                    printRecalculateTau(time, currentTau, newTau, currentProcess, readyQueue)
                    processes[currentProcess].setTau(newTau)

                    unblockTime = time + blockTime
                    printIOBlock(time, currentProcess, unblockTime, readyQueue)
                    blockedProcesses[currentProcess] = unblockTime

            # wait for another 2ms for cpu to be reused
            if time == runningEnd + 2:
                usingCPU = False

        unblockedProcesses = []
        for proc, unblockTime in blockedProcesses.items():
            if time == unblockTime:
                readyQueue.append(copy.deepcopy(proc))
                unblockedProcesses.append(copy.deepcopy(proc))
        if unblockedProcesses:
            readyQueue.sort(key=lambda x: (processes[x].getTau(), x))
            nextProcess = readyQueue[0]
            tempRunningTime = time - runningStart
            # if time == 128127:
            #     print('')
            if usingCPU and processes[nextProcess].getTau() < processes[runningProcess].getTau() - tempRunningTime:
                printPreemption(time, runningProcess, processes, readyQueue)
                preempted = True
                numPreemptions += 1
                processes[runningProcess].getCPUBurstTimes()[0] -= tempRunningTime
                runningEnd = time
                CPUBurstStart -= tempRunningTime
                if nextProcess in unblockedProcesses:
                    unblockedProcesses.remove(nextProcess)
            for proc in unblockedProcesses:
                printIOComplete(time, proc, processes[proc].getTau(), readyQueue)

        # Check if there's a process coming at this time
        getIncomingProcesses(time, processes, arrivalTimes, readyQueue, True)

        # Get next ready process if CPU isn't being used
        if not usingCPU and readyQueue:
            if preempted:
                readyQueue.append(runningProcess)
                preempted = False
            usingCPU = True
            nextProcess = readyQueue.pop(0)
            runningStart = time + 2
            runningEnd = runningStart + processes[nextProcess].getCurrCPUBurst()
            runningProcess = nextProcess

            # Context switch
            numContextSwitches += 1

            if currentProcess != '' and nextProcess != currentProcess:
                runningStart += 2
                runningEnd += 2

        waitTime += len(readyQueue)

        time += 1

    totalCPUBursts = sum([proc.getNumCPUBursts() for proc in processList])
    CPUBurstStart = sum([sum(proc.getCPUBurstTimes()) for proc in processList])
    avgCPUBurstTime = CPUBurstStart / totalCPUBursts
    avgWaitTime = waitTime / totalCPUBursts
    avgTurnaroundTime = (CPUBurstStart + waitTime + numContextSwitches * contextSwitchTime) / totalCPUBursts
    CPUUtilization = 100 * CPUBurstStart / (time + 1)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions,
              CPUUtilization)
    print()