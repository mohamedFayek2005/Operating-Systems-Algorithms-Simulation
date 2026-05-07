import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def plot_memory(blocks, processes, allocation, title):
    used = [0] * len(blocks)
    for i in range(len(processes)):
        if allocation[i] != -1:
            used[allocation[i]] = processes[i]

    x = list(range(1, len(blocks) + 1))
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x, blocks, label="Block Size", color="lightgray")
    ax.bar(x, used, label="Used Size", color="steelblue")
    ax.set_xlabel("Memory Blocks")
    ax.set_ylabel("Size")
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels([f"B{i}" for i in x])
    ax.legend()
    plt.tight_layout()
    return fig



def plot_memory_comparison(best_int, best_ext, first_int, first_ext):
    labels = ['Best Fit', 'First Fit']
    internal = [best_int, first_int]
    external = [best_ext, first_ext]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(x - width/2, internal, width, label='Internal Fragmentation', color='orange')
    ax.bar(x + width/2, external, width, label='External Fragmentation', color='crimson')

    ax.set_ylabel('Memory Size (Units)')
    ax.set_title('Fragmentation Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    return fig



def execute_memory_algo(algo_name, blocks, processes, allocation_logic):
    original_blocks = blocks[:]
    allocation = [-1] * len(processes)
    steps = []

    allocation_logic(blocks, processes, allocation, steps)
    steps_text = f"#### {algo_name} - Step by Step Execution\n"
    for step in steps:
        steps_text += f"- {step}\n"

    total_internal, allocated_total = 0, 0
    table_data = []
    
    for i in range(len(processes)):
        if allocation[i] != -1:
            frag = original_blocks[allocation[i]] - processes[i]
            total_internal += frag
            allocated_total += processes[i]
            table_data.append({
                "Process": f"P{i+1}", 
                "Size": processes[i], 
                "Block": f"B{allocation[i]+1}", 
                "Internal Fragmentation": str(frag)
            })
        else:
            table_data.append({
                "Process": f"P{i+1}", 
                "Size": processes[i], 
                "Block": "Not Allocated", 
                "Internal Fragmentation": "-"
            })

    external_fragmentation = sum(original_blocks) - allocated_total    
    df_results = pd.DataFrame(table_data)
    
    return steps_text, df_results, allocation, original_blocks, total_internal, external_fragmentation



def best_fit(blocks, processes):
    def logic(blk, proc, alloc, stp):
        for i in range(len(proc)):
            best_idx = -1
            for j in range(len(blk)):
                if blk[j] >= proc[i]:
                    if best_idx == -1 or blk[j] < blk[best_idx]:
                        best_idx = j
            if best_idx != -1:
                alloc[i] = best_idx
                stp.append(f"Process P{i+1} ({proc[i]}) allocated to Block B{best_idx+1} ({blk[best_idx]})")
                blk[best_idx] = -1 
            else:
                stp.append(f"Process P{i+1} ({proc[i]}) cannot be allocated")
    return execute_memory_algo("Best Fit", blocks, processes, logic)



def first_fit(blocks, processes):
    def logic(blk, proc, alloc, stp):
        for i in range(len(proc)):
            for j in range(len(blk)):
                if blk[j] >= proc[i]:
                    alloc[i] = j
                    stp.append(f"Process P{i+1} ({proc[i]}) allocated to Block B{j+1} ({blk[j]})")
                    blk[j] = -1 
                    break
            if alloc[i] == -1:
                stp.append(f"Process P{i+1} ({proc[i]}) cannot be allocated")
    return execute_memory_algo("First Fit", blocks, processes, logic)