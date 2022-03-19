
import math

DISPLAY_MAX_T = 1000

def printStartSimulator(algo):
    print(f"time 0ms: Simulator started for {algo} [Q empty]")


def printEndSimulator(time, algo):
    print(f"time {time}ms: Simulator ended for {algo} [Q empty]")


def printReadyQueue(readyQueue):
    ret = '[Q '
    if not readyQueue:
        ret += 'empty]'
    else:
        for item in readyQueue:
            ret += item
        ret = ret + ']'
    return ret


def printTau(tau):
    if tau != -1:
        print(f'(tau {tau}ms) ', end='')


def printProcessArrived(time, process, tau, readyQueue):
    if time <= DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(f'arrived; added to ready queue', printReadyQueue(readyQueue))


def printProcessTerminated(time, process, readyQueue):
    print(f'time {time}ms: Process {process} terminated', printReadyQueue(readyQueue))


def printStartCPU(time, process, tau, burstTime, readyQueue):
    if time <= DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(f'started using the CPU for {burstTime}ms burst', printReadyQueue(readyQueue))


def printCPUComplete(time, process, tau, numCPUBursts, readyQueue):
    if time <= DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(
            f'completed a CPU burst; '
            f'{numCPUBursts} '
            f'burst{"s" if numCPUBursts > 1 else ""} to go',
            printReadyQueue(readyQueue))

def printIOBlock(time, process, unblockTime, readyQueue):
    if time <= DISPLAY_MAX_T:
        print(
            f'time {time}ms: Process {process} '
            f'switching out of CPU; will block on I/O '
            f'until time {unblockTime}ms',
            printReadyQueue(readyQueue))


def printIOComplete(time, process, tau, readyQueue):
    if time <= DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(f'completed I/O; added to ready queue', printReadyQueue(readyQueue))


def printProcessPreempted(time, process, timeLeft, readyQueue):
    if time <= DISPLAY_MAX_T:
        print(
            f'time {time}ms: Time slice expired; '
            f'process {process} preempted with {timeLeft}ms to go',
            printReadyQueue(readyQueue))


def printNoPreemption(time, readyQueue):
    if time <= DISPLAY_MAX_T:
        print(
            f'time {time}ms: Time slice expired; '
            f'no preemption because ready queue is empty',
            printReadyQueue(readyQueue))


def printRecalculateTau(time, prevTau, newTau, process, readyQueue):
    if time <= DISPLAY_MAX_T:
        print(
            f'time {time}ms: Recalculated tau from '
            f'{prevTau}ms to {newTau}ms '
            f'for process {process}',
            printReadyQueue(readyQueue))


def updateTau(alpha, burstTime, tau):
    return math.ceil(alpha * burstTime + (1 - alpha) * tau)


def addWaitTime(prevReadyQueue, readyQueue):
    count = 0
    for process in prevReadyQueue:
        if process in readyQueue:
            count += 1
    return count


def writeData(f, algo, avgCPUBurstTime, avgWaitTime, avgTurnaroundTime, numContextSwitches, numPreemptions, CPUUtilization):

    f.write(f'Algorithm {algo}\n')
    f.write(f'-- average CPU burst time: {"%.3f" % round(avgCPUBurstTime, 3)} ms\n')
    f.write(f'-- average wait time: {"%.3f" % round(avgWaitTime, 3)} ms\n')
    f.write(f'-- average turnaround time: {"%.3f" % round(avgTurnaroundTime, 3)} ms\n')
    f.write(f'-- total number of context switches: {numContextSwitches}\n')
    f.write(f'-- total number of preemptions: {numPreemptions}\n')
    f.write(f'-- CPU utilization: {"%.3f" % CPUUtilization}%\n')
