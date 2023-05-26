*******************************************************************************
*                                                                             *
*                BLINK DETECTOR SENSIBLE TO FACIAL ORIENTATION                *
*                               BY NORINA GROSCH                              *
*                                                                             *
*******************************************************************************

REQUIREMENTS:

- python 3.9
- packages: opencv-python, mediapipe, numpy, math, csv, time
- webcam

USAGE:

To use the blink detector, execute the program via shell or terminal.
It will open a video stream of your webcam and the facial orientation and 
number of counted blinks will be shown on the stream. 

To exit the program press 'ESC'.

In the background a csv file will be created. It contains:
'time'  - time in seconds since program was executed
'blink' - bool, True if subject blinked
'ratio' - average ratio of both eyes openness
'ratio_r' - ratio of right eyes openness
'ratio_l' - ratio of left eyes openness
'counted' - number of counted blinks
'orientation'  - facial orientation, l = left, r = right, d = down, f = forward
'still_closed' - bool, is true as long as eyes are closed (eg. longer blink)
'blink_length' - time difference in seconds to last measurement, adds up if 
                 still closed is True

Depending on the facial orientation different ratios are used to determine if 
eyes are closed based on comparison to a threshold. If the face is forward or 
downward oriented the average ratio of both eyes is used. 
If the face is oriented to the left, only the ratio of the right eye will be 
used. Vice versa if the face is oriented to the right.

NOTE:

The program is sensible to camera positioning. It works best when the angle of 
the camera is on the same hight as the eyes. When it is higher looking forward
still works well for me, but looking left or right is counting more 
blinks than actually happened. 
For looking downward it is also harder for the program to determine the blinks 
correctly. 

Works better when the subject does not wear glasses.

REFERENCES:

https://medium.com/@aiphile/eyes-blink-detector-and-counter-mediapipe-a66254eb002c 
https://towardsdatascience.com/head-pose-estimation-using-python-d165d3541600