from collections import deque
import matplotlib.pyplot as plt


def get_processes():
    processes = []
    n = int(input("Enter number of processes: "))

    for i in range(n):
        print(f"\nProcess P{i + 1}")
        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))
        processes.append({
            "pid": f"P{i + 1}",
            "arrival": arrival,
            "burst": burst
        })

    return processes


def print_gantt_chart(gantt):
    print("\nGantt Chart:")
    for item in gantt:
        print(f"| {item[0]} ", end="")
    print("|")

    if gantt:
        print(gantt[0][1], end="")
        for item in gantt:
            print(f"    {item[2]}", end="")
        print()


def plot_gantt(gantt, title):
    if not gantt:
        return

    plt.figure(figsize=(10, 3))

    for i, item in enumerate(gantt):
        pid = item[0]
        start = item[1]
        finish = item[2]
        duration = finish - start

        plt.barh(0, duration, left=start, height=0.5)
        plt.text(start + duration / 2, 0, pid, ha="center", va="center")
        plt.text(start, -0.35, str(start), ha="center")
        if i == len(gantt) - 1:
            plt.text(finish, -0.35, str(finish), ha="center")

    plt.yticks([])
    plt.xlabel("Time")
    plt.title(title)
    plt.grid(axis="x")
    plt.tight_layout()
    plt.show()


def non_preemptive_sjf(processes):
    time = 0
    completed = 0
    n = len(processes)
    visited = [False] * n

    gantt = []
    result = []

    print("\nStep by Step Execution for Non-Preemptive SJF:")

    while completed < n:
        idx = -1
        min_burst = 10**9

        for i in range(n):
            if not visited[i] and processes[i]["arrival"] <= time:
                if processes[i]["burst"] < min_burst:
                    min_burst = processes[i]["burst"]
                    idx = i
                elif processes[i]["burst"] == min_burst:
                    if idx == -1 or processes[i]["arrival"] < processes[idx]["arrival"]:
                        idx = i

        if idx == -1:
            time += 1
            continue

        start = time
        finish = time + processes[idx]["burst"]
        waiting = start - processes[idx]["arrival"]
        turnaround = finish - processes[idx]["arrival"]

        gantt.append((processes[idx]["pid"], start, finish))
        result.append({
            "pid": processes[idx]["pid"],
            "arrival": processes[idx]["arrival"],
            "burst": processes[idx]["burst"],
            "waiting": waiting,
            "turnaround": turnaround
        })

        print(f"{processes[idx]['pid']} runs from {start} to {finish}")

        time = finish
        visited[idx] = True
        completed += 1

    print_gantt_chart(gantt)
    plot_gantt(gantt, "Non-Preemptive SJF Gantt Chart")

    total_waiting = 0
    total_turnaround = 0

    print("\nFinal Results:")
    print("PID\tAT\tBT\tWT\tTAT")
    for p in result:
        print(f"{p['pid']}\t{p['arrival']}\t{p['burst']}\t{p['waiting']}\t{p['turnaround']}")
        total_waiting += p["waiting"]
        total_turnaround += p["turnaround"]

    print(f"\nAverage Waiting Time = {total_waiting / n:.2f}")
    print(f"Average Turnaround Time = {total_turnaround / n:.2f}")


def round_robin(processes, quantum):
    n = len(processes)
    remaining = [p["burst"] for p in processes]
    completion = [0] * n

    time = 0
    gantt = []
    ready_queue = deque()
    arrived = [False] * n
    completed = 0

    print("\nStep by Step Execution for Round Robin:")

    while completed < n:
        for i in range(n):
            if not arrived[i] and processes[i]["arrival"] <= time:
                ready_queue.append(i)
                arrived[i] = True

        if not ready_queue:
            time += 1
            continue

        idx = ready_queue.popleft()
        run_time = min(quantum, remaining[idx])

        start = time
        time += run_time
        remaining[idx] -= run_time
        gantt.append((processes[idx]["pid"], start, time))

        print(f"{processes[idx]['pid']} runs from {start} to {time}")

        for i in range(n):
            if not arrived[i] and processes[i]["arrival"] <= time:
                ready_queue.append(i)
                arrived[i] = True

        if remaining[idx] > 0:
            ready_queue.append(idx)
        else:
            completion[idx] = time
            completed += 1

    print_gantt_chart(gantt)
    plot_gantt(gantt, "Round Robin Gantt Chart")

    total_waiting = 0
    total_turnaround = 0

    print("\nFinal Results:")
    print("PID\tAT\tBT\tWT\tTAT")

    for i in range(n):
        turnaround = completion[i] - processes[i]["arrival"]
        waiting = turnaround - processes[i]["burst"]
        total_waiting += waiting
        total_turnaround += turnaround
        print(f"{processes[i]['pid']}\t{processes[i]['arrival']}\t{processes[i]['burst']}\t{waiting}\t{turnaround}")

    print(f"\nAverage Waiting Time = {total_waiting / n:.2f}")
    print(f"Average Turnaround Time = {total_turnaround / n:.2f}")


def fcfs(processes):
    processes = sorted(processes, key=lambda x: x["arrival"])
    time = 0
    total_waiting = 0
    total_turnaround = 0
    gantt = []

    print("\nFCFS Comparison Result:")
    print("PID\tAT\tBT\tWT\tTAT")

    for p in processes:
        if time < p["arrival"]:
            time = p["arrival"]

        start = time
        waiting = time - p["arrival"]
        turnaround = waiting + p["burst"]
        time += p["burst"]
        finish = time

        gantt.append((p["pid"], start, finish))

        total_waiting += waiting
        total_turnaround += turnaround

        print(f"{p['pid']}\t{p['arrival']}\t{p['burst']}\t{waiting}\t{turnaround}")

    print_gantt_chart(gantt)
    plot_gantt(gantt, "FCFS Gantt Chart")

    print(f"\nFCFS Average Waiting Time = {total_waiting / len(processes):.2f}")
    print(f"FCFS Average Turnaround Time = {total_turnaround / len(processes):.2f}")


def compare_cpu_algorithms():
    processes = get_processes()
    quantum = int(input("Enter Time Quantum for Round Robin: "))

    print("\n--- Non-Preemptive SJF ---")
    non_preemptive_sjf([p.copy() for p in processes])

    print("\n--- Round Robin ---")
    round_robin([p.copy() for p in processes], quantum)

    print("\n--- FCFS ---")
    fcfs([p.copy() for p in processes])


def cpu_menu():
    while True:
        print("\n" + "=" * 60)
        print("CPU SCHEDULING")
        print("=" * 60)
        print("1) Non-Preemptive SJF")
        print("2) Round Robin")
        print("3) FCFS (Comparison)")
        print("4) Compare All")
        print("5) Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            processes = get_processes()
            non_preemptive_sjf(processes)
        elif choice == "2":
            processes = get_processes()
            quantum = int(input("Enter Time Quantum: "))
            round_robin(processes, quantum)
        elif choice == "3":
            processes = get_processes()
            fcfs(processes)
        elif choice == "4":
            compare_cpu_algorithms()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")