
'''
The RR algorithm is essentially the FCFS algorithm with predeﬁned time slice t slice . Each process is given t slice amount of time to complete its CPU burst. If this time slice expires, the process is preempted and added to the end of the ready queue.
If a process completes its CPU burst before a time slice expiration, the next process on the ready queue is immediately context-switched in to use the CPU.
'''

from helpers import printReadyQueue, writeData, DISPLAY_MAX_T

def RR(procsList, f, timeSlice):
    numContextSwitches = 0
    count_preemption = 0
    cpu_burst_time = [0,0]
    waitTime = 0
    useful_time = 0

    print(f"time 0ms: Simulator started for RR with time slice {timeSlice}ms [Q empty]")

    arrivalTimeDict = {}
    processes = {}
    readyQueue = []
    for thread in procsList:
        arrivalTimeDict[thread.get()[1]] = thread.get()
        processes[thread.get()[0]] = [*thread.get()]

    time = 0
    running = [False, '', '', '']
    blockDict = {}

    while True:

        old_read_queue = readyQueue

        curr_proc = ''

        # no processes left
        if len(processes.keys()) == 0:
            print(f"time {time + 1}ms: Simulator ended for RR [Q empty]")
            break

        # print changes to the process
        if running[0] and time == running[1]:
            cpu_burst_time[0] += running[2] - running[1]
            useful_time += running[2] - running[1]
            cpu_burst_time[1] += 1
            if time <= DISPLAY_MAX_T:
                print(
                    f'time {time}ms: Process {processes[running[3]][0]} '
                    f'started using the CPU for {running[2] - running[1]}ms burst',
                    printReadyQueue(readyQueue))

        if running[0]:
            # preemption occur when ready queue isn't empty
            if time-running[1]==timeSlice:
                if len(readyQueue) > 0:
                    cpu_burst_time[0] -= running[2] - time
                    count_preemption += 1
                    curr_proc = running[3]
                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Time slice expired; '
                            f'process {curr_proc} preempted with {processes[curr_proc][3][0]-(time-running[1])}ms to go',
                            printReadyQueue(readyQueue))
                    
                    # context switch
                    processes[curr_proc][3][0] -= timeSlice
                    running[0] = False
                    readyQueue.append(curr_proc)

                else: # no preemption
                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Time slice expired; '
                            f'no preemption because ready queue is empty',
                            printReadyQueue(readyQueue))

        if running[0]:
            # complete a CPU burst
            if time == running[2]:

                curr_proc = running[3]
                processes[curr_proc][2] -= 1
                processes[curr_proc][3].pop(0)

                if len(processes[curr_proc][3]) == 0:
                    print(f'time {time}ms: Process {curr_proc} terminated',
                          printReadyQueue(readyQueue))
                    del processes[curr_proc]
                else:
                    if time <= DISPLAY_MAX_T:
                        if processes[curr_proc][2] > 1:
                            print(
                                f'time {time}ms: Process {processes[curr_proc][0]} '
                                f'completed a CPU burst; '
                                f'{processes[curr_proc][2]} bursts to go',
                            printReadyQueue(readyQueue))
                        else:
                            print(
                                f'time {time}ms: Process {processes[curr_proc][0]} '
                                f'completed a CPU burst; '
                                f'{processes[curr_proc][2]} burst to go',
                                printReadyQueue(readyQueue))
                    block_time = processes[curr_proc][4][0] + 2

                    processes[curr_proc][4].pop(0)

                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Process {processes[curr_proc][0]} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + block_time}ms',
                            printReadyQueue(readyQueue))
                    blockDict[processes[curr_proc][0]] = \
                        time + block_time, processes[curr_proc][0]

        if running[0]:
            if time == running[2] + 2:
                running[0] = False

        completed_proc = []
        for v in blockDict.values():

            # in case there are multiple processes ending at this time
            if time == v[0]:
                completed_proc.append(v[1])

        completed_proc.sort()
        readyQueue += completed_proc
        for proc in completed_proc:
            if time <= DISPLAY_MAX_T:
                print(
                    f'time {time}ms: Process {proc} '
                    f'completed I/O; added to ready queue',
                    printReadyQueue(readyQueue))

        # check if there is a process coming at this time
        if time in arrivalTimeDict.keys():
            readyQueue.append(arrivalTimeDict[time][0])
            if time <= DISPLAY_MAX_T:
                print(
                    f'time {time}ms: Process {arrivalTimeDict[time][0]} arrived; '
                    f'added to ready queue', printReadyQueue(readyQueue))

        # no process is running and there is at least one ready process
        if not running[0] and len(readyQueue) > 0:
            nextProcess = readyQueue[0]
            readyQueue.pop(0)
            running[0] = True
            running[1] = time + 2  # start
            running[2] = time + processes[nextProcess][3][0] + 2  # end
            running[3] = nextProcess

            # context switch
            numContextSwitches += 1

            if curr_proc != '' and nextProcess != curr_proc:
                running[1] += 2
                running[2] += 2

        for p in set(old_read_queue).intersection(readyQueue):
            waitTime += 1

        time += 1

    avgCPUBurstTime = cpu_burst_time[0] / cpu_burst_time[1]
    avgWaitTime = waitTime / sum([p.get()[2] for p in procsList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round( 100 * useful_time / (time+1), 3)

    data = avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, count_preemption, CPUUtilization
    writeData(f, "RR", data)