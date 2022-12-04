# <p align="center">self-checkout</p>

This is a self-checkout system base on pre-trained object detection model. There are two steps in this self-checkout system.
The first step is object detection. The system will turn on a camera to detect and recognize things that appears in the frame.
Second, the system will search those items' price in the google sheet with google-sheet-api for calculating total cost. 
Furthermore, the system will also sales records into a google sheet for further data mining.
