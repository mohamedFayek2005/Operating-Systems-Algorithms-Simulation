import matplotlib.pyplot as plt
from collections import deque
import numpy as np
import pandas as pd



def plot_gantt(gantt, title):
    if not gantt:
        return None
    fig, ax = plt.subplots(figsize=(10, 3))
    for i, item in enumerate(gantt):
        pid, start, finish = item
        duration = finish - start
        ax.barh(0, duration, left=start, height=0.5, edgecolor="black")
        ax.text(start + duration / 2, 0, pid, ha="center", va="center", color="white", fontweight="bold")
        ax.text(start, -0.35, str(start), ha="center")
        if i == len(gantt) - 1:
            ax.text(finish, -0.35, str(finish), ha="center")

    ax.set_yticks([])
    ax.set_xlabel("Time")
    ax.set_title(title)
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig



def plot_cpu_comparison_chart(metrics_dict):
    labels = list(metrics_dict.keys())
    wts = [metrics_dict[alg]['wt'] for alg in labels]
    tats = [metrics_dict[alg]['tat'] for alg in labels]
    rts = [metrics_dict[alg]['rt'] for alg in labels]

    x = np.arange(len(labels))
    width = 0.25
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width, wts, width, label='Avg WT', color='skyblue')
    ax.bar(x, tats, width, label='Avg TAT', color='salmon')
    ax.bar(x + width, rts, width, label='Avg RT', color='lightgreen')
    ax.set_ylabel('Time Units')
    ax.set_title('CPU Algorithms Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    return fig



def generate_cpu_outputs(name, steps, result):
    steps_text = f"#### {name} - Step by Step Execution\n"
    for step in steps:
        steps_text += f"- {step}\n"
        
    table_data = []
    for p in result:
        table_data.append({
            "Process": p["pid"],
            "Arrival Time": p["arrival"],
            "Burst Time": p["burst"],
            "Priority": p.get("priority", "-"),
            "Waiting Time": p["waiting"],
            "Turnaround Time": p["turnaround"],
            "Response Time": p["response_time"]
        })
        
    df_results = pd.DataFrame(table_data)
    return steps_text, df_results



def priority_scheduling(processes):
    n = len(processes)
    time, completed = 0, 0
    visited = [False] * n
    gantt, result, steps = [], [], []

    while completed < n:
        idx = -1
        highest_prio = 10**9
        for i in range(n):
            if not visited[i] and processes[i]["arrival"] <= time:
                if processes[i]["priority"] < highest_prio:
                    highest_prio = processes[i]["priority"]
                    idx = i
                elif processes[i]["priority"] == highest_prio:
                    if idx == -1 or processes[i]["arrival"] < processes[idx]["arrival"]:
                        idx = i
        if idx == -1:
            time += 1
            continue

        start = time
        finish = time + processes[idx]["burst"]
        waiting = start - processes[idx]["arrival"]
        turnaround = finish - processes[idx]["arrival"]
        response_time = start - processes[idx]["arrival"]

        gantt.append((processes[idx]["pid"], start, finish))
        result.append({
            "pid": processes[idx]["pid"], "arrival": processes[idx]["arrival"],
            "burst": processes[idx]["burst"], "priority": processes[idx]["priority"],
            "waiting": waiting, "turnaround": turnaround, "response_time": response_time
        })
        steps.append(f"{processes[idx]['pid']} runs from {start} to {finish}")

        time = finish
        visited[idx] = True
        completed += 1

    avg_wt = sum(x["waiting"] for x in result) / n
    avg_tat = sum(x["turnaround"] for x in result) / n
    avg_rt = sum(x["response_time"] for x in result) / n

    steps_text, df_results = generate_cpu_outputs("Priority Scheduling (Non-Preemptive)", steps, result)
    return steps_text, df_results, gantt, avg_wt, avg_tat, avg_rt



def fcfs(processes):
    ordered = sorted(processes, key=lambda x: x["arrival"])
    time, total_wt, total_tat, total_rt = 0, 0, 0, 0
    gantt, result, steps = [], [], []

    for p in ordered:
        if time < p["arrival"]:
            time = p["arrival"]
        start = time
        waiting = time - p["arrival"]
        turnaround = waiting + p["burst"]
        response_time = start - p["arrival"]
        time += p["burst"]
        finish = time

        gantt.append((p["pid"], start, finish))
        result.append({
            "pid": p["pid"], "arrival": p["arrival"], "burst": p["burst"], "priority": p.get("priority", "-"),
            "waiting": waiting, "turnaround": turnaround, "response_time": response_time
        })
        steps.append(f"{p['pid']} runs from {start} to {finish}")
        
        total_wt += waiting
        total_tat += turnaround
        total_rt += response_time

    n = len(ordered)
    avg_wt = total_wt / n
    avg_tat = total_tat / n
    avg_rt = total_rt / n

    steps_text, df_results = generate_cpu_outputs("FCFS", steps, result)
    return steps_text, df_results, gantt, avg_wt, avg_tat, avg_rt