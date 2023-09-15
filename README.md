# YMCA Detector
This project uses the MediaPipe machine learning library. A specific hand-and-face-recognizing model has been downloaded to lighten the computational load. OpenCV is used to capture each frame from the webcam. Each frame is then passed through the machine learning model to identify the location of the user's head and hands. 

## Instructions to Run 
1. Clone the repository with `git clone git@github.com:aidanGoesch/YMCADetector.git`

2. Run `cd YMCADetector` to switch into the repository directory

3. Install the external libraries with `pip install -r requirements.txt`

4. To run the script, use the command `python main.py` in the top level of the repository 


## Tips for Use
While the machine learning model is good, it is not perfect. Try to use the program in a well-lit environment, where the background is a distinctly different color than your skin tone. Lastly, for the best results possible, face your palms towards the webcam and spread your fingers; this makes it easier for the machine learning model to identify your hands.
