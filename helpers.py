
import math
from printHelpers import *

def updateTau(alpha, burstTime, tau):
    return math.ceil(alpha * burstTime + (1 - alpha) * tau)


DISPLAY_MAX_T = 1000


def printReadyQueue(readyQueue):
    ret = '[Q '
    if len(readyQueue) == 0:
        ret += 'empty]'
    else:
        for item in readyQueue:
            ret += item
        ret = ret + ']'
    return ret

def addWaitTime(prevReadyQueue, readyQueue):
    count = 0
    for process in prevReadyQueue:
        if process in readyQueue:
            count += 1
    return count


def checkIncomingProcesses(time, arrivalTimeDict, readyQueue):
    if time in arrivalTimeDict.keys():
        readyQueue.append(arrivalTimeDict[time][0])
        printProcessArrived(time, arrivalTimeDict[time][0], -1, readyQueue)


def writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions, CPUUtilization):

    f.write(f'Algorithm {algo}\n')
    f.write(f'-- average CPU burst time: {"%.3f" % round(avgCPUBurstTime, 3)} ms\n')
    f.write(f'-- average wait time: {"%.3f" % round(avgWaitTime, 3)} ms\n')
    f.write(f'-- average turnaround time: {"%.3f" % round(avgTurnaroundTime, 3)} ms\n')
    f.write(f'-- total number of context switches: {numContextSwitches}\n')
    f.write(f'-- total number of preemptions: {numPreemptions}\n')
    f.write(f'-- CPU utilization: {"%.3f" % CPUUtilization}%\n')
