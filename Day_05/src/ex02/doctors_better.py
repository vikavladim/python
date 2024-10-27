import asyncio
import random


class Screwdriver:
    def __init__(self, index):
        self.is_locked = False
        self.index = index

    async def get(self):
        if self.is_locked:
            return False
        else:
            self.is_locked = True
            # print(f'Screwdriver {self.index}: GET!')
            return True

    async def put(self):
        if self.is_locked:
            self.is_locked = False
            # print(f'Screwdriver {self.index}: PUT!')
            return True
        else:
            return False


class Doctor:

    def __init__(self, index, screwdriver_left, screwdriver_right):
        self.index = index
        self.screwdriver_left = screwdriver_left
        self.screwdriver_right = screwdriver_right

    async def blast(self):
        while True:
            if await self.screwdriver_left.get() and await self.screwdriver_right.get():
                print(f'Doctor {self.index}: BLAST!')
                await self.screwdriver_left.put()
                await self.screwdriver_right.put()
                await asyncio.sleep(random.random() * 5)


async def main():
    screwdrivers = [Screwdriver(i) for i in range(5)]
    doctors = [Doctor(i, screwdrivers[i % 5], screwdrivers[(i + 1) % 5]) for i in range(9, 14)]

    tasks = [asyncio.create_task(doctor.blast()) for doctor in doctors]

    # for task in tasks:
    #     await task

    await asyncio.gather(*tasks)

asyncio.run(main())
