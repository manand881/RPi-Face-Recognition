# Documentation

This document will contain my learning journey so far with regard to what i've learnt about this project. This is an informal document.

## Hurdles.

* Though Ubuntu may be a posished operating system it lacks a few things on the raspberry pi such as being able to run 
```
pip install picamera
pip install picamera[array]
```
My understanding of the picamera library is that it is not built for ubuntu and cannot be installed on ubuntu using the usual method. Ive tried this on ubuntu 20.04LTS. i may have to try to run the code on a different operating system such as 18.04LTS. there is an option to compile the library from scratch is what i believe.

* while trying to use the picamera[array] library i found that the library has a certain set of issues with opencv and numpy which requires a lot of work to fix. numpy must be upgraded using ```pip install -U numpy``` and the version number must be 1.8.0.

* while trying to uninstall python2 and python3 both from the rpi, i find that sometimes the pi does not boot up after the uninstallation. i have tried to reboot the pi and it still does not boot up. there is a browish screen that appears instead of the gui.
  
*  While using the Pi a good indicator of the SD card not functioning properly is when the green light does not blink often. the green light is on when the SD card is working properly and is reading and writing files to the SD card normally. This issue may be either due to the SD card not being plugged in correctly or the SD card not being formatted correctly. Static electricity also seems to cause an issue. I have been using the official Rpi power adapter.

* A proper casing is required for the Raspberry pi to operate properly. I had kept the raspberry pi on a rubber pad assuming that it is a good insulator and will prevent static electricity buildup. I have found that it causes static electricity buildup due to charge isolation. This causes the pi to not function properly. keeping it on my bed seemed to help a lot more.

* The video memory allotted to the pi by default is 64MB in models with 1gb of ram and 76MB for models with more ram. though this number is adjustable, the maximum recommended amount is 128MB. configuring a number higher than 128MB may cause the pi to crash or not boot up properly from the next boot.
  
* Enabling the CSI camera module on the pi is a must. this is a requirement for the picamera library to work. for some reason this took a couple of tries for it to function normally. even though i enabled it both in the configuration tab in the menu bar and in the ``` sudo raspi-config``` utility. the changes did not seem to reflect properly in the terminal while running the code.
  
* There was one instance when ```cv2.VideoCapture(0)``` led to the CSI camera being used rather than the USB camera. to access the USB camera, I had to change the 1 to 0 and try again

* I have come to realise that there will always be a lag of some sort on the raspberry pi while using haarcascade since each core on the raspberry pi isn't really that strong when compared to an x86 processor. the lag occurs due to the processing time of the classifier.
* The right camera module has to be chosen when using a csi camera module since low exposure modules lead to darker images which dont work on the haarcascade classifier
* It is worth exploring performing face detection and recognition on every other frame rather than every frame because the face isnt really going to go anywhere within the span of a single frame when you are capturing frames at 30FPS. one can assume that the subject's face isnt really moving fast.
* i have tried to use generators to name files, but there seems to be an issue with being able to do the same. i am naming files according to the current time since i can expect the system time to be a unique string.
* Running a flask app on debug mode spawns the api recieve process twice which causes a conflit output. flask must run in ```debug=false```
* while running the docker container the container must run in python unbuffered mode so all the print statements print instantly without any buffer, other wise the print statement do not open up on time and cause lots of issues. 