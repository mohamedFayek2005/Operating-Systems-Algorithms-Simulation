import matplotlib.pyplot as plt


def get_memory_data():
    blocks = []
    processes = []

    nb = int(input("Enter number of memory blocks: "))
    for i in range(nb):
        size = int(input(f"Enter size of Block {i + 1}: "))
        blocks.append(size)

    np = int(input("Enter number of processes: "))
    for i in range(np):
        size = int(input(f"Enter size of Process {i + 1}: "))
        processes.append(size)

    return blocks, processes


def print_allocation_table(allocation, process_sizes, original_blocks, title):
    print(f"\n{title}")
    print("Process\tSize\tBlock Allocated\tInternal Fragmentation")

    total_internal = 0
    allocated_process_total = 0

    for i in range(len(process_sizes)):
        if allocation[i] != -1:
            frag = original_blocks[allocation[i]] - process_sizes[i]
            total_internal += frag
            allocated_process_total += process_sizes[i]
            print(f"P{i+1}\t{process_sizes[i]}\tB{allocation[i]+1}\t\t{frag}")
        else:
            print(f"P{i+1}\t{process_sizes[i]}\tNot Allocated\t-")

    total_memory = sum(original_blocks)
    external_fragmentation = total_memory - allocated_process_total

    print(f"\nTotal Internal Fragmentation = {total_internal}")
    print(f"Total External Fragmentation = {external_fragmentation}")


def plot_memory(blocks, processes, allocation, title):
    used = [0] * len(blocks)
    free = blocks[:]

    for i in range(len(processes)):
        if allocation[i] != -1:
            used[allocation[i]] = processes[i]
            free[allocation[i]] = blocks[allocation[i]] - processes[i]

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


def best_fit(blocks, processes):
    original_blocks = blocks[:]
    allocation = [-1] * len(processes)

    print("\nStep by Step Execution for Best Fit:")

    for i in range(len(processes)):
        best_idx = -1
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                if best_idx == -1 or blocks[j] < blocks[best_idx]:
                    best_idx = j

        if best_idx != -1:
            allocation[i] = best_idx
            print(f"Process P{i+1} ({processes[i]}) allocated to Block B{best_idx+1} ({blocks[best_idx]})")
            blocks[best_idx] = -1
        else:
            print(f"Process P{i+1} ({processes[i]}) cannot be allocated")

    print_allocation_table(allocation, processes, original_blocks, "Best Fit Final Results")
    plot_memory(original_blocks, processes, allocation, "Best Fit Memory Allocation Chart")


def first_fit(blocks, processes):
    original_blocks = blocks[:]
    allocation = [-1] * len(processes)

    print("\nStep by Step Execution for First Fit:")

    for i in range(len(processes)):
        for j in range(len(blocks)):
            if blocks[j] >= processes[i]:
                allocation[i] = j
                print(f"Process P{i+1} ({processes[i]}) allocated to Block B{j+1} ({blocks[j]})")
                blocks[j] = -1
                break

        if allocation[i] == -1:
            print(f"Process P{i+1} ({processes[i]}) cannot be allocated")

    print_allocation_table(allocation, processes, original_blocks, "First Fit Final Results")
    plot_memory(original_blocks, processes, allocation, "First Fit Memory Allocation Chart")


def compare_memory_algorithms():
    blocks, processes = get_memory_data()

    print("\n--- Best Fit ---")
    best_fit(blocks[:], processes[:])

    print("\n--- First Fit ---")
    first_fit(blocks[:], processes[:])


def memory_menu():
    while True:
        print("\n" + "=" * 60)
        print("MEMORY ALLOCATION")
        print("=" * 60)
        print("1) Best Fit")
        print("2) First Fit")
        print("3) Compare Best Fit and First Fit")
        print("4) Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            blocks, processes = get_memory_data()
            best_fit(blocks, processes)
        elif choice == "2":
            blocks, processes = get_memory_data()
            first_fit(blocks, processes)
        elif choice == "3":
            compare_memory_algorithms()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")