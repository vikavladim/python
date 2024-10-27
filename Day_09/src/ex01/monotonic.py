import ctypes
import os
import sys
import time

if os.name == 'nt':
    lib=ctypes.windll.kernel32
    def monotonic():
        ticks = lib.GetTickCount()
        if ticks < monotonic.last:
            # Integer overflow detected
            monotonic.delta += 2**32
        monotonic.last = ticks
        return (ticks + monotonic.delta) * 1e-3
    monotonic.last = 0
    monotonic.delta = 0

# elif sys.platform == 'darwin':
#     print('darwin')
    # def monotonic():
    #     if monotonic.factor is None:
    #         factor = _time.mach_timebase_info()
    #         monotonic.factor = timebase[0] / timebase[1] * 1e-9
    #     return _time.mach_absolute_time() * monotonic.factor
    # monotonic.factor = None

# elif hasattr(time, "clock_gettime") and hasattr(time, "CLOCK_HIGHRES"):
#     print('linux highres')
    # def monotonic():
    #     return time.clock_gettime(time.CLOCK_HIGHRES)

elif hasattr(time, "clock_gettime") and hasattr(time, "CLOCK_MONOTONIC"):
    lib=ctypes.CDLL('librt.so.1', use_errno=True)

    CLOCK_MONOTONIC=4
    class timespec(ctypes.Structure):
        _fields_ = [
            ('tv_sec', ctypes.c_long),
            ('tv_nsec', ctypes.c_long)
        ]

    ts=timespec(0,0)

    def monotonic():
        lib.clock_gettime(CLOCK_MONOTONIC, ctypes.byref(ts))
        return ts.tv_sec + ts.tv_nsec / 1e9
