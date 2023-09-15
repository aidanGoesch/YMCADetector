# YMCA Detector
This project uses the MediaPipe machine learning library. A specific hand-and-face-recognizing model has been downloaded to lighten the computational load. OpenCV is used to capture each frame from the webcam. Each frame is then passed through the machine learning model to identify the location of the user's head and hands. 

## Instructions to run
1. Clone the repository with `git clone git@github.com:aidanGoesch/YMCADetector.git`

2. Run `cd YMCADetector` to switch into the repository directory

3. Install the external libraries with `pip install -r requirements.txt`

4. To run the script, use the command `python main.py` in the top level of the repository 
