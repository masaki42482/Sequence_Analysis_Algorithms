import numpy as np
from scipy.signal import fftconvolve
import psutil
import os
import threading
import time

# ---------------- Resource Monitor ----------------

class ResourceMonitor:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.cpu_log = []
        self.mem_log = []
        self._running = False

    def start(self):
        self._running = True
        self.thread = threading.Thread(target=self._monitor)
        self.thread.start()

    def _monitor(self):
        process = psutil.Process(os.getpid())
        while self._running:
            cpu = psutil.cpu_percent(interval=None)
            mem = process.memory_info().rss / (1024 * 1024)  # MB
            self.cpu_log.append(cpu)
            self.mem_log.append(mem)
            time.sleep(self.interval)

    def stop(self):
        self._running = False
        self.thread.join()

    def save_log(self, filename="resource_log.csv"):
        with open(filename, "w") as f:
            f.write("time_sec,cpu_percent,memory_mb\n")
            for i, (cpu, mem) in enumerate(zip(self.cpu_log, self.mem_log)):
                f.write(f"{i * self.interval:.2f},{cpu:.2f},{mem:.2f}\n")

# ---------------- FFT Matcher ----------------

def fft_string_matching_optimized(text: str, pattern: str):
    n = len(text)
    m = len(pattern)

    if n < m:
        raise ValueError("Pattern length must be less than or equal to text length.")

    total_match_score = np.zeros(n - m + 1)
    reversed_pattern = pattern[::-1]

    for base in "ACGT":
        t_vec = (np.array(list(text)) == base).astype(int)
        p_vec = (np.array(list(reversed_pattern)) == base).astype(int)

        base_match_score = fftconvolve(t_vec, p_vec, mode='valid')
        total_match_score += base_match_score

    rounded_scores = np.round(total_match_score)
    match_indices = np.where(rounded_scores == m)[0].tolist()
    return match_indices

# ---------------- Utils ----------------

def load_pattern_and_positions(filename):
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()
    pattern_line = lines[0]
    if not pattern_line.startswith("Search Pattern: "):
        raise ValueError("First line must start with 'Search Pattern: '")
    pattern = pattern_line[len("Search Pattern: "):]
    positions = [int(line) for line in lines[1:] if line.strip().isdigit()]
    return pattern, positions

def load_text(filename):
    with open(filename, "r") as f:
        return f.read()

def compare_matches(correct_positions, found_positions):
    correct_set = set(correct_positions)
    found_set = set(found_positions)

    correct_only = correct_set - found_set
    found_only = found_set - correct_set
    matched = correct_set & found_set

    print(f"Number of correct matches: {len(correct_positions)}")
    print(f"Number of found matches: {len(found_positions)}")
    print(f"Number of matches correctly found: {len(matched)}")
    if correct_only:
        print(f"Matches missed (correct but not found): {sorted(correct_only)}")
    if found_only:
        print(f"False positives (found but not correct): {sorted(found_only)}")

# ---------------- Main ----------------

def main():
    dna_text_file = "dna_text.txt"
    dna_positions_file = "dna_positions.txt"

    dna_sequence = load_text(dna_text_file)
    pattern, correct_positions = load_pattern_and_positions(dna_positions_file)

    print(f"Text length: {len(dna_sequence):,}")
    print(f"Pattern length: {len(pattern):,}")
    print("\nRunning fft-convolution matching with resource monitoring...")

    monitor = ResourceMonitor(interval=0.1)
    monitor.start()

    start_time = time.time()
    found_positions = fft_string_matching_optimized(dna_sequence, pattern)
    end_time = time.time()

    monitor.stop()
    monitor.save_log("resource_log.csv")

    print(f"\nFinished in {end_time - start_time:.4f} seconds.")
    print(f"Found {len(found_positions):,} matches.")
    compare_matches(correct_positions, found_positions)

if __name__ == "__main__":
    main()
