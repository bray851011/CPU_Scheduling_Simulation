
'''
In SJF, processes are stored in the ready queue in order of priority based on their anticipated
CPU burst times. More speciﬁcally, the process with the shortest CPU burst time will be
selected as the next process executed by the CPU.
'''

import math
from helpers import *

def SJF(processList, f, alpha):

    # analysis variable
    numContextSwitches = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0

    print("time 0ms: Simulator started for SJF [Q empty]")

    arrivalTimeDict = {}
    processes = {}
    readyQueue = []
    for process in processList:
        arrivalTimeDict[process.getArrivalTime()] = process.get()
        processes[process.getName()] = [*process.get()]

    time = 0

    # isRunning -- whether CPU is in use
    # runningStart -- if isRunning, then this represents the start time of this running
    # runningEnd -- if isRunning, then this represents the end time of this running
    # runningProcess -- if isRunning, then this represents the process name of this running
    isRunning = False

    # when a process is blocked, add to this map with its time
    blockDict = {}

    while True:

        prevReadyQueue = readyQueue

        currentProcess = ''

        # If there are no processes left, then simulator is done
        if not processes:
            print(f"time {time + 1}ms: Simulator ended for SJF [Q empty]")
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
                        f'time {time}ms: Process {currentProcess} '
                        f'(tau {processes[currentProcess][5]}ms) started using the CPU '
                        f'for {burstTime}ms burst',
                        printReadyQueue(readyQueue))
            
            # end running a process -- time == end time of the process
            if time == runningEnd:
                currentProcess = runningProcess

                # check if the process reaches the end -- cpu burst time list is empty
                if len(processes[currentProcess][3]) == 0:
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

        # check if there is a process coming at this time
        if time in arrivalTimeDict.keys():
            readyQueue.append(arrivalTimeDict[time][0])
            readyQueue.sort(key=lambda x: (processes[x][5], x))
            if time <= DISPLAY_MAX_T:
                print(
                    f'time {time}ms: Process {arrivalTimeDict[time][0]} '
                    f'(tau {arrivalTimeDict[time][5]}ms) arrived; '
                    f'added to ready queue', printReadyQueue(readyQueue))

        # no process is running and there is at least one ready process
        if not isRunning and len(readyQueue):
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
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round(100 * useful_time / (time + 1), 3)

    data = avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization
    writeData(f, "SJF", data)