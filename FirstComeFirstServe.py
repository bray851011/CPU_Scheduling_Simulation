'''
The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
queue, waiting to use the CPU. This is your baseline algorithm (and could be implemented as RR
with an "infinite" time slice).
'''

import copy
from helpers import *

def FCFS(processList, f):

    numContextSwitches = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0

    print("time 0ms: Simulator started for FCFS [Q empty]")

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
            print(f"time {time + 1}ms: Simulator ended for FCFS [Q empty]")
            break

        # print changes to the process
        if usingCPU:
            if time == runningStart:
                runningTime = runningEnd - runningStart
                CPUBurstStart += runningTime
                useful_time += runningTime
                CPUBurstEnd += 1
                if time <= DISPLAY_MAX_T:
                    print(
                        f'time {time}ms: Process {processes[runningProcess].getName()} '
                        f'started using the CPU for {runningTime}ms burst',
                        printReadyQueue(readyQueue))

        if usingCPU:
            if time == runningEnd:
                currentProcess = runningProcess

                if len(processes[currentProcess].getCPUBurstTimes()) == 0:
                    print(f'time {time}ms: Process {currentProcess} terminated',
                          printReadyQueue(readyQueue))
                    del processes[currentProcess]
                else:
                    if time <= DISPLAY_MAX_T:
                            print(
                                f'time {time}ms: Process {processes[currentProcess].getName()} '
                                f'completed a CPU burst; '
                                f'{processes[currentProcess].getNumCPUBursts()} '
                                f'burst{"s" if processes[currentProcess].getNumCPUBursts() > 1 else ""} to go',
                                printReadyQueue(readyQueue))
                    blockTime = processes[currentProcess].popNextIOBurstTime() + 2

                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Process {processes[currentProcess].getName()} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + blockTime}ms',
                            printReadyQueue(readyQueue))
                    blockDict[currentProcess] = \
                        time + blockTime, currentProcess

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
            if time <= DISPLAY_MAX_T:
                print(
                    f'time {time}ms: Process {proc} '
                    f'completed I/O; added to ready queue',
                    printReadyQueue(readyQueue))

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

        for p in prevReadyQueue:
            if p in readyQueue:
                waitTime += 1

        time += 1

    avgCPUBurstTime = CPUBurstStart / CPUBurstEnd
    avgWaitTime = waitTime / sum([p.getNumCPUBursts() for p in processList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round( 100 * useful_time / (time+1), 3)

    data = avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization
    writeData(f, "FCFS", data)