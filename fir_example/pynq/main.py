from __future__ import print_function
import math
import sys
import numpy as np
from time import time
import matplotlib.pyplot as plt 

sys.path.append('/home/xilinx')
from pynq import Overlay
from pynq import allocate

if __name__ == "__main__":
    print("Entry:", sys.argv[0])
    print("System argument(s):", len(sys.argv))

    print("Start of \"" + sys.argv[0] + "\"")
    
    ol = Overlay("/home/xilinx/IPBitFile/itlin/fir_example/design_1.bit")
    ipFIRF18 = ol.fir_filter_0
    
    fiSamples = open("input.dat", "r+") #input
    Ref = open("ref_res.dat", "r+")
    numSamples = 0
    line = fiSamples.readline()

    while line:
        numSamples = numSamples + 1
        line = fiSamples.readline()
  

    temp0 = allocate(shape=(numSamples,), dtype=np.int32)
    reference = allocate(shape=(numSamples,), dtype=np.float64)
 
    inBuffer0 = allocate(shape=(numSamples,), dtype=np.int32)

    Ref.seek(0)
    fiSamples.seek(0)
    for i in range(numSamples):
        line = fiSamples.readline()
        temp0[i] = math.floor(float(line)*2**16)
        line_ref = Ref.readline()
        reference[i] = float(line_ref)

    fiSamples.close()
    numTaps = 16
    f18Taps = allocate(shape=(numTaps,), dtype=np.int32)
    
    f18Taps = [0.180617, 0.045051, 0.723173, 0.347438, 0.660617, 0.383869, 0.627347, 0.021650, 0.910570,
    0.800559, 0.745847, 0.813113, 0.383306, 0.617279, 0.575495, 0.530052]
    new_f18Taps = [math.floor(i * 2**16) for i in f18Taps]

    timeKernelStart = time()
    #COEF

    output = allocate(shape=(numSamples,), dtype=np.float64)
    
    for i in range(numSamples):
        ipFIRF18.write(0x1c, int(temp0[i]))
        for j in range(numTaps): # 0~7
            ipFIRF18.write(0x24 + j * 8, new_f18Taps[j])    
        ipFIRF18.write(0x00, 0x1)
        a = ipFIRF18.read(0x10)
        b = ipFIRF18.read(0x14)
        output[i] = (b*2**32+a)*2**(-36)
        while (ipFIRF18.read(0x00) & 0x4) == 0x0:
            continue
    tot_diff = 0
    for i in range(numSamples):
        print("output = %.5f"%output[i], " ref = %.5f"%reference[i])
        diff = abs(output[i]-reference[i])
        tot_diff += diff
    if (tot_diff < 1.0):
        print("TEST PASSED")
    else:
        print("TEST FAILED")
    timeKernelEnd = time()

    print("============================")
    print("Exit process")
