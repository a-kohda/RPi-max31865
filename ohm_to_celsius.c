#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]){
  float R0, R, dR, T;
  R0 = 100;
  R  = atof(argv[1]);
  T  = (R/100 - 1)/ 3.9083e-3;
  dR = R-R0*((((- 4.183e-12*T+4.183e-10)*T-5.775e-7)*T+3.9083e-3)*T+1.0);
  T  = T+dR/R0/(((-4.183e-12*2.0*T+4.183e-10)*T-5.775e-7*2)*T+3.9083e-3);
  dR = R-R0*((((- 4.183e-12*T+4.183e-10)*T-5.775e-7)*T+3.9083e-3)*T+1.0);
  T  = T+dR/R0/(((-4.183e-12*2.0*T+4.183e-10)*T-5.775e-7*2)*T+3.9083e-3);

  printf("%.2f\n",T);
  return 0;
}
