'''inverse sqrt test'''

from ctypes import c_float, c_int32, cast, byref, POINTER

def ctypes_isqrt(number):
    threehalfs = 1.5
    x2 = number * 0.5
    y = c_float(number)

    i = cast(byref(y), POINTER(c_int32)).contents.value
    i = c_int32(0x5f3759df - (i >> 1))
    y = cast(byref(i), POINTER(c_float)).contents.value

    y = y * (1.5 - (x2 * y * y))
    return y

def numpy_isqrt(number):
    threehalfs = 1.5
    x2 = number * 0.5
    y = np.float32(number)
    
    i = y.view(np.int32)
    i = np.int32(0x5f3759df) - np.int32(i >> 1)
    y = i.view(np.float32)
    
    y = y * (threehalfs - (x2 * y * y))
    return float(y)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100

    left = calc(101)
    right = -18.67
    if abs(left - right) > 0.1:
        print("%f != %f" % (left, right), file=sys.stderr)
        quit(1)

    notify("%s\t%d" % (platform.python_implementation(), os.getpid()))
    results = calc(n)
    notify("stop")

    print(results)
