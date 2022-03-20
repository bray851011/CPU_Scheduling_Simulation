
'''
The RR algorithm is essentially the FCFS algorithm with predeﬁned time slice t slice . Each process is given t slice amount of time to complete its CPU burst. If this time slice expires, the process is preempted and added to the end of the ready queue.
If a process completes its CPU burst before a time slice expiration, the next process on the ready queue is immediately context-switched in to use the CPU.
'''

import copy
from helpers import *
from printHelpers import *

def RR(processList, f, timeSlice):
    
    algo = 'RR'
    numContextSwitches = 0
    numPreemptions = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0

    print(f"time 0ms: Simulator started for RR with time slice {timeSlice}ms [Q empty]")

    arrivalTimes = {}
    originalBurstTimes = {}
    processes = {}
    readyQueue = []
    for process in processList:
        originalBurstTimes[process.getName()] = copy.deepcopy(process.getCPUBurstTimes())
        arrivalTimes[process.getArrivalTime()] = copy.deepcopy(process)
        processes[process.getName()] = copy.deepcopy(process)

    time = 0
    usingCPU = False
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
                currentProcess = runningProcess
                burstTime = runningEnd - runningStart
                CPUBurstStart += burstTime
                useful_time += burstTime
                CPUBurstEnd += 1
                originalBurstTime = originalBurstTimes[runningProcess][0]
                # If the current process is a newcomer
                if burstTime == originalBurstTime:
                    printStartCPU(time, currentProcess, -1, burstTime, readyQueue)
                else:
                    printRestartCPU(time, currentProcess, burstTime, originalBurstTime, -1, readyQueue)
            
            # If time slice is over
            if time == timeSlice + runningStart:
                # If there's stuff in the ready queue, preempt
                if readyQueue:
                    CPUBurstStart -= (runningEnd - time)
                    numPreemptions += 1
                    currentProcess = runningProcess
                    printProcessPreempted(time, currentProcess, processes[currentProcess].getCPUBurstTimes()[0]-(time-runningStart), readyQueue)
                    
                    # Context switch
                    processes[currentProcess].getCPUBurstTimes()[0] -= timeSlice
                    usingCPU = False
                    # Add current process back to ready queue
                    readyQueue.append(currentProcess)
                else:
                    printNoPreemption(time, readyQueue)
            
            # If a CPU burst is complete
            if time == runningEnd:

                currentProcess = runningProcess
                processes[currentProcess].popCurrCPUBurst()

                # If process has no more CPU bursts, terminate it
                if not processes[currentProcess].getNumCPUBursts():
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    printCPUComplete(time, currentProcess, -1, processes[currentProcess].getNumCPUBursts(), readyQueue)
                    
                    blockTime = processes[currentProcess].getCurrIOBurst() + 2

                    processes[currentProcess].popCurrIOBurst()
                    originalBurstTimes[currentProcess].pop(0)

                    unblockTime = time + blockTime
                    printIOBlock(time, currentProcess, unblockTime, readyQueue)

                    blockedProcesses[currentProcess] = unblockTime

            if time == runningEnd + 2:
                usingCPU = False

        # Get processes that have finished their IO block
        unblockedProcesses = []
        for proc, v in blockedProcesses.items():
            # in case there are multiple processes ending at this time
            if time == v:
                unblockedProcesses.append(proc)
        unblockedProcesses.sort()
        readyQueue += unblockedProcesses
        for process in unblockedProcesses:
            printIOComplete(time, process, -1, readyQueue)

        # Check if there's a process coming at this time
        getIncomingProcesses(time, None, arrivalTimes, readyQueue, False)

        # If there aren't any processes running but there are some in the ready queue
        if not usingCPU and readyQueue:
            nextProcess = readyQueue.pop(0)
            usingCPU = True
            runningStart = time + 2
            runningEnd = time + processes[nextProcess].getCurrCPUBurst() + 2
            runningProcess = nextProcess

            # context switch
            numContextSwitches += 1

            if currentProcess != '' and nextProcess != currentProcess:
                runningStart += 2
                runningEnd += 2

        waitTime += len(readyQueue)

        time += 1

    totalCPUBursts = sum([proc.getNumCPUBursts() for proc in processList])
    avgCPUBurstTime = CPUBurstStart / totalCPUBursts
    avgWaitTime = waitTime / totalCPUBursts
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round(100 * CPUBurstStart / (time + 1), 3)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions, CPUUtilization)
