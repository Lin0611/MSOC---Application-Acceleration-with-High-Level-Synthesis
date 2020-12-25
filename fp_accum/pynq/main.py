from __future__ import print_function

import sys
import numpy as np
from random import seed
from random import random
from time import time
import matplotlib.pyplot as plt 

sys.path.append('/home/xilinx')
from pynq import Overlay
from pynq import allocate

import struct

def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

if __name__ == "__main__":
    print("Entry:", sys.argv[0])
    print("System argument(s):", len(sys.argv))

    print("Start of \"" + sys.argv[0] + "\"")

    ol = Overlay("/home/xilinx/IPbitFile/itlin/fp_accum/design_1.bit")
    ipFP_ACCUM = ol.hls_fp_accumulator_0

    # generate random number
    seed(1)
    window = []
    for i in range(128):
        window.append(random())
        
    

    # allocate input array
    inBuffer0 = allocate(shape=(128), dtype=np.float32)
    for i in range(128):        
        inBuffer0[i] = float(window[i])
        #print(inBuffer0[i], window[i])
    

    timeKernelStart = time()
    
    # setup the ip ...
    ipFP_ACCUM.write(0x10, inBuffer0.device_address)
    ipFP_ACCUM.write(0x00, 0x01)
    while (ipFP_ACCUM.read(0x00) & 0x4) == 0x0:
        continue
    timeKernelEnd = time()
    print("============================")
    print("Kernel execution time: " + str(timeKernelEnd - timeKernelStart) + " s")

    
    hw_res = ipFP_ACCUM.read(0x18)
    hw_res = "{0:032b}".format(hw_res)
    hw_res = bin_to_float(hw_res)
    sw_res = np.float32(0.0)
    for i in range(128):
        sw_res += np.float32(window[i])

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
