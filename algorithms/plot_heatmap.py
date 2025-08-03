import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

directory = "./log/"

def generate_heatmap(algorithm_name):
    data = {}  
    pattern = re.compile(rf"{algorithm_name}_(\d+)_(\d+)_resource_log\.csv")

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            e = int(match.group(1))  # text length = 10^e
            f = int(match.group(2))  # pattern length = 5*f

            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f_csv:
                for line in f_csv:
                    if line.startswith("Total Execution Time"):
                        try:
                            time_sec = float(line.strip().split(",")[1])
                            data[(f * 5, 10 ** e)] = time_sec
                        except ValueError:
                            pass
                        break

    if not data:
        print(f"No data found for {algorithm_name}")
        return

    df = pd.DataFrame.from_dict(data, orient="index", columns=["time"])
    df.index = pd.MultiIndex.from_tuples(df.index, names=["pattern_len", "text_len"])
    heatmap_data = df.unstack(level="text_len").droplevel(axis=1, level=0)

    heatmap_data = heatmap_data.sort_index(ascending=True)

    text_lengths = heatmap_data.columns.tolist()
    text_labels = [f"$10^{len(str(tl))-1}$" for tl in text_lengths]

    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".4f",
        cmap="YlOrRd",
        yticklabels=heatmap_data.index,
        xticklabels=text_labels
    )
    plt.title(f"{algorithm_name} Execution Time Heatmap")
    plt.xlabel("Text Length (10^e)")
    plt.ylabel("Pattern Length (5×f)")
    plt.tight_layout()
    plt.savefig(f"{algorithm_name}_heatmap.png")
    plt.close()
    print(f"Saved {algorithm_name}_heatmap.png")

algorithms = ["Boyer_Moore", "KMP", "FFT"]

for algo in algorithms:
    generate_heatmap(algo)
