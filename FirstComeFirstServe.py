
'''
The FCFS algorithm is a non-preemptive algorithm in which processes simply line up in the ready
queue, waiting to use the CPU. This is your baseline algorithm (and could be implemented as RR
with an “inﬁnite” time slice).
'''

from helpers import print_ready_Q, writeData

def FCFS(procsList, f):

    count_context_switch = 0
    cpu_burst_time = [0,0]
    wait_time = 0
    useful_time = 0

    print("time 0ms: Simulator started for FCFS [Q empty]")

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
            print(f"time {time + 1}ms: Simulator ended for FCFS [Q empty]")
            break

        # print changes to the process
        if running[0]:
            if time == running[1]:
                cpu_burst_time[0] += running[2] - running[1]
                useful_time += running[2] - running[1]
                cpu_burst_time[1] += 1
                if time <= 1000:
                    print(
                        f'time {time}ms: Process {procs_map[running[3]][0]} '
                        f'started using the CPU for {running[2] - running[1]}ms burst',
                        print_ready_Q(ready_queue))

        if running[0]:
            if time == running[2]:
                curr_proc = running[3]

                if len(procs_map[running[3]][3]) == 0:
                    print(f'time {time}ms: Process {running[3]} terminated',
                          print_ready_Q(ready_queue))
                    del procs_map[running[3]]
                else:
                    if procs_map[running[3]][2] > 1:
                        if time <= 1000:
                            print(
                                f'time {time}ms: Process {procs_map[running[3]][0]} '
                                f'completed a CPU burst; '
                                f'{procs_map[running[3]][2]} bursts to go',
                                print_ready_Q(ready_queue))
                    else:
                        if time <= 1000:
                            print(
                                f'time {time}ms: Process {procs_map[running[3]][0]} '
                                f'completed a CPU burst; '
                                f'{procs_map[running[3]][2]} burst to go',
                                print_ready_Q(ready_queue))
                    block_time = procs_map[running[3]][4][0] + 2

                    procs_map[running[3]][4].pop(0)

                    if time <= 1000:
                        print(
                            f'time {time}ms: Process {procs_map[running[3]][0]} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + block_time}ms',
                            print_ready_Q(ready_queue))
                    block_map[procs_map[running[3]][0]] = \
                        time + block_time, procs_map[running[3]][0]

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
            if time <= 1000:
                print(
                    f'time {time}ms: Process {proc} '
                    f'completed I/O; added to ready queue',
                    print_ready_Q(ready_queue))

        # check if there is a process coming at this time
        if time in arrival_time_map.keys():
            ready_queue.append(arrival_time_map[time][0])
            if time <= 1000:
                print(
                    f'time {time}ms: Process {arrival_time_map[time][0]} arrived; '
                    f'added to ready queue', print_ready_Q(ready_queue))

        # no process is running and there is at least one ready process
        if not running[0] and len(ready_queue) > 0:
            next_proc = ready_queue[0]
            ready_queue.pop(0)
            running[0] = True
            running[1] = time + 2  # start
            running[2] = time + procs_map[next_proc][3][0] + 2  # end
            procs_map[next_proc][3].pop(0)
            procs_map[next_proc][2] -= 1
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

    data = average_cpu_burst_time, average_wait_time, average_turnaround_time, count_context_switch, 0, CPU_utilization
    writeData(f, "FCFS", data)