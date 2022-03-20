
import copy

# DISPLAY_MAX_T = 1000
DISPLAY_MAX_T = float("inf")

def printStartSimulator(algo):
    print(f"time 0ms: Simulator started for {algo} [Q empty]")


def printEndSimulator(time, algo):
    print(f"time {time}ms: Simulator ended for {algo} [Q empty]")


def printReadyQueue(readyQueue):
    queue = copy.deepcopy(readyQueue)
    ret = '[Q '
    if not queue:
        ret += 'empty]'
    else:
        for item in queue:
            ret += item
        ret = ret + ']'
    return ret


def printTau(tau):
    if tau != -1:
        print(f'(tau {tau}ms) ', end='')


def printProcessArrived(time, process, tau, readyQueue):
    if time < DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(f'arrived; added to ready queue', printReadyQueue(readyQueue))


def printProcessTerminated(time, process, readyQueue):
    print(f'time {time}ms: Process {process} terminated', printReadyQueue(readyQueue))


def printStartCPU(time, process, tau, burstTime, readyQueue):
    if time < DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(f'started using the CPU for {burstTime}ms burst', printReadyQueue(readyQueue))


def printRestartCPU(time, process, timeLeft, burstTime, tau, readyQueue):
    if time < DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(
            f'started using the CPU for remaining {timeLeft}ms of '
            f'{burstTime}ms burst', printReadyQueue(readyQueue))


def printCPUComplete(time, process, tau, numCPUBursts, readyQueue):
    if time < DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(
            f'completed a CPU burst; '
            f'{numCPUBursts} '
            f'burst{"s" if numCPUBursts > 1 else ""} to go',
            printReadyQueue(readyQueue))

def printIOBlock(time, process, unblockTime, readyQueue):
    if time < DISPLAY_MAX_T:
        print(
            f'time {time}ms: Process {process} '
            f'switching out of CPU; will block on I/O '
            f'until time {unblockTime}ms',
            printReadyQueue(readyQueue))


def printIOComplete(time, process, tau, readyQueue):
    if time < DISPLAY_MAX_T:
        print(f'time {time}ms: Process {process} ', end='')
        printTau(tau)
        print(f'completed I/O; added to ready queue', printReadyQueue(readyQueue))


def printProcessPreempted(time, process, timeLeft, readyQueue):
    if time < DISPLAY_MAX_T:
        print(
            f'time {time}ms: Time slice expired; '
            f'process {process} preempted with {timeLeft}ms to go',
            printReadyQueue(readyQueue))


def printNoPreemption(time, readyQueue):
    if time < DISPLAY_MAX_T:
        print(
            f'time {time}ms: Time slice expired; '
            f'no preemption because ready queue is empty',
            printReadyQueue(readyQueue))


def printRecalculateTau(time, prevTau, newTau, process, readyQueue):
    if time < DISPLAY_MAX_T:
        print(
            f'time {time}ms: Recalculated tau from '
            f'{prevTau}ms to {newTau}ms '
            f'for process {process}',
            printReadyQueue(readyQueue))


def printPreemption(time, currentProcess, nextProcess, processes, readyQueue):
    if time < DISPLAY_MAX_T:
        print(
            f'time {time}ms: Process {nextProcess} (tau {processes[nextProcess].getTau()}ms) completed I/O; '
            f'preempting {currentProcess}', printReadyQueue(readyQueue))
