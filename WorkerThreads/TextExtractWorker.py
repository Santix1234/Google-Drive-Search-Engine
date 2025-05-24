import threading
import queue
import textract
import os

class TextExtractWorker(threading.Thread):
    def __init__(self, que=None, *args, **kwargs):
        self.queue = que or queue.Queue()
        super().__init__(*args, **kwargs)
    
    def run(self):
        while True:
            try:
                filepath = self.queue.get(timeout=3)  # 3s timeout
            except queue.Empty:
                return
            
            try:
                text = textract.process(filepath)
                text = str(text, 'utf-8', 'ignore')
                pre, _ = os.path.splitext(os.path.basename(filepath))
                
                # Ensure ExtractedText directory exists
                os.makedirs('ExtractedText', exist_ok=True)
                
                with open(os.path.join("ExtractedText", pre+".txt"), "w") as f:
                    f.write(text)
                
                self.queue.task_done()
            except Exception as e:
                print(f"Error processing {filepath}: {e}")
                self.queue.task_done()