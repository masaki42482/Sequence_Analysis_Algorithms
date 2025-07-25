import psutil
import os
import threading
import time

class ResourceMonitor:
    def __init__(self, interval=0.1):
        self.interval = interval
        self.cpu_log = []
        self.mem_log = []
        self._running = False
        self.start_time = 0.0
        self.end_time = 0.0
        self.execution_time = 0.0

    def start(self):
        self._running = True
        self.start_time = time.time()
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
        if self._running:
            self._running = False
            self.thread.join()
            self.end_time = time.time()
            self.execution_time = self.end_time - self.start_time
            print(f"\nFinished in {self.execution_time:.4f} seconds.")


    def save_log(self, filename="resource_log.csv"):
        log_dir = "log"

        os.makedirs(log_dir, exist_ok=True)

        filepath = os.path.join(log_dir, filename)

        with open(filepath, "w") as f:
            f.write("time_sec,cpu_percent,memory_mb\n")
            for i, (cpu, mem) in enumerate(zip(self.cpu_log, self.mem_log)):
                f.write(f"{i * self.interval:.2f},{cpu:.2f},{mem:.2f}\n")
            
            f.write("\n")
            f.write(f"Total Execution Time,{self.execution_time:.4f},seconds\n")
        
        print(f"Resource log saved to {filepath}")


if __name__ == "__main__":
    monitor = ResourceMonitor(interval=0.1)

    monitor.start()

    print("Running a sample task for 3 seconds...")
    result = [i**2 for i in range(10**7)]

    monitor.stop()
    
    monitor.save_log()