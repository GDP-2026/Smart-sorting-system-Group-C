import threading
import tkinter as tk
import customtkinter as ctk

from algorithms import *
from benchmarking import benchmark
from utils import generate_dataset

from visualization import (
    show_single_result,
    show_comparison_chart,
    show_heatmap
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Quick Sort": quick_sort,
    "Merge Sort": merge_sort,
}


class SortingApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Advanced Sorting Benchmark System")
        self.geometry("1100x700")

        self.running = False
        self.results_store = {}

        self.build_ui()

    # ==========================
    # UI SETUP
    # ==========================

    def build_ui(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=280)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Main Panel
        self.main_panel = ctk.CTkFrame(self)
        self.main_panel.grid(row=0, column=1, sticky="nsew")

        self.build_sidebar()
        self.build_main_panel()

    # ==========================
    # SIDEBAR
    # ==========================

    def build_sidebar(self):

        ctk.CTkLabel(self.sidebar, text="Configuration",
                     font=("Arial", 20, "bold")).pack(pady=15)

        self.size_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Dataset Size (e.g. 10000)"
        )
        self.size_entry.pack(pady=10)

        self.dataset_type = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Random", "Sorted", "Reverse Sorted", "Nearly Sorted"]
        )
        self.dataset_type.pack(pady=10)

        self.algorithm_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=list(ALGORITHMS.keys())
        )
        self.algorithm_menu.pack(pady=10)

        self.reverse_var = tk.BooleanVar()
        self.reverse_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Reverse Order",
            variable=self.reverse_var
        )
        self.reverse_switch.pack(pady=10)

        self.compare_var = tk.BooleanVar()
        self.compare_switch = ctk.CTkSwitch(
            self.sidebar,
            text="Run All Algorithms",
            variable=self.compare_var
        )
        self.compare_switch.pack(pady=10)

        self.run_button = ctk.CTkButton(
            self.sidebar,
            text="Run Benchmark",
            command=self.safe_run
        )
        self.run_button.pack(pady=20)

        self.theme_button = ctk.CTkButton(
            self.sidebar,
            text="Toggle Theme",
            command=self.toggle_theme
        )
        self.theme_button.pack(pady=5)

    # ==========================
    # MAIN PANEL
    # ==========================

    def build_main_panel(self):

        self.output_box = ctk.CTkTextbox(self.main_panel, height=250)
        self.output_box.pack(fill="x", padx=20, pady=10)

        self.chart_container = ctk.CTkFrame(self.main_panel)
        self.chart_container.pack(fill="both", expand=True, padx=20, pady=10)

    # ==========================
    # THREAD SAFE RUN
    # ==========================

    def safe_run(self):

        if self.running:
            return

        try:
            size = int(self.size_entry.get())

            if size <= 0:
                self.log("⚠ Dataset size must be positive.")
                return

            if size > 200000:
                self.log("⚠ Dataset too large (limit 200,000).")
                return

        except ValueError:
            self.log("⚠ Invalid dataset size.")
            return

        self.running = True
        self.clear_chart()

        thread = threading.Thread(target=self.run_benchmark, daemon=True)
        thread.start()

    # ==========================
    # BENCHMARK ENGINE
    # ==========================

    def run_benchmark(self):

        size = int(self.size_entry.get())
        dataset_type = self.dataset_type.get()
        reverse = self.reverse_var.get()
        compare_all = self.compare_var.get()

        data = generate_dataset(size, dataset_type)

        self.log(f"\nDataset: {dataset_type} | Size: {size}")

        if compare_all:
            self.results_store = {}

            for name, algorithm in ALGORITHMS.items():
                self.log(f"\nRunning {name}...")
                result = benchmark(algorithm, data, reverse=reverse, runs=3)
                self.results_store[name] = result

            self.after(0, self.show_comparison_results)

        else:
            algorithm_name = self.algorithm_menu.get()
            algorithm = ALGORITHMS[algorithm_name]

            self.log(f"\nRunning {algorithm_name}...")
            result = benchmark(algorithm, data, reverse=reverse, runs=3)

            self.results_store = {algorithm_name: result}

            self.after(0, lambda: self.show_single_result_ui(result, algorithm_name))

        self.running = False

    # ==========================
    # DISPLAY SINGLE RESULT
    # ==========================

    def show_single_result_ui(self, result, algorithm_name):

        self.log("\n=== RESULTS ===")
        self.log(f"Time: {result['avg_time']:.6f} sec")
        self.log(f"Memory: {result['avg_memory']} bytes")
        self.log(f"Comparisons: {result['avg_comparisons']}")

        show_single_result(self.chart_container, result, algorithm_name)

    # ==========================
    # DISPLAY COMPARISON
    # ==========================

    def show_comparison_results(self):

        self.log("\n=== COMPARISON RESULTS ===")

        best_algo = min(
            self.results_store,
            key=lambda x: self.results_store[x]["avg_time"]
        )

        for name, result in self.results_store.items():
            self.log(f"\n{name}")
            self.log(f"  Time: {result['avg_time']:.6f}")
            self.log(f"  Memory: {result['avg_memory']}")
            self.log(f"  Comparisons: {result['avg_comparisons']}")

        self.log(f"\n🏆 Best Algorithm (Fastest): {best_algo}")

        show_comparison_chart(self.chart_container, self.results_store)
        show_heatmap(self.chart_container, self.results_store)

    # ==========================
    # UTILITIES
    # ==========================

    def clear_chart(self):
        for widget in self.chart_container.winfo_children():
            widget.destroy()

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if current == "Dark" else "dark")

    def log(self, message):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")


# ==========================
# LAUNCH
# ==========================

def launch_app():
    app = SortingApp()
    app.mainloop()