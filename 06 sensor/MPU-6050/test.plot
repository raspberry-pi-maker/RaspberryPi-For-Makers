set terminal wxt size 1500, 500
plot "6050_1.dat" using 1:5 t "X Rotate", "6050_1.dat" using 1:6 t "Y Rotate", "6050_1.dat" using 1:7 t "Z Rotate";
pause -1 "Hit return to continue"