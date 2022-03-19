'''
The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
queue, waiting to use the CPU. This is your baseline algorithm (and could be implemented as RR
with an "infinite" time slice).
'''

from helpers import printReadyQueue, writeData, DISPLAY_MAX_T


def FCFS(procsList, f):

    numContextSwitches = 0
    cpu_burst_time = [0, 0]
    waitTime = 0
    useful_time = 0

    print("time 0ms: Simulator started for FCFS [Q empty]")

    arrival_time_map = {}
    processes = {}
    readyQueue = []
    for process in procsList:
        arrival_time_map[process.getArrivalTime()] = process.get()
        processes[process.getName()] = [*process.get()]

    time = 0
    running = [False, '', '', '']
    block_map = {}

    while True:

        old_read_queue = readyQueue

        currentProcess = ''

        # no processes left
        if len(processes) == 0:
            print(f"time {time + 1}ms: Simulator ended for FCFS [Q empty]")
            break

        # print changes to the process
        if running[0]:
            if time == running[1]:
                cpu_burst_time[0] += running[2] - running[1]
                useful_time += running[2] - running[1]
                cpu_burst_time[1] += 1
                if time <= DISPLAY_MAX_T:
                    print(
                        f'time {time}ms: Process {processes[running[3]][0]} '
                        f'started using the CPU for {running[2] - running[1]}ms burst',
                        printReadyQueue(readyQueue))

        if running[0]:
            if time == running[2]:
                currentProcess = running[3]

                if len(processes[running[3]][3]) == 0:
                    print(f'time {time}ms: Process {running[3]} terminated',
                          printReadyQueue(readyQueue))
                    del processes[running[3]]
                else:
                    if processes[running[3]][2] > 1:
                        if time <= DISPLAY_MAX_T:
                            print(
                                f'time {time}ms: Process {processes[running[3]][0]} '
                                f'completed a CPU burst; '
                                f'{processes[running[3]][2]} bursts to go',
                                printReadyQueue(readyQueue))
                    else:
                        if time <= DISPLAY_MAX_T:
                            print(
                                f'time {time}ms: Process {processes[running[3]][0]} '
                                f'completed a CPU burst; '
                                f'{processes[running[3]][2]} burst to go',
                                printReadyQueue(readyQueue))
                    block_time = processes[running[3]][4][0] + 2

                    processes[running[3]][4].pop(0)

                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Process {processes[running[3]][0]} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + block_time}ms',
                            printReadyQueue(readyQueue))
                    block_map[processes[running[3]][0]] = \
                        time + block_time, processes[running[3]][0]

        if running[0]:
            if time == running[2] + 2:
                running[0] = False

        doneProcesses = []
        for v in block_map.values():

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
        if time in arrival_time_map.keys():
            readyQueue.append(arrival_time_map[time][0])
            if time <= DISPLAY_MAX_T:
                print(
                    f'time {time}ms: Process {arrival_time_map[time][0]} arrived; '
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

            if currentProcess != '' and next_proc != currentProcess:
                running[1] += 2
                running[2] += 2

        for p in set(old_read_queue).intersection(readyQueue):
            waitTime += 1

        time += 1

    avgCPUBurstTime = cpu_burst_time[0] / cpu_burst_time[1]
    avgWaitTime = waitTime / sum([p.get()[2] for p in procsList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round( 100 * useful_time / (time+1), 3)

    data = avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, 0, CPUUtilization
    writeData(f, "FCFS", data)