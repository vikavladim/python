import threading
import time
from threading import Lock
import random

count_doctors = 5
start_doctor = 9


class Doctor():
    def __init__(self, index, screwdriver_left, screwdriver_right):
        self.index = index
        self.screwdriver_left = screwdriver_left
        self.screwdriver_right = screwdriver_right

    def blast(self):
        while True:
            self.screwdriver_left.get()
            self.screwdriver_right.get()

            print(f'Doctor {self.index}: BLAST!')

            self.screwdriver_left.put()
            self.screwdriver_right.put()

            time.sleep(random.random() * 5)


class Screwdriver():
    def __init__(self):
        self.lock = Lock()

    def get(self):
        self.lock.acquire()

    def put(self):
        self.lock.release()


if __name__ == '__main__':
    screwdrivers = [Screwdriver() for _ in range(count_doctors)]
    doctors = [Doctor(i + start_doctor, screwdrivers[i],
                      screwdrivers[(i + 1) % count_doctors]) for i in range(count_doctors)]
    random.shuffle(doctors)

    threads = [threading.Thread(target=i.blast) for i in doctors]
    for i in threads:
        i.start()

    for i in threads:
        i.join()
