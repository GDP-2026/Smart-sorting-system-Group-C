def bubble_sort(arr, tracker, key=lambda x: x, reverse=False, step_callback=None):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            tracker["comparisons"] += 1

            if reverse:
                condition = key(arr[j]) < key(arr[j + 1])
            else:
                condition = key(arr[j]) > key(arr[j + 1])

            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                if step_callback:
                    step_callback(arr.copy())

    return arr


def insertion_sort(arr, tracker, key=lambda x: x, reverse=False, step_callback=None):
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1

        while j >= 0:
            tracker["comparisons"] += 1

            if reverse:
                condition = key(arr[j]) < key(current)
            else:
                condition = key(arr[j]) > key(current)

            if condition:
                arr[j + 1] = arr[j]
                j -= 1
                if step_callback:
                    step_callback(arr.copy())
            else:
                break

        arr[j + 1] = current

    return arr


def selection_sort(arr, tracker, key=lambda x: x, reverse=False, step_callback=None):
    n = len(arr)

    for i in range(n):
        selected = i

        for j in range(i + 1, n):
            tracker["comparisons"] += 1

            if reverse:
                condition = key(arr[j]) > key(arr[selected])
            else:
                condition = key(arr[j]) < key(arr[selected])

            if condition:
                selected = j

        arr[i], arr[selected] = arr[selected], arr[i]
        if step_callback:
            step_callback(arr.copy())

    return arr


def quick_sort(arr, tracker, key=lambda x: x, reverse=False, step_callback=None):

    def partition(low, high):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            tracker["comparisons"] += 1

            if reverse:
                condition = key(arr[j]) > key(pivot)
            else:
                condition = key(arr[j]) < key(pivot)

            if condition:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                if step_callback:
                    step_callback(arr.copy())

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def _quick_sort(low, high):
        if low < high:
            pi = partition(low, high)
            _quick_sort(low, pi - 1)
            _quick_sort(pi + 1, high)

    _quick_sort(0, len(arr) - 1)
    return arr


def merge_sort(arr, tracker, key=lambda x: x, reverse=False, step_callback=None):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], tracker, key, reverse, step_callback)
    right = merge_sort(arr[mid:], tracker, key, reverse, step_callback)

    return merge(left, right, tracker, key, reverse, step_callback)


def merge(left, right, tracker, key, reverse, step_callback):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        tracker["comparisons"] += 1

        if reverse:
            condition = key(left[i]) > key(right[j])
        else:
            condition = key(left[i]) < key(right[j])

        if condition:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

        if step_callback:
            step_callback(result + left[i:] + right[j:])

    result.extend(left[i:])
    result.extend(right[j:])
    return result