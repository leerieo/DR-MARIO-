#Compare outputs of nightmareci's main.c for the SNES algorithm
#with SNES-single-player.py for level 10


#NOTE: output of main.c should be in a file named main  (gcc fileName.c -o main)

for i in in {0..66535}
do
  seed=$(echo "obase=16; $i" | bc)
  echo "seed: $seed"

  commandA="./main 10 $seed"
  commandB="python SNES-single-player.py 10 $seed"
  diff <($commandA) <($commandB)

done
