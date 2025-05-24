import threading
import queue

class DownloadWorker(threading.Thread):
    def __init__(self, que=None, *args, **kwargs):
        self.queue = que or queue.Queue()
        super().__init__(*args, **kwargs)
    
    def run(self):
        while True:
            try:
                # Placeholder for download logic
                item = self.queue.get(timeout=3)  # 3s timeout
                # Simulate download or processing
                print(f"Processing: {item}")
                self.queue.task_done()
            except queue.Empty:
                return
            except Exception as e:
                print(f"Error in download worker: {e}")
                self.queue.task_done()