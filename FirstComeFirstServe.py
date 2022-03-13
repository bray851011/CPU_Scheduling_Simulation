
'''
The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
queue, waiting to use the CPU. This is your baseline algorithm (and could be implemented as RR
with an “inﬁnite” time slice).
'''

from helpers import printReadyQueue, writeData, PRINT_UNTIL

def FCFS(procsList, f):

    numContextSwitches = 0
    cpu_burst_time = [0,0]
    wait_time = 0
    useful_time = 0

    print("time 0ms: Simulator started for FCFS [Q empty]")

    arrival_time_map = {}
    processes = {}
    readyQueue = []
    for thread in procsList:
        arrival_time_map[thread.get()[1]] = thread.get()
        processes[thread.get()[0]] = [*thread.get()]

    time = 0
    running = [False, '', '', '']
    block_map = {}

    while True:

        old_read_queue = readyQueue

        currentProcess = ''

        # no processes left
        if len(processes.keys()) == 0:
            print(f"time {time + 1}ms: Simulator ended for FCFS [Q empty]")
            break

        # print changes to the process
        if running[0]:
            if time == running[1]:
                cpu_burst_time[0] += running[2] - running[1]
                useful_time += running[2] - running[1]
                cpu_burst_time[1] += 1
                if time <= PRINT_UNTIL:
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
                        if time <= PRINT_UNTIL:
                            print(
                                f'time {time}ms: Process {processes[running[3]][0]} '
                                f'completed a CPU burst; '
                                f'{processes[running[3]][2]} bursts to go',
                                printReadyQueue(readyQueue))
                    else:
                        if time <= PRINT_UNTIL:
                            print(
                                f'time {time}ms: Process {processes[running[3]][0]} '
                                f'completed a CPU burst; '
                                f'{processes[running[3]][2]} burst to go',
                                printReadyQueue(readyQueue))
                    block_time = processes[running[3]][4][0] + 2

                    processes[running[3]][4].pop(0)

                    if time <= PRINT_UNTIL:
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
            if time <= PRINT_UNTIL:
                print(
                    f'time {time}ms: Process {proc} '
                    f'completed I/O; added to ready queue',
                    printReadyQueue(readyQueue))

        # check if there is a process coming at this time
        if time in arrival_time_map.keys():
            readyQueue.append(arrival_time_map[time][0])
            if time <= PRINT_UNTIL:
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
            wait_time += 1

        time += 1

    average_cpu_burst_time = cpu_burst_time[0] / cpu_burst_time[1]
    average_wait_time = wait_time / sum([p.get()[2] for p in procsList])
    average_turnaround_time = average_cpu_burst_time + average_wait_time + 4
    CPU_utilization = round( 100 * useful_time / (time+1), 3)

    data = average_cpu_burst_time, average_wait_time, average_turnaround_time, numContextSwitches, 0, CPU_utilization
    writeData(f, "FCFS", data)