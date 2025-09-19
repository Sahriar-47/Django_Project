from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# Index page
def index(request):
    return render(request, 'Algorithms/index.html')


# optional -> if we find any need, we will use it.
# def result(request):
# return render(request, 'Algorithms/result.html')


# FCFS Algorithm
def fcfs(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))

        n = len(at_list)
        processes = list(zip(at_list, bt_list, range(n)))  # (arrival_time, burst_time, index)
        processes.sort()  # Sort by arrival time

        completion_times = [0] * n
        waiting_times = [0] * n
        turnaround_times = [0] * n

        time = 0  # CPU time tracker

        for arrival_time, burst_time, idx in processes:
            if time < arrival_time:
                time = arrival_time  # CPU waits if no process has arrived

            time += burst_time
            completion_times[idx] = time

            turnaround_times[idx] = completion_times[idx] - arrival_time
            waiting_times[idx] = turnaround_times[idx] - burst_time

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'Algorithms/result.html', {
            'avg_waiting_time': round(avg_waiting_time, 2),
            'avg_turnaround_time': round(avg_turnaround_time, 2),
        })
    return render(request, 'Algorithms/fcfs.html')


# priority scheduling algorithm
def priority(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))
        pr_list = list(map(int, request.POST['priority'].split(',')))

        n = len(at_list)
        processes = list(range(n))

        # Sort processes by arrival time and priority
        processes.sort(key=lambda x: (at_list[x], pr_list[x]))

        completion_times = [0] * n
        waiting_times = [0] * n
        turnaround_times = [0] * n

        current_time = 0
        for i in processes:
            if current_time < at_list[i]:
                current_time = at_list[i]
            current_time += bt_list[i]
            completion_times[i] = current_time

        for i in range(n):
            turnaround_times[i] = completion_times[i] - at_list[i]
            waiting_times[i] = turnaround_times[i] - bt_list[i]

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })

    return render(request, 'algorithms/priority.html')


# Non-Preemptive Shortest Job First Algorithm
def sjf(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))

        n = len(at_list)
        processes = list(zip(range(n), at_list, bt_list))  # Process ID, Arrival Time, Burst Time
        processes.sort(key=lambda x: (x[1], x[2]))  # Sort by Arrival Time, then Burst Time

        current_time = 0
        waiting_times = [0] * n
        turnaround_times = [0] * n
        completed = []

        # Process scheduling
        while len(completed) < n:
            available = [p for p in processes if p[1] <= current_time and p not in completed]
            if available:
                shortest = min(available, key=lambda x: x[2])  # Select process with the shortest burst time
                pid, at, bt = shortest
                current_time += bt
                turnaround_times[pid] = current_time - at
                waiting_times[pid] = turnaround_times[pid] - bt
                completed.append(shortest)
            else:
                current_time += 1  # If no process is available, increment time

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })

    return render(request, 'algorithms/sjf.html')


# preemptive sjf algorithm
def preemptive_sjf(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))

        n = len(at_list)
        remaining_time = bt_list[:]  # To keep track of remaining burst times
        waiting_times = [0] * n
        turnaround_times = [0] * n

        current_time = 0
        completed = 0
        shortest = -1
        finish_time = 0
        check = False

        # Process scheduling
        while completed != n:
            # Find the process with the shortest remaining time at the current time
            for i in range(n):
                if at_list[i] <= current_time and remaining_time[i] > 0:
                    if shortest == -1 or remaining_time[i] < remaining_time[shortest]:
                        shortest = i
                        check = True

            if not check:
                current_time += 1
                continue

            # Execute the shortest process
            remaining_time[shortest] -= 1
            current_time += 1

            # If the process is completed
            if remaining_time[shortest] == 0:
                completed += 1
                finish_time = current_time
                turnaround_times[shortest] = finish_time - at_list[shortest]
                waiting_times[shortest] = turnaround_times[shortest] - bt_list[shortest]

            shortest = -1
            check = False

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })

    return render(request, 'algorithms/preemptive_sjf.html')


# round_robin Algorithm
def round_robin(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))
        quantum = int(request.POST['quantum_time'])

        n = len(at_list)
        remaining_time = bt_list[:]  # Copy of burst times
        waiting_times = [0] * n
        turnaround_times = [0] * n

        # Track the current time and queue for processes
        time = 0
        queue = []
        completed = 0
        visited = [False] * n

        # Add processes to the queue as they arrive
        while completed != n:
            # Add all processes that have arrived
            for i in range(n):
                if at_list[i] <= time and not visited[i]:
                    queue.append(i)
                    visited[i] = True

            if not queue:
                time += 1
                continue

            # Process the first process in the queue
            current = queue.pop(0)
            execution_time = min(quantum, remaining_time[current])
            remaining_time[current] -= execution_time
            time += execution_time

            # Add newly arrived processes during this time to the queue
            for i in range(n):
                if at_list[i] <= time and not visited[i]:
                    queue.append(i)
                    visited[i] = True

            # If the process is not finished, re-add it to the queue
            if remaining_time[current] > 0:
                queue.append(current)
            else:
                # Process finished
                completed += 1
                turnaround_times[current] = time - at_list[current]
                waiting_times[current] = turnaround_times[current] - bt_list[current]

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })
    return render(request, 'algorithms/round_robin.html')

import ast
def parse_2d_list(text):
    try:
        result = ast.literal_eval(text)
        if not isinstance(result, list) or not all(isinstance(row, list) for row in result):
            raise ValueError
        return result
    except:
        return None

def bankers(request):
    context = {}
    if request.method == "POST":
        try:
            processes = request.POST.get("processes[]", "").split(",")
            processes = [p.strip() for p in processes]
            available = list(map(int, request.POST.get("available[]", "").split(",")))
            allocation = parse_2d_list(request.POST.get("allocation", "[]"))
            max_demand = parse_2d_list(request.POST.get("max_demand", "[]"))

            if not allocation or not max_demand or len(allocation) != len(max_demand) or len(allocation) != len(processes):
                context["error"] = "Mismatch or invalid format in inputs."
                return render(request, "Algorithms/bankers_form.html", context)

            n = len(processes)
            m = len(available)

            need = [[max_demand[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
            finish = [False] * n
            safe_seq = []
            work = available[:]

            while len(safe_seq) < n:
                progress = False
                for i in range(n):
                    if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                        for j in range(m):
                            work[j] += allocation[i][j]
                        finish[i] = True
                        safe_seq.append(processes[i])
                        progress = True
                if not progress:
                    break

            if len(safe_seq) == n:
                context["message"] = "System is in a safe state."
                context["success"] = True
                context["sequence"] = safe_seq
            else:
                context["message"] = "System is NOT in a safe state."
                context["success"] = False

        except Exception as e:
            context["error"] = f"Error: {str(e)}"
    return render(request, "Algorithms/bankers_form.html", context)

def fcfs_disk_scheduling(request):
    result = None
    if request.method == 'POST':
        try:
            requests = request.POST.get('requests')
            head = int(request.POST.get('head'))

            # Parse requests into a list of integers
            request_sequence = list(map(int, requests.split(',')))

            seek_sequence = []
            seek_time = 0
            current_position = head

            for track in request_sequence:
                seek_sequence.append(track)
                seek_time += abs(current_position - track)
                current_position = track

            result = {
                'seek_sequence': seek_sequence,
                'total_seek_time': seek_time,
            }

        except Exception as e:
            result = {'error': f'Error: {str(e)}'}

    return render(request, 'Algorithms/fcfs_disk.html', {'result': result})

def sstf_disk_scheduling(request):
    result = None
    if request.method == 'POST':
        try:
            requests = request.POST.get('requests')
            head = int(request.POST.get('head'))

            request_sequence = list(map(int, requests.split(',')))
            seek_sequence = []
            total_seek_time = 0
            current_position = head
            pending = request_sequence.copy()

            while pending:
                # Find the closest request
                distances = [(abs(track - current_position), track) for track in pending]
                distances.sort()
                closest = distances[0][1]

                seek_sequence.append(closest)
                total_seek_time += abs(current_position - closest)
                current_position = closest
                pending.remove(closest)

            result = {
                'seek_sequence': seek_sequence,
                'total_seek_time': total_seek_time,
            }

        except Exception as e:
            result = {'error': f'Error: {str(e)}'}
    return render(request, 'Algorithms/sstf_disk.html', {'result': result})
def scan_disk_scheduling(request):
    result = None
    if request.method == 'POST':
        try:
            requests = request.POST.get('requests')
            head = int(request.POST.get('head'))
            direction = request.POST.get('direction')  # 'left' or 'right'
            disk_size = int(request.POST.get('disk_size'))

            request_sequence = list(map(int, requests.split(',')))
            request_sequence.append(head)
            request_sequence.sort()

            head_index = request_sequence.index(head)
            seek_sequence = []
            total_seek_time = 0
            current_position = head

            if direction == 'left':
                left = request_sequence[:head_index][::-1]
                right = request_sequence[head_index + 1:]

                for track in left:
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

                # After reaching 0, reverse direction
                if left:
                    total_seek_time += current_position  # Move to 0
                    current_position = 0

                for track in right:
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

            else:  # right
                left = request_sequence[:head_index]
                right = request_sequence[head_index + 1:]

                for track in right:
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

                # After reaching end of disk, reverse direction
                if right:
                    total_seek_time += abs(current_position - (disk_size - 1))
                    current_position = disk_size - 1

                for track in reversed(left):
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

            result = {
                'seek_sequence': seek_sequence,
                'total_seek_time': total_seek_time,
                'direction': direction,
                'disk_size': disk_size,
            }

        except Exception as e:
            result = {'error': f'Error: {str(e)}'}
    return render(request, 'Algorithms/scan_disk.html', {'result': result})

def cscan_disk_scheduling(request):
    result = None
    if request.method == 'POST':
        try:
            requests = request.POST.get('requests')
            head = int(request.POST.get('head'))
            disk_size = int(request.POST.get('disk_size'))

            request_sequence = list(map(int, requests.split(',')))
            request_sequence.append(head)
            request_sequence.sort()

            head_index = request_sequence.index(head)
            left = request_sequence[:head_index]
            right = request_sequence[head_index + 1:]

            seek_sequence = []
            total_seek_time = 0
            current_position = head

            # Move towards right (max end)
            for track in right:
                seek_sequence.append(track)
                total_seek_time += abs(current_position - track)
                current_position = track

            # Jump to beginning (simulate circular move)
            if left:
                total_seek_time += abs(current_position - (disk_size - 1))  # move to end
                total_seek_time += (disk_size - 1)  # jump from end to start (costly)
                current_position = 0

                for track in left:
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

            result = {
                'seek_sequence': seek_sequence,
                'total_seek_time': total_seek_time,
                'disk_size': disk_size,
            }

        except Exception as e:
            result = {'error': f'Error: {str(e)}'}
    return render(request, 'Algorithms/cscan_disk.html', {'result': result})

def look_disk_scheduling(request):
    result = None
    if request.method == 'POST':
        try:
            requests = request.POST.get('requests')
            head = int(request.POST.get('head'))
            direction = request.POST.get('direction')  # 'left' or 'right'

            request_sequence = list(map(int, requests.split(',')))
            request_sequence.append(head)
            request_sequence.sort()

            head_index = request_sequence.index(head)
            seek_sequence = []
            total_seek_time = 0
            current_position = head

            if direction == 'left':
                left = request_sequence[:head_index][::-1]
                right = request_sequence[head_index + 1:]

                for track in left:
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

                for track in right:
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

            else:  # right
                left = request_sequence[:head_index]
                right = request_sequence[head_index + 1:]

                for track in right:
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

                for track in reversed(left):
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

            result = {
                'request_sequence': list(map(int, requests.split(','))),
                'head': head,
                'seek_sequence': seek_sequence,
                'total_seek_time': total_seek_time,
                'direction': direction,
            }

        except Exception as e:
            result = {'error': f'Error: {str(e)}'}
    return render(request, 'Algorithms/look_disk.html', {'result': result})

def clook_disk_scheduling(request):
    result = None
    if request.method == 'POST':
        try:
            requests = request.POST.get('requests')
            head = int(request.POST.get('head'))
            direction = request.POST.get('direction')  # 'left' or 'right'

            request_sequence = list(map(int, requests.split(',')))
            request_sequence.append(head)
            request_sequence.sort()

            head_index = request_sequence.index(head)
            left = request_sequence[:head_index]
            right = request_sequence[head_index + 1:]

            seek_sequence = []
            total_seek_time = 0
            current_position = head

            if direction == 'left':
                # Service left side first
                for track in reversed(left):
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

                # Jump to the rightmost
                if right:
                    total_seek_time += abs(current_position - right[-1])
                    current_position = right[-1]

                    for track in reversed(right[:-1]):
                        seek_sequence.append(track)
                        total_seek_time += abs(current_position - track)
                        current_position = track

            else:  # direction == 'right'
                for track in right:
                    seek_sequence.append(track)
                    total_seek_time += abs(current_position - track)
                    current_position = track

                # Jump to the leftmost
                if left:
                    total_seek_time += abs(current_position - left[0])
                    current_position = left[0]

                    for track in left[1:]:
                        seek_sequence.append(track)
                        total_seek_time += abs(current_position - track)
                        current_position = track

            result = {
                'seek_sequence': seek_sequence,
                'total_seek_time': total_seek_time,
            }

        except Exception as e:
            result = {'error': f'Error: {str(e)}'}
    return render(request, 'Algorithms/clook_disk.html', {'result': result})
