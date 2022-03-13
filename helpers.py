
PRINT_UNTIL = 1000

def printReadyQueue(ready_queue):
    res = '[Q '
    if len(ready_queue) == 0:
        res += 'empty]'
    else:
        for item in ready_queue:
            res += item
        res = res + ']'
    return res



def writeData(f, algo, data):

    average_cpu_burst_time, average_wait_time, average_turnaround_time, count_context_switch, count_preemptions, CPU_utilization = data
    f.write(f'Algorithm {algo}\n')
    f.write(f'-- average CPU burst time: {"%.3f" % round(average_cpu_burst_time, 3)} ms\n')
    f.write(f'-- average wait time: {"%.3f" % round(average_wait_time, 3)} ms\n')
    f.write(f'-- average turnaround time: {"%.3f" % round(average_turnaround_time, 3)} ms\n')
    f.write(f'-- total number of context switches: {count_context_switch}\n')
    f.write(f'-- total number of preemptions: {count_preemptions}\n')
    f.write(f'-- CPU utilization: {"%.3f" % CPU_utilization}%\n')
