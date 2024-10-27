import os
import unittest
from monotonic import *
import time


class TestMonotonic(unittest.TestCase):
    def test_monotonic(self):
        if os.name == 'nt':
            print('windows')
        elif hasattr(time, "clock_gettime") and hasattr(time, "CLOCK_MONOTONIC"):
            print('linux monotonic')
        else:
            print('no support system')
            return

        start=monotonic()
        time.sleep(1)
        end=monotonic()
        self.assertAlmostEqual(end-start, 1, delta=3e-3)




if __name__ == '__main__':
    unittest.main()
