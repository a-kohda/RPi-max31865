#!/bin/bash

for CS in 19 20 21 # 値を読むCSのGPIOピン番号のリスト 
do
  OHM=`python RPi_max31865.py ${CS}`
  TEMP=`./ohm_to_celsius ${OHM}`
  echo -n "${TEMP},"
done

echo ""
