'''
In SJF, processes are stored in the ready queue in order of priority based on their anticipated
CPU burst times. More speciﬁcally, the process with the shortest CPU burst time will be
selected as the next process executed by the CPU.
'''

import copy
from helpers import *
from printHelpers import *

def SJF(processList, f, alpha):

    # analysis variable
    algo = 'SJF'
    numContextSwitches = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0

    printStartSimulator(algo)

    arrivalTimes = {}
    processes = {}
    readyQueue = []
    for process in processList:
        arrivalTimes[process.getArrivalTime()] = copy.deepcopy(process)
        processes[process.getName()] = copy.deepcopy(process)

    time = 0

    usingCPU = False

    # when a process is blocked, add to this map with its time
    blockedProcesses = {}

    while True:

        prevReadyQueue = readyQueue
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
                useful_time += burstTime
                CPUBurstEnd += 1
                printStartCPU(time, currentProcess, processes[currentProcess].getTau(), burstTime, readyQueue)

            # end running a process -- time == end time of the process
            if time == runningEnd:
                currentProcess = runningProcess

                # check if the process reaches the end -- cpu burst time list is empty
                if not processes[currentProcess].getNumCPUBursts():
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    # If there are more CPU bursts, then it's time for IO block
                    currentTau = processes[currentProcess].getTau()
                    printCPUComplete(time, currentProcess, currentTau, processes[currentProcess].getNumCPUBursts(), readyQueue)

                    blockTime = processes[currentProcess].popCurrIOBurst() + 2

                    # update tau <- alpha * burst time + (1 - alpha) * tau
                    newTau = updateTau(alpha, runningEnd - runningStart, currentTau)
                    printRecalculateTau(time, currentTau, newTau, currentProcess, readyQueue)
                    processes[currentProcess].setTau(newTau)

                    unblockTime = time + blockTime
                    printIOBlock(time, currentProcess, unblockTime, readyQueue)
                    blockedProcesses[currentProcess] = unblockTime

            # wait for another 2ms for cpu to be reused
            if time == runningEnd + 2:
                usingCPU = False

        for proc, unblockTime in blockedProcesses.items():
            if time == unblockTime:
                readyQueue.append(proc)
                readyQueue.sort(key=lambda x: (processes[x].getTau(), x))
                printIOComplete(time, proc, processes[proc].getTau(), readyQueue)

        # Check if there is a process coming at this time
        getIncomingProcesses(time, processes, arrivalTimes, readyQueue, True)

        # no process is running and there is at least one ready process
        if not usingCPU and len(readyQueue):
            nextProcess = readyQueue.pop(0)
            usingCPU = True
            runningStart = time + 2
            runningEnd = time + processes[nextProcess].getCurrCPUBurst() + 2
            processes[nextProcess].popCurrCPUBurst()
            runningProcess = nextProcess

            # context switch
            numContextSwitches += 1

            if currentProcess != '' and nextProcess != currentProcess:
                runningStart += 2
                runningEnd += 2

        waitTime += addWaitTime(prevReadyQueue, readyQueue)

        time += 1

    totalCPUBursts = sum([proc.getNumCPUBursts() for proc in processList])
    avgCPUBurstTime = CPUBurstStart / totalCPUBursts
    avgWaitTime = waitTime / totalCPUBursts
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round(100 * CPUBurstStart / (time + 1), 3)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization)