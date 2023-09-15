import cv2
from pygame import mixer
import source.face_detection
import source.hand_detection
from source.letters import Letters


class YMCA:
    def __init__(self, show_lm=False, print_letters=True) -> None:
        mixer.init()
        mixer.music.load('source/Village People - YMCA OFFICIAL Music Video 1978.mp3')

        self.switch = False

        self.head_detector = source.face_detection.HeadDetection(show_lm=show_lm)
        self.hand_detector = source.hand_detection.HandDetection(show_lm=show_lm)

        self.print_letters = print_letters
        self.letters = Letters()

    def detect(self, image):
        self.head_detector.detect(image)

        self.check_letter()

        self.hand_detector.detect(self.head_detector.annotated_image)

    def draw(self):
        self.hand_detector.draw()

    def draw_collision_boxes(self):
        self.head_detector.draw_radius()
        self.hand_detector.draw_radius(image=self.head_detector.annotated_image)
        self.show_instructions(image=self.hand_detector.annotated_image)

    def show_instructions(self, image):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_color = (0, 0, 255)  # White color in BGR
        font_thickness = 1

        # Specify the position where you want to write the text (x, y)
        position = (20, 20)  # Adjust these coordinates as needed

        # Use the putText function to write the text on the image
        cv2.putText(image, "press 'q' to exit program", position, font, font_scale, font_color, font_thickness)
        cv2.imshow("WebCam", image)

    def check_letter(self):
        self._check_y()
        self._check_m()
        self._check_c()
        self._check_a()

        if self.print_letters:
            print(self.letters)

        if len(self.letters) >= 4:
            if self.letters[-4:] == ['Y', 'M', 'C', 'A']:
                if not self.switch:
                    self.switch = True
                    mixer.music.play()

    def _check_y(self):
        hand_center_1 = self.hand_detector.landmarks["center 0"]
        hand_center_2 = self.hand_detector.landmarks["center 1"]
        hand_radius = self.hand_detector.radius

        head_center = self.head_detector.landmarks["center"]
        head_radius = self.head_detector.radius

        # Check if hands are above the head
        if hand_center_1[1] + hand_radius < head_center[1] - (head_radius * .3) and \
                hand_center_2[1] + hand_radius < head_center[1] - (head_radius * .3):
            # Check that one hand is on either side of the head
            left_bound = head_center[0] - head_radius
            right_bound = head_center[0] + head_radius

            if (hand_center_1[0] + hand_radius < left_bound and hand_center_2[0] - hand_radius > right_bound) or \
                    (hand_center_2[0] + hand_radius < left_bound and hand_center_1[0] - hand_radius > right_bound):
                self.letters.add('Y')

    def _check_m(self):
        hand_center_1 = self.hand_detector.landmarks["center 0"]
        hand_center_2 = self.hand_detector.landmarks["center 1"]

        head_center = self.head_detector.landmarks["center"]

        # check that the hands are touching each other and then check if they are touching the head
        self.hand_detector.check_touching(self.head_detector)
        if self.hand_detector.landmarks["touching 0"] and self.hand_detector.landmarks["touching 1"]:
            if hand_center_2[1] < head_center[1] and hand_center_1[1] < head_center[1]:
                self.letters.add('M')

    def _check_c(self):
        hand_center_1 = self.hand_detector.landmarks["center 0"]
        hand_center_2 = self.hand_detector.landmarks["center 1"]

        head_center = self.head_detector.landmarks["center"]
        head_radius = self.head_detector.radius

        if (hand_center_1 != (-1, -1) and hand_center_1 != (-1, -1)):  # check that there are hands on the screen
            if (hand_center_1[0] < head_center[0] - head_radius and hand_center_1[1] > head_center[1] - head_radius and hand_center_2[1] < head_center[1] - head_radius) or \
                    (hand_center_2[0] < head_center[0] - head_radius and hand_center_2[1] > head_center[1] - head_radius and hand_center_1[1] < head_center[1] - head_radius):
                self.letters.add('C')

    def _check_a(self):
        hand_center = self.hand_detector.landmarks["center 1"]
        head_center = self.head_detector.landmarks["center"]
        head_radius = self.head_detector.radius

        left_bound = head_center[0] - head_radius
        right_bound = head_center[0] + head_radius

        if self.hand_detector.check_hands_touching():  # check that the hands are touching
            if hand_center[1] < head_center[1] - 2 * self.head_detector.radius:  # check that the hands are above the head
                if left_bound < hand_center[0] < right_bound:
                    self.letters.add('A')


def main():
    sensor = YMCA(show_lm=True)
    webcam = cv2.VideoCapture(0)

    while True:
        ret, frame = webcam.read()
        sensor.detect(frame)
        sensor.draw_collision_boxes()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            mixer.music.stop()
            break

if __name__ == '__main__':
    main()