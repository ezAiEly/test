# visualize.py

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy

def animate_sorting(snapshots, interval=200):
    """播放排序动画"""
    if not snapshots:
        print("没有记录到任何步骤。")
        return

    fig, ax = plt.subplots()
    # 所有快照中最大的长度（用于统一x轴范围，因为斯大林排序长度会变）
    max_len = max(len(s) for s in snapshots)
    # 初始化条形图，用第一个快照填充，多余的条设为0高度
    first = snapshots[0]
    bars = ax.bar(range(max_len), 
                  first + [0] * (max_len - len(first)))
    ax.set_ylim(0, max(max(s) for s in snapshots) * 1.1 if snapshots else 1)
    ax.set_title("排序过程可视化")

    def update(frame):
        data = snapshots[frame]
        # 将当前数据扩展到 max_len，缺失部分填0
        full_data = data + [0] * (max_len - len(data))
        for bar, val in zip(bars, full_data):
            bar.set_height(val)
        ax.set_title(f"步骤 {frame+1}/{len(snapshots)}")
        return bars

    ani = animation.FuncAnimation(fig, update, frames=len(snapshots), interval=interval, repeat=False)
    plt.show()
    return ani

def visualize_sort(sort_func, arr):
    """
    通用可视化排序入口
    :param sort_func: 已添加 callback 参数的排序函数（如 bubble_sort）
    :param arr: 待排序的原始列表
    :return: 排序后的列表
    """
    snapshots = []
    # 记录初始状态
    snapshots.append(arr[:])

    # 定义回调函数，收集快照
    def record(state):
        snapshots.append(state)

    # 执行排序，传入回调
    # 注意：如果排序函数是原地修改，我们直接传入 arr（它会修改 arr）；如果是返回新列表，我们需要传入 arr 的副本？
    # 为了一致性，我们总是传入 arr 的副本，这样原列表 arr 不会被修改。
    # 但原地排序函数会修改传入的列表，所以我们需要传入一个副本，以免污染外部。
    # 同时，排序函数返回的结果要么是原列表（原地排序）要么是新列表，我们统一接收返回值。
    data = arr[:]  # 工作副本
    sorted_result = sort_func(data, callback=record)

    # 播放动画
    animate_sorting(snapshots)

    # 返回排序结果（可能与 arr 不同，如果 sort_func 返回新列表）
    return sorted_result