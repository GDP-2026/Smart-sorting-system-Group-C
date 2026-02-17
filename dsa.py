def smart_sort(arr):
    integers = []
    strings = []

    for item in arr:
        if isinstance(item, int):
            integers.append(item)
        elif isinstance(item, str):
            strings.append(item)


    integers.sort()
    strings.sort()
    return integers + strings

data = [1, "banana", 3, "apple", 2]
print(smart_sort(data))
   



   