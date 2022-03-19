
'''
In SJF, processes are stored in the ready queue in order of priority based on their anticipated
CPU burst times. More speciﬁcally, the process with the shortest CPU burst time will be
selected as the next process executed by the CPU.
'''

import math
import copy
from helpers import printReadyQueue, writeData, DISPLAY_MAX_T

def SJF(processList, f, alpha):

    # analysis variable
    numContextSwitches = 0
    cpu_burst_time = [0, 0]
    waitTime = 0
    useful_time = 0

    print("time 0ms: Simulator started for SJF [Q empty]")

    arrivalTimeDict = {}
    processes = {}
    readyQueue = []
    for process in processList:
        arrivalTimeDict[process.getArrivalTime()] = copy.deepcopy(list(process.get()))
        processes[process.getName()] = copy.deepcopy(list(process.get()))
        # arrivalTimeDict[process.get()[1]] = process.get()
        # processes[process.get()[0]] = [*process.get()]

    time = 0

    # running[0] -- whether CPU is in use
    # running[1] -- if running[0], then this represents the start time of this running
    # running[2] -- if running[0], then this represents the end time of this running
    # running[3] -- if running[0], then this represents the process name of this running
    CPUstatus = [False, '', '', '']

    # when a process is blocked, add to this map with its time
    blockDict = {}

    # main SJF process starts here
    while True:

        old_read_queue = readyQueue

        curr_proc = ''

        # CPU being used
        if CPUstatus[0]:
            # time == start time of the process
            if time == CPUstatus[1]:
                curr_proc = CPUstatus[3]
                cpu_burst_time[0] += CPUstatus[2] - CPUstatus[1]
                useful_time += CPUstatus[2] - CPUstatus[1]
                cpu_burst_time[1] += 1
                if time <= DISPLAY_MAX_T:
                    print(
                        f'time {time}ms: Process {processes[CPUstatus[3]][0]} '
                        f'(tau {processes[CPUstatus[3]][5]}ms) started using the CPU '
                        f'for {CPUstatus[2] - CPUstatus[1]}ms burst',
                        printReadyQueue(readyQueue))
            # time == end time of the process
            if time == CPUstatus[2]:
                curr_proc = CPUstatus[3]

                # check if the process reaches the end -- cpu burst time list is empty
                if len(processes[CPUstatus[3]][3]) == 0:
                    print(f'time {time}ms: Process {CPUstatus[3]} terminated',
                          printReadyQueue(readyQueue))
                    del processes[CPUstatus[3]]
                else:
                    if processes[CPUstatus[3]][2] > 1:
                        if time <= DISPLAY_MAX_T:
                            print(
                                f'time {time}ms: Process {processes[CPUstatus[3]][0]} '
                                f'(tau {processes[CPUstatus[3]][5]}ms) '
                                f'completed a CPU burst; '
                                f'{processes[CPUstatus[3]][2]} bursts to go',
                                printReadyQueue(readyQueue))
                    else:
                        if time <= DISPLAY_MAX_T:
                            print(
                                f'time {time}ms: Process {processes[CPUstatus[3]][0]} '
                                f'(tau {processes[CPUstatus[3]][5]}ms) '
                                f'completed a CPU burst; '
                                f'{processes[CPUstatus[3]][2]} burst to go',
                                printReadyQueue(readyQueue))
                    block_time = processes[CPUstatus[3]][4][0] + 2

                    processes[CPUstatus[3]][4].pop(0)

                    # update tau <- alpha * burst time + (1 - alpha) * tau
                    tau = math.ceil(alpha * (CPUstatus[2] - CPUstatus[1]) +
                                    (1 - alpha) * processes[CPUstatus[3]][5])
                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Recalculated tau from '
                            f'{processes[CPUstatus[3]][5]}ms to {tau}ms '
                            f'for process {processes[CPUstatus[3]][0]}',
                            printReadyQueue(readyQueue))
                    processes[CPUstatus[3]][5] = tau

                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Process {processes[CPUstatus[3]][0]} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + block_time}ms',
                            printReadyQueue(readyQueue))
                    blockDict[processes[CPUstatus[3]][0]] = \
                        time + block_time, processes[CPUstatus[3]][0]
            # time == the time CPU ready for the next process
            if time == CPUstatus[2] + 2:
                CPUstatus[0] = False

        # new arrival when CPU being used
        for v in blockDict.values():
            if time == v[0]:
                readyQueue.append(v[1])
                readyQueue.sort(key=lambda x: (processes[x][5], x))
                if time <= DISPLAY_MAX_T:
                    print(
                        f'time {time}ms: Process {v[1]} (tau {processes[v[1]][5]}ms) '
                        f'completed I/O; added to ready queue',
                        printReadyQueue(readyQueue))

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
        if not CPUstatus[0] and len(readyQueue) > 0:
            nextProcess = CPUstatus[3] = readyQueue.pop(0)  # get the name of next process store it to CPUstatus[3]
            CPUstatus[0] = True  # CPU in used
            CPUstatus[1] = time + 2  # start time
            CPUstatus[2] = time + processes[nextProcess][3][0] + 2  # end time
            processes[nextProcess][3].pop(0)  # pop first cpu burst
            processes[nextProcess][2] -= 1  # number of cpu bursts - 1

            # number of context switch + 1
            numContextSwitches += 1

            if curr_proc != '' and nextProcess != curr_proc:
                CPUstatus[1] += 2
                CPUstatus[2] += 2

        # no processes left
        if len(processes.keys()) == 0:
            print(f"time {time + 1}ms: Simulator ended for SJF [Q empty]")
            break

        for _ in set(old_read_queue).intersection(readyQueue):
            waitTime += 1

        time += 1

    avgCPUBurstTime = cpu_burst_time[0] / cpu_burst_time[1]
    avgWaitTime = waitTime / sum([p.get()[2] for p in processList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round(100 * useful_time / (time + 1), 3)

    data = avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization
    writeData(f, "SJF", data)