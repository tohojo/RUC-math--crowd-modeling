import threading, multiprocessing

thread_no = multiprocessing.cpu_count()

def run_in_threads(objects, method, args):
    """Function to run a method on a number of objects in worker threads"""

    def run_in_thread(objects, method, args):
        for o in objects:
            getattr(o, method)(*args)


    chunks = []
    threads = []
    chunk_len = len(objects)/thread_no
    next_chunk = 0

    while next_chunk < len(objects):
        chunks.append(objects[next_chunk:next_chunk+chunk_len+1])
        next_chunk += chunk_len+1

    for c in chunks:
        thread = threading.Thread(target=run_in_thread, args=(c, method, args))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()
