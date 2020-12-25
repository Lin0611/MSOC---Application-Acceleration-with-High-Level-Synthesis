/************************************************
Copyright (c) 2016, Xilinx, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software 
without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.// Copyright (c) 2016 Xilinx, Inc.
************************************************/

//#pragma HLS ARRAY_PARTITION variable=a complete
//#pragma HLS ARRAY_PARTITION variable=b complete
//#pragma HLS PIPELINE II=1

#include "../src/diff_sq_acc.h"

void diff_sq_acc(din_t a[N], din_t b[N], dout_t *dout)
{
	#pragma HLS INTERFACE s_axilite port=dout
	#pragma HLS INTERFACE m_axi depth=128 port=a offset=slave
	#pragma HLS INTERFACE m_axi depth=128 port=b offset=slave
	#pragma HLS INTERFACE s_axilite port=return


	#pragma HLS ARRAY_PARTITION variable=a complete
	#pragma HLS ARRAY_PARTITION variable=b complete
	int i;
	int acc= 0;
	int a_reg, b_reg, sub, sub2;
#pragma HLS PIPELINE II=1
	for(i=0; i<N; i++)
	{
		a_reg  = a[i];
		b_reg  = b[i];
		sub = a_reg - b_reg;
		sub2 = sub*sub;
		acc += sub2;
	}
	*dout = acc;
}






