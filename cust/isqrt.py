import time
import numpy as np
from functools import wraps
from time import time
import struct

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' %(f.__name__, args, kw, te-ts))
        return result
    return wrap

def isqrt(l):
    return l **(-1/2)   # equiv to:  z * 1/sqrt(l)

def isqrt_raw(number):
    a = float(number) # number to get square root of
    for i in range(500): # iteration number
        number = 0.5 * (number + a / number) # update
    return 1/number

def newtonSqrt(n):
    approx = 0.5 * n
    better = 0.5 * (approx + n/approx)
    while better != approx:
        approx = better
        better = 0.5 * (approx + n/approx)
    return 1/ approx

def struct_isqrt(number):
    x2 = number * 0.5
    
    packed_y = struct.pack('f', number)       
    i = struct.unpack('i', packed_y)[0]  # treat float's bytes as int 
    i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
    packed_i = struct.pack('i', i)
    number = struct.unpack('f', packed_i)[0]  # treat int's bytes as float
    
    number = number * (1.5 - (x2 * number * number))  # Newton's method
    return number

def numpy_isqrt(number):
    threehalfs = 1.5
    x2 = number * 0.5
    y = np.float32(number)
    
    i = y.view(np.int32)
    i = np.int32(0x5f3759df) - np.int32(i >> 1)
    y = i.view(np.float32)
    
    y = y * (threehalfs - (x2 * y * y))
    return float(y)


@timing
def callme(f, n):
    l = 62532433
    for x in range(n):
        y = f(l)
        # l = l/1.15
    print(f"sqrt of {l} is {y}")

n=500000
print ('starting...')
callme(isqrt, n)
callme(isqrt_raw, n)
callme(newtonSqrt, n)
callme(numpy_isqrt, n)
callme(struct_isqrt, n)
print ('... end')
