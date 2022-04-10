# UnboxTheGoose

Welcome to UnboxTheGoose! We are a team of five students from the University of Waterloo in the Software Engineering program, and created this project as a final project for one of our courses. [Video](https://youtu.be/EJQF64A8H0g) of the project in action!

# The Machine

Our machine uses two cameras to read in the position of a Rubik's Cube, and then uses mechanical arms to physically solve it.

![image](https://user-images.githubusercontent.com/51809855/146691724-e9d1ea17-ead2-402f-aab6-25c1c152c526.png)

# Implementation Overview

The backbone for our solver uses a bitboard system to allow for fast computations using Python! Using a very simple data type allows for minimal computational efforts to be wasted. The actual solving algorithm is based on techniques used by speedcubers.
