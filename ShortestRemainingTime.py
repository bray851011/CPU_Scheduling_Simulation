
'''
The SRT algorithm is a preemptive version of the SJF algorithm. In SRT, when a process arrives, before it enters the ready queue, if it has a CPU burst time that is less than the remaining time of the currently running process, a preemption occurs. When such a preemption occurs, the currently running process is added back to the ready queue.
'''

import math
from helpers import *

def SRT(processList, f, alpha, contextSwitchTime):

    # analysis variable
    numContextSwitches = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0
    numPreemptions = 0

    print("time 0ms: Simulator started for SRT [Q empty]")

    arrivalTimeDict = {}
    processes = {}
    readyQueue = []
    for thread in processList:
        arrivalTimeDict[thread.get()[1]] = thread.get()
        processes[thread.get()[0]] = [*thread.get()]

    time = 0

    isRunning = False

    # when a process is blocked, add to this map with its time
    blockDict = {}

    while True:

        prevReadyQueue = readyQueue

        currentProcess = ''

        # If there are no processes left, then simulator is done
        if not processes:
            print(f"time {time + 1}ms: Simulator ended for SRT [Q empty]")
            break

        if isRunning:
            # start running a process -- time == start time of the process
            if time == runningStart:
                burstTime = runningEnd - runningStart
                currentProcess = runningProcess
                CPUBurstStart += burstTime
                useful_time += burstTime
                CPUBurstEnd += 1
                if time <= DISPLAY_MAX_T:
                    print(
                        f'time {time}ms: Process {processes[runningProcess][0]} '
                        f'(tau {processes[runningProcess][5]}ms) started using the CPU '
                        f'for {burstTime}ms burst',
                        printReadyQueue(readyQueue))
            
            # end running a process -- time == end time of the process
            if time == runningEnd:
                currentProcess = runningProcess

                # check if the process reaches the end -- cpu burst time list is empty
                if len(processes[runningProcess][3]) == 0:
                    print(f'time {time}ms: Process {currentProcess} terminated',
                          printReadyQueue(readyQueue))
                    del processes[currentProcess]
                else:
                    if time <= DISPLAY_MAX_T:
                        print(
                                f'time {time}ms: Process {currentProcess} '
                                f'(tau {processes[currentProcess][5]}ms) '
                                f'completed a CPU burst; '
                                f'{processes[currentProcess][2]} '
                                f'burst{"s" if processes[currentProcess][2] > 1 else ""} to go',
                                printReadyQueue(readyQueue))
                    blockTime = processes[currentProcess][4][0] + 2

                    processes[currentProcess][4].pop(0)

                    # update tau <- alpha * burst time + (1 - alpha) * tau
                    tau = math.ceil(alpha * (runningEnd - runningStart) +
                                    (1 - alpha) * processes[currentProcess][5])
                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Recalculated tau from '
                            f'{processes[currentProcess][5]}ms to {tau}ms '
                            f'for process {currentProcess}',
                            printReadyQueue(readyQueue))
                    processes[currentProcess][5] = tau

                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Process {currentProcess} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + blockTime}ms',
                            printReadyQueue(readyQueue))
                    blockDict[currentProcess] = time + blockTime, currentProcess

        # wait for another 2ms for cpu to be reused
        if isRunning:
            if time == runningEnd + 2:
                isRunning = False

        for v in blockDict.values():
            if time == v[0]:
                readyQueue.append(v[1])
                readyQueue.sort(key=lambda x: (processes[x][5], x))
                if time <= DISPLAY_MAX_T:
                    printIOCompleted(time, v[1], processes[v[1]][5], readyQueue)

        # Check if there's a process coming at this time
        if time in arrivalTimeDict.keys():
            readyQueue.append(arrivalTimeDict[time][0])
            readyQueue.sort(key=lambda x: (processes[x][5], x))
            if time <= DISPLAY_MAX_T:
                printProcessArrived(time, arrivalTimeDict[time][0], arrivalTimeDict[time][5], readyQueue)
                # print(
                #     f'time {time}ms: Process {arrivalTimeDict[time][0]} '
                #     f'(tau {arrivalTimeDict[time][5]}ms) arrived; '
                #     f'added to ready queue', printReadyQueue(readyQueue))

        # no process is running and there is at least one ready process
        if not isRunning and len(readyQueue) > 0:
            nextProcess = readyQueue.pop(0)
            isRunning = True
            runningStart = time + 2  # start
            runningEnd = time + processes[nextProcess][3][0] + 2  # end
            processes[nextProcess][3].pop(0)
            processes[nextProcess][2] -= 1
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
    avgWaitTime = waitTime / sum([p.get()[2] for p in processList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + contextSwitchTime
    CPUUtilization = round(100 * useful_time / (time + 1), 3)

    data = avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions, CPUUtilization
    writeData(f, "SRT", data)