
from __future__ import print_function

import sys
import numpy as np
from random import seed
import random
from time import time
import matplotlib.pyplot as plt 

sys.path.append('/home/xilinx')
from pynq import Overlay
from pynq import allocate

import struct

if __name__ == "__main__":
    print("Entry:", sys.argv[0])
    print("System argument(s):", len(sys.argv))

    print("Start of \"" + sys.argv[0] + "\"")

    ol = Overlay("/home/xilinx/IPbitFile/itlin/diff_sq_acc/design_1.bit")
    diff_sq_acc = ol.design_1_wrapper

    # generate random data
    seed(1)
    a = []
    for i in range(10):
        a.append(random.randint(0,10))
    b = []
    for i in range(10):
        b.append(random.randint(0,10))   
    

    # allocate input array
    inBuffer_a = allocate(shape=(10), dtype=np.int16)
    for i in range(10):        
        inBuffer_a[i] = a[i]
    inBuffer_b = allocate(shape=(10), dtype=np.int16)
    for i in range(10):        
        inBuffer_b[i] = b[i] 

    timeKernelStart = time()
    
    # setup the ip ...
    diff_sq_acc.write(0x10, inBuffer_a.device_address)
    diff_sq_acc.write(0x18, inBuffer_b.device_address)
    diff_sq.acc.write(0x00, 0x01)
    while (diff_sq_acc.read(0x00) & 0x4) == 0x0:
        continue
    timeKernelEnd = time()
    print("============================")
    print("Kernel execution time: " + str(timeKernelEnd - timeKernelStart) + " s")

    
    hw_res = diff_sq_acc.read(0x20)
    hw_res = "{0:032b}".format(hw_res)
   
    sw_res = np.int64(0)
    for i in range(10):
        sw_res += np.int16((a[i] - b[i]) ** 2)

    total_error = 0.0
    total_error = sw_res - hw_res
    if(total_error<0):
        total_error = 0-total_error
    #print(window)
    print("software sum: ", sw_res)
    print("hardware sum: ", hw_res)
    print("total error: ", total_error)
    if (total_error < 1.0):
        print("TEST OK!\n")
    else:
        print("TEST FAILED!\n")
      
    print("============================")
    print("Exit process")
