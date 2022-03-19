
'''
The RR algorithm is essentially the FCFS algorithm with predeﬁned time slice t slice . Each process is given t slice amount of time to complete its CPU burst. If this time slice expires, the process is preempted and added to the end of the ready queue.
If a process completes its CPU burst before a time slice expiration, the next process on the ready queue is immediately context-switched in to use the CPU.
'''

from helpers import *

def RR(processList, f, timeSlice):
    
    numContextSwitches = 0
    count_preemption = 0
    CPUBurstStart = 0
    CPUBurstEnd = 0
    waitTime = 0
    useful_time = 0

    print(f"time 0ms: Simulator started for RR with time slice {timeSlice}ms [Q empty]")

    arrivalTimeDict = {}
    processes = {}
    readyQueue = []
    for thread in processList:
        arrivalTimeDict[thread.get()[1]] = thread.get()
        processes[thread.get()[0]] = [*thread.get()]

    time = 0
    isRunning = False
    blockDict = {}

    while True:

        prevReadyQueue = readyQueue

        currentProcess = ''

        # If there are no processes left, then simulator is done
        if not processes:
            print(f"time {time + 1}ms: Simulator ended for RR [Q empty]")
            break

        # print changes to the process
        if isRunning and time == runningStart:
            CPUBurstStart += runningEnd - runningStart
            useful_time += runningEnd - runningStart
            CPUBurstEnd += 1
            if time <= DISPLAY_MAX_T:
                print(
                    f'time {time}ms: Process {processes[runningProcess][0]} '
                    f'started using the CPU for {runningEnd - runningStart}ms burst',
                    printReadyQueue(readyQueue))

        if isRunning:
            # preemption occur when ready queue isn't empty
            if time - runningStart == timeSlice:
                if len(readyQueue) > 0:
                    CPUBurstStart -= runningEnd - time
                    count_preemption += 1
                    currentProcess = runningProcess
                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Time slice expired; '
                            f'process {currentProcess} preempted with {processes[currentProcess][3][0]-(time-runningStart)}ms to go',
                            printReadyQueue(readyQueue))
                    
                    # context switch
                    processes[currentProcess][3][0] -= timeSlice
                    isRunning = False
                    readyQueue.append(currentProcess)

                else: # no preemption
                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Time slice expired; '
                            f'no preemption because ready queue is empty',
                            printReadyQueue(readyQueue))

        if isRunning:
            # complete a CPU burst
            if time == runningEnd:

                currentProcess = runningProcess
                processes[currentProcess][2] -= 1
                processes[currentProcess][3].pop(0)

                if len(processes[currentProcess][3]) == 0:
                    print(f'time {time}ms: Process {currentProcess} terminated',
                          printReadyQueue(readyQueue))
                    del processes[currentProcess]
                else:
                    if time <= DISPLAY_MAX_T:
                        if processes[currentProcess][2] > 1:
                            print(
                                f'time {time}ms: Process {currentProcess} '
                                f'completed a CPU burst; '
                                f'{processes[currentProcess][2]} bursts to go',
                            printReadyQueue(readyQueue))
                        else:
                            print(
                                f'time {time}ms: Process {currentProcess} '
                                f'completed a CPU burst; '
                                f'{processes[currentProcess][2]} burst to go',
                                printReadyQueue(readyQueue))
                    blockTime = processes[currentProcess][4][0] + 2

                    processes[currentProcess][4].pop(0)

                    if time <= DISPLAY_MAX_T:
                        print(
                            f'time {time}ms: Process {currentProcess} '
                            f'switching out of CPU; will block on I/O '
                            f'until time {time + blockTime}ms',
                            printReadyQueue(readyQueue))
                    blockDict[currentProcess] = \
                        time + blockTime, currentProcess

        if isRunning:
            if time == runningEnd + 2:
                isRunning = False

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
            printProcessArrived(time, arrivalTimeDict[time][0], -1, readyQueue)

        # no process is running and there is at least one ready process
        if not isRunning and len(readyQueue) > 0:
            nextProcess = readyQueue.pop(0)
            isRunning = True
            runningStart = time + 2  # start
            runningEnd = time + processes[nextProcess][3][0] + 2  # end
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
    CPUUtilization = round( 100 * useful_time / (time+1), 3)

    data = avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, count_preemption, CPUUtilization
    writeData(f, "RR", data)