
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



def writeData(f, algo, data):

    avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions, CPUUtilization = data
    f.write(f'Algorithm {algo}\n')
    f.write(f'-- average CPU burst time: {"%.3f" % round(avgCPUBurstTime, 3)} ms\n')
    f.write(f'-- average wait time: {"%.3f" % round(avgWaitTime, 3)} ms\n')
    f.write(f'-- average turnaround time: {"%.3f" % round(avgTurnaroundTime, 3)} ms\n')
    f.write(f'-- total number of context switches: {numContextSwitches}\n')
    f.write(f'-- total number of preemptions: {numPreemptions}\n')
    f.write(f'-- CPU utilization: {"%.3f" % CPUUtilization}%\n')
