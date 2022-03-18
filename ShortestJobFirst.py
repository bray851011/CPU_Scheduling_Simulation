
'''
In SJF, processes are stored in the ready queue in order of priority based on their anticipated
CPU burst times. More speciﬁcally, the process with the shortest CPU burst time will be
selected as the next process executed by the CPU.
'''

import math
from helpers import printReadyQueue, writeData, DISPLAY_MAX_T

def SJF(procsList, f, alpha):

    # analysis variable
    numContextSwitches = 0
    cpu_burst_time = [0, 0]
    waitTime = 0
    useful_time = 0

    print("time 0ms: Simulator started for SJF [Q empty]")

    arrival_time_map = {}
    processes = {}
    readyQueue = []
    for thread in procsList:
        arrival_time_map[thread.get()[1]] = thread.get()
        processes[thread.get()[0]] = [*thread.get()]

    time = 0

    # running[0] -- whether CPU is in use
    # running[1] -- if running[0], then this represents the start time of this running
    # running[2] -- if running[0], then this represents the end time of this running
    # running[3] -- if running[0], then this represents the process name of this running
    running = [False, '', '', '']

    # when a process is blocked, add to this map with its time
    block_map = {}

    while True:

        old_read_queue = readyQueue

        curr_proc = ''

        # no processes left
        if len(processes.keys()) == 0:
            print(f"time {time + 1}ms: Simulator ended for SJF [Q empty]")
            break

        # start running a process -- time == start time of the process
        if running[0]:
            if time == running[1]:
                curr_proc = running[3]
                cpu_burst_time[0] += running[2] - running[1]
                useful_time += running[2] - running[1]
                cpu_burst_time[1] += 1
                if time <= DISPLAY_MAX_T:
                    print(
                        f'time {time}ms: Process {processes[running[3]][0]} '
                        f'(tau {processes[running[3]][5]}ms) started using the CPU '
                        f'for {running[2] - running[1]}ms burst',
                        printReadyQueue(readyQueue))

        # end running a process -- time == end time of the process
        if running[0]:
            if time == running[2]:
                curr_proc = running[3]

                # check if the process reaches the end -- cpu burst time list is empty
                if len(processes[running[3]][3]) == 0:
                    print(f'time {time}ms: Process {running[3]} terminated',
                          printReadyQueue(readyQueue))
                    del processes[running[3]]
                else:
                    if processes[running[3]][2] > 1:
                        if time <= DISPLAY_MAX_T:
                            print(
                                f'time {time}ms: Process {processes[running[3]][0]} '
                                f'(tau {processes[running[3]][5]}ms) '
                                f'completed a CPU burst; '
                                f'{processes[running[3]][2]} bursts to go',
                                printReadyQueue(readyQueue))
                    else:
                        if time <= DISPLAY_MAX_T:
                            print(
                                f'time {time}ms: Process {processes[running[3]][0]} '
                                f'(tau {processes[running[3]][5]}ms) '
                                f'completed a CPU burst; '
                                f'{processes[running[3]][2]} burst to go',
                                printReadyQueue(readyQueue))
                    block_time = processes[running[3]][4][0] + 2

                    processes[running[3]][4].pop(0)

                    # update tau <- alpha * burst time + (1 - alpha) * tau
                    tau = math.ceil(alpha * (running[2] - running[1]) +
                                    (1 - alpha) * processes[running[3]][5])
                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Recalculated tau from '
                            f'{processes[running[3]][5]}ms to {tau}ms '
                            f'for process {processes[running[3]][0]}',
                            printReadyQueue(readyQueue))
                    processes[running[3]][5] = tau

                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Process {processes[running[3]][0]} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + block_time}ms',
                            printReadyQueue(readyQueue))
                    block_map[processes[running[3]][0]] = \
                        time + block_time, processes[running[3]][0]

        # wait for another 2ms for cpu to be reused
        if running[0]:
            if time == running[2] + 2:
                running[0] = False

        for v in block_map.values():
            if time == v[0]:
                readyQueue.append(v[1])
                readyQueue.sort(key=lambda x: (processes[x][5], x))
                if time <= DISPLAY_MAX_T:
                    print(
                        f'time {time}ms: Process {v[1]} (tau {processes[v[1]][5]}ms) '
                        f'completed I/O; added to ready queue',
                        printReadyQueue(readyQueue))

        # check if there is a process coming at this time
        if time in arrival_time_map.keys():
            readyQueue.append(arrival_time_map[time][0])
            readyQueue.sort(key=lambda x: (processes[x][5], x))
            if time <= DISPLAY_MAX_T:
                print(
                    f'time {time}ms: Process {arrival_time_map[time][0]} '
                    f'(tau {arrival_time_map[time][5]}ms) arrived; '
                    f'added to ready queue', printReadyQueue(readyQueue))

        # no process is running and there is at least one ready process
        if not running[0] and len(readyQueue) > 0:
            next_proc = readyQueue[0]
            readyQueue.pop(0)
            running[0] = True
            running[1] = time + 2  # start
            running[2] = time + processes[next_proc][3][0] + 2  # end
            processes[next_proc][3].pop(0)
            processes[next_proc][2] -= 1
            running[3] = next_proc

            # context switch
            numContextSwitches += 1

            if curr_proc != '' and next_proc != curr_proc:
                running[1] += 2
                running[2] += 2

        for _ in set(old_read_queue).intersection(readyQueue):
            waitTime += 1

        time += 1

    avgCPUBurstTime = cpu_burst_time[0] / cpu_burst_time[1]
    avgWaitTime = waitTime / sum([p.get()[2] for p in procsList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round(100 * useful_time / (time + 1), 3)

    data = avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization
    writeData(f, "SJF", data)