import sys
import random


def deep_getsizeof(obj, seen=None):
    size = sys.getsizeof(obj)

    if seen is None:
        seen = set()

    obj_id = id(obj)
    if obj_id in seen:
        return 0

    seen.add(obj_id)

    if isinstance(obj, dict):
        size += sum(deep_getsizeof(k, seen) + deep_getsizeof(v, seen)
                    for k, v in obj.items())

    elif hasattr(obj, "__dict__"):
        size += deep_getsizeof(obj.__dict__, seen)

    elif isinstance(obj, (list, tuple, set)):
        size += sum(deep_getsizeof(i, seen) for i in obj)

    return size


def generate_dataset(size, dataset_type="Random"):
    data = [random.randint(1, 100000) for _ in range(size)]

    if dataset_type == "Sorted":
        return sorted(data)

    elif dataset_type == "Reverse Sorted":
        return sorted(data, reverse=True)

    elif dataset_type == "Nearly Sorted":
        data = sorted(data)
        for _ in range(size // 10):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            data[i], data[j] = data[j], data[i]
        return data

    return data