import threading
import queue
import random
import time

BLOCK_SIZE = 100

data_queue = queue.Queue()

# Producer thread
def sensor():
    while True:
        sample = random.randint(0, 100)
        data_queue.put(sample)

        time.sleep(0.001)  # sensor sampling rate 1000samples/sec


# Consumer thread
def processor():
    block = []

    while True:
        sample = data_queue.get()
        block.append(sample)

        if len(block) == BLOCK_SIZE:
            print("Processing block of 100 samples")

            maximum = max(block)
            minimum = min(block)
            average = sum(block) / BLOCK_SIZE

            print("Max:", maximum)
            print("Min:", minimum)
            print("Average:", average)

            block = []


t1 = threading.Thread(target=sensor)
t2 = threading.Thread(target=processor)

t1.start()
t2.start()