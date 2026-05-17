import threading
import queue
import random
import time
import math

BLOCK_SIZE = 100

# Shared queue
data_queue = queue.Queue()

# -------------------------------------------------
# Producer Thread (Sensor)
# -------------------------------------------------

def sensor():

    while True:

        r = random.random()

        # Simulate missing sample
        if r < 0.05:
            sample = None

        # Simulate corrupted sample
        elif r < 0.10:
            sample = random.randint(101, 150)

        # Valid sample
        else:
            sample = random.randint(0, 100)

        data_queue.put(sample)

        # Sensor sampling rate
        time.sleep(0.001)   # 1000 samples/sec


# -------------------------------------------------
# Consumer Thread (Processor)
# -------------------------------------------------

def processor():

    block = []
    block_number = 1

    while True:

        sample = data_queue.get()
        block.append(sample)

        # Process every 100 samples
        if len(block) == BLOCK_SIZE:

            valid_samples = []

            missing_samples = 0
            corrupted_samples = 0

            # -----------------------------------------
            # Validate samples
            # -----------------------------------------

            for value in block:

                # Missing sample
                if value is None:
                    missing_samples += 1

                # Corrupted sample
                elif value < 0 or value > 100:
                    corrupted_samples += 1

                # Valid sample
                else:
                    valid_samples.append(value)

            # Prevent divide-by-zero
            if len(valid_samples) == 0:
                print("\nNo valid samples found.")
                block = []
                continue

            # -----------------------------------------
            # Statistical calculations
            # -----------------------------------------

            maximum = max(valid_samples)
            minimum = min(valid_samples)

            average = sum(valid_samples) / len(valid_samples)

            variance = 0

            for value in valid_samples:
                variance += (value - average) ** 2

            variance /= len(valid_samples)

            standard_deviation = math.sqrt(variance)

            # -----------------------------------------
            # Display results
            # -----------------------------------------

            print("\n=================================================")
            print("Processing Block :", block_number)
            print("=================================================")

            print("Maximum Value                :", maximum)
            print("Minimum Value                :", minimum)
            print("Average (Mean)               :", round(average, 2))
            print("Standard Deviation           :", round(standard_deviation, 2))
            print("Missing Samples              :", missing_samples)
            print("Corrupted / Invalid Samples  :", corrupted_samples)

            # Clear block
            block = []

            block_number += 1


# -------------------------------------------------
# Main
# -------------------------------------------------

t1 = threading.Thread(target=sensor)
t2 = threading.Thread(target=processor)

t1.daemon = True

t1.start()
t2.start()

t2.join()
