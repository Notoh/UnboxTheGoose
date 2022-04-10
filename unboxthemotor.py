import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
control_pins = [[12, 16, 18, 22], #white
                [7,11,13,15], #orange
                [29,31,33,35], #green
                [19, 21, 23, 24], #red
                [36, 38, 40, 37]] #blue

faces = [[1, 1, 4, 1, 0, 0, 3, 5, 5],
        [5, 0, 4, 3, 1, 5, 0, 1, 5],
        [0, 4, 4, 2, 2, 0, 2, 2, 3],
        [3, 3, 1, 4, 3, 1, 2, 3, 1],
        [0, 4, 4, 2, 4, 4, 2, 2, 1],
        [3, 3, 0, 5, 5, 5, 2, 0, 5]]

for group in control_pins:
  for pin in group:
     GPIO.setup(pin, GPIO.OUT)
     GPIO.output(pin, 0)
seq = [
  [1,0,0,1],
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1]
]

steps = len(halfstep_seq)
waitTime = 2 / float(1000)


def rotate(face, times, direction):
  degree = int(90 * times * 11.377777777777)
  seqPos = 0
  
  for step in range(0, degree):
    for pin in range(0, 4):
       realPin = control_pins[face][pin]
       if seq[seqPos][pin] != 0:
         GPIO.output(realPin, True)
       else:
         GPIO.output(realPin, False)
    seqPos += direction
    if(seqPos >= steps):
      seqPos = 0
    if(seqPos < 0):
      seqPos = steps + direction
    time.sleep(waitTime)

GPIO.cleanup()
