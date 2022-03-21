
import copy
from helpers import *
from printHelpers import *

def SJF(f, processList, alpha, contextSwitchTime):

    algo = 'SJF'
    hCST = int(contextSwitchTime / 2)
    numContextSwitches = 0
    totalCPUBurstTime = 0
    waitTime = 0
    time = 0

    arrivalTimes = {}
    processes = {}
    blockedProcesses = {}
    for process in processList:
        arrivalTimes[process.getArrivalTime()] = copy.deepcopy(process)
        processes[process.getName()] = copy.deepcopy(process)
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
                currentProcess = runningProcess
                totalCPUBurstTime += burstTime
                printStartCPU(time, currentProcess, processes[currentProcess].getTau(), burstTime, readyQueue)

            if time == runningEnd:
                currentProcess = runningProcess

                if not processes[currentProcess].getNumCPUBursts():
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    # If there are more CPU bursts, then it's time for IO block
                    currentTau = processes[currentProcess].getTau()
                    printCPUComplete(time, currentProcess, currentTau, processes[currentProcess].getNumCPUBursts(), readyQueue)

                    blockTime = processes[currentProcess].popCurrIOBurst() + hCST

                    newTau = updateTau(alpha, runningEnd - runningStart, currentTau)
                    printRecalculateTau(time, currentTau, newTau, currentProcess, readyQueue)
                    processes[currentProcess].setTau(newTau)

                    unblockTime = time + blockTime
                    printIOBlock(time, currentProcess, unblockTime, readyQueue)
                    blockedProcesses[currentProcess] = unblockTime

            if time == runningEnd + hCST:
                usingCPU = False

        for proc, unblockT in blockedProcesses.items():
            if time == unblockT:
                readyQueue.append(proc)
                readyQueue.sort(key=lambda x: (processes[x].getTau(), x))
                printIOComplete(time, proc, processes[proc].getTau(), readyQueue)

        getIncomingProcesses(time, processes, arrivalTimes, readyQueue, True)

        if not usingCPU and len(readyQueue):
            nextProcess = readyQueue.pop(0)
            usingCPU = True
            runningStart = time + hCST
            runningEnd = time + processes[nextProcess].getCurrCPUBurst() + hCST
            processes[nextProcess].popCurrCPUBurst()
            runningProcess = nextProcess

            if currentProcess is not None and nextProcess != currentProcess:
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
