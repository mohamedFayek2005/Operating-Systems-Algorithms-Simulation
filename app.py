import streamlit as st
import pandas as pd
from utils import parse_int_list
from cpu_scheduling import plot_gantt, plot_cpu_comparison_chart, fcfs, priority_scheduling
from memory_allocation import plot_memory, plot_memory_comparison, best_fit, first_fit
from page_replacement import plot_page_fault_history, plot_page_comparison, lru, fifo



st.set_page_config(page_title="OS Project Web App", layout="wide")
st.title("Operating Systems Project Analyzer:")
tab_cpu, tab_memory, tab_page = st.tabs(["CPU Scheduling", "Memory Allocation", "Page Replacement"])



with tab_cpu:
    col_input, col_output = st.columns([1, 2])
    with col_input:
        st.subheader("Process Inputs")
        if "cpu_df" not in st.session_state:
            st.session_state.cpu_df = pd.DataFrame([
                {"PID": "P1", "Arrival Time": 0, "Burst Time": 6, "Priority": 2},
                {"PID": "P2", "Arrival Time": 1, "Burst Time": 8, "Priority": 1},
                {"PID": "P3", "Arrival Time": 2, "Burst Time": 7, "Priority": 4},
                {"PID": "P4", "Arrival Time": 3, "Burst Time": 3, "Priority": 3}
            ])
            
        edited_df = st.data_editor(st.session_state.cpu_df, num_rows="dynamic", use_container_width=True)
        st.caption("*Note: For Priority Scheduling, a lower number indicates higher priority.*")
        cpu_algo = st.selectbox("Select Algorithm", ["FCFS", "Priority (Non-Preemptive)", "Compare Both"])
        run_cpu = st.button("Run CPU Scheduling")

    with col_output:
        if run_cpu:
            processes = [{"pid": row["PID"], "arrival": row["Arrival Time"], "burst": row["Burst Time"], "priority": row["Priority"]} 
                         for idx, row in edited_df.iterrows()]
            
            if not processes:
                st.error("Please add at least one process.")
            else:
                st.subheader("Results")
                if cpu_algo == "FCFS":
                    # Unpacking 6 values here fixes your error!
                    steps_text, df_results, gantt, avg_wt, avg_tat, avg_rt = fcfs([p.copy() for p in processes])
                    st.markdown(steps_text)
                    st.table(df_results)
                    st.info(f"**Average Waiting Time:** {avg_wt:.2f} | **Average Turnaround Time:** {avg_tat:.2f} | **Average Response Time:** {avg_rt:.2f}")
                    st.pyplot(plot_gantt(gantt, "FCFS Gantt Chart"))
                    
                elif cpu_algo == "Priority (Non-Preemptive)":
                    steps_text, df_results, gantt, avg_wt, avg_tat, avg_rt = priority_scheduling([p.copy() for p in processes])
                    st.markdown(steps_text)
                    st.table(df_results)
                    st.info(f"**Average Waiting Time:** {avg_wt:.2f} | **Average Turnaround Time:** {avg_tat:.2f} | **Average Response Time:** {avg_rt:.2f}")
                    st.pyplot(plot_gantt(gantt, "Priority Scheduling Gantt Chart"))
                    
                elif cpu_algo == "Compare Both":
                    f_steps, f_df, _, fcfs_w, fcfs_t, fcfs_r = fcfs([p.copy() for p in processes])
                    p_steps, p_df, _, prio_w, prio_t, prio_r = priority_scheduling([p.copy() for p in processes])
                    
                    metrics = {
                        "FCFS": {"wt": fcfs_w, "tat": fcfs_t, "rt": fcfs_r},
                        "Priority": {"wt": prio_w, "tat": prio_t, "rt": prio_r}
                    }
                    
                    st.pyplot(plot_cpu_comparison_chart(metrics))
                    
                    st.markdown("### Theoretical Analysis")
                    st.markdown("""
                    | Algorithm | Advantages | Disadvantages | Best Use Case | Performance Note |
                    |-----------|------------|---------------|---------------|------------------|
                    | **FCFS** | Simple to implement, no starvation. | Convoy effect (long processes delay short ones). High WT. | Batch systems. | Poor Average RT and WT. |
                    | **Priority** | Honors process importance. | Indefinite blocking (starvation) for low-priority processes. | Real-time Operating Systems. | Performance depends purely on priority distribution. |
                    """)
                    
                    with st.expander("Show Detailed Execution Steps and Tables"):
                        c1, c2 = st.columns(2)
                        with c1: 
                            st.markdown(f_steps)
                            st.table(f_df)
                            st.info(f"**Avg WT:** {fcfs_w:.2f} | **Avg TAT:** {fcfs_t:.2f} | **Avg RT:** {fcfs_r:.2f}")
                        with c2: 
                            st.markdown(p_steps)
                            st.table(p_df)
                            st.info(f"**Avg WT:** {prio_w:.2f} | **Avg TAT:** {prio_t:.2f} | **Avg RT:** {prio_r:.2f}")



with tab_memory:
    col_input, col_output = st.columns([1, 2])
    with col_input:
        st.subheader("Memory Inputs")
        blocks_str = st.text_input("Memory Blocks (space separated)", "100 500 200 300 600")
        processes_str = st.text_input("Process Sizes (space separated)", "212 417 112 426")
        mem_algo = st.selectbox("Select Memory Algorithm", ["First Fit", "Best Fit", "Compare Both"])
        run_mem = st.button("Run Memory Allocation")

    with col_output:
        if run_mem:
            try:
                blocks = parse_int_list(blocks_str)
                process_sizes = parse_int_list(processes_str)
                
                st.subheader("Results")
                if mem_algo == "First Fit":
                    steps_text, df_results, allocation, orig_blocks, t_int, t_ext = first_fit(blocks[:], process_sizes)
                    st.markdown(steps_text)
                    st.table(df_results)
                    st.info(f"**Total Internal Fragmentation:** {t_int}  |  **Total External Fragmentation:** {t_ext}")
                    st.pyplot(plot_memory(orig_blocks, process_sizes, allocation, "First Fit Memory Allocation"))
                
                elif mem_algo == "Best Fit":
                    steps_text, df_results, allocation, orig_blocks, t_int, t_ext = best_fit(blocks[:], process_sizes)
                    st.markdown(steps_text)
                    st.table(df_results)
                    st.info(f"**Total Internal Fragmentation:** {t_int}  |  **Total External Fragmentation:** {t_ext}")
                    st.pyplot(plot_memory(orig_blocks, process_sizes, allocation, "Best Fit Memory Allocation"))
                
                elif mem_algo == "Compare Both":
                    b_steps, b_df, _, _, b_int, b_ext = best_fit(blocks[:], process_sizes)
                    f_steps, f_df, _, _, f_int, f_ext = first_fit(blocks[:], process_sizes)
                    
                    st.pyplot(plot_memory_comparison(b_int, b_ext, f_int, f_ext))
                    
                    st.markdown("### Theoretical Analysis")
                    st.markdown("""
                    | Algorithm | Advantages | Disadvantages | Best Use Case | Performance Note |
                    |-----------|------------|---------------|---------------|------------------|
                    | **First Fit** | Faster execution, simpler to implement. | Leaves fragmented blocks scattered at the beginning. | General rapid memory allocation. | Often yields higher external fragmentation overall. |
                    | **Best Fit** | Minimizes internal fragmentation by picking the tightest space. | Slower (searches entire list). Creates tiny unusable external fragments. | Environments where memory is strictly limited. | Typically yields lower internal fragmentation. |
                    """)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f_steps)
                        st.table(f_df)
                        st.info(f"Internal Frag: {f_int} | External Frag: {f_ext}")
                    with col2:
                        st.markdown(b_steps)
                        st.table(b_df)
                        st.info(f"Internal Frag: {b_int} | External Frag: {b_ext}")
            except Exception as e:
                st.error(f"Error parsing inputs: {e}")



with tab_page:
    col_input, col_output = st.columns([1, 2])
    with col_input:
        st.subheader("Page Replacements Inputs")
        pages_str = st.text_input("Page Reference String (space separated)", "1 2 3 4 1 2 5 1 2 3 4 5")
        frames_count = st.number_input("Number of Frames", min_value=1, value=3)
        page_algo = st.selectbox("Select Page Algorithm", ["FIFO", "LRU", "Compare Both"])
        run_page = st.button("Run Page Replacement")

    with col_output:
        if run_page:
            try:
                pages = parse_int_list(pages_str)
                
                st.subheader("Results")
                if page_algo == "FIFO":
                    text, faults, history = fifo(pages, frames_count)
                    st.text(text)
                    st.pyplot(plot_page_fault_history(history, "FIFO Page Fault Progress"))
                elif page_algo == "LRU":
                    text, faults, history = lru(pages, frames_count)
                    st.text(text)
                    st.pyplot(plot_page_fault_history(history, "LRU Page Fault Progress"))
                elif page_algo == "Compare Both":
                    fifo_text, fifo_faults, _ = fifo(pages, frames_count)
                    lru_text, lru_faults, _ = lru(pages, frames_count)
                    
                    st.pyplot(plot_page_comparison(["FIFO", "LRU"], [fifo_faults, lru_faults]))
                    
                    st.markdown("### Theoretical Analysis")
                    st.markdown("""
                    | Algorithm | Advantages | Disadvantages | Best Use Case | Performance Note |
                    |-----------|------------|---------------|---------------|------------------|
                    | **FIFO** | Very simple to understand and code. Low overhead. | Suffers from Belady's Anomaly (more frames = more faults). Ignores usage frequency. | Basic caching where strict timing doesn't matter. | Generally yields more page faults. |
                    | **LRU** | Closer to optimal behavior. Does not suffer from Belady's Anomaly. | High hardware/software overhead to track timestamps for every access. | Modern operating systems' virtual memory. | Consistently yields fewer page faults. |
                    """)
                    
                    c1, c2 = st.columns(2)
                    with c1: st.text(fifo_text)
                    with c2: st.text(lru_text)
            except Exception as e:
                st.error(f"Error parsing inputs: {e}")