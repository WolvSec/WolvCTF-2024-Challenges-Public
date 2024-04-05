#!/bin/bash

date

echo "-------- solving misc: made sense..."
cd ../misc/make1_madesense
python3 solve.py

cd - > /dev/null

echo "-------- solving misc: made functional..."
cd ../misc/make2_madefunctional
python3 solve.py

cd - > /dev/null

echo "-------- solving misc: made harder..."
cd ../misc/make3_madeharder
python3 solve.py

cd - > /dev/null


echo "-------- solving misc: made with love..."
cd ../misc/make4_madewithlove
python3 solve.py

cd - > /dev/null

echo "-------- solving beginner web: gauntlet..."
cd ../beginner/web/gauntlet/solution
python3 solve-gauntlet.py

cd - > /dev/null

echo "-------- solving web: bean-cafe..."
cd bean-cafe/solution
python3 solve.py

cd - > /dev/null

echo "-------- solving web: upload-fun..."
cd upload-fun/solution
python3 solve-upload-fun.py

cd - > /dev/null

echo "-------- solving web: username..."
cd username/solution
python3 solve-username.py

cd - > /dev/null


echo "-------- solving web: order-up1..."
cd order-up/solution
python3 solve-order-up1.py

cd - > /dev/null

echo "-------- solving web: order-up2..."
cd order-up/solution
python3 solve-order-up2.py

cd - > /dev/null

echo "-------- solving web: order-up3..."
cd order-up/solution
python3 solve-order-up3.py

cd - > /dev/null

echo "-------- solving web: order-up4..."
cd order-up/solution
python3 solve-order-up4.py

cd - > /dev/null

date