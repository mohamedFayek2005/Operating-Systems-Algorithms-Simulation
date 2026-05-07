import matplotlib.pyplot as plt

def plot_page_fault_history(history, title):
    steps = list(range(1, len(history) + 1))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(steps, history, marker="o")
    ax.set_xlabel("Step")
    ax.set_ylabel("Cumulative Page Faults")
    ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    return fig



def plot_page_comparison(names, values):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(names, values)
    ax.set_xlabel("Algorithms")
    ax.set_ylabel("Total Page Faults")
    ax.set_title("Page Replacement Comparison")
    plt.tight_layout()
    return fig



def lru(pages, frames_count):
    frames, recent, history, lines = [], {}, [], []
    faults = 0

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

    text = "LRU\n\nStep by Step:\n" + "\n".join(lines) + f"\n\nTotal Page Faults = {faults}\n"
    return text, faults, history



def fifo(pages, frames_count):
    frames, history, lines = [], [], []
    queue_index, faults = 0, 0

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

    text = "FIFO\n\nStep by Step:\n" + "\n".join(lines) + f"\n\nTotal Page Faults = {faults}\n"
    return text, faults, history