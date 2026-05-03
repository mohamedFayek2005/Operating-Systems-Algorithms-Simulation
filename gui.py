import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from collections import deque


def parse_int_list(text):
    text = text.replace(",", " ").replace("\n", " ")
    parts = [x.strip() for x in text.split() if x.strip()]
    return [int(x) for x in parts]


def show_result(box, text):
    box.config(state="normal")
    box.delete("1.0", tk.END)
    box.insert(tk.END, text)
    box.config(state="disabled")


def plot_gantt(gantt, title):
    if not gantt:
        return

    plt.figure(figsize=(10, 3))
    for i, item in enumerate(gantt):
        pid, start, finish = item
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


def sjf_non_preemptive(processes):
    n = len(processes)
    time = 0
    completed = 0
    visited = [False] * n
    gantt = []
    result = []
    steps = []

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

        steps.append(f"{processes[idx]['pid']} runs from {start} to {finish}")

        time = finish
        visited[idx] = True
        completed += 1

    avg_waiting = sum(x["waiting"] for x in result) / n
    avg_turnaround = sum(x["turnaround"] for x in result) / n

    text = "Non-Preemptive SJF\n\n"
    text += "Step by Step:\n"
    text += "\n".join(steps)
    text += "\n\nFinal Results:\n"
    text += "PID\tAT\tBT\tWT\tTAT\n"

    for p in result:
        text += f"{p['pid']}\t{p['arrival']}\t{p['burst']}\t{p['waiting']}\t{p['turnaround']}\n"

    text += f"\nAverage Waiting Time = {avg_waiting:.2f}\n"
    text += f"Average Turnaround Time = {avg_turnaround:.2f}\n"

    return text, gantt, avg_waiting, avg_turnaround


def round_robin(processes, quantum):
    n = len(processes)
    remaining = [p["burst"] for p in processes]
    completion = [0] * n
    time = 0
    gantt = []
    ready_queue = deque()
    arrived = [False] * n
    completed = 0
    steps = []

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
        steps.append(f"{processes[idx]['pid']} runs from {start} to {time}")

        for i in range(n):
            if not arrived[i] and processes[i]["arrival"] <= time:
                ready_queue.append(i)
                arrived[i] = True

        if remaining[idx] > 0:
            ready_queue.append(idx)
        else:
            completion[idx] = time
            completed += 1

    result = []
    total_waiting = 0
    total_turnaround = 0

    for i in range(n):
        turnaround = completion[i] - processes[i]["arrival"]
        waiting = turnaround - processes[i]["burst"]
        total_waiting += waiting
        total_turnaround += turnaround
        result.append({
            "pid": processes[i]["pid"],
            "arrival": processes[i]["arrival"],
            "burst": processes[i]["burst"],
            "waiting": waiting,
            "turnaround": turnaround
        })

    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    text = "Round Robin\n\n"
    text += "Step by Step:\n"
    text += "\n".join(steps)
    text += "\n\nFinal Results:\n"
    text += "PID\tAT\tBT\tWT\tTAT\n"

    for p in result:
        text += f"{p['pid']}\t{p['arrival']}\t{p['burst']}\t{p['waiting']}\t{p['turnaround']}\n"

    text += f"\nAverage Waiting Time = {avg_waiting:.2f}\n"
    text += f"Average Turnaround Time = {avg_turnaround:.2f}\n"

    return text, gantt, avg_waiting, avg_turnaround


def fcfs(processes):
    ordered = sorted(processes, key=lambda x: x["arrival"])
    time = 0
    gantt = []
    result = []
    total_waiting = 0
    total_turnaround = 0
    steps = []

    for p in ordered:
        if time < p["arrival"]:
            time = p["arrival"]

        start = time
        waiting = time - p["arrival"]
        turnaround = waiting + p["burst"]
        time += p["burst"]
        finish = time

        gantt.append((p["pid"], start, finish))
        result.append({
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "waiting": waiting,
            "turnaround": turnaround
        })
        steps.append(f"{p['pid']} runs from {start} to {finish}")

        total_waiting += waiting
        total_turnaround += turnaround

    avg_waiting = total_waiting / len(ordered)
    avg_turnaround = total_turnaround / len(ordered)

    text = "FCFS\n\n"
    text += "Step by Step:\n"
    text += "\n".join(steps)
    text += "\n\nFinal Results:\n"
    text += "PID\tAT\tBT\tWT\tTAT\n"

    for p in result:
        text += f"{p['pid']}\t{p['arrival']}\t{p['burst']}\t{p['waiting']}\t{p['turnaround']}\n"

    text += f"\nAverage Waiting Time = {avg_waiting:.2f}\n"
    text += f"Average Turnaround Time = {avg_turnaround:.2f}\n"

    return text, gantt, avg_waiting, avg_turnaround


def best_fit(blocks, processes):
    original_blocks = blocks[:]
    allocation = [-1] * len(processes)
    steps = []

    for i in range(len(processes)):
        best_idx = -1
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                if best_idx == -1 or blocks[j] < blocks[best_idx]:
                    best_idx = j

        if best_idx != -1:
            allocation[i] = best_idx
            steps.append(f"Process P{i+1} ({processes[i]}) allocated to Block B{best_idx+1} ({blocks[best_idx]})")
            blocks[best_idx] = -1
        else:
            steps.append(f"Process P{i+1} ({processes[i]}) cannot be allocated")

    text = "Best Fit\n\n"
    text += "Step by Step:\n"
    text += "\n".join(steps)
    text += "\n\nFinal Results:\n"
    text += "Process\tSize\tBlock\tInternal Fragmentation\n"

    total_internal = 0
    allocated_total = 0

    for i in range(len(processes)):
        if allocation[i] != -1:
            frag = original_blocks[allocation[i]] - processes[i]
            total_internal += frag
            allocated_total += processes[i]
            text += f"P{i+1}\t{processes[i]}\tB{allocation[i]+1}\t{frag}\n"
        else:
            text += f"P{i+1}\t{processes[i]}\tNot Allocated\t-\n"

    total_memory = sum(original_blocks)
    external_fragmentation = total_memory - allocated_total

    text += f"\nTotal Internal Fragmentation = {total_internal}\n"
    text += f"Total External Fragmentation = {external_fragmentation}\n"

    return text, allocation, original_blocks


def first_fit(blocks, processes):
    original_blocks = blocks[:]
    allocation = [-1] * len(processes)
    steps = []

    for i in range(len(processes)):
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                allocation[i] = j
                steps.append(f"Process P{i+1} ({processes[i]}) allocated to Block B{j+1} ({blocks[j]})")
                blocks[j] = -1
                break

        if allocation[i] == -1:
            steps.append(f"Process P{i+1} ({processes[i]}) cannot be allocated")

    text = "First Fit\n\n"
    text += "Step by Step:\n"
    text += "\n".join(steps)
    text += "\n\nFinal Results:\n"
    text += "Process\tSize\tBlock\tInternal Fragmentation\n"

    total_internal = 0
    allocated_total = 0

    for i in range(len(processes)):
        if allocation[i] != -1:
            frag = original_blocks[allocation[i]] - processes[i]
            total_internal += frag
            allocated_total += processes[i]
            text += f"P{i+1}\t{processes[i]}\tB{allocation[i]+1}\t{frag}\n"
        else:
            text += f"P{i+1}\t{processes[i]}\tNot Allocated\t-\n"

    total_memory = sum(original_blocks)
    external_fragmentation = total_memory - allocated_total

    text += f"\nTotal Internal Fragmentation = {total_internal}\n"
    text += f"Total External Fragmentation = {external_fragmentation}\n"

    return text, allocation, original_blocks


def plot_memory(blocks, processes, allocation, title):
    used = [0] * len(blocks)

    for i in range(len(processes)):
        if allocation[i] != -1:
            used[allocation[i]] = processes[i]

    x = list(range(1, len(blocks) + 1))

    plt.figure(figsize=(8, 5))
    plt.bar(x, blocks, label="Block Size")
    plt.bar(x, used, label="Used Size")
    plt.xlabel("Memory Blocks")
    plt.ylabel("Size")
    plt.title(title)
    plt.xticks(x, [f"B{i}" for i in x])
    plt.legend()
    plt.tight_layout()
    plt.show()


def lru(pages, frames_count):
    frames = []
    recent = {}
    faults = 0
    lines = []
    history = []

    for i, page in enumerate(pages):
        if page not in frames:
            faults += 1
            if len(frames) < frames_count:
                frames.append(page)
            else:
                victim = min(frames, key=lambda x: recent[x])
                idx = frames.index(victim)
                frames[idx] = page

        recent[page] = i
        history.append(faults)
        lines.append(f"Step {i+1}: Page {page} -> {frames}")

    text = "LRU\n\n"
    text += "Step by Step:\n"
    text += "\n".join(lines)
    text += f"\n\nTotal Page Faults = {faults}\n"

    return text, faults, history


def fifo(pages, frames_count):
    frames = []
    queue_index = 0
    faults = 0
    lines = []
    history = []

    for i, page in enumerate(pages):
        if page not in frames:
            faults += 1
            if len(frames) < frames_count:
                frames.append(page)
            else:
                frames[queue_index] = page
                queue_index = (queue_index + 1) % frames_count

        history.append(faults)
        lines.append(f"Step {i+1}: Page {page} -> {frames}")

    text = "FIFO\n\n"
    text += "Step by Step:\n"
    text += "\n".join(lines)
    text += f"\n\nTotal Page Faults = {faults}\n"

    return text, faults, history


def clock_method(pages, frames_count):
    frames = [-1] * frames_count
    use_bit = [0] * frames_count
    pointer = 0
    faults = 0
    lines = []
    history = []

    for i, page in enumerate(pages):
        if page in frames:
            idx = frames.index(page)
            use_bit[idx] = 1
        else:
            faults += 1
            while True:
                if use_bit[pointer] == 0:
                    frames[pointer] = page
                    use_bit[pointer] = 1
                    pointer = (pointer + 1) % frames_count
                    break
                else:
                    use_bit[pointer] = 0
                    pointer = (pointer + 1) % frames_count

        history.append(faults)
        lines.append(f"Step {i+1}: Page {page} -> Frames: {frames} | Use bits: {use_bit}")

    text = "Clock\n\n"
    text += "Step by Step:\n"
    text += "\n".join(lines)
    text += f"\n\nTotal Page Faults = {faults}\n"

    return text, faults, history


def plot_page_fault_history(history, title):
    steps = list(range(1, len(history) + 1))
    plt.figure(figsize=(8, 4))
    plt.plot(steps, history, marker="o")
    plt.xlabel("Step")
    plt.ylabel("Cumulative Page Faults")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_page_comparison(names, values):
    plt.figure(figsize=(7, 4))
    plt.bar(names, values)
    plt.xlabel("Algorithms")
    plt.ylabel("Total Page Faults")
    plt.title("Page Replacement Comparison")
    plt.tight_layout()
    plt.show()


root = tk.Tk()
root.title("OS Project GUI")
root.geometry("1000x700")

tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True)

cpu_tab = tk.Frame(tabs)
memory_tab = tk.Frame(tabs)
page_tab = tk.Frame(tabs)

tabs.add(cpu_tab, text="CPU Scheduling")
tabs.add(memory_tab, text="Memory Allocation")
tabs.add(page_tab, text="Page Replacement")

cpu_left = tk.Frame(cpu_tab)
cpu_left.pack(side="left", fill="y", padx=10, pady=10)

cpu_right = tk.Frame(cpu_tab)
cpu_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(cpu_left, text="Processes", font=("Arial", 11, "bold")).pack(anchor="w")

process_rows_frame = tk.Frame(cpu_left)
process_rows_frame.pack(anchor="w", pady=5)

process_entries = []


def refresh_process_labels():
    for i, (row, at_entry, bt_entry) in enumerate(process_entries, start=1):
        widgets = row.winfo_children()
        widgets[0].config(text=f"P{i}")


def add_process_row(arrival="", burst=""):
    row_index = len(process_entries) + 1
    row = tk.Frame(process_rows_frame)
    row.pack(anchor="w", pady=2)

    tk.Label(row, text=f"P{row_index}", width=4).pack(side="left")
    tk.Label(row, text="AT").pack(side="left")
    at_entry = tk.Entry(row, width=6)
    at_entry.pack(side="left", padx=2)
    at_entry.insert(0, arrival)

    tk.Label(row, text="BT").pack(side="left")
    bt_entry = tk.Entry(row, width=6)
    bt_entry.pack(side="left", padx=2)
    bt_entry.insert(0, burst)

    def remove_this_row():
        if len(process_entries) <= 1:
            messagebox.showwarning("Warning", "At least one process is required")
            return
        row.destroy()
        process_entries.remove((row, at_entry, bt_entry))
        refresh_process_labels()

    tk.Button(row, text="X", width=3, command=remove_this_row).pack(side="left", padx=4)

    process_entries.append((row, at_entry, bt_entry))
    refresh_process_labels()


def clear_all_processes():
    for row, _, _ in process_entries[:]:
        row.destroy()
    process_entries.clear()
    add_process_row()


def get_processes_from_rows():
    processes = []
    for i, (_, at_entry, bt_entry) in enumerate(process_entries, start=1):
        at_text = at_entry.get().strip()
        bt_text = bt_entry.get().strip()

        if at_text == "" or bt_text == "":
            raise ValueError(f"Please complete data for P{i}")

        arrival = int(at_text)
        burst = int(bt_text)

        processes.append({
            "pid": f"P{i}",
            "arrival": arrival,
            "burst": burst
        })

    if not processes:
        raise ValueError("Please enter at least one process")

    return processes


add_buttons_frame = tk.Frame(cpu_left)
add_buttons_frame.pack(anchor="w", pady=5)

tk.Button(add_buttons_frame, text="Add Process", width=14, command=add_process_row).pack(side="left", padx=2)
tk.Button(add_buttons_frame, text="Clear", width=10, command=clear_all_processes).pack(side="left", padx=2)

add_process_row("0", "6")
add_process_row("1", "8")
add_process_row("2", "7")
add_process_row("3", "3")

tk.Label(cpu_left, text="Quantum for Round Robin", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
quantum_entry = tk.Entry(cpu_left, width=15)
quantum_entry.pack(anchor="w", pady=5)
quantum_entry.insert(0, "2")

cpu_result = ScrolledText(cpu_right, width=70, height=30, state="disabled")
cpu_result.pack(fill="both", expand=True)


def run_sjf_gui():
    try:
        processes = get_processes_from_rows()
        text, gantt, _, _ = sjf_non_preemptive(processes)
        show_result(cpu_result, text)
        plot_gantt(gantt, "Non-Preemptive SJF Gantt Chart")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_rr_gui():
    try:
        processes = get_processes_from_rows()
        quantum = int(quantum_entry.get())
        text, gantt, _, _ = round_robin(processes, quantum)
        show_result(cpu_result, text)
        plot_gantt(gantt, "Round Robin Gantt Chart")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_fcfs_gui():
    try:
        processes = get_processes_from_rows()
        text, gantt, _, _ = fcfs(processes)
        show_result(cpu_result, text)
        plot_gantt(gantt, "FCFS Gantt Chart")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_cpu_compare():
    try:
        processes = get_processes_from_rows()
        quantum = int(quantum_entry.get())

        sjf_text, _, sjf_w, sjf_t = sjf_non_preemptive([p.copy() for p in processes])
        rr_text, _, rr_w, rr_t = round_robin([p.copy() for p in processes], quantum)
        fcfs_text, _, fcfs_w, fcfs_t = fcfs([p.copy() for p in processes])

        text = "CPU Comparison\n\n"
        text += f"SJF  -> Avg WT = {sjf_w:.2f}, Avg TAT = {sjf_t:.2f}\n"
        text += f"RR   -> Avg WT = {rr_w:.2f}, Avg TAT = {rr_t:.2f}\n"
        text += f"FCFS -> Avg WT = {fcfs_w:.2f}, Avg TAT = {fcfs_t:.2f}\n\n"
        text += "SJF Details:\n" + sjf_text + "\n\n"
        text += "RR Details:\n" + rr_text + "\n\n"
        text += "FCFS Details:\n" + fcfs_text

        show_result(cpu_result, text)
    except Exception as e:
        messagebox.showerror("Error", str(e))


tk.Button(cpu_left, text="Run SJF", width=20, command=run_sjf_gui).pack(pady=5)
tk.Button(cpu_left, text="Run Round Robin", width=20, command=run_rr_gui).pack(pady=5)
tk.Button(cpu_left, text="Run FCFS", width=20, command=run_fcfs_gui).pack(pady=5)
tk.Button(cpu_left, text="Compare All", width=20, command=run_cpu_compare).pack(pady=5)

memory_left = tk.Frame(memory_tab)
memory_left.pack(side="left", fill="y", padx=10, pady=10)

memory_right = tk.Frame(memory_tab)
memory_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(memory_left, text="Memory Blocks", font=("Arial", 11, "bold")).pack(anchor="w")
blocks_input = ScrolledText(memory_left, width=30, height=5)
blocks_input.pack(pady=5)
blocks_input.insert(tk.END, "100 500 200 300 600")

tk.Label(memory_left, text="Process Sizes", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
process_sizes_input = ScrolledText(memory_left, width=30, height=5)
process_sizes_input.pack(pady=5)
process_sizes_input.insert(tk.END, "212 417 112 426")

memory_result = ScrolledText(memory_right, width=70, height=30, state="disabled")
memory_result.pack(fill="both", expand=True)


def run_best_fit_gui():
    try:
        blocks = parse_int_list(blocks_input.get("1.0", tk.END))
        processes = parse_int_list(process_sizes_input.get("1.0", tk.END))
        text, allocation, original_blocks = best_fit(blocks, processes)
        show_result(memory_result, text)
        plot_memory(original_blocks, processes, allocation, "Best Fit Memory Allocation")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_first_fit_gui():
    try:
        blocks = parse_int_list(blocks_input.get("1.0", tk.END))
        processes = parse_int_list(process_sizes_input.get("1.0", tk.END))
        text, allocation, original_blocks = first_fit(blocks, processes)
        show_result(memory_result, text)
        plot_memory(original_blocks, processes, allocation, "First Fit Memory Allocation")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_memory_compare():
    try:
        blocks = parse_int_list(blocks_input.get("1.0", tk.END))
        processes = parse_int_list(process_sizes_input.get("1.0", tk.END))

        best_text, _, _ = best_fit(blocks[:], processes[:])
        first_text, _, _ = first_fit(blocks[:], processes[:])

        text = "Memory Comparison\n\n"
        text += best_text + "\n\n" + first_text
        show_result(memory_result, text)
    except Exception as e:
        messagebox.showerror("Error", str(e))


tk.Button(memory_left, text="Run Best Fit", width=20, command=run_best_fit_gui).pack(pady=5)
tk.Button(memory_left, text="Run First Fit", width=20, command=run_first_fit_gui).pack(pady=5)
tk.Button(memory_left, text="Compare Both", width=20, command=run_memory_compare).pack(pady=5)

page_left = tk.Frame(page_tab)
page_left.pack(side="left", fill="y", padx=10, pady=10)

page_right = tk.Frame(page_tab)
page_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tk.Label(page_left, text="Page Reference String", font=("Arial", 11, "bold")).pack(anchor="w")
pages_input = ScrolledText(page_left, width=30, height=7)
pages_input.pack(pady=5)
pages_input.insert(tk.END, "1 2 3 4 1 2 5 1 2 3 4 5")

tk.Label(page_left, text="Number of Frames", font=("Arial", 11, "bold")).pack(anchor="w", pady=(10, 0))
frames_entry = tk.Entry(page_left, width=15)
frames_entry.pack(anchor="w", pady=5)
frames_entry.insert(0, "3")

page_result = ScrolledText(page_right, width=70, height=30, state="disabled")
page_result.pack(fill="both", expand=True)


def run_lru_gui():
    try:
        pages = parse_int_list(pages_input.get("1.0", tk.END))
        frames = int(frames_entry.get())
        text, _, history = lru(pages, frames)
        show_result(page_result, text)
        plot_page_fault_history(history, "LRU Page Fault Progress")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_fifo_gui():
    try:
        pages = parse_int_list(pages_input.get("1.0", tk.END))
        frames = int(frames_entry.get())
        text, _, history = fifo(pages, frames)
        show_result(page_result, text)
        plot_page_fault_history(history, "FIFO Page Fault Progress")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_clock_gui():
    try:
        pages = parse_int_list(pages_input.get("1.0", tk.END))
        frames = int(frames_entry.get())
        text, _, history = clock_method(pages, frames)
        show_result(page_result, text)
        plot_page_fault_history(history, "Clock Page Fault Progress")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def run_page_compare():
    try:
        pages = parse_int_list(pages_input.get("1.0", tk.END))
        frames = int(frames_entry.get())

        lru_text, lru_faults, _ = lru(pages, frames)
        fifo_text, fifo_faults, _ = fifo(pages, frames)
        clock_text, clock_faults, _ = clock_method(pages, frames)

        text = "Page Replacement Comparison\n\n"
        text += f"LRU Faults   = {lru_faults}\n"
        text += f"FIFO Faults  = {fifo_faults}\n"
        text += f"Clock Faults = {clock_faults}\n\n"
        text += lru_text + "\n\n" + fifo_text + "\n\n" + clock_text

        show_result(page_result, text)
        plot_page_comparison(["LRU", "FIFO", "Clock"], [lru_faults, fifo_faults, clock_faults])
    except Exception as e:
        messagebox.showerror("Error", str(e))


tk.Button(page_left, text="Run LRU", width=20, command=run_lru_gui).pack(pady=5)
tk.Button(page_left, text="Run FIFO", width=20, command=run_fifo_gui).pack(pady=5)
tk.Button(page_left, text="Run Clock", width=20, command=run_clock_gui).pack(pady=5)
tk.Button(page_left, text="Compare All", width=20, command=run_page_compare).pack(pady=5)

root.mainloop()