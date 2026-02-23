import time
from utils import deep_getsizeof


def benchmark(algorithm, data, key=lambda x: x,
              reverse=False, runs=1, step_callback=None):

    total_time = 0
    total_memory = 0
    total_comparisons = 0

    for _ in range(runs):
        tracker = {"comparisons": 0}
        data_copy = data.copy()

        start = time.perf_counter()
        sorted_data = algorithm(data_copy, tracker,
                                key=key,
                                reverse=reverse,
                                step_callback=step_callback)
        end = time.perf_counter()

        total_time += (end - start)
        total_memory += deep_getsizeof(sorted_data)
        total_comparisons += tracker["comparisons"]

    return {
        "sorted_data": sorted_data,
        "avg_time": total_time / runs,
        "avg_memory": total_memory / runs,
        "avg_comparisons": total_comparisons / runs
    }