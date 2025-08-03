import os
import re
import pandas as pd
import matplotlib.pyplot as plt

directory = "./log/"

def extract_execution_times():
    # {(algo, pattern_len, text_len): time}
    data = {}
    pattern = re.compile(r"([A-Za-z_]+)_(\d+)_(\d+)_resource_log\.csv")

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            algo = match.group(1)
            e = int(match.group(2))  # text length = 10^e
            f = int(match.group(3))  # pattern length = 5*f
            text_len = 10 ** e
            pattern_len = 5 * f

            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f_csv:
                for line in f_csv:
                    if line.startswith("Total Execution Time"):
                        try:
                            time_sec = float(line.strip().split(",")[1])
                            data[(algo, pattern_len, text_len)] = time_sec
                        except ValueError:
                            pass
                        break
    return data

def plot_pattern_length_comparison(data):
    # 条件：text_len = 10^9
    target_text_len = 10**9
    algorithms = ["Boyer_Moore", "KMP", "FFT"]

    plt.figure(figsize=(10, 6))

    for algo in algorithms:
        x_vals = []
        y_vals = []
        for (a, pattern_len, text_len), time in data.items():
            if a == algo and text_len == target_text_len:
                x_vals.append(pattern_len)
                y_vals.append(time)
        if x_vals:
            # ソートしてプロット
            sorted_pairs = sorted(zip(x_vals, y_vals))
            x_sorted, y_sorted = zip(*sorted_pairs)
            plt.plot(x_sorted, y_sorted, marker='o', label=algo)

    plt.title("Execution Time vs Pattern Length (Text Length = 10⁹)")
    plt.xlabel("Pattern Length")
    plt.ylabel("Execution Time (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparison_pattern_length.png")
    plt.close()
    print("Saved comparison_pattern_length.png")

def plot_text_length_comparison(data):
    # 条件：pattern_len = 125
    target_pattern_len = 125
    algorithms = ["Boyer_Moore", "KMP", "FFT"]

    plt.figure(figsize=(10, 6))

    for algo in algorithms:
        x_vals = []
        y_vals = []
        for (a, pattern_len, text_len), time in data.items():
            if a == algo and pattern_len == target_pattern_len:
                x_vals.append(text_len)
                y_vals.append(time)
        if x_vals:
            # ソートしてプロット
            sorted_pairs = sorted(zip(x_vals, y_vals))
            x_sorted, y_sorted = zip(*sorted_pairs)
            x_labels = [f"$10^{len(str(x))-1}$" for x in x_sorted]  # eに戻すため
            plt.plot(x_labels, y_sorted, marker='o', label=algo)

    plt.title("Execution Time vs Text Length (Pattern Length = 125)")
    plt.xlabel("Text Length (10^e)")
    plt.ylabel("Execution Time (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("comparison_text_length.png")
    plt.close()
    print("Saved comparison_text_length.png")

# 実行
data = extract_execution_times()
plot_pattern_length_comparison(data)
plot_text_length_comparison(data)
