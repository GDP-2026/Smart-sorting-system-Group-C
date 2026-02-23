import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np


# ==========================
# THEME ADAPTATION
# ==========================

def apply_theme_to_plot():
    mode = ctk.get_appearance_mode()

    if mode == "Dark":
        plt.style.use("dark_background")
    else:
        plt.style.use("default")


# ==========================
# SINGLE RESULT BAR CHART
# ==========================

def show_single_result(parent, result, algorithm_name):

    apply_theme_to_plot()

    fig, ax = plt.subplots(figsize=(6, 4))

    metrics = ["Time (s)", "Memory (bytes)", "Comparisons"]
    values = [
        result["avg_time"],
        result["avg_memory"],
        result["avg_comparisons"]
    ]

    ax.bar(metrics, values)
    ax.set_title(f"{algorithm_name} Performance")

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return canvas


# ==========================
# MULTI-ALGORITHM COMPARISON
# ==========================

def show_comparison_chart(parent, results_dict):

    apply_theme_to_plot()

    fig, ax = plt.subplots(figsize=(8, 5))

    algorithms = list(results_dict.keys())
    times = [results_dict[a]["avg_time"] for a in algorithms]

    ax.bar(algorithms, times)
    ax.set_ylabel("Average Time (s)")
    ax.set_title("Algorithm Time Comparison")
    ax.tick_params(axis='x', rotation=45)

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return canvas


# ==========================
# HEATMAP SYSTEM
# ==========================

def show_heatmap(parent, results_dict):

    apply_theme_to_plot()

    algorithms = list(results_dict.keys())

    data_matrix = np.array([
        [
            results_dict[a]["avg_time"],
            results_dict[a]["avg_memory"],
            results_dict[a]["avg_comparisons"]
        ]
        for a in algorithms
    ])

    fig, ax = plt.subplots(figsize=(8, 5))
    heatmap = ax.imshow(data_matrix, aspect='auto')

    ax.set_xticks(range(3))
    ax.set_xticklabels(["Time", "Memory", "Comparisons"])
    ax.set_yticks(range(len(algorithms)))
    ax.set_yticklabels(algorithms)

    fig.colorbar(heatmap)

    ax.set_title("Performance Heatmap")

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return canvas


# ==========================
# LIVE ANIMATION SUPPORT
# ==========================

class SortingAnimator:

    def __init__(self, parent, initial_data):

        apply_theme_to_plot()

        self.data = initial_data
        self.frames = []

        self.fig, self.ax = plt.subplots()
        self.bar_container = self.ax.bar(range(len(initial_data)), initial_data)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def add_frame(self, data_snapshot):
        self.frames.append(data_snapshot)

    def animate(self):

        def update(frame):
            for rect, val in zip(self.bar_container, frame):
                rect.set_height(val)
            return self.bar_container

        ani = animation.FuncAnimation(
            self.fig,
            update,
            frames=self.frames,
            repeat=False,
            blit=False
        )

        self.canvas.draw()
        return ani