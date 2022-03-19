
'''
The SRT algorithm is a preemptive version of the SJF algorithm. In SRT, when a process arrives, before it enters the ready queue, if it has a CPU burst time that is less than the remaining time of the currently running process, a preemption occurs. When such a preemption occurs, the currently running process is added back to the ready queue.
'''

from helpers import *

def SRT(processList, f, alpha, contextSwitchTime):

    # analysis variable
    algo = 'SRT'
    numContextSwitches = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0
    numPreemptions = 0

    printStartSimulator(algo)

    arrivalTimeDict = {}
    processes = {}
    readyQueue = []
    for process in processList:
        arrivalTimeDict[process.getArrivalTime()] = process.get()
        processes[process.getName()] = [*process.get()]

    time = 0

    usingCPU = False

    # when a process is blocked, add to this map with its time
    blockDict = {}

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
                printStartCPU(time, currentProcess, processes[runningProcess][5], burstTime, readyQueue)
            
            # end running a process -- time == end time of the process
            if time == runningEnd:
                currentProcess = runningProcess

                # check if the process reaches the end -- cpu burst time list is empty
                if len(processes[runningProcess][3]) == 0:
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    currentTau = processes[currentProcess][5]
                    printCPUComplete(time, currentProcess, processes[currentProcess][5], processes[currentProcess][2], readyQueue)
                    
                    blockTime = processes[currentProcess][4][0] + 2

                    processes[currentProcess][4].pop(0)

                    # update tau <- alpha * burst time + (1 - alpha) * tau
                    newTau = updateTau(alpha, runningEnd - runningStart, currentTau)

                    printRecalculateTau(time, currentTau, newTau, currentProcess, readyQueue)

                    processes[currentProcess][5] = newTau

                    printIOBlock(time, currentProcess, time + blockTime, readyQueue)

                    blockDict[currentProcess] = time + blockTime, currentProcess

            # wait for another 2ms for cpu to be reused
            if time == runningEnd + 2:
                usingCPU = False


        for v in blockDict.values():
            if time == v[0]:
                readyQueue.append(v[1])
                readyQueue.sort(key=lambda x: (processes[x][5], x))
                printIOComplete(time, v[1], processes[v[1]][5], readyQueue)

        # Check if there's a process coming at this time
        if time in arrivalTimeDict.keys():
            readyQueue.append(arrivalTimeDict[time][0])
            readyQueue.sort(key=lambda x: (processes[x][5], x))
            printProcessArrived(time, arrivalTimeDict[time][0], arrivalTimeDict[time][5], readyQueue)

        # no process is running and there is at least one ready process
        if not usingCPU and readyQueue:
            nextProcess = readyQueue.pop(0)
            usingCPU = True
            runningStart = time + 2
            runningEnd = time + processes[nextProcess][3][0] + 2
            processes[nextProcess][3].pop(0)
            processes[nextProcess][2] -= 1
            runningProcess = nextProcess

            # context switch
            numContextSwitches += 1

            if currentProcess != '' and nextProcess != currentProcess:
                runningStart += 2
                runningEnd += 2

        waitTime += addWaitTime(prevReadyQueue, readyQueue)

        time += 1

    avgCPUBurstTime = CPUBurstStart / CPUBurstEnd
    avgWaitTime = waitTime / sum([p.get()[2] for p in processList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + contextSwitchTime
    CPUUtilization = round(100 * useful_time / (time + 1), 3)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions, CPUUtilization)
