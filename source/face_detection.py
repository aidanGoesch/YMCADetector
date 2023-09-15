import cv2
import mediapipe as mp
import math

webcam = cv2.VideoCapture(0)


class HeadDetection:
    def __init__(self, show_lm = False):
        self.radius = 0
        self.show_landmarks = show_lm
        self.landmarks = {"center": (0, 0),
                          "left": (0, 0),
                          "right": (0, 0)}

        self.annotated_image = None

        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    def detect(self, image):
        with self.mp_face_detection.FaceDetection(min_detection_confidence=0.7, model_selection=1) \
                as face_detection:
            # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
            results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.detections:  # if there are no detections then just draw the image
                self.annotated_image = image
            else:
                self.annotated_image = image.copy()

                detection = results.detections[0]

                if self.show_landmarks:
                    self.mp_drawing.draw_detection(self.annotated_image, detection)

                image_rows, image_cols, _ = image.shape

                # calculate the radius (size of head)
                self.landmarks["left"] = (int(detection.location_data.relative_keypoints[4].x * image_cols), \
                               int(detection.location_data.relative_keypoints[4].y * image_rows))
                self.landmarks["right"] = (int(detection.location_data.relative_keypoints[5].x * image_cols), \
                               int(detection.location_data.relative_keypoints[5].y * image_rows))
                self.radius = distance(self.landmarks["left"], self.landmarks["right"])

                self.landmarks["center"] = (int(detection.location_data.relative_keypoints[2].x * image_cols), \
                                            int(detection.location_data.relative_keypoints[2].y * image_rows - 0.4 * self.radius))

    def draw(self):
        cv2.imshow("WebCam", self.annotated_image)

    def draw_radius(self):
        self.annotated_image = cv2.circle(self.annotated_image, self.landmarks["center"], radius=self.radius,
                                          color=(0, 255, 0), thickness=1)
        # self.draw()

    def print(self):
        print("radius: ", self.radius, "   center: ", self.landmarks['center'])




def distance(left: tuple, right: tuple):
    return int(math.sqrt(math.pow((left[0] - right[0]), 2) + math.pow((left[1] - right[1]), 2)))

cv2.destroyAllWindows()

if __name__ == '__main__':
    # h = HeadDetection()
    # h.detect(cv2.imread("tom-cruise.png"))
    # h.draw()

    h = HeadDetection(show_lm=True)
    while True:
        ret, i = webcam.read()
        h.detect(i)
        h.draw()
        # h.draw_radius()
        h.print()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
