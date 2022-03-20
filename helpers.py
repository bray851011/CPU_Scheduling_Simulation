import math
from printHelpers import *

def updateTau(alpha, burstTime, tau):
    return math.ceil(alpha * burstTime + (1 - alpha) * tau)


def addWaitTime(prevReadyQueue, readyQueue):
    count = 0
    for process in set(prevReadyQueue):
        if process in readyQueue:
            count += 1
    return count


def getIncomingProcesses(time, processes, arrivalTimes, readyQueue, hasTau):
    if time in arrivalTimes.keys():
        tau = -1
        process = arrivalTimes[time].getName()
        readyQueue.append(process)
        if hasTau:
            readyQueue.sort(key=lambda x: (processes[x].getTau(), x))
            tau = arrivalTimes[time].getTau()
        printProcessArrived(time, process, tau, readyQueue)


def writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions, CPUUtilization):

    f.write(f'Algorithm {algo}\n')
    f.write(f'-- average CPU burst time: {"%.3f" % (math.ceil(1000 * avgCPUBurstTime) / 1000)} ms\n')
    f.write(f'-- average wait time: {"%.3f" % (math.ceil(1000 * avgWaitTime) / 1000)} ms\n')
    f.write(f'-- average turnaround time: {"%.3f" % (math.ceil(1000 * avgTurnaroundTime) / 1000)} ms\n')
    f.write(f'-- total number of context switches: {numContextSwitches}\n')
    f.write(f'-- total number of preemptions: {numPreemptions}\n')
    f.write(f'-- CPU utilization: {"%.3f" % (math.ceil(1000 * CPUUtilization) / 1000)}%\n')