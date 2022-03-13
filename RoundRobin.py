
'''
The RR algorithm is essentially the FCFS algorithm with predeﬁned time slice t slice . Each process is given t slice amount of time to complete its CPU burst. If this time slice expires, the process is preempted and added to the end of the ready queue.
If a process completes its CPU burst before a time slice expiration, the next process on the ready queue is immediately context-switched in to use the CPU.
'''

from helpers import printReadyQueue, writeData, PRINT_UNTIL

def RR(procsList, f, timeSlice):
    count_context_switch = 0
    count_preemption = 0
    cpu_burst_time = [0,0]
    wait_time = 0
    useful_time = 0

    print(f"time 0ms: Simulator started for RR with time slice {timeSlice}ms [Q empty]")

    arrival_time_map = {}
    procs_map = {}
    ready_queue = []
    for thread in procsList:
        arrival_time_map[thread.get()[1]] = thread.get()
        procs_map[thread.get()[0]] = [*thread.get()]

    time = 0
    running = [False, '', '', '']
    block_map = {}

    while True:

        old_read_queue = ready_queue

        curr_proc = ''

        # no processes left
        if len(procs_map.keys()) == 0:
            print(f"time {time + 1}ms: Simulator ended for RR [Q empty]")
            break

        # print changes to the process
        if running[0] and time == running[1]:
            cpu_burst_time[0] += running[2] - running[1]
            useful_time += running[2] - running[1]
            cpu_burst_time[1] += 1
            if time <= PRINT_UNTIL:
                print(
                    f'time {time}ms: Process {procs_map[running[3]][0]} '
                    f'started using the CPU for {running[2] - running[1]}ms burst',
                    printReadyQueue(ready_queue))

        if running[0]:
            # preemption occur when ready queue isn't empty
            if time-running[1]==timeSlice:
                if len(ready_queue) > 0:
                    cpu_burst_time[0] -= running[2] - time
                    count_preemption += 1
                    curr_proc = running[3]
                    if time <= PRINT_UNTIL:
                        print(
                            f'time {time}ms: Time slice expired; '
                            f'process {curr_proc} preempted with {procs_map[curr_proc][3][0]-(time-running[1])}ms to go',
                            printReadyQueue(ready_queue))
                    
                    # context switch
                    procs_map[curr_proc][3][0] -= timeSlice
                    running[0] = False
                    ready_queue.append(curr_proc)

                else: # no preemption
                    if time <= PRINT_UNTIL:
                        print(
                            f'time {time}ms: Time slice expired; '
                            f'no preemption because ready queue is empty',
                            printReadyQueue(ready_queue))

        if running[0]:
            # complete a CPU burst
            if time == running[2]:

                curr_proc = running[3]
                procs_map[curr_proc][2] -= 1
                procs_map[curr_proc][3].pop(0)

                if len(procs_map[curr_proc][3]) == 0:
                    print(f'time {time}ms: Process {curr_proc} terminated',
                          printReadyQueue(ready_queue))
                    del procs_map[curr_proc]
                else:
                    if time <= PRINT_UNTIL:
                        if procs_map[curr_proc][2] > 1:
                            print(
                                f'time {time}ms: Process {procs_map[curr_proc][0]} '
                                f'completed a CPU burst; '
                                f'{procs_map[curr_proc][2]} bursts to go',
                            printReadyQueue(ready_queue))
                        else:
                            print(
                                f'time {time}ms: Process {procs_map[curr_proc][0]} '
                                f'completed a CPU burst; '
                                f'{procs_map[curr_proc][2]} burst to go',
                                printReadyQueue(ready_queue))
                    block_time = procs_map[curr_proc][4][0] + 2

                    procs_map[curr_proc][4].pop(0)

                    if time <= PRINT_UNTIL:
                        print(
                            f'time {time}ms: Process {procs_map[curr_proc][0]} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + block_time}ms',
                            printReadyQueue(ready_queue))
                    block_map[procs_map[curr_proc][0]] = \
                        time + block_time, procs_map[curr_proc][0]

        if running[0]:
            if time == running[2] + 2:
                running[0] = False

        completed_proc = []
        for v in block_map.values():

            # in case there are multiple processes ending at this time
            if time == v[0]:
                completed_proc.append(v[1])

        completed_proc.sort()
        ready_queue += completed_proc
        for proc in completed_proc:
            if time <= PRINT_UNTIL:
                print(
                    f'time {time}ms: Process {proc} '
                    f'completed I/O; added to ready queue',
                    printReadyQueue(ready_queue))

        # check if there is a process coming at this time
        if time in arrival_time_map.keys():
            ready_queue.append(arrival_time_map[time][0])
            if time <= PRINT_UNTIL:
                print(
                    f'time {time}ms: Process {arrival_time_map[time][0]} arrived; '
                    f'added to ready queue', printReadyQueue(ready_queue))

        # no process is running and there is at least one ready process
        if not running[0] and len(ready_queue) > 0:
            next_proc = ready_queue[0]
            ready_queue.pop(0)
            running[0] = True
            running[1] = time + 2  # start
            running[2] = time + procs_map[next_proc][3][0] + 2  # end
            running[3] = next_proc

            # context switch
            count_context_switch += 1

            if curr_proc != '' and next_proc != curr_proc:
                running[1] += 2
                running[2] += 2

        for p in set(old_read_queue).intersection(ready_queue):
            wait_time += 1

        time += 1

    average_cpu_burst_time = cpu_burst_time[0] / cpu_burst_time[1]
    average_wait_time = wait_time / sum([p.get()[2] for p in procsList])
    average_turnaround_time = average_cpu_burst_time + average_wait_time + 4
    CPU_utilization = round( 100 * useful_time / (time+1), 3)

    data = average_cpu_burst_time, average_wait_time, average_turnaround_time, count_context_switch, count_preemption, CPU_utilization
    writeData(f, "RR", data)