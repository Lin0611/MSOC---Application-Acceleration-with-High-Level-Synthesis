#include "fir.h"

out_data_t fir_filter (inp_data_t x,   coef_t c[N])
{


#pragma HLS INTERFACE s_axilite port=x
#pragma HLS INTERFACE s_axilite port=c
#pragma HLS INTERFACE s_axilite port=return

static inp_data_t shift_reg[N];
#pragma HLS array_partition variable=c complete
  acc_t acc = 0;
  acc_t mult;
  out_data_t y;
#pragma HLS pipeline II=1
  Shift_Accum_Loop: for (int i=N-1;i>=0;i--)
  {
#pragma HLS LOOP_TRIPCOUNT min=1 max=16 avg=8
     if (i==0){
       //acc+=x*c[0];
       shift_reg[0]=x;
     }
     else{
			shift_reg[i]=shift_reg[i-1];
			//acc+=shift_reg[i]*c[i];
     }
     mult = shift_reg[i]*c[i];
     acc  = acc + mult;
  }
  y = (out_data_t) acc;
  return y;
}
