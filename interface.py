import sys
import csv
import time
import threading
from Blink.blink_detector import BlinkDetector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QRadioButton, QButtonGroup, QMessageBox, QHBoxLayout, QSlider, QStyle, QFileDialog, QSizePolicy, QMainWindow, QSizePolicy, QAction, qApp, QSlider, QInputDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtCore import QTime

""" 
Sources:
    for Video & Audio encodings:
    https://www.codecguide.com/download_k-lite_codec_pack_basic.htm
    Qt5 Tutorials:
    https://wiki.qt.io/How_to_Use_QPushButton
    https://doc.qt.io/qt-5/qvideowidget.html
"""

class VideoPlayer(QWidget):
    def __init__(self, blink):
        super().__init__()
        self.setWindowTitle("Usability & Testing - Video Player")
        self.blink_detector = blink
        # self.setGeometry(100, 100, 800, 600)
        self.showFullScreen()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.positionChanged.connect(self.updatePosition)
        self.mediaPlayer.positionChanged.connect(self.updatePosition)

        self.videoWidget = QVideoWidget()

        self.playButton = QPushButton("Play")
        self.playButton.setCheckable(True)
        self.playButton.setChecked(False)
        self.playButton.toggled.connect(self.playButtonToggled)
        self.playButton.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            QPushButton:checked {
                background-color: #f44336;
            }
            """
        )

        self.nextButton = QPushButton("Next -> Questionnaire")
        self.nextButton.setEnabled(False)#
        self.nextButton.clicked.connect(self.showNextSlide)
        self.nextButton.clicked.connect(self.pauseVideo)
        self.nextButton.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.playButton)
        layout.addWidget(self.nextButton)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.exitShortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.exitShortcut.activated.connect(self.exitFullScreen)
        self.fullScreenShortcut = QShortcut(QKeySequence(Qt.Key_F), self)
        self.fullScreenShortcut.activated.connect(self.makeFullScreen)

        self.nextSlide = None
    
    def openFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Video", "Videos/")
        if file != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.playButton.setEnabled(True)
            self.nextButton.setEnabled(True)

    def playVideo(self):
        self.mediaPlayer.play()

    def pauseVideo(self):
        self.mediaPlayer.pause()

    def playButtonToggled(self, checked):
        if checked:
            self.mediaPlayer.play()
        else:
            self.mediaPlayer.pause()

    def exitFullScreen(self):
        self.showNormal()

    def makeFullScreen(self):
        self.showFullScreen()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setText("Pause")
        else:
            self.playButton.setText("Play")

    def positionChanged(self, position):
        pass

    def durationChanged(self, duration):
        pass
    
    def updatePosition(self, position):
        current_position = position

        time = QTime(0, 0)
        time = time.addMSecs(current_position)

        print("Current Time:", time.toString("hh:mm:ss"))

    def updateDuration(self, duration):
        video_duration = duration

        current_position = player.position()

        frame_counter = (current_position * frame_rate) / 1000

        print("Frame Counter:", frame_counter)

    def killMediaPlayer(self):
        self.mediaPlayer.stop()
        # Clean up and release resources
        self.mediaPlayer.deleteLater()

    def showNextSlide(self):
        self.nextSlide = SlideWidget(self.blink_detector)  # Pass blink_detector instance to the next SlideWidget
        self.nextSlide.showFullScreen()
        self.playButton.setEnabled(False)
        self.nextButton.setEnabled(False)
        self.pauseVideo()
        self.killMediaPlayer()
        self.blink_detector.stop()
        #self.hide()
        self.close()

class SlideWidget(QWidget):
    def __init__(self, blink):
        super().__init__()

        self.blink_detector = blink
        self.setWindowTitle("Slide")
        #self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.showFullScreen
        self.username = "default name"
        self.username, ok = QInputDialog.getText(None, "Enter Username", "Username:")

        # slider answers
        self.sliderValue_q1 = None
        self.sliderValue_q2 = None
        self.sliderValue_q3 = None

        self.question1 = QLabel("Question 1: General interest in the product category")

        self.minimumQ = 0
        self.maximumQ = 10
        self.slider_q1 = QSlider(Qt.Horizontal)
        self.slider_q1.setMinimum(self.minimumQ)
        self.slider_q1.setMaximum(self.maximumQ)
        self.slider_q1.setTickInterval(1)
        self.slider_q1.setTickPosition(QSlider.TicksBelow)
        self.slider_q1.valueChanged.connect(self.updateSlider1Value)
        self.result_label_q1 = QLabel('', self)

        self.slider_q1.setStyleSheet(
            """
            QSlider {
                background-color: #e0e0e0;
                height: 10px;
            }

            QSlider::groove:horizontal {
                background-color: #bdbdbd;
                height: 6px;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                background-color: #4CAF50;
                width: 20px;  /* Adjust handle width to make it bigger */
                margin: -7px 0;  /* Adjust handle margin to center it vertically */
                border-radius: 10px;  /* Adjust border-radius to make it circular */
            }

            QSlider::handle:horizontal:hover {
                background-color: #45a049;
            }

            QSlider::sub-page:horizontal {
                background-color: #4CAF50;
                height: 6px;
                border-radius: 3px;
            }

            QSlider::add-page:horizontal {
                background-color: #bdbdbd;
                height: 6px;
                border-radius: 3px;
            }

            QSlider::sub-page:horizontal:disabled,
            QSlider::add-page:horizontal:disabled {
                background-color: #dcdcdc;
            }

            QSlider::tick-mark:horizontal {
                width: 1px;
                height: 10px;
                background-color: #000000;
            }

            QSlider::tick-position:top,
            QSlider::tick-position:bottom {
                margin-top: -15px;  /* Adjust margin to make room for the tick number labels */
            }

            QSlider::sub-page:horizontal:disabled {
                background-color: #dcdcdc;
            }

            QSlider::handle:horizontal:focus {
                border: 1px solid #4CAF50;
            }
            """
        )

        self.question2 = QLabel("Question 2: Was it interesting to watch?")

        self.slider_q2 = QSlider(Qt.Horizontal)
        self.slider_q2.setMinimum(self.minimumQ)
        self.slider_q2.setMaximum(self.maximumQ)
        self.slider_q2.setTickInterval(1)
        self.slider_q2.setTickPosition(QSlider.TicksBelow)
        self.slider_q2.valueChanged.connect(self.updateSlider2Value)
        self.slider_q2.setStyleSheet(self.slider_q1.styleSheet())
        self.result_label_q2 = QLabel('', self)


        self.question3 = QLabel("Question 3: Positive or Negative Emotion?")

        self.slider_q3 = QSlider(Qt.Horizontal)
        self.slider_q3.setMinimum(self.minimumQ)
        self.slider_q3.setMaximum(self.maximumQ)
        self.slider_q3.setTickInterval(1)
        self.slider_q3.setTickPosition(QSlider.TicksBelow)
        self.slider_q3.valueChanged.connect(self.updateSlider3Value)
        self.slider_q3.setStyleSheet(self.slider_q1.styleSheet())
        self.result_label_q3 = QLabel('', self)

        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.submitAnswers)
        self.submitButton.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: black;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 20px;
                margin: 4px 2px;
                border-radius: 12px;
            }
            """
        )

        self.setLayout(layout)
        layout.addWidget(self.question1)
        layout.addWidget(self.slider_q1)
        layout.addWidget(self.result_label_q1)

        layout.addWidget(self.question2)
        layout.addWidget(self.slider_q2)
        layout.addWidget(self.result_label_q2)

        layout.addWidget(self.question3)
        layout.addWidget(self.slider_q3)
        layout.addWidget(self.result_label_q3)

        layout.addWidget(self.submitButton)

        self.setLayout(layout)

    def submitAnswers(self):
        message_box = None
        data = None

        answer_1 = self.sliderValue_q1
        answer_2 = self.sliderValue_q2
        answer_3 = self.sliderValue_q3

        if (self.sliderValue_q1 is not None) and (self.sliderValue_q2 is not None) and (self.sliderValue_q3 is not None) and (self.username != None):
            print("Selected values:", self.sliderValue_q1, self.sliderValue_q2, self.sliderValue_q3)
            message_box = QMessageBox(QMessageBox.Information, "Submission", f"User & Selected Answers: {self.username, answer_1, answer_2, answer_3}", QMessageBox.Close)
            data = [
                ["Username: ", self.username],
                ["Answer 1: ", answer_1],
                ["Answer 2: ", answer_2],
                ["Answer 3: ", answer_3]
            ]
            message_box.exec_()
        else:
            print("No values selected or no user name!")
        self.openCSV(data)
        self.close()

    def openCSV(self, data):
        csv_file = "test_new.csv"
        self.clearCSV(csv_file)
        if(len(data) == 0):
            QMessageBox.warning(self, "Error", "Something went wrong, data is empty!!")
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)

    def clearCSV(self, csv_file):
        with open(csv_file, mode='w', newline='') as file:
            pass 

    def updateSlider1Value(self, value):
        self.sliderValue_q1 = value
        self.result_label_q1.setText(f'Current Value: {value}')

    def updateSlider2Value(self, value):
        self.sliderValue_q2 = value
        self.result_label_q2.setText(f'Current Value: {value}')

    def updateSlider3Value(self, value):
        self.sliderValue_q3 = value
        self.result_label_q3.setText(f'Current Value: {value}')

def run_video_player(videoPlayer):
    videoPlayer.show()

def run_blink_detector(blinkDetector):
    blinkDetector.run()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    blinkDetector = BlinkDetector()
    videoPlayer = VideoPlayer(blinkDetector)
    videoPlayer.openFile()

    blink_detector_thread = threading.Thread(target=run_blink_detector, args=(blinkDetector,))
    video_player_thread = threading.Thread(target=run_video_player, args=(videoPlayer,))

    videoPlayer.mediaPlayer.stateChanged.connect(lambda state: blinkDetector.stop() if state == QMediaPlayer.StoppedState else None)

    blink_detector_thread.start()
    video_player_thread.start()

    # Wait for the threads to complete or until the video player is closed
    while videoPlayer.isVisible():
        app.processEvents()

    # If the video player is closed, stop the blink detector
    #blinkDetector.stop()

    blink_detector_thread.join()
    video_player_thread.join()

    sys.exit(app.exec_())