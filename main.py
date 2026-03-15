# main.py

import sys
import inspect
import sort_algorithms  # 导入模块
from visualize import visualize_sort

#def is_sort_function(obj):
    #"""判断对象是否为排序函数（以 '_sort' 结尾的函数）"""
    #return inspect.isfunction(obj) and obj.__name__.endswith('_sort')

def collect_algorithms(module):
    """从模块中自动收集所有排序函数，返回列表，每个元素为 (显示名称, 函数, 是否返回新列表)"""
    algorithms = []
    for name, func in inspect.getmembers(module, inspect.isfunction):
        if name.endswith('_sort'):
            # 将下划线替换为空格，并首字母大写
            display_name = name.replace('_', ' ').title()
            # 获取 returns_new 属性，默认为 False
            returns_new = getattr(func, 'returns_new', False)
            algorithms.append((display_name, func, returns_new))
    # 可以按名称排序，使菜单顺序固定
    algorithms.sort(key=lambda x: x[0])
    return algorithms

#def print_menu(algorithms):
    #print("\n请选择排序算法：")
    #for i, (name, _, _) in enumerate(algorithms, start=1):
        #print(f"{i}. {name}")
    #print("0. 退出")

def get_numbers_from_input():
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

def run_visualize_sort(algo_name, algo_func):
    """运行可视化排序"""
    numbers = get_numbers_from_input()
    print(f"正在可视化 {algo_name}...")
    sorted_result = visualize_sort(algo_func, numbers)
    print(f"排序完成，结果：{sorted_result}")

def main():
    # 自动收集算法
    algorithms = collect_algorithms(sort_algorithms)
    if not algorithms:
        print("错误：未找到任何排序函数（函数名应以 '_sort' 结尾）。")
        return

    while True:
        print("\n请选择操作：")
        for i, (name, _) in enumerate(algorithms, start=1):
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
            algo_name, algo_func = algorithms[choice - 1]
            run_normal_sort(algo_name, algo_func)

        elif choice == len(algorithms) + 1:
            # 可视化排序：先选择具体算法
            print("\n请选择要可视化的算法：")
            for i, (name, _) in enumerate(algorithms, start=1):
                print(f"{i}. {name}")
            sub_choice = input("请输入算法编号：").strip()
            if not sub_choice.isdigit():
                print("输入无效，返回主菜单。")
                continue
            sub_choice = int(sub_choice)
            if 1 <= sub_choice <= len(algorithms):
                algo_name, algo_func = algorithms[sub_choice - 1]
                run_visualize_sort(algo_name, algo_func)
            else:
                print("无效选择。")

        else:
            print(f"无效选择，请输入 1-{len(algorithms) + 1} 之间的数字。")


if __name__ == "__main__":
    main()