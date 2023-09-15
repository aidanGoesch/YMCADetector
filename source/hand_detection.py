import cv2
import mediapipe as mp
import math
import source.face_detection

webcam = cv2.VideoCapture(0)


class HandDetection:
    def __init__(self, show_lm = False):
        self.radius = 0
        self.show_landmarks = show_lm
        self.landmarks = {"center 0": (0, 0), "radius 0": 0, "touching 0": False,
                          "center 1": (0, 0), "radius 1": 0, "touching 1": False}

        self.annotated_image = None

        self.mp_hand_detection = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    def detect(self, image):
        with self.mp_hand_detection.Hands(min_detection_confidence=0.7) as hand_detection:
            # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
            results = hand_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.multi_hand_landmarks:  # if there are no detections then just draw the image
                self.annotated_image = image
                self.landmarks["center 0"] = (-1, -1)
                self.landmarks["center 1"] = (-1, -1)
            else:
                self.annotated_image = image.copy()
                for hand_no, detection in enumerate(results.multi_hand_landmarks):
                    if self.show_landmarks:
                        self.mp_drawing.draw_landmarks(self.annotated_image, detection)

                    image_rows, image_cols, _ = image.shape

                    self.landmarks[f'center {hand_no}'] = (int(detection.landmark[9].x * image_cols), \
                                                        int(detection.landmark[9].y * image_rows))
                    self.landmarks[f'radius {hand_no}'] = calculate_radius(detection, image_rows, image_cols)

                self.average_radius()

    def average_radius(self):
        self.radius = (self.landmarks["radius 0"] + self.landmarks["radius 0"]) // 2

    def draw(self):
        cv2.imshow("WebCam", self.annotated_image)

    def draw_radius(self, image=None):
        if image is not None:
            self.annotated_image = image

        self.annotated_image = cv2.circle(self.annotated_image, self.landmarks["center 0"], radius=self.radius,
                                          color=(0, 255, 0), thickness=1)
        self.annotated_image = cv2.circle(self.annotated_image, self.landmarks["center 1"], radius=self.radius,
                                          color=(0, 255, 0), thickness=1)
        # self.draw()

    def check_touching(self, head: source.face_detection.HeadDetection):
        if distance(head.landmarks["center"], self.landmarks["center 0"]) <= head.radius + self.radius:
            self.landmarks["touching 0"] = True
        else:
            self.landmarks["touching 0"] = False

        if distance(head.landmarks["center"], self.landmarks["center 1"]) <= head.radius + self.radius:
            self.landmarks["touching 1"] = True
        else:
            self.landmarks["touching 1"] = False

    def check_hands_touching(self):
        return distance(self.landmarks["center 0"], self.landmarks["center 1"]) <= 2 * self.radius


def distance(left: tuple, right: tuple):
    return int(math.sqrt(math.pow((left[0] - right[0]), 2) + math.pow((left[1] - right[1]), 2)))


def calculate_radius(detection, image_rows, image_cols):
    left = (int(detection.landmark[4].x * image_cols), int(detection.landmark[4].y * image_rows))
    right = (int(detection.landmark[20].x * image_cols), int(detection.landmark[20].y * image_rows))
    bottom = (int(detection.landmark[0].x * image_cols), int(detection.landmark[0].y * image_rows))

    r1 = int(math.sqrt(math.pow((left[0] - right[0]), 2) + math.pow((left[1] - right[1]), 2)))
    r2 = int(math.sqrt(math.pow((left[0] - bottom[0]), 2) + math.pow((left[1] - bottom[1]), 2)))
    r3 = int(math.sqrt(math.pow((bottom[0] - right[0]), 2) + math.pow((bottom[1] - right[1]), 2)))

    return max(r1, r2, r3)


if __name__ == '__main__':
    h = HandDetection(show_lm=True)

    while True:
        ret, i = webcam.read()
        h.detect(i)
        # h.draw()
        h.draw_radius()
        print(h.landmarks)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break