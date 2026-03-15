# main.py

import sys
import inspect
import sort_algorithms
from visualize import visualize_sort

def collect_algorithms(module):
    """
    从模块中自动收集所有以 '_sort' 结尾的函数。
    返回列表，每个元素为 (显示名称, 函数对象)
    """
    algorithms = []
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if name.endswith('_sort'):
            # 生成友好的显示名称：将下划线替换为空格，并首字母大写
            display_name = name.replace('_', ' ').title()
            algorithms.append((display_name, func))
    # 按显示名称排序，使菜单顺序固定
    algorithms.sort(key=lambda x: x[0])
    return algorithms

def get_numbers_from_input():
    """获取用户输入的数字列表"""
    while True:
        try:
            numbers_str = input("请输入要排序的数字（用空格分隔）：")
            numbers = list(map(int, numbers_str.split()))
            if not numbers:
                print("输入不能为空，请重新输入。")
                continue
            return numbers
        except ValueError:
            print("输入无效，请确保输入的是整数，并用空格分隔。")

def run_normal_sort(algo_name, algo_func):
    """运行普通排序（非可视化）"""
    numbers = get_numbers_from_input()
    original = numbers.copy()
    data_copy = original.copy()

    # 调用排序函数
    result = algo_func(data_copy)  # 原地排序函数会修改 data_copy 并返回它；返回新列表的函数则返回新对象

    # 判断是原地修改还是返回新列表
    if result is data_copy:  # 同一个对象，说明是原地修改
        sorted_numbers = data_copy
    else:                    # 不同对象，说明返回了新列表
        sorted_numbers = result

    print(f"\n使用【{algo_name}】排序结果：")
    print(f"原始列表：{original}")
    print(f"排序后：{sorted_numbers}\n")

def parse_interval(input_str):
    """将用户输入的字符串（如'1s', '500ms', '1000'）解析为毫秒整数"""
    input_str = input_str.strip().lower()
    if not input_str:
        return 1000  # 默认改为1000毫秒，与提示一致
    if input_str.endswith('s'):
        # 秒为单位（例如 1s, 1.5s）
        try:
            seconds = float(input_str[:-1])
            return int(seconds * 1000)
        except ValueError:
            pass
    elif input_str.endswith('ms'):
        # 毫秒为单位（例如 500ms）
        try:
            return int(input_str[:-2])
        except ValueError:
            pass
    else:
        # 纯数字，当作毫秒
        try:
            return int(input_str)
        except ValueError:
            pass
    print("输入无效，使用默认速度1000毫秒")
    return 1000

def run_visualize_sort(algo_name, algo_func):
    numbers = get_numbers_from_input()
    speed_input = input("请输入动画速度（如 1s 表示1秒，1000ms 表示1000毫秒，直接回车默认1000毫秒）：").strip()
    interval = parse_interval(speed_input)
    print(f"正在可视化 {algo_name}，速度：{interval}毫秒...")
    sorted_result = visualize_sort(algo_func, numbers, interval=interval)
    print(f"排序完成，结果：{sorted_result}")

def main():
    # 自动收集所有排序算法
    algorithms = collect_algorithms(sort_algorithms)
    if not algorithms:
        print("错误：未找到任何排序函数（函数名应以 '_sort' 结尾）。")
        return

    while True:
        # 打印主菜单
        print("\n请选择操作：")
        # 使用更安全的解包方式：每个算法信息可以包含任意多个元素，我们只取前两个
        for i, algo_info in enumerate(algorithms, start=1):
            # 假设 algo_info 的第一个元素是名称，第二个是函数
            if isinstance(algo_info, (tuple, list)) and len(algo_info) >= 2:
                name = algo_info[0]
            else:
                # 如果格式不对，直接使用字符串表示
                name = str(algo_info)
            print(f"{i}. 普通排序 - {name}")
        print(f"{len(algorithms) + 1}. 可视化排序")
        print("0. 退出")

        choice = input("请输入数字选择：").strip()

        if choice == '0':
            print("程序已退出。")
            break

        if not choice.isdigit():
            print("输入无效，请输入数字。")
            continue

        choice = int(choice)

        if 1 <= choice <= len(algorithms):
            # 普通排序
            algo_info = algorithms[choice - 1]
            # 安全获取名称和函数
            if isinstance(algo_info, (tuple, list)) and len(algo_info) >= 2:
                algo_name, algo_func = algo_info[0], algo_info[1]
            else:
                print("算法信息格式错误，请检查 collect_algorithms 返回值。")
                continue
            run_normal_sort(algo_name, algo_func)

        elif choice == len(algorithms) + 1:
            # 可视化排序：先选择具体算法
            print("\n请选择要可视化的算法：")
            for i, algo_info in enumerate(algorithms, start=1):
                if isinstance(algo_info, (tuple, list)) and len(algo_info) >= 2:
                    name = algo_info[0]
                else:
                    name = str(algo_info)
                print(f"{i}. {name}")
            sub_choice = input("请输入算法编号：").strip()
            if not sub_choice.isdigit():
                print("输入无效，返回主菜单。")
                continue
            sub_choice = int(sub_choice)
            if 1 <= sub_choice <= len(algorithms):
                algo_info = algorithms[sub_choice - 1]
                if isinstance(algo_info, (tuple, list)) and len(algo_info) >= 2:
                    algo_name, algo_func = algo_info[0], algo_info[1]
                else:
                    print("算法信息格式错误。")
                    continue
                run_visualize_sort(algo_name, algo_func)
            else:
                print("无效选择。")

        else:
            print(f"无效选择，请输入 1-{len(algorithms) + 1} 之间的数字。")

if __name__ == "__main__":
    main()