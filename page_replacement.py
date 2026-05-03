import matplotlib.pyplot as plt


def get_pages():
    pages = list(map(int, input("Enter page reference string separated by space: ").split()))
    frames = int(input("Enter number of frames: "))
    return pages, frames


def lru(pages, frames_count, show_plot=True):
    frames = []
    recent = {}
    faults = 0
    fault_history = []

    print("\nStep by Step Execution for LRU:")

    for i, page in enumerate(pages):
        if page not in frames:
            faults += 1
            if len(frames) < frames_count:
                frames.append(page)
            else:
                lru_page = min(frames, key=lambda x: recent[x])
                idx = frames.index(lru_page)
                frames[idx] = page

        recent[page] = i
        fault_history.append(faults)
        print(f"Step {i + 1}: Page {page} -> {frames}")

    print(f"\nTotal Page Faults = {faults}")

    if show_plot:
        plot_fault_progress(fault_history, "LRU Page Fault Progress")

    return faults


def clock_method(pages, frames_count, show_plot=True):
    frames = [-1] * frames_count
    use_bit = [0] * frames_count
    pointer = 0
    faults = 0
    fault_history = []

    print("\nStep by Step Execution for Clock:")

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

        fault_history.append(faults)
        print(f"Step {i+1}: Page {page} -> Frames: {frames} | Use bits: {use_bit}")

    print(f"\nTotal Page Faults = {faults}")

    if show_plot:
        plot_fault_progress(fault_history, "Clock Page Fault Progress")

    return faults


def fifo(pages, frames_count, show_plot=True):
    frames = []
    queue_index = 0
    faults = 0
    fault_history = []

    print("\nStep by Step Execution for FIFO:")

    for i, page in enumerate(pages):
        if page not in frames:
            faults += 1
            if len(frames) < frames_count:
                frames.append(page)
            else:
                frames[queue_index] = page
                queue_index = (queue_index + 1) % frames_count

        fault_history.append(faults)
        print(f"Step {i + 1}: Page {page} -> {frames}")

    print(f"\nTotal Page Faults = {faults}")

    if show_plot:
        plot_fault_progress(fault_history, "FIFO Page Fault Progress")

    return faults


def plot_fault_progress(fault_history, title):
    steps = list(range(1, len(fault_history) + 1))

    plt.figure(figsize=(8, 4))
    plt.plot(steps, fault_history, marker="o")
    plt.xlabel("Step")
    plt.ylabel("Cumulative Page Faults")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_comparison(algorithms, faults):
    plt.figure(figsize=(7, 4))
    plt.bar(algorithms, faults)
    plt.xlabel("Algorithms")
    plt.ylabel("Total Page Faults")
    plt.title("Page Replacement Algorithms Comparison")
    plt.tight_layout()
    plt.show()


def compare_page_algorithms():
    pages, frames = get_pages()

    print("\n--- LRU ---")
    lru_faults = lru(pages, frames, show_plot=False)

    print("\n--- Clock ---")
    clock_faults = clock_method(pages, frames, show_plot=False)

    print("\n--- FIFO ---")
    fifo_faults = fifo(pages, frames, show_plot=False)

    print("\nComparison Summary:")
    print(f"LRU Faults   = {lru_faults}")
    print(f"Clock Faults = {clock_faults}")
    print(f"FIFO Faults  = {fifo_faults}")

    plot_comparison(["LRU", "Clock", "FIFO"], [lru_faults, clock_faults, fifo_faults])


def page_menu():
    while True:
        print("\n" + "=" * 60)
        print("PAGE REPLACEMENT")
        print("=" * 60)
        print("1) LRU")
        print("2) Clock")
        print("3) FIFO")
        print("4) Compare LRU, Clock, FIFO")
        print("5) Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            pages, frames = get_pages()
            lru(pages, frames)
        elif choice == "2":
            pages, frames = get_pages()
            clock_method(pages, frames)
        elif choice == "3":
            pages, frames = get_pages()
            fifo(pages, frames)
        elif choice == "4":
            compare_page_algorithms()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")