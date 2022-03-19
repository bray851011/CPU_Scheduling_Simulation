
'''
The RR algorithm is essentially the FCFS algorithm with predeﬁned time slice t slice . Each process is given t slice amount of time to complete its CPU burst. If this time slice expires, the process is preempted and added to the end of the ready queue.
If a process completes its CPU burst before a time slice expiration, the next process on the ready queue is immediately context-switched in to use the CPU.
'''

from helpers import *

def RR(processList, f, timeSlice):
    
    algo = 'RR'
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
    for process in processList:
        arrivalTimeDict[process.getArrivalTime()] = process.get()
        processes[process.getName()] = [*process.get()]

    time = 0
    usingCPU = False
    blockDict = {}

    while True:

        prevReadyQueue = readyQueue
        currentProcess = ''

        # If there are no processes left, then simulator is done
        if not processes:
            printEndSimulator(time + 1, algo)
            break

        if usingCPU:
            if time == runningStart:
                burstTime = runningEnd - runningStart
                CPUBurstStart += burstTime
                useful_time += burstTime
                CPUBurstEnd += 1
                printStartCPU(time, runningProcess, -1, burstTime, readyQueue)
            
            # preemption occur when ready queue isn't empty
            if time == timeSlice + runningStart:
                if readyQueue:
                    CPUBurstStart -= runningEnd - time
                    count_preemption += 1
                    currentProcess = runningProcess
                    printProcessPreempted(time, currentProcess, processes[currentProcess][3][0]-(time-runningStart), readyQueue)
                    
                    # context switch
                    processes[currentProcess][3][0] -= timeSlice
                    usingCPU = False
                    readyQueue.append(currentProcess)

                else: # no preemption
                    printNoPreemption(time, readyQueue)
            
            # complete a CPU burst
            if time == runningEnd:

                currentProcess = runningProcess
                processes[currentProcess][2] -= 1
                processes[currentProcess][3].pop(0)

                if len(processes[currentProcess][3]) == 0:
                    printProcessTerminated(time, currentProcess, readyQueue)
                    del processes[currentProcess]
                else:
                    printCPUComplete(time, currentProcess, -1, processes[currentProcess][2], readyQueue)
                    
                    blockTime = processes[currentProcess][4][0] + 2

                    processes[currentProcess][4].pop(0)

                    printIOBlock(time, currentProcess, time + blockTime, readyQueue)

                    blockDict[currentProcess] = time + blockTime, currentProcess

            if time == runningEnd + 2:
                usingCPU = False

        doneProcesses = []
        for v in blockDict.values():

            # in case there are multiple processes ending at this time
            if time == v[0]:
                doneProcesses.append(v[1])

        doneProcesses.sort()
        readyQueue += doneProcesses
        for proc in doneProcesses:
            printIOComplete(time, proc, -1, readyQueue)

        # check if there is a process coming at this time
        if time in arrivalTimeDict.keys():
            readyQueue.append(arrivalTimeDict[time][0])
            printProcessArrived(time, arrivalTimeDict[time][0], -1, readyQueue)

        # no process is running and there is at least one ready process
        if not usingCPU and len(readyQueue) > 0:
            nextProcess = readyQueue.pop(0)
            usingCPU = True
            runningStart = time + 2  # start
            runningEnd = time + processes[nextProcess][3][0] + 2  # end
            runningProcess = nextProcess

            # context switch
            numContextSwitches += 1

            if currentProcess != '' and nextProcess != currentProcess:
                runningStart += 2
                runningEnd += 2

        waitTime += addWaitTime(prevReadyQueue, readyQueue)

        time += 1


    avgCPUBurstTime = CPUBurstStart / CPUBurstEnd
    avgWaitTime = waitTime / sum([p.get()[2] for p in processList])
    avgTurnaroundTime = avgCPUBurstTime + avgWaitTime + 4
    CPUUtilization = round( 100 * useful_time / (time+1), 3)

    writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, count_preemption, CPUUtilization)
