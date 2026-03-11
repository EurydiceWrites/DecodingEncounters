import time
import sys

def watch_log():
    log_file = "motif_log5.txt"
    end_string = "Phase 2 LLM Ingestion Complete"
    error_string = "Error processing chunk"
    timeout = 7200 # 2 hours
    start = time.time()
    
    print("Watcher started. Waiting for completion...")
    
    while time.time() - start < timeout:
        try:
            with open(log_file, "r") as f:
                lines = f.readlines()
                if not lines:
                    time.sleep(30)
                    continue
                
                last_few = "".join(lines[-10:])
                
                if end_string in last_few:
                    print(f"\n[SUCCESS] Script Finished!\n{last_few}")
                    sys.exit(0)
                elif error_string in last_few:
                    print(f"\n[FAILED] Script Errored Out:\n{last_few}")
                    sys.exit(1)
        except Exception as e:
            pass
        
        # Check every 45 secs to match the quota sleep timer
        time.sleep(45)
        
    print("Watcher timed out after 2 hours.")
    sys.exit(1)

if __name__ == "__main__":
    watch_log()
