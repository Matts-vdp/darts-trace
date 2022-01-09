Matts Van Der Poel
# Darts tracer
When throwing a dart the trajectory should be fluent. When you're training its common to have a
wobble in the trajectory but it’s hard to detect this when focussing on the throw. To try to detect this
a video is made of the throw.
This program traces the front and back of the dart. This way you can clearly see the difference in trajectory between both.
This can be seen in the example below.

## Usage
- Run Darts_trace.py
- Enter the filename of the video you want to analyse 
- Enter the filename of the output video or leave empty for "out.mp4"
- Wait until processing is complete
- A new window will open with the result
- You can also watch the output video
- If the detection of the dart is bad you can try selecting a new shape

## Select new shape
The program uses a predefined shape but you can select this yourself if you want to track other objects or if the current shape doesn't work on the video.
To do this follow these steps:
- Run Create_shape.py
- Enter the filename of the video you want to use
- Look at the new window and press q when the contour of the object you want to track is fully seperated from other contours
- Look at the new window and click on the object you want to track
- If done correct the contour of this object will become visible
- Press any button when done selecting
- The selected shape is now saved 

## Example
An example of a bad throw:

https://user-images.githubusercontent.com/70054706/148682331-47a68dac-583a-4c57-a210-ccc140e054e4.mp4

