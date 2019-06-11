from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
s = []
def f(a):
    global s
    r = random.randrange(5)
    s.append(r)
    return time.sleep(r)
# .shutdown() in exit
with ThreadPoolExecutor(max_workers=3) as pool:
    results = [pool.submit(f, i) for i in range(10)]
    timer = time.time()
    for future in as_completed(results):
        print(future.result())
    print(time.time() - timer, sum(s), max(s))
