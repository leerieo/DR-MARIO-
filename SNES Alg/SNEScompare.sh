#Compare outputs of nightmareci's main.c for the SNES algorithm
#with SNES-single-player.py for level 21
#starting from level 21, there are "bad seeds" where the virus generator algorithm
#generates fewer viruses than expected - should check this

#NOTE1: to run shell script, must change permission modes for script
#NOTE2: output of main.c should be in a file named main
#gcc fileName.c -o main

for i in in {0..66535}
do
  seed=$(echo "obase=16; $i" | bc)
  #echo "seed: $seed"

  commandA="./main 21 $seed"
  commandB="python SNES-single-player.py 21 $seed"
  diff <($commandA) <($commandB)

done
