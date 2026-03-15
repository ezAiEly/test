# sort_algorithms.py

def bubble_sort(arr, callback=None):
    """冒泡排序（原地排序）"""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                if callback:
                    callback(arr[:])  # 记录交换后的状态
    return arr
# bubble_sort.returns_new = False   # 可以省略，因为默认 False

def selection_sort(arr, callback=None):
    """选择排序（原地排序）"""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            if callback:
                callback(arr[:])
    return arr

def insertion_sort(arr, callback=None):
    """插入排序（原地排序）"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            if callback:
                callback(arr[:])  # 每次移动元素后记录
        arr[j + 1] = key
        if callback:
            callback(arr[:])  # 记录插入后的状态
    return arr

def quick_sort(arr, callback=None):
    """快速排序（返回新列表）"""
    def _quick_sort(lst):
        if len(lst) <= 1:
            if callback:
                callback(lst[:])  # 记录当前状态
            return lst
        pivot = lst[len(lst) // 2]
        left = [x for x in lst if x < pivot]
        middle = [x for x in lst if x == pivot]
        right = [x for x in lst if x > pivot]
        # 递归排序子数组，并合并结果
        sorted_left = _quick_sort(left)
        sorted_right = _quick_sort(right)
        result = sorted_left + middle + sorted_right
        if callback:
            callback(result[:])  # 记录合并后的结果
        return result
    return _quick_sort(arr)  # 标记返回新列表

def gnome_sort(arr, callback=None):
    """侏儒排序（原地排序）"""
    index = 1
    while index < len(arr):
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            if callback:
                callback(arr[:])  # 记录交换后的状态
            index -= 1
    return arr

def stalin_sort(arr, callback=None):
    """斯大林排序（返回新列表）"""
    if len(arr) == 0:
        return []
    result = [arr[0]]
    if callback:
        callback(result[:])  # 记录初始状态
    maxSoFar = arr[0]
    for i in range(1, len(arr)):
        if arr[i] >= maxSoFar:
            result.append(arr[i])
            maxSoFar = arr[i]
            if callback:
                callback(result[:])  # 每次添加元素后记录
    return result
stalin_sort.returns_new = True






# 将来新增排序函数，只需定义并以 _sort 结尾，如需返回新列表则设置 returns_new = True
# 例如：
# def heap_sort(arr):
#     ... 
# heap_sort.returns_new = False   # 如果原地排序，可以省略，但显式标记更清晰