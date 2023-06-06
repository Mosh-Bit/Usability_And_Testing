import cv2
import mediapipe as mp
import numpy as np
import math
import csv
import time

"""
    Taken from @Norina Grosch
    only a restructured as a class!
"""

class BlinkDetector:
    def __init__(self):
        self.RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.BLINK_RATIO_THRESHOLD = 3.4

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.INITAL_TIME = time.time()

        self.blink_counter = 0
        self.ratio, self.ratio_r, self.ratio_l = 0, 0, 0
        self.file = None
        self.writer = None
        self.start_time = 0
        self.still_closed = False
        self.true_blink = False
        self.blink_len = 0
        self.time_passed = time.time()

    def get_face_orientation(self, results, img):
        img_h, img_w, img_c = img.shape
        face_3d = []
        face_2d = []

        text = 'no_orientation'
        direct = ' '

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        face_2d.append([x, y])

                        face_3d.append([x, y, lm.z])

                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                focal_length = 1 * img_w

                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                rmat, jac = cv2.Rodrigues(rot_vec)

                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                x = angles[0] * 360
                y = angles[1] * 360

                if y < -10:
                    text = "Looking Left"
                    direct = 'l'
                elif y > 10:
                    text = "Looking Right"
                    direct = 'r'
                elif x < -10:
                    text = "Looking Down"
                    direct = 'd'
                else:
                    text = "Forward"
                    direct = 'f'

        return text, direct

    def landmarks_detection(self, img, results, draw=False):
        img_height, img_width = img.shape[:2]
        try:
            mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in
                          results.multi_face_landmarks[0].landmark]

            if draw:
                [cv2.circle(img, p, 2, (0, 255, 0), -1) for p in mesh_coord]

            return mesh_coord
        except:
            print('No mesh')
            return []

    def euclidean_distance(self, point, point1):
        x, y = point
        x1, y1 = point1
        distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
        return distance

    def blink_ratio(self, img, landmarks, right_indices, left_indices):
        rh_right = landmarks[right_indices[0]]
        rh_left = landmarks[right_indices[8]]
        rv_top = landmarks[right_indices[12]]
        rv_bottom = landmarks[right_indices[4]]

        lh_right = landmarks[left_indices[0]]
        lh_left = landmarks[left_indices[8]]
        lv_top = landmarks[left_indices[12]]
        lv_bottom = landmarks[left_indices[4]]

        rhDistance = self.euclidean_distance(rh_right, rh_left)
        rvDistance = self.euclidean_distance(rv_top, rv_bottom)
        lvDistance = self.euclidean_distance(lv_top, lv_bottom)
        lhDistance = self.euclidean_distance(lh_right, lh_left)

        ratio_r = rhDistance / rvDistance
        ratio_l = lhDistance / lvDistance
        ratio = (ratio_r + ratio_l) / 2

        return ratio, ratio_r, ratio_l

    def oriented_ratio(self, ratio, ratio_r, ratio_l, direct_char):
        if direct_char == 'l':
            return ratio_r
        if direct_char == 'r':
            return ratio_l
        else:
            return ratio

    def get_true_blink(self, start):
        end = time.time()
        elapsed = end - start
        true_blink = elapsed > 0.15
        start = time.time()
        return true_blink, start, elapsed

    def run(self):
        cap = cv2.VideoCapture(0)
        self.file = open("test_new.csv", 'w', newline='')
        self.writer = csv.writer(self.file, delimiter=';')
        self.writer.writerow(['time', 'blink', 'ratio', 'ratio_r', 'ratio_l', 'counted', 'orientation',
                              'still_closed', 'blink_length'])
        self.start_time = time.time()

        while cap.isOpened():
            success, image = cap.read()
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.face_mesh.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            direct_text, direct_char = self.get_face_orientation(results, image)
            lm = self.landmarks_detection(image, results)

            if lm == []:
                self.ratio = 0
                self.ratio_r = 0
                self.ratio_l = 0
            else:
                self.ratio, self.ratio_r, self.ratio_l = self.blink_ratio(image, lm, self.RIGHT_EYE, self.LEFT_EYE)

            self.ratio_correct = self.oriented_ratio(self.ratio, self.ratio_r, self.ratio_l, direct_char)

            if self.still_closed:
                self.blink_len += time.time() - self.INITAL_TIME - self.time_passed
            else:
                self.blink_len = time.time() - self.INITAL_TIME - self.time_passed

            self.time_passed = time.time() - self.INITAL_TIME

            if self.ratio_correct > self.BLINK_RATIO_THRESHOLD:
                true_blink, self.start_time, _ = self.get_true_blink(self.start_time)
                if true_blink:
                    self.blink_counter += 1
                    self.still_closed = True
            else:
                self.still_closed = False
                true_blink = False

            try:
                rh_right = lm[self.RIGHT_EYE[0]]
                rh_left = lm[self.RIGHT_EYE[8]]
                rv_top = lm[self.RIGHT_EYE[12]]
                rv_bottom = lm[self.RIGHT_EYE[4]]
                cv2.line(image, rh_right, rh_left, (0, 255, 0), 2)
                cv2.line(image, rv_top, rv_bottom, (0, 255, 0), 2)
            except:
                pass

            self.writer.writerow([self.time_passed, true_blink, self.ratio, self.ratio_r, self.ratio_l,
                                  self.blink_counter, direct_char, self.still_closed, self.blink_len])

            cv2.putText(image, "Blinks: " + str(self.blink_counter), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
            cv2.putText(image, direct_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Blink Detector', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        self.file.close()
        cap.release()

if __name__ == '__main__':
    blink_detector = BlinkDetector()
    blink_detector.run()